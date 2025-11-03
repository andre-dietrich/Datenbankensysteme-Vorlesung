# Session 5 – Relationales Modell: Tabellen, Keys, Integrität

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale Grundlagen)

---

## Zusammenfassung

Nach dem Paradigmen-Überblick (L1–L4) tauchen wir nun tief in das **relationale Modell** ein – das Fundament moderner Datenbanken und SQL. In dieser Session lernen Sie die Grundprinzipien relationaler Datenbanken kennen: **Tabellen**, **Zeilen und Spalten**, **Primär- und Fremdschlüssel**, **Integritätsbedingungen** und die Grundidee der **Normalisierung**.

Wir klären, warum das relationale Modell so erfolgreich ist, welche Probleme es löst (z. B. Redundanz, Inkonsistenz) und wie es sich von den bisher betrachteten Paradigmen (KV, Document, Column) unterscheidet. Am Ende dieser Session haben Sie ein solides Verständnis der relationalen Architektur und sind bereit für die SQL-Praxis ab L7.

**Bezug zur Agenda:**  
Diese Session bildet den Übergang von Block 1 (Paradigmen-Überblick) zu Block 2 (SQL-Praxis). Sie liefert das konzeptionelle Fundament für alle folgenden SQL-Sessions.

---

## Inhalte (Geplant)

### Block 1: Das relationale Modell – Grundlagen

- **Was ist das relationale Modell?**
  - Definition: Daten in Tabellen (Relations), Zeilen (Tupel), Spalten (Attribute)
  - Codd's Relational Model (1970): Formale Grundlage
  
- **Warum relational?**
  - Strukturierte Daten, klare Schemata
  - Vermeidung von Redundanz und Inkonsistenz
  - Deklarative Abfragesprache (SQL)
  
- **Vergleich zu bisherigen Paradigmen:**
  - KV: Unstrukturiert, keine Beziehungen
  - Document: Flexibles Schema, aber schwierige Joins
  - Column: Analytisch, aber nicht für OLTP
  - Relational: Strukturiert, konsistent, Join-fähig

### Block 2: Tabellen, Zeilen, Spalten

- **Tabellen (Relations):**
  - Jede Tabelle repräsentiert eine Entität (z. B. `Customers`, `Orders`)
  - Spalten: Attribute (z. B. `name`, `email`, `order_date`)
  - Zeilen: Datensätze (z. B. ein Kunde, eine Bestellung)
  
- **Datentypen:**
  - INT, VARCHAR, DATE, BOOLEAN, DECIMAL, ...
  - Warum Datentypen wichtig sind: Validierung, Speichereffizienz
  
- **Constraints (Integritätsbedingungen):**
  - NOT NULL: Pflichtfelder
  - UNIQUE: Eindeutige Werte
  - CHECK: Bedingungen (z. B. `age >= 18`)
  - DEFAULT: Standardwerte

### Block 3: Schlüssel – Primär- und Fremdschlüssel

- **Primärschlüssel (Primary Key):**
  - Eindeutige Identifikation jeder Zeile
  - Nicht NULL, unveränderlich
  - Beispiel: `customer_id`, `order_id`
  
- **Fremdschlüssel (Foreign Key):**
  - Referenziert Primärschlüssel einer anderen Tabelle
  - Sichert referenzielle Integrität
  - Beispiel: `Orders.customer_id` → `Customers.customer_id`
  
- **Beziehungen:**
  - 1:1, 1:N, N:M
  - Wie Fremdschlüssel Beziehungen modellieren

### Block 4: Normalisierung (Überblick)

- **Warum Normalisierung?**
  - Redundanz vermeiden
  - Update-Anomalien verhindern
  - Datenintegrität sichern
  
- **Normalformen (Kurzüberblick):**
  - 1NF: Atomare Werte, keine Wiederholungsgruppen
  - 2NF: Keine partiellen Abhängigkeiten
  - 3NF: Keine transitiven Abhängigkeiten
  - (BCNF, 4NF, 5NF: optional, später)
  
- **Trade-offs:**
  - Normalisierung vs. Performance (Join-Overhead)
  - Denormalisierung in OLAP-Szenarien

### Block 5: Integritätsbedingungen & Constraints

- **Arten von Constraints:**
  - Entity Integrity: Primärschlüssel NOT NULL
  - Referential Integrity: Fremdschlüssel-Validierung
  - Domain Integrity: Datentypen, CHECK-Bedingungen
  
- **Cascading Operations:**
  - ON DELETE CASCADE / SET NULL / RESTRICT
  - ON UPDATE CASCADE / RESTRICT
  
- **Warum Constraints wichtig sind:**
  - Datenkonsistenz auf DB-Ebene
  - Weniger Fehler in Anwendungslogik

---

## Aktivitäten (Geplant)

1. **Aktivierungsimpuls (5 Min):**
   - Szenario: "Ein E-Commerce-System speichert Bestellungen. Welche Probleme entstehen, wenn wir Kundendaten in jeder Bestellung wiederholen?"
   - Hypothese sammeln: Redundanz, Update-Anomalien

2. **Live-Modellierung (15 Min):**
   - Gemeinsam eine einfache Datenbank entwerfen: `Customers`, `Orders`, `Products`
   - Primär- und Fremdschlüssel definieren
   - Constraints hinzufügen (NOT NULL, UNIQUE, CHECK)

3. **Normalisierungs-Beispiel (10 Min):**
   - Denormalisierte Tabelle zeigen (z. B. Kunde + Bestellung in einer Zeile)
   - Schrittweise normalisieren (1NF → 2NF → 3NF)

4. **Paradigmen-Matrix erweitern (5 Min):**
   - Relationales Modell: Strukturiert, konsistent, Join-fähig, ACID
   - Vergleich mit KV, Document, Column

5. **Reflexion (5 Min):**
   - 1-Minute-Paper: "Was ist der größte Vorteil des relationalen Modells? Was könnte ein Nachteil sein?"

---

## Referenzen & Quellen

- **E. F. Codd: "A Relational Model of Data for Large Shared Data Banks"** (1970)
- **Database System Concepts** (Silberschatz, Korth, Sudarshan) – Kapitel 2 & 3
- **SQL Performance Explained** (Markus Winand) – Normalisierung & Indexierung
- **Paradigmen-Matrix (laufend)**: `docs/paradigms-matrix.md`
- **DuckDB Documentation**: [https://duckdb.org/docs/](https://duckdb.org/docs/)
- **SQLite Tutorial**: [https://www.sqlitetutorial.net/](https://www.sqlitetutorial.net/)

---

## Offene Fragen / TODOs

- [ ] Live-Modellierungs-Beispiel vorbereiten (Customers, Orders, Products)
- [ ] Normalisierungs-Beispiel mit schrittweiser Transformation
- [ ] Paradigmen-Matrix aktualisieren (Relationales Modell hinzufügen)
- [ ] Constraints-Demo in DuckDB/SQLite (CREATE TABLE mit Constraints)
