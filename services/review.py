from pyexpat.errors import messages

import config
from repositories.redis_repository import RedisRepository
from repositories.github_repository import GitHubRepository
from repositories.open_ai_repository import OpenAIRepository
from schemas.review import CompletedReview, Review


class ReviewService:
    def __init__(
            self,
            redis_repository: RedisRepository,
            github_repository: GitHubRepository,
            open_ai_repository: OpenAIRepository
    ):
        self.redis_repository = redis_repository
        self.github_repository = github_repository
        self.open_ai_repository = open_ai_repository

    async def set_cache(self, review: Review) -> CompletedReview:
        cache_key = f"review:{hash(review.model_dump_json())}"

        if cached_review:= await self.redis_repository.get(cache_key) is not None:
            return CompletedReview(data=cached_review)

        repo_content, repo_structure = await self.github_repository.fetch_repository_files(str(review.github_repo_url))

        prompt = self._create_prompt(repo_content, review)

        openai_response = await self.open_ai_repository.completion_with_backoff(
            model=config.OPEN_AI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        feedback = openai_response["choices"][0]["message"]["content"]

        await self.redis_repository.set(cache_key, value=feedback)

        return CompletedReview(data=feedback)

    @staticmethod
    def _create_prompt(repo_content, review_data):
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
