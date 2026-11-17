"""Group the two lookup dictionaries selected for a boiler's firmware."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..parameter_description import ParameterDescription


@dataclass(frozen=True)
class FirmwareDefinitions:
    """Default lookups, sparse firmware overrides, or a resolved combination.

    Empty tables are valid overrides and inherit all default values. Consumers
    must not mutate the registered dictionaries; the resolver merges dedicated
    profiles into independent tables and entity option lists remain local.
    """

    parameter_descriptions: dict[str, ParameterDescription] = field(default_factory=dict)
    error_codes: dict[str, dict[str, str]] = field(default_factory=dict)
    display_name: str | None = None
