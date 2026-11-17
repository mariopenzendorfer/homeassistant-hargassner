"""V10_2HAR_n2 differences from the default profile.

Migrated from hargassner_telnet/telegram.py's active formatter bindings. Enum
codes retain the original zero-based list positions and German labels. English
translations are added here; unused buffer states and non-XML aliases are omitted.
Names inherit defaults when their meaning matches; only missing names and
semantic corrections are retained. Parsing keeps native numeric values.
"""

from typing import Final

from ..parameter_description import ParameterDescription
from .definitions import FirmwareDefinitions

# None or an empty string displays the firmware version key in selectors.
DISPLAY_NAME: Final[str | None] = "Neo-HV 30 + Nano-PK 20"

PARAMETER_DESCRIPTIONS: Final[dict[str, ParameterDescription]] = {
    "Max Anf Kessel": {
        "device_class": "temperature",
    },
    "ZK": {
        "en": "HV State",
        "de": "HV Status",
        "enum": {
            0: {"en": "Initializing", "de": "Init"},
            2: {"en": "Waiting for ignition", "de": "Zündung warten"},
            3: {"en": "Ignition", "de": "Zündung"},
            4: {"en": "Heating up", "de": "Anheizen"},
            5: {"en": "Ember bed", "de": "Grundglut"},
            6: {"en": "Full firing", "de": "Leistungsbrand"},
            7: {"en": "Transition to partial load", "de": "zu Teillast"},
            8: {"en": "Partial load", "de": "Teillast"},
            9: {"en": "Burnout", "de": "Ausbrand"},
            10: {"en": "Ember preservation", "de": "Gluterhaltung"},
            11: {"en": "Residual heat", "de": "Restwärme"},
            12: {"en": "Overtemperature", "de": "Übertemperatur"},
            13: {"en": "Door open", "de": "Tür offen"},
            14: {"en": "Door closed", "de": "Tür geschlossen"},
            15: {"en": "Chimney sweep", "de": "Rauchfangkehrer"},
            16: {"en": "TÜV", "de": "TÜV"},
            17: {"en": "ABS", "de": "ABS"},
            18: {"en": "STB", "de": "STB"},
            19: {"en": "Manual", "de": "Hand"},
        },
    },
    "O2_soll": {
        "en": "HV O2 Setpoint",
        "de": "HV O2 soll",
    },
    "Programm": {
        "enum": {
            0: {"en": "Unknown", "de": "Unbekannt"},
            1: {"en": "Off", "de": "Aus"},
            2: {"en": "Boiler", "de": "Boiler"},
            3: {"en": "Automatic", "de": "Auto"},
            4: {"en": "Firing off", "de": "Feuerung Aus"},
        },
    },
    "PufZustand": {
        "en": "PK Enable Status",
        "de": "PK Freigabestatus",
        "enum": {
            0: {"en": "Blocked", "de": "Gesperrt"},
            1: {"en": "Enabled", "de": "Freigegeben"},
        },
    },
    "HKZustand_1": {
        "enum": {
            0: {"en": "Off", "de": "Aus"},
            1: {"en": "Heating", "de": "Heizen"},
            2: {"en": "Setback ramp", "de": "Absenken Rampe"},
            3: {"en": "Setback", "de": "Absenken"},
            4: {"en": "Day/night shutdown", "de": "Tag/Nacht Abschaltung"},
            5: {"en": "Summer shutdown", "de": "Sommerabschaltung"},
            6: {"en": "Frost protection", "de": "Frostschutz"},
            7: {"en": "Screed drying", "de": "Estrich"},
            8: {"en": "Summer bathroom heating", "de": "Sommerbadheizen"},
            9: {"en": "Manual", "de": "Hand"},
        },
    },
    "FR1 Zustand": {
        "en": "HC1 Mode",
        "de": "HK1 Modus",
        "enum": {
            0: {"en": "Unknown", "de": "Unbekannt"},
            1: {"en": "Automatic", "de": "Auto"},
            2: {"en": "Setback", "de": "Absenken"},
            3: {"en": "Heating", "de": "Heizen"},
            4: {"en": "Off", "de": "Aus"},
            5: {"en": "Heating once", "de": "1x Heizen"},
            6: {"en": "Setback once", "de": "1x Absenken"},
        },
    },
    "BoiZustand_1": {
        "enum": {
            0: {"en": "Off", "de": "Aus"},
            1: {"en": "Charging active", "de": "Ladung aktiv"},
            2: {"en": "Overtemperature", "de": "Übertemperatur"},
            3: {"en": "Manual", "de": "Hand"},
        },
    },
    "PK_ZK": {
        "en": "PK State",
        "de": "PK Status",
        "enum": {
            0: {"en": "Initializing", "de": "Init"},
            1: {"en": "Off", "de": "Aus"},
            2: {"en": "Grate initialization", "de": "Schieberost Init"},
            3: {"en": "Start", "de": "Start"},
            4: {"en": "Ignition feed", "de": "Zündung Einschub"},
            5: {"en": "Ignition pause", "de": "Zündung Pause"},
            6: {"en": "Reduced ignition", "de": "Zündung Reduziert"},
            7: {"en": "Full firing", "de": "Leistungsbrand"},
            8: {"en": "Ember preservation", "de": "Gluterhaltung"},
            9: {"en": "Ash removal", "de": "Entaschung"},
            10: {"en": "Grate ash removal", "de": "Entaschung Rost"},
            11: {"en": "Ash removal run-on", "de": "Entaschung Nachlauf"},
            12: {"en": "Cleaning", "de": "Reinigung"},
            13: {"en": "Starting filling", "de": "Füllen Start"},
            14: {"en": "Filling", "de": "Füllen"},
            15: {"en": "Manual", "de": "Hand"},
        },
        "device_class": None,
        "state_class": None,
        "sensor_type": "boiler_state",
        "entity_id_suffix": "pk_state",
        "icon": "mdi:fireplace-off"
    },
    "O2": {
        "en": "HV O2",
        "de": "HV O2",
    },
    "O2soll": {
        "en": "HV O2 Setpoint",
        "de": "HV O2 soll",
    },
    "PK_O2": {
        "en": "PK O2",
        "de": "PK O2",
    },
    "PK_O2soll": {
        "en": "PK O2 Setpoint",
        "de": "PK O2 soll",
    },
    "PK_TKsoll": {
        "en": "PK Temperature Setpoint",
        "de": "PK Kesseltemperatur soll",
    },
    "PK_TRL": {
        "en": "PK Return Temperature",
        "de": "PK Rücklauftemperatur",
    },
    "PK_TRLsoll": {
        "en": "PK Return Temperature Setpoint",
        "de": "PK Rücklauftemperatur soll",
    },
    "PK_SZ": {
        "en": "PK Draft",
        "de": "PK Saugzug",
    },
    "PK_SZs": {
        "en": "PK Draft Setpoint",
        "de": "PK Saugzug soll",
    },
    "PK_Leistung": {
        "en": "PK Output",
        "de": "PK Leistung",
    },
    "PK_Programm": {
        "en": "PK Mode",
        "de": "PK Modus",
    },
    "PK_AUPSoll": {
        "en": "Pellet Suction Unit Position Setpoint",
        "de": "Pellets Saugeinheit Position soll",
    },
    "PK_AUPIst": {
        "en": "Pellet Suction Unit Position",
        "de": "Pellets Saugeinheit Position",
    },
    "PK_AUPStrom": {
        "en": "Pellet Suction Unit Motor Current",
        "de": "Pellets Saugeinheit Motorstrom",
    },
    "Störung": {
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "RLm_auf": {
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "RLm_zu": {
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "FW Pumpe": {
        "en": "PK Pump",
        "de": "PK Pumpe",
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "HKP1": {
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "BP1": {
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "PK_RLm_auf": {
        "en": "PK Return Mixer Open",
        "de": "PK Rücklaufmischer auf",
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
    "PK_RLm_zu": {
        "en": "PK Return Mixer Close",
        "de": "PK Rücklaufmischer zu",
        "enum": {
            0: {"en": "Inactive", "de": "Inaktiv"},
            1: {"en": "Active", "de": "Aktiv"},
        },
    },
}

# Notification 309 (Nachlegen) already matches the default error translation.
ERROR_CODES: Final[dict[str, dict[str, str]]] = {}

DEFINITIONS: Final = FirmwareDefinitions(PARAMETER_DESCRIPTIONS, ERROR_CODES, DISPLAY_NAME)
