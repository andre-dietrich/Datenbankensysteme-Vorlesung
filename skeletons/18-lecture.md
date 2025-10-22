# Session 16 (Lecture)

## Titel

Session 16 – Views, Materialized Views, Triggers, Stored Procedures (Lecture)

## Zusammenfassung

Abstraktion, Cached Queries, Business Logic in der DB. Fortgeschrittene SQL-Features für Modularität und Datenkapselung.

## Inhalte

- Views:
  - Logische Abstraktion (Virtual Tables)
  - Vereinfachung komplexer Queries
  - Security: Row-Level Filtering via Views
  - Updatable Views (Einschränkungen)
- Materialized Views (Vertiefung aus L14):
  - Precomputed Results
  - Refresh-Strategien
- Triggers:
  - BEFORE/AFTER INSERT/UPDATE/DELETE
  - Use Cases: Audit Logging, Derived Columns
  - Risiken: Versteckte Logik, Performance
- Stored Procedures & Functions:
  - Business Logic in der DB
  - Parameter, Return Values
  - Vor/Nachteile: Performance vs. Wartbarkeit

## Aktivitäten

- Live-Coding: View und Trigger erstellen
- Diskussion: Wann Logik in DB vs. Application Layer?
- Übung: Audit-Log via Trigger implementieren

## Referenzen & Quellen

- PostgreSQL Views & Triggers Documentation
- "SQL and Relational Theory" (Date)
- Stored Procedures Best Practices
