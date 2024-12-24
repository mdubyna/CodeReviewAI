from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, validator, field_validator


class CandidateLevelEnum(Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Review(BaseModel):
    assignment_description: str
    github_repo_url: HttpUrl
    candidate_level: CandidateLevelEnum = Field(default=CandidateLevelEnum.middle)

    @field_validator("github_repo_url")
    @classmethod
    def validate_repo_url(cls, value: HttpUrl) -> HttpUrl:
        if value.host and not value.host.endswith("github.com") or value.scheme != "https":
            raise ValueError("URL must be a valid GitHub HTTPS address.")

        path_parts = value.path.split("/")
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub repository URL")

        return value

class CompletedReview(BaseModel):
    data: str
