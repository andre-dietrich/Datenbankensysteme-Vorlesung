# Session 8 (Lecture)

## Titel

Session 8 – SQL Vertiefung: Subqueries, CTEs, Window Functions (Lecture)

## Zusammenfassung

Korrelierte Subqueries, WITH-Klausel, ROW_NUMBER, PARTITION BY. Fortgeschrittene SQL-Techniken für komplexe analytische Abfragen.

## Inhalte

- Subqueries:
  - Skalare Subqueries (SELECT mit einzelnem Wert)
  - Korrelierte vs. unkorrelierte Subqueries
  - EXISTS, NOT EXISTS
  - IN, NOT IN, ANY, ALL
- Common Table Expressions (CTEs): WITH-Klausel
  - Einfache CTEs
  - Rekursive CTEs (Hierarchien, Pfade)
- Window Functions:
  - ROW_NUMBER, RANK, DENSE_RANK
  - PARTITION BY, ORDER BY
  - Aggregate mit OVER: SUM() OVER (), AVG() OVER ()
  - LEAD, LAG (Zugriff auf benachbarte Zeilen)
- Use Cases: Top-N Queries, Running Totals, Moving Averages

## Aktivitäten

- Live-Coding: CTE für mehrstufige Aggregation
- Übung: Window Function für Ranking
- Vergleich: Subquery vs. JOIN vs. CTE (Performance & Lesbarkeit)

## Referenzen & Quellen

- PostgreSQL Window Functions Documentation
- "Modern SQL" (Markus Winand)
- Recursive CTE Examples
