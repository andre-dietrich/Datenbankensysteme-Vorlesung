# Session 13 – Advanced SQL: SET Operations & Views (Lecture)

> **Professor-Persona:** Praxisorientierter Architekt mit Analyse-Coach-Elementen  
> **Stil:** Klar & Praxisfokussiert + Analytisch Reflexiv  
> **Didaktik:** Live-Coding, praktische Beispiele, Vergleichstabellen

## Zusammenfassung

Diese Session erweitert Ihr SQL-Arsenal um fortgeschrittene Techniken: **SET Operations** (UNION, INTERSECT, EXCEPT) für Mengenlehre auf Datenbanken und **Views** für wiederverwendbare, abstrakte Abfragen.

Wir arbeiten weiterhin mit der **IMDB-Datenbank** und zeigen, wie diese Features L12 (Indexe) ergänzen: SET Operations haben eigene Optimierungsstrategien, Views können Indexe der Basistabellen nutzen und komplexe Queries elegant kapseln.

**Bezug zur Agenda:**
- Aufbauend auf L11-L12: Fortgeschrittene Analysen auf optimierten Datenbanken
- Didaktisches Konzept: Praxisfokussiert + Analytisch Reflexiv
- Vergleichsdenken: Wann welches Feature nutzen?

## Inhalte

### 1. SET Operations – Mengenlehre für SQL

**Konzept:**
- UNION, INTERSECT, EXCEPT – Mathematische Mengenoperationen
- Venn-Diagramm-Visualisierung

**UNION / UNION ALL:**
```sql
-- Alle Filme + alle Serien (ohne Duplikate)
SELECT primaryTitle, 'movie' AS type FROM title_basics WHERE titleType = 'movie'
UNION
SELECT primaryTitle, 'series' AS type FROM title_basics WHERE titleType = 'tvSeries';

-- Mit Duplikaten (schneller)
UNION ALL
```

**INTERSECT:**
```sql
-- Personen, die sowohl Schauspieler als auch Regisseur sind
SELECT nconst FROM name_basics WHERE primaryProfession LIKE '%actor%'
INTERSECT
SELECT nconst FROM name_basics WHERE primaryProfession LIKE '%director%';
```

**EXCEPT:**
```sql
-- Alle Titel ohne Ratings
SELECT tconst FROM title_basics
EXCEPT
SELECT tconst FROM title_ratings;
```

**Performance-Hinweise:**
- UNION entfernt Duplikate → langsamer als UNION ALL
- SET Ops nutzen oft Sorts → Indexe helfen
- Spalten müssen kompatibel sein (gleiche Anzahl, passende Typen)

---

### 2. Views – Abstraktion & Wiederverwendung

**Konzept:**
- Was sind Views? Gespeicherte SELECT-Statements
- Anwendungsfälle: Wiederverwendung, Sicherheit, Abstraktion
- CREATE VIEW, DROP VIEW

**Praktisches Beispiel:**
```sql
-- View für hochbewertete Filme
CREATE VIEW top_rated_movies AS
SELECT tb.primaryTitle, tr.averageRating, tb.startYear
FROM title_basics tb
JOIN title_ratings tr ON tb.tconst = tr.tconst
WHERE tr.averageRating > 8.0 AND tb.titleType = 'movie';

-- View nutzen wie eine Tabelle
SELECT * FROM top_rated_movies WHERE startYear > '2010';
```

**Views & SET Operations kombinieren:**
```sql
-- Komplexe UNION-Query als View speichern
CREATE VIEW all_content AS
  SELECT primaryTitle, 'movie' AS type, startYear FROM title_basics WHERE titleType = 'movie'
  UNION ALL
  SELECT primaryTitle, 'series' AS type, startYear FROM title_basics WHERE titleType = 'tvSeries';

-- View wiederverwenden
SELECT * FROM all_content WHERE startYear > '2020';
```

**Trade-offs:**
- ✅ Vorteile: Code-Reuse, Zugriffskontrolle, Kapselung, Vereinfachung komplexer Queries
- ⚠️ Nachteile: Keine eigenen Daten, Performance-Fallstricke (bei komplexen Views)

**Views & Indexe:**
- Views nutzen Indexe der Basistabellen
- Materialized Views (Ausblick): Eigene Indexe möglich

---

### 3. Vergleich & Best Practices

**Wann welches Feature?**

| Anforderung | Empfehlung | Warum? |
|-------------|-----------|--------|
| Wiederverwendbare Query | VIEW | Code-Reuse, Abstraktion |
| Zwei Ergebnismengen kombinieren | UNION | Mengenoperation |
| Gemeinsame Elemente finden | INTERSECT | Schnittmenge |

**Performance-Matrix:**

| Feature | Index-Nutzung | Sortierung nötig? | Trade-offs |
|---------|---------------|-------------------|------------|
| VIEW | Ja (Basistabellen) | Abhängig | Performance wie Basistabelle |
| UNION | Ja | Ja (Deduplizierung) | UNION ALL schneller |
| INTERSECT | Ja | Ja | Kann teuer werden |
| EXCEPT | Ja | Ja | Wie INTERSECT |

---

## Aktivitäten

### Aktivität 1: SET Operations kombinieren (15 Min)

**Szenario:** Analyse der IMDB-Datenbank

**Fragen:**
1. Wie viele Titel haben **kein** Rating? (EXCEPT)
2. Welche Personen sind Schauspieler **und** Regisseur? (INTERSECT)
3. Kombinieren Sie alle Filme und Serien mit UNION – wie viele Einträge?

**Bonus:** Warum ist UNION ALL schneller? (EXPLAIN ANALYZE nutzen)

---

### Aktivität 2: Views für Abstraktion nutzen (10 Min)

**Aufgabe:**
1. Speichern Sie eine der SET Operations aus Aktivität 1 als View
2. Erstellen Sie eine weitere View für eine häufige Query aus L11
3. Kombinieren Sie beide Views in einer neuen Query

**Reflexion:** Wann würden Sie Views in Production einsetzen? Welche Vorteile sehen Sie?

---

## Referenzen & Quellen

### SET Operations
- SQL Standard: UNION, INTERSECT, EXCEPT
- Performance Tips: UNION vs. UNION ALL
- Venn-Diagramme für visuelle Erklärung

### Views
- PostgreSQL: CREATE VIEW
- SQLite: Views Documentation
- Best Practices: When to use Views vs. Materialized Views

---

## Nächste Schritte

**Ausblick:**
- Materialized Views (bei großen Datenmengen)
- Rekursive CTEs (falls noch nicht in L10)
- User-Defined Functions (UDFs)

**Hausaufgabe (optional):**
1. Kombinieren Sie alle drei SET Operations (UNION, INTERSECT, EXCEPT) in einer komplexen Query
2. Erstellen Sie 3 Views: eine für eine SET Operation, zwei für typische Analysen
3. Bauen Sie eine finale Query, die alle drei Views kombiniert

---

**Lernziel-Check:**
- [ ] UNION, INTERSECT, EXCEPT verstehen und anwenden
- [ ] Views erstellen und sinnvoll einsetzen
- [ ] SET Operations und Views kombinieren
- [ ] Performance-Implikationen verstehen
- [ ] Best Practices: Wann welches Feature?

