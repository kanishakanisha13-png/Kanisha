from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.models.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import create_recommendation


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# Home Decor page
@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"request": request}
    )


# Home Decor recommendation API
@router.post("/generate-home", response_model=RecommendationResponse)
async def generate_home(
    request: RecommendationRequest,
    http_request: Request
):

    user_id = http_request.session.get("user_id")

    recommendations = create_recommendation(
        category="Home Decor",
        budget=request.budget,
        preferences=request.preferences,
        user_id=user_id
    )

    return RecommendationResponse(
        category="Home Decor",
        budget=request.budget,
        recommendations=recommendations
    )