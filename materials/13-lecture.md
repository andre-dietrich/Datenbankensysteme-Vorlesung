<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  2.0.0
language: de
narrator: Deutsch Female

logo:     ../assets/img/logo/13-lecture.jpg

comment:  Advanced SQL: SET Operations & Views – Mengenlehre und Abstraktion für wiederverwendbare Queries im E-Commerce-Kontext

@style
.lia-effect__circle {
  display: none !important;
}

details {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.5em;
  margin: 1em 0;
}

summary {
  font-weight: bold;
  cursor: pointer;
  padding: 0.5em;
}

details[open] summary {
  border-bottom: 1px solid #ccc;
  margin-bottom: 0.5em;
}
@end

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md

-->

# L13: Advanced SQL – SET Operations & Views

> **Session 13 – Lecture**  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)  
> **Block:** 3 – SQL Vertiefung

    --{{0}}--
Willkommen zur dreizehnten Session! In den letzten Sessions haben Sie gelernt, wie man Daten mit Joins kombiniert, Aggregationen durchführt und mit Subqueries arbeitet. Heute erweitern wir Ihr SQL-Toolkit um zwei mächtige Konzepte: SET Operations und Views.

    --{{1}}--
SET Operations erlauben es uns, Ergebnismengen mathematisch zu kombinieren – wie Vereinigung, Schnittmenge und Differenz aus der Mengenlehre. Views hingegen geben uns die Möglichkeit, komplexe Queries als wiederverwendbare virtuelle Tabellen zu speichern.

    --{{2}}--
Wir arbeiten heute mit unserem bekannten E-Commerce-Schema aus Session 10 und erweitern es um eine neue Tabelle: Mitarbeiter. Denn stellen Sie sich vor: Einige Ihrer Mitarbeiter bestellen auch privat im Shop – und genau hier kommen SET Operations ins Spiel!

## Datenbank-Setup: Online-Shop erweitert

    --{{0}}--
Bevor wir loslegen, initialisieren wir unsere Datenbank. Wir nutzen das bekannte E-Commerce-Schema und fügen eine neue Tabelle hinzu: Mitarbeiter.

```sql
-- Locations: Normalisierte Orte mit PLZ
CREATE TABLE locations (
  location_id INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  postal_code TEXT NOT NULL,
  country TEXT DEFAULT 'Germany'
);

-- Categories: Normalisierte Produktkategorien
CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY,
  category_name TEXT NOT NULL UNIQUE,
  description TEXT
);

-- Customers: Erweitert mit strukturierten Adressdaten
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE,
  street TEXT,
  street_number TEXT,
  location_id INTEGER REFERENCES locations(location_id)
);

-- Orders: Kundenbestellungen
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(customer_id),
  order_date DATE,
  total_amount DECIMAL(10,2),
  status TEXT
);

-- Products: Produktkatalog
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT NOT NULL,
  price DECIMAL(10,2)
);

-- Product_Categories: N:M Beziehung zwischen Produkten und Kategorien
CREATE TABLE product_categories (
  product_id INTEGER REFERENCES products(product_id),
  category_id INTEGER REFERENCES categories(category_id),
  PRIMARY KEY (product_id, category_id)
);

-- Order_Items: Bestellpositionen
CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER REFERENCES orders(order_id),
  product_id INTEGER REFERENCES products(product_id),
  quantity INTEGER,
  line_total DECIMAL(10,2)
);

-- NEU: Employees – Mitarbeitertabelle
CREATE TABLE employees (
  employee_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE,
  department TEXT,
  hire_date DATE
);

-- Sample Data: Locations
INSERT INTO locations(location_id, city, postal_code, country) VALUES
  (1, 'Berlin', '10115', 'Germany'),
  (2, 'Hamburg', '20095', 'Germany'),
  (3, 'Munich', '80331', 'Germany'),
  (4, 'Cologne', '50667', 'Germany');

-- Sample Data: Categories
INSERT INTO categories(category_id, category_name, description) VALUES
  (1, 'Electronics', 'Electronic devices and accessories'),
  (2, 'Furniture', 'Office and home furniture'),
  (3, 'Stationery', 'Paper products and writing supplies'),
  (4, 'Office Equipment', 'Printers, scanners, and office machines');

-- Sample Data: Customers (erweitert)
INSERT INTO customers(customer_id, first_name, last_name, email, street, street_number, location_id) VALUES
  (1, 'Alice', 'Smith', 'alice.smith@example.com', 'Main Street', '42', 1),
  (2, 'Bob', 'Johnson', 'bob.johnson@example.com', 'Oak Avenue', '15', 2),
  (3, 'Carol', 'Williams', 'carol.williams@example.com', 'Elm Road', '8', 1),
  (4, 'David', 'Lee', 'david.lee@example.com', 'Maple Lane', '23', 3),
  (5, 'Emma', 'Brown', 'emma.brown@example.com', 'Pine Street', '7', 4);

-- Sample Data: Employees (einige überlappen mit Customers!)
INSERT INTO employees(employee_id, first_name, last_name, email, department, hire_date) VALUES
  (1, 'Alice', 'Smith', 'alice.smith@shop-corp.com', 'Sales', '2020-03-15'),
  (2, 'David', 'Lee', 'david.lee@shop-corp.com', 'IT', '2019-07-01'),
  (3, 'Frank', 'Wilson', 'frank.wilson@shop-corp.com', 'HR', '2021-11-20'),
  (4, 'Grace', 'Taylor', 'grace.taylor@shop-corp.com', 'Marketing', '2022-02-14'),
  (5, 'Hannah', 'Martinez', 'hannah.martinez@shop-corp.com', 'Finance', '2020-09-10');

-- Sample Data: Orders
INSERT INTO orders(order_id, customer_id, order_date, total_amount, status) VALUES
  (101, 1, '2024-01-15', 299.99, 'delivered'),
  (102, 1, '2024-02-20', 139.97, 'delivered'),
  (103, 2, '2024-01-22', 999.99, 'delivered'),
  (104, 3, '2024-03-01', 749.94, 'processing'),
  (105, 4, '2024-02-10', 199.99, 'delivered');

-- Sample Data: Products
INSERT INTO products(product_id, product_name, price) VALUES
  (1, 'Laptop', 999.99),
  (2, 'Mouse', 29.99),
  (3, 'Keyboard', 79.99),
  (4, 'Monitor', 299.99),
  (5, 'Desk Chair', 199.99),
  (6, 'Notebook', 9.99),
  (7, 'USB Cable', 14.99),
  (8, 'Desk Lamp', 39.99),
  (9, 'Paper (500 sheets)', 12.99);

-- Sample Data: Product Categories (N:M Beziehungen)
INSERT INTO product_categories(product_id, category_id) VALUES
  (1, 1),  -- Laptop → Electronics
  (2, 1),  -- Mouse → Electronics
  (3, 1),  -- Keyboard → Electronics
  (4, 1),  -- Monitor → Electronics
  (4, 4),  -- Monitor → Office Equipment
  (5, 2),  -- Desk Chair → Furniture
  (5, 4),  -- Desk Chair → Office Equipment
  (6, 3),  -- Notebook → Stationery
  (7, 1),  -- USB Cable → Electronics
  (8, 2),  -- Desk Lamp → Furniture
  (8, 4),  -- Desk Lamp → Office Equipment
  (9, 3);  -- Paper → Stationery

-- Sample Data: Order Items
INSERT INTO order_items(order_item_id, order_id, product_id, quantity, line_total) VALUES
  (1, 101, 4, 1, 299.99),
  (2, 102, 2, 2,  59.98),
  (3, 102, 3, 1,  79.99),
  (4, 103, 1, 1, 999.99),
  (5, 104, 6, 5,  49.95),
  (6, 104, 5, 1, 199.99),
  (7, 105, 5, 1, 199.99);
```
@PGlite.eval(online-shop)

    {{1}}
**Schema-Übersicht:**

    {{1}}
``` sql @dbdiagram
Table locations {
  location_id int [pk]
  city varchar [not null]
  postal_code varchar [not null]
  country varchar [default: 'Germany']
}

Table categories {
  category_id int [pk]
  category_name varchar [not null, unique]
  description varchar
}

Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int [ref: > locations.location_id]
}

Table employees {
  employee_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  department varchar
  hire_date date
  Note: "Einige Mitarbeiter sind auch Kunden!"
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}

Table products {
  product_id int [pk]
  product_name varchar [not null]
  price decimal(10,2)
}

Table product_categories {
  product_id int [ref: > products.product_id]
  category_id int [ref: > categories.category_id]
  indexes {
    (product_id, category_id) [pk]
  }
}

Table order_items {
  order_item_id int [pk]
  order_id int [ref: > orders.order_id]
  product_id int [ref: > products.product_id]
  quantity int
  line_total decimal(10,2)
}
```

    --{{2}}--
Beachten Sie die neue Employees-Tabelle! Alice Smith und David Lee sind sowohl Kunden als auch Mitarbeiter – das werden wir gleich nutzen, um SET Operations zu demonstrieren.

## Motivation & Kontext

    --{{0}}--
Stellen Sie sich folgende Business-Szenarien vor:

    {{1}}
**Szenario 1: Newsletter-Kampagne**

    --{{1}}--
Ihr Marketing-Team möchte einen Newsletter versenden – an ALLE Personen in Ihrer Datenbank: Kunden UND Mitarbeiter. Wie kombinieren Sie diese beiden Listen effizient?

    {{2}}
**Szenario 2: Mitarbeiter-Rabatt-Programm**

    --{{2}}--
Sie möchten herausfinden, welche Mitarbeiter AUCH als Kunden bei Ihnen einkaufen, um ihnen spezielle Mitarbeiter-Rabatte anzubieten. Wie identifizieren Sie Überschneidungen?

    {{3}}
**Szenario 3: Komplexe Analysen wiederverwenden**

    --{{3}}--
Ihre Analyse-Queries für "VIP-Kunden" und "Aktive Kunden" werden immer länger und müssen in mehreren Reports verwendet werden. Wie vermeiden Sie Code-Duplikation?

    --{{4}}--
Die Antworten liegen in zwei mächtigen SQL-Features: SET Operations für Mengen-Kombinationen und Views für Query-Wiederverwendung. Beginnen wir mit SET Operations!

## Teil 1: SET Operations – Mengenlehre für SQL

    --{{0}}--
SET Operations basieren direkt auf mathematischen Mengenoperationen. Wenn Sie Venn-Diagramme aus der Schule kennen, werden Sie diese intuitiv verstehen.

### Überblick: Die drei SET Operations

    --{{0}}--
SQL bietet drei Haupt-SET-Operations: UNION, INTERSECT und EXCEPT. Jede löst ein spezifisches Problem.

    {{1}}
```ascii
    Venn-Diagramme für SET Operations:

    UNION (Vereinigung)        INTERSECT (Schnittmenge)    EXCEPT (Differenz)
    
    +-------+-------+            +-------+-------+            +-------+-------+
    |       |       |            |       |       |            |       |       |
    |   A   |   B   |            |   A   | A∩B   |  B         |   A   |       |  B
    |#######│#######|            |       │#######│            |#######│       │       |
    |       |       |            |       |       |            |       |       |
    +-------+-------+            +-------+-------+            +-------+-------+
    
    Alle Elemente aus A oder B   Nur gemeinsame Elemente    Nur Elemente aus A
                                  von A und B                (nicht in B)
```

    {{2}}
| Operation | Bedeutung | Use Case |
|-----------|-----------|----------|
| **UNION** | Vereinigung beider Mengen | Newsletter an Kunden UND Mitarbeiter |
| **INTERSECT** | Nur gemeinsame Elemente | Mitarbeiter, die auch Kunden sind |
| **EXCEPT** | Nur Elemente aus A, nicht in B | Kunden, die KEINE Mitarbeiter sind |

    --{{3}}--
Schauen wir uns jede Operation im Detail an, beginnend mit UNION.

### UNION – Vereinigung von Mengen

    --{{0}}--
UNION kombiniert die Ergebnisse zweier SELECT-Statements zu einer einzigen Ergebnismenge. Duplikate werden automatisch entfernt – es sei denn, Sie verwenden UNION ALL.

    {{1}}
**Syntax:**

    {{1}}
```sql
SELECT spalten FROM tabelle1
UNION [ALL]
SELECT spalten FROM tabelle2;
```

    {{2}}
**Wichtige Regeln:**

    {{2}}
- Beide SELECT-Statements müssen die **gleiche Anzahl** von Spalten haben
- Spaltentypen müssen **kompatibel** sein (oder konvertierbar)
- **UNION** entfernt Duplikate → langsamer
- **UNION ALL** behält Duplikate → schneller

    --{{3}}--
Lassen Sie uns das praktisch demonstrieren. Wir kombinieren Kunden und Mitarbeiter für eine Newsletter-Liste.

    {{3}}
**Beispiel 1: Newsletter-Liste erstellen**

    {{3}}
```sql
-- UNION: Alle Personen (Kunden + Mitarbeiter) ohne Duplikate
-- Problem: E-Mail-Adressen sind unterschiedlich (@example.com vs @shop-corp.com)
-- Lösung: Nur Name vergleichen, nicht E-Mail!
SELECT 
  first_name,
  last_name
FROM customers

UNION

SELECT 
  first_name,
  last_name
FROM employees

ORDER BY last_name, first_name;
```
@PGlite.eval(online-shop)

    {{4}}
**Was sehen Sie?**

    --{{4}}--
Jetzt sehen Sie 8 Personen statt 10! Alice Smith und David Lee erscheinen nur einmal. Warum? UNION vergleicht ALLE Spalten – hier nur first_name und last_name. Da beide Personen in beiden Tabellen vorkommen (gleicher Name), werden die Duplikate entfernt!

    --{{4}}--
Wichtig: Wenn wir email mit einbeziehen würden, wären Alice und David KEINE Duplikate, weil ihre E-Mail-Adressen unterschiedlich sind (alice.smith@example.com vs alice.smith@shop-corp.com)!

    {{5}}
**UNION ALL – Alle Einträge behalten:**

    {{5}}
```sql
-- UNION ALL: Behält ALLE Einträge (keine Deduplizierung)
SELECT 
  first_name,
  last_name,
  'Customer' AS type
FROM customers

UNION ALL

SELECT 
  first_name,
  last_name,
  'Employee' AS type
FROM employees

ORDER BY last_name, first_name;
```
@PGlite.eval(online-shop)

    --{{6}}--
Jetzt sehen Sie 10 Zeilen! Alice und David erscheinen zweimal – einmal als Customer, einmal als Employee. UNION ALL ist schneller, weil keine Deduplizierung nötig ist.

    {{6}}
**Warum E-Mail-Adressen problematisch sind:**

    {{6}}
```sql
-- UNION mit E-Mail: Keine Deduplizierung wegen unterschiedlicher E-Mails!
SELECT 
  first_name,
  last_name,
  email
FROM customers

UNION

SELECT 
  first_name,
  last_name,
  email
FROM employees

ORDER BY last_name, first_name;
```
@PGlite.eval(online-shop)

    --{{7}}--
Überraschung: Wieder 10 Zeilen! Warum? UNION vergleicht ALLE Spalten. Obwohl Alice Smith in beiden Tabellen vorkommt, sind die E-Mails unterschiedlich (alice.smith@example.com vs alice.smith@shop-corp.com) – also keine Deduplizierung! Wenn Sie nur eindeutige Personen wollen, vergleichen Sie nur die Spalten, die wirklich identisch sein müssen (z.B. nur Name).

    {{8}}
**Performance-Tipp:**

    {{8}}
> Nutzen Sie **UNION ALL**, wenn Sie wissen, dass keine Duplikate existieren oder Duplikate gewünscht sind. Das spart die kostspielige Deduplizierung!

### INTERSECT – Schnittmenge finden

    --{{0}}--
INTERSECT gibt nur die Zeilen zurück, die in BEIDEN Ergebnismengen vorkommen. Perfekt, um Gemeinsamkeiten zu identifizieren.

    {{1}}
**Syntax:**

    {{1}}
```sql
SELECT spalten FROM tabelle1
INTERSECT
SELECT spalten FROM tabelle2;
```

    --{{2}}--
Unser Business-Szenario: Finden Sie alle Mitarbeiter, die auch als Kunden im Shop einkaufen, um ihnen Mitarbeiter-Rabatte anzubieten.

    {{2}}
**Beispiel 2: Mitarbeiter-Kunden identifizieren**

    {{2}}
```sql
-- Mitarbeiter, die auch Kunden sind (basierend auf Namen)
SELECT 
  first_name,
  last_name
FROM customers

INTERSECT

SELECT 
  first_name,
  last_name
FROM employees

ORDER BY last_name;
```
@PGlite.eval(online-shop)

    {{3}}
**Ergebnis:**

    --{{3}}--
Nur Alice Smith und David Lee erscheinen! Das sind exakt die Personen, die in beiden Tabellen vorkommen (gleicher Name). Perfekt für unser Mitarbeiter-Rabatt-Programm. Beachten Sie: Wir vergleichen nur Namen, nicht E-Mails, da diese unterschiedlich sein können!

    {{4}}
**Alternative mit JOIN:**

    --{{4}}--
Man könnte das auch mit einem JOIN lösen, aber INTERSECT ist oft lesbarer für diesen spezifischen Use-Case.

    {{4}}
```sql
-- Gleichwertig mit INNER JOIN
SELECT DISTINCT
  c.first_name,
  c.last_name,
  c.email
FROM customers c
INNER JOIN employees e 
  ON c.first_name = e.first_name 
  AND c.last_name = e.last_name
ORDER BY c.last_name;
```
@PGlite.eval(online-shop)

    --{{5}}--
Beide Queries liefern das gleiche Ergebnis, aber INTERSECT macht die Intention klarer: "Zeige mir die Überschneidung!"

### EXCEPT – Differenz finden

    --{{0}}--
EXCEPT gibt die Zeilen aus der ersten Ergebnismenge zurück, die NICHT in der zweiten vorkommen. Ideal, um "fehlende" oder "exklusive" Datensätze zu identifizieren.

    {{1}}
**Syntax:**

    {{1}}
```sql
SELECT spalten FROM tabelle1
EXCEPT
SELECT spalten FROM tabelle2;
```

    --{{2}}--
Business-Szenario: Finden Sie alle Kunden, die KEINE Mitarbeiter sind, für eine reine Kunden-Marketing-Kampagne.

    {{2}}
**Beispiel 3: Reine Kunden identifizieren**

    {{2}}
```sql
-- Kunden, die KEINE Mitarbeiter sind
SELECT 
  first_name, (basierend auf Namen)
SELECT 
  first_name,
  last_name
FROM customers

EXCEPT

SELECT 
  first_name,
  last_name
FROM employees

ORDER BY last_name;
```
@PGlite.eval(online-shop)

    {{3}}
**Ergebnis:**

    --{{3}}--
Nur Bob, Carol und Emma erscheinen – die drei Kunden, die NICHT in der Mitarbeiter-Tabelle sind (basierend auf Namen). Alice und David werden herausgefiltert, weil sie auch als Mitarbeiter existieren
**Alternative mit LEFT JOIN:**

    --{{4}}--
EXCEPT kann auch mit einem Anti-Join (LEFT JOIN + NULL Check) gelöst werden.

    {{4}}
```sql
-- Gleichwertig mit LEFT JOIN + NULL
SELECT 
  c.first_name,
  c.last_name,
  c.email
FROM customers c
LEFT JOIN employees e 
  ON c.first_name = e.first_name 
  AND c.last_name = e.last_name
WHERE e.employee_id IS NULL
ORDER BY c.last_name;
```
@PGlite.eval(online-shop)

    --{{5}}--
Wieder: Beide Ansätze funktionieren, aber EXCEPT ist semantisch klarer für "Zeige mir A ohne B".

    {{6}}
**Wichtig: Reihenfolge zählt!**

    --{{6}}--
EXCEPT ist nicht kommutativ! A EXCEPT B ist NICHT das gleiche wie B EXCEPT A.

    {{6}}
```sql
-- Umgekehrt: Mitarbeiter, die KEINE Kunden sind
SELECT first_name, last_name, email FROM employees
EXCEPT
SELECT first_name, last_name, email FROM customers
ORDER BY last_name;
```
@PGlite.eval(online-shop)

    --{{7}}--
Jetzt sehen Sie Frank, Grace und Hannah – die drei Mitarbeiter, die nicht in der Kunden-Tabelle sind!

### Komplexes Beispiel: Produkte ohne Verkäufe

    --{{0}}--
Ein sehr praktisches Beispiel: Finden Sie alle Produkte, die noch NIE verkauft wurden. Das sind Ihre "Ladenhüter", die Sie vielleicht aus dem Sortiment nehmen oder bewerben sollten.

    {{1}}
```sql
-- Produkte, die noch nie verkauft wurden
SELECT 
  product_id,
  product_name,
  price
FROM products

EXCEPT

SELECT 
  p.product_id,
  p.product_name,
  p.price
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id

ORDER BY product_name;
```
@PGlite.eval(online-shop)

    {{2}}
**Ergebnis:**

    --{{2}}--
USB Cable, Desk Lamp und Paper wurden nie verkauft! Das ist wertvolle Business-Intelligence. Schauen wir uns die Alternative mit LEFT JOIN an.

    {{3}}
```sql
-- Alternative: LEFT JOIN + NULL Check
SELECT 
  p.product_id,
  p.product_name,
  p.price
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL
ORDER BY p.product_name;
```
@PGlite.eval(online-shop)

    --{{4}}--
Identisches Ergebnis! Welche Variante ist besser? Das hängt von der Datenbank und den Indizes ab. Bei modernen Datenbanken sind beide meist gleich schnell.

### Performance & Best Practices

    --{{0}}--
SET Operations haben ihre eigenen Performance-Charakteristika. Hier sind die wichtigsten Punkte.

    {{1}}
**Performance-Matrix:**

    {{1}}
| Operation | Sortierung nötig? | Deduplizierung? | Performance-Tipp |
|-----------|-------------------|-----------------|------------------|
| UNION | Ja | Ja | Nutze UNION ALL wenn möglich |
| UNION ALL | Nein | Nein | Schnellste Option |
| INTERSECT | Ja | Ja | Hash-Algorithmus effizient |
| EXCEPT | Ja | Ja | Anti-Join Alternative prüfen |

    {{2}}
**Best Practices:**

    {{2}}
- ✅ **UNION ALL statt UNION**, wenn Duplikate OK sind
- ✅ **Spalten-Typen kompatibel halten** – implizite Konvertierungen vermeiden
- ✅ **Indexe auf Join-Spalten** setzen (bei der Alternative mit JOINs)
- ✅ **EXPLAIN ANALYZE nutzen**, um Performance zu vergleichen
- ⚠️ **Große Mengen vorsichtig** – SET Ops können Sorts auslösen
- ⚠️ **WHERE-Filter VOR SET Ops** anwenden, um Datenmenge zu reduzieren

    {{3}}
**Performance-Optimierung:**

    {{3}}
```sql
-- ❌ Ineffizient: Große Mengen erst kombinieren, dann filtern
SELECT *
FROM (
  SELECT first_name, last_name, email FROM customers
  UNION
  SELECT first_name, last_name, email FROM employees
)
WHERE last_name LIKE 'S%';  -- Filter NACH UNION

-- ✅ Besser: Erst filtern, dann kombinieren
SELECT first_name, last_name, email 
FROM customers 
WHERE last_name LIKE 'S%'
UNION
SELECT first_name, last_name, email 
FROM employees 
WHERE last_name LIKE 'S%';
```
@PGlite.eval(online-shop)

    --{{4}}--
Durch frühes Filtern reduzieren wir die Datenmengen vor der UNION – das spart Ressourcen!

## Teil 2: Views – Abstraktion & Wiederverwendung

    --{{0}}--
Nachdem wir SET Operations gemeistert haben, kommen wir zu Views. Views lösen ein anderes Problem: Code-Wiederverwendung und Abstraktion komplexer Queries.

### Was sind Views?

    --{{0}}--
Eine View ist eine gespeicherte SELECT-Query, die wie eine Tabelle abgefragt werden kann – aber keine eigenen Daten speichert. Man nennt sie auch "virtuelle Tabelle".

    {{1}}
**Konzept:**

    {{1}}
```sql
CREATE VIEW view_name AS
SELECT spalten
FROM tabellen
WHERE bedingungen;

-- Dann wie eine Tabelle nutzen:
SELECT * FROM view_name;
```

    {{2}}
**Wichtige Eigenschaften:**

    {{2}}
- ❌ **Keine Datenspeicherung** – Views speichern nur die Query-Definition
- ✅ **Immer aktuell** – Daten werden bei jeder Abfrage neu gelesen
- ✅ **Code-Wiederverwendung** – Komplexe Queries einmal definieren
- ✅ **Zugriffskontrolle** – Beschränkung auf bestimmte Spalten/Zeilen
- ⚠️ **Performance** – Views sind so schnell (oder langsam) wie die zugrundeliegende Query

### Einfache Views erstellen

    --{{0}}--
Beginnen wir mit einem einfachen Beispiel: Eine View für alle VIP-Kunden (die mehr als 500€ ausgegeben haben).

    {{1}}
```sql
-- View für VIP-Kunden erstellen
CREATE VIEW vip_customers AS
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email,
  SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING SUM(o.total_amount) > 500;

-- View abfragen
SELECT * FROM vip_customers ORDER BY total_spent DESC;
```
@PGlite.eval(online-shop)

    {{2}}
**Was sehen Sie?**

    --{{2}}--
Alice (439.96€) und Bob (999.99€) sind unsere VIP-Kunden! Die komplexe Query mit JOIN, GROUP BY und HAVING ist jetzt in einer View gekapselt. Sie können sie beliebig oft wiederverwenden, ohne den Code zu duplizieren.

    {{3}}
**Views weiter filtern:**

    --{{3}}--
Das Schöne: Sie können Views wie normale Tabellen behandeln – filtern, sortieren, joinen!

    {{3}}
```sql
-- View weiter filtern
SELECT 
  first_name,
  last_name,
  total_spent
FROM vip_customers
WHERE total_spent > 400
ORDER BY last_name;
```
@PGlite.eval(online-shop)

    --{{4}}--
Die Datenbank kombiniert intern Ihre Filter mit der View-Definition – das nennt man "View Merging". Moderne Datenbanken sind hier sehr effizient!

### Views für häufige Analysen

    --{{0}}--
Views sind ideal, um wiederkehrende Analyse-Queries zu speichern. Schauen wir uns weitere praktische Beispiele an.

    {{1}}
**View für Produktkategorien:**

    {{1}}
```sql
-- View: Produkte mit ihren Kategorien (N:M Beziehung aufgelöst)
CREATE VIEW products_with_categories AS
SELECT 
  p.product_id,
  p.product_name,
  p.price,
  c.category_name,
  c.description AS category_description
FROM products p
INNER JOIN product_categories pc ON p.product_id = pc.product_id
INNER JOIN categories c ON pc.category_id = c.category_id;

-- View nutzen
SELECT * FROM products_with_categories 
ORDER BY category_name, product_name;
```
@PGlite.eval(online-shop)

    {{2}}
**View für aktive Kunden:**

    {{2}}
```sql
-- View: Kunden mit Bestellungen in 2024
CREATE VIEW active_customers_2024 AS
SELECT DISTINCT
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email,
  l.city
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN locations l ON c.location_id = l.location_id
WHERE EXTRACT(YEAR FROM o.order_date) = 2024;

-- View nutzen
SELECT * FROM active_customers_2024 ORDER BY city, last_name;
```
@PGlite.eval(online-shop)

    --{{3}}--
Diese View kapselt die Logik für "aktive Kunden" – alle Reports können sie wiederverwenden!

### Views & SET Operations kombinieren

    --{{0}}--
Jetzt wird es mächtig! Wir können SET Operations in Views einbetten und Views mit SET Operations kombinieren.

    {{1}}
**View mit UNION – Alle Kontakte:**

    {{1}}
```sql
-- View: Alle Personen (Kunden + Mitarbeiter)
CREATE VIEW all_contacts AS
  SELECT 
    customer_id AS person_id,
    first_name,
    last_name,
    email,
    'Customer' AS type
  FROM customers
  
  UNION ALL
  
  SELECT 
    employee_id AS person_id,
    first_name,
    last_name,
    email,
    'Employee' AS type
  FROM employees;

-- View abfragen
SELECT * FROM all_contacts ORDER BY last_name, first_name;
```
@PGlite.eval(online-shop)

    {{2}}
**Vorteil:**

    --{{2}}--
Die UNION-Logik ist jetzt wiederverwendbar! Jeder Report, der alle Kontakte braucht, kann einfach FROM all_contacts selektieren.

    {{3}}
**Views kombinieren:**

    {{3}}
```sql
-- Zwei separate Views für verschiedene Analysen
CREATE VIEW customers_berlin AS
SELECT c.*, l.city
FROM customers c
INNER JOIN locations l ON c.location_id = l.location_id
WHERE l.city = 'Berlin';

CREATE VIEW employees_sales AS
SELECT *
FROM employees
WHERE department = 'Sales';

-- Views mit UNION kombinieren
SELECT first_name, last_name, 'Customer' AS type FROM customers_berlin
UNION ALL
SELECT first_name, last_name, 'Employee' AS type FROM employees_sales
ORDER BY last_name;
```
@PGlite.eval(online-shop)

    --{{4}}--
Alice erscheint zweimal: Als Berliner Kundin und als Sales-Mitarbeiterin. Jede View kann unabhängig gewartet werden!

### Views für Zugriffskontrolle

    --{{0}}--
Ein wichtiger Use-Case für Views ist die Zugriffskontrolle. Sie können sensible Daten verbergen oder nur bestimmte Zeilen/Spalten freigeben.

    {{1}}
**Szenario: Public vs. Internal Data**

    {{1}}
```sql
-- View für öffentliche Produktdaten (ohne Preise)
CREATE VIEW public_products AS
SELECT 
  product_id,
  product_name
FROM products;

-- View für interne Analysten (mit Preisen)
CREATE VIEW internal_products AS
SELECT 
  product_id,
  product_name,
  price
FROM products;

-- Externe API würde nur public_products sehen:
SELECT * FROM public_products;
```
@PGlite.eval(online-shop)

    {{2}}
**Zugriffskontrolle in Praxis:**

    --{{2}}--
In echten Systemen würden Sie Datenbank-Permissions setzen: Externe User bekommen nur Zugriff auf public_products, interne auf internal_products. Die Basistabelle products bleibt geschützt!

    {{3}}
**View für gefilterte Daten:**

    {{3}}
```sql
-- View: Nur abgeschlossene Bestellungen
CREATE VIEW delivered_orders AS
SELECT 
  order_id,
  customer_id,
  order_date,
  total_amount
FROM orders
WHERE status = 'delivered';

-- Reports nutzen nur gelieferte Bestellungen
SELECT * FROM delivered_orders;
```
@PGlite.eval(online-shop)

    --{{4}}--
Der Report-User sieht nur fertige Bestellungen – egal ob versehentlich oder absichtlich, unfertige Bestellungen sind nicht zugänglich.

### Views verwalten

    --{{0}}--
Wie erstellt, ändert und löscht man Views? Hier die wichtigsten Operationen.

    {{1}}
**View erstellen oder ersetzen:**

    {{1}}
```sql
-- Neue View erstellen
CREATE VIEW my_view AS SELECT ...;

-- View ersetzen (falls existiert)
-- In PGlite: DROP + CREATE
DROP VIEW IF EXISTS my_view;
CREATE VIEW my_view AS SELECT ...;
```

    {{2}}
**View löschen:**

    {{2}}
```sql
-- View löschen
DROP VIEW IF EXISTS my_view;

-- Mehrere Views löschen
DROP VIEW IF EXISTS view1, view2, view3;
```

    {{3}}
**Best Practices für View-Management:**

    {{3}}
- ✅ **Benennungskonvention** nutzen (z.B. `vw_` Präfix oder `_view` Suffix)
- ✅ **Views dokumentieren** (Kommentare im SQL, README)
- ✅ **Views versionieren** (wie Code in Git)
- ✅ **Views testen** mit realistischen Datenmengen
- ⚠️ **View-Hierarchien begrenzen** (max. 2-3 Ebenen)
- ⚠️ **Verwaiste Views vermeiden** (regelmäßig aufräumen)

### Materialized Views – Performance durch Caching

    --{{0}}--
Standard-Views sind virtuelle Tabellen ohne eigene Datenspeicherung. Bei jeder Abfrage wird die zugrundeliegende Query neu ausgeführt. Materialized Views hingegen speichern das Ergebnis physisch – wie ein Snapshot.

    {{1}}
**Materialized View erstellen:**

    {{1}}
```sql
CREATE VIEW vw_vip_customers AS
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  SUM(o.total_amount) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > 500;

-- Materialized View für VIP-Kunden (Ausgaben > 500€)
CREATE MATERIALIZED VIEW mv_vip_customers AS
SELECT * FROM vw_vip_customers;

-- Abfragen wie eine normale Tabelle
SELECT * FROM mv_vip_customers ORDER BY total_spent DESC;
```
@PGlite.eval(online-shop)

    --{{2}}--
Alice und Bob sind unsere VIP-Kunden mit 439.96€ und 999.99€! Die Daten sind jetzt physisch gespeichert – nicht nur als Query-Definition.

    {{2}}
**Das Problem: Veraltete Daten nach Updates**

    --{{2}}--
Fügen wir eine neue Bestellung für Alice hinzu – was passiert mit der Materialized View?

    {{2}}
```sql
-- Neue Bestellung für Alice (wird zum VIP)
INSERT INTO orders(order_id, customer_id, order_date, total_amount, status)
VALUES (106, 1, '2024-03-20', 199.99, 'delivered');

-- Prüfe direkt in orders: Alice hat jetzt mehr ausgegeben
SELECT * FROM vw_vip_customers;

-- ABER: Materialized View zeigt noch alte Werte!
SELECT * FROM mv_vip_customers;
```
@PGlite.eval(online-shop)

    --{{3}}--
Sehen Sie das Problem? Die echte Abfrage zeigt 639.95€ für Alice, aber die Materialized View zeigt noch 439.96€! Materialized Views werden NICHT automatisch aktualisiert.

    {{3}}
**Lösung: REFRESH MATERIALIZED VIEW**

    {{3}}
```sql
-- Materialized View manuell aktualisieren
REFRESH MATERIALIZED VIEW mv_vip_customers;

-- Jetzt sind die Daten aktuell!
SELECT * FROM mv_vip_customers ORDER BY total_spent DESC;
```
@PGlite.eval(online-shop)

    --{{4}}--
Nach dem REFRESH zeigt die Materialized View die aktuellen Werte! Alice hat jetzt 639.95€ insgesamt.


### Performance-Überlegungen

    --{{0}}--
Views sind praktisch, aber haben Performance-Implikationen. Hier die wichtigsten Punkte.

    {{1}}
**Performance-Fakten:**

    {{1}}
- Views speichern **keine Daten** → kein zusätzlicher Speicher
- Views nutzen **Indexe der Basistabellen** → keine eigenen Indexe
- Views werden bei **jeder Abfrage neu ausgeführt** → keine Caching
- Moderne DBs nutzen **View Merging** → Filter werden optimiert

    {{2}}
**Wann Views langsam werden:**

    {{2}}
| Problem                | Symptom                   | Lösung                        |
| ---------------------- | ------------------------- | ----------------------------- |
| Komplexe Aggregationen | Langsame Abfragen         | Materialized View erwägen     |
| Viele Joins (5+)       | Lange Laufzeit            | Query-Optimierung, Indexe     |
| Views auf Views (tief) | Verschachtelte Executions | Flachere Hierarchie           |
| Große Datenmengen      | Timeouts                  | WHERE-Filter, Partitionierung |

    {{3}}
**Performance prüfen:**

    {{3}}
```sql
-- Query Plan für View analysieren
EXPLAIN QUERY PLAN
SELECT * FROM vip_customers WHERE total_spent > 400;
```
@PGlite.eval(online-shop)

    --{{4}}--
Der Query Plan zeigt Ihnen, wie die Datenbank die View-Query + Ihre Filter kombiniert. Achten Sie auf Index-Nutzung und Scan-Methoden!

## Teil 3: Praktische Patterns & Best Practices

    --{{0}}--
Jetzt, wo Sie beide Konzepte kennen, schauen wir uns praktische Patterns an, die SET Operations und Views kombinieren.

### Pattern 1: Layered Views

    --{{0}}--
Strukturieren Sie Views in logischen Schichten – von Basis-Views bis zu Business-Logic-Views.

    {{1}}
```sql
-- Layer 1: Basis-Views (direkte Tabellenzugriffe)
CREATE VIEW base_customers AS
SELECT customer_id, first_name, last_name, email, location_id
FROM customers;

CREATE VIEW base_employees AS
SELECT employee_id, first_name, last_name, email, department
FROM employees;

-- Layer 2: Business-Logic Views
CREATE VIEW all_persons AS
  SELECT 
    customer_id AS person_id,
    first_name,
    last_name,
    email,
    'Customer' AS type,
    NULL AS department
  FROM base_customers
  UNION ALL
  SELECT 
    employee_id AS person_id,
    first_name,
    last_name,
    email,
    'Employee' AS type,
    department
  FROM base_employees;

-- Layer 3: Report-Views (User-facing)
CREATE VIEW berlin_persons AS
SELECT p.*
FROM all_persons p
WHERE type = 'Customer' 
  AND person_id IN (
    SELECT customer_id FROM customers c
    INNER JOIN locations l ON c.location_id = l.location_id
    WHERE l.city = 'Berlin'
  );

-- Reports nutzen Layer 3
SELECT * FROM berlin_persons;
```
@PGlite.eval(online-shop)

    --{{2}}--
Diese Architektur ist wartbar: Änderungen in Layer 1 propagieren automatisch nach oben, jede Schicht hat eine klare Verantwortung!

### Pattern 2: Views für Data Quality

    --{{0}}--
Nutzen Sie Views, um Datenqualitäts-Regeln zentral zu definieren.

    {{1}}
```sql
-- View: Nur valide Bestellungen
CREATE VIEW valid_orders AS
SELECT 
  o.*,
  c.first_name,
  c.last_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.total_amount > 0
  AND o.order_date IS NOT NULL
  AND o.status IN ('processing', 'delivered', 'shipped');

-- Alle Reports nutzen nur valide Daten
SELECT * FROM valid_orders;
```
@PGlite.eval(online-shop)

    --{{2}}--
Data-Quality-Regeln sind jetzt zentral! Ändern Sie die Definition in der View, und alle abhängigen Queries nutzen automatisch die neuen Regeln.

### Pattern 3: Views als API-Schicht

    --{{0}}--
Views können als stabile API für externe Systeme dienen – auch wenn sich das interne Schema ändert.

    {{1}}
```sql
-- API-View: Stabile Schnittstelle für externe Systeme
CREATE VIEW api_products AS
SELECT 
  product_id AS id,
  product_name AS name,
  price,
  CASE 
    WHEN price < 50 THEN 'Budget'
    WHEN price < 200 THEN 'Mid-Range'
    ELSE 'Premium'
  END AS price_category
FROM products;

-- Externe API liest nur aus dieser View
SELECT * FROM api_products;
```
@PGlite.eval(online-shop)

    --{{2}}--
Wenn Sie später die products-Tabelle umbenennen oder umstrukturieren, müssen Sie nur die View anpassen – externe Systeme merken nichts!

### Vergleichstabelle: Wann was?

    --{{0}}--
Fassen wir zusammen: Wann nutzen Sie SET Operations, wann Views?

    {{1}}
| Anforderung                    | Empfehlung                           | Begründung                 |
| ------------------------------ | ------------------------------------ | -------------------------- |
| Zwei Listen kombinieren        | **UNION / UNION ALL**                | Mengenvereinigung          |
| Überschneidungen finden        | **INTERSECT**                        | Schnittmenge               |
| Exklusive Elemente finden      | **EXCEPT** oder **LEFT JOIN + NULL** | Differenz                  |
| Query wiederverwenden          | **VIEW**                             | Code-Reuse                 |
| Komplexe Query kapseln         | **VIEW**                             | Abstraktion                |
| Zugriffskontrolle              | **VIEW**                             | Spalten/Zeilen beschränken |
| SET Ops wiederverwenden        | **VIEW mit SET Ops**                 | Beste aus beiden Welten    |
| Performance bei teuren Queries | **Materialized View** (andere DBs)   | Caching                    |

### Best Practices Cheat Sheet

    --{{0}}--
Abschließend die wichtigsten Best Practices auf einen Blick.

    {{1}}
**DO's:**

    {{1}}
- ✅ Nutze **UNION ALL** statt UNION, wenn Duplikate OK sind
- ✅ Nutze **Views** für wiederverwendbare Queries
- ✅ Nutze **klare Benennungskonventionen** (`vw_`, `_view`)
- ✅ **Dokumentiere** Views (Zweck, Author, Datum)
- ✅ Nutze **Views für Zugriffskontrolle**
- ✅ Kombiniere **SET Ops und Views** für Flexibilität
- ✅ **Teste Performance** mit realistischen Datenmengen
- ✅ Nutze **WHERE-Filter VOR SET Ops** (Performance)

    {{2}}
**DON'Ts:**

    {{2}}
- ❌ Keine **tiefen View-Hierarchien** (max. 2-3 Ebenen)
- ❌ Kein **SELECT *** in View-Definitionen (Wartbarkeit)
- ❌ Keine **vergessenen Views** (View Sprawl)
- ❌ Kein **UNION**, wenn UNION ALL reicht
- ❌ Keine **INTERSECT/EXCEPT**, wenn JOIN lesbarer ist
- ❌ Keine **ungetesteten Views** in Produktion

## Wrap-up & Zusammenfassung

    --{{0}}--
Fassen wir zusammen, was Sie heute gelernt haben.

    {{1}}
**SET Operations:**

    {{1}}
- **UNION** kombiniert Listen (mit oder ohne Duplikate)
- **INTERSECT** findet Gemeinsamkeiten
- **EXCEPT** findet Unterschiede
- Performance: UNION ALL > UNION, Filter vorher anwenden

    {{2}}
**Views:**

    {{2}}
- Virtuelle Tabellen ohne Datenspeicherung
- Code-Wiederverwendung und Abstraktion
- Zugriffskontrolle und API-Schicht
- Performance = Basistabellen-Performance

    {{3}}
**Kombinationen:**

    {{3}}
- Views können SET Operations enthalten
- Views können mit SET Operations kombiniert werden
- Layered Architecture möglich

    {{4}}
> **Pro-Tipp für Ihre Projekte:** Beginnen Sie früh mit Views für häufige Analysen. Das spart später enorm Zeit und reduziert Bugs durch Code-Duplikation!

---

**Referenzen & Weiterführendes:**

- SQL Standards: ISO/IEC 9075 (SET Operations seit SQL-92)
- PostgreSQL Views Dokumentation
- SQL Performance Explained (Markus Winand)
- Database Design Patterns (Fowler et al.)
