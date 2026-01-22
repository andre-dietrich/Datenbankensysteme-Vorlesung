<!--
author:   André Dietrich; GitHub Copilot
email:    LiaScript@web.de

language: de
narrator: German Male

version:  2.0.0

edit:     true

comment:  Erweiterte SQL-Referenz: Von SELECT-Grundlagen über DDL/DML, Joins und Normalisierung bis zu SET Operations, Views, Transaktionen (ACID), Stored Functions und Triggern. Basiert auf Sessions 7-10, 13-15 der Datenbankensysteme-Vorlesung.

logo:     ../assets/img/logo/sql-cheat-sheet.jpg

@logo-prompt
Finalisierte Variante – 16:9 Wide Banner / Cheat-Sheet Cover

Full Prompt (DE/EN Hybrid – für Midjourney / SDXL / Ideogram):
„Wide aspect 16:9 flat minimal technical reference illustration. Zentrum: aufgeklapptes, stilisiertes Notizbuch (Cheat-Sheet) mit sichtbaren SQL-Code-Schnipseln (SELECT, JOIN, CREATE TABLE) als dezente Textur auf den Seiten. Links vom Buch schwebt ein kompakter Datenbank-Zylinder (3 klare horizontale Ringe), rechts schwebt ein abstraktes Tabellen-Gitter-Symbol (3×3 Grid) mit Pfeilen, die Datenfluss symbolisieren. Über dem Buch: kleine schwebende Icon-Cluster – Schlüssel-Symbol (Primary Key), Verbindungs-Knoten (Join), Zahnrad (Query), Blitz (Performance) – geordnet entlang einer sanften horizontalen Linie. Komposition ausbalanciert: Buch zentral, Zylinder links-oben, Grid rechts-oben, Icons als subtile Akzente. Optional: Schriftzug ‚SQL Cheat-Sheet' oder ‚Quick Reference' dezent integriert, moderne Sans-Serif, nicht dominant. Farbschema: 3 Hauptfarben – Tech Blue (#2563EB), SQL Green (#10B981), Neutral Grey (#6B7280) + Off-White (#F9FAFB) Hintergrund. Klare Konturen, keine Gradienten, geometrisch präzise, hoher Kontrast, Flat Design Aesthetic, gut lesbare Hierarchie, negative space nutzen, brandable reference design."

Midjourney Parameter (Beispiel):  --ar 16:9 --style raw --v 6 --s 50

DALL·E / Firefly Variante (EN Compact):
"Flat minimal wide 16:9 technical cheat-sheet cover. Open notebook center with SQL code snippets texture; left: compact database cylinder (3 rings); right: abstract table grid 3×3 with data flow arrows; floating icons above (key, join nodes, gear, lightning) aligned horizontally. Tech blue (#2563EB), SQL green (#10B981), grey (#6B7280), off-white background, clean outlines, no gradients, geometric precision, high contrast, modern reference aesthetic."

Short Prompt (Schnellvariante):
"16:9 flat wide cheat-sheet banner, open notebook center + database cylinder left + table grid right + floating SQL icons (key, join, gear, bolt), tech blue/green/grey, minimal flat design, geometric clean."

Dark Mode Zusatz (optional anfügen):
"Dark background #1F2937, subtle blue glow on notebook edges, green accent on grid connections, low-opacity grey icons."

Icon-Version (FavIcon / Monomark):
Vereinfachtes offenes Buch-Symbol mit einem einzelnen Datenbank-Zylinder-Ring als Lesezeichen + kleines SQL-Zeichen { } darüber. 1-Farb Version in Tech Blue.

Branding-Hinweis: Falls Typografie + Farbleitfaden benötigt wird, einfach „Branding ausarbeiten" anfragen.
@end

import: https://raw.githubusercontent.com/LiaTemplates/DuckDB/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md
-->

# SQL Cheat-Sheet – Quick Reference

> **Erweiterte Referenz** basierend auf Lectures 7-10, 13-15  
> **Themen:** SELECT, DDL/DML, Normalisierung, Joins, SET Operations, Views, Transaktionen, Functions, Trigger

---

## 📖 Wie nutze ich dieses Cheat-Sheet?

Dieses Dokument ist eine **erweiterte Referenz** für die wichtigsten SQL-Konzepte:

**Grundlagen:**

- **L7:** SELECT, WHERE, ORDER BY, GROUP BY, Aggregation
- **L8:** CREATE TABLE, ALTER, DROP, INSERT, UPDATE, DELETE, Constraints
- **L9:** Normalisierung (1NF, 2NF, 3NF), ER-Diagramme
- **L10:** Joins (INNER, LEFT, RIGHT, FULL, CROSS), Subqueries

**Fortgeschritten:**

- **L13:** SET Operations (UNION, INTERSECT, EXCEPT), Views
- **L14:** Transaktionen (BEGIN, COMMIT, ROLLBACK), ACID, Isolation Levels
- **L15:** Stored Functions (IF, CASE, RAISE), Trigger (BEFORE/AFTER)

**Navigation:**

- Nutze das **Inhaltsverzeichnis** (☰ links oben)
- Springe direkt zum gewünschten Thema
- Alle Code-Beispiele sind **interaktiv** – probiere sie aus!

---

## 1. DDL – Tabellen definieren (L8)

### 1.1 CREATE TABLE

```sql
-- Grundstruktur
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
@PGlite.eval(ddl)

### 1.2 Datentypen

| Typ                | Verwendung            | Beispiel                   |
| ------------------ | --------------------- | -------------------------- |
| `INTEGER`          | Ganzzahlen            | `age INTEGER`              |
| `BIGINT`           | Große Ganzzahlen      | `user_id BIGINT`           |
| `DECIMAL(p,s)`     | Präzise Dezimalzahlen | `price DECIMAL(10,2)`      |
| `FLOAT/DOUBLE`     | Approximative Zahlen  | `latitude FLOAT`           |
| `TEXT`             | Unbegrenzter Text     | `description TEXT`         |
| `VARCHAR(n)`       | Text mit Längenlimit  | `email VARCHAR(255)`       |
| `CHAR(n)`          | Festlängen-Text       | `country_code CHAR(2)`     |
| `DATE`             | Datum                 | `birth_date DATE`          |
| `TIMESTAMP`        | Datum + Uhrzeit       | `created_at TIMESTAMP`     |
| `BOOLEAN`          | Wahr/Falsch           | `is_active BOOLEAN`        |
| `JSON`             | JSON-Objekte          | `metadata JSON`            |

### 1.3 Constraints

```sql
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,                    -- Eindeutig + NOT NULL
  customer_id INTEGER NOT NULL,                    -- Pflichtfeld
  total DECIMAL(10,2) CHECK (total >= 0),          -- Validierung
  status TEXT CHECK (status IN ('pending', 'shipped', 'delivered')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Standardwert
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```
@PGlite.eval(ddl)

**Constraint-Übersicht:**

| Constraint       | Zweck                    | Beispiel                        |
| ---------------- | ------------------------ | ------------------------------- |
| `PRIMARY KEY`    | Eindeutig + NOT NULL     | `user_id INTEGER PRIMARY KEY`   |
| `FOREIGN KEY`    | Referenzielle Integrität | `FOREIGN KEY (user_id) REFERENCES users(user_id)` |
| `UNIQUE`         | Eindeutig (NULL erlaubt) | `email TEXT UNIQUE`             |
| `NOT NULL`       | Pflichtfeld              | `name TEXT NOT NULL`            |
| `CHECK`          | Benutzerdefiniert        | `age INTEGER CHECK (age >= 18)` |
| `DEFAULT`        | Standardwert             | `status TEXT DEFAULT 'active'`  |

### 1.4 Foreign Keys

```sql
-- Mit ON DELETE / ON UPDATE
CREATE TABLE order_items (
  item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  FOREIGN KEY (order_id) REFERENCES orders(order_id) 
    ON DELETE CASCADE,           -- Löscht Items, wenn Order gelöscht wird
  FOREIGN KEY (product_id) REFERENCES products(product_id)
    ON DELETE RESTRICT           -- Verhindert Löschen, wenn Items existieren
);
```
@PGlite.eval(ddl)

**ON DELETE Optionen:**

| Option      | Verhalten                            |
| ----------- | ------------------------------------ |
| `CASCADE`   | Abhängige Zeilen werden gelöscht     |
| `SET NULL`  | Foreign Key wird auf NULL gesetzt    |
| `RESTRICT`  | Löschen wird verhindert (Standard)   |
| `NO ACTION` | Wie RESTRICT                         |

### 1.5 ALTER TABLE

```sql
-- Spalte hinzufügen
ALTER TABLE customers
ADD COLUMN phone TEXT;

-- Spalte ändern (nicht alle DBs unterstützen alle Operationen)
ALTER TABLE customers
ALTER COLUMN email SET NOT NULL;

-- Spalte umbenennen (PostgreSQL)
ALTER TABLE customers
RENAME COLUMN phone TO mobile;

-- Tabelle umbenennen
ALTER TABLE customers RENAME TO clients;

-- Spalte löschen
ALTER TABLE clients
DROP COLUMN mobile;
```
@PGlite.terminal(ddl)

### 1.6 DROP TABLE

```sql
-- Einfach
DROP TABLE IF EXISTS temp_table;

-- Mit CASCADE (löscht auch abhängige Objekte)
DROP TABLE products CASCADE;

-- Mit RESTRICT (verhindert Löschen bei Abhängigkeiten)
DROP TABLE products RESTRICT;
```
@PGlite.terminal(ddl)

---

## 2. DML – Daten manipulieren (L8)

### 2.1 INSERT

```sql
-- Einzelne Zeile
INSERT INTO customers (customer_id, first_name, last_name, email)
VALUES (1, 'Alice', 'Anderson', 'alice@email.com');

-- Mehrere Zeilen (Bulk Insert)
INSERT INTO customers (customer_id, first_name, last_name, email) VALUES
  (2, 'Bob', 'Brown', 'bob@email.com'),
  (3, 'Carol', 'Clark', 'carol@email.com'),
  (4, 'David', 'Davis', 'david@email.com');

-- INSERT ... SELECT (Daten kopieren)
INSERT INTO customers_backup (customer_id, first_name, last_name, email)
SELECT customer_id, first_name, last_name, email 
FROM customers
WHERE email IS NOT NULL;

-- INSERT ... ON CONFLICT (Upsert)
INSERT INTO customers (customer_id, first_name, last_name, email)
VALUES (1, 'Alice Updated', 'alice_new@email.com')
ON CONFLICT (customer_id) DO UPDATE
SET 
  first_name = EXCLUDED.first_name,
  email = EXCLUDED.email;
```
@PGlite.terminal(ddl)

### 2.2 UPDATE

```sql
-- Einzelne Zeile
UPDATE customers
SET email = 'alice_new@email.com'
WHERE customer_id = 1;

-- Mehrere Spalten
UPDATE customers
SET 
  first_name = 'Alice',
  last_name = 'Smith',
  email = 'alice.smith@email.com'
WHERE customer_id = 1;

-- Berechnete Updates
UPDATE products
SET price = price * 1.10;  -- 10% Preiserhöhung

-- UPDATE mit Subquery
UPDATE products
SET price = price * (1 - (
  SELECT discount_percent / 100 
  FROM categories 
  WHERE categories.category_id = products.category_id
));
```
@PGlite.terminal(ddl)

⚠️ **Immer WHERE nutzen!** Ohne WHERE werden ALLE Zeilen geändert!

### 2.3 DELETE

```sql
-- Einzelne Zeile
DELETE FROM customers
WHERE customer_id = 5;

-- Mehrere Zeilen
DELETE FROM customers
WHERE email IS NULL;

-- DELETE mit Subquery
DELETE FROM customers
WHERE customer_id NOT IN (
  SELECT DISTINCT customer_id FROM orders
);
```
@PGlite.terminal(ddl)

⚠️ **Immer WHERE nutzen!** Ohne WHERE werden ALLE Zeilen gelöscht!

### 2.4 TRUNCATE vs DELETE

```sql
-- DELETE: Selektiv, in Transaktion reversibel
DELETE FROM products WHERE price < 50;

-- TRUNCATE: Löscht alle Zeilen, schneller, meist nicht reversibel
TRUNCATE TABLE products;
```
@PGlite.terminal(ddl)

| Feature        | DELETE                | TRUNCATE               |
| -------------- | --------------------- | ---------------------- |
| WHERE-Klausel  | ✅ Ja                 | ❌ Nein                |
| Performance    | Langsamer             | Schneller              |
| Rollback       | ✅ Möglich            | ⚠️ DB-abhängig        |
| Triggers       | ✅ Werden ausgelöst   | ❌ Meist nicht         |
| Auto-Increment | Bleibt                | Wird zurückgesetzt     |

---

## 3. SELECT – Daten abfragen (L7)

### 3.1 Grundstruktur

```sql
SELECT spalte1, spalte2, ...
FROM tabelle
WHERE bedingung
ORDER BY spalte [ASC|DESC]
LIMIT anzahl;
```

### 3.2 Beispieldatenbank laden

```sql
INSTALL httpfs;
LOAD httpfs;

CREATE TEMP TABLE products_raw AS
SELECT *
FROM read_json('https://raw.githubusercontent.com/andre-dietrich/Datenbankensysteme-Vorlesung/refs/heads/main/assets/dat/products.json');

CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  category TEXT,
  brand TEXT,
  price REAL,
  stock INTEGER,
  rating REAL,
  created_at DATE
);

INSERT INTO products
SELECT
  CAST(product_id AS INTEGER),
  name::TEXT,
  category::TEXT,
  brand::TEXT,
  CAST(price AS REAL),
  CAST(stock AS INTEGER),
  CAST(rating AS REAL),
  CAST(created_at AS DATE)
FROM products_raw;
```
@DuckDB.eval(cheat)

### 3.3 Spalten auswählen

```sql
-- Alle Spalten
SELECT * FROM products LIMIT 5;

-- Spezifische Spalten
SELECT name, price, category FROM products LIMIT 5;

-- Mit Alias
SELECT 
  name AS product_name,
  price AS price_eur,
  category
FROM products LIMIT 5;
```
@DuckDB.terminal(cheat)

### 3.4 WHERE – Filtern

```sql
-- Vergleichsoperatoren: =, <>, <, >, <=, >=
SELECT name, price FROM products 
WHERE price < 50;

-- Logische Operatoren: AND, OR, NOT
SELECT name, price, category FROM products
WHERE category = 'Electronics' AND price < 100;

-- BETWEEN
SELECT name, price FROM products
WHERE price BETWEEN 100 AND 500;

-- IN
SELECT name, category FROM products
WHERE category IN ('Electronics', 'Office', 'Groceries');

-- LIKE (Pattern Matching)
SELECT name FROM products
WHERE name LIKE '%Laptop%';  -- % = beliebig viele Zeichen

-- NULL-Werte
SELECT name, rating FROM products
WHERE rating IS NULL;
```
@DuckDB.terminal(cheat)

### 3.5 ORDER BY – Sortieren

```sql
-- Aufsteigend (Standard)
SELECT name, price FROM products
ORDER BY price ASC
LIMIT 10;

-- Absteigend
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 10;

-- Nach mehreren Spalten
SELECT category, name, price FROM products
ORDER BY category ASC, price DESC
LIMIT 10;

-- NULL-Behandlung
SELECT name, rating FROM products
ORDER BY rating DESC NULLS LAST
LIMIT 10;
```
@DuckDB.terminal(cheat)

### 3.6 DISTINCT – Duplikate entfernen

```sql
-- Eindeutige Kategorien
SELECT DISTINCT category 
FROM products
ORDER BY category;

-- Eindeutige Kombinationen
SELECT DISTINCT category, brand 
FROM products
ORDER BY category, brand;
```
@DuckDB.terminal(cheat)

### 3.7 GROUP BY & Aggregation

```sql
-- Anzahl pro Kategorie
SELECT 
  category,
  COUNT(*) AS product_count
FROM products
GROUP BY category
ORDER BY product_count DESC;

-- Mehrere Aggregate
SELECT 
  category,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS avg_price,
  MIN(price) AS cheapest,
  MAX(price) AS most_expensive,
  SUM(stock) AS total_stock
FROM products
GROUP BY category;

-- HAVING – Gruppen filtern
SELECT 
  category,
  COUNT(*) AS count,
  ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
HAVING COUNT(*) > 50
ORDER BY count DESC;

-- WHERE + GROUP BY + HAVING
SELECT 
  brand,
  COUNT(*) AS products,
  ROUND(AVG(price), 2) AS avg_price
FROM products
WHERE category = 'Electronics'
GROUP BY brand
HAVING COUNT(*) > 5
ORDER BY products DESC;
```
@DuckDB.terminal(cheat)

### 3.8 LIMIT & OFFSET – Paginierung

```sql
-- Top 10
SELECT name, price FROM products
ORDER BY price DESC
LIMIT 10;

-- Seite 2 (Zeilen 11-20)
SELECT name, price FROM products
ORDER BY name
LIMIT 10 OFFSET 10;

-- Cursor-basierte Paginierung (besser bei großen Offsets)
SELECT product_id, name, price FROM products
WHERE product_id > 'P00010'
ORDER BY product_id
LIMIT 10;
```
@DuckDB.terminal(cheat)

---

## 4. Normalisierung (L9)

### 4.1 Normalformen-Übersicht

| Normalform | Regel                                                     | Beispiel-Problem                 |
| ---------- | --------------------------------------------------------- | -------------------------------- |
| **1NF**    | Alle Werte sind atomar (keine Listen)                     | Adresse = "Straße, PLZ, Stadt"   |
| **2NF**    | 1NF + keine partiellen Abhängigkeiten                     | Produktname hängt nur von product_id ab |
| **3NF**    | 2NF + keine transitiven Abhängigkeiten                    | Stadt hängt von PLZ ab           |

### 4.2 1NF – Erste Normalform

**Regel:** Alle Attribute sind atomar (kein einziges Attribut enthält mehrere Werte).

```sql
-- ❌ Nicht 1NF (Adresse nicht atomar)
CREATE TABLE users_bad (
  user_id INTEGER,
  name TEXT,
  address TEXT  -- "Hauptstraße 12, 04109 Leipzig"
);

-- ✅ 1NF (Adresse aufgeteilt)
CREATE TABLE users_good (
  user_id INTEGER,
  name TEXT,
  street TEXT,      -- "Hauptstraße 12"
  zip TEXT,         -- "04109"
  city TEXT         -- "Leipzig"
);
```
@PGlite.eval(norm)

### 4.3 2NF – Zweite Normalform

**Regel:** 1NF + jedes Nicht-Schlüssel-Attribut hängt vom gesamten Primärschlüssel ab (keine partiellen Abhängigkeiten).

```sql
-- ❌ Nicht 2NF (product_name hängt nur von product_id ab, nicht von order_id)
CREATE TABLE order_items_bad (
  order_id INTEGER,
  product_id INTEGER,
  product_name TEXT,    -- Redundant! Hängt nur von product_id ab
  quantity INTEGER,
  PRIMARY KEY (order_id, product_id)
);

-- ✅ 2NF (Produktdaten ausgelagert)
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT
);

CREATE TABLE order_items_good (
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```
@PGlite.eval(norm)

### 4.4 3NF – Dritte Normalform

**Regel:** 2NF + keine transitiven Abhängigkeiten (kein Nicht-Schlüssel-Attribut hängt von einem anderen Nicht-Schlüssel-Attribut ab).

```sql
-- ❌ Nicht 3NF (city hängt von zip ab → transitive Abhängigkeit)
CREATE TABLE customers_bad (
  customer_id INTEGER PRIMARY KEY,
  name TEXT,
  zip TEXT,
  city TEXT  -- Hängt von zip ab!
);

-- ✅ 3NF (PLZ/Stadt ausgelagert)
CREATE TABLE locations (
  location_id INTEGER PRIMARY KEY,
  zip TEXT UNIQUE,
  city TEXT
);

CREATE TABLE customers_good (
  customer_id INTEGER PRIMARY KEY,
  name TEXT,
  location_id INTEGER,
  FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
```
@PGlite.eval(norm)

### 4.5 ER-Diagramm-Notation

**Kardinalitäten:**

- **1:1** (Eins-zu-Eins): `User ||--|| Profile` – Ein User hat genau ein Profil
- **1:N** (Eins-zu-Viele): `User ||--o{ Order` – Ein User kann viele Orders haben
- **N:M** (Viele-zu-Viele): `Product }o--o{ Order` – Viele Products in vielen Orders (via Junction Table)

**Schlüssel:**

- **PK** = Primary Key (unterstrichen)
- **FK** = Foreign Key (gestrichelt)

---

## 5. Joins (L10)

### 5.1 Testdaten erstellen

```sql
-- Locations
CREATE TABLE locations (
  location_id INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  postal_code TEXT NOT NULL
);

INSERT INTO locations VALUES
  (1, 'Berlin', '10115'),
  (2, 'Hamburg', '20095'),
  (3, 'Munich', '80331');

-- Customers
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  location_id INTEGER,
  FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

INSERT INTO customers VALUES
  (1, 'Alice', 'Anderson', 1),
  (2, 'Bob', 'Brown', 2),
  (3, 'Carol', 'Clark', 3),
  (4, 'David', 'Davis', NULL);  -- Kein Standort

-- Orders
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders VALUES
  (101, 1, '2024-01-15'),
  (102, 1, '2024-02-20'),
  (103, 2, '2024-01-22'),
  (104, 3, '2024-03-10');
-- Kunde 4 hat keine Bestellung!
```
@PGlite.eval(joins)

### 5.2 INNER JOIN

**Regel:** Nur Zeilen, die in BEIDEN Tabellen übereinstimmen.

```sql
SELECT 
  c.first_name,
  c.last_name,
  o.order_id,
  o.order_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```
@PGlite.terminal(joins)

**Ergebnis:** Nur Kunden MIT Bestellungen (Alice, Bob, Carol). David fehlt!

### 5.3 LEFT JOIN (LEFT OUTER JOIN)

**Regel:** Alle Zeilen aus der linken Tabelle + passende aus der rechten. Wenn keine Übereinstimmung → NULL.

```sql
SELECT 
  c.first_name,
  c.last_name,
  o.order_id,
  o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```
@PGlite.terminal(joins)

**Ergebnis:** Alle Kunden (auch David), aber bei David ist order_id = NULL.

**Use Case:** "Zeige alle Kunden, auch die ohne Bestellung."

### 5.4 RIGHT JOIN (RIGHT OUTER JOIN)

**Regel:** Alle Zeilen aus der rechten Tabelle + passende aus der linken.

```sql
SELECT 
  c.first_name,
  o.order_id
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
```
@PGlite.terminal(joins)

**In der Praxis:** Selten genutzt (kann durch LEFT JOIN ersetzt werden).

### 5.5 FULL OUTER JOIN

**Regel:** Alle Zeilen aus BEIDEN Tabellen. Wenn keine Übereinstimmung → NULL.

```sql
SELECT 
  c.first_name,
  o.order_id
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;
```
@PGlite.terminal(joins)

**Ergebnis:** Alle Kunden UND alle Bestellungen. Lücken werden mit NULL gefüllt.

**Use Case:** "Zeige alle Kunden UND alle Bestellungen, unabhängig von Beziehungen."

### 5.6 CROSS JOIN (Kartesisches Produkt)

**Regel:** Jede Zeile der ersten Tabelle wird mit jeder Zeile der zweiten kombiniert.

```sql
SELECT 
  c.first_name,
  l.city
FROM customers c
CROSS JOIN locations l;
```
@PGlite.terminal(joins)

**Ergebnis:** 4 Kunden × 3 Städte = 12 Zeilen.

**Use Case:** Selten! Z.B. für Preis-Matrices oder kombinatorische Abfragen.

### 5.7 Self Join

**Regel:** Tabelle mit sich selbst joinen (z.B. Hierarchien).

```sql
-- Mitarbeiter-Hierarchie
CREATE TABLE employees (
  emp_id INTEGER PRIMARY KEY,
  name TEXT,
  manager_id INTEGER,
  FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);

INSERT INTO employees VALUES
  (1, 'CEO', NULL),
  (2, 'CTO', 1),
  (3, 'Dev Lead', 2),
  (4, 'Developer', 3);

-- Wer ist wessen Manager?
SELECT 
  e.name AS employee,
  m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```
@PGlite.terminal(joins)

### 5.8 Mehrere Joins kombinieren

```sql
-- Kunde → Bestellung → Positionen → Produkte
SELECT 
  c.first_name,
  o.order_id,
  oi.quantity,
  p.product_name,
  p.price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

**Faustregel:** Jeder JOIN braucht eine ON-Bedingung!

### 5.9 Join-Cheat-Sheet

| Join-Typ          | Ergebnis                                  | Use Case                          |
| ----------------- | ----------------------------------------- | --------------------------------- |
| `INNER JOIN`      | Nur übereinstimmende Zeilen               | Kunden MIT Bestellungen           |
| `LEFT JOIN`       | Alle aus links + passende aus rechts      | Alle Kunden (auch ohne Orders)    |
| `RIGHT JOIN`      | Alle aus rechts + passende aus links      | Selten (wie LEFT, nur umgekehrt)  |
| `FULL OUTER JOIN` | Alle aus beiden (Lücken = NULL)           | Alle Kunden UND alle Orders       |
| `CROSS JOIN`      | Kartesisches Produkt (alle Kombinationen) | Kombinatorik, Matrizen            |
| `SELF JOIN`       | Tabelle mit sich selbst                   | Hierarchien, Vergleiche           |

---

## 6. SET Operations (L13)

SET Operations kombinieren Ergebnismengen zweier Queries – ähnlich wie Mengenoperationen in der Mathematik.

**Wichtige Regeln:**

- Beide SELECT-Statements müssen **gleich viele Spalten** haben
- Spaltentypen müssen **kompatibel** sein
- Spaltennamen werden aus der ersten Query übernommen

### 6.1 UNION – Vereinigung

**Regel:** Kombiniert beide Ergebnismengen und **entfernt Duplikate**.

```sql
-- Newsletter-Liste: Alle Personen (Kunden + Mitarbeiter)
SELECT first_name, last_name, 'Customer' AS type
FROM customers
UNION
SELECT first_name, last_name, 'Employee' AS type
FROM employees
ORDER BY last_name;
```
@PGlite.terminal(joins)

**UNION vs UNION ALL:**

| Operation     | Duplikate        | Performance |
| ------------- | ---------------- | ----------- |
| `UNION`       | Werden entfernt  | Langsamer   |
| `UNION ALL`   | Bleiben erhalten | Schneller   |

```sql
-- UNION ALL: Behält alle Einträge (auch Duplikate)
SELECT first_name, last_name FROM customers
UNION ALL
SELECT first_name, last_name FROM employees;
```
@PGlite.terminal(joins)

**Tipp:** Nutze `UNION ALL`, wenn keine Duplikate existieren oder gewünscht sind!

### 6.2 INTERSECT – Schnittmenge

**Regel:** Nur Zeilen, die in **BEIDEN** Ergebnismengen vorkommen.

```sql
-- Mitarbeiter, die auch Kunden sind (basierend auf Name)
SELECT first_name, last_name
FROM customers
INTERSECT
SELECT first_name, last_name
FROM employees
ORDER BY last_name;
```
@PGlite.terminal(joins)

**Alternative mit JOIN:**

```sql
-- Gleichwertig mit INNER JOIN
SELECT DISTINCT c.first_name, c.last_name
FROM customers c
INNER JOIN employees e 
  ON c.first_name = e.first_name 
  AND c.last_name = e.last_name;
```

**Wann INTERSECT?** Klarer Intent: "Zeig mir die Überschneidung!"

### 6.3 EXCEPT – Differenz

**Regel:** Zeilen aus der **ersten** Query, die **NICHT** in der zweiten vorkommen.

```sql
-- Kunden, die KEINE Mitarbeiter sind
SELECT first_name, last_name
FROM customers
EXCEPT
SELECT first_name, last_name
FROM employees
ORDER BY last_name;
```
@PGlite.terminal(joins)

**⚠️ Reihenfolge zählt!** `A EXCEPT B` ≠ `B EXCEPT A`

```sql
-- Umgekehrt: Mitarbeiter, die KEINE Kunden sind
SELECT first_name, last_name FROM employees
EXCEPT
SELECT first_name, last_name FROM customers;
```

**Alternative mit LEFT JOIN:**

```sql
-- Gleichwertig mit Anti-Join
SELECT c.first_name, c.last_name
FROM customers c
LEFT JOIN employees e 
  ON c.first_name = e.first_name 
  AND c.last_name = e.last_name
WHERE e.employee_id IS NULL;
```

### 6.4 SET Operations kombinieren

```sql
-- Komplexe Abfragen mit mehreren SET Operations
(SELECT first_name, last_name FROM customers WHERE location_id = 1
 UNION
 SELECT first_name, last_name FROM customers WHERE location_id = 2)
EXCEPT
SELECT first_name, last_name FROM employees;
```

**Tipp:** Nutze Klammern `()` für klare Gruppierung!

---

## 7. Views (L13)

### 7.1 Was sind Views?

**Views** sind gespeicherte Queries, die wie virtuelle Tabellen funktionieren. Sie speichern keine Daten, sondern nur die Query-Definition.

**Vorteile:**

- ✅ **Wiederverwendbarkeit:** Komplexe Queries einmal definieren
- ✅ **Abstraktion:** Versteckt Komplexität vor Nutzern
- ✅ **Sicherheit:** Kontrollierter Zugriff auf Daten
- ✅ **Konsistenz:** Eine Definition, überall nutzbar

### 7.2 CREATE VIEW

```sql
-- Einfache View: Aktive Kunden mit Standort
CREATE VIEW active_customers AS
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email,
  l.city,
  l.postal_code
FROM customers c
INNER JOIN locations l ON c.location_id = l.location_id
WHERE c.is_active = true;

-- View nutzen wie eine Tabelle
SELECT * FROM active_customers WHERE city = 'Berlin';
```
@PGlite.eval(joins)

### 7.3 Views mit Aggregation

```sql
-- Customer-Summary: Bestellungen pro Kunde
CREATE VIEW customer_summary AS
SELECT 
  c.customer_id,
  c.first_name || ' ' || c.last_name AS full_name,
  COUNT(o.order_id) AS order_count,
  COALESCE(SUM(o.total_amount), 0) AS total_spent,
  MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- VIP-Kunden finden
SELECT * FROM customer_summary 
WHERE total_spent > 1000 
ORDER BY total_spent DESC;
```
@PGlite.eval(joins)

### 7.4 Views aktualisieren

```sql
-- View ersetzen
CREATE OR REPLACE VIEW active_customers AS
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email,
  l.city
FROM customers c
LEFT JOIN locations l ON c.location_id = l.location_id
WHERE c.is_active = true;
```
@PGlite.terminal(joins)

### 7.5 Views löschen

```sql
-- View entfernen
DROP VIEW IF EXISTS customer_summary;

-- Mit CASCADE (löscht auch abhängige Views)
DROP VIEW customer_summary CASCADE;
```
@PGlite.terminal(joins)

### 7.6 Materialized Views (PostgreSQL)

**Materialized Views** speichern das Ergebnis physisch → schneller, aber nicht automatisch aktualisiert.

```sql
-- Materialized View erstellen
CREATE MATERIALIZED VIEW sales_stats AS
SELECT 
  DATE_TRUNC('month', order_date) AS month,
  COUNT(*) AS orders,
  SUM(total_amount) AS revenue
FROM orders
GROUP BY month;

-- Daten aktualisieren (manuell)
REFRESH MATERIALIZED VIEW sales_stats;

-- Löschen
DROP MATERIALIZED VIEW sales_stats;
```

**View vs Materialized View:**

| Feature            | VIEW                    | MATERIALIZED VIEW       |
| ------------------ | ----------------------- | ----------------------- |
| Speicherung        | Nur Query-Definition    | Physische Daten         |
| Aktualität         | Immer aktuell           | Manuell refreshen       |
| Performance        | Query bei jedem Zugriff | Schnell (vorberechnet)  |
| Speicherplatz      | Minimal                 | Benötigt Platz          |

**Use Cases:**

- **VIEW:** Einfache Abstraktion, Sicherheit, oft geänderte Daten
- **MATERIALIZED VIEW:** Komplexe Aggregationen, Reports, seltene Änderungen

---

## 8. Transaktionen & ACID (L14)

### 8.1 Was sind Transaktionen?

**Transaktion** = Logische Arbeitseinheit, die garantiert, dass entweder **alle** Operationen erfolgreich sind – oder **keine**.

**Metapher:** Ein Paket mit Garantiesiegel – entweder kommt alles an oder gar nichts.

### 8.2 Transaktionssteuerung

```sql
-- Transaktion starten
BEGIN TRANSACTION;  -- oder: START TRANSACTION;

-- Operationen ausführen
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';

-- Bestätigen (Änderungen dauerhaft speichern)
COMMIT;

-- ODER: Rückgängig machen
ROLLBACK;
```
@PGlite.terminal

**Wichtig:** Ohne `COMMIT` werden Änderungen **nicht** dauerhaft gespeichert!

### 8.3 SAVEPOINT – Partielle Rollbacks

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

SAVEPOINT transfer_step1;

UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
-- ❌ Fehler! Konto B existiert nicht

ROLLBACK TO transfer_step1;  -- Nur Schritt 2 rückgängig
COMMIT;  -- Schritt 1 bleibt bestehen
```
@PGlite.terminal

### 8.4 ACID-Eigenschaften

**ACID** = Vier Garantien, die jede Transaktion erfüllen sollte:

#### A – Atomicity (Atomarität)

**"Alles oder Nichts"** – Transaktion ist unteilbar.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
-- ❌ Server-Crash hier → Automatisches ROLLBACK!
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;
```

**Garantie:** Bei Fehler/Crash werden ALLE Änderungen rückgängig gemacht.

#### C – Consistency (Konsistenz)

**Gültiger Zustand → Gültiger Zustand** – Constraints werden eingehalten.

```sql
-- Constraint: Balance nie negativ
ALTER TABLE accounts ADD CONSTRAINT balance_positive CHECK (balance >= 0);

BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';
-- ❌ Constraint verletzt → Automatisches ROLLBACK
COMMIT;
```

**Garantie:** Datenbank bleibt konsistent – Constraints gelten immer.

#### I – Isolation

**Parallele Transaktionen beeinflussen sich nicht** – jede läuft isoliert.

```sql
-- Transaktion A
BEGIN;
SELECT balance FROM accounts WHERE id = 'A';  -- 100
-- ... (lange Berechnung)
UPDATE accounts SET balance = balance - 50 WHERE id = 'A';
COMMIT;

-- Transaktion B (parallel!)
BEGIN;
SELECT balance FROM accounts WHERE id = 'A';  -- Sieht auch 100
UPDATE accounts SET balance = balance - 30 WHERE id = 'A';
COMMIT;
```

**Problem ohne Isolation:** Lost Update! Nur eine Änderung bleibt.  
**Mit Isolation:** B muss warten, bis A fertig ist.

#### D – Durability (Dauerhaftigkeit)

**Nach COMMIT = Für immer gespeichert** – selbst bei Crash.

```sql
BEGIN;
INSERT INTO orders VALUES (999, 1, '2024-01-01', 500);
COMMIT;
-- ✅ Auch bei Stromausfall DIREKT nach COMMIT: Daten sind sicher!
```

**Technisch:** Write-Ahead Log (WAL) schreibt Änderungen auf Festplatte.

### 8.5 Isolation Levels

**Trade-off:** Perfekte Isolation = langsam. Verschiedene Levels erlauben Kompromisse.

| Level                | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
| -------------------- | ---------- | ------------------- | ------------ | ----------- |
| `READ UNCOMMITTED`   | ✅ Möglich | ✅ Möglich          | ✅ Möglich   | Schnellst   |
| `READ COMMITTED`     | ❌         | ✅ Möglich          | ✅ Möglich   | Gut         |
| `REPEATABLE READ`    | ❌         | ❌                  | ✅ Möglich   | Mittel      |
| `SERIALIZABLE`       | ❌         | ❌                  | ❌           | Langsam     |

**Setzen:**

```sql
-- Für aktuelle Transaktion
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Global (Session)
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

**Standard:** Meist `READ COMMITTED` (PostgreSQL, Oracle) oder `REPEATABLE READ` (MySQL).

### 8.6 Transaktions-Probleme

#### Problem 1: Dirty Read

**Transaktion A liest uncommitted Daten von B:**

```sql
-- Session 1
BEGIN;
UPDATE accounts SET balance = 1000 WHERE id = 'A';
-- NOCH NICHT COMMITTED!

-- Session 2
SELECT balance FROM accounts WHERE id = 'A';  -- 1000 (Dirty!)

-- Session 1
ROLLBACK;  -- Änderung rückgängig!
-- Session 2 hat einen Wert gelesen, der nie existiert hat!
```

#### Problem 2: Lost Update

**Zwei Transaktionen überschreiben sich gegenseitig:**

```sql
-- A: Liest balance = 100
-- B: Liest balance = 100
-- A: Schreibt balance = 50  (100 - 50)
-- B: Schreibt balance = 70  (100 - 30)
-- Ergebnis: 70 statt 20! (50 Euro verloren)
```

**Lösung:** `SELECT ... FOR UPDATE` (sperrt Zeile):

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 'A' FOR UPDATE;
-- Zeile ist jetzt gesperrt – andere müssen warten
UPDATE accounts SET balance = balance - 50 WHERE id = 'A';
COMMIT;
```

#### Problem 3: Deadlock

**Zwei Transaktionen warten aufeinander:**

```sql
-- Transaction A
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 'A';
-- Wartet auf Konto B...

-- Transaction B
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 'B';
-- Wartet auf Konto A...

-- ❌ Deadlock! Datenbank bricht eine Transaktion ab.
```

**Lösung:** Immer in gleicher Reihenfolge sperren (z.B. aufsteigend nach ID).

### 8.7 Best Practices

✅ **Transaktionen kurz halten** (schnellere Sperren)

✅ **Explizite Transaktionen** für Multi-Step-Operationen

✅ **FOR UPDATE nutzen** bei konkurrierenden Updates

✅ **Deadlocks vermeiden** durch konsistente Reihenfolge

✅ **Fehlerbehandlung:** Immer `ROLLBACK` bei Fehler

❌ **Keine langen User-Interaktionen** in Transaktionen

---

## 9. Functions & Trigger (L15)

### 9.1 Stored Functions

**Stored Functions** = Wiederverwendbare Code-Blöcke, gespeichert in der Datenbank.

#### Grundsyntax (PostgreSQL)

```sql
CREATE FUNCTION function_name(param1 TYPE, param2 TYPE)
RETURNS return_type AS $$
BEGIN
    -- Code hier
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

#### Beispiel: Preisberechnung

```sql
CREATE FUNCTION calculate_total(price DECIMAL, tax_rate DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    IF price < 0 THEN
        RAISE EXCEPTION 'Preis darf nicht negativ sein!';
    END IF;
    IF tax_rate < 0 OR tax_rate > 1 THEN
        RAISE EXCEPTION 'Steuersatz muss zwischen 0 und 1 liegen!';
    END IF;
    RETURN price * (1 + tax_rate);
END;
$$ LANGUAGE plpgsql;

-- Aufrufen
SELECT calculate_total(100, 0.19) as brutto;  -- 119.00
```
@PGlite.eval

### 9.2 Kontrollstrukturen

#### IF / THEN / ELSE

```sql
CREATE FUNCTION check_age(age INT)
RETURNS TEXT AS $$
BEGIN
    IF age >= 18 THEN
        RETURN 'Volljährig';
    ELSE
        RETURN 'Minderjährig';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

#### CASE

```sql
CREATE FUNCTION get_grade(score INT)
RETURNS TEXT AS $$
BEGIN
    RETURN CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        WHEN score >= 70 THEN 'C'
        WHEN score >= 60 THEN 'D'
        ELSE 'F'
    END;
END;
$$ LANGUAGE plpgsql;
```

### 9.3 Fehlerbehandlung: RAISE

```sql
CREATE FUNCTION divide(a INT, b INT)
RETURNS DECIMAL AS $$
BEGIN
    IF b = 0 THEN
        RAISE EXCEPTION 'Division durch Null nicht erlaubt!';
    END IF;
    RETURN a::DECIMAL / b;
END;
$$ LANGUAGE plpgsql;

-- Test
SELECT divide(10, 2);   -- ✅ 5.0
SELECT divide(10, 0);   -- ❌ Exception
```

### 9.4 Trigger

**Trigger** = Automatisch ausgeführte Funktionen bei bestimmten Events (INSERT/UPDATE/DELETE).

#### Trigger-Function erstellen

```sql
-- 1. Function mit RETURNS TRIGGER
CREATE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Trigger erstellen
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

**Besondere Variablen:**

- `NEW` – Die neue Zeile (bei INSERT/UPDATE)
- `OLD` – Die alte Zeile (bei UPDATE/DELETE)

#### BEFORE vs AFTER

| Timing   | Verwendung                           | Kann abbrechen? |
| -------- | ------------------------------------ | --------------- |
| `BEFORE` | Daten validieren/ändern              | ✅ Ja (RETURN NULL) |
| `AFTER`  | Logging, Audit, abhängige Aktionen   | ❌ Nein         |

#### Beispiel: Audit-Logging

```sql
-- Audit-Tabelle
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name TEXT,
    action TEXT,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger-Function
CREATE FUNCTION log_price_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.price IS DISTINCT FROM NEW.price THEN
        INSERT INTO audit_log (table_name, action, old_value, new_value)
        VALUES ('products', 'UPDATE', OLD.price::TEXT, NEW.price::TEXT);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER audit_price_changes
AFTER UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION log_price_changes();
```

#### Trigger löschen

```sql
DROP TRIGGER IF EXISTS audit_price_changes ON products;
```

### 9.5 Use Cases

| Use Case                  | Function | Trigger |
| ------------------------- | -------- | ------- |
| Wiederverwendbare Logik   | ✅✅     | ⚠️      |
| Automatische Timestamps   | ⚠️       | ✅✅    |
| Audit-Logging             | ⚠️       | ✅✅    |
| Validierung (nicht umgehbar) | ⚠️    | ✅✅    |
| Soft Delete               | ⚠️       | ✅✅    |
| Komplexe Berechnungen     | ✅✅     | ⚠️      |

**Faustregel:**

- **Function** = Aktiv aufrufen, testbar, wiederverwendbar
- **Trigger** = Automatisch, konsistent, kann nicht vergessen werden

---

## 10. Best Practices

### 7.1 Query-Optimierung

✅ **Spalten explizit benennen** statt `SELECT *`

✅ **WHERE statt HAVING** (wenn möglich)

✅ **Aliase nutzen** für Lesbarkeit

✅ **Indexes auf Foreign Keys** (Performance)

✅ **LIMIT bei Exploration** (nicht alle Millionen Zeilen laden)

### 7.2 Schema-Design

✅ **Immer Primary Keys** definieren

✅ **Foreign Keys für Integrität** nutzen

✅ **NOT NULL für Pflichtfelder**

✅ **CHECK Constraints** für Validierung

✅ **DEFAULT-Werte** wo sinnvoll

✅ **Normalisierung bis 3NF** (außer Performance-Gründe)

### 7.3 Datenmanipulation

✅ **Immer WHERE bei UPDATE/DELETE** (außer wirklich alle Zeilen)

✅ **Transaktionen für Multi-Step-Operationen**

✅ **Bulk Insert statt einzelne INSERTs**

✅ **Backup vor riskanten Änderungen**

⚠️ **TRUNCATE nur wenn sicher** (meist nicht reversibel)

---

## 10. Best Practices

### 10.1 Query-Optimierung

✅ **Spalten explizit benennen** statt `SELECT *`

✅ **WHERE statt HAVING** (wenn möglich)

✅ **Aliase nutzen** für Lesbarkeit

✅ **Indexes auf Foreign Keys** (Performance)

✅ **LIMIT bei Exploration** (nicht alle Millionen Zeilen laden)

### 10.2 Schema-Design

✅ **Immer Primary Keys** definieren

✅ **Foreign Keys für Integrität** nutzen

✅ **NOT NULL für Pflichtfelder**

✅ **CHECK Constraints** für Validierung

✅ **DEFAULT-Werte** wo sinnvoll

✅ **Normalisierung bis 3NF** (außer Performance-Gründe)

### 10.3 Datenmanipulation

✅ **Immer WHERE bei UPDATE/DELETE** (außer wirklich alle Zeilen)

✅ **Transaktionen für Multi-Step-Operationen**

✅ **Bulk Insert statt einzelne INSERTs**

✅ **Backup vor riskanten Änderungen**

⚠️ **TRUNCATE nur wenn sicher** (meist nicht reversibel)

### 10.4 Transaktionen & Concurrency

✅ **Transaktionen kurz halten** (schnellere Sperren freigeben)

✅ **FOR UPDATE nutzen** bei konkurrierenden Updates

✅ **Deadlocks vermeiden** durch konsistente Sperr-Reihenfolge

✅ **Fehlerbehandlung:** Immer `ROLLBACK` bei Fehler

❌ **Keine User-Interaktionen** in Transaktionen

### 10.5 Functions & Trigger

✅ **Functions für wiederverwendbare Logik**

✅ **Trigger für Automatisierung** (Timestamps, Audit)

✅ **RAISE für aussagekräftige Fehler**

✅ **Views für komplexe Queries**

⚠️ **Trigger sparsam einsetzen** (schwer zu debuggen)

❌ **Keine komplexe Business-Logik in Triggern**

---

## 11. Häufige Fehler & Lösungen

### ❌ Fehler: UPDATE ohne WHERE

```sql
-- GEFAHR: Ändert ALLE Zeilen!
UPDATE customers SET name = 'Unknown';
```

✅ **Immer WHERE nutzen:**

```sql
UPDATE customers SET name = 'Unknown' WHERE customer_id = 5;
```

### ❌ Fehler: Kartesisches Produkt

```sql
-- GEFAHR: 1000 Kunden × 1000 Orders = 1 Million Zeilen!
SELECT * FROM customers, orders;
```

✅ **Immer JOIN mit ON:**

```sql
SELECT * FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

### ❌ Fehler: NULL-Vergleich mit =

```sql
-- Funktioniert NICHT:
WHERE rating = NULL
```

✅ **Nutze IS NULL:**

```sql
WHERE rating IS NULL
```

### ❌ Fehler: Alias in WHERE

```sql
-- Fehler: price_with_tax nicht verfügbar!
SELECT price * 1.19 AS price_with_tax
FROM products
WHERE price_with_tax > 100;
```

✅ **Berechnung in WHERE wiederholen:**

```sql
SELECT price * 1.19 AS price_with_tax
FROM products
WHERE price * 1.19 > 100;
```

(Oder mit CTE/Subquery – siehe L10)

### ❌ Fehler: Transaktion nicht geschlossen

```sql
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 'A';
-- Vergessen: COMMIT oder ROLLBACK!
-- → Sperren bleiben bestehen, andere warten ewig
```

✅ **Immer schließen:**

```sql
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 'A';
COMMIT;  -- oder ROLLBACK bei Fehler
```

### ❌ Fehler: UNION ohne gleiche Spaltenanzahl

```sql
-- Fehler: 2 Spalten vs 3 Spalten!
SELECT first_name, last_name FROM customers
UNION
SELECT first_name, last_name, email FROM employees;
```

✅ **Gleiche Anzahl + kompatible Typen:**

```sql
SELECT first_name, last_name, email FROM customers
UNION
SELECT first_name, last_name, email FROM employees;
```

---

## 12. Weiterführende Themen

**Diese Themen wurden in den Lectures behandelt:**

- ✅ **SET Operations** (L13) – UNION, INTERSECT, EXCEPT
- ✅ **Views** (L13) – Virtuelle Tabellen, Materialized Views
- ✅ **Transaktionen & ACID** (L14) – BEGIN, COMMIT, ROLLBACK, Isolation Levels
- ✅ **Functions** (L15) – Stored Functions, IF/CASE, RAISE
- ✅ **Trigger** (L15) – Automatische Reaktionen auf Events

**Weitere fortgeschrittene Themen:**

- **Subqueries & CTEs** (Common Table Expressions)
- **Window Functions** (ROW_NUMBER, RANK, LAG, LEAD)
- **Recursive Queries** (Hierarchien, Graphen)
- **Full-Text Search** (tsvector, tsquery)
- **JSON Operations** (JSON_AGG, JSONB)
- **Performance Tuning** (EXPLAIN, Indexstrategien)
- **Partitioning** (Tabellen-Partitionierung)

---

## 13. Quick-Links zur Vorlesung

- **L7:** [SQL Introduction & SELECT](./7-lecture.md)
- **L8:** [DDL & DML](./8-lecture.md)
- **L9:** [Normalisierung](./9-lecture.md)
- **L10:** [Joins & Combining Data](./10-lecture.md)
- **L13:** [SET Operations & Views](./13-lecture.md)
- **L14:** [Transaktionen & ACID](./14-lecture.md)
- **L15:** [Functions & Trigger](./15-lecture.md)

---

## 📚 Zusätzliche Ressourcen

- [SQL Standard (ISO/IEC 9075)](https://www.iso.org/standard/76583.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [DB-Fiddle (Online SQL Editor)](https://www.db-fiddle.com/)

---

🎉 **Happy Querying!** Nutze dieses Cheat-Sheet als schnelle Referenz während der Übungen und Projekte!
