# Session 4 – Wide Column & Column Stores (kompakt)

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 1 (Paradigmen-Überblick)

---

## Zusammenfassung

In dieser Session beleuchten wir zwei verwandte, aber konzeptionell unterschiedliche Speicherparadigmen: **Wide Column Stores** (wie Cassandra, HBase) und **Column Stores** (wie DuckDB, Parquet). Beide setzen auf spaltenorientierte Organisation, verfolgen aber unterschiedliche Ziele: Wide Column Stores für hochskalierbaren, verteilten Key-Row-Zugriff mit flexiblen Column Families; Column Stores für analytische Workloads mit effizienter Kompression und spaltenweiser Aggregation.

Wir klären, warum Spalten-Speicherung für Analytics-Queries oft schneller ist als zeilenorientierte Formate, wie Kompressionsverfahren (RLE, Dictionary Encoding) die Effizienz steigern, und in welchen Szenarien Sie welches Modell einsetzen sollten.

**Bezug zur Agenda:**  
Diese Session schließt den Paradigmen-Überblick ab (Block 1) und bereitet die Transition zum relationalen Modell vor. Wir ergänzen die Paradigmen-Matrix um die Achse "Spalten vs. Zeilen" und "OLTP vs. OLAP".

---

## Inhalte (Geplant)

### Block 1: Wide Column Stores (Cassandra, HBase)

- **Was sind Wide Column Stores?**
  - Grundkonzept: Row Key → Column Families → Columns
  - Unterschied zu relationalen Tabellen (dynamische Spalten, keine feste Schema-Einschränkung)
  
- **Einsatzszenarien:**
  - Hochskalierbare, verteilte Systeme (z. B. soziale Netzwerke, IoT)
  - Time-Series-Daten, Event Logs
  
- **Zugriffsmuster:**
  - Primärer Zugriff: Row Key → schneller Lookup
  - Range Queries auf Row Keys möglich
  - Column Family als Gruppierung verwandter Daten

- **Vor- und Nachteile:**
  - ✅ Horizontal skalierbar, flexibles Schema
  - ❌ Komplexere Modellierung, weniger Ad-hoc-Queries

### Block 2: Column Stores (DuckDB, Parquet)

- **Was sind Column Stores?**
  - Spaltenorientierte Speicherung: Alle Werte einer Spalte zusammen
  - Ideal für analytische Abfragen (Aggregationen, Scans über wenige Spalten)
  
- **Kompression:**
  - Run-Length Encoding (RLE)
  - Dictionary Encoding
  - Bit-Packing
  
- **Einsatzszenarien:**
  - OLAP (Online Analytical Processing)
  - Data Warehouses, Big Data Analytics
  - Reporting, BI-Dashboards
  
- **Zugriffsmuster:**
  - Spaltenweise Scans (z. B. `SELECT AVG(price) FROM products`)
  - Deutlich schneller bei wenigen Spalten, vielen Zeilen
  
- **Vor- und Nachteile:**
  - ✅ Hohe Kompression, schnelle Aggregationen
  - ❌ Langsamer bei Zeilen-Updates, OLTP-ungeeignet

### Block 3: Vergleich & Trade-offs

- **Wide Column vs. Column Stores:**
  - Wide Column: Verteilte Key-Row-Architektur, flexibles Schema
  - Column Stores: Analytische Performance, feste Strukturen
  
- **OLTP vs. OLAP:**
  - OLTP: Transaktional, zeilenorientiert, viele kleine Updates
  - OLAP: Analytisch, spaltenorientiert, große Scans, wenige Writes
  
- **Hands-on-Demo (geplant):**
  - DuckDB-Wasm: Spaltenweise Aggregation auf CSV-Daten
  - Vergleich mit zeilenorientiertem Zugriff (z. B. SQLite)

---

## Aktivitäten (Geplant)

1. **Aktivierungsimpuls (5 Min):**
   - Frage: "Warum ist `SELECT AVG(price) FROM products` in DuckDB schneller als in SQLite?"
   - Hypothese sammeln, dann spaltenorientierte Speicherung erklären

2. **Live-Demo (15 Min):**
   - DuckDB-Wasm: CSV-Import, spaltenweise Aggregation
   - Vergleich mit zeilenorientiertem Scan

3. **Paradigmen-Matrix erweitern (10 Min):**
   - Achse hinzufügen: "Spalten vs. Zeilen", "OLTP vs. OLAP"
   - Einordnung: Wide Column (skalierbar, OLTP), Column Stores (Analytics, OLAP)

4. **Reflexion (5 Min):**
   - 1-Minute-Paper: "Wann würden Sie einen Column Store einem Wide Column Store vorziehen?"

---

## Referenzen & Quellen

- **Cassandra Documentation**: [https://cassandra.apache.org/doc/latest/](https://cassandra.apache.org/doc/latest/)
- **HBase Documentation**: [https://hbase.apache.org/](https://hbase.apache.org/)
- **DuckDB Documentation**: [https://duckdb.org/docs/](https://duckdb.org/docs/)
- **Apache Parquet**: [https://parquet.apache.org/](https://parquet.apache.org/)
- **Paper: "Column-Oriented Database Systems"** (Abadi et al., 2009)
- **Paradigmen-Matrix (laufend)**: `docs/paradigms-matrix.md`

---

## Offene Fragen / TODOs

- [ ] DuckDB-Wasm-Demo vorbereiten (CSV-Import, Aggregation)
- [ ] Vergleichstabelle: Wide Column vs. Column Stores
- [ ] Optional: Kompressionsverfahren visualisieren (RLE, Dictionary Encoding)
- [ ] Paradigmen-Matrix aktualisieren (Spalten vs. Zeilen, OLTP vs. OLAP)
