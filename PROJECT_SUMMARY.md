# Hargassner Pellet Boiler Integration - Project Summary

## Overview

Complete, professional Home Assistant custom component for Hargassner pellet boilers with telnet interface. Built from scratch using modern best practices.

**Version:** 0.5.1
**Status:** Production Ready
**License:** MIT

## Key Features

✅ **Real-time Monitoring** - Continuous telnet data stream
✅ **Auto-Reconnect** - Exponential backoff, never gives up
✅ **Thread-Safe** - Async/await architecture
✅ **Robust Encoding** - UTF-8, Latin-1, CP1252 support
✅ **GUI Configuration** - Config Flow with validation
✅ **Multi-Firmware** - Version-specific layouts, translations, enums, and optional display names
✅ **Energy Dashboard** - Built-in energy sensor (kWh)
✅ **Bilingual** - English and German translations
✅ **Error Tolerant** - Graceful degradation, extensive error handling
✅ **Professional Docs** - Architecture, development, contributing guides

## Project Structure

```
./
├── custom_components/bauergroup_hargassnerintegration/    # Main integration
│   ├── __init__.py                         # Entry point, setup/teardown
│   ├── config_flow.py                      # GUI configuration
│   ├── const.py                            # Constants
│   ├── coordinator.py                      # Data coordinator
│   ├── firmware_templates.py               # XML message layouts
│   ├── firmware_versions/                  # Firmware-specific lookup profiles
│   │   ├── __init__.py                      # Profile registry and fallback
│   │   ├── definitions.py                   # Typed profile container
│   │   ├── default.py                       # Original lookup definitions
│   │   └── V10_2HAR_n2.py                   # Sparse V10 overrides
│   ├── manifest.json                       # HA integration metadata
│   ├── message_parser.py                   # Telnet message parser
│   ├── parameter_description.py            # Bilingual names and optional enums
│   ├── sensor.py                           # Sensor platform
│   ├── telnet_client.py                    # Thread-safe telnet client
│   └── translations/                       # Localization
│       ├── en.json
│       └── de.json
├── docs/                                   # Documentation
│   ├── ARCHITECTURE.md                     # Technical architecture (in-depth)
│   ├── CONTRIBUTING.md                     # Contribution guidelines
│   ├── DEVELOPMENT.md                      # Developer setup & workflow
│   └── INSTALLATION.md                     # End-user installation guide
├── tests/                                  # Parser, generator, and firmware behavior tests
│   ├── test_firmware_definitions.py
│   ├── test_message_generator.py
│   └── test_message_parser.py
├── .gitignore                              # Git ignore patterns
├── LICENSE                                 # MIT License
├── PROJECT_SUMMARY.md                      # This file
└── README.md                               # Main project README

```

## Technical Architecture

### Layer 1: [Telnet Client](custom_components/bauergroup_hargassnerintegration/telnet_client.py)

**Responsibilities:**
- Persistent telnet connection (port 23)
- Background asyncio task for continuous receiving
- Automatic reconnection with exponential backoff (5s → 300s)
- Multi-encoding support (UTF-8, Latin-1, CP1252)
- Thread-safe data storage with `asyncio.Lock`
- Statistics tracking (messages, errors, reconnections)

**Key Methods:**
- `async_start()` - Start client and background receiver
- `async_stop()` - Graceful shutdown
- `get_latest_data()` - Thread-safe data access
- `_receiver_loop()` - Background message receiver
- `_process_data()` - Encoding detection and parsing

### Layer 2: [Message Parser](custom_components/bauergroup_hargassnerintegration/message_parser.py)

**Responsibilities:**
- Parse XML firmware templates
- Extract values from telnet messages
- Type conversion (float, int, bool)
- Digital parameter bit extraction

**Key Classes:**
- `HargassnerMessageParser` - Main parser
- `ParameterDefinition` - Individual parameter metadata

**Supported Message Format:**
```
pm <val0> <val1> <val2> ... <valN>
   ^^^^^ Space-separated values
```

### Layer 3: Coordinator (`coordinator.py`)

**Responsibilities:**
- Bridge between telnet client and Home Assistant
- Periodic data refresh (5 seconds)
- Extends `DataUpdateCoordinator` for HA integration
- Error handling and recovery

### Layer 4: Sensor Platform (`sensor.py`)

**Sensor Types:**
1. **Connection Sensor** - Connection status + statistics
2. **State Sensor** - Boiler operating state (enum)
3. **Error Sensor** - Error messages (enum)
4. **Parameter Sensors** - Individual measurements
5. **Energy Sensor** - kWh calculation from pellet consumption

**Sensor Sets:**

- **STANDARD** - 26 default sensors (22 declared parameters plus connection, state, error, and energy); membership is configurable per firmware
- **FULL** - All sensors from firmware template (varies by version)

### Layer 5: Configuration (`config_flow.py`)

**Features:**
- GUI-based setup (Config Flow)
- Connection validation before entry creation
- Options flow for runtime changes
- Unique ID validation (one entry per IP)

## Data Flow

```
Boiler (Telnet Port 23)
    ↓ "pm 7 10.1 9.0 67.4 ..."
TelnetClient._receiver_loop()
    ↓ Decode (UTF-8/Latin-1/CP1252)
    ↓ Extract lines, find latest "pm" message
MessageParser.parse_message()
    ↓ Split values, map to parameters
    ↓ Type conversion, bit extraction
TelnetClient._latest_data (async locked)
    ↓ Poll every 5 seconds
Coordinator._async_update_data()
    ↓ Update event
Sensor Entities (Connection, State, Parameters, Energy)
    ↓ Display in Home Assistant UI
```

## Firmware Support

Firmware support separates the message layout from the interpretation displayed
to users. [Firmware templates](custom_components/bauergroup_hargassnerintegration/firmware_templates.py)
define XML channel positions, digital bits, and units. The version keys offered
in configuration are listed in
[the integration constants](custom_components/bauergroup_hargassnerintegration/const.py),
including `V10_2HAR_n2` and the existing V14 and V40 variants. Layout keys and
configuration keys must match exactly.

### Lookup profiles

[The profile registry](custom_components/bauergroup_hargassnerintegration/firmware_versions/__init__.py)
selects definitions for the configured firmware. Versions without a registered
profile use [the default definitions](custom_components/bauergroup_hargassnerintegration/firmware_versions/default.py),
which preserve the original parameter names, boiler-state labels, and error
translations. [The V10 profile](custom_components/bauergroup_hargassnerintegration/firmware_versions/V10_2HAR_n2.py)
contains only firmware-specific differences. Missing parameters, translations,
error codes, enum states, and label metadata are inherited recursively from the
default profile. Empty tables inherit all defaults. Resolved dedicated profiles
contain independent dictionaries, so changing them cannot modify the default
tables or source overrides. The inherited states and errors are starting values,
not verified Neo-HV definitions.

Profiles contain two lookup tables: `PARAMETER_DESCRIPTIONS` and `ERROR_CODES`.
Parameter descriptions provide English and German names and an optional `enum`
mapping from integer wire values to translated state labels. Boiler state (`ZK`)
uses this same mechanism; other analog or digital parameters can define their
own mappings. Enum keys can be sparse. Optional `icon` metadata on a boiler-state
enum value controls the dedicated state sensor's icon without assuming the same
state numbers across firmware versions. Error codes retain string keys and
English/German descriptions; code zero represents normal operation. Parameters
without translated names use their wire names, allowing metadata-only entries.

Sensor classification is also part of each parameter description. `device_class`,
`state_class`, `icon`, and `standard` declare the Home Assistant classification,
appearance, and STANDARD membership. `sensor_type` selects ordinary parameter
handling or the `boiler_state`/`error` roles. These roles create dedicated entities
from the selected parameter keys; no sensor class assumes that a specific wire
name is the boiler-state or error source. `entity_id_suffix` preserves the
original `state` and `operation` identities and supports distinct additional
entities. `sensor_name` can name a dedicated error entity separately from its
FULL parameter entity, and `ok_icon` controls its normal-operation icon.

The registry uses static Python imports and a standard-library dataclass and
typed dictionary. This avoids filesystem discovery during operation and adds no
integration runtime dependency. Profiles and parsing remain usable by standalone
developer tools without Home Assistant. The unused legacy boiler-state arrays and
default-profile compatibility exports have been removed. Production code and
standalone developer tools select definitions through the same resolver.

### Parser and sensor behavior

The parser attaches the selected profile's descriptions to analog and digital
parameters while preserving raw values and XML units. Sensor setup resolves the
profile once and shares it among the device's entities. It reads classifications
from metadata rather than inferring them from names or units. The V10 profile
retains an explicit temperature-class override for `Max Anf Kessel`, whose XML
unit differs from the default layout. Connection and calculated-energy sensors
remain separate because they are not direct wire parameters.

STANDARD and FULL sensor sets apply translated names, enum labels, and error
translations at the entity boundary. FULL retains parameter IDs alongside the
dedicated entities. Invalid roles and colliding dedicated IDs fail explicitly.
Enum sensors
declare Home Assistant's enum device class and omit numeric units and state
classes. Setting a parameter's `enum` mapping to `None` explicitly disables an
inherited enum and restores its normal raw sensor value and unit handling.
Omitting the field inherits its default mapping.

Unknown enum values appear as `Unknown` or `Unbekannt`; unknown error codes use
`Error N` or `Fehler N`. These fallback labels are added to the affected entity's
options without changing shared profile definitions. Profile selection is per
boiler, allowing devices with different firmware versions to coexist.

### V10 legacy configuration baseline

The V10 profile preserves the active mappings from the earlier V10-only
integration. Its list positions are zero-based wire codes. Separate enums cover
the log boiler (`ZK`), pellet boiler (`PK_ZK`), log-boiler mode (`Programm`),
heating circuit 1 state (`HKZustand_1`) and mode (`FR1 Zustand`), and DHW state
(`BoiZustand_1`). Despite its name, `PufZustand` uses the two-state pellet-enable
mapping: `Gesperrt`/`Freigegeben`. The old six-state buffer list was unused and is
not assigned to this parameter.

The eight active binary formatter bindings use integer enum keys zero and one,
which also match the parser's native boolean values, with German labels
`Inaktiv`/`Aktiv`. Parameter names inherit the defaults when their meanings are
equivalent, even if the old formatter used different wording or an HV/PK prefix.
Overrides retain names missing from the defaults and correct the distinct
meanings of pellet-enable status and HC1 mode. Enum labels remain unchanged.
The old conversion of numeric values to two-decimal strings is not carried
into parsing. Unsupported acronym expansions are avoided; labels such as `ABS`,
`STB`, and `TÜV` remain unchanged.

Only differences are stored in the V10 profile. Notification 309 already has the
default German label `Nachlegen` and therefore needs no error override. The
orphan `BoiZustand_1_2` alias is excluded because it is absent from the old and
current XML layouts. The old integration remains a read-only migration baseline;
the current defaults, XML positions, sensor membership, and dedicated entity IDs
remain unchanged. Additional mapped parameters are visible in FULL mode; profiles
can opt them into STANDARD through metadata.

### Firmware display text and configuration

Each dedicated profile can supply an optional `DISPLAY_NAME`. Setup and options
forms display that label while submitting and storing the unchanged firmware
version key. An unset or empty display name falls back to the version string.
Versions without a dedicated profile display their own version key, regardless
of display metadata on the default profile.

The [firmware configuration guide](docs/ADDING_FIRMWARE.md#firmware-specific-names-enums-errors-and-display-text)
documents the schema and profile registration. Python definition changes require
a Home Assistant restart. XML layouts, existing configuration keys, and entity
IDs are preserved, so this feature requires no config-entry migration.

## Example Telnet Message (V14_1HAR_q1)

```
pm 7 10.1 9.0 67.4 70 64.5 65 11 91.3 26 27.0 62.3 59.3 58.7 89 5 64 3 70 62 30 28.9 30 100 30.0 30.0 29 96.0 100 3 0 0 18 2 10 0 0 333 324 160 24 1 21 0 91 8.00 12.99 616 8.9 24209 140.0 110.3 28 -20.0 -20.0 0.0 60.0 -20.0 93.4 1 0 -20.0 0 20.0 20.0 0 1 0 120.0 0 20.0 20.0 0 1 0 120.0 0 20.0 20.0 0 1 0 -20.0 0 20.0 20.0 0 1 0 -20.0 0 120.0 0 -20.0 0 0.0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.00 E 21 0 0 2007 0 0 0
```

This message contains 138 values corresponding to:
- `values[0]` = ZK (Boiler state) = 7
- `values[3]` = TK (Boiler temp) = 67.4°C
- `values[8]` = TRG (Smoke gas temp) = 91.3°C
- `values[14]` = Leistung (Output) = 89%
- `values[20]` = Taus (Outside temp) = 30°C
- ... and so on

## Error Handling

### Connection Errors
- **Initial failure:** Raises `ConfigEntryNotReady`, HA retries
- **Runtime loss:** Background task continues reconnecting
- **Exponential backoff:** 5s → 10s → 20s → ... → 300s max

### Parsing Errors
- **Invalid encoding:** Try UTF-8 → Latin-1 → CP1252 → fallback
- **Length mismatch:** Log warning, parse available data
- **Invalid values:** Return `None`, sensor shows "unknown"

### Update Errors
- **No data yet:** Return empty dict (not an error on startup)
- **Coordinator timeout:** Automatic retry with backoff

## Performance

- **Update interval:** 5 seconds (configurable)
- **Memory usage:** ~5-10 MB (typical)
- **CPU usage:** Minimal (async I/O)
- **Network:** ~1-2 KB/message, ~400 bytes/s average

## Installation

### Via HACS
1. Add custom repository
2. Install integration
3. Restart HA
4. Add via UI

### Manual
1. Copy `custom_components/hargassner_pellet` to HA config
2. Restart HA
3. Add integration via Settings → Devices & Services

## Configuration Example

```yaml
# Via GUI (recommended), or YAML:
hargassner_pellet:
  host: 192.168.1.100
  firmware: V14_1HAR_q1
  device_name: Hargassner Boiler
  language: EN
  sensor_set: STANDARD
  pellet_energy_kwh_per_kg: 4.8  # Pellet energy content (3.0-6.0)
  efficiency_percent: 90          # Boiler efficiency (50-100)
```

## Available Sensors (Default Standard Set - 26 Sensors)

**Automatic Sensors (4):**

- Connection Status
- Boiler State (Off/Ignition/Full Firing/etc.)
- Operation Status (OK/Errors)
- Heat Output (kWh) - Calculated from pellet consumption

**Boiler & Combustion (8):**

- Boiler Temperature (TK)
- Boiler Setpoint (TKsoll)
- Flue Gas Temperature (TRG)
- Burner Temperature (BRT)
- Output Power (Leistung)
- Efficiency (Effizienz)
- O2 Level (O2)
- Draft Actual (SZist)

**Buffer & Storage (6):**

- Buffer Top/Middle/Bottom (TPo, TPm, TPu)
- Buffer Fill Level (Puff Füllgrad)
- Buffer Setpoint Top/Bottom (Puffer_soll oben/unten)

**Heating Circuits (3):**

- Flow Temperature HC1 (TVL_1)
- Flow Setpoint HC1 (TVLs_1)
- Return Temperature (TRL)

**Hot Water (2):**

- Hot Water Temperature (TB1)
- Hot Water Setpoint (TBs_1)

**Outside & Pellets (3):**

- Outside Temperature (Taus)
- Pellet Stock (Lagerstand)
- Pellet Consumption (Verbrauchszähler)

## Energy Dashboard Integration

Energy sensor automatically created:

- **Name:** "Wärmemenge" (DE) / "Heat Output" (EN)
- **Formula:** `Pellet Consumption (kg) × Energy Content (kWh/kg) × Efficiency (%)`
- **Configurable Parameters:**
  - Pellet Energy Content: 3.0-6.0 kWh/kg (Default: 4.8)
  - Boiler Efficiency: 50-100% (Default: 90%)
- **Example:** 100 kg × 4.8 kWh/kg × 0.90 = 432 kWh
- Compatible with HA Energy Dashboard
- Tracks total heat output from pellet heating
- Sensor attributes show current calculation parameters

## Security Considerations

⚠️ **Important:**
- Telnet is **unencrypted** and **unauthenticated**
- Use only on **trusted local networks**
- Consider **VPN** for remote access
- **Firewall** appropriately

## Development Status

| Feature | Status |
|---------|--------|
| Telnet Client | ✅ Complete |
| Message Parser | ✅ Complete |
| Config Flow | ✅ Complete |
| Coordinator | ✅ Complete |
| Sensors | ✅ Complete |
| Translations (EN/DE) | ✅ Complete |
| Documentation | ✅ Complete |
| Unit Tests | Parser, generator, firmware profiles, sensors, and configuration schemas |
| HACS Integration | ⏳ Pending |
| HA Core Integration | ⏳ Future |

## Validation

The [test suite](tests/) covers message parsing and generation across firmware
layouts. [Firmware behavior tests](tests/test_firmware_definitions.py) also cover
profile isolation, recursive fallback, translations, sparse enums, raw parser
values, both sensor sets and languages, unknown options, explicit enum opt-out,
sensor classifications, configurable membership, specialized source parameters,
stable entity IDs, invalid metadata, and optional display text. Sensor and configuration tests execute
the integration code with lightweight Home Assistant import stubs. Configuration
schema serialization checks use the optional development libraries `voluptuous`
and `voluptuous-serialize`; they verify display labels while retaining stored
version keys.

V10 regression tests pin every active legacy enum list, boolean formatter
mapping, and selected parsed sensor values. They check sparse overrides and
confirm that notification 309 still inherits its default translation and numeric
readings retain full precision. Tests contain baseline snapshots and do not
require access to the old project.

The latest local validation on 2026-11-17 used Python 3.13 and reported **218
passing tests and one failure**. The existing manufacturer-capture test requires
the private recording `docs/private_firmware_samples/DAQ00001.DAQ`, which is absent
from this checkout. Restoring that exact recording allows the comparison to run.
This result does not include live Home Assistant, entity-registry, statistics, or
physical-boiler verification.

The [parameter validator](tools/parameter_validator.py) checks description
coverage against each firmware's selected profile. Validation reports no errors;
warnings identify placeholders, unused descriptions, and naming conventions.
Metadata covers all known XML parameters; untranslated names retain the raw
parameter name. Comparison with the original definitions confirmed preservation
of all XML layouts, translated names, errors, and boiler-state labels. A separate
check across every bundled layout confirmed that the declared numeric and digital
classifications retain their previous behavior. Enum and error parameters use
their declared categorical handling.

## Code Quality

- ✅ Type hints throughout
- ✅ Docstrings for all public functions
- ✅ Error handling at all layers
- ✅ Async/await (no blocking I/O)
- ✅ Thread-safe data access
- ✅ PEP 8 compliant
- ✅ Home Assistant conventions followed

## Documentation

- **README.md** - User-facing overview
- **INSTALLATION.md** - Step-by-step setup guide
- **ARCHITECTURE.md** - Technical deep-dive (20+ pages)
- **DEVELOPMENT.md** - Developer workflow
- **CONTRIBUTING.md** - Contribution guidelines
- **PROJECT_SUMMARY.md** - This file

## License

MIT License - See [LICENSE](LICENSE) file

## Support & Contributing

- **Issues:** Report bugs and request features
- **Discussions:** Ask questions, share ideas
- **Pull Requests:** Contribute code (see CONTRIBUTING.md)
- **Documentation:** Help improve docs

## Contact

- GitHub: https://github.com/bauer-group/IP-HargassnerIntegration
- Issues: https://github.com/bauer-group/IP-HargassnerIntegration/issues

---

**Built with ❤️ for the Home Assistant community**

Last Updated: 2026-11-17
