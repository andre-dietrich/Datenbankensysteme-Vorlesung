# Lecture Didactics & Style

> Draft Version (v0.1) – basiert auf Outline & Abstimmungen. Stellen mit *[Optional / Erweiterung]* können später verfeinert werden.

## Bezug zur Outline

- Titel: "Databases Unlocked: A Beginner's Journey"
- Zielgruppe: Bachelor Informatik (3.–5. Semester)
- Zeitaufwand (aus Outline):
   - Vorlesungen: 22 × 90 Min
   - Übungen: 7 × 90 Min
   - Selbststudium: 20–40 Min / Woche
- Lernziele (gekürzt paraphrasiert):
   1. Paradigmen & Einsatzszenarien verstehen (File, KV, Object, Column, Relational, Graph)
   2. Relationale DB & SQL praktisch anwenden (Modellierung, Normalisierung, DML/DDL, Integrität, Transaktionen)
   3. Praktische Erfahrung mit Browser-basierten DB-Engines sammeln
   4. Kernkonzepte (ACID, Konsistenz, Transaktionen, Verteiltheit) analysieren & vergleichen
   5. Stärken/Schwächen bewerten und auf Anwendungskontexte übertragen

---
 
## Didaktisches Konzept

Hybrid-Modell: "Spiral & Praxis-First" (Basis) + 20–30% analytisch-vergleichende Phasen + selektive projektgestützte Artefakte.

### Leitprinzipien

1. Frühzeitige Konzeptachsen: ACID, CAP, Konsistenzmodelle, Datenmodell-Flexibilität werden in Woche 1/2 eingeführt als wiederkehrende Vergleichsfolie.
2. Jede Session beginnt mit einem Aktivierungsimpuls:
   - Mini-Demo (z. B. Query in DuckDB-Wasm / IndexedDB-Inspektor)
   - oder Kurze Hypothese: "Welche Paradigmen wären für X ungeeignet – warum?"  
3. Theoretische Blöcke sind maximal ~15 Minuten ohne Interaktion.
4. Progressive Vertiefung (Spirale): Ein Thema (z. B. Indexe) taucht zuerst intuitiv (Warum schneller?), später formal (B-Baum, Kosten), ggf. optional intern (Speicherlayout) *[Optional / Erweiterung]*.
5. Vergleichsschleifen: Alle 2–3 Sessions Pflege einer "Paradigmen-Matrix" (Kriterien: Modellierung, Konsistenz, Abfrageausdruck, Performanceprofil, Betrieb, Tool-Reife).
6. Mini-Projekt-Meilensteine (4 Checkpoints):
   - M1: Rohdaten + einfache persistente Speicherung (File/KV)
   - M2: Relationales Redesign + Normalisierung
   - M3: Performance & Index + Explain Plan
   - M4: Erweiterung mit Graph-Aspekt (z. B. Beziehungsanalyse)
7. Reflexionsformate:
   - 1-Minute-Paper: "Was ist heute klarer geworden?"
   - Entscheidungsfrage: "Welche 2 Paradigmen schließen wir für Use-Case Y aus? Mit Begründung."
8. Übungen: Hands-on Querying, Modellierungs-Canvas, Performance-Experimente (Index an/aus, Joins), JSON vs. Relational Mapping.
9. Didaktische Reduktion: Komplexe Themen wie Isolation Levels werden szenariobasiert eingeführt ("Ticketbuchung"), formale Tabelle folgt erst nach Szenario.

### Lernphasen (Makro)

| Phase | Fokus | Typische Dauer | Beispiel |
|-------|-------|----------------|----------|
| Aktivierung | Relevanz & Problem | 5 Min | Demo: Unstrukturierte CSV-Abfrage vs. strukturiertes Schema |
| Exploration | Erste Hands-on/Beobachtung | 10–15 Min | Browser-SQL vs. KV Lookup |
| Konzeptualisierung | Begriffe & Modelle | 15 Min | ACID, CAP Achsendefinition |
| Vertiefung/Transfer | Vergleich & Anwendung | 15–20 Min | Normalisierung alt vs. neu |
| Reflexion | Metakognition | 5 Min | 1-Minute-Paper |

---
 
## Professor-Persona

"Praxisorientierter Architekt mit Analyse-Coach-Elementen"

| Aspekt | Beschreibung |
|--------|--------------|
| Hintergrund | >10 Jahre Backend/Data Eng. + Performance & Modellierungserfahrung |
| Rolle | Übersetzt Theorie direkt in funktionierende Minimalbeispiele |
| Haltung | Offen, reflektierend, lädt zu Hypothesen ein |
| Signature Moves | 2-Minuten-Demo Start; Bewertungsmatrix am Ende von Blöcken |
| Interaktion | Sokratische Fragen: "Was passiert, wenn... ?" |
| Werkzeugstil | Live-Coding, Explain-Plan Screenshots, tabellarische Gegenüberstellungen |

---
 
## Stil & Schwierigkeitsgrad

- Stil-Hybrid: Klar & Praxisfokussiert (Basis) + Analytisch Reflexiv (ca. 25%) + Explorativ Iterativ (ca. 15%).
- Sprachstil: Präzise, anschauliche Metaphern ("Transaktion = Paket mit Garantiesiegel"), vermeidet unnötige Modebegriffe.
- Visualisierung: Vergleichstabellen, vereinfachte Diagramme, farbcodierte Konsistenzachsen.
- Schwierigkeitsgrad: Mittel-Fortgeschritten (C) – mit klar markierten Optional-Blöcken ("Deep Dive: Locking vs. MVCC").
- Frühe Einführung: ACID, CAP, Konsistenzkategorien (stark, eventual, monotonic) als wiederkehrende Beobachtungs-Brille.

### Umgang mit Komplexität

- Layering: "Was" → "Wie" → "Warum jetzt / Wann nicht".
- Kognitive Entlastung: Einheitliche Struktur pro Paradigma.
- Optional-Kennzeichnung: [Advanced], [Deep Dive], [Internals].

---
 
## Kursart

Mischform: Einführung + Vergleichsmatrix + leichte Projektstützung.

| Element | Umsetzung |
|---------|-----------|
| Grundstruktur | Einführungsveranstaltung mit klarer Progression von einfach zu komplex |
| Vergleich | Regelmäßige Paradigmen-Matrix Pflege |
| Projekt | 4 definierte Meilensteine (siehe oben) |
| Bewertung (Vorschlag) *[Optional]* | 40% Übungen/Abgaben, 30% Projekt-Artefakte, 30% Abschlussreflexion/Kurztest |
| Transparenz | Übersichtsdokument mit aktueller Matrix nach jeder zweiten Session |

---
 
## Didaktische Methoden (Auswahl)

- Live-Coding & Inline-Queries (DuckDB-Wasm, SQLite-Wasm)
- Performance-Microbenchmarks (Index vs. kein Index)
- Modellierungsvergleich: ERD vs. JSON Schema vs. Graph Knoten/Kanten
- Entscheidungsraster: "Wenn Anforderung X hoch → bevorzugtes Paradigma?"
- Fehlersimulation: Dirty Reads / Lost Updates (szenariobasiert)
- Refactoring-Schritte dokumentiert (Git Branch Naming: `m1_raw`, `m2_relational`, `m3_index_perf`, `m4_graph_extend`)

---
 
## Bewertung der Lernziele (Alignment-Map)

| Lernziel | Hauptmethoden | Evidenz | Wiederkehrende Achse |
|----------|---------------|--------|-----------------------|
| 1 | Aktivierungsdemos + Paradigmen-Matrix | Vergleichsprotokolle | Flexibilität, Konsistenz |
| 2 | Live-Coding SQL + Übungen | Query-Lösungen, Normalisierung | Integrität, Transaktionen |
| 3 | Browser-Engines Hands-on | Abgabe-Screens / Artefakte | Praktikabilität |
| 4 | CAP/ACID Reflexion + Szenarien | Mini-Essays | Konsistenzdimension |
| 5 | Bewertungsmatrix + Projekt | Begründete Auswahl | Trade-offs |

---
 
## Risiken & Mitigation

| Risiko | Beschreibung | Strategie |
|--------|--------------|-----------|
| Überfrachtung früher Begriffe | CAP + ACID + Konsistenz zu früh überfordernd | Minimal intuitive Einführung + spätere Formalisierung |
| Tool-Ablenkung | Fokus driftet zu Tool-spezifischen Details | Prinzipien vor Syntax priorisieren |
| Zeitdruck in Übungen | Query/Index Tests dauern zu lange | Vorbereitete Datensätze + Skriptfragmente |
| Heterogene Vorkenntnisse | Unterschiedliche SQL-Erfahrung | Differenzierte Aufgaben: Basis / Stretch |
| Projekt-Scope creep | Mini-Projekt wächst unkontrolliert | Fixe Meilensteine + Abbruchkriterien |

---
 
## Iterative Verbesserung

- Nach Session 2: Erste Feedback-Umfrage (Tempo, Tooling Klarheit)
- Nach Meilenstein 2: Anpassung Tiefe Performance-Themen
- Vor Abschluss: Matrix-Vergleich Session 1 vs. vorletzte Session reflektieren lassen

---
 
## Offene Punkte / Platzhalter

- Feinplanung Session-Zuordnung der Meilensteine *[Pending]*
- Konkrete Bewertungsrubriken für Projekt *[Pending]*
- Ausformulierte Paradigmen-Matrix Template *[TODO]*

---
*Ende Draft – Bitte Rückmeldung: Änderungen? Ergänzungen? Wenn ok → Finalisierung / Agenda-Erstellung als nächster Schritt.*
