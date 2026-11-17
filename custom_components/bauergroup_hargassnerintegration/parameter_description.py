"""Typed bilingual parameter names and optional wire-value enum mappings."""

from __future__ import annotations

from typing import Literal, TypedDict


class ParameterDescription(TypedDict, total=False):
    """Describe a parameter or a sparse override of its default description.

    Enum labels contain ``en`` and ``de`` translations and may include an ``icon``
    for state-dependent sensor icons. Missing fields inherit the default profile;
    ``enum: None`` explicitly disables an inherited enum. New enum labels without
    a default must supply both ``en`` and ``de`` translations.
    Sensor metadata controls classification and specialized handling; units still
    come from the firmware XML. Untranslated parameters display their wire name.
    """

    en: str
    de: str
    enum: dict[int, dict[str, str]] | None
    sensor_type: Literal["parameter", "boiler_state", "error"]
    device_class: str | None
    state_class: str | None
    icon: str | None
    ok_icon: str | None
    standard: bool
    entity_id_suffix: str
    sensor_name: dict[str, str]
