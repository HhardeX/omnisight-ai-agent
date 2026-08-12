from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BuildEvent(BaseModel):
    """Validated CI/CD build event used to start an OmniSight audit."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    repository: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Repository identifier, for example owner/repository.",
    )

    commit_sha: str = Field(
        ...,
        min_length=7,
        max_length=128,
        description="Git commit SHA associated with the build.",
    )

    branch: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Git branch associated with the build.",
    )

    target_url: HttpUrl = Field(
        ...,
        description="Target application URL to be audited by Playwright.",
    )