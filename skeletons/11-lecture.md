# Session 9 (Lecture)

## Titel

Session 9 – Normalisierung (1NF–BCNF) + Denormalisierung (Lecture)

## Zusammenfassung

Redundanzabbau, funktionale Abhängigkeiten, Trade-offs. Systematische Techniken zur Vermeidung von Anomalien durch Normalisierung und bewusste Denormalisierung für Performance.

## Inhalte

- Anomalien: Insertion, Update, Deletion Anomalies
- Funktionale Abhängigkeiten (FD): A → B
- Normalformen:
  - 1NF: Atomare Werte (keine Wiederholungsgruppen)
  - 2NF: Volle funktionale Abhängigkeit vom Schlüssel
  - 3NF: Keine transitiven Abhängigkeiten
  - BCNF: Jede FD hat Superschlüssel als Determinante
- Normalisierungsprozess: Von unnormalisiert zu BCNF
- Denormalisierung:
  - Performance Trade-offs (weniger Joins)
  - Materialisierte Aggregate
  - Redundanz bewusst einführen
- Use Cases: OLTP (hochnormalisiert) vs. OLAP/Reporting (denormalisiert)

## Aktivitäten

- Tafel: Beispiel-Schema normalisieren (Schritt für Schritt)
- Diskussion: Wann ist Denormalisierung sinnvoll?
- Gruppenarbeit: Gegeben Schema → Anomalien identifizieren

## Referenzen & Quellen

- "Database Design for Mere Mortals" (Hernandez)
- Codd's Normal Forms
- "Denormalization for Performance" (Patterns)
