# Session 9 (Lecture)

## Titel

Session 9 – Database Normalization & Schema Design

## Zusammenfassung

Interaktive Session zum Thema Normalisierung: Von chaotischen "All-in-One" Tabellen zu sauberen, normalisierten Schemas. Studierende erleben Update-, Delete- und Insert-Anomalien live und entwickeln schrittweise ein normalisiertes Online-Shop-Schema. Fokus auf 1NF, 2NF, 3NF mit praktischem Refactoring.

## Lernziele

Nach dieser Session können Studierende:
- Datenbank-Anomalien (Update, Delete, Insert) erkennen und erklären
- Die drei Normalformen (1NF, 2NF, 3NF) verstehen und anwenden
- Ein denormalisiertes Schema schrittweise normalisieren
- Abwägungen zwischen Normalisierung und Denormalisierung treffen
- Ein funktionierendes Online-Shop-Schema mit korrekten Beziehungen erstellen

## Inhalte

### 1. Intro: Rückblick & Motivation (5 Min)
- Was haben wir in Session 8 gelernt? (DDL, DML, Constraints)
- Heute: Nicht WIE man Tabellen baut, sondern wie man GUTE Tabellen baut

### 2. Problem: Der chaotische Online-Shop (15 Min)
- Live-Demo: "All-in-One" Tabelle mit allen Daten
- Redundanz sichtbar machen
- Anomalien live erleben:
  - Update-Anomalie: Produktpreis in 100 Zeilen ändern
  - Delete-Anomalie: Letzten Kunden löschen → Produkt verschwindet
  - Insert-Anomalie: Produkt ohne Bestellung kann nicht eingefügt werden
- Diskussion: "Was läuft hier schief?"

### 3. Normalisierung: Theorie kompakt (15 Min)
- Was ist Normalisierung? Warum brauchen wir das?
- **Erste Normalform (1NF):**
  - Atomare Werte (keine Wiederholgruppen)
  - Jede Spalte enthält nur einen Wert
- **Zweite Normalform (2NF):**
  - Erfüllt 1NF
  - Keine partiellen Abhängigkeiten (nur relevant bei zusammengesetzten Schlüsseln)
- **Dritte Normalform (3NF):**
  - Erfüllt 2NF
  - Keine transitiven Abhängigkeiten (Nicht-Schlüssel-Attribute dürfen nicht voneinander abhängen)
- Visualisierung mit einfachen Beispielen

### 4. Interaktives Refactoring: Online-Shop normalisieren (40 Min)

**Schritt 1: Erste Normalform (1NF) – 10 Min**
- Problem zeigen: Spalte "products" enthält mehrere Werte
- Lösung entwickeln: Aufspalten in einzelne Zeilen
- Gemeinsam: CREATE TABLE statements schreiben
- Testen: Daten einfügen und vergleichen

**Schritt 2: Zweite Normalform (2NF) – 10 Min**
- Problem zeigen: Produktinformationen in jeder Bestellzeile dupliziert
- Lösung entwickeln: Separate `products` Tabelle
- Gemeinsam: Refactoring mit ALTER TABLE / CREATE TABLE
- Testen: UPDATE auf Produkt → alle Bestellungen aktualisiert

**Schritt 3: Dritte Normalform (3NF) – 10 Min**
- Problem zeigen: Kategorie-Informationen in `products` dupliziert
- Lösung entwickeln: Separate `categories` Tabelle
- Gemeinsam: Finale Tabellenstruktur erstellen
- ERD zeichnen (Mermaid)

**Schritt 4: Order Items Zwischentabelle (Many-to-Many) – 10 Min**
- Problem: Ein Produkt in mehreren Bestellungen, mehrere Produkte in einer Bestellung
- Lösung: `order_items` als Zwischentabelle
- Composite Primary Key demonstrieren
- Finale Schema-Version testen

### 5. Erweiterte Konzepte (10 Min)
- **Denormalisierung:** Wann & Warum?
  - Performance-Trade-offs
  - Read-heavy vs Write-heavy Systeme
  - Materialized Views (Ausblick)
- **BCNF & höhere Normalformen:** Kurze Erwähnung (optional)
- **Best Practice:** 3NF ist meist der Sweet Spot

### 6. Weitere Beispiele (5 Min)
- Blog-System (Posts, Authors, Comments, Tags)
- Bibliothek (Books, Authors, Copies, Loans)
- Social Network (Users, Friendships als Self-Referencing)

### 7. Zusammenfassung & Ausblick (5 Min)
- Was haben wir gelernt?
- Checkliste: "Ist mein Schema normalisiert?"
- Ausblick Session 10: Joins (mehrere normalisierte Tabellen kombinieren)

## Aktivitäten

### Interaktive Elemente
- **Live-Polling:** "Ist diese Tabelle in 2NF?" (Ja/Nein/Kommt drauf an)
- **Gruppen-Refactoring:** 5 Min Zeit, um eine chaotische Tabelle zu normalisieren
- **Fehler-Detektor:** Welche Anomalie entsteht hier? (Multiple Choice)
- **Schema-Evolution Live:** Schrittweises Refactoring gemeinsam entwickeln

### Hands-on
- Studierende schreiben CREATE TABLE Statements mit
- INSERT/UPDATE/DELETE Tests auf verschiedenen Normalisierungs-Stufen
- ERD gemeinsam zeichnen (Mermaid oder Whiteboard)

### Diskussion
- "Wann würdet ihr bewusst denormalisieren?"
- "Welche Performance-Probleme könnten durch Normalisierung entstehen?"

## Technische Anforderungen

- PGlite / DuckDB-Wasm für Browser-basierte SQL-Sandbox
- Mermaid für ERD-Visualisierung
- Vorbereitete Datensätze (CSV) für Online-Shop
- Live-Coding Setup mit sichtbarem Terminal

## Materialien

- Chaos-Tabelle als Startpunkt (vorausgefüllt)
- Schritt-für-Schritt Refactoring-Skripte
- Finale normalisierte Version als Referenz
- Checkliste "Normalisierung prüfen"
- Quiz mit typischen Normalisierungs-Fragen

## Referenzen & Quellen

- Codd, E.F. (1970): "A Relational Model of Data for Large Shared Data Banks"
- Date, C.J.: "Database Design and Relational Theory"
- Elmasri & Navathe: "Fundamentals of Database Systems" (Kapitel Normalisierung)
- PostgreSQL Documentation: Best Practices for Schema Design
- SQL Antipatterns (Bill Karwin) – Kapitel "Naive Trees" & "Polymorphic Associations"

## Notizen für Dozent:innen

- **Timing:** Interaktive Teile können länger dauern – Puffer einplanen
- **Backup-Plan:** Falls Zeit knapp wird, Schritt 4 (Order Items) optional/verkürzen
- **Vorbereitung:** Chaos-Tabelle mit vielen Duplikaten füllen (mindestens 20 Zeilen)
- **Interaktion fördern:** Regelmäßig fragen "Was würdet ihr jetzt tun?"
- **Fehlerkultur:** Bewusst schlechtes Design zeigen, dann gemeinsam verbessern
- **Visual Aid:** ERD nach jedem Refactoring-Schritt aktualisieren
- **Overflow:** Falls Session 8 überzogen hat, kurz wiederholen: PRIMARY KEY, FOREIGN KEY

## Logo - Prompt

Wide aspect 16:9 flat minimal educational tech illustration. Mittelpunkt: stilisierte Transformation von chaotisch zu strukturiert – links eine ungeordnete, überladene Tabelle (0NF: alle Daten durcheinander, Redundanz-Markierungen in Rot), die sich über 3 Stufen nach rechts hin zu einem sauberen, normalisierten ER-Diagramm (3NF) entwickelt: 1) Links "0NF": chaotische Tabelle mit vielen duplizierten Zeilen, rote Warnzeichen (❌), 2) Mitte: Zwischenstufe mit aufgeteilten Tabellen (1NF → 2NF), gelbe Pfeile zeigen Aufteilung, 3) Rechts "3NF": sauberes ER-Diagramm mit 3-4 verbundenen Entitäten (Rechtecke: USER, ORDER, PRODUCT), grüne Häkchen (✅), klare Beziehungslinien (1:1, 1:N, N:M). Oben über der Transformation: 3 große Zahlen "1 → 2 → 3" (für 1NF, 2NF, 3NF) mit Fortschrittsbalken darunter. Unten: stilisiertes Twitter-Vogel-Icon (vereinfacht) mit ER-DiagWide aspect 16:9 flat minimal educational tech illustration. Mittelpunkt: stilisierte Transformation von chaotisch zu strukturiert – links eine ungeordnete, überladene Tabelle (0NF: alle Daten durcheinander, Redundanz-Markierungen in Rot), die sich über 3 Stufen nach rechts hin zu einem sauberen, normalisierten ER-Diagramm (3NF) entwickelt:

1) Links "0NF": chaotische Tabelle mit vielen duplizierten Zeilen, rote Warnzeichen (❌),
2) Mitte: Zwischenstufe mit aufgeteilten Tabellen (1NF → 2NF), gelbe Pfeile zeigen Aufteilung,
3) Rechts "3NF": sauberes ER-Diagramm mit 3-4 verbundenen Entitäten (Rechtecke: USER, ORDER, PRODUCT), grüne Häkchen (✅), klare Beziehungslinien (1:1, 1:N, N:M).

Oben über der Transformation: 3 große Zahlen "1 → 2 → 3" (für 1NF, 2NF, 3NF) mit Fortschrittsbalken darunter. Unten: stilisiertes Twitter-Vogel-Icon (vereinfacht) mit ER-Diagramm-Knotenpunkten um ihn herum (Andeutung: Twitter-Modellierung). Hintergrund: subtiler Datenfluss von links (chaotisch, geschwungene Linien) nach rechts (strukturiert, gerade Linien). Schriftzug (optional) "Session 9: Normalisierung & ER" dezent, sans-serif, unten rechts. Farbschema: Petrol (#0B6E75 – ER-Diagramm-Entitäten), Warm Orange (#FF8C42 – Highlights auf 3NF/Erfolg), Red (#E63946 – 0NF-Probleme), Yellow (#F4A261 – Zwischenstufen), Sand (#F2E9DC – Background), Dark Gray (#333 – Tabellenlinien), Off-White (#F9F9F9 – Flächen). Keine Gradients, klare Konturen, weiche Rundungen, hoher Kontrast, kein Photorealismus, educational diagram style, clean edges, negative space sinnvoll nutzen.