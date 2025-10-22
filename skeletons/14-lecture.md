# Session 12 (Lecture)

## Titel

Session 12 – Indexe: B-Trees, Hash, Bitmap (Lecture)

## Zusammenfassung

Indexstrukturen, Kosten, Covering Indexes. Mechanismen zur Beschleunigung von Abfragen durch zusätzliche Datenstrukturen.

## Inhalte

- Warum Indexe? Sequential Scan vs. Index Scan
- Index-Typen:
  - **B-Tree**: Sortierte Struktur, Range Queries
  - **Hash Index**: O(1) Equality Lookups, keine Ranges
  - **Bitmap Index**: Niedrige Kardinalität (z. B. Status-Felder)
  - Volltext-Index (Erwähnung)
- Covering Index: Alle benötigten Spalten im Index
- Composite Index: Multi-Column Indexes, Spaltenreihenfolge wichtig
- Index-Overhead:
  - Speicherplatz
  - INSERT/UPDATE/DELETE Performance
- Wann Indexe sinnvoll sind (Selektivität, Query Patterns)

## Aktivitäten

- Live-Demo: Query mit/ohne Index (EXPLAIN Output vergleichen)
- Übung: Gegeben Query → passenden Index entwerfen
- Diskussion: Wann zu viele Indexe schaden

## Referenzen & Quellen

- "Use The Index, Luke!" (Markus Winand)
- PostgreSQL Index Types Documentation
- B-Tree Visualization Tools
