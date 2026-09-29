from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.models.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import create_recommendation


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Party Planning page
@router.get("/party", response_class=HTMLResponse)
async def party_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={"request": request}
    )


# Party recommendation API
@router.post("/generate-party", response_model=RecommendationResponse)
async def generate_party(
    request: RecommendationRequest,
    http_request: Request
):

    user_id = http_request.session.get("user_id")

    recommendations = create_recommendation(
        category="Party Planning",
        budget=request.budget,
        preferences=request.preferences,
        user_id=user_id
    )

    return RecommendationResponse(
        category="Party Planning",
        budget=request.budget,
        recommendations=recommendations
    )