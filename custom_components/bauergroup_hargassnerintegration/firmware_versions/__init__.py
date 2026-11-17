"""Select firmware lookups through static imports, with a default fallback."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final

from . import V10_2HAR_n2, default
from .definitions import FirmwareDefinitions

# Register sparse overrides here; unspecified fields inherit the default profile.
FIRMWARE_DEFINITIONS: Final[dict[str, FirmwareDefinitions]] = {
    "V10_2HAR_n2": V10_2HAR_n2.DEFINITIONS,
}


def get_firmware_definitions(firmware_version: str) -> FirmwareDefinitions:
    """Overlay a firmware's sparse overrides on the default lookup definitions.

    XML layout selection remains in firmware_templates; these definitions only
    control presentation of the parsed values, never their positions or units.
    Missing parameters, languages, error codes, and enum entries inherit defaults.
    An explicit ``enum: None`` disables the inherited enum. Resolved overrides
    contain independent dictionaries so neither input profile can be mutated.
    """
    overrides = FIRMWARE_DEFINITIONS.get(firmware_version)
    if overrides is None:
        return default.DEFINITIONS

    return FirmwareDefinitions(
        parameter_descriptions=_merge_lookup_tables(
            default.PARAMETER_DESCRIPTIONS, overrides.parameter_descriptions
        ),
        error_codes=_merge_lookup_tables(default.ERROR_CODES, overrides.error_codes),
        display_name=overrides.display_name,
    )


def _merge_lookup_tables(
    defaults: dict[Any, Any], overrides: dict[Any, Any]
) -> dict[Any, Any]:
    """Merge nested lookup dictionaries without sharing mutable input values.

    Scalar values, including an explicit None, replace the corresponding default.
    Empty dictionaries introduce no overrides and therefore inherit their defaults.
    """
    merged = deepcopy(defaults)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_lookup_tables(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def get_firmware_display_name(firmware_version: str) -> str:
    """Use an optional dedicated display name, otherwise the stable version key.

    The default profile's presentation metadata must not rename other firmware.
    """
    definitions = FIRMWARE_DEFINITIONS.get(firmware_version)
    if definitions and definitions.display_name:
        return definitions.display_name
    return firmware_version
