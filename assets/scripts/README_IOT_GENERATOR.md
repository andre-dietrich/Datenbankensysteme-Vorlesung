# IoT Sensor Data Generator

Python-Script zur Generierung synthetischer Smart-Home-Sensordaten für Column Store Demos.

## Features

- ✅ Realistische Temperatur-Zyklen (saisonal + täglich)
- ✅ Korrelierte Luftfeuchtigkeit (inverse Korrelation mit Temperatur)
- ✅ Licht-Sensoren (Tageslicht + künstliches Licht)
- ✅ CO2-Sensoren (abhängig von Belegung und Lüftung)
- ✅ Bewegungssensoren (binär, zeitabhängig)
- ✅ Stromverbrauch (abhängig von Tageszeit und Geräten)
- ✅ **29 Spalten** für dramatische Column Store vs. Row Store Vergleiche
- ✅ Flexibel konfigurierbar (Start/End-Datum, Intervall)

## Installation

Keine Dependencies erforderlich – nutzt nur Python Standard Library:

```bash
python3 generate_iot_data.py --help
```

## Usage

### Beispiel 1: 90 Tage, stündliche Messungen

```bash
python3 generate_iot_data.py --days 90 --interval 1h --output iot_sensors_90d.csv
```

**Resultat:** 2.161 Zeilen × 29 Spalten = 62.669 Datenpunkte

---

### Beispiel 2: 1 Jahr, stündliche Messungen

```bash
python3 generate_iot_data.py --start "2023-01-01" --end "2023-12-31" --interval 1h
```

**Resultat:** 8.760 Zeilen × 29 Spalten = 254.040 Datenpunkte

---

### Beispiel 3: 7 Tage, 10-Minuten-Intervall (granular)

```bash
python3 generate_iot_data.py --days 7 --interval 10min --output sensors_7d_10min.csv
```

**Resultat:** 1.008 Zeilen × 29 Spalten

---

### Beispiel 4: 30 Tage, minütlich (massive Daten)

```bash
python3 generate_iot_data.py --days 30 --interval 1min --output sensors_30d_1min.csv
```

**Resultat:** 43.200 Zeilen × 29 Spalten = 1.252.800 Datenpunkte 🔥

---

## Datenstruktur

### 29 Spalten

| Spalte                  | Typ       | Beschreibung                          |
|-------------------------|-----------|---------------------------------------|
| `timestamp`             | TIMESTAMP | Zeitstempel der Messung               |
| `room_id`               | TEXT      | Raum (living, bedroom, kitchen, bathroom) |
| `temp_living`           | REAL      | Temperatur Wohnzimmer (°C)            |
| `temp_bedroom`          | REAL      | Temperatur Schlafzimmer (°C)          |
| `temp_kitchen`          | REAL      | Temperatur Küche (°C)                 |
| `temp_bathroom`         | REAL      | Temperatur Bad (°C)                   |
| `temp_outside`          | REAL      | Außentemperatur (°C)                  |
| `humidity_living`       | REAL      | Luftfeuchtigkeit Wohnzimmer (%)       |
| `humidity_bedroom`      | REAL      | Luftfeuchtigkeit Schlafzimmer (%)     |
| `humidity_kitchen`      | REAL      | Luftfeuchtigkeit Küche (%)            |
| `humidity_bathroom`     | REAL      | Luftfeuchtigkeit Bad (%)              |
| `humidity_outside`      | REAL      | Luftfeuchtigkeit Außen (%)            |
| `light_living`          | REAL      | Licht-Level Wohnzimmer (Lux)          |
| `light_bedroom`         | REAL      | Licht-Level Schlafzimmer (Lux)        |
| `light_kitchen`         | REAL      | Licht-Level Küche (Lux)               |
| `light_bathroom`        | REAL      | Licht-Level Bad (Lux)                 |
| `light_outside`         | REAL      | Licht-Level Außen (Lux)               |
| `co2_living`            | REAL      | CO2-Level Wohnzimmer (ppm)            |
| `co2_bedroom`           | REAL      | CO2-Level Schlafzimmer (ppm)          |
| `co2_kitchen`           | REAL      | CO2-Level Küche (ppm)                 |
| `co2_bathroom`          | REAL      | CO2-Level Bad (ppm)                   |
| `motion_living`         | INTEGER   | Bewegung Wohnzimmer (0/1)             |
| `motion_bedroom`        | INTEGER   | Bewegung Schlafzimmer (0/1)           |
| `motion_kitchen`        | INTEGER   | Bewegung Küche (0/1)                  |
| `motion_bathroom`       | INTEGER   | Bewegung Bad (0/1)                    |
| `power_living`          | REAL      | Stromverbrauch Wohnzimmer (Watt)      |
| `power_bedroom`         | REAL      | Stromverbrauch Schlafzimmer (Watt)    |
| `power_kitchen`         | REAL      | Stromverbrauch Küche (Watt)           |
| `power_bathroom`        | REAL      | Stromverbrauch Bad (Watt)             |

---

## Warum 29 Spalten?

Column Stores profitieren dramatisch von **vielen Spalten**, weil:

1. **Spalten-Aggregationen** (z.B. `AVG(temp_living)`) nur eine Spalte lesen
2. **Row-Stores** müssen alle 29 Spalten lesen, auch ungenutzte
3. **Performance-Unterschied** ist bei 29 Spalten 10-20× größer als bei 5 Spalten

**Demo-Query:**
```sql
SELECT AVG(temp_living) FROM sensors;
```

- **DuckDB (Column Store):** Liest 1 Spalte (temp_living)
- **PGlite (Row Store):** Liest alle 29 Spalten

---

## Parameter

### Zeitraum

**Option A:** Start + End

```bash
--start "2023-01-01" --end "2023-12-31"
```

**Option B:** Nur Tage (ab heute rückwärts)

```bash
--days 90
```

### Intervall

Unterstützte Formate:

- `1h` → 1 Stunde
- `10min` → 10 Minuten
- `30s` → 30 Sekunden
- `1d` → 1 Tag

### Output

```bash
--output my_sensors.csv
```

Standard: `iot_sensors.csv`

---

## Verwendung in LiaScript

Die generierten CSV-Dateien können direkt in DuckDB/PGlite geladen werden:

```sql
CREATE TABLE sensors AS 
SELECT * FROM read_csv_auto(
    'http://localhost:8000/assets/dat/iot_sensors_90d.csv',
    header = true,
    timestampformat = '%Y-%m-%d %H:%M:%S'
);
```

---

## Realismus

Die Daten sind **synthetisch**, aber **realistisch**:

- ✅ Saisonale Temperaturschwankungen (Winter kälter, Sommer wärmer)
- ✅ Tägliche Zyklen (nachts kühler, tagsüber wärmer)
- ✅ Raum-spezifische Offsets (Bad wärmer, Schlafzimmer kühler)
- ✅ Korrelierte Luftfeuchtigkeit (inverse Korrelation mit Temperatur)
- ✅ Zeitabhängige Belegung (tagsüber mehr Bewegung, nachts weniger)
- ✅ Realistische Stromverbrauchsmuster (Kochen 11-13 Uhr und 18-20 Uhr)

---

## Lizenz

MIT – frei verwendbar für Lehrzwecke
