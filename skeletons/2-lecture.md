# Session 2 (Lecture)

## Titel

Session 2 – Key-Value Stores (kompakt) (Lecture)

## Zusammenfassung

Zugriff, Patterns, TTL, Atomic Keys, Grenzen (keine Range Queries). Kompakter Überblick über Key-Value Paradigma: Grundkonzepte, typische Patterns und Limitierungen.

## Inhalte

- Key-Value Grundprinzip: O(1) Lookup
- Zugriffsmuster: GET, SET, DELETE, EXISTS
- TTL (Time-To-Live) & Expiration
- Atomic Operations: INCR, DECR, CAS (Compare-And-Set)
- Key-Design Patterns: Namespacing, Composite Keys
- Typische Use Cases: Session Store, Caching, Rate Limiting
- Grenzen: Keine Range Queries, keine Joins, eingeschränkte Ad-hoc Analysen
- Beispiel-Systeme: Redis, Memcached, LocalStorage/IndexedDB (Browser)

## Aktivitäten

- Mini-Demo: Redis/LocalStorage Live-Zugriff
- Diskussion: Für welche Szenarien ist KV optimal/ungeeignet?
- Pattern-Katalog Übersicht

## Referenzen & Quellen

- Redis Documentation (Commands Overview)
- LocalStorage / IndexedDB Web APIs
- Caching Patterns (Martin Fowler, Cache-Aside)
