# Session 4 (Lecture)

## Titel

Session 4 – Column Stores (kompakt) (Lecture)

## Zusammenfassung

Kompression, Analytics, Aggregations-Performance. Kompakter Überblick über Column-orientierte Speicherung für analytische Workloads.

## Inhalte

- Column Storage Grundprinzip: Spaltenweise statt zeilenweise
- Kompression: Run-Length Encoding, Dictionary Encoding, Bit-Packing
- Speicherlayout: Segmentierung, Zonenmaps
- Read-Optimierung: Projektionen, Late Materialization
- Analytical Workloads vs. Transactional (OLAP vs. OLTP)
- Performance: Aggregationen, Scans, Filter Pushdown
- Typische Use Cases: Data Warehousing, BI, Reporting
- Grenzen: Langsame Inserts/Updates, Row-Reconstruction Overhead
- Beispiel-Systeme: DuckDB, ClickHouse, Apache Parquet, Google BigQuery

## Aktivitäten

- Mini-Demo: Aggregation auf CSV vs. Parquet (Performance-Vergleich)
- Szenario: Wann Column Store, wann Row Store?
- Kompression Live-Beispiel

## Referenzen & Quellen

- DuckDB Documentation (Parquet Support)
- ClickHouse Blog (Compression Algorithms)
- "Column-Stores vs. Row-Stores" (Abadi et al.)
