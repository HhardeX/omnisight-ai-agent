import pytest
from pydantic import ValidationError

from app.models.jobs import BuildEvent


def valid_build_event() -> dict:
    return {
        "repository": "HhardeX/omnisight-ai-agent",
        "commit_sha": "fb29e74",
        "branch": "feature/Aishwarya",
        "target_url": "https://example.com",
    }


def test_build_event_accepts_valid_payload() -> None:
    event = BuildEvent(**valid_build_event())

    assert event.repository == "HhardeX/omnisight-ai-agent"
    assert event.commit_sha == "fb29e74"
    assert event.branch == "feature/Aishwarya"
    assert str(event.target_url) == "https://example.com/"


def test_build_event_strips_string_whitespace() -> None:
    event = BuildEvent(
        repository="  HhardeX/omnisight-ai-agent  ",
        commit_sha="  fb29e74  ",
        branch="  feature/Aishwarya  ",
        target_url="https://example.com",
    )

    assert event.repository == "HhardeX/omnisight-ai-agent"
    assert event.commit_sha == "fb29e74"
    assert event.branch == "feature/Aishwarya"


@pytest.mark.parametrize(
    "field",
    ["repository", "commit_sha", "branch", "target_url"],
)
def test_build_event_requires_all_fields(field: str) -> None:
    payload = valid_build_event()
    payload.pop(field)

    with pytest.raises(ValidationError):
        BuildEvent(**payload)


def test_build_event_rejects_invalid_target_url() -> None:
    payload = valid_build_event()
    payload["target_url"] = "not-a-url"

    with pytest.raises(ValidationError):
        BuildEvent(**payload)


def test_build_event_rejects_extra_fields() -> None:
    payload = valid_build_event()
    payload["unexpected"] = "value"

    with pytest.raises(ValidationError):
        BuildEvent(**payload)


@pytest.mark.parametrize(
    "field,value",
    [
        ("repository", ""),
        ("commit_sha", "123456"),
        ("branch", ""),
    ],
)
def test_build_event_rejects_values_below_minimum_length(
    field: str,
    value: str,
) -> None:
    payload = valid_build_event()
    payload[field] = value

    with pytest.raises(ValidationError):
        BuildEvent(**payload)