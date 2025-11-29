from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from database import Base
import enum

# Enum for vendor status
class VendorStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# Vendor Model
class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(String, unique=True, index=True, nullable=False)
    
    # Personal Information
    name = Column(String, nullable=False)  # Full Name as per ID proof
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=False)  # Made required
    fathers_name = Column(String, nullable=True)
    mothers_name = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)  # Single, Married, Divorced, etc.
    nationality = Column(String, default="Indian", nullable=True)
    
    # Contact Information
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)  # Mobile linked to Aadhaar for OTP
    alternate_phone = Column(String, nullable=True)
    aadhaar_linked_mobile = Column(String, nullable=True)  # Aadhaar-linked mobile for OTP
    
    # Address Information
    current_address = Column(String, nullable=False)  # Current Residential Address
    current_city = Column(String, nullable=True)
    current_state = Column(String, nullable=True)
    current_pincode = Column(String, nullable=True)
    permanent_address = Column(String, nullable=True)  # Permanent Address (if different)
    permanent_city = Column(String, nullable=True)
    permanent_state = Column(String, nullable=True)
    permanent_pincode = Column(String, nullable=True)
    country = Column(String, default="India")
    
    # Identity Details
    pan_number = Column(String, nullable=True)
    aadhaar_number = Column(String, nullable=True)  # Aadhaar Number for e-KYC
    passport_number = Column(String, nullable=True)
    voter_id = Column(String, nullable=True)
    driving_license = Column(String, nullable=True)
    
    # Business Information (Optional - for business KYC)
    business_name = Column(String, nullable=True)  # Made optional
    business_type = Column(String, nullable=True)  # e.g., Sole Proprietor, Partnership, Company
    business_category = Column(String, nullable=True)  # e.g., Manufacturing, Trading, Services
    gst_number = Column(String, nullable=True)
    
    # Additional Information - For Students
    is_student = Column(String, nullable=True)  # Yes/No
    college_id = Column(String, nullable=True)
    student_local_address = Column(String, nullable=True)  # Hostel/rent agreement
    
    # Additional Information - For Working Professionals
    occupation = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    annual_income = Column(String, nullable=True)  # Income bracket
    source_of_funds = Column(String, nullable=True)
    
    # Additional Information - For Minors
    is_minor = Column(String, nullable=True)  # Yes/No
    guardians_name = Column(String, nullable=True)
    guardians_pan = Column(String, nullable=True)
    guardians_aadhaar = Column(String, nullable=True)
    birth_certificate_number = Column(String, nullable=True)
    
    # Additional Information - For NRI/OCI
    is_nri_oci = Column(String, nullable=True)  # Yes/No
    visa_number = Column(String, nullable=True)
    oci_card_number = Column(String, nullable=True)
    overseas_address = Column(String, nullable=True)
    fatca_declaration = Column(String, nullable=True)  # Yes/No
    
    # Bank Details (Optional)
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    
    # KYC Documents - Identity Proof (Any 1 required)
    aadhaar_document = Column(String, nullable=True)  # File path
    pan_document = Column(String, nullable=True)  # File path
    passport_document = Column(String, nullable=True)  # File path
    voter_id_document = Column(String, nullable=True)  # File path
    driving_license_document = Column(String, nullable=True)  # File path
    
    # KYC Documents - Address Proof (Any 1 required)
    address_proof_aadhaar = Column(String, nullable=True)
    address_proof_passport = Column(String, nullable=True)
    address_proof_voter_id = Column(String, nullable=True)
    address_proof_driving_license = Column(String, nullable=True)
    address_proof_electricity_bill = Column(String, nullable=True)
    address_proof_water_gas_bill = Column(String, nullable=True)
    address_proof_bank_statement = Column(String, nullable=True)
    
    # KYC Documents - Photograph
    passport_photo = Column(String, nullable=True)  # Passport-size photo
    live_selfie = Column(String, nullable=True)  # Live selfie for online KYC
    
    # KYC Documents - Business (if applicable)
    gst_certificate = Column(String, nullable=True)
    partnership_deed = Column(String, nullable=True)
    certificate_of_incorporation = Column(String, nullable=True)
    memorandum_articles = Column(String, nullable=True)
    shop_establishment_certificate = Column(String, nullable=True)
    
    # KYC Documents - Additional
    college_id_document = Column(String, nullable=True)  # For students
    local_address_proof = Column(String, nullable=True)  # For students (hostel/rent)
    guardians_kyc_documents = Column(String, nullable=True)  # For minors
    birth_certificate_document = Column(String, nullable=True)  # For minors
    visa_document = Column(String, nullable=True)  # For NRI/OCI
    oci_card_document = Column(String, nullable=True)  # For NRI/OCI
    overseas_address_proof = Column(String, nullable=True)  # For NRI/OCI
    fatca_declaration_document = Column(String, nullable=True)  # For NRI/OCI
    
    # Status
    status = Column(SQLEnum(VendorStatus), default=VendorStatus.PENDING)
    rejection_reason = Column(String, nullable=True)
    
    # Additional Notes
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Admin Model (simple username/password for admin login)
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())