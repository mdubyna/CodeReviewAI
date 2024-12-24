from fastapi import APIRouter, Depends

from depends import get_review_service
from schemas.review import Review, CompletedReview
from services.review import ReviewService

router = APIRouter(prefix="/review", tags=["review"])


@router.post(
    "",
    # response_model=CompletedReview
)
async def review_endpoint(review_data: Review, review_service: ReviewService = Depends(get_review_service)) -> dict:
    completed_review = await review_service.set_cache(review_data)
    return completed_review