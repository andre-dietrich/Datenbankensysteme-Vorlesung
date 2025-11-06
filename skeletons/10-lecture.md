# Session 10 – SQL Joins & Combining Data

> **Session-Typ:** Lecture  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)

---

## Zusammenfassung

Bisher haben Sie mit einzelnen Tabellen gearbeitet – SELECT, WHERE, GROUP BY, alles auf einer Tabelle. Aber die Macht relationaler Datenbanken liegt in Beziehungen: Kunden haben Bestellungen, Bestellungen haben Positionen, Produkte gehören zu Kategorien. Wie kombinieren Sie diese Daten?

**Joins** sind die Antwort. Sie verbinden Tabellen basierend auf gemeinsamen Spalten (meist Foreign Keys) und ermöglichen komplexe Analysen über mehrere Tabellen hinweg.

**Set-Operationen** (UNION, INTERSECT, EXCEPT) kombinieren Ergebnisse vertikal: „Zeige mir alle Kunden UND alle Lieferanten" oder „Welche Produkte sind in Kategorie A, aber NICHT in B?"

In dieser Session lernen Sie:

1. **INNER JOIN:** Nur übereinstimmende Datensätze (Standard-Fall)
2. **LEFT/RIGHT JOIN:** Alle Datensätze von einer Seite + Matches (häufig für „fehlende" Analysen)
3. **FULL OUTER JOIN:** Alle Datensätze von beiden Seiten (selten, aber mächtig)
4. **CROSS JOIN:** Kartesisches Produkt (alle Kombinationen)
5. **Self Joins:** Tabelle mit sich selbst verbinden (Hierarchien)
6. **Anti-Joins:** Fehlende Beziehungen finden (LEFT JOIN + IS NULL, NOT EXISTS, NOT IN)
7. **Set-Operationen:** UNION, INTERSECT, EXCEPT

**Bezug zur Agenda:** Nach dieser Session können Sie Multi-Table-Queries schreiben – das Herzstück relationaler Datenbanken. Sie verstehen, wann welcher Join-Typ passt, und können Daten aus verschiedenen Quellen kombinieren.

**Relevanz:** 90% aller SQL-Queries in Produktion nutzen Joins. Ohne Joins sind Sie auf isolierte Tabellen beschränkt – mit Joins erschließen Sie das volle Potenzial Ihrer Datenbank.

---

## Inhalte

### 1. Join-Grundlagen

#### Warum Joins?
- Normalisierung führt zu mehreren Tabellen
- Beziehungen über Foreign Keys
- Joins rekonstruieren die Informationen

#### Join-Syntax
- Explizit: `JOIN ... ON` (modern, empfohlen)
- Implizit: `FROM table1, table2 WHERE ...` (veraltet)
- USING-Klausel (wenn Spaltennamen gleich sind)

#### Join-Typen im Überblick
- INNER JOIN (nur Matches)
- LEFT/RIGHT JOIN (alle von einer Seite + Matches)
- FULL OUTER JOIN (alle von beiden Seiten)
- CROSS JOIN (kartesisches Produkt)

---

### 2. INNER JOIN

#### Konzept
- Nur Zeilen mit Match in beiden Tabellen
- Standard-Fall für Beziehungen (Kunde → Bestellung)
- NULL-Werte in Join-Spalte werden ignoriert

#### Syntax
- `SELECT ... FROM table1 INNER JOIN table2 ON table1.id = table2.foreign_id`
- `INNER` ist optional (JOIN = INNER JOIN)

#### Use Cases
- Kunden mit Bestellungen
- Produkte mit Kategorien
- Bestellungen mit Positionen

#### Multi-Table Joins
- Mehr als 2 Tabellen verbinden
- Reihenfolge wichtig für Performance

---

### 3. LEFT/RIGHT JOIN (OUTER JOIN)

#### LEFT JOIN
- Alle Zeilen aus linker Tabelle
- Matching Zeilen aus rechter Tabelle
- NULL für fehlende Matches

#### RIGHT JOIN
- Alle Zeilen aus rechter Tabelle
- Matching Zeilen aus linker Tabelle
- RIGHT JOIN = LEFT JOIN mit vertauschten Tabellen

#### Use Cases
- Kunden ohne Bestellungen finden
- Produkte ohne Verkäufe
- Fehlende Referenzdaten identifizieren

#### NULL-Handling
- IS NULL / IS NOT NULL für Filter
- COALESCE für Default-Werte

---

### 4. FULL OUTER JOIN

#### Konzept
- Alle Zeilen aus beiden Tabellen
- NULL für fehlende Matches auf beiden Seiten
- Symmetrische Erweiterung von LEFT/RIGHT

#### Use Cases
- Daten-Sync-Vergleich (Quelle vs. Ziel)
- Vollständige Inventur (alle Kategorien + alle Produkte)
- Gap-Analysen

#### Performance
- Oft langsamer als INNER/LEFT JOIN
- Alternativen: UNION von LEFT + RIGHT

---

### 5. CROSS JOIN

#### Konzept
- Kartesisches Produkt: Jede Zeile mit jeder Zeile
- Keine ON-Bedingung
- Ergebnis: rows(A) × rows(B)

#### Syntax
- Explizit: `CROSS JOIN`
- Implizit: `FROM table1, table2` (ohne WHERE)

#### Use Cases
- Alle Kombinationen generieren (Testdaten)
- Kalender × Produkte (Zeitreihen-Vorbereitung)
- Permutationen

#### Gefahr
- Explosion der Zeilenzahl (1000 × 1000 = 1 Mio!)
- Meist nur mit LIMIT sinnvoll

---

### 6. Self Joins

#### Konzept
- Tabelle mit sich selbst verbinden
- Aliase zwingend notwendig
- Für hierarchische Daten

#### Use Cases
- Mitarbeiter → Manager (beide in employees-Tabelle)
- Produkt → Vorgänger-Produkt
- Kategorie → Übergeordnete Kategorie

#### Rekursive Hierarchien
- Vorschau: WITH RECURSIVE (Session 13)
- Self Join zeigt nur eine Ebene

---

### 7. Anti-Joins (Fehlende Beziehungen finden)

#### Konzept
- "Zeige mir alle A, die KEIN B haben"
- Kunden ohne Bestellungen
- Produkte ohne Verkäufe
- Fehlende Referenzdaten

#### Methode 1: LEFT JOIN + IS NULL
- `LEFT JOIN ... WHERE right_table.id IS NULL`
- Klassischer Ansatz
- Einfach zu verstehen

#### Methode 2: NOT EXISTS (Subquery)
- `WHERE NOT EXISTS (SELECT 1 FROM ...)`
- Oft performanter
- Stoppt bei erstem Match

#### Methode 3: NOT IN (mit Vorsicht!)
- `WHERE id NOT IN (SELECT ...)`
- Gefahr bei NULL-Werten
- Meist vermeiden

#### Use Cases
- Kunden ohne Bestellungen (Inaktive identifizieren)
- Produkte ohne Verkäufe (Ladenhüter)
- Fehlende Übersetzungen
- Orphaned Records (Datenqualität)

#### Performance
- NOT EXISTS meist schneller als LEFT JOIN + IS NULL
- NOT IN problematisch bei NULL
- Index auf Join-Spalte wichtig

---

### 8. Set-Operationen

#### UNION
- Kombiniert Ergebnisse vertikal (Zeilen anhängen)
- UNION: Duplikate entfernen
- UNION ALL: Duplikate behalten (schneller)

#### INTERSECT
- Nur Zeilen, die in beiden Ergebnissen vorkommen
- Schnittmenge

#### EXCEPT (oder MINUS)
- Zeilen aus Ergebnis 1, die NICHT in Ergebnis 2 sind
- Differenzmenge

#### Bedingungen
- Gleiche Anzahl Spalten
- Kompatible Datentypen
- Spaltennamen aus erster Query

---

### 8. Join-Strategien & Performance

#### Join-Algorithmen (Übersicht)
- Nested Loop Join (klein × groß)
- Hash Join (groß × groß, gleichwertige Bedingung)
- Merge Join (sortierte Daten)

#### EXPLAIN & Query Plans
- Join-Reihenfolge analysieren
- Index-Nutzung prüfen
- Performance-Engpässe identifizieren

#### Best Practices
- Indexes auf Join-Spalten (Foreign Keys!)
- Kleinere Tabellen zuerst
- WHERE vor JOIN filtern (subqueries/CTEs)

---

### 9. Erweiterte Join-Techniken

#### JOIN mit mehreren Bedingungen
- `ON table1.id = table2.id AND table1.status = 'active'`
- Range Joins: `ON date BETWEEN start_date AND end_date`

#### JOIN mit Aggregation
- GROUP BY nach Join
- Aggregieren vor Join (Subqueries)

#### Non-Equi Joins
- `ON table1.price < table2.max_price`
- Range-Overlaps

---

## Aktivitäten

### Demo 1: INNER vs. LEFT JOIN
- Live-Coding: Customers ↔ Orders
- INNER: Nur Kunden mit Bestellungen
- LEFT: Alle Kunden, auch ohne Bestellungen
- Visualisierung: Venn-Diagramm

### Demo 2: Anti-Joins in der Praxis
- Methode 1: LEFT JOIN + IS NULL (Kunden ohne Bestellungen)
- Methode 2: NOT EXISTS (Produkte ohne Verkäufe)
- Methode 3: NOT IN (Vorsicht bei NULL!)
- Performance-Vergleich: EXPLAIN für alle 3 Methoden

### Demo 3: Multi-Table Join
- 3-4 Tabellen verbinden (Customers → Orders → OrderItems → Products)
- Schrittweise aufbauen
- Performance vergleichen (mit/ohne Indexes)

### Demo 4: Set-Operationen
- UNION: Aktive + inaktive Kunden
- INTERSECT: Produkte in beiden Kategorien
- EXCEPT: Produkte ohne Verkäufe

### Reflexionsfrage
> "Wann würden Sie LEFT JOIN statt INNER JOIN nutzen? Geben Sie 2 Beispiele."

### 1-Minute-Paper
> "Was ist der Unterschied zwischen UNION und UNION ALL? Welches ist schneller und warum?"

---

## Referenzen & Quellen

### Offizielle Dokumentation
- PostgreSQL Joins: https://www.postgresql.org/docs/current/tutorial-join.html
- DuckDB Joins: https://duckdb.org/docs/sql/query_syntax/from
- SQL Standard (ISO/IEC 9075)

### Visualisierungen
- SQL Joins Visualized: https://joins.spathon.com/
- Venn-Diagramme für Joins (klassisch, aber ungenau)
- Set Operations Visualizations

### Best Practices
- Use The Index, Luke: https://use-the-index-luke.com/sql/join
- Join Performance Tuning
- Query Optimization Patterns

### Weiterführend
- Subqueries & CTEs (Session 13)
- Window Functions (Session 12)
- Query Plans & EXPLAIN (Session 15)

---

## Notizen für Materialisierung

- **Praxis-First:** Alle Join-Typen mit Live-Beispielen (E-Commerce-Schema)
- **Venn-Diagramme:** Visualisierung von INNER/LEFT/RIGHT/FULL (aber Warnung: nicht präzise für NULL!)
- **Vergleichstabelle:** Join-Typen Matrix (Use Cases, Performance, NULL-Verhalten)
- **Performance-Demo:** EXPLAIN für verschiedene Join-Strategien
- **Anti-Pattern:** Häufige Fehler (falsches ON, kartesisches Produkt versehentlich)
- **Set-Operations:** Klare Abgrenzung zu Joins (vertikal vs. horizontal)
- **Übung E4:** Hands-on Joins & Set Operations (Multi-Table Queries)
