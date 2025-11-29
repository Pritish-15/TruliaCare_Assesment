from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Vendor, VendorStatus
from schemas import VendorCreate, VendorResponse, StatusCheckRequest, StatusCheckResponse
from utils import generate_vendor_id, save_upload_file, delete_file

router = APIRouter(prefix="/api/vendor", tags=["Vendor"])

# 1. Register Vendor (Complete KYC Information)
@router.post("/register", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def register_vendor(
    # Personal Information
    name: str = Form(...),  # Full Name as per ID proof
    age: int = Form(...),
    gender: Optional[str] = Form(None),
    date_of_birth: str = Form(...),  # Made required
    fathers_name: Optional[str] = Form(None),
    mothers_name: Optional[str] = Form(None),
    marital_status: Optional[str] = Form(None),
    nationality: Optional[str] = Form("Indian"),
    
    # Contact Information
    email: str = Form(...),
    phone: str = Form(...),  # Mobile linked to Aadhaar for OTP
    alternate_phone: Optional[str] = Form(None),
    aadhaar_linked_mobile: Optional[str] = Form(None),
    
    # Address Information
    current_address: str = Form(...),  # Current Residential Address
    current_city: Optional[str] = Form(None),
    current_state: Optional[str] = Form(None),
    current_pincode: Optional[str] = Form(None),
    permanent_address: Optional[str] = Form(None),
    permanent_city: Optional[str] = Form(None),
    permanent_state: Optional[str] = Form(None),
    permanent_pincode: Optional[str] = Form(None),
    country: Optional[str] = Form("India"),
    
    # Identity Details
    pan_number: Optional[str] = Form(None),
    aadhaar_number: Optional[str] = Form(None),
    passport_number: Optional[str] = Form(None),
    voter_id: Optional[str] = Form(None),
    driving_license: Optional[str] = Form(None),
    
    # Business Information (Optional)
    business_name: Optional[str] = Form(None),
    business_type: Optional[str] = Form(None),
    business_category: Optional[str] = Form(None),
    gst_number: Optional[str] = Form(None),
    
    # Additional Information - For Students
    is_student: Optional[str] = Form(None),
    college_id: Optional[str] = Form(None),
    student_local_address: Optional[str] = Form(None),
    
    # Additional Information - For Working Professionals
    occupation: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    annual_income: Optional[str] = Form(None),
    source_of_funds: Optional[str] = Form(None),
    
    # Additional Information - For Minors
    is_minor: Optional[str] = Form(None),
    guardians_name: Optional[str] = Form(None),
    guardians_pan: Optional[str] = Form(None),
    guardians_aadhaar: Optional[str] = Form(None),
    birth_certificate_number: Optional[str] = Form(None),
    
    # Additional Information - For NRI/OCI
    is_nri_oci: Optional[str] = Form(None),
    visa_number: Optional[str] = Form(None),
    oci_card_number: Optional[str] = Form(None),
    overseas_address: Optional[str] = Form(None),
    fatca_declaration: Optional[str] = Form(None),
    
    # Bank Details
    bank_name: Optional[str] = Form(None),
    account_number: Optional[str] = Form(None),
    ifsc_code: Optional[str] = Form(None),
    
    # Additional Notes
    notes: Optional[str] = Form(None),
    
    db: Session = Depends(get_db)
):
    """Register a new vendor with complete KYC information"""
    
    # Check if email already exists
    existing_vendor = db.query(Vendor).filter(Vendor.email == email).first()
    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate age
    if age <= 0 or age > 150:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid age. Age must be between 1 and 150"
        )
    
    # Generate unique sequential vendor ID
    try:
        vendor_id = generate_vendor_id(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate vendor ID: {str(e)}"
        )
    
    # Create new vendor with all KYC fields
    new_vendor = Vendor(
        vendor_id=vendor_id,
        # Personal Information
        name=name,
        age=age,
        gender=gender,
        date_of_birth=date_of_birth,
        fathers_name=fathers_name,
        mothers_name=mothers_name,
        marital_status=marital_status,
        nationality=nationality,
        # Contact Information
        email=email,
        phone=phone,
        alternate_phone=alternate_phone,
        aadhaar_linked_mobile=aadhaar_linked_mobile,
        # Address Information
        current_address=current_address,
        current_city=current_city,
        current_state=current_state,
        current_pincode=current_pincode,
        permanent_address=permanent_address,
        permanent_city=permanent_city,
        permanent_state=permanent_state,
        permanent_pincode=permanent_pincode,
        country=country,
        # Identity Details
        pan_number=pan_number,
        aadhaar_number=aadhaar_number,
        passport_number=passport_number,
        voter_id=voter_id,
        driving_license=driving_license,
        # Business Information
        business_name=business_name,
        business_type=business_type,
        business_category=business_category,
        gst_number=gst_number,
        # Additional Information - Students
        is_student=is_student,
        college_id=college_id,
        student_local_address=student_local_address,
        # Additional Information - Professionals
        occupation=occupation,
        company_name=company_name,
        annual_income=annual_income,
        source_of_funds=source_of_funds,
        # Additional Information - Minors
        is_minor=is_minor,
        guardians_name=guardians_name,
        guardians_pan=guardians_pan,
        guardians_aadhaar=guardians_aadhaar,
        birth_certificate_number=birth_certificate_number,
        # Additional Information - NRI/OCI
        is_nri_oci=is_nri_oci,
        visa_number=visa_number,
        oci_card_number=oci_card_number,
        overseas_address=overseas_address,
        fatca_declaration=fatca_declaration,
        # Bank Details
        bank_name=bank_name,
        account_number=account_number,
        ifsc_code=ifsc_code,
        # Additional
        notes=notes,
        status=VendorStatus.PENDING
    )
    
    try:
        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create vendor: {str(e)}"
        )
    
    return new_vendor

# 2. Upload KYC Documents
@router.post("/upload-documents/{vendor_id}", response_model=VendorResponse)
async def upload_documents(
    vendor_id: str,
    # Identity Proof Documents (Any 1 required)
    aadhaar_document: Optional[UploadFile] = File(None),
    pan_document: Optional[UploadFile] = File(None),
    passport_document: Optional[UploadFile] = File(None),
    voter_id_document: Optional[UploadFile] = File(None),
    driving_license_document: Optional[UploadFile] = File(None),
    
    # Address Proof Documents (Any 1 required)
    address_proof_aadhaar: Optional[UploadFile] = File(None),
    address_proof_passport: Optional[UploadFile] = File(None),
    address_proof_voter_id: Optional[UploadFile] = File(None),
    address_proof_driving_license: Optional[UploadFile] = File(None),
    address_proof_electricity_bill: Optional[UploadFile] = File(None),
    address_proof_water_gas_bill: Optional[UploadFile] = File(None),
    address_proof_bank_statement: Optional[UploadFile] = File(None),
    
    # Photograph
    passport_photo: Optional[UploadFile] = File(None),
    live_selfie: Optional[UploadFile] = File(None),
    
    # Business Documents (if applicable)
    gst_certificate: Optional[UploadFile] = File(None),
    partnership_deed: Optional[UploadFile] = File(None),
    certificate_of_incorporation: Optional[UploadFile] = File(None),
    memorandum_articles: Optional[UploadFile] = File(None),
    shop_establishment_certificate: Optional[UploadFile] = File(None),
    
    # Additional Documents
    college_id_document: Optional[UploadFile] = File(None),  # For students
    local_address_proof: Optional[UploadFile] = File(None),  # For students
    guardians_kyc_documents: Optional[UploadFile] = File(None),  # For minors
    birth_certificate_document: Optional[UploadFile] = File(None),  # For minors
    visa_document: Optional[UploadFile] = File(None),  # For NRI/OCI
    oci_card_document: Optional[UploadFile] = File(None),  # For NRI/OCI
    overseas_address_proof: Optional[UploadFile] = File(None),  # For NRI/OCI
    fatca_declaration_document: Optional[UploadFile] = File(None),  # For NRI/OCI
    
    db: Session = Depends(get_db)
):
    """Upload KYC documents for a vendor"""
    
    # Find vendor
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Save documents
    try:
        # Identity Proof Documents (Only ONE allowed - clear others when one is uploaded)
        identity_proof_uploaded = False
        if aadhaar_document:
            # Clear all other identity proof documents and delete their files
            delete_file(vendor.pan_document)
            delete_file(vendor.passport_document)
            delete_file(vendor.voter_id_document)
            delete_file(vendor.driving_license_document)
            vendor.pan_document = None
            vendor.passport_document = None
            vendor.voter_id_document = None
            vendor.driving_license_document = None
            vendor.aadhaar_document = await save_upload_file(aadhaar_document, vendor_id, "aadhaar")
            identity_proof_uploaded = True
        elif pan_document:
            # Clear all other identity proof documents and delete their files
            delete_file(vendor.aadhaar_document)
            delete_file(vendor.passport_document)
            delete_file(vendor.voter_id_document)
            delete_file(vendor.driving_license_document)
            vendor.aadhaar_document = None
            vendor.passport_document = None
            vendor.voter_id_document = None
            vendor.driving_license_document = None
            vendor.pan_document = await save_upload_file(pan_document, vendor_id, "pan")
            identity_proof_uploaded = True
        elif passport_document:
            # Clear all other identity proof documents and delete their files
            delete_file(vendor.aadhaar_document)
            delete_file(vendor.pan_document)
            delete_file(vendor.voter_id_document)
            delete_file(vendor.driving_license_document)
            vendor.aadhaar_document = None
            vendor.pan_document = None
            vendor.voter_id_document = None
            vendor.driving_license_document = None
            vendor.passport_document = await save_upload_file(passport_document, vendor_id, "passport")
            identity_proof_uploaded = True
        elif voter_id_document:
            # Clear all other identity proof documents and delete their files
            delete_file(vendor.aadhaar_document)
            delete_file(vendor.pan_document)
            delete_file(vendor.passport_document)
            delete_file(vendor.driving_license_document)
            vendor.aadhaar_document = None
            vendor.pan_document = None
            vendor.passport_document = None
            vendor.driving_license_document = None
            vendor.voter_id_document = await save_upload_file(voter_id_document, vendor_id, "voter_id")
            identity_proof_uploaded = True
        elif driving_license_document:
            # Clear all other identity proof documents and delete their files
            delete_file(vendor.aadhaar_document)
            delete_file(vendor.pan_document)
            delete_file(vendor.passport_document)
            delete_file(vendor.voter_id_document)
            vendor.aadhaar_document = None
            vendor.pan_document = None
            vendor.passport_document = None
            vendor.voter_id_document = None
            vendor.driving_license_document = await save_upload_file(driving_license_document, vendor_id, "driving_license")
            identity_proof_uploaded = True
        
        # Address Proof Documents (Only ONE allowed - clear others when one is uploaded)
        address_proof_uploaded = False
        if address_proof_aadhaar:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_water_gas_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_passport = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_aadhaar = await save_upload_file(address_proof_aadhaar, vendor_id, "address_proof_aadhaar")
            address_proof_uploaded = True
        elif address_proof_passport:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_water_gas_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_passport = await save_upload_file(address_proof_passport, vendor_id, "address_proof_passport")
            address_proof_uploaded = True
        elif address_proof_voter_id:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_water_gas_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_passport = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_voter_id = await save_upload_file(address_proof_voter_id, vendor_id, "address_proof_voter_id")
            address_proof_uploaded = True
        elif address_proof_driving_license:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_water_gas_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_passport = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_driving_license = await save_upload_file(address_proof_driving_license, vendor_id, "address_proof_driving_license")
            address_proof_uploaded = True
        elif address_proof_electricity_bill:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_water_gas_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_passport = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_electricity_bill = await save_upload_file(address_proof_electricity_bill, vendor_id, "address_proof_electricity_bill")
            address_proof_uploaded = True
        elif address_proof_water_gas_bill:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_bank_statement)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_passport = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_bank_statement = None
            vendor.address_proof_water_gas_bill = await save_upload_file(address_proof_water_gas_bill, vendor_id, "address_proof_water_gas_bill")
            address_proof_uploaded = True
        elif address_proof_bank_statement:
            # Clear all other address proof documents and delete their files
            delete_file(vendor.address_proof_aadhaar)
            delete_file(vendor.address_proof_passport)
            delete_file(vendor.address_proof_voter_id)
            delete_file(vendor.address_proof_driving_license)
            delete_file(vendor.address_proof_electricity_bill)
            delete_file(vendor.address_proof_water_gas_bill)
            vendor.address_proof_aadhaar = None
            vendor.address_proof_passport = None
            vendor.address_proof_voter_id = None
            vendor.address_proof_driving_license = None
            vendor.address_proof_electricity_bill = None
            vendor.address_proof_water_gas_bill = None
            vendor.address_proof_bank_statement = await save_upload_file(address_proof_bank_statement, vendor_id, "address_proof_bank_statement")
            address_proof_uploaded = True
        
        # Photograph
        if passport_photo:
            vendor.passport_photo = await save_upload_file(passport_photo, vendor_id, "passport_photo")
        if live_selfie:
            vendor.live_selfie = await save_upload_file(live_selfie, vendor_id, "live_selfie")
        
        # Business Documents
        if gst_certificate:
            vendor.gst_certificate = await save_upload_file(gst_certificate, vendor_id, "gst_certificate")
        if partnership_deed:
            vendor.partnership_deed = await save_upload_file(partnership_deed, vendor_id, "partnership_deed")
        if certificate_of_incorporation:
            vendor.certificate_of_incorporation = await save_upload_file(certificate_of_incorporation, vendor_id, "certificate_of_incorporation")
        if memorandum_articles:
            vendor.memorandum_articles = await save_upload_file(memorandum_articles, vendor_id, "memorandum_articles")
        if shop_establishment_certificate:
            vendor.shop_establishment_certificate = await save_upload_file(shop_establishment_certificate, vendor_id, "shop_establishment_certificate")
        
        # Additional Documents
        if college_id_document:
            vendor.college_id_document = await save_upload_file(college_id_document, vendor_id, "college_id_document")
        if local_address_proof:
            vendor.local_address_proof = await save_upload_file(local_address_proof, vendor_id, "local_address_proof")
        if guardians_kyc_documents:
            vendor.guardians_kyc_documents = await save_upload_file(guardians_kyc_documents, vendor_id, "guardians_kyc_documents")
        if birth_certificate_document:
            vendor.birth_certificate_document = await save_upload_file(birth_certificate_document, vendor_id, "birth_certificate_document")
        if visa_document:
            vendor.visa_document = await save_upload_file(visa_document, vendor_id, "visa_document")
        if oci_card_document:
            vendor.oci_card_document = await save_upload_file(oci_card_document, vendor_id, "oci_card_document")
        if overseas_address_proof:
            vendor.overseas_address_proof = await save_upload_file(overseas_address_proof, vendor_id, "overseas_address_proof")
        if fatca_declaration_document:
            vendor.fatca_declaration_document = await save_upload_file(fatca_declaration_document, vendor_id, "fatca_declaration_document")
        
        db.commit()
        db.refresh(vendor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload documents: {str(e)}"
        )
    
    return vendor

# 3. Check Status by Vendor ID
@router.post("/check-status", response_model=StatusCheckResponse)
async def check_status(
    request: StatusCheckRequest,
    db: Session = Depends(get_db)
):
    """Check vendor application status"""
    
    vendor = db.query(Vendor).filter(Vendor.vendor_id == request.vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor ID not found"
        )
    
    return StatusCheckResponse(
        vendor_id=vendor.vendor_id,
        name=vendor.name,
        business_name=vendor.business_name or "N/A",
        status=vendor.status,
        rejection_reason=vendor.rejection_reason,
        created_at=vendor.created_at
    )

# 4. Get Vendor Details by ID (for vendor to view their own info)
@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor_details(
    vendor_id: str,
    db: Session = Depends(get_db)
):
    """Get vendor details by vendor ID"""
    
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    return vendor