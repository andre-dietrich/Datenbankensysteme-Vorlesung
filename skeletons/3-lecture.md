# Session 3 (Lecture)

## Titel

Session 3 – Document Stores (kompakt) (Lecture)

## Zusammenfassung

JSON Persistenz, Schema-Evolution, Sync & Konflikte. Kompakter Überblick über Document Stores: Flexible Strukturen, Validierung und Offline-Synchronisation.

## Inhalte

### Block 1: Document Store Grundlagen (15 Min)

- Document Store Grundprinzip: JSON/BSON Persistenz
- Flexible Schemas vs. Schema Validation (JSON Schema)
- Verschachtelte Strukturen & Denormalisierung vs. Relational
- PouchDB: Browser-native Document DB (Setup & Basics)

### Block 2: Komplexe Suchanfragen mit Mango-Queries (25 Min)

- **Mango Query Language Grundlagen** (PouchDB Find Plugin)
  - Selektoren: `$eq`, `$gt`, `$lt`, `$gte`, `$lte`, `$in`, `$nin`
  - Logische Operatoren: `$and`, `$or`, `$not`, `$nor`
  - Verschachtelte Felder durchsuchen: `"user.profile.age": {$gt: 18}`
  - Array-Operatoren: `$elemMatch`, `$size`, `$all`
- **Komplexe Query-Beispiele**
  - Multi-Kriterien-Suche (Produktfilter: Preis + Kategorie + Rating)
  - Verschachtelte Objekte & Arrays kombinieren
  - Sortierung & Limitierung (`sort`, `limit`, `skip`)

### Block 3: Index-Strategien für Performance (15 Min)

- **Warum Indexe?** Full-Table-Scan vs. Index-Lookup
- **PouchDB Index-Erstellung**: `createIndex()` Syntax
  - Einfache Indexe (einzelnes Feld)
  - Composite Indexe (mehrere Felder)
  - Index-Planung: Welche Felder indexieren?
- **Live-Performance-Demo**:
  - Gleiche Mango-Query mit/ohne Index
  - Zeitmessung & Explain (wo verfügbar)
  - Best Practices: Index vor Query erstellen

### Block 4: Schema-Evolution & Versionierung (10 Min)

- Schema-Evolution: Versionierung, Migration Patterns
- Umgang mit Legacy-Dokumenten (v1, v2, v3)
- Validator-Patterns (optional bei PouchDB)

### Block 5: Offline-First & Synchronisation (15 Min)

- Offline-First Architektur (PouchDB/CouchDB Konzept)
- Bidirektionale Sync: `sync()`, `replicate.to()`, `replicate.from()`
- Konfliktauflösung: Last-Write-Wins, Revision Trees, Custom Merge
- Live-Demo: Zwei Browser-Tabs synchronisieren

### Block 6: Use Cases & Abgrenzung (10 Min)

- Typische Use Cases: Content Management, User Profiles, Mobile Apps, Offline-Apps
- Wann Document Store? Wann Relational? (Entscheidungsmatrix)
- Beispiel-Systeme: MongoDB, CouchDB, PouchDB, IndexedDB

## Aktivitäten

- **Aktivierung (5 Min)**: Mini-Demo PouchDB im Browser (DevTools Inspektion)
- **Hands-on Mango-Queries (20 Min)**: Live-Coding mit steigender Komplexität
  - Einfache Selektoren → Logische Operatoren → Verschachtelte Felder → Arrays
- **Performance-Experiment (10 Min)**: Gleiche Query mit/ohne Index + Zeitmessung
- **Sync-Demo (10 Min)**: Zwei Browser-Tabs live synchronisieren (PouchDB ↔ PouchDB)
- **Szenario-Diskussion (10 Min)**: Konfliktauflösung bei Offline-Sync
- **Schema-Evolution Beispiel (5 Min)**: v1 → v2 Migration Pattern
- **Reflexion (5 Min)**: 1-Minute-Paper: "Wann Document Store statt Relational?"

## Referenzen & Quellen

- **PouchDB Official Docs**: https://pouchdb.com/guides/
- **PouchDB Find Plugin**: https://pouchdb.com/guides/mango-queries.html
- **Mango Query Language Reference**: https://docs.couchdb.org/en/stable/api/database/find.html
- **CouchDB Replication Protocol**: https://docs.couchdb.org/en/stable/replication/protocol.html
- **JSON Schema Specification**: https://json-schema.org/
- **IndexedDB API (Browser)**: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- **MongoDB Query Language** (Vergleich): https://www.mongodb.com/docs/manual/tutorial/query-documents/
