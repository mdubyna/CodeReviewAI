from logging import getLogger

import openai
from fastapi import HTTPException

import config
from repositories.redis_repository import RedisRepository
from repositories.github_repository import GitHubRepository
from repositories.open_ai_repository import OpenAIRepository
from schemas.review import CompletedReview, Review


logger = getLogger(__name__)


class ReviewService:
    """
    Service for managing the review process of a candidate's code.

    Handles fetching data from GitHub, generating feedback using OpenAI, and caching the results
    in Redis for faster retrieval.
    """

    def __init__(
        self,
        redis_repository: RedisRepository,
        github_repository: GitHubRepository,
        open_ai_repository: OpenAIRepository,
    ):
        """
        Initializes the ReviewService with the required repositories for Redis, GitHub, and OpenAI.

        Args:
            redis_repository (RedisRepository): Repository for interacting with Redis cache.
            github_repository (GitHubRepository): Repository for fetching GitHub repository data.
            open_ai_repository (OpenAIRepository): Repository for interacting with the OpenAI API.
        """
        self.redis_repository = redis_repository
        self.github_repository = github_repository
        self.open_ai_repository = open_ai_repository

    async def process_the_review(self, review: Review) -> CompletedReview | dict[str, str]:
        """
        Processes the review by fetching repository data, generating feedback using OpenAI,
        and caching the result in Redis.

        If the review has already been processed and cached, returns the cached feedback.

        Args:
            review (Review): The review data containing assignment description, GitHub URL, and candidate level.

        Returns:
            CompletedReview: The completed review with feedback data.
        """
        cache_key = f"review:{hash(review.model_dump_json())}"

        if cached_review := await self.redis_repository.get(cache_key) is not None:
            return CompletedReview(data=str(cached_review))

        repo_content, repo_structure = (
            await self.github_repository.fetch_repository_files(
                str(review.github_repo_url)
            )
        )

        prompt = self._create_prompt(repo_content, review)

        try:
            openai_response = await self.open_ai_repository.completion_with_backoff(
                model=config.OPEN_AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )

        except openai.BadRequestError as e:
            raise HTTPException(
                status_code=400, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.AuthenticationError as e:
            raise HTTPException(
                status_code=401, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.PermissionDeniedError as e:
            raise HTTPException(
                status_code=403, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.NotFoundError as e:
            raise HTTPException(
                status_code=404, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.UnprocessableEntityError as e:
            raise HTTPException(
                status_code=422, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.RateLimitError as e:
            raise HTTPException(
                status_code=429, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.InternalServerError as e:
            raise HTTPException(
                status_code=500, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        except openai.APIConnectionError as e:
            raise HTTPException(
                status_code=400, detail=f"Error accessing OpenAI API: {str(e)}"
            )

        feedback = openai_response["choices"][0]["message"]["content"]

        await self.redis_repository.set(
            key=cache_key, value=feedback, ttl=int(config.CACHE_TIME_TO_LIVE)
        )

        return CompletedReview(data=feedback)

    @staticmethod
    def _create_prompt(repo_content, review_data):
        """
        Creates the prompt for OpenAI based on the provided repository content and review data.

        The prompt instructs OpenAI to analyze the code and provide feedback in a structured format.

        Args:
            repo_content (str): The content of the candidate's GitHub repository.
            review_data (Review): The review data containing assignment description and candidate level.

        Returns:
            str: The generated prompt for OpenAI.
        """
        return (
            f"Review the following test assignment for a {review_data.candidate_level} candidate.\n\n"
            f"Assignment Description: {review_data.assignment_description}\n\n"
            f"Candidate code:\n{repo_content}\n\n"
            f"Analyze the code and provide feedback in the following structured format, "
            f"limited to 255 words:\n\n"
            f"1. **Downsides**: Highlight the major issues in the code.\n"
            f"2. **Documentation and comments**: Assess the quality of comments and documentation.\n"
            f"3. **Rating**: Evaluate the code quality on a scale of 1 to 5 based on the candidate's level ({review_data.candidate_level}).\n"
            f"4. **Conclusion**: Summarize the analysis and provide overall recommendations for improvement.\n\n"
            f"Provide concise and actionable feedback."
        )
