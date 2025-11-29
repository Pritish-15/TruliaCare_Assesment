from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from database import get_db
from models import Vendor, Admin, VendorStatus
from schemas import VendorResponse, UpdateVendorStatus, AdminLogin, Token
from auth import authenticate_admin, create_access_token, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
import os

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# 1. Admin Login
@router.post("/login", response_model=Token)
async def admin_login(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """Admin login endpoint"""
    
    admin = authenticate_admin(db, login_data.username, login_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# 2. Get All Vendors
@router.get("/vendors", response_model=List[VendorResponse])
async def get_all_vendors(
    status_filter: VendorStatus = None,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get all vendors (with optional status filter)"""
    
    query = db.query(Vendor)
    
    if status_filter:
        query = query.filter(Vendor.status == status_filter)
    
    vendors = query.order_by(Vendor.created_at.desc()).all()
    return vendors

# 3. Get Single Vendor Details
@router.get("/vendors/{vendor_id}", response_model=VendorResponse)
async def get_vendor_by_id(
    vendor_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get vendor details by ID"""
    
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    return vendor

# 4. Update Vendor Status (Approve/Reject)
@router.put("/vendors/{vendor_id}/status", response_model=VendorResponse)
async def update_vendor_status(
    vendor_id: str,
    status_update: UpdateVendorStatus,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update vendor status (approve or reject)"""
    
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Update status
    vendor.status = status_update.status
    
    # If rejected, store reason
    if status_update.status == VendorStatus.REJECTED:
        if not status_update.rejection_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rejection reason is required when rejecting a vendor"
            )
        vendor.rejection_reason = status_update.rejection_reason
    else:
        vendor.rejection_reason = None
    
    try:
        db.commit()
        db.refresh(vendor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update vendor status: {str(e)}"
        )
    
    return vendor

# 5. Download Vendor Document
@router.get("/vendors/{vendor_id}/documents/{doc_type}")
async def download_document(
    vendor_id: str,
    doc_type: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Download vendor KYC document by type"""
    
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Map document types to vendor attributes
    doc_mapping = {
        # Identity Proof Documents
        "aadhaar": vendor.aadhaar_document,
        "pan": vendor.pan_document,
        "passport": vendor.passport_document,
        "voter_id": vendor.voter_id_document,
        "driving_license": vendor.driving_license_document,
        # Address Proof Documents
        "address_proof_aadhaar": vendor.address_proof_aadhaar,
        "address_proof_passport": vendor.address_proof_passport,
        "address_proof_voter_id": vendor.address_proof_voter_id,
        "address_proof_driving_license": vendor.address_proof_driving_license,
        "address_proof_electricity_bill": vendor.address_proof_electricity_bill,
        "address_proof_water_gas_bill": vendor.address_proof_water_gas_bill,
        "address_proof_bank_statement": vendor.address_proof_bank_statement,
        # Photograph
        "passport_photo": vendor.passport_photo,
        "live_selfie": vendor.live_selfie,
        # Business Documents
        "gst_certificate": vendor.gst_certificate,
        "partnership_deed": vendor.partnership_deed,
        "certificate_of_incorporation": vendor.certificate_of_incorporation,
        "memorandum_articles": vendor.memorandum_articles,
        "shop_establishment_certificate": vendor.shop_establishment_certificate,
        # Additional Documents
        "college_id_document": vendor.college_id_document,
        "local_address_proof": vendor.local_address_proof,
        "guardians_kyc_documents": vendor.guardians_kyc_documents,
        "birth_certificate_document": vendor.birth_certificate_document,
        "visa_document": vendor.visa_document,
        "oci_card_document": vendor.oci_card_document,
        "overseas_address_proof": vendor.overseas_address_proof,
        "fatca_declaration_document": vendor.fatca_declaration_document,
    }
    
    file_path = doc_mapping.get(doc_type)
    
    if file_path is None:
        valid_types = ", ".join(doc_mapping.keys())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type. Valid types: {valid_types}"
        )
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{doc_type.replace('_', ' ').title()} document not found"
        )
    
    return FileResponse(file_path)

# 6. Get Dashboard Statistics
@router.get("/dashboard/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get dashboard statistics"""
    
    total_vendors = db.query(Vendor).count()
    pending_vendors = db.query(Vendor).filter(Vendor.status == VendorStatus.PENDING).count()
    approved_vendors = db.query(Vendor).filter(Vendor.status == VendorStatus.APPROVED).count()
    rejected_vendors = db.query(Vendor).filter(Vendor.status == VendorStatus.REJECTED).count()
    
    return {
        "total_vendors": total_vendors,
        "pending": pending_vendors,
        "approved": approved_vendors,
        "rejected": rejected_vendors
    }