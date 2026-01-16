<!--
author:   André Dietrich; GitHub Copilot
email:    LiaScript@web.de

language: de
narrator: German Male

version:  2.0.0

edit:     true

comment:  In dieser Session lernen Sie die Grundlagen der SQL Data Definition Language (DDL) und Data Manipulation Language (DML) kennen. Sie erfahren, wie Sie Tabellen und Schemata mit CREATE, ALTER und DROP definieren, wie Sie Daten mit INSERT, UPDATE und DELETE manipulieren und wie Constraints wie PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK und DEFAULT die Datenintegrität sichern. Praxisnahe Beispiele, Best Practices und interaktive Aufgaben helfen Ihnen, die Konzepte direkt anzuwenden und typische Fehler zu vermeiden. Am Ende sind Sie in der Lage, eigene Datenbankschemata zu entwerfen, zu verändern und sicher zu verwalten.

logo:     ../assets/img/logo/8-lecture-full.jpg

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
-->

# Session 8 – SQL Data Definition (DDL) & Manipulation (DML)

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (SQL-Praxis)

## Intro: Von Abfragen zu Strukturen

    --{{0}}--
Bisher haben Sie gelernt, Daten abzufragen – SELECT, WHERE, GROUP BY, alles in Session 7. Aber wie kommen die Tabellen überhaupt in die Datenbank? Wie definieren Sie Spalten, Datentypen, Constraints? Und wie fügen Sie Daten ein, ändern sie, löschen sie? Das ist der nächste Schritt: Von der Abfrageebene zur Strukturebene.

    {{0}}
**Heute lernen Sie:**

- **DDL (Data Definition Language):** CREATE, ALTER, DROP – Ihre Werkzeuge für Schema-Design
- **DML (Data Manipulation Language):** INSERT, UPDATE, DELETE – Daten schreiben, nicht nur lesen
- **Constraints:** PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK – Datenintegrität sichern
- **Best Practices:** Sichere Schema-Evolution, häufige Fehler vermeiden

    --{{1}}--
Warum ist das wichtig? Weil Ihre Datenbank nur so gut ist wie Ihr Schema. Falsche Datentypen führen zu Performance-Problemen. Fehlende Constraints führen zu Inkonsistenzen. Unsichere Updates können Ihre gesamte Datenbank zerstören. Diese Session gibt Ihnen die Kontrolle.

---

## Datenbank vorbereiten

    --{{0}}--
Wir starten mit einer einfachen Sandbox-Datenbank. Keine Sorge – alles läuft im Browser, nichts wird dauerhaft gespeichert. Sie können experimentieren, Fehler machen, lernen.

```sql
-- Sandbox initialisieren
CREATE TABLE IF NOT EXISTS demo_test (id INTEGER, name TEXT);
INSERT INTO demo_test VALUES (1, 'Test');
SELECT 'Datenbank bereit!' AS status;
```
@PGlite.eval(ddl_dml)

```sql
-- Interaktives Terminal (nutzen Sie es für eigene Experimente)
SELECT * FROM demo_test;
```
@PGlite.terminal(ddl_dml)

---

## Was ist DDL & DML?

    --{{0}}--
SQL ist keine monolithische Sprache. Es gibt Kategorien: DDL für Schema-Definition, DML für Datenmanipulation, DCL für Zugriffsrechte, TCL für Transaktionen. Heute fokussieren wir DDL und DML – das Fundament für alles Weitere.

    {{0}}
<section>

### SQL-Kategorien im Überblick

| Kategorie                        | Abkürzung | Zweck                   | Befehle                                | Session     |
| -------------------------------- | --------- | ----------------------- | -------------------------------------- | ----------- |
| **Data Definition Language**     | DDL       | Schema erstellen/ändern | `CREATE`, `ALTER`, `DROP`              | **Heute**   |
| **Data Manipulation Language**   | DML       | Daten lesen/schreiben   | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | **Heute**   |
| **Data Control Language**        | DCL       | Zugriffsrechte          | `GRANT`, `REVOKE`                      | Später      |
| **Transaction Control Language** | TCL       | Transaktionen           | `BEGIN`, `COMMIT`, `ROLLBACK`          | Session 11+ |

**Heute:** DDL (Struktur) + DML (Daten)

</section>

    --{{1}}--
DDL ist wie der Bauplan Ihres Hauses: Sie definieren Räume (Tabellen), Türen (Foreign Keys), Regeln (Constraints). DML ist das Leben im Haus: Sie stellen Möbel auf (INSERT), verschieben sie (UPDATE), werfen sie raus (DELETE).

---

## DDL – Tabellen erstellen (CREATE TABLE)

    --{{0}}--
CREATE TABLE ist Ihr wichtigster DDL-Befehl. Sie definieren den Tabellennamen, die Spalten, die Datentypen, die Constraints. Schauen wir uns die Grundsyntax an.

    {{0}}
<section>

### Grundsyntax

**Minimal-Beispiel:**

```sql
CREATE TABLE products (
  id INTEGER,
  name TEXT,
  price DECIMAL(10, 2)
);
```
@PGlite.eval(ddl_dml)

**Was passiert hier?**

- Tabelle `products` wird erstellt
- 3 Spalten: `id` (Ganzzahl), `name` (Text), `price` (Dezimalzahl mit 2 Nachkommastellen)
- Keine Constraints – jeder Wert ist erlaubt, auch NULL

</section>

    --{{1}}--
Aber das ist zu simpel. In der Praxis wollen Sie mehr Kontrolle: Ein Primärschlüssel, NOT NULL für Pflichtfelder, DEFAULT-Werte. Schauen wir uns eine realistischere Version an.

    {{1}}
<section>

### Realistisches Beispiel mit Constraints

```sql
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  stock INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
@PGlite.eval(ddl_dml)

**Was ist neu?**

- `PRIMARY KEY`: `product_id` ist eindeutig + NOT NULL
- `NOT NULL`: `name` und `price` sind Pflichtfelder
- `CHECK`: `price` muss >= 0 sein (keine negativen Preise!)
- `DEFAULT`: `stock` ist standardmäßig 0, `created_at` wird automatisch gesetzt

**Testen:**

```sql
-- Funktioniert:
INSERT INTO products (product_id, name, price) 
VALUES (1, 'Laptop', 999.99);

-- Funktioniert NICHT (price negativ):
INSERT INTO products (product_id, name, price) 
VALUES (2, 'Mouse', -10.00);
```
@PGlite.terminal(ddl_dml)

</section>

    --{{2}}--
Sie können Primärschlüssel auch inline definieren oder als separaten Constraint. Beides funktioniert, aber die separate Form ist flexibler – vor allem bei Composite Keys.

    {{2}}
<section>

### Primärschlüssel: Inline vs. Constraint

**Inline (einfach):**

```sql
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_name TEXT
);
```

**Als Constraint (flexibel):**

```sql
CREATE TABLE orders (
  order_id INTEGER,
  customer_name TEXT,
  CONSTRAINT pk_orders PRIMARY KEY (order_id)
);
```

**Composite Key (mehrere Spalten):**

```sql
CREATE TABLE order_items (
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  PRIMARY KEY (order_id, product_id)
);
```
@PGlite.eval(ddl_dml)

**Wann Composite Keys?**

- Wenn Eindeutigkeit nur durch Kombination gegeben ist
- Beispiel: Ein Produkt kann in mehreren Bestellungen vorkommen, aber pro Bestellung nur einmal

</section>

---

## Datentypen-Überblick

    --{{0}}--
Datentypen sind wichtig für Speichereffizienz, Performance und Validierung. Ein INTEGER braucht weniger Platz als TEXT. Eine DECIMAL-Zahl ist präziser als FLOAT. Datum-Typen ermöglichen Zeitberechnungen. Schauen wir uns die wichtigsten an.

    {{0}}
<section>

### Numerische Typen

| Typ                | Bereich             | Speicher  | Wann nutzen?                         |
| ------------------ | ------------------- | --------- | ------------------------------------ |
| `INTEGER` / `INT`  | -2^31 bis 2^31-1    | 4 Bytes   | IDs, Zähler, ganze Zahlen            |
| `BIGINT`           | -2^63 bis 2^63-1    | 8 Bytes   | Große IDs, Zeitstempel (Unix)        |
| `DECIMAL(p,s)`     | Präzise Dezimalzahl | Variabel  | Geld, Preise (keine Rundungsfehler!) |
| `FLOAT` / `DOUBLE` | Approximativ        | 4/8 Bytes | Wissenschaftliche Berechnungen       |

**Beispiel: Warum DECIMAL für Geld?**

```sql
-- FLOAT hat Rundungsfehler:
SELECT 0.1 + 0.2 AS float_sum;  -- Ergebnis: 0.30000000000000004

-- DECIMAL ist präzise:
SELECT CAST(0.1 AS DECIMAL(10,2)) + CAST(0.2 AS DECIMAL(10,2)) AS decimal_sum;
```
@PGlite.terminal(ddl_dml)

</section>

    --{{1}}--
Text-Typen haben verschiedene Längen. VARCHAR begrenzt die Länge, TEXT ist unbegrenzt. In PGlite.und PostgreSQL gibt es keinen Performance-Unterschied mehr, aber in älteren Systemen (MySQL) schon.

    {{1}}
<section>

### Text-Typen

| Typ          | Max. Länge     | Wann nutzen?                                   |
| ------------ | -------------- | ---------------------------------------------- |
| `CHAR(n)`    | Fix n Zeichen  | Festlängen-Codes (z.B. Ländercodes 'DE', 'US') |
| `VARCHAR(n)` | Variabel bis n | Namen, E-Mails mit Längenbegrenzung            |
| `TEXT`       | Unbegrenzt     | Beschreibungen, Kommentare, JSON               |

**Beispiel:**

```sql
CREATE TABLE users (
  country_code CHAR(2),      -- Immer 2 Zeichen: 'DE', 'US'
  email VARCHAR(255),        -- Max. 255 Zeichen
  bio TEXT                   -- Unbegrenzt
);
```
@PGlite.eval(ddl_dml)

</section>

    --{{2}}--
Datum- und Zeit-Typen sind essenziell für zeitbasierte Analysen. DATE speichert nur das Datum, TIMESTAMP speichert Datum + Uhrzeit, INTERVAL repräsentiert Zeitdauern.

    {{2}}
<section>

### Datum & Zeit

| Typ         | Format              | Beispiel            | Wann nutzen?        |
| ----------- | ------------------- | ------------------- | ------------------- |
| `DATE`      | YYYY-MM-DD          | 2025-11-04          | Geburtstage, Events |
| `TIME`      | HH:MM:SS            | 14:30:00            | Öffnungszeiten      |
| `TIMESTAMP` | YYYY-MM-DD HH:MM:SS | 2025-11-04 14:30:00 | Logs, created_at    |
| `INTERVAL`  | Duration            | '3 days', '2 hours' | Zeitrechnungen      |

**Beispiel: Zeitberechnungen**

```sql
CREATE TABLE events (
  event_id INTEGER PRIMARY KEY,
  event_name TEXT,
  event_date DATE,
  start_time TIMESTAMP
);

INSERT INTO events VALUES 
  (1, 'Konferenz', '2025-12-15', '2025-12-15 09:00:00');

-- 3 Tage vor dem Event:
SELECT 
  event_name,
  event_date,
  event_date - INTERVAL '3 days' AS reminder_date
FROM events;
```
@PGlite.terminal(ddl_dml)

</section>

    --{{3}}--
Boolean und Spezialtypen runden das Bild ab. BOOLEAN für Ja/Nein-Flags, JSON für strukturierte Daten, ARRAY für Listen.

    {{3}}
<section>

### Boolean & Spezialtypen

| Typ       | Werte                 | Beispiel           | Wann nutzen?   |
| --------- | --------------------- | ------------------ | -------------- |
| `BOOLEAN` | TRUE, FALSE, NULL     | is_active          | Flags, Status  |
| `JSON`    | JSON-Objekt           | `{"key": "value"}` | Flexible Daten |
| `ARRAY`   | Liste                 | `[1, 2, 3]`        | Tags, Listen   |
| `UUID`    | Universally Unique ID | `550e8400-e29b...` | Verteilte IDs  |

**Beispiel: JSON-Spalte**

```sql
CREATE TABLE products_ext (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  metadata JSON  -- Flexible Zusatzdaten
);

INSERT INTO products_ext VALUES 
  (1, 'Laptop', '{"brand": "Dell", "warranty_years": 3}');

-- JSON abfragen (PGlite.:
SELECT 
  name,
  metadata->>'brand' AS brand,
  metadata->>'warranty_years' AS warranty
FROM products_ext;
```
@PGlite.terminal(ddl_dml)

</section>

---

## DDL – Tabellen ändern (ALTER TABLE)

    --{{0}}--
Schemas ändern sich. Sie fügen Spalten hinzu, ändern Datentypen, löschen veraltete Felder. ALTER TABLE ist Ihr Werkzeug für Schema-Evolution. Aber Vorsicht: Manche Operationen sind riskant bei großen Tabellen.

    {{0}}
<section>

### Spalten hinzufügen (ADD COLUMN)

**Syntax:**

```sql
ALTER TABLE table_name
ADD COLUMN column_name datatype [constraints];
```

**Beispiel:**

```sql
-- Neue Spalte hinzufügen:
ALTER TABLE products
ADD COLUMN category TEXT DEFAULT 'Uncategorized';

-- Prüfen:
SELECT * FROM products;
```
@PGlite.terminal(ddl_dml)

**💡 Best Practice:** Neue Spalten mit DEFAULT oder NULL hinzufügen, um Lock-Probleme zu vermeiden.

</section>

    --{{1}}--
Spalten ändern ist komplexer. Sie können Datentypen ändern, Defaults setzen, Constraints hinzufügen. Aber nicht alle Datenbanken unterstützen alle Operationen gleich.

    {{1}}
<section>

### Spalten ändern (ALTER COLUMN)

**Datentyp ändern:**

```sql
-- In PostgreSQL/PGlite.
ALTER TABLE products
ALTER COLUMN price TYPE DECIMAL(12, 2);

-- In MySQL:
ALTER TABLE products
MODIFY COLUMN price DECIMAL(12, 2);
```

**Default setzen/ändern:**

```sql
ALTER TABLE products
ALTER COLUMN stock SET DEFAULT 10;
```

**⚠️ Achtung bei Datentyp-Änderungen:**

- `TEXT` → `INTEGER`: Funktioniert nur, wenn alle Werte Zahlen sind
- `INTEGER` → `BIGINT`: Meist sicher
- Bei großen Tabellen: Kann lange dauern!

</section>

    --{{2}}--
Spalten löschen ist riskant. Sobald weg, sind die Daten weg. Überlegen Sie zweimal, bevor Sie DROP COLUMN nutzen. Manchmal ist es besser, eine Spalte zu "verstecken" (in Views) statt zu löschen.

    {{2}}
<section>

### Spalten löschen (DROP COLUMN)

**Syntax:**

```sql
ALTER TABLE products
DROP COLUMN description;
```

**⚠️ Vorsicht:**

- Daten werden **permanent** gelöscht
- Kann nicht rückgängig gemacht werden (außer via Backup)
- Bei FOREIGN KEY Constraints: Kann fehlschlagen

**Alternative: Soft Delete**

Statt Spalte zu löschen:

```sql
-- Spalte umbenennen (verstecken):
ALTER TABLE products
RENAME COLUMN description TO _deprecated_description;

-- Oder in Views weglassen:
CREATE VIEW products_view AS
SELECT product_id, name, price FROM products;
```

</section>

    --{{3}}--
Tabellen können umbenannt werden. Das ist nützlich, wenn Sie Schema-Migrationen machen oder alte Versionen als Backup behalten wollen.

    {{3}}
<section>

### Tabelle umbenennen (RENAME TO)

**Syntax:**

```sql
ALTER TABLE old_name RENAME TO new_name;
```

**Beispiel:**

```sql
-- Backup erstellen:
CREATE TABLE products_backup AS SELECT * FROM products;

-- Original umbenennen:
ALTER TABLE products RENAME TO products_v1;

-- Neue Version wird zu "products":
CREATE TABLE products AS SELECT * FROM products_v1;
```
@PGlite.terminal(ddl_dml)

</section>

---

## DDL – Tabellen löschen (DROP TABLE)

    --{{0}}--
DROP TABLE ist der gefährlichste DDL-Befehl. Einmal ausgeführt, ist die Tabelle weg – inklusive aller Daten. Nutzen Sie IF EXISTS, um Fehler zu vermeiden, und CASCADE/RESTRICT, um Abhängigkeiten zu kontrollieren.

    {{0}}
<section>

### Grundsyntax

**Einfaches DROP:**

```sql
DROP TABLE products;
```

**Mit Sicherheitsnetz:**

```sql
DROP TABLE IF EXISTS products;
```

**⚠️ Gefahr:**

- Tabelle wird **sofort** gelöscht
- Alle Daten gehen verloren
- Kann nicht rückgängig gemacht werden (außer Backup/Transaktion)

</section>

    --{{1}}--
CASCADE und RESTRICT steuern, was mit abhängigen Objekten passiert. CASCADE löscht alles mit (Views, Foreign Keys), RESTRICT verhindert das Löschen, wenn Abhängigkeiten existieren.

    {{1}}
<section>

### CASCADE vs. RESTRICT

**RESTRICT (Standard):**

```sql
-- Fehlschlägt, wenn andere Tabellen via FOREIGN KEY abhängen:
DROP TABLE products RESTRICT;
```

**CASCADE (Vorsicht!):**

```sql
-- Löscht Tabelle UND alle abhängigen Objekte (Views, FKs):
DROP TABLE products CASCADE;
```

**Beispiel:**

```sql
CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE products_fk (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  category_id INTEGER,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Fehlschlägt (products_fk hängt davon ab):
DROP TABLE categories RESTRICT;

-- Funktioniert (löscht auch FOREIGN KEY Constraint):
DROP TABLE categories CASCADE;
```
@PGlite.terminal(ddl_dml)

**💡 Best Practice:** Immer RESTRICT nutzen, außer Sie wissen genau, was Sie tun.

</section>

---

## Constraints – Datenintegrität sichern

    --{{0}}--
Constraints sind Regeln, die Ihre Daten schützen. PRIMARY KEY verhindert Duplikate, FOREIGN KEY sichert Beziehungen, CHECK validiert Werte. Ohne Constraints ist Ihre Datenbank ein Wilder Westen – jeder Wert ist erlaubt.

    {{0}}
<section>

### Warum Constraints?

**Ohne Constraints:**

```sql
CREATE TABLE orders_bad (
  order_id INTEGER,
  customer_id INTEGER,
  total DECIMAL(10,2)
);

-- Alles erlaubt:
INSERT INTO orders_bad VALUES (1, NULL, -100);  -- ❌ Kein Kunde, negativer Betrag
INSERT INTO orders_bad VALUES (1, 999, 50);     -- ❌ Duplikat-ID, nicht-existierender Kunde
```

**Mit Constraints:**

```sql
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE orders_good (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  total DECIMAL(10,2) CHECK (total >= 0),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Schutz aktiviert:
INSERT INTO orders_good VALUES (1, NULL, 50);    -- ❌ customer_id NOT NULL
INSERT INTO orders_good VALUES (1, 999, 50);     -- ❌ customer_id existiert nicht
INSERT INTO orders_good VALUES (1, 1, -100);     -- ❌ total CHECK fehlschlägt
```

</section>

---

## PRIMARY KEY

    --{{0}}--
PRIMARY KEY ist der wichtigste Constraint. Er garantiert Eindeutigkeit und NOT NULL. Jede Tabelle sollte einen Primärschlüssel haben – er ist die Identität jeder Zeile.

    {{0}}
<section>

### Single-Column vs. Composite Keys

**Single-Column (häufigster Fall):**

```sql
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  email TEXT
);
```

**Composite Key (mehrere Spalten):**

```sql
CREATE TABLE enrollments (
  student_id INTEGER,
  course_id INTEGER,
  enrollment_date DATE,
  PRIMARY KEY (student_id, course_id)  -- Ein Student kann jeden Kurs nur einmal belegen
);
```
@PGlite.eval(ddl_dml)

**Wann Composite Keys?**

- Viele-zu-Viele-Beziehungen (Student ↔ Kurs)
- Zeitreihendaten (sensor_id, timestamp)

</section>

    --{{1}}--
Natürliche vs. künstliche Keys: Natürlich = aus Daten (E-Mail, ISBN), künstlich = generiert (Auto-Increment ID). Künstliche Keys sind meist besser, weil sie unveränderlich sind.

    {{1}}
<section>

### Natürliche vs. künstliche Keys

**Natürlicher Key (aus Daten):**

```sql
CREATE TABLE books (
  isbn TEXT PRIMARY KEY,  -- ISBN ist natürlich eindeutig
  title TEXT,
  author TEXT
);
```

**Künstlicher Key (generiert):**

```sql
CREATE TABLE books_auto (
  book_id INTEGER PRIMARY KEY,  -- Auto-generiert
  isbn TEXT UNIQUE,
  title TEXT,
  author TEXT
);
```

**Wann was?**

| Kriterium | Natürlich | Künstlich |
|-----------|-----------|-----------|
| Unveränderlich | ❌ (z.B. E-Mail ändert sich) | ✅ |
| Performance | ⚠️ (Text-Keys langsamer) | ✅ (Integer schnell) |
| Lesbarkeit | ✅ (ISBN sagt etwas aus) | ❌ (ID 4711 ist abstrakt) |

**💡 Empfehlung:** Künstlicher Primärschlüssel + natürlicher UNIQUE Constraint

```sql
CREATE TABLE users_best (
  user_id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  username TEXT
);
```

</section>

---

## FOREIGN KEY

    --{{0}}--
FOREIGN KEY verbindet Tabellen. Er garantiert, dass Beziehungen gültig sind: Jede Bestellung muss einem existierenden Kunden gehören. Das ist referenzielle Integrität.

    {{0}}
<section>

### Referenzielle Integrität

**Beispiel: Kunden und Bestellungen**

```sql
CREATE TABLE customers_fk (
  customer_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE orders_fk (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  order_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers_fk(customer_id)
);

INSERT INTO customers_fk VALUES (1, 'Alice'), (2, 'Bob');

-- Funktioniert (customer_id 1 existiert):
INSERT INTO orders_fk VALUES (101, 1, '2025-11-04');

-- Fehlschlägt (customer_id 999 existiert nicht):
INSERT INTO orders_fk VALUES (102, 999, '2025-11-04');
```
@PGlite.terminal(ddl_dml)

**Was passiert bei Verstößen?**

- `INSERT`: Fehlschlag, wenn referenzierter Key nicht existiert
- `UPDATE`: Fehlschlag, wenn neuer Wert nicht existiert
- `DELETE`: Abhängig von ON DELETE (siehe unten)

</section>

    --{{1}}--
ON DELETE und ON UPDATE steuern, was passiert, wenn der referenzierte Datensatz gelöscht oder geändert wird. CASCADE löscht/ändert mit, SET NULL setzt NULL, RESTRICT verhindert die Aktion.

    {{1}}
<section>

### ON DELETE / ON UPDATE

| Option | Bei DELETE | Bei UPDATE |
|--------|------------|------------|
| `CASCADE` | Abhängige Zeilen werden auch gelöscht | Abhängige Zeilen werden aktualisiert |
| `SET NULL` | FK wird auf NULL gesetzt | FK wird auf NULL gesetzt |
| `RESTRICT` | Löschen/Ändern wird verhindert | Löschen/Ändern wird verhindert |
| `NO ACTION` | Wie RESTRICT (Standard) | Wie RESTRICT (Standard) |

**Beispiel: ON DELETE CASCADE**

```sql
CREATE TABLE authors (
  author_id INTEGER PRIMARY KEY,
  name TEXT
);

CREATE TABLE books_cascade (
  book_id INTEGER PRIMARY KEY,
  title TEXT,
  author_id INTEGER,
  FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

INSERT INTO authors VALUES (1, 'Tolkien');
INSERT INTO books_cascade VALUES (1, 'Hobbit', 1), (2, 'LOTR', 1);

-- Autor löschen → Bücher werden auch gelöscht:
DELETE FROM authors WHERE author_id = 1;

SELECT * FROM books_cascade;  -- Leer!
```
@PGlite.terminal(ddl_dml)

**Beispiel: ON DELETE SET NULL**

```sql
CREATE TABLE books_setnull (
  book_id INTEGER PRIMARY KEY,
  title TEXT,
  author_id INTEGER,
  FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE SET NULL
);

-- Autor löschen → author_id wird NULL:
DELETE FROM authors WHERE author_id = 1;
-- Bücher bleiben, aber ohne Autor
```

**💡 Wann was nutzen?**

- **CASCADE:** Abhängige Daten sind ohne Parent sinnlos (z.B. Bestellpositionen ohne Bestellung)
- **SET NULL:** Beziehung optional (z.B. Autor gelöscht, Buch bleibt)
- **RESTRICT:** Keine Löschung, solange Abhängigkeiten bestehen (Standard, sicher)

</section>

    --{{2}}--
Self-Referencing Foreign Keys sind nützlich für hierarchische Daten: Jeder Mitarbeiter hat einen Manager, der selbst ein Mitarbeiter ist. Jede Kategorie kann eine übergeordnete Kategorie haben.

    {{2}}
<section>

### Self-Referencing (Hierarchien)

**Beispiel: Mitarbeiter-Hierarchie**

```sql
CREATE TABLE employees (
  employee_id INTEGER PRIMARY KEY,
  name TEXT,
  manager_id INTEGER,
  FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

INSERT INTO employees VALUES 
  (1, 'CEO', NULL),           -- Kein Manager (Top)
  (2, 'CTO', 1),              -- Manager: CEO
  (3, 'Dev Lead', 2),         -- Manager: CTO
  (4, 'Developer', 3);        -- Manager: Dev Lead

-- Wer ist der Manager von Developer?
SELECT 
  e.name AS employee,
  m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
WHERE e.name = 'Developer';
```
@PGlite.terminal(ddl_dml)

**Use Cases:**

- Organisationshierarchien
- Kategorie-Bäume (Produkte → Elektronik → Laptops)
- Threads/Kommentare (parent_comment_id)

</section>

---

## UNIQUE, NOT NULL, CHECK, DEFAULT

    --{{0}}--
Diese Constraints sind einfacher, aber nicht weniger wichtig. UNIQUE verhindert Duplikate, NOT NULL erzwingt Werte, CHECK validiert Bedingungen, DEFAULT setzt Standardwerte.

    {{0}}
<section>

### UNIQUE – Eindeutigkeit ohne Primary Key

**Syntax:**

```sql
CREATE TABLE users_unique (
  user_id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE
);
```

**Unterschied zu PRIMARY KEY:**

- PRIMARY KEY: Eindeutig + NOT NULL + nur 1 pro Tabelle
- UNIQUE: Eindeutig, aber NULL erlaubt (mehrfach!), mehrere pro Tabelle

**NULL-Verhalten:**

```sql
INSERT INTO users_unique VALUES (1, 'alice@example.com', 'alice');
INSERT INTO users_unique VALUES (2, 'bob@example.com', NULL);   -- OK
INSERT INTO users_unique VALUES (3, 'charlie@example.com', NULL); -- OK (NULL != NULL)
```
@PGlite.terminal(ddl_dml)

**Composite UNIQUE:**

```sql
CREATE TABLE reservations (
  reservation_id INTEGER PRIMARY KEY,
  room_number INTEGER,
  date DATE,
  UNIQUE (room_number, date)  -- Raum kann pro Tag nur 1x gebucht werden
);
```

</section>

    --{{1}}--
NOT NULL ist der einfachste Constraint, aber extrem wichtig. Er verhindert NULL-Werte in Spalten, die immer einen Wert haben müssen.

    {{1}}
<section>

### NOT NULL – Pflichtfelder

**Syntax:**

```sql
CREATE TABLE products_nn (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  description TEXT  -- NULL erlaubt
);
```

**Warum wichtig?**

- NULL ist nicht 0, nicht leerer String – es ist "unbekannt"
- Berechnungen mit NULL geben NULL zurück
- WHERE-Bedingungen können scheitern

**Beispiel:**

```sql
-- Fehlschlägt (name ist NOT NULL):
INSERT INTO products_nn (product_id, price) VALUES (1, 99.99);

-- Funktioniert:
INSERT INTO products_nn (product_id, name, price) VALUES (1, 'Laptop', 999.99);
```
@PGlite.terminal(ddl_dml)

</section>

    --{{2}}--
CHECK ermöglicht benutzerdefinierte Validierung. Sie können Bereiche prüfen, Muster validieren, Bedingungen zwischen Spalten definieren.

    {{2}}
<section>

### CHECK – Benutzerdefinierte Validierung

**Syntax:**

```sql
CHECK (condition)
```

**Beispiele:**

```sql
CREATE TABLE products_check (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price DECIMAL(10,2) CHECK (price >= 0),
  discount_percent INTEGER CHECK (discount_percent BETWEEN 0 AND 100),
  stock INTEGER CHECK (stock >= 0),
  release_date DATE CHECK (release_date >= CURRENT_DATE)
);
```
@PGlite.eval(ddl_dml)

**Multi-Column Checks:**

```sql
CREATE TABLE discounts (
  discount_id INTEGER PRIMARY KEY,
  start_date DATE,
  end_date DATE,
  CHECK (end_date > start_date)  -- Ende muss nach Start sein
);
```

**Enum-Simulation:**

```sql
CREATE TABLE orders_status (
  order_id INTEGER PRIMARY KEY,
  status TEXT CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled'))
);

-- Fehlschlägt (ungültiger Status):
INSERT INTO orders_status VALUES (1, 'in_transit');
```
@PGlite.terminal(ddl_dml)

</section>

    --{{3}}--
DEFAULT setzt Standardwerte, wenn beim INSERT kein Wert angegeben wird. Praktisch für Zeitstempel, Flags, Status.

    {{3}}
<section>

### DEFAULT – Standardwerte

**Syntax:**

```sql
CREATE TABLE products_default (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
@PGlite.eval(ddl_dml)

**Nutzung:**

```sql
-- Ohne stock, is_active, created_at:
INSERT INTO products_default (product_id, name, price) 
VALUES (1, 'Laptop', 999.99);

SELECT * FROM products_default;
-- → stock = 0, is_active = TRUE, created_at = jetzt
```
@PGlite.terminal(ddl_dml)

**Funktionen als Default:**

```sql
CREATE TABLE logs (
  log_id INTEGER PRIMARY KEY,
  message TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  random_id TEXT DEFAULT (gen_random_uuid()::TEXT)
);
```

</section>

---

## DML – INSERT

    --{{0}}--
Jetzt verlassen wir DDL und gehen zu DML: Daten manipulieren. INSERT fügt neue Zeilen ein. Sie können einzelne Zeilen einfügen, mehrere gleichzeitig, oder Daten aus anderen Tabellen kopieren.

    {{0}}
<section>

### Einzelne Zeile einfügen

**Syntax:**

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

**Beispiel:**

```sql
CREATE TABLE customers_insert (
  customer_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers_insert (customer_id, name, email)
VALUES (1, 'Alice', 'alice@example.com');

SELECT * FROM customers_insert;
```
@PGlite.terminal(ddl_dml)

**Alle Spalten (Reihenfolge wie in CREATE TABLE):**

```sql
INSERT INTO customers_insert
VALUES (2, 'Bob', 'bob@example.com', CURRENT_TIMESTAMP);
```

</section>

    --{{1}}--
Bulk Insert ist effizienter als viele einzelne INSERTs. Statt 100 Befehle schreiben Sie einen mit 100 Wertepaaren.

    {{1}}
<section>

### Mehrere Zeilen gleichzeitig (Bulk Insert)

**Syntax:**

```sql
INSERT INTO table_name (columns)
VALUES 
  (values1),
  (values2),
  (values3),
  ...;
```

**Beispiel:**

```sql
INSERT INTO customers_insert (customer_id, name, email) VALUES
  (3, 'Charlie', 'charlie@example.com'),
  (4, 'Diana', 'diana@example.com'),
  (5, 'Eve', 'eve@example.com');

SELECT * FROM customers_insert;
```
@PGlite.terminal(ddl_dml)

**Performance-Vorteil:**

- 1 INSERT mit 1000 Zeilen: ~10ms
- 1000 einzelne INSERTs: ~1000ms

</section>

    --{{2}}--
INSERT ... SELECT kopiert Daten aus einer anderen Tabelle. Praktisch für Backups, Datenmigrationen, berechnete Tabellen.

    {{2}}
<section>

### INSERT ... SELECT

**Syntax:**

```sql
INSERT INTO target_table (columns)
SELECT columns FROM source_table WHERE condition;
```

**Beispiel: Backup erstellen**

```sql
CREATE TABLE customers_backup (
  customer_id INTEGER,
  name TEXT,
  email TEXT,
  backup_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO customers_backup (customer_id, name, email)
SELECT customer_id, name, email FROM customers_insert;

SELECT * FROM customers_backup;
```
@PGlite.terminal(ddl_dml)

**Beispiel: Gefilterte Kopie**

```sql
-- Nur Kunden mit E-Mail:
INSERT INTO customers_backup (customer_id, name, email)
SELECT customer_id, name, email 
FROM customers_insert 
WHERE email IS NOT NULL;
```

</section>

    --{{3}}--
Upsert (INSERT ... ON CONFLICT) ist ein fortgeschrittenes Pattern: „Füge ein, oder update, wenn schon vorhanden." Praktisch für Daten-Synchronisation.

    {{3}}
<section>

### INSERT ... ON CONFLICT (Upsert)

**Problem:** Was, wenn die ID schon existiert?

```sql
-- Fehlschlägt (customer_id 1 existiert schon):
INSERT INTO customers_insert (customer_id, name, email)
VALUES (1, 'Alice Updated', 'alice_new@example.com');
```

**Lösung: ON CONFLICT DO UPDATE**

```sql
INSERT INTO customers_insert (customer_id, name, email)
VALUES (1, 'Alice Updated', 'alice_new@example.com')
ON CONFLICT (customer_id) DO UPDATE
SET 
  name = EXCLUDED.name,
  email = EXCLUDED.email;

SELECT * FROM customers_insert WHERE customer_id = 1;
```
@PGlite.terminal(ddl_dml)

**ON CONFLICT DO NOTHING:**

```sql
-- Ignoriere Duplikate:
INSERT INTO customers_insert (customer_id, name, email)
VALUES (1, 'Alice', 'alice@example.com')
ON CONFLICT (customer_id) DO NOTHING;
```

**💡 Use Cases:**

- Daten-Sync aus externen Systemen
- Idempotente Pipelines (mehrfaches Ausführen = gleiches Ergebnis)

</section>

---

## DML – UPDATE

    --{{0}}--
UPDATE ändert bestehende Daten. Der gefährlichste Befehl ist UPDATE ohne WHERE – dann werden ALLE Zeilen geändert. Immer mit WHERE filtern!

    {{0}}
<section>

### UPDATE mit WHERE

**Syntax:**

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

**Beispiel:**

```sql
-- Einzelne Zeile ändern:
UPDATE customers_insert
SET email = 'alice_updated@example.com'
WHERE customer_id = 1;

SELECT * FROM customers_insert WHERE customer_id = 1;
```
@PGlite.terminal(ddl_dml)

**⚠️ GEFAHR: UPDATE ohne WHERE**

```sql
-- ALLE Zeilen werden geändert!
UPDATE customers_insert
SET name = 'Unknown';

-- Jetzt heißen ALLE Kunden "Unknown"!
```

**💡 Best Practice:** Immer WHERE nutzen, außer Sie wollen wirklich alle Zeilen ändern.

</section>

    --{{1}}--
Sie können mehrere Spalten gleichzeitig ändern und berechnete Updates machen.

    {{1}}
<section>

### Mehrere Spalten & berechnete Updates

**Mehrere Spalten:**

```sql
UPDATE customers_insert
SET 
  name = 'Alice Smith',
  email = 'alice.smith@example.com'
WHERE customer_id = 1;
```

**Berechnete Updates:**

```sql
CREATE TABLE products_update (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  price DECIMAL(10,2),
  stock INTEGER
);

INSERT INTO products_update VALUES 
  (1, 'Laptop', 1000.00, 50),
  (2, 'Mouse', 25.00, 200);

-- Preiserhöhung um 10%:
UPDATE products_update
SET price = price * 1.10;

-- Stock reduzieren:
UPDATE products_update
SET stock = stock - 5
WHERE product_id = 1;

SELECT * FROM products_update;
```
@PGlite.terminal(ddl_dml)

</section>

    --{{2}}--
UPDATE mit Subqueries oder Joins ist fortgeschritten, aber sehr mächtig. Sie können Werte aus anderen Tabellen holen und einfügen.

    {{2}}
<section>

### UPDATE mit Subquery (Fortgeschritten)

**Beispiel: Preis basierend auf Kategorie anpassen**

```sql
CREATE TABLE categories_update (
  category_id INTEGER PRIMARY KEY,
  name TEXT,
  discount_percent DECIMAL(5,2)
);

CREATE TABLE products_cat (
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  price DECIMAL(10,2),
  category_id INTEGER
);

INSERT INTO categories_update VALUES (1, 'Electronics', 10.00), (2, 'Books', 5.00);
INSERT INTO products_cat VALUES 
  (1, 'Laptop', 1000.00, 1),
  (2, 'Novel', 20.00, 2);

-- Preis mit Kategorie-Discount reduzieren:
UPDATE products_cat
SET price = price * (1 - (
  SELECT discount_percent / 100 
  FROM categories_update 
  WHERE categories_update.category_id = products_cat.category_id
));

SELECT * FROM products_cat;
```
@PGlite.terminal(ddl_dml)

</section>

---

## DML – DELETE

    --{{0}}--
DELETE entfernt Zeilen. Wie bei UPDATE gilt: Immer mit WHERE, außer Sie wollen wirklich alles löschen. DELETE ist reversibel (via Transaktion), TRUNCATE nicht.

    {{0}}
<section>

### DELETE mit WHERE

**Syntax:**

```sql
DELETE FROM table_name
WHERE condition;
```

**Beispiel:**

```sql
-- Einzelne Zeile löschen:
DELETE FROM customers_insert
WHERE customer_id = 5;

-- Mehrere Zeilen:
DELETE FROM customers_insert
WHERE email IS NULL;

SELECT * FROM customers_insert;
```
@PGlite.terminal(ddl_dml)

**⚠️ GEFAHR: DELETE ohne WHERE**

```sql
-- ALLE Zeilen werden gelöscht!
DELETE FROM customers_insert;

-- Tabelle ist jetzt leer!
```

</section>

    --{{1}}--
TRUNCATE vs. DELETE: TRUNCATE ist schneller, aber weniger flexibel. DELETE kann mit WHERE filtern und ist in Transaktionen reversibel.

    {{1}}
<section>

### TRUNCATE vs. DELETE

| Feature | DELETE | TRUNCATE |
|---------|--------|----------|
| WHERE-Klausel | ✅ Ja | ❌ Nein (alle Zeilen) |
| Performance | ⚠️ Langsamer (Zeile für Zeile) | ✅ Schneller (gesamte Tabelle) |
| Rollback | ✅ In Transaktion möglich | ⚠️ Meist nicht (DB-abhängig) |
| Triggers | ✅ Werden ausgelöst | ❌ Meist nicht |
| Auto-Increment Reset | ❌ Nein | ✅ Ja (zurück auf 1) |

**Beispiel:**

```sql
-- DELETE: Kann WHERE nutzen
DELETE FROM products_update WHERE price < 50;

-- TRUNCATE: Löscht alles
TRUNCATE TABLE products_update;
```

**💡 Wann was?**

- **DELETE:** Selektives Löschen, Transaktionen wichtig
- **TRUNCATE:** Komplettes Leeren, Performance wichtig

</section>

    --{{2}}--
Soft Delete ist ein Pattern, bei dem Sie Daten nicht wirklich löschen, sondern nur als "gelöscht" markieren. Praktisch für Audit-Trails und Wiederherstellung.

    {{2}}
<section>

### Soft Delete Pattern

**Problem:** Gelöschte Daten sind weg – kein Audit-Trail, keine Wiederherstellung.

**Lösung: Status-Flag**

```sql
CREATE TABLE users_soft (
  user_id INTEGER PRIMARY KEY,
  username TEXT,
  email TEXT,
  is_deleted BOOLEAN DEFAULT FALSE,
  deleted_at TIMESTAMP
);

INSERT INTO users_soft (user_id, username, email) VALUES
  (1, 'alice', 'alice@example.com'),
  (2, 'bob', 'bob@example.com');

-- Statt DELETE:
UPDATE users_soft
SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
WHERE user_id = 1;

-- View für aktive User:
CREATE VIEW active_users AS
SELECT * FROM users_soft WHERE is_deleted = FALSE;

SELECT * FROM active_users;
```
@PGlite.terminal(ddl_dml)

**Vorteile:**

- ✅ Wiederherstellung möglich (SET is_deleted = FALSE)
- ✅ Audit-Trail (wann wurde gelöscht?)
- ✅ Analytics über gelöschte Daten

**Nachteile:**

- ❌ Tabelle wird größer
- ❌ Queries komplexer (immer WHERE is_deleted = FALSE)

</section>

---

## Schema-Evolution & Best Practices

    --{{0}}--
Schemas ändern sich im Lauf der Zeit. Neue Features erfordern neue Spalten, Refactorings ändern Strukturen. Wie machen Sie das sicher, ohne Downtime, ohne Datenverlust?

    {{0}}
<section>

### Migrations-Konzept

**Problem:** Schema-Änderungen müssen nachvollziehbar und wiederholbar sein.

**Lösung: Migrations (Up/Down)**

```sql
-- Migration 001: Initial Schema
-- UP:
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  username TEXT NOT NULL
);

-- DOWN:
DROP TABLE users;
```

```sql
-- Migration 002: Add Email
-- UP:
ALTER TABLE users ADD COLUMN email TEXT;

-- DOWN:
ALTER TABLE users DROP COLUMN email;
```

**Tools:**

- **Flyway** (Java): SQL-basiert, einfach
- **Liquibase** (Java): XML/YAML, komplex aber mächtig
- **Alembic** (Python): Code-basiert, für SQLAlchemy
- **Migrate** (Go): Einfach, Library

**Workflow:**

1. Entwicklung: Neue Migration schreiben
2. Review: Migration prüfen (Syntax, Logik)
3. Test: Auf Testdatenbank anwenden
4. Produktion: Rollout mit Monitoring

</section>

    --{{1}}--
Sichere Schema-Änderungen vermeiden Downtime. ADD COLUMN ist meist sicher, DROP COLUMN riskant. Große Tabellen erfordern besondere Vorsicht.

    {{1}}
<section>

### Sichere Schema-Änderungen

**✅ Sicher (keine Downtime):**

```sql
-- Spalte mit DEFAULT hinzufügen:
ALTER TABLE products ADD COLUMN category TEXT DEFAULT 'Uncategorized';

-- Index erstellen (CONCURRENT in PostgreSQL):
CREATE INDEX CONCURRENTLY idx_products_category ON products(category);
```

**⚠️ Riskant (Lock/Downtime):**

```sql
-- Datentyp ändern (gesamte Tabelle wird gesperrt):
ALTER TABLE products ALTER COLUMN price TYPE DECIMAL(12,2);

-- Spalte löschen (Lock):
ALTER TABLE products DROP COLUMN description;
```

**💡 Best Practices:**

1. **ADD COLUMN mit DEFAULT:** Schnell, keine Lock-Probleme
2. **NOT NULL schrittweise:**
   - Schritt 1: Spalte als NULL hinzufügen
   - Schritt 2: Werte füllen (UPDATE)
   - Schritt 3: NOT NULL Constraint hinzufügen
3. **Große Tabellen:** Off-Peak-Zeiten nutzen
4. **Indexes:** CONCURRENT erstellen (PostgreSQL)

</section>

    --{{2}}--
Rückwärtskompatibilität ist wichtig, wenn mehrere App-Versionen parallel laufen. Neue Spalten sollten optional sein, alte Spalten nicht sofort gelöscht werden.

    {{2}}
<section>

### Rückwärtskompatibilität

**Problem:** App v1 läuft noch, aber DB-Schema ist für App v2.

**Strategie: Expand-Contract**

1. **Expand:** Neue Spalte hinzufügen (optional)
2. **Migrate:** App v2 deployed, nutzt neue Spalte
3. **Contract:** Nach Rollout alte Spalte löschen

**Beispiel:**

```sql
-- Phase 1: EXPAND (neue Spalte hinzufügen)
ALTER TABLE users ADD COLUMN email_new TEXT;

-- Phase 2: MIGRATE
-- App v2 schreibt in email_new
-- App v1 schreibt weiter in email

-- Phase 3: CONTRACT (nach vollständigem Rollout)
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_new TO email;
```

**💡 Best Practice:** Niemals breaking changes ohne Übergangsphase!

</section>

---

## Ausblick: Transaktionen

    --{{0}}--
Ein letzter Punkt, den wir heute nur kurz anreißen: Transaktionen. Sie haben INSERT, UPDATE, DELETE gelernt – aber was, wenn Sie mehrere Operationen atomar ausführen wollen? „Entweder alles oder nichts"? Das sind Transaktionen.

    {{0}}
<section>

### Warum Transaktionen?

**Problem:**

```sql
-- Geldtransfer:
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;  -- ✅ OK
-- ❌ Fehler! Server-Crash!
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;  -- Wird nie ausgeführt
-- → 100 Euro verschwunden!
```

**Lösung: Transaktion**

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;  -- Beide oder keine
```

**Wenn Fehler:**

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
  -- Fehler hier!
ROLLBACK;  -- Alles rückgängig
```

</section>

    --{{1}}--
Transaktionen lernen Sie ausführlich in Session 11+, nach Joins. Warum später? Weil Transaktionen erst bei Multi-Table-Operations richtig relevant werden. Für heute reicht: Sie existieren, sie garantieren ACID (Atomicity, Consistency, Isolation, Durability), und wir kommen darauf zurück.

---

## Zusammenfassung

    --{{0}}--
Was haben Sie gelernt? DDL für Schema-Design: CREATE TABLE mit Datentypen und Constraints, ALTER TABLE für Änderungen, DROP TABLE zum Löschen. DML für Datenmanipulation: INSERT zum Einfügen, UPDATE zum Ändern, DELETE zum Löschen. Constraints für Integrität: PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, DEFAULT. Und Best Practices für sichere Schema-Evolution.

    {{0}}
<section>

| Konzept | Befehl | Zweck |
|---------|--------|-------|
| **DDL** | `CREATE TABLE` | Tabelle erstellen |
| | `ALTER TABLE` | Tabelle ändern |
| | `DROP TABLE` | Tabelle löschen |
| **Constraints** | `PRIMARY KEY` | Eindeutigkeit + NOT NULL |
| | `FOREIGN KEY` | Referenzielle Integrität |
| | `UNIQUE` | Eindeutigkeit (NULL erlaubt) |
| | `NOT NULL` | Pflichtfeld |
| | `CHECK` | Benutzerdefinierte Validierung |
| | `DEFAULT` | Standardwert |
| **DML** | `INSERT` | Daten einfügen |
| | `UPDATE` | Daten ändern |
| | `DELETE` | Daten löschen |

</section>

    --{{1}}--
Die wichtigsten Takeaways: Nutzen Sie Constraints – sie schützen Ihre Daten. Immer WHERE bei UPDATE/DELETE – außer Sie wollen wirklich alles ändern. Künstliche Primary Keys sind meist besser als natürliche. FOREIGN KEY mit ON DELETE/UPDATE steuert Kaskaden. Und: Schema-Evolution ist ein Prozess, keine einmalige Aktion.

---

## Best Practices: Checkliste

    --{{0}}--
Zum Abschluss eine Checkliste, die Sie bei jedem Schema-Design durchgehen sollten.

    {{0}}
<section>

**Schema-Design:**

- [ ] Jede Tabelle hat einen PRIMARY KEY
- [ ] Künstliche Keys (INTEGER) statt natürliche (TEXT) für Performance
- [ ] FOREIGN KEYs für alle Beziehungen definiert
- [ ] ON DELETE/UPDATE explizit gewählt (CASCADE/RESTRICT/SET NULL)
- [ ] NOT NULL für alle Pflichtfelder
- [ ] CHECK Constraints für Validierung (z.B. price >= 0)
- [ ] DEFAULT für sinnvolle Standardwerte (z.B. created_at)

**Datenmanipulation:**

- [ ] INSERT: Spalten explizit benennen, nicht auf Reihenfolge verlassen
- [ ] UPDATE: Immer mit WHERE (außer wirklich alle Zeilen ändern)
- [ ] DELETE: Immer mit WHERE (außer wirklich alle Zeilen löschen)
- [ ] Bulk Operations nutzen (1 INSERT mit 100 Zeilen statt 100 INSERTs)

**Schema-Evolution:**

- [ ] Migrations-System nutzen (Flyway, Liquibase, Alembic)
- [ ] Jede Änderung hat UP + DOWN Migration
- [ ] Rückwärtskompatibilität beachten (Expand-Contract)
- [ ] Große Änderungen off-peak ausführen

**Sicherheit:**

- [ ] Keine DDL/DML in Produktion ohne Backup
- [ ] Transaktionen für multi-step Operationen (ab Session 11)
- [ ] Testen auf Testdatenbank vor Produktion

</section>

---

## Quiz: Testen Sie Ihr Wissen

**Frage 1: Was ist der Unterschied zwischen PRIMARY KEY und UNIQUE?**

- [( )] Kein Unterschied
- [(X)] PRIMARY KEY ist eindeutig + NOT NULL, UNIQUE erlaubt NULL
- [( )] UNIQUE ist schneller als PRIMARY KEY
- [( )] PRIMARY KEY kann mehrfach pro Tabelle vorkommen

**Frage 2: Was passiert bei ON DELETE CASCADE?**

- [( )] Löschen wird verhindert
- [(X)] Abhängige Zeilen werden auch gelöscht
- [( )] Foreign Key wird auf NULL gesetzt
- [( )] Nichts

**Frage 3: Was macht TRUNCATE im Vergleich zu DELETE?**

- [(X)] TRUNCATE ist schneller, löscht alle Zeilen, kein WHERE möglich
- [( )] TRUNCATE ist langsamer als DELETE
- [( )] TRUNCATE löscht nur eine Zeile
- [( )] Kein Unterschied

**Frage 4: Warum sollten Sie UPDATE ohne WHERE vermeiden?**

- [( )] Es ist langsamer
- [( )] Es funktioniert nicht
- [(X)] Es ändert ALLE Zeilen in der Tabelle
- [( )] Es ist unsicher (SQL Injection)

**Frage 5: Was ist der Vorteil von künstlichen Primary Keys (INTEGER) gegenüber natürlichen (z.B. E-Mail)?**

- [( )] Künstliche Keys sind lesbarer
- [(X)] Künstliche Keys sind unveränderlich und schneller
- [( )] Natürliche Keys sind besser
- [( )] Kein Unterschied

---

## Übungsaufgaben

    --{{0}}--
Zeit für Praxis! Probieren Sie diese Aufgaben selbst aus.

**Aufgabe 1: Tabelle erstellen**

Erstellen Sie eine `students` Tabelle mit:
- `student_id` (Primary Key, Integer)
- `first_name` und `last_name` (NOT NULL)
- `email` (UNIQUE, NOT NULL)
- `enrollment_date` (DEFAULT: aktuelles Datum)
- `gpa` (CHECK: zwischen 0.0 und 4.0)

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    CREATE TABLE students (
      student_id INTEGER PRIMARY KEY,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      enrollment_date DATE DEFAULT CURRENT_DATE,
      gpa DECIMAL(3,2) CHECK (gpa BETWEEN 0.0 AND 4.0)
    );
    ```
    @PGlite.terminal(ddl_dml)
    
    *******************

**Aufgabe 2: Foreign Key**

Erstellen Sie eine `enrollments` Tabelle, die `students` mit `courses` verbindet:
- Composite Primary Key (student_id, course_id)
- Foreign Keys zu beiden Tabellen
- ON DELETE CASCADE für beide

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    CREATE TABLE courses (
      course_id INTEGER PRIMARY KEY,
      title TEXT NOT NULL
    );
    
    CREATE TABLE enrollments (
      student_id INTEGER,
      course_id INTEGER,
      grade TEXT,
      PRIMARY KEY (student_id, course_id),
      FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
      FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
    );
    ```
    @PGlite.terminal(ddl_dml)
    
    *******************

**Aufgabe 3: INSERT & UPDATE**

1. Fügen Sie 3 Students ein
2. Fügen Sie 2 Courses ein
3. Enrollen Sie Students in Courses
4. Aktualisieren Sie den GPA eines Students

    [[Lösung anzeigen]]
    *******************
    
    ```sql
    INSERT INTO students (student_id, first_name, last_name, email, gpa) VALUES
      (1, 'Alice', 'Smith', 'alice@university.edu', 3.8),
      (2, 'Bob', 'Jones', 'bob@university.edu', 3.5),
      (3, 'Charlie', 'Brown', 'charlie@university.edu', 3.9);
    
    INSERT INTO courses (course_id, title) VALUES
      (1, 'Databases'),
      (2, 'Algorithms');
    
    INSERT INTO enrollments (student_id, course_id, grade) VALUES
      (1, 1, 'A'),
      (1, 2, 'B'),
      (2, 1, 'A-');
    
    UPDATE students
    SET gpa = 3.85
    WHERE student_id = 1;
    
    SELECT * FROM students;
    SELECT * FROM enrollments;
    ```
    @PGlite.terminal(ddl_dml)
    
    *******************

---

## Ausblick: Was kommt als Nächstes?

    --{{0}}--
Sie können jetzt Schemas erstellen, Daten einfügen, ändern, löschen. Aber Ihre Queries sind noch auf eine Tabelle beschränkt. Was, wenn Sie Daten aus mehreren Tabellen kombinieren wollen? Das sind Joins – unser nächstes großes Thema.

**Kommende Sessions:**

- **Session 9:** SQL Filtering & Operators (BETWEEN, IN, LIKE, CASE)
- **Session 10:** SQL Joins & Combining Data (INNER, LEFT, RIGHT, FULL, CROSS)
- **Session 11+:** Transaktionen & ACID (nach Joins)
- **Session 12:** Aggregation & Window Functions
- **Session 15:** Performance Optimization & Indexing

🎉 **Glückwunsch!** Sie beherrschen jetzt DDL & DML – das Fundament jeder Datenbank-Arbeit!
