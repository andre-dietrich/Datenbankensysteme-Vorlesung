<!--
language: de
narrator: German Male
-->

import: https://raw.githubusercontent.com/liaTemplates/PyScript/main/README.md
        https://raw.githubusercontent.com/LiaScript/CodeRunner/master/README.md

# Vergleichsachsen & Paradigmen-Matrix v1

    --{{0}}--
Willkommen zu einer der wichtigsten Sessions dieses Kurses! Heute entwickeln wir gemeinsam ein Werkzeug, das Sie durch die gesamte Vorlesung begleiten wird: die Paradigmen-Matrix. Kein Auswendiglernen von Features, keine Vendor-Propaganda – sondern ein systematisches Framework zur begründeten Technologie-Bewertung.

    {{0-1}}
<section>

**Rückblick Sessions 1–2:**

> - **Session 1:** Rohdatenformate (CSV, JSON, YAML, XML) – flexibel, aber ineffizient
> - **Session 2:** Übergang zu Keyed Access – O(1) Zugriff, aber mit Limitierungen

**Die zentrale Frage heute:**

> Wie bewerten wir Speicherparadigmen **systematisch** statt intuitiv?

</section>

    --{{1}}--
Wenn Sie technische Diskussionen verfolgen, hören Sie oft Aussagen wie "MongoDB ist webscale" oder "PostgreSQL ist langsam". Solche Pauschalurteile sind wertlos. Was bedeutet "webscale"? Langsam für welche Workload? Wir brauchen ein analytisches Raster, das uns zwingt, präzise zu denken. Genau das bauen wir heute: Fünf Achsen, die jedes Paradigma entlang messbarer Dimensionen einordnen. Diese Matrix ist explizit vorläufig – wir werden sie in L6, L9, L12, L16, L18 und L21 aktualisieren, wenn unser Verständnis wächst.

    {{1}}
<section>

## 🎯 Lernziele dieser Session

Nach dieser Session können Sie:

1. **Die fünf Vergleichsachsen** benennen und deren Bewertungskriterien erklären
2. **Paradigmen-Matrix v1** interpretieren und Ratings begründen
3. **Hypothesen für spätere Paradigmen** formulieren (KV, Document, Column, Relational, Graph)
4. **Trade-offs explizit machen** statt implizite Annahmen zu verwenden

</section>

---

## Die fünf Vergleichsachsen: Konzept

    --{{0}}--
Unser Framework basiert auf fünf fundamentalen Dimensionen, die jedes Speichersystem charakterisieren. Wichtig: Diese Achsen sind nicht binär ("gut" vs. "schlecht"), sondern beschreiben Trade-offs. Ein System kann auf einer Achse stark sein und auf einer anderen schwach – und das ist völlig legitim, wenn es zur Anwendung passt.

    {{0-1}}
<section>

### Achse 1: Strukturgrad

**Was misst diese Achse?**

> Wie rigide ist das Datenmodell? Wieviel Flexibilität vs. Ordnung bietet das System?

**Spektrum:**

```ascii
Flexibel                                              Rigide
├────────────────┼────────────────┼────────────────┤
Schemalos        Schema-optional  Schema-erzwungen
(JSON, KV)       (Document Stores) (Relational)
```

**Bewertungskriterien:**

- **Flexibel (1–3):** Keine vordefinierten Strukturen, jeder Datensatz kann unterschiedlich sein
- **Mittel (4–6):** Validierung möglich, aber optional oder nachträglich definierbar
- **Rigide (7–10):** Schema muss vor Datenerfassung existieren, Änderungen sind aufwändig

**Trade-off:**

- ⬆️ Flexibilität → schnelle Iteration, einfache Schema-Evolution
- ⬇️ Rigidität → weniger Fehler, explizite Kontrakte, bessere Tooling-Unterstützung

</section>

    --{{1}}--
Flexibilität ist nicht automatisch besser. Ein flexibles Schema ermöglicht schnelle Prototypen und agile Entwicklung – aber ohne Constraints riskieren Sie Inkonsistenzen. Ein rigides Schema erzwingt Disziplin und Dokumentation – aber erschwert Änderungen. Die richtige Wahl hängt vom Kontext ab: Exploratives Data Science profitiert von Flexibilität, Banktransaktionen brauchen Rigidität.

    {{1-2}}
<section>

### Achse 2: Integrität

**Was misst diese Achse?**

> Welche Konsistenzgarantien gibt das System? Wie werden Constraints durchgesetzt?

**Spektrum:**

```ascii
Keine Garantien                                    Starke Garantien
├────────────────┼────────────────┼────────────────┤
Best Effort      Eventual         ACID
(Flat Files)     (NoSQL)          (Relational)
```

**Bewertungskriterien:**

- **Schwach (1–3):** Keine automatische Validierung, Anwendung verantwortlich
- **Mittel (4–6):** Eventual Consistency, optimistische Locks, Validierungsregeln
- **Stark (7–10):** ACID-Transaktionen, referentielle Integrität, Constraints

**Trade-off:**

- ⬆️ Flexibilität → höhere Performance, bessere Skalierung
- ⬇️ Garantien → komplexere Anwendungslogik, mögliche Inkonsistenzen

</section>

    --{{2}}--
Hier wird es philosophisch: Brauchen Sie Garantien vom System oder von Ihrer Anwendung? Relationale Datenbanken sagen: "Wir garantieren Konsistenz, koste es was es wolle." NoSQL-Systeme sagen: "Konsistenz ist teuer, wir geben Ihnen Geschwindigkeit und Verfügbarkeit." Das ist kein Bug, sondern Feature – es reflektiert das CAP-Theorem, das wir in L22 formalisieren. Für jetzt: Integrität kostet Performance, aber verhindert Fehler.

    {{2}}
<section>

### Achse 3: Konfliktpotenzial

**Was misst diese Achse?**

> Was passiert bei konkurrierenden Zugriffen? Wie robust ist das System gegen Race Conditions?

**Spektrum:**

```ascii
Hohe Konflikte                                     Niedrige Konflikte
├────────────────┼────────────────┼────────────────┤
Manuell          Optimistisch     Pessimistisch
(Files, KV)      (Document)       (Relational)
```

**Bewertungskriterien:**

- **Hoch (1–3):** Keine automatische Konfliktbehandlung, Lost Updates möglich
- **Mittel (4–6):** Versionierung, Eventual Consistency, manuelle Konfliktauflösung
- **Niedrig (7–10):** Transaktionale Isolation, Locking, serialisierbare Ausführung

**Trade-off:**

- ⬆️ Konfliktrisiko → einfachere Implementierung, bessere Parallelität
- ⬇️ Konfliktrisiko → komplexere Mechanismen, potenzielle Bottlenecks

</section>

    --{{3}}--
Konkurrenz ist die Achillesferse verteilter Systeme. Wenn zwei Nutzer gleichzeitig denselben Datensatz ändern – wer gewinnt? Last-Write-Wins ist simpel, aber Daten gehen verloren. Pessimistische Locks sind sicher, aber blockieren. Optimistische Locks sind performant, aber erfordern Retry-Logik. Kein System kann alle Konflikte magisch lösen – sie verschieben nur, wer die Komplexität trägt: das System oder Ihre Anwendung.

    {{3}}
<section>

### Achse 4: Ausdrucksstärke

**Was misst diese Achse?**

> Wie mächtig sind die Abfragesprachen? Welche Operationen sind effizient möglich?

**Spektrum:**

```ascii
Eingeschränkt                                      Mächtig
├────────────────┼────────────────┼────────────────┤
Key Lookup       Indizes + Filter SQL + Joins
(KV)             (Document)       (Relational)
```

**Bewertungskriterien:**

- **Schwach (1–3):** Nur exakte Schlüssel-Zugriffe, Full Scan für Filter
- **Mittel (4–6):** Sekundäre Indizes, einfache Filter, eingeschränkte Joins
- **Stark (7–10):** Deklarative Sprachen (SQL, SPARQL), komplexe Joins, Aggregationen

**Trade-off:**

- ⬆️ Einfachheit → vorhersehbare Performance, klare Semantik
- ⬇️ Ausdrucksstärke → flexible Ad-hoc Queries, weniger Anwendungslogik

</section>

    --{{4}}--
Diese Achse trennt Speicher-APIs von Abfragesprachen. Key-Value Stores sind brillant für Punkt-Zugriffe, aber hilflos bei "Finde alle X mit Eigenschaft Y". SQL ist mächtig für komplexe Analysen, aber Overhead für simple Lookups. Die Frage ist: Wo wollen Sie Komplexität handhaben? Im Speichersystem (mächtige Query-Engine) oder in Ihrer Anwendung (manuelle Filterung)?

    {{4}}
<section>

### Achse 5: Performanceprofil

**Was misst diese Achse?**

> Wo liegen die Stärken/Schwächen? Für welche Workloads ist das System optimiert?

**Dimensionen (nicht linear!):**

- **Punkt-Abfragen** (Einzelner Datensatz per Schlüssel)
- **Range Queries** (Bereichsabfragen, z.B. "Preise 10–50€")
- **Aggregationen** (SUM, AVG, COUNT über viele Zeilen)
- **Schreibdurchsatz** (INSERT/UPDATE/DELETE Rate)
- **Skalierung** (Horizontal/Vertikal, Replikation)

**Bewertung:**

> **Keine Einzelzahl!** Stattdessen: Profil mit Stärken/Schwächen pro Workload.

**Trade-off:**

- Systeme optimieren für **bestimmte** Workloads – es gibt kein "bestes für alles"
- OLTP (Transaktionen) vs. OLAP (Analytics) erfordern gegensätzliche Optimierungen

</section>

---

## Paradigmen-Matrix v1: Initiale Bewertung

    --{{0}}--
Jetzt wird es konkret. Wir bewerten die Paradigmen, die wir bisher kennen – Flat Files (CSV/JSON) und konzeptionell Key-Value – entlang unserer fünf Achsen. Wichtig: Diese Ratings sind **explizit vorläufig**. Sie basieren auf unserem aktuellen Verständnis und werden sich ändern, wenn wir tiefer einsteigen.

    {{0-1}}
<section>

### Matrix v1: Flat Files & Key-Value (konzeptionell)

| Achse | Flat Files (CSV/JSON) | Key-Value (konzeptionell) | Begründung |
|-------|----------------------|---------------------------|------------|
| **1. Strukturgrad** | 2/10 (sehr flexibel) | 3/10 (flexibel) | CSV: Keine Typen. JSON: Schema optional. KV: Wert ist Blackbox |
| **2. Integrität** | 1/10 (keine) | 2/10 (minimal) | Keine Constraints, keine Transaktionen, keine Validierung |
| **3. Konfliktpotenzial** | 9/10 (sehr hoch) | 8/10 (hoch) | File-Locking primitiv. KV: Lost Updates ohne Atomic Operations |
| **4. Ausdrucksstärke** | 1/10 (keine) | 2/10 (minimal) | Files: Grep/Scan. KV: get/set/delete – keine Filter |
| **5. Performanceprofil** | Punkt: O(n), Range: O(n), Agg: O(n) | Punkt: O(1), Range: O(n), Agg: O(n) | KV brillant für Punkt-Zugriffe, schwach sonst |

**Status:** 🟡 Vorläufig – Update geplant nach L4 (Redis Details)

</section>

    --{{1}}--
Schauen Sie sich diese Tabelle genau an. Was fällt auf? Flat Files sind extrem flexibel, aber auf allen anderen Achsen schwach. Key-Value verbessert massiv die Punkt-Abfrage-Performance – aber nichts anderes. Das ist kein Versagen, sondern Design-Entscheidung. Key-Value Stores opfern bewusst Ausdrucksstärke für Geschwindigkeit. Die Frage ist: Passt das zu Ihrer Anwendung?

    {{1-2}}
<section>

### Visualisierung: Radar-Chart (konzeptionell)

```ascii
            Strukturgrad (10 = rigide)
                    |
                    2 (Flat)
                   /|\
                  / | \
                 /  |  \
    Integrität  1   |   9  Konfliktpotenzial
    (10 = stark)    |      (10 = niedrig)
                    |
         Performance-Profil
         (komplex, siehe Text)
```

**Interpretation:**

- **Kleine Fläche** = spezialisiertes System
- **Große Fläche** = vielseitiges System (aber evtl. "Master of None")
- **Unbalanciert** = klare Stärken/Schwächen

> Flat Files: Winzige Fläche – nur für simple Szenarien geeignet.

</section>

    --{{2}}--
Ein häufiger Denkfehler: "Mehr ist besser". Nein! Ein System mit maximalen Werten auf allen Achsen wäre komplex, langsam und schwer zu betreiben. Redis ist erfolgreich, weil es bewusst einfach bleibt. PostgreSQL ist mächtig, weil es Komplexität akzeptiert. Die Matrix zeigt: Jedes System macht Trade-offs. Ihre Aufgabe ist, die Trade-offs zu erkennen und mit Ihren Anforderungen abzugleichen.

    {{2}}
<section>

### Hypothesen für kommende Paradigmen

**Noch nicht behandelt, aber wir können spekulieren:**

| Paradigma | Hypothese | Zu klären in Session |
|-----------|-----------|---------------------|
| **Document Stores** | Höhere Ausdrucksstärke (sekundäre Indizes), Flexibilität bleibt | L7–L9 |
| **Column Stores** | Optimiert für Aggregationen, schwach bei Punkt-Abfragen? | L10–L12 |
| **Relational** | Hohe Integrität & Ausdrucksstärke, aber rigide? | L13–L18 |
| **Graph** | Spezialisiert für Beziehungen, neu: Traversal-Ausdrucksstärke | L19–L21 |

**Aufgabe:** Notieren Sie sich diese Hypothesen – wir testen sie in den kommenden Wochen!

</section>

---

## Anwendung: Entscheidungsraster

    --{{0}}--
Theorie ist schön, aber wir brauchen Praxis. Wie nutzen Sie die Matrix für konkrete Entscheidungen? Hier ein strukturiertes Vorgehen, das Sie auf jedes Projekt anwenden können.

    {{0-1}}
<section>

### Schritt 1: Anforderungsprofil erstellen

**Beispiel: Session-Management für Web-App**

| Anforderung | Gewichtung (1–10) | Begründung |
|-------------|-------------------|------------|
| Punkt-Abfragen (Session Lookup) | 10 | Jeder Request braucht Session |
| Schreibdurchsatz (Session Updates) | 8 | Bei jedem Request aktualisiert |
| Range Queries | 1 | Nicht benötigt |
| Transaktionale Integrität | 3 | Sessions sind unabhängig |
| Schema-Flexibilität | 7 | Session-Struktur ändert sich oft |

**Interpretation:** Brauchen O(1) Zugriff, hohen Durchsatz, Flexibilität – Integrität weniger wichtig.

</section>

    --{{1}}--
Jetzt gleichen wir unser Anforderungsprofil mit der Matrix ab. Session-Management braucht extrem schnelle Punkt-Abfragen – Key-Value ist perfekt. Transaktionale Integrität ist unwichtig – die Schwäche von KV stört nicht. Schema-Flexibilität ist wichtig – KV bietet das. Ergebnis: Redis oder Memcached. Kein SQL, kein Document Store – die wären Overkill. Die Matrix macht diese Argumentation explizit und überprüfbar.

    {{1-2}}
<section>

### Schritt 2: Paradigmen abgleichen

**Matrix-Mapping:**

```ascii
Anforderung              | Gewicht | Flat Files | Key-Value | Document | Relational
─────────────────────────┼─────────┼────────────┼───────────┼──────────┼───────────
Punkt-Abfragen           |   10    |     ❌     |    ✅     |    ✅    |    ⚠️
Schreibdurchsatz         |    8    |     ❌     |    ✅     |    ⚠️    |    ❌
Range Queries            |    1    |     ❌     |    ❌     |    ✅    |    ✅
Transaktionale Integrität|    3    |     ❌     |    ⚠️     |    ⚠️    |    ✅
Schema-Flexibilität      |    7    |     ✅     |    ✅     |    ✅    |    ❌
```

**Gewichtete Bewertung:**

- **Key-Value:** 10×✅ + 8×✅ + 1×❌ + 3×⚠️ + 7×✅ = **Beste Wahl**
- **Document:** Overkill (unnötige Features)
- **Relational:** Falsche Trade-offs (zu rigide, zu langsam)

</section>

    --{{2}}--
Diese Methode zwingt Sie, Ihre Annahmen zu explizieren. Oft hören Sie: "Wir brauchen eine Datenbank". Die Matrix fragt zurück: Wozu genau? Punkt-Abfragen oder Analysen? Transaktionen oder Durchsatz? Flexibilität oder Garantien? Erst wenn Sie das beantwortet haben, können Sie rational entscheiden. Und manchmal überrascht die Antwort: "Wir brauchen gar keine Datenbank, eine In-Memory Map reicht."

    {{2}}
<section>

### Schritt 3: Trade-offs dokumentieren

**Entscheidungsdokumentation (Beispiel):**

> **Projekt:** Session-Management
>
> **Gewähltes Paradigma:** Key-Value (Redis)
>
> **Begründung:**
>
> - ✅ O(1) Punkt-Abfragen (Hauptanforderung)
> - ✅ Hoher Schreibdurchsatz (TTL-Support für Auto-Expiry)
> - ✅ Schema-Flexibilität (Session-Struktur evolviert)
> - ⚠️ Keine Transaktionen – akzeptabel, da Sessions unabhängig
> - ⚠️ Keine Range Queries – nicht benötigt
>
> **Risiken & Alternativen:**
>
> - **Risiko:** Datenverlust bei Redis-Crash → Mitigation: Persistenz-Modus + Replikation
> - **Alternative:** Memcached (schneller, aber keine Persistenz) → Verworfen, da Sessions nach Restart erhalten bleiben sollen

**Wert:** Nachvollziehbare Entscheidung, die in 6 Monaten noch verstanden wird.

</section>

---

## Matrix-Update Roadmap

    --{{0}}--
Die Matrix ist ein lebendes Dokument. Mit jeder Session erweitern wir unser Verständnis und verfeinern die Bewertungen. Hier die geplanten Updates – markieren Sie sich diese Termine!

    {{0-1}}
<section>

### Geplante Matrix-Updates

| Session | Update | Fokus |
|---------|--------|-------|
| **L3 (heute)** | Matrix v1 | Initiale Bewertung (File, KV konzeptionell) |
| **L6** | Matrix v2 | KV Details (Redis), Grenzen formalisiert, Document Preview |
| **L9** | Matrix v3 | Document & Column hinzugefügt, Trade-off-Analyse |
| **L12** | Matrix v4 | Analytics-Profil verfeinert, Relational Preview |
| **L16** | Matrix v5 | Relational vollständig, Index-Performance integriert |
| **L18** | Matrix v6 | Polyglot-Ansätze, Kombinationen diskutiert |
| **L21** | Matrix v7 (Final) | Graph hinzugefügt, Vollständige Bewertung aller Paradigmen |

**Wichtig:** Jedes Update ist **inkrementell** – wir verwerfen nicht, sondern verfeinern!

</section>

    --{{1}}--
Warum dieser iterative Ansatz? Weil Lernen nicht linear ist. Nach L4 werden Sie Redis besser verstehen und unsere heutigen KV-Ratings anpassen wollen. Nach L15 werden Sie Transaktionen verstehen und die Integritäts-Achse neu bewerten. Das ist kein Fehler im Kurs-Design, sondern bewusste Didaktik: Wir bauen Ihr mentales Modell schrittweise auf, statt alles auf einmal zu werfen. Die Matrix dokumentiert diese Reise.

    {{1}}
<section>

### Wie Sie die Matrix nutzen

**Während der Vorlesung:**

1. **Vor neuen Paradigmen:** Hypothesen formulieren (z.B. "Column Stores sind langsam bei Punkt-Abfragen")
2. **Nach Sessions:** Hypothesen überprüfen, Matrix aktualisieren
3. **Bei Vergleichen:** Explizit auf Achsen referenzieren ("KV ist stark auf Achse 5, schwach auf Achse 4")

**Im Projekt:**

1. **Anforderungsprofil** erstellen (siehe Schritt 1 oben)
2. **Paradigmen abgleichen** (siehe Schritt 2)
3. **Entscheidung dokumentieren** (siehe Schritt 3)

**Im Beruf:**

- Bei Architektur-Reviews: "Welche Achsen haben Sie evaluiert?"
- Bei Technologie-Auswahl: "Wie sieht Ihr Anforderungsprofil aus?"
- Bei Migrationen: "Welche Achsen verbessern/verschlechtern sich?"

</section>

---

## Aktivität: Erste Matrix-Übung

    --{{0}}--
Jetzt sind Sie dran! Arbeiten Sie in Kleingruppen an einem konkreten Szenario. Ziel ist nicht die "richtige" Antwort, sondern explizite Argumentation entlang der Achsen.

    {{0-1}}
<section>

### Szenario: Blog-System

**Gegeben:**

Ein persönlicher Blog mit folgenden Features:

- Blogposts (Titel, Inhalt, Autor, Datum, Tags)
- Kommentare (pro Post)
- Suchfunktion ("Alle Posts mit Tag 'Databases'")
- Statistiken (Views pro Post, Top-5 Posts)
- Traffic: ~1000 Zugriffe/Tag, ~10 neue Posts/Monat

**Aufgaben (15 Minuten Gruppenarbeit):**

1. Erstellen Sie ein **Anforderungsprofil** (5 wichtigste Anforderungen mit Gewichtung)
2. Bewerten Sie **Flat Files** und **Key-Value** für diesen Use-Case
3. **Diskutieren Sie:** Was fehlt? Welche Paradigmen könnten besser passen?

**Hinweis:** Wir kennen Document/Column/Relational noch nicht im Detail – spekulieren Sie!

</section>

    --{{1}}--
Nehmen Sie sich wirklich die Zeit für diese Übung. Typische Fallen: "Wir brauchen eine Datenbank" ohne zu spezifizieren warum. Oder: "PostgreSQL, weil das kann alles" ohne Trade-offs zu bedenken. Zwingen Sie sich, konkret zu werden. Wie oft werden Posts geschrieben vs. gelesen? Sind Tags fix oder dynamisch? Brauchen Sie Transaktionen beim Kommentieren? Diese Details entscheiden die Architektur.

    {{1-2}}
<section>

### Mögliche Lösung (Diskussionsimpuls)

**Anforderungsprofil (Beispiel):**

| Anforderung | Gewicht | Begründung |
|-------------|---------|------------|
| Lesezugriffe (Post abrufen) | 9 | 99% des Traffics |
| Tag-basierte Suche | 7 | Hauptnavigation |
| Schema-Evolution | 6 | Posts können neue Felder bekommen |
| Schreibdurchsatz | 2 | Nur 10 Posts/Monat |
| Transaktionale Integrität | 4 | Kommentare sollten atomar sein |

**Analyse:**

- **Flat Files:** ❌ Suche ineffizient, keine Indizes
- **Key-Value:** ⚠️ Lesezugriffe schnell, aber Tag-Suche = Full Scan
- **Hypothese:** Document Store (z.B. MongoDB) könnte besser passen – sekundäre Indizes für Tags, flexible Schemas

**Erkenntnis:** KV alleine reicht nicht – wir brauchen Indizes auf Nicht-Key-Feldern!

</section>

    --{{2}}--
Sehen Sie, wie die Matrix zwingt, präzise zu argumentieren? "MongoDB ist gut für Blogs" ist eine Meinung. "Document Stores bieten sekundäre Indizes für Tag-Suche bei erhaltener Schema-Flexibilität" ist eine Begründung. In L7 werden wir Document Stores im Detail behandeln und diese Hypothese überprüfen. Bis dahin: Sie haben gelernt, systematisch zu denken.

    {{2}}
<section>

### Plenum-Diskussion (5 Minuten)

**Leitfragen:**

1. Welche Anforderungen waren in Ihrer Gruppe umstritten?
2. Wo fehlten Ihnen Informationen für eine Bewertung?
3. Welche Paradigmen wollen Sie als Nächstes kennenlernen?

**Ziel:**

- Unsicherheiten explizit machen
- Erwartungen für kommende Sessions klären
- Matrix als "Forschungsfragen-Generator" verstehen

</section>

---

## Zusammenfassung & Reflexion

    --{{0}}--
Lassen Sie uns die Kernideen dieser Session festhalten. Wir haben ein analytisches Framework entwickelt, das uns die gesamte Vorlesung begleiten wird. Die Matrix ist kein dogmatisches Regelwerk, sondern ein Denkwerkzeug.

    {{0-1}}
<section>

### Kernerkenntnisse

1. **Fünf Achsen charakterisieren jedes Paradigma:**
   - Strukturgrad (Flexibilität vs. Rigidität)
   - Integrität (Konsistenzgarantien)
   - Konfliktpotenzial (Nebenläufigkeit)
   - Ausdrucksstärke (Query-Mächtigkeit)
   - Performanceprofil (Workload-spezifisch)

2. **Kein Paradigma ist "das Beste"** – nur "das Beste für X"

3. **Trade-offs explizit machen** ist wichtiger als Features aufzählen

4. **Matrix ist iterativ** – wir verfeinern mit wachsendem Verständnis

5. **Entscheidungen dokumentieren** macht Architektur nachvollziehbar

</section>

    --{{1}}--
Bevor Sie gehen: Ein Meta-Reflexionsimpuls. Die Matrix ist ein Werkzeug – aber wie alle Werkzeuge hat sie Grenzen. Sie kann Ihnen nicht sagen, welches Paradigma "richtig" ist, weil das vom Kontext abhängt. Sie kann Sie nicht vor schlechten Entscheidungen schützen, wenn Sie falsche Anforderungen definieren. Was sie kann: Ihre Denkprozesse strukturieren, Annahmen sichtbar machen und Diskussionen versachlichen. Verwenden Sie sie als Kompass, nicht als Karte.

    {{1}}
<section>

### 🤔 Reflexionsfragen (2 Minuten)

> **Persönliche Reflexion:**
>
> 1. Welche Achse finden Sie am schwierigsten zu bewerten? Warum?
> 2. Gibt es Anforderungen, die die Matrix nicht abdeckt? (z.B. Kosten, Betriebsaufwand, Team-Skills)
> 3. Wie würden Sie einem Nicht-Techniker die Matrix erklären?

**Optionale Vertiefung:**

- Wenden Sie die Matrix auf ein Projekt an, das Sie kennen
- Dokumentieren Sie: Was hätte die Matrix damals verhindert/verbessert?

</section>

---

## Ausblick: Block 2 – Key-Value im Detail

    --{{0}}--
In den nächsten drei Sessions tauchen wir tief in Key-Value Stores ein. L4 behandelt Grundlagen und Caching-Patterns, L5 erkundet Key-Design und Anwendungsmuster, L6 diskutiert Grenzen und aktualisiert die Matrix. Nach Block 2 haben Sie ein vollständiges Bild von KV – und verstehen, warum wir komplexere Paradigmen brauchen.

    {{0}}
<section>

### Block 2 Preview: Key-Value Deep Dive

| Session | Thema | Matrix-Relevanz |
|---------|-------|-----------------|
| **L4** | KV Grundlagen & Caching | TTL, Atomic Operations, Race Conditions (Achse 3) |
| **L5** | Key-Design & Patterns | Namespacing, Composite Keys, Real-World Use-Cases |
| **L6** | Grenzen & Vergleich | **Matrix v2:** KV-Ratings verfeinert, Document-Preview |

**Nach Block 2:**

- Meilenstein MS1 (Rohdaten + KV Layer)
- Erste vollständige Paradigmen-Bewertung
- Motivation für Document Stores klar

</section>

    --{{1}}--
Der Kurs folgt einem bewussten Rhythmus: Einführung → Vertiefung → Reflexion → Nächstes Paradigma. Wir sprinten nicht durch Features, sondern bauen Verständnis auf. Jedes Paradigma löst ein Problem des vorherigen – und schafft neue. Die Matrix dokumentiert diese Evolution. Am Ende haben Sie nicht nur Technologien gelernt, sondern Denkmuster für Architektur-Entscheidungen.

---

## Referenzen & Vertiefung

    --{{0}}--
Für alle, die das Matrix-Konzept vertiefen möchten, hier weiterführende Ressourcen. Diese sind optional, aber hilfreich für eigene Projekte.

    {{0}}
<section>

### Empfohlene Ressourcen

**Entscheidungs-Frameworks:**

- **Architecture Decision Records (ADR):** [adr.github.io](https://adr.github.io/)
- **Trade-off Analysis:** "Designing Data-Intensive Applications" (Kleppmann, Kap. 1-3)
- **CAP Theorem:** [Brewer's Original Paper](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/)

**Paradigmen-Vergleiche:**

- **Database Comparison Matrix:** [db-engines.com](https://db-engines.com/en/ranking)
- **NoSQL Distilled** (Sadalage & Fowler) – Systematischer Paradigmen-Überblick
- **The Architecture of Open Source Applications** – Innenansichten echter Systeme

**Didaktische Ansätze:**

- **Comparative Learning:** Wie Vergleichsachsen das Lernen unterstützen
- **Spiral Curriculum:** Warum wir iterativ verfeinern statt alles auf einmal zu lehren

</section>

---

## Anhang: Template für Ihre Projekte

    --{{0}}--
Abschließend ein praktisches Artefakt: Ein Template, das Sie in realen Projekten verwenden können. Passen Sie es an Ihre Bedürfnisse an!

    {{0}}
<section>

### Paradigmen-Matrix Template (Markdown)

```markdown
# Datenbank-Evaluierung: [Projekt-Name]

## Anforderungsprofil

| Anforderung | Gewicht (1-10) | Begründung |
|-------------|----------------|------------|
| ...         | ...            | ...        |

## Paradigmen-Vergleich

| Achse | [Paradigma 1] | [Paradigma 2] | [Paradigma 3] |
|-------|---------------|---------------|---------------|
| Strukturgrad | x/10 | x/10 | x/10 |
| Integrität | x/10 | x/10 | x/10 |
| Konfliktpotenzial | x/10 | x/10 | x/10 |
| Ausdrucksstärke | x/10 | x/10 | x/10 |
| Performanceprofil | [Details] | [Details] | [Details] |

## Entscheidung

**Gewählt:** [Paradigma X]

**Begründung:**
- ✅ [Stärke 1]
- ✅ [Stärke 2]
- ⚠️ [Trade-off 1, akzeptiert weil...]
- ❌ [Ausgeschlossene Alternative, weil...]

**Risiken & Mitigation:**
- [Risiko 1] → [Mitigation]

**Review-Datum:** [Datum für Re-Evaluierung]
```

**Nutzung:**

1. Template kopieren
2. Projekt-spezifisch ausfüllen
3. Im Repo dokumentieren (z.B. `docs/architecture/db-decision.md`)
4. Bei Reviews referenzieren

</section>

---

    --{{0}}--
Vielen Dank für Ihre aktive Teilnahme! Die Matrix ist jetzt Ihr Werkzeug – nutzen Sie sie in den kommenden Wochen. In Session 4 starten wir mit Redis: praktisch, konkret, hands-on. Bis dahin: Denken Sie in Achsen, nicht in Buzzwords!

