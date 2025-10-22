# Session 13 (Lecture)

## Titel

Session 13 – Query Optimization & EXPLAIN (Lecture)

## Zusammenfassung

Abfragepfade, Kostenschätzung, Join Order, Optimierungshebel. Verständnis für die Arbeit des Query Optimizers und Interpretation von Execution Plans.

## Inhalte

- Query Optimizer Grundlagen:
  - Parser → Planner → Executor
  - Cost-Based Optimization
  - Statistics & Cardinality Estimation
- EXPLAIN & EXPLAIN ANALYZE:
  - Execution Plan lesen
  - Seq Scan, Index Scan, Index Only Scan
  - Nested Loop, Hash Join, Merge Join
  - Cost-Werte interpretieren (Startup Cost, Total Cost)
- Join Order Optimierung:
  - Warum Reihenfolge wichtig ist
  - Heuristics & Dynamic Programming
- Optimierungshebel:
  - Index-Design
  - Query Rewriting (Äquivalente Ausdrücke)
  - Statistics Update (ANALYZE)
  - Hints (erwähnen, aber mit Vorsicht)

## Aktivitäten

- Live-Coding: EXPLAIN auf mehrere Queries
- Übung: Execution Plan analysieren und Flaschenhälse finden
- Diskussion: Wann manuelle Optimierung vs. Optimizer vertrauen?

## Referenzen & Quellen

- "SQL Performance Explained" (Markus Winand)
- PostgreSQL EXPLAIN Documentation
- Query Optimization Papers (Selinger et al.)
