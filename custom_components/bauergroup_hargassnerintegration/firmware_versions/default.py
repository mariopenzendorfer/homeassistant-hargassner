"""Default firmware names, enum mappings, and error translations.

These preserve the original integration definitions. Firmware without a dedicated
profile uses these tables. Enum mappings belong inside parameter descriptions."""

from typing import Final

from ..parameter_description import ParameterDescription
from .definitions import FirmwareDefinitions

DISPLAY_NAME: Final[str | None] = None

# Error codes (source: Hargassner Nano-PK 6-32 Manual, shb-nano-pk-6-32-de.pdf)
ERROR_CODES: Final = {
    # Boiler and safety (1-9)
    "1": {"en": "Overtemperature - STB triggered", "de": "Übertemperatur STB gefallen"},
    "2": {"en": "Overcurrent feed screw", "de": "Überstrom Einschubschnecke"},
    "3": {"en": "Overcurrent room auger 1", "de": "Überstrom Raumaustragungsschnecke 1"},
    "4": {"en": "Thermal protection room auger 1", "de": "Thermoschutz Raumaustragungsschnecke 1"},
    "5": {"en": "Empty ash drawer", "de": "Aschelade entleeren"},
    "6": {"en": "Ash drawer too full", "de": "Aschelade zu voll"},
    "7": {"en": "Grate does not open", "de": "Schieberost öffnet nicht"},
    "8": {"en": "Grate does not close", "de": "Schieberost schließt nicht"},
    "9": {"en": "Overcurrent cleaning device", "de": "Überstrom Putzeinrichtung"},
    # Probes and sensors (10-59)
    "10": {"en": "Flue gas sensor wrong connection", "de": "Rauchgasfühler falsch angeschlossen"},
    "11": {"en": "Flue gas sensor disconnected", "de": "Rauchgasfühler Unterbrechung"},
    "12": {"en": "Boiler sensor short circuit", "de": "Kesselfühler Kurzschluss"},
    "13": {"en": "Boiler sensor disconnected", "de": "Kesselfühler Unterbrechung"},
    "14": {"en": "DHW sensor 1 short circuit", "de": "Boilerfühler 1 Kurzschluss"},
    "15": {"en": "DHW sensor 1 disconnected", "de": "Boilerfühler 1 Unterbrechung"},
    "16": {"en": "Outdoor sensor short circuit", "de": "Außenfühler Kurzschluss"},
    "17": {"en": "Outdoor sensor disconnected", "de": "Außenfühler Unterbrechung"},
    "18": {"en": "Flow sensor HC1 short circuit", "de": "Vorlauffühler HK1 Kurzschluss"},
    "19": {"en": "Flow sensor HC1 disconnected", "de": "Vorlauffühler HK1 Unterbrechung"},
    "20": {"en": "Flow sensor HC2 short circuit", "de": "Vorlauffühler HK2 Kurzschluss"},
    "21": {"en": "Flow sensor HC2 disconnected", "de": "Vorlauffühler HK2 Unterbrechung"},
    "22": {"en": "Room sensor HC1 short circuit", "de": "Raumfühler HK1 Kurzschluss"},
    "23": {"en": "Room sensor HC1 disconnected", "de": "Raumfühler HK1 Unterbrechung"},
    "24": {"en": "Room sensor HC2 short circuit", "de": "Raumfühler HK2 Kurzschluss"},
    "25": {"en": "Room sensor HC2 disconnected", "de": "Raumfühler HK2 Unterbrechung"},
    "34": {"en": "Buffer sensor top short circuit", "de": "Pufferfühler oben Kurzschluss"},
    "35": {"en": "Buffer sensor top disconnected", "de": "Pufferfühler oben Unterbrechung"},
    "36": {"en": "Buffer sensor bottom short circuit", "de": "Pufferfühler unten Kurzschluss"},
    "37": {"en": "Buffer sensor bottom disconnected", "de": "Pufferfühler unten Unterbrechung"},
    "39": {"en": "DHW sensor 2 short circuit", "de": "Boilerfühler 2 Kurzschluss"},
    "40": {"en": "DHW sensor 2 disconnected", "de": "Boilerfühler 2 Unterbrechung"},
    "46": {"en": "Return sensor short circuit", "de": "Rücklauffühler Kurzschluss"},
    "47": {"en": "Return sensor disconnected", "de": "Rücklauffühler Unterbrechung"},
    "52": {"en": "External heat sensor short circuit", "de": "Fremdwärmefühler Kurzschluss"},
    "53": {"en": "External heat sensor disconnected", "de": "Fremdwärmefühler Unterbrechung"},
    "54": {"en": "Buffer sensor middle short circuit", "de": "Pufferfühler Mitte Kurzschluss"},
    "55": {"en": "Buffer sensor middle disconnected", "de": "Pufferfühler Mitte Unterbrechung"},
    "56": {"en": "Buffer sensor upper middle short circuit", "de": "Pufferfühler oben Mitte Kurzschluss"},
    "57": {"en": "Buffer sensor upper middle disconnected", "de": "Pufferfühler oben Mitte Unterbrechung"},
    "58": {"en": "Buffer sensor lower middle short circuit", "de": "Pufferfühler unten Mitte Kurzschluss"},
    "59": {"en": "Buffer sensor lower middle disconnected", "de": "Pufferfühler unten Mitte Unterbrechung"},
    # Combustion and operation (26-50)
    "26": {"en": "Ignition time exceeded", "de": "Zündzeit überschritten"},
    "27": {"en": "Flue gas temperature too low", "de": "Rauchgastemperatur unterschritten"},
    "28": {"en": "System too long on O2 stop", "de": "Anlage zu lange auf O2-Stopp"},
    "29": {"en": "Combustion fault", "de": "Verbrennungsstörung"},
    "30": {"en": "Battery empty", "de": "Batterie leer"},
    "31": {"en": "Feed motor blocked", "de": "Blockade Einschubmotor"},
    "32": {"en": "Max fill time exceeded", "de": "Maximale Füllzeit überschritten"},
    "33": {"en": "Cleaning device not in rest position", "de": "Putzeinrichtung nicht in Ruhelage"},
    "38": {"en": "Overcurrent grate", "de": "Überstrom Schieberost"},
    "41": {"en": "Ash box almost full", "de": "Aschebox fast voll"},
    "42": {"en": "Overcurrent ash screw", "de": "Überstrom Ascheschnecke"},
    "43": {"en": "Ash conveyor not connected", "de": "Ascheaustragung nicht angeschlossen"},
    "45": {"en": "Return temperature not reached", "de": "Rücklaufanhebung Temperatur nicht erreicht"},
    "49": {"en": "Induced draft fan fault", "de": "Saugzuggebläse Störung"},
    "50": {"en": "Fill process timeout", "de": "Zeitüberschreitung Füllvorgang"},
    # Communication and modules (62-99)
    "62": {"en": "GSM module not connected", "de": "GSM-Modul nicht angeschlossen"},
    "65": {"en": "GSM module send error", "de": "GSM-Modul Sendefehler"},
    "67": {"en": "Parameter error - factory defaults loaded", "de": "Fehler in Parametern, Werkseinstellungen geladen"},
    "70": {"en": "Pellet stock low", "de": "Pelletslagerstand gering"},
    "80": {"en": "Switching unit not connected", "de": "Umschalteinheit nicht angeschlossen"},
    "81": {"en": "Switching unit position 1 error", "de": "Positionsfehler Umschalteinheit Pos. 1"},
    "82": {"en": "Switching unit position 2 error", "de": "Positionsfehler Umschalteinheit Pos. 2"},
    "83": {"en": "Switching unit position 3 error", "de": "Positionsfehler Umschalteinheit Pos. 3"},
    "84": {"en": "Switching unit position 4 error", "de": "Positionsfehler Umschalteinheit Pos. 4"},
    "89": {"en": "Grate stiff", "de": "Schieberost schwergängig"},
    "90": {"en": "Boiler IO not connected", "de": "Kessel IO nicht angeschlossen"},
    "91": {"en": "Max board temperature exceeded", "de": "Max. Platinentemperatur überschritten"},
    "92": {"en": "Lambda probe not connected or defective", "de": "Lambdasonde nicht angeschlossen oder defekt"},
    "93": {"en": "Ash drawer open", "de": "Aschelade offen"},
    "94": {"en": "System set to Off - no frost protection", "de": "Betriebsart Aus, Frostschutz nicht gewährleistet"},
    "95": {"en": "Ash box switch must be bridged", "de": "Eingang Ascheboxschalter muss gebrückt werden"},
    "96": {"en": "Check power supply voltage", "de": "Spannung Netzteil kontrollieren"},
    "99": {"en": "Boiler overtemperature", "de": "Kessel Übertemperatur"},
    # Heating circuit modules (100-150)
    "100": {"en": "Heating circuit module CAN 1 not connected", "de": "Heizkreismodul CAN 1 nicht angeschlossen"},
    "103": {"en": "DHW sensor 3 short circuit", "de": "Boilerfühler 3 Kurzschluss"},
    "104": {"en": "DHW sensor 3 disconnected", "de": "Boilerfühler 3 Unterbrechung"},
    "107": {"en": "Flow sensor HC3 short circuit", "de": "Vorlauffühler HK3 Kurzschluss"},
    "108": {"en": "Flow sensor HC3 disconnected", "de": "Vorlauffühler HK3 Unterbrechung"},
    "109": {"en": "Flow sensor HC4 short circuit", "de": "Vorlauffühler HK4 Kurzschluss"},
    "110": {"en": "Flow sensor HC4 disconnected", "de": "Vorlauffühler HK4 Unterbrechung"},
    "111": {"en": "Room sensor HC3 short circuit", "de": "Raumfühler HK3 Kurzschluss"},
    "112": {"en": "Room sensor HC3 disconnected", "de": "Raumfühler HK3 Unterbrechung"},
    "113": {"en": "Room sensor HC4 short circuit", "de": "Raumfühler HK4 Kurzschluss"},
    "114": {"en": "Room sensor HC4 disconnected", "de": "Raumfühler HK4 Unterbrechung"},
    "120": {"en": "Heating circuit module CAN 2 not connected", "de": "Heizkreismodul CAN 2 nicht angeschlossen"},
    "127": {"en": "Flow sensor HC5 short circuit", "de": "Vorlauffühler HK5 Kurzschluss"},
    "128": {"en": "Flow sensor HC5 disconnected", "de": "Vorlauffühler HK5 Unterbrechung"},
    "129": {"en": "Flow sensor HC6 short circuit", "de": "Vorlauffühler HK6 Kurzschluss"},
    "130": {"en": "Flow sensor HC6 disconnected", "de": "Vorlauffühler HK6 Unterbrechung"},
    "131": {"en": "Room sensor HC5 short circuit", "de": "Raumfühler HK5 Kurzschluss"},
    "132": {"en": "Room sensor HC5 disconnected", "de": "Raumfühler HK5 Unterbrechung"},
    "133": {"en": "Room sensor HC6 short circuit", "de": "Raumfühler HK6 Kurzschluss"},
    "134": {"en": "Room sensor HC6 disconnected", "de": "Raumfühler HK6 Unterbrechung"},
    "140": {"en": "Heating circuit board CAN A not connected", "de": "Heizkreisplatine CAN A nicht angeschlossen"},
    "141": {"en": "Flow sensor HCA short circuit", "de": "Vorlauffühler HKA Kurzschluss"},
    "142": {"en": "Flow sensor HCA disconnected", "de": "Vorlauffühler HKA Unterbrechung"},
    "143": {"en": "DHW sensor A short circuit", "de": "Boilerfühler A Kurzschluss"},
    "144": {"en": "DHW sensor A disconnected", "de": "Boilerfühler A Unterbrechung"},
    "145": {"en": "Flow sensor remote line short circuit", "de": "Vorlauffühler geregelte Fernleitung Kurzschluss"},
    "146": {"en": "Flow sensor remote line disconnected", "de": "Vorlauffühler geregelte Fernleitung Unterbrechung"},
    "147": {"en": "Remote line board CAN F not connected", "de": "Fernleitungsplatine CAN F nicht angeschlossen"},
    "148": {"en": "Buffer board CAN C not connected", "de": "Pufferplatine CAN C nicht angeschlossen"},
    "149": {"en": "No connection to Loxone server", "de": "Keine Verbindung zu Loxone-Server"},
    "150": {"en": "Screed heating program deactivated", "de": "Estrich-Ausheizprogramm deaktiviert"},
    # Nano-PK Plus (153-161)
    "153": {"en": "No temperature rise (Nano-PK Plus)", "de": "Kein Temperaturanstieg (Nano-PK Plus)"},
    "154": {"en": "No temperature rise (Nano-PK Plus)", "de": "Kein Temperaturanstieg (Nano-PK Plus)"},
    "155": {"en": "Flushing defective (Nano-PK Plus)", "de": "Spülung defekt (Nano-PK Plus)"},
    "156": {"en": "Sensor Nano-PK Plus short circuit", "de": "Fühler Nano-PK Plus Kurzschluss"},
    "157": {"en": "Sensor Nano-PK Plus disconnected", "de": "Fühler Nano-PK Plus Unterbrechung"},
    "158": {"en": "No temperature rise after flushing", "de": "Kein Temperaturanstieg nach Spülung"},
    "159": {"en": "Flushing temperature not reached", "de": "Temperatur für Spülung nicht erreicht"},
    "160": {"en": "No communication with IO32 (AUE board)", "de": "Keine Kommunikation mit IO32 (AUE-Platine)"},
    "161": {"en": "No communication with motor board 0", "de": "Keine Kommunikation mit Motorplatine 0"},
    # Pellet positions and configuration (171-197)
    "171": {"en": "Pellet fill via position 1 not possible", "de": "Pellets füllen über Position 1 nicht möglich"},
    "172": {"en": "Pellet fill via position 2 not possible", "de": "Pellets füllen über Position 2 nicht möglich"},
    "173": {"en": "Pellet fill via position 3 not possible", "de": "Pellets füllen über Position 3 nicht möglich"},
    "174": {"en": "Pellet fill via position 4 not possible", "de": "Pellets füllen über Position 4 nicht möglich"},
    "175": {"en": "Pellet fill via position 5 not possible", "de": "Pellets füllen über Position 5 nicht möglich"},
    "176": {"en": "Pellet fill via position 6 not possible", "de": "Pellets füllen über Position 6 nicht möglich"},
    "177": {"en": "Pellet fill via position 7 not possible", "de": "Pellets füllen über Position 7 nicht möglich"},
    "178": {"en": "Pellet fill via position 8 not possible", "de": "Pellets füllen über Position 8 nicht möglich"},
    "179": {"en": "Request exceeds max temperature", "de": "Anforderung größer als Maximaltemperatur"},
    "180": {"en": "Check buffer sensor bottom position", "de": "Position Pufferfühler unten kontrollieren"},
    "190": {"en": "Check combustion - O2 target not reached", "de": "Verbrennung überprüfen, O2-Sollwert nicht erreicht"},
    "195": {"en": "Check system configuration urgently", "de": "Anlagenkonfiguration dringend überprüfen"},
    "196": {"en": "Burnout not completed multiple times", "de": "Ausbrand mehrmals nicht vollständig ausgeführt"},
    "197": {"en": "Check pump settings on boiler", "de": "Pumpeneinstellung am Kessel überprüfen"},
    # External contacts and remote controls (201-248)
    "201": {"en": "Check external contact wiring HC1", "de": "Kontrolle Beschaltung externer Kontakt HK1"},
    "202": {"en": "Check external contact wiring HC2", "de": "Kontrolle Beschaltung externer Kontakt HK2"},
    "203": {"en": "Check external contact wiring HC3", "de": "Kontrolle Beschaltung externer Kontakt HK3"},
    "204": {"en": "Check external contact wiring HC4", "de": "Kontrolle Beschaltung externer Kontakt HK4"},
    "205": {"en": "Check external contact wiring HC5", "de": "Kontrolle Beschaltung externer Kontakt HK5"},
    "206": {"en": "Check external contact wiring HC6", "de": "Kontrolle Beschaltung externer Kontakt HK6"},
    "210": {"en": "Remote FR35 HCA not connected", "de": "Fernbedienung FR35 HKA nicht angeschlossen"},
    "211": {"en": "Remote FR35 HC1 not connected", "de": "Fernbedienung FR35 HK1 nicht angeschlossen"},
    "212": {"en": "Remote FR35 HC2 not connected", "de": "Fernbedienung FR35 HK2 nicht angeschlossen"},
    "213": {"en": "Remote FR35 HC3 not connected", "de": "Fernbedienung FR35 HK3 nicht angeschlossen"},
    "214": {"en": "Remote FR35 HC4 not connected", "de": "Fernbedienung FR35 HK4 nicht angeschlossen"},
    "215": {"en": "Remote FR35 HC5 not connected", "de": "Fernbedienung FR35 HK5 nicht angeschlossen"},
    "216": {"en": "Remote FR35 HC6 not connected", "de": "Fernbedienung FR35 HK6 nicht angeschlossen"},
    "217": {"en": "Remote FR35 HCB not connected", "de": "Fernbedienung FR35 HKB nicht angeschlossen"},
    "220": {"en": "Remote FR40 HCA not connected", "de": "Fernbedienung FR40 HKA nicht angeschlossen"},
    "221": {"en": "Remote FR40 HC1 not connected", "de": "Fernbedienung FR40 HK1 nicht angeschlossen"},
    "222": {"en": "Remote FR40 HC2 not connected", "de": "Fernbedienung FR40 HK2 nicht angeschlossen"},
    "223": {"en": "Remote FR40 HC3 not connected", "de": "Fernbedienung FR40 HK3 nicht angeschlossen"},
    "224": {"en": "Remote FR40 HC4 not connected", "de": "Fernbedienung FR40 HK4 nicht angeschlossen"},
    "225": {"en": "Remote FR40 HC5 not connected", "de": "Fernbedienung FR40 HK5 nicht angeschlossen"},
    "226": {"en": "Remote FR40 HC6 not connected", "de": "Fernbedienung FR40 HK6 nicht angeschlossen"},
    "227": {"en": "Storage room switch off", "de": "Lagerraumschalter aus"},
    "228": {"en": "Pellet container almost empty", "de": "Pelletsbehälter fast leer"},
    "229": {"en": "Check level indicator", "de": "Füllstandsmelder kontrollieren"},
    "233": {"en": "Remote FR40 HCB not connected", "de": "Fernbedienung FR40 HKB nicht angeschlossen"},
    "240": {"en": "Remote control mismatch HCA", "de": "Fernbedienung stimmt nicht zur Parametrierung HKA"},
    "241": {"en": "Remote control mismatch HC1", "de": "Fernbedienung stimmt nicht zur Parametrierung HK1"},
    "242": {"en": "Remote control mismatch HC2", "de": "Fernbedienung stimmt nicht zur Parametrierung HK2"},
    "243": {"en": "Remote control mismatch HC3", "de": "Fernbedienung stimmt nicht zur Parametrierung HK3"},
    "244": {"en": "Remote control mismatch HC4", "de": "Fernbedienung stimmt nicht zur Parametrierung HK4"},
    "245": {"en": "Remote control mismatch HC5", "de": "Fernbedienung stimmt nicht zur Parametrierung HK5"},
    "246": {"en": "Remote control mismatch HC6", "de": "Fernbedienung stimmt nicht zur Parametrierung HK6"},
    "247": {"en": "Remote control mismatch HCB", "de": "Fernbedienung stimmt nicht zur Parametrierung HKB"},
    "248": {"en": "Check external request wiring", "de": "Kontrolle Beschaltung externe Anforderung"},
    # Cascade and communication (230-236)
    "230": {"en": "Communication error to lead boiler", "de": "Kommunikationsfehler zu Führungskessel"},
    "231": {"en": "Follower boiler failed", "de": "Folgekessel ausgefallen"},
    "232": {"en": "Follower boiler fault", "de": "Folgekessel Störung"},
    "235": {"en": "CHP unit in fault or off", "de": "KWK in Störung oder auf Aus"},
    "236": {"en": "External boiler in fault or off", "de": "Fremdkessel in Störung oder auf Aus"},
    # Switching unit and motor board (250-262)
    "250": {"en": "Switching unit motor board not connected", "de": "Motorplatine Umschalteinheit nicht angeschlossen"},
    "251": {"en": "Switching unit motor not connected", "de": "Motor Umschalteinheit nicht angeschlossen"},
    "252": {"en": "Switching unit position not reached", "de": "Umschalteinheit erreicht Position nicht"},
    "253": {"en": "AUP motor short circuit", "de": "Motor AUP Kurzschluss"},
    "254": {"en": "AUP motor board overtemperature", "de": "Motorplatine AUP Übertemperatur"},
    "255": {"en": "AUP motor board undervoltage 24V", "de": "Motorplatine AUP Unterspannung 24V"},
    "256": {"en": "Switching unit not in position", "de": "Umschalteinheit nicht in Position"},
    "260": {"en": "DRM AHF board not connected", "de": "DRM AHF-Platine nicht angeschlossen"},
    "261": {"en": "DRM AHF board phase sequence wrong", "de": "DRM AHF-Platine Phasenfolge falsch"},
    "262": {"en": "Room auger motor not connected or fuse defective", "de": "Motor Raumaustragung nicht angeschlossen oder Sicherung defekt"},
    "275": {"en": "Confirm to continue - cause: STB", "de": "Zum Fortsetzen Meldung quittieren, Ursache: STB"},
    # Differential controllers (280-297)
    "280": {"en": "Differential controller CAN D not connected", "de": "Differenzregler CAN D nicht angeschlossen"},
    "281": {"en": "Heat source sensor S1 short circuit", "de": "Wärmequellenfühler S1 Kurzschluss"},
    "282": {"en": "Heat source sensor S1 disconnected", "de": "Wärmequellenfühler S1 Unterbrechung"},
    "283": {"en": "Reference sensor S2 short circuit", "de": "Referenzfühler S2 Kurzschluss"},
    "284": {"en": "Reference sensor S2 disconnected", "de": "Referenzfühler S2 Unterbrechung"},
    "285": {"en": "Return sensor external boiler short circuit", "de": "Rücklauffühler Fremdwärmekessel Kurzschluss"},
    "286": {"en": "Return sensor external boiler disconnected", "de": "Rücklauffühler Fremdwärmekessel Unterbrechung"},
    "287": {"en": "Return temp external boiler not reached", "de": "Rücklauftemperatur Fremdwärmekessel nicht erreicht"},
    "290": {"en": "Differential controller 2 CAN 9 not connected", "de": "Differenzregler 2 CAN 9 nicht angeschlossen"},
    "291": {"en": "Heat source sensor S3 short circuit", "de": "Wärmequellenfühler S3 Kurzschluss"},
    "292": {"en": "Heat source sensor S3 disconnected", "de": "Wärmequellenfühler S3 Unterbrechung"},
    "293": {"en": "Reference sensor S4 short circuit", "de": "Referenzfühler S4 Kurzschluss"},
    "294": {"en": "Reference sensor S4 disconnected", "de": "Referenzfühler S4 Unterbrechung"},
    "295": {"en": "Return sensor external boiler 2 short circuit", "de": "Rücklauffühler Fremdwärmekessel 2 Kurzschluss"},
    "296": {"en": "Return sensor external boiler 2 disconnected", "de": "Rücklauffühler Fremdwärmekessel 2 Unterbrechung"},
    "297": {"en": "Return temp external boiler 2 not reached", "de": "Rücklauftemperatur Fremdwärmekessel 2 nicht erreicht"},
    # Boiler ID and storage room (305-332)
    "305": {"en": "Wrong boiler ID card", "de": "Falsche Kessel ID-Card"},
    "309": {"en": "Reload Wood", "de": "Nachlegen"},
    "310": {"en": "ATTENTION! Combustor temperature exceeded 92°C", "de": "ACHTUNG! Kesseltemperatur bei letztem Abbrand erreichte über 92°C"},
    "314": {"en": "Ash screw blocked", "de": "Ascheschnecke blockiert"},
    "322": {"en": "Boiler ID card not connected", "de": "Kessel ID-Card nicht angeschlossen"},
    "332": {"en": "Storage room switch activated", "de": "Lagerraumschalter betätigt"},
    # Heating circuit controller connections (355-370)
    "355": {"en": "No connection to HKR 0", "de": "Keine Verbindung zu HKR 0"},
    "356": {"en": "No connection to HKR 1", "de": "Keine Verbindung zu HKR 1"},
    "357": {"en": "No connection to HKR 2", "de": "Keine Verbindung zu HKR 2"},
    "358": {"en": "No connection to HKR 3", "de": "Keine Verbindung zu HKR 3"},
    "359": {"en": "No connection to HKR 4", "de": "Keine Verbindung zu HKR 4"},
    "360": {"en": "No connection to HKR 5", "de": "Keine Verbindung zu HKR 5"},
    "361": {"en": "No connection to HKR 6", "de": "Keine Verbindung zu HKR 6"},
    "362": {"en": "No connection to HKR 7", "de": "Keine Verbindung zu HKR 7"},
    "363": {"en": "No connection to HKR 8", "de": "Keine Verbindung zu HKR 8"},
    "364": {"en": "No connection to HKR 9", "de": "Keine Verbindung zu HKR 9"},
    "365": {"en": "No connection to HKR 10", "de": "Keine Verbindung zu HKR 10"},
    "366": {"en": "No connection to HKR 11", "de": "Keine Verbindung zu HKR 11"},
    "367": {"en": "No connection to HKR 12", "de": "Keine Verbindung zu HKR 12"},
    "368": {"en": "No connection to HKR 13", "de": "Keine Verbindung zu HKR 13"},
    "369": {"en": "No connection to HKR 14", "de": "Keine Verbindung zu HKR 14"},
    "370": {"en": "No connection to HKR 15", "de": "Keine Verbindung zu HKR 15"},
    # Maintenance and combustion chamber (371-398)
    "371": {"en": "Check combustion chamber", "de": "Brennraum prüfen"},
    "380": {"en": "Service due - factory maintenance required", "de": "Wartung fällig, Werkswartung durchführen lassen"},
    "381": {"en": "Suction turbine runtime - replace carbon brushes", "de": "Laufzeit Saugturbine, Schleifkohlen tauschen"},
    "390": {"en": "Heat source sensor (board S, S4) short circuit", "de": "Wärmequellenfühler (Platine S, S4) Kurzschluss"},
    "391": {"en": "Heat source sensor (board S, S4) disconnected", "de": "Wärmequellenfühler (Platine S, S4) Unterbrechung"},
    "392": {"en": "Reference sensor (board S, S3) short circuit", "de": "Referenzfühler (Platine S, S3) Kurzschluss"},
    "393": {"en": "Reference sensor (board S, S3) disconnected", "de": "Referenzfühler (Platine S, S3) Unterbrechung"},
    "394": {"en": "Return sensor external boiler 3 short circuit", "de": "Rücklauffühler Fremdwärmekessel 3 Kurzschluss"},
    "395": {"en": "Return sensor external boiler 3 disconnected", "de": "Rücklauffühler Fremdwärmekessel 3 Unterbrechung"},
    "396": {"en": "Return temp external boiler 3 not reached", "de": "Rücklauftemperatur Fremdwärmekessel 3 nicht erreicht"},
    "397": {"en": "Reference sensor (board S, S2) short circuit", "de": "Referenzfühler (Platine S, S2) Kurzschluss"},
    "398": {"en": "Reference sensor (board S, S2) disconnected", "de": "Referenzfühler (Platine S, S2) Unterbrechung"},
    # Freshwater station (422-498)
    "422": {"en": "Flow sensor FWS 1 short circuit", "de": "Vorlauffühler FWS 1 Kurzschluss"},
    "423": {"en": "Flow sensor FWS 1 disconnected", "de": "Vorlauffühler FWS 1 Unterbrechung"},
    "424": {"en": "Flow sensor FWS 2 short circuit", "de": "Vorlauffühler FWS 2 Kurzschluss"},
    "425": {"en": "Flow sensor FWS 2 disconnected", "de": "Vorlauffühler FWS 2 Unterbrechung"},
    "426": {"en": "Flow sensor FWS 3 short circuit", "de": "Vorlauffühler FWS 3 Kurzschluss"},
    "427": {"en": "Flow sensor FWS 3 disconnected", "de": "Vorlauffühler FWS 3 Unterbrechung"},
    "428": {"en": "Flow sensor FWS 4 short circuit", "de": "Vorlauffühler FWS 4 Kurzschluss"},
    "429": {"en": "Flow sensor FWS 4 disconnected", "de": "Vorlauffühler FWS 4 Unterbrechung"},
    "440": {"en": "Heating circuit board CAN B not connected", "de": "Heizkreisplatine CAN B nicht angeschlossen"},
    "441": {"en": "Flow sensor HCB short circuit", "de": "Vorlauffühler HKB Kurzschluss"},
    "442": {"en": "Flow sensor HCB disconnected", "de": "Vorlauffühler HKB Unterbrechung"},
    "443": {"en": "DHW sensor B short circuit", "de": "Boilerfühler B Kurzschluss"},
    "444": {"en": "DHW sensor B disconnected", "de": "Boilerfühler B Unterbrechung"},
    "450": {"en": "Smart-HV not connected", "de": "Smart-HV nicht angeschlossen"},
    "452": {"en": "Smart combi master/slave config wrong", "de": "Smart-Kombi Parametrierung Master/Slave falsch"},
    "453": {"en": "Smart combi fault", "de": "Smart-Kombi Störung"},
    "480": {"en": "Buffer temp for DHW 1 too low", "de": "Puffertemperatur für Warmwasser 1 unterschritten"},
    "481": {"en": "Buffer temp for DHW 2 too low", "de": "Puffertemperatur für Warmwasser 2 unterschritten"},
    "482": {"en": "Buffer temp for DHW 3 too low", "de": "Puffertemperatur für Warmwasser 3 unterschritten"},
    "483": {"en": "Buffer temp for DHW 4 too low", "de": "Puffertemperatur für Warmwasser 4 unterschritten"},
    "487": {"en": "Circulation pump could not be calibrated", "de": "Zirkulationspumpe konnte nicht angelernt werden"},
    "488": {"en": "Flow sensor FWS short circuit", "de": "Vorlauffühler FWS Kurzschluss"},
    "489": {"en": "Flow sensor FWS disconnected", "de": "Vorlauffühler FWS Unterbrechung"},
    "490": {"en": "FWS 1 temperature sensor disconnected", "de": "Frischwasserstation 1 Temperaturfühler Unterbrechung"},
    "492": {"en": "FWS 1 temperature sensor short circuit", "de": "Frischwasserstation 1 Temperaturfühler Kurzschluss"},
    "493": {"en": "FWS 2 temperature sensor disconnected", "de": "Frischwasserstation 2 Temperaturfühler Unterbrechung"},
    "494": {"en": "FWS 2 temperature sensor short circuit", "de": "Frischwasserstation 2 Temperaturfühler Kurzschluss"},
    "495": {"en": "FWS 3 temperature sensor disconnected", "de": "Frischwasserstation 3 Temperaturfühler Unterbrechung"},
    "496": {"en": "FWS 3 temperature sensor short circuit", "de": "Frischwasserstation 3 Temperaturfühler Kurzschluss"},
    "497": {"en": "FWS 4 temperature sensor disconnected", "de": "Frischwasserstation 4 Temperaturfühler Unterbrechung"},
    "498": {"en": "FWS 4 temperature sensor short circuit", "de": "Frischwasserstation 4 Temperaturfühler Kurzschluss"},
    # IO-X10 expansion boards (540-571)
    "540": {"en": "Extension board 0 not connected", "de": "IO-X10-104 Erweiterungsplatine 0 nicht angeschlossen"},
    "541": {"en": "Extension board 1 not connected", "de": "IO-X10-104 Erweiterungsplatine 1 nicht angeschlossen"},
    "542": {"en": "Extension board 2 not connected", "de": "IO-X10-104 Erweiterungsplatine 2 nicht angeschlossen"},
    "543": {"en": "Extension board 3 not connected", "de": "IO-X10-104 Erweiterungsplatine 3 nicht angeschlossen"},
    "544": {"en": "Extension board 4 not connected", "de": "IO-X10-104 Erweiterungsplatine 4 nicht angeschlossen"},
    "545": {"en": "Extension board 5 not connected", "de": "IO-X10-104 Erweiterungsplatine 5 nicht angeschlossen"},
    "546": {"en": "Extension board 6 not connected", "de": "IO-X10-104 Erweiterungsplatine 6 nicht angeschlossen"},
    "547": {"en": "Extension board 7 not connected", "de": "IO-X10-104 Erweiterungsplatine 7 nicht angeschlossen"},
    "548": {"en": "Extension board 8 not connected", "de": "IO-X10-104 Erweiterungsplatine 8 nicht angeschlossen"},
    "549": {"en": "Extension board 9 not connected", "de": "IO-X10-104 Erweiterungsplatine 9 nicht angeschlossen"},
    "570": {"en": "Extension board A not connected", "de": "IO-X10-104 Erweiterungsplatine A nicht angeschlossen"},
    "571": {"en": "Extension board B not connected", "de": "IO-X10-104 Erweiterungsplatine B nicht angeschlossen"},
    # System and protocol (902-910)
    "902": {"en": "Error log initialized", "de": "Fehlerspeicher initialisiert"},
    "903": {"en": "Restart (Power ON)", "de": "Neustart (Power ON)"},
    "910": {"en": "Write to dongle failed", "de": "Schreiben auf Dongle fehlgeschlagen"},
    # Remote line board (1100-1102)
    "1100": {"en": "Remote line board CAN 0 not connected", "de": "Fernleitungsplatine CAN 0 nicht angeschlossen"},
    "1101": {"en": "Flow sensor remote line 2 short circuit", "de": "Vorlauffühler geregelte Fernleitung 2 Kurzschluss"},
    "1102": {"en": "Flow sensor remote line 2 disconnected", "de": "Vorlauffühler geregelte Fernleitung 2 Unterbrechung"},
    # Hardware test faults (4020-5275)
    "4020": {"en": "Room auger motor not connected", "de": "Raumschnecke Motor nicht angeschlossen"},
    "4030": {"en": "Fuse F15 defective", "de": "Sicherung F15 defekt"},
    "4120": {"en": "Suction turbine not connected", "de": "Saugturbine nicht angeschlossen"},
    "4130": {"en": "Fuse F21 defective (suction turbine)", "de": "Sicherung F21 defekt (Saugturbine)"},
    "4220": {"en": "Fuse F13 defective", "de": "Sicherung F13 defekt"},
    "4230": {"en": "Fuse F17 defective", "de": "Sicherung F17 defekt"},
    "4250": {"en": "Fuse F21 defective", "de": "Sicherung F21 defekt"},
    "4320": {"en": "Feed motor not connected", "de": "Einschubmotor nicht angeschlossen"},
    "4330": {"en": "Fuse F18 defective", "de": "Sicherung F18 defekt"},
    "4420": {"en": "Induced draft motor not connected", "de": "Saugzugmotor nicht angeschlossen"},
    "4430": {"en": "Fuse F20 defective", "de": "Sicherung F20 defekt"},
    "4630": {"en": "Fuse F19 defective (ignition)", "de": "Sicherung F19 defekt (Zündung)"},
    "4720": {"en": "Ignition not connected", "de": "Zündung nicht angeschlossen"},
    "4820": {"en": "Cleaning device not connected", "de": "Putzeinrichtung nicht angeschlossen"},
    "5020": {"en": "Grate drive not connected", "de": "Schieberost nicht angeschlossen"},
    "5120": {"en": "Room auger 2 motor not connected", "de": "Motor Raumaustragung 2 nicht angeschlossen"},
    "5220": {"en": "HC1 pump not connected or safety thermostat triggered", "de": "HK1 Pumpe nicht angeschlossen oder Sicherheitsthermostat ausgelöst"},
    "5270": {"en": "Overcurrent room auger 1 - check auger and turbine", "de": "Überstrom Raumaustragungsschnecke 1, Saugturbine überprüfen"},
    "5275": {"en": "Thermal protection room auger 1", "de": "Thermoschutz Raumaustragungsschnecke 1"},
}

# Bilingual names, optional enums, and declared sensor metadata for known XML parameters.
# Firmware-specific profiles recursively override individual fields in this table.
PARAMETER_DESCRIPTIONS: Final[dict[str, ParameterDescription]] = {
    # ===== ANALOG PARAMETERS (0-111) =====

    # Boiler core (0-10)
    "ZK": {
        "en": "Boiler State",
        "de": "Kesselzustand",
        "enum": {
            0: {
                "en": "Unknown",
                "de": "Unbekannt"
            },
            1: {
                "en": "Off",
                "de": "Aus"
            },
            2: {
                "en": "Preparing start",
                "de": "Startvorbereitung"
            },
            3: {
                "en": "Boiler start",
                "de": "Kessel Start"
            },
            4: {
                "en": "Monitoring ignition",
                "de": "Zündüberwachung"
            },
            5: {
                "en": "Ignition",
                "de": "Zündung"
            },
            6: {
                "en": "Transition to FF",
                "de": "Übergang LB",
                "icon": "mdi:fireplace"
            },
            7: {
                "en": "Full firing",
                "de": "Leistungsbrand",
                "icon": "mdi:fireplace"
            },
            8: {
                "en": "Ember preservation",
                "de": "Gluterhaltung"
            },
            9: {
                "en": "Waiting for AR",
                "de": "Warten auf EA"
            },
            10: {
                "en": "Ash removal",
                "de": "Entaschung"
            },
            11: {
                "en": "-",
                "de": "-"
            },
            12: {
                "en": "Cleaning",
                "de": "Putzen"
            }
        },
        "device_class": None,
        "state_class": None,
        "sensor_type": "boiler_state",
        "entity_id_suffix": "state",
        "icon": "mdi:fireplace-off"
    },
    "O2": {
        "en": "O2 Level",
        "de": "O2-Gehalt",
        "device_class": None,
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:chart-line"
    },
    "O2soll": {
        "en": "O2 Setpoint",
        "de": "O2-Sollwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "TK": {
        "en": "Boiler Temperature",
        "de": "Kesseltemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer"
    },
    "TKsoll": {
        "en": "Boiler Setpoint",
        "de": "Kessel-Solltemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-lines"
    },
    "TRL": {
        "en": "Return Temperature",
        "de": "Rücklauftemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:coolant-temperature"
    },
    "TRLsoll": {
        "en": "Return Setpoint",
        "de": "Rücklauf-Solltemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Spreizung": {
        "en": "Temperature Spread",
        "de": "Temperaturspreizung",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRG": {
        "en": "Flue Gas Temperature",
        "de": "Rauchgastemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:smoke"
    },
    "SZist": {
        "en": "Draft Actual",
        "de": "Saugzug Ist",
        "device_class": None,
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:fan"
    },
    "SZsoll": {
        "en": "Draft Setpoint",
        "de": "Saugzug Soll",
        "device_class": None,
        "state_class": "measurement"
    },

    # Buffer (11-19)
    "TPo": {
        "en": "Buffer Top",
        "de": "Puffer Oben",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-lines"
    },
    "TPm": {
        "en": "Buffer Middle",
        "de": "Puffer Mitte",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-lines"
    },
    "TPu": {
        "en": "Buffer Bottom",
        "de": "Puffer Unten",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-lines"
    },
    "Puff Füllgrad": {
        "en": "Buffer Fill Level",
        "de": "Pufferfüllgrad",
        "device_class": None,
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:battery-medium"
    },
    "Puff Fuellgrad": {
        "en": "Buffer Fill Level",
        "de": "Pufferfüllgrad",
        "device_class": None,
        "state_class": "measurement"
    },  # V14_0HAR_q ASCII variant
    "Puffer_soll oben": {
        "en": "Buffer Setpoint Top",
        "de": "Puffer Sollwert Oben",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-plus"
    },
    "Puffer_soll unten": {
        "en": "Buffer Setpoint Bottom",
        "de": "Puffer Sollwert Unten",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer-minus"
    },
    "PuffZustand": {
        "en": "Buffer State",
        "de": "Pufferzustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "Max Anf Kessel": {
        "en": "Max Boiler Demand",
        "de": "Max Kesselanforderung",
        "device_class": None,
        "state_class": "measurement"
    },
    "TFW": {
        "en": "Fresh Water Temperature",
        "de": "Frischwassertemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },

    # Power & Control (20-29)
    "Leistung": {
        "en": "Output Power",
        "de": "Ausgangsleistung",
        "device_class": None,
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:gauge"
    },
    "ESsoll": {
        "en": "Auger Setpoint",
        "de": "Einschubschnecke Soll",
        "device_class": None,
        "state_class": "measurement"
    },
    "min.Leist.TRG": {
        "en": "Min Power Flue Gas",
        "de": "Min Leistung Rauchgas",
        "device_class": None,
        "state_class": "measurement"
    },
    "max.Leist.TRG": {
        "en": "Max Power Flue Gas",
        "de": "Max Leistung Rauchgas",
        "device_class": None,
        "state_class": "measurement"
    },
    "max.Leist.Fuell": {
        "en": "Max Power Fill",
        "de": "Max Leistung Füllung",
        "device_class": None,
        "state_class": "measurement"
    },
    "max.Leist.TPO": {
        "en": "Max Power Buffer Top",
        "de": "Max Leistung Puffer Oben",
        "device_class": None,
        "state_class": "measurement"
    },
    "ESRegler": {
        "en": "Auger Controller",
        "de": "Einschubschnecken-Regler",
        "device_class": None,
        "state_class": "measurement"
    },
    "Regler K": {
        "en": "Controller K",
        "de": "Regler K",
        "device_class": None,
        "state_class": "measurement"
    },
    "KeBrstScale": {
        "en": "Boiler Burner Scale",
        "de": "Kessel-Brenner-Skalierung",
        "device_class": None,
        "state_class": "measurement"
    },
    "Programm": {
        "en": "Program",
        "de": "Programm",
        "device_class": None,
        "state_class": "measurement"
    },

    # Error & System (30-42)
    "Störungs Nr": {
        "en": "Error Code",
        "de": "Störungsnummer",
        "device_class": None,
        "state_class": "measurement",
        "sensor_type": "error",
        "entity_id_suffix": "operation",
        "icon": "mdi:alert",
        "ok_icon": "mdi:check",
        "sensor_name": {
            "en": "Operation Status",
            "de": "Betriebsstatus"
        }
    },
    "Storungs Nr": {
        "en": "Error Code",
        "de": "Störungsnummer",
        "device_class": None,
        "state_class": "measurement"
    },  # V14_0HAR_q typo variant (keep for entity ID stability)
    "Stoerungs Nr": {
        "en": "Error Code",
        "de": "Störungsnummer",
        "device_class": None,
        "state_class": None
    },  # V14_0HAR_q proper ASCII variant
    "Max Anf ZenPuf": {
        "en": "Max Central Buffer Demand",
        "de": "Max Zentralpuffer-Anforderung",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "I Es": {
        "en": "Current Auger",
        "de": "Strom Einschubschnecke",
        "device_class": "current",
        "state_class": "measurement"
    },
    "I Ra": {
        "en": "Current Grate",
        "de": "Strom Rost",
        "device_class": "current",
        "state_class": "measurement"
    },
    "I Aa": {
        "en": "Current Ash Auger",
        "de": "Strom Aschenschnecke",
        "device_class": "current",
        "state_class": "measurement"
    },
    "I Sr": {
        "en": "Current Stoker",
        "de": "Strom Schürer",
        "device_class": "current",
        "state_class": "measurement"
    },
    "I Rein": {
        "en": "Current Cleaning",
        "de": "Strom Reinigung",
        "device_class": "current",
        "state_class": "measurement"
    },
    "BLDC_ES ist": {
        "en": "BLDC Auger Actual",
        "de": "BLDC Einschubschnecke Ist",
        "device_class": None,
        "state_class": "measurement"
    },
    "BLDC_ES soll": {
        "en": "BLDC Auger Setpoint",
        "de": "BLDC Einschubschnecke Soll",
        "device_class": None,
        "state_class": "measurement"
    },
    "LZ ES seit Füll.": {
        "en": "Runtime Since Fill",
        "de": "Laufzeit seit Füllung",
        "device_class": None,
        "state_class": "measurement"
    },
    "LZ ES seit Fuell.": {
        "en": "Runtime Since Fill",
        "de": "Laufzeit seit Füllung",
        "device_class": None,
        "state_class": "measurement"
    },  # V14_0HAR_q ASCII variant
    "LZ ES seit Ent.": {
        "en": "Runtime Since Ash",
        "de": "Laufzeit seit Entaschung",
        "device_class": None,
        "state_class": "measurement"
    },
    "Anzahl Entasch.": {
        "en": "Ash Removal Count",
        "de": "Anzahl Entaschungen",
        "device_class": None,
        "state_class": "measurement"
    },
    "Anzahl SR Beweg.": {
        "en": "Stoker Movement Count",
        "de": "Anzahl Schürerbewegungen",
        "device_class": None,
        "state_class": "measurement"
    },

    # Pellets (43-44)
    "Lagerstand": {
        "en": "Pellet Stock",
        "de": "Pelletvorrat",
        "device_class": None,
        "state_class": "total",
        "standard": True,
        "icon": "mdi:silo"
    },
    "Verbrauchszähler": {
        "en": "Pellet Consumption",
        "de": "Pelletverbrauch",
        "device_class": None,
        "state_class": "total_increasing",
        "standard": True,
        "icon": "mdi:counter"
    },
    "Verbrauchszaehler": {
        "en": "Pellet Consumption",
        "de": "Pelletverbrauch",
        "device_class": None,
        "state_class": "total_increasing"
    },  # V14_0HAR_q ASCII variant

    # Lambda Probe (45-49)
    "Heiz P Lambda": {
        "en": "Lambda Heating Power",
        "de": "Lambda Heizleistung",
        "device_class": None,
        "state_class": "measurement"
    },
    "Heiz U Lambda": {
        "en": "Lambda Heating Voltage",
        "de": "Lambda Heizspannung",
        "device_class": None,
        "state_class": "measurement"
    },
    "Heiz I Lambda": {
        "en": "Lambda Heating Current",
        "de": "Lambda Heizstrom",
        "device_class": "current",
        "state_class": "measurement"
    },
    "U_Lambda": {
        "en": "Lambda Voltage",
        "de": "Lambda Spannung",
        "device_class": None,
        "state_class": "measurement"
    },
    "U Netzteil": {
        "en": "Power Supply Voltage",
        "de": "Netzteil-Spannung",
        "device_class": None,
        "state_class": "measurement"
    },

    # Temperatures (50-58)
    "T Spülung": {
        "en": "Flushing Temperature",
        "de": "Spültemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "T Spuelung": {
        "en": "Flushing Temperature",
        "de": "Spültemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },  # V14_0HAR_q ASCII variant
    "BRT": {
        "en": "Burner Temperature",
        "de": "Brennraumtemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:fire"
    },
    "Tplat": {
        "en": "Board Temperature",
        "de": "Platinentemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVG": {
        "en": "Pre-Flow Temperature",
        "de": "Vorlauftemperatur Gesamt",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVG2": {
        "en": "Pre-Flow Temperature 2",
        "de": "Vorlauftemperatur 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "AIN17": {
        "en": "Analog Input 17",
        "de": "Analogeingang 17",
        "device_class": None,
        "state_class": "measurement"
    },
    "Taus": {
        "en": "Outside Temperature",
        "de": "Außentemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:thermometer"
    },
    "TA Gem.": {
        "en": "Average Outside Temperature",
        "de": "Außentemperatur Gemittelt",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Effizienz": {
        "en": "Efficiency",
        "de": "Wirkungsgrad",
        "device_class": None,
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:speedometer"
    },

    # External Heating Circuit (59-66)
    "ExtHK Solltmp.": {
        "en": "Ext. HC Setpoint",
        "de": "Ext. Heizkreis Solltemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVL_A": {
        "en": "Flow HC A",
        "de": "Vorlauf HK A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_A": {
        "en": "Flow Setpoint HC A",
        "de": "Vorlauf Soll HK A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_A": {
        "en": "Return HC A",
        "de": "Rücklauf HK A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_A": {
        "en": "Return Setpoint HC A",
        "de": "Rücklauf Soll HK A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_A": {
        "en": "State HC A",
        "de": "Zustand HK A",
        "device_class": None,
        "state_class": "measurement"
    },
    "FRA Zustand": {
        "en": "Room Thermostat A State",
        "de": "Raumthermostat A Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "HKPA Status": {
        "en": "Pump A Status",
        "de": "Heizkreispumpe A Status",
        "device_class": None,
        "state_class": "measurement"
    },

    # Heating Circuit 1 (67-73)
    "TVL_1": {
        "en": "Flow HC 1",
        "de": "Vorlauf HK 1",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:coolant-temperature"
    },
    "TVLs_1": {
        "en": "Flow Setpoint HC 1",
        "de": "Vorlauf Soll HK 1",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:target"
    },
    "TRA_1": {
        "en": "Return HC 1",
        "de": "Rücklauf HK 1",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_1": {
        "en": "Return Setpoint HC 1",
        "de": "Rücklauf Soll HK 1",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_1": {
        "en": "State HC 1",
        "de": "Zustand HK 1",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR1 Zustand": {
        "en": "Room Thermostat 1 State",
        "de": "Raumthermostat 1 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "HKP1 Status": {
        "en": "Pump 1 Status",
        "de": "Heizkreispumpe 1 Status",
        "device_class": None,
        "state_class": "measurement"
    },

    # Heating Circuit 2 (74-80)
    "TVL_2": {
        "en": "Flow HC 2",
        "de": "Vorlauf HK 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_2": {
        "en": "Flow Setpoint HC 2",
        "de": "Vorlauf Soll HK 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_2": {
        "en": "Return HC 2",
        "de": "Rücklauf HK 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_2": {
        "en": "Return Setpoint HC 2",
        "de": "Rücklauf Soll HK 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_2": {
        "en": "State HC 2",
        "de": "Zustand HK 2",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR2 Zustand": {
        "en": "Room Thermostat 2 State",
        "de": "Raumthermostat 2 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "HKP2 Status": {
        "en": "Pump 2 Status",
        "de": "Heizkreispumpe 2 Status",
        "device_class": None,
        "state_class": "measurement"
    },

    # Heating Circuit B (81-87)
    "TVL_B": {
        "en": "Flow HC B",
        "de": "Vorlauf HK B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_B": {
        "en": "Flow Setpoint HC B",
        "de": "Vorlauf Soll HK B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_B": {
        "en": "Return HC B",
        "de": "Rücklauf HK B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_B": {
        "en": "Return Setpoint HC B",
        "de": "Rücklauf Soll HK B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_B": {
        "en": "State HC B",
        "de": "Zustand HK B",
        "device_class": None,
        "state_class": "measurement"
    },
    "FRB Zustand": {
        "en": "Room Thermostat B State",
        "de": "Raumthermostat B Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "HKPB Status": {
        "en": "Pump B Status",
        "de": "Heizkreispumpe B Status",
        "device_class": None,
        "state_class": "measurement"
    },

    # Hot Water (88-93)
    "TBA": {
        "en": "Hot Water A",
        "de": "Warmwasser A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TBs_A": {
        "en": "Hot Water Setpoint A",
        "de": "Warmwasser Soll A",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TB1": {
        "en": "Hot Water 1",
        "de": "Warmwasser 1",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:water-boiler"
    },
    "TBs_1": {
        "en": "Hot Water Setpoint 1",
        "de": "Warmwasser Soll 1",
        "device_class": "temperature",
        "state_class": "measurement",
        "standard": True,
        "icon": "mdi:target"
    },
    "TBB": {
        "en": "Hot Water B",
        "de": "Warmwasser B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TBs_B": {
        "en": "Hot Water Setpoint B",
        "de": "Warmwasser Soll B",
        "device_class": "temperature",
        "state_class": "measurement"
    },

    # Heating Circuit Demands (94-110)
    "HKR Anf": {
        "en": "HC Demand",
        "de": "Heizkreis-Anforderung",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR0": {
        "en": "Demand HC 0",
        "de": "Anforderung HK 0",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR1": {
        "en": "Demand HC 1",
        "de": "Anforderung HK 1",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR2": {
        "en": "Demand HC 2",
        "de": "Anforderung HK 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR3": {
        "en": "Demand HC 3",
        "de": "Anforderung HK 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR4": {
        "en": "Demand HC 4",
        "de": "Anforderung HK 4",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR5": {
        "en": "Demand HC 5",
        "de": "Anforderung HK 5",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR6": {
        "en": "Demand HC 6",
        "de": "Anforderung HK 6",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR7": {
        "en": "Demand HC 7",
        "de": "Anforderung HK 7",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR8": {
        "en": "Demand HC 8",
        "de": "Anforderung HK 8",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR9": {
        "en": "Demand HC 9",
        "de": "Anforderung HK 9",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR10": {
        "en": "Demand HC 10",
        "de": "Anforderung HK 10",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR11": {
        "en": "Demand HC 11",
        "de": "Anforderung HK 11",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR12": {
        "en": "Demand HC 12",
        "de": "Anforderung HK 12",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR13": {
        "en": "Demand HC 13",
        "de": "Anforderung HK 13",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR14": {
        "en": "Demand HC 14",
        "de": "Anforderung HK 14",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Anf. HKR15": {
        "en": "Demand HC 15",
        "de": "Anforderung HK 15",
        "device_class": "temperature",
        "state_class": "measurement"
    },

    # Water Pressure (111)
    "Wasserdruck": {
        "en": "Water Pressure",
        "de": "Wasserdruck",
        "device_class": "pressure",
        "state_class": "measurement"
    },

    # ===== DIGITAL PARAMETERS =====

    # Digital 0 - System Status
    "Störung": {
        "en": "Error",
        "de": "Störung",
        "device_class": None,
        "state_class": None
    },
    "Stoerung": {
        "en": "Error",
        "de": "Störung",
        "device_class": None,
        "state_class": None
    },  # V14_0HAR_q ASCII variant
    "Stb": {
        "en": "Standby",
        "de": "Standby",
        "device_class": None,
        "state_class": None
    },
    "Fuellstand": {
        "en": "Fill Level",
        "de": "Füllstand",
        "device_class": None,
        "state_class": None
    },
    "RLP/PuffP": {
        "en": "Return Pump/Buffer Pump",
        "de": "Rücklaufpumpe/Pufferpumpe",
        "device_class": None,
        "state_class": None
    },
    "RLm_auf": {
        "en": "Return Mixer Open",
        "de": "Rücklaufmischer Auf",
        "device_class": None,
        "state_class": None
    },
    "RLm_zu": {
        "en": "Return Mixer Close",
        "de": "Rücklaufmischer Zu",
        "device_class": None,
        "state_class": None
    },
    "WS freig.": {
        "en": "Water Protection Release",
        "de": "Wasserschutz Freigabe",
        "device_class": None,
        "state_class": None
    },
    "Akt. Code": {
        "en": "Active Code",
        "de": "Aktiver Code",
        "device_class": None,
        "state_class": None
    },
    "FW Freig.": {
        "en": "Fresh Water Release",
        "de": "Frischwasser Freigabe",
        "device_class": None,
        "state_class": None
    },
    "gFlP": {
        "en": "Floorheating Pump",
        "de": "Fußbodenheizung Pumpe",
        "device_class": None,
        "state_class": None
    },
    "gFlM auf": {
        "en": "Floorheating Mixer Open",
        "de": "Fußbodenheizung Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "gFlM zu": {
        "en": "Floorheating Mixer Close",
        "de": "Fußbodenheizung Mischer Zu",
        "device_class": None,
        "state_class": None
    },
    "gFl2P": {
        "en": "Floorheating 2 Pump",
        "de": "Fußbodenheizung 2 Pumpe",
        "device_class": None,
        "state_class": None
    },
    "gFl2M auf": {
        "en": "Floorheating 2 Mixer Open",
        "de": "Fußbodenheizung 2 Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "gFl2M zu": {
        "en": "Floorheating 2 Mixer Close",
        "de": "Fußbodenheizung 2 Mischer Zu",
        "device_class": None,
        "state_class": None
    },

    # Digital 1 - Burner & Motors
    "L Heiz.": {
        "en": "Load Heating",
        "de": "Ladung Heizung",
        "device_class": None,
        "state_class": None
    },
    "Z Heiz.": {
        "en": "Ignition Heating",
        "de": "Zündung Heizung",
        "device_class": None,
        "state_class": None
    },
    "Z Geb.": {
        "en": "Ignition Blower",
        "de": "Zündgebläse",
        "device_class": None,
        "state_class": None
    },
    "AA Run": {
        "en": "Ash Auger Run",
        "de": "Aschenschnecke Läuft",
        "device_class": None,
        "state_class": None
    },
    "AA Dir": {
        "en": "Ash Auger Direction",
        "de": "Aschenschnecke Richtung",
        "device_class": None,
        "state_class": None
    },
    "ES Run": {
        "en": "Auger Run",
        "de": "Einschubschnecke Läuft",
        "device_class": None,
        "state_class": None
    },
    "ES Dir": {
        "en": "Auger Direction",
        "de": "Einschubschnecke Richtung",
        "device_class": None,
        "state_class": None
    },
    "AS Saug": {
        "en": "Ash Suction",
        "de": "Asche Saugen",
        "device_class": None,
        "state_class": None
    },
    "AS RA Run": {
        "en": "Ash Grate Run",
        "de": "Asche Rost Läuft",
        "device_class": None,
        "state_class": None
    },
    "AS RA Dir": {
        "en": "Ash Grate Direction",
        "de": "Asche Rost Richtung",
        "device_class": None,
        "state_class": None
    },
    "Rein En": {
        "en": "Cleaning Enable",
        "de": "Reinigung Aktiviert",
        "device_class": None,
        "state_class": None
    },
    "Rein Run": {
        "en": "Cleaning Run",
        "de": "Reinigung Läuft",
        "device_class": None,
        "state_class": None
    },
    "Es Rein Endl": {
        "en": "Auger Cleaning Endpoint",
        "de": "Einschubschnecke Reinigung Endlage",
        "device_class": None,
        "state_class": None
    },
    "sAS Anf Füll": {
        "en": "Ash Auger Fill Request",
        "de": "Aschenschnecke Anforderung Füllung",
        "device_class": None,
        "state_class": None
    },
    "sAS Anf Fuell": {
        "en": "Ash Auger Fill Request",
        "de": "Aschenschnecke Anforderung Füllung",
        "device_class": None,
        "state_class": None
    },  # V14_0HAR_q ASCII variant

    # Digital 2 - Heating Circuit Pumps & Mixers
    "HKPA": {
        "en": "HC Pump A",
        "de": "Heizkreispumpe A",
        "device_class": None,
        "state_class": None
    },
    "MAA": {
        "en": "Mixer A Open",
        "de": "Mischer A Auf",
        "device_class": None,
        "state_class": None
    },
    "MAZ": {
        "en": "Mixer A Close",
        "de": "Mischer A Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP1": {
        "en": "HC Pump 1",
        "de": "Heizkreispumpe 1",
        "device_class": None,
        "state_class": None
    },
    "M1A": {
        "en": "Mixer 1 Open",
        "de": "Mischer 1 Auf",
        "device_class": None,
        "state_class": None
    },
    "M1Z": {
        "en": "Mixer 1 Close",
        "de": "Mischer 1 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP2": {
        "en": "HC Pump 2",
        "de": "Heizkreispumpe 2",
        "device_class": None,
        "state_class": None
    },
    "M2A": {
        "en": "Mixer 2 Open",
        "de": "Mischer 2 Auf",
        "device_class": None,
        "state_class": None
    },
    "M2Z": {
        "en": "Mixer 2 Close",
        "de": "Mischer 2 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP3": {
        "en": "HC Pump 3",
        "de": "Heizkreispumpe 3",
        "device_class": None,
        "state_class": None
    },
    "M3A": {
        "en": "Mixer 3 Open",
        "de": "Mischer 3 Auf",
        "device_class": None,
        "state_class": None
    },
    "M3Z": {
        "en": "Mixer 3 Close",
        "de": "Mischer 3 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP4": {
        "en": "HC Pump 4",
        "de": "Heizkreispumpe 4",
        "device_class": None,
        "state_class": None
    },
    "M4A": {
        "en": "Mixer 4 Open",
        "de": "Mischer 4 Auf",
        "device_class": None,
        "state_class": None
    },
    "M4Z": {
        "en": "Mixer 4 Close",
        "de": "Mischer 4 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP5": {
        "en": "HC Pump 5",
        "de": "Heizkreispumpe 5",
        "device_class": None,
        "state_class": None
    },
    "M5A": {
        "en": "Mixer 5 Open",
        "de": "Mischer 5 Auf",
        "device_class": None,
        "state_class": None
    },
    "M5Z": {
        "en": "Mixer 5 Close",
        "de": "Mischer 5 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKP6": {
        "en": "HC Pump 6",
        "de": "Heizkreispumpe 6",
        "device_class": None,
        "state_class": None
    },
    "M6A": {
        "en": "Mixer 6 Open",
        "de": "Mischer 6 Auf",
        "device_class": None,
        "state_class": None
    },
    "M6Z": {
        "en": "Mixer 6 Close",
        "de": "Mischer 6 Zu",
        "device_class": None,
        "state_class": None
    },
    "HKPB": {
        "en": "HC Pump B",
        "de": "Heizkreispumpe B",
        "device_class": None,
        "state_class": None
    },
    "MBA": {
        "en": "Mixer B Open",
        "de": "Mischer B Auf",
        "device_class": None,
        "state_class": None
    },
    "MBZ": {
        "en": "Mixer B Close",
        "de": "Mischer B Zu",
        "device_class": None,
        "state_class": None
    },
    "HK-P Poolp": {
        "en": "HC Pool Pump",
        "de": "Heizkreis Poolpumpe",
        "device_class": None,
        "state_class": None
    },
    "HK-P Primp": {
        "en": "HC Primary Pump",
        "de": "Heizkreis Primärpumpe",
        "device_class": None,
        "state_class": None
    },
    "HK-P MA": {
        "en": "HC Mixer Open",
        "de": "Heizkreis Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "HK-P MZ": {
        "en": "HC Mixer Close",
        "de": "Heizkreis Mischer Zu",
        "device_class": None,
        "state_class": None
    },

    # Digital 3 - Boiler Pumps
    "BPA": {
        "en": "Boiler Pump A",
        "de": "Boilerpumpe A",
        "device_class": None,
        "state_class": None
    },
    "BP1": {
        "en": "Boiler Pump 1",
        "de": "Boilerpumpe 1",
        "device_class": None,
        "state_class": None
    },
    "BP2": {
        "en": "Boiler Pump 2",
        "de": "Boilerpumpe 2",
        "device_class": None,
        "state_class": None
    },
    "BP3": {
        "en": "Boiler Pump 3",
        "de": "Boilerpumpe 3",
        "device_class": None,
        "state_class": None
    },
    "BPB": {
        "en": "Boiler Pump B",
        "de": "Boilerpumpe B",
        "device_class": None,
        "state_class": None
    },
    "BZPA": {
        "en": "Circulation Pump A",
        "de": "Zirkulationspumpe A",
        "device_class": None,
        "state_class": None
    },
    "BZP1": {
        "en": "Circulation Pump 1",
        "de": "Zirkulationspumpe 1",
        "device_class": None,
        "state_class": None
    },
    "BZP2": {
        "en": "Circulation Pump 2",
        "de": "Zirkulationspumpe 2",
        "device_class": None,
        "state_class": None
    },
    "BZP3": {
        "en": "Circulation Pump 3",
        "de": "Zirkulationspumpe 3",
        "device_class": None,
        "state_class": None
    },
    "BZPB": {
        "en": "Circulation Pump B",
        "de": "Zirkulationspumpe B",
        "device_class": None,
        "state_class": None
    },

    # Digital 4 - System Components
    "Aschebox": {
        "en": "Ash Box",
        "de": "Aschebox",
        "device_class": None,
        "state_class": None
    },
    "Netztrafo": {
        "en": "Power Transformer",
        "de": "Netztrafo",
        "device_class": None,
        "state_class": None
    },
    "Netzrelais": {
        "en": "Power Relay",
        "de": "Netzrelais",
        "device_class": None,
        "state_class": None
    },
    "Lagerraum": {
        "en": "Storage Room",
        "de": "Lagerraum",
        "device_class": None,
        "state_class": None
    },
    "FLP": {
        "en": "Floorheating Pump",
        "de": "Fußbodenheizungspumpe",
        "device_class": None,
        "state_class": None
    },
    "ATW": {
        "en": "Heat Pump",
        "de": "Außentemperatur-Wärmepumpe",
        "device_class": None,
        "state_class": None
    },
    "Entasch gesp.": {
        "en": "Ash Removal Locked",
        "de": "Entaschung Gesperrt",
        "device_class": None,
        "state_class": None
    },
    "HKV": {
        "en": "HC Distribution",
        "de": "Heizkreisverteiler",
        "device_class": None,
        "state_class": None
    },
    "Spülung Aktiv": {
        "en": "Flushing Active",
        "de": "Spülung Aktiv",
        "device_class": None,
        "state_class": None
    },
    "Spuelung Aktiv": {
        "en": "Flushing Active",
        "de": "Spülung Aktiv",
        "device_class": None,
        "state_class": None
    },  # V14_0HAR_q ASCII variant
    "ExtHK vorh": {
        "en": "Ext HC Present",
        "de": "Ext Heizkreis Vorhanden",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_2 vorh": {
        "en": "Ext HC 2 Present",
        "de": "Ext Heizkreis 2 Vorhanden",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_3 vorh": {
        "en": "Ext HC 3 Present",
        "de": "Ext Heizkreis 3 Vorhanden",
        "device_class": None,
        "state_class": None
    },

    # Digital 6 - External HC & Cascades
    "ExtHK Anf": {
        "en": "Ext HC Request",
        "de": "Ext Heizkreis Anforderung",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_2 Anf": {
        "en": "Ext HC 2 Request",
        "de": "Ext Heizkreis 2 Anforderung",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_3 Anf": {
        "en": "Ext HC 3 Request",
        "de": "Ext Heizkreis 3 Anforderung",
        "device_class": None,
        "state_class": None
    },
    "ExtHK Pumpe": {
        "en": "Ext HC Pump",
        "de": "Ext Heizkreis Pumpe",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_2 Pumpe": {
        "en": "Ext HC 2 Pump",
        "de": "Ext Heizkreis 2 Pumpe",
        "device_class": None,
        "state_class": None
    },
    "ExtHK_3 Pumpe": {
        "en": "Ext HC 3 Pump",
        "de": "Ext Heizkreis 3 Pumpe",
        "device_class": None,
        "state_class": None
    },
    "KASK1 MinLeist": {
        "en": "Cascade 1 Min Power",
        "de": "Kaskade 1 Minimalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK2 MinLeist": {
        "en": "Cascade 2 Min Power",
        "de": "Kaskade 2 Minimalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK3 MinLeist": {
        "en": "Cascade 3 Min Power",
        "de": "Kaskade 3 Minimalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK4 MinLeist": {
        "en": "Cascade 4 Min Power",
        "de": "Kaskade 4 Minimalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK1 MaxLeist": {
        "en": "Cascade 1 Max Power",
        "de": "Kaskade 1 Maximalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK2 MaxLeist": {
        "en": "Cascade 2 Max Power",
        "de": "Kaskade 2 Maximalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK3 MaxLeist": {
        "en": "Cascade 3 Max Power",
        "de": "Kaskade 3 Maximalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK4 MaxLeist": {
        "en": "Cascade 4 Max Power",
        "de": "Kaskade 4 Maximalleistung",
        "device_class": None,
        "state_class": None
    },
    "KASK1 Run": {
        "en": "Cascade 1 Running",
        "de": "Kaskade 1 Läuft",
        "device_class": None,
        "state_class": None
    },
    "KASK2 Run": {
        "en": "Cascade 2 Running",
        "de": "Kaskade 2 Läuft",
        "device_class": None,
        "state_class": None
    },
    "KASK3 Run": {
        "en": "Cascade 3 Running",
        "de": "Kaskade 3 Läuft",
        "device_class": None,
        "state_class": None
    },
    "KASK4 Run": {
        "en": "Cascade 4 Running",
        "de": "Kaskade 4 Läuft",
        "device_class": None,
        "state_class": None
    },
    "KASK1 OK": {
        "en": "Cascade 1 OK",
        "de": "Kaskade 1 OK",
        "device_class": None,
        "state_class": None
    },
    "KASK2 OK": {
        "en": "Cascade 2 OK",
        "de": "Kaskade 2 OK",
        "device_class": None,
        "state_class": None
    },
    "KASK3 OK": {
        "en": "Cascade 3 OK",
        "de": "Kaskade 3 OK",
        "device_class": None,
        "state_class": None
    },
    "KASK4 OK": {
        "en": "Cascade 4 OK",
        "de": "Kaskade 4 OK",
        "device_class": None,
        "state_class": None
    },
    "Kask KWK Out": {
        "en": "Cascade CHP Output",
        "de": "Kaskade KWK Ausgang",
        "device_class": None,
        "state_class": None
    },
    "Kask FW Out": {
        "en": "Cascade FW Output",
        "de": "Kaskade FW Ausgang",
        "device_class": None,
        "state_class": None
    },
    "KASK KWK OK": {
        "en": "Cascade CHP OK",
        "de": "Kaskade KWK OK",
        "device_class": None,
        "state_class": None
    },
    "KASK FW OK": {
        "en": "Cascade FW OK",
        "de": "Kaskade FW OK",
        "device_class": None,
        "state_class": None
    },

    # Digital 5 - Reserved
    "Reserved_5": {
        "en": "Reserved Digital 5",
        "de": "Reserviert Digital 5",
        "device_class": None,
        "state_class": None
    },

    # Digital 7 - Pressure Controllers
    "DReg P2": {
        "en": "Pressure Ctrl Pump 2",
        "de": "Druckregler Pumpe 2",
        "device_class": None,
        "state_class": None
    },
    "DReg P3": {
        "en": "Pressure Ctrl Pump 3",
        "de": "Druckregler Pumpe 3",
        "device_class": None,
        "state_class": None
    },
    "DReg Mi auf": {
        "en": "Pressure Ctrl Mixer Open",
        "de": "Druckregler Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "DReg Mi zu": {
        "en": "Pressure Ctrl Mixer Close",
        "de": "Druckregler Mischer Zu",
        "device_class": None,
        "state_class": None
    },
    "DReg2 P2": {
        "en": "Pressure Ctrl 2 Pump 2",
        "de": "Druckregler 2 Pumpe 2",
        "device_class": None,
        "state_class": None
    },
    "DReg2 Mi auf": {
        "en": "Pressure Ctrl 2 Mixer Open",
        "de": "Druckregler 2 Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "DReg2 Mi zu": {
        "en": "Pressure Ctrl 2 Mixer Close",
        "de": "Druckregler 2 Mischer Zu",
        "device_class": None,
        "state_class": None
    },
    "DReg3 P2": {
        "en": "Pressure Ctrl 3 Pump 2",
        "de": "Druckregler 3 Pumpe 2",
        "device_class": None,
        "state_class": None
    },
    "DReg3 P3": {
        "en": "Pressure Ctrl 3 Pump 3",
        "de": "Druckregler 3 Pumpe 3",
        "device_class": None,
        "state_class": None
    },
    "DReg3 Mi auf": {
        "en": "Pressure Ctrl 3 Mixer Open",
        "de": "Druckregler 3 Mischer Auf",
        "device_class": None,
        "state_class": None
    },
    "DReg3 Mi zu": {
        "en": "Pressure Ctrl 3 Mixer Close",
        "de": "Druckregler 3 Mischer Zu",
        "device_class": None,
        "state_class": None
    },

    # Digital 8 - Reserved
    "Reserved_8": {
        "en": "Reserved Digital 8",
        "de": "Reserviert Digital 8",
        "device_class": None,
        "state_class": None
    },

    # ===== CLASSIC LAMBDA SPECIFIC PARAMETERS =====

    # Additional Buffer Sensors (Classic has 5 buffer sensors)
    "TPmo": {
        "en": "Buffer Middle-Upper",
        "de": "Puffer Mitte-Oben",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TPmu": {
        "en": "Buffer Middle-Lower",
        "de": "Puffer Mitte-Unten",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Puffer_soll": {
        "en": "Buffer Setpoint",
        "de": "Puffer Sollwert",
        "device_class": "temperature",
        "state_class": "measurement"
    },

    # Lambda Sensor (Classic naming)
    "Sens U Lambda": {
        "en": "Lambda Sensor Voltage",
        "de": "Lambda Sensorspannung",
        "device_class": None,
        "state_class": "measurement"
    },

    # Heating Circuits 3-6 (Classic supports up to 6 circuits)
    "TVL_3": {
        "en": "Flow HC 3",
        "de": "Vorlauf HK 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_3": {
        "en": "Flow Setpoint HC 3",
        "de": "Vorlauf Soll HK 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_3": {
        "en": "Return HC 3",
        "de": "Rücklauf HK 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_3": {
        "en": "Return Setpoint HC 3",
        "de": "Rücklauf Soll HK 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_3": {
        "en": "State HC 3",
        "de": "Zustand HK 3",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR3 Zustand": {
        "en": "Room Thermostat 3 State",
        "de": "Raumthermostat 3 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "TVL_4": {
        "en": "Flow HC 4",
        "de": "Vorlauf HK 4",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_4": {
        "en": "Flow Setpoint HC 4",
        "de": "Vorlauf Soll HK 4",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_4": {
        "en": "Return HC 4",
        "de": "Rücklauf HK 4",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_4": {
        "en": "Return Setpoint HC 4",
        "de": "Rücklauf Soll HK 4",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_4": {
        "en": "State HC 4",
        "de": "Zustand HK 4",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR4 Zustand": {
        "en": "Room Thermostat 4 State",
        "de": "Raumthermostat 4 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "TVL_5": {
        "en": "Flow HC 5",
        "de": "Vorlauf HK 5",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_5": {
        "en": "Flow Setpoint HC 5",
        "de": "Vorlauf Soll HK 5",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_5": {
        "en": "Return HC 5",
        "de": "Rücklauf HK 5",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_5": {
        "en": "Return Setpoint HC 5",
        "de": "Rücklauf Soll HK 5",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_5": {
        "en": "State HC 5",
        "de": "Zustand HK 5",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR5 Zustand": {
        "en": "Room Thermostat 5 State",
        "de": "Raumthermostat 5 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "TVL_6": {
        "en": "Flow HC 6",
        "de": "Vorlauf HK 6",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TVLs_6": {
        "en": "Flow Setpoint HC 6",
        "de": "Vorlauf Soll HK 6",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRA_6": {
        "en": "Return HC 6",
        "de": "Rücklauf HK 6",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRs_6": {
        "en": "Return Setpoint HC 6",
        "de": "Rücklauf Soll HK 6",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKZustand_6": {
        "en": "State HC 6",
        "de": "Zustand HK 6",
        "device_class": None,
        "state_class": "measurement"
    },
    "FR6 Zustand": {
        "en": "Room Thermostat 6 State",
        "de": "Raumthermostat 6 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },

    # Additional Hot Water (Classic supports TB2, TB3)
    "TB2": {
        "en": "Hot Water 2",
        "de": "Warmwasser 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TBs_2": {
        "en": "Hot Water Setpoint 2",
        "de": "Warmwasser Soll 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TB3": {
        "en": "Hot Water 3",
        "de": "Warmwasser 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TBs_3": {
        "en": "Hot Water Setpoint 3",
        "de": "Warmwasser Soll 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TRB": {
        "en": "Return HC B",
        "de": "Rücklauf HK B",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "BoiZustand_2": {
        "en": "Boiler State 2",
        "de": "Boilerzustand 2",
        "device_class": None,
        "state_class": "measurement"
    },

    # External Heating Circuits (Classic)
    "Ext.HK Soll": {
        "en": "Ext. HC Setpoint",
        "de": "Ext. HK Sollwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "Ext.HK Soll_2": {
        "en": "Ext. HC 2 Setpoint",
        "de": "Ext. HK 2 Sollwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "Ext.HK Soll_3": {
        "en": "Ext. HC 3 Setpoint",
        "de": "Ext. HK 3 Sollwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "Höchste Anf": {
        "en": "Highest Demand",
        "de": "Höchste Anforderung",
        "device_class": None,
        "state_class": "measurement"
    },
    "Anf. EHK Spg": {
        "en": "Ext. HC Voltage Demand",
        "de": "Ext. HK Spannungsanforderung",
        "device_class": None,
        "state_class": "measurement"
    },

    # Programs (Classic)
    "Programm HKM1": {
        "en": "Program HC Module 1",
        "de": "Programm HK Modul 1",
        "device_class": None,
        "state_class": "measurement"
    },
    "Programm HKM2": {
        "en": "Program HC Module 2",
        "de": "Programm HK Modul 2",
        "device_class": None,
        "state_class": "measurement"
    },
    "UsePos": {
        "en": "Position Usage",
        "de": "Positionsnutzung",
        "device_class": None,
        "state_class": "measurement"
    },
    "max.Leist.P3F.HT": {
        "en": "Max Power P3F HT",
        "de": "Max Leistung P3F HT",
        "device_class": None,
        "state_class": "measurement"
    },

    # External HC Pumps (Classic Digital)
    "EHKP": {
        "en": "Ext. HC Pump",
        "de": "Ext. Heizkreispumpe",
        "device_class": None,
        "state_class": None
    },
    "EHKP2": {
        "en": "Ext. HC Pump 2",
        "de": "Ext. Heizkreispumpe 2",
        "device_class": None,
        "state_class": None
    },
    "EHKP3": {
        "en": "Ext. HC Pump 3",
        "de": "Ext. Heizkreispumpe 3",
        "device_class": None,
        "state_class": None
    },
    "EHK Anf": {
        "en": "Ext. HC Demand",
        "de": "Ext. HK Anforderung",
        "device_class": None,
        "state_class": None
    },
    "EHK Anf2": {
        "en": "Ext. HC 2 Demand",
        "de": "Ext. HK 2 Anforderung",
        "device_class": None,
        "state_class": None
    },
    "EHK Anf3": {
        "en": "Ext. HC 3 Demand",
        "de": "Ext. HK 3 Anforderung",
        "device_class": None,
        "state_class": None
    },
    "DReg2 P3": {
        "en": "Pressure Ctrl 2 Pump 3",
        "de": "Druckregler 2 Pumpe 3",
        "device_class": None,
        "state_class": None
    },

    # ===== SOLAR EXTENSION PARAMETERS (V14_1HAR_q1_solar) =====

    # Solar Thermal (DiffR3 = Differential Controller 3)
    "DiffR3TWq": {
        "en": "Solar Heat Source Temp",
        "de": "Solar Temperatur Wärmequelle",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Solar DiffR3 K1": {
        "en": "Solar Diff Controller 1",
        "de": "Solar Differenzregler 1",
        "device_class": None,
        "state_class": "measurement"
    },
    "Solar DiffR3 K2": {
        "en": "Solar Diff Controller 2",
        "de": "Solar Differenzregler 2",
        "device_class": None,
        "state_class": "measurement"
    },
    "Solar DiffR3TDiff1": {
        "en": "Solar Temp Diff 1",
        "de": "Solar Temperaturdifferenz 1",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Solar DiffR3TDiff2": {
        "en": "Solar Temp Diff 2",
        "de": "Solar Temperaturdifferenz 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Solar DiffR3 P1": {
        "en": "Solar Pump 1",
        "de": "Solar Pumpe 1",
        "device_class": None,
        "state_class": "measurement"
    },
    "Solar DiffR3 P2": {
        "en": "Solar Pump 2",
        "de": "Solar Pumpe 2",
        "device_class": None,
        "state_class": "measurement"
    },
    "Solar DiffR3 P3": {
        "en": "Solar Pump 3",
        "de": "Solar Pumpe 3",
        "device_class": None,
        "state_class": "measurement"
    },
    "Solar DiffR3 P1 Reg.": {
        "en": "Solar Pump 1 Controller",
        "de": "Solar Pumpe 1 Regler",
        "device_class": None,
        "state_class": "measurement"
    },
    "DiffR3 WMZ_Ges": {
        "en": "Solar Total Heat",
        "de": "Solar Wärmemenge gesamt",
        "device_class": None,
        "state_class": "measurement"
    },
    "DiffR3 WMZ_Tag": {
        "en": "Solar Daily Heat",
        "de": "Solar Wärmemenge Tag",
        "device_class": None,
        "state_class": "measurement"
    },
    "DiffR3 WMZ_Moment": {
        "en": "Solar Current Heat",
        "de": "Solar Wärmemenge aktuell",
        "device_class": None,
        "state_class": "measurement"
    },

    # Ash Container Position (AUP)
    "AUPSoll": {
        "en": "Ash Container Setpoint",
        "de": "Aschebehälter Sollwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "AUPIst": {
        "en": "Ash Container Actual",
        "de": "Aschebehälter Istwert",
        "device_class": None,
        "state_class": "measurement"
    },
    "AUPStrom": {
        "en": "Ash Container Current",
        "de": "Aschebehälter Strom",
        "device_class": "current",
        "state_class": "measurement"
    },

    # Dummy Channels (placeholders for extended board configurations)
    "Dummy 1": {
        "en": "Dummy 1",
        "de": "Dummy 1",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Dummy 2": {
        "en": "Dummy 2",
        "de": "Dummy 2",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Dummy 3": {
        "en": "Dummy 3",
        "de": "Dummy 3",
        "device_class": "temperature",
        "state_class": "measurement"
    },

    # Digital variant with umlaut (V14_1HAR_q1_solar uses Füllstand instead of Fuellstand)
    "Füllstand": {
        "en": "Fill Level",
        "de": "Füllstand",
        "device_class": None,
        "state_class": None
    },
    "BoiZustand_1": {
        "en": "Boiler State 1",
        "de": "Boilerzustand 1",
        "device_class": None,
        "state_class": "measurement"
    },

    # V14_0d specific (HSV/CL 9-60KW)
    "MWZ Vorl.": {
        "en": "Heat Meter Flow",
        "de": "Wärmemengenzähler Vorlauf",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "MWZ Rueckl.": {
        "en": "Heat Meter Return",
        "de": "Wärmemengenzähler Rücklauf",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "MWZ Durchf.": {
        "en": "Heat Meter Flow Rate",
        "de": "Wärmemengenzähler Durchfluss",
        "device_class": None,
        "state_class": "measurement"
    },
    "MWZ Leist.": {
        "en": "Heat Meter Power",
        "de": "Wärmemengenzähler Leistung",
        "device_class": None,
        "state_class": "measurement"
    },
    "VFS Flow": {
        "en": "VFS Flow Rate",
        "de": "VFS Durchfluss",
        "device_class": None,
        "state_class": "measurement"
    },
    "VFS Temp": {
        "en": "VFS Temperature",
        "de": "VFS Temperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "SR motor": {
        "en": "Grate Motor",
        "de": "Schieberost Motor",
        "device_class": None,
        "state_class": "measurement"
    },
    "SRpos ist": {
        "en": "Grate Position Actual",
        "de": "Schieberost Position Ist",
        "device_class": None,
        "state_class": "measurement"
    },
    "SR mode": {
        "en": "Grate Mode",
        "de": "Schieberost Modus",
        "device_class": None,
        "state_class": "measurement"
    },
    "Mode Fw": {
        "en": "Firmware Mode",
        "de": "Firmware Modus",
        "device_class": None,
        "state_class": "measurement"
    },
    "Einschubschn. BSZ": {
        "en": "Auger Operating Hours",
        "de": "Einschubschnecke Betriebsstundenzähler",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_STEUERUNG": {
        "en": "Op. Hours Control",
        "de": "Betriebsstunden Steuerung",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_HEIZUNG": {
        "en": "Op. Hours Heating",
        "de": "Betriebsstunden Heizung",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_ZUENDUNG": {
        "en": "Op. Hours Ignition",
        "de": "Betriebsstunden Zündung",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_SZ": {
        "en": "Op. Hours Draft",
        "de": "Betriebsstunden Saugzug",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_AUSTRAG": {
        "en": "Op. Hours Discharge",
        "de": "Betriebsstunden Austrag",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_HEIZUNG_UPD": {
        "en": "Op. Hours Heating Upd",
        "de": "Betriebsstunden Heizung Upd",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_ZUENDUNGEN": {
        "en": "Ignition Count",
        "de": "Anzahl Zündungen",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_LEIST_90": {
        "en": "Op. Hours >90% Power",
        "de": "Betriebsstunden >90% Leistung",
        "device_class": None,
        "state_class": "measurement"
    },
    "BSZ_GLUTERH": {
        "en": "Op. Hours Ember Pres.",
        "de": "Betriebsstunden Gluterhaltung",
        "device_class": None,
        "state_class": "measurement"
    },
    "BRT Soll": {
        "en": "Burner Temp. Setpoint",
        "de": "Brennraumtemperatur Soll",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "KasEntaschFreigabe": {
        "en": "Cascade Ash Removal Release",
        "de": "Kaskade Entaschung Freigabe",
        "device_class": None,
        "state_class": "measurement"
    },
    "BoiZustand_A": {
        "en": "Boiler State A",
        "de": "Boilerzustand A",
        "device_class": None,
        "state_class": "measurement"
    },
    "BoiZustand_3": {
        "en": "Boiler State 3",
        "de": "Boilerzustand 3",
        "device_class": None,
        "state_class": "measurement"
    },
    # ===== AUXILIARY BUFFER / EXTRA HEATING CIRCUITS (Issue #17) =====
    "TPO_ZusPuf1": {
        "en": "Aux. Buffer 1 Top",
        "de": "Zusatzpuffer 1 Oben",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TPM_ZusPuf1": {
        "en": "Aux. Buffer 1 Middle",
        "de": "Zusatzpuffer 1 Mitte",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "TPU_ZusPuf1": {
        "en": "Aux. Buffer 1 Bottom",
        "de": "Zusatzpuffer 1 Unten",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "Pfg_ZusPuf1": {
        "en": "Aux. Buffer 1 Fill Level",
        "de": "Zusatzpuffer 1 Füllgrad",
        "device_class": None,
        "state_class": "measurement"
    },
    "Pumpe_ZusPuf1": {
        "en": "Aux. Buffer 1 Pump",
        "de": "Zusatzpuffer 1 Pumpe",
        "device_class": None,
        "state_class": "measurement"
    },
    "ZusPuf1_soll oben": {
        "en": "Aux. Buffer 1 Setpoint Top",
        "de": "Zusatzpuffer 1 Sollwert Oben",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "ZusPuf1_soll unten": {
        "en": "Aux. Buffer 1 Setpoint Bottom",
        "de": "Zusatzpuffer 1 Sollwert Unten",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "ZusPuf1 Zustand": {
        "en": "Aux. Buffer 1 State",
        "de": "Zusatzpuffer 1 Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "Max Anf ZusPuf1": {
        "en": "Max Aux. Buffer 1 Demand",
        "de": "Max Zusatzpuffer 1 Anforderung",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "ExtHK_2 Solltmp.": {
        "en": "Ext. HC 2 Setpoint",
        "de": "Ext. Heizkreis 2 Solltemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "HKP3 Status": {
        "en": "Pump 3 Status",
        "de": "Heizkreispumpe 3 Status",
        "device_class": None,
        "state_class": "measurement"
    },
    "HKP4 Status": {
        "en": "Pump 4 Status",
        "de": "Heizkreispumpe 4 Status",
        "device_class": None,
        "state_class": "measurement"
    },

    # V10_2HAR_n2: Neo-HV 30 + Nano-PK 20
    "PufLad": {
        "en": "Buffer Percentage",
        "de": "Puffer Ladung",
        "device_class": None,
        "state_class": "measurement"
    },
    "PufZustand": {
        "en": "Buffer State",
        "de": "Puffer Zustand",
        "device_class": None,
        "state_class": "measurement"
    },
    "RLP/PuffPumpe": {
        "en": "Return Pump/Buffer Pump",
        "de": "Rücklaufpumpe/Pufferpumpe",
        "device_class": None,
        "state_class": "measurement"
    },
    "PK_TK": {
        "en": "Pellets Combustor Temperature",
        "de": "Pellets Kesseltemperatur",
        "device_class": "temperature",
        "state_class": "measurement"
    },
    "PK_TRG": {
        "en": "Pellets Flue Gas Temperature",
        "de": "Pellets Rauchgastemperatur",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:smoke"
    },
    "PK_UsePos": {
        "en": "Pellets Suctionpoint",
        "de": "Pellets Saugpunkt",
        "device_class": None,
        "state_class": "measurement"
    },
    "PK_UsePos": {
        "en": "Pellets Suctionpoint",
        "de": "Pellets Saugpunkt",
        "device_class": None,
        "state_class": "measurement"
    },
    "PK_Verbrauchszähler": {
        "en": "Pellets Total Consumption",
        "de": "Pellets Gesmatverbrauchszähler",
        "device_class": None,
        "state_class": "measurement"
    },
    "PK_Lagerstand": {
        "en": "Pellets Capacity",
        "de": "Pellets Lagerstand",
        "device_class": None,
        "state_class": "measurement"
    },

    # Known XML parameters without translated names retain their wire names.
    "DUMMY": {'device_class': None, 'state_class': 'measurement'},
    "Emerson Out3": {'device_class': None, 'state_class': None},
    "FS Asche": {'device_class': None, 'state_class': None},
    "FS Asche Gruppe 2": {'device_class': None, 'state_class': None},
    "FS Asche Gruppe 3": {'device_class': None, 'state_class': None},
    "FS Asche Gruppe 4": {'device_class': None, 'state_class': None},
    "FW Pumpe": {'device_class': None, 'state_class': None},
    "FW-Anforderung": {'device_class': 'temperature', 'state_class': 'measurement'},
    "Feuerung aktiv (F2)": {'device_class': None, 'state_class': None},
    "Feuerung aktiv (F3)": {'device_class': None, 'state_class': None},
    "Freig Entasch": {'device_class': None, 'state_class': None},
    "GBF": {'device_class': None, 'state_class': 'measurement'},
    "GBF soll": {'device_class': None, 'state_class': 'measurement'},
    "Geb. Relais": {'device_class': None, 'state_class': None},
    "HK1 Status": {'device_class': None, 'state_class': 'measurement'},
    "IO32 509": {'device_class': None, 'state_class': 'measurement'},
    "IO32 510": {'device_class': None, 'state_class': 'measurement'},
    "IO32 517": {'device_class': 'temperature', 'state_class': 'measurement'},
    "IO32 521": {'device_class': None, 'state_class': 'measurement'},
    "IO32 522": {'device_class': None, 'state_class': 'measurement'},
    "IO32 VL": {'device_class': 'temperature', 'state_class': 'measurement'},
    "I_Lambda": {'device_class': 'current', 'state_class': 'measurement'},
    "KASK1 AschAnf": {'device_class': None, 'state_class': None},
    "KASK2 AschAnf": {'device_class': None, 'state_class': None},
    "KASK3 AschAnf": {'device_class': None, 'state_class': None},
    "KASK4 AschAnf": {'device_class': None, 'state_class': None},
    "Kask LZLeist_1": {'device_class': None, 'state_class': 'measurement'},
    "Kask LZLeist_2": {'device_class': None, 'state_class': 'measurement'},
    "Kask LZLeist_3": {'device_class': None, 'state_class': 'measurement'},
    "Kask LZLeist_4": {'device_class': None, 'state_class': 'measurement'},
    "KaskIstTmp_1": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskIstTmp_2": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskIstTmp_3": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskIstTmp_4": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskLZLeisMax_1": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMax_2": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMax_3": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMax_4": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMin_1": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMin_2": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMin_3": {'device_class': None, 'state_class': 'measurement'},
    "KaskLZLeisMin_4": {'device_class': None, 'state_class': 'measurement'},
    "KaskSollTmp_1": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskSollTmp_2": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskSollTmp_3": {'device_class': 'temperature', 'state_class': 'measurement'},
    "KaskSollTmp_4": {'device_class': 'temperature', 'state_class': 'measurement'},
    "LZ LB seit Ent.": {'device_class': None, 'state_class': 'measurement'},
    "LambdaOk": {'device_class': None, 'state_class': None},
    "Lamdaheiz.": {'device_class': None, 'state_class': None},
    "M-AFS FS1 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS1 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS2 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS2 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS3 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS3 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS4 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS4 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS5 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS5 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS6 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS6 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS7 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS7 Run": {'device_class': None, 'state_class': None},
    "M-AFS FS8 Dir": {'device_class': None, 'state_class': None},
    "M-AFS FS8 Run": {'device_class': None, 'state_class': None},
    "O2_soll": {'device_class': None, 'state_class': 'measurement'},
    "PK_AA Dir": {'device_class': None, 'state_class': None},
    "PK_AA Run": {'device_class': None, 'state_class': None},
    "PK_AS RA Dir": {'device_class': None, 'state_class': None},
    "PK_AS RA Run": {'device_class': None, 'state_class': None},
    "PK_AS Saug": {'device_class': None, 'state_class': None},
    "PK_AUPIst": {'device_class': None, 'state_class': 'measurement'},
    "PK_AUPSoll": {'device_class': None, 'state_class': 'measurement'},
    "PK_AUPStrom": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_Aschebox": {'device_class': None, 'state_class': None},
    "PK_ES Dir": {'device_class': None, 'state_class': None},
    "PK_ES Run": {'device_class': None, 'state_class': None},
    "PK_ESRegler": {'device_class': None, 'state_class': 'measurement'},
    "PK_ESsoll": {'device_class': None, 'state_class': 'measurement'},
    "PK_Fuellstand": {'device_class': None, 'state_class': None},
    "PK_Heiz I Lambda": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_Heiz P Lambda": {'device_class': None, 'state_class': 'measurement'},
    "PK_Heiz U Lambda": {'device_class': None, 'state_class': 'measurement'},
    "PK_I Aa": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_I Es": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_I Ra": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_I Rein": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_I Sr": {'device_class': 'current', 'state_class': 'measurement'},
    "PK_KeBrstScale": {'device_class': None, 'state_class': 'measurement'},
    "PK_L Heiz.": {'device_class': None, 'state_class': None},
    "PK_LZ ES seit Ent.": {'device_class': None, 'state_class': 'measurement'},
    "PK_LZ ES seit Füll.": {'device_class': None, 'state_class': 'measurement'},
    "PK_LambdaOk": {'device_class': None, 'state_class': None},
    "PK_Leistung": {'device_class': None, 'state_class': 'measurement'},
    "PK_O2": {'device_class': None, 'state_class': 'measurement'},
    "PK_O2soll": {'device_class': None, 'state_class': 'measurement'},
    "PK_Programm": {'device_class': None, 'state_class': 'measurement'},
    "PK_RL Pumpe": {'device_class': None, 'state_class': None},
    "PK_RL Verz Aktiv": {'device_class': None, 'state_class': None},
    "PK_RLP": {'device_class': None, 'state_class': 'measurement'},
    "PK_RLm_auf": {'device_class': None, 'state_class': None},
    "PK_RLm_zu": {'device_class': None, 'state_class': None},
    "PK_Rein En": {'device_class': None, 'state_class': None},
    "PK_Rein Run": {'device_class': None, 'state_class': None},
    "PK_SZ": {'device_class': None, 'state_class': 'measurement'},
    "PK_SZs": {'device_class': None, 'state_class': 'measurement'},
    "PK_Sens U Lambda": {'device_class': None, 'state_class': 'measurement'},
    "PK_Spreizung": {'device_class': 'temperature', 'state_class': 'measurement'},
    "PK_TKsoll": {'device_class': 'temperature', 'state_class': 'measurement'},
    "PK_TRL": {'device_class': 'temperature', 'state_class': 'measurement'},
    "PK_TRLsoll": {'device_class': 'temperature', 'state_class': 'measurement'},
    "PK_Tplat": {'device_class': 'temperature', 'state_class': 'measurement'},
    "PK_Z Geb.": {'device_class': None, 'state_class': None},
    "PK_Z Heiz.": {'device_class': None, 'state_class': None},
    "PK_ZK": {'device_class': None, 'state_class': 'measurement'},
    "PK_max.Leist.TRG": {'device_class': None, 'state_class': 'measurement'},
    "PK_min.Leist.TRG": {'device_class': None, 'state_class': 'measurement'},
    "PLK": {'device_class': None, 'state_class': 'measurement'},
    "PLK auf": {'device_class': None, 'state_class': None},
    "PLK zu": {'device_class': None, 'state_class': None},
    "PLK_auf": {'device_class': None, 'state_class': None},
    "PLK_zu": {'device_class': None, 'state_class': None},
    "PLKsoll": {'device_class': None, 'state_class': 'measurement'},
    "Prim.ist": {'device_class': None, 'state_class': 'measurement'},
    "Prim.soll": {'device_class': None, 'state_class': 'measurement'},
    "PuffP": {'device_class': None, 'state_class': None},
    "RL Pumpe": {'device_class': None, 'state_class': None},
    "RLP": {'device_class': None, 'state_class': 'measurement'},
    "RostPos": {'device_class': None, 'state_class': 'measurement'},
    "SG1/Lock aktiv": {'device_class': None, 'state_class': None},
    "SG2 aktiv": {'device_class': None, 'state_class': None},
    "SK M-AFS FS1": {'device_class': None, 'state_class': None},
    "SK M-AFS FS2": {'device_class': None, 'state_class': None},
    "SK M-AFS FS3": {'device_class': None, 'state_class': None},
    "SK M-AFS FS4": {'device_class': None, 'state_class': None},
    "SK M-AFS FS5": {'device_class': None, 'state_class': None},
    "SK M-AFS FS6": {'device_class': None, 'state_class': None},
    "SK M-AFS FS7": {'device_class': None, 'state_class': None},
    "SK M-AFS FS8": {'device_class': None, 'state_class': None},
    "SK eCleaner 1": {'device_class': None, 'state_class': None},
    "SK eCleaner 2": {'device_class': None, 'state_class': None},
    "SLK auf": {'device_class': None, 'state_class': None},
    "SLK zu": {'device_class': None, 'state_class': None},
    "SLK_auf": {'device_class': None, 'state_class': None},
    "SLK_zu": {'device_class': None, 'state_class': None},
    "STB": {'device_class': None, 'state_class': None},
    "SZ": {'device_class': None, 'state_class': 'measurement'},
    "SZs": {'device_class': None, 'state_class': 'measurement'},
    "Schnellladev.": {'device_class': None, 'state_class': None},
    "Sek.ist": {'device_class': None, 'state_class': 'measurement'},
    "Sek.soll": {'device_class': None, 'state_class': 'measurement'},
    "Störung AFM": {'device_class': None, 'state_class': None},
    "TKS": {'device_class': None, 'state_class': None},
    "TR1": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TR2": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TR3": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TR4": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TR5": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TR6": {'device_class': 'temperature', 'state_class': 'measurement'},
    "TRA": {'device_class': 'temperature', 'state_class': 'measurement'},
    "U_lambda_soll": {'device_class': None, 'state_class': 'measurement'},
    "Unbekannt": {'device_class': 'temperature', 'state_class': 'measurement'},
    "Unbekannt 2": {'device_class': None, 'state_class': 'measurement'},
    "Use FuellDis": {'device_class': None, 'state_class': None},
    "UseMotIst": {'device_class': None, 'state_class': 'measurement'},
    "UseMotSoll": {'device_class': None, 'state_class': 'measurement'},
    "Verbl. Zeit Rein": {'device_class': None, 'state_class': 'measurement'},
    "ZP Boi.1": {'device_class': None, 'state_class': None},
    "ZP Boi.2": {'device_class': None, 'state_class': None},
    "ZP Boi.3": {'device_class': None, 'state_class': None},
    "ZP Boi.A": {'device_class': None, 'state_class': None},
    "ZP Boi.B": {'device_class': None, 'state_class': None},
    "Zündheiz.": {'device_class': None, 'state_class': None},
    "dummy1": {'device_class': None, 'state_class': 'measurement'},
    "dummy2": {'device_class': None, 'state_class': 'measurement'},
    "dummy3": {'device_class': None, 'state_class': 'measurement'},
    "dummy4": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 I-Elek": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 I-NT": {'device_class': 'current', 'state_class': 'measurement'},
    "eCleaner 1 Leistung": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 Max_U-HV": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 Temp": {'device_class': 'temperature', 'state_class': 'measurement'},
    "eCleaner 1 U-HV": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 U-HVs": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 U-NT": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 U-ZK": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 Ueberschlag": {'device_class': None, 'state_class': 'measurement'},
    "eCleaner 1 aktiv": {'device_class': None, 'state_class': None},
    "eCleaner 2 aktiv": {'device_class': None, 'state_class': None},
    "eCleaner AA Dir": {'device_class': None, 'state_class': None},
    "eCleaner AA Run": {'device_class': None, 'state_class': None},
    "eCleaner RR Run": {'device_class': None, 'state_class': None},
}


# Keep these references together when registering this profile.
DEFINITIONS: Final = FirmwareDefinitions(PARAMETER_DESCRIPTIONS, ERROR_CODES, DISPLAY_NAME)
