import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create the Gemini client only when an API key is available.
# This allows the FastAPI app to start even if the Vercel
# environment variable has not been configured yet.
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_recommendation(prompt: str) -> str:
    """
    Generate budget-based recommendations using Gemini.
    """

    if not GEMINI_API_KEY or client is None:
        return (
            "Gemini API key is not configured yet. "
            "Please add your GEMINI_API_KEY to the Vercel environment variables."
        )

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if response and response.text:
            return response.text

        return "No recommendation was generated."

    except Exception as e:

        return (
            "Gemini is temporarily unavailable.\n\n"

            "Sample budget-based recommendations:\n"

            "1. Modern Wall Decor\n"
            "   Estimated Price: ₹1,500 - ₹3,000\n"
            "   Source: Amazon / Flipkart\n\n"

            "2. Decorative Lighting\n"
            "   Estimated Price: ₹1,000 - ₹2,500\n"
            "   Source: IKEA / Amazon\n\n"

            "3. Cushion Set\n"
            "   Estimated Price: ₹800 - ₹1,500\n"
            "   Source: Amazon / Flipkart\n\n"

            "4. Indoor Plants\n"
            "   Estimated Price: ₹500 - ₹1,000\n"
            "   Source: Local nursery / Online stores\n\n"

            f"Gemini service status: {str(e)}"
        )
