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

    def configure(self, configuration: RuntimeConfiguration, *, profile: str | None = None,
                  capabilities: tuple[str, ...] = ()) -> RuntimeConfiguration:
        if capabilities:
            return configuration.with_assessment_profile("explicit", capabilities)
        try:
            selected = self._profiles.resolve(profile)
        except ValueError as error:
            raise AssessmentError(str(error)) from error
        if selected is None:
            label = profile if profile is not None else "default"
            raise AssessmentError(f"assessment profile is not registered: {label}")
        capabilities = tuple(item["identifier"] for item in selected["capabilities"])
        return configuration.with_assessment_profile(str(selected["identifier"]), capabilities,
                                                     identity=dict(selected["identity"]),
                                                     policy_file=str(selected["policyFile"]))
