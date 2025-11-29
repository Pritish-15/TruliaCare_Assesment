from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import VendorStatus

# Vendor Registration Schema
class VendorCreate(BaseModel):
    # Personal Information
    name: str  # Full Name as per ID proof
    age: int
    gender: Optional[str] = None
    date_of_birth: str  # Made required
    fathers_name: Optional[str] = None
    mothers_name: Optional[str] = None
    marital_status: Optional[str] = None  # Single, Married, Divorced, etc.
    nationality: Optional[str] = "Indian"
    
    # Contact Information
    email: EmailStr
    phone: str  # Mobile linked to Aadhaar for OTP
    alternate_phone: Optional[str] = None
    aadhaar_linked_mobile: Optional[str] = None  # Aadhaar-linked mobile for OTP
    
    # Address Information
    current_address: str  # Current Residential Address
    current_city: Optional[str] = None
    current_state: Optional[str] = None
    current_pincode: Optional[str] = None
    permanent_address: Optional[str] = None  # Permanent Address (if different)
    permanent_city: Optional[str] = None
    permanent_state: Optional[str] = None
    permanent_pincode: Optional[str] = None
    country: Optional[str] = "India"
    
    # Identity Details
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None  # Aadhaar Number for e-KYC
    passport_number: Optional[str] = None
    voter_id: Optional[str] = None
    driving_license: Optional[str] = None
    
    # Business Information (Optional - for business KYC)
    business_name: Optional[str] = None  # Made optional
    business_type: Optional[str] = None
    business_category: Optional[str] = None
    gst_number: Optional[str] = None
    
    # Additional Information - For Students
    is_student: Optional[str] = None  # Yes/No
    college_id: Optional[str] = None
    student_local_address: Optional[str] = None
    
    # Additional Information - For Working Professionals
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    annual_income: Optional[str] = None
    source_of_funds: Optional[str] = None
    
    # Additional Information - For Minors
    is_minor: Optional[str] = None  # Yes/No
    guardians_name: Optional[str] = None
    guardians_pan: Optional[str] = None
    guardians_aadhaar: Optional[str] = None
    birth_certificate_number: Optional[str] = None
    
    # Additional Information - For NRI/OCI
    is_nri_oci: Optional[str] = None  # Yes/No
    visa_number: Optional[str] = None
    oci_card_number: Optional[str] = None
    overseas_address: Optional[str] = None
    fatca_declaration: Optional[str] = None  # Yes/No
    
    # Bank Details
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    
    # Additional Notes
    notes: Optional[str] = None

# Vendor Response Schema
class VendorResponse(BaseModel):
    id: int
    vendor_id: str
    
    # Personal Information
    name: str
    age: int
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    fathers_name: Optional[str] = None
    mothers_name: Optional[str] = None
    marital_status: Optional[str] = None
    nationality: Optional[str] = None
    
    # Contact Information
    email: str
    phone: str
    alternate_phone: Optional[str] = None
    aadhaar_linked_mobile: Optional[str] = None
    
    # Address Information
    current_address: Optional[str] = None
    current_city: Optional[str] = None
    current_state: Optional[str] = None
    current_pincode: Optional[str] = None
    permanent_address: Optional[str] = None
    permanent_city: Optional[str] = None
    permanent_state: Optional[str] = None
    permanent_pincode: Optional[str] = None
    country: Optional[str] = None
    
    # Identity Details
    pan_number: Optional[str] = None
    aadhaar_number: Optional[str] = None
    passport_number: Optional[str] = None
    voter_id: Optional[str] = None
    driving_license: Optional[str] = None
    
    # Business Information
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    business_category: Optional[str] = None
    gst_number: Optional[str] = None
    
    # Additional Information - For Students
    is_student: Optional[str] = None
    college_id: Optional[str] = None
    student_local_address: Optional[str] = None
    
    # Additional Information - For Working Professionals
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    annual_income: Optional[str] = None
    source_of_funds: Optional[str] = None
    
    # Additional Information - For Minors
    is_minor: Optional[str] = None
    guardians_name: Optional[str] = None
    guardians_pan: Optional[str] = None
    guardians_aadhaar: Optional[str] = None
    birth_certificate_number: Optional[str] = None
    
    # Additional Information - For NRI/OCI
    is_nri_oci: Optional[str] = None
    visa_number: Optional[str] = None
    oci_card_number: Optional[str] = None
    overseas_address: Optional[str] = None
    fatca_declaration: Optional[str] = None
    
    # Bank Details
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    
    # Status & Documents - Identity Proof
    aadhaar_document: Optional[str] = None
    pan_document: Optional[str] = None
    passport_document: Optional[str] = None
    voter_id_document: Optional[str] = None
    driving_license_document: Optional[str] = None
    
    # Status & Documents - Address Proof
    address_proof_aadhaar: Optional[str] = None
    address_proof_passport: Optional[str] = None
    address_proof_voter_id: Optional[str] = None
    address_proof_driving_license: Optional[str] = None
    address_proof_electricity_bill: Optional[str] = None
    address_proof_water_gas_bill: Optional[str] = None
    address_proof_bank_statement: Optional[str] = None
    
    # Status & Documents - Photograph
    passport_photo: Optional[str] = None
    live_selfie: Optional[str] = None
    
    # Status & Documents - Business
    gst_certificate: Optional[str] = None
    partnership_deed: Optional[str] = None
    certificate_of_incorporation: Optional[str] = None
    memorandum_articles: Optional[str] = None
    shop_establishment_certificate: Optional[str] = None
    
    # Status & Documents - Additional
    college_id_document: Optional[str] = None
    local_address_proof: Optional[str] = None
    guardians_kyc_documents: Optional[str] = None
    birth_certificate_document: Optional[str] = None
    visa_document: Optional[str] = None
    oci_card_document: Optional[str] = None
    overseas_address_proof: Optional[str] = None
    fatca_declaration_document: Optional[str] = None
    
    # Status
    status: VendorStatus
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Status Check Schema
class StatusCheckRequest(BaseModel):
    vendor_id: str

class StatusCheckResponse(BaseModel):
    vendor_id: str
    name: str
    business_name: str
    status: VendorStatus
    rejection_reason: Optional[str] = None
    created_at: datetime

# Admin Update Vendor Status Schema
class UpdateVendorStatus(BaseModel):
    status: VendorStatus
    rejection_reason: Optional[str] = None

# Admin Login Schema
class AdminLogin(BaseModel):
    username: str
    password: str

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str