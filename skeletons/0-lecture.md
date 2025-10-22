# Session 0 – Vorstellung: Mein Weg zu Datenbanken & interaktivem OER

> **Session-Typ:** Einführung / Vorstellung (keine vollständige Vorlesung)  
> **Dauer:** ca. 30–45 Minuten  
> **Fokus:** Persönlicher Background, technologische Reise, Motivation für diese Vorlesung

---

## Zusammenfassung

In dieser Session stelle ich mich vor – **André Dietrich**, Ihr Dozent für diese Vorlesung. Ich gebe Ihnen einen Einblick in meinen akademischen und beruflichen Werdegang, von meiner Promotion in eingebetteten Systemen und Robotik über meine Arbeit mit verteilten Datenbanksystemen bis hin zur Entwicklung interaktiver Lehr- und Lernmaterialien. 

Dabei erzähle ich, wie meine Leidenschaft für **Programmiersprachen, Datenbankparadigmen und Web-Technologien** mich zu Projekten wie **LiaScript**, **SelectScript**, **cassandra_ros**, **Industrial eLab** und **Edrys-Lite** geführt hat – und warum ich überzeugt bin, dass **interaktive Open Educational Resources (OER)** die Zukunft des Lernens sind.

Diese Session ist **kein Pflichtbestandteil der Vorlesung**, sondern eine persönliche Einladung, meinen Hintergrund kennenzulernen und zu verstehen, warum diese Vorlesung so ist, wie sie ist.

---

## Inhalte

### 1. Über mich – André Dietrich

**Promotion: Eingebettete Systeme & Robotik**

- Promoviert in **Embedded Systems und Robotics** an der Otto-von-Guericke-Universität Magdeburg
- Fokus meiner Dissertation: **Internet of Things (IoT)** und **Zugriff auf verteilte Systeme**
- Motivation: Wie können wir große Mengen an Sensordaten aus verschiedenen Quellen effizient sammeln, speichern und abfragen?

**Interesse: Programmiersprachen & Paradigmen**

- Während der Promotion: Faszination für **deklarative Programmiersprachen** und **Datenbankparadigmen**
- Frage: Wie können wir Daten **holistisch** und **intuitiv** zugänglich machen – ohne uns in technischen Details zu verlieren?

---

### 2. Meine Projekte: Von NoSQL zu OER

#### **cassandra_ros – NoSQL & Sensordaten**

- **Projekt:** ROS-Adapter für Apache Cassandra (NoSQL Column Store)
- **Ziel:** Sensorsignale aus Robotern in einer verteilten Datenbank speichern
- **Technologie:** Cassandra als **NoSQL-Datenbank** mit **CQL (Cassandra Query Language)**
- **Link:** [cassandra_ros Wiki](http://mirror-ap.wiki.ros.org/cassandra_ros.html)

**Was ich gelernt habe:**

- **Column Stores** bieten flexible Schemas und horizontale Skalierbarkeit
- **CQL** ermöglicht SQL-ähnliche Abfragen auf NoSQL-Systemen
- **Trade-offs:** Eventual Consistency vs. starke Konsistenz (CAP-Theorem)

---

#### **SelectScript – Deklarative Abfragesprache**

- **Projekt:** Eine **Lua-ähnliche, eingebettete Programmiersprache** für Simulationsumgebungen
- **Besonderheit:** **SELECT-Statements** für Problemlösung (nicht nur Datenabfragen!)
- **Anwendung:** Rekursive Abfragen, hierarchische Strukturen, robotische Weltmodelle
- **Link:** [SelectScript auf GitHub](https://github.com/andre-dietrich/SelectScript)

**Was ich gelernt habe:**

- **Deklarative Sprachen** ermöglichen intuitive Problemlösung
- **SQL-ähnliche Syntax** kann über klassische Datenbanken hinausgehen
- **Rekursive Queries** sind mächtiger, als man denkt (z. B. Türme von Hanoi, Graphtraversierung)

---

#### **Industrial eLab – Remote Labs & Web-Technologien**

- **Projekt:** BMBF-gefördertes Projekt (2017–2020) für **Remote Labs** in der Ingenieurausbildung
- **Technologie:** **Elixir Backend** + **Elm Frontend** + **WebRTC**
- **Ziel:** Studierende arbeiten zeit- und ortsunabhängig mit realer Hardware (Roboter, Mikrocontroller)
- **Link:** [Industrial eLab Projektseite](https://www.wihoforschung.de/wihoforschung/de/bmbf-projektfoerderung/foerderlinien/forschung-zur-digitalen-hochschulbildung/erste-foerderlinie-zur-digitalen-hochschulbildung/industrial-elab/industrial-elab.html)

**Was ich gelernt habe:**

- **Browser als Betriebssystem:** Moderne Web-Technologien (WebRTC, IndexedDB, Service Workers) ermöglichen komplexe Anwendungen
- **Offline-Fähigkeit & Persistenz:** Progressive Web Apps (PWAs) mit **IndexedDB** und **Caching**
- **Didaktische Herausforderung:** Wie gestalten wir adaptive Lernumgebungen, die Studierende beim Problemlösen unterstützen?

**Entstehung von LiaScript:**

Aus diesem Projekt entstand die Idee für **LiaScript** – eine Markdown-basierte Beschreibungssprache für **interaktive Lehr- und Lernmaterialien**.

---

#### **LiaScript – Interaktive OER im Browser**

- **Projekt:** Open-Source-Projekt für **interaktive Kurse in Markdown**
- **Vision:** Lehrende erstellen Kurse als **einfache Textdateien** (z. B. auf GitHub), ohne Build-Steps oder CMS
- **Features:**
  - **Multimedia:** Videos, Audio, ASCII-Diagramme, Mermaid, LaTeX
  - **Interaktion:** Quizze, Live-Coding (JavaScript, Python, SQL), TTS (Text-to-Speech)
  - **Kollaboration:** WebRTC-basierte Klassenräume (Peer-to-Peer)
  - **Persistenz:** IndexedDB für Offline-Fähigkeit und Fortschritt speichern
- **Link:** [LiaScript Homepage](https://liascript.github.io/)

**Technologien:**

- **IndexedDB** für lokale Datenhaltung
- **Service Workers** für Offline-Caching
- **WebRTC** für Peer-to-Peer-Kommunikation (collaborative classrooms)

**Was ich gelernt habe:**

- **Browser-basierte Datenbanken** (IndexedDB) sind mächtig, aber anders als traditionelle SQL-Datenbanken
- **NoSQL im Browser:** Object Stores, Key-Value Zugriffe, Indexierung
- **Trade-offs:** Flexibilität vs. strukturierte Abfragen

---

#### **Selbständiger Elm-Entwickler – Linked Data & SPARQL**

- **Projekt:** Web-Entwicklung für Linked Data Anwendungen
- **Technologie:** **Elm Frontend** + **Semantic Web** + **SPARQL**
- **Datenbank:** RDF-Stores (Triple Stores) für **Wissensgraphen**

**Was ich gelernt habe:**

- **Graphdatenbanken** sind ideal für vernetzte, semantische Daten
- **SPARQL** ist SQL für Graphen – aber mit eigenen Herausforderungen
- **RDF/Linked Data:** Flexibel, aber komplex zu modellieren

---

#### **CrossLab & Edrys-Lite – Peer-to-Peer Remote Labs**

- **Projekt:** Dezentrales, Peer-to-Peer-System zum Teilen von Remote Labs
- **Technologie:** **WebRTC** für direkte Browser-zu-Browser-Kommunikation (ohne zentralen Server)
- **Ziel:** Lehre und Labore **dezentral** organisieren – jeder Browser ist ein potenzieller "Server"
- **Link:** [Edrys-Lite](https://edrys-labs.github.io/)

**Was ich gelernt habe:**

- **Dezentrale Architekturen:** Peer-to-Peer reduziert Abhängigkeiten von zentralen Servern
- **Browser-Technologien:** WebRTC, WebSockets, IndexedDB ermöglichen verteilte Anwendungen
- **Trade-offs:** Konsistenz vs. Verfügbarkeit (CAP-Theorem in der Praxis)

---

### 3. Meine Motivation für diese Vorlesung

**Interaktive OER als Lernformat**

- Ich bin überzeugt: **Interaktive Materialien** (Quizze, Live-Coding, Visualisierungen) fördern das Verständnis
- LiaScript ermöglicht es, **direkt im Browser** mit Datenbanken zu arbeiten (DuckDB, SQLite, IndexedDB)
- **Kein Setup, kein Installieren** – nur Browser öffnen und loslegen

**Spec-Driven Development mit GitHub Copilot**

- Ich nutze **GitHub Copilot** als Co-Autor für diese Vorlesung
- Ansatz: **Spec-Driven Development** – ich definiere Struktur, Lernziele, Didaktik; Copilot hilft bei Inhalten
- **Experiment:** Wie kann KI Lehrende bei der Erstellung von OER unterstützen?

**Aktuelle Rolle**

- Dozent für **Datenbanken** im Wintersemester 2025/26 an der TU Bergakademie Freiberg
- Ziel: Eine **praxisnahe, vergleichende Vorlesung** mit Fokus auf **Browser-basierte Technologien**

---

## Aktivitäten

**Reflexionsfrage (optional):**

> Was ist Ihnen bei Ihren bisherigen Erfahrungen mit Datenbanken begegnet? Haben Sie schon mit SQL, NoSQL, IndexedDB oder anderen Systemen gearbeitet?

**Diskussion (optional):**

> Welche Erwartungen haben Sie an diese Vorlesung? Was möchten Sie über Datenbanken lernen?

---

## Referenzen & Quellen

### Projekte

- **cassandra_ros:** [http://mirror-ap.wiki.ros.org/cassandra_ros.html](http://mirror-ap.wiki.ros.org/cassandra_ros.html)
- **SelectScript:** [https://github.com/andre-dietrich/SelectScript](https://github.com/andre-dietrich/SelectScript)
- **Industrial eLab:** [https://www.wihoforschung.de/wihoforschung/de/bmbf-projektfoerderung/foerderlinien/forschung-zur-digitalen-hochschulbildung/erste-foerderlinie-zur-digitalen-hochschulbildung/industrial-elab/industrial-elab.html](https://www.wihoforschung.de/wihoforschung/de/bmbf-projektfoerderung/foerderlinien/forschung-zur-digitalen-hochschulbildung/erste-foerderlinie-zur-digitalen-hochschulbildung/industrial-elab/industrial-elab.html)
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

Nach dieser Vorstellung starten wir in **Session 1** mit der eigentlichen Vorlesung:

1. **Was sind Datenbanken?** – Grundbegriffe, Paradigmen, Einsatzszenarien
2. **Erste Hands-on-Beispiele** – CSV, JSON, IndexedDB im Browser

---

*Ende Session 0 – Willkommen zur Vorlesung!* 🎓
