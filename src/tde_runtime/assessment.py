"""Profile-driven assessment orchestration without analyzer knowledge."""

from __future__ import annotations

from .configuration import RuntimeConfiguration
from .registries import AssessmentProfileRegistry


class AssessmentError(ValueError):
    """Raised when an assessment cannot be planned from registered profiles."""


class AssessmentOrchestrator:
    """Selects the assessment capability set before the Runtime executes it."""

    def __init__(self, profiles: AssessmentProfileRegistry | None = None) -> None:
        self._profiles = profiles or AssessmentProfileRegistry()

    def configure(self, configuration: RuntimeConfiguration, *, profile: str = "default",
                  capabilities: tuple[str, ...] = ()) -> RuntimeConfiguration:
        if capabilities:
            return configuration.with_assessment_profile("explicit", capabilities)
        selected = self._profiles.resolve(profile)
        if selected is None:
            raise AssessmentError(f"assessment profile is not registered: {profile}")
        return configuration.with_assessment_profile(str(selected["id"]), tuple(selected["capabilities"]))
