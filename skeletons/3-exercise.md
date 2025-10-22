# Session 3 (Exercise)

## Titel

Session 3 – Sync & Konflikte (IndexedDB/PouchDB) (Exercise)

## Zusammenfassung

Offline-fähige Replikation eines einfachen Datensets und Simulation konkurrierender Updates. Untersuchung von Last-Write-Wins und einfachen Merge-Heuristiken.

## Inhalte

- Kurzer Überblick: IndexedDB/PouchDB Sync Konzept
- Setup: Lokale DB + Änderung + Sync
- Konfliktszenario erzeugen (zwei Tabs)
- Konfliktauflösung: naive vs. heuristisch (Timestamp / Feld-Merge)
- Logging von Konfliktfällen

## Aktivitäten

- Schritt-für-Schritt Sync testen
- Konflikte absichtlich provozieren & notieren
- Mini-Reflexion: Welche Metadaten fehlen für bessere Auflösung?

## Referenzen & Quellen

- PouchDB Docs (Konzept Sync)
- Conflict Resolution Patterns (vereinfacht)
