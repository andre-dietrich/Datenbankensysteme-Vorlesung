<!--
author:   André Dietrich; ; GitHub CoPilot
email:    andre.dietrich@informatik.tu-freiberg.de
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  Persönliche Vorstellung des Dozenten: Von der Promotion in Robotik über NoSQL-Systeme (Cassandra), deklarative Abfragesprachen (SelectScript), Remote Labs (Industrial eLab) bis zur Entwicklung von LiaScript und Edrys-Lite. Diese Session erklärt den Hintergrund der Vorlesung, warum Browser-basierte Technologien (IndexedDB, DuckDB-Wasm, SQLite-Wasm) im Fokus stehen und wie GitHub Copilot als Co-Autor für interaktive OER-Materialien eingesetzt wird.

logo:     ../assets/img/logo/0-lecture.jpg

edit:    true

import:   https://raw.githubusercontent.com/LiaScript/CodeRunner/master/README.md
          https://raw.githubusercontent.com/LiaTemplates/Communica/0.0.2/README.md
-->

# Session 0 – Vorstellung: Mein Weg zu Datenbanken & interaktivem OER

> **Session-Typ:** Einführung / Vorstellung (keine vollständige Vorlesung)  
> **Dauer:** ca. 30–45 Minuten  
> **Fokus:** Persönlicher Background, technologische Reise, Motivation für diese Vorlesung

**Hinweis:** Diese Session ist **kein Pflichtbestandteil** der Vorlesung, sondern eine persönliche Einladung, meinen Hintergrund kennenzulernen und zu verstehen, warum diese Vorlesung so gestaltet ist, wie sie ist.

---

## Zusammenfassung

    --{{0}}--
In dieser Session stelle ich mich vor – André Dietrich, Ihr Dozent für diese Vorlesung. Ich gebe Ihnen einen Einblick in meinen akademischen und beruflichen Werdegang, von meiner Promotion in eingebetteten Systemen und Robotik über meine Arbeit mit verteilten Datenbanksystemen bis hin zur Entwicklung interaktiver Lehr- und Lernmaterialien.

    --{{1}}--
Dabei erzähle ich, wie meine Leidenschaft für Programmiersprachen, Datenbankparadigmen und Web-Technologien mich zu Projekten wie LiaScript, SelectScript, cassandra_ros, Industrial eLab und Edrys-Lite geführt hat – und warum ich überzeugt bin, dass interaktive Open Educational Resources die Zukunft des Lernens sind.

---

## Über mich – André Dietrich

Promotion: Eingebettete Systeme & Robotik
-----------------------------------------

    --{{0}}--
Ich habe in Embedded Systems und Robotics an der Otto-von-Guericke-Universität Magdeburg promoviert. Der Fokus meiner Dissertation lag auf dem Internet of Things und dem Zugriff auf verteilte Systeme.

      {{0-1}}
<div>

**Zentrale Frage meiner Forschung:**

> Wie können wir große Mengen an Sensordaten aus verschiedenen Quellen effizient sammeln, speichern und abfragen?

**Herausforderungen:**

- **Heterogenität:** Sensoren liefern Daten in unterschiedlichen Formaten (JSON, Binär, Protobuf)
- **Verteilung:** Daten kommen von vielen Quellen (Roboter, Mikrocontroller, Cloud-Services)
- **Skalierbarkeit:** Millionen von Datenpunkten pro Sekunde
- **Abfragbarkeit:** Wie machen wir diese Daten sinnvoll zugänglich?

</div>

    --{{1}}--
Während meiner Promotion entwickelte sich eine Faszination für Programmiersprachen und Paradigmen. Eine zentrale Frage war: Wie können wir Daten holistisch und intuitiv zugänglich machen – ohne uns in technischen Details zu verlieren?

      {{1}}
<div>

### Interesse: Programmiersprachen & Paradigmen

**Leitfragen:**

- Wie können Abfragesprachen über klassische Datenbanken hinausgehen?
- Welche Paradigmen eignen sich für welche Anwendungsfälle?
- Wie können wir Komplexität reduzieren, ohne Mächtigkeit zu verlieren?

</div>

---

## Meine Projekte: Von NoSQL zu OER

### cassandra_ros – NoSQL & Sensordaten

    --{{0}}--
Mein erstes größeres Datenbankprojekt war ein ROS-Adapter für Apache Cassandra, einen NoSQL Wide Column Store. Das Ziel: Sensorsignale aus Robotern in einer verteilten Datenbank speichern und abfragen.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt             | Details                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| **Projekt**        | ROS-Adapter für Apache Cassandra                                       |
| **Ziel**           | Sensorsignale aus Robotern speichern                                   |
| **Technologie**    | Cassandra (NoSQL Wide Column Store)                                    |
| **Abfragesprache** | CQL (Cassandra Query Language)                                         |
| **Link**           | [cassandra_ros Wiki](http://mirror-ap.wiki.ros.org/cassandra_ros.html) |

</div>

    --{{1}}--
Was habe ich dabei gelernt? Wide Column Stores bieten flexible Schemas und horizontale Skalierbarkeit – perfekt für write-heavy Workloads wie Sensordaten. CQL ermöglicht SQL-ähnliche Abfragen auf NoSQL-Systemen. Aber es gibt Trade-offs: Eventual Consistency versus starke Konsistenz – das CAP-Theorem in der Praxis.

      {{1}}
<div>

**Wichtigste Erkenntnisse:**

```ascii
┌─────────────────────────────────────────────────┐
│  Wide Column Store (Cassandra)                  │
├─────────────────────────────────────────────────┤
│  ✓  Flexible Schemas                            │
│  ✓  Horizontale Skalierbarkeit                  │
│  ✓  Write-heavy Workloads                       │
│  ✓  SQL-ähnliche Abfragen (CQL)                 │
│  ✗  Eventual Consistency (CAP-Theorem)          │
│  ✗  Komplexe Joins schwierig                    │
└─────────────────────────────────────────────────┘
```

**Trade-off (CAP-Theorem):**

- **Consistency:** Alle Knoten sehen dieselben Daten zur gleichen Zeit
- **Availability:** System antwortet immer (auch bei Netzwerkpartitionierung)
- **Partition Tolerance:** System funktioniert trotz Netzwerkausfällen

> Cassandra wählt: **Availability + Partition Tolerance** → Eventual Consistency

!?[IROS 2014 - Distributed Management and Representation of Data and Context in Robotic Applications 1](https://www.youtube.com/watch?v=Xt403wPCYD8)
!?[IROS 2014 - Distributed Management and Representation of Data and Context in Robotic Applications 2](https://www.youtube.com/watch?v=kvoC5yxdzsw)

</div>

---

### SelectScript – Deklarative Abfragesprache

    --{{0}}--
Parallel entwickelte ich SelectScript – eine Lua-ähnliche, eingebettete Programmiersprache für Simulationsumgebungen. Die Besonderheit: SELECT-Statements werden nicht nur für Datenabfragen verwendet, sondern für allgemeine Problemlösungen.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt           | Details                                                                   |
| ---------------- | ------------------------------------------------------------------------- |
| **Projekt**      | Deklarative Abfragesprache für Simulationen                               |
| **Besonderheit** | SELECT-Statements für Problemlösung                                       |
| **Anwendung**    | Rekursive Abfragen, hierarchische Strukturen, robotische Weltmodelle      |
| **Beispiele**    | Türme von Hanoi, 4-Farben-Problem, Graphtraversierung                     |
| **Link**         | [SelectScript auf GitHub](https://github.com/andre-dietrich/SelectScript) |

</div>

    --{{1}}--
SelectScript zeigt, dass SQL-ähnliche Syntax weit über klassische Datenbanken hinausgehen kann. Rekursive Queries sind mächtiger, als man denkt – ob Türme von Hanoi, Graphtraversierung oder Constraint-Satisfaction-Probleme. Deklarative Sprachen ermöglichen intuitive Problemlösung.

      {{1}}
<div>

**Beispiel: Rekursive Query (Türme von Hanoi)**

``` SQL
mov
  = PROC(Tower, frm, to)
    "A simple tower move function that returns a new tower configuration:
     mov([[3,2,1], [], []], 0, 1) -> [[3,2], [1], []]

     In case of an unalowed move a None value gets returned:
     mov([[3,2], [1], []], 0, 1)  -> None "
    : ( IF( $Tower == None, EXIT None);

        IF( not $Tower[$frm], EXIT None);

        IF( $Tower[$to],
            IF( $Tower[$frm][-1] > $Tower[$to][-1],
                EXIT None));

        $Tower[$to]@+( $Tower[$frm][-1] );
        $Tower[$frm]@pop();
        $Tower;
      );


# initial tower configuration
tower = [[3,2,1], [], []];

# allowed moves [from, to]
moves = [[0,1], [0,2], [1,0], [1,2], [2,0], [2,1]];

# goal configuration
finish = [[], [], [3,2,1]];



# vanilla-approach: recusively test all combinations for 7 moves
$start_time = time();
rslt1 = SELECT [$m1, $m2, $m3, $m4, $m5, $m6, $m7]
          FROM m1:moves, m2:moves, m3:moves, m4:moves,
               m5:moves, m6:moves, m7:moves
         WHERE finish == (tower
                          |> mov($m1[0], $m1[1])
                          |> mov($m2[0], $m2[1])
                          |> mov($m3[0], $m3[1])
                          |> mov($m4[0], $m4[1])
                          |> mov($m5[0], $m5[1])
                          |> mov($m6[0], $m6[1])
                          |> mov($m7[0], $m7[1]))
           AS list;

print("######################################################################");
print("first vanilla-approach search");
print("time:   ", time()-$start_time);
print("result: ", rslt1);



$start_time = time();
rslt2 = SELECT $m
          FROM m:moves
         WHERE finish == mov($tower, $m[0], $m[1])
    START WITH $tower = tower
    CONNECT BY $tower@mov($m[0], $m[1])
     STOP WITH $tower == None OR $step$ > 6
            AS list;

print("######################################################################");
print("simple CONNECT BY (recursive search)");
print("time:   ", time()-$start_time);
print("result: ", rslt2);



$start_time = time();
rslt3 = SELECT $tower
          FROM m:moves
         WHERE finish == mov($tower, $m[0], $m[1])
    START WITH $tower = tower
    CONNECT BY NO CYCLE
               $tower@mov($m[0], $m[1])
     STOP WITH $tower == None OR $step$ > 6
            AS LIST;

print("######################################################################");
print("CONNECT BY with no cycles");
print("time:   ", time()-$start_time);
print("result: ", rslt3);


rslt4 = SELECT $step$, $tower, $m
          FROM m:moves
         WHERE finish == mov($tower, $m[0], $m[1])
    START WITH $tower = tower
    CONNECT BY UNIQUE
               $tower@mov($m[0], $m[1])
     STOP WITH $tower == None OR $step$ > 7
            AS LIST;

print("######################################################################");
print("CONNECT BY with UNIQUE");
print("time:   ", time()-$start_time);
print("result: ", rslt4);

True;
```
@LIA.selectscript

**Wichtigste Erkenntnisse:**

- **Deklarative Sprachen** ermöglichen intuitive Problemlösung
- **SQL-ähnliche Syntax** kann über klassische Datenbanken hinausgehen
- **Rekursive Queries** sind mächtig (Graphtraversierung, Constraint-Solving)

!?[SelectScript & OpenRave](https://www.youtube.com/watch?v=jSaoCXRNVNg)

</div>

---

### Industrial eLab – Remote Labs & Web-Technologien

    --{{0}}--
Von zweitausendsiebzehn bis zwanzig arbeitete ich am BMBF-geförderten Projekt Industrial eLab. Ziel war es, Remote Labs für die Ingenieurausbildung zu entwickeln – Studierende sollten zeit- und ortsunabhängig mit realer Hardware wie Robotern und Mikrocontrollern arbeiten können.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt          | Details                                                                                                                                                                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Projekt**     | BMBF-gefördertes Remote Lab (2017–2020)                                                                                                                                                                                                            |
| **Partner**     | Otto-von-Guericke-Universität Magdeburg, Hochschule Magdeburg-Stendal                                                                                                                                                                              |
| **Technologie** | Elixir Backend, Elm Frontend, WebSockets                                                                                                                                                                                                           |
| **Ziel**        | Zeit- und ortsunabhängiger Zugriff auf reale Hardware                                                                                                                                                                                              |
| **Förderung**   | 895.890 EUR                                                                                                                                                                                                                                        |
| **Link**        | [Industrial eLab Projektseite](https://www.wihoforschung.de/wihoforschung/de/bmbf-projektfoerderung/foerderlinien/forschung-zur-digitalen-hochschulbildung/erste-foerderlinie-zur-digitalen-hochschulbildung/industrial-elab/industrial-elab.html) |

</div>

    --{{1}}--
Aus diesem Projekt habe ich drei zentrale Erkenntnisse mitgenommen. Erstens: Der Browser ist ein vollwertiges Betriebssystem – moderne Web-Technologien wie WebRTC, IndexedDB und Service Workers ermöglichen komplexe Anwendungen. Zweitens: Progressive Web Apps mit IndexedDB und Caching ermöglichen Offline-Fähigkeit und Persistenz. Drittens: Die didaktische Herausforderung – Wie gestalten wir adaptive Lernumgebungen, die Studierende beim Problemlösen unterstützen?

      {{1-2}}
<div>

**Technologie-Stack:**

```ascii
┌──────────────────────────────────────────┐
│  Frontend (Elm)                          │
│  ├── Funktionale Programmierung          │
│  ├── Type-Safe UI                        │
│  └── WebSockets für Echtzeit             │
├──────────────────────────────────────────┤
│  Backend (Elixir)                        │
│  ├── Hochverfügbar (Erlang VM)           │
│  ├── Nebenläufig (Actor Model)           │
│  └── WebSocket Server                    │
├──────────────────────────────────────────┤
│  Browser-Technologien                    │
│  ├── IndexedDB (Persistenz)              │
│  ├── Service Workers (Offline)           │
│  └── WebRTC (Peer-to-Peer)               │
└──────────────────────────────────────────┘
```

</div>

    --{{2}}--
Und genau aus diesem Projekt entstand die Idee für LiaScript – eine Markdown-basierte Beschreibungssprache für interaktive Lehr- und Lernmaterialien. Die Vision: Lehrinhalte sollten so einfach wie Markdown sein, aber so mächtig wie moderne Web-Apps.

      {{2}}
<div>

### Entstehung von LiaScript

> **Idee:** Markdown + Interaktivität + Browser-Power = LiaScript

**Zentrale Frage:**

Wie können Lehrende ohne Programmierkenntnisse interaktive, multimediale Kurse erstellen?

**Antwort:** Eine erweiterte Markdown-Syntax, die direkt im Browser interpretiert wird.

</div>

---

### LiaScript – Interaktive OER im Browser

    --{{0}}--
LiaScript ist heute ein Open-Source-Projekt für interaktive Kurse in Markdown. Die Vision: Lehrende erstellen Kurse als einfache Textdateien, zum Beispiel auf GitHub, ohne Build-Steps oder Content-Management-Systeme.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt          | Details                                                    |
| --------------- | ---------------------------------------------------------- |
| **Projekt**     | Open-Source Markdown-Interpreter für interaktive Kurse     |
| **Vision**      | Kurse als Textdateien (z. B. auf GitHub), ohne Build-Steps |
| **Features**    | Multimedia, Quizze, Live-Coding, TTS, Kollaboration        |
| **Technologie** | IndexedDB, Service Workers, WebRTC                         |
| **Link**        | [LiaScript Homepage](https://liascript.github.io/)         |

!?[Hello World](https://www.youtube.com/watch?v=S3hIK8_kjl8)

</div>

    --{{1}}--
LiaScript bietet eine Vielzahl von Features: Multimedia wie Videos, Audio, ASCII-Diagramme, Mermaid und LaTeX. Interaktion durch Quizze, Live-Coding in JavaScript, Python oder SQL, und Text-to-Speech. Kollaboration über WebRTC-basierte Klassenräume mit Peer-to-Peer-Kommunikation. Und Persistenz durch IndexedDB für Offline-Fähigkeit und Fortschritt speichern.

      {{1-2}}
<div>

**Feature-Übersicht:**

```ascii
┌─────────────────────────────────────────────────┐
│  LiaScript Features                             │
├─────────────────────────────────────────────────┤
│  📹  Multimedia                                 │
│      Videos, Audio, ASCII-Art, Mermaid, oEmbed  │
├─────────────────────────────────────────────────┤
│  🎮  Interaktion                                │
│      Quizze, Live-Coding (JS/Python/SQL), TTS   │
├─────────────────────────────────────────────────┤
│  👥  Kollaboration                              │
│      WebRTC-Klassenräume (Peer-to-Peer)         │
├─────────────────────────────────────────────────┤
│  💾  Persistenz                                 │
│      IndexedDB (Offline + Fortschritt)          │
└─────────────────────────────────────────────────┘
```

</div>

    --{{2}}--
Welche Technologien stecken dahinter? IndexedDB für lokale Datenhaltung – eine NoSQL-Datenbank direkt im Browser. Service Workers für Offline-Caching – Kurse funktionieren auch ohne Internetverbindung. Und WebRTC für Peer-to-Peer-Kommunikation in kollaborativen Klassenräumen.

      {{2}}
<div>

**Technologie-Stack:**

| Technologie         | Zweck               | Datenbankbezug                  |
| ------------------- | ------------------- | ------------------------------- |
| **IndexedDB**       | Lokale Datenhaltung | NoSQL Object Store im Browser   |
| **Service Workers** | Offline-Caching     | Persistent Storage API          |
| **WebRTC**          | Peer-to-Peer        | Dezentrale Datensynchronisation |

**Wichtigste Erkenntnisse:**

- **Browser-basierte Datenbanken** (IndexedDB) sind mächtig, aber anders als traditionelle SQL-DBs
- **NoSQL im Browser:** Object Stores, Key-Value Zugriffe, Indexierung
- **Trade-offs:** Flexibilität vs. strukturierte Abfragen

</div>

### Selbständiger Elm-Entwickler – Linked Data & SPARQL

    --{{0}}--
Nach dem Industrial eLab-Projekt war ich als selbständiger Elm-Entwickler tätig und arbeitete an Linked Data Anwendungen. Dabei kam ich mit dem Semantic Web und SPARQL in Kontakt.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt          | Details                                       |
| --------------- | --------------------------------------------- |
| **Projekt**     | Web-Entwicklung für Linked Data Anwendungen   |
| **Technologie** | Elm Frontend, Semantic Web, SPARQL            |
| **Datenbank**   | RDF-Stores (Triple Stores) für Wissensgraphen |

</div>

    --{{1}}--
Was habe ich dabei gelernt? Graphdatenbanken sind ideal für vernetzte, semantische Daten. SPARQL ist SQL für Graphen – aber mit eigenen Herausforderungen. RDF und Linked Data sind flexibel, aber komplex zu modellieren.

      {{1}}
<div>

**RDF Triple Store Konzept:**

```ascii
┌────────────────────────────────────────────┐
│  RDF Triple: Subject → Predicate → Object  │
├────────────────────────────────────────────┤
│  Beispiel:                                 │
│  André → arbeitet_an → LiaScript           │
│  LiaScript → ist_ein → OER_Projekt         │
│  OER_Projekt → hat_Lizenz → CC-BY          │
└────────────────────────────────────────────┘
```

**SPARQL Query Beispiel: Datenbank-Erfinder und ihre Geburtstage**

``` sparql
# source: https://dbpedia.org/sparql

PREFIX dbo:  <http://dbpedia.org/ontology/>
PREFIX dbr:  <http://dbpedia.org/resource/>
PREFIX dbc:  <http://dbpedia.org/resource/Category:>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?person ?name ?birthDate ?work ?workLabel
WHERE {
  # a "database" work: software whose category contains “database”
  ?work a dbo:Software ;
        dct:subject ?cat .
  FILTER(CONTAINS(LCASE(STR(?cat)), "database"))

  # link people to the work via common creator-like properties
  ?person a dbo:Person ;
          (dbo:author|dbo:developer|dbo:designer|dbo:creator|dbo:notableWork|dbo:knownFor) ?work ;
          foaf:name ?name .
  
  OPTIONAL { ?person dbo:birthDate ?birthDate . }
  OPTIONAL { ?work rdfs:label ?workLabel . FILTER(LANG(?workLabel) = "en") }
  FILTER(LANG(?name) = "en")
}
ORDER BY ?name
LIMIT 20
```
@Communica.SPARQL

**Wichtigste Erkenntnisse:**

- **Graphdatenbanken** sind ideal für vernetzte, semantische Daten
- **SPARQL** ist SQL für Graphen – aber mit eigenen Herausforderungen
- **RDF/Linked Data:** Flexibel, aber komplex zu modellieren

</div>

---

### CrossLab & Edrys-Lite – Peer-to-Peer Remote Labs

    --{{0}}--
In Freiberg hatte ich dann die Möglichkeit, LiaScript in verschiedenen Projekten zu erweitern und Peer-to-Peer-Mechanismen zu untersuchen. Daraus entstand Edrys-Lite – ein dezentrales Peer-to-Peer-System zum Teilen von Remote Labs.

      {{0-1}}
<div>

**Projekt-Steckbrief:**

| Aspekt           | Details                                             |
| ---------------- | --------------------------------------------------- |
| **Projekt**      | Dezentrales Peer-to-Peer Remote Lab System          |
| **Technologie**  | WebRTC für direkte Browser-zu-Browser-Kommunikation |
| **Ziel**         | Lehre und Labore dezentral organisieren             |
| **Besonderheit** | Jeder Browser ist ein potenzieller "Server"         |
| **Link**         | [Edrys-Lite](https://edrys-labs.github.io/)         |

</div>

    --{{1}}--
Die wichtigste Erkenntnis? Dezentrale Architekturen mit Peer-to-Peer reduzieren Abhängigkeiten von zentralen Servern. Browser-Technologien wie WebRTC, WebSockets und IndexedDB ermöglichen verteilte Anwendungen. Aber es gibt Trade-offs: Konsistenz versus Verfügbarkeit – das CAP-Theorem in der Praxis.

      {{1}}
<div>

**Architektur-Vergleich:**

```ascii
Klassisch (Client-Server):
┌────────┐     ┌────────┐     ┌────────┐
│ Client │────▶│ Server │◀────│ Client │
└────────┘     └────────┘     └────────┘
              Single Point of Failure

Edrys-Lite (Peer-to-Peer):
┌────────┐     ┌────────┐
│  Peer  │◀───▶│  Peer  │
└───┬────┘     └───┬────┘
    │              │
    └──────┬───────┘
           ▼
      ┌────────┐
      │  Peer  │
      └────────┘
    Dezentral, resilient
```

**Trade-off (CAP-Theorem):**

- **Consistency:** Schwierig bei P2P (Eventual Consistency)
- **Availability:** Hoch (kein Single Point of Failure)
- **Partition Tolerance:** Hoch (funktioniert bei Netzwerkausfällen)

**Wichtigste Erkenntnisse:**

- **Dezentrale Architekturen:** Peer-to-Peer reduziert Abhängigkeiten
- **Browser-Technologien:** WebRTC, WebSockets, IndexedDB ermöglichen verteilte Apps
- **Trade-offs:** Konsistenz vs. Verfügbarkeit (CAP-Theorem)

</div>

---

## Meine Motivation für diese Vorlesung

### Interaktive OER als Lernformat

    --{{0}}--
Ich bin überzeugt: Interaktive Materialien mit Quizzen, Live-Coding und Visualisierungen fördern das Verständnis. LiaScript ermöglicht es, direkt im Browser mit Datenbanken zu arbeiten – DuckDB, SQLite, IndexedDB. Kein Setup, kein Installieren – nur Browser öffnen und loslegen.

      {{0}}
<div>

**Vorteile interaktiver OER:**

| Aspekt            | Klassische Vorlesung      | Interaktive OER (LiaScript) |
| ----------------- | ------------------------- | --------------------------- |
| **Setup**         | Installation erforderlich | Browser genügt              |
| **Feedback**      | Verzögert                 | Sofort (Quizze, Live-Code)  |
| **Exploration**   | Begrenzt                  | Unbegrenzt (eigene Queries) |
| **Persistenz**    | Notizen auf Papier        | Automatisch im Browser      |
| **Kollaboration** | Schwierig                 | WebRTC-Klassenräume         |

> **In dieser Vorlesung:** Sie arbeiten direkt mit DuckDB, SQLite, IndexedDB – alles im Browser!

</div>

---

### Spec-Driven Development mit GitHub Copilot

    --{{0}}--
Ich nutze GitHub Copilot als Co-Autor für diese Vorlesung. Der Ansatz: Spec-Driven Development – ich definiere Struktur, Lernziele und Didaktik, Copilot hilft bei den Inhalten. Das Experiment: Wie kann KI Lehrende bei der Erstellung von OER unterstützen?

      {{0}}
<div>

**Workflow:**

```ascii
┌─────────────────────────────────────────┐
│  1. Outline erstellen                   │
│     (Titel, Zielgruppe, Lernziele)      │
├─────────────────────────────────────────┤
│  2. Didactics definieren                │
│     (Persona, Stil, Methoden)           │
├─────────────────────────────────────────┤
│  3. Agenda strukturieren                │
│     (Sessions, Meilensteine)            │
├─────────────────────────────────────────┤
│  4. Co-Authoring mit Copilot            │
│     (Inhalte, Beispiele, Übungen)       │
├─────────────────────────────────────────┤
│  5. Iteration & Feedback                │
│     (Studierende, Selbstreflexion)      │
└─────────────────────────────────────────┘
```

**Forschungsfrage:**

> Kann KI den Prozess der OER-Erstellung beschleunigen, ohne Qualität zu verlieren?

</div>

---

### Aktuelle Rolle

    --{{0}}--
Ich bin Dozent für Datenbanken im Wintersemester zweitausendfünfundzwanzig-sechsundzwanzig an der TU Bergakademie Freiberg. Mein Ziel: Eine praxisnahe, vergleichende Vorlesung mit Fokus auf Browser-basierte Technologien.

      {{0}}
<div>

**Vorlesungsziele:**

1. **Paradigmen verstehen:** File, KV, Document, Column, Relational, Graph
2. **Relationale Datenbanken meistern:** SQL, Normalisierung, Transaktionen, Indexe
3. **Praktisch arbeiten:** DuckDB, SQLite, IndexedDB – alles im Browser
4. **Vergleichen & bewerten:** ACID, CAP, Trade-offs
5. **Anwenden:** Polyglot Persistence Projekt

> **Diese Vorlesung ist anders:** Browser-first, interaktiv, OER, spec-driven mit Copilot.

</div>

---

## Reflexion & Diskussion

    --{{0}}--
Nun sind Sie dran! Lassen Sie uns über Ihre Erfahrungen und Erwartungen sprechen.

      {{0}}
<div>

### Reflexionsfrage

> Was ist Ihnen bei Ihren bisherigen Erfahrungen mit Datenbanken begegnet?
>
> Haben Sie schon mit SQL, NoSQL, IndexedDB oder anderen Systemen gearbeitet?

**Mögliche Themen:**

- Welche Datenbanken haben Sie bereits verwendet?
- Was war besonders einfach oder schwierig?
- Welche Fragen sind offengeblieben?

</div>

      {{1}}
<div>

### Diskussion

> Welche Erwartungen haben Sie an diese Vorlesung?
>
> Was möchten Sie über Datenbanken lernen?

**Ideen für die Diskussion:**

1. Praktische Anwendung vs. theoretische Fundierung
2. Vergleich verschiedener Paradigmen
3. Performance-Optimierung
4. Neue Technologien (NoSQL, Distributed DBs)

</div>

---

## Referenzen & Quellen

### Projekte

- **cassandra_ros:** [http://mirror-ap.wiki.ros.org/cassandra_ros.html](http://mirror-ap.wiki.ros.org/cassandra_ros.html)
- **SelectScript:** [https://github.com/andre-dietrich/SelectScript](https://github.com/andre-dietrich/SelectScript)
- **Industrial eLab:** [Projektseite](https://www.wihoforschung.de/wihoforschung/de/bmbf-projektfoerderung/foerderlinien/forschung-zur-digitalen-hochschulbildung/erste-foerderlinie-zur-digitalen-hochschulbildung/industrial-elab/industrial-elab.html)
- **LiaScript:** [https://liascript.github.io/](https://liascript.github.io/)
- **Edrys-Lite:** [https://edrys-labs.github.io/](https://edrys-labs.github.io/)

### Publikationen (Industrial eLab)

- Hawlitschek, A., Berndt, S., Dietrich, A. & Zug, S. (2020). *Iterative Adaption eines Remote-Labors unter Berücksichtigung des Feedbacks der Studierenden*. In C. Terkowsky et al. (Hrsg.). *Labore in der Hochschullehre: Labordidaktik, Digitalisierung, Organisation*. wbv-Media.
- Hawlitschek, A., Köppen, V., Dietrich, A., & Zug, S. (2019). *Drop-out in programming courses – prediction and prevention*. *Journal of Applied Research in Higher Education*, 12(1), 124-136. [https://doi.org/10.1108/JARHE-02-2019-0035](https://doi.org/10.1108/JARHE-02-2019-0035)
- Hawlitschek, A., Krenz, T., & Zug, S. (2019). *When students get stuck: Adaptive remote labs as a way to support students in practical engineering education*. In D. Ifenthaler, D.-K. Mah, & J. Y.-K, Yau (Hrsg.). *Utilizing Learning Analytics to Support Study Success* (pp. 73-88), New York: Springer. [https://doi.org/10.1007/978-3-319-64792-0_5](https://doi.org/10.1007/978-3-319-64792-0_5)

### Weitere Links

- **LiaScript YouTube-Kanal:** [https://www.youtube.com/@liascript4180](https://www.youtube.com/@liascript4180)
- **LiaScript Dokumentation:** [https://liascript.github.io/course/?https://raw.githubusercontent.com/liaScript/docs/master/README.md](https://liascript.github.io/course/?https://raw.githubusercontent.com/liaScript/docs/master/README.md)

---

## Nächste Schritte

    --{{0}}--
Nach dieser Vorstellung starten wir in Session eins mit der eigentlichen Vorlesung.

      {{0}}
<div>

**Session 1 Vorschau:**

1. **Was sind Datenbanken?** – Grundbegriffe, Paradigmen, Einsatzszenarien
2. **Erste Hands-on-Beispiele** – CSV, JSON, IndexedDB im Browser
3. **DIKW-Pyramide** – Daten, Information, Wissen, Weisheit

> **Bereit für die Reise?** Lassen Sie uns gemeinsam Datenbanken "unlocken"! 🎓

</div>

---

*Willkommen zur Vorlesung "Databases Unlocked: A Beginner's Journey"!* 🚀
