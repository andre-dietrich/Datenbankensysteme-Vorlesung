<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  0.1.0
language: de
narrator: Deutsch Female

@style
.lia-effect__circle {
  display: none !important;
}

details {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.5em;
  margin: 1em 0;
}

summary {
  font-weight: bold;
  cursor: pointer;
  padding: 0.5em;
}

details[open] summary {
  border-bottom: 1px solid #ccc;
  margin-bottom: 0.5em;
}

@end

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md
        https://raw.githubusercontent.com/liaScript/mermaid_template/master/README.md

@SQL.exec
<script>
function loadDB(resolve, reject) {
  initSqlJs({locateFile: filename => `https://cdn.jsdelivr.net/npm/sql.js@1.10.2/dist/${filename}`}).then(SQL => {
    const db = new SQL.Database();
    
    // Sample E-Commerce Schema
    db.run(`
      CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        city TEXT
      );
      
      CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        total_amount DECIMAL(10,2),
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
      );
      
      CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price DECIMAL(10,2)
      );
      
      CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        line_total DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
      );
      
      -- Sample Data: Customers
      INSERT INTO customers VALUES
        (1, 'Alice', 'Anderson', 'alice@email.com', 'Berlin'),
        (2, 'Bob', 'Brown', 'bob@email.com', 'Hamburg'),
        (3, 'Carol', 'Clark', 'carol@email.com', 'Munich'),
        (4, 'David', 'Davis', 'david@email.com', 'Cologne'),
        (5, 'Emma', 'Evans', 'emma@email.com', 'Frankfurt');
      
      -- Sample Data: Orders (Note: Customer 5 has NO orders!)
      INSERT INTO orders VALUES
        (101, 1, '2024-01-15', 299.99, 'completed'),
        (102, 1, '2024-02-20', 149.50, 'completed'),
        (103, 2, '2024-01-22', 499.99, 'completed'),
        (104, 3, '2024-03-10', 89.99, 'pending'),
        (105, 4, '2024-03-15', 199.99, 'completed');
      
      -- Sample Data: Products
      INSERT INTO products VALUES
        (1, 'Laptop', 'Electronics', 999.99),
        (2, 'Mouse', 'Electronics', 29.99),
        (3, 'Keyboard', 'Electronics', 79.99),
        (4, 'Monitor', 'Electronics', 299.99),
        (5, 'Desk Chair', 'Furniture', 199.99),
        (6, 'Notebook', 'Stationery', 9.99);
      
      -- Sample Data: Order Items
      INSERT INTO order_items VALUES
        (1, 101, 4, 1, 299.99),
        (2, 102, 2, 2, 59.98),
        (3, 102, 3, 1, 79.99),
        (4, 103, 1, 1, 999.99),
        (5, 104, 6, 5, 49.95),
        (6, 105, 5, 1, 199.99);
    `);
    
    try {
      let result = db.exec(`@input`);
      if (result.length > 0) {
        let columns = result[0].columns;
        let values = result[0].values;
        
        let output = '<table style="width:100%; border-collapse: collapse;">';
        output += '<thead><tr>';
        columns.forEach(col => {
          output += `<th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">${col}</th>`;
        });
        output += '</tr></thead><tbody>';
        
        values.forEach(row => {
          output += '<tr>';
          row.forEach(cell => {
            output += `<td style="border: 1px solid #ddd; padding: 8px;">${cell !== null ? cell : '<em>NULL</em>'}</td>`;
          });
          output += '</tr>';
        });
        output += '</tbody></table>';
        
        send.lia(output);
        send.lia("LIA: stop");
      } else {
        send.lia("Query executed successfully (no results returned)");
        send.lia("LIA: stop");
      }
    } catch (e) {
      send.lia("Error: " + e.message);
      send.lia("LIA: stop");
    }
  }).catch(err => {
    send.lia("Error loading SQL.js: " + err.message);
    send.lia("LIA: stop");
  });
}

loadDB();
"LIA: wait";
</script>
@end

-->

# L10: SQL Joins & Combining Data

> **Session 10 – Lecture**  
> **Dauer:** 90 Minuten  
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)  
> **Block:** 2 – SQL Einführung & Grundlagen

---

    --{{0}}--
Willkommen zur zehnten Session! Bisher haben Sie mit einzelnen Tabellen gearbeitet – SELECT, WHERE, GROUP BY, alles auf einer Tabelle. Das war wichtig zum Lernen, aber die wahre Macht relationaler Datenbanken liegt woanders: in Beziehungen.

    --{{1}}--
Kunden haben Bestellungen. Bestellungen haben Positionen. Produkte gehören zu Kategorien. Mitarbeiter haben Manager. All diese Informationen leben in verschiedenen Tabellen – und Joins sind der Schlüssel, sie zusammenzubringen.

    --{{2}}--
In dieser Session lernen Sie, wie Sie Daten über Tabellen hinweg kombinieren. Sie verstehen, wann Sie welchen Join-Typ brauchen. Sie können Multi-Table-Queries schreiben. Und Sie wissen, wie Sie fehlende Beziehungen finden – eine der mächtigsten Analysetechniken überhaupt.

    --{{3}}--
Los geht's mit der Frage: Warum brauchen wir Joins überhaupt?

## Warum Joins?

    --{{0}}--
Stellen Sie sich vor, Sie speichern alles in einer Tabelle: Kundendaten, Bestellungen, Produktdetails – alles zusammen. Was passiert?

    {{1}}
> **Problem 1: Redundanz**  
> Sie speichern die Kundenadresse bei jeder Bestellung neu. Zieht der Kunde um, müssen Sie Dutzende Zeilen aktualisieren.

    {{2}}
> **Problem 2: Inkonsistenz**  
> Bei manchen Bestellungen steht „Berlin", bei anderen „Berln" – Tippfehler.

    {{3}}
> **Problem 3: Update-Anomalien**  
> Sie ändern den Preis eines Produkts – aber welche Bestellungen bekommen den neuen Preis? Die alten sollten den alten Preis behalten!

    --{{4}}--
Die Lösung? Normalisierung. Wir teilen Daten in mehrere Tabellen auf. Jede Tabelle hat eine klar definierte Verantwortung. Beziehungen werden über Foreign Keys hergestellt.

    {{4}}
**Normalisierung führt zu mehreren Tabellen.**  
**Joins rekonstruieren die Informationen.**

## Unser E-Commerce-Schema

    --{{0}}--
Für alle Beispiele heute nutzen wir ein einfaches E-Commerce-Schema mit vier Tabellen.

```ascii
+-------------+       +------------+       +---------------+
| customers   |       | orders     |       | order_items   |
+-------------+       +------------+       +---------------+
| customer_id |<---+  | order_id   |<---+  | order_item_id |
| first_name  |    |  | customer_id|    |  | order_id      |
| last_name   |    +--| order_date |    +--| product_id    |
| email       |       | total_amt  |       | quantity      |
| city        |       | status     |       | line_total    |
+-------------+       +------------+       +---------------+
                                                   |
                                                   v
                                           +-------------+
                                           | products    |
                                           +-------------+
                                           | product_id  |
                                           | product_name|
                                           | category    |
                                           | price       |
                                           +-------------+
```

    {{1}}
**Beziehungen:**

    {{1}}
- Ein Kunde kann viele Bestellungen haben (1:N)
- Eine Bestellung hat viele Positionen (1:N)
- Ein Produkt kann in vielen Positionen vorkommen (N:M über order_items)

    --{{2}}--
Diese Struktur ist typisch für relationale Datenbanken. Joins erlauben uns, die Informationen bei Bedarf wieder zusammenzusetzen.

---

## Join-Grundlagen

### Join-Syntax: Modern vs. Veraltet

    --{{0}}--
Es gibt zwei Wege, Joins zu schreiben. Einen modernen, expliziten Weg – und einen veralteten, impliziten Weg. Schauen wir uns beide an.

    {{1}}
**Moderne Syntax (empfohlen):**

    {{1}}
```sql
SELECT c.first_name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

    {{2}}
**Veraltete Syntax (nicht empfohlen):**

    {{2}}
```sql
SELECT c.first_name, o.order_id
FROM customers c, orders o
WHERE c.customer_id = o.customer_id;
```

    --{{3}}--
Beide Queries liefern das gleiche Ergebnis. Aber die moderne Syntax ist klarer: Sie trennt die Join-Bedingung vom WHERE-Filter. Das macht Queries lesbarer und weniger fehleranfällig.

    {{3}}
> **Best Practice:** Nutzen Sie immer die explizite `JOIN ... ON` Syntax!

---

### USING-Klausel (Shortcut)

    --{{0}}--
Wenn die Join-Spalten in beiden Tabellen den gleichen Namen haben, können Sie eine Abkürzung nutzen: die USING-Klausel.

```sql
-- Statt:
SELECT * FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Können Sie schreiben:
SELECT * FROM customers
INNER JOIN orders USING (customer_id);
```

    {{1}}
> **Achtung:** USING funktioniert nur, wenn die Spaltennamen identisch sind. Bei verschiedenen Namen (z.B. `customer_id` vs. `cust_id`) müssen Sie `ON` verwenden.

---

### Join-Typen: Überblick

    --{{0}}--
Es gibt fünf Haupt-Join-Typen. Jeder hat seinen Einsatzzweck.

| Join-Typ         | Ergebnis                                      | Use Case                        |
|------------------|-----------------------------------------------|---------------------------------|
| **INNER JOIN**   | Nur Matches                                   | Standard-Fall                   |
| **LEFT JOIN**    | Alle links + Matches rechts                   | Fehlende Beziehungen finden     |
| **RIGHT JOIN**   | Alle rechts + Matches links                   | Selten (meist LEFT stattdessen) |
| **FULL OUTER**   | Alle von beiden Seiten                        | Daten-Sync-Vergleich            |
| **CROSS JOIN**   | Kartesisches Produkt (alle Kombinationen)     | Test-Kombinationen generieren   |

    --{{1}}--
In der Praxis sind INNER JOIN und LEFT JOIN die mit Abstand häufigsten. CROSS JOIN und FULL OUTER sind Spezialfälle. Schauen wir uns jeden im Detail an.

---

## INNER JOIN: Nur Matches

    --{{0}}--
Der INNER JOIN ist der Standard. Er gibt nur Zeilen zurück, bei denen es in beiden Tabellen einen Match gibt.

### Konzept

```ascii
Customers        Orders
+----+-----+    +----+--------+
| ID | Name|    | ID | Cust_ID|
+----+-----+    +----+--------+
| 1  | Alice    | 101| 1      |  ← Match!
| 2  | Bob      | 102| 1      |  ← Match!
| 3  | Carol    | 103| 2      |  ← Match!
| 5  | Emma     | 105| 4      |  ← Match!
+----+-----+    +----+--------+

Ergebnis (INNER JOIN):
Alice - Order 101
Alice - Order 102
Bob   - Order 103
David - Order 105

Emma hat KEINE Bestellung → taucht NICHT auf!
```

    --{{1}}--
Emma ist Kundin, hat aber noch nie bestellt. Im INNER JOIN verschwindet sie aus dem Ergebnis. Das ist manchmal genau das, was Sie wollen – manchmal aber auch nicht.

---

### Live-Beispiel: Kunden mit Bestellungen

    {{1}}
**Aufgabe:** Zeigen Sie alle Kunden, die mindestens eine Bestellung haben.

    {{1}}
```sql
SELECT 
  c.first_name,
  c.last_name,
  o.order_id,
  o.order_date,
  o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.last_name, o.order_date;
```
@SQL.exec

    --{{2}}--
Führen Sie die Query aus. Sie sehen: Nur Kunden mit Bestellungen erscheinen. Emma (customer_id = 5) fehlt komplett.

---

### Multi-Table Joins

    --{{0}}--
Sie können beliebig viele Tabellen verbinden. Jeder weitere JOIN wird an den vorherigen angehängt.

**Aufgabe:** Zeigen Sie für jede Bestellung die gekauften Produkte.

```sql
SELECT 
  c.first_name || ' ' || c.last_name AS customer,
  o.order_id,
  p.product_name,
  oi.quantity,
  oi.line_total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id;
```
@SQL.exec

    {{1}}
> **Lesbarkeit:** Ketten Sie Joins schrittweise – erst Kunde → Bestellung, dann Bestellung → Positionen, dann Positionen → Produkte.

---

### NULL-Werte in Join-Spalten

    --{{0}}--
Wichtig: Wenn die Join-Spalte NULL enthält, wird die Zeile im INNER JOIN ignoriert.

```sql
-- Angenommen, eine Bestellung hat customer_id = NULL
-- (sollte durch Constraints verhindert werden, aber theoretisch möglich)

SELECT * FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
-- Bestellung mit NULL customer_id taucht NICHT auf!
```

    {{1}}
> **Best Practice:** Definieren Sie Foreign Keys als `NOT NULL`, um solche Situationen zu vermeiden.

---

## LEFT JOIN: Alle von links + Matches

    --{{0}}--
Der LEFT JOIN (auch LEFT OUTER JOIN) gibt alle Zeilen der linken Tabelle zurück – auch wenn es keinen Match rechts gibt. Fehlende Matches werden mit NULL aufgefüllt.

### Konzept

```ascii
Customers (links)   Orders (rechts)
+----+-----+       +----+--------+
| ID | Name|       | ID | Cust_ID|
+----+-----+       +----+--------+
| 1  | Alice       | 101| 1      |  ← Match
| 2  | Bob         | 102| 1      |  ← Match
| 3  | Carol       | 103| 2      |  ← Match
| 4  | David       | 105| 4      |  ← Match
| 5  | Emma        (keine Bestellung)
+----+-----+       +----+--------+

Ergebnis (LEFT JOIN):
Alice - Order 101
Alice - Order 102
Bob   - Order 103
David - Order 105
Emma  - NULL     ← Emma bleibt erhalten!
```

    --{{1}}--
Emma erscheint jetzt im Ergebnis – aber die Order-Spalten sind NULL. Das ist der Schlüssel: LEFT JOIN behält alle linken Zeilen.

---

### Live-Beispiel: Alle Kunden (auch ohne Bestellungen)

    {{1}}
```sql
SELECT 
  c.first_name,
  c.last_name,
  o.order_id,
  o.order_date,
  o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.last_name;
```
@SQL.exec

    --{{2}}--
Führen Sie die Query aus. Jetzt sehen Sie Emma – mit NULL bei allen Order-Feldern.

---

### Use Case: Fehlende Beziehungen finden (Anti-Join)

    --{{0}}--
Der mächtigste Einsatz von LEFT JOIN: Finden Sie Datensätze, die KEINE Beziehung haben.

**Frage:** Welche Kunden haben noch NIE bestellt?

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name,
  c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```
@SQL.exec

    {{1}}
**Trick:** Nach dem LEFT JOIN filtern Sie auf `IS NULL` der rechten Tabelle. Das sind genau die Zeilen ohne Match.

    --{{2}}--
Diese Technik nennt man „Anti-Join". Sie kommt in der Praxis extrem häufig vor: Fehlende Übersetzungen, nicht verkaufte Produkte, inaktive Nutzer – alles Anti-Joins.

---

### NULL-Handling: COALESCE

    --{{0}}--
Wenn Sie NULL-Werte nicht mögen, können Sie Defaults setzen.

```sql
SELECT 
  c.first_name,
  COALESCE(o.order_id, 'No Orders') AS order_status,
  COALESCE(o.total_amount, 0) AS total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;
```
@SQL.exec

    {{1}}
> `COALESCE(value, default)` gibt den ersten Nicht-NULL-Wert zurück.

---

## RIGHT JOIN (kurz)

    --{{0}}--
RIGHT JOIN ist das Spiegelbild von LEFT JOIN: Alle Zeilen der rechten Tabelle, Matches links.

```sql
SELECT * FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;
-- Alle Bestellungen (auch ohne zugehörigen Kunden)
```

    {{1}}
**In der Praxis:** RIGHT JOIN wird selten genutzt – meist schreiben Sie die Query so um, dass Sie LEFT JOIN verwenden können. Das ist intuitiver.

    {{2}}
```sql
-- Statt RIGHT JOIN:
SELECT * FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;
-- Gleicher Effekt, aber links = Haupttabelle
```

---

## FULL OUTER JOIN: Alle von beiden Seiten

    --{{0}}--
FULL OUTER JOIN kombiniert LEFT und RIGHT: Alle Zeilen von beiden Seiten, Matches wo möglich, NULL wo nicht.

### Konzept

```ascii
Table A         Table B
+----+-----+   +----+-----+
| ID | Name|   | ID | Attr|
+----+-----+   +----+-----+
| 1  | X        | 1  | A   |  ← Match
| 2  | Y        | 3  | B   |  ← Kein Match links
| 4  | Z        +----+-----+
+----+-----+

Ergebnis (FULL OUTER):
1 - X - A   ← Match
2 - Y - NULL ← Nur links
4 - Z - NULL ← Nur links
NULL - NULL - 3 - B  ← Nur rechts
```

    --{{1}}--
Jede Zeile aus beiden Tabellen erscheint mindestens einmal. Fehlende Matches werden mit NULL aufgefüllt – auf beiden Seiten.

---

### Use Case: Daten-Sync-Vergleich

    --{{0}}--
FULL OUTER JOIN wird oft für Vergleiche genutzt: Quelle vs. Ziel, Soll vs. Ist.

**Beispiel:** Vergleich zweier Produktkataloge (alt vs. neu).

```sql
-- Hypothetisches Beispiel (nicht mit unserem Schema ausführbar)
SELECT 
  COALESCE(old.product_id, new.product_id) AS product_id,
  old.product_name AS old_name,
  new.product_name AS new_name,
  CASE
    WHEN old.product_id IS NULL THEN 'Neu hinzugefügt'
    WHEN new.product_id IS NULL THEN 'Entfernt'
    ELSE 'Vorhanden'
  END AS status
FROM old_products old
FULL OUTER JOIN new_products new ON old.product_id = new.product_id;
```

    {{1}}
> **Performance:** FULL OUTER kann langsam sein. Alternative: `UNION` von LEFT und RIGHT JOIN.

---

## CROSS JOIN: Kartesisches Produkt

    --{{0}}--
CROSS JOIN verbindet jede Zeile der ersten Tabelle mit jeder Zeile der zweiten Tabelle. Keine Bedingung, kein Filter – alle Kombinationen.

### Konzept

```ascii
Table A (3 Zeilen)   Table B (2 Zeilen)
+----+             +----+
| A1 |             | B1 |
| A2 |             | B2 |
| A3 |             +----+
+----+

CROSS JOIN → 3 × 2 = 6 Zeilen:
A1-B1, A1-B2, A2-B1, A2-B2, A3-B1, A3-B2
```

    --{{1}}--
Das nennt man kartesisches Produkt. Wenn Sie 1000 Kunden und 500 Produkte haben, entstehen 500.000 Zeilen!

---

### Syntax

```sql
-- Explizit:
SELECT * FROM customers CROSS JOIN products;

-- Implizit (veraltet):
SELECT * FROM customers, products;
```

    {{1}}
> **Achtung:** Vergessen Sie bei der impliziten Syntax die WHERE-Bedingung, passiert ein versehentlicher CROSS JOIN!

---

### Use Case: Kombinationen generieren

    --{{0}}--
CROSS JOIN ist nützlich, um alle möglichen Kombinationen zu erzeugen.

**Beispiel:** Testdaten – jeder Kunde mit jedem Produkt kombinieren (für A/B-Tests).

```sql
SELECT 
  c.customer_id,
  c.first_name,
  p.product_id,
  p.product_name
FROM customers c
CROSS JOIN products p
LIMIT 10;  -- Nur erste 10 Kombinationen zeigen
```
@SQL.exec

    {{1}}
**Ergebnis:** 5 Kunden × 6 Produkte = 30 Kombinationen (wir zeigen nur 10).

---

### Gefahr: Explosion der Zeilenzahl

    --{{0}}--
Seien Sie vorsichtig mit CROSS JOIN bei großen Tabellen!

| Tabelle A | Tabelle B | Ergebnis       |
|-----------|-----------|----------------|
| 100       | 100       | 10.000         |
| 1.000     | 1.000     | 1.000.000      |
| 10.000    | 10.000    | 100.000.000 ❌ |

    {{1}}
> **Regel:** Nutzen Sie CROSS JOIN nur, wenn Sie wirklich alle Kombinationen brauchen – und meist mit `LIMIT`.

---

## Self Joins: Tabelle mit sich selbst verbinden

    --{{0}}--
Manchmal müssen Sie eine Tabelle mit sich selbst verbinden – für hierarchische Daten.

### Konzept: Mitarbeiter-Manager-Beziehung

```ascii
employees Tabelle:
+-----+------+--------+
| ID  | Name | Mgr_ID |
+-----+------+--------+
| 1   | Alice| NULL   |  (CEO, kein Manager)
| 2   | Bob  | 1      |  (Manager: Alice)
| 3   | Carol| 1      |  (Manager: Alice)
| 4   | David| 2      |  (Manager: Bob)
+-----+------+--------+

Self Join → Mitarbeiter + Manager-Name:
Bob   → Manager: Alice
Carol → Manager: Alice
David → Manager: Bob
```

    --{{1}}--
Die Mgr_ID zeigt auf die ID in derselben Tabelle. Um beide Namen zu sehen, joinen Sie die Tabelle mit sich selbst.

---

### Live-Beispiel (simuliert mit Kunden)

    --{{0}}--
Unser Schema hat keine Hierarchie, aber wir simulieren eine: „Empfehlungs-Beziehung".

Angenommen, Kunde 2 wurde von Kunde 1 empfohlen, Kunde 3 von Kunde 1, usw.

```sql
-- Hypothetischer Self Join (Schema müsste erweitert werden)
-- customers: customer_id, first_name, referred_by_id

SELECT 
  c1.first_name AS customer,
  c2.first_name AS referred_by
FROM customers c1
LEFT JOIN customers c2 ON c1.referred_by_id = c2.customer_id;
```

    {{1}}
**Wichtig:** Aliase (`c1`, `c2`) sind zwingend – sonst weiß die Datenbank nicht, welche Instanz gemeint ist!

---

### Rekursive Hierarchien (Vorschau)

    --{{0}}--
Self Joins zeigen nur eine Ebene. Für ganze Hierarchien (alle Vorgesetzten eines Mitarbeiters) brauchen Sie rekursive CTEs – das kommt in Session 13.

```sql
-- Vorschau: WITH RECURSIVE (noch nicht heute!)
WITH RECURSIVE hierarchy AS (
  SELECT employee_id, name, manager_id, 0 AS level
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.employee_id, e.name, e.manager_id, h.level + 1
  FROM employees e
  INNER JOIN hierarchy h ON e.manager_id = h.employee_id
)
SELECT * FROM hierarchy;
```

    {{1}}
> Das ist **advanced SQL** – kommt später!

---

## Anti-Joins: Fehlende Beziehungen finden

    --{{0}}--
Anti-Joins sind eine der mächtigsten Analysetechniken. Frage: „Zeige mir alle A, die KEIN B haben."

    {{1}}
**Use Cases:**

    {{1}}
- Kunden ohne Bestellungen (Inaktive identifizieren)
- Produkte ohne Verkäufe (Ladenhüter)
- Fehlende Übersetzungen (Content-Lücken)
- Orphaned Records (Datenqualität)

    --{{2}}--
Es gibt drei Methoden für Anti-Joins. Alle liefern das gleiche Ergebnis, aber mit unterschiedlicher Performance.

---

### Methode 1: LEFT JOIN + IS NULL

    --{{0}}--
Das ist die klassische Methode. Sie joinen links und filtern dann auf NULL rechts.

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```
@SQL.exec

    {{1}}
**Vorteil:** Einfach zu verstehen, intuitiv.  
**Nachteil:** Bei großen Tabellen kann das langsamer sein als NOT EXISTS.

---

### Methode 2: NOT EXISTS (Subquery)

    --{{0}}--
NOT EXISTS prüft, ob eine Subquery mindestens eine Zeile zurückgibt. Wenn nicht → Zeile kommt ins Ergebnis.

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 
  FROM orders o 
  WHERE o.customer_id = c.customer_id
);
```
@SQL.exec

    {{1}}
**Vorteil:** Oft performanter (stoppt bei erstem Match).  
**Nachteil:** Etwas weniger intuitiv als LEFT JOIN.

---

### Methode 3: NOT IN (mit Vorsicht!)

    --{{0}}--
NOT IN prüft, ob ein Wert NICHT in einer Liste vorkommt.

```sql
SELECT 
  c.customer_id,
  c.first_name,
  c.last_name
FROM customers c
WHERE c.customer_id NOT IN (
  SELECT customer_id FROM orders
);
```
@SQL.exec

    {{1}}
**Problem:** Wenn die Subquery NULL enthält, liefert NOT IN **kein Ergebnis**!

    {{2}}
```sql
-- Beispiel: Wenn orders.customer_id NULL enthalten kann:
WHERE customer_id NOT IN (1, 2, NULL)
-- → Evaluiert zu: customer_id != 1 AND customer_id != 2 AND customer_id != NULL
-- → NULL-Vergleiche sind UNKNOWN → Gesamtergebnis: UNKNOWN → Keine Zeilen!
```

    --{{3}}--
Deshalb: Vermeiden Sie NOT IN für Anti-Joins. Nutzen Sie NOT EXISTS oder LEFT JOIN + IS NULL.

---

### Performance-Vergleich

    --{{0}}--
Welche Methode ist am schnellsten? Das hängt vom DBMS und der Datenmenge ab.

| Methode               | Typische Performance | Best Case                     |
|-----------------------|----------------------|-------------------------------|
| LEFT JOIN + IS NULL   | Mittel               | Kleine bis mittlere Tabellen  |
| NOT EXISTS            | Schnell              | Große Tabellen, stoppt früh   |
| NOT IN                | Langsam (+ NULL-Bug) | Vermeiden!                    |

    {{1}}
> **Empfehlung:** Nutzen Sie **NOT EXISTS** für große Tabellen, **LEFT JOIN + IS NULL** für Klarheit bei kleinen Datenmengen.

---

### Anti-Join Use Case: Produkte ohne Verkäufe

    --{{0}}--
Welche Produkte wurden noch nie verkauft?

```sql
SELECT 
  p.product_id,
  p.product_name,
  p.category
FROM products p
WHERE NOT EXISTS (
  SELECT 1 
  FROM order_items oi 
  WHERE oi.product_id = p.product_id
);
```
@SQL.exec

    {{1}}
**Ergebnis:** Alle Produkte, die in keiner Bestellung vorkommen (Ladenhüter-Analyse).

---

## Set-Operationen: Vertikal kombinieren

    --{{0}}--
Joins kombinieren Tabellen horizontal (Spalten hinzufügen). Set-Operationen kombinieren vertikal (Zeilen anhängen).

| Operation    | Bedeutung                                 | SQL-Operator  |
|--------------|-------------------------------------------|---------------|
| Vereinigung  | Alle aus A + alle aus B (ohne Duplikate)  | `UNION`       |
| Vereinigung  | Alle aus A + alle aus B (mit Duplikaten)  | `UNION ALL`   |
| Schnittmenge | Nur Zeilen, die in beiden vorkommen       | `INTERSECT`   |
| Differenz    | Nur in A, nicht in B                      | `EXCEPT`      |

    --{{1}}--
Set-Operationen funktionieren wie mathematische Mengenoperationen. Sie brauchen kompatible Strukturen: gleiche Anzahl Spalten, passende Datentypen.

---

### UNION: Vereinigung (ohne Duplikate)

    --{{0}}--
UNION kombiniert Ergebnisse zweier Queries und entfernt Duplikate.

**Beispiel:** Liste aller Städte – aus Kunden UND aus einer Lieferantentabelle (die wir simulieren).

```sql
SELECT city FROM customers
UNION
SELECT 'Stuttgart' AS city
UNION
SELECT 'Berlin' AS city;
```
@SQL.exec

    {{1}}
**Ergebnis:** Jede Stadt nur einmal (Berlin erscheint nur einmal, obwohl es bei Kunden vorkommt).

---

### UNION ALL: Vereinigung (mit Duplikaten)

    --{{0}}--
UNION ALL behält alle Zeilen – Duplikate inklusive.

```sql
SELECT city FROM customers
UNION ALL
SELECT 'Stuttgart' AS city
UNION ALL
SELECT 'Berlin' AS city;
```
@SQL.exec

    {{1}}
**Ergebnis:** Berlin erscheint mehrfach.

    --{{2}}--
UNION ALL ist schneller als UNION, weil keine Duplikate-Prüfung nötig ist. Nutzen Sie UNION ALL, wenn Sie sicher sind, dass keine Duplikate entstehen – oder Duplikate ok sind.

---

### INTERSECT: Schnittmenge

    --{{0}}--
INTERSECT gibt nur Zeilen zurück, die in beiden Ergebnissen vorkommen.

**Beispiel:** Welche Städte haben sowohl Kunden als auch (hypothetische) Lieferanten?

```sql
SELECT city FROM customers
INTERSECT
SELECT city FROM (
  VALUES ('Berlin'), ('Munich'), ('Vienna')
) AS suppliers(city);
```
@SQL.exec

    {{1}}
**Ergebnis:** Nur Berlin und Munich (Vienna hat keine Kunden).

---

### EXCEPT: Differenz

    --{{0}}--
EXCEPT (in einigen DBMS `MINUS`) gibt Zeilen aus der ersten Query zurück, die NICHT in der zweiten vorkommen.

**Beispiel:** Welche Städte haben Kunden, aber keine (hypothetischen) Lieferanten?

```sql
SELECT city FROM customers
EXCEPT
SELECT city FROM (
  VALUES ('Berlin'), ('Munich')
) AS suppliers(city);
```
@SQL.exec

    {{1}}
**Ergebnis:** Hamburg, Cologne, Frankfurt (Berlin und Munich sind ausgeschlossen).

---

### Bedingungen für Set-Operationen

    --{{0}}--
Damit Set-Operationen funktionieren, müssen beide Queries kompatibel sein:

1. **Gleiche Anzahl Spalten**
2. **Kompatible Datentypen** (Position für Position)
3. **Spaltennamen aus erster Query** (zweite Query ignoriert Namen)

```sql
-- ❌ Fehler: Unterschiedliche Spaltenanzahl
SELECT first_name, last_name FROM customers
UNION
SELECT product_name FROM products;

-- ✅ Korrekt: Gleiche Spaltenanzahl
SELECT first_name FROM customers
UNION
SELECT product_name FROM products;
```

---

## Join-Strategien & Performance

    --{{0}}--
Bisher haben wir uns auf die Syntax konzentriert. Aber was passiert intern? Wie führt die Datenbank Joins aus?

### Join-Algorithmen (Übersicht)

    {{1}}
**1. Nested Loop Join**

    {{1}}
- Für jede Zeile der äußeren Tabelle durchsucht die Datenbank die innere Tabelle
- Einfach, aber langsam bei großen Tabellen
- Gut bei: Kleine äußere Tabelle × große innere (mit Index!)

    {{2}}
**2. Hash Join**

    {{2}}
- Erstellt Hash-Tabelle für eine Tabelle, scannt die andere
- Schnell bei großen Tabellen mit Gleichheitsbedingung (`=`)
- Braucht Speicher für Hash-Tabelle

    {{3}}
**3. Merge Join**

    {{3}}
- Beide Tabellen werden sortiert, dann parallel gescannt
- Sehr schnell, wenn Daten bereits sortiert sind
- Gut bei vorhandenen Indexes auf Join-Spalten

    --{{4}}--
Welcher Algorithmus gewählt wird, entscheidet der Query Optimizer basierend auf Statistiken, Indexes und Datenmenge.

---

### EXPLAIN: Query Plans analysieren

    --{{0}}--
Mit `EXPLAIN` sehen Sie, wie die Datenbank Ihre Query ausführt.

```sql
EXPLAIN QUERY PLAN
SELECT c.first_name, o.order_id
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
```

    {{1}}
**Typisches Ergebnis:**

    {{1}}
```
QUERY PLAN
|--SCAN customers AS c
`--SEARCH orders AS o USING INDEX orders_customer_id (customer_id=?)
```

    --{{2}}--
Hier sehen Sie: Die Datenbank scannt alle Kunden, sucht dann für jeden Kunden in der orders-Tabelle via Index. Das ist ein Nested Loop Join mit Index-Lookup.

---

### Index auf Join-Spalten (essentiell!)

    --{{0}}--
Ohne Indexes auf Join-Spalten (besonders Foreign Keys!) werden Joins extrem langsam.

```sql
-- ❌ Kein Index auf orders.customer_id:
-- Für jeden Kunden muss die gesamte orders-Tabelle gescannt werden!

-- ✅ Mit Index:
CREATE INDEX idx_orders_customer ON orders(customer_id);
-- Lookup ist O(log n) statt O(n)
```

    {{1}}
> **Best Practice:** Erstellen Sie immer Indexes auf Foreign Key-Spalten!

---

### Join-Reihenfolge optimieren

    --{{0}}--
Bei Multi-Table Joins kann die Reihenfolge die Performance beeinflussen.

**Faustregel:** Joinen Sie kleinere Tabellen zuerst, filtern Sie früh.

```sql
-- ❌ Schlechter Plan:
SELECT * 
FROM huge_table
INNER JOIN small_table ON ...
WHERE small_table.status = 'active';

-- ✅ Besserer Plan:
SELECT * 
FROM small_table
INNER JOIN huge_table ON ...
WHERE small_table.status = 'active';
-- Filter auf small_table wird zuerst angewendet
```

    {{1}}
**Noch besser:** Nutzen Sie Subqueries/CTEs, um vor dem Join zu filtern.

    {{1}}
```sql
WITH active_small AS (
  SELECT * FROM small_table WHERE status = 'active'
)
SELECT * FROM active_small
INNER JOIN huge_table ON ...;
```

---

## Erweiterte Join-Techniken

### JOIN mit mehreren Bedingungen

    --{{0}}--
Sie können mehrere Bedingungen im ON kombinieren.

```sql
SELECT *
FROM customers c
INNER JOIN orders o 
  ON c.customer_id = o.customer_id 
  AND o.status = 'completed';
-- Nur abgeschlossene Bestellungen
```
@SQL.exec

    {{1}}
**Unterschied zu WHERE:**

    {{1}}
```sql
-- Bei INNER JOIN: ON vs. WHERE ist (oft) äquivalent
-- Bei LEFT JOIN: ON filtert vor dem Join, WHERE filtert nach dem Join!

-- Beispiel: LEFT JOIN + Bedingung im ON
SELECT c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o 
  ON c.customer_id = o.customer_id 
  AND o.status = 'completed';
-- Alle Kunden, nur completed Orders (andere Orders werden NULL)

-- vs. Bedingung im WHERE:
SELECT c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed';
-- Nur Kunden mit completed Orders (funktioniert wie INNER JOIN!)
```

    --{{2}}--
Bei LEFT/RIGHT/FULL OUTER Joins macht der Ort der Bedingung einen Unterschied!

---

### Range Joins (Non-Equi Joins)

    --{{0}}--
Joins müssen nicht immer auf Gleichheit (`=`) basieren.

```sql
-- Beispiel: Zeiträume überlappen
SELECT 
  e1.employee_name AS emp1,
  e2.employee_name AS emp2
FROM employment e1
INNER JOIN employment e2 
  ON e1.start_date <= e2.end_date 
  AND e1.end_date >= e2.start_date
  AND e1.employee_id < e2.employee_id;
-- Findet Mitarbeiter, deren Beschäftigungszeiten sich überlappen
```

    {{1}}
**Use Cases:** Zeitreihen-Overlaps, Preis-Ranges, geografische Bereiche.

---

### JOIN mit Aggregation

    --{{0}}--
Sie können nach einem Join aggregieren – oder vor dem Join aggregieren (in einer Subquery).

**Nach dem Join:**

```sql
SELECT 
  c.first_name,
  COUNT(o.order_id) AS order_count,
  SUM(o.total_amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name;
```
@SQL.exec

    {{1}}
**Vor dem Join (Subquery):**

    {{1}}
```sql
SELECT 
  c.first_name,
  COALESCE(order_stats.order_count, 0) AS order_count,
  COALESCE(order_stats.total_spent, 0) AS total_spent
FROM customers c
LEFT JOIN (
  SELECT 
    customer_id,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_spent
  FROM orders
  GROUP BY customer_id
) order_stats ON c.customer_id = order_stats.customer_id;
```
@SQL.exec

    --{{2}}--
Zweite Variante ist oft performanter: Sie aggregieren zuerst (kleineres Ergebnis), dann joinen Sie.

---

## Zusammenfassung & Entscheidungsmatrix

    --{{0}}--
Wann nutzen Sie welchen Join? Hier ist Ihre Entscheidungshilfe:

| Szenario                                      | Join-Typ                       |
|-----------------------------------------------|--------------------------------|
| Nur Datensätze mit Match                      | **INNER JOIN**                 |
| Alle von Tabelle A, auch ohne Match           | **LEFT JOIN**                  |
| Fehlende Beziehungen finden (A ohne B)        | **LEFT JOIN + IS NULL** oder **NOT EXISTS** |
| Daten-Sync-Vergleich (A vs. B vollständig)    | **FULL OUTER JOIN**            |
| Alle Kombinationen erzeugen                   | **CROSS JOIN** (mit Vorsicht!) |
| Hierarchie/Rekursion (eine Ebene)             | **Self Join**                  |
| Ergebnisse vertikal kombinieren               | **UNION** / **INTERSECT** / **EXCEPT** |

    --{{1}}--
90% aller Joins in Produktion sind INNER oder LEFT. Beherrschen Sie diese beiden, und Sie sind für die meisten Szenarien gerüstet.

---

## Live-Demo: Komplexe Multi-Table Query

    --{{0}}--
Zum Abschluss eine komplexe Query, die alles kombiniert.

**Aufgabe:** Zeigen Sie für jeden Kunden:

- Name
- Anzahl Bestellungen
- Gesamtumsatz
- Meist gekaufte Produkt-Kategorie

```sql
SELECT 
  c.first_name || ' ' || c.last_name AS customer,
  COUNT(DISTINCT o.order_id) AS order_count,
  COALESCE(SUM(o.total_amount), 0) AS total_spent,
  (
    SELECT p.category
    FROM order_items oi
    INNER JOIN products p ON oi.product_id = p.product_id
    WHERE oi.order_id IN (
      SELECT order_id FROM orders WHERE customer_id = c.customer_id
    )
    GROUP BY p.category
    ORDER BY SUM(oi.quantity) DESC
    LIMIT 1
  ) AS favorite_category
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;
```
@SQL.exec

    --{{1}}--
Diese Query nutzt LEFT JOIN, GROUP BY, Subquery und Aggregation. Solche Queries sind in der Praxis Standard für analytische Berichte.

---

## Reflexionsfragen

    --{{0}}--
Bevor wir schließen, zwei Fragen zum Nachdenken:

    {{1}}
> **Frage 1:** Wann würden Sie LEFT JOIN statt INNER JOIN nutzen? Geben Sie zwei konkrete Beispiele.

    {{2}}
<details>
<summary>Mögliche Antworten</summary>

- Kunden ohne Bestellungen finden (Inaktive identifizieren)
- Produkte ohne Verkäufe (Ladenhüter-Analyse)
- Mitarbeiter ohne zugewiesene Projekte
- Kategorien ohne zugehörige Artikel

</details>

    {{3}}
> **Frage 2:** Was ist der Unterschied zwischen UNION und UNION ALL? Welches ist schneller und warum?

    {{4}}
<details>
<summary>Antwort</summary>

- **UNION:** Entfernt Duplikate (benötigt zusätzlichen Schritt: Sortieren/Hashing)
- **UNION ALL:** Behält alle Zeilen, keine Duplikate-Prüfung
- **Schneller:** UNION ALL (keine Overhead für Duplikate-Entfernung)
- **Nutzen Sie UNION ALL**, wenn keine Duplikate erwartet oder Duplikate ok sind

</details>

---

## 1-Minute-Paper

    --{{0}}--
Zum Abschluss eine Minute Zeit zum Nachdenken:

> **Was ist heute klarer geworden?**  
> Notieren Sie 1–2 Sätze:
>
> - Was war neu für Sie?
> - Welches Konzept hat „Klick" gemacht?
> - Gibt es noch Unklarheiten?

    {{1}}
**Teilen Sie Ihre Gedanken im Forum oder in der nächsten Übung!**

---

## Ausblick: Session 11

    --{{0}}--
In der nächsten Session tauchen wir in **Row-Level Functions** ein: String-Manipulation, Zahlen-Funktionen, Datum-Operationen, CASE-Statements.

Sie lernen, Daten innerhalb von Zeilen zu transformieren – bevor Sie aggregieren oder joinen.

**Bis dahin:**

- Üben Sie Joins mit Übung E4
- Probieren Sie Anti-Joins auf eigenen Daten
- Experimentieren Sie mit EXPLAIN (wenn verfügbar)

---

## Referenzen & Quellen

### Offizielle Dokumentation

- [PostgreSQL: Joins](https://www.postgresql.org/docs/current/tutorial-join.html)
- [DuckDB: FROM Clause & Joins](https://duckdb.org/docs/sql/query_syntax/from)
- [SQLite: Query Language](https://www.sqlite.org/lang_select.html)
- [ISO SQL Standard (9075)](https://www.iso.org/standard/63555.html)

### Visualisierungen

- [SQL Joins Visualized](https://joins.spathon.com/) – Interaktive Venn-Diagramme
- [Visual Representation of SQL Joins](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins)

### Best Practices & Performance

- [Use The Index, Luke: SQL Joins](https://use-the-index-luke.com/sql/join) – Performance-Guide
- [Modern SQL: Join](https://modern-sql.com/feature/join) – SQL-99/2003 Features
- [PostgreSQL Wiki: Join Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)

### Weiterführende Themen

- **Subqueries & CTEs:** Session 13
- **Window Functions:** Session 12 (Aggregation mit Kontext)
- **Query Plans & EXPLAIN:** Session 15 (Performance Optimization)
- **Recursive CTEs:** Session 13 (Hierarchien & Graphen)

---

## Übung E4: Hands-on Joins & Set Operations

    --{{0}}--
Die Übung zu dieser Session finden Sie in `materials/4-exercise.md`.

**Aufgaben:**

1. Einfache Joins (INNER, LEFT)
2. Multi-Table Queries (3+ Tabellen)
3. Anti-Joins (fehlende Beziehungen)
4. Set-Operationen (UNION, INTERSECT, EXCEPT)
5. Performance-Vergleich (EXPLAIN für verschiedene Join-Strategien)

**Datensets:**

- E-Commerce Schema (Customers, Orders, Products, Order_Items)
- Erweitert um: Categories, Suppliers, Inventory

---

**Viel Erfolg – und bis zur nächsten Session! 🚀**
