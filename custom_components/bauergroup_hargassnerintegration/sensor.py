"""Sensor platform for Hargassner Pellet Boiler."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfMass,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_DEVICE_NAME,
    CONF_EFFICIENCY,
    CONF_FIRMWARE,
    CONF_LANGUAGE,
    CONF_PELLET_ENERGY,
    CONF_SENSOR_SET,
    DEFAULT_EFFICIENCY,
    DEFAULT_PELLET_ENERGY,
    DOMAIN,
    SENSOR_SET_FULL,
)
from .coordinator import HargassnerDataUpdateCoordinator
from .firmware_versions import get_firmware_definitions
from .firmware_versions.definitions import FirmwareDefinitions

# Bidirectional mapping for parameter name variants (umlauts vs ASCII-normalized)
# Some firmware templates use German umlauts, others use ASCII replacements
_PARAM_NAME_ALIASES: dict[str, str] = {
    "Verbrauchszähler": "Verbrauchszaehler",
    "Verbrauchszaehler": "Verbrauchszähler",
    "Störungs Nr": "Storungs Nr",
    "Storungs Nr": "Störungs Nr",
    "Stoerungs Nr": "Störungs Nr",
    "Puff Füllgrad": "Puff Fuellgrad",
    "Puff Fuellgrad": "Puff Füllgrad",
}


def _get_param_data(data: dict, key: str) -> dict | None:
    """Get parameter data with umlaut-normalized fallback."""
    result = data.get(key)
    if result is not None:
        return result
    alt_key = _PARAM_NAME_ALIASES.get(key)
    if alt_key:
        return data.get(alt_key)
    return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create entities using the selected firmware's declared sensor metadata."""
    coordinator: HargassnerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    sensor_set = entry.data.get(CONF_SENSOR_SET, "STANDARD")
    language = entry.data.get(CONF_LANGUAGE, "EN")
    definitions = get_firmware_definitions(entry.data.get(CONF_FIRMWARE, "V14_1HAR_q1"))

    # Connection and calculated energy are integration-level entities.
    entities: list[SensorEntity] = [
        HargassnerConnectionSensor(coordinator, entry, language, definitions=definitions),
        HargassnerEnergySensor(coordinator, entry, language, definitions=definitions),
    ]

    # Profiles select the source parameters for dedicated state/error entities.
    for key, description in definitions.parameter_descriptions.items():
        sensor_type = description.get("sensor_type", "parameter")
        if sensor_type == "boiler_state":
            entities.append(HargassnerStateSensor(
                coordinator, entry, language, key, definitions=definitions
            ))
        elif sensor_type == "error":
            entities.append(HargassnerErrorSensor(
                coordinator, entry, language, key, definitions=definitions
            ))
        elif sensor_type != "parameter":
            raise ValueError(f"Unknown sensor_type {sensor_type!r} for parameter {key!r}")

    if sensor_set == SENSOR_SET_FULL:
        # Preserve FULL parameter entities, including their existing unique IDs.
        parameter_keys = [p.name for p in coordinator.telnet_client._parser.parameters]
    else:
        parameter_keys = [
            key for key, description in definitions.parameter_descriptions.items()
            if description.get("standard", False)
        ]

    for key in parameter_keys:
        entities.append(HargassnerParameterSensor(coordinator, entry, key, definitions=definitions))

    entity_ids = [entity._attr_unique_id for entity in entities]
    if len(entity_ids) != len(set(entity_ids)):
        raise ValueError(
            "Firmware sensor metadata produces duplicate entity IDs; "
            "use distinct entity_id_suffix values for dedicated entities"
        )
    async_add_entities(entities)


class HargassnerBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Hargassner sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        # Resolve per boiler, so multiple firmware versions can coexist.
        self._definitions = definitions if definitions is not None else get_firmware_definitions(
            entry.data.get(CONF_FIRMWARE, "V14_1HAR_q1")
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data.get(CONF_DEVICE_NAME, "Hargassner Boiler"),
            manufacturer="Hargassner",
            model="Nano-PK",
            sw_version=entry.data.get("firmware", "Unknown"),
            configuration_url=f"http://{entry.data.get('host', '')}",
        )

    def _configure_parameter_enum(self, key: str, language: str) -> None:
        """Build entity-local options from a parameter's firmware enum mapping."""
        self._enum_language = language.lower()
        self._enum_labels = self._definitions.parameter_descriptions.get(key, {}).get("enum")
        if self._enum_labels is not None:
            # Deduplicate labels; multiple wire values may describe the same state.
            self._attr_options = list(
                dict.fromkeys(
                    labels.get(self._enum_language, labels["en"])
                    for labels in self._enum_labels.values()
                )
            )
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_state_class = None

    def _parameter_enum_value(self, value: Any) -> str:
        """Translate a wire value, retaining unknown states as valid enum options."""
        labels = self._enum_labels.get(value, {})
        fallback = "Unbekannt" if self._enum_language == "de" else "Unknown"
        label = labels.get(self._enum_language, labels.get("en", fallback))
        if label not in self._attr_options:
            self._attr_options.append(label)
        return label


class HargassnerConnectionSensor(HargassnerBaseSensor):
    """Sensor representing connection status."""

    _attr_icon = "mdi:network-outline"

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        language: str,
        *,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Initialize connection sensor."""
        super().__init__(coordinator, entry, definitions)
        self._attr_name = "Connection" if language.upper() == "EN" else "Verbindung"
        self._attr_unique_id = f"{entry.entry_id}_connection"
        self._language = language

    @property
    def native_value(self) -> str:
        """Return connection state."""
        if self.coordinator.telnet_client.connected:
            return "Verbunden" if self._language.upper() == "DE" else "Connected"
        return "Getrennt" if self._language.upper() == "DE" else "Disconnected"

    @property
    def icon(self) -> str:
        """Return icon based on connection state."""
        if self.coordinator.telnet_client.connected:
            return "mdi:network-outline"
        return "mdi:network-off-outline"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        stats = self.coordinator.telnet_client.statistics
        return {
            "messages_received": stats.get("messages_received", 0),
            "messages_parsed": stats.get("messages_parsed", 0),
            "parse_errors": stats.get("parse_errors", 0),
            "reconnections": stats.get("reconnections", 0),
            "last_error": stats.get("last_error"),
            "last_update": self.coordinator.telnet_client.last_update,
            # Template fit: if these two differ, the selected firmware template does
            # not match this boiler and values may land in the wrong entities
            "firmware_template": self._entry.data.get("firmware"),
            "expected_length": stats.get("expected_length", 0),
            "last_message_length": stats.get("last_message_length", 0),
        }


class HargassnerParameterSensor(HargassnerBaseSensor):
    """Display one wire parameter according to its firmware's declared metadata."""

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        param_key: str,
        *,
        language: str | None = None,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Apply the resolved profile's parameter metadata.

        XML units remain authoritative. Enum and error handling suppress numeric
        units/state classes because Home Assistant requires categorical metadata.
        """
        super().__init__(coordinator, entry, definitions)
        self._param_key = param_key
        self._language = (language or entry.data.get(CONF_LANGUAGE, "EN")).lower()
        self._description = self._definitions.parameter_descriptions.get(param_key, {})
        self._sensor_type = self._description.get("sensor_type", "parameter")
        self._attr_name = self._description.get(
            self._language, self._description.get("en", param_key)
        )
        self._attr_unique_id = f"{entry.entry_id}_{param_key}"
        self._attr_device_class = self._description.get("device_class")
        self._attr_state_class = self._description.get("state_class")
        self._attr_icon = self._description.get("icon")
        self._configure_parameter_enum(param_key, self._language)

        if self._sensor_type == "error":
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_state_class = None
            self._attr_options = list(dict.fromkeys(
                ["OK"] + [err[self._language] for err in self._definitions.error_codes.values()]
            ))

    @property
    def native_value(self) -> float | int | str | None:
        """Return a raw value, enum label, or error translation as declared."""
        if self._sensor_type == "error":
            return self._error_value()
        param_data = _get_param_data(self.coordinator.data, self._param_key)
        if param_data:
            value = param_data.get("value")
            if value is not None and self._enum_labels is not None:
                return self._parameter_enum_value(value)
            return value
        return None

    def _error_value(self) -> str:
        """Translate the selected error parameter and keep unknown options local."""
        param_data = _get_param_data(self.coordinator.data, self._param_key)
        if not param_data:
            return "OK"
        error_code = str(int(param_data.get("value", 0)))
        if error_code == "0":
            return "OK"
        labels = self._definitions.error_codes.get(error_code)
        if labels:
            return labels[self._language]
        label = f"Fehler {error_code}" if self._language == "de" else f"Error {error_code}"
        if label not in self._attr_options:
            self._attr_options.append(label)
        return label

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Use the XML unit for ordinary parameters; categorical sensors have none."""
        if self._enum_labels is not None or self._sensor_type == "error":
            return None
        param_data = _get_param_data(self.coordinator.data, self._param_key)
        if param_data and param_data.get("unit"):
            unit = param_data["unit"]
            if unit == "°C":
                return UnitOfTemperature.CELSIUS
            if unit == "%":
                return PERCENTAGE
            if unit == "kg":
                return UnitOfMass.KILOGRAMS
            return unit
        return None

    @property
    def icon(self) -> str | None:
        """Read icons from profile metadata, including enum values and OK status."""
        if self._sensor_type == "error" and self.native_value == "OK":
            return self._description.get("ok_icon", self._attr_icon)
        param_data = _get_param_data(self.coordinator.data, self._param_key)
        if self._enum_labels is not None and param_data:
            labels = self._enum_labels.get(param_data.get("value"), {})
            return labels.get("icon", self._attr_icon)
        return self._attr_icon


class HargassnerStateSensor(HargassnerParameterSensor):
    """Preserve the dedicated state entity's identity using a profile-selected key."""

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        language: str,
        param_key: str,
        *,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Reuse generic parameter behavior with the declared dedicated entity ID."""
        super().__init__(coordinator, entry, param_key, language=language, definitions=definitions)
        suffix = self._description.get("entity_id_suffix", f"{param_key}_state")
        self._attr_unique_id = f"{entry.entry_id}_{suffix}"


class HargassnerErrorSensor(HargassnerParameterSensor):
    """Preserve the dedicated error entity's identity using a profile-selected key."""

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        language: str,
        param_key: str,
        *,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Reuse declared error handling and optional dedicated translated names."""
        super().__init__(coordinator, entry, param_key, language=language, definitions=definitions)
        names = self._description.get("sensor_name", {})
        self._attr_name = names.get(self._language, names.get("en", self._attr_name))
        suffix = self._description.get("entity_id_suffix", f"{param_key}_operation")
        self._attr_unique_id = f"{entry.entry_id}_{suffix}"


class HargassnerEnergySensor(HargassnerBaseSensor):
    """Sensor for energy consumption calculated from pellet usage."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_icon = "mdi:radiator"

    def __init__(
        self,
        coordinator: HargassnerDataUpdateCoordinator,
        entry: ConfigEntry,
        language: str,
        *,
        definitions: FirmwareDefinitions | None = None,
    ) -> None:
        """Initialize energy sensor."""
        super().__init__(coordinator, entry, definitions)
        self._attr_name = "Heat Output" if language.upper() == "EN" else "Wärmemenge"
        self._attr_unique_id = f"{entry.entry_id}_energy"
        self._language = language
        self._entry = entry

    @property
    def native_value(self) -> float | None:
        """Return heat output in kWh (calculated from pellet consumption with efficiency)."""
        pellet_data = _get_param_data(self.coordinator.data, "Verbrauchszähler")
        if pellet_data:
            try:
                pellets_kg = float(pellet_data.get("value", 0))

                # Get configuration values
                pellet_energy = self._entry.data.get(CONF_PELLET_ENERGY, DEFAULT_PELLET_ENERGY)
                efficiency = self._entry.data.get(CONF_EFFICIENCY, DEFAULT_EFFICIENCY)

                # Calculate: kg * kWh/kg * efficiency%
                return pellets_kg * pellet_energy * (efficiency / 100.0)
            except (ValueError, TypeError):
                pass
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        pellet_energy = self._entry.data.get(CONF_PELLET_ENERGY, DEFAULT_PELLET_ENERGY)
        efficiency = self._entry.data.get(CONF_EFFICIENCY, DEFAULT_EFFICIENCY)

        return {
            "pellet_energy_kwh_per_kg": pellet_energy,
            "efficiency_percent": efficiency,
            "calculation": f"{pellet_energy} kWh/kg × {efficiency}% efficiency",
        }
