<!--
author:   André Dietrich
email:    andre.dietrich@informatik.tu-freiberg.de
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  Functions & Trigger – Server-seitige Logik in der Datenbank. Von einfachen Stored Functions mit IF/CASE bis zu automatischen Triggern für Timestamps, Audit-Logging und Validierung. Alle Konzepte mit interaktiven PGlite-Demos: Schreiben Sie wiederverwendbare Funktionen und lassen Sie die Datenbank auf Änderungen reagieren!

logo:     

edit:     true

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md

-->

# Session 15 – Functions & Trigger

> **Session-Typ:** Vorlesung  
> **Dauer:** 90 Minuten  
> **Lernziele:** Stored Functions schreiben, Trigger erstellen, Automatisierung verstehen

    --{{0}}--
Willkommen zu Session 15! Heute schauen wir uns an, wie wir Logik nicht nur in unserer Anwendung, sondern direkt in der Datenbank ausführen können. Warum ist das sinnvoll? Stellen Sie sich vor, Sie möchten, dass bei jeder Änderung an einem Produkt automatisch ein Timestamp aktualisiert wird – oder dass jede Preisänderung protokolliert wird. Das manuell in jeder Anwendung zu implementieren ist fehleranfällig. Besser: Die Datenbank macht es automatisch! Heute lernen Sie Functions und Trigger kennen – und probieren alles direkt im Browser aus.

---

## Motivation: Warum Logik in der Datenbank?

    --{{0}}--
Beginnen wir mit einer Frage: Wo sollte Geschäftslogik leben? In der Anwendung oder in der Datenbank? Die Antwort ist: Es kommt darauf an! Aber für bestimmte Aufgaben ist die Datenbank der perfekte Ort.

### Problem 1: Vergessene Timestamps

    --{{0}}--
Klassisches Szenario: Sie wollen bei jeder Änderung an einem Datensatz das "updated_at" Feld aktualisieren.

      {{0-1}}
<div>

**Ohne Automatisierung (Anwendungsseite):**

```javascript
// In jeder Update-Funktion manuell:
await db.query(
  'UPDATE products SET price = $1, updated_at = NOW() WHERE id = $2',
  [newPrice, productId]
);

// ❌ Fehleranfällig: Was, wenn jemand vergisst, updated_at zu setzen?
// ❌ Duplizierter Code: In 50 verschiedenen Update-Funktionen
// ❌ Inkonsistent: Manche Entwickler machen es, andere nicht
```

</div>

    --{{1}}--
Mit einem Trigger ist das Problem gelöst – einmal definiert, funktioniert es immer. Automatisch. Konsistent. Ohne dass die Anwendung daran denken muss.

      {{1-2}}
<div>

**Mit Trigger (Datenbank):**

```sql
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- ✅ Funktioniert immer, egal welche Anwendung zugreift
-- ✅ Code an einer zentralen Stelle
-- ✅ Konsistent für alle Updates
```

</div>

### Problem 2: Audit-Logging

    --{{2}}--
Zweites Szenario: Sie wollen nachvollziehen, wer wann welche Preise geändert hat. Compliance-Anforderung!

      {{2-3}}
<div>

**Ohne Trigger:**

```javascript
// In jedem Update manuell protokollieren
await db.query('UPDATE products SET price = $1 WHERE id = $2', [newPrice, id]);
await db.query(
  'INSERT INTO audit_log (table_name, action, old_value, new_value) VALUES ($1, $2, $3, $4)',
  ['products', 'UPDATE', oldPrice, newPrice]
);

// ❌ Zwei Queries – was bei Fehler zwischen beiden?
// ❌ Entwickler muss daran denken
// ❌ Audit-Log kann vergessen werden
```

</div>

    --{{3}}--
Mit einem Trigger passiert das Logging automatisch – transparent, konsistent, fehlerfrei.

      {{3-4}}
<div>

**Mit Trigger:**

```sql
CREATE TRIGGER audit_changes
AFTER UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION log_change();

-- ✅ Automatisch bei jedem Update
-- ✅ Kann nicht vergessen werden
-- ✅ Atomar: Entweder beide Operationen oder keine
```

</div>

### Use Cases für Functions & Trigger

    --{{4}}--
Wann machen Functions und Trigger Sinn? Hier ist eine Übersicht:

      {{4}}
<div>

| Use Case | Functions | Trigger |
|----------|-----------|---------|
| Berechnungen (z.B. Steuer, Rabatt) | ✅ Wiederverwendbar | ⚠️ Automatisch bei jedem Event |
| Validierung (z.B. negative Preise verhindern) | ✅ Kann manuell aufgerufen werden | ✅✅ Automatisch, kann nicht umgangen werden |
| Automatische Timestamps | ⚠️ Muss aufgerufen werden | ✅✅ Automatisch bei INSERT/UPDATE |
| Audit-Logging | ⚠️ Muss explizit aufgerufen werden | ✅✅ Automatisch, konsistent |
| Soft Delete (Löschen = Markieren) | ⚠️ Muss implementiert werden | ✅✅ Überschreibt DELETE automatisch |
| Komplexe Geschäftslogik | ✅ Gut testbar, wiederverwendbar | ⚠️ Schwer zu debuggen |

**Faustregel:**

- **Functions** = Wiederverwendbare Logik, die Sie aktiv aufrufen
- **Trigger** = Automatische Reaktion auf Datenbankänderungen

</div>

    --{{5}}--
Heute lernen Sie beide Konzepte kennen – und zwar nicht nur theoretisch, sondern mit vielen praktischen Demos, die Sie direkt im Browser ausprobieren können!

---

## Teil 1: Stored Functions

    --{{0}}--
Beginnen wir mit Stored Functions. Das sind quasi JavaScript-Funktionen, aber in der Datenbank. Sie schreiben sie einmal, speichern sie in der Datenbank – und können sie dann in Queries verwenden.

### Was sind Stored Functions?

    --{{0}}--
Eine Stored Function ist ein Stück SQL-Code, das in der Datenbank gespeichert wird und wiederverwendet werden kann.

      {{0-1}}
<div>

**Vorteile:**

- ✅ **Wiederverwendbarkeit:** Einmal schreiben, überall nutzen
- ✅ **Performance:** Code läuft auf dem Datenbankserver (kein Netzwerk-Overhead)
- ✅ **Konsistenz:** Eine zentrale Definition, keine Duplikation
- ✅ **Sicherheit:** Benutzer können Funktionen aufrufen, ohne Tabellenzugriff zu haben

**Nachteile:**

- ⚠️ **Portabilität:** Syntax unterscheidet sich zwischen Datenbanken
- ⚠️ **Debugging:** Schwieriger als Anwendungscode
- ⚠️ **Testing:** Unit-Tests sind komplizierter

</div>

### Grundlegende Syntax

    --{{1}}--
Die Syntax für `CREATE FUNCTION` sieht in PostgreSQL so aus:

      {{1-2}}
<div>

```sql
CREATE FUNCTION function_name(parameter1 TYPE, parameter2 TYPE, ...)
RETURNS return_type AS $$
BEGIN
    -- Funktionskörper
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

**Wichtige Bestandteile:**

- `CREATE FUNCTION function_name(...)` – Name und Parameter
- `RETURNS return_type` – Was gibt die Funktion zurück? (INT, TEXT, DECIMAL, ...)
- `$$ ... $$` – String-Delimiter (statt `'...'`), macht Code lesbarer
- `BEGIN ... END;` – Der eigentliche Code
- `LANGUAGE plpgsql` – PostgreSQL's Procedural Language

</div>

### Demo 1: Einfache Addition

    --{{2}}--
Schauen wir uns ein ganz einfaches Beispiel an: Eine Funktion, die zwei Zahlen addiert.

      {{2}}
``` sql
CREATE FUNCTION add_numbers(a INT, b INT)
RETURNS INT AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;

-- Aufruf
SELECT add_numbers(5, 3) as result;
```
@PGlite.terminal

    --{{3}}--
Das war's! Sie sehen: Parameter in Klammern, Rückgabetyp mit RETURNS, und im Body ein einfaches RETURN. Probieren Sie es aus – ändern Sie die Zahlen!

### Demo 2: String-Verarbeitung

    --{{3}}--
Functions können auch mit Strings arbeiten. Hier eine Grußfunktion:

      {{3}}
``` sql
CREATE FUNCTION greet(name TEXT)
RETURNS TEXT AS $$
BEGIN
    IF name IS NULL THEN
        RETURN 'Hallo Unbekannter!';
    ELSE
        RETURN 'Hallo ' || name || '!';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Aufruf
SELECT greet('Alice') as greeting;
SELECT greet('Bob') as greeting;
SELECT greet(NULL) as greeting;
```
@PGlite.terminal

    --{{4}}--
Hier sehen Sie das erste Mal IF...THEN...ELSE. Schauen wir uns Kontrollstrukturen genauer an.

---

## Kontrollstrukturen: IF & CASE

### IF / THEN / ELSE

    --{{0}}--
Mit IF können Sie Bedingungen prüfen – wie in jeder Programmiersprache.

      {{0-1}}
<div>

**Syntax:**

```sql
IF condition THEN
    -- Code, wenn wahr
ELSE
    -- Code, wenn falsch
END IF;
```

**Wichtig:**

- `THEN` nach der Bedingung
- `END IF;` zum Abschließen (nicht nur `END`)

</div>

### Demo 3: Alterscheck

    --{{1}}--
Ein praktisches Beispiel: Prüfen, ob jemand volljährig ist.

      {{1}}
``` sql
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

-- Testen
SELECT check_age(25) as status;
SELECT check_age(16) as status;
SELECT check_age(18) as status;  -- Grenzfall
SELECT check_age(NULL) as status; -- Was passiert hier?
```
@PGlite.eval

    --{{2}}--
Beachten Sie: Bei NULL gibt die Funktion auch NULL zurück – denn NULL >= 18 ist NULL, also falsch. Das ist SQL-Logik!

### CASE: Alternative zu IF

    --{{2}}--
Für Mehrfachauswahl ist CASE oft eleganter als verschachtelte IFs.

      {{2-3}}
<div>

**Syntax:**

```sql
RETURN CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result
END;
```

</div>

### Demo 4: Notensystem

    --{{3}}--
Ein Notensystem – perfekt für CASE:

      {{3}}
``` sql
CREATE FUNCTION get_grade(score INT)
RETURNS TEXT AS $$
BEGIN
    RETURN CASE
        WHEN score >= 90 THEN 'Sehr gut (1)'
        WHEN score >= 80 THEN 'Gut (2)'
        WHEN score >= 70 THEN 'Befriedigend (3)'
        WHEN score >= 60 THEN 'Ausreichend (4)'
        ELSE 'Nicht bestanden (5)'
    END;
END;
$$ LANGUAGE plpgsql;

-- Testen
SELECT get_grade(95) as note;
SELECT get_grade(85) as note;
SELECT get_grade(72) as note;
SELECT get_grade(50) as note;
```
@PGlite.eval

    --{{4}}--
CASE ist hier viel lesbarer als verschachtelte IFs. Wann nutzen Sie was? IF für komplexe Bedingungen mit mehreren Anweisungen, CASE für einfache Wertauswahl.

---

## Fehlerbehandlung: RAISE

    --{{0}}--
Was, wenn etwas schiefgeht? Mit RAISE können Sie Fehler werfen – ähnlich wie "throw" in JavaScript.

### RAISE EXCEPTION

      {{0-1}}
<div>

**Syntax:**

```sql
RAISE EXCEPTION 'Fehlermeldung: %', variable;
```

**Platzhalter:**
- `%` wird durch die nächste Variable ersetzt
- Ähnlich wie `printf` in C oder String-Interpolation

</div>

### Demo 5: Division mit Fehlerbehandlung

    --{{1}}--
Ein Klassiker: Division durch Null verhindern.

      {{1}}
``` sql
CREATE FUNCTION divide(a INT, b INT)
RETURNS DECIMAL AS $$
BEGIN
    IF b = 0 THEN
        RAISE EXCEPTION 'Division durch Null ist nicht erlaubt! (Divisor: %)', b;
    END IF;
    RETURN a::DECIMAL / b;
END;
$$ LANGUAGE plpgsql;

-- Testen: Erfolg
SELECT divide(10, 2) as result;
SELECT divide(100, 4) as result;

-- Testen: Fehler
SELECT divide(10, 0) as result;  -- ❌ Wirft Exception
```
@PGlite.eval

    --{{2}}--
Probieren Sie die letzte Zeile aus – Sie sehen eine klare Fehlermeldung! Das ist besser als ein kryptischer Datenbankfehler.

---

## Praxisbeispiel: Preisberechnung

    --{{0}}--
Kombinieren wir alles Gelernte in einem realistischen Beispiel: Gesamtpreis mit Steuer berechnen.

### Demo 6: Preisberechnung mit MwSt.

      {{0}}
``` sql
CREATE FUNCTION calculate_total(price DECIMAL, tax_rate DECIMAL)
RETURNS DECIMAL AS $$
BEGIN
    IF price < 0 THEN
        RAISE EXCEPTION 'Preis kann nicht negativ sein: %', price;
    END IF;
    
    IF tax_rate < 0 OR tax_rate > 1 THEN
        RAISE EXCEPTION 'Steuersatz muss zwischen 0 und 1 liegen: %', tax_rate;
    END IF;
    
    RETURN price * (1 + tax_rate);
END;
$$ LANGUAGE plpgsql;

-- Testen mit verschiedenen Szenarien
SELECT calculate_total(100, 0.19) as brutto;    -- Deutschland: 19% MwSt
SELECT calculate_total(50, 0.07) as brutto;     -- Ermäßigt: 7%
SELECT calculate_total(200, 0) as brutto;       -- Steuerfrei

-- Fehler provozieren:
-- SELECT calculate_total(-10, 0.19) as brutto;  -- ❌ Negativer Preis
-- SELECT calculate_total(100, 1.5) as brutto;   -- ❌ Ungültiger Steuersatz
```
@PGlite.eval

    --{{1}}--
Perfekt! Jetzt können Sie solide Functions schreiben. Aber was, wenn Sie wollen, dass Code automatisch ausgeführt wird – ohne dass jemand die Funktion aufruft? Genau dafür gibt es Trigger!

---

## Teil 2: Trigger

    --{{0}}--
Trigger sind das Automatisierungs-Werkzeug der Datenbank. Sie "triggern" – werden ausgelöst – bei bestimmten Events: INSERT, UPDATE oder DELETE. Denken Sie an Event-Listener in JavaScript, aber auf Datenbankebene.

### Was sind Trigger?

      {{0-1}}
<div>

**Definition:**

Ein Trigger ist eine Funktion, die automatisch ausgeführt wird, wenn ein bestimmtes Event auf einer Tabelle passiert.

**Komponenten:**

1. **Trigger-Function:** Eine spezielle Function mit `RETURNS TRIGGER`
2. **Trigger:** Verbindet die Function mit einer Tabelle und einem Event

**Syntax:**

```sql
-- 1. Function erstellen
CREATE FUNCTION trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    -- Code hier
    RETURN NEW;  -- oder OLD oder NULL
END;
$$ LANGUAGE plpgsql;

-- 2. Trigger erstellen
CREATE TRIGGER trigger_name
BEFORE UPDATE ON table_name
FOR EACH ROW
EXECUTE FUNCTION trigger_function();
```

</div>

### Besonderheiten von Trigger-Functions

    --{{1}}--
Trigger-Functions sind anders als normale Functions:

      {{1-2}}
<div>

**Spezielle Variablen:**

| Variable | Typ | Beschreibung | Verfügbar bei |
|----------|-----|--------------|---------------|
| `NEW` | RECORD | Die neue Zeile | INSERT, UPDATE |
| `OLD` | RECORD | Die alte Zeile | UPDATE, DELETE |

**Beispiel:**

```sql
CREATE FUNCTION my_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Bei INSERT: nur NEW verfügbar
    -- Bei UPDATE: OLD und NEW verfügbar
    -- Bei DELETE: nur OLD verfügbar
    
    RAISE NOTICE 'Alte Zeile: %, Neue Zeile: %', OLD, NEW;
    
    RETURN NEW;  -- Gibt die (ggf. modifizierte) Zeile zurück
END;
$$ LANGUAGE plpgsql;
```

</div>

### RETURN-Werte bei BEFORE-Triggern

    --{{2}}--
Bei BEFORE-Triggern ist der RETURN-Wert wichtig:

      {{2-3}}
<div>

| RETURN | Bedeutung |
|--------|-----------|
| `RETURN NEW;` | Änderungen übernehmen (bei INSERT/UPDATE) |
| `RETURN OLD;` | Ursprüngliche Werte behalten (bei UPDATE) |
| `RETURN NULL;` | Operation abbrechen! (bei DELETE: Zeile wird NICHT gelöscht) |

**Bei AFTER-Triggern:** RETURN-Wert wird ignoriert, `RETURN NULL;` ist üblich.

</div>

### CREATE TRIGGER Syntax

    --{{3}}--
So erstellen Sie einen Trigger:

      {{3-4}}
<div>

```sql
CREATE TRIGGER trigger_name
{ BEFORE | AFTER } { INSERT | UPDATE | DELETE [ OR ... ] }
ON table_name
FOR EACH ROW
EXECUTE FUNCTION function_name();
```

**Optionen:**

- `BEFORE` – Trigger läuft VOR der Operation (kann Daten ändern oder Operation abbrechen)
- `AFTER` – Trigger läuft NACH der Operation (kann nicht mehr eingreifen)
- `FOR EACH ROW` – Trigger wird für jede betroffene Zeile ausgeführt
- Mehrere Events: `BEFORE INSERT OR UPDATE OR DELETE`

</div>

    --{{4}}--
Genug Theorie – schauen wir uns vier praktische Beispiele an, die Sie sofort nutzen können!

---

## Demo 7: Automatische Timestamps

    --{{0}}--
Das häufigste Use Case: Timestamp-Felder automatisch aktualisieren.

### Schritt 1: Tabelle vorbereiten

    --{{0}}--
Zuerst erstellen wir eine Produkte-Tabelle mit Timestamp-Feldern.

      {{0}}
``` sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Testdaten einfügen
INSERT INTO products (name, price) VALUES 
    ('Laptop', 999.99),
    ('Maus', 29.99);

-- Ausgangszustand
SELECT id, name, price, created_at, updated_at FROM products;
```
@PGlite.eval(timestamps-demo)

### Schritt 2: Trigger-Function & Trigger erstellen

    --{{1}}--
Jetzt die Magie: Eine Function, die updated_at automatisch setzt.

      {{1}}
``` sql
-- Function: Setzt updated_at auf NOW()
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Wird bei jedem UPDATE ausgeführt
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Bestätigung
SELECT 'Trigger erfolgreich erstellt!' as status;
```
@PGlite.eval(timestamps-demo)

### Schritt 3: Testen

    --{{2}}--
Jetzt ändern wir Daten und schauen, ob updated_at automatisch aktualisiert wird.

      {{2}}
``` sql
-- Kurze Pause simulieren (damit Zeitunterschied sichtbar ist)
SELECT pg_sleep(1);

-- Preis ändern
UPDATE products 
SET price = 899.99 
WHERE name = 'Laptop';

-- Ergebnis prüfen
SELECT 
    name, 
    price,
    created_at,
    updated_at,
    (updated_at > created_at) as timestamp_updated
FROM products;
```
@PGlite.eval(timestamps-demo)

    --{{3}}--
Perfekt! Das updated_at-Feld wurde automatisch aktualisiert – ohne dass wir es in der UPDATE-Query angeben mussten. Das funktioniert jetzt für jedes Update, egal aus welcher Anwendung!

---

## Demo 8: Audit-Logging

    --{{0}}--
Zweitens: Änderungen protokollieren für Compliance und Nachvollziehbarkeit.

### Schritt 1: Tabellen vorbereiten

    --{{0}}--
Wir brauchen eine Audit-Tabelle, um Änderungen zu protokollieren.

      {{0}}
``` sql
-- Produkte-Tabelle
CREATE TABLE products_audit_demo (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL(10, 2)
);

-- Audit-Tabelle
CREATE TABLE products_audit_log (
    audit_id SERIAL PRIMARY KEY,
    product_id INT,
    old_price DECIMAL(10, 2),
    new_price DECIMAL(10, 2),
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Testdaten
INSERT INTO products_audit_demo (name, price) VALUES ('Laptop', 999.99);

-- Ausgangszustand
SELECT * FROM products_audit_demo;
SELECT * FROM products_audit_log;  -- Noch leer
```
@PGlite.eval(audit-demo)

### Schritt 2: Audit-Trigger erstellen

    --{{1}}--
Function, die Preisänderungen protokolliert:

      {{1}}
``` sql
-- Function: Protokolliert Preisänderungen
CREATE OR REPLACE FUNCTION log_price_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Nur protokollieren, wenn sich der Preis tatsächlich geändert hat
    IF OLD.price IS DISTINCT FROM NEW.price THEN
        INSERT INTO products_audit_log (product_id, old_price, new_price)
        VALUES (NEW.id, OLD.price, NEW.price);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Wird NACH jedem UPDATE ausgeführt
CREATE TRIGGER audit_price_changes
AFTER UPDATE ON products_audit_demo
FOR EACH ROW
EXECUTE FUNCTION log_price_change();

SELECT 'Audit-Trigger erstellt!' as status;
```
@PGlite.eval(audit-demo)

### Schritt 3: Testen

    --{{2}}--
Jetzt ändern wir den Preis mehrmals und schauen ins Audit-Log.

      {{2}}
``` sql
-- Mehrere Preisänderungen
UPDATE products_audit_demo SET price = 899.99 WHERE name = 'Laptop';
UPDATE products_audit_demo SET price = 799.99 WHERE name = 'Laptop';
UPDATE products_audit_demo SET price = 849.99 WHERE name = 'Laptop';

-- Aktueller Zustand
SELECT * FROM products_audit_demo;

-- Audit-Log: Alle Änderungen protokolliert!
SELECT 
    audit_id,
    product_id,
    old_price,
    new_price,
    old_price - new_price as price_change,
    changed_at
FROM products_audit_log
ORDER BY changed_at;
```
@PGlite.eval(audit-demo)

    --{{3}}--
Exzellent! Jede Preisänderung wurde automatisch protokolliert. Das ist perfekt für Compliance-Anforderungen – die Anwendung kann das Logging nicht "vergessen".

---

## Demo 9: Validierung

    --{{0}}--
Drittens: Datenintegrität mit Triggern erzwingen – z.B. negative Preise verhindern.

### Schritt 1: Tabelle & Trigger erstellen

    --{{0}}--
Wir erstellen eine Tabelle und einen Trigger, der negative Preise verhindert.

      {{0}}
``` sql
-- Tabelle
CREATE TABLE products_validation (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL(10, 2)
);

-- Function: Prüft, ob Preis gültig ist
CREATE OR REPLACE FUNCTION prevent_negative_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price < 0 THEN
        RAISE EXCEPTION 'Preis % ist ungültig (negativ)!', NEW.price;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Läuft bei INSERT und UPDATE
CREATE TRIGGER check_price
BEFORE INSERT OR UPDATE ON products_validation
FOR EACH ROW
EXECUTE FUNCTION prevent_negative_price();

SELECT 'Validierungs-Trigger erstellt!' as status;
```
@PGlite.eval(validation-demo)

### Schritt 2: Erfolgreiche Einfügungen

    --{{1}}--
Zuerst testen wir mit gültigen Daten:

      {{1}}
``` sql
-- Gültige Inserts
INSERT INTO products_validation (name, price) VALUES ('Laptop', 999.99);
INSERT INTO products_validation (name, price) VALUES ('Maus', 29.99);
INSERT INTO products_validation (name, price) VALUES ('Gratis-Ebook', 0.00);

-- Alles funktioniert
SELECT * FROM products_validation;
```
@PGlite.eval(validation-demo)

### Schritt 3: Ungültige Daten provozieren

    --{{2}}--
Jetzt versuchen wir, einen negativen Preis einzufügen:

      {{2}}
``` sql
-- Dieser Versuch schlägt fehl!
INSERT INTO products_validation (name, price) VALUES ('Fehlerhaft', -10.00);

-- ❌ ERROR: Preis -10.00 ist ungültig (negativ)!
```
@PGlite.eval(validation-demo)

    --{{3}}--
Perfekt! Der Trigger hat die ungültige Operation verhindert. Die Anwendung kann diese Regel nicht umgehen – sie ist in der Datenbank verankert.

---

## Demo 10: Soft Delete mit Views & INSTEAD OF Trigger

    --{{0}}--
Viertens: Löschen, ohne wirklich zu löschen – für Wiederherstellung und Audit-Zwecke. Diesmal mit einem eleganten Twist: Die Anwendung arbeitet nur mit einer View und weiß gar nicht, dass Soft Delete passiert!

### Schritt 1: Basis-Tabelle mit Soft-Delete-Flag

    --{{0}}--
Wir erstellen die eigentliche Produkte-Tabelle mit einem deleted_at Feld:

      {{0}}
``` sql
-- Basis-Tabelle (kennt die Anwendung nicht!)
CREATE TABLE products_base (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP  -- NULL = aktiv, Timestamp = gelöscht
);

-- Testdaten
INSERT INTO products_base (name, price) VALUES 
    ('Laptop', 999.99),
    ('Maus', 29.99),
    ('Tastatur', 79.99);

-- Alle Daten (inkl. deleted_at)
SELECT * FROM products_base;
```
@PGlite.eval(softdelete-demo)

### Schritt 2: View für aktive Produkte

    --{{1}}--
Die Anwendung arbeitet nur mit dieser View – sie zeigt nur aktive Produkte:

      {{1}}
``` sql
-- View: Die "öffentliche" Schnittstelle zur Datenbank
CREATE VIEW products AS
SELECT id, name, price, created_at
FROM products_base
WHERE deleted_at IS NULL;  -- Filter: nur aktive Produkte

-- Anwendung sieht nur diese View
SELECT * FROM products;
```
@PGlite.eval(softdelete-demo)

    --{{2}}--
Beachten Sie: Die View zeigt das deleted_at Feld gar nicht – die Anwendung weiß nichts von Soft Delete!

### Schritt 3: INSTEAD OF Trigger auf der View

    --{{2}}--
Jetzt kommt die Magie: Ein Trigger auf der View, der DELETE-Operationen abfängt:

      {{2}}
``` sql
-- Function: Führt Soft Delete auf der Basis-Tabelle aus
CREATE OR REPLACE FUNCTION soft_delete_via_view()
RETURNS TRIGGER AS $$
BEGIN
    -- Setzt deleted_at auf der echten Tabelle
    UPDATE products_base 
    SET deleted_at = NOW() 
    WHERE id = OLD.id;
    
    -- RETURN OLD bei INSTEAD OF Triggern
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- INSTEAD OF Trigger: Ersetzt DELETE auf der View
CREATE TRIGGER soft_delete_products
INSTEAD OF DELETE ON products
FOR EACH ROW
EXECUTE FUNCTION soft_delete_via_view();

SELECT 'Soft-Delete-Trigger auf View erstellt!' as status;
```
@PGlite.eval(softdelete-demo)

    --{{3}}--
INSTEAD OF Trigger funktionieren nur auf Views und ersetzen die Operation komplett. Perfekt für unseren Use Case!

### Schritt 4: "Löschen" über die View

    --{{3}}--
Die Anwendung "löscht" ein Produkt – aber es wird nur markiert:

      {{3}}
``` sql
-- Anwendung löscht über die View (weiß nichts von Soft Delete!)
DELETE FROM products WHERE name = 'Maus';

-- View zeigt nur noch aktive Produkte
SELECT 'Aktive Produkte (View):' as info;
SELECT * FROM products;

-- Basis-Tabelle zeigt ALLE Produkte (inkl. deleted_at)
SELECT 'Alle Produkte (Basis-Tabelle):' as info;
SELECT 
    id,
    name,
    price,
    deleted_at,
    CASE 
        WHEN deleted_at IS NULL THEN '✅ Aktiv'
        ELSE '❌ Gelöscht'
    END as status
FROM products_base
ORDER BY id;
```
@PGlite.eval(softdelete-demo)

    --{{4}}--
Brilliant! Die Maus ist aus der View verschwunden – aber in der Basis-Tabelle noch vorhanden mit gesetztem deleted_at Timestamp. Die Anwendung merkt nichts von der Implementierung!

### Schritt 5: Wiederherstellung

    --{{4}}--
Gelöschte Produkte können einfach wiederhergestellt werden:

      {{4}}
``` sql
-- Admin-Funktion: Produkt wiederherstellen
UPDATE products_base 
SET deleted_at = NULL 
WHERE name = 'Maus';

-- View zeigt das Produkt wieder!
SELECT * FROM products;
```
@PGlite.eval(softdelete-demo)

    --{{5}}--
Perfekt! Durch die View-Abstraktion haben Sie eine saubere Trennung: Die Anwendung arbeitet mit der View, Admins können auf die Basis-Tabelle zugreifen.

### Warum ist das elegant?

    --{{5}}--
Schauen wir uns die Vorteile an:

      {{5}}
<div>

**Vorteile dieser Architektur:**

| Aspekt | Ohne View | Mit View + INSTEAD OF Trigger |
|--------|-----------|-------------------------------|
| Anwendungscode | Muss Soft Delete implementieren | Arbeitet normal mit DELETE |
| Komplexität | Verteilt über viele Stellen | Zentralisiert in der DB |
| Konsistenz | Entwickler können es vergessen | Automatisch garantiert |
| Wiederherstellung | Muss explizit implementiert werden | Einfaches UPDATE auf Basis-Tabelle |
| Migration | Anwendung muss angepasst werden | Transparent – keine Code-Änderung |
| Testen | Schwierig (überall prüfen) | Einfach (nur View testen) |

**Anwendungscode-Vergleich:**

```javascript
// Ohne View: Anwendung muss Soft Delete kennen
await db.query(
  'UPDATE products SET deleted_at = NOW() WHERE id = $1',
  [productId]
);

// Mit View: Anwendung nutzt normales DELETE
await db.query(
  'DELETE FROM products WHERE id = $1',  
  [productId]
);
// ✅ Trigger macht den Rest – transparent!
```

**Best Practice:** Diese Architektur nennt sich **Database Abstraction Layer**. Die View ist die öffentliche API, die Implementierung dahinter kann sich ändern, ohne die Anwendung anzufassen.

</div>

---

## Gefahren & Best Practices

    --{{0}}--
Trigger sind mächtig – aber mit großer Macht kommt große Verantwortung! Schauen wir uns potenzielle Probleme an.

### Gefahr 1: Trigger-Kaskaden

    --{{0}}--
Das größte Problem: Trigger, die andere Trigger auslösen – eine Kettenreaktion!

      {{0-1}}
<div>

**Szenario:**

```
Trigger A (on products) 
  → UPDATE inventory  
    → Trigger B (on inventory)  
      → INSERT audit_log  
        → Trigger C (on audit_log)  
          → UPDATE statistics  
            → Trigger D (on statistics)  
              → ... 💥
```

**Problem:**

- ❌ Schwer zu debuggen
- ❌ Performance-Einbruch
- ❌ Risiko von Endlosschleifen
- ❌ Unvorhersehbares Verhalten

**Lösung:**

```sql
-- NIEMALS in einem Trigger weitere Trigger auslösen!
-- Stattdessen: Komplexe Logik in eine Funktion auslagern
CREATE FUNCTION process_order()
RETURNS VOID AS $$
BEGIN
    -- Alle Operationen explizit hier
    UPDATE inventory ...;
    INSERT INTO audit_log ...;
    UPDATE statistics ...;
END;
$$ LANGUAGE plpgsql;
```

</div>

### Gefahr 2: Performance-Impact

    --{{1}}--
Trigger laufen bei JEDER Operation – auch bei BULK Inserts!

      {{1-2}}
<div>

**Problem:**

```sql
-- BULK INSERT von 100.000 Zeilen
INSERT INTO products SELECT * FROM imported_data;

-- Wenn ein Trigger existiert:
-- → 100.000× Trigger-Ausführung!
-- → Kann Minuten statt Sekunden dauern
```

**Lösung:**

```sql
-- Trigger temporär deaktivieren (PostgreSQL)
ALTER TABLE products DISABLE TRIGGER set_updated_at;

-- BULK Operation
INSERT INTO products SELECT * FROM imported_data;

-- Trigger wieder aktivieren
ALTER TABLE products ENABLE TRIGGER set_updated_at;
```

**Best Practice:** Überlegen Sie, ob ein Batch-Job statt Trigger sinnvoller ist!

</div>

### Gefahr 3: Debugging-Schwierigkeiten

    --{{2}}--
Trigger sind unsichtbar für die Anwendung – Fehler sind schwer zu finden.

      {{2-3}}
<div>

**Problem:**

```javascript
// Anwendungscode
await db.query('UPDATE products SET price = 99.99 WHERE id = 1');

// ❓ Plötzlich ist die Performance schlecht
// ❓ Plötzlich gibt es unerwartete Änderungen in anderen Tabellen
// ❓ Die Anwendung weiß nicht, dass Trigger existieren!
```

**Lösung:**

1. **Dokumentation:** Kommentiere alle Trigger im Schema-Script
2. **Naming Convention:** `trigger_<table>_<event>_<action>`
3. **Logging:** RAISE NOTICE in Triggern für Debugging
4. **Monitoring:** Query-Performance überwachen

```sql
CREATE TRIGGER trigger_products_after_update_audit
AFTER UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION log_price_change();

-- Name verrät: Tabelle = products, Event = update, Aktion = audit
```

</div>

### Best Practice 1: Trigger nur wenn nötig

    --{{3}}--
Viele Anforderungen können einfacher gelöst werden!

      {{3-4}}
<div>

| Anforderung | ❌ Trigger | ✅ Bessere Lösung |
|-------------|-----------|------------------|
| Validierung | `CREATE TRIGGER check_price...` | `CHECK (price >= 0)` |
| Default-Werte | `CREATE TRIGGER set_default...` | `DEFAULT NOW()` |
| Ref. Integrität | `CREATE TRIGGER check_fk...` | `FOREIGN KEY` |
| Timestamps | ✅ Trigger ist OK | Oder: `DEFAULT NOW()` + Trigger für UPDATE |
| Audit-Logging | ✅ Trigger ist ideal | Keine Alternative |
| Soft Delete | ✅ Trigger ist gut | Oder: App-seitig |

**Faustregel:** Nutze deklarative Constraints wo möglich, Trigger nur wenn nötig!

</div>

### Best Practice 2: BEFORE vs. AFTER

    --{{4}}--
Wann welchen Trigger-Typ nutzen?

      {{4-5}}
<div>

| Use Case | BEFORE | AFTER |
|----------|--------|-------|
| Daten ändern (z.B. Timestamps) | ✅ Ja | ❌ Zu spät |
| Validierung (z.B. negative Preise) | ✅ Ja | ❌ Zu spät |
| Operation abbrechen | ✅ RETURN NULL | ❌ Nicht möglich |
| Audit-Logging | ⚠️ Möglich | ✅ Besser (Änderung ist garantiert committed) |
| Andere Tabellen ändern | ⚠️ Möglich | ✅ Besser (Hauptoperation ist fertig) |

**Faustregel:** 
- **BEFORE** für Änderungen an der aktuellen Zeile
- **AFTER** für Änderungen an anderen Tabellen oder Logging

</div>

### Best Practice 3: Testen, testen, testen!

    --{{5}}--
Trigger sind Code – und Code muss getestet werden!

      {{5}}
<div>

**Test-Strategie:**

```sql
-- Test 1: Erfolgreicher Fall
BEGIN;
INSERT INTO products (name, price) VALUES ('Test', 99.99);
SELECT * FROM products WHERE name = 'Test';
-- Erwartung: updated_at ist gesetzt
ROLLBACK;

-- Test 2: Fehlerfall
BEGIN;
INSERT INTO products (name, price) VALUES ('Test', -10);
-- Erwartung: Fehler wird geworfen
ROLLBACK;

-- Test 3: Edge Cases
BEGIN;
UPDATE products SET price = NULL WHERE id = 1;
-- Erwartung: ???
ROLLBACK;
```

**Best Practice:** 
- Schreibe Test-Scripts für jeden Trigger
- Teste Edge Cases (NULL, 0, negative Werte)
- Teste Performance mit vielen Zeilen

</div>

---

## Zusammenfassung

    --{{0}}--
Was haben wir heute gelernt? Functions und Trigger sind mächtige Werkzeuge für server-seitige Logik in der Datenbank.

      {{0}}
<div>

### Kernpunkte: Functions

1. **Stored Functions** = Wiederverwendbare Logik in der Datenbank
2. **Syntax:** `CREATE FUNCTION name(params) RETURNS type AS $$ ... $$ LANGUAGE plpgsql;`
3. **Kontrollstrukturen:** `IF...THEN...ELSE` und `CASE`
4. **Fehlerbehandlung:** `RAISE EXCEPTION`
5. **Use Cases:** Berechnungen, Validierung, String-Verarbeitung

### Kernpunkte: Trigger

6. **Trigger** = Automatische Reaktion auf Datenbankänderungen
7. **Trigger-Functions:** `RETURNS TRIGGER`, nutzen `OLD` und `NEW`
8. **Syntax:** `CREATE TRIGGER name BEFORE/AFTER event ON table FOR EACH ROW EXECUTE FUNCTION func();`
9. **Use Cases:** Timestamps, Audit-Logging, Validierung, Soft Delete
10. **Gefahren:** Kaskaden, Performance, Debugging-Schwierigkeiten

### Wann was nutzen?

| Szenario | Lösung |
|----------|--------|
| Einfache Validierung | ✅ CHECK Constraint |
| Default-Werte | ✅ DEFAULT Clause |
| Automatische Timestamps | ✅ Trigger (UPDATE) + DEFAULT (INSERT) |
| Audit-Logging | ✅ Trigger |
| Soft Delete | ✅ Trigger oder App-Logik |
| Komplexe Berechnungen | ✅ Function |
| Referentielle Integrität | ✅ FOREIGN KEY |

</div>

    --{{1}}--
Sie haben heute 10 interaktive Demos durchgearbeitet – von einfachen Functions bis zu komplexen Triggern. Experimentieren Sie weiter! Ändern Sie die Beispiele, brechen Sie sie, fixen Sie sie wieder. So lernt man am besten!

---

## Referenzen & Quellen

      {{0}}
<div>

### Offizielle Dokumentation

- [PostgreSQL: PL/pgSQL Functions](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL: Trigger Functions](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [PostgreSQL: CREATE TRIGGER](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- [PGlite: Browser PostgreSQL](https://github.com/electric-sql/pglite)

### Bücher & Tutorials

- "PostgreSQL: Up and Running" – Regina Obe & Leo Hsu (Kapitel zu Functions & Trigger)
- "Mastering PostgreSQL" – Hans-Jürgen Schönig
- [PostGIS Tutorial: Custom Functions](https://postgis.net/workshops/postgis-intro/functions.html)

### Best Practices

- [Use the Index, Luke: Triggers & Performance](https://use-the-index-luke.com/)
- [PostgreSQL Wiki: Trigger Best Practices](https://wiki.postgresql.org/wiki/Triggers)

### Tools

- [pgAdmin](https://www.pgadmin.org/) – Trigger-Debugging
- [DBeaver](https://dbeaver.io/) – Cross-Platform Database Tool
- [PGlite](https://pglite.dev/) – PostgreSQL im Browser

</div>

---

**Nächste Session:** Performance Optimization – Indexes, Query Plans & Best Practices
