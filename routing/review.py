from fastapi import APIRouter, Depends

from depends import get_review_service
from schemas.review import Review, CompletedReview
from services.review import ReviewService

router = APIRouter(prefix="/review", tags=["review"])


@router.post(
    "",
    response_model=CompletedReview
)
async def review_endpoint(
        review_data: Review,
        review_service: ReviewService = Depends(get_review_service)
) -> CompletedReview:
    """
    Endpoint to submit a review and store it in cache.

    This endpoint receives review data, processes it using the provided review service,
    and returns the completed review, which has been stored in the cache.

    Args:
        review_data (Review): The review data to be processed and stored.
        review_service (ReviewService, optional): An instance of the ReviewService
            used to handle the review logic. It's injected using dependency injection.

    Returns:
        CompletedReview: The completed review data after processing and caching.
    """
    completed_review = await review_service.process_the_review(review_data)
    return completed_review
