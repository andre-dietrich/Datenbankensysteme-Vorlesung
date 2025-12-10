<!--
author:   André Dietrich; GitHub Copilot
email:    LiaScript@web.de
version:  2.0.0
language: de
narrator: Deutsch Female

comment:  Diese Session erschließt die wahre Macht relationaler Datenbanken: das Kombinieren von Daten über Tabellengrenzen hinweg. Sie lernen vier Techniken kennen – vom kartesischen Produkt über Subqueries und CTEs bis zu expliziten JOINs (INNER, LEFT, RIGHT, FULL, CROSS) – und verstehen, wann welcher Ansatz optimal ist. Praxisnah am E-Commerce-Schema mit 7 normalisierten Tabellen erleben Sie, wie Foreign Keys Beziehungen herstellen, wie Anti-Joins fehlende Daten aufspüren, und wie Set-Operationen (UNION, INTERSECT, EXCEPT) Ergebnisse vertikal kombinieren. Am Ende beherrschen Sie Multi-Table-Queries – das Herzstück von SQL in Produktion.

edit:     true

logo:     ../assets/img/logo/10-lecture.jpg

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
        https://raw.githubusercontent.com/liaScript/mermaid_template/master/README.md

-->

# L10: Daten über Tabellengrenzen hinweg kombinieren – Von Subqueries zu CTEs zu Joins

> **Session 10 – Lecture**  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)  
> **Block:** 2 – SQL Einführung & Grundlagen

---

    --{{0}}--
Willkommen zur zehnten Session! Bisher haben Sie mit einzelnen Tabellen gearbeitet – SELECT, WHERE, GROUP BY, alles auf einer Tabelle. Das war wichtig zum Lernen, aber die wahre Macht relationaler Datenbanken liegt woanders: in Beziehungen.

    --{{1}}--
Kunden haben Bestellungen. Bestellungen haben Positionen. Produkte gehören zu Kategorien. All diese Informationen leben in verschiedenen Tabellen – aber wie kombinieren wir sie? Es gibt drei Hauptansätze: Subqueries, CTEs und Joins.

    --{{2}}--
In dieser Session lernen Sie alle drei Techniken kennen – und verstehen, wann Sie welche einsetzen. Wir beginnen mit dem intuitiven Weg (Subqueries), zeigen dessen Grenzen, verbessern ihn mit CTEs, und landen schließlich bei der elegantesten Lösung: Joins.

    --{{3}}--
Los geht's mit der Frage: Warum müssen wir Daten überhaupt kombinieren?

## Warum Daten kombinieren?

    --{{0}}--
Stellen Sie sich vor, Sie speichern alles in einer Tabelle: Kundendaten, Bestellungen, Produktdetails – alles zusammen. Was passiert?

    {{1}}
> **Problem 1: Redundanz**  
> Sie speichern die Kundenadresse bei jeder Bestellung neu. Zieht der Kunde um, müssen Sie Dutzende Zeilen aktualisieren.

    {{2}}
> **Problem 2: Inkonsistenz**  
> Bei manchen Bestellungen steht „Berlin", bei anderen „Berln" – Tippfehler.

    {{3}}
> **Problem 3: Update-Anomalien**  
> Sie ändern den Preis eines Produkts – aber welche Bestellungen bekommen den neuen Preis? Die alten sollten den alten Preis behalten!

    --{{4}}--
Die Lösung? Normalisierung. Wir teilen Daten in mehrere Tabellen auf. Jede Tabelle hat eine klar definierte Verantwortung. Beziehungen werden über Foreign Keys hergestellt.

    {{4}}
**Normalisierung führt zu mehreren Tabellen.**

    {{5}}
**Joins rekonstruieren die Informationen.**

## Unser E-Commerce-Schema

    --{{0}}--
Für alle Beispiele heute nutzen wir ein realistisches E-Commerce-Schema mit sieben normalisierten Tabellen inklusive einer N:M-Beziehung über eine Junction Table.

```SQL
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
  location_id INTEGER,
  FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Orders: Unverändert
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date DATE,
  total_amount DECIMAL(10,2),
  status TEXT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Products: Ohne direkte Category-Referenz (N:M über Junction Table)
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  product_name TEXT NOT NULL,
  price DECIMAL(10,2)
);

-- Product Categories: Junction Table für N:M-Beziehung
CREATE TABLE product_categories (
  product_id INTEGER,
  category_id INTEGER,
  PRIMARY KEY (product_id, category_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Order Items: Unverändert
CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  line_total DECIMAL(10,2),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
 
-- Sample Data: Locations
INSERT INTO locations(location_id, city, postal_code, country) VALUES
  (1, 'Berlin', '10115', 'Germany'),
  (2, 'Hamburg', '20095', 'Germany'),
  (3, 'Munich', '80331', 'Germany'),
  (4, 'Cologne', '50667', 'Germany'),
  (5, 'Frankfurt', '60311', 'Germany');

-- Sample Data: Categories
INSERT INTO categories(category_id, category_name, description) VALUES
  (1, 'Electronics', 'Electronic devices and accessories'),
  (2, 'Furniture', 'Office and home furniture'),
  (3, 'Stationery', 'Office supplies and paper products'),
  (4, 'Office Equipment', 'Professional office tools and devices');

-- Sample Data: Customers (mit strukturierten Adressen)
INSERT INTO customers(customer_id, first_name, last_name, email, street, street_number, location_id) VALUES
  (1, 'Alice', 'Anderson', 'alice@email.com', 'Unter den Linden', '42', 1),
  (2, 'Bob',   'Brown',    'bob@email.com',   'Reeperbahn',       '15', 2),
  (3, 'Carol', 'Clark',    'carol@email.com', 'Marienplatz',       '8', 3),
  (4, 'David', 'Davis',    'david@email.com', 'Hohe Straße',     '123', 4),
  (5, 'Emma',  'Evans',    'emma@email.com',  'Zeil',             '99', 5),
  (99, 'Zoe',   'Zimmer',  'zoe@emailcom',    'Unter den Linden',  '1', 1); -- Orphaned customer! No orders.

-- Sample Data: Orders (Note: Customer 5 has NO orders! Order 106 has invalid customer_id!)
INSERT INTO orders(order_id, customer_id, order_date, total_amount, status) VALUES
  (101, 1, '2024-01-15', 299.99, 'completed'),
  (102, 1, '2024-02-20', 149.50, 'completed'),
  (103, 2, '2024-01-22', 499.99, 'completed'),
  (104, 3, '2024-03-10',  89.99, 'pending'  ),
  (105, 4, '2024-03-15', 199.99, 'completed'),
  (106, 99, '2023-03-20', 79.99, 'completed'); -- Orphaned order! Customer 99 doesn't exist!

-- Sample Data: Products (ohne direkte Category-Referenz)
INSERT INTO products(product_id, product_name, price) VALUES
  (1, 'Laptop',     999.99),
  (2, 'Mouse',       29.99),
  (3, 'Keyboard',    79.99),
  (4, 'Monitor',    299.99),
  (5, 'Desk Chair', 199.99),
  (6, 'Notebook',     9.99),
  (7, 'USB Cable',   14.99),
  (8, 'Desk Lamp',   49.99),
  (9, 'Paper',        4.99);

-- Sample Data: Product Categories (N:M-Beziehungen)
INSERT INTO product_categories(product_id, category_id) VALUES
  (1, 1),  -- Laptop → Electronics
  (1, 4),  -- Laptop → Office Equipment
  (2, 1),  -- Mouse → Electronics
  (2, 4),  -- Mouse → Office Equipment
  (3, 1),  -- Keyboard → Electronics
  (3, 4),  -- Keyboard → Office Equipment
  (4, 1),  -- Monitor → Electronics
  (4, 4),  -- Monitor → Office Equipment
  (5, 2),  -- Desk Chair → Furniture
  (5, 4),  -- Desk Chair → Office Equipment
  (6, 3),  -- Notebook → Stationery (nur eine Kategorie!)
  (7, 1),  -- USB Cable → Electronics (nicht verkauft!)
  (8, 2),  -- Desk Lamp → Furniture (nicht verkauft!)
  (8, 4),  -- Desk Lamp → Office Equipment
  (9, 3);  -- Paper → Stationery (nicht verkauft!)

-- Sample Data: Order Items
INSERT INTO order_items(order_item_id, order_id, product_id, quantity, line_total) VALUES
  (1, 101, 4, 1, 299.99),
  (2, 102, 2, 2,  59.98),
  (3, 102, 3, 1,  79.99),
  (4, 103, 1, 1, 999.99),
  (5, 104, 6, 5,  49.95),
  (6, 105, 5, 1, 199.99),
  (7, 106, 7, 5,  74.95); -- Orphaned order 106: USB Cable

-- Create orphan data for testing purposes
UPDATE orders
SET customer_id = NULL
WHERE customer_id = 99;

DELETE FROM customers
WHERE customer_id = 99;
```
@PGlite.terminal(online-shop)

    {{1}}
**Beziehungen:**

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

    {{1}}
- Ein Ort kann viele Kunden haben (1:N)
- **Ein Produkt kann viele Kategorien haben (N:M über product_categories)**
- **Eine Kategorie kann viele Produkte haben (N:M über product_categories)**
- Ein Kunde kann viele Bestellungen haben (1:N)
- Eine Bestellung hat viele Positionen (1:N)
- Ein Produkt kann in vielen Positionen vorkommen (N:M über order_items)

    --{{2}}--
Diese Struktur ist typisch für relationale Datenbanken. Aber wie kombinieren wir diese Informationen? Schauen wir uns vier Ansätze an – beginnend mit dem ältesten, aber wichtigsten zum Verstehen.

## Technik 0: Verknüpfen von Tabellen über `FROM`

    --{{0}}--
Bevor wir zu modernen Techniken kommen, müssen wir die Basis verstehen: Wie kombiniert SQL überhaupt Tabellen? Die Antwort liegt im FROM. Sie können mehrere Tabellen einfach durch Kommata trennen – und erhalten das kartesische Produkt.

### Das kartesische Produkt: Alle Kombinationen

    --{{0}}--
Wenn Sie zwei Tabellen im FROM auflisten, verbindet SQL jede Zeile der ersten Tabelle mit jeder Zeile der zweiten Tabelle. Das nennt man kartesisches Produkt oder Cross Product.

    {{1}}
**Konzept:**

    {{1}}
```ascii
Customers (3 Zeilen)   Orders (5 Zeilen)
+----+-------+         +-----+------+
| ID | Name  |         | OID | CID  |
+----+-------+         +-----+------+
| 1  | Alice |         | 101 | 1    |
| 2  | Bob   |         | 102 | 1    |
| 5  | Emma  |         | 103 | 2    |
+----+-------+         | 104 | 3    |
                       | 105 | 4    |
                       +-----+------+

FROM customers, orders → 3 × 5 = 15 Kombinationen!
```

    --{{2}}--
Jeder Kunde wird mit jeder Bestellung kombiniert – auch wenn die Bestellung gar nicht zu diesem Kunden gehört! Das ist meist nicht das, was wir wollen.

---

### Live-Beispiel: Kartesisches Produkt im Online-Shop

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

    {{1}}
**Experiment:** Listen Sie Customers und Orders im FROM auf, ohne Bedingung.

    {{1}}
```sql
-- VORSICHT: Kartesisches Produkt!
SELECT 
  c.customer_id,
  c.first_name,
  o.order_id,
  o.customer_id AS order_customer_id
FROM customers c, orders o
LIMIT 10;  -- Nur erste 10 Zeilen zeigen
```
@PGlite.eval(online-shop)

    --{{2}}--
Führen Sie die Query aus. Was sehen Sie? Alice (customer_id = 1) erscheint mit allen Bestellungen – auch mit Bestellungen von Bob und Carol! Das ist das kartesische Produkt: 5 Kunden × 5 Bestellungen = 25 Zeilen.

    {{2}}
**Problem:** Die meisten dieser Kombinationen sind unsinnig! Alice sollte nur mit ihren eigenen Bestellungen verknüpft werden.

---

### Die Lösung: WHERE-Bedingung

    --{{0}}--
Um nur sinnvolle Kombinationen zu bekommen, filtern wir im WHERE: Verbinde nur Zeilen, wo customer_id übereinstimmt.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

```sql
-- TODO: Filtern Sie das kartesische Produkt:
-- Zeigen Sie nur Kunden mit ihren eigenen Bestellungen.
-- Tipp: c.customer_id = o.customer_id
SELECT 
  customer_id,
  first_name,
  order_id,
  order_date,
  total_amount
FROM ???
```
@PGlite.eval(online-shop)

    {{1}}
**So funktioniert das:**

    {{1}}
1. SQL erzeugt zunächst das kartesische Produkt (5 × 5 = 25 Zeilen)
2. Dann filtert WHERE: Nur Zeilen, wo customer_id übereinstimmt
3. Ergebnis: Nur 5 Zeilen (Kunde mit seiner Bestellung)

    --{{2}}--
Das ist die klassische Methode, Tabellen zu verbinden – und genau so wurde SQL in den 1980ern geschrieben! Aber diese Syntax hat Nachteile.

---

### Mehrere Tabellen kombinieren

    --{{0}}--
Sie können beliebig viele Tabellen auflisten – aber die WHERE-Bedingungen werden schnell komplex.

**Aufgabe:** Zeigen Sie Kunde, Bestellung UND Produkt zusammen.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
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

Table order_items {
  order_item_id int [pk]
  order_id int [ref: > orders.order_id]
  product_id int [ref: > products.product_id]
  quantity int
  line_total decimal(10,2)
}
```

```sql
-- TODO: Verbinden Sie customers, orders, order_items, products
-- Hinweis: Sie brauchen 3 WHERE-Bedingungen!
SELECT 
  first_name || ' ' || last_name AS customer,
  order_id,
  product_name,
  quantity
FROM ???
WHERE ???
```
@PGlite.eval(online-shop)

    {{1}}
**Das funktioniert, aber:**

    {{1}}
- Die WHERE-Bedingungen mischen Join-Logik mit Filter-Logik
- Bei 4 Tabellen sind das schon 3 Bedingungen – bei 10 Tabellen?
- Vergessen Sie eine Bedingung → versehentliches kartesisches Produkt!
- Unleserlich: Was ist Join, was ist Filter?

---

### Das Problem mit der impliziten Syntax

    --{{0}}--
Diese Methode wird **implizite Join-Syntax** genannt. Sie hat mehrere Nachteile:

| Problem                | Beschreibung                                           | Beispiel                          |
|------------------------|--------------------------------------------------------|-----------------------------------|
| **Unleserlich**        | Join-Bedingungen vermischt mit Filter-Bedingungen      | `WHERE a.id = b.id AND b.status = 'active'` |
| **Fehleranfällig**     | Vergessene Bedingung → kartesisches Produkt            | `FROM t1, t2, t3 WHERE t1.id = t2.id` (t3 fehlt!) |
| **Kein LEFT/RIGHT**    | Outer Joins nicht möglich (ohne proprietary Syntax)    | Oracle: (`+`) Notation              |
| **Veraltet**           | SQL-92 Standard hat explizite JOIN-Syntax eingeführt   | Vor 30+ Jahren!                   |

    --{{1}}--
Deshalb gilt heute: **Nutzen Sie immer die explizite JOIN-Syntax!** Die ist moderner, klarer und mächtiger.

---

### Warum Sie das trotzdem kennen müssen

    --{{0}}--
Warum habe ich Ihnen dann die implizite Syntax gezeigt? Drei Gründe:

    {{1}}
**1. Legacy-Code verstehen**

    --{{1}}--
Viele alte Datenbanken und Anwendungen nutzen diese Syntax noch. Wenn Sie bestehenden Code warten, werden Sie ihr begegnen.

    {{2}}
**2. Kartesisches Produkt verstehen**

    --{{2}}--
Die explizite JOIN-Syntax versteckt, was wirklich passiert. Mit FROM + WHERE sehen Sie: SQL erzeugt zunächst alle Kombinationen, dann filtert es. Das hilft beim Performance-Verständnis.

    {{3}}
**3. CROSS JOIN erkennen**

    --{{3}}--
Wenn Sie versehentlich mehrere Tabellen auflisten ohne JOIN-Bedingung, passiert ein CROSS JOIN (kartesisches Produkt). Sie müssen das erkennen können!

```sql
-- ❌ Versehentlicher CROSS JOIN (häufiger Fehler!):
SELECT * FROM customers, orders;
-- 5 × 5 = 25 Zeilen, meist ungewollt!

-- ✅ Expliziter CROSS JOIN (wenn gewollt):
SELECT * FROM customers CROSS JOIN orders;
```
@PGlite.eval(online-shop)

---

### Vergleich: Implizit vs. Explizit

    --{{0}}--
Schauen wir uns beide Syntaxen direkt nebeneinander an – für die gleiche Aufgabe.

| Implizite Syntax (veraltet)                          | Explizite Syntax (modern)                          |
|------------------------------------------------------|----------------------------------------------------|
| `FROM customers c, orders o`                         | `FROM customers c INNER JOIN orders o`             |
| `WHERE c.customer_id = o.customer_id`                | `ON c.customer_id = o.customer_id`                 |
| Filter UND Join vermischt                            | Join getrennt von Filter                           |
| Kein LEFT/RIGHT JOIN möglich                         | Alle Join-Typen verfügbar                          |
| Kartesisches Produkt bei Fehler                      | Fehler bei fehlender ON-Bedingung                  |

    {{1}}
**Faustregel:** Implizite Syntax = INNER JOIN ohne `ON`. Mehr geht nicht.

### Übung: Implizit

**Aufgabe:** Zeigen Sie Vorname, Stadt und Bestelldatum für alle abgeschlossenen Bestellungen.

``` sql @dbdiagram
Table locations {
  location_id int [pk]
  city varchar [not null]
  postal_code varchar [not null]
  country varchar [default: 'Germany']
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

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

```sql
-- Gegeben (implizit):
SELECT 
  first_name,
  city,
  order_date
FROM ???
WHERE ???
```
@PGlite.eval(online-shop)


### Zusammenfassung: FROM mit mehreren Tabellen

    {{1}}
**Was passiert intern:**

    {{1}}
1. SQL erzeugt das kartesische Produkt aller Tabellen im FROM
2. WHERE filtert dann die gewünschten Kombinationen
3. Das ist ineffizient – aber so funktioniert die logische Verarbeitung

    {{2}}
**Warum explizite JOINs besser sind:**

    {{2}}
- ✅ Klar getrennt: Join-Bedingungen (`ON`) vs. Filter (`WHERE`)
- ✅ Alle Join-Typen verfügbar (`LEFT`, `RIGHT`, `FULL OUTER`)
- ✅ Weniger fehleranfällig (kein versehentliches kartesisches Produkt)
- ✅ Bessere Performance-Optimierung durch Query Planner

    {{3}}
> **Best Practice:** Nutzen Sie immer `JOIN ... ON` statt `FROM ..., ... WHERE`!

    --{{4}}--
Jetzt, wo Sie verstehen, was im Hintergrund passiert, schauen wir uns die ersten echten Abfrage-Techniken an: Subqueries!

## Technik 1: Subqueries (Verschachtelte SELECT)

    --{{0}}--
Der erste Ansatz, um Daten aus verschiedenen Tabellen zu kombinieren, sind Subqueries – verschachtelte SELECT-Statements. Das fühlt sich natürlich an: "Ich brauche Daten aus Tabelle B, um Tabelle A zu filtern."

    --{{1}}--
Aber was ist eine Subquery genau? Und wo können wir sie überall einsetzen?

### Was ist eine Subquery?

    --{{0}}--
Eine Subquery ist ein SELECT-Statement, das innerhalb eines anderen SQL-Statements ausgeführt wird. Statt erst eine Query auszuführen, das Ergebnis zu notieren und dann in einer zweiten Query zu verwenden, verschachteln wir beide.

    {{1}}
**Konzept:**

    {{1}}
```sql
-- Ohne Subquery (zwei Schritte):
-- Schritt 1: Welche customer_ids haben Bestellungen?
SELECT DISTINCT customer_id FROM orders;
-- Ergebnis: 1, 2, 3, 4

-- Schritt 2: Zeige diese Kunden
SELECT * FROM customers WHERE customer_id IN (1, 2, 3, 4);
```
@PGlite.eval(online-shop)

    {{2}}
<section>

**Mit Subquery (ein Schritt):**

```sql
SELECT * FROM "TABLE" 
WHERE id IN (
  SELECT ... FROM "OTHER TABLE"
);
```

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

```sql
-- TODO: Schreiben sie die Bestellung um und ermitteln sie alle Kunden, die eine Bestellung haben.
SELECT * 
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;
```
@PGlite.eval(online-shop)

</section>

    --{{3}}--
Die innere Query (Subquery) wird zuerst ausgeführt. Ihr Ergebnis wird dann von der äußeren Query verwendet.


### Subquery-Typen: Übersicht

    --{{0}}--
Je nachdem, was eine Subquery zurückgibt, unterscheiden wir verschiedene Typen:

| Subquery-Typ         | Rückgabewert                | Beispiel-Operator         | Use Case                          |
|----------------------|-----------------------------|---------------------------|-----------------------------------|
| **Scalar Subquery**  | Ein einzelner Wert          | `=`, `>`, `<`             | Durchschnitt, Maximum vergleichen |
| **Row Subquery**     | Eine Zeile (mehrere Spalten)| `= (col1, col2)`          | Selten, Multi-Column-Vergleich    |
| **Table Subquery**   | Mehrere Zeilen, eine Spalte | `IN`, `ANY`, `ALL`        | Filtern mit Liste                 |
| **Derived Table**    | Mehrere Zeilen/Spalten      | Im `FROM`                 | Komplexe Aggregationen            |
| **Correlated**       | Referenziert äußere Query   | Mit Spalte aus äußerer Q. | Pro-Zeile-Berechnung              |

    --{{1}}--
Schauen wir uns jetzt die wichtigsten dieser Typen im Detail an, beginnend mit dem häufigsten: WHERE Subqueries.


### WHERE Subqueries: Filtern mit Ergebnissen aus anderen Tabellen

    --{{0}}--
Die häufigste Form: Eine Subquery im WHERE liefert Werte zum Filtern.

**Aufgabe:** Zeigen Sie alle Kunden, die mindestens eine Bestellung haben.

```sql
-- Ohne Subquery (zwei Schritte):
-- Schritt 1: Welche customer_ids haben Bestellungen?
SELECT DISTINCT customer_id FROM orders;
-- Ergebnis: 1, 2, 3, 4

-- Schritt 2: Zeige diese Kunden
SELECT * FROM customers WHERE customer_id IN (1, 2, 3, 4);
```
@PGlite.terminal(online-shop)



```sql
SELECT 
  column_1,
  column_2,
  ...
FROM table_1
WHERE column_x IN (
  -- Subquery
  SELECT column
  FROM table_n
  WHERE condition
);
```

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

---

```sql
-- TODO: Verändern sie die folgende Query, sodass sie eine Subquery im WHERE nutzt,
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;
```
@PGlite.terminal(online-shop)

    {{1}}
**Wie funktioniert das?**

    {{1}}
1. Die **innere Query** (Subquery) wird zuerst ausgeführt: `SELECT customer_id FROM orders`
2. Ergebnis: Liste von customer_ids, die Bestellungen haben: `(1, 1, 2, 3, 4)`
3. Die **äußere Query** filtert damit: `WHERE customer_id IN (1, 1, 2, 3, 4)`

    --{{2}}--
Das ist einfach zu lesen und zu verstehen. Aber Emma (customer_id = 5) fehlt – die hat keine Bestellung. Subqueries im WHERE sind gut für "zeige mir nur die mit..."

---

### Scalar Subqueries: Einzelwerte berechnen

    --{{0}}--
Eine Subquery kann auch einen einzelnen Wert zurückgeben – zum Vergleichen oder Berechnen.

```sql
SELECT
    column_a,
    column_b,
    ...,
    (
        -- Subquery: liefert einen Wert (z. B. Durchschnitt)
        SELECT AGG(target_column)
        FROM source_table
    ) AS computed_value
FROM main_table
WHERE filter_column > (
        -- Subquery: derselbe Wert für die WHERE-Bedingung
        SELECT AGG(target_column)
        FROM source_table
    );
```

    {{1}}
<section>

**Aufgabe:** Zeigen Sie alle Produkte, die teurer sind als der Durchschnittspreis.

``` sql @dbdiagram
Table products {
  product_id int [pk]
  product_name varchar [not null]
  price decimal(10,2)
}
```

```sql
SELECT 
  product_id,
  product_name,
  price,
  ??? AS avg_price
FROM products
WHERE ???;
```
@PGlite.eval(online-shop)

    {{2}}
**Problem:** Wir berechnen den Durchschnitt zweimal! Subquery in SELECT UND in WHERE. Das ist ineffizient und schwer wartbar.

</section>

    --{{2}}--
Scalar Subqueries sind nützlich, aber wenn Sie denselben Wert mehrfach brauchen, wird es unübersichtlich. Später sehen wir, wie CTEs dieses Problem lösen.

### Subqueries in SELECT: Spalten aus anderen Tabellen

    --{{0}}--
Sie können Subqueries auch nutzen, um zusätzliche Spalten zu berechnen.

``` sql
SELECT
    column_1,
    column_2,
    ...,
    (
        -- Subquery: berechnet einen Wert pro Zeile der äußeren Tabelle
        SELECT AGG(*)
        FROM inner_table
        WHERE inner_table.foreign_key = outer_table.primary_key
    ) AS computed_value
FROM outer_table;
```

    {{1}}
<section>

**Aufgabe:** Zeigen Sie für jeden Kunden die Anzahl seiner Bestellungen.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [unique]
  street varchar
  street_number varchar
  location_id int
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal(10,2)
  status varchar
}
```

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  (???)
FROM customers c;
```
@PGlite.terminal(online-shop)

</section>

    {{2}}
**Das ist eine correlated Subquery** – sie referenziert die äußere Query (`c.customer_id`). Für jeden Kunden wird die Subquery neu ausgeführt.

    --{{2}}--
Funktioniert, aber: Bei 10.000 Kunden wird die Subquery 10.000 Mal ausgeführt! Performance-Problem.

### Subquery-Grenzen: Wann wird es problematisch?

    --{{0}}--
Subqueries sind intuitiv, aber sie haben Grenzen:

| Problem                      | Beschreibung                                                | Beispiel                          |
| ---------------------------- | ----------------------------------------------------------- | --------------------------------- |
| **Unleserlich**              | Verschachtelte Queries sind schwer zu verstehen             | 3+ Ebenen Verschachtelung         |
| **Nicht wiederverwendbar**   | Berechnete Werte können nicht mehrfach genutzt werden       | Durchschnitt 2× berechnen         |
| **Performance**              | Correlated Subqueries werden oft wiederholt ausgeführt      | 10.000 Kunden = 10.000 Subqueries |
| **Keine parallelen Spalten** | Schwierig, Spalten aus mehreren Tabellen parallel zu zeigen | Kunde + Bestellung + Produkt      |

    --{{1}}--
Es muss einen besseren Weg geben! Und den gibt es: CTEs (Common Table Expressions).

## Technik 2: CTEs (WITH) – Benannte Zwischenergebnisse

    --{{0}}--
CTEs sind "benannte Subqueries". Sie machen Queries lesbarer und wiederverwendbar. Statt alles in einer verschachtelten Monster-Query zu schreiben, teilen Sie es in logische Schritte auf.

### CTE-Syntax: WITH ... AS

    --{{0}}--
Die Syntax ist einfach: `WITH name AS (SELECT ...)`.

**Aufgabe:** Durchschnittspreis berechnen und wiederverwenden.

``` sql @dbdiagram
Table products {
  product_id int [pk]
  product_name varchar [not null]
  price decimal(10,2)
}
```

```sql
WITH avg_price_cte AS (
  SELECT AVG(price) AS avg_price FROM products
)

SELECT 
  p.product_id,
  p.product_name,
  p.price,
  (SELECT avg_price FROM avg_price_cte) AS avg_price,
  p.price - (SELECT avg_price FROM avg_price_cte) AS difference
FROM products p
WHERE p.price > (SELECT avg_price FROM avg_price_cte);
```
@PGlite.terminal(online-shop)

    {{1}}
**Vorteil:** Der Durchschnitt wird nur einmal in der CTE berechnet. Die Query ist lesbar: "Was ist avg_price_cte? Schaue am Anfang!"

---

### Multiple CTEs: Logische Schritte

    --{{0}}--
Sie können mehrere CTEs definieren – jede kann auf vorherige zugreifen.

**Aufgabe:** Finden Sie alle Produkte, die teurer sind als der durchschnittliche Preis in ihrer Kategorie.

```sql
WITH product_with_categories AS (
  SELECT 
    p.product_id,
    p.product_name,
    p.price,
    pc.category_id
  FROM products p, product_categories pc
  WHERE p.product_id = pc.product_id
),
category_avg_prices AS (
  SELECT 
    category_id,
    AVG(price) AS avg_price
  FROM product_with_categories
  GROUP BY category_id
)
SELECT 
  pwc.product_name,
  pwc.price,
  pwc.category_id,
  (SELECT avg_price FROM category_avg_prices cap WHERE cap.category_id = pwc.category_id) AS category_avg
FROM product_with_categories pwc
WHERE pwc.price > (SELECT avg_price FROM category_avg_prices cap WHERE cap.category_id = pwc.category_id);
```
@PGlite.terminal(online-shop)

    {{1}}
**Das ist jetzt viel lesbarer!**

    {{1}}
1. `product_with_categories`: Produkte mit ihren Kategorien verknüpfen
2. `category_avg_prices`: Durchschnittspreis pro Kategorie berechnen
3. Hauptquery: Zeigt Produkte, die teurer als der Kategorie-Durchschnitt sind

    --{{2}}--
Jeder Schritt ist klar benannt. Die Logik ist in kleine, verständliche Blöcke aufgeteilt.

---

### CTEs vs. Subqueries: Wann was?

| Kriterium            | Subqueries                   | CTEs                         |
| -------------------- | ---------------------------- | ---------------------------- |
| **Lesbarkeit**       | Schlecht bei Verschachtelung | Gut (logische Schritte)      |
| **Wiederverwendung** | Nein                         | Ja (mehrfach referenzierbar) |
| **Performance**      | Identisch                    | Identisch (meist)            |
| **Komplexität**      | Einfache Fälle ok            | Komplexe Queries besser      |

    {{1}}
> **Faustregel:** Bei mehr als einer Verschachtelungsebene → nutzen Sie CTEs!

---

### CTEs: Die Grenze

    --{{0}}--
CTEs sind großartig für komplexe Berechnungen und schrittweise Aggregationen, aber sie haben eine Einschränkung: Das **parallele Zusammenführen von Spalten aus mehreren Tabellen** wird schnell unübersichtlich.

**Problem:** Zeigen Sie für jede Bestellung den Kundennamen UND die bestellten Produkte.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
}

Table order_items {
  order_item_id int [pk]
  order_id int [ref: > orders.order_id]
  product_id int [ref: > products.product_id]
}

Table products {
  product_id int [pk]
  product_name varchar [not null]
}
```

```sql
-- Mit CTE und Subqueries: Umständlich!
WITH order_data AS (
  SELECT 
    o.order_id,
    o.order_date,
    o.customer_id
  FROM orders o
)
SELECT 
  od.order_id,
  od.order_date,
  (SELECT c.first_name || ' ' || c.last_name 
   FROM customers c 
   WHERE c.customer_id = od.customer_id) AS customer_name,
  (SELECT p.product_name 
   FROM order_items oi, products p 
   WHERE oi.order_id = od.order_id 
     AND oi.product_id = p.product_id 
   LIMIT 1) AS first_product
FROM order_data od;
```
@PGlite.terminal(online-shop)

    {{1}}
**Problem mit diesem Ansatz:**

    {{1}}
- Mehrere verschachtelte Subqueries – schwer zu lesen
- Zeigt nur das *erste* Produkt pro Bestellung (LIMIT 1)
- Performance: Subqueries werden für jede Zeile neu ausgeführt
- Wenn eine Bestellung mehrere Produkte hat, fehlen diese

    --{{2}}--
CTEs helfen bei Komplexität und schrittweisen Berechnungen, aber für das **elegante Zusammenführen von Daten aus mehreren Tabellen** brauchen wir ein besseres Werkzeug: Joins!

    --{{3}}--
Zeit für Technik 3: Joins – die Lösung für genau dieses Problem!

---

## Technik 3: Joins – Die elegante Lösung

    --{{0}}--
Joins sind das Werkzeug, um Spalten aus mehreren Tabellen **parallel** in einer Zeile zusammenzuführen. Statt verschachtelt zu denken (Subqueries) oder in Schritten (CTEs), denken Sie horizontal: "Füge Tabellen nebeneinander zusammen."

    --{{1}}--
Ein Join ist wie ein Reißverschluss: Sie haben zwei Listen und verbinden passende Einträge. Kunden und ihre Bestellungen. Produkte und ihre Kategorien. Das Ergebnis? Eine Zeile mit Informationen aus beiden Tabellen.

    --{{2}}--
Aber es gibt verschiedene Arten von Joins – je nachdem, was Sie mit nicht-passenden Einträgen machen wollen. Schauen wir uns die wichtigsten an.

---

### Die JOIN-Syntax

    --{{0}}--
Moderne Joins nutzen das Schlüsselwort `JOIN` mit einer `ON`-Bedingung. Das trennt die Join-Logik sauber vom WHERE-Filter.

```sql
SELECT 
  spalten_aus_tabelle_a,
  spalten_aus_tabelle_b
FROM tabelle_a
JOIN_TYP tabelle_b ON tabelle_a.key = tabelle_b.key
WHERE weitere_filter;
```

    {{1}}
**Bestandteile:**

    {{1}}
- `JOIN_TYP`: INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, CROSS JOIN
- `ON`: Die Bedingung, wie Zeilen zusammenpassen (meist Foreign Key = Primary Key)
- `WHERE`: Zusätzliche Filter (optional, nach dem Join)

    --{{2}}--
Wichtig: ON definiert die Beziehung, WHERE filtert das Ergebnis. Das nicht zu verwechseln macht Queries klar und wartbar!

---

### Überblick: Die 5 Join-Typen

    --{{0}}--
Es gibt fünf Haupt-Join-Typen. Jeder beantwortet eine andere Frage.

| Join-Typ           | Frage                                                  | Wann nutzen?                         |
|--------------------|--------------------------------------------------------|--------------------------------------|
| **INNER JOIN**     | Zeige nur Einträge, die in beiden Tabellen existieren  | Standard-Fall, nur Matches wichtig   |
| **LEFT JOIN**      | Zeige alle aus Tabelle A, auch ohne Match in B        | "Wer hat KEINE Bestellung?"          |
| **RIGHT JOIN**     | Zeige alle aus Tabelle B, auch ohne Match in A        | Selten (meist LEFT stattdessen)      |
| **FULL OUTER JOIN**| Zeige alles aus beiden Tabellen                        | Vergleiche, Sync-Checks              |
| **CROSS JOIN**     | Zeige alle Kombinationen (kartesisches Produkt)        | Test-Kombinationen, Kalender         |

    --{{1}}--
In der Praxis machen INNER JOIN und LEFT JOIN etwa 95% aller Joins aus. Die anderen sind Spezialfälle. Beginnen wir mit dem häufigsten: INNER JOIN.

---

## INNER JOIN: Nur die Matches

    --{{0}}--
INNER JOIN ist der Standard-Join. Er gibt nur Zeilen zurück, bei denen es in **beiden** Tabellen einen passenden Eintrag gibt.

### Visualisierung: Venn-Diagramm


<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Kreise definieren -->
    <circle id="circleCustomers" cx="240" cy="130" r="80" />
    <circle id="circleOrders"   cx="360" cy="130" r="80" />

    <!-- ClipPath für die Schnittmenge -->
    <clipPath id="clipIntersection">
      <use href="#circleOrders" />
    </clipPath>
  </defs>

  <!-- Linker Kreis -->
  <use href="#circleCustomers"
       fill="#e3f2fd"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.8" />

  <!-- Rechter Kreis -->
  <use href="#circleOrders"
       fill="#fff3e0"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.8" />

  <!-- Schnittmenge -->
  <use href="#circleCustomers"
       fill="#4caf50"
       opacity="0.85"
       clip-path="url(#clipIntersection)" />

  <!-- Titel der Kreise -->
  <text x="240" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="360" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight="bold"
        text-anchor="middle">
    Orders
  </text>
</svg>

    --{{1}}--
Denken Sie an die Überschneidung zweier Kreise: Nur der grüne Bereich (wo sich beide überlappen) kommt ins Ergebnis. Alles andere wird ignoriert.

---

### Konzept: Wie funktioniert INNER JOIN?

    --{{0}}--
Stellen Sie sich zwei Listen vor:

```ascii
Customers                 Orders
+----+---------+          +-----+-------------+
| ID | Name    |          | OID | customer_id |
+----+---------+          +-----+-------------+
| 1  | Alice   |          | 101 | 1           | ← Passt zu Alice
| 2  | Bob     |          | 102 | 1           | ← Passt zu Alice
| 3  | Carol   |          | 103 | 2           | ← Passt zu Bob
| 5  | Emma    |          | 105 | 4           | ← Passt zu David
+----+---------+          +-----+-------------+

INNER JOIN ON customer_id:
Alice - Order 101 ✓
Alice - Order 102 ✓
Bob   - Order 103 ✓
David - Order 105 ✓

Emma? Hat keine Bestellung → kommt NICHT ins Ergebnis!
```

    --{{1}}--
SQL geht beide Tabellen durch und verbindet nur Zeilen, wo die customer_id übereinstimmt. Emma hat keine Bestellung, also keine Übereinstimmung, also kein Ergebnis.

### Beispiel 1: Kunden mit ihren Bestellungen

    --{{0}}--
Zeigen Sie jeden Kunden zusammen mit seinen Bestellungen.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar
  last_name varchar
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal
}
```

```sql
SELECT 
  c.first_name,
  c.last_name,
  o.order_id,
  o.order_date
FROM customers c, orders o
WHERE c.customer_id = o.customer_id
ORDER BY c.last_name, o.order_date;
```
@PGlite.eval(online-shop)

    {{1}}
**Was passiert hier?**

    {{1}}
1. SQL nimmt jeden Kunden aus `customers`
2. Sucht alle passenden Bestellungen in `orders` (wo `customer_id` übereinstimmt)
3. Erstellt eine Zeile pro Match: Kunde + Bestellung
4. Emma hat keine Bestellung → erscheint nicht

    --{{2}}--
Führen Sie die Query aus. Sie sehen: Alice erscheint zweimal (hat zwei Bestellungen), Emma fehlt komplett.

---

### Beispiel 2: Bestellungen mit Produktnamen

    --{{0}}--
Zeigen Sie für jede Bestellposition das Produkt mit Namen.

``` sql @dbdiagram
Table order_items {
  order_item_id int [pk]
  order_id int
  product_id int [ref: > products.product_id]
  quantity int
}

Table products {
  product_id int [pk]
  product_name varchar
  price decimal
}
```

```sql
SELECT 
  oi.order_id,
  oi.quantity
FROM order_items oi
```
@PGlite.eval(online-shop)

    {{1}}
**Was sehen Sie?**

    {{1}}
- Order 101: Monitor
- Order 102: Mouse (2×) + Keyboard
- Order 103: Laptop
- ...
- Jede Zeile kombiniert Bestellposition mit Produktdetails

    --{{2}}--
Das ist die Essenz von Joins: Informationen aus verschiedenen Tabellen landen in einer Zeile. Praktisch!

---

### Wann INNER JOIN nutzen?

    --{{0}}--
INNER JOIN ist Ihre Standard-Wahl, wenn Sie nur an **existierenden Beziehungen** interessiert sind.

    {{1}}
**Typische Anwendungsfälle:**

    {{1}}
- Bestellungen mit Kundendaten anzeigen (nur abgeschlossene Bestellungen)
- Produkte mit Kategorien (nur kategorisierte Produkte)
- Rechnungen mit Zahlungen (nur bezahlte Rechnungen)
- Log-Einträge mit User-Details (nur bekannte User)

    {{2}}
> **Faustregel:** INNER JOIN = "Zeige mir nur, wo beides existiert"

---

## LEFT JOIN: Alle von links + Matches

    --{{0}}--
LEFT JOIN (auch LEFT OUTER JOIN genannt) gibt **alle Zeilen der linken Tabelle** zurück – auch wenn es rechts keinen Match gibt. Fehlende Matches werden mit NULL aufgefüllt.

### Visualisierung: Venn-Diagramm


<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Basis-Kreise -->
    <circle id="circleLeft"  cx="240" cy="130" r="80" />
    <circle id="circleRight" cx="360" cy="130" r="80" />

    <!-- Schnittmenge: rechter Kreis schneidet linken -->
    <clipPath id="clipIntersection">
      <use href="#circleRight" />
    </clipPath>
  </defs>

  <!-- Linker Kreis (Customers) – komplettes Ergebnis grün -->
  <use href="#circleLeft"
       fill="#4caf50"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.85" />

  <!-- Rechter Kreis (Orders) nur als Umriss / Kontext -->
  <use href="#circleRight"
       fill="#fff3e0"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.4" />

  <!-- Titel der Kreise -->
  <text x="240" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="360" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight="bold"
        text-anchor="middle">
    Orders
  </text>

  <!-- Beschriftung -->
  <text x="240" y="130"
        font-size="18"
        fill="white"
        font-weight="bold"
        text-anchor="middle"
        alignment-baseline="middle">
    LEFT
  </text>

  <!-- Erklärung unten -->
  <text x="300" y="235"
        font-size="14"
        fill="#666"
        text-anchor="middle">
    Alle Werte aus der linken Tabelle (Customer) + deren Matches (LEFT JOIN)
  </text>
</svg>



    --{{1}}--
Der komplette linke Kreis ist grün – das bedeutet: ALLE Einträge aus der linken Tabelle kommen ins Ergebnis, egal ob es rechts einen Match gibt.

---

### Konzept: Wie funktioniert LEFT JOIN?

    --{{0}}--
LEFT JOIN behält alle Zeilen der linken Tabelle und fügt passende Daten von rechts hinzu – oder NULL, wenn nichts passt.

```ascii
Customers (links)         Orders (rechts)
+----+---------+          +-----+-------------+
| ID | Name    |          | OID | customer_id |
+----+---------+          +-----+-------------+
| 1  | Alice   |          | 101 | 1           | ← Match
| 2  | Bob     |          | 102 | 1           | ← Match
| 3  | Carol   |          | 103 | 2           | ← Match
| 4  | David   |          | 105 | 4           | ← Match
| 5  | Emma    |          (keine Bestellung)
+----+---------+          +-----+-------------+

LEFT JOIN ON customer_id:
Alice - Order 101 ✓
Alice - Order 102 ✓
Bob   - Order 103 ✓
David - Order 105 ✓
Emma  - NULL      ← Emma bleibt im Ergebnis, aber Order-Felder sind NULL!
```

    --{{1}}--
Das ist der Schlüssel: Die linke Tabelle bestimmt, welche Zeilen im Ergebnis erscheinen. Die rechte Tabelle ergänzt nur.

---

### Beispiel 1: Alle Kunden (auch ohne Bestellungen)

    --{{0}}--
Zeigen Sie ALLE Kunden – egal ob sie bestellt haben oder nicht.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar
  last_name varchar
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal
}
```

```sql
SELECT 
  first_name,
  last_name
FROM customers c
-- JOIN 
ORDER BY last_name;
```
@PGlite.eval(online-shop)

    {{1}}
**Was sehen Sie?**

    {{1}}
- Alice, Bob, Carol, David: Jeweils mit ihren Bestellungen
- Emma: Erscheint auch! Aber `order_id`, `order_date`, `total_amount` sind NULL

    --{{2}}--
Das ist der Unterschied zu INNER JOIN: Emma wird nicht ignoriert. Links bestimmt das Ergebnis!

---

### Beispiel 2: Produkte mit Verkaufszahlen (auch unverkaufte)

    --{{0}}--
Zeigen Sie alle Produkte – auch die, die noch nie verkauft wurden.

``` sql @dbdiagram
Table products {
  product_id int [pk]
  product_name varchar
  price decimal
}

Table order_items {
  order_item_id int [pk]
  product_id int [ref: > products.product_id]
  quantity int
}
```

```sql
SELECT 
  p.product_name,
  p.price,
FROM products p
```
@PGlite.eval(online-shop)

    {{1}}
**Was passiert hier?**

    {{1}}
- Produkte mit Verkäufen: `times_sold` > 0
- Unverkaufte Produkte: `times_sold` = 0 (COUNT zählt NULL als 0)

    --{{2}}--
LEFT JOIN ermöglicht es, fehlende Beziehungen zu finden. Das ist extrem wertvoll für Analysen!

---

### Wann LEFT JOIN nutzen?

    --{{0}}--
LEFT JOIN ist perfekt, wenn Sie **fehlende Beziehungen** identifizieren wollen.

    {{1}}
**Typische Anwendungsfälle:**

    {{1}}
- Kunden ohne Bestellungen (Inaktive finden)
- Produkte ohne Verkäufe (Ladenhüter)
- Artikel ohne Übersetzungen (Content-Lücken)
- Rechnungen ohne Zahlung (Offene Posten)

    {{2}}
> **Faustregel:** LEFT JOIN = "Zeige alle von links, ergänze rechts wenn möglich"

---

### Anti-Join: Fehlende finden mit IS NULL

    --{{0}}--
Eine mächtige Technik: LEFT JOIN + WHERE IS NULL = "Zeige nur die OHNE Match"

<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Basis-Kreise -->
    <circle id="circleLeft"  cx="240" cy="130" r="80" />
    <circle id="circleRight" cx="360" cy="130" r="80" />

    <!-- Maske: rechter Kreis "stanzt" sich aus dem linken aus -->
    <mask id="maskLeftAnti">
      <!-- Alles sichtbar machen -->
      <rect x="0" y="0" width="600" height="260" fill="white" />
      <!-- Bereich der rechten Kugel ausblenden -->
      <use href="#circleRight" fill="black" />
    </mask>
  </defs>

  <!-- Linker Kreis (leicht im Hintergrund) -->
  <use href="#circleLeft"
       fill="#e3f2fd"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.4" />

  <!-- Rechter Kreis (Kontext) -->
  <use href="#circleRight"
       fill="#fff3e0"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.4" />

  <!-- LEFT ANTI JOIN: nur der Teil des linken Kreises,
       der NICHT mit dem rechten überlappt -->
  <use href="#circleLeft"
       fill="#4caf50"
       stroke="#1976d2"
       stroke-width="4"
       mask="url(#maskLeftAnti)"
       opacity="0.9" />

  <!-- Titel der Kreise -->
  <text x="240" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="360" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight="bold"
        text-anchor="middle">
    Orders
  </text>

  <!-- Beschriftung im grünen Bereich (links) -->
  <text x="235" y="135"
        font-size="16"
        fill="white"
        font-weight="bold"
        text-anchor="middle"
        alignment-baseline="middle">
    LEFT ANTI
  </text>

  <!-- Erklärung -->
  <text x="300" y="235"
        font-size="14"
        fill="#666"
        text-anchor="middle">
    Nur Customers, die KEINE passenden Orders haben (LEFT ANTI JOIN)
  </text>
</svg>


**Frage:** Welche Kunden haben noch NIE bestellt?

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar
  last_name varchar
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
}
```

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name
FROM customers c
```
@PGlite.eval(online-shop)

    {{1}}
**Trick:** Nach dem LEFT JOIN filtern Sie auf NULL in der rechten Tabelle. Das sind exakt die Zeilen ohne Match!

    --{{2}}--
Diese Technik heißt "Anti-Join" und ist in der Praxis extrem häufig. Sie finden damit Lücken in Ihren Daten.

---

## RIGHT JOIN: Alle von rechts + Matches

    --{{0}}--
RIGHT JOIN ist das Spiegelbild von LEFT JOIN: Alle Zeilen der **rechten** Tabelle bleiben erhalten, links wird ergänzt.

### Visualisierung: Venn-Diagramm

<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Basis-Kreise -->
    <circle id="circleLeft"  cx="240" cy="130" r="80" />
    <circle id="circleRight" cx="360" cy="130" r="80" />

    <!-- Maske: linker Kreis ausschneiden für Anti-Bereiche (hier nicht benötigt) -->
  </defs>

  <!-- Linker Kreis (Kontext, nicht Teil des Ergebnisses) -->
  <use href="#circleLeft"
       fill="#e3f2fd"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.35" />

  <!-- Rechter Kreis (Orders) – komplettes Ergebnis grün -->
  <use href="#circleRight"
       fill="#4caf50"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.9" />

  <!-- Titel der Kreise -->
  <text x="240" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="360" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight="bold"
        text-anchor="middle">
    Orders
  </text>

  <!-- Beschriftung im Ergebnis-Kreis -->
  <text x="360" y="130"
        font-size="18"
        fill="white"
        font-weight="bold"
        alignment-baseline="middle"
        text-anchor="middle">
    RIGHT
  </text>

  <!-- Erklärung -->
  <text x="300" y="235"
        font-size="14"
        fill="#666"
        text-anchor="middle">
    Alle Werte aus Orders + deren Matches (RIGHT JOIN)
  </text>
</svg>


    --{{1}}--
Der komplette rechte Kreis ist grün. Alle Bestellungen kommen ins Ergebnis – auch wenn der Kunde unbekannt ist (was eigentlich nicht passieren sollte, aber theoretisch möglich ist).

---

### In der Praxis: Selten genutzt

    --{{0}}--
RIGHT JOIN wird in der Praxis kaum verwendet. Warum? Weil Sie fast immer eine LEFT JOIN Alternative schreiben können, die leichter zu verstehen ist.

```sql
-- RIGHT JOIN:
SELECT * FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

-- Definieren Sie das gleichbedeutende LEFT JOIN:
```
@PGlite.eval(online-shop)

    {{1}}
**Beide Queries liefern identische Ergebnisse!** Die zweite ist aber intuitiver: Links ist die Haupttabelle.

    --{{2}}--
Mein Rat: Vermeiden Sie RIGHT JOIN. Schreiben Sie stattdessen LEFT JOIN mit vertauschter Reihenfolge. Das ist Standard in den meisten Teams.

---

## FULL OUTER JOIN: Alles aus beiden Tabellen

    --{{0}}--
FULL OUTER JOIN (oder nur FULL JOIN) kombiniert LEFT und RIGHT JOIN: Alle Zeilen aus **beiden** Tabellen kommen ins Ergebnis. Matches werden verbunden, fehlende Matches mit NULL aufgefüllt.

### Visualisierung: Venn-Diagramm

<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Basis-Kreise -->
    <circle id="circleLeft"  cx="240" cy="130" r="80" />
    <circle id="circleRight" cx="360" cy="130" r="80" />
  </defs>

  <!-- Linker Kreis (Teil des Ergebnisses) -->
  <use href="#circleLeft"
       fill="#4caf50"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.85" />

  <!-- Rechter Kreis (Teil des Ergebnisses) -->
  <use href="#circleRight"
       fill="#4caf50"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.85" />

  <!-- Titel der Kreise -->
  <text x="240" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="360" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight="bold"
        text-anchor="middle">
    Orders
  </text>

  <!-- Beschriftung im Zentrum -->
  <text x="300" y="130"
        font-size="18"
        fill="white"
        font-weight="bold"
        alignment-baseline="middle"
        text-anchor="middle">
    FULL
  </text>

  <!-- Erklärung -->
  <text x="300" y="235"
        font-size="14"
        fill="#666"
        text-anchor="middle">
    Alle Werte aus Customers und Orders (FULL JOIN)
  </text>
</svg>


    --{{1}}--
Beide Kreise sind komplett grün. Jede Zeile aus jeder Tabelle erscheint mindestens einmal – entweder mit Match oder mit NULLs.

---

### Konzept: Die vollständige Vereinigung

    --{{0}}--
FULL OUTER JOIN ist wie: "Zeige mir alles – Matches, Nur-Links, Nur-Rechts."

```ascii
Customers           Orders
+----+-------+     +-----+------+
| 1  | Alice |     | 101 | 1    | ← Match mit Alice
| 2  | Bob   |     | 102 | 1    | ← Match mit Alice
| 5  | Emma  |     | 106 | NULL | ← Kunde wurde gelöscht!
+----+-------+     +-----+------+

FULL OUTER JOIN:
Alice - Order 101 ✓
Alice - Order 102 ✓
Bob   - NULL      ✓ (Bob hat keine Bestellung)
Emma  - NULL      ✓ (Emma hat keine Bestellung)
NULL  - Order 106 ✓ (Bestellung hat ungültigen Kunden)
```

    --{{1}}--
Sie sehen: Sowohl Emma (Kunde ohne Bestellung) als auch Order 106 (Bestellung ohne Kunden) erscheinen im Ergebnis. Nichts geht verloren!

---

### Beispiel 1: Vollständiger Datenabgleich

    --{{0}}--
Zeigen Sie ALLE Kunden und ALLE Bestellungen – auch wenn Kunden keine Bestellung haben ODER Bestellungen keinen gültigen Kunden haben.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar
  last_name varchar
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
  order_date date
  total_amount decimal
}
```

```sql
SELECT 
  c.customer_id,
  c.first_name || ' ' || c.last_name AS customer_name,
--  o.order_id,
--  o.order_date,
--  o.total_amount
FROM customers c
```
@PGlite.eval(online-shop)

    {{1}}
**Was sehen Sie?**

    {{1}}
- Emma (customer_id = 5): Erscheint mit NULL bei Bestellungen → Kunde ohne Bestellung
- Order 106: Erscheint mit NULL bei Kundendaten → Bestellung ohne gültigen Kunden (customer_id = 99 existiert nicht!)
- Alle anderen: Normale Matches

    --{{2}}--
FULL OUTER JOIN ist perfekt für Datenqualitäts-Checks: "Zeige mir ALLES, damit ich Inkonsistenzen erkenne." Hier sehen wir beide Probleme: Emma hat nicht bestellt UND Order 106 hat einen ungültigen Kunden.


### Wann FULL OUTER JOIN nutzen?

    --{{0}}--
FULL OUTER JOIN ist selten, aber für spezielle Aufgaben perfekt.

    {{1}}
**Typische Anwendungsfälle:**

    {{1}}
- Datenbank-Sync prüfen (Quelle vs. Ziel)
- Inkonsistenzen finden (Orphaned Records auf beiden Seiten)
- Audit-Reports (vollständige Übersicht)

    {{2}}
> **Faustregel:** FULL OUTER JOIN = "Zeige alles aus beiden Welten"

    --{{3}}--
In der Praxis wird FULL OUTER JOIN selten genutzt – oft kann man das Problem mit zwei LEFT JOINs + UNION lösen. Aber wenn Sie ihn brauchen, ist er unschlagbar praktisch!

---

## CROSS JOIN: Alle Kombinationen (Kartesisches Produkt)

    --{{0}}--
CROSS JOIN ist der ungewöhnlichste Join: Er verbindet **jede Zeile** der ersten Tabelle mit **jeder Zeile** der zweiten Tabelle. Keine Bedingung, keine Filter – alle Kombinationen.

### Visualisierung: Venn-Diagramm

<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Kreise -->
    <circle id="circleLeft"  cx="200" cy="130" r="80" />
    <circle id="circleRight" cx="400" cy="130" r="80" />
  </defs>

  <!-- Linker Kreis -->
  <use href="#circleLeft"
       fill="#4caf50"
       stroke="#1976d2"
       stroke-width="4"
       opacity="0.85" />

  <!-- Rechter Kreis -->
  <use href="#circleRight"
       fill="#4caf50"
       stroke="#f57c00"
       stroke-width="4"
       opacity="0.85" />

  <!-- Titel -->
  <text x="200" y="45"
        font-size="18"
        fill="#1976d2"
        font-weight="bold"
        text-anchor="middle">
    Customers
  </text>

  <text x="400" y="45"
        font-size="18"
        fill="#f57c00"
        font-weight-bold
        text-anchor="middle">
    Orders
  </text>

  <!-- CROSS JOIN: X zwischen den Kreisen -->
  <line x1="285" y1="100" x2="315" y2="160"
        stroke="#666" stroke-width="6" stroke-linecap="round" />
  <line x1="315" y1="100" x2="285" y2="160"
        stroke="#666" stroke-width="6" stroke-linecap="round" />

  <!-- Beschreibung -->
  <text x="300" y="235"
        font-size="14"
        fill="#666"
        text-anchor="middle">
    Kartesisches Produkt: jede Zeile × jede Zeile
  </text>
</svg>


    --{{1}}--
Die Kreise überlappen nicht – weil CROSS JOIN keine Beziehung braucht. Er erzeugt einfach alle Kombinationen. Das nennt man kartesisches Produkt.

---

### Konzept: Alle Kombinationen

    --{{0}}--
CROSS JOIN ist wie eine Tabelle mit allen möglichen Paarungen erstellen.

```ascii
Sizes              Colors
+------+          +--------+
| Size |          | Color  |
+------+          +--------+
| S    |          | Red    |
| M    |          | Blue   |
| L    |          | Green  |
+------+          +--------+

CROSS JOIN → 3 × 3 = 9 Kombinationen:
S - Red
S - Blue
S - Green
M - Red
M - Blue
M - Green
L - Red
L - Blue
L - Green
```

    --{{1}}--
Jede Größe wird mit jeder Farbe kombiniert. Kein Filter, keine Bedingung – einfach alle Möglichkeiten.

---

### Syntax: Zwei Varianten

    --{{0}}--
CROSS JOIN kann explizit oder implizit geschrieben werden.

```sql
-- Explizit (empfohlen):
SELECT * FROM customers CROSS JOIN products;

-- Implizit (veraltet):
SELECT * FROM customers, products;
```
@PGlite.eval(online-shop)

    {{1}}
> **Achtung:** Die implizite Syntax (`FROM a, b`) ist gefährlich! Wenn Sie vergessen, eine WHERE-Bedingung hinzuzufügen, passiert ein versehentlicher CROSS JOIN.

    --{{2}}--
Nutzen Sie immer die explizite Syntax – dann ist klar: "Ich WILL alle Kombinationen!"

---

### Beispiel 1: Produktkombinationen generieren

    --{{0}}--
Erstellen Sie alle möglichen Kombinationen von zwei Produkten (z.B. für Paket-Angebote).

``` sql @dbdiagram
Table products {
  product_id int [pk]
  product_name varchar
  price decimal
}
```

```sql
SELECT 
  p1.product_name AS product_1,
  p2.product_name AS product_2,
  p1.price + p2.price AS bundle_price
FROM products p1
CROSS JOIN products p2
WHERE p1.product_id < p2.product_id  -- Vermeidet Duplikate (A-B vs B-A)
ORDER BY bundle_price
LIMIT 5;
```
@PGlite.eval(online-shop)

    {{1}}
**Was passiert?**

    {{1}}
- Jedes Produkt wird mit jedem anderen kombiniert
- `WHERE p1.product_id < p2.product_id`: Verhindert, dass "Laptop + Mouse" und "Mouse + Laptop" beide erscheinen
- Ergebnis: Alle möglichen 2er-Pakete mit Gesamtpreis

    --{{2}}--
Das ist praktisch für Preis-Kombinationen, Test-Daten oder Kalender-Aufgaben!

---

### Beispiel 2: Datumsreihen generieren

    --{{0}}--
CROSS JOIN ist perfekt, um alle Kombinationen aus zwei Listen zu erzeugen – z.B. jeden Kunden mit jedem Datum (für Reports).

```sql
-- Simuliere eine Datumsreihe mit VALUES
WITH dates AS (
  SELECT * FROM (VALUES 
    ('2024-01-01'), 
    ('2024-01-02'), 
    ('2024-01-03')
  ) AS d(date)
)
SELECT 
  c.customer_id,
  c.first_name,
  dates.date
FROM customers c
CROSS JOIN dates
ORDER BY dates.date, c.customer_id
LIMIT 10;
```
@PGlite.eval(online-shop)

    {{1}}
**Ergebnis:** Jeder Kunde erscheint für jedes Datum. Perfekt für Kalender-Grids oder A/B-Test-Setups!

---

### Gefahr: Zeilen-Explosion!

    --{{0}}--
CROSS JOIN kann schnell außer Kontrolle geraten.

| Tabelle A | Tabelle B | Ergebnis          | Status |
|-----------|-----------|-------------------|--------|
| 5         | 6         | 30                | ✓ OK   |
| 100       | 100       | 10.000            | ⚠️ Vorsicht |
| 1.000     | 1.000     | 1.000.000         | ❌ Langsam |
| 10.000    | 10.000    | 100.000.000       | 💥 Absturz |

    {{1}}
> **Best Practice:** Nutzen Sie CROSS JOIN nur mit kleinen Tabellen oder mit `LIMIT`!

    --{{2}}--
In Produktions-Datenbanken ist CROSS JOIN selten. Aber für Teszdaten-Generierung oder Kombinatorik ist er unschlagbar.

---

## Join-Zusammenfassung: Welchen wann?

    --{{0}}--
Sie haben jetzt 5 Join-Typen kennengelernt. Hier ist ein Entscheidungsbaum:

``` text
Brauchen Sie eine Beziehung zwischen Tabellen?
│
├─ Ja, nur Matches wichtig
│  └─ INNER JOIN
│
├─ Ja, aber ALLE von links (auch ohne Match)
│  └─ LEFT JOIN
│
├─ Ja, aber ALLE von rechts (auch ohne Match)
│  └─ RIGHT JOIN (oder besser: LEFT JOIN mit getauschter Reihenfolge)
│
├─ Ja, ALLES aus beiden (für Vergleiche)
│  └─ FULL OUTER JOIN
│
└─ Nein, ich brauche ALLE Kombinationen
   └─ CROSS JOIN
```

    --{{1}}--
In der Praxis machen INNER JOIN und LEFT JOIN etwa 95% aller Fälle aus. Die anderen sind Spezialwerkzeuge.

---

### Quick Reference: Join-Cheat-Sheet

| Join-Typ     | Ergebnis                     | Syntax                                                   | Use Case                   |
|--------------|------------------------------|----------------------------------------------------------|----------------------------|
| INNER        | Nur Matches                  | `FROM a INNER JOIN b ON a.id = b.id`                     | Standard                   |
| LEFT         | Alle A + Matches B           | `FROM a LEFT JOIN b ON a.id = b.id`                      | Fehlende finden            |
| RIGHT        | Alle B + Matches A           | `FROM a RIGHT JOIN b ON a.id = b.id`                     | Selten (nutze LEFT)        |
| FULL OUTER   | Alles aus beiden             | `FROM a FULL OUTER JOIN b ON a.id = b.id`                | Sync-Checks                |
| CROSS        | Alle Kombinationen           | `FROM a CROSS JOIN b`                                    | Test-Kombinationen         |

    {{1}}
> **Faustregel:** Wenn unsicher → starte mit INNER JOIN. Fehlt etwas? → Probiere LEFT JOIN.

---

## Mehrere Tabellen verbinden (Multi-Table Joins)

    --{{0}}--
In der Realität joinen Sie selten nur zwei Tabellen. Oft sind es drei, vier oder mehr. Wie geht man das systematisch an?

### Die Kette: JOIN nach JOIN

    --{{0}}--
Sie können beliebig viele Joins aneinanderhängen. Jeder neue JOIN baut auf dem vorherigen Ergebnis auf.

```sql
SELECT spalten
FROM tabelle_a
JOIN tabelle_b ON a.id = b.id
JOIN tabelle_c ON b.id = c.id
JOIN tabelle_d ON c.id = d.id
-- ... und so weiter
```

    {{1}}
**Wichtig:** Die Reihenfolge ist logisch, nicht Performance-kritisch. Der Query Optimizer kann die beste Reihenfolge selbst wählen.

---

### Beispiel: Vollständige Bestellung (4 Tabellen)

    --{{0}}--
Zeigen Sie: Kunde → Bestellung → Positionen → Produkte – alles in einer Zeile.

``` sql @dbdiagram
Table customers {
  customer_id int [pk]
  first_name varchar
}

Table orders {
  order_id int [pk]
  customer_id int [ref: > customers.customer_id]
}

Table order_items {
  order_item_id int [pk]
  order_id int [ref: > orders.order_id]
  product_id int [ref: > products.product_id]
  quantity int
}

Table products {
  product_id int [pk]
  product_name varchar
  price decimal
}
```

```sql
SELECT 
  c.first_name || ' ' || c.last_name AS customer,
--  o.order_id,
--  o.order_date,
--  p.product_name,
--  oi.quantity,
--  oi.quantity * p.price AS line_total
FROM customers c
```
@PGlite.eval(online-shop)

    {{1}}
**Was passiert hier?**

    {{1}}
1. customers → orders: Welcher Kunde hat welche Bestellung?
2. orders → order_items: Welche Positionen gehören zur Bestellung?
3. order_items → products: Welches Produkt ist das?

    --{{2}}--
Das Ergebnis: Jede Bestellposition mit allen relevanten Details in einer Zeile. Das ist die Power von Joins!

---

### Best Practices für Multi-Table Joins

    --{{0}}--
Wenn Sie viele Tabellen joinen, helfen diese Regeln:

    {{1}}
**1. Logische Reihenfolge einhalten**

    {{1}}
Joinen Sie in der Reihenfolge der Beziehungen: Kunde → Bestellung → Position → Produkt (nicht wild durcheinander).

    {{2}}
**2. Aliase nutzen**

    {{2}}
Kurze Aliase machen Queries lesbarer: `customers c`, `orders o`, `products p`

    {{3}}
**3. Joins einrücken**

    {{3}}
```sql
FROM customers c
  INNER JOIN orders o ON c.customer_id = o.customer_id
  INNER JOIN order_items oi ON o.order_id = oi.order_id
```
Jeder JOIN eine eigene Zeile – so erkennen Sie die Struktur sofort!

    {{4}}
**4. Kommentare bei komplexen Joins**

    {{4}}
```sql
-- Hole Kundendaten
FROM customers c
  -- Füge Bestellungen hinzu
  INNER JOIN orders o ON c.customer_id = o.customer_id
```

---

## Abschluss: Joins meistern

    --{{0}}--
Sie haben jetzt das wichtigste Werkzeug relationaler Datenbanken kennengelernt: Joins. Von INNER bis CROSS, von einfachen 2-Tabellen-Joins bis zu komplexen Multi-Table-Queries.

    {{1}}
**Was Sie gelernt haben:**

    {{1}}
- ✅ INNER JOIN: Nur Matches (Standard)
- ✅ LEFT JOIN: Alle links + Matches rechts (fehlende finden!)
- ✅ RIGHT JOIN: Alle rechts + Matches links (selten)
- ✅ FULL OUTER JOIN: Alles aus beiden (Sync-Checks)
- ✅ CROSS JOIN: Alle Kombinationen (Vorsicht!)
- ✅ Multi-Table Joins: Systematisch verketten

    --{{2}}--
Joins sind das Herzstück von SQL. Mit diesem Wissen können Sie jetzt fast jede Abfrage in der Praxis lösen. Zeit, es zu üben!