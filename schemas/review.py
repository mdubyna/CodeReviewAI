from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, validator, field_validator


class CandidateLevelEnum(Enum):
    """
    Enum representing the candidate's skill level.

    Includes the following levels:
    - junior
    - middle
    - senior
    """

    junior = "junior"
    middle = "middle"
    senior = "senior"


class Review(BaseModel):
    """
    A Pydantic model for submitting a review of a candidate's assignment.

    Attributes:
        assignment_description (str): A description of the candidate's assignment.
        github_repo_url (HttpUrl): The URL of the GitHub repository associated with the assignment.
        candidate_level (CandidateLevelEnum): The skill level of the candidate (junior, middle, senior).
    """

    assignment_description: str
    github_repo_url: HttpUrl
    candidate_level: CandidateLevelEnum = Field(default=CandidateLevelEnum.middle)

    @field_validator("github_repo_url")
    @classmethod
    def validate_repo_url(cls, value: HttpUrl) -> HttpUrl:
        """
        Validates that the provided GitHub repository URL is in the correct format.

        Ensures the URL is an HTTPS GitHub URL and points to a valid repository.

        Args:
            value (HttpUrl): The GitHub repository URL to be validated.

        Raises:
            ValueError: If the URL is not a valid GitHub repository URL.

        Returns:
            HttpUrl: The validated GitHub URL.
        """
        if (
            value.host
            and not value.host.endswith("github.com")
            or value.scheme != "https"
        ):
            raise ValueError("URL must be a valid GitHub HTTPS address.")

        if path_parts := value.path:
            if len(path_parts.split("/")) < 2:
                raise ValueError("Invalid GitHub repository URL")

        return value


class CompletedReview(BaseModel):
    """
    A Pydantic model representing the completed review result.

    Attributes:
        data (str): The result or summary of the completed review.
    """

    data: str
