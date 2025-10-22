# Session 10 (Lecture)

## Titel

Session 10 – Constraints & Referentielle Integrität (Lecture)

## Zusammenfassung

PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL. Mechanismen zur Durchsetzung von Datenintegrität auf Schemaebene.

## Inhalte

- Constraints Überblick: Warum? (Datenkonsistenz, Fehlerprävention)
- PRIMARY KEY: Eindeutigkeit, Identifikation
- FOREIGN KEY: Referentielle Integrität
  - ON DELETE CASCADE / SET NULL / RESTRICT
  - ON UPDATE CASCADE / SET NULL / RESTRICT
- UNIQUE: Eindeutigkeit ohne Primary Key
- NOT NULL: Pflichtfelder
- CHECK: Benutzerdefinierte Bedingungen (z. B. Wertebereiche)
- DEFAULT: Standardwerte
- Constraint-Verletzungen: Error Handling
- Performance-Implikationen: Overhead bei INSERT/UPDATE/DELETE

## Aktivitäten

- Live-Coding: Schema mit Constraints erstellen
- Übung: Constraint-Verletzungen provozieren und beobachten
- Diskussion: Wann CHECK vs. Anwendungslogik?

## Referenzen & Quellen

- SQL Standard (Constraints Section)
- PostgreSQL Constraints Documentation
- "Pro SQL Database Design" (Kunen)
