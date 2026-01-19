<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  0.1.0
language: de
narrator: Deutsch Female
comment:  Column Stores & Wide-Column-Stores – Analytics vs. Distributed Storage

import:   https://raw.githubusercontent.com/LiaTemplates/DuckDB/refs/heads/main/README.md
          https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
          https://raw.githubusercontent.com/liaTemplates/SQLite/main/README.md

-->

# Column Stores & Wide-Column-Stores

> **Session 4** – Lecture (90 Minuten)  
> **Block 1:** Paradigmen-Überblick (kompakt)  
> **Lernziel:** LZ 1 – Paradigmen & Einsatzszenarien verstehen

    --{{0}}--
Willkommen zur vierten Vorlesung! Heute schließen wir den Paradigmen-Überblick mit zwei faszinierenden Speicherarchitekturen ab: Column Stores und Wide-Column-Stores. Beide arbeiten mit Spalten – aber auf völlig unterschiedliche Weise und für völlig unterschiedliche Zwecke. Wir werden sehen, warum DuckDB Ihre Analytics-Queries dramatisch beschleunigen kann, während Cassandra Milliarden von Events speichert, ohne ins Schwitzen zu geraten.

---

## Was erwartet Sie heute?

    --{{0}}--
Heute klären wir zwei Konzepte, die oft verwechselt werden: Column Stores für Analytics und Wide-Column-Stores für verteilte Systeme. Wir schauen uns an, wie Spalten-Speicherung funktioniert, warum Kompression hier so effektiv ist, und wann Sie welches Paradigma einsetzen sollten.

      {{0-1}}
<div>

### Überblick

- **Column Stores** (z.B. DuckDB, Parquet): Spaltenorientierte Speicherung für analytische Workloads
- **Wide-Column-Stores** (z.B. Cassandra, HBase): Verteilte Key-Row-Architekturen mit flexiblen Column Families
- **Performance-Vergleich:** DuckDB vs. SQLite bei Analytics-Queries
- **Kompression:** RLE, Dictionary Encoding, Bit-Packing
- **Use Cases:** Wann welches Paradigma?

</div>

    --{{1}}--
Bevor wir einsteigen, eine Frage zum Warmwerden: Stellen Sie sich vor, Sie haben eine Tabelle mit 10 Millionen Zeilen und 50 Spalten. Sie wollen den Durchschnitt von einer einzigen Spalte berechnen. Was glauben Sie: Muss Ihre Datenbank alle 50 Spalten lesen, oder reicht eine?

      {{1}}
> 🤔 **Denkpause:** Warum könnte `SELECT AVG(temperature) FROM weather` in DuckDB schneller sein als in SQLite oder PostgreSQL?

---

## Column Stores – Analytics auf Steroiden

    --{{0}}--
Lassen Sie uns mit Column Stores beginnen – die Geheimwaffe für Analytics. Das Konzept ist bestechend einfach: Statt Zeilen hintereinander zu speichern, speichern wir alle Werte einer Spalte zusammen. Das klingt trivial, hat aber enorme Konsequenzen.

### Zeilenorientiert vs. Spaltenorientiert

    --{{0}}--
Schauen wir uns den Unterschied an. In einer zeilenorientierten Datenbank – wie SQLite, PostgreSQL oder MySQL – werden alle Felder einer Zeile zusammen gespeichert.

      {{0-1}}
<div>

#### Zeilenorientiert (Row-Store)

Alle Felder einer Zeile liegen hintereinander im Speicher:

```ascii
┌─────────────────────────────────────────────────────┐
│ Row 1: [Datum|Temp|Wind|Druck|Feuchte|...]          │
│ Row 2: [Datum|Temp|Wind|Druck|Feuchte|...]          │
│ Row 3: [Datum|Temp|Wind|Druck|Feuchte|...]          │
└─────────────────────────────────────────────────────┘
```

**Vorteil:** Ganze Zeilen schnell lesen (z.B. `SELECT * FROM weather WHERE datum = '2026-01-15'`)  
**Nachteil:** Für `SELECT AVG(temperature)` müssen alle Spalten gelesen werden

</div>

    --{{1}}--
Column Stores drehen das um: Alle Werte einer Spalte werden zusammen gespeichert. Das bedeutet: Wenn Sie nur die Temperatur brauchen, lesen Sie nur die Temperatur-Spalte – nicht die anderen 49 Spalten.

      {{1}}
<div>

#### Spaltenorientiert (Column-Store)

Alle Werte einer Spalte liegen zusammen:

```ascii
┌─────────────────────────────────────────────────────┐
│ Datum:       [15.01.26, 14.01.26, 13.01.26, ...]    │
│ Temp:        [6.4, 5.8, 4.6, -2.3, -7, ...]         │
│ Wind:        [4.1, 5.4, 5.2, 4.6, ...]              │
│ Druck:       [1015, 1013, 1012, 1014, ...]          │
│ Feuchte:     [94, 91, 97, 73, ...]                  │
└─────────────────────────────────────────────────────┘
```

**Vorteil:** Spalten-Aggregationen blitzschnell (nur relevante Spalten lesen)  
**Nachteil:** Einzelne Zeilen rekonstruieren ist teurer

</div>

---

### Live-Demo: DuckDB vs. SQLite

    --{{0}}--
Jetzt wird es praktisch! Wir laden unsere Wetterdaten in DuckDB – eine spaltenorientierte In-Memory-Datenbank, die direkt im Browser läuft. Beobachten Sie, wie schnell DuckDB mit spaltenweisen Aggregationen umgeht.

      {{0-1}}
<div>

#### Schritt 1: CSV-Daten laden

Wir laden die `weather.csv` direkt in DuckDB:

```sql DuckDB
CREATE TABLE weather AS 
SELECT * FROM read_csv_auto(
  'http://localhost:8000/assets/dat/data.csv',
  header = true
);

SELECT * FROM weather LIMIT 5;
```
@DuckDB.eval

---

```js PGlite
// CSV laden const 
let csv = await fetch("../assets/dat/data.csv").then(r => r.text()); 

// Zeilen splitten 
const lines = csv.trim().split(/\r?\n/);

// Header entfernen
lines.shift(); 
await db.query(`CREATE TABLE weather (
    Datum DATE,
    Anzahl_Messwerte INTEGER,
    Windgeschwindigkeit REAL,
    Windrichtung REAL,
    Strahlung REAL,
    Luftdruck REAL,
    Temp_2m REAL,
    Temp_5cm REAL,
    Bodentemp_-10cm REAL,
    Luftfeuchte INTEGER,
    Niederschlagsmenge REAL
);`)

for (const line of lines) { 
    const [ 
        date,
        count,
        wind_speed,
        wind_dir,
        radiation,
        pressure,
        temp_2m,
        temp_5cm,
        soil_temp,
        humidity,
        precipitation
    ] = line.split(","); 

    await db.query(`INSERT INTO weather
        VALUES ( $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11 )`, [
        date, 
        Number(count),
        Number(wind_speed),
        Number(wind_dir),
        Number(radiation),
        Number(pressure),
        Number(temp_2m),
        Number(temp_5cm),
        Number(soil_temp),
        Number(humidity),
        Number(precipitation)
    ]);
}
```
@PGlite.js

</div>

    --{{1}}--
Jetzt kommt der spannende Teil: Wir berechnen Aggregationen – genau das, wofür Column Stores optimiert sind.

      {{1}}
<div>

#### Schritt 2: Spalten-Aggregationen

Berechnen Sie Durchschnittswerte über mehrere tausend Zeilen:

```sql
SELECT 
  COUNT(*) as messungen,
  ROUND(AVG(Temp_2m), 2) as avg_temp,
  ROUND(MIN(Temp_2m), 2) as min_temp,
  ROUND(MAX(Temp_2m), 2) as max_temp,
  ROUND(AVG(Windgeschwindigkeit), 2) as avg_wind
FROM weather;
```
@DuckDB.eval

    --{{1}}--
Beachten Sie: DuckDB liest nur die benötigten Spalten – Temperatur und Windgeschwindigkeit. Alle anderen Spalten bleiben unberührt. Das ist der Performance-Boost!

</div>

---

### Kompression – Der geheime Turbo

    --{{0}}--
Aber es wird noch besser! Spaltenorientierte Speicherung ermöglicht extrem effiziente Kompression. Warum? Weil Werte in einer Spalte oft ähnlich sind – zum Beispiel Temperaturen zwischen minus 10 und plus 30 Grad. Das nutzen Column Stores aus.

      {{0-1}}
<div>

#### Run-Length Encoding (RLE)

Wiederholende Werte werden zusammengefasst:

```ascii
Original:  [10, 10, 10, 10, 11, 11, 12, 12, 12]
RLE:       [(10, 4x), (11, 2x), (12, 3x)]
```

**Beispiel:** Spalte mit vielen NULL-Werten oder konstanten Status-Codes

</div>

    --{{1}}--
Eine weitere Technik ist Dictionary Encoding: Alle eindeutigen Werte werden in einem Wörterbuch gespeichert, die Spalte enthält nur Referenzen.

      {{1-2}}
<div>

#### Dictionary Encoding

Kategorische Werte werden durch Indizes ersetzt:

```ascii
Original:    ["Montag", "Dienstag", "Montag", "Mittwoch", "Montag"]
Dictionary:  {0: "Montag", 1: "Dienstag", 2: "Mittwoch"}
Encoded:     [0, 1, 0, 2, 0]
```

**Vorteil:** Statt "Montag" 7-mal zu speichern, speichern Sie nur die Zahl 0

</div>

    --{{2}}--
Und schließlich Bit-Packing: Wenn Ihre Werte klein sind – zum Beispiel 0 bis 100 – brauchen Sie nicht 32 Bit pro Zahl, sondern nur 7 Bit.

      {{2}}
<div>

#### Bit-Packing

Kleine Werte brauchen weniger Bits:

```ascii
Werte 0-100:    7 Bit statt 32 Bit → 78% Platzersparnis
Werte 0-1000:   10 Bit statt 32 Bit → 69% Platzersparnis
```

**Kombination:** DuckDB kombiniert alle drei Techniken automatisch!

</div>

---

### DuckDB Chunks & Parallelisierung

    --{{0}}--
DuckDB organisiert Daten in sogenannten Chunks – Blöcken von typischerweise 2048 Zeilen. Das ermöglicht parallele Verarbeitung und effiziente Kompression pro Chunk.

      {{0-1}}
<div>

#### Chunk-Architektur

```ascii
Table:
  ┌─────────────┐
  │  Chunk 1    │  Zeilen 1-2048    → komprimiert
  ├─────────────┤
  │  Chunk 2    │  Zeilen 2049-4096 → komprimiert
  ├─────────────┤
  │  Chunk 3    │  Zeilen 4097-6144 → komprimiert
  └─────────────┘
```

**Vorteile:**
- Parallele Verarbeitung (4 CPU-Kerne → 4 Chunks gleichzeitig)
- Chunk-spezifische Kompression
- Effiziente Min/Max-Filter (Chunk kann übersprungen werden)

</div>

    --{{1}}--
Schauen wir uns die Chunk-Statistiken an – Sie können sehen, wie DuckDB Ihre Daten intern organisiert.

      {{1}}
<div>

#### Chunk-Statistiken anzeigen

```sql
PRAGMA storage_info('weather');
```
@DuckDB.eval

    --{{1}}--
Diese Ausgabe zeigt Ihnen: Spalten-Namen, Datentypen, Kompression, Speichergröße. Vergleichen Sie die Original-CSV-Größe mit der komprimierten Größe in DuckDB!

</div>

---

### Use Cases für Column Stores

    --{{0}}--
Wann sollten Sie einen Column Store einsetzen? Die Antwort ist einfach: Immer wenn Sie Analytics machen – also wenige Spalten über viele Zeilen aggregieren.

      {{0}}
<div>

#### Perfekt für Column Stores

- **Data Warehouses:** Millionen Zeilen, Aggregationen über wenige Spalten
- **BI & Reporting:** Dashboards mit `SUM`, `AVG`, `COUNT`
- **Time-Series Analytics:** Sensor-Daten, Logs, Metriken
- **Machine Learning:** Feature-Extraktion aus großen Datasets
- **Data Science:** Explorative Analysen mit Pandas/DuckDB

**Beispiel:** `SELECT AVG(temperature) FROM sensors WHERE timestamp > '2026-01-01'`  
→ DuckDB liest nur `temperature` und `timestamp`, nicht alle 50 Spalten!

</div>

    --{{1}}--
Aber Vorsicht: Column Stores sind nicht für alles ideal. Wenn Sie einzelne Zeilen häufig updaten oder ganze Zeilen schreiben, sind Row-Stores besser.

      {{1}}
<div>

#### Weniger ideal für Column Stores

- **OLTP (Online Transaction Processing):** Viele kleine Updates/Inserts
- **Zeilen-basierter Zugriff:** `SELECT * FROM users WHERE id = 123`
- **Häufige Updates:** `UPDATE products SET price = 9.99 WHERE id = 456`

**Warum?** Zeilen sind über Spalten verteilt → Update bedeutet viele Dateien/Chunks ändern

</div>

---

## Performance-Vergleich: DuckDB vs. SQLite

    --{{0}}--
Jetzt kommt der direkte Vergleich! Wir führen dieselbe Abfrage in DuckDB (spaltenorientiert) und SQLite (zeilenorientiert) aus.

      {{0-1}}
<div>

### Gleiche Abfrage, unterschiedliche Engines

#### DuckDB (Column-Store)

```sql
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  ROUND(AVG(Temp_2m), 2) as avg_temp,
  COUNT(*) as messungen
FROM weather
GROUP BY monat
ORDER BY monat DESC;
```
@DuckDB.eval

---

```sql
SELECT 
  DATE_TRUNC('month', Datum) as monat,
  ROUND(AVG(Temp_2m), 2) as avg_temp,
  COUNT(*) as messungen
FROM weather
GROUP BY monat
ORDER BY monat DESC;
```
@PGlite.eval

</div>

    --{{1}}--
Bei SQLite würde dieselbe Query länger dauern, besonders bei großen Datasets. Warum? Weil SQLite alle Spalten lesen muss, auch wenn wir nur Datum und Temperatur brauchen.

      {{1}}
<div>

#### SQLite (Row-Store)

SQLite ist zeilenorientiert – hier eine vereinfachte Darstellung:

```sql
-- SQLite muss alle Spalten lesen, auch wenn nur 2 benötigt werden
-- Bei 4253 Zeilen × 12 Spalten = 51.036 Werte gelesen
-- DuckDB liest nur 4253 × 2 = 8.506 Werte!
```

**Performance-Unterschied:**
- Kleine Datasets (<100k Zeilen): Kaum Unterschied
- Mittlere Datasets (1M Zeilen): DuckDB ~3-5× schneller
- Große Datasets (>10M Zeilen): DuckDB ~10-50× schneller

</div>

    --{{2}}--
Das ist der Grund, warum moderne Data Warehouses wie Snowflake, BigQuery oder ClickHouse alle spaltenorientiert arbeiten. Analytics-Performance ist einfach in einer anderen Liga.

      {{2}}
> 💡 **Merke:** Spalten-Speicherung ist für **OLAP** (Analytical Processing), Zeilen-Speicherung für **OLTP** (Transaction Processing)

---

## Wide-Column-Stores – Verteilte Flexibilität

    --{{0}}--
Jetzt wechseln wir das Thema: Wide-Column-Stores. Der Name klingt ähnlich, aber das Konzept ist völlig anders! Hier geht es nicht um Analytics, sondern um hochskalierbaren, verteilten Speicher mit flexiblem Schema.

### Was sind Wide-Column-Stores?

    --{{0}}--
Wide-Column-Stores – wie Apache Cassandra oder HBase – organisieren Daten in einer Drei-Ebenen-Hierarchie: Row Key, Column Family, Columns. Das klingt kompliziert, ist aber mächtig.

      {{0-1}}
<div>

#### Datenmodell

```ascii
Row Key: "user:12345"
  └─ Column Family: "profile"
       ├─ name:      "Alice"
       ├─ email:     "alice@example.com"
       └─ created:   "2026-01-01"
  └─ Column Family: "activity"
       ├─ last_login: "2026-01-15"
       ├─ posts:      142
       └─ likes:      1523
```

**Wichtig:** Jede Zeile kann unterschiedliche Spalten haben!

</div>

    --{{1}}--
Das ist der zentrale Unterschied zu relationalen Datenbanken: Das Schema ist flexibel. Manche Zeilen haben 5 Spalten, andere 50 – kein Problem.

      {{1-2}}
<div>

#### Flexible Schema

```ascii
Row "user:1":  [name, email, age]
Row "user:2":  [name, email, phone, address, company]
Row "user:3":  [name]
```

**Vorteil:** Schema-Evolution ohne Migrations-Albträume  
**Nachteil:** Mehr Verantwortung für konsistente Datenmodellierung

</div>

    --{{2}}--
Wide-Column-Stores sind perfekt für Use Cases, bei denen Sie nach Row Keys suchen – zum Beispiel User-Profile, Event-Logs oder Time-Series-Daten.

      {{2}}
<div>

#### Zugriffsmuster

**Schnell:**
- `GET user:12345` → direkter Row Key Lookup
- `SCAN user:12345 TO user:12999` → Range Query auf Row Keys

**Langsam:**
- `SELECT * WHERE email = 'alice@example.com'` → kein Index auf beliebige Spalten
- Joins sind nicht unterstützt

</div>

---

### Use Cases für Wide-Column-Stores

    --{{0}}--
Wann setzen Sie Wide-Column-Stores ein? Immer dann, wenn Sie extreme Skalierung brauchen und Ihre Zugriffsmuster Row-Key-basiert sind.

      {{0}}
<div>

#### Perfekt für Wide-Column-Stores

- **Time-Series Data:** IoT-Sensoren, Logs, Metriken (Row Key = Sensor-ID + Timestamp)
- **Social Networks:** User-Profile, Posts, Feeds (Row Key = User-ID)
- **Event Sourcing:** Event-Logs mit flexiblem Schema
- **High-Volume Writes:** Millionen Events pro Sekunde

**Beispiel (Cassandra):**
```cql
SELECT * FROM sensor_data 
WHERE sensor_id = 'temp-sensor-42' 
  AND timestamp > '2026-01-01';
```

</div>

    --{{1}}--
Aber Vorsicht: Wide-Column-Stores sind keine Analytics-Engines. Sie sind für Lookups und Scans optimiert, nicht für komplexe Aggregationen.

      {{1}}
<div>

#### Weniger ideal für Wide-Column-Stores

- **Ad-hoc Analytics:** Komplexe Aggregationen, Joins
- **Transaktionen über mehrere Zeilen:** Kein ACID über Partitionen hinweg
- **Queries ohne Row Key:** Langsame Full-Table-Scans

**Warum?** Cassandra ist für Verfügbarkeit und Skalierung optimiert, nicht für SQL-Komfort

</div>

---

### Column Store vs. Wide-Column-Store

    --{{0}}--
Zeit für Klarheit! Hier ist die Gegenüberstellung – zwei völlig unterschiedliche Paradigmen mit ähnlichem Namen.

      {{0}}
<div>

| Aspekt | Column Store (DuckDB) | Wide-Column-Store (Cassandra) |
|--------|----------------------|-------------------------------|
| **Primärzweck** | Analytics (OLAP) | Hochskalierbare Lookups (OLTP) |
| **Speicherung** | Spalten physisch zusammen | Row Key + Column Families |
| **Schema** | Fest (Schema-on-Write) | Flexibel (Schema-on-Read) |
| **Zugriffsmuster** | Spalten-Scans, Aggregationen | Row Key Lookups, Range Queries |
| **Kompression** | Hoch (RLE, Dictionary) | Moderat |
| **Skalierung** | Vertikal (Single-Node) | Horizontal (Cluster) |
| **Use Case** | Data Warehouse, BI | IoT, Social Networks, Logs |
| **Beispiel-Query** | `SELECT AVG(temp)` | `WHERE sensor_id = 'x'` |

</div>

    --{{1}}--
Die Namensverwirrung ist historisch bedingt – aber merken Sie sich: Column Stores sind für Analytics, Wide-Column-Stores für verteilte Systeme.

      {{1}}
> 🎯 **Merkhilfe:**  
> **Column Store** = Spalten zusammen → Analytics  
> **Wide-Column-Store** = Zeilen mit vielen Spalten → Skalierung

---

## OLTP vs. OLAP – Das große Bild

    --{{0}}--
Lassen Sie uns einen Schritt zurücktreten und das große Bild betrachten: OLTP versus OLAP – zwei fundamental unterschiedliche Workloads.

      {{0-1}}
<div>

### OLTP – Online Transaction Processing

```ascii
Typische Queries:
  INSERT INTO orders (user_id, product_id, quantity) VALUES (123, 456, 1);
  UPDATE users SET last_login = NOW() WHERE id = 123;
  SELECT * FROM products WHERE id = 789;
```

**Charakteristika:**
- Viele kleine Transaktionen
- Updates/Inserts/Deletes
- Zeilen-basierter Zugriff
- ACID-Garantien wichtig

**Optimales Paradigma:** Row-Store (PostgreSQL, MySQL)

</div>

    --{{1}}--
OLAP ist das Gegenteil: Wenige große Queries, die viele Zeilen scannen, aber nur wenige Spalten brauchen.

      {{1}}
<div>

### OLAP – Online Analytical Processing

```ascii
Typische Queries:
  SELECT region, AVG(sales) FROM orders GROUP BY region;
  SELECT DATE_TRUNC('month', timestamp), COUNT(*) 
    FROM events WHERE timestamp > '2025-01-01' GROUP BY 1;
```

**Charakteristika:**
- Wenige große Queries
- Hauptsächlich Reads
- Spalten-Scans & Aggregationen
- Historische Daten

**Optimales Paradigma:** Column-Store (DuckDB, ClickHouse, BigQuery)

</div>

---

## Paradigmen-Matrix Update

    --{{0}}--
Erweitern wir unsere Paradigmen-Matrix um die heutigen Erkenntnisse! So sehen Sie, wie alle Paradigmen zusammenpassen.

      {{0}}
<div>

### Paradigmen-Vergleich (Block 1 Abschluss)

| Paradigma | Struktur | Flexibilität | Skalierung | Query-Ausdruck | Use Case |
|-----------|----------|--------------|------------|----------------|----------|
| **CSV/JSON** | Datei | Sehr hoch | - | Ad-hoc (Skripte) | Export, Austausch |
| **Key-Value** | Key → Value | Hoch | Horizontal | Key-Lookup | Caching, Sessions |
| **Document** | JSON-Dokumente | Hoch | Horizontal | Query-Sprache | CMS, Kataloge |
| **Wide-Column** | Row Key + Families | Hoch | Horizontal | Row Key Scan | IoT, Social, Logs |
| **Column Store** | Spalten zusammen | Niedrig | Vertikal | SQL (Analytics) | Data Warehouse, BI |
| **Relational** | Tabellen + Schema | Niedrig | Vertikal/Horizontal | SQL (OLTP) | Business Apps |

</div>

    --{{1}}--
Sie sehen: Jedes Paradigma hat seine Stärken. Column Stores für Analytics, Wide-Column für Skalierung, Relational für Transaktionen. Das ist der Kern von Polyglot Persistence – das richtige Tool für den richtigen Job.

      {{1}}
> 💡 **Polyglot Persistence:** Nutze das beste Paradigma für jeden Use Case in deiner Architektur

---

## Zusammenfassung & Reflexion

    --{{0}}--
Fassen wir zusammen: Heute haben wir zwei mächtige Paradigmen kennengelernt und verstanden, warum "Column" nicht gleich "Column" ist.

      {{0-1}}
<div>

### Was Sie heute gelernt haben

1. **Column Stores** speichern Spalten physisch zusammen → Analytics-Performance
2. **Kompression** (RLE, Dictionary, Bit-Packing) ist extrem effektiv bei Spalten
3. **DuckDB** zeigt, wie schnell spaltenorientierte Analytics sein kann
4. **Wide-Column-Stores** nutzen Row Keys + Column Families → Skalierung
5. **OLTP vs. OLAP:** Unterschiedliche Workloads brauchen unterschiedliche Paradigmen

</div>

    --{{1}}--
Jetzt sind Sie dran: Reflektieren Sie kurz, was Sie heute gelernt haben.

      {{1}}
<div>

### 🤔 Reflexionsfragen

1. **Wann würden Sie DuckDB statt PostgreSQL einsetzen?**

   [[Analytics-Queries über große Datasets mit spaltenweisen Aggregationen]]

2. **Warum ist Kompression bei Column Stores so effektiv?**

   [[Werte in einer Spalte sind ähnlich (z.B. Temperaturen 0-30°C), daher hohe Redundanz]]

3. **Wide-Column-Store für ein Online-Shop-Produkt-Katalog – sinnvoll?**

   [(X)] Nein, Document Store ist besser (flexibles Schema + komplexe Queries)
   [( )] Ja, perfekt für Skalierung
   [( )] Relational ist besser

</div>

---

## Ausblick & Nächste Schritte

    --{{0}}--
In der nächsten Vorlesung tauchen wir tiefer ins relationale Modell ein: Tabellen, Schlüssel, Integrität, Normalisierung. Sie werden sehen, dass relationale Datenbanken nach wie vor die Basis der meisten Anwendungen sind – nicht ohne Grund.

      {{0}}
<div>

### 📚 Vorbereitung für Lecture 5

- **Thema:** Relationales Modell – Tabellen, Keys, Integrität
- **Lesen:** Was sind Primärschlüssel? Was sind Fremdschlüssel?
- **Überlegen:** Warum brauchen wir Constraints (UNIQUE, NOT NULL, CHECK)?

</div>

    --{{1}}--
Und hier ein Vorgeschmack: In Lecture 16 kommen wir zurück zu Column Stores – dann zeigen wir Ihnen, wie Sie mit Window Functions und gleitenden Mittelwerten arbeiten, und warum DuckDB bei Sensor-Daten unschlagbar ist.

      {{1}}
> 🚀 **Vorschau Lecture 16:** Aggregationen, Window Functions, gleitende Mittelwerte – und der Performance-Showdown mit echten Wetterdaten!

---

## Referenzen & Weiterführende Links

    --{{0}}--
Zum Abschluss noch ein paar Ressourcen, falls Sie tiefer einsteigen wollen.

      {{0}}
<div>

### Column Stores

- [DuckDB Documentation](https://duckdb.org/docs/) – Offizielle Docs mit vielen Beispielen
- [Apache Parquet Format](https://parquet.apache.org/) – Spaltenorientiertes Dateiformat
- [ClickHouse](https://clickhouse.com/) – Column Store für extreme Performance

### Wide-Column-Stores

- [Apache Cassandra](https://cassandra.apache.org/) – Hochskalierbare Wide-Column-DB
- [Apache HBase](https://hbase.apache.org/) – Hadoop-basierter Wide-Column-Store
- [ScyllaDB](https://www.scylladb.com/) – Cassandra-kompatibel, in C++ geschrieben

### Vergleiche & Konzepte

- [OLTP vs OLAP](https://www.databricks.com/glossary/oltp-vs-olap) – Guter Überblick
- [Column Store Paper (C-Store)](http://db.csail.mit.edu/projects/cstore/) – Akademischer Hintergrund

</div>

---

## 🎓 Ende der Lecture 4

    --{{0}}--
Vielen Dank für Ihre Aufmerksamkeit! Sie haben heute zwei wichtige Paradigmen kennengelernt, die in modernen Architekturen eine zentrale Rolle spielen. Nächste Woche starten wir mit dem relationalen Modell – die Basis, auf der fast alles aufbaut.

      {{0}}
> **Bis zur nächsten Vorlesung!** 🚀
