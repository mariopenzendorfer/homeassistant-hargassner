"""Verify firmware lookup isolation and sensor behavior without Home Assistant."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from dataclasses import replace
from types import ModuleType, SimpleNamespace

import pytest

from conftest import HargassnerMessageParser, REPO_ROOT, load_module
from bauergroup_hargassnerintegration.firmware_versions import (
    FIRMWARE_DEFINITIONS,
    default,
    get_firmware_definitions,
    get_firmware_display_name,
)
from bauergroup_hargassnerintegration.firmware_versions.definitions import FirmwareDefinitions


@pytest.fixture
def custom_profile(monkeypatch):
    """Replace V10 lookups temporarily, with deliberately different enum codes."""
    profile = FirmwareDefinitions()
    profile.parameter_descriptions["ZK"] = {
        "en": "Wood boiler state", "de": "Holzkesselzustand",
        "enum": {
            0: {"en": "Unclassified", "de": "Nicht klassifiziert"},
            42: {"en": "Wood burning", "de": "Holzbrand", "icon": "mdi:fire"},
        },
    }
    profile.parameter_descriptions["TK"] = {"en": "Wood temperature", "de": "Holztemperatur"}
    profile.parameter_descriptions["TVL_1"] = {
        "en": "Circuit mode", "de": "Heizkreismodus",
        "enum": {0: {"en": "Stopped", "de": "Gestoppt"}, 3: {"en": "Active", "de": "Aktiv"}},
    }
    profile.error_codes["1"] = {"en": "Wood boiler fault", "de": "Holzkesselfehler"}
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", profile)
    return profile


@pytest.fixture
def sensor_module(monkeypatch):
    """Stub HA's imports only; execute the real setup and sensor implementations.

    This exercises entity values and metadata, but not HA's registry or frontend.
    """
    def add_module(name, **attributes):
        module = ModuleType(name)
        module.__dict__.update(attributes)
        monkeypatch.setitem(sys.modules, name, module)

    add_module("homeassistant")
    add_module("homeassistant.components")
    add_module("homeassistant.helpers")
    add_module(
        "homeassistant.components.sensor",
        SensorEntity=type("SensorEntity", (), {"_attr_device_class": None, "_attr_state_class": None}),
        SensorDeviceClass=SimpleNamespace(TEMPERATURE="temperature", CURRENT="current", PRESSURE="pressure", ENUM="enum", ENERGY="energy"),
        SensorStateClass=SimpleNamespace(MEASUREMENT="measurement", TOTAL="total", TOTAL_INCREASING="total_increasing"),
    )
    add_module("homeassistant.config_entries", ConfigEntry=object)
    add_module(
        "homeassistant.const", PERCENTAGE="%",
        UnitOfEnergy=SimpleNamespace(KILO_WATT_HOUR="kWh"),
        UnitOfMass=SimpleNamespace(KILOGRAMS="kg"),
        UnitOfTemperature=SimpleNamespace(CELSIUS="°C"),
    )
    add_module("homeassistant.core", HomeAssistant=object)
    add_module("homeassistant.helpers.entity", DeviceInfo=dict)
    add_module("homeassistant.helpers.entity_platform", AddEntitiesCallback=object)
    add_module(
        "homeassistant.helpers.update_coordinator",
        CoordinatorEntity=type("CoordinatorEntity", (), {
            "__init__": lambda self, coordinator: setattr(self, "coordinator", coordinator),
        }),
    )
    add_module("bauergroup_hargassnerintegration.coordinator", HargassnerDataUpdateCoordinator=object)
    name = "bauergroup_hargassnerintegration.sensor"
    path = REPO_ROOT / "custom_components" / "bauergroup_hargassnerintegration" / "sensor.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


def boiler_context(firmware="V10_2HAR_n2", language="EN", sensor_set="FULL"):
    """Create the coordinator/config data read by sensor constructors and setup."""
    entry = SimpleNamespace(entry_id="test_boiler", data={
        "firmware": firmware, "language": language, "sensor_set": sensor_set,
    })
    parser = HargassnerMessageParser(firmware)
    coordinator = SimpleNamespace(
        data={"ZK": {"value": 42}, "TK": {"value": 62.5, "unit": "°C"},
              "TVL_1": {"value": 3, "unit": "°C"}, "Störungs Nr": {"value": 1}},
        telnet_client=SimpleNamespace(_parser=parser),
    )
    return entry, coordinator


def test_profiles_start_equal_but_share_no_mutable_tables(monkeypatch):
    """An edit to a nested V10 translation cannot affect the default profile."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "empty_profile", FirmwareDefinitions())
    profile = get_firmware_definitions("empty_profile")
    assert profile == default.DEFINITIONS
    for custom, original in (
        (profile.parameter_descriptions, default.PARAMETER_DESCRIPTIONS),
        (profile.error_codes, default.ERROR_CODES),
    ):
        assert custom is not original
        assert all(custom[key] is not original[key] for key in custom)
    assert profile.parameter_descriptions["ZK"]["enum"] is not default.PARAMETER_DESCRIPTIONS["ZK"]["enum"]
    assert FIRMWARE_DEFINITIONS["V10_2HAR_n2"].parameter_descriptions["Max Anf Kessel"] == {
        "device_class": "temperature",
    }
    assert FIRMWARE_DEFINITIONS["V10_2HAR_n2"].error_codes == {}


@pytest.mark.parametrize("key,labels", [
    ("ZK", [
        "Init", "Aus", "Zündung warten", "Zündung", "Anheizen", "Grundglut",
        "Leistungsbrand", "zu Teillast", "Teillast", "Ausbrand", "Gluterhaltung",
        "Restwärme", "Übertemperatur", "Tür offen", "Tür geschlossen",
        "Rauchfangkehrer", "TÜV", "ABS", "STB", "Hand",
    ]),
    ("PK_ZK", [
        "Init", "Aus", "Schieberost Init", "Start", "Zündung Einschub",
        "Zündung Pause", "Zündung Reduziert", "Leistungsbrand", "Gluterhaltung",
        "Entaschung", "Entaschung Rost", "Entaschung Nachlauf", "Reinigung",
        "Füllen Start", "Füllen", "Hand",
    ]),
    ("Programm", ["Unbekannt", "Aus", "Boiler", "Auto", "Feuerung Aus"]),
    ("PufZustand", ["Gesperrt", "Freigegeben"]),
    ("HKZustand_1", [
        "Aus", "Heizen", "Absenken Rampe", "Absenken", "Tag/Nacht Abschaltung",
        "Sommerabschaltung", "Frostschutz", "Estrich", "Sommerbadheizen", "Hand",
    ]),
    ("FR1 Zustand", ["Unbekannt", "Auto", "Absenken", "Heizen", "Aus", "1x Heizen", "1x Absenken"]),
    ("BoiZustand_1", ["Aus", "Ladung aktiv", "Übertemperatur", "Hand"]),
])
def test_v10_legacy_list_positions_are_wire_values(sensor_module, key, labels):
    """Pin the active legacy MappingFormatter lists, including Init at index zero.

    These lists are a snapshot of telegram.py, not derived from the migrated
    profile, so an offset or swapped log/pellet mapping fails this comparison.
    """
    entry, coordinator = boiler_context(language="DE")
    sensor = sensor_module.HargassnerParameterSensor(coordinator, entry, key)
    enum = get_firmware_definitions("V10_2HAR_n2").parameter_descriptions[key]["enum"]
    assert set(enum) == set(range(len(labels)))
    for code, expected in enumerate(labels):
        coordinator.data[key] = {"value": code}
        assert sensor.native_value == expected
        assert expected in sensor._attr_options
        assert enum[code]["en"]
    assert sensor._attr_device_class == "enum"
    assert sensor._attr_state_class is None
    assert sensor.native_unit_of_measurement is None


@pytest.mark.parametrize("key", [
    "Störung", "RLm_auf", "RLm_zu", "FW Pumpe", "HKP1", "BP1", "PK_RLm_auf", "PK_RLm_zu",
])
@pytest.mark.parametrize("value,expected", [(False, "Inaktiv"), (True, "Aktiv")])
def test_v10_legacy_binary_formatter_uses_parsed_booleans(sensor_module, key, value, expected):
    """Legacy True/False strings become the same labels from native bool values."""
    entry, coordinator = boiler_context(language="DE")
    coordinator.data[key] = {"value": value}
    sensor = sensor_module.HargassnerParameterSensor(coordinator, entry, key)
    assert sensor.native_value == expected
    assert sensor._attr_device_class == "enum"


def test_v10_legacy_migration_keeps_overrides_sparse():
    """Omit duplicate defaults, the unused buffer table, and the non-XML alias."""
    overrides = FIRMWARE_DEFINITIONS["V10_2HAR_n2"]

    def check_differences(values, inherited):
        for key, value in values.items():
            if isinstance(value, dict) and isinstance(inherited.get(key), dict):
                assert value, key
                check_differences(value, inherited[key])
            else:
                assert value != inherited.get(key), (key, value)

    check_differences(overrides.parameter_descriptions, default.PARAMETER_DESCRIPTIONS)
    assert overrides.error_codes == {}
    resolved = get_firmware_definitions("V10_2HAR_n2")
    assert resolved.error_codes["309"] == default.ERROR_CODES["309"]
    assert resolved.error_codes["309"]["de"] == "Nachlegen"
    assert "BoiZustand_1_2" not in resolved.parameter_descriptions
    assert resolved.parameter_descriptions["PuffZustand"].get("enum") is None
    assert set(resolved.parameter_descriptions["PufZustand"]["enum"]) == {0, 1}


def test_v10_legacy_enums_reach_real_parsed_sensor_values(sensor_module):
    """Interpret V10 wire values while preserving full-precision numeric readings."""
    entry, coordinator = boiler_context(language="DE")
    parser = coordinator.telnet_client._parser
    values = ["0"] * parser.expected_length
    for key, value in {
        "ZK": "6", "PK_ZK": "7", "Programm": "3", "PufZustand": "1",
        "HKZustand_1": "2", "FR1 Zustand": "2", "BoiZustand_1": "1",
        "Störungs Nr": "309", "TK": "68.237",
    }.items():
        values[parser.get_parameter_info(key).index] = value
    coordinator.data = parser.parse_message("pm " + " ".join(values))
    state = sensor_module.HargassnerStateSensor(coordinator, entry, "DE", "ZK")
    error = sensor_module.HargassnerErrorSensor(coordinator, entry, "DE", "Störungs Nr")
    temperature = sensor_module.HargassnerParameterSensor(coordinator, entry, "TK")
    assert state.native_value == "Leistungsbrand"
    assert state._attr_name == default.PARAMETER_DESCRIPTIONS["ZK"]["de"]
    assert error.native_value == "Nachlegen"
    assert error._attr_name == default.PARAMETER_DESCRIPTIONS["Störungs Nr"]["sensor_name"]["de"]
    assert temperature.native_value == 68.237
    assert temperature._attr_name == default.PARAMETER_DESCRIPTIONS["TK"]["de"]
    assert isinstance(coordinator.data["ZK"]["value"], int)
    assert default.PARAMETER_DESCRIPTIONS["ZK"]["enum"][6]["de"] == "Übergang LB"


def test_partial_overrides_inherit_parameters_languages_enums_and_errors(monkeypatch):
    """A single nested translation overrides only that field in the default."""
    overrides = FirmwareDefinitions(
        parameter_descriptions={
            "TK": {"de": "Holztemperatur"},
            "ZK": {"enum": {7: {"de": "Holzbrand"}}},
        },
        error_codes={"1": {"de": "Holzkesselfehler"}},
    )
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", overrides)
    resolved = get_firmware_definitions("V10_2HAR_n2")
    assert resolved.parameter_descriptions["TK"] == {
        **default.PARAMETER_DESCRIPTIONS["TK"], "de": "Holztemperatur",
    }
    assert resolved.parameter_descriptions["O2"] == default.PARAMETER_DESCRIPTIONS["O2"]
    assert resolved.parameter_descriptions["ZK"]["de"] == default.PARAMETER_DESCRIPTIONS["ZK"]["de"]
    states = resolved.parameter_descriptions["ZK"]["enum"]
    assert states[7] == {"en": "Full firing", "de": "Holzbrand", "icon": "mdi:fireplace"}
    assert states[1] == default.PARAMETER_DESCRIPTIONS["ZK"]["enum"][1]
    assert resolved.error_codes["1"]["de"] == "Holzkesselfehler"
    assert resolved.error_codes["1"]["en"] == default.ERROR_CODES["1"]["en"]
    assert resolved.error_codes["2"] == default.ERROR_CODES["2"]
    assert overrides.parameter_descriptions["TK"] == {"de": "Holztemperatur"}
    assert overrides.parameter_descriptions["ZK"] == {"enum": {7: {"de": "Holzbrand"}}}
    # Resolved dictionaries must not mutate defaults, overrides, or another result.
    states[7]["de"] = "Temporary change"
    resolved.parameter_descriptions["O2"]["de"] = "Temporary change"
    resolved.error_codes["2"]["en"] = "Temporary change"
    fresh = get_firmware_definitions("V10_2HAR_n2")
    assert fresh.parameter_descriptions["ZK"]["enum"][7]["de"] == "Holzbrand"
    assert fresh.parameter_descriptions["O2"] == default.PARAMETER_DESCRIPTIONS["O2"]
    assert fresh.error_codes["2"] == default.ERROR_CODES["2"]
    assert default.PARAMETER_DESCRIPTIONS["ZK"]["enum"][7]["de"] == "Leistungsbrand"


def test_empty_nested_overrides_inherit_default_enums(monkeypatch):
    """Empty tables do not erase inherited languages or enum states."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={"ZK": {"enum": {}}, "TK": {}},
        error_codes={"1": {}},
    ))
    assert get_firmware_definitions("V10_2HAR_n2") == default.DEFINITIONS


def test_explicit_none_disables_an_inherited_enum(sensor_module, monkeypatch):
    """An intentional enum opt-out differs from omitting the override."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={"ZK": {"enum": None}},
    ))
    entry, coordinator = boiler_context()
    state = sensor_module.HargassnerStateSensor(coordinator, entry, "EN", "ZK")
    assert state.native_value == 42
    assert state._attr_device_class is None
    assert state._enum_labels is None
    assert get_firmware_definitions("V10_2HAR_n2").parameter_descriptions["ZK"]["en"] == "Boiler State"
    assert default.PARAMETER_DESCRIPTIONS["ZK"]["enum"][7]["en"] == "Full firing"


def test_sparse_descriptions_reach_both_sensor_sets(sensor_module, monkeypatch):
    """Inherited translations reach the parser and STANDARD/FULL entity setup."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={"TK": {"de": "Holztemperatur"}},
        error_codes={"1": {"de": "Holzkesselfehler"}},
    ))
    for sensor_set in ("STANDARD", "FULL"):
        for language in ("EN", "DE"):
            entry, coordinator = boiler_context(language=language, sensor_set=sensor_set)
            hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
            entities = []
            asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
            by_id = {entity._attr_unique_id: entity for entity in entities}
            assert by_id["test_boiler_TK"]._attr_name == (
                "Holztemperatur" if language == "DE" else "Boiler Temperature"
            )
            assert by_id["test_boiler_operation"].native_value == (
                "Holzkesselfehler" if language == "DE" else default.ERROR_CODES["1"]["en"]
            )


@pytest.mark.parametrize("firmware", ["V14_1HAR_q1", "unknown", "default"])
def test_unregistered_firmware_uses_default(firmware):
    """Existing and unknown firmware keep the original lookup behavior."""
    assert get_firmware_definitions(firmware) is default.DEFINITIONS
    assert get_firmware_display_name(firmware) == firmware


@pytest.mark.parametrize("display_name", [None, "", "Neo-HV 30 + Nano-PK 20"])
def test_optional_display_name_preserves_version_key(monkeypatch, display_name):
    """Display labels change presentation only and default to the version key."""
    version = "V10_2HAR_n2"
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, version, replace(
        get_firmware_definitions(version), display_name=display_name,
    ))
    assert get_firmware_display_name(version) == (display_name or version)
    assert "V10_2HAR_n2" in load_module("const").FIRMWARE_VERSIONS


def test_parser_preserves_values_and_uses_custom_analog_and_digital_descriptions(custom_profile):
    """Enums change metadata, while raw wire values stay available to callers."""
    custom_profile.parameter_descriptions["Störung"] = {"en": "Custom alarm", "de": "Eigener Alarm"}
    parser = HargassnerMessageParser("V10_2HAR_n2")
    parsed = parser.parse_message("pm 42 " + "0 " * (parser.expected_length - 1))
    assert parsed["ZK"]["value"] == 42
    assert parsed["ZK"]["description"]["enum"][42]["en"] == "Wood burning"
    assert parser.get_parameter_info("TK").description["en"] == "Wood temperature"
    assert parser.get_parameter_info("Störung").description["en"] == "Custom alarm"
    assert HargassnerMessageParser("V14_1HAR_q1").get_parameter_info("TK").description["en"] == "Boiler Temperature"


@pytest.mark.parametrize("language,state,error,temp,mode", [
    ("EN", "Wood burning", "Wood boiler fault", "Wood temperature", "Active"),
    ("DE", "Holzbrand", "Holzkesselfehler", "Holztemperatur", "Aktiv"),
])
@pytest.mark.parametrize("sensor_set", ["STANDARD", "FULL"])
def test_sensor_sets_use_firmware_names_errors_and_enums(
    sensor_module, custom_profile, language, state, error, temp, mode, sensor_set,
):
    """Both sensor sets localize normal names and generic enums per firmware."""
    entry, coordinator = boiler_context(language=language, sensor_set=sensor_set)
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    entities = []
    asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
    by_id = {entity._attr_unique_id: entity for entity in entities}
    state_sensor = by_id["test_boiler_state"]
    assert state_sensor._attr_name == ("Holzkesselzustand" if language == "DE" else "Wood boiler state")
    assert state_sensor.native_value == state
    assert state_sensor.icon == "mdi:fire"
    assert state in state_sensor._attr_options
    assert by_id["test_boiler_operation"].native_value == error
    assert by_id["test_boiler_TK"]._attr_name == temp
    assert by_id["test_boiler_TK"].native_value == 62.5
    mode_sensor = by_id["test_boiler_TVL_1"]
    assert mode_sensor.native_value == mode
    assert mode_sensor._attr_device_class == "enum"
    assert mode_sensor._attr_state_class is None
    assert mode_sensor.native_unit_of_measurement is None


def test_unknown_enum_and_error_options_are_local(sensor_module, custom_profile):
    """Unknown values are valid HA options without modifying shared lookups."""
    entry, coordinator = boiler_context()
    first = sensor_module.HargassnerStateSensor(coordinator, entry, "EN", "ZK")
    second = sensor_module.HargassnerStateSensor(coordinator, entry, "EN", "ZK")
    coordinator.data["ZK"]["value"] = -1
    assert first.native_value == "Unknown"
    assert "Unknown" in first._attr_options
    assert "Unknown" not in second._attr_options
    assert -1 not in custom_profile.parameter_descriptions["ZK"]["enum"]
    error = sensor_module.HargassnerErrorSensor(coordinator, entry, "EN", "Störungs Nr")
    coordinator.data["Störungs Nr"]["value"] = 99999
    assert error.native_value == "Error 99999"
    assert "Error 99999" in error._attr_options
    assert "99999" not in custom_profile.error_codes


def test_removing_enum_restores_raw_parameter(sensor_module, custom_profile):
    """Removing an enum mapping keeps normal translations and numeric behavior."""
    del custom_profile.parameter_descriptions["TVL_1"]["enum"]
    entry, coordinator = boiler_context()
    sensor = sensor_module.HargassnerParameterSensor(
        coordinator, entry, "TVL_1",
    )
    assert sensor.native_value == 3
    assert sensor.native_unit_of_measurement == "°C"
    assert sensor._attr_device_class == "temperature"
    assert sensor._attr_state_class == "measurement"


@pytest.mark.parametrize("sensor_set", ["STANDARD", "FULL"])
def test_sensor_metadata_controls_classification_and_standard_membership(
    sensor_module, monkeypatch, sensor_set,
):
    """Sensor type, icon, and inclusion come from metadata rather than names/units."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={
            "TK": {"standard": False},
            "Leistung": {
                "device_class": None, "state_class": "total_increasing", "icon": "mdi:counter",
            },
            "HKZustand_1": {"standard": True, "state_class": None},
        },
    ))
    entry, coordinator = boiler_context(sensor_set=sensor_set)
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    entities = []
    asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
    by_id = {entity._attr_unique_id: entity for entity in entities}
    assert ("test_boiler_TK" in by_id) == (sensor_set == "FULL")
    assert by_id["test_boiler_Leistung"]._attr_device_class is None
    assert by_id["test_boiler_Leistung"]._attr_state_class == "total_increasing"
    assert by_id["test_boiler_Leistung"].icon == "mdi:counter"
    assert by_id["test_boiler_HKZustand_1"]._attr_state_class is None


@pytest.mark.parametrize("sensor_set", ["STANDARD", "FULL"])
def test_metadata_selects_specialized_source_parameters(sensor_module, monkeypatch, sensor_set):
    """Firmware can move the dedicated boiler and error entities to other keys."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={
            "ZK": {"sensor_type": "parameter"},
            "Störungs Nr": {"sensor_type": "parameter"},
            "PK_ZK": {
                "en": "Pellet boiler state", "de": "Pelletkesselzustand",
                "sensor_type": "boiler_state", "entity_id_suffix": "state",
                "enum": {42: {"en": "Pellets burning", "de": "Pelletbrand", "icon": "mdi:fire"}},
            },
            "PK_Programm": {
                "sensor_type": "error", "entity_id_suffix": "operation",
                "sensor_name": {"en": "Pellet boiler status", "de": "Pelletkesselstatus"},
                "icon": "mdi:alert", "ok_icon": "mdi:check",
            },
        },
    ))
    entry, coordinator = boiler_context(sensor_set=sensor_set)
    coordinator.data["PK_ZK"] = {"value": 42}
    coordinator.data["PK_Programm"] = {"value": 1}
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    entities = []
    asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
    ids = [entity._attr_unique_id for entity in entities]
    assert len(ids) == len(set(ids))
    by_id = {entity._attr_unique_id: entity for entity in entities}
    assert by_id["test_boiler_state"].native_value == "Pellets burning"
    assert by_id["test_boiler_state"].icon == "mdi:fire"
    assert by_id["test_boiler_operation"]._attr_name == "Pellet boiler status"
    assert by_id["test_boiler_operation"].native_value == default.ERROR_CODES["1"]["en"]
    if sensor_set == "FULL":
        assert by_id["test_boiler_PK_ZK"].native_value == "Pellets burning"
        assert by_id["test_boiler_PK_Programm"].native_value == default.ERROR_CODES["1"]["en"]
    coordinator.data["PK_Programm"]["value"] = 0
    assert by_id["test_boiler_operation"].native_value == "OK"
    assert by_id["test_boiler_operation"].icon == "mdi:check"


def test_default_metadata_preserves_standard_entity_ids(sensor_module):
    """Moving classifications into metadata retains all original STANDARD IDs."""
    entry, coordinator = boiler_context(firmware="V14_1HAR_q1", sensor_set="STANDARD")
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    entities = []
    asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
    expected = {
        "TK", "TKsoll", "TRG", "BRT", "Leistung", "Effizienz", "O2", "SZist",
        "TPo", "TPm", "TPu", "Puff Füllgrad", "Puffer_soll oben", "Puffer_soll unten",
        "TVL_1", "TVLs_1", "TRL", "TB1", "TBs_1", "Taus", "Lagerstand", "Verbrauchszähler",
        "connection", "state", "operation", "energy",
    }
    by_id = {entity._attr_unique_id: entity for entity in entities}
    assert set(by_id) == {f"test_boiler_{key}" for key in expected}
    assert by_id["test_boiler_TK"]._attr_device_class == "temperature"
    assert by_id["test_boiler_TK"]._attr_state_class == "measurement"
    assert by_id["test_boiler_Lagerstand"]._attr_state_class == "total"
    assert by_id["test_boiler_Verbrauchszähler"]._attr_state_class == "total_increasing"


def test_additional_dedicated_entity_has_distinct_full_mode_id(sensor_module, monkeypatch):
    """An additional state role has a safe default ID beside its FULL parameter."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={"PK_ZK": {"sensor_type": "boiler_state"}},
    ))
    entry, coordinator = boiler_context()
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    entities = []
    asyncio.run(sensor_module.async_setup_entry(hass, entry, entities.extend))
    ids = [entity._attr_unique_id for entity in entities]
    assert len(ids) == len(set(ids))
    assert "test_boiler_PK_ZK_state" in ids
    assert "test_boiler_PK_ZK" in ids


@pytest.mark.parametrize("description,message", [
    ({"sensor_type": "unsupported"}, "Unknown sensor_type"),
    ({"sensor_type": "boiler_state", "entity_id_suffix": "state"}, "duplicate entity IDs"),
])
def test_invalid_role_metadata_reports_configuration_error(
    sensor_module, monkeypatch, description, message,
):
    """Invalid roles or colliding dedicated IDs fail with a concrete remedy."""
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, "V10_2HAR_n2", FirmwareDefinitions(
        parameter_descriptions={"PK_ZK": description},
    ))
    entry, coordinator = boiler_context()
    hass = SimpleNamespace(data={"bauergroup_hargassnerintegration": {entry.entry_id: coordinator}})
    with pytest.raises(ValueError, match=message):
        asyncio.run(sensor_module.async_setup_entry(hass, entry, lambda entities: None))


@pytest.mark.parametrize("step", ["user", "init"])
def test_firmware_forms_serialize_labels_and_accept_version_keys(sensor_module, monkeypatch, step):
    """Real setup/options schemas expose display labels without changing values.

    Schema libraries are optional test dependencies; HA imports use the same
    lightweight stubs as the sensor tests.
    """
    vol = pytest.importorskip("voluptuous")
    serializer = pytest.importorskip("voluptuous_serialize")
    flow_base = type("FlowBase", (), {
        "__init_subclass__": classmethod(lambda cls, **kwargs: None),
        "async_show_form": lambda self, **kwargs: kwargs,
    })
    config_entries = sys.modules["homeassistant.config_entries"]
    monkeypatch.setattr(config_entries, "ConfigFlow", flow_base, raising=False)
    monkeypatch.setattr(config_entries, "OptionsFlow", flow_base, raising=False)
    monkeypatch.setattr(sys.modules["homeassistant"], "config_entries", config_entries, raising=False)
    monkeypatch.setattr(sys.modules["homeassistant.core"], "callback", lambda fn: fn, raising=False)
    for name, attributes in (
        ("homeassistant.data_entry_flow", {"FlowResult": dict}),
        ("homeassistant.helpers.config_validation", {"string": str}),
    ):
        module = ModuleType(name)
        module.__dict__.update(attributes)
        monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.setattr(sys.modules["homeassistant.const"], "CONF_HOST", "host", raising=False)
    version = "V10_2HAR_n2"
    label = "Neo-HV 30 + Nano-PK 20"
    monkeypatch.setitem(FIRMWARE_DEFINITIONS, version, replace(
        get_firmware_definitions(version), display_name=label,
    ))
    name = "bauergroup_hargassnerintegration.config_flow"
    path = REPO_ROOT / "custom_components" / "bauergroup_hargassnerintegration" / "config_flow.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    if step == "user":
        form = asyncio.run(module.HargassnerConfigFlow().async_step_user())
    else:
        flow = module.HargassnerOptionsFlow()
        flow.config_entry = boiler_context()[0]
        form = asyncio.run(flow.async_step_init())
    schema = form["data_schema"]
    firmware_field = next(field for field in serializer.convert(schema) if field["name"] == "firmware")
    assert (version, label) in firmware_field["options"]
    assert ("V14_1HAR_q1", "V14_1HAR_q1") in firmware_field["options"]
    assert schema({"host": "192.0.2.1", "firmware": version} if step == "user" else {"firmware": version})["firmware"] == version
    with pytest.raises(vol.Invalid):
        schema({"host": "192.0.2.1", "firmware": label} if step == "user" else {"firmware": label})
