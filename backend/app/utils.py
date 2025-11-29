import os
from fastapi import UploadFile
from typing import Optional

# Create uploads directory if it doesn't exist
# Use absolute path to ensure it works regardless of where the app is run from
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Generate unique sequential vendor ID
def generate_vendor_id(db_session) -> str:
    """
    Generate sequential vendor ID (VEN000001, VEN000002, etc.)
    Requires database session to check existing IDs
    """
    from models import Vendor
    
    # Get all existing vendor IDs
    all_vendors = db_session.query(Vendor.vendor_id).all()
    
    max_number = 0
    for (vendor_id,) in all_vendors:
        if vendor_id and vendor_id.startswith("VEN"):
            try:
                # Extract number from vendor_id (e.g., "VEN000123" -> 123)
                number_str = vendor_id.replace("VEN", "").lstrip("0") or "0"
                number = int(number_str)
                if number > max_number:
                    max_number = number
            except (ValueError, AttributeError):
                # Skip invalid IDs (old random format)
                continue
    
    # Next number is max + 1
    next_number = max_number + 1
    
    # Format as VEN000001, VEN000002, etc. (with zero padding to 6 digits)
    vendor_id = f"VEN{next_number:06d}"
    
    # Final uniqueness check (safety)
    existing = db_session.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if existing:
        # If collision, increment and try again
        next_number += 1
        vendor_id = f"VEN{next_number:06d}"
    
    return vendor_id

# Save uploaded file
async def save_upload_file(file: UploadFile, vendor_id: str, doc_type: str) -> str:
    """
    Save uploaded file and return the file path
    doc_type: 'pan', 'gst', or 'certificate'
    """
    # Create vendor-specific folder
    vendor_folder = os.path.join(UPLOAD_DIR, vendor_id)
    os.makedirs(vendor_folder, exist_ok=True)
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1]
    
    # Create unique filename
    filename = f"{doc_type}{file_extension}"
    file_path = os.path.join(vendor_folder, filename)
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return file_path

# Delete file if exists
def delete_file(file_path: Optional[str]):
    """Delete a file if it exists"""
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")