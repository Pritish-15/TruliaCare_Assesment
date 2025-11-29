# Vendor Onboarding & KYC Platform

A comprehensive full-stack web application for vendor onboarding and Know Your Customer (KYC) verification. This platform enables vendors to register, submit KYC documents, and allows administrators to review and approve/reject applications.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Key Concepts & Tools](#key-concepts--tools)
- [Frontend Architecture](#frontend-architecture)
- [Backend Architecture](#backend-architecture)
- [Security Features](#security-features)
- [File Upload System](#file-upload-system)
- [Deployment](#deployment)
- [Default Credentials](#default-credentials)

## 🎯 Overview

This platform provides a complete solution for vendor onboarding with comprehensive KYC (Know Your Customer) verification. It consists of:

- **Vendor Portal**: Multi-step registration form, document upload with webcam support, and application status tracking
- **Admin Dashboard**: Review applications, approve/reject vendors, download documents, and view statistics

The system handles various vendor types including students, professionals, minors, and NRI/OCI applicants with appropriate document requirements.

## ✨ Features

### Vendor Features
- **Multi-Step Registration Form**: 
  - Step 1: Personal Information (name, age, DOB, gender, marital status, etc.)
  - Step 2: Contact & Address Information
  - Step 3: Identity Details, Business Information, Bank Details
- **KYC Document Upload**:
  - Identity Proof: Select one from Aadhaar, PAN, Passport, Voter ID, or Driving License
  - Address Proof: Select one from multiple options (Aadhaar, Passport, Utility Bills, Bank Statement, etc.)
  - Live Selfie: Webcam capture for real-time verification
  - Passport Photo: Upload passport-size photograph
  - Business Documents: GST Certificate, Partnership Deed, Certificate of Incorporation, etc.
- **Application Status Tracking**: Real-time status check using Vendor ID
- **Sequential Vendor ID Generation**: Consistent IDs (VEN000001, VEN000002, etc.)

### Admin Features
- **Secure Authentication**: JWT-based admin login
- **Dashboard Statistics**: 
  - Total vendors
  - Pending applications
  - Approved vendors
  - Rejected vendors
- **Vendor Management**:
  - View all vendors with filtering (Pending/Approved/Rejected)
  - Detailed vendor review page
  - Approve/Reject applications
  - Add rejection reasons
  - Download KYC documents
- **Document Management**: Download any uploaded document for verification

## 🛠 Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite (Development) / PostgreSQL (Production-ready)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt (via passlib)
- **File Upload**: FastAPI UploadFile
- **Validation**: Pydantic
- **Server**: Uvicorn (ASGI server)

### Frontend
- **Framework**: React 19.2.0
- **Language**: TypeScript
- **Routing**: Wouter (Lightweight React router)
- **Form Management**: React Hook Form with Zod validation
- **State Management**: React Query (TanStack Query)
- **UI Components**: 
  - Radix UI (Headless components)
  - Tailwind CSS (Styling)
  - shadcn/ui (Component library)
- **Icons**: Lucide React
- **Build Tool**: Vite
- **HTTP Client**: Fetch API

### Development Tools
- **Backend**: 
  - Python 3.8+
  - pip (Package manager)
- **Frontend**:
  - Node.js 18+
  - npm/yarn (Package manager)
  - TypeScript
  - PostCSS
  - Autoprefixer

## 📁 Project Structure

```
TruliaCare Assessment/
├── backend/
│   ├── app/
│   │   ├── __pycache__/          # Python cache files
│   │   ├── admin_routes.py        # Admin API endpoints
│   │   ├── auth.py                # Authentication & JWT utilities
│   │   ├── database.py            # Database connection & session
│   │   ├── main.py                # FastAPI app initialization
│   │   ├── models.py              # SQLAlchemy database models
│   │   ├── schemas.py             # Pydantic request/response schemas
│   │   ├── utils.py               # Utility functions (ID generation, file handling)
│   │   ├── vednor_routes.py       # Vendor API endpoints
│   │   └── vendors.db             # SQLite database file
│   ├── uploads/                   # Document storage directory
│   │   └── [VENDOR_ID]/          # Vendor-specific folders
│   │       ├── pan.jpg
│   │       ├── aadhaar.jpg
│   │       ├── live_selfie.jpg
│   │       └── ...
│   └── requirements.txt           # Python dependencies
│
└── frontend/
    └── ReactFrontend/
        ├── client/
        │   ├── src/
        │   │   ├── components/
        │   │   │   ├── layout.tsx          # Main layout component
        │   │   │   └── ui/                # shadcn/ui components
        │   │   ├── hooks/
        │   │   │   ├── use-toast.ts       # Toast notification hook
        │   │   │   └── use-mobile.tsx     # Mobile detection hook
        │   │   ├── lib/
        │   │   │   ├── api.ts             # API client functions
        │   │   │   ├── queryClient.ts     # React Query configuration
        │   │   │   └── utils.ts           # Utility functions
        │   │   ├── pages/
        │   │   │   ├── admin/
        │   │   │   │   ├── dashboard.tsx      # Admin dashboard
        │   │   │   │   ├── login.tsx         # Admin login page
        │   │   │   │   └── vendor-review.tsx  # Vendor review page
        │   │   │   ├── vendor/
        │   │   │   │   ├── register.tsx       # Vendor registration form
        │   │   │   │   ├── kyc-upload.tsx     # Document upload page
        │   │   │   │   ├── status.tsx         # Status check page
        │   │   │   │   ├── success.tsx        # Success page
        │   │   │   │   └── login.tsx         # Vendor login (if needed)
        │   │   │   ├── home.tsx              # Landing page
        │   │   │   └── not-found.tsx         # 404 page
        │   │   ├── App.tsx                   # Main app component with routing
        │   │   ├── main.tsx                  # React entry point
        │   │   └── index.css                  # Global styles
        │   ├── index.html                    # HTML template
        │   └── public/                      # Static assets
        ├── package.json                      # Node.js dependencies
        ├── vite.config.ts                   # Vite configuration
        ├── tsconfig.json                     # TypeScript configuration
        └── tailwind.config.js               # Tailwind CSS configuration
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend/app
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-multipart passlib[bcrypt] python-jose[cryptography] email-validator bcrypt==4.0.1
   ```

4. **Initialize database**:
   The database will be created automatically on first run. To reset:
   ```bash
   # Delete existing database
   rm vendors.db  # On macOS/Linux
   del vendors.db  # On Windows
   ```

5. **Run the backend server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Or use Python directly:
   ```bash
   python main.py
   ```

6. **Verify backend is running**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend/ReactFrontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure API URL** (if needed):
   Create a `.env` file in `frontend/ReactFrontend/client/`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Run the development server**:
   ```bash
   npm run dev:client
   # or
   yarn dev:client
   ```

5. **Access the application**:
   - Frontend: http://localhost:5000
   - Backend API: http://localhost:8000

### Running Both Servers

**Option 1: Separate Terminals**
- Terminal 1: Backend (`cd backend/app && uvicorn main:app --reload`)
- Terminal 2: Frontend (`cd frontend/ReactFrontend && npm run dev:client`)

**Option 2: Background Processes**
```bash
# Backend
cd backend/app && uvicorn main:app --reload &

# Frontend
cd frontend/ReactFrontend && npm run dev:client &
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Vendor Endpoints

#### 1. Register Vendor
```http
POST /api/vendor/register
Content-Type: multipart/form-data

Form Fields:
- name (required): Full name
- age (required): Age (1-150)
- email (required): Email address
- phone (required): Phone number
- date_of_birth (required): Date of birth
- current_address (required): Current address
- [All other KYC fields as optional]
```

**Response**: `VendorResponse` with generated `vendor_id`

#### 2. Upload Documents
```http
POST /api/vendor/upload-documents/{vendor_id}
Content-Type: multipart/form-data

Files:
- aadhaar_document (optional): Aadhaar card
- pan_document (optional): PAN card
- passport_document (optional): Passport
- voter_id_document (optional): Voter ID
- driving_license_document (optional): Driving License
- address_proof_* (optional): Address proof documents
- passport_photo (optional): Passport photo
- live_selfie (optional): Live selfie
- [Business documents as needed]
```

**Note**: Only ONE identity proof and ONE address proof can be uploaded per vendor.

#### 3. Check Status
```http
POST /api/vendor/check-status
Content-Type: application/json

{
  "vendor_id": "VEN000001"
}
```

**Response**: Status information with rejection reason if applicable

### Admin Endpoints

#### 1. Admin Login
```http
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response**: 
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### 2. Get All Vendors
```http
GET /api/admin/vendors?status_filter=pending
Authorization: Bearer {token}
```

**Query Parameters**:
- `status_filter` (optional): `pending`, `approved`, or `rejected`

#### 3. Get Vendor by ID
```http
GET /api/admin/vendors/{vendor_id}
Authorization: Bearer {token}
```

#### 4. Update Vendor Status
```http
PUT /api/admin/vendors/{vendor_id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "approved"  // or "rejected"
  "rejection_reason": "Reason here"  // Required if rejected
}
```

#### 5. Download Document
```http
GET /api/admin/vendors/{vendor_id}/documents/{doc_type}
Authorization: Bearer {token}
```

**Document Types**:
- `aadhaar`, `pan`, `passport`, `voter_id`, `driving_license`
- `address_proof_aadhaar`, `address_proof_passport`, etc.
- `passport_photo`, `live_selfie`
- `gst_certificate`, `partnership_deed`, etc.

#### 6. Dashboard Statistics
```http
GET /api/admin/dashboard/stats
Authorization: Bearer {token}
```

**Response**:
```json
{
  "total_vendors": 100,
  "pending": 25,
  "approved": 60,
  "rejected": 15
}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄 Database Schema

### Vendor Model

The `Vendor` model includes comprehensive KYC fields:

**Core Fields**:
- `id`: Primary key (Integer)
- `vendor_id`: Unique sequential ID (String, e.g., "VEN000001")
- `status`: Enum (pending, approved, rejected)
- `rejection_reason`: Optional rejection reason
- `created_at`: Timestamp
- `updated_at`: Timestamp

**Personal Information**:
- `name`, `age`, `gender`, `date_of_birth`
- `fathers_name`, `mothers_name`, `marital_status`, `nationality`

**Contact Information**:
- `email` (unique), `phone`, `alternate_phone`, `aadhaar_linked_mobile`

**Address Information**:
- `current_address`, `current_city`, `current_state`, `current_pincode`
- `permanent_address`, `permanent_city`, `permanent_state`, `permanent_pincode`
- `country`

**Identity Details**:
- `pan_number`, `aadhaar_number`, `passport_number`, `voter_id`, `driving_license`

**Business Information**:
- `business_name`, `business_type`, `business_category`, `gst_number`

**Additional Information**:
- **Students**: `is_student`, `college_id`, `student_local_address`
- **Professionals**: `occupation`, `company_name`, `annual_income`, `source_of_funds`
- **Minors**: `is_minor`, `guardians_name`, `guardians_pan`, `guardians_aadhaar`, `birth_certificate_number`
- **NRI/OCI**: `is_nri_oci`, `visa_number`, `oci_card_number`, `overseas_address`, `fatca_declaration`

**Bank Details**:
- `bank_name`, `account_number`, `ifsc_code`

**Document Paths** (stored as file paths):
- Identity: `aadhaar_document`, `pan_document`, `passport_document`, `voter_id_document`, `driving_license_document`
- Address: `address_proof_aadhaar`, `address_proof_passport`, `address_proof_voter_id`, `address_proof_driving_license`, `address_proof_electricity_bill`, `address_proof_water_gas_bill`, `address_proof_bank_statement`
- Photos: `passport_photo`, `live_selfie`
- Business: `gst_certificate`, `partnership_deed`, `certificate_of_incorporation`, `memorandum_articles`, `shop_establishment_certificate`
- Additional: `college_id_document`, `local_address_proof`, `guardians_kyc_documents`, `birth_certificate_document`, `visa_document`, `oci_card_document`, `overseas_address_proof`, `fatca_declaration_document`

### Admin Model

- `id`: Primary key
- `username`: Unique username
- `hashed_password`: Bcrypt hashed password

## 🔑 Key Concepts & Tools

### Backend Concepts

#### 1. **FastAPI Framework**
- Modern, fast Python web framework
- Automatic API documentation
- Type hints for validation
- Async/await support

#### 2. **SQLAlchemy ORM**
- Object-Relational Mapping
- Database abstraction layer
- Session management
- Query building

#### 3. **Pydantic Schemas**
- Data validation
- Type conversion
- Request/response models
- Automatic serialization

#### 4. **JWT Authentication**
- Token-based authentication
- Stateless authentication
- Secure token generation
- Token expiration handling

#### 5. **Password Security**
- Bcrypt hashing
- Salt generation
- Secure password storage
- Password verification

#### 6. **File Upload Handling**
- Multipart form data
- File validation
- Secure file storage
- Vendor-specific folders

#### 7. **Dependency Injection**
- FastAPI's `Depends()`
- Database session management
- Authentication dependencies
- Reusable components

#### 8. **Error Handling**
- HTTPException for API errors
- Try-except blocks
- Database rollback on errors
- User-friendly error messages

### Frontend Concepts

#### 1. **React Hooks**
- `useState`: Component state management
- `useEffect`: Side effects and lifecycle
- `useRef`: DOM references (for webcam)
- Custom hooks: `useToast`, `useMobile`

#### 2. **React Hook Form**
- Form state management
- Validation integration
- Error handling
- Multi-step forms

#### 3. **Zod Validation**
- Schema-based validation
- Type-safe validation
- Step-specific schemas
- Error messages

#### 4. **React Query (TanStack Query)**
- Server state management
- Caching
- Background updates
- Error handling

#### 5. **Wouter Routing**
- Lightweight router
- Route matching
- URL parameters
- Navigation

#### 6. **TypeScript**
- Type safety
- Interface definitions
- Type inference
- Compile-time error checking

#### 7. **Component Architecture**
- Reusable UI components
- Layout components
- Page components
- Form components

#### 8. **Webcam Integration**
- MediaDevices API
- Video stream handling
- Canvas for image capture
- Blob to File conversion

#### 9. **File Upload**
- FormData API
- File validation
- Progress tracking
- Error handling

#### 10. **State Management**
- Local state (useState)
- Server state (React Query)
- Form state (React Hook Form)
- URL state (route params)

## 🏗 Frontend Architecture

### Component Hierarchy

```
App
├── QueryClientProvider (React Query)
├── TooltipProvider
├── Router (Wouter)
│   ├── Home
│   ├── Vendor Routes
│   │   ├── VendorRegister (Multi-step form)
│   │   ├── KYCUpload (Document upload with webcam)
│   │   ├── VendorStatus (Status check)
│   │   └── VendorSuccess
│   └── Admin Routes
│       ├── AdminLogin
│       ├── AdminDashboard
│       └── VendorReview
└── Toaster (Notifications)
```

### Key Components

#### 1. **Layout Component**
- Consistent page structure
- Navigation
- Footer
- Responsive design

#### 2. **Multi-Step Registration Form**
- Three-step wizard
- Step-specific validation
- Progress indicator
- Data persistence between steps

#### 3. **Document Upload Component**
- Dynamic document selection
- File validation
- Upload status tracking
- Webcam integration

#### 4. **Live Selfie Capture**
- Webcam access
- Video preview
- Image capture
- Canvas manipulation

#### 5. **Admin Dashboard**
- Statistics cards
- Vendor table
- Filtering
- Status badges

#### 6. **Vendor Review Page**
- Complete vendor details
- Document download
- Approve/Reject actions
- Rejection reason input

### API Client Architecture

The `lib/api.ts` file centralizes all API calls:

- **Token Management**: localStorage for JWT tokens
- **Request Wrapper**: Generic `apiRequest` function
- **Form Data Handler**: `apiFormRequest` for file uploads
- **Error Handling**: Consistent error messages
- **Type Safety**: TypeScript interfaces for all requests/responses

## 🔒 Security Features

### Backend Security

1. **Password Hashing**
   - Bcrypt with salt
   - Secure password storage
   - No plaintext passwords

2. **JWT Authentication**
   - Secure token generation
   - Token expiration (24 hours)
   - Bearer token authentication

3. **CORS Configuration**
   - Configurable origins
   - Credential support
   - Method restrictions

4. **Input Validation**
   - Pydantic schemas
   - Type checking
   - Required field validation
   - Email validation

5. **File Upload Security**
   - File size limits (5MB)
   - File type validation
   - Secure file storage
   - Vendor-specific folders

6. **Database Security**
   - Parameterized queries (SQLAlchemy)
   - SQL injection prevention
   - Session management

### Frontend Security

1. **Token Storage**
   - localStorage for tokens
   - Secure token handling
   - Token removal on logout

2. **Input Validation**
   - Client-side validation (Zod)
   - Server-side validation (Pydantic)
   - Type checking (TypeScript)

3. **Error Handling**
   - User-friendly error messages
   - No sensitive data exposure
   - Proper error boundaries

4. **HTTPS Ready**
   - Secure API communication
   - Environment-based URLs
   - CORS configuration

## 📤 File Upload System

### Storage Structure

```
backend/uploads/
├── VEN000001/
│   ├── pan.jpg
│   ├── aadhaar.jpg
│   ├── live_selfie.jpg
│   └── passport_photo.jpg
├── VEN000002/
│   └── ...
```

### Upload Process

1. **File Selection**: User selects file or captures via webcam
2. **Validation**: File size (max 5MB) and type checking
3. **Storage**: Files saved in vendor-specific folders
4. **Database**: File paths stored in vendor record
5. **Serving**: Files served via FastAPI StaticFiles

### Document Categories

- **Identity Proof**: One document required (Aadhaar, PAN, Passport, Voter ID, or Driving License)
- **Address Proof**: One document required (Multiple options)
- **Photographs**: Passport photo and live selfie
- **Business Documents**: Optional, based on business type

### Webcam Integration

- Uses `navigator.mediaDevices.getUserMedia()`
- Front-facing camera access
- Canvas-based image capture
- Blob to File conversion
- Automatic cleanup of media streams

## 🚢 Deployment

### Backend Deployment

1. **Production Server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Environment Variables**:
   - Database URL (for PostgreSQL)
   - Secret key for JWT
   - CORS origins

3. **Database Migration**:
   - Use Alembic for production migrations
   - Or recreate tables on first run

4. **File Storage**:
   - Use cloud storage (S3, Azure Blob) for production
   - Or mount persistent volume

### Frontend Deployment

1. **Build for Production**:
   ```bash
   npm run build
   ```

2. **Environment Configuration**:
   - Set `VITE_API_BASE_URL` to production API URL

3. **Static Hosting**:
   - Deploy to Vercel, Netlify, or similar
   - Or serve via Nginx/Apache

4. **HTTPS**:
   - Required for webcam access
   - SSL certificate configuration

### Recommended Production Setup

- **Backend**: 
  - PostgreSQL database
  - Cloud file storage
  - Load balancer
  - SSL/TLS certificates

- **Frontend**:
  - CDN for static assets
  - Environment-based configuration
  - Error tracking (Sentry)
  - Analytics integration

## 🔐 Default Credentials

### Admin Account

On first startup, a default admin account is created:

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change the default password immediately after first login!

The default admin is created in `main.py` startup event. To disable this in production, remove or modify the startup event.

## 📝 Additional Notes

### Vendor ID Generation

- Sequential IDs: VEN000001, VEN000002, etc.
- 6-digit zero-padded format
- Handles existing random IDs gracefully
- Ensures uniqueness

### Status Workflow

1. **Pending**: Initial status after registration
2. **Approved**: Admin approves application
3. **Rejected**: Admin rejects with reason

### Document Management

- Only one identity proof per vendor
- Only one address proof per vendor
- Previous documents are deleted when new ones are uploaded
- Files are organized by vendor ID

### Error Handling

- Backend: HTTPException with appropriate status codes
- Frontend: Toast notifications for user feedback
- Validation errors shown inline in forms
- Network errors handled gracefully

## 🤝 Contributing

This is a complete, production-ready application. To extend:

1. Add new KYC fields in `models.py` and `schemas.py`
2. Update frontend forms in `register.tsx`
3. Add new document types in `kyc-upload.tsx`
4. Extend API endpoints as needed

## 📄 License

This project is part of the TruliaCare Assessment.

## 🎓 Learning Resources

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Frontend
- [React Documentation](https://react.dev/)
- [React Hook Form](https://react-hook-form.com/)
- [Zod Documentation](https://zod.dev/)
- [Wouter Documentation](https://github.com/molefrog/wouter)
- [TanStack Query](https://tanstack.com/query)

---

**Built with ❤️ using FastAPI, React, and TypeScript**

