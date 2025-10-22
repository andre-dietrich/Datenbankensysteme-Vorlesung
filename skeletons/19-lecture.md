# Session 17 (Lecture)

## Titel

Session 17 – Graph Databases (kompakt) (Lecture)

## Zusammenfassung

Property Graph, Traversal, Pattern Matching vs. Joins. Kompakter Überblick über Graph-Datenbanken für Beziehungsmodellierung.

## Inhalte

- Graph-Modell Grundlagen:
  - Knoten (Nodes) & Kanten (Edges/Relationships)
  - Property Graph: Knoten und Kanten mit Properties
  - vs. RDF (Triples: Subject-Predicate-Object)
- Use Cases:
  - Social Networks (Freundschaften, Follower)
  - Recommendation Engines
  - Knowledge Graphs
  - Network Analysis, Fraud Detection
- Traversal vs. Joins:
  - Rekursive CTEs in SQL (Vergleich)
  - Graph-spezifische Query Languages: Cypher (Neo4j), Gremlin
- Pattern Matching:
  - Pfadsuche (Shortest Path, All Paths)
  - Nachbarschaftsabfragen (1-Hop, N-Hop)
- Grenzen: Nicht für alle Datenmodelle geeignet (Aggregationen schwächer)

## Aktivitäten

- Mini-Demo: Cypher Query (Neo4j Browser oder Beispiel)
- Diskussion: Wann Graph besser als Relational?
- Vergleich: Rekursive SQL CTE vs. Graph Traversal

## Referenzen & Quellen

- Neo4j Cypher Documentation
- "Graph Databases" (Robinson et al., O'Reilly)
- Property Graph vs. RDF Comparison
