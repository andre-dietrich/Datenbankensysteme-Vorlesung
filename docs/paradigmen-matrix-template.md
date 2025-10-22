# Paradigmen-Vergleichsmatrix (Template)

> Zweck: Kontinuierliche Pflege nach ausgewählten Sessions. Dient als Reflexions- & Entscheidungswerkzeug.
>
> Nutzungsempfehlung: Initial in Session 2 (nach Einführung ACID/CAP) anlegen, dann Aktualisierung nach jeder 2. Session.

## Legende

- Bewertungs-Skala (qualitativ + Icons optional):
  - ++ (stark / sehr geeignet)
  - \+ (geeignet / solide)
  - o (neutral / situationsabhängig)
  - \− (eingeschränkt / Schwäche)
  - −− (deutlich ungeeignet / kritisches Defizit)
- Konsistenzmodelle Beispiele: stark, eventual, monotonic, causal (bei Bedarf erweitern)
- Performance-Charakteristik: Lese-/Schreib-lastig, analytisch, latenzkritisch, throughput-orientiert

## Kriterien (Anpassbar)

1. Datenmodell-Flexibilität
2. Schema-Evolution
3. Konsistenzmodell(e)
4. Transaktionsunterstützung (ACID-Qualität)
5. Abfrageausdrucksstärke
6. Join-/Relationsexpressivität
7. Performance-Profil (typisch)
8. Skalierungsansatz (vertikal/horizontal)
9. Indexierungsoptionen & Optimierer-Reife
10. Tooling & Ökosystem
11. Lernkurve für Einsteiger
12. Betriebskomplexität
13. Speicher-Effizienz (typisch)
14. Integritätsmechanismen (Constraints, Validation)
15. Reife für Analytics / BI
16. Reife für hochdynamische Web-Anwendungen
17. Zugriffsmuster-Eignung (CRUD vs. Graph Traversal vs. OLAP)
18. Sicherheit / Zugriffskontrolle

> Optional weitere Achsen: Replikation, Partitionierung, Reife für Event-Sourcing, Streaming-Eignung.

## Paradigmen (Platzhalter)

- Datei / Flat Files
- Key-Value Store (z. B. Redis)
- Object / Document Store (IndexedDB / PouchDB)
- Column Store (DuckDB)
- Relational (SQL / SQLite / PostgreSQL analog)
- Graph / RDF / SPARQL

## Matrix (Draft – ausfüllen & iterativ verfeinern)

| Kriterium                          | Datei           | KV                | Document         | Column                  | Relational          | Graph           |
| ---------------------------------- | --------------- | ----------------- | ---------------- | ----------------------- | ------------------- | --------------- |
| 1. Datenmodell-Flexibilität        | +               | o                 | ++               | −                       | o                   | +               |
| 2. Schema-Evolution                | +               | o                 | ++               | o                       | −                   | +               |
| 3. Konsistenzmodell(e)             | o               | eventual (konfig) | eventual         | o                       | stark               | variabel        |
| 4. Transaktionsunterstützung       | −               | o (Atomic Key)    | o                | o                       | ++                  | o               |
| 5. Abfrageausdrucksstärke          | −               | −                 | +                | +                       | ++                  | +               |
| 6. Join-/Relationsexpressivität    | −               | −                 | o (Embedding)    | −                       | ++                  | +               |
| 7. Performance-Profil (typisch)    | I/O-bound       | Speicher          | Lese-orientiert  | Analyse-optimiert       | gemischt            | Traversal       |
| 8. Skalierungsansatz               | manuell         | horizontal        | horizontal       | lokal/spalten-optimiert | vertikal + Sharding | horizontal      |
| 9. Indexierungs-/Optimierer-Reife  | −               | + (Key)           | o                | +                       | ++                  | o               |
| 10. Tooling & Ökosystem            | + (Einfachheit) | ++                | +                | +                       | ++                  | o               |
| 11. Lernkurve                      | ++              | +                 | +                | o                       | o                   | −               |
| 12. Betriebskomplexität            | +               | o                 | o                | +                       | o                   | −               |
| 13. Speicher-Effizienz             | o               | +                 | o                | ++                      | +                   | o               |
| 14. Integritätsmechanismen         | −               | −                 | o                | o                       | ++                  | o               |
| 15. Analytics / BI                 | −               | −                 | o                | ++                      | +                   | o               |
| 16. Dynamische Web-Apps            | o               | ++ (Cache)        | ++               | o                       | +                   | o               |
| 17. Zugriffsmuster-Eignung         | einfach         | Key Lookup        | Flexible Queries | Aggregation/Analytics   | Relational Abfragen | Graph Traversal |
| 18. Sicherheit / Zugriffskontrolle | manuell         | basic             | o                | o                       | ++                  | o               |

> Hinweis: Tabelle ist initial bewusst grob; jede Bewertung sollte im Verlauf durch Beispiele / Gegenbeispiele oder Messungen (Microbenchmarks, Abfragen) abgestützt werden.

## Änderungsverlauf (Changelog)

| Session | Änderung                                                | Begründung                      |
| ------- | ------------------------------------------------------- | ------------------------------- |
| S2      | Initial angelegt                                        | Einführung Vergleichsachsen     |
| S4      | Feinjustierung Document vs. Relational bei Flexibilität | Beispiel: JSON Schema Evolution |
| ...     | ...                                                     | ...                             |

## Reflexionsfragen (Beispiele)

- Welches Paradigma hat sich im Laufe der letzten zwei Sessions verbessert (Neubewertung) – warum?
- Welche Achse ist für unser Mini-Projekt aktuell kritisch? Müssen wir eine Neubewertung vornehmen?
- Gibt es Divergenzen zwischen theoretischer Bewertung und praktischer Erfahrung (Hands-on)?

## Nächste Schritte

- Ergänzung um konkrete Beispiele (Query-Snippets)
- Messpunkte definieren (z. B. Response-Zeit mit/ohne Index)
- Erweiterung um Replikation / Partitionierung bei Bedarf
