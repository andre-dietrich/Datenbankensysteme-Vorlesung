# Session 17 (Lecture)

## Titel

Session 17 – RESTful APIs & SQL: Online-Shop Backend

## Zusammenfassung

Einführung in RESTful APIs mit praktischem Fokus auf HTTP → SQL Mapping. Studierende lernen, wie REST-Requests (GET, POST, DELETE) in SQL-Queries (SELECT, INSERT, DELETE) übersetzt werden. Hands-on Übungen mit simulierter Browser-API, die SQL in PGlite ausführt. Praktische Erfahrung mit CRUD-Operationen, Joins, Error-Handling und Response-Formatierung im E-Commerce-Kontext.

## Inhalte

### Teil 1: Was ist eine REST-API? (15 Min)
- REST-Prinzipien (Representational State Transfer)
- HTTP-Methoden: GET, POST, PUT, DELETE
- Status Codes: 200, 201, 404, 400, 500
- JSON als Datenformat
- Live-Demo mit echter API (Fake Store API)

### Teil 2: HTTP → SQL Mapping (15 Min)
- CRUD-Mapping:
  - GET → SELECT
  - POST → INSERT
  - PUT → UPDATE
  - DELETE → DELETE
- Ressourcen vs. Tabellen
- URL-Parameter → WHERE-Bedingungen
- Request Body → SQL-Values
- Response-Formatierung

### Teil 3: Setup & Architektur (10 Min)
- fetch-Override Konzept (vorgegeben)
- `http://little-amazon.com` als lokale API
- PGlite Integration
- Error-Handling Strategie
- JSON Response-Format

### Teil 4: Hands-on SELECT Queries (20 Min)
- **Aufgabe 1**: Alle Produkte laden (einfaches SELECT)
- **Aufgabe 2**: Produkt nach ID (WHERE-Bedingung)
- **Aufgabe 3**: Produkte einer Kategorie (JOIN)
- **Aufgabe 4**: Kunden mit Bestellungen (JOIN, Aggregation)
- Frontend: Produktliste als Tabelle

### Teil 5: Hands-on INSERT Queries (15 Min)
- **Aufgabe 5**: Neues Produkt hinzufügen
- **Aufgabe 6**: Neuen Kunden anlegen
- Request Body → SQL VALUES
- RETURNING Clause für neue IDs
- Frontend: Formular mit Response-Anzeige

### Teil 6: Hands-on DELETE Queries (10 Min)
- **Aufgabe 7**: Produkt löschen
- **Aufgabe 8**: Kunde löschen (CASCADE-Überlegung)
- Frontend: Mini-Shop mit Löschen-Button

### Teil 7: Error-Handling (10 Min)
- 404: Ressource nicht gefunden
- 400: Ungültige Daten (z.B. negativer Preis)
- 500: SQL-Fehler (Foreign Key Constraint)
- Try-Catch in SQL-Ausführung

### Wrap-up (5 Min)
- Best Practices (SQL Injection Warnung, Prepared Statements)
- REST vs. GraphQL (Ausblick)
- Real-World APIs (Authentifizierung, Rate Limiting)

## Aktivitäten

- Live-Demo: Fake Store API im Browser erkunden
- Code-Along: fetch-Override Setup verstehen
- Hands-on Übungen: 8 SQL-Aufgaben mit TODO-Platzhaltern
- Mini-Frontends: 
  1. Produktliste (Tabelle)
  2. Produkt hinzufügen (Formular)
  3. Mini-Shop (Cards mit DELETE-Button)
- Error-Testing: Bewusst Fehler provozieren

## Didaktischer Ansatz

- **Motivation**: Live-Demo mit echter API (Fake Store) zeigt Relevanz
- **Scaffolding**: fetch-Override vorgegeben, Fokus auf SQL
- **Progressive Complexity**: SELECT → INSERT → DELETE
- **Immediate Feedback**: Frontends visualisieren SQL-Ergebnisse direkt
- **Error-First**: Studierende lernen Error-Handling durch Experimentieren
- **Real-World Connection**: E-Commerce-Schema = realistische Business-Logik

## Lernziele

1. REST-Prinzipien verstehen (HTTP-Methoden, Status Codes)
2. HTTP-Requests zu SQL-Queries mappen können
3. SELECT-Queries für verschiedene Use-Cases schreiben (WHERE, JOIN, Aggregation)
4. INSERT-Queries mit Request-Body-Daten erstellen
5. DELETE-Queries mit CASCADE-Implikationen verstehen
6. Error-Handling in API-Kontext anwenden
7. JSON-Response-Formatierung kennenlernen

## Technische Vorbereitung

- PGlite Template (bereits aus L13 vorhanden)
- Fake Store API: https://fakestoreapi.com
- Online-Shop Schema (aus L13 wiederverwenden)
- fetch-Override Script (wird vorgegeben)
- 3 Mini-Frontends (HTML/JavaScript)

## Referenzen & Quellen

- Fake Store API: https://fakestoreapi.com
- REST API Design Best Practices (Roy Fielding)
- MDN Web Docs: Fetch API
- HTTP Status Codes (RFC 7231)
- SQL Injection Prevention (OWASP)
