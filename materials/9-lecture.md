<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  0.1.0
language: de
narrator: Deutsch Female

comment:  Interaktive Session zur Datenbank-Normalisierung und ER-Modellierung: Studierende lernen ER-Diagramm-Basics (Entitäten, Beziehungen, Kardinalitäten 1:1, 1:N, N:M), entwickeln schrittweise ein normalisiertes Online-Shop-Schema (0NF → 1NF → 2NF → 3NF) mit Visualisierung via dbdiagram.io und bauen gemeinsam ein Twitter-Datenmodell von Grund auf (User, Follower, Tweets, Likes, Many-to-Many-Beziehungen). Hands-on Didaktik: Anomalien werden live erlebbar gemacht.

logo:    ../assets/img/logo/9-lecture.jpg

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md
        https://raw.githubusercontent.com/liaScript/mermaid_template/master/README.md
-->

# Session 9 – Normalisierung & ER-Diagramme

> **Interaktive Übung:** Gemeinsam entwickeln wir normalisierte Schemas und ER-Diagramme – von chaotisch zu strukturiert.

## Überblick

Willkommen zur interaktiven Normalisierungs-Session! Heute arbeiten wir **zusammen** – ihr seid nicht Zuschauer, sondern Co-Entwickler. Wir durchlaufen:

0. **ER-Diagramme**: Was können wir damit beschreiben? Wie modellieren wir Entitäten und Beziehungen?
1. **Normalisierung (1NF → 2NF → 3NF)** am Beispiel eines Online-Shops
2. **Praxis-Übung**: Schritt für Schritt bauen wir Twitter 

**Lernziele:**

- ER-Diagramme lesen und erstellen
- Normalisierungsschritte verstehen und anwenden (inkl. Transitivität)
- Komplexe Datenmodelle gemeinsam entwickeln

## Teil 0: ER-Diagramme – Entitäten & Beziehungen

ER-Diagramme (Entity-Relationship-Diagramme) sind visuelle Werkzeuge zur Datenmodellierung. Sie zeigen Entitäten (Objekte), ihre Attribute und die Beziehungen zwischen ihnen.

**Entitäten:**

    {{1}}
- Rechtecke (z.B. `User`, `Product`)

  ```mermaid   @mermaid
  erDiagram
        USER {}

        PRODUCT {}
  ```

    {{2}}
- Attribute als Ovale oder in der Entität

  ```mermaid   @mermaid
  erDiagram
        USER {
            int user_id
            string username
            string email
        }

        PRODUCT {
            int product_id
            string product_name
            decimal price
        }
  ```

**Beziehungen:**

    {{3}}
- Rauten oder Linien (z.B. `kauft`, `gehört zu`)

  ```mermaid   @mermaid
    erDiagram
            USER ||--o{ ORDER : "kauft"
            ORDER ||--|{ PRODUCT : "enthält"
  ```

    {{4}}
- Kardinalitäten: 1:1, 1:N, N:M

    {{5}}
  - **1:1 (Eins-zu-Eins):** Ein User hat genau ein Profil, ein Profil gehört zu genau einem User

    ```mermaid   @mermaid
        erDiagram
                USER ||--|| PROFILE : "hat"
                USER {
                   
                }
                PROFILE {
                    
                }
    ```

    {{6}}
  - **1:N (Eins-zu-Viele):** Ein User kann viele Orders haben, eine Order gehört zu einem User

    ```mermaid   @mermaid
        erDiagram
                USER ||--o{ ORDER : "erstellt"
                USER {
                   
                }
                ORDER {
                   
                }
    ```

    {{7}}
  - **N:M (Viele-zu-Viele):** Viele Users können viele Products kaufen, viele Products können von vielen Users gekauft werden

    ```mermaid   @mermaid
        erDiagram
                PRODUCT }o--o{ ORDER : "enthalten in"
                PRODUCT {
                   
                }
                ORDER {
                   
                }
    ```

**Schlüssel:**

    {{8}}
- Primärschlüssel (unterstrichen)

  ```mermaid   @mermaid
    erDiagram
        USER {
            int user_id PK
            string username
            string email
        }
  ```


- Fremdschlüssel (gestrichelt)

  ```mermaid   @mermaid
        erDiagram
            ORDER {
                int order_id PK
                int user_id FK
                date order_date
            }
  ```

## Teil 1: Normalisierung – Von Chaos zu Struktur

### Problem: Der chaotische Online-Shop

    --{{0}}--
Stellt euch vor: Ihr habt gerade einen Online-Shop geerbt. Alle Daten liegen in einer riesigen Tabelle. Klingt praktisch? Schauen wir mal...


### Schritt 0: Die Ausgangslage (0NF)

    --{{1}}--
Hier ist unsere "All-in-One" Tabelle. Auf den ersten Blick funktioniert sie – aber schaut genauer hin: Was fällt euch auf?

      {{1}}
<div>

#### Die chaotische Tabelle

``` sql
-- Erstelle die chaotische "Alles-in-Einem" Tabelle
CREATE TABLE shop_nf0 (
    order_id INTEGER,
    order_date DATE,
    customer_id INTEGER,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(100),
    product_id INTEGER,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    category VARCHAR(50),
    quantity INTEGER
);

-- Befülle mit realistischen Beispieldaten (mit nicht-atomaren Adressen!)
INSERT INTO shop_nf0 VALUES
(1, '2024-01-15', 1, 'Anna Müller', 'anna@mail.de', 'Hauptstraße 12, 04109 Leipzig', 1, 'Laptop Dell XPS', 1299.99, 'Elektronik', 1),
(2, '2024-01-16', 1, 'Anna Müller', 'anna@mail.de', 'Hauptstraße 12, 04109 Leipzig', 1, 'USB-C Kabel', 15.99, 'Zubehör', 2),
(3, '2024-01-16', 2, 'Max Schmidt', 'max.s@web.de', 'Berliner Allee 45, 10115 Berlin', 1, 'Laptop Dell XPS', 1299.99, 'Elektronik', 1),
(4, '2024-01-17', 3, 'Lisa Weber', 'lisa.w@gmail.com', 'Hafenstraße 8, 20095 Hamburg', 1, 'Wireless Maus', 29.99, 'Zubehör', 1);

-- Schauen wir uns das Chaos an
SELECT * FROM shop_nf0;
```
@PGlite.terminal(nf)

{{2}} **Gibt es Probleme, die man direkt sehen kann?**

</div>

### Schritt 1: Erste Normalform (1NF)


**Regel:** Atomare Werte – keine Listen, keine verschachtelten Strukturen. Jede Zelle enthält genau einen Wert.

      {{1}}
<div>

#### Was ändert sich?

**Aufgabe:** Identifiziert Spalten, die gegen 1NF verstoßen.

``` sql
CREATE TABLE shop_nf1 (
    
);

--INSERT INTO shop_nf1 VALUES

--SELECT * FROM shop_nf1;
```
@PGlite.terminal(nf)

</div>

### Schritt 2: Zweite Normalform (2NF)

**Regel:** Keine partiellen Abhängigkeiten. Alle Nicht-Schlüssel-Attribute müssen vom gesamten Primärschlüssel abhängen.

      {{1}}
<div>

#### Was bedeutet das konkret?

``` sql
-- TODO: Zerlege die Tabelle in 2NF-konforme Tabellen


```
@PGlite.terminal(nf)

**Frage an euch:**

- Welche Daten hängen nur von einem Teil des Schlüssels ab?
- Welche Tabellen fehlen uns noch?

</div>

### Schritt 3: Dritte Normalform (3NF) – Transitivität eliminieren


**Regel:** Keine transitiven Abhängigkeiten. Nicht-Schlüssel-Attribute dürfen nicht voneinander abhängen.

    {{1}}
<div>

#### Was sind transitive Abhängigkeiten?

``` sql
-- TODO: Zerlege die Tabelle in 3NF-konforme Tabellen


```
@PGlite.terminal(nf)

- Welche Tabelle brauchen wir zusätzlich?
- Wann ist das praktikabel, wann übertrieben?

</div>

### Finales normalisiertes Schema

Das ist unser Ziel: Ein sauberes, normalisiertes Schema mit klaren Beziehungen und ohne Redundanz.


      {{0-2}}
<div>

#### Unser Online-Shop (0NF)

``` sql   @dbdiagram
// 0NF: Chaotische "Alles-in-Einem" Tabelle
// Alle Daten redundant in einer Tabelle - kein gutes Design!

Table shop_nf0 {
  order_id integer [note: 'Bestellnummer (aber kein echter PK!)']
  order_date date [note: 'Bestelldatum']
  customer_id integer [note: 'Kunde (redundant gespeichert!)']
  customer_name varchar(100) [note: 'Name (dupliziert bei jedem Order!)']
  email varchar(100) [note: 'Email (dupliziert!)']
  address varchar(100) [note: 'NICHT ATOMAR! Enthält Straße, PLZ, Stadt zusammen']
  product_id integer [note: 'Produkt (redundant!)']
  product_name varchar(100) [note: 'Produktname (dupliziert!)']
  price decimal(10,2) [note: 'Preis (dupliziert - Update-Anomalie!)']
  category varchar(50) [note: 'Kategorie (dupliziert!)']
  quantity integer [note: 'Bestellmenge']
  
  Note: '''
    PROBLEME dieser Tabelle:
    
    ❌ Keine echte Primärschlüssel-Definition
    ❌ NICHT ATOMAR: address enthält mehrere Werte
    ❌ MASSIVE REDUNDANZ:
       - Anna Müller's Daten stehen 2x drin
       - Laptop-Daten stehen 2x drin
    ❌ UPDATE-ANOMALIE: Preis ändern = in mehreren Zeilen
    ❌ DELETE-ANOMALIE: Letzten Kunden löschen = Produkt verschwindet
    ❌ INSERT-ANOMALIE: Produkt ohne Bestellung = unmöglich
    
    Beispieldaten zeigen:
    - Anna (customer_id=1) taucht 2x auf
    - Laptop (product_id=1) taucht 2x auf mit gleichem Preis
    - Adressen wie 'Hauptstraße 12, 04109 Leipzig' sind nicht atomar
  '''
}

// Keine Relationships - alles in einer Tabelle!
// Keine Foreign Keys - alles redundant!
// Kein echtes Schema-Design - nur Datenmüll!
```

</div>


        {{1-3}}
<div>

#### Unser Online-Shop (1NF)

``` sql   @dbdiagram
// 1NF: Erste Normalform
// Adresse aufgeteilt in atomare Spalten - aber noch viel Redundanz!

Table shop_nf1 {
  order_id integer [pk, note: 'Jetzt echter Primary Key']
  order_date date [not null]
  customer_id integer [note: 'Kunde (noch redundant!)']
  customer_name varchar(100) [note: 'Name (noch dupliziert!)']
  email varchar(100) [note: 'Email (noch dupliziert!)']
  street varchar(100) [note: '✅ ATOMAR: Nur Straße + Hausnummer']
  zip varchar(10) [note: '✅ ATOMAR: Nur PLZ']
  city varchar(50) [note: '✅ ATOMAR: Nur Stadt']
  product_id integer [note: 'Produkt (noch redundant!)']
  product_name varchar(100) [note: 'Produktname (noch dupliziert!)']
  price decimal(10,2) [note: 'Preis (noch dupliziert!)']
  category varchar(50) [note: 'Kategorie (noch dupliziert!)']
  quantity integer [not null, default: 1]
  
  Note: '''
    1NF ERREICHT:
    ✅ Alle Werte sind atomar (keine Listen mehr)
    ✅ Adresse aufgeteilt: street, zip, city
    ✅ Primärschlüssel definiert (order_id)
    
    ABER NOCH PROBLEME:
    ❌ MASSIVE REDUNDANZ bleibt:
       - Anna Müller's Daten (Name, Email, Adresse) stehen 2x drin
       - Laptop-Daten (Name, Preis, Kategorie) stehen 2x drin
    ❌ UPDATE-ANOMALIE: Preis ändern = mehrere Zeilen
    ❌ DELETE-ANOMALIE: Kunde löschen = Produkt weg
    ❌ PARTIELLE ABHÄNGIGKEITEN:
       - customer_* Felder hängen nicht vom ganzen PK ab
       - product_* Felder hängen nicht vom ganzen PK ab
    
    → Für 2NF müssen wir Tabellen aufteilen!
  '''
}

// Immer noch keine Relationships - alles in einer Tabelle!
// Redundanz-Problem besteht weiterhin!
// Nächster Schritt: 2NF (Tabellen aufteilen)
```

</div>

        {{2}}
<div>

#### Unser Online-Shop (2NF)

``` sql   @dbdiagram
// 2NF: Online-Shop Schema
// Keine partiellen Abhängigkeiten mehr!

Table customers {
  customer_id integer [pk, increment]
  customer_name varchar(100) [not null]
  email varchar(100) [not null, unique]
  street varchar(100)
  zip varchar(10)
  city varchar(50)
  
  Note: 'Kundendaten - einmal gespeichert, keine Redundanz'
}

Table products {
  product_id integer [pk, increment]
  product_name varchar(100) [not null]
  price decimal(10,2) [not null]
  category varchar(50)
  
  Note: 'Produktdaten - einmal gespeichert'
}

Table orders {
  order_id integer [pk, increment]
  customer_id integer [not null, ref: > customers.customer_id]
  order_date date [not null, default: `now()`]
  
  Note: 'Bestellungen - verknüpft Kunden mit Zeitpunkt'
}

Table order_items {
  order_id integer [pk, ref: > orders.order_id]
  product_id integer [pk, ref: > products.product_id]
  quantity integer [not null, default: 1]
  
  Note: 'Zwischentabelle für M:N-Beziehung zwischen Orders und Products'
}

// Relationships (automatisch durch ref: definiert)
// customers 1 --< orders (Ein Kunde, viele Bestellungen)
// orders 1 --< order_items (Eine Bestellung, viele Items)
// products 1 --< order_items (Ein Produkt, in vielen Bestellungen)

// 2NF erreicht:
// ✅ Alle Attribute hängen vom gesamten Primärschlüssel ab
// ✅ Keine partiellen Abhängigkeiten
// ⚠️ Aber: city hängt von zip ab → für 3NF muss das noch gelöst werden!
```

</div>


      {{3}}
<div>

#### Unser Online-Shop (3NF)

``` sql   @dbdiagram
// 3NF: Dritte Normalform
// Vollständig normalisiert - keine Redundanz, keine transitiven Abhängigkeiten!

Table customers {
  customer_id integer [pk, increment]
  customer_name varchar(100) [not null]
  email varchar(100) [not null, unique]
  street varchar(100)
  location_id integer [ref: > locations.location_id, note: 'FK zu locations']
  
  Note: '''
    Kundendaten - einmal gespeichert
    ✅ Keine Redundanz
    ✅ PLZ/Stadt ausgelagert (keine transitive Abhängigkeit mehr!)
  '''
}

Table locations {
  location_id integer [pk, increment]
  zip varchar(10) [not null, unique]
  city varchar(50) [not null]
  
  Note: '''
    PLZ/Stadt-Zuordnung - einmal gespeichert
    ✅ Löst transitive Abhängigkeit: city hängt von zip ab
    ✅ '04109' → 'Leipzig' steht nur 1x in der DB
    ✅ Stadt-Name ändern? Nur 1 Update!
  '''
}

Table products {
  product_id integer [pk, increment]
  product_name varchar(100) [not null]
  price decimal(10,2) [not null]
  category_id integer [ref: > categories.category_id, note: 'FK zu categories']
  
  Note: '''
    Produktdaten - einmal gespeichert
    ✅ Kategorie ausgelagert (optional für 3NF, aber sauberer)
  '''
}

Table categories {
  category_id integer [pk, increment]
  category_name varchar(50) [not null, unique]
  
  Note: '''
    Kategorien - einmal gespeichert
    ✅ 'Elektronik', 'Zubehör' etc. nur 1x in DB
    ✅ Kategorie umbenennen? Nur 1 Update!
  '''
}

Table orders {
  order_id integer [pk, increment]
  customer_id integer [not null, ref: > customers.customer_id]
  order_date date [not null, default: `now()`]
  
  Note: 'Bestellungen - verknüpft Kunden mit Zeitpunkt'
}

Table order_items {
  order_id integer [pk, ref: > orders.order_id]
  product_id integer [pk, ref: > products.product_id]
  quantity integer [not null, default: 1]
  
  Note: 'Zwischentabelle für M:N-Beziehung zwischen Orders und Products'
}

// Relationships
// customers 1 --< orders (Ein Kunde, viele Bestellungen)
// orders 1 --< order_items (Eine Bestellung, viele Items)
// products 1 --< order_items (Ein Produkt in vielen Bestellungen)
// locations 1 --< customers (Eine PLZ/Stadt, viele Kunden)
// categories 1 --< products (Eine Kategorie, viele Produkte)
```

**Diskussion:**
- Wann würdet ihr denormalisieren?
- Performance vs. Konsistenz?

</div>


## Teil 2: Twitter-Modell gemeinsam entwickeln

> Aufgabe: Baue twitter nach und befülle es mit Beispieldaten – Schritt für Schritt!


``` sql   Twitter.db











```
@PGlite.terminal(twitter)