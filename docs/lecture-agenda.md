# Lecture Agenda

> Draft v2.0 – Fokus auf Relationale Datenbanken, SQL & Relationale Algebra. Andere Paradigmen (KV, Document, Column, Graph) jeweils kompakt in 1 Lektion. Polyglot-Projekt bleibt erhalten. Tags: [MSx] = Projekt-Meilenstein.

## Überblick

Die Agenda führt kompakt durch verschiedene DB-Paradigmen (File, KV, Document, Column, Graph), legt aber den **Hauptfokus auf Relationale Datenbanken**: Relationale Algebra, SQL (Grundlagen & Vertiefung), Normalisierung, Transaktionen, Indexe, Query-Optimierung und Nebenläufigkeit. Das Polyglot-Projekt vergleicht Paradigmen in der Praxis.

## Lernziele Mapping

| Lernziel                       | Primäre Phasen                                        |
| ------------------------------ | ----------------------------------------------------- |
| 1 Paradigmen verstehen         | L1–L6 (kompakt) + L18 (Graph) + L20 (Polyglot)       |
| 2 Relationale DB & SQL         | **L7–L17** (Hauptfokus: 11 Lektionen + 4 Exercises)  |
| 3 Praktische Erfahrung         | Alle Exercises (E1–E7)                                |
| 4 ACID/Konsistenz/Verteiltheit | L10 (ACID formal), L16–L17 (MVCC/Locking), L21 (CAP) |
| 5 Bewertung & Trade-offs       | L6, L20 (Polyglot), L21 (Abschluss)                   |

## Projekt-Meilensteine (Polyglot)

| Code  | Zeitpunkt | Inhalt                                                        |
| ----- | --------- | ------------------------------------------------------------- |
| MS1   | Nach L6   | Rohdaten + KV/Document/Wide-Column/Column Layer (Vergleich)   |
| MS2   | Nach L11  | Relational Redesign + Normalisierung + DDL                    |
| MS3   | Nach L15  | Index-Design + Query-Optimierung + Performance-Analyse        |
| MS4   | Nach L18  | Graph-Extension (Beziehungsanalyse)                           |
| Final | L20/L21   | Polyglot Architektur + Konsistenz-Narrativ + Trade-off Report |

---

## Sessions im Detail

### Block 1 – Paradigmen-Überblick (kompakt)

| Nr  | Type      | Titel                                      | Dauer | Lernziele | Tags | Summary                                                                  | Material                |
| --- | --------- | ------------------------------------------ | ----- | --------- | ---- | ------------------------------------------------------------------------ | ----------------------- |
| L1  | lecture   | Daten & Serialisierung + DIKW              | 90m   | 1,4       |      | CSV/JSON/YAML/XML, Ad-hoc Analyse, Inkonsistenz-Motivation              | materials/1-lecture.md  |
| E1  | exercise  | Hands-on: CSV→DuckDB & JSON Flatten        | 90m   | 1,3       |      | Querying CSV direkt, JSON Feldextraktion, Inkonsistenz-Fahndung          | materials/1-exercise.md |
| L2  | lecture   | Key-Value Stores (kompakt)                 | 90m   | 1         |      | Zugriff, Patterns, TTL, Atomic Keys, Grenzen (keine Range Queries)      | materials/2-lecture.md  |
| L3  | lecture   | Document Stores (kompakt)                  | 90m   | 1         |      | JSON Persistenz, Schema-Evolution, Sync & Konflikte                      | materials/3-lecture.md  |
| L4  | lecture   | Wide Column Stores (kompakt)               | 90m   | 1         |      | Column Families, Distributed, Write-Heavy, Cassandra/HBase/Bigtable      | materials/4-lecture.md  |
| L5  | lecture   | Column Stores (kompakt)                    | 90m   | 1         |      | Kompression, Analytics, Aggregations-Performance, DuckDB/Parquet         | materials/5-lecture.md  |
| L6  | lecture   | Paradigmen im Vergleich & Trade-offs       | 90m   | 1,5       |      | Strukturgrad, Konsistenz, Abfrageausdruck, Performance-Profile           | materials/6-lecture.md  |
| -   | milestone | MS1 nach L6                                | -     | 1,5       | MS1  | Rohdaten + KV/Document/Wide-Column/Column Artefakt & Vergleichsnotizen   | project/ms1.md          |

### Block 2 – Relationale Grundlagen (Algebra & SQL Basics)

| Nr  | Type     | Titel                                                     | Dauer | Lernziele | Tags | Summary                                                              | Material                |
| --- | -------- | --------------------------------------------------------- | ----- | --------- | ---- | -------------------------------------------------------------------- | ----------------------- |
| L7  | lecture  | Relationales Modell & Relationale Algebra                 | 90m   | 2         |      | Tabellen, Keys, Relationale Operationen (σ, π, ⨝, ∪, −), Äquivalenz | materials/7-lecture.md  |
| E2  | exercise | Relationale Algebra & SQL Translation                     | 90m   | 2,3       |      | Formale Notation, Äquivalenzen, Übersetzung in SQL                   | materials/2-exercise.md |
| L8  | lecture  | SQL Basics: SELECT, FROM, WHERE, JOIN                     | 90m   | 2         |      | Grundlegende Abfragen, Inner/Outer Joins, Aggregate (COUNT, SUM)    | materials/8-lecture.md  |
| E3  | exercise | SQL Basics: Praktische Abfragen                           | 90m   | 2,3       |      | Queries auf Beispielschema, Joins, Gruppierungen                     | materials/3-exercise.md |
| L9  | lecture  | SQL Vertiefung: Subqueries, CTEs, Window Functions        | 90m   | 2         |      | Korrelierte Subqueries, WITH-Klausel, ROW_NUMBER, PARTITION BY       | materials/9-lecture.md  |
| E4  | exercise | SQL Vertiefung: Komplexe Queries                          | 90m   | 2,3       |      | Mehrstufige CTEs, Window Functions, analytische Abfragen             | materials/4-exercise.md |

### Block 3 – Relationale Integrität & Transaktionen

| Nr  | Type      | Titel                                                | Dauer | Lernziele | Tags | Summary                                                      | Material                 |
| --- | --------- | ---------------------------------------------------- | ----- | --------- | ---- | ------------------------------------------------------------ | ------------------------ |
| L10 | lecture   | Normalisierung (1NF–BCNF) + Denormalisierung         | 90m   | 2,5       |      | Redundanzabbau, funktionale Abhängigkeiten, Trade-offs      | materials/10-lecture.md  |
| L11 | lecture   | Constraints & Referentielle Integrität               | 90m   | 2,4       |      | PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL            | materials/11-lecture.md  |
| L12 | lecture   | Transaktionen & ACID (formal)                        | 90m   | 2,4       |      | Atomicität, Konsistenz, Isolation, Durability (formalisiert) | materials/12-lecture.md  |
| E5  | exercise  | ACID & Isolation Levels: Anomalie-Simulation         | 90m   | 2,4       |      | Lost Update, Dirty Read, Phantom Read (praktische Szenarien) | materials/5-exercise.md  |
| -   | milestone | MS2 nach L11                                         | -     | 2,4,5     | MS2  | Relational Redesign + Normalisierung + DDL                   | project/ms2.md           |

### Block 4 – Query-Optimierung & Performance

| Nr  | Type      | Titel                                         | Dauer | Lernziele | Tags | Summary                                                       | Material                |
| --- | --------- | --------------------------------------------- | ----- | --------- | ---- | ------------------------------------------------------------- | ----------------------- |
| L13 | lecture   | Indexe: B-Trees, Hash, Bitmap                 | 90m   | 2,4,5     |      | Indexstrukturen, Kosten, Covering Indexes                     | materials/13-lecture.md |
| L14 | lecture   | Query Optimization & EXPLAIN                  | 90m   | 2,4,5     |      | Abfragepfade, Kostenschätzung, Join Order, Optimierungshebel | materials/14-lecture.md |
| E6  | exercise  | Index-Design & Performance-Analyse            | 90m   | 2,3,4,5   |      | Index an/aus, EXPLAIN Plan lesen, Benchmark-Vergleich        | materials/6-exercise.md |
| L15 | lecture   | Performance Strategien: Denormalisierung & Co | 90m   | 2,5       |      | Materialized Views, Partitioning, Query Rewriting             | materials/15-lecture.md |
| -   | milestone | MS3 nach L15                                  | -     | 2,4,5     | MS3  | Index-Design + Query-Optimierung + Performance-Report         | project/ms3.md          |

### Block 5 – Nebenläufigkeit & Fortgeschrittene Konzepte

| Nr  | Type    | Titel                                                        | Dauer | Lernziele | Tags | Summary                                                 | Material                |
| --- | ------- | ------------------------------------------------------------ | ----- | --------- | ---- | ------------------------------------------------------- | ----------------------- |
| L16 | lecture | Locking vs. MVCC                                             | 90m   | 2,4       |      | Pessimistic/Optimistic Locking, Snapshot Isolation      | materials/16-lecture.md |
| L17 | lecture | Views, Materialized Views, Triggers, Stored Procedures       | 90m   | 2         |      | Abstraktion, Cached Queries, Business Logic in der DB   | materials/17-lecture.md |

### Block 6 – Graph & Polyglot

| Nr  | Type      | Titel                                        | Dauer | Lernziele | Tags | Summary                                                 | Material                |
| --- | --------- | -------------------------------------------- | ----- | --------- | ---- | ------------------------------------------------------- | ----------------------- |
| L18 | lecture   | Graph Databases (kompakt)                    | 90m   | 1,5       |      | Property Graph, Traversal, Pattern Matching vs. Joins   | materials/18-lecture.md |
| E7  | exercise  | Graph Traversal & Relationales Redesign      | 90m   | 1,3,5     |      | Pfadsuche, Vergleich Graph Query vs. rekursive SQL CTEs | materials/7-exercise.md |
| -   | milestone | MS4 nach L18                                 | -     | 1,5       | MS4  | Graph-Extension (Beziehungsanalyse)                     | project/ms4.md          |

### Block 7 – Polyglot & Verteiltheit

| Nr  | Type      | Titel                                            | Dauer | Lernziele | Tags  | Summary                                                           | Material                |
| --- | --------- | ------------------------------------------------ | ----- | --------- | ----- | ----------------------------------------------------------------- | ----------------------- |
| L19 | lecture   | Polyglot Persistence & Architektur-Patterns      | 90m   | 5         |      | CQRS, Event Sourcing, Data Lake, Integrationsstrategien           | materials/19-lecture.md |
| L20 | lecture   | Verteiltheit: Replikation, Sharding, Konsistenz  | 90m   | 4,5       |      | Master-Replica, Partitioning, Eventual Consistency                | materials/20-lecture.md |
| L21 | lecture   | CAP-Theorem, Konsistenzmodelle & Abschluss       | 90m   | 4,5       |      | CAP Formalisierung, Strong/Eventual/Causal, NewSQL/HTAP Ausblick  | materials/21-lecture.md |
| -   | milestone | Final nach L21                                   | -     | 1,2,4,5   | Final | Polyglot Architektur + Konsistenz-Narrativ + Trade-off Report    | project/final.md        |

---

## Nächste Schritte

1. **Review**: Feedback zur neuen Struktur?
2. **Session-Skeletons**: Soll ich die Skeletons entsprechend aktualisieren?
3. **Materials**: Sollen bestehende Materials migriert/angepasst werden?

> Bitte Rückmeldung: "Agenda OK" oder Änderungswünsche. Danach: Skeleton-Anpassung & Material-Migration.
