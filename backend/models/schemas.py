from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    category: str = Field(..., min_length=1)
    budget: float = Field(..., gt=0)
    preferences: str = ""


class RecommendationResponse(BaseModel):
    category: str
    budget: float
    recommendations: str