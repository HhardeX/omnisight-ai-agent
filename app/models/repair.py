from pydantic import BaseModel, Field


class RepairRequest(BaseModel):
    """Request describing a validated visual repair to publish."""

    job_id: str = Field(min_length=1)
    viewport: str = Field(min_length=1)
    file_path: str = Field(min_length=1)
    content: str
    commit_message: str = Field(min_length=1)
    pull_request_title: str = Field(min_length=1)
    pull_request_body: str = Field(min_length=1)


class RepairResponse(BaseModel):
    """Response returned after publishing a repair."""

    job_id: str = Field(min_length=1)
    viewport: str = Field(min_length=1)
    branch_name: str = Field(min_length=1)
    commit_sha: str = Field(min_length=1)
    pull_request_url: str = Field(min_length=1)