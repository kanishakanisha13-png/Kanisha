from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.models.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import create_recommendation


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Jewelry page
@router.get("/jewelry", response_class=HTMLResponse)
async def jewelry_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={"request": request}
    )


# Jewelry recommendation API
@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(
    request: RecommendationRequest,
    http_request: Request
):

    user_id = http_request.session.get("user_id")

    recommendations = create_recommendation(
        category="Jewelry",
        budget=request.budget,
        preferences=request.preferences,
        user_id=user_id
    )

    return RecommendationResponse(
        category="Jewelry",
        budget=request.budget,
        recommendations=recommendations
    )