from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base, get_db, SessionLocal
from models import Admin
from auth import get_password_hash
import vednor_routes
import admin_routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Vendor KYC Platform",
    description="Backend API for Vendor Onboarding and KYC Management",
    version="1.0.0"
)

# CORS Configuration (Allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving files
import os
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(vednor_routes.router)
app.include_router(admin_routes.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Vendor KYC Platform API",
        "version": "1.0.0",
        "endpoints": {
            "vendor": "/api/vendor",
            "admin": "/api/admin",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Startup event - Create default admin if not exists
@app.on_event("startup")
async def startup_event():
    """Create default admin user on startup if not exists"""
    db = SessionLocal()
    try:
        # Check if admin exists
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        
        if not existing_admin:
            # Create default admin
            default_admin = Admin(
                username="admin",
                hashed_password=get_password_hash("admin123")  # Change this password!
            )
            db.add(default_admin)
            db.commit()
            print("✅ Default admin created - Username: admin, Password: admin123")
            print("⚠️  Please change the default password after first login!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating default admin: {e}")
    finally:
        db.close()

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)