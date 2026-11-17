"""Constants for the Hargassner Integration."""
from typing import Final

# Integration domain
DOMAIN: Final = "bauergroup_hargassnerintegration"

# Configuration keys
CONF_FIRMWARE: Final = "firmware"
CONF_DEVICE_NAME: Final = "device_name"
CONF_LANGUAGE: Final = "language"
CONF_SENSOR_SET: Final = "sensor_set"
CONF_PELLET_ENERGY: Final = "pellet_energy_kwh_per_kg"
CONF_EFFICIENCY: Final = "efficiency_percent"

# Language options
LANGUAGE_EN: Final = "EN"
LANGUAGE_DE: Final = "DE"

# Sensor set options
SENSOR_SET_STANDARD: Final = "STANDARD"
SENSOR_SET_FULL: Final = "FULL"

# Telnet settings
TELNET_PORT: Final = 23
TELNET_TIMEOUT: Final = 10.0
TELNET_RECONNECT_DELAY: Final = 5.0
TELNET_BUFFER_SIZE: Final = 65536
TELNET_DATA_STALENESS_TIMEOUT: Final = 60.0  # Reconnect if no data for this many seconds

# Firmware versions
# IMPORTANT: Keep this list in sync with FIRMWARE_TEMPLATES in firmware_templates.py
# When adding a new firmware version:
# 1. Add the XML template to FIRMWARE_TEMPLATES in firmware_templates.py
# 2. Add the version string here
# 3. Optionally register a dedicated lookup profile in firmware_versions/__init__.py
# 4. Run tools/parameter_validator.py to verify consistency
FIRMWARE_VERSIONS: Final = [
    "V14_1HAR_q1",  # Nano.2, original layout - unchanged since the first release
    "V14_1HAR_q1_nano2_32",  # same firmware string, manufacturer DAQ channel order
    "V14_1HAR_q1_nanopkplus",  # Nano PK Plus on V14.1HAR.q (Issue #21)
    "V14_1HAR_q1_solar",  # Nano.2 20 + Solar/3HK extension (Issue #11)
    "V14_0HAR_q",
    "V14_0m5",  # Classic Lambda 40L-60L
    "V14_0d",  # HSV/CL 9-60KW (Issue #14)
    "V40_0HAR_az15",  # Nano 65
    "V14_1HAR_q_nano2_zuspuf_aup3",  # Nano.2(.3) 15 + auxiliary buffer/AUP (Issue #17)
    "V10_2HAR_n2", # Neo-HV 30 + Nano-PK 20
]

# Energy calculation defaults
DEFAULT_PELLET_ENERGY: Final = 4.8  # kWh per kg (Heizwert)
DEFAULT_EFFICIENCY: Final = 90  # % Wirkungsgrad
