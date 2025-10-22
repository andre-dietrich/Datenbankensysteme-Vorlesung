# Session 18 (Lecture)

## Titel

Session 18 – Polyglot Persistence & Architektur-Patterns (Lecture)

## Zusammenfassung

CQRS, Event Sourcing, Data Lake, Integrationsstrategien. Kombination verschiedener Datenbankparadigmen in einer Gesamtarchitektur.

## Inhalte

- Polyglot Persistence Konzept:
  - Verschiedene DBs für verschiedene Use Cases
  - Transactional (Relational) + Caching (KV) + Analytics (Column) + Relationships (Graph)
- Architektur-Patterns:
  - **CQRS** (Command Query Responsibility Segregation): Trennung Write/Read Models
  - **Event Sourcing**: Ereignisse als Single Source of Truth
  - **Data Lake**: Zentrale Ablage für Raw Data + Pipelines
  - **Lambda Architecture**: Batch + Streaming Layer
- Integration:
  - Change Data Capture (CDC)
  - ETL/ELT Pipelines
  - API-basierte Sync
- Trade-offs:
  - Komplexität vs. Spezialisierung
  - Eventual Consistency zwischen Systemen
  - Operational Overhead

## Aktivitäten

- Szenario: E-Commerce System → Polyglot Design
- Diskussion: Wann lohnt sich Polyglot vs. Single DB?
- Gruppenarbeit: Integration Pattern skizzieren

## Referenzen & Quellen

- "NoSQL Distilled" (Fowler & Sadalage) - Polyglot Persistence Chapter
- CQRS & Event Sourcing (Martin Fowler)
- Debezium (CDC Tool) Documentation
