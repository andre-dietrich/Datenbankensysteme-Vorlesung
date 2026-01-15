# Lecture Agenda

## Überblick

Diese Vorlesung führt systematisch in Datenbanksysteme ein – von kompakten Paradigmen-Überblicken über eine tiefgehende relationale Ausbildung bis hin zu modernen Polyglot-Persistence-Architekturen.

**Struktur:**

- **Block 1**: Paradigmen-Überblick (kompakt) – Key-Value, Document, Wide Column, Column Stores
- **Block 2**: SQL Einführung & Grundlagen – SELECT, DDL, DML, Filtering, Joins
- **Block 3**: SQL Vertiefung – Row-Level Functions, Aggregation, Window Functions, Advanced Techniques
- **Block 4**: Theorie, Optimierung & Polyglot – Relationale Algebra, Performance, Graph/Time Series, Polyglot Persistence
- **Block 5**: Projektabschluss – Präsentation, DSGVO, Ausblick

---

## Sessions & Module

### Block 1 – Paradigmen-Überblick (kompakt)

| Nr  | Type      | Titel                                                     | Dauer | Lernziele | Tags | Summary                                                                                      | Material                |
|-----|-----------|-----------------------------------------------------------|-------|-----------|------|----------------------------------------------------------------------------------------------|-------------------------|
| L1  | lecture   | Daten & Serialisierung + DIKW                             | 90m   | 1,4       |      | CSV/JSON/YAML/XML, Ad-hoc Analyse, Inkonsistenz-Motivation                                  | materials/1-lecture.md  |
| E1  | exercise  | Hands-on: CSV→DuckDB & JSON Flatten                       | 90m   | 1,3       |      | Querying CSV direkt, JSON Feldextraktion, Inkonsistenz-Fahndung                             | materials/1-exercise.md |
| L2  | lecture   | Key-Value Stores (kompakt)                                | 90m   | 1         |      | Zugriff, Patterns, TTL, Atomic Keys, Grenzen (keine Range Queries)                          | materials/2-lecture.md  |
| L3  | lecture   | Document Stores (kompakt)                                 | 90m   | 1         |      | JSON Persistenz, Schema-Evolution, Sync & Konflikte                                          | materials/3-lecture.md  |
| L4  | lecture   | Wide Column & Column Stores (kompakt)                     | 90m   | 1         |      | Column Families (Cassandra/HBase) + Columnar Storage (DuckDB/Parquet), Kompression, Analytics | materials/4-lecture.md  |
| L5  | lecture   | Relationales Modell: Tabellen, Keys, Integrität           | 90m   | 2         |      | Einführung Relationale Datenbanken, Tabellen, Primär-/Fremdschlüssel, Normalisierung (Überblick), Constraints | materials/5-lecture.md  |
| L6  | lecture   | Paradigmen im Vergleich & Trade-offs                      | 90m   | 1,5       |      | Strukturgrad, Konsistenz, Abfrageausdruck, Performance-Profile                               | materials/6-lecture.md  |
| -   | milestone | MS1 nach L6                                               | -     | 1,5       | MS1  | Rohdaten + KV/Document/Wide-Column/Column Artefakt & Vergleichsnotizen                       | project/ms1.md          |

---

### Block 2 – SQL Einführung & Grundlagen

| Nr  | Type      | Titel                                                     | Dauer | Lernziele | Tags | Summary                                                                                      | Material                |
|-----|-----------|-----------------------------------------------------------|-------|-----------|------|----------------------------------------------------------------------------------------------|-------------------------|
| L7  | lecture   | SQL Introduction & Query Data (SELECT)                    | 90m   | 2         |      | Was ist SQL, Komponenten, SELECT/FROM/WHERE/ORDER BY/GROUP BY/HAVING/DISTINCT               | materials/7-lecture.md  |
| E2  | exercise  | SQL Basics: Praktische SELECT-Abfragen                    | 90m   | 2,3       |      | Queries auf Beispielschema, Sortierung, Gruppierung, Aggregation                            | materials/2-exercise.md |
| L8  | lecture   | SQL Data Definition (DDL) & Manipulation (DML)            | 90m   | 2         |      | CREATE/ALTER/DROP, INSERT/UPDATE/DELETE, Constraints                                         | materials/8-lecture.md  |
| E3  | exercise  | DDL/DML Hands-on                                          | 90m   | 2,3       |      | Tabellen erstellen, ändern, Daten einfügen/ändern/löschen                                   | materials/3-exercise.md |
| L9  | lecture   | Database Normalization & Schema Design                    | 90m   | 2         |      | Normalisierung (1NF, 2NF, 3NF), Anomalien vermeiden, Interaktives Schema-Design (Online-Shop) | materials/9-lecture.md  |
| L10 | lecture   | SQL Joins & Combining Data                                | 90m   | 2         |      | INNER/LEFT/RIGHT/FULL/CROSS, UNION/EXCEPT/INTERSECT                                         | materials/10-lecture.md |
| E4  | exercise  | Joins & Set Operations                                    | 90m   | 2,3       |      | Multi-Table Queries, Join-Strategien, Set-Operatoren                                        | materials/4-exercise.md |
| -   | milestone | MS2 nach L10                                              | -     | 2,3       | MS2  | SQL-Schema + DDL-Skript, grundlegende Abfragen                                              | project/ms2.md          |

---

### Block 3 – SQL Vertiefung

| Nr  | Type      | Titel                                                     | Dauer | Lernziele | Tags | Summary                                                                                      | Material                |
|-----|-----------|-----------------------------------------------------------|-------|-----------|------|----------------------------------------------------------------------------------------------|-------------------------|
| L11 | lecture   | Row-Level Functions (String, Number, Date, CASE)          | 90m   | 2         |      | String/Number/Date-Funktionen, Null-Handling, CASE                                           | materials/11-lecture.md |
| L12 | lecture   | Aggregation & Window Functions                            | 90m   | 2         |      | Aggregate Functions, Window Basics, Ranking/Value Functions                                 | materials/12-lecture.md |
| E5  | exercise  | Advanced Aggregation & Analytics                          | 90m   | 2,3       |      | Window Functions, Ranking, analytische Queries                                               | materials/5-exercise.md |
| L13 | lecture   | Advanced SQL Techniques                                   | 90m   | 2         |      | Subqueries, CTEs, Views, Temp Tables, Stored Procedures                                     | materials/13-lecture.md |
| E6  | exercise  | Subqueries, CTEs & Views                                  | 90m   | 2,3       |      | Mehrstufige CTEs, komplexe Subqueries, View-Erstellung                                      | materials/6-exercise.md |
| -   | milestone | MS3 nach L13                                              | -     | 2,3       | MS3  | Erweiterte Abfragen + Analytics, Views/CTEs                                                  | project/ms3.md          |

---

### Block 4 – Theorie, Optimierung & Polyglot-Abschluss

| Nr  | Type      | Titel                                                     | Dauer | Lernziele | Tags | Summary                                                                                      | Material                |
|-----|-----------|-----------------------------------------------------------|-------|-----------|------|----------------------------------------------------------------------------------------------|-------------------------|
| L14 | lecture   | Transaktionen & ACID                                      | 90m   | 2,4       |      | BEGIN/COMMIT/ROLLBACK, ACID-Eigenschaften, Isolation Levels, Savepoints, Szenariobasiert    | materials/14-lecture.md |
| E7  | exercise  | Transaktionen & Concurrency Scenarios                     | 90m   | 2,3       |      | Praktische Übungen: Lost Updates, Dirty Reads, Deadlock-Szenarien                           | materials/7-exercise.md |
| L15 | lecture   | Performance Optimization                                  | 90m   | 2         |      | Indexes, Partitions, Query Plans, Best Practices                                             | materials/15-lecture.md |
| L16 | lecture   | Graph Stores (kompakt)                                    | 90m   | 1         |      | Nodes, Edges, Cypher, Neo4j, Use Cases                                                       | materials/16-lecture.md |
| L17 | lecture   | Time Series Stores (kompakt)                              | 90m   | 1         |      | InfluxDB, Tags/Fields, Retention Policies                                                    | materials/17-lecture.md |
| L18 | lecture   | Polyglot Persistence Pattern                              | 90m   | 5         |      | Use Cases, Technologie-Mix, Trade-offs                                                       | materials/18-lecture.md |
| -   | milestone | MS4 nach L18                                              | -     | 5         | MS4  | Polyglot-Architektur skizziert                                                               | project/ms4.md          |

---

### Block 5 – Projektabschluss

| Nr  | Type      | Titel                                                     | Dauer | Lernziele | Tags  | Summary                                                                                      | Material                |
|-----|-----------|-----------------------------------------------------------|-------|-----------|-------|----------------------------------------------------------------------------------------------|-------------------------|
| L19 | lecture   | Projektpräsentation & Best Practices                      | 90m   | 5         |       | Architektur-Review, Lessons Learned                                                          | materials/19-lecture.md |
| L20 | lecture   | DSGVO, Datensicherheit & Compliance                       | 90m   | 5         |       | Regulatorische Anforderungen (GDPR, Finance)                                                 | materials/20-lecture.md |
| L21 | lecture   | Abschluss & Ausblick                                      | 90m   | 5         |       | Zusammenfassung, moderne Trends (Lakehouse, Cloud-DBs)                                       | materials/21-lecture.md |
| -   | milestone | Final nach L21                                            | -     | 1-5       | FINAL | Gesamtprojekt + Doku + Präsentation                                                          | project/final.md        |

---

## Lernziel-Zuordnung

- **LZ 1**: Paradigmen-Überblick, Datenformate, Serialisierung
- **LZ 2**: Relationale Grundlagen, SQL-Praxis, Theorie
- **LZ 3**: Praktische Übungen, Projektarbeit
- **LZ 4**: DIKW-Modell, Datenqualität
- **LZ 5**: Polyglot Persistence, Architektur, Best Practices
