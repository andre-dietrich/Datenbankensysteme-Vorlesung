# Session 4 (Lecture)

## Titel

Session 4 – Wide Column Stores (kompakt) (Lecture)

## Zusammenfassung

Column Families, Distributed, Write-Heavy, Cassandra/HBase/Bigtable. Kompakter Überblick über Wide-Column-orientierte Speicherung für verteilte, write-intensive Workloads.

## Inhalte

- Wide Column Store Grundprinzip: Row Key + Column Families
- Unterschied zu Row Stores und Column Stores
- Verteilte Architektur: Partitionierung, Replikation, Eventual Consistency
- Write-Path Optimierung: Memtable, SSTable, Compaction
- Read-Path: Bloom Filters, Index-Strukturen
- Schema-Flexibilität: Spalten pro Row können variieren
- Typische Use Cases: Time-Series, IoT, Log-Aggregation, Distributed Systems
- Grenzen: Komplexe Queries, keine Joins, Eventual Consistency Trade-offs
- Beispiel-Systeme: Apache Cassandra, Apache HBase, Google Bigtable, ScyllaDB

## Aktivitäten

- Vergleichstabelle: Row Store vs. Wide Column vs. Column Store
- Szenario: Wann Wide Column Store, wann Relational?
- Mini-Demo: Write-Performance-Simulation (conceptual)

## Referenzen & Quellen

- Apache Cassandra Documentation (Architecture Overview)
- Google Bigtable Paper (2006)
- "Wide Column Stores Explained" (DataStax Blog)
- HBase Architecture Guide
