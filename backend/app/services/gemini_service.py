import google.generativeai as genai
import json
import typing_extensions as typing
from app.core.config import settings

# Configure Gemini once when the module loads
if settings:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# ---------------------------------------------------------
# DEFINE THE STRICT JSON SCHEMA (Type Safety)
# ---------------------------------------------------------
class FoodItem(typing.TypedDict):
    name: str
    bbox: list[int]  # [ymin, xmin, ymax, xmax]
    weight_g: int
    calories: int
    protein: int
    carbs: int
    fat: int
    confidence: float

class AnalysisResult(typing.TypedDict):
    foods: list[FoodItem]
    total_calories: int
    health_tip: str

# ---------------------------------------------------------
# THE AI LOGIC
# ---------------------------------------------------------
async def analyze_image_with_gemini(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """
    Sends raw image bytes to Gemini 1.5 Flash and returns structured JSON nutrition data.
    """
    if not settings:
        return {"error": "Server configuration error: Missing API Key"}

    model = genai.GenerativeModel('gemini-1.5-flash')

    # The Prompt Engineering (as defined in TRD)
    prompt = """
    Analyze the attached food image.
    1. Identify all food items.
    2. Draw Bounding Boxes for each item using normalized coordinates [ymin, xmin, ymax, xmax] (0-1000 scale).
    3. Estimate Weight in grams. Assume standard dinnerware sizes unless a reference object is visible.
    4. Calculate Macros (Calories, Protein, Carbs, Fat).

    CRITICAL: Output ONLY a valid JSON object.
    """

    try:
        # Prepare the content for Gemini
        # We wrap the bytes in the specific structure required by the SDK
        response = model.generate_content(
            [
                {"mime_type": mime_type, "data": image_bytes},
                prompt
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=AnalysisResult
            )
        )
        
        # Parse the response
        # Since we enforced JSON mode, response.text should be valid JSON
        result = json.loads(response.text)
        return result

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {"error": f"Failed to analyze image: {str(e)}"}