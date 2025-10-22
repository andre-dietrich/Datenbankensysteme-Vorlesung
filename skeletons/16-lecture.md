# Session 14 (Lecture)

## Titel

Session 14 – Performance Strategien: Denormalisierung & Co (Lecture)

## Zusammenfassung

Materialized Views, Partitioning, Query Rewriting. Fortgeschrittene Techniken zur Performance-Optimierung jenseits von Indexen.

## Inhalte

- Denormalisierung (Wiederholung aus L9):
  - Bewusste Redundanz für weniger Joins
  - Trade-offs: Konsistenz vs. Performance
- Materialized Views:
  - Precomputed Results speichern
  - Refresh Strategien (ON DEMAND, ON COMMIT, Scheduled)
  - Use Cases: Reporting, Dashboards
- Partitioning:
  - Range Partitioning (z. B. nach Datum)
  - List Partitioning, Hash Partitioning
  - Partition Pruning (Query Optimizer nutzt Partitionen)
- Query Rewriting:
  - Subquery → JOIN
  - Äquivalente Formulierungen testen
- Caching-Strategien:
  - Query Result Cache
  - Application-Level Caching (Redis vor Relational DB)

## Aktivitäten

- Szenario: Reporting-Dashboard → Materialized View Design
- Übung: Partitioning Strategy für Log-Daten
- Diskussion: Wann Caching, wann Denormalisierung?

## Referenzen & Quellen

- PostgreSQL Materialized Views Documentation
- Partitioning Best Practices
- "High Performance MySQL" (Schwartz et al.)
