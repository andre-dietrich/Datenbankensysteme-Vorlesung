# Session 11 (Lecture)

## Titel

Session 11 – Transaktionen & ACID (formal) (Lecture)

## Zusammenfassung

Atomicität, Konsistenz, Isolation, Durability (formalisiert). Detaillierte Betrachtung der ACID-Eigenschaften und deren Bedeutung für Datenbankintegrität.

## Inhalte

- Transaktionskonzept: BEGIN, COMMIT, ROLLBACK
- ACID-Eigenschaften (formal):
  - **Atomicity**: Alles oder nichts (All-or-Nothing)
  - **Consistency**: Integritätsbedingungen erhalten
  - **Isolation**: Transaktionen beeinflussen sich nicht
  - **Durability**: Committete Änderungen überleben Systemausfälle
- Isolation Levels (Überblick):
  - READ UNCOMMITTED
  - READ COMMITTED
  - REPEATABLE READ
  - SERIALIZABLE
- Anomalien:
  - Dirty Read
  - Non-Repeatable Read
  - Phantom Read
  - Lost Update
- Use Cases: Banküberweisung, Ticketbuchung, Inventory Management

## Aktivitäten

- Szenario-Durchspiel: Banküberweisung mit/ohne Transaktion
- Diskussion: Was passiert bei Crash zwischen zwei Updates?
- Vorbereitung E5: Isolation Level Experimente

## Referenzen & Quellen

- "Transaction Processing" (Gray & Reuter)
- SQL Standard (Transaction Isolation Levels)
- PostgreSQL Transaction Documentation
