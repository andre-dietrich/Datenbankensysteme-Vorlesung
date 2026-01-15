# Session 14 (Lecture)

## Titel

Session 14 – Transaktionen & ACID (Lecture)

## Zusammenfassung

Transaktionen gewährleisten Datenkonsistenz bei konkurrierenden Zugriffen und Systemausfällen. Diese Session führt szenariobasiert in ACID-Eigenschaften, Transaktionssteuerung (BEGIN/COMMIT/ROLLBACK) und Isolation Levels ein – mit praktischen Beispielen aus Ticketbuchung und Geldüberweisung.

## Inhalte

### 1. Motivation: Warum Transaktionen?
- **Szenario**: Geldüberweisung zwischen Konten
- Probleme ohne Transaktionen:
  - Inkonsistente Zwischenzustände (Geld doppelt/verschwunden)
  - Systemausfall während Operation
  - Konkurrierende Zugriffe (zwei Buchungen parallel)
- **Definition**: Transaktion = logische Arbeitseinheit ("alles oder nichts")

### 2. ACID-Eigenschaften
- **Atomicity** (Atomarität): Ganz oder gar nicht
- **Consistency** (Konsistenz): Gültige Zustände vor/nach Transaktion
- **Isolation** (Isolation): Transaktionen beeinflussen sich nicht
- **Durability** (Dauerhaftigkeit): Bestätigte Änderungen sind persistent
- Metapher: "Paket mit Garantiesiegel"

### 3. Transaktionssteuerung in SQL
- `BEGIN` / `START TRANSACTION`
- `COMMIT` – Änderungen bestätigen
- `ROLLBACK` – Änderungen zurückrollen
- `SAVEPOINT` – Teilweise Rollbacks
- **Live-Demo**: Geldüberweisung mit/ohne COMMIT

### 4. Isolation Levels (szenariobasiert)
Probleme bei parallelen Transaktionen:
- **Dirty Read**: Lese uncommitted Daten
- **Non-Repeatable Read**: Zweites Lesen gibt anderen Wert
- **Phantom Read**: Zweites Lesen findet neue Zeilen
- **Lost Update**: Überschreiben von Änderungen

Isolation Levels (von schwach zu stark):
1. `READ UNCOMMITTED` – Keine Isolation
2. `READ COMMITTED` – Nur committete Daten (Standard bei PostgreSQL)
3. `REPEATABLE READ` – Snapshot innerhalb Transaktion
4. `SERIALIZABLE` – Vollständige Isolation (wie sequentiell)

**Trade-off**: Stärkere Isolation = mehr Locking = weniger Concurrency

### 5. Praktische Beispiele
- **Ticketbuchung**: Verhindere Doppelbuchung
- **Inventarverwaltung**: Konsistente Bestandsänderungen
- **Multi-Step Operations**: INSERT + UPDATE atomar

### 6. Deadlocks (Einführung)
- **Definition**: Zwei Transaktionen warten gegenseitig aufeinander
- **Erkennung**: Datenbank bricht eine Transaktion ab
- **Vermeidung**: Konsistente Lock-Reihenfolge
- Hinweis: Details in L15 (Performance)

### 7. Best Practices
- Transaktionen kurz halten (Locks minimieren)
- Explizites COMMIT/ROLLBACK (kein Autocommit in Produktionscode)
- Passenden Isolation Level wählen (Standard meist ausreichend)
- Fehlerbehandlung mit ROLLBACK

## Aktivitäten

### Demo 1: Geldüberweisung ohne/mit Transaktion
- Zeige Inkonsistenz bei Fehler ohne BEGIN/COMMIT
- Mit Transaktion: ROLLBACK nach Fehler

### Demo 2: Isolation Levels
- Zwei parallele Sessions (Split-Screen)
- Lost Update demonstrieren (READ COMMITTED vs. SERIALIZABLE)

### Übung: Szenario-Analyse
Gegeben: 3 Szenarien (E-Commerce Checkout, Banktransfer, Sitzplatzreservierung)
- Welche ACID-Eigenschaft ist verletzt?
- Welcher Isolation Level ist minimal nötig?

### Diskussion
- Wann sind Transaktionen übertrieben? (Read-only, Analytics)
- Trade-off zwischen Konsistenz und Performance

## Referenzen & Quellen

- PostgreSQL Documentation: Transaction Isolation
- "Designing Data-Intensive Applications" (Martin Kleppmann) – Kapitel 7
- SQL Standard: ISO/IEC 9075 (Transaction Management)
- Praktische Isolation Level Tests: https://www.postgresql.org/docs/current/transaction-iso.html
