# Session 19 (Lecture)

## Titel

Session 19 – Verteiltheit: Replikation, Sharding, Konsistenz (Lecture)

## Zusammenfassung

Master-Replica, Partitioning, Eventual Consistency. Grundlagen verteilter Datenbanksysteme und deren Konsistenzmodelle.

## Inhalte

- Motivation Verteilung:
  - Skalierung (Horizontal Scaling)
  - Verfügbarkeit (High Availability)
  - Geographische Verteilung (Latency)
- Replikation:
  - **Master-Replica** (Single Writer, Multiple Readers)
  - **Multi-Master** (Konfliktauflösung nötig)
  - Synchrone vs. Asynchrone Replikation
  - Lag & Eventual Consistency
- Sharding (Partitioning):
  - Horizontal Partitioning über mehrere Nodes
  - Sharding Strategies: Range, Hash, Geographic
  - Shard Key Design (Hot Spots vermeiden)
  - Cross-Shard Queries (teuer)
- Konsistenzmodelle:
  - **Strong Consistency**: Linearisierbarkeit
  - **Eventual Consistency**: Konvergenz über Zeit
  - **Causal Consistency**: Kausalität erhalten
  - **Read-Your-Writes**, **Monotonic Reads**

## Aktivitäten

- Szenario: Globales System → Replikation/Sharding Design
- Diskussion: Wann Strong vs. Eventual Consistency?
- Übung: Sharding Strategy für User-DB entwerfen

## Referenzen & Quellen

- "Designing Data-Intensive Applications" (Kleppmann) - Replication & Partitioning Chapters
- Consistency Models Overview
- MongoDB Sharding Documentation
