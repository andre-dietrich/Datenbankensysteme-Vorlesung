# Session 12 – Indexe & Performance (Lecture)

> **Professor-Persona:** Praxisorientierter Architekt mit Analyse-Coach-Elementen  
> **Stil:** Klar & Praxisfokussiert + Analytisch Reflexiv  
> **Didaktik:** Live-Demos, Performance-Experimente, Explain-Plan Screenshots

## Zusammenfassung

In dieser Session erkunden wir **Indexe als zentrales Werkzeug zur Performanceoptimierung**. Nach L11 (MCP Tutorial) haben Sie gesehen, wie KI SQL generiert – aber sind diese Queries auch effizient? Hier lernen Sie, Performance zu messen, zu verstehen und zu optimieren.

Wir arbeiten mit der **IMDB-Datenbank aus L11** und führen praktische Performance-Experimente durch: Queries mit und ohne Index, Analyse mit EXPLAIN, Messung von Ausführungszeiten.

**Bezug zur Agenda:**
- Aufbauend auf L11 (MCP): "Die KI schreibt SQL – Sie optimieren die Performance"
- Vorbereitung auf L13 (Advanced SQL): Komplexe Queries brauchen gute Indexe
- Didaktisches Konzept: Hands-on Performance-Experimente (Index an/aus)

## Inhalte

### 1. Motivation: Warum Performance wichtig ist
- Problem-Szenario aus L11: Query auf 178k+ Titeln
- Demo: Gleiche Query mit/ohne Index
- Zeitvergleich live zeigen

### 2. Was sind Indexe?
- Metapher: "Buchindex für Datenbanken"
- B-Baum-Struktur (vereinfacht visualisiert)
- Trade-offs: Schnelleres Lesen vs. langsameres Schreiben
- Typen: Single-Column, Composite, Unique, Full-Text

### 3. Hands-on: Index erstellen & Performance messen
- Experiment 1: Index auf `averageRating`
- Experiment 2: Composite Index auf `startYear` + `genres`
- Messung mit EXPLAIN ANALYZE
- Query Plan vorher/nachher vergleichen

### 4. EXPLAIN & EXPLAIN ANALYZE
- Tool-Einführung: Query Plans lesen
- Seq Scan vs. Index Scan
- Nested Loop vs. Hash Join
- Actual Time vs. Estimated Rows

### 5. Wann Indexe NICHT helfen
- Kleine Tabellen (< 1000 Zeilen)
- Hohe Write-Last
- Low Selectivity (z.B. `gender`: M/F)
- Funktionen in WHERE-Klauseln

### 6. Best Practices & Strategien
- Analysiere erst, optimiere dann
- Index auf häufig gefilterte Spalten
- Composite Indexe richtig nutzen
- Redundante Indexe vermeiden
- Monitoring & Wartung

## Aktivitäten

- **Aktivität 1:** Performance-Experiment (15 Min) – Query aus L11 mit/ohne Index
- **Aktivität 2:** Query Plan lesen (10 Min) – Bottlenecks identifizieren
- **Aktivität 3:** Trade-off Diskussion (5 Min) – E-Commerce-Szenario

## Referenzen & Quellen

- SQLite Index Documentation
- PostgreSQL: Using EXPLAIN
- Use The Index, Luke! – https://use-the-index-luke.com
- B-Tree Visualisierung
- IMDB-Datenbank (6MB, 10MB, 40MB) aus L11
