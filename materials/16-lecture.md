<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  0.1.0
language: de
narrator: Deutsch Female
comment:  Aggregationen & Window Functions – Column Store Performance mit Wetterdaten

import:   https://raw.githubusercontent.com/LiaTemplates/DuckDB/refs/heads/main/README.md
          https://raw.githubusercontent.com/liaTemplates/SQLite/main/README.md
-->

# Aggregationen & Window Functions

> **Session 16** – Lecture (90 Minuten)  
> **Block 4:** Theorie, Optimierung & Polyglot  
> **Lernziel:** LZ 2 – SQL-Praxis vertiefen & Performance verstehen

    --{{0}}--
Willkommen zur sechzehnten Vorlesung! Heute wird es richtig spannend: Wir verbinden alles, was Sie bisher über SQL und Column Stores gelernt haben. Wir werden sehen, warum DuckDB bei Sensor- und Zeitreihen-Daten unschlagbar ist, wie Sie mit Window Functions gleitende Mittelwerte berechnen, und was im Hintergrund passiert, wenn Ihre Datenbank Millionen von Zeilen aggregiert. Heute lernen Sie nicht nur SQL – Sie lernen, wie Performance entsteht.

---

## Was erwartet Sie heute?

    --{{0}}--
Heute kombinieren wir drei große Themen: Klassische Aggregationen, fortgeschrittene Window Functions und Performance-Optimierung mit Column Stores. Alles mit echten Wetterdaten – über 4000 Messungen aus mehreren Monaten.

      {{0-1}}
<div>

### Überblick

- **Klassische Aggregationen:** COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
- **Window Functions:** ROW_NUMBER, RANK, LAG, LEAD, gleitende Mittelwerte
- **Zeitbasierte Analytics:** DATE_TRUNC, EXTRACT, ROWS BETWEEN
- **Performance-Vergleich:** Column Store (DuckDB) vs. Row Store (PostgreSQL)
- **DuckDB Internals:** Kompression, Chunks, Parallelisierung

</div>

    --{{1}}--
Erinnern Sie sich an Lecture 4? Damals haben wir gelernt, dass Column Stores Spalten physisch zusammen speichern. Heute sehen Sie, warum das bei Analytics-Queries einen Riesenunterschied macht.

      {{1}}
> 🔗 **Rückblick Lecture 4:** Column Stores speichern Spalten zusammen → weniger I/O bei Aggregationen

---

## Setup: Wetterdaten laden

    --{{0}}--
Lassen Sie uns mit unseren Daten starten. Wir haben echte Wettermessungen aus den letzten Monaten – Temperatur, Luftdruck, Windgeschwindigkeit, Luftfeuchte und mehr. Insgesamt über 4000 Zeilen.

      {{0-1}}
<div>

### Daten laden

```sql
CREATE TABLE weather AS 
SELECT * FROM read_csv_auto(
  'https://raw.githubusercontent.com/andre-dietrich/Datenbankensysteme-Vorlesung/refs/heads/main/assets/dat/weather.csv',
  header = true
);

SELECT * FROM weather LIMIT 5;
```
@DuckDB.eval

</div>

    --{{1}}--
Schauen wir uns die Struktur an: Datum, Anzahl Messwerte pro Tag, dann verschiedene Sensoren.

      {{1}}
<div>

### Datenstruktur verstehen

```sql
DESCRIBE weather;
```
@DuckDB.eval

    --{{1}}--
Sie sehen: 12 Spalten, hauptsächlich numerische Werte. Perfekt für Aggregationen!

</div>

---

## Teil 1: Klassische Aggregationen

    --{{0}}--
Starten wir mit den Basics: Aggregationsfunktionen. Diese kennen Sie bereits, aber heute schauen wir genauer hin, wie sie intern funktionieren.

### COUNT, SUM, AVG, MIN, MAX

    --{{0}}--
Die fundamentalen Aggregationsfunktionen – jede Datenbank hat sie, aber die Performance variiert dramatisch.

      {{0-1}}
<div>

#### Einfache Aggregationen

```sql
SELECT 
  COUNT(*) as anzahl_tage,
  ROUND(AVG(Temp_2m), 2) as durchschnitts_temp,
  ROUND(MIN(Temp_2m), 2) as min_temp,
  ROUND(MAX(Temp_2m), 2) as max_temp,
  ROUND(AVG(Windgeschwindigkeit), 2) as durchschnitts_wind
FROM weather;
```
@DuckDB.eval

    --{{0}}--
Über 4200 Tage werden in Millisekunden verarbeitet. Warum so schnell?

</div>

    --{{1}}--
Column Stores! DuckDB liest nur die benötigten Spalten – Temperatur und Windgeschwindigkeit. Die anderen 10 Spalten bleiben unberührt.

      {{1-2}}
<div>

#### Was passiert im Hintergrund?

**Row-Store (PostgreSQL):**
```ascii
Liest alle Zeilen: [Datum|Anzahl|Messwerte|Wind|Windrichtung|Strahlung|Druck|Temp2m|Temp5cm|Bodentemp|Feuchte|Niederschlag]
→ 4252 Zeilen × 12 Spalten = 51.024 Werte gelesen
```

**Column-Store (DuckDB):**
```ascii
Liest nur benötigte Spalten: [Temp2m, Windgeschwindigkeit]
→ 4252 Zeilen × 2 Spalten = 8.504 Werte gelesen
→ 6× weniger I/O!
```

</div>

    --{{2}}--
Und jetzt kommt der Clou: DuckDB komprimiert diese Spalten auch noch. Schauen wir uns an, wie viel Speicher tatsächlich gelesen wird.

      {{2}}
<div>

#### Kompression in Aktion

```sql
PRAGMA storage_info('weather');
```
@DuckDB.eval

    --{{2}}--
Die Ausgabe zeigt Ihnen: Spalten-Name, Typ, Kompression-Methode, komprimierte Größe. Temperaturen lassen sich extrem gut komprimieren – Werte zwischen -10 und +30 brauchen nur wenige Bits pro Wert!

</div>

---

### GROUP BY – Gruppierte Aggregationen

    --{{0}}--
Jetzt wird es interessanter: Gruppierungen. Wir berechnen Monats-Durchschnitte – ein klassischer Analytics-Use-Case.

      {{0-1}}
<div>

#### Nach Monat gruppieren

```sql
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  ROUND(AVG(Temp_2m), 2) as avg_temp,
  ROUND(AVG(Luftfeuchte), 1) as avg_feuchte,
  COUNT(*) as anzahl_messungen
FROM weather
GROUP BY monat
ORDER BY monat DESC;
```
@DuckDB.eval

</div>

    --{{1}}--
Sie sehen: Jeder Monat hat einen Durchschnitt. Aber was, wenn wir nur Monate mit bestimmten Eigenschaften wollen?

      {{1}}
<div>

#### HAVING – Filterung nach Aggregation

```sql
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  ROUND(AVG(Temp_2m), 2) as avg_temp,
  COUNT(*) as anzahl_messungen
FROM weather
GROUP BY monat
HAVING AVG(Temp_2m) < 0  -- Nur Monate mit Durchschnitt unter 0°C
ORDER BY avg_temp;
```
@DuckDB.eval

    --{{1}}--
HAVING ist wie WHERE – aber für Aggregate. WHERE filtert vor der Gruppierung, HAVING danach.

</div>

---

### Performance-Analyse mit EXPLAIN ANALYZE

    --{{0}}--
Jetzt schauen wir unter die Haube! Mit EXPLAIN ANALYZE sehen wir, was DuckDB intern macht.

      {{0-1}}
<div>

#### Query-Plan anzeigen

```sql
EXPLAIN
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  ROUND(AVG(Temp_2m), 2) as avg_temp
FROM weather
GROUP BY monat;
```
@DuckDB.eval

</div>

    --{{1}}--
Der Query-Plan zeigt Ihnen: Welche Operationen, wie viele Zeilen verarbeitet, wie viel Zeit. Achten Sie auf "COLUMN_DATA_SCAN" – das bedeutet, DuckDB liest nur die benötigten Spalten.

      {{1}}
> 💡 **Performance-Tipp:** EXPLAIN ANALYZE ist Ihr bester Freund beim Debugging langsamer Queries!

---

## Teil 2: Window Functions

    --{{0}}--
Jetzt kommen wir zu den mächtigen Window Functions – ein Game-Changer für Analytics. Window Functions erlauben es Ihnen, Berechnungen über Zeilen-Bereiche durchzuführen, ohne zu gruppieren.

### Grundkonzept: OVER

    --{{0}}--
Der Unterschied zu GROUP BY: Window Functions behalten alle Zeilen bei, berechnen aber trotzdem Aggregate über Fenster.

      {{0-1}}
<div>

#### GROUP BY vs. Window Function

**Mit GROUP BY (kollabiert Zeilen):**
```sql
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  AVG(Temp_2m) as avg_temp
FROM weather
GROUP BY monat;
-- Ergebnis: 12 Zeilen (eine pro Monat)
```

**Mit Window Function (behält alle Zeilen):**
```sql
SELECT 
  Datum,
  Temp_2m,
  AVG(Temp_2m) OVER (
    PARTITION BY DATE_TRUNC('month', Datum)
  ) as monats_durchschnitt
FROM weather
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

    --{{0}}--
Jede Zeile behält ihre Originaldaten, bekommt aber zusätzlich den Monats-Durchschnitt dazu!

</div>

    --{{1}}--
Das ist besonders nützlich, wenn Sie Abweichungen vom Durchschnitt berechnen wollen.

      {{1}}
<div>

#### Abweichung vom Monatsdurchschnitt

```sql
SELECT 
  Datum,
  Temp_2m as temp,
  ROUND(AVG(Temp_2m) OVER (
    PARTITION BY DATE_TRUNC('month', Datum)
  ), 2) as monats_avg,
  ROUND(
    Temp_2m - AVG(Temp_2m) OVER (
      PARTITION BY DATE_TRUNC('month', Datum)
    ), 
    2
  ) as abweichung
FROM weather
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

</div>

---

### ROW_NUMBER, RANK, DENSE_RANK

    --{{0}}--
Ranking-Funktionen – perfekt, um die Top-N-Werte zu finden.

      {{0-1}}
<div>

#### Die kältesten Tage finden

```sql
SELECT 
  Datum,
  Temp_2m as temp,
  ROW_NUMBER() OVER (ORDER BY Temp_2m) as row_num,
  RANK() OVER (ORDER BY Temp_2m) as rank,
  DENSE_RANK() OVER (ORDER BY Temp_2m) as dense_rank
FROM weather
ORDER BY temp
LIMIT 10;
```
@DuckDB.eval

</div>

    --{{1}}--
Der Unterschied: ROW_NUMBER ist durchgängig, RANK springt bei Ties, DENSE_RANK nicht. Bei gleichen Werten macht das einen Unterschied!

      {{1-2}}
<div>

#### Unterschiede bei Ties

```ascii
Temp:  -7.0   -7.0   -6.8   -5.7
ROW_NUMBER: 1, 2, 3, 4
RANK:       1, 1, 3, 4    (springt über 2)
DENSE_RANK: 1, 1, 2, 3    (kein Sprung)
```

</div>

    --{{2}}--
Welche Funktion Sie nutzen, hängt von Ihrem Use Case ab. Für "Top 10" ist DENSE_RANK oft die richtige Wahl.

      {{2}}
> 🎯 **Merkhilfe:** DENSE_RANK = keine Lücken, RANK = mit Lücken, ROW_NUMBER = immer eindeutig

---

### LAG & LEAD – Zugriff auf Nachbarzeilen

    --{{0}}--
Jetzt wird es richtig mächtig: LAG und LEAD erlauben Ihnen, auf vorherige oder nächste Zeilen zuzugreifen. Perfekt für Zeitreihen!

      {{0-1}}
<div>

#### Temperatur-Veränderung zum Vortag

```sql
SELECT 
  Datum,
  Temp_2m as temp_heute,
  LAG(Temp_2m, 1) OVER (ORDER BY Datum) as temp_gestern,
  ROUND(
    Temp_2m - LAG(Temp_2m, 1) OVER (ORDER BY Datum),
    2
  ) as veraenderung
FROM weather
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

    --{{0}}--
LAG(spalte, 1) gibt Ihnen den Wert der vorherigen Zeile. Mit LAG(spalte, 7) bekommen Sie den Wert von vor 7 Tagen!

</div>

    --{{1}}--
LEAD funktioniert genauso, nur in die andere Richtung – in die Zukunft.

      {{1}}
<div>

#### LEAD – Vorausschau

```sql
SELECT 
  Datum,
  Temp_2m as temp_heute,
  LEAD(Temp_2m, 1) OVER (ORDER BY Datum) as temp_morgen,
  ROUND(
    LEAD(Temp_2m, 1) OVER (ORDER BY Datum) - Temp_2m,
    2
  ) as erwartete_veraenderung
FROM weather
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

</div>

---

### Gleitende Mittelwerte – Der Analytics-Klassiker

    --{{0}}--
Jetzt kommt das, worauf Sie gewartet haben: Gleitende Mittelwerte! Damit glätten Sie Schwankungen und erkennen Trends.

      {{0-1}}
<div>

#### 7-Tages-Gleitender Durchschnitt

```sql
SELECT 
  Datum,
  Temp_2m as temp,
  ROUND(
    AVG(Temp_2m) OVER (
      ORDER BY Datum
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ),
    2
  ) as temp_7tage_avg
FROM weather
ORDER BY Datum DESC
LIMIT 15;
```
@DuckDB.eval

    --{{0}}--
"ROWS BETWEEN 6 PRECEDING AND CURRENT ROW" bedeutet: Nimm die aktuellen Zeile plus die 6 davor – macht 7 Tage.

</div>

    --{{1}}--
Sie können auch asymmetrische Fenster bauen – zum Beispiel zentriert:

      {{1-2}}
<div>

#### Zentrierter gleitender Durchschnitt

```sql
SELECT 
  Datum,
  Temp_2m as temp,
  ROUND(
    AVG(Temp_2m) OVER (
      ORDER BY Datum
      ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
    ),
    2
  ) as temp_7tage_zentriert
FROM weather
WHERE Datum BETWEEN '2025-12-15' AND '2025-12-31'
ORDER BY Datum;
```
@DuckDB.eval

    --{{1}}--
Zentrierte Mittelwerte sind genauer, aber für Echtzeit-Daten nicht nutzbar – Sie brauchen ja zukünftige Werte.

</div>

    --{{2}}--
Gleitende Mittelwerte können Sie auch mit LAG kombinieren – das ist etwas umständlicher, aber manchmal nötig.

      {{2}}
<div>

#### Manueller gleitender Durchschnitt mit LAG

```sql
SELECT 
  Datum,
  Temp_2m as temp,
  ROUND(
    (
      Temp_2m +
      LAG(Temp_2m, 1) OVER (ORDER BY Datum) +
      LAG(Temp_2m, 2) OVER (ORDER BY Datum) +
      LAG(Temp_2m, 3) OVER (ORDER BY Datum)
    ) / 4.0,
    2
  ) as temp_4tage_avg_manuell
FROM weather
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

    --{{2}}--
Das ist genau das Gleiche wie ROWS BETWEEN 3 PRECEDING – aber expliziter. Nutzen Sie ROWS BETWEEN, wenn verfügbar!

</div>

---

### FIRST_VALUE & LAST_VALUE

    --{{0}}--
Zwei weitere nützliche Funktionen: FIRST_VALUE und LAST_VALUE. Damit können Sie den ersten oder letzten Wert eines Fensters abrufen.

      {{0-1}}
<div>

#### Temperatur-Range pro Monat

```sql
SELECT DISTINCT
  DATE_TRUNC('month', Datum) as monat,
  FIRST_VALUE(Temp_2m) OVER (
    PARTITION BY DATE_TRUNC('month', Datum)
    ORDER BY Temp_2m
  ) as kaeltester_tag,
  LAST_VALUE(Temp_2m) OVER (
    PARTITION BY DATE_TRUNC('month', Datum)
    ORDER BY Temp_2m
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) as waermster_tag
FROM weather
ORDER BY monat DESC;
```
@DuckDB.eval

    --{{0}}--
Wichtig: LAST_VALUE braucht oft "ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING", sonst sehen Sie nur bis zur aktuellen Zeile!

</div>

    --{{1}}--
Das ist ein häufiger Fehler – ohne UNBOUNDED FOLLOWING sehen Sie nicht das tatsächliche Ende des Fensters.

      {{1}}
> ⚠️ **Achtung:** LAST_VALUE ohne UNBOUNDED FOLLOWING gibt Ihnen nicht das erwartete Ergebnis!

---

## Teil 3: Performance-Showdown – Column vs. Row

    --{{0}}--
Jetzt kommt der Moment der Wahrheit: Warum ist DuckDB bei diesen Queries so schnell? Lassen Sie uns die Performance analysieren.

### Was macht Column Stores schnell?

    --{{0}}--
Drei Faktoren zusammen ergeben den Performance-Boost: Spalten-Layout, Kompression, Parallelisierung.

      {{0-1}}
<div>

#### Faktor 1: Spalten-Layout

**Row-Store liest:**
```ascii
Query: SELECT AVG(temp), AVG(wind) FROM weather;

Disk: [Datum|Anz|Messw|Wind|Windr|Strahl|Druck|Temp2m|Temp5cm|Boden|Feuchte|Nied]
      [Datum|Anz|Messw|Wind|Windr|Strahl|Druck|Temp2m|Temp5cm|Boden|Feuchte|Nied]
      ...
→ 4252 Zeilen × 12 Spalten = 51.024 Werte gelesen
→ Nur 2 Spalten benötigt = 83% verschwendet!
```

**Column-Store liest:**
```ascii
Query: SELECT AVG(temp), AVG(wind) FROM weather;

Disk: [Windgeschwindigkeit: 4.1, 5.4, 5.2, 4.6, ...]
      [Temp. in 2m Höhe: 6.4, 5.8, 4.6, -2.3, ...]
→ 4252 Zeilen × 2 Spalten = 8.504 Werte gelesen
→ 100% relevant!
```

**Ergebnis: 6× weniger I/O**

</div>

    --{{1}}--
Aber es wird noch besser: Kompression!

      {{1-2}}
<div>

#### Faktor 2: Kompression

Temperaturen schwanken zwischen -10°C und +30°C:

```ascii
Ohne Kompression: 4252 × 8 Bytes (DOUBLE) = 34.016 Bytes
Mit Dictionary: 40 unique values × 8 Bytes + 4252 × 1 Byte = 4.572 Bytes
→ 87% Platzersparnis!
→ 87% weniger Disk I/O!
```

DuckDB kombiniert:
- **Dictionary Encoding:** Häufige Werte werden durch Index ersetzt
- **Bit-Packing:** Werte 0-100 brauchen nur 7 Bit statt 64 Bit
- **RLE (Run-Length):** Wiederholungen wie NULL, NULL, NULL → (NULL, 3x)

**Reale Kompression:** Oft 5-10× weniger Speicher als unkomprimiert!

</div>

    --{{2}}--
Und dann kommt noch Parallelisierung dazu.

      {{2}}
<div>

#### Faktor 3: Parallelisierung mit Chunks

DuckDB teilt Daten in Chunks (typisch 2048 Zeilen):

```ascii
CPU-Kerne:    [Core 1]  [Core 2]  [Core 3]  [Core 4]
Chunks:       Chunk 1   Chunk 2   Chunk 3   Chunk 4
              ↓         ↓         ↓         ↓
              AVG()     AVG()     AVG()     AVG()
              ↓         ↓         ↓         ↓
              ╰─────────┴─────────┴─────────╯
                        Merge
```

**Ergebnis:** 4× CPU-Kerne = ~4× schneller (bei CPU-bound Operations)

</div>

---

### EXPLAIN ANALYZE – Performance verstehen

    --{{0}}--
Schauen wir uns an, was DuckDB intern macht, wenn wir eine komplexe Window Function ausführen.

      {{0-1}}
<div>

#### Komplexe Query analysieren

```sql
EXPLAIN
SELECT 
  Datum,
  Temp_2m as temp,
  AVG(Temp_2m) OVER (
    ORDER BY Datum
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as temp_7tage_avg
FROM weather
WHERE Datum >= '2025-12-01';
```
@DuckDB.eval

</div>

    --{{1}}--
Der Query-Plan zeigt Ihnen: Filter, Window-Operation, Spalten-Scan. Achten Sie auf die Ausführungszeit – selbst mit Window Functions bleibt es im Millisekunden-Bereich!

      {{1}}
> 💡 **Performance-Regel:** Column Stores sind unschlagbar bei:  
> - Wenige Spalten aus vielen  
> - Aggregationen & Scans  
> - Analytics & Reporting

---

### Row-Store vs. Column-Store: Wann was?

    --{{0}}--
Lassen Sie uns das große Bild betrachten: Wann nutzen Sie welches Paradigma?

      {{0}}
<div>

| Use Case | Row-Store (PostgreSQL) | Column-Store (DuckDB) | Gewinner |
|----------|------------------------|----------------------|----------|
| **Zeilen-Lookup** | `WHERE id = 123` | ❌ Langsam | Row-Store |
| **Spalten-Aggregation** | `AVG(temp)` über 1M Zeilen | ✅ Sehr schnell | Column-Store |
| **Viele Updates** | `UPDATE ... WHERE ...` | ❌ Teuer | Row-Store |
| **Analytics-Queries** | `GROUP BY`, Window Functions | ✅ Extrem schnell | Column-Store |
| **Joins** | Multi-Table Joins | ✅ Gut (wenn spaltenweise) | Beide |
| **OLTP** | Transaktionen, kleine Writes | ❌ Nicht ideal | Row-Store |
| **OLAP** | Reporting, BI, Dashboards | ✅ Perfekt | Column-Store |
| **Sensor-Daten** | Time-Series, IoT | ✅ Ideal | Column-Store |

</div>

    --{{1}}--
Die Regel ist einfach: Wenn Sie mehr lesen als schreiben, und wenn Sie Aggregate über Spalten berechnen, sind Column Stores die richtige Wahl.

      {{1}}
> 🎯 **Faustregel:** Lesen >> Schreiben + Spalten-Aggregationen = Column Store

---

## Teil 4: Sensor-Daten – Der perfekte Use Case

    --{{0}}--
Jetzt kombinieren wir alles: Sensor-Daten, gleitende Mittelwerte, Anomalie-Erkennung – der Paradefall für Column Stores!

### Warum Sensor-Daten ideal für Column Stores sind

    --{{0}}--
Sensor-Daten haben drei Eigenschaften, die perfekt zu Column Stores passen.

      {{0-1}}
<div>

#### Eigenschaft 1: Append-Only

Sensoren schreiben nur neue Daten, ändern nie alte:

```ascii
Timeline:
  t1: [sensor_1: 23.5°C]
  t2: [sensor_1: 23.7°C]  ← Neuer Eintrag, kein Update
  t3: [sensor_1: 23.4°C]  ← Neuer Eintrag, kein Update
```

**Vorteil für Column Stores:** Keine Updates = keine teuren Row-Reconstructions!

</div>

    --{{1}}--
Eigenschaft 2: Wenige Spalten abfragen, viele Zeilen scannen.

      {{1-2}}
<div>

#### Eigenschaft 2: Spalten-Fokus

Typische Sensor-Query:

```sql
-- Durchschnitt einer Sensor-Variable über Zeitraum
SELECT AVG(temperature) 
FROM sensors 
WHERE timestamp BETWEEN '2026-01-01' AND '2026-01-31';
```

**Row-Store:** Liest alle Spalten (timestamp, sensor_id, temp, humidity, pressure, ...)  
**Column-Store:** Liest nur `timestamp` und `temperature`

**Ergebnis:** 5-10× schneller!

</div>

    --{{2}}--
Eigenschaft 3: Zeitbasierte Partitionierung.

      {{2}}
<div>

#### Eigenschaft 3: Zeitbasierte Partitionierung

Sensoren produzieren natürliche Zeit-Partitionen:

```ascii
Partition 2025-12:  [4000 rows]
Partition 2026-01:  [4252 rows]  ← Nur diese Partition lesen!
Partition 2026-02:  [...]
```

**Partition Pruning:** DuckDB überspringt irrelevante Partitionen automatisch!

</div>

---

### Praktisches Beispiel: Anomalie-Erkennung

    --{{0}}--
Jetzt bauen wir etwas Cooles: Wir finden Tage, an denen die Temperatur stark vom gleitenden Durchschnitt abweicht – mögliche Anomalien!

      {{0-1}}
<div>

#### Abweichungen vom gleitenden Durchschnitt

```sql
WITH moving_avg AS (
  SELECT 
    Datum,
    Temp_2m as temp,
    ROUND(
      AVG(Temp_2m) OVER (
        ORDER BY Datum
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
      ),
      2
    ) as temp_7tage_avg
  FROM weather
)
SELECT 
  Datum,
  temp,
  temp_7tage_avg,
  ROUND(temp - temp_7tage_avg, 2) as abweichung,
  CASE 
    WHEN ABS(temp - temp_7tage_avg) > 5 THEN '🔴 Anomalie'
    WHEN ABS(temp - temp_7tage_avg) > 3 THEN '🟡 Auffällig'
    ELSE '🟢 Normal'
  END as status
FROM moving_avg
WHERE ABS(temp - temp_7tage_avg) > 3
ORDER BY ABS(temp - temp_7tage_avg) DESC
LIMIT 15;
```
@DuckDB.eval

    --{{0}}--
Tage mit Abweichung > 5°C vom Durchschnitt sind echte Ausreißer – das könnten Messfehler oder Wetterextreme sein!

</div>

    --{{1}}--
Diese Query kombiniert CTEs, Window Functions und CASE – und läuft trotzdem in Millisekunden. Das ist die Macht von Column Stores!

      {{1}}
> 💪 **Power-Combo:** CTE + Window Function + CASE = Flexible Analytics mit Lesbarkeit

---

### Visualisierung: Temperatur-Trend

    --{{0}}--
Zum Abschluss noch ein größeres Beispiel: Monatliche Trends mit Extremwerten.

      {{0}}
<div>

#### Monatliche Temperatur-Statistiken

```sql
WITH daily_stats AS (
  SELECT 
    DATE_TRUNC('month', Datum) as monat,
    Temp_2m as temp,
    Luftfeuchte as feuchte,
    Windgeschwindigkeit as wind
  FROM weather
)
SELECT 
  monat,
  COUNT(*) as anzahl_tage,
  ROUND(AVG(temp), 2) as avg_temp,
  ROUND(MIN(temp), 2) as min_temp,
  ROUND(MAX(temp), 2) as max_temp,
  ROUND(STDDEV(temp), 2) as stddev_temp,
  ROUND(AVG(feuchte), 1) as avg_feuchte,
  ROUND(AVG(wind), 2) as avg_wind
FROM daily_stats
GROUP BY monat
ORDER BY monat DESC;
```
@DuckDB.eval

    --{{0}}--
Sie sehen: Durchschnitt, Min, Max, Standardabweichung – alles in einer Query. DuckDB verarbeitet das über tausende Zeilen, als wäre es nichts.

</div>

---

## Teil 5: DuckDB Internals – Unter der Haube

    --{{0}}--
Zum Abschluss schauen wir unter die Haube: Was macht DuckDB so schnell? Drei Kern-Techniken.

### Chunk-Architektur

    --{{0}}--
DuckDB organisiert Tabellen in Chunks – typischerweise 2048 Zeilen pro Chunk. Jeder Chunk ist unabhängig komprimiert und verarbeitbar.

      {{0-1}}
<div>

#### Chunk-Struktur

```ascii
Tabelle "weather" (4252 Zeilen):
  ┌──────────────────┐
  │  Chunk 0         │  Zeilen 0-2047
  │  - Temp: [...]   │  ← Komprimiert mit Dictionary
  │  - Wind: [...]   │  ← Komprimiert mit RLE
  │  - Druck: [...]  │
  ├──────────────────┤
  │  Chunk 1         │  Zeilen 2048-4095
  │  - Temp: [...]   │
  │  - Wind: [...]   │
  ├──────────────────┤
  │  Chunk 2         │  Zeilen 4096-4251
  │  - Temp: [...]   │
  └──────────────────┘
```

**Vorteile:**
- Parallele Verarbeitung (1 Chunk pro CPU-Kern)
- Chunk-spezifische Kompression
- Min/Max-Statistiken pro Chunk → Pruning

</div>

    --{{1}}--
Chunk-Pruning ist besonders mächtig bei Zeitreihen: Wenn Sie nach "2026-01" filtern, überspringt DuckDB alle Chunks mit anderen Monaten.

      {{1}}
<div>

#### Chunk-Pruning in Aktion

```sql
-- Query: WHERE Datum >= '2026-01-01'
-- DuckDB prüft Min/Max jedes Chunks:

Chunk 0: Min=2025-10-01, Max=2025-11-30  → ❌ Überspringen
Chunk 1: Min=2025-12-01, Max=2026-01-15  → ✅ Scannen (teilweise relevant)
Chunk 2: Min=2026-01-16, Max=2026-01-31  → ✅ Scannen (komplett relevant)
```

**Ergebnis:** Nur 2 von 3 Chunks gelesen → 33% weniger I/O!

</div>

---

### Vektorisierung

    --{{0}}--
DuckDB nutzt SIMD (Single Instruction, Multiple Data) – moderne CPUs können mehrere Werte gleichzeitig verarbeiten.

      {{0-1}}
<div>

#### Vektorisierte Operationen

**Ohne SIMD (naiv):**
```cpp
for (int i = 0; i < 2048; i++) {
  result[i] = temp[i] + 273.15;  // Celsius → Kelvin
}
// 2048 Operationen
```

**Mit SIMD (AVX-512):**
```cpp
for (int i = 0; i < 2048; i += 16) {
  result[i:i+15] = temp[i:i+15] + 273.15;  // 16 Werte auf einmal!
}
// 128 Operationen (16× schneller)
```

</div>

    --{{1}}--
Das funktioniert besonders gut mit Column Stores, weil alle Werte einer Spalte direkt hintereinander liegen – perfekt für SIMD!

      {{1}}
> ⚡ **Performance-Boost:** SIMD × Column-Layout × Kompression = 10-100× schneller als naive Row-Stores

---

### Zero-Copy & Memory Mapping

    --{{0}}--
DuckDB kann Parquet-Dateien direkt lesen, ohne sie erst zu kopieren – Zero-Copy-Architektur.

      {{0}}
<div>

#### Zero-Copy Data Access

**Traditionell (PostgreSQL):**
```ascii
Disk → OS Buffer → DB Buffer → Query Engine
     ↑           ↑           ↑
     Copy 1      Copy 2      Copy 3
```

**Zero-Copy (DuckDB + Parquet):**
```ascii
Disk → Memory-Mapped File → Query Engine direkt
     ↑                    ↑
     OS managed          Zero-Copy!
```

**Vorteil:** Keine Kopier-Operationen = weniger CPU, weniger RAM, schneller!

</div>

    --{{1}}--
Das ist besonders relevant für Data Lakes: Parquet-Files auf S3, direkt querien, ohne sie erst zu laden.

      {{1}}
> 🌊 **Data Lake Pattern:** DuckDB + Parquet = Analytics ohne ETL!

---

## Zusammenfassung & Reflexion

    --{{0}}--
Was für eine Session! Lassen Sie uns zusammenfassen, was Sie heute gelernt haben.

      {{0-1}}
<div>

### Was Sie heute gelernt haben

1. **Klassische Aggregationen:** COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING
2. **Window Functions:** ROW_NUMBER, RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE
3. **Gleitende Mittelwerte:** ROWS BETWEEN für flexible Fenster
4. **Performance:** Column Stores sind 5-50× schneller bei Analytics-Queries
5. **DuckDB Internals:** Chunks, Kompression, Vektorisierung
6. **Sensor-Daten:** Perfekter Use Case für Column Stores (Append-Only, Spalten-Fokus)

</div>

    --{{1}}--
Jetzt sind Sie dran: Testen Sie Ihr Wissen!

      {{1}}
<div>

### 🤔 Reflexionsfragen

1. **Warum ist DuckDB bei `SELECT AVG(temp) FROM sensors` schneller als PostgreSQL?**

   [[Column-Layout + Kompression + nur relevante Spalten lesen]]

2. **Wann brauchen Sie LAG/LEAD statt ROWS BETWEEN?**

   [(X)] Wenn Sie explizit vorherige/nächste Zeilen brauchen (z.B. Differenz zum Vortag)
   [( )] LAG/LEAD ist immer besser
   [( )] ROWS BETWEEN ist veraltet

3. **Was ist der Unterschied zwischen GROUP BY und Window Functions?**

   [[GROUP BY kollabiert Zeilen, Window Functions behalten alle Zeilen bei]]

</div>

---

## Praktische Übung für Sie

    --{{0}}--
Zum Abschluss eine Aufgabe: Nutzen Sie das Gelernte, um eine eigene Analyse zu bauen!

      {{0}}
<div>

### 🎯 Ihre Aufgabe

Erstellen Sie eine Query, die:

1. **Gleitenden 14-Tages-Durchschnitt** für Luftfeuchte berechnet
2. **Tage findet, an denen Luftfeuchte > 95%** (Nebel/Regen-Kandidaten)
3. **Rangfolge** der feuchtesten Tage ausgibt (mit RANK)
4. **Abweichung vom Monatsdurchschnitt** zeigt

**Starter-Code:**

```sql
WITH humidity_analysis AS (
  SELECT 
    Datum,
    Luftfeuchte,
    AVG(Luftfeuchte) OVER (
      ORDER BY Datum
      ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
    ) as feuchte_14tage_avg,
    -- Ihre Erweiterungen hier!
  FROM weather
)
SELECT * FROM humidity_analysis
WHERE Luftfeuchte > 95
ORDER BY Datum DESC
LIMIT 10;
```
@DuckDB.eval

**Tipp:** Kombinieren Sie Window Functions, RANK und Abweichungs-Berechnungen!

</div>

---

## Ausblick & Nächste Schritte

    --{{0}}--
Sie haben heute mächtige Werkzeuge kennengelernt – Aggregationen und Window Functions sind das Rückgrat moderner Analytics. In den nächsten Lectures vertiefen wir SQL weiter und schauen uns andere Paradigmen an.

      {{0}}
<div>

### 📚 Vorbereitung für Lecture 17

- **Thema:** Graph Stores – Nodes, Edges, Cypher
- **Überlegen:** Welche Beziehungen in Ihren Daten könnten als Graph modelliert werden?
- **Vorwissen:** Relationale Joins vs. Graph Traversal

</div>

    --{{1}}--
Und vergessen Sie nicht: Column Stores sind nicht nur für Batch-Analytics – moderne Tools wie ClickHouse oder TimescaleDB kombinieren OLTP und OLAP in hybriden Architekturen!

      {{1}}
> 🚀 **Trend:** Hybride Datenbanken = OLTP + OLAP in einem System (z.B. CockroachDB, TimescaleDB)

---

## Referenzen & Weiterführende Links

    --{{0}}--
Zum Abschluss noch Ressourcen für Ihr Selbststudium.

      {{0}}
<div>

### Aggregationen & Window Functions

- [PostgreSQL Window Functions Tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Modern SQL: Window Functions](https://modern-sql.com/feature/over)
- [SQL Window Functions Cheat Sheet](https://learnsql.com/blog/sql-window-functions-cheat-sheet/)

### DuckDB

- [DuckDB Official Docs](https://duckdb.org/docs/)
- [DuckDB vs. Others Performance](https://duckdb.org/why_duckdb)
- [DuckDB Internals Blog](https://duckdb.org/docs/internals/overview)

### Column Stores

- [ClickHouse Architecture](https://clickhouse.com/docs/en/development/architecture/)
- [Apache Parquet Documentation](https://parquet.apache.org/docs/)
- [The Design and Implementation of Modern Column-Oriented Databases](https://stratos.seas.harvard.edu/files/stratos/files/columnstoresfntdbs.pdf) (Paper)

### Time-Series & Analytics

- [TimescaleDB Docs](https://docs.timescale.com/)
- [Time-Series Databases Compared](https://www.timescale.com/blog/time-series-database-benchmarks/)

</div>

---

## 🎓 Ende der Lecture 16

    --{{0}}--
Vielen Dank! Sie haben heute einen tiefen Einblick in Analytics-SQL und Column Store Performance bekommen. Nutzen Sie dieses Wissen für Ihre Projekte – und experimentieren Sie mit DuckDB, es ist ein fantastisches Werkzeug!

      {{0}}
> **Bis zur nächsten Vorlesung!** 🚀  
> **Tipp:** Installieren Sie DuckDB lokal (`pip install duckdb`) und spielen Sie mit Ihren eigenen Daten!
