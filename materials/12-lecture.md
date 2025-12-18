<!--
author:   André Dietrich
email:    andre.dietrich@ovgu.de
version:  0.1.0
language: de
narrator: Deutsch Female
comment:  Session 12: Indexe & Performance – Von der KI-generierten Query zur Optimierung
logo:     ../assets/img/logo/logo.png

import:   https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
          https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md

-->

# Session 12: Indexe & Performance

    --{{0}}--
Willkommen zur Session über Indexe und Performance! In der letzten Session haben Sie gesehen, wie KI mit MCP SQL-Queries generiert – aber sind diese Queries auch effizient? Heute lernen Sie, Performance zu messen, zu verstehen und zu optimieren.

    --{{1}}--
Stellen Sie sich vor: Eine Query läuft auf der IMDB-Datenbank mit über 178.000 Titeln. Ohne Index scannt die Datenbank jede einzelne Zeile. Mit dem richtigen Index? Direkter Zugriff in Millisekunden. Das ist der Unterschied, den wir heute erleben werden.

      {{1}}
> **Lernziele dieser Session:**
>
> - Verstehen, was Indexe sind und wie sie funktionieren
> - Praktische Indexe erstellen und Performance messen
> - Query Plans mit EXPLAIN ANALYZE lesen können
> - Kritisch bewerten: Wann Indexe sinnvoll sind (und wann nicht)
> - Best Practices für Index-Strategien anwenden

``` js
const response = await fetch("http://localhost:8000/assets/dat/imdb-40.sql");
if (!response.ok) {
  console.error("Failed to fetch SQL dump");
  return;
}

let sql = await response.text();
sql = sql
	.split(/;\s*\n/)   // split on statement-ending semicolon
  .map(s => s.trim())
  .filter(Boolean)
  .map(s => s + ";"); // re-add semicolon


let size = Math.round(sql.length / 100);
for (let i = 0; i < sql.length; i += size) {
    console.log((i * 100) / sql.length, "%");
    await db.exec(sql.slice(i, i+size).join("\n"));
}

// Load into PGlite
console.log("done")
```
@PGlite.js(imdb)

## Motivation: Der Performance-Unterschied




    --{{0}}--
Lassen Sie uns mit einem konkreten Problem beginnen. Sie haben in Session 11 mit MCP die IMDB-Datenbank erkundet. GitHub Copilot hat Ihnen SQL-Queries generiert – aber niemand hat über Performance gesprochen.

    --{{1}}--
Nehmen wir eine typische Anfrage: "Zeige mir alle Filme mit einem Rating über 8.0". Klingt einfach, oder?

      {{1}}
**Das Problem:**

      {{1}}
```sql
SELECT tb.primaryTitle, tr.averageRating, tb.startYear
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating > 8.0 AND tb.titleType = 'movie';
```
@PGlite.eval(imdb)

    --{{2}}--
Ohne Index durchsucht SQLite jede einzelne Zeile in title_ratings – das sind über 178.000 Einträge! Bei einer großen Produktionsdatenbank wären das Millionen oder Milliarden.

      {{2}}
> **Szenario ohne Index:**
>
> - Table Scan über 178.000+ Zeilen
> - Jede Zeile wird gelesen und gefiltert
> - Typische Ausführungszeit: 50–200ms (abhängig vom System)
>
> **Szenario mit Index:**
>
> - Index Scan nur auf relevante Zeilen
> - Direkter Zugriff via B-Baum
> - Typische Ausführungszeit: 5–20ms (10× schneller!)

    --{{3}}--
Das ist nicht nur ein akademisches Problem. In einer E-Commerce-Anwendung bedeutet das: 10× schnellere Produktsuche, 10× mehr gleichzeitige Nutzer, 10× bessere User Experience.

      {{3}}
**Frage zum Nachdenken:**

      {{3}}
> Wenn eine Query ohne Index 100ms braucht und 1000× pro Sekunde ausgeführt wird – wie viel CPU-Zeit sparen Sie mit einem 10× schnelleren Index?

---

## Was sind Indexe?

    --{{0}}--
Bevor wir in die Praxis gehen, lassen Sie uns verstehen, was Indexe eigentlich sind. Die beste Metapher: Ein Buchindex.



      {{1}}
<div>

### Konzept: Datenbank-Indexe

    --{{1}}--
Stellen Sie sich ein Fachbuch mit 1000 Seiten vor. Sie suchen den Begriff "B-Baum". Ohne Index müssten Sie jede Seite durchblättern – das dauert. Mit Index? Sie schauen hinten nach, finden "B-Baum → Seite 342" und springen direkt dorthin.

Ein **Index** ist eine zusätzliche Datenstruktur, die Spalten einer Tabelle sortiert und schnellen Zugriff ermöglicht.

**Ohne Index:**

```ascii
Table: title_ratings
┌────────────┬──────────────┬─────────┐
│ tconst     │ averageRating│ numVotes│
├────────────┼──────────────┼─────────┤
│ tt0000001  │ 5.7          │ 2000    │  ← Scan Zeile 1
│ tt0000002  │ 6.1          │ 300     │  ← Scan Zeile 2
│ tt0000003  │ 8.2          │ 5000    │  ← Scan Zeile 3
│ ...        │ ...          │ ...     │  ← Scan Zeile 4-178000
│ tt0999999  │ 7.5          │ 1200    │  ← Scan Zeile 178000
└────────────┴──────────────┴─────────┘
       ↓
  Sequential Scan (langsam!)
```

**Mit Index auf `averageRating`:**

```ascii
B-Tree Index:
       [7.5]
      /     \
   [6.0]   [8.5]
   /  \     /  \
[5.0][6.5][8.0][9.0]
  ↓    ↓    ↓    ↓
Direkte Pointer zu Zeilen mit Rating 8.0+
```

</div>

      {{2}}
<div>

      {{2}}
### B-Baum: Die Datenstruktur hinter Indexen

    --{{2}}--
Der Index ist wie ein sortierter Wegweiser. Anstatt linear zu suchen, navigieren Sie durch einen Baum – das ist logarithmisch schneller: O(log n) statt O(n).

Die meisten Datenbanken (SQLite, PostgreSQL, MySQL) nutzen **B-Bäume** (balanced trees) für Indexe.

**Eigenschaften:**

- Selbstbalancierend (immer gleiche Tiefe)
- Mehrere Werte pro Knoten (Cache-effizient)
- Sortierte Speicherung (Range-Queries möglich)

**Zeitkomplexität:**

- Suche: O(log n)
- Einfügen: O(log n)
- Löschen: O(log n)

**Beispiel:** Bei 1.000.000 Zeilen:

- Ohne Index: ~1.000.000 Vergleiche
- Mit B-Baum: ~20 Vergleiche (log₂ 1.000.000 ≈ 20)

</div>

    --{{3}}--
Das ist der Grund, warum Indexe so mächtig sind. Aber Vorsicht: Jeder Index kostet Speicherplatz und verlangsamt INSERT/UPDATE/DELETE. Es ist ein Trade-off.

      {{3}}
**Trade-offs: Die Kehrseite der Medaille**

      {{3}}
| Aspekt          | Vorteil ✅                     | Nachteil ⚠️                                  |
| --------------- | ------------------------------ | ---------------------------------------------- |
| **SELECT**      | Schnellere Abfragen (10×–100×) | –                                              |
| **INSERT**      | –                              | Langsamer (Index aktualisieren)                |
| **UPDATE**      | –                              | Langsamer (Index neu sortieren)                |
| **DELETE**      | –                              | Langsamer (Index bereinigen)                   |
| **Speicher**    | –                              | Zusätzlicher Platzbedarf (~10–30% der Tabelle) |
| **Maintenance** | –                              | Fragmentierung, VACUUM nötig                   |

    --{{4}}--
Die Kunst des Datenbankdesigns ist es, die richtigen Indexe zu wählen: Genug für Performance, aber nicht zu viele, um Writes nicht zu bremsen.

## Hands-on: Indexe in Aktion

    --{{0}}--
Jetzt wird es praktisch! Wir nutzen die IMDB-Datenbank aus Session 11 und führen Performance-Experimente durch. Sie werden den Unterschied selbst sehen – und messen.

### Setup: IMDB-Datenbank verbinden

    --{{0}}--
Falls Sie die Datenbank aus Session 11 noch haben: Perfekt! Falls nicht, laden Sie sie hier herunter:

      {{0}}
> **Download IMDB-Datenbank:**
>
> - [6 MB Version](../assets/dat/imdb/6-mb.sqlite) (kompakt)
> - [10 MB Version](../assets/dat/imdb/10-mb.sqlite) (mittel)
> - [40 MB Version](../assets/dat/imdb/40-mb.sqlite) (vollständig, 178k+ Titel)
>
> Öffnen Sie die Datenbank in Ihrem SQLite-Client oder nutzen Sie MCP wie in Session 11.

    --{{1}}--
Prüfen wir zunächst, welche Indexe bereits existieren. Neue Tabellen haben meist nur einen Index auf dem Primärschlüssel.

      {{1}}
**Schritt 1: Vorhandene Indexe prüfen**

      {{1}}
```sql
-- SQLite-Syntax: Alle Indexe anzeigen
SELECT name, tbl_name, sql 
FROM sqlite_master 
WHERE type = 'index';
```

    --{{2}}--
Sie sehen vermutlich nur automatische Indexe auf Primärschlüsseln wie `tconst` oder `nconst`. Gut – das ist unser Ausgangspunkt.

---

### Experiment 1: Index auf `averageRating`

    --{{0}}--
Unser erstes Experiment: Wir suchen alle Titel mit einem Rating über 8.0. Erst ohne Index, dann mit Index – und vergleichen die Performance.

      {{0}}
**Schritt 2: Baseline messen (ohne Index)**

      {{0}}
```sql
-- Query ohne Index ausführen
EXPLAIN QUERY PLAN
SELECT * FROM title_ratings 
WHERE averageRating > 8.0;
```

    --{{1}}--
Das `EXPLAIN QUERY PLAN` zeigt uns, wie SQLite die Query ausführt. Sie sehen vermutlich "SCAN title_ratings" – das bedeutet: Sequential Scan, jede Zeile wird gelesen.

      {{1}}
**Erwartete Ausgabe:**

      {{1}}
```
QUERY PLAN
`--SCAN title_ratings
```

    --{{2}}--
Jetzt messen wir die tatsächliche Ausführungszeit. Nutzen Sie `.timer on` in SQLite oder schauen Sie in Ihrem Client nach der Execution Time.

      {{2}}
```sql
-- In SQLite CLI:
.timer on

SELECT COUNT(*) FROM title_ratings 
WHERE averageRating > 8.0;

-- Notieren Sie die Zeit!
```

    --{{3}}--
Typisches Ergebnis: 20–100ms (abhängig von System und Datenbankgröße). Das ist nicht katastrophal, aber auch nicht schnell.

      {{3}}
**Schritt 3: Index erstellen**

      {{3}}
```sql
-- Index auf averageRating erstellen
CREATE INDEX idx_rating ON title_ratings(averageRating);

-- SQLite bestätigt: Index erfolgreich erstellt
```

    --{{4}}--
Das Erstellen dauert ein paar Sekunden – die Datenbank sortiert jetzt alle 178.000+ Einträge nach Rating und baut den B-Baum auf.

      {{4}}
**Schritt 4: Gleiche Query mit Index**

      {{4}}
```sql
-- Query erneut ausführen (mit Index)
EXPLAIN QUERY PLAN
SELECT * FROM title_ratings 
WHERE averageRating > 8.0;
```

    --{{5}}--
Jetzt sollten Sie "SEARCH title_ratings USING INDEX idx_rating" sehen. SQLite nutzt den Index!

      {{5}}
**Erwartete Ausgabe:**

      {{5}}
```
QUERY PLAN
`--SEARCH title_ratings USING INDEX idx_rating (averageRating>?)
```

    --{{6}}--
Messen wir erneut die Zeit:

      {{6}}
```sql
SELECT COUNT(*) FROM title_ratings 
WHERE averageRating > 8.0;

-- Wie viel schneller ist es?
```

    --{{7}}--
Typisches Ergebnis: 2–10ms – das ist 5×–10× schneller! Je größer die Datenbank, desto dramatischer der Unterschied.

      {{7}}
> **Reflexion:**
>
> - Wie groß war der Speedup bei Ihnen?
> - Würden Sie diesen Index in Production einsetzen?
> - Welche Queries würden davon profitieren?

---

### Experiment 2: Composite Index auf `startYear` + `titleType`

    --{{0}}--
Manchmal filtern Queries nach mehreren Spalten. Ein **Composite Index** (Multi-Column Index) kann hier helfen – aber die Reihenfolge der Spalten ist wichtig!

      {{0}}
**Szenario:** Alle Filme aus 2020 oder später

      {{0}}
```sql
-- Query ohne Composite Index
EXPLAIN QUERY PLAN
SELECT * FROM title_basics 
WHERE startYear >= '2020' AND titleType = 'movie';
```

    --{{1}}--
Ohne Index: Sequential Scan. Bei 178.000+ Titeln dauert das.

      {{1}}
**Schritt 5: Composite Index erstellen**

      {{1}}
```sql
-- Wichtig: Reihenfolge beachten!
-- Meist gefilterte Spalte zuerst
CREATE INDEX idx_year_type ON title_basics(startYear, titleType);
```

    --{{2}}--
Warum diese Reihenfolge? Weil `startYear` eine Range ist (>=), `titleType` eine Gleichheit (=). B-Bäume arbeiten am besten, wenn Ranges zuerst kommen.

      {{2}}
**Schritt 6: Query mit Composite Index**

      {{2}}
```sql
EXPLAIN QUERY PLAN
SELECT * FROM title_basics 
WHERE startYear >= '2020' AND titleType = 'movie';
```

    --{{3}}--
Jetzt nutzt SQLite den Composite Index – aber nur, wenn beide Spalten im WHERE vorkommen!

      {{3}}
**Wichtige Erkenntnis:**

      {{3}}
> Ein Index auf `(A, B)` hilft bei:
>
> - `WHERE A = ...` ✅
> - `WHERE A = ... AND B = ...` ✅
> - `WHERE B = ...` ❌ (Nur zweite Spalte → Index nutzlos!)
>
> Reihenfolge der Spalten im Index ist entscheidend!

    --{{4}}--
Testen Sie das selbst: Erstellen Sie einen Index `(titleType, startYear)` und vergleichen Sie die Performance. Sie werden sehen: Oft langsamer!

---

### Experiment 3: JOIN-Performance mit Foreign Keys

    --{{0}}--
Joins sind häufige Performance-Killer. Foreign Keys sollten **immer** einen Index haben – prüfen wir das.

      {{0}}
**Szenario:** Alle Filme mit ihren Ratings

      {{0}}
```sql
SELECT tb.primaryTitle, tr.averageRating
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tb.titleType = 'movie';
```

    --{{1}}--
Der JOIN läuft über `tconst` – haben beide Tabellen einen Index darauf?

      {{1}}
**Schritt 7: Indexe auf JOIN-Spalten prüfen**

      {{1}}
```sql
-- Prüfen: Gibt es Indexe auf tconst?
SELECT name, tbl_name 
FROM sqlite_master 
WHERE type = 'index' AND (tbl_name = 'title_basics' OR tbl_name = 'title_ratings');
```

    --{{2}}--
Falls `tconst` ein Primärschlüssel ist, existiert automatisch ein Index. Falls nicht: Erstellen Sie einen!

      {{2}}
```sql
-- Falls nötig: Index auf JOIN-Spalte
CREATE INDEX idx_tconst_basics ON title_basics(tconst);
CREATE INDEX idx_tconst_ratings ON title_ratings(tconst);
```

    --{{3}}--
Ohne diese Indexe würde SQLite einen Nested Loop Join machen – O(n²) Komplexität! Mit Index: Hash Join oder Index Nested Loop – O(n log n).

      {{3}}
**Best Practice:**

      {{3}}
> **Jede Foreign Key-Spalte sollte einen Index haben.**
>
> Das gilt besonders für:
> - Primärschlüssel (automatisch)
> - Foreign Keys (manuell erstellen!)
> - Häufig gejoinete Spalten

---

## EXPLAIN ANALYZE: Query Plans verstehen

    --{{0}}--
Bisher haben wir mit `EXPLAIN QUERY PLAN` gearbeitet – das zeigt uns den Plan, aber nicht die tatsächliche Ausführung. `EXPLAIN ANALYZE` (in PostgreSQL) oder `.eqp on` (SQLite) liefern mehr Details.

    --{{1}}--
Lassen Sie uns einen Query Plan Schritt für Schritt lesen. Das ist wie eine Landkarte für die Datenbank.

      {{1}}
### Anatomie eines Query Plans

      {{1}}
```sql
EXPLAIN QUERY PLAN
SELECT tb.primaryTitle, tr.averageRating
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating > 9.0 AND tb.startYear > '2010';
```

    --{{2}}--
Ein typischer Plan sieht so aus:

      {{2}}
```
QUERY PLAN
|--SEARCH tr USING INDEX idx_rating (averageRating>?)
`--SEARCH tb USING INTEGER PRIMARY KEY (rowid=?)
```

    --{{3}}--
Was bedeutet das? Die Datenbank arbeitet von innen nach außen:

      {{3}}
<div>

1. **SEARCH tr USING INDEX idx_rating**
   - Start: Durchsuche `title_ratings` mit Index `idx_rating`
   - Filter: `averageRating > 9.0`
   - Ergebnis: Liste von `tconst`-Werten

2. **SEARCH tb USING INTEGER PRIMARY KEY**
   - Für jeden `tconst` aus Schritt 1:
   - Suche passende Zeile in `title_basics`
   - Nutze Primary Key (schneller Lookup)

3. **Impliziter Filter:**
   - Prüfe `startYear > '2010'`
   - Nur Zeilen, die beide Bedingungen erfüllen

</div>

    --{{4}}--
Das ist ein effizienter Plan: Zwei Index-Lookups, kein Sequential Scan. Gut!

      {{4}}
### Scan-Typen verstehen

      {{4}}
| Scan-Typ | Bedeutung | Performance |
|----------|-----------|-------------|
| **SCAN** | Sequential Scan (jede Zeile) | 🐌 Langsam |
| **SEARCH ... USING INDEX** | Index Scan (B-Baum) | 🚀 Schnell |
| **SEARCH ... USING PRIMARY KEY** | Primärschlüssel-Lookup | 🚀 Sehr schnell |
| **SEARCH ... USING COVERING INDEX** | Alle Spalten im Index | 🚀🚀 Ultraschnell |

    --{{5}}--
Ihr Ziel beim Optimieren: SCAN vermeiden, SEARCH maximieren!

      {{5}}
### Checkliste für Query-Plan-Analyse

      {{5}}
<div>

Wenn Sie einen Query Plan sehen, fragen Sie sich:

- [ ] **Gibt es Sequential Scans?** → Fehlende Indexe?
- [ ] **Werden die richtigen Indexe genutzt?** → Vergleich mit `sqlite_master`
- [ ] **Ist die Reihenfolge der JOINs sinnvoll?** → Kleinste Tabelle zuerst
- [ ] **Gibt es Subqueries, die vermeidbar wären?** → CTEs oder Joins nutzen
- [ ] **Sind Filter früh angewendet?** → WHERE vor JOIN

</div>

    --{{6}}--
Mit dieser Checkliste können Sie selbst komplexe Queries debuggen und optimieren.

---

## Wann Indexe NICHT helfen

    --{{0}}--
Jetzt kommt der kritische Teil: Indexe sind kein Allheilmittel. Es gibt Situationen, in denen sie sogar schaden können. Lassen Sie uns vier typische Fälle analysieren.

### Fall 1: Kleine Tabellen

    --{{0}}--
Bei Tabellen mit weniger als 1000 Zeilen ist der Overhead eines Index oft größer als der Nutzen.

      {{0}}
**Beispiel:**

      {{0}}
```sql
-- Tabelle mit 100 Einträgen
SELECT * FROM users WHERE role = 'admin';
```

    --{{1}}--
Ohne Index: 100 Zeilen lesen = ~1ms. Mit Index: Index lesen + Zeilen lesen = ~1ms. Kein Unterschied – aber der Index kostet Speicher und verlangsamt INSERTs.

      {{1}}
> **Faustregel:**
>
> - < 100 Zeilen: Nie Index (außer Primary Key)
> - 100–1000 Zeilen: Nur bei sehr häufigen Queries
> - > 1000 Zeilen: Index meist sinnvoll

---

### Fall 2: Hohe Write-Last

    --{{0}}--
Jeder INSERT, UPDATE, DELETE muss alle Indexe aktualisieren. Bei schreibintensiven Anwendungen wird das zum Flaschenhals.

      {{0}}
**Szenario:** Logging-Tabelle mit 10.000 Einträgen pro Sekunde

      {{0}}
```sql
INSERT INTO access_logs (timestamp, user_id, endpoint) 
VALUES (NOW(), 42, '/api/data');
```

    --{{1}}--
Mit 5 Indexen muss die Datenbank bei jedem INSERT 5 B-Bäume aktualisieren – das kostet Performance.

      {{1}}
**Trade-off-Strategie:**

      {{1}}
<div>

1. **Option A:** Wenige Indexe (nur die wichtigsten)
2. **Option B:** Batch-Inserts ohne Index, später REINDEX
3. **Option C:** Partitionierung (z.B. nach Datum)

</div>

    --{{2}}--
In Data Warehouses (viel Lesen, wenig Schreiben) sind 10+ Indexe normal. In OLTP-Systemen (viel Schreiben) sind 2–3 Indexe oft optimal.

---

### Fall 3: Low Selectivity

    --{{0}}--
"Selectivity" bedeutet: Wie viele verschiedene Werte hat eine Spalte? Bei niedriger Selectivity (wenige Werte) bringt ein Index kaum etwas.

      {{0}}
**Beispiel:** Geschlecht in einer Nutzertabelle

      {{0}}
```sql
SELECT * FROM users WHERE gender = 'F';
```

    --{{1}}--
Angenommen, 50% der Nutzer sind weiblich. Ein Index hilft hier nicht – die Datenbank müsste trotzdem die Hälfte aller Zeilen lesen!

      {{1}}
**Selectivity berechnen:**

      {{1}}
```sql
-- Wie viele verschiedene Werte?
SELECT COUNT(DISTINCT gender) FROM users;  -- Antwort: 2

-- Wie viele Zeilen insgesamt?
SELECT COUNT(*) FROM users;  -- Antwort: 100.000

-- Selectivity: 2 / 100.000 = 0.002% (sehr niedrig!)
```

    --{{2}}--
Faustregel: Index nur, wenn Selectivity > 5%. Bei Gender (0.002%) ist ein Index verschwendet.

      {{2}}
> **Hohe Selectivity = Index sinnvoll:**
>
> - E-Mail-Adressen (100% unique)
> - IDs (100% unique)
> - Namen (80%+ unique)
>
> **Niedrige Selectivity = Index nutzlos:**
>
> - Boolean-Felder (50% Selectivity)
> - Status-Felder (z.B. active/inactive)
> - Geschlecht (50% Selectivity)

---

### Fall 4: Funktionen in WHERE-Klauseln

    --{{0}}--
Wenn Sie in WHERE eine Funktion auf die Spalte anwenden, kann SQLite den Index oft nicht nutzen.

      {{0}}
**Beispiel:**

      {{0}}
```sql
-- Index wird NICHT genutzt:
SELECT * FROM title_basics 
WHERE LOWER(primaryTitle) = 'inception';

-- Index WIRD genutzt:
SELECT * FROM title_basics 
WHERE primaryTitle = 'Inception';
```

    --{{1}}--
Warum? Der Index ist auf `primaryTitle` gebaut – aber `LOWER(primaryTitle)` ist ein anderer Wert. Die Datenbank müsste jeden Eintrag transformieren.

      {{1}}
**Lösungen:**

      {{1}}
<div>

1. **Funktion vermeiden:** Exakte Suche statt Case-Insensitive
2. **Computed Column:** Spalte mit `LOWER(primaryTitle)` speichern + Index darauf
3. **Function-Based Index:** In PostgreSQL möglich (nicht in SQLite)

</div>

    --{{2}}--
Weitere Funktionen, die Indexe "brechen": `SUBSTRING()`, `CONCAT()`, `DATE()`, arithmetische Operationen (`salary * 1.1`).

      {{2}}
**Best Practice:**

      {{2}}
> **Indexe funktionieren nur auf rohen Spaltenwerten.**
>
> - ✅ `WHERE startYear = '2020'`
> - ❌ `WHERE CAST(startYear AS INTEGER) = 2020`
> - ✅ `WHERE created_at > '2024-01-01'`
> - ❌ `WHERE YEAR(created_at) = 2024`

---

## Best Practices & Strategien

    --{{0}}--
Sie haben jetzt gesehen, wie Indexe funktionieren – und wann sie scheitern. Lassen Sie uns das in actionable Strategien übersetzen.

### 1. Analysiere erst, optimiere dann

    --{{0}}--
Der häufigste Fehler: "Blindly" Indexe erstellen, ohne zu messen. Das führt zu Index-Bloat und verschlechtert die Performance.

      {{0}}
**Workflow:**

      {{0}}
<div>

1. **Profiling:** Welche Queries sind langsam? (> 100ms)
2. **EXPLAIN:** Query Plan analysieren – wo sind Sequential Scans?
3. **Index Candidate:** Welche WHERE/JOIN-Spalten werden gefiltert?
4. **Erstellen:** Index auf diese Spalten
5. **Messen:** Hat sich die Performance verbessert?
6. **Monitoring:** Index-Nutzung über Zeit beobachten

</div>

    --{{1}}--
Viele Datenbanken bieten Tools, um ungenutzte Indexe zu finden. In PostgreSQL: `pg_stat_user_indexes`. In SQLite: Manuelle Analyse mit EXPLAIN.

      {{1}}
```sql
-- PostgreSQL: Unused Indexes finden
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexname NOT LIKE 'pg_toast%';
```

---

### 2. Index auf häufig gefilterte Spalten

    --{{0}}--
Schauen Sie sich Ihre Top 10 langsamsten Queries an. Welche Spalten tauchen in WHERE, JOIN, ORDER BY auf?

      {{0}}
**Prioritätsliste:**

      {{0}}
| Prio | Spalten-Typ | Beispiel |
|------|-------------|----------|
| 🔴 Hoch | Foreign Keys | `user_id`, `product_id`, `order_id` |
| 🔴 Hoch | Häufige WHERE-Filter | `status`, `created_at`, `email` |
| 🟡 Mittel | ORDER BY-Spalten | `created_at DESC`, `price ASC` |
| 🟡 Mittel | GROUP BY-Spalten | `category`, `region` |
| 🟢 Niedrig | Selten genutzte Spalten | `middle_name`, `favorite_color` |

    --{{1}}--
Ein einfacher Trick: Loggen Sie alle SQL-Queries über eine Woche und zählen Sie, welche Spalten am häufigsten gefiltert werden.

---

### 3. Composite Indexe richtig nutzen

    --{{0}}--
Die Reihenfolge der Spalten in einem Composite Index ist kritisch. Hier ist die Formel:

      {{0}}
**Reihenfolge-Regel:**

      {{0}}
> 1. **Equality-Filter zuerst:** `WHERE status = 'active'`
> 2. **Range-Filter danach:** `WHERE created_at > '2024-01-01'`
> 3. **ORDER BY zuletzt:** `ORDER BY created_at DESC`

    --{{1}}--
Beispiel: Query mit mehreren Filtern

      {{1}}
```sql
SELECT * FROM orders
WHERE status = 'shipped' 
  AND created_at > '2024-01-01'
ORDER BY created_at DESC;
```

    --{{2}}--
Optimaler Index: `(status, created_at)` – Equality zuerst, Range danach.

      {{2}}
```sql
CREATE INDEX idx_orders_status_date 
ON orders(status, created_at);
```

    --{{3}}--
Falscher Index: `(created_at, status)` – Range zuerst → Index nur teilweise genutzt!

---

### 4. Redundante Indexe vermeiden

    --{{0}}--
Ein Index auf `(A, B)` deckt auch Queries auf `A` allein ab. Aber nicht auf `B` allein!

      {{0}}
**Beispiel:**

      {{0}}
```sql
-- Gegeben: Index auf (startYear, titleType)

-- ✅ Index wird genutzt:
WHERE startYear = '2020';

-- ✅ Index wird genutzt:
WHERE startYear = '2020' AND titleType = 'movie';

-- ❌ Index wird NICHT genutzt:
WHERE titleType = 'movie';
```

    --{{1}}--
Das bedeutet: Sie brauchen keinen separaten Index auf `startYear`, wenn Sie bereits `(startYear, titleType)` haben.

      {{1}}
**Redundanz-Check:**

      {{1}}
<div>

- Index `(A)` + Index `(A, B)` → **Redundant!** Lösche `(A)`
- Index `(A, B)` + Index `(B, A)` → **Nicht redundant** (verschiedene Queries)
- Index `(A)` + Index `(B)` → **Nicht redundant** (verschiedene Spalten)

</div>

---

### 5. Monitoring & Wartung

    --{{0}}--
Indexe fragmentieren über Zeit – besonders bei vielen UPDATE/DELETE-Operationen. Regelmäßige Wartung ist nötig.

      {{0}}
**SQLite:**

      {{0}}
```sql
-- Datenbank kompaktieren
VACUUM;

-- Index neu aufbauen
REINDEX idx_rating;
```

    --{{1}}--
In PostgreSQL gibt es zusätzlich `ANALYZE`, um Query-Planer-Statistiken zu aktualisieren.

      {{1}}
**Monitoring-Metriken:**

      {{1}}
<div>

- **Index Size:** Zu groß? Redundante Indexe?
- **Index Scans:** Wird der Index genutzt?
- **Sequential Scans:** Steigen sie an?
- **Write Performance:** Verlangsamen Indexe INSERTs?

</div>

    --{{2}}--
Empfohlene Frequenz: VACUUM wöchentlich, REINDEX monatlich (oder bei Performance-Problemen).

---

## Praktische Übungen

    --{{0}}--
Jetzt sind Sie dran! Diese Übungen helfen Ihnen, das Gelernte zu vertiefen. Arbeiten Sie mit der IMDB-Datenbank aus Session 11.

### Übung 1: Performance-Experiment (15 Min)

    --{{0}}--
Wählen Sie eine Query aus Session 11, die Sie mit MCP gestellt haben – oder erstellen Sie eine neue.

      {{0}}
**Aufgabe:**

      {{0}}
<div>

1. Führen Sie die Query **ohne Index** aus
   - Nutzen Sie `.timer on` (SQLite) oder messen Sie die Zeit
   - Notieren Sie: Ausführungszeit in ms

2. Analysieren Sie mit `EXPLAIN QUERY PLAN`
   - Gibt es Sequential Scans?
   - Welche Spalten werden gefiltert?

3. Erstellen Sie einen **passenden Index**
   - Single-Column oder Composite?
   - Welche Spalten in welcher Reihenfolge?

4. Führen Sie die Query **mit Index** erneut aus
   - Wie viel schneller ist sie? (Faktor: X×)
   - Zeigt EXPLAIN jetzt "SEARCH ... USING INDEX"?

5. **Reflexion:**
   - Würden Sie diesen Index in Production einsetzen?
   - Welche Trade-offs gibt es? (Speicher, Write-Performance)

</div>

    --{{1}}--
Beispiel-Queries, falls Sie Inspiration brauchen:

      {{1}}
```sql
-- Alle Filme aus den 2010ern mit Rating > 7
SELECT * FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tb.startYear BETWEEN '2010' AND '2019'
  AND tr.averageRating > 7.0;

-- Top 100 Personen nach Anzahl der Filme
SELECT nb.primaryName, COUNT(*) AS film_count
FROM name_basics nb
JOIN title_principals tp ON nb.nconst = tp.nconst
GROUP BY nb.nconst
ORDER BY film_count DESC
LIMIT 100;
```

---

### Übung 2: Query Plan Detektiv (10 Min)

    --{{0}}--
Sie bekommen einen Query Plan – Ihre Aufgabe: Bottlenecks finden und Lösungen vorschlagen.

      {{0}}
**Gegeben:** Query Plan (simuliert)

      {{0}}
```
QUERY PLAN
|--SCAN tb
`--SEARCH tr USING INDEX idx_rating (averageRating>?)
```

    --{{1}}--
Fragen:

      {{1}}
<div>

1. **Welche Tabelle wird sequentiell gescannt?**  
   → `title_basics` (tb)

2. **Ist das ein Problem?**  
   → Ja! Bei 178.000+ Zeilen teuer

3. **Welcher Index fehlt vermutlich?**  
   → Index auf der JOIN-Spalte (`tconst`) in `title_basics`

4. **Wie würden Sie optimieren?**  
   → `CREATE INDEX idx_tconst_basics ON title_basics(tconst);`

5. **Was würde sich ändern?**  
   → SCAN → SEARCH USING INDEX

</div>

    --{{2}}--
Testen Sie Ihre Hypothese: Erstellen Sie den Index und prüfen Sie den neuen Plan!

---

### Übung 3: Trade-off Diskussion (5 Min)

    --{{0}}--
Szenario: Sie designen die Datenbank für einen E-Commerce-Shop.

      {{0}}
**Tabellen:**

      {{0}}
<div>

- `products` (100.000 Einträge)
  - `id`, `name`, `category`, `price`, `stock`, `created_at`
- `orders` (1.000.000 Einträge)
  - `id`, `user_id`, `product_id`, `quantity`, `status`, `created_at`
- `users` (50.000 Einträge)
  - `id`, `email`, `name`, `country`, `created_at`

</div>

    --{{1}}--
Fragen:

      {{1}}
<div>

1. **Auf welche Spalten würden Sie Indexe legen?**  
   → Ihre Antwort: ...

2. **Wo würden Sie bewusst KEINE Indexe erstellen?**  
   → Ihre Antwort: ...

3. **Welche Queries sind am kritischsten?**  
   → Produktsuche? Bestellhistorie? User-Login?

4. **Composite Indexe: Welche Kombinationen sinnvoll?**  
   → Z.B. `(user_id, created_at)` für "Meine letzten Bestellungen"?

</div>

    --{{2}}--
Diskutieren Sie mit Kommilitonen oder notieren Sie Ihre Überlegungen. Es gibt keine perfekte Lösung – nur Trade-offs!

      {{2}}
**Mögliche Lösung (Beispiel):**

      {{2}}
<div>

**Indexe:**
- `products`: `(category, price)` (Produktsuche), `(name)` (Textsuche)
- `orders`: `(user_id, created_at)` (Bestellhistorie), `(product_id)` (Verkaufszahlen), `(status)` (offene Bestellungen)
- `users`: `(email)` (Login), `(country)` (Statistiken)

**Keine Indexe:**
- `users.name` (zu viele Variationen, wenig Selectivity)
- `products.stock` (ändert sich ständig → Write-Overhead)
- `orders.quantity` (nie allein gefiltert)

</div>

---

## Zusammenfassung & Ausblick

    --{{0}}--
Glückwunsch! Sie haben jetzt ein fundiertes Verständnis von Indexen und Performance-Optimierung. Lassen Sie uns die wichtigsten Punkte zusammenfassen.

      {{0}}
**Was Sie gelernt haben:**

      {{0}}
<div>

✅ **Konzept:** Indexe sind sortierte B-Bäume für schnellen Zugriff  
✅ **Praxis:** Indexe erstellen, Performance messen, Query Plans lesen  
✅ **Trade-offs:** Schnelleres Lesen vs. langsameres Schreiben  
✅ **Best Practices:** Wann Indexe sinnvoll sind (und wann nicht)  
✅ **Tooling:** EXPLAIN QUERY PLAN, .timer, VACUUM, REINDEX

</div>

    --{{1}}--
Das Wichtigste: Indexe sind kein Autopilot. Sie müssen verstehen, wie Queries ausgeführt werden, und gezielt optimieren.

      {{1}}
### Checkliste für Production-Datenbanken

      {{1}}
<div>

- [ ] **Foreign Keys haben Indexe?**
- [ ] **Häufige WHERE-Spalten indexiert?**
- [ ] **Query Plans für kritische Queries gecheckt?**
- [ ] **Redundante Indexe entfernt?**
- [ ] **Index-Nutzung im Monitoring sichtbar?**
- [ ] **VACUUM/REINDEX regelmäßig durchgeführt?**

</div>

    --{{2}}--
Wenn Sie diese Checkliste befolgen, sind Sie auf einem guten Weg zu performanten Datenbanken.

      {{2}}
### Verbindung zu Session 11 (MCP)

      {{2}}
> **Erinnerung an L11:**
>
> GitHub Copilot generiert SQL-Queries – aber sie sind nicht immer optimal. Jetzt können Sie:
>
> - Query Plans analysieren
> - Fehlende Indexe identifizieren
> - Performance selbst optimieren
>
> **Die KI ist Ihr Werkzeug – aber Sie sind der Architekt!**

    --{{3}}--
In der nächsten Session (L13) lernen Sie Advanced SQL: Views, SET Operations und Window Functions. Diese Features profitieren alle von guten Indexen!

      {{3}}
### Ausblick: Weitere Performance-Themen

      {{3}}
<div>

**Themen, die wir NICHT behandelt haben (aber relevant sind):**

- **Query Optimization:** Subquery vs. JOIN, CTE Materialization
- **Partitioning:** Große Tabellen in kleinere Chunks aufteilen
- **Caching:** Redis, Memcached vor der Datenbank
- **Sharding:** Daten auf mehrere Server verteilen
- **Read Replicas:** Lesezugriffe skalieren
- **Connection Pooling:** Datenbankverbindungen wiederverwenden

</div>

    --{{4}}--
Diese Themen gehören zum Bereich "Database Scaling" – wenn eine einzelne Datenbank nicht mehr ausreicht.

---

## Hausaufgabe (Optional)

    --{{0}}--
Möchten Sie Ihr Wissen vertiefen? Hier sind drei optionale Aufgaben:

      {{0}}
**Aufgabe 1: Index-Portfolio für IMDB**

      {{0}}
<div>

Erstellen Sie **3 Indexe** für die IMDB-Datenbank, die verschiedene Use Cases abdecken:

1. **Produktsuche:** Filme nach Genre + Rating filtern
2. **Zeitreise:** Filme pro Jahrzehnt analysieren
3. **Personen-Lookup:** Schauspieler/Regisseure schnell finden

Dokumentieren Sie:
- Welche Spalten? (Single vs. Composite)
- Warum diese Reihenfolge?
- Welcher Speedup? (Vorher/Nachher-Messung)

</div>

    --{{1}}--
Aufgabe 2: Index-Killer finden

      {{1}}
<div>

Finden Sie eine Query aus Session 11, bei der ein Index **nicht hilft**.

Mögliche Kandidaten:
- Low Selectivity (z.B. `titleType` mit nur 10 Werten)
- Funktionen in WHERE (`LOWER(primaryTitle)`)
- Kleine Ergebnismenge (< 100 Zeilen)

Erklären Sie: Warum hilft der Index nicht? Was wäre die Alternative?

</div>

    --{{2}}--
Aufgabe 3: Real-World Szenario

      {{2}}
<div>

Stellen Sie sich vor, Sie bauen eine Film-Empfehlungs-App mit der IMDB-Datenbank.

**Anforderungen:**
- Nutzer suchen Filme nach Genre, Jahr, Rating
- Top 10 Filme pro Genre
- Personensuche (Schauspieler, Regisseure)
- Tägliche Updates (neue Filme hinzufügen)

**Fragen:**
1. Welche Indexe würden Sie erstellen?
2. Welche Queries sind am kritischsten?
3. Wie würden Sie die Write-Performance (Updates) optimieren?

Schreiben Sie ein kurzes Design-Dokument (1 Seite).

</div>

---

## Referenzen & Ressourcen

    --{{0}}--
Hier sind weiterführende Ressourcen zum Thema Indexe und Performance:

      {{0}}
### Pflichtlektüre

      {{0}}
<div>

- **Use The Index, Luke!** – [https://use-the-index-luke.com](https://use-the-index-luke.com)  
  → Bestes kostenloses Buch zu SQL-Indexen (auch als Print)

- **SQLite Index Documentation** – [https://www.sqlite.org/lang_createindex.html](https://www.sqlite.org/lang_createindex.html)  
  → Offizielle Dokumentation mit Beispielen

- **PostgreSQL: Using EXPLAIN** – [https://www.postgresql.org/docs/current/using-explain.html](https://www.postgresql.org/docs/current/using-explain.html)  
  → Query Plans verstehen (gilt auch für SQLite)

</div>

    --{{1}}--
Weiterführende Ressourcen

      {{1}}
<div>

- **B-Tree Visualisierung** – [https://www.cs.usfca.edu/~galles/visualization/BTree.html](https://www.cs.usfca.edu/~galles/visualization/BTree.html)  
  → Interaktive Animation der Datenstruktur

- **DuckDB Performance Guide** – [https://duckdb.org/docs/guides/performance/indexing](https://duckdb.org/docs/guides/performance/indexing)  
  → Moderne Ansätze (Column Store statt B-Tree)

- **Artikel: "When NOT to use an index"** – Stack Overflow  
  → Diskussion zu Edge Cases

- **YouTube: "Database Indexing Explained"** – Hussein Nasser  
  → Video-Tutorial (30 Min)

</div>

    --{{2}}--
Tools für die Praxis

      {{2}}
<div>

- **SQLite Browser** – [https://sqlitebrowser.org](https://sqlitebrowser.org)  
  → GUI für Index-Management

- **DBeaver** – [https://dbeaver.io](https://dbeaver.io)  
  → Universeller Datenbank-Client (mit EXPLAIN-Visualisierung)

- **pgAdmin** – [https://www.pgadmin.org](https://www.pgadmin.org)  
  → PostgreSQL-spezifisch, aber gute Query-Analyse

</div>

---

    --{{3}}--
Das war Session 12! Sie haben jetzt die Werkzeuge, um jede Datenbank zu analysieren und zu optimieren. In der nächsten Session erweitern wir Ihr SQL-Arsenal mit Views, SET Operations und Window Functions – alles aufbauend auf dem, was Sie heute gelernt haben.

      {{3}}
{{|>}}
**Happy Optimizing! 🚀📊**
