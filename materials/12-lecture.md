<!--
author:   André Dietrich
email:    andre.dietrich@ovgu.de
version:  0.1.0
language: de
narrator: Deutsch Female
comment:  Session 12: Indexe & Performance – Praktische Optimierung mit PGlite
logo:     ../assets/img/logo/logo.png

import:   https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
          https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md

-->

# Session 12: Indexe & Performance

    --{{0}}--
Willkommen zur Session über Indexe und Performance! In der letzten Session haben Sie gesehen, wie KI mit MCP SQL-Queries generiert – aber sind diese Queries auch effizient? Heute lernen Sie, Performance zu messen, zu verstehen und zu optimieren.

    --{{1}}--
Stellen Sie sich vor: Eine Query läuft auf der IMDB-Datenbank mit über 178.000 Titeln. Ohne Index scannt die Datenbank jede einzelne Zeile. Mit dem richtigen Index? Direkter Zugriff in Millisekunden. Das ist der Unterschied, den wir heute mit PGlite live erleben werden.

      {{1}}
> **Lernziele dieser Session:**
>
> - Verstehen, was Indexe sind und wie sie funktionieren
> - Praktische Indexe mit PGlite erstellen und Performance messen
> - Query Plans mit EXPLAIN ANALYZE lesen können
> - Kritisch bewerten: Wann Indexe sinnvoll sind (und wann nicht)
> - Best Practices für Index-Strategien anwenden


## Motivation: Der Performance-Unterschied

    --{{0}}--
Lassen Sie uns mit einem konkreten Problem beginnen. Sie haben in Session 11 mit MCP die IMDB-Datenbank erkundet. GitHub Copilot hat Ihnen SQL-Queries generiert – aber niemand hat über Performance gesprochen.

    --{{1}}--
Nehmen wir eine typische Anfrage: "Zeige mir alle Filme mit einem Rating über 8.0". Klingt einfach, oder?

      {{1}}
**Das Problem:**

      {{1}}
```sql
SELECT tb.primarytitle, tr.averagerating, tb.startyear
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averagerating > 8.0 AND tb.titletype = 'movie';
```
``` @output
|   # | primarytitle                | averagerating | startyear |
|-----|-----------------------------|---------------|-----------|
|   1 | Milionar pentru o zi        |      8.3      |   1924    |
|   2 | Napoleon                    |      8.2      |   1927    |
|   3 | Zeinab                      |      8.6      |   1930    |
|   4 | It's a Wise Child           |      8.4      |   1931    |
|   5 | Geld fällt vom Himmel       |      8.2      |   1938    |
|   6 | La tonta del bote           |      8.6      |   1939    |
|   7 | Herzensfreud - Herzensleid  |      8.6      |   1940    |
|   8 | The Best Years of Our Lives |      8.1      |   1946    |
|   9 | Abhimanyu                   |      8.2      |   1948    |
|  10 | Los tres huastecos          |      8.1      |   1948    |
|  11 | Pathala Bhairavi            |      8.5      |   1951    |
|  12 | The Life of Oharu           |      8.1      |   1952    |
... (more rows) ...
```

    --{{2}}--
Ohne Index durchsucht PostgreSQL jede einzelne Zeile in title_ratings – das sind über 178.000 Einträge! Bei einer großen Produktionsdatenbank wären das Millionen oder Milliarden.

      {{2}}
> **Szenario ohne Index:**
>
> - Sequential Scan über 178.000+ Zeilen
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

### Demo

??[BTree Visualization](https://btree.app)<!-- style="width: 100%; height: 70vh" -->

## Hands-on: Indexe in Aktion

    --{{0}}--
Jetzt wird es praktisch! Wir nutzen die IMDB-Datenbank aus Session 11 und führen Performance-Experimente durch. Sie werden den Unterschied selbst sehen – und messen.

### Setup: IMDB-Datenbank verbinden

    --{{0}}--
Führen Sie das folgenden Script aus um die IMDB-Datenbank für diese Session in PGlite zu laden.

``` js
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const response = await fetch("../assets/dat/imdb.sql");
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
    await wait(50); // small delay to keep UI responsive
}

// Load into PGlite
console.log("done")
```
@PGlite.js(imdb)

      {{0}}
> **PGlite-Setup:**
>
> - Datenbank läuft im Browser (kein Server nötig!)
> - Alle Queries führen Sie direkt in dieser Session aus
> - Die Daten bleiben im Browser-Speicher

    --{{1}}--
Prüfen wir zunächst, welche Indexe bereits existieren. Neue Tabellen haben meist nur einen Index auf dem Primärschlüssel.

      {{1}}
**Schritt 1: Vorhandene Indexe prüfen**

      {{1}}
```sql
-- PostgreSQL-Syntax: Alle Indexe in der aktuellen Datenbank
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```
@PGlite.eval(imdb)

    --{{2}}--
Sie sehen vermutlich nur automatische Indexe auf Primärschlüsseln wie `tconst_pkey` oder `nconst_pkey`. Gut – das ist unser Ausgangspunkt.

### Experiment 0: (Index-) Scan Typen

    --{{0}}--
Bevor wir zu komplexen Beispielen kommen, lernen wir die verschiedenen Scan-Strategien kennen. PostgreSQL wählt unterschiedliche Ansätze, je nachdem welche Spalten abgefragt werden. Wir erstellen erst einen Index und testen dann drei Szenarien.

__Index auf primaryTitle erstellen__

``` sql
-- Index für unsere Experimente
CREATE INDEX IF NOT EXISTS
  idx_title
  ON title_basics(primaryTitle);

-- Bitmap Scan (vorläufig ausschalten)
SET enable_bitmapscan = off;
```
@PGlite.eval(imdb)

      --{{1}}--
Jetzt haben wir einen B-Baum-Index auf den Filmtiteln. Schauen wir uns an, wie PostgreSQL diesen Index nutzt.

      {{1}}
``` sql
-- Suche nach Titel-Muster (Index kann nicht helfen!)
EXPLAIN
SELECT primaryTitle, startYear
FROM title_basics
WHERE primaryTitle LIKE '%Matrix%';
```
@PGlite.eval(imdb)

      --{{2}}--
Sie sehen „Seq Scan“ – warum? Weil `LIKE '%Matrix%'` in der Mitte sucht. Der Index ist alphabetisch sortiert, kann aber nur Präfix-Suchen optimieren. Hier muss jede Zeile gelesen werden.

{{2}} __Szenario 2: Index Scan (Index + Table)__

      {{2}}
``` sql
EXPLAIN
SELECT primaryTitle, startYear, titleType, genres
FROM title_basics
WHERE primaryTitle LIKE 'Matrix%';
```
@PGlite.eval(imdb)

      --{{3}}--
Jetzt sehen Sie „Index Scan using idx_title“ – PostgreSQL nutzt den Index, um die Zeile zu finden, muss aber zusätzlich die Tabelle lesen, um `startYear`, `titleType` und `genres` zu holen (die sind NICHT im Index gespeichert).

{{3}}
__Index Scan bedeutet:__ 1. Index durchsuchen -> Zeilen-Position finden 2. Zur Tabelle (Heap) springen -> Alle Spalten lesen

 {{3}} __Szenario 3:__ Index Only Scan (nur Index!)

``` sql
-- Query NUR auf die indexierte Spalte
EXPLAIN
SELECT primaryTitle
FROM title_basics
WHERE primaryTitle::Text = 'Interstellar';
```
@PGlite.eval(imdb)

    {{4}}
<section>

      --{{4}}--
Jetzt könnte PGlite/PostgreSQL einen „Index Only Scan“ verwenden – alle Daten (nur primaryTitle) sind bereits im Index! Kein Table-Read nötig. Das ist die schnellste Variante.

__Index Only Scan bedeutet:__

1. Index durchsuchen → Wert direkt aus Index lesen
2. Kein Heap-Zugriff nötig!

__Hinweis:__ In PGlite/PostgreSQL funktioniert Index Only Scan nur, wenn: - Alle SELECT-Spalten im Index sind - Die Tabelle „visibility map“ hat (VACUUM wurde ausgeführt)

 __Bonus: COUNT mit Index__

``` sql
-- Zählen mit Index-Unterstützung

EXPLAIN ANALYZE
SELECT COUNT(*)
FROM title_basics
WHERE primaryTitle LIKE 'Matrix%';
```
@PGlite.eval(imdb)

    --{{5}}--
Diese Query findet 4 Filme mit „Matrix“ am Anfang. PGlite kann den Index nutzen, weil es eine Präfix-Suche ist (sortierter Index hilft!). Je nach Optimierung sehen Sie einen Bitmap Index Scan.

### Experiment 1: Index auf `averageRating`

    --{{0}}--
Unser erstes Experiment: Wir suchen alle Titel mit einem Rating über 9.5. Erst ohne Index, dann mit Index – und vergleichen die Performance.

      {{0}}
**Schritt 2: Baseline messen (ohne Index)**

      {{0}}
```sql
-- Bitmap Scan (wieder einschalten)
SET enable_bitmapscan = on;

-- Query ohne Index analysieren
EXPLAIN ANALYZE
SELECT * FROM title_ratings 
WHERE averagerating > 9.5;
```
@PGlite.eval(imdb)

    --{{1}}--
Das `EXPLAIN ANALYZE` zeigt uns, wie PostgreSQL die Query ausführt UND misst die tatsächliche Zeit. Sie sehen vermutlich "Seq Scan on title_ratings" – das bedeutet: Sequential Scan, jede Zeile wird gelesen.

      {{1}}
**Erwartete Ausgabe:**

      {{1}}
```
Seq Scan on title_ratings  (cost=10000000000.00..10000002837.50 rows=45400 width=40)
```

    --{{2}}--
Jetzt führen wir die Query tatsächlich aus und zählen die Ergebnisse:

      {{2}}
```sql
-- Query ausführen und Anzahl zählen
SELECT COUNT(*) FROM title_ratings 
WHERE averagerating > 9.5;
```
@PGlite.eval(imdb)

    --{{3}}--
PGlite ist im Browser sehr schnell, aber bei größeren Datenmengen sehen Sie trotzdem den Unterschied. Merken Sie sich die Ausführungszeit!

      {{3}}
**Schritt 3: Index erstellen**

      {{3}}
```sql
-- Index auf averagerating erstellen
CREATE INDEX idx_rating ON title_ratings(averagerating);
```
@PGlite.eval(imdb)

    --{{4}}--
Das Erstellen dauert ein paar Sekunden – die Datenbank sortiert jetzt alle 178.000+ Einträge nach Rating und baut den B-Baum auf.

      {{4}}
**Schritt 4: Gleiche Query mit Index**

      {{4}}
```sql
-- Query erneut analysieren (mit Index)
EXPLAIN ANALYZE
SELECT * FROM title_ratings 
WHERE averagerating > 9.5;
```
@PGlite.eval(imdb)

    --{{5}}--
Jetzt sollten Sie "Index Scan using idx_rating" oder "Bitmap Index Scan" sehen. PostgreSQL nutzt den Index!

      {{5}}
**Erwartete Ausgabe:**

      {{5}}
```
Index Scan using idx_rating on title_ratings  (cost=0.29..XXX.XX rows=XXXX width=XX)
  Index Cond: (averagerating > '8.0'::numeric)
```

    --{{6}}--
Messen wir erneut durch direktes Ausführen:

      {{6}}
```sql
SELECT COUNT(*) FROM title_ratings 
WHERE averagerating > 9.5;
```
@PGlite.eval(imdb)

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
EXPLAIN ANALYZE
SELECT * FROM title_basics 
WHERE startyear >= '2020' AND titletype = 'movie';
```
@PGlite.eval(imdb)

    --{{1}}--
Ohne Index: Sequential Scan. Bei 178.000+ Titeln dauert das.

      {{1}}
**Schritt 5: Composite Index erstellen**

      {{1}}
```sql
-- Wichtig: Reihenfolge beachten!
-- Meist gefilterte Spalte zuerst
CREATE INDEX idx_year_type ON title_basics(startyear, titletype);
```
@PGlite.eval(imdb)

    --{{2}}--
Warum diese Reihenfolge? Weil `startYear` eine Range ist (>=), `titleType` eine Gleichheit (=). B-Bäume arbeiten am besten, wenn Ranges zuerst kommen.

      {{2}}
**Schritt 6: Query mit Composite Index**

      {{2}}
```sql
EXPLAIN ANALYZE
SELECT * FROM title_basics 
WHERE startyear >= '2020' AND titletype = 'movie';
```
@PGlite.eval(imdb)

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
Jetzt wird es dramatisch! Joins ohne Index sind der Performance-Albtraum schlechthin. Ohne Index auf der JOIN-Spalte muss die Datenbank einen Nested Loop durchführen – bei 178.000 Zeilen bedeutet das theoretisch 31 MILLIARDEN Vergleiche!

      {{0}}
**Szenario:** Top-bewertete Filme mit allen Details

      {{0}}
**Schritt 7: Baseline ohne Index (LANGSAM!)**

      {{0}}
```sql
-- Query OHNE Index auf tconst analysieren
EXPLAIN ANALYZE
SELECT tb.primaryTitle, tr.averageRating, tb.startYear
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating >= '9.0'
ORDER BY tr.averageRating DESC
LIMIT 20;
```
@PGlite.eval(imdb)

    --{{1}}--
Sie sehen vermutlich "Seq Scan" auf beiden Tabellen und einen "Hash Join" oder "Nested Loop". Bei großen Datenmengen ist das extrem langsam – jede Zeile aus title_ratings muss mit ALLEN Zeilen aus title_basics verglichen werden.

      {{1}}
**Erwartete Ausgabe (ohne Index):**

      {{1}}
```
Hash Join  (cost=5000..15000 rows=10000)
  ->  Seq Scan on title_basics tb
  ->  Hash
        ->  Seq Scan on title_ratings tr
              Filter: (averageRating >= '9.0')
```

    --{{2}}--
Messen wir die tatsächliche Zeit durch direktes Ausführen:

      {{2}}
```sql
-- Query ausführen und Ergebnisse zählen
SELECT COUNT(*) as result_count
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating >= '9.0';
```
@PGlite.eval(imdb)

    --{{3}}--
Bei mir im Browser dauert das ohne Index spürbar länger – merken Sie sich die Zeit!

      {{3}}
**Schritt 8: Indexe auf JOIN-Spalten erstellen**

      {{3}}
```sql
-- Index auf tconst in BEIDEN Tabellen erstellen
CREATE INDEX IF NOT EXISTS idx_tconst_basics ON title_basics(tconst);
CREATE INDEX IF NOT EXISTS idx_tconst_ratings ON title_ratings(tconst);

-- Bonus: Index auf averageRating für den WHERE-Filter
CREATE INDEX IF NOT EXISTS idx_rating ON title_ratings(averageRating);
```
@PGlite.eval(imdb)

    --{{4}}--
Das Erstellen dauert ein paar Sekunden – die Datenbank baut jetzt B-Bäume für schnelle Lookups auf. In Production würden diese Indexe normalerweise bereits existieren (besonders auf Primär- und Fremdschlüsseln).

      {{4}}
**Schritt 9: Gleiche Query mit Index**

      {{4}}
```sql
-- Query erneut analysieren (MIT Index)
EXPLAIN ANALYZE
SELECT tb.primaryTitle, tr.averageRating, tb.startYear
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating >= '9.0'
ORDER BY tr.averageRating DESC
LIMIT 20;
```
@PGlite.eval(imdb)

    --{{5}}--
Jetzt sollten Sie "Index Scan" oder "Index Only Scan" sehen – die Datenbank nutzt die Indexe! Der JOIN wird dramatisch schneller.

      {{5}}
**Erwartete Ausgabe (mit Index):**

      {{5}}
```
Nested Loop  (cost=0.29..500 rows=10000)
  ->  Index Scan using idx_rating on title_ratings tr
        Index Cond: (averageRating >= '9.0')
  ->  Index Scan using idx_tconst_basics on title_basics tb
        Index Cond: (tconst = tr.tconst)
```

    --{{6}}--
Die Komplexität ist von O(n²) auf O(n log n) gesunken – das ist bei großen Datenmengen der Unterschied zwischen Minuten und Millisekunden!

      {{6}}
**Performance-Vergleich:**

      {{6}}
```sql
-- Erneut ausführen und Zeit vergleichen
SELECT COUNT(*) as result_count
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating >= '9.0';
```
@PGlite.eval(imdb)

    --{{7}}--
Typisches Ergebnis: 5–20× schneller! Bei Millionen von Zeilen wäre der Unterschied noch dramatischer – aus mehreren Minuten werden Sekunden.

      {{7}}
**Best Practice:**

      {{7}}
> **Jede Foreign Key-Spalte sollte einen Index haben.**
>
> Das gilt besonders für:
> - Primärschlüssel (meist automatisch)
> - Foreign Keys (oft manuell erstellen!)
> - Häufig gejoinete Spalten
>
> **Unsere IMDB-Demo-DB hat bewusst KEINE Indexe**, um den Performance-Unterschied zu zeigen. In Production wäre das ein kritischer Fehler!

    --{{8}}--
Reflexion: Überlegen Sie sich – welche anderen Spalten in der IMDB-Datenbank würden von Indexen profitieren? Welche nicht?

---

## EXPLAIN ANALYZE: Query Plans verstehen

    --{{0}}--
Bisher haben wir mit `EXPLAIN ANALYZE` gearbeitet – das zeigt uns sowohl den Plan ALS AUCH die tatsächliche Ausführung mit echten Timings. Das ist besonders wertvoll in PostgreSQL!

    --{{1}}--
Lassen Sie uns einen Query Plan Schritt für Schritt lesen. Das ist wie eine Landkarte für die Datenbank.

### Anatomie eines Query Plans

      {{1}}
```sql
EXPLAIN ANALYZE
SELECT tb.primarytitle, tr.averagerating
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averagerating > 9.0 AND tb.startyear > '2010';
```
@PGlite.eval(imdb)

    --{{2}}--
Ein typischer PostgreSQL-Plan sieht so aus:

      {{2}}
```
Hash Join  (cost=X..Y rows=Z width=W) (actual time=...)
  Hash Cond: (tb.tconst = tr.tconst)
  ->  Seq Scan on title_basics tb  (cost=...)
        Filter: ((startyear)::text > '2010'::text)
  ->  Hash  (cost=...)
        ->  Index Scan using idx_rating on title_ratings tr  (cost=...)
              Index Cond: (averagerating > '9.0'::numeric)
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
| Scan-Typ (PostgreSQL) | Bedeutung | Performance |
|----------|-----------|-------------|
| **Seq Scan** | Sequential Scan (jede Zeile) | 🐌 Langsam |
| **Index Scan** | Index Scan (B-Baum) | 🚀 Schnell |
| **Index Only Scan** | Alle Daten aus Index | 🚀🚀 Ultraschnell |
| **Bitmap Index Scan** | Index + Bitmap für viele Zeilen | 🚀 Mittelschnell |
| **Hash Join / Merge Join** | Effiziente JOIN-Strategien | 🚀 Schnell |

    --{{5}}--
Ihr Ziel beim Optimieren: SCAN vermeiden, SEARCH maximieren!

      {{5}}
### Checkliste für Query-Plan-Analyse

      {{5}}
<div>

Wenn Sie einen Query Plan sehen, fragen Sie sich:

- [ ] **Gibt es Seq Scans?** → Fehlende Indexe?
- [ ] **Werden die richtigen Indexe genutzt?** → Vergleich mit `pg_indexes`
- [ ] **Ist die Reihenfolge der JOINs sinnvoll?** → Kleinste Tabelle zuerst
- [ ] **Gibt es Subqueries, die vermeidbar wären?** → CTEs oder Joins nutzen
- [ ] **Sind Filter früh angewendet?** → WHERE vor JOIN
- [ ] **Sind die Kosten (cost) realistisch?** → ANALYZE regelmäßig ausführen

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
**Selectivity berechnen (Konzept):**

      {{1}}
```sql
-- Beispiel mit IMDB: Wie viele verschiedene titletype-Werte?
SELECT COUNT(DISTINCT titletype) FROM title_basics;

-- Wie viele Zeilen insgesamt?
SELECT COUNT(*) FROM title_basics;

-- Selectivity = DISTINCT values / Total rows
-- Wenn das Ergebnis < 5%, ist ein Index oft nicht sinnvoll
```
@PGlite.eval(imdb)

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
WHERE LOWER(primarytitle) = 'inception';

-- Index WIRD genutzt:
SELECT * FROM title_basics 
WHERE primarytitle = 'Inception';
```
@PGlite.eval(imdb)

    --{{1}}--
Warum? Der Index ist auf `primaryTitle` gebaut – aber `LOWER(primaryTitle)` ist ein anderer Wert. Die Datenbank müsste jeden Eintrag transformieren.

      {{1}}
**Lösungen:**

      {{1}}
<div>

1. **Funktion vermeiden:** Exakte Suche statt Case-Insensitive
2. **Computed Column:** Spalte mit `LOWER(primarytitle)` speichern + Index darauf
3. **Function-Based Index:** In PostgreSQL möglich! (Beispiel unten)

</div>

      {{2}}
```sql
-- PostgreSQL: Expression Index (Function-Based Index)
CREATE INDEX idx_title_lower ON title_basics(LOWER(primarytitle));

-- Jetzt funktioniert die Query mit Index:
SELECT * FROM title_basics WHERE LOWER(primarytitle) = 'inception';
```
@PGlite.eval(imdb)

    --{{2}}--
Weitere Funktionen, die Indexe "brechen": `SUBSTRING()`, `CONCAT()`, `DATE()`, arithmetische Operationen (`salary * 1.1`).

      {{3}}
**Best Practice:**

      {{3}}
> **Indexe funktionieren am besten auf rohen Spaltenwerten.**
>
> - ✅ `WHERE startyear = '2020'`
> - ❌ `WHERE CAST(startyear AS INTEGER) = 2020`
> - ✅ `WHERE created_at > '2024-01-01'`
> - ❌ `WHERE EXTRACT(YEAR FROM created_at) = 2024`
> - ✅ (PostgreSQL) `CREATE INDEX ON table(EXTRACT(YEAR FROM created_at))`

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
-- (Hinweis: pg_stat_user_indexes ist in PGlite möglicherweise nicht verfügbar,
--  funktioniert aber in vollständigen PostgreSQL-Installationen)
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexname NOT LIKE 'pg_toast%';
```

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
> 1. **Equality-Filter zuerst:** `WHERE titleType = 'movie'`
> 2. **Range-Filter danach:** `WHERE startYear >= '2020'`
> 3. **ORDER BY zuletzt:** `ORDER BY startYear DESC`

    --{{1}}--
Beispiel: Realistische IMDB-Query mit mehreren Filtern

      {{1}}
```sql
-- Alle Filme seit zwischen 2015 und 2017
EXPLAIN ANALYZE
SELECT primaryTitle, startYear
FROM title_basics tb
WHERE titleType = 'movie' 
  AND startYear >= '2015'
  AND startYEAR <= 2017
ORDER BY startYear DESC
LIMIT 50;
```
@PGlite.eval(imdb)

    --{{2}}--
Diese Query findet 1.638 Top-Filme seit 2015. Ohne Index: Sequential Scan über 178.124 Zeilen. Welcher Index wäre optimal?

      {{2}}
**Optimaler Composite Index:**

      {{2}}
```sql
-- Equality (titleType) zuerst, Range (startYear) danach
CREATE INDEX idx_type_year 
ON title_basics(titleType, startYear);
```
@PGlite.eval(imdb)

    --{{3}}--
Warum diese Reihenfolge? `titleType = 'movie'` ist eine Equality (=), `startYear >= '2015'` ist eine Range (>=). B-Bäume filtern erst exakt, dann im Bereich.

      {{3}}
**Test: Query mit optimalem Index**

      {{3}}
```sql
EXPLAIN ANALYZE
SELECT COUNT(*) 
FROM title_basics
WHERE titleType = 'movie' AND startYear >= '2015';
```
@PGlite.eval(imdb)

    --{{4}}--
Sie sehen vermutlich "Index Scan using idx\_type\_year" oder "Bitmap Index Scan" – der Index wird effizient genutzt!

      {{4}}
**Falscher Index: Range zuerst**

      {{4}}
```sql
DROP INDEX IF EXISTS idx_type_year;
-- FALSCH: Range (startYear) vor Equality (titleType)
CREATE INDEX idx_year_type_wrong 
ON title_basics(startYear, titleType);
```
@PGlite.eval(imdb)

    --{{5}}--
Mit diesem Index kann PostgreSQL nur `startYear` nutzen – `titleType` wird ignoriert, weil es nach der Range kommt. Bei 136 verschiedenen Jahren weniger effizient!

      {{5}}
**Vergleich: Welche Queries profitieren?**

      {{5}}
```sql
-- Index: (titleType, startYear)

-- ✅ NUTZT Index effizient:
WHERE titleType = 'movie' AND startYear >= '2015';

-- ✅ NUTZT Index teilweise (nur titleType):
WHERE titleType = 'movie';

-- ⚠️ NUTZT Index schlecht (nur startYear):
WHERE startYear >= '2015';

-- ❌ NUTZT Index NICHT:
WHERE startYear >= '2015' AND titleType = 'movie';  -- Reihenfolge egal!
```

    --{{6}}--
Merke: Die WHERE-Reihenfolge im SQL ist egal – aber die Index-Spalten-Reihenfolge ist kritisch!

---

### 4. Redundante Indexe vermeiden

    --{{0}}--
Ein Index auf `(A, B)` deckt auch Queries auf `A` allein ab. Aber nicht auf `B` allein!

      {{0}}
**Beispiel:**

      {{0}}
```sql
-- Gegeben: Index auf (startyear, titletype)

-- ✅ Index wird genutzt:
WHERE startyear = '2020';

-- ✅ Index wird genutzt:
WHERE startyear = '2020' AND titletype = 'movie';

-- ❌ Index wird NICHT effizient genutzt:
WHERE titletype = 'movie';
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
**PostgreSQL/PGlite:**

      {{0}}
```sql
-- Statistiken aktualisieren (wichtig für Query Planer!)
ANALYZE;

-- Spezifische Tabelle analysieren
ANALYZE title_ratings;

-- Index neu aufbauen (selten nötig)
REINDEX INDEX idx_rating;
```
@PGlite.eval(imdb)

    --{{1}}--
In PostgreSQL ist `ANALYZE` besonders wichtig – der Query Planer braucht aktuelle Statistiken, um die besten Indexe zu wählen!

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

## Referenzen & Ressourcen


      {{0}}
<div>

### Pflichtlektüre

    --{{0}}--
Hier sind weiterführende Ressourcen zum Thema Indexe und Performance:

- **Use The Index, Luke!** – [https://use-the-index-luke.com](https://use-the-index-luke.com)  
  → Bestes kostenloses Buch zu SQL-Indexen (auch als Print)

- **PostgreSQL: Using EXPLAIN** – [https://www.postgresql.org/docs/current/using-explain.html](https://www.postgresql.org/docs/current/using-explain.html)  
  → Query Plans verstehen (direkt für PGlite relevant!)

- **PostgreSQL Indexes** – [https://www.postgresql.org/docs/current/indexes.html](https://www.postgresql.org/docs/current/indexes.html)  
  → Offizielle Dokumentation mit fortgeschrittenen Techniken

</div>

      {{1}}
<div>

    --{{1}}--
Weiterführende Ressourcen

- **B-Tree Visualisierung** – [https://www.cs.usfca.edu/~galles/visualization/BTree.html](https://www.cs.usfca.edu/~galles/visualization/BTree.html)  
  → Interaktive Animation der Datenstruktur

- **DuckDB Performance Guide** – [https://duckdb.org/docs/guides/performance/indexing](https://duckdb.org/docs/guides/performance/indexing)  
  → Moderne Ansätze (Column Store statt B-Tree)

- **Artikel: "When NOT to use an index"** – Stack Overflow  
  → Diskussion zu Edge Cases

- **YouTube: "Database Indexing Explained"** – Hussein Nasser  
  → Video-Tutorial (30 Min)

</div>

      {{2}}
<div>

    --{{2}}--
Tools für die Praxis

- **PGlite** – [https://pglite.dev](https://pglite.dev)  
  → PostgreSQL im Browser (was wir in dieser Session nutzen!)

- **DBeaver** – [https://dbeaver.io](https://dbeaver.io)  
  → Universeller Datenbank-Client (mit EXPLAIN-Visualisierung)

- **pgAdmin** – [https://www.pgadmin.org](https://www.pgadmin.org)  
  → PostgreSQL-spezifisch, gute Query-Analyse

- **EXPLAIN Visualizer** – [https://explain.dalibo.com](https://explain.dalibo.com)  
  → PostgreSQL EXPLAIN Plans visualisieren

</div>


    --{{3}}--
Das war Session 12! Sie haben jetzt die Werkzeuge, um jede PostgreSQL-Datenbank zu analysieren und zu optimieren – direkt im Browser mit PGlite. In der nächsten Session erweitern wir Ihr SQL-Arsenal mit Advanced Techniques – alles aufbauend auf dem, was Sie heute gelernt haben.

      {{3}}
{{|>}}
**Happy Optimizing mit PGlite! 🚀📊**
