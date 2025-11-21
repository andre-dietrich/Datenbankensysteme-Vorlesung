<!--
language: de
narrator: German Male

version:  1.0.0

author:   André Dietrich; GitHub Copilot
email:    LiaScript@web.de

comment:  Interaktiver SQL-Kurs mit Fokus auf praxisnahen Aufgaben, Live-Hands-on-Session und direkter Anwendung von SELECT-Statements in SQL. Studierende lernen, eigenständig Abfragen zu formulieren und Datenbankkonzepte praktisch umzusetzen.

logo:    ../assets/img/logo/7-lecture.jpg

import: https://raw.githubusercontent.com/LiaTemplates/DuckDB/refs/heads/main/README.md
-->

# Session 7 – SQL Introduction & SELECT Statements (Komplettlösung)

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (SQL-Praxis)

## Datenbank vorbereiten

    --{{0}}--
Bevor wir mit SQL-Abfragen starten, laden wir unsere Produktdatenbank. Wir nutzen die Products-Tabelle aus der CSV-Datei mit 418 Elektronikartikeln, Kleidung, Lebensmitteln und Büromaterial. Diese Daten sind unser Spielplatz für alle SELECT-Statements in dieser Session.

```sql
INSTALL httpfs;
LOAD httpfs;

CREATE TABLE Products AS
SELECT * FROM read_json('https://raw.githubusercontent.com/andre-dietrich/Datenbankensysteme-Vorlesung/refs/heads/main/assets/dat/products.json');
```
@DuckDB.eval(sql_intro)

---

__Falls das laden über URL nicht funktioniert, hier der Code zum manuellen Laden der Datei:__

``` js
const res  = await fetch('https://raw.githubusercontent.com/andre-dietrich/Datenbankensysteme-Vorlesung/refs/heads/main/assets/dat/products.json');
const text = await res.text();

// als "Datei" in DuckDB registrieren
await db.registerFileText('products.json', text);

// jetzt normal aus der "lokalen" Datei lesen
await conn.query(`CREATE TABLE Products AS SELECT * FROM read_json('products.json');`);

console.log("ready")
```
@DuckDB.js(sql_intro)


```sql
-- Kurzer Blick auf die Daten
SELECT * FROM Products LIMIT 5;
```
@DuckDB.eval(sql_intro)

---

## Was ist SQL?

    --{{0}}--
Bevor wir in die praktischen Abfragen eintauchen, klären wir die Grundlagen: Was ist SQL überhaupt? SQL steht für Structured Query Language – eine deklarative Sprache, mit der Sie Datenbanken abfragen und manipulieren. Entwickelt wurde SQL in den 1970er Jahren bei IBM für das System R-Projekt. Heute ist es der Standard für relationale Datenbanken weltweit, mit ANSI- und ISO-Standardisierung.

    {{0}}
<section>

**SQL = Structured Query Language**

- **Deklarativ:** Sie beschreiben **was** Sie wollen, nicht **wie** die Datenbank es holen soll
- **Standardisiert:** ANSI/ISO SQL – funktioniert auf MySQL, PostgreSQL, SQL Server, Oracle, SQLite, DuckDB
- **Mächtig:** Von einfachen Lookups (`SELECT * FROM ...`) bis zu komplexen Analysen mit Joins, Subqueries, Window Functions

**Entwickelt:** 1970er bei IBM (System R), erste kommerzielle Version: Oracle 1979

</section>

    --{{1}}--
SQL ist keine monolithische Sprache, sondern besteht aus mehreren Komponenten. Die wichtigsten vier sind: DDL für Schema-Definitionen, DML für Datenmanipulation, DCL für Zugriffsrechte und TCL für Transaktionen. In dieser Session fokussieren wir uns auf DML – genauer gesagt auf SELECT, die Königin der SQL-Befehle.

    {{1}}
<section>

### SQL-Komponenten

| Kategorie | Abkürzung | Zweck | Beispiele |
|-----------|-----------|-------|-----------|
| **Data Definition Language** | DDL | Schema erstellen/ändern | `CREATE`, `ALTER`, `DROP` |
| **Data Manipulation Language** | DML | Daten lesen/schreiben | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **Data Control Language** | DCL | Zugriffsrechte | `GRANT`, `REVOKE` |
| **Transaction Control Language** | TCL | Transaktionen | `COMMIT`, `ROLLBACK` |

**Heute fokus:** DML – speziell **SELECT**

</section>

    --{{2}}--
Warum sollten Sie SQL lernen? Erstens: SQL ist portabel. Ein SQL-Query läuft mit minimalen Anpassungen auf fast jedem relationalen Datenbanksystem. Zweitens: SQL ist deklarativ – Sie sagen „Gib mir alle Produkte unter 50 Euro", nicht „Öffne die Tabelle, iteriere über alle Zeilen, prüfe den Preis...". Die Datenbank kümmert sich um die Optimierung. Drittens: SQL ist omnipräsent. Egal ob Sie mit Webdaten, Analytics, IoT oder Machine Learning arbeiten – irgendwo ist SQL im Spiel.

    {{2}}
<section>

### Warum SQL?

✅ **Deklarativ:** Sie beschreiben das „Was", die Datenbank optimiert das „Wie"

```sql
-- Sie schreiben:
SELECT name, price FROM Products WHERE price < 50;

-- Die Datenbank entscheidet:
-- - Welchen Index nutzen?
-- - Table Scan oder Index Scan?
-- - Parallel execution?
```

✅ **Portabel:** SQL-Standard funktioniert auf vielen Systemen  
✅ **Mächtig:** Von einfachen Queries bis komplexe Analysen  
✅ **Verbreitet:** Fast jede Datenbank spricht SQL

</section>

---

## SELECT & FROM – Die Grundlagen

    --{{0}}--
Jede SQL-Abfrage beginnt mit SELECT und FROM. SELECT definiert, welche Spalten Sie sehen möchten. FROM sagt, aus welcher Tabelle die Daten kommen. Das ist das Fundament. Schauen wir uns die einfachste mögliche Abfrage an: SELECT * FROM Products – zeige mir alle Spalten aus der Products-Tabelle.

    {{0}}
<section>

### Die einfachste Query: SELECT *

**Syntax:**

```sql
SELECT * FROM Products;
```

- `SELECT *` = Alle Spalten
- `FROM Products` = Aus der Tabelle „Products"

**Live-Beispiel:**

```sql
SELECT * FROM Products LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
In der Praxis wollen Sie selten ALLE Spalten. Besser ist es, explizit die Spalten zu benennen, die Sie brauchen. Das macht Ihre Query schneller, lesbarer und weniger anfällig für Fehler, wenn sich das Schema ändert. Schauen wir uns an, wie Sie nur die Produkt-ID, den Namen und den Preis abrufen.

    {{1}}
<section>

### Spezifische Spalten auswählen

**Syntax:**

```sql
SELECT column1, column2, column3
FROM table_name;
```

**Beispiel:** Nur ID, Name und Preis

```sql
SELECT product_id, name, price
FROM Products
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Warum nicht immer `SELECT *`?**

- ❌ Langsamer (mehr Daten übertragen)
- ❌ Unlesbar (zu viele Spalten)
- ❌ Wartungsproblem (Schema ändert sich)

✅ **Best Practice:** Spalten explizit benennen

</section>

    --{{2}}--
Sie können Spalten auch umbenennen mit AS. Das ist nützlich für Lesbarkeit oder wenn Sie berechnete Spalten erstellen. Zum Beispiel: Zeigen Sie den Preis in Euro statt in der Original-Währung, oder geben Sie der Spalte einen aussagekräftigeren Namen.

    {{2}}
<section>

### Spalten umbenennen mit AS (Aliase)

**Syntax:**

```sql
SELECT column_name AS new_name
FROM table_name;
```

**Beispiel:**

```sql
SELECT 
  product_id AS id,
  name AS product_name,
  price AS price_eur,
  category
FROM Products
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Wann Aliase nutzen?**

- Berechnete Spalten: `price * 1.19 AS price_with_tax`
- Kurze Namen: `c.customer_name AS name`
- Lesbarkeit: `SUM(quantity) AS total_sold`

</section>

---

## WHERE – Daten filtern

    --{{0}}--
Die WHERE-Klausel ist Ihr Filter. Sie sagt der Datenbank: „Gib mir nur die Zeilen, die diese Bedingung erfüllen." Ohne WHERE bekommen Sie alle Zeilen. Mit WHERE filtern Sie auf genau das, was Sie brauchen. Beginnen wir mit einfachen Vergleichen: Alle Produkte, die weniger als 50 Euro kosten.

    {{0}}
<section>

### Grundlegende Filterung

**Syntax:**

```sql
SELECT columns
FROM table
WHERE condition;
```

**Beispiel:** Alle Produkte unter 50 Euro

```sql
SELECT product_id, name, price
FROM Products
WHERE price < 50
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
WHERE unterstützt alle Standard-Vergleichsoperatoren: gleich, ungleich, kleiner, größer, kleiner-gleich, größer-gleich. In SQL gibt es zwei Schreibweisen für „ungleich": `<>` (SQL-Standard) und `!=` (aus Programmiersprachen). Beide funktionieren in DuckDB, aber `<>` ist der offizielle Standard.

    {{1}}
<section>

### Vergleichsoperatoren

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `=` | Gleich | `price = 100` |
| `<>` oder `!=` | Ungleich | `category <> 'Electronics'` |
| `<` | Kleiner | `price < 50` |
| `>` | Größer | `stock > 100` |
| `<=` | Kleiner oder gleich | `rating <= 3.0` |
| `>=` | Größer oder gleich | `price >= 1000` |

**Beispiel: Produkte über 1000 Euro**

```sql
SELECT name, price, category
FROM Products
WHERE price >= 1000
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{2}}--
Sie können mehrere Bedingungen kombinieren mit AND und OR. AND bedeutet: Beide Bedingungen müssen erfüllt sein. OR bedeutet: Mindestens eine Bedingung muss erfüllt sein. Achten Sie auf Klammern, wenn Sie AND und OR mischen – die Priorität kann überraschend sein.

    {{2}}
<section>

### Logische Operatoren: AND, OR, NOT

**AND – Beide Bedingungen müssen wahr sein:**

```sql
SELECT name, price, category, stock
FROM Products
WHERE price < 100 AND stock > 200
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**OR – Mindestens eine Bedingung muss wahr sein:**

```sql
SELECT name, price, category
FROM Products
WHERE category = 'Electronics' OR category = 'Office'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**NOT – Negiert eine Bedingung:**

```sql
SELECT name, price, category
FROM Products
WHERE NOT category = 'Groceries'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**⚠️ Achtung bei gemischten Operatoren:**

```sql
-- Falsch (ohne Klammern):
WHERE category = 'Electronics' OR category = 'Office' AND price < 100
-- Bedeutet: (Electronics) ODER (Office UND price < 100)

-- Richtig (mit Klammern):
WHERE (category = 'Electronics' OR category = 'Office') AND price < 100
-- Bedeutet: (Electronics ODER Office) UND (price < 100)
```

</section>

    --{{3}}--
Für Bereichsabfragen gibt es BETWEEN. Das ist syntaktischer Zucker für „größer-gleich UND kleiner-gleich". Statt `price >= 100 AND price <= 500` schreiben Sie `price BETWEEN 100 AND 500`. Beides funktioniert, aber BETWEEN ist lesbarer.

    {{3}}
<section>

### BETWEEN – Bereichsabfragen

**Syntax:**

```sql
WHERE column BETWEEN value1 AND value2
```

Entspricht: `column >= value1 AND column <= value2`

**Beispiel: Produkte zwischen 100 und 500 Euro**

```sql
SELECT name, price, category
FROM Products
WHERE price BETWEEN 100 AND 500
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Datum-Bereiche:**

```sql
SELECT name, price, created_at
FROM Products
WHERE created_at BETWEEN '2025-01-01' AND '2025-06-30'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{4}}--
IN ist perfekt für Listen. Statt `category = 'Electronics' OR category = 'Office' OR category = 'Clothing'` schreiben Sie `category IN ('Electronics', 'Office', 'Clothing')`. Das ist kürzer und lesbarer.

    {{4}}
<section>

### IN – Listen-Abfragen

**Syntax:**

```sql
WHERE column IN (value1, value2, value3, ...)
```

**Beispiel: Nur bestimmte Kategorien**

```sql
SELECT name, price, category
FROM Products
WHERE category IN ('Electronics', 'Office', 'Groceries')
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Negation mit NOT IN:**

```sql
SELECT name, price, category
FROM Products
WHERE category NOT IN ('Clothing', 'Home & Kitchen')
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{5}}--
LIKE ist für Muster-Matching. Sie können nach Produkten suchen, deren Name mit „Laptop" beginnt, oder die „Pro" irgendwo im Namen haben. Der Prozent-Zeichen-Wildcard `%` steht für „beliebige Zeichen", der Unterstrich `_` für genau ein Zeichen.

    {{5}}
<section>

### LIKE – Pattern Matching

**Wildcards:**

- `%` = Beliebige Anzahl von Zeichen (0 oder mehr)
- `_` = Genau ein Zeichen

**Beispiel: Produkte, die „Laptop" im Namen haben**

```sql
SELECT name, price, category
FROM Products
WHERE name LIKE '%Laptop%'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Beispiel: Namen, die mit „Wireless" beginnen**

```sql
SELECT name, price, category
FROM Products
WHERE name LIKE 'Wireless%'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Beispiel: Produkt-IDs im Format „P00_01" (genau 6 Zeichen)**

```sql
SELECT product_id, name
FROM Products
WHERE product_id LIKE 'P00_01'
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**⚠️ Case Sensitivity:**

- DuckDB: LIKE ist standardmäßig **case-sensitive**
- Für case-insensitive: `ILIKE` (DuckDB, PostgreSQL)

```sql
SELECT name FROM Products WHERE name ILIKE '%laptop%' LIMIT 5;
```
@DuckDB.eval(sql_intro)

</section>

    --{{6}}--
NULL ist ein Spezialfall. NULL bedeutet „Wert unbekannt" oder „Wert fehlt". Sie können NULL nicht mit Gleichheit prüfen – `price = NULL` funktioniert nicht. Stattdessen müssen Sie `IS NULL` oder `IS NOT NULL` verwenden.

    {{6}}
<section>

### NULL-Werte behandeln

**NULL ist NICHT gleich 0 oder leerer String!**

NULL = „Wert unbekannt" oder „Wert fehlt"

**Falsch:**

```sql
-- Funktioniert NICHT:
WHERE rating = NULL
```

**Richtig:**

```sql
WHERE rating IS NULL
```

**Beispiel: Produkte ohne Rating**

```sql
SELECT name, price, rating
FROM Products
WHERE rating IS NULL
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Beispiel: Produkte MIT Rating**

```sql
SELECT name, price, rating
FROM Products
WHERE rating IS NOT NULL
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**⚠️ NULL in Vergleichen:**

- `NULL = NULL` → NULL (nicht TRUE!)
- `NULL > 5` → NULL
- `NULL AND TRUE` → NULL

</section>

---

## ORDER BY – Ergebnisse sortieren

    --{{0}}--
ORDER BY sortiert Ihre Ergebnisse. Standardmäßig aufsteigend (ASC = ascending), aber Sie können auch absteigend sortieren (DESC = descending). Sie können nach mehreren Spalten sortieren – zuerst nach Kategorie, dann nach Preis zum Beispiel.

    {{0}}
<section>

### Grundlegende Sortierung

**Syntax:**

```sql
SELECT columns
FROM table
ORDER BY column [ASC|DESC];
```

- **ASC** = Ascending (aufsteigend) – Standard
- **DESC** = Descending (absteigend)

**Beispiel: Produkte nach Preis sortiert (günstigste zuerst)**

```sql
SELECT name, price, category
FROM Products
ORDER BY price ASC
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Beispiel: Teuerste Produkte zuerst**

```sql
SELECT name, price, category
FROM Products
ORDER BY price DESC
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
Sie können nach mehreren Spalten sortieren. Die Reihenfolge ist wichtig: Erst wird nach der ersten Spalte sortiert, dann innerhalb gleicher Werte nach der zweiten Spalte, und so weiter. Hier sortieren wir erst nach Kategorie, dann innerhalb jeder Kategorie nach Preis.

    {{1}}
<section>

### Nach mehreren Spalten sortieren

**Syntax:**

```sql
ORDER BY column1 [ASC|DESC], column2 [ASC|DESC], ...
```

**Beispiel: Erst nach Kategorie, dann nach Preis**

```sql
SELECT category, name, price
FROM Products
ORDER BY category ASC, price DESC
LIMIT 20;
```
@DuckDB.eval(sql_intro)

**Wie funktioniert das?**

1. Alle Zeilen werden nach `category` sortiert (alphabetisch)
2. Innerhalb jeder Kategorie werden die Zeilen nach `price` sortiert (teuerste zuerst)

</section>

    --{{2}}--
NULL-Werte sind ein Spezialfall bei der Sortierung. Standardmäßig kommen NULLs in DuckDB am Ende (bei ASC) oder am Anfang (bei DESC). Sie können das mit NULLS FIRST oder NULLS LAST explizit steuern.

    {{2}}
<section>

### NULL-Werte in ORDER BY

**Standard-Verhalten:**

- **ASC:** NULLs kommen am Ende
- **DESC:** NULLs kommen am Anfang

**Explizite Steuerung:**

```sql
ORDER BY column NULLS FIRST  -- NULLs zuerst
ORDER BY column NULLS LAST   -- NULLs zuletzt
```

**Beispiel: Produkte nach Rating sortiert, NULLs am Ende**

```sql
SELECT name, price, rating
FROM Products
ORDER BY rating DESC NULLS LAST
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

---

## DISTINCT – Duplikate eliminieren

    --{{0}}--
DISTINCT entfernt Duplikate aus Ihren Ergebnissen. Wenn Sie wissen wollen, welche Kategorien es gibt, ohne Wiederholungen, nutzen Sie `SELECT DISTINCT category`. Das gibt Ihnen eine Liste eindeutiger Werte.

    {{0}}
<section>

### Eindeutige Werte abrufen

**Syntax:**

```sql
SELECT DISTINCT column
FROM table;
```

**Beispiel: Alle Kategorien (ohne Duplikate)**

```sql
SELECT DISTINCT category
FROM Products
ORDER BY category;
```
@DuckDB.eval(sql_intro)

**Beispiel: Alle Brands**

```sql
SELECT DISTINCT brand
FROM Products
ORDER BY brand;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
DISTINCT arbeitet über ALLE ausgewählten Spalten. Wenn Sie mehrere Spalten angeben, bekommt Sie jede eindeutige Kombination. Das ist wichtig zu verstehen: `SELECT DISTINCT category, brand` gibt Ihnen jede Kombination von Kategorie und Marke, die vorkommt.

    {{1}}
<section>

### DISTINCT über mehrere Spalten

**DISTINCT gilt für die gesamte Zeile:**

```sql
SELECT DISTINCT column1, column2
FROM table;
```

Gibt jede **eindeutige Kombination** von column1 + column2

**Beispiel: Alle Kategorie-Brand-Kombinationen**

```sql
SELECT DISTINCT category, brand
FROM Products
ORDER BY category, brand;
```
@DuckDB.eval(sql_intro)

**Wie viele eindeutige Kombinationen gibt es?**

```sql
SELECT COUNT(DISTINCT category || '-' || brand) AS unique_combinations
FROM Products;
```
@DuckDB.eval(sql_intro)

</section>

    --{{2}}--
DISTINCT vs. GROUP BY: Beides kann Duplikate entfernen, aber GROUP BY ist mächtiger. Mit GROUP BY können Sie aggregieren – zählen, summieren, Durchschnitt berechnen. DISTINCT gibt nur eindeutige Werte zurück, ohne Aggregation. Wir schauen uns GROUP BY im nächsten Abschnitt an.

    {{2}}
<section>

### DISTINCT vs. GROUP BY

**DISTINCT:**

- Entfernt Duplikate
- Keine Aggregation
- Einfacher, schneller für simple Fälle

```sql
SELECT DISTINCT category FROM Products;
```

**GROUP BY:**

- Gruppiert Zeilen
- Ermöglicht Aggregation (COUNT, SUM, AVG, ...)
- Mächtiger, flexibler

```sql
SELECT category, COUNT(*) AS count
FROM Products
GROUP BY category;
```
@DuckDB.eval(sql_intro)

**Wann was nutzen?**

- **DISTINCT:** Nur eindeutige Werte, keine Statistiken
- **GROUP BY:** Gruppierung + Aggregation

</section>

---

## GROUP BY & HAVING – Aggregation

    --{{0}}--
GROUP BY ist eine der mächtigsten Funktionen in SQL. Es gruppiert Zeilen mit gleichen Werten und ermöglicht Aggregation: Zählen Sie, wie viele Produkte es pro Kategorie gibt. Berechnen Sie den durchschnittlichen Preis pro Marke. Finden Sie die teuerste Ware pro Kategorie. All das geht mit GROUP BY.

    {{0}}
<section>

### Grundlagen von GROUP BY

**Syntax:**

```sql
SELECT column, AGGREGATE_FUNCTION(column)
FROM table
GROUP BY column;
```

**Aggregat-Funktionen:**

- `COUNT(*)` – Anzahl Zeilen
- `SUM(column)` – Summe
- `AVG(column)` – Durchschnitt
- `MIN(column)` – Minimum
- `MAX(column)` – Maximum

**Beispiel: Anzahl Produkte pro Kategorie**

```sql
SELECT category, COUNT(*) AS product_count
FROM Products
GROUP BY category
ORDER BY product_count DESC;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
Sie können mehrere Aggregat-Funktionen gleichzeitig nutzen. Zum Beispiel: Für jede Kategorie zählen Sie die Produkte, berechnen den Durchschnittspreis, finden den günstigsten und teuersten Artikel. Das alles in einer Query.

    {{1}}
<section>

### Mehrere Aggregate gleichzeitig

**Beispiel: Statistiken pro Kategorie**

```sql
SELECT 
  category,
  COUNT(*) AS total_products,
  AVG(price) AS avg_price,
  MIN(price) AS cheapest,
  MAX(price) AS most_expensive,
  SUM(stock) AS total_stock
FROM Products
GROUP BY category
ORDER BY total_products DESC;
```
@DuckDB.eval(sql_intro)

**Runden für Lesbarkeit:**

```sql
SELECT 
  category,
  COUNT(*) AS count,
  ROUND(AVG(price), 2) AS avg_price,
  ROUND(MIN(price), 2) AS min_price,
  ROUND(MAX(price), 2) AS max_price
FROM Products
GROUP BY category;
```
@DuckDB.eval(sql_intro)

</section>

    --{{2}}--
Nach mehreren Spalten gruppieren ist möglich. Zum Beispiel: Gruppieren Sie nach Kategorie UND Marke. Das gibt Ihnen Statistiken für jede Kombination – wie viele Laptops hat jede Marke, wie viele Handys, und so weiter.

    {{2}}
<section>



### Nach mehreren Spalten gruppieren

**Syntax:**

```sql
GROUP BY column1, column2, ...
```

**Beispiel: Statistiken pro Kategorie und Brand**

```sql
SELECT 
  category,
  brand,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS avg_price
FROM Products
GROUP BY category, brand
ORDER BY category, products DESC
LIMIT 20;
```
@DuckDB.eval(sql_intro)

</section>

    --{{3}}--
HAVING ist wie WHERE, aber für gruppierte Daten. WHERE filtert VOR dem Gruppieren, HAVING filtert NACH dem Gruppieren. Sie können sagen: „Zeige mir nur Kategorien mit mehr als 50 Produkten" oder „Brands mit einem Durchschnittspreis über 200 Euro".

    {{3}}
<section>

### HAVING – Gruppen filtern

**WHERE vs. HAVING:**

- **WHERE:** Filtert **Zeilen** vor dem Gruppieren
- **HAVING:** Filtert **Gruppen** nach dem Gruppieren

**Syntax:**

```sql
SELECT column, AGGREGATE_FUNCTION(column)
FROM table
WHERE condition          -- Filter VORHER
GROUP BY column
HAVING condition;        -- Filter NACHHER
```

**Beispiel: Nur Kategorien mit mehr als 50 Produkten**

```sql
SELECT 
  category,
  COUNT(*) AS product_count,
  ROUND(AVG(price), 2) AS avg_price
FROM Products
GROUP BY category
HAVING COUNT(*) > 50
ORDER BY product_count DESC;
```
@DuckDB.eval(sql_intro)

**Beispiel: Brands mit Durchschnittspreis über 200€**

```sql
SELECT 
  brand,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS avg_price
FROM Products
GROUP BY brand
HAVING AVG(price) > 200
ORDER BY avg_price DESC;
```
@DuckDB.eval(sql_intro)

</section>

    --{{4}}--
Komplexes Beispiel: Kombinieren Sie WHERE und HAVING. Filtern Sie erst die Zeilen (nur Electronics), dann gruppieren Sie (pro Brand), dann filtern Sie die Gruppen (nur Brands mit mehr als 5 Produkten). Das ist die Macht von SQL: Deklarativ beschreiben, was Sie wollen, und die Datenbank optimiert die Ausführung.

    {{4}}
<section>

### WHERE + GROUP BY + HAVING kombiniert

**Beispiel: Electronics-Brands mit mehr als 5 Produkten**

```sql
SELECT 
  brand,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS avg_price,
  ROUND(MIN(price), 2) AS min_price,
  ROUND(MAX(price), 2) AS max_price
FROM Products
WHERE category = 'Electronics'    -- Filter VORHER
GROUP BY brand
HAVING COUNT(*) > 5               -- Filter NACHHER
ORDER BY products DESC;
```
@DuckDB.eval(sql_intro)

**Ausführungsreihenfolge:**

1. `WHERE`: Nur Electronics
2. `GROUP BY`: Gruppiere nach Brand
3. `HAVING`: Nur Gruppen mit > 5 Produkten
4. `SELECT`: Berechne Aggregate
5. `ORDER BY`: Sortiere nach Anzahl

</section>


## LIMIT – Top-N Queries

    --{{0}}--
LIMIT begrenzt die Anzahl der zurückgegebenen Zeilen. Das ist perfekt für „Top 10"-Abfragen oder für Paginierung. Sie können auch einen Offset angeben: „Überspringe die ersten 20 Zeilen, dann gib mir die nächsten 10." Das ist die Grundlage für Seitennummerierung in Webanwendungen.

    {{0}}
<section>

### Anzahl Ergebnisse begrenzen

**Syntax:**

```sql
SELECT columns
FROM table
LIMIT n;
```

**Beispiel: Die 10 teuersten Produkte**

```sql
SELECT name, price, category
FROM Products
ORDER BY price DESC
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Beispiel: Die 10 günstigsten Produkte**

```sql
SELECT name, price, category
FROM Products
WHERE price > 0
ORDER BY price ASC
LIMIT 10;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
Mit OFFSET können Sie Zeilen überspringen. Das ist die Basis für Paginierung: Seite 1 = LIMIT 10 OFFSET 0, Seite 2 = LIMIT 10 OFFSET 10, Seite 3 = LIMIT 10 OFFSET 20, und so weiter. Aber Achtung: OFFSET kann bei großen Werten langsam werden, weil die Datenbank alle übersprungenen Zeilen trotzdem verarbeiten muss.

    {{1}}
<section>

### OFFSET – Zeilen überspringen (Paginierung)

**Syntax:**

```sql
SELECT columns
FROM table
LIMIT n OFFSET m;
```

- `LIMIT n`: Maximal n Zeilen
- `OFFSET m`: Überspringe m Zeilen

**Beispiel: Paginierung (Seite 2, 10 pro Seite)**

```sql
SELECT name, price, category
FROM Products
ORDER BY name
LIMIT 10 OFFSET 10;  -- Zeilen 11-20
```
@DuckDB.eval(sql_intro)

**Seite 3:**

```sql
SELECT name, price, category
FROM Products
ORDER BY name
LIMIT 10 OFFSET 20;  -- Zeilen 21-30
```
@DuckDB.eval(sql_intro)

**⚠️ Performance-Problem bei großem OFFSET:**

- `OFFSET 10000` → Datenbank muss 10.000 Zeilen überspringen
- Besser: Cursor-basierte Paginierung (mit WHERE + ID)

</section>

    --{{2}}--
Alternative zu OFFSET: Cursor-basierte Paginierung. Statt „überspringe 1000 Zeilen" sagen Sie „gib mir alle Produkte mit ID größer als 1000". Das ist viel schneller, weil die Datenbank direkt zum richtigen Startpunkt springen kann.

    {{2}}
<section>

### Cursor-basierte Paginierung (Alternative zu OFFSET)

**Problem mit OFFSET:**

```sql
-- Langsam bei großen Werten:
SELECT * FROM Products ORDER BY product_id LIMIT 10 OFFSET 10000;
```

**Besser: WHERE + Cursor:**

```sql
-- Seite 1:
SELECT product_id, name, price
FROM Products
ORDER BY product_id
LIMIT 10;
-- Merke letzte ID: z.B. P00010

-- Seite 2:
SELECT product_id, name, price
FROM Products
WHERE product_id > 'P00010'
ORDER BY product_id
LIMIT 10;
```
@DuckDB.eval(sql_intro)

**Vorteile:**

- ✅ Schneller (kein Überspringen)
- ✅ Stabil bei Änderungen

**Nachteil:**

- ❌ Komplizierter Code
- ❌ Keine direkten Seitensprünge (Seite 5 → Seite 100)

</section>

---

## Query Order & Execution

    --{{0}}--
Jetzt wird es interessant: Die Reihenfolge, in der Sie SQL schreiben, ist NICHT die Reihenfolge, in der die Datenbank es ausführt. Sie schreiben SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT. Aber intern arbeitet die Datenbank in einer anderen Reihenfolge: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT. Das zu verstehen ist wichtig für Performance und Fehlersuche.

    {{0}}
<section>

### Logische vs. Physische Ausführungsreihenfolge

**Wie Sie es schreiben (logische Reihenfolge):**

```sql
SELECT column, COUNT(*)       -- 5
FROM table                    -- 1
WHERE condition               -- 2
GROUP BY column               -- 3
HAVING condition              -- 4
ORDER BY column               -- 6
LIMIT n;                      -- 7
```

**Wie die Datenbank es ausführt (physische Reihenfolge):**

1. **FROM:** Tabelle laden
2. **WHERE:** Zeilen filtern
3. **GROUP BY:** Gruppieren
4. **HAVING:** Gruppen filtern
5. **SELECT:** Spalten berechnen
6. **ORDER BY:** Sortieren
7. **LIMIT:** Anzahl begrenzen

</section>

    --{{1}}--
Warum ist das wichtig? Erstens: Aliase aus SELECT sind in WHERE nicht verfügbar, weil WHERE VOR SELECT ausgeführt wird. Zweitens: HAVING kann Aliase nutzen, weil es NACH SELECT kommt. Drittens: ORDER BY kann Aliase nutzen. Das erklärt viele Fehler, die Anfänger machen.

    {{1}}
<section>

### Warum ist die Reihenfolge wichtig?

**Beispiel-Query:**

```sql
SELECT 
  category,
  COUNT(*) AS product_count,
  AVG(price) AS avg_price
FROM Products
WHERE price > 100            -- Alias "avg_price" NICHT verfügbar
GROUP BY category
HAVING avg_price > 500       -- Alias "avg_price" verfügbar (nach SELECT)
ORDER BY product_count DESC; -- Alias "product_count" verfügbar
```

**Warum?**

- **WHERE** wird VOR **SELECT** ausgeführt → Aliase nicht verfügbar
- **HAVING** wird NACH **SELECT** ausgeführt → Aliase verfügbar
- **ORDER BY** wird NACH **SELECT** ausgeführt → Aliase verfügbar

**Häufiger Fehler:**

```sql
-- FEHLER:
SELECT name, price * 1.19 AS price_with_tax
FROM Products
WHERE price_with_tax > 100;   -- Alias nicht verfügbar!

-- RICHTIG:
SELECT name, price * 1.19 AS price_with_tax
FROM Products
WHERE price * 1.19 > 100;     -- Berechnung wiederholen
```

</section>

    --{{2}}--
Visualisieren wir das: FROM holt die Tabelle. WHERE reduziert die Zeilen. GROUP BY gruppiert. HAVING reduziert die Gruppen. SELECT berechnet die finalen Spalten. ORDER BY sortiert. LIMIT schneidet ab. Jeder Schritt arbeitet auf dem Ergebnis des vorherigen Schritts. Das ist die Pipeline.

    {{2}}
<section>

### Query-Ausführung visualisiert

```ascii
     FROM Products
          ↓
    418 Zeilen geladen
          ↓
     WHERE price > 100
          ↓
    ~200 Zeilen übrig
          ↓
     GROUP BY category
          ↓
    4 Gruppen (Electronics, Clothing, Groceries, Office)
          ↓
     HAVING COUNT(*) > 50
          ↓
    2 Gruppen übrig
          ↓
     SELECT category, COUNT(*), AVG(price)
          ↓
    2 Zeilen mit Aggregaten
          ↓
     ORDER BY COUNT(*) DESC
          ↓
    2 Zeilen sortiert
          ↓
     LIMIT 1
          ↓
    1 Zeile final
```

**Beispiel-Query:**

```sql
SELECT 
  category,
  COUNT(*) AS count,
  ROUND(AVG(price), 2) AS avg_price
FROM Products
WHERE price > 100
GROUP BY category
HAVING COUNT(*) > 50
ORDER BY count DESC
LIMIT 1;
```
@DuckDB.eval(sql_intro)

</section>

---

## Zusammenfassung & Best Practices

    --{{0}}--
Fassen wir zusammen: SELECT ist die Königin von SQL. Sie haben gelernt, Spalten auszuwählen, Daten zu filtern, zu sortieren, Duplikate zu entfernen, zu gruppieren und zu aggregieren. Sie verstehen die Ausführungsreihenfolge und wissen, warum Aliase manchmal funktionieren und manchmal nicht. Das ist Ihr Fundament für alle weiteren SQL-Sessions.

    {{0}}
<section>

### Was haben wir gelernt?

| Konzept      | Zweck               | Syntax-Beispiel                    |
| ------------ | ------------------- | ---------------------------------- |
| **SELECT**   | Spalten auswählen   | `SELECT name, price FROM Products` |
| **FROM**     | Tabelle angeben     | `FROM Products`                    |
| **WHERE**    | Zeilen filtern      | `WHERE price > 100`                |
| **ORDER BY** | Sortieren           | `ORDER BY price DESC`              |
| **DISTINCT** | Duplikate entfernen | `SELECT DISTINCT category`         |
| **GROUP BY** | Gruppieren          | `GROUP BY category`                |
| **HAVING**   | Gruppen filtern     | `HAVING COUNT(*) > 10`             |
| **LIMIT**    | Anzahl begrenzen    | `LIMIT 10`                         |
| **OFFSET**   | Zeilen überspringen | `OFFSET 20`                        |

</section>

    --{{1}}--
Best Practices: Erstens – Spalten explizit benennen, nicht SELECT *. Zweitens – Aliase nutzen für Lesbarkeit. Drittens – WHERE für Zeilen-Filter, HAVING für Gruppen-Filter. Viertens – LIMIT für Top-N, aber Cursor für Paginierung. Fünftens – Ausführungsreihenfolge verstehen.

    {{1}}
<section>

### Best Practices

✅ **Spalten explizit benennen**

```sql
-- Gut:
SELECT product_id, name, price FROM Products;

-- Schlecht (außer für Exploration):
SELECT * FROM Products;
```

✅ **Aliase für Lesbarkeit**

```sql
SELECT 
  product_id AS id,
  name AS product_name,
  price * 1.19 AS price_with_tax
FROM Products;
```

✅ **WHERE für Zeilen, HAVING für Gruppen**

```sql
-- Zeilen filtern:
WHERE price > 100

-- Gruppen filtern:
HAVING COUNT(*) > 10
```

✅ **LIMIT für Top-N, Cursor für große Offsets**

```sql
-- Top 10: OK
LIMIT 10

-- Seite 1000: Besser mit WHERE + ID
WHERE id > 'last_seen_id' LIMIT 10
```

✅ **Ausführungsreihenfolge verstehen**

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

</section>


## Quiz: Testen Sie Ihr Wissen

    --{{0}}--
Zeit für einen Selbsttest! Probieren Sie diese Fragen, um Ihr Verständnis zu überprüfen.

**Frage 1: Welche Query zeigt die 5 teuersten Electronics-Produkte?**

- [( )] `SELECT * FROM Products WHERE category = 'Electronics' LIMIT 5`
- [(X)] `SELECT name, price FROM Products WHERE category = 'Electronics' ORDER BY price DESC LIMIT 5`
- [( )] `SELECT name, price FROM Products ORDER BY price LIMIT 5`
- [( )] `SELECT DISTINCT name FROM Products WHERE category = 'Electronics'`

**Frage 2: Was ist der Unterschied zwischen WHERE und HAVING?**

- [( )] Beide machen das Gleiche
- [(X)] WHERE filtert Zeilen vor dem Gruppieren, HAVING filtert Gruppen nach dem Gruppieren
- [( )] WHERE ist schneller als HAVING
- [( )] HAVING kann nur mit COUNT() genutzt werden

**Frage 3: In welcher Reihenfolge wird diese Query ausgeführt?**

```sql
SELECT category, COUNT(*)
FROM Products
WHERE price > 100
GROUP BY category
ORDER BY COUNT(*) DESC;
```

- [( )] SELECT → FROM → WHERE → GROUP BY → ORDER BY
- [(X)] FROM → WHERE → GROUP BY → SELECT → ORDER BY
- [( )] FROM → SELECT → WHERE → GROUP BY → ORDER BY
- [( )] FROM → GROUP BY → WHERE → SELECT → ORDER BY

**Frage 4: Wie filtern Sie auf NULL-Werte?**

- [( )] `WHERE column = NULL`
- [( )] `WHERE column == NULL`
- [(X)] `WHERE column IS NULL`
- [( )] `WHERE ISNULL(column)`

**Frage 5: Was macht DISTINCT?**

- [(X)] Entfernt Duplikate aus den Ergebnissen
- [( )] Sortiert die Ergebnisse
- [( )] Gruppiert die Ergebnisse
- [( )] Begrenzt die Anzahl der Ergebnisse

---

## Übungsaufgaben

    --{{0}}--
Probieren Sie diese Übungen selbst aus. Nutzen Sie die Products-Tabelle und experimentieren Sie mit verschiedenen Kombinationen.

**Aufgabe 1: Grundlagen**

Schreiben Sie eine Query, die alle Produkte der Kategorie "Clothing" zeigt, sortiert nach Preis (günstigste zuerst), nur die ersten 10.

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    SELECT name, price, brand
    FROM Products
    WHERE category = 'Clothing'
    ORDER BY price ASC
    LIMIT 10;
    ```
    @DuckDB.eval(sql_intro)
    
    *******************

**Aufgabe 2: Aggregation**

Berechnen Sie für jede Kategorie die Anzahl Produkte, den Durchschnittspreis und den Gesamtbestand. Sortieren Sie nach Anzahl Produkte (größte zuerst).

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    SELECT 
      category,
      COUNT(*) AS product_count,
      ROUND(AVG(price), 2) AS avg_price,
      SUM(stock) AS total_stock
    FROM Products
    GROUP BY category
    ORDER BY product_count DESC;
    ```
    @DuckDB.eval(sql_intro)
    
    *******************

**Aufgabe 3: Filterung mit HAVING**

Zeigen Sie alle Brands, die mehr als 20 Produkte haben UND deren Durchschnittspreis über 100 Euro liegt.

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    SELECT 
      brand,
      COUNT(*) AS products,
      ROUND(AVG(price), 2) AS avg_price
    FROM Products
    GROUP BY brand
    HAVING COUNT(*) > 20 AND AVG(price) > 100
    ORDER BY products DESC;
    ```
    @DuckDB.eval(sql_intro)
    
    *******************

**Aufgabe 4: Komplexe Filterung**

Finden Sie alle Electronics-Produkte, deren Name "Pro" oder "Max" enthält, mit einem Rating über 4.0, sortiert nach Rating (beste zuerst).

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    SELECT name, price, rating, brand
    FROM Products
    WHERE category = 'Electronics'
      AND (name LIKE '%Pro%' OR name LIKE '%Max%')
      AND rating > 4.0
    ORDER BY rating DESC
    LIMIT 20;
    ```
    @DuckDB.eval(sql_intro)
    
    *******************

---

## Ausblick: Was kommt als Nächstes?

    --{{0}}--
Sie haben jetzt die Grundlagen von SELECT gemeistert. In den nächsten Sessions gehen wir tiefer: Joins (mehrere Tabellen kombinieren), Subqueries (Queries in Queries), Window Functions (erweiterte Analysen), und vieles mehr. Aber alles baut auf dem auf, was Sie heute gelernt haben. SELECT ist Ihr Fundament.

**Kommende Sessions:**

- **Session 8:** Data Definition (CREATE, ALTER, DROP)
- **Session 9:** Data Manipulation (INSERT, UPDATE, DELETE)
- **Session 10:** Joins – Tabellen kombinieren
- **Session 11:** Subqueries & CTEs
- **Session 12:** Window Functions
- **Session 13:** Performance & Indexierung


🎉 **Herzlichen Glückwunsch!** Sie sind jetzt bereit, SQL-Abfragen zu schreiben!


## DuckDB Aggregat-Funktionen Übersicht

    --{{0}}--
DuckDB bietet eine reiche Palette an Aggregatfunktionen – weit mehr als nur COUNT und SUM. Schauen wir uns die wichtigsten Kategorien an: Statistische Funktionen, String-Aggregate, logische Aggregate und approximative Funktionen. Jede hat ihren Einsatzzweck.

    {{0}}
<section>

#### Standard-Aggregatfunktionen

Diese Funktionen kennen Sie bereits – sie sind das Fundament jeder Datenanalyse:

| Funktion        | Beschreibung            | NULL-Verhalten  | Beispiel        |
| --------------- | ----------------------- | --------------- | --------------- |
| `COUNT(*)`      | Anzahl aller Zeilen     | Zählt auch NULL | `COUNT(*)`      |
| `COUNT(column)` | Anzahl nicht-NULL-Werte | Ignoriert NULL  | `COUNT(rating)` |
| `SUM(column)`   | Summe aller Werte       | Ignoriert NULL  | `SUM(stock)`    |
| `AVG(column)`   | Durchschnitt            | Ignoriert NULL  | `AVG(price)`    |
| `MIN(column)`   | Kleinster Wert          | Ignoriert NULL  | `MIN(price)`    |
| `MAX(column)`   | Größter Wert            | Ignoriert NULL  | `MAX(price)`    |

**Beispiel: Alle auf einmal**

```sql
SELECT 
  COUNT(*) AS total_products,
  COUNT(rating) AS rated_products,
  ROUND(AVG(price), 2) AS avg_price,
  MIN(price) AS cheapest,
  MAX(price) AS most_expensive,
  SUM(stock) AS total_inventory
FROM Products;
```
@DuckDB.eval(sql_intro)

</section>

    --{{1}}--
Statistische Funktionen gehen über einfache Durchschnitte hinaus. Varianz und Standardabweichung zeigen, wie stark Ihre Daten streuen. Median ist robuster gegen Ausreißer als der Durchschnitt. Wenn ein einziges Produkt 10.000 Euro kostet, verschiebt das den Durchschnitt massiv – aber nicht den Median.

    {{1}}
<section>

#### Statistische Funktionen

Diese Funktionen helfen bei tieferer Datenanalyse – Streuung, Median, Quantile:

| Funktion | Beschreibung | Wann nutzen? |
|----------|--------------|--------------|
| `STDDEV(column)` | Standardabweichung (Sample) | Streuung messen |
| `STDDEV_POP(column)` | Standardabweichung (Population) | Gesamtpopulation |
| `VARIANCE(column)` | Varianz (Sample) | Streuung² |
| `VAR_POP(column)` | Varianz (Population) | Gesamtpopulation |
| `MEDIAN(column)` | Median (50. Perzentil) | Robuster Mittelwert |
| `QUANTILE(column, 0.25)` | Beliebiges Quantil | Quartile, Dezile |

**Beispiel: Preisverteilung analysieren**

```sql
SELECT 
  category,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS mean_price,
  ROUND(MEDIAN(price), 2) AS median_price,
  ROUND(STDDEV(price), 2) AS price_stddev,
  ROUND(QUANTILE(price, 0.25), 2) AS q1_price,
  ROUND(QUANTILE(price, 0.75), 2) AS q3_price
FROM Products
GROUP BY category
ORDER BY products DESC;
```
@DuckDB.eval(sql_intro)

**Was sagt uns das?**

- **Mean vs. Median:** Große Differenz → Ausreißer vorhanden
- **Standardabweichung:** Hoch → große Preisspanne
- **Q1/Q3:** Interquartilsbereich = mittlere 50% der Daten

</section>

    --{{2}}--
String-Aggregate sind mächtig, wenn Sie Werte zusammenfassen wollen. STRING_AGG sammelt alle Werte einer Gruppe in einen einzigen String – perfekt für „zeige mir alle Brands pro Kategorie" oder „liste alle Produktnamen in einer Zeile". LIST/ARRAY_AGG erstellt Arrays, die Sie später weiterverarbeiten können.

    {{2}}
<section>

#### String- und Listen-Aggregate

Diese Funktionen sammeln Werte in Strings oder Arrays:

| Funktion | Beschreibung | Ausgabe | Beispiel |
|----------|--------------|---------|----------|
| `STRING_AGG(column, separator)` | Konkateniert Strings mit Trennzeichen | String | `STRING_AGG(name, ', ')` |
| `LIST(column)` | Sammelt Werte in Array | Array | `LIST(brand)` |
| `ARRAY_AGG(column)` | Alias für LIST | Array | `ARRAY_AGG(price)` |

**Beispiel: Alle Brands pro Kategorie**

```sql
SELECT 
  category,
  COUNT(DISTINCT brand) AS brand_count,
  STRING_AGG(DISTINCT brand, ', ' ORDER BY brand) AS brands
FROM Products
GROUP BY category
ORDER BY brand_count DESC;
```
@DuckDB.eval(sql_intro)

**Beispiel: Preis-Arrays für Analyse**

```sql
SELECT 
  category,
  LIST(price ORDER BY price) AS all_prices,
  LIST(price ORDER BY price DESC LIMIT 5) AS top_5_prices
FROM Products
GROUP BY category;
```
@DuckDB.eval(sql_intro)

**💡 Tipp:** `STRING_AGG` kann mit `ORDER BY` innerhalb der Funktion sortieren!

</section>

    --{{3}}--
Logische Aggregate sind unterschätzt, aber extrem nützlich. BOOL_AND prüft: „Sind ALLE Werte in der Gruppe wahr?" BOOL_OR prüft: „Ist MINDESTENS einer wahr?" Das ist perfekt für Validierung: „Hat jede Kategorie mindestens ein Produkt auf Lager?" oder „Sind alle Produkte bewertet?"

    {{3}}
<section>

#### Logische Aggregate

Perfekt für Validierung und Bedingungsprüfungen:

| Funktion | Beschreibung | Gibt TRUE wenn... |
|----------|--------------|-------------------|
| `BOOL_AND(condition)` | Logisches AND über alle Zeilen | ALLE Zeilen TRUE sind |
| `BOOL_OR(condition)` | Logisches OR über alle Zeilen | MINDESTENS eine Zeile TRUE ist |
| `EVERY(condition)` | Alias für BOOL_AND | ALLE Zeilen TRUE sind |

**Beispiel: Validierung pro Kategorie**

```sql
SELECT 
  category,
  COUNT(*) AS products,
  BOOL_AND(stock > 0) AS all_in_stock,
  BOOL_OR(stock > 100) AS some_high_stock,
  BOOL_AND(rating IS NOT NULL) AS all_rated,
  BOOL_OR(price > 1000) AS has_premium_items
FROM Products
GROUP BY category;
```
@DuckDB.eval(sql_intro)

**Interpretation:**

- `all_in_stock = TRUE` → Alle Produkte verfügbar
- `some_high_stock = TRUE` → Mindestens ein Produkt mit hohem Bestand
- `all_rated = FALSE` → Nicht alle Produkte haben Bewertungen

</section>

    --{{4}}--
Approximative Funktionen sind die Geheimwaffe für Big Data. APPROX_COUNT_DISTINCT zählt eindeutige Werte, aber nicht exakt – dafür viel schneller und speicherschonender. Bei Millionen von Zeilen ist der Unterschied zwischen „exakt 10.234.567" und „circa 10.2 Millionen" oft irrelevant. Sie gewinnen massive Performance für minimalen Genauigkeitsverlust.

    {{4}}
<section>

#### Approximative Aggregate (Performance)

Für große Datenmengen – schneller, aber mit kleinem Fehler:

| Funktion | Beschreibung | Genauigkeit | Wann nutzen? |
|----------|--------------|-------------|--------------|
| `APPROX_COUNT_DISTINCT(column)` | Ungefähre Anzahl eindeutiger Werte | ~2% Fehler | Millionen von Zeilen |
| `APPROX_QUANTILE(column, 0.5)` | Approximatives Quantil | ~1% Fehler | Große Datasets |

**Beispiel: Exakt vs. Approximativ**

```sql
SELECT 
  'Exact' AS method,
  COUNT(DISTINCT product_id) AS unique_products,
  COUNT(DISTINCT brand) AS unique_brands
FROM Products

UNION ALL

SELECT 
  'Approx' AS method,
  APPROX_COUNT_DISTINCT(product_id) AS unique_products,
  APPROX_COUNT_DISTINCT(brand) AS unique_brands
FROM Products;
```
@DuckDB.eval(sql_intro)

**💡 Performance-Tipp:**

- Bei < 1 Million Zeilen: Exakte Funktionen nutzen
- Bei > 10 Millionen Zeilen: Approximativ kann 10x schneller sein
- Bei 418 Zeilen (unsere Products): Kein Unterschied 😊

</section>

    --{{5}}--
Fortgeschrittene Aggregate: FIRST und LAST holen den ersten oder letzten Wert in einer Gruppe – nützlich für Zeitreihen. BIT_AND/BIT_OR/BIT_XOR sind für Bit-Operationen. Und dann gibt es noch spezielle Aggregate wie MODE (häufigster Wert) und ARG_MIN/ARG_MAX (Wert einer anderen Spalte bei Min/Max).

    {{5}}
<section>

#### Fortgeschrittene Aggregate

Spezialisierte Funktionen für besondere Anwendungsfälle:

| Funktion | Beschreibung | Beispiel |
|----------|--------------|----------|
| `FIRST(column)` | Erster Wert in Gruppe | `FIRST(name ORDER BY price)` |
| `LAST(column)` | Letzter Wert in Gruppe | `LAST(name ORDER BY created_at)` |
| `ARG_MIN(arg, val)` | Argument beim Minimum-Wert | `ARG_MIN(name, price)` |
| `ARG_MAX(arg, val)` | Argument beim Maximum-Wert | `ARG_MAX(name, price)` |
| `MODE(column)` | Häufigster Wert | `MODE(category)` |

**Beispiel: Günstigstes und teuerstes Produkt pro Kategorie**

```sql
SELECT 
  category,
  ARG_MIN(name, price) AS cheapest_product,
  MIN(price) AS min_price,
  ARG_MAX(name, price) AS most_expensive_product,
  MAX(price) AS max_price
FROM Products
GROUP BY category
ORDER BY category;
```
@DuckDB.eval(sql_intro)

**Beispiel: Häufigste Brand pro Kategorie**

```sql
SELECT 
  category,
  MODE(brand) AS most_common_brand,
  COUNT(*) AS total_products
FROM Products
GROUP BY category;
```
@DuckDB.eval(sql_intro)

**💡 Warum ARG_MIN/ARG_MAX?**

Statt zwei Queries:
```sql
-- Umständlich:
SELECT name FROM Products WHERE price = (SELECT MIN(price) FROM Products);

-- Elegant:
SELECT ARG_MIN(name, price) FROM Products;
```

</section>

    --{{6}}--
FILTER-Klausel: Das ist ein Game-Changer für bedingte Aggregation. Statt mehrere CASE-Statements zu schreiben, nutzen Sie FILTER direkt in der Aggregatfunktion. „Zähle nur Electronics", „Summiere nur Produkte über 100 Euro", „Durchschnitt nur für bewertete Artikel" – alles in einer Zeile.

    {{6}}
<section>

#### FILTER-Klausel (Bedingte Aggregation)

**Syntax:**

```sql
AGGREGATE_FUNCTION(column) FILTER (WHERE condition)
```

Aggregiert nur Zeilen, die die Bedingung erfüllen.

**Beispiel: Kategorisierte Statistiken**

```sql
SELECT 
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE price < 100) AS budget_items,
  COUNT(*) FILTER (WHERE price BETWEEN 100 AND 500) AS mid_range,
  COUNT(*) FILTER (WHERE price > 500) AS premium,
  AVG(price) FILTER (WHERE rating > 4.0) AS avg_price_top_rated,
  SUM(stock) FILTER (WHERE category = 'Electronics') AS electronics_stock
FROM Products;
```
@DuckDB.eval(sql_intro)

**Beispiel: Pro Kategorie mit Filtern**

```sql
SELECT 
  category,
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE stock > 0) AS in_stock,
  COUNT(*) FILTER (WHERE stock = 0) AS out_of_stock,
  ROUND(AVG(price) FILTER (WHERE rating >= 4.0), 2) AS avg_price_good_rated
FROM Products
GROUP BY category
ORDER BY total DESC;
```
@DuckDB.eval(sql_intro)

**💡 Statt CASE WHEN:**

```sql
-- Umständlich:
SUM(CASE WHEN price > 100 THEN 1 ELSE 0 END)

-- Elegant:
COUNT(*) FILTER (WHERE price > 100)
```

</section>