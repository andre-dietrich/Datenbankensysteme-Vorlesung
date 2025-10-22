# Session 15 (Lecture)

## Titel

Session 15 – Locking vs. MVCC (Lecture)

## Zusammenfassung

Pessimistic/Optimistic Locking, Snapshot Isolation. Nebenläufigkeitsstrategien und deren Auswirkungen auf Performance und Konsistenz.

## Inhalte

- Nebenläufigkeitsprobleme (Wiederholung aus L11):
  - Lost Update, Dirty Read, Non-Repeatable Read, Phantom Read
- Locking-Strategien:
  - **Pessimistic Locking**: Sperren vor Zugriff (Shared/Exclusive Locks)
  - **Optimistic Locking**: Versionsprüfung bei COMMIT
  - Deadlocks: Entstehung & Auflösung
- Multi-Version Concurrency Control (MVCC):
  - Grundprinzip: Jede Transaktion sieht Snapshot
  - Versionskette, Garbage Collection
  - Vorteile: Lesezugriffe ohne Sperren
  - Nachteile: Write Skew, Phantom Reads möglich
- Isolation Levels Vertiefung:
  - SERIALIZABLE (echte Serialisierung)
  - REPEATABLE READ (MVCC-basiert)
- Performance Trade-offs: Locking vs. MVCC

## Aktivitäten

- Szenario-Durchspiel: Zwei konkurrierende Transaktionen
- Vergleich: Pessimistic vs. Optimistic (Vor/Nachteile)
- Diskussion: Wann welche Strategie?

## Referenzen & Quellen

- PostgreSQL MVCC Documentation
- "Concurrency Control and Recovery" (Bernstein & Goodman)
- Deadlock Detection Algorithms
