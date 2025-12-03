from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.gemini_service import analyze_image_with_gemini

# Initialize the App
app = FastAPI(
    title=settings.PROJECT_NAME if settings else "NutriLens",
    version="1.0.0"
)

# CORS Configuration
# This is crucial for allowing the Streamlit frontend (running on a different port)
# to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """
    Simple endpoint to verify the server is running.
    """
    return {"status": "healthy", "service": "NutriLens Backend"}

@app.post("/analyze")
async def analyze_meal(file: UploadFile = File(...)):
    """
    Receives an image file, sends it to Gemini, and returns nutrition data.
    """
    # 1. Validate File Type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, or WebP allowed.")

    try:
        # 2. Read Bytes
        contents = await file.read()

        # 3. Call AI Service
        result = await analyze_image_with_gemini(contents, file.content_type)
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))