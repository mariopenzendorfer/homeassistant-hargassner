# Neue Firmware-Version hinzufügen

Diese Anleitung erklärt, wie du Unterstützung für zusätzliche Hargassner-Firmware-Versionen zur Integration hinzufügst - mit dem automatisierten DAQ-Parser-Tool.

Firmware-spezifische Parameternamen, Zuordnungen von Aufzählungswerten (einschließlich
der Kesselzustände), übersetzte Fehlermeldungen und ein optionaler Anzeigename für
die Firmware werden getrennt vom XML-Layout konfiguriert. Einzelheiten findest du
in der gepflegten
[Anleitung zur Profilkonfiguration (Englisch)](ADDING_FIRMWARE.md#firmware-specific-names-enums-errors-and-display-text).
Das schlanke V10-Profil enthält nur abweichende Definitionen und liegt in
[`firmware_versions/V10_2HAR_n2.py`](../custom_components/bauergroup_hargassnerintegration/firmware_versions/V10_2HAR_n2.py).
Nicht angegebene Parameter, Übersetzungen, Fehlercodes und einzelne
Aufzählungswerte werden aus dem Standardprofil übernommen. Leere Tabellen
übernehmen alle Standardwerte. Mit `"enum": None` kannst du eine geerbte
Aufzählung ausdrücklich deaktivieren und den Rohwert anzeigen lassen.

Auch der Sensortyp wird im Parameterprofil festgelegt: `sensor_type` wählt zwischen
`parameter`, `boiler_state` und `error`. `device_class` und `state_class` bestimmen
die Klassifizierung in Home Assistant, `standard` die Aufnahme in den
STANDARD-Sensorsatz und `icon` das Symbol. Der Sensorcode leitet diese Angaben
nicht mehr aus Parameternamen oder Einheiten ab. Einheiten stammen weiterhin aus
dem XML-Layout. Der FULL-Sensorsatz enthält alle dort deklarierten Parameter.

Mit `boiler_state` oder `error` erzeugt die Integration zusätzlich einen eigenen
Zustands- beziehungsweise Fehlersensor für den jeweiligen Parameter.
`entity_id_suffix` legt dessen eindeutige Kennung fest; die bisherigen Kennungen
`state` und `operation` bleiben im Standardprofil erhalten. Für zusätzliche
Sensoren müssen die Kennungen eindeutig sein. `sensor_name` kann den Namen eines
eigenen Fehlersensors übersetzen, `ok_icon` dessen Symbol bei fehlerfreiem Betrieb
festlegen. Verbindung und berechnete Wärmemenge bleiben separate Sensoren der
Integration. Das V10-Profil enthält außerdem eine abweichende Temperaturklasse
für `Max Anf Kessel`, da nur dessen V10-Layout eine Celsius-Einheit angibt.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Schnellstart (4 Schritte)](#schnellstart-4-schritte)
- [Schritt 1: Firmware-Version ablesen](#schritt-1-firmware-version-ablesen)
- [Schritt 2: SD-Karten-Logging aktivieren](#schritt-2-sd-karten-logging-aktivieren)
- [Schritt 3: DAQ-Datei auslesen](#schritt-3-daq-datei-auslesen)
- [Schritt 4: Code einfügen](#schritt-4-code-einfügen)
- [Testen und Validieren](#testen-und-validieren)
- [Fehlerbehebung](#fehlerbehebung)
- [Template beitragen](#template-beitragen)

---

## Überblick

Die Integration verwendet XML-basierte Firmware-Templates (DAQPRJ-Format) um Telnet-Nachrichten von verschiedenen Kessel-Firmware-Versionen zu parsen. Jede Firmware-Version kann unterschiedliche Parameter-Positionen, Namen und Datenformate haben.

**Architektur:**
```
Kessel → DAQ-Datei auf SD-Karte → DAQ Parser Tool → Firmware Template → Integration
```

**Der einfache Weg:** Hargassner-Kessel loggen automatisch alle Parameter-Definitionen auf die SD-Karte in DAQ-Dateien. Unser `daq_parser.py` Tool extrahiert alles automatisch - keine manuelle Analyse nötig!

## Schnellstart (4 Schritte)

### Voraussetzungen

- ✅ Zugang zu deinem Hargassner-Kessel
- ✅ Python 3.8+ installiert
- ✅ Source-Code dieser Integration

### Gesamtzeit: ~10 Minuten

1. **Firmware-Version am Kessel-Display ablesen** (1 min)
2. **SD-Karten-Logging für einige Minuten aktivieren** (5 min)
3. **DAQ-Datei mit Tool auslesen und Python-Code generieren** (2 min)
4. **Python-Code an richtigen Stellen einfügen** (2 min)

Fertig! ✨

---

## Schritt 1: Firmware-Version ablesen

### Am Kessel-Display

1. Gehe zum Hauptmenü deines Hargassner-Kessels
2. Navigiere zu **Service** oder **Info**
3. Suche nach **Software-Version** oder **Firmware**
4. Notiere die Version (z.B. `V14.1HAR.q1`, `V15.2HAR`, etc.)

**Beispiel:**
```
Software: V14.1HAR.q1
Hardware: V1.0
```

Diese Version benötigst du später für die Benennung im Code.

---

## Schritt 2: SD-Karten-Logging aktivieren

### 2.1 SD-Karte einlegen

Falls noch keine SD-Karte im Kessel ist:

- Öffne das Bedienfeld des Kessels
- Lege eine SD-Karte ein (in der Regel hinter einer kleinen Klappe)
- Der Kessel beginnt automatisch mit dem Logging

### 2.2 Logging laufen lassen

**Wichtig:** Lasse den Kessel für mindestens **5-10 Minuten** laufen, während die SD-Karte eingelegt ist.

Der Kessel schreibt kontinuierlich DAQ-Dateien mit allen Parameter-Definitionen und Messwerten.

### 2.3 SD-Karte entnehmen

Nach 5-10 Minuten:

- Öffne das Bedienfeld
- Entnimm die SD-Karte
- Stecke sie in deinen Computer (SD-Kartenleser)

**Hinweis:** Der Kessel kann ohne SD-Karte weiterlaufen, loggt dann aber keine neuen Daten.

---

## Schritt 3: DAQ-Datei auslesen

### 3.1 DAQ-Datei finden

Auf der SD-Karte findest du Dateien wie:

```
DAQ00000.DAQ
DAQ00001.DAQ
DAQ00002.DAQ
```

**Welche Datei?** Nimm die **neueste** DAQ-Datei (höchste Nummer oder neuestes Datum).

Typische Dateigröße: 1-10 MB

### 3.2 DAQ Parser ausführen

Öffne ein Terminal/Kommandozeile und navigiere zum `tools`-Ordner der Integration:

**Windows:**

```bash
cd /path/to/IP-HargassnerIntegration/tools
python daq_parser.py E:\DAQ00000.DAQ --output python > firmware_template.txt
```

**Linux/macOS:**

```bash
cd /path/to/IP-HargassnerIntegration/tools
python3 daq_parser.py /media/sd-card/DAQ00000.DAQ --output python > firmware_template.txt
```

**Hinweis:** Ersetze den Pfad zur DAQ-Datei mit dem tatsächlichen Pfad auf deinem System (z.B. `E:\DAQ00000.DAQ` wenn die SD-Karte als Laufwerk E: eingebunden ist).

### 3.3 Generierter Code

Das Tool erstellt automatisch eine Datei `firmware_template.txt` mit fertigem Python-Code:

**Beispiel-Output:**

```python
"""
Firmware Template: V14_1HAR_q1
Generated from DAQ file

System Information:
- Manufacturer: Hargassner
- Model: Nano-PK 32
- Software: V14.1HAR.q1
- Hardware: V1.0
- Serial: 123456

Statistics:
- Analog Parameters: 112
- Digital Parameters: 116
- Expected Message Length: 138
"""

# Add to FIRMWARE_TEMPLATES in firmware_templates.py
FIRMWARE_TEMPLATES["V14_1HAR_q1"] = """<DAQPRJ>
  <ANALOG>
    <CHANNEL id="0" name="ZK" dop="" unit="" />
    <CHANNEL id="3" name="TK" dop="" unit="°C" />
    <CHANNEL id="8" name="TRG" dop="" unit="°C" />
    <!-- ... alle weiteren Parameter ... -->
  </ANALOG>
  <DIGITAL>
    <CHANNEL id="102" bit="0" name="M1_Kessel_Geblaese" />
    <!-- ... alle weiteren Bits ... -->
  </DIGITAL>
</DAQPRJ>"""

# Add to FIRMWARE_VERSIONS in const.py
FIRMWARE_VERSIONS.append("V14_1HAR_q1")
```

Dieser Code enthält:

- ✅ Komplettes DAQPRJ-XML-Template mit allen Parametern
- ✅ System-Informationen (Hersteller, Modell, Version)
- ✅ Statistiken (Anzahl Parameter, Message-Länge)
- ✅ Fertige Code-Snippets zum Einfügen

---

## Schritt 4: Code einfügen

Jetzt fügst du den generierten Code an zwei Stellen ein:

### 4.1 Datei 1: firmware_templates.py

Öffne: `custom_components/bauergroup_hargassnerintegration/src/firmware_templates.py`

**Was einfügen:** Die komplette Zeile mit `FIRMWARE_TEMPLATES["..."] = """<DAQPRJ>...</DAQPRJ>"""`

**Wo einfügen:** In das Dictionary `FIRMWARE_TEMPLATES`, unterhalb der bestehenden Einträge.

**Beispiel:**

```python
FIRMWARE_TEMPLATES = {
    # Existing firmware
    "V14_1HAR_q1": """<DAQPRJ>
        <!-- existing template -->
    </DAQPRJ>""",

    # Deine neue Firmware (aus firmware_template.txt kopieren)
    "V15_2HAR": """<DAQPRJ>
        <!-- HIER DEN KOMPLETTEN DAQPRJ-BLOCK EINFÜGEN -->
    </DAQPRJ>""",
}
```

**Tipp:** Kopiere einfach die komplette Zeile aus `firmware_template.txt` und füge sie vor der schließenden `}` ein.

### 4.2 Datei 2: const.py

Öffne: `custom_components/bauergroup_hargassnerintegration/const.py`

**Was einfügen:** Die Firmware-Version als String

**Wo einfügen:** In die Liste `FIRMWARE_VERSIONS`

**Beispiel:**

```python
FIRMWARE_VERSIONS: Final = [
    "V14_1HAR_q1",
    "V15_2HAR",      # Deine neue Version hier hinzufügen
]
```

**Wichtig:** Der Name muss **exakt identisch** sein mit dem Dictionary-Key in `firmware_templates.py`!

### 4.3 Fertig!

Das war's! Du hast erfolgreich:

- ✅ DAQPRJ-XML-Template in `firmware_templates.py` eingefügt
- ✅ Firmware-Version in `const.py` hinzugefügt

Jetzt kannst du die Integration testen.

---

## Testen und Validieren

Nach dem Einfügen des Codes musst du die Integration testen.

### 5.1 Home Assistant neustarten

```bash
# Via Home Assistant UI
Einstellungen → System → Neu starten
```

### 5.2 Debug-Logging aktivieren (optional)

Füge in `configuration.yaml` ein:

```yaml
logger:
  default: info
  logs:
    custom_components.bauergroup_hargassnerintegration: debug
```

Starte Home Assistant erneut.

### 5.3 Integration mit neuer Firmware hinzufügen

1. Gehe zu **Einstellungen → Geräte & Dienste**
2. Klicke **Integration hinzufügen**
3. Suche nach **"BAUERGROUP Hargassner"**
4. Konfiguriere:
   - **Host:** IP-Adresse deines Kessels
   - **Firmware:** Wähle deine neue Firmware-Version
   - **Sensor Set:** Starte mit **STANDARD**
5. Klicke **Absenden**

### 5.4 Sensoren überprüfen

Prüfe, dass die Sensoren korrekte Werte anzeigen:

1. **Einstellungen → Geräte & Dienste → Deine Integration**
2. Klicke auf die Integration, um alle Entitäten zu sehen
3. Vergleiche Sensorwerte mit dem Kessel-Display:
   - Kesseltemperatur sollte übereinstimmen
   - Außentemperatur sollte übereinstimmen
   - Kesselzustand sollte übereinstimmen
   - Werte sollten alle 5 Sekunden aktualisiert werden

### 5.5 Logs prüfen

**Einstellungen → System → Protokolle**

Erwartete Meldungen:

- ✅ `Successfully connected to boiler`
- ✅ `Parsed message with X parameters`
- ❌ Keine Parsing-Fehler oder "Unknown state" Warnungen

**Beispiel-Logs:**

```
[custom_components.bauergroup_hargassnerintegration.telnet_client] Successfully connected to 192.168.1.100:23
[custom_components.bauergroup_hargassnerintegration.message_parser] Parsed message with 138 values
[custom_components.bauergroup_hargassnerintegration.coordinator] Data update successful
```

### 5.6 Validierung mit Tools (optional)

Prüfe die Template-Konsistenz:

```bash
cd tools
python parameter_validator.py
```

Das Tool prüft:

- XML ist valide
- Keine duplizierten Parameter
- Namenskonventionen eingehalten
- Alle Standard-Parameter vorhanden

### 5.7 Erweiterte Tests

Lasse die Integration 24 Stunden laufen, um sicherzustellen:

- Verbindung bleibt stabil
- Keine Memory Leaks
- Alle Sensorwerte aktualisieren korrekt
- Keine unerwarteten Fehler in Logs

---

## Fehlerbehebung

### Problem: "Failed to parse DAQPRJ XML"

**Ursache:** XML-Syntaxfehler im Template

**Lösung:**

- Validiere das XML mit einem Online-Validator
- Stelle sicher, dass du den kompletten `<DAQPRJ>...</DAQPRJ>` Block kopiert hast
- Prüfe auf Sonderzeichen oder Encoding-Probleme

### Problem: "Firmware version not found"

**Ursache:** Versionsname stimmt nicht überein zwischen `const.py` und `firmware_templates.py`

**Lösung:**

- Stelle sicher, dass der Dictionary-Key in `FIRMWARE_TEMPLATES` exakt mit dem String in `FIRMWARE_VERSIONS` übereinstimmt
- Versionsnamen sind case-sensitive

### Problem: Sensoren zeigen "Unknown" Status

**Ursache:** Parameter nicht in Telnet-Nachricht gefunden

**Lösung:**

- Aktiviere Debug-Logging
- Prüfe Logs für Message-Länge: `Parsed message with X values`
- Verifiziere, dass die DAQ-Datei vom selben Kessel stammt, mit dem du dich verbindest
- Manche Parameter sind möglicherweise nicht bei allen Konfigurationen verfügbar

### Problem: Falsche Sensorwerte

**Ursache:** Parameter-Index-Mismatch oder falsches Firmware-Template

**Lösung:**

- Prüfe, dass du die korrekte Firmware-Version in der Konfiguration verwendest
- Verifiziere, dass die DAQ-Datei zu deinem Kesselmodell und Firmware passt
- Vergleiche einige Schlüsselwerte manuell:
  - Kesseltemperatur ist in den meisten Firmwares Index 3
  - Außentemperatur ist üblicherweise Index 20
  - Prüfe gegen Kessel-Display zur Validierung

### Problem: DAQ Parser kann DAQPRJ nicht extrahieren

**Ursache:** DAQ-Datei ist beschädigt oder falsches Format

**Lösung:**

- Probiere eine andere DAQ-Datei von der SD-Karte
- Stelle sicher, dass die Datei vollständig kopiert wurde (prüfe Dateigröße)
- Versuche `--output text` um zu sehen, welche Informationen verfügbar sind
- Prüfe, ob die Datei verschlüsselt ist (ältere Firmwares nutzen eventuell andere Formate)

### Problem: Integration lädt nicht nach Hinzufügen des Templates

**Ursache:** Python-Syntaxfehler in `firmware_templates.py`

**Lösung:**

- Prüfe Home Assistant Logs für Python Traceback
- Stelle sicher, dass der XML-String korrekt in `""" ... """` eingeschlossen ist
- Überprüfe Kommata zwischen Dictionary-Einträgen
- Kein Komma nach dem letzten Eintrag

---

## Template beitragen

Sobald du dein Firmware-Template getestet hast und es funktioniert, trage es bitte bei, um anderen zu helfen!

### Wie du beitragen kannst

1. **Fork das Repository** auf GitHub
2. **Füge dein Template hinzu** zu `firmware_templates.py`
3. **Füge Firmware-Version hinzu** zu `const.py`
4. **Füge Sample-DAQ-Datei hinzu** (optional) zu `docs/firmware_samples/`
5. **Aktualisiere README** um die unterstützte Firmware-Version aufzulisten
6. **Erstelle Pull Request** mit Beschreibung:
   - Firmware-Version
   - Kesselmodell
   - Testdauer
   - Besonderheiten oder spezielle Hinweise

### Was einzuschließen ist

**Erforderlich:**

- Firmware-Template in `firmware_templates.py`
- Versions-String in `const.py`

**Empfohlen:**

- Sample-DAQ-Datei (erste 100 Zeilen) in `docs/firmware_samples/DEINE_VERSION.txt`
- Screenshot der funktionierenden Sensoren in `docs/images/`
- Notizen zu spezieller Konfiguration

**Template für Pull Request:**

```markdown
# Unterstützung für Firmware V15.2HAR hinzugefügt

- **Firmware:** V15.2HAR
- **Kesselmodell:** Nano-PK 32
- **Testdauer:** 7 Tage
- **Sensoren:** 112 analog, 116 digital
- **Hinweise:** Funktioniert identisch zu V14.1HAR.q1

Getestet auf Produktivsystem ohne Probleme.
```

### Test-Checkliste vor dem Beitragen

- ✅ Template lädt ohne Fehler
- ✅ Alle Sensoren zeigen korrekte Werte
- ✅ Mindestens 24 Stunden getestet
- ✅ Keine Fehler in Home Assistant Logs
- ✅ Mit `parameter_validator.py` validiert
- ✅ Verbindung bleibt stabil
- ✅ Energie-Sensor berechnet korrekt

---

## Zusätzliche Ressourcen

### Tool-Dokumentation

Siehe [tools/README.md](../tools/README.md) für detaillierte Informationen über:

- `daq_parser.py` - DAQ-Datei-Parser
- `telnet_tester.py` - Telnet-Verbindungstester
- `message_generator.py` - Test-Nachrichten-Generator
- `parameter_validator.py` - Template-Validator

### Integrations-Dokumentation

- **[Architektur-Übersicht](ARCHITECTURE.md)** - Technischer Deep-Dive
- **[Entwicklungs-Guide](DEVELOPMENT.md)** - Entwickler-Setup und Workflow
- **[Beitrags-Richtlinien](CONTRIBUTING.md)** - Wie du beitragen kannst

### Hilfe bekommen

Wenn du auf Probleme stößt:

1. **Prüfe Logs:** Aktiviere Debug-Logging und schaue Home Assistant Logs durch
2. **Validiere Template:** Führe `parameter_validator.py` aus
3. **Teste Verbindung:** Nutze `telnet_tester.py` um Konnektivität zu verifizieren
4. **Frage um Hilfe:**
   - Öffne ein Issue: https://github.com/bauer-group/IP-HargassnerIntegration/issues
   - Füge hinzu: Firmware-Version, DAQ Parser Output, Fehlermeldungen, Logs
5. **Community-Diskussion:** https://github.com/bauer-group/IP-HargassnerIntegration/discussions

---

**Deine Beiträge machen diese Integration besser für alle! 🙏**

Zuletzt aktualisiert: 2025-11-23
