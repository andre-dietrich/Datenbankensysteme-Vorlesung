# Session 8 – SQL Data Definition (DDL) & Manipulation (DML)

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)

---

## Zusammenfassung

In dieser Session verlassen wir die reine Abfragewelt von SELECT und tauchen in die Strukturebene ein: Wie definieren Sie Schemas? Wie erstellen, ändern und löschen Sie Tabellen? Und wie manipulieren Sie die Daten selbst – Einfügen, Aktualisieren, Löschen?

**DDL (Data Definition Language)** gibt Ihnen die Macht, die Datenbank-Struktur zu formen: `CREATE TABLE` baut Tabellen, `ALTER TABLE` passt sie an, `DROP TABLE` entfernt sie. **DML (Data Manipulation Language)** arbeitet mit den Daten: `INSERT` fügt neue Zeilen ein, `UPDATE` ändert bestehende, `DELETE` entfernt sie.

Wir betrachten beide Welten systematisch:

1. **DDL-Grundlagen:** CREATE, ALTER, DROP für Tabellen
2. **Constraints & Integrität:** PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, DEFAULT
3. **DML-Operationen:** INSERT (single & bulk), UPDATE, DELETE
4. **Best Practices:** Sichere Schema-Evolution, Migration-Strategien

**Bezug zur Agenda:** Nach dieser Session können Sie nicht nur Daten abfragen, sondern auch komplette Datenbank-Schemas entwerfen, implementieren und pflegen. Sie verstehen, wie Constraints Datenintegrität sichern und wie Sie Daten sicher manipulieren.

**Relevanz:** Schema-Design ist die Basis jeder Anwendung. Falsche Constraints führen zu Inkonsistenzen, fehlende zu Chaos. Diese Session ist Ihr Werkzeugkasten für solide Datenbank-Architektur.

---

## Inhalte

### 1. DDL – Data Definition Language

#### CREATE TABLE
- Grundsyntax: Spalten, Datentypen
- Primärschlüssel definieren (inline vs. Constraint)
- Automatische IDs (SERIAL, AUTO_INCREMENT, Sequences)
- Temporäre Tabellen (TEMP/TEMPORARY)

#### Datentypen-Überblick
- Numerisch: INTEGER, BIGINT, DECIMAL, FLOAT, DOUBLE
- Text: VARCHAR(n), TEXT, CHAR(n)
- Datum/Zeit: DATE, TIME, TIMESTAMP, INTERVAL
- Boolean: BOOLEAN
- Spezialtypen: JSON, ARRAY, UUID (je nach DBMS)

#### ALTER TABLE
- Spalten hinzufügen (ADD COLUMN)
- Spalten ändern (ALTER COLUMN, MODIFY)
- Spalten löschen (DROP COLUMN)
- Constraints nachträglich hinzufügen/entfernen
- Tabelle umbenennen (RENAME TO)

#### DROP TABLE
- Tabelle komplett löschen
- CASCADE vs. RESTRICT
- IF EXISTS (sichere Skripte)

---

### 2. Constraints – Datenintegrität sichern

#### PRIMARY KEY
- Eindeutigkeit + NOT NULL
- Single-Column vs. Composite Keys
- Wann natürliche vs. künstliche Keys?

#### FOREIGN KEY
- Referenzielle Integrität
- ON DELETE CASCADE / SET NULL / RESTRICT
- ON UPDATE CASCADE / RESTRICT
- Self-Referencing (hierarchische Daten)

#### UNIQUE
- Eindeutigkeit ohne Primärschlüssel-Semantik
- NULL-Verhalten (je nach DBMS)
- Composite UNIQUE Constraints

#### NOT NULL
- Pflichtfelder
- Kombination mit DEFAULT

#### CHECK
- Benutzerdefinierte Validierung
- Beispiele: Preis > 0, Datum in Zukunft, Enum-Simulation

#### DEFAULT
- Standardwerte bei INSERT
- Zeitstempel, Flags, Default-Status

---

### 3. DML – Data Manipulation Language

#### INSERT
- Einzelne Zeile einfügen
- Mehrere Zeilen gleichzeitig (Bulk Insert)
- INSERT ... SELECT (aus anderer Tabelle)
- INSERT ... ON CONFLICT (Upsert in PostgreSQL/DuckDB)
- RETURNING-Klausel (generierte IDs abrufen)

#### UPDATE
- Einzelne/mehrere Zeilen aktualisieren
- WHERE-Klausel (Vorsicht: ohne WHERE = alle Zeilen!)
- Berechnete Updates (SET price = price * 1.1)
- Mehrere Spalten gleichzeitig
- UPDATE mit JOIN (abhängig von DBMS)

#### DELETE
- Zeilen löschen mit WHERE
- TRUNCATE vs. DELETE (Performance, Rollback)
- Soft Delete Pattern (Status-Flag statt DELETE)

---

### 4. Schema-Evolution & Best Practices

#### Versionierung
- Migrations-Konzept (Up/Down)
- Tools: Flyway, Liquibase, Alembic (Python)
- Rückwärtskompatibilität

#### Sichere Schema-Änderungen
- ADD COLUMN mit DEFAULT (keine Lock-Probleme)
- Spalten umbenennen vs. neu erstellen
- Constraint-Hinzufügen bei großen Tabellen (Downtime-Risiko)

#### Datenintegrität vs. Performance
- Constraints = Sicherheit, aber Overhead
- Wann Constraints weglassen? (Bulk Import, Vertrauenswürdige Pipelines)
- Deferred Constraints (PostgreSQL)

#### Ausblick: Transaktionen
- Vorschau: Nach Joins lernen Sie, wie ACID-Transaktionen mehrere Operationen atomar machen
- Warum später? Transaktionen werden erst bei Multi-Table-Operations richtig relevant

---

## Aktivitäten

### Demo 1: Tabelle erstellen & Schema inspizieren
- Live-Coding: CREATE TABLE Products mit allen Constraint-Typen
- DESCRIBE/SHOW CREATE TABLE zur Inspektion
- ALTER TABLE: Spalte hinzufügen, DEFAULT setzen

### Demo 2: INSERT-Strategien
- Einzelner INSERT
- Bulk INSERT (mehrere Zeilen)
- INSERT ... SELECT (Daten kopieren)
- Fehlerbehandlung bei Constraint-Verletzungen

### Demo 3: UPDATE & DELETE sicher ausführen
- UPDATE mit WHERE-Bedingung
- Gefahr: UPDATE ohne WHERE (alle Zeilen betroffen!)
- DELETE mit WHERE
- TRUNCATE vs. DELETE Performance-Vergleich

### Reflexionsfrage
> "Wann würden Sie auf FOREIGN KEY Constraints verzichten? Welche Risiken nehmen Sie in Kauf?"

### 1-Minute-Paper
> "Was ist der wichtigste Unterschied zwischen ALTER TABLE und DROP/CREATE TABLE?"

---

## Referenzen & Quellen

### Offizielle Dokumentation
- PostgreSQL DDL: https://www.postgresql.org/docs/current/ddl.html
- DuckDB DDL: https://duckdb.org/docs/sql/statements/create_table
- SQL Standard (ISO/IEC 9075)

### Best Practices
- Martin Fowler: Evolutionary Database Design
- Migrations-Pattern: https://flywaydb.org/documentation/concepts/migrations
- Schema Versioning: https://martinfowler.com/articles/evodb.html

### Weiterführend
- Normalisierung & Schema-Design (Session 5 Recap)
- Transaktionen & ACID (Session 11+, nach Joins)
- Indexierung & Performance (Session 15)

---

## Notizen für Materialisierung

- **Praxis-First:** Alle Konzepte mit Live-Beispielen (DuckDB in Browser)
- **Vergleichstabelle:** DDL vs. DML, CREATE vs. ALTER vs. DROP
- **Constraint-Matrix:** Typ, Zweck, Syntax, Beispiel
- **Anti-Pattern:** Häufige Fehler (UPDATE ohne WHERE, DROP CASCADE versehentlich)
- **Migration-Workflow:** Visualisierung einer typischen Schema-Änderung
- **Übung E3:** Hands-on DDL/DML (Tabellen erstellen, Daten einfügen, Schema ändern)
