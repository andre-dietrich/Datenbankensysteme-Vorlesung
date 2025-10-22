# Session 2 (Exercise)

## Titel

Session 2 – KV Implementierung & Atomic Counter (Exercise)

## Zusammenfassung

Praktischer Aufbau eines einfachen In-Browser Key-Value Layers (Map + Fallback LocalStorage/IndexedDB). Demonstration eines Lost-Update Problems und Einführung einer primitiven Atomic Operation.

## Inhalte

- Einfacher Wrapper um Map/LocalStorage
- put/get/exists/delete API Skizze
- Atomic increment naive vs. geschützt
- TTL Simulation (Timestamp + Prüflogik)
- Logging race outcome

## Aktivitäten

- Implementiere increment(key) parallel in zwei Tabs
- Beobachte Inkonsistenzen & dokumentiere Fälle
- Ergänze Schutz (z. B. Compare + Retry Schleife vereinfacht)

## Referenzen & Quellen

- LocalStorage / IndexedDB Basics
- Nebenläufigkeit (Begriffsteaser)
