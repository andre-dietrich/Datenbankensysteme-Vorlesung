<!--
author:   André Dietrich
email:    andre.dietrich@informatik.tu-freiberg.de
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  Transaktionen & ACID – Szenariobasierte Einführung in Transaktionssteuerung, ACID-Eigenschaften und Isolation Levels. Von Geldüberweisungen bis Ticketbuchungen: Warum Transaktionen unverzichtbar sind für konsistente Datenbanksysteme. Mit Live-Demos zu BEGIN/COMMIT/ROLLBACK und praktischen Beispielen zu Dirty Reads, Lost Updates und Deadlocks.

logo:     

edit:    true


import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md

-->

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md

# Session 14 – Transaktionen & ACID

> **Session-Typ:** Vorlesung  
> **Dauer:** 90 Minuten  
> **Lernziele:** ACID verstehen, Transaktionssteuerung anwenden, Isolation Levels vergleichen

    --{{0}}--
Willkommen zu Session 14! Heute geht es um eines der fundamentalsten Konzepte relationaler Datenbanksysteme: Transaktionen und ACID. Wir haben bisher viel über SQL-Abfragen, Modellierung und komplexe Queries gelernt – aber was passiert, wenn mehrere Nutzer gleichzeitig auf dieselben Daten zugreifen? Wie garantieren wir Konsistenz bei Systemausfällen? Diese Fragen beantworten Transaktionen.

---

## Motivation: Warum Transaktionen?

Szenario: Geldüberweisung zwischen Konten
-----------------------------------------

    --{{0}}--
Stellen Sie sich vor, Sie überweisen 100 Euro von Konto A nach Konto B. Das klingt simpel, aber technisch sind das zwei separate Operationen: Erst wird Konto A belastet, dann Konto B gutgeschrieben. Was passiert, wenn zwischen diesen beiden Schritten der Server abstürzt? Oder wenn eine andere Transaktion genau in diesem Moment auf Konto A zugreift?

      {{0-1}}
<div>

### Ohne Transaktionen: Probleme

```sql
-- Schritt 1: 100 Euro von Konto A abziehen
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

-- ❌ Server-Crash hier!

-- Schritt 2: 100 Euro auf Konto B gutschreiben (wird nie ausgeführt)
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
```

**Ergebnis:** 100 Euro sind verschwunden! Konto A ist belastet, aber Konto B wurde nie gutgeschrieben.

</div>

    --{{1}}--
Genau solche Inkonsistenzen verhindern Transaktionen. Eine Transaktion ist eine logische Arbeitseinheit, die garantiert, dass entweder alle Operationen erfolgreich durchgeführt werden – oder gar keine. Das ist das "Alles-oder-Nichts"-Prinzip.

      {{1-2}}
<div>

### Mit Transaktionen: Atomar & Sicher

```sql
BEGIN TRANSACTION;

-- Schritt 1: 100 Euro von Konto A abziehen
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

-- Schritt 2: 100 Euro auf Konto B gutschreiben
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';

COMMIT; -- Erst jetzt werden beide Änderungen dauerhaft gespeichert
```

**Garantie:** Wenn `COMMIT` erfolgreich ist, sind beide Änderungen persistent. Bei einem Fehler vor `COMMIT` wird automatisch `ROLLBACK` ausgeführt – keine Änderung bleibt bestehen.

</div>

    --{{2}}--
Eine Transaktion ist also ein Paket mit Garantiesiegel: Entweder kommt alles an – oder gar nichts. Damit sind wir schon beim ersten Buchstaben von ACID.

---

## ACID-Eigenschaften

    --{{0}}--
ACID ist ein Akronym für vier fundamentale Eigenschaften, die jede Datenbanktransaktion erfüllen sollte: Atomicity, Consistency, Isolation und Durability. Diese Eigenschaften wurden in den 1980ern von Jim Gray definiert und sind bis heute der Goldstandard für transaktionale Systeme.

``` ascii
 .-------------+-------------+-------------+-------------.
 |     ⚛️      |     ✅      |     👁️‍🗨️      |     🛡️      |
 |             |             |             |             |
 |  Atomicity  | Consistency |  Isolation  | Durability  |
 '-------------+-------------+-------------+-------------'

 <-------------------- ACID Database --------------------> 
```
### A – Atomicity (Atomarität)

    --{{0}}--
Atomarität bedeutet: Eine Transaktion ist eine unteilbare Einheit. Entweder werden alle Operationen ausgeführt – oder keine. Es gibt keine Zwischenzustände, die nach außen sichtbar sind.

      {{0-1}}
<div>

**Metapher:** Wie ein Atom (griech. "átomos" = unteilbar) ist eine Transaktion eine Einheit, die nicht weiter zerlegbar ist.

**Beispiel:**

| Aktion            | Ohne Atomarität            | Mit Atomarität              |
| ----------------- | -------------------------- | --------------------------- |
| UPDATE accounts A | ✅ Erfolg                  | ✅ Erfolg                   |
| ❌ Server-Crash   | 💥 Inkonsistenter Zustand  | ✅ Automatisches ROLLBACK   |
| UPDATE accounts B | ❌ Wird nie ausgeführt     | ❌ Beide Updates rückgängig |

</div>

### C – Consistency (Konsistenz)

    --{{1}}--
Konsistenz bedeutet: Eine Transaktion überführt die Datenbank von einem gültigen Zustand in einen anderen gültigen Zustand. Alle Constraints, Trigger und Integritätsbedingungen werden eingehalten – vor und nach der Transaktion.

      {{1-2}}
<div>

**Beispiel:**

```sql
-- Constraint: Balance darf nie negativ werden
ALTER TABLE accounts ADD CONSTRAINT balance_positive CHECK (balance >= 0);

BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE id = 'A';
-- ❌ Fehler: Constraint verletzt → automatisches ROLLBACK
COMMIT; -- wird nie erreicht
```

**Garantie:** Die Datenbank bleibt in einem konsistenten Zustand – Constraints werden *immer* durchgesetzt.

</div>

### I – Isolation

    --{{2}}--
Isolation bedeutet: Parallel laufende Transaktionen beeinflussen sich nicht gegenseitig. Jede Transaktion hat die Illusion, als wäre sie allein auf der Datenbank. Wie stark diese Isolation ist, können wir über Isolation Levels steuern – dazu gleich mehr.

      {{2-3}}
<div>

**Beispiel: Ticketbuchung**

| Zeitpunkt | Nutzer A                                              | Nutzer B                                              |
| --------- | ----------------------------------------------------- | ----------------------------------------------------- |
| T1        | `SELECT * FROM tickets`<br>`WHERE seat = '12A'`              |                                                       |
| T2        |                                                       | `SELECT * FROM tickets`<br>`WHERE seat = '12A'`              |
| T3        | `UPDATE tickets SET reserved = true`<br>`WHERE seat = '12A'` |                                                       |
| T4        |                                                       | `UPDATE tickets SET reserved = true `<br>`WHERE seat = '12A'` |

**Ohne Isolation:** Beide sehen Sitz 12A als frei → Doppelbuchung!\
**Mit Isolation:** Nutzer B muss warten, bis Nutzer A seine Transaktion abgeschlossen hat.

</div>

### D – Durability (Dauerhaftigkeit)

    --{{3}}--
Dauerhaftigkeit bedeutet: Sobald eine Transaktion mit COMMIT bestätigt wurde, sind die Änderungen dauerhaft gespeichert – selbst wenn direkt danach ein Stromausfall oder Server-Crash passiert.

      {{3}}
<div>

**Technische Umsetzung:**

- **Write-Ahead Log (WAL):** Änderungen werden zuerst in ein Log geschrieben (auf Festplatte), bevor die Datenbank-Seiten aktualisiert werden.
- **Crash Recovery:** Nach einem Neustart liest die Datenbank das WAL und stellt den Zustand wieder her.

**Garantie:** Nach `COMMIT` geht keine Änderung verloren – auch bei Hardware-Ausfällen.

</div>

    --{{4}}--
Diese vier Eigenschaften zusammen machen Transaktionen zum Rückgrat relationaler Datenbanksysteme. Aber wie steuern wir Transaktionen konkret in SQL?

---

## Transaktionssteuerung in SQL

Basic Commands
--------------

    --{{0}}--
In SQL steuern wir Transaktionen mit vier grundlegenden Befehlen: BEGIN zum Starten, COMMIT zum Bestätigen, ROLLBACK zum Rückgängigmachen und SAVEPOINT für partielle Rollbacks.

      {{0-1}}
<div>

### `BEGIN` / `START TRANSACTION`

Startet eine neue Transaktion. Ab jetzt werden alle Änderungen zunächst nur temporär gespeichert.

```sql
BEGIN TRANSACTION;
-- oder: START TRANSACTION;
```

</div>

      {{1-2}}
<div>

### `COMMIT`

Bestätigt alle Änderungen seit BEGIN. Ab jetzt sind sie dauerhaft und für andere sichtbar.

```sql
COMMIT;
```

</div>

      {{2-3}}
<div>

### `ROLLBACK`

Macht alle Änderungen seit BEGIN rückgängig. Die Datenbank kehrt zum Zustand vor BEGIN zurück.

```sql
ROLLBACK;
```

</div>

      {{3-4}}
<div>

### `SAVEPOINT`

Setzt einen Zwischenpunkt innerhalb einer Transaktion. Erlaubt partielle Rollbacks.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

SAVEPOINT transfer_step1;

UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
-- Fehler! Konto B existiert nicht

ROLLBACK TO transfer_step1; -- Nur Schritt 2 rückgängig, Schritt 1 bleibt
COMMIT;
```

</div>

### Live-Demo: Geldüberweisung

    --{{4}}--
Schauen wir uns das Ganze in Aktion an. Ich starte mit einer einfachen Konten-Tabelle und zeige, was mit und ohne Transaktion passiert.

      {{4}}
``` sql
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,
    owner TEXT,
    balance INTEGER CHECK (balance >= 0)
);

INSERT INTO accounts VALUES 
    ('A', 'Alice', 500),
    ('B', 'Bob', 300);

SELECT * FROM accounts;
```
@PGlite.eval(transactions-demo)

    --{{5}}--
Jetzt führen wir eine Überweisung ohne Transaktion durch – und simulieren einen Fehler nach dem ersten UPDATE.

      {{5}}
``` sql
-- Ohne Transaktion: Gefährlich!
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
-- ❌ Fehler: System-Crash simuliert
-- UPDATE accounts SET balance = balance + 100 WHERE id = 'B';

SELECT * FROM accounts;
-- Ergebnis: A hat 400 Euro, B hat 300 Euro → 100 Euro verschwunden!
```
@PGlite.eval(transactions-demo)

    --{{6}}--
Und jetzt dasselbe mit Transaktion. Wenn ein Fehler auftritt, wird automatisch ein ROLLBACK durchgeführt.

      {{6}}
``` sql
-- Reset
UPDATE accounts SET balance = 500 WHERE id = 'A';

BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

-- Fehler simulieren (ungültige Constraint-Verletzung)
UPDATE accounts SET balance = balance + 100 WHERE id = 'Z'; -- Konto existiert nicht

ROLLBACK; -- Manuell rückgängig gemacht

SELECT * FROM accounts;
-- Ergebnis: A hat 500 Euro, B hat 300 Euro → Alles wie vorher!
```
@PGlite.eval(transactions-demo)

    --{{7}}--
Perfekt! Mit Transaktionen haben wir Atomarität garantiert. Aber was passiert, wenn mehrere Transaktionen parallel laufen? Hier kommen Isolation Levels ins Spiel.

---

## Isolation Levels

```` ascii
+------+-------------------------------------------+-------------------------------------------+
| Zeit |            Transaction A                  |            Transaction B                  |
+------+-------------------------------------------+-------------------------------------------+
|      |                                           |                                           |
|  T1  |  "``` sql                              "  |  "``` sql                              "  |
|      |  "SELECT balance FROM accounts         "  |  "SELECT balance FROM accounts         "  |
|      |  "WHERE id = 'A'                       "  |  "WHERE id = 'A'                       "  |
|      |  "```                                  "  |  "```                                  "  |
|      |                                           |                                           |
|      |   Ergebnis -> 100                         |                                           |
+------+-------------------------------------------+-------------------------------------------+

````

Probleme bei parallelen Transaktionen
--------------------------------------

    --{{0}}--
Isolation ist die komplizierteste der vier ACID-Eigenschaften. Warum? Weil perfekte Isolation extrem teuer ist – sie würde bedeuten, dass immer nur eine Transaktion gleichzeitig laufen darf. Deshalb gibt es verschiedene Isolation Levels, die einen Trade-off zwischen Konsistenz und Performance erlauben.

      {{0-1}}
<div>

### Welche Probleme können auftreten?

Wenn Transaktionen parallel laufen, gibt es vier klassische Anomalien:

#### 1. Dirty Read (Schmutziges Lesen)

Transaktion A liest Daten, die von Transaktion B geändert, aber noch nicht committed wurden.

| Zeit | Transaktion A                                                            | Transaktion B                                            |
| ---- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| T1   |                                                                          | `UPDATE accounts SET balance = 1000`<br>`WHERE id = 'A'` |
| T2   | `SELECT balance FROM accounts`<br>`WHERE id = 'A'` <br> → Ergebnis: 1000 |                                                          |
| T3   |                                                                          | `ROLLBACK;`                                              |
| T4   | -- A hat 1000 gelesen, aber das war nie committed!                       |                                                          |

**Problem:** A hat einen Wert gelesen, der nie existiert hat.

</div>

      {{1-2}}
<div>

#### 2. Non-Repeatable Read (Nicht-wiederholbares Lesen)

Transaktion A liest denselben Datensatz zweimal und bekommt unterschiedliche Werte.

| Zeit | Transaktion A                                                            | Transaktion B                                                          |
| ---- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| T1   | `SELECT balance FROM accounts`<br>`WHERE id = 'A'` <br> → Ergebnis: 500  |                                                                        |
| T2   |                                                                          | `UPDATE accounts SET balance = 1000`<br>`WHERE id = 'A';`<br>`COMMIT;` |
| T3   | `SELECT balance FROM accounts`<br>`WHERE id = 'A'` <br> → Ergebnis: 1000 |                                                                        |

**Problem:** A liest zweimal – und bekommt unterschiedliche Ergebnisse innerhalb derselben Transaktion.

</div>

      {{2-3}}
<div>

#### 3. Phantom Read (Phantom-Lesen)

Transaktion A führt dieselbe Abfrage zweimal aus und findet beim zweiten Mal zusätzliche Zeilen.

| Zeit | Transaktion A                                                                  | Transaktion B                                                  |
| ---- | ------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| T1   | `SELECT * FROM tickets`<br>`WHERE reserved = false` <br> → Ergebnis: 5 Tickets |                                                                |
| T2   |                                                                                | `INSERT INTO tickets`<br>`VALUES ('12F', false);`<br>`COMMIT;` |
| T3   | `SELECT * FROM tickets`<br>`WHERE reserved = false` <br> → Ergebnis: 6 Tickets |                                                                |

**Problem:** Plötzlich sind neue Zeilen aufgetaucht – wie ein Phantom.

</div>

      {{3-4}}
<div>

#### 4. Lost Update (Verlorenes Update)

Zwei Transaktionen lesen denselben Wert, ändern ihn parallel – und eine Änderung geht verloren.

| Zeit | Transaktion A                                                          | Transaktion B                                                          |
| ---- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| T1   | `SELECT balance FROM accounts`<br>`WHERE id = 'A'`<br> → Ergebnis: 500 | `SELECT balance FROM accounts`<br>`WHERE id = 'A'`<br> → Ergebnis: 500 |
| T2   | balance = 500 - 100 = 400                                              | balance = 500 + 200 = 700                                              |
| T3   | `UPDATE accounts SET balance = 400`<br>`WHERE id = 'A';`<br>`COMMIT;`  |                                                                        |
| T4   |                                                                        | `UPDATE accounts SET balance = 700`<br>`WHERE id = 'A';`<br>`COMMIT;`  |

**Problem:** A's Update (400) wurde von B's Update (700) überschrieben. Die -100 sind verloren!

</div>

### Die vier Isolation Levels

    --{{4}}--
Um diese Probleme zu adressieren, definiert der SQL-Standard vier Isolation Levels – von schwach (schnell, aber unsicher) bis stark (sicher, aber langsam).

      {{4}}
<div>

| Isolation Level    | Dirty Read    | Non-Repeatable Read | Phantom Read  | Lost Update   | Performance         |
| ------------------ | ------------- | ------------------- | ------------- | ------------- | ------------------- |
| `READ UNCOMMITTED` | ⚠️ Möglich    | ⚠️ Möglich          | ⚠️ Möglich    | ⚠️ Möglich    | ⚡⚡⚡ Sehr schnell    |
| `READ COMMITTED`   | ✅ Verhindert | ✅ Verhindert       | ⚠️ Möglich    | ⚠️ Möglich    | ⚡⚡ Schnell          |
| `REPEATABLE READ`  | ✅ Verhindert | ✅ Verhindert       | ⚠️ Möglich    | ✅ Verhindert | ⚡ Langsamer         |
| `SERIALIZABLE`     | ✅ Verhindert | ✅ Verhindert       | ✅ Verhindert | ✅ Verhindert | 🐌 Am langsamsten   |

**Standard in PostgreSQL:** `READ COMMITTED`\
**Standard in MySQL:** `REPEATABLE READ`

</div>

    --{{5}}--
Wie setzen wir das in SQL? Mit dem SET TRANSACTION Befehl.

      {{5}}
``` sql
-- Isolation Level für die nächste Transaktion setzen
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN TRANSACTION;
-- Alle Operationen hier laufen mit SERIALIZABLE Isolation
COMMIT;
```

    --{{6}}--
In der Praxis reicht `READ COMMITTED` für die meisten Anwendungen. Nur bei kritischen Operationen wie Ticketbuchungen oder Finanztransaktionen brauchen wir stärkere Isolation.

---

## Praktische Beispiele

Szenario 1: Ticketbuchung
--------------------------

    --{{0}}--
Schauen wir uns ein klassisches Concurrency-Problem an: Zwei Nutzer wollen gleichzeitig denselben Sitzplatz buchen.

      {{0}}
``` sql
CREATE TABLE tickets (
    seat TEXT PRIMARY KEY,
    reserved BOOLEAN DEFAULT false
);

INSERT INTO tickets VALUES ('12A', false), ('12B', false), ('12C', false);

-- Transaktion 1 (Nutzer Alice)
BEGIN TRANSACTION;
SELECT * FROM tickets WHERE seat = '12A' AND reserved = false;
-- Ergebnis: Sitz ist frei

-- 💥 Gleichzeitig startet Transaktion 2 (Nutzer Bob)
-- BEGIN TRANSACTION;
-- SELECT * FROM tickets WHERE seat = '12A' AND reserved = false;
-- Ergebnis: Sitz ist frei (falls READ COMMITTED)

UPDATE tickets SET reserved = true WHERE seat = '12A';
COMMIT;

-- Transaktion 2 würde jetzt ebenfalls versuchen:
-- UPDATE tickets SET reserved = true WHERE seat = '12A';
-- ❌ Mit SERIALIZABLE: Fehler oder Warten
-- ⚠️ Mit READ COMMITTED: Überschreibt still (Doppelbuchung!)
```
@PGlite.eval(transactions-demo)

    --{{1}}--
Lösung: Verwende SERIALIZABLE oder SELECT FOR UPDATE, um den Sitz zu locken.

      {{1}}
``` sql
-- Bessere Variante: SELECT FOR UPDATE
BEGIN TRANSACTION;
SELECT * FROM tickets WHERE seat = '12A' AND reserved = false FOR UPDATE;
-- Sperrt die Zeile → andere Transaktionen müssen warten

UPDATE tickets SET reserved = true WHERE seat = '12A';
COMMIT;
```
@PGlite.eval(transactions-demo)

    {{2}}
Szenario 2: Inventarverwaltung
-------------------------------

    --{{2}}--
Ein weiteres Beispiel: Ein Online-Shop aktualisiert den Lagerbestand, während parallel eine Bestellung aufgegeben wird.

      {{2}}
``` sql
CREATE TABLE inventory (
    product_id TEXT PRIMARY KEY,
    stock INTEGER CHECK (stock >= 0)
);

INSERT INTO inventory VALUES ('laptop_123', 5);

-- Transaktion 1: Kunde kauft 2 Laptops
BEGIN TRANSACTION;
UPDATE inventory SET stock = stock - 2 WHERE product_id = 'laptop_123';
COMMIT;

-- Transaktion 2: Lieferung kommt (3 neue Laptops)
BEGIN TRANSACTION;
UPDATE inventory SET stock = stock + 3 WHERE product_id = 'laptop_123';
COMMIT;

SELECT * FROM inventory;
-- Ergebnis: stock = 6 (5 - 2 + 3)
```
@PGlite.eval(transactions-demo)

    --{{3}}--
Hier ist READ COMMITTED ausreichend, da beide Transaktionen unabhängig sind – keine Konflikte.

---

## Deadlocks

    --{{0}}--
Ein Deadlock entsteht, wenn zwei Transaktionen gegenseitig aufeinander warten. Klassisches Beispiel: Transaktion A sperrt Zeile 1 und will Zeile 2, während Transaktion B Zeile 2 sperrt und Zeile 1 will.

      {{0-1}}
<div>

### Was ist ein Deadlock?

| Zeit | Transaktion A | Transaktion B |
|------|---------------|---------------|
| T1 | `UPDATE accounts`<br>`SET balance = balance - 100`<br>`WHERE id = 'A'` <br> → Sperrt Zeile A | `UPDATE accounts`<br>`SET balance = balance - 50`<br>`WHERE id = 'B'` <br> → Sperrt Zeile B |
| T2 | `UPDATE accounts`<br>`SET balance = balance + 100`<br>`WHERE id = 'B'` <br> ⏳ Wartet auf Lock von B | `UPDATE accounts`<br>`SET balance = balance + 50`<br>`WHERE id = 'A'` <br> ⏳ Wartet auf Lock von A |
| T3 | 💀 Deadlock! | 💀 Deadlock! |

**Beide warten ewig aufeinander.**

</div>

    --{{1}}--
Die Datenbank erkennt Deadlocks automatisch (über einen Deadlock Detector) und bricht eine der Transaktionen ab.

      {{1-2}}
<div>

### Deadlock-Erkennung

```
ERROR:  deadlock detected
DETAIL:  Process 1234 waits for ShareLock on transaction 5678;
         blocked by process 5678.
HINT:  See server log for query details.
```

Eine Transaktion wird automatisch mit ROLLBACK abgebrochen, die andere kann fortfahren.

</div>

    --{{2}}--
Wie vermeiden wir Deadlocks? Konsistente Lock-Reihenfolge!

      {{2}}
<div>

### Deadlock-Vermeidung

**Falsch (kann Deadlock verursachen):**

```sql
-- Transaktion A
UPDATE accounts SET ... WHERE id = 'A';
UPDATE accounts SET ... WHERE id = 'B';

-- Transaktion B
UPDATE accounts SET ... WHERE id = 'B';
UPDATE accounts SET ... WHERE id = 'A';
```

**Richtig (immer alphabetische Reihenfolge):**

```sql
-- Transaktion A
UPDATE accounts SET ... WHERE id = 'A';
UPDATE accounts SET ... WHERE id = 'B';

-- Transaktion B
UPDATE accounts SET ... WHERE id = 'A'; -- Wartet auf A
UPDATE accounts SET ... WHERE id = 'B';
```

**Regel:** Immer Ressourcen in derselben Reihenfolge sperren.

</div>

---

## Best Practices

    --{{0}}--
Zum Abschluss noch ein paar praktische Tipps für den Umgang mit Transaktionen.

      {{0}}
<div>

### 1. Transaktionen kurz halten

**Warum?** Lange Transaktionen sperren Ressourcen → andere müssen warten → Performance leidet.

**Falsch:**

```sql
BEGIN;
SELECT * FROM orders WHERE status = 'pending'; -- 10.000 Zeilen
-- 💤 Jetzt 5 Minuten warten, während Nutzer Eingaben macht...
UPDATE orders SET status = 'processed' WHERE id = 123;
COMMIT;
```

**Richtig:**

```sql
-- Lesen außerhalb der Transaktion
SELECT * FROM orders WHERE status = 'pending';

-- Transaktion nur für Updates
BEGIN;
UPDATE orders SET status = 'processed' WHERE id = 123;
COMMIT;
```

</div>

      {{1}}
<div>

### 2. Explizites COMMIT/ROLLBACK

**Warum?** Autocommit ist praktisch für Ad-hoc-Queries, aber gefährlich in Produktionscode.

```sql
-- Explizit ist besser als implizit
BEGIN TRANSACTION;
-- Operationen
COMMIT;
```

</div>

      {{2}}
<div>

### 3. Passenden Isolation Level wählen

**Faustregel:**

| Anwendungsfall            | Empfohlener Level                 |
| ------------------------- | --------------------------------- |
| Analytics (Read-only)     | `READ COMMITTED`                  |
| Standard CRUD             | `READ COMMITTED`                  |
| Ticketbuchung, Sitzplätze | `SERIALIZABLE`                    |
| Finanztransaktionen       | `SERIALIZABLE`                    |
| High-throughput Logging   | `READ UNCOMMITTED` (sehr selten!) |

</div>

      {{3}}
<div>

### 4. Fehlerbehandlung mit ROLLBACK

``` js
// Create a table with sample data
await db.exec(`
  CREATE TABLE accounts (
      id TEXT,
      name TEXT,
      balance INTEGER CHECK (balance >= 0)
  );
  
  INSERT INTO accounts VALUES
      ('A', 'Alice', 1500),
      ('B', 'Bob', 2300);
`);

try {
    await db.exec("BEGIN TRANSACTION;");
    await db.exec("UPDATE accounts SET balance = balance - 100 WHERE id = 'A';");
    // Simuliere einen Fehler
    //throw new Error("Simulierter Fehler während der Transaktion");
    await db.exec("UPDATE accounts SET balance = balance - 10000 WHERE id = 'B';");
    await db.exec("COMMIT;");
} catch (error) {
    await db.exec("ROLLBACK;");
    console.error(JSON.stringify(error, null, 2) || error.message);
}

let result = await db.query("SELECT * FROM accounts;");

console.debug(JSON.stringify(result, null, 2))
```
@PGlite.js

</div>

      {{4}}
<div>

### 5. Vermeide SELECT ohne WHERE in Transaktionen

**Warum?** Sperrt potenziell die ganze Tabelle.

```sql
-- ❌ Gefährlich
BEGIN;
SELECT * FROM orders FOR UPDATE; -- Sperrt alle Zeilen!
-- ...
COMMIT;

-- ✅ Besser
BEGIN;
SELECT * FROM orders WHERE id = 123 FOR UPDATE;
-- ...
COMMIT;
```

</div>

---

## Zusammenfassung

    --{{0}}--
Was haben wir heute gelernt? Transaktionen sind das Fundament für konsistente Datenbanken – sie garantieren ACID-Eigenschaften auch bei parallelen Zugriffen und Systemausfällen.

      {{0}}
<div>

### Kernpunkte

1. **Transaktionen** = Logische Arbeitseinheit ("Alles oder Nichts")
2. **ACID** = Atomicity, Consistency, Isolation, Durability
3. **SQL-Commands:** `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`
4. **Isolation Levels:** Trade-off zwischen Konsistenz und Performance

   - `READ COMMITTED`: Standard, verhindert Dirty Reads
   - `SERIALIZABLE`: Maximale Isolation, aber teuer

5. **Probleme:** Dirty Reads, Non-Repeatable Reads, Phantom Reads, Lost Updates
6. **Deadlocks:** Automatisch erkannt, vermeidbar durch konsistente Lock-Reihenfolge
7. **Best Practices:** Kurze Transaktionen, explizite Steuerung, passender Isolation Level

</div>

---


## Referenzen & Quellen

    {{0}}
<div>

### Dokumentation

- [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [MySQL: InnoDB Locking](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html)
- [SQLite: Transactions](https://www.sqlite.org/lang_transaction.html)

### Bücher

- Martin Kleppmann: "Designing Data-Intensive Applications" (Kapitel 7: Transactions)
- Abraham Silberschatz et al.: "Database System Concepts" (Kapitel 14: Transactions)

### Papers

- Jim Gray: "The Transaction Concept: Virtues and Limitations" (1981)
- ISO/IEC 9075: SQL Standard (Transaction Management)

### Tools

- [PostgreSQL EXPLAIN Visualizer](https://explain.dalibo.com/)
- [SQL Fiddle](http://sqlfiddle.com/) – Test Isolation Levels online

</div>

---

**Nächste Session:** Performance Optimization – Indexe, Query Plans & Concurrency Control
