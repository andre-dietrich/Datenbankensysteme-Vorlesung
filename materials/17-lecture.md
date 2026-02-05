<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  1.0.0
language: de
narrator: Deutsch Female

logo:     ../assets/img/logo/17-lecture.jpg

comment:  RESTful APIs & SQL – HTTP-Requests in SQL-Queries übersetzen. Hands-on Übungen mit simulierter Browser-API für praktische CRUD-Operationen im E-Commerce-Kontext.

@async.eval
<script>
setTimeout(async function() {
  @input
  send.lia("LIA: stop")
}, 100);

"LIA: wait"
</script>
@end

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

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  display: inline-block;
  width: 220px;
  vertical-align: top;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.product-card h4 {
  margin: 10px 0;
  color: #333;
}

.product-card .price {
  font-size: 1.2em;
  font-weight: bold;
  color: #2c5aa0;
}

.product-card button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.product-card button:hover {
  background-color: #c82333;
}

.api-response {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 15px;
  margin: 10px 0;
  font-family: monospace;
  white-space: pre-wrap;
  max-height: 400px;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.btn-primary:hover {
  background-color: #0056b3;
}

table.product-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

table.product-table th,
table.product-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

table.product-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

table.product-table tr:hover {
  background-color: #f5f5f5;
}
@end

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md
        https://raw.githubusercontent.com/LiaTemplates/dbdiagram/main/README.md

-->

# L17: RESTful APIs & SQL – Online-Shop Backend

> **Session 17 – Lecture**
>
> **Dauer:** 90 Minuten
>
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)
>
> **Block:** 4 – Theorie, Optimierung & Polyglot

    --{{0}}--
Willkommen zur siebzehnten Session! Heute verbinden wir zwei Welten: RESTful APIs und SQL. Sie lernen, wie moderne Web-APIs funktionieren und wie HTTP-Requests in SQL-Queries übersetzt werden. Das Besondere: Wir simulieren eine vollständige REST-API direkt im Browser – mit echter SQL-Ausführung in PGlite!

    --{{1}}--
Stellen Sie sich vor: Sie bauen das Backend für einen Online-Shop. Frontend-Developer schicken HTTP-Requests an Ihre API, und Sie müssen diese in SQL-Queries übersetzen. Genau das üben wir heute – praxisnah und interaktiv!

## Motivation: Warum REST & SQL?

    --{{0}}--
Bevor wir loslegen, schauen wir uns an, wie RESTful APIs in der Praxis eingesetzt werden.

    {{1}}
**Szenario: Online-Shop Architecture**

    {{1}}
```ascii
┌─────────────┐         HTTP GET /products         ┌──────────────┐
│   Browser   │ ---------------------------------> │  REST API    │
│  (Frontend) │                                    │  (Backend)   │
└─────────────┘                                    └──────────────┘
                                                           |
                                                           | SELECT * FROM products
                                                           V
                                                   ┌──────────────┐
                                                   │  PostgreSQL  │
                                                   │  Database    │
                                                   └──────────────┘
```

    --{{2}}--
In echten Systemen übersetzt ein Backend-Server (z.B. Node.js, Python, Java) HTTP-Requests in SQL-Queries. Heute lernen Sie genau diese Übersetzung – und bauen sie selbst!

    {{3}}
**Live-Demo: Echte REST-API erkunden**

    --{{3}}--
Schauen wir uns zuerst eine echte öffentliche API an: die Fake Store API. Öffnen Sie die folgenden URLs in einem neuen Tab und beobachten Sie die JSON-Responses:

    {{3}}
- 🛍️ **Alle Produkte**: https://fakestoreapi.com/products
- 📦 **Ein Produkt**: https://fakestoreapi.com/products/1
- 📂 **Kategorien**: https://fakestoreapi.com/products/categories
- 🔍 **Elektronik**: https://fakestoreapi.com/products/category/electronics

    {{4}}
**Interaktive Demo: API im Browser testen**

    {{4}}
<div id="fake-store-demo"></div>

    {{4}}
``` js
async function loadFakeStoreProducts() {
  try {
    const response = await fetch('https://fakestoreapi.com/products?limit=5');
    const products = await response.json();

    console.table(products);
  } catch (error) {
    console.error(error.message);
  }
}

loadFakeStoreProducts();
```
<script>@input</script>

    --{{5}}--
Beeindruckend, oder? Diese Daten kommen von einem echten Server. Heute bauen Sie eine identische API – aber die Daten kommen aus Ihrer eigenen SQL-Datenbank im Browser!

## Teil 1: Was ist eine REST-API?

    --{{0}}--
REST steht für "Representational State Transfer" – ein Architekturstil für Web-APIs. Klingt kompliziert? Ist es nicht! Im Kern geht es um vier einfache HTTP-Methoden.

### HTTP-Methoden & CRUD

    --{{0}}--
REST nutzt HTTP-Methoden, um Operationen auf Ressourcen auszuführen. Diese mappen direkt auf SQL-Operationen!

    {{1}}
| HTTP-Methode | Bedeutung                     | SQL-Operation | Beispiel-URL         |
| ------------ | ----------------------------- | ------------- | -------------------- |
| **GET**      | Daten abrufen (Read)          | `SELECT`      | `GET /products`      |
| **POST**     | Neue Daten erstellen (Create) | `INSERT`      | `POST /products`     |
| **PUT**      | Daten aktualisieren (Update)  | `UPDATE`      | `PUT /products/5`    |
| **DELETE**   | Daten löschen (Delete)        | `DELETE`      | `DELETE /products/5` |

    --{{2}}--
Das Schöne: HTTP-Methoden und SQL-Operationen haben eine natürliche 1:1-Beziehung. GET wird zu SELECT, POST zu INSERT, DELETE zu DELETE!

### URL-Struktur & Ressourcen

    --{{0}}--
REST-APIs arbeiten mit Ressourcen, die über URLs identifiziert werden. Ressourcen entsprechen meist Datenbank-Tabellen.

    {{1}}
**URL-Pattern:**

    {{1}}
```
https://api.example.com/ressource
https://api.example.com/ressource/{id}
https://api.example.com/ressource?filter=value
```

    {{2}}
**Konkrete Beispiele:**

    {{2}}
| URL                                  | Beschreibung             | SQL-Äquivalent                                          |
| ------------------------------------ | ------------------------ | ------------------------------------------------------- |
| `GET /products`                      | Alle Produkte            | `SELECT * FROM products`                                |
| `GET /products/5`                    | Produkt mit ID 5         | `SELECT * FROM products WHERE product_id = 5`           |
| `GET /products?category=Electronics` | Gefilterte Produkte      | `SELECT * FROM products WHERE category = 'Electronics'` |
| `GET /customers/3/orders`            | Bestellungen von Kunde 3 | `SELECT * FROM orders WHERE customer_id = 3`            |

    --{{3}}--
Sehen Sie das Muster? URLs beschreiben die Daten, die Sie wollen – und Sie übersetzen das in SQL!

### HTTP-Status Codes

    --{{0}}--
APIs kommunizieren Erfolg oder Fehler über HTTP-Status Codes. Die wichtigsten sollten Sie kennen.

    {{1}}
| Status Code                   | Bedeutung                | Wann verwenden?                      |
| ----------------------------- | ------------------------ | ------------------------------------ |
| **200 OK**                    | Erfolg                   | Daten erfolgreich abgerufen/geändert |
| **201 Created**               | Ressource erstellt       | Nach erfolgreichem INSERT            |
| **400 Bad Request**           | Ungültige Anfrage        | Fehlende/falsche Parameter           |
| **404 Not Found**             | Ressource nicht gefunden | Keine Daten in Datenbank             |
| **500 Internal Server Error** | Server-Fehler            | SQL-Fehler, Constraint-Verletzung    |

    --{{2}}--
Diese Codes helfen dem Frontend zu verstehen, was passiert ist – ohne die Response-Daten zu parsen!

### JSON als Datenformat

    --{{0}}--
REST-APIs senden und empfangen Daten im JSON-Format. JSON ist leichtgewichtig und JavaScript-nativ.

    {{1}}
**Response-Beispiel:**

    {{1}}
```json
{
  "data": [
    {
      "product_id": 1,
      "product_name": "Laptop",
      "price": 999.99
    },
    {
      "product_id": 2,
      "product_name": "Mouse",
      "price": 29.99
    }
  ],
  "status": "success",
  "count": 2
}
```

    --{{2}}--
Ihre SQL-Query-Ergebnisse werden in dieses Format konvertiert – automatisch durch die API-Schicht!

## Teil 2: HTTP → SQL Mapping

    --{{0}}--
Jetzt wird es praktisch! Wir schauen uns an, wie jede HTTP-Operation in eine SQL-Query übersetzt wird.

### GET → SELECT

    --{{0}}--
GET-Requests rufen Daten ab – das einfachste Mapping.

    {{1}}
**Pattern 1: Alle Ressourcen**

    {{1}}
```
GET /products
↓
SELECT * FROM products ORDER BY product_name;
```

    {{2}}
**Pattern 2: Eine Ressource nach ID**

    {{2}}
```
GET /products/5
↓
SELECT * FROM products WHERE product_id = 5;
```

    {{3}}
**Pattern 3: Gefilterte Ressourcen**

    {{3}}
```
GET /products?category=Electronics
↓
SELECT p.* 
FROM products p
INNER JOIN product_categories pc ON p.product_id = pc.product_id
INNER JOIN categories c ON pc.category_id = c.category_id
WHERE c.category_name = 'Electronics';
```

    {{4}}
**Pattern 4: Verschachtelte Ressourcen (Joins)**

    {{4}}
```
GET /customers/3/orders
↓
SELECT o.*
FROM orders o
WHERE o.customer_id = 3
ORDER BY o.order_date DESC;
```

    --{{5}}--
Sehen Sie das Muster? URL-Parameter werden zu WHERE-Bedingungen, verschachtelte Pfade zu Joins!

### POST → INSERT

    --{{0}}--
POST-Requests erstellen neue Daten. Der Request-Body enthält die Werte.

    {{1}}
**Request:**

    {{1}}
```http
POST /products
Content-Type: application/json

{
  "product_name": "Webcam",
  "price": 89.99
}
```

    {{2}}
**SQL-Translation:**

    {{2}}
```sql
INSERT INTO products (product_name, price)
VALUES ('Webcam', 89.99)
RETURNING product_id, product_name, price;
```

    --{{3}}--
Wichtig: RETURNING gibt die neu erstellte Zeile zurück – inklusive auto-generierter ID! Das ist das Ergebnis der POST-Response.

    {{4}}
**Response:**

    {{4}}
```json
{
  "data": {
    "product_id": 10,
    "product_name": "Webcam",
    "price": 89.99
  },
  "status": "success",
  "message": "Product created"
}
```

### DELETE → DELETE

    --{{0}}--
DELETE-Requests entfernen Daten.

    {{1}}
**Request:**

    {{1}}
```
DELETE /products/7
```

    {{2}}
**SQL-Translation:**

    {{2}}
```sql
DELETE FROM products WHERE product_id = 7;
```

    {{3}}
**Response:**

    {{3}}
```json
{
  "status": "success",
  "message": "Product deleted",
  "deleted_id": 7
}
```

    --{{4}}--
Achtung: Was passiert, wenn das Produkt in order_items referenziert wird? Foreign Key Constraint! Das ist ein 500-Fehler – dazu später mehr.

### PUT/PATCH → UPDATE (Optional)

    --{{0}}--
PUT aktualisiert eine komplette Ressource, PATCH nur Teile davon. Heute fokussieren wir auf POST und DELETE, aber hier das Konzept:

    {{1}}
```http
PUT /products/5
Content-Type: application/json

{
  "product_name": "Gaming Mouse Pro",
  "price": 39.99
}
```

    {{1}}
```sql
UPDATE products
SET product_name = 'Gaming Mouse Pro',
    price = 39.99
WHERE product_id = 5
RETURNING *;
```

## Datenbank-Setup: Online-Shop

    --{{0}}--
Bevor wir mit der API-Implementierung starten, initialisieren wir unsere Datenbank. Wir nutzen das bekannte E-Commerce-Schema.

```sql
-- Locations
CREATE TABLE locations (
  location_id INTEGER PRIMARY KEY,
  city TEXT NOT NULL,
  postal_code TEXT NOT NULL,
  country TEXT DEFAULT 'Germany'
);

-- Categories
CREATE TABLE categories (
  category_id INTEGER PRIMARY KEY,
  category_name TEXT NOT NULL UNIQUE,
  description TEXT
);

-- Customers
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT UNIQUE,
  street TEXT,
  street_number TEXT,
  location_id INTEGER REFERENCES locations(location_id)
);

-- Orders
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(customer_id),
  order_date DATE,
  total_amount DECIMAL(10,2),
  status TEXT
);

-- Products
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  product_name TEXT NOT NULL,
  price DECIMAL(10,2)
);

-- Product_Categories
CREATE TABLE product_categories (
  product_id INTEGER REFERENCES products(product_id),
  category_id INTEGER REFERENCES categories(category_id),
  PRIMARY KEY (product_id, category_id)
);

-- Order_Items
CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id INTEGER REFERENCES orders(order_id),
  product_id INTEGER REFERENCES products(product_id),
  quantity INTEGER,
  line_total DECIMAL(10,2)
);

-- Sample Data
INSERT INTO locations VALUES (1, 'Berlin', '10115', 'Germany'), (2, 'Hamburg', '20095', 'Germany');
INSERT INTO categories VALUES (1, 'Electronics', 'Electronic devices'), (2, 'Furniture', 'Office furniture');
INSERT INTO customers VALUES 
  (1, 'Alice', 'Smith', 'alice@example.com', 'Main St', '42', 1),
  (2, 'Bob', 'Johnson', 'bob@example.com', 'Oak Ave', '15', 2);
INSERT INTO products (product_name, price) VALUES 
  ('Laptop', 999.99), ('Mouse', 29.99), ('Keyboard', 79.99),
  ('Monitor', 299.99), ('Desk Chair', 199.99);
INSERT INTO product_categories VALUES (1,1), (2,1), (3,1), (4,1), (5,2);
INSERT INTO orders VALUES (101, 1, '2024-01-15', 299.99, 'delivered'), (102, 2, '2024-01-22', 999.99, 'delivered');
INSERT INTO order_items VALUES (1, 101, 4, 1, 299.99), (2, 102, 1, 1, 999.99);
```
@PGlite.eval(online-shop)

    --{{1}}--
Perfekt! Unsere Datenbank ist bereit. Jetzt implementieren wir die API-Schicht!

``` sql Playground
ERDIAGRAM
```
@PGlite.terminal(online-shop)

## Teil 3: API-Setup – fetch-Override

    --{{0}}--
Hier kommt die Magie: Wir überschreiben die globale `fetch`-Funktion, um HTTP-Requests abzufangen und in SQL-Queries zu übersetzen!

    {{1}}
**Architektur:**

    {{1}}
```ascii
JavaScript Code                          Browser Database
─────────────────                        ────────────────
                                         
fetch('http://little-amazon.com/products')
    │
    ├──> URL-Prüfung: little-amazon.com?
    │
    └──> JA → Route zu SQL mappen
         │
         ├──> SQL in PGlite ausführen
         │
         └──> JSON-Response zurückgeben
```

    {{2}}
**Implementation (vorgegeben):**

    {{2}}
``` javascript -Router.js
// ========== Einfacher Router (inspiriert von Express.js) ==========
class SimpleRouter {
  constructor() {
    this.routes = { GET: {}, POST: {}, DELETE: {} };
    this._requestBody = null;
  }
  
  get(path, handler) {
    this.routes.GET[path] = { pattern: this._pathToRegex(path), handler };
  }
  
  post(path, handler) {
    this.routes.POST[path] = { pattern: this._pathToRegex(path), handler };
  }
  
  delete(path, handler) {
    this.routes.DELETE[path] = { pattern: this._pathToRegex(path), handler };
  }
  
  _pathToRegex(path) {
    // Konvertiert /products/:id zu Regex mit Named Groups
    const paramNames = [];
    const regexPattern = path
      .replace(/:\w+/g, (match) => {
        paramNames.push(match.slice(1)); // ':id' -> 'id'
        return '([^/]+)'; // Match alles außer /
      })
      .replace(/\//g, '\\/'); // Escape /
    
    return { regex: new RegExp(`^${regexPattern}$`), paramNames };
  }
  
  async handle(method, path, body) {
    // Body für POST-Handler verfügbar machen
    if (body) {
      try {
        this._requestBody = JSON.parse(body);
      } catch (e) {
        this._requestBody = body;
      }
    }
    
    const routes = this.routes[method] || {};
    
    for (const [routePath, route] of Object.entries(routes)) {
      const match = path.match(route.pattern.regex);
      if (match) {
        // Extrahiere Parameter (z.B. { id: '5' })
        const params = {};
        route.pattern.paramNames.forEach((name, i) => {
          params[name] = match[i + 1];
        });
        
        try {
          return await route.handler(params, this._requestBody);
        } catch (error) {
          return {
            status: 'error',
            message: `Handler error: ${error.message}`,
            httpStatus: 500
          };
        }
      }
    }
    
    return { status: 'error', message: 'Endpoint not found', httpStatus: 404 };
  }
}

// Router-Instanz erstellen
const router = new SimpleRouter();
window.router = router;
```
``` js     -Fetch.js
// ========== Globaler fetch-Override ==========
window.originalFetch = window.fetch;

window.fetch = async function(url, options = {}) {
  // Nur little-amazon.com abfangen
  if (typeof url === 'string' && url.startsWith('http://little-amazon.com')) {
    const path = url.replace('http://little-amazon.com', '');
    const method = options.method || 'GET';
    
    try {
      const result = await router.handle(method, path, options.body);
      return new Response(JSON.stringify(result), {
        status: result.httpStatus || 200,
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (error) {
      return new Response(JSON.stringify({
        status: 'error',
        message: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
  
  // Normale Requests durchreichen
  return window.originalFetch(url, options);
};

// ========== Routen definieren (TODO: Implementieren Sie die Handler!) ==========

// Syntax-Beispiele (noch nicht implementiert):
//
// router.get('/products', async (params) => {
//   // Handler für GET /products
//   return { status: 'success', data: [...], httpStatus: 200 };
// });
//
// router.get('/products/:id', async (params) => {
//   const productId = params.id;  // ✨ Parameter automatisch extrahiert!
//   // Handler für GET /products/:id
// });
//
// router.post('/products', async (params) => {
//   const data = router._requestBody;  // Body als JSON-Objekt
//   // Handler für POST /products
// });
//
// router.delete('/products/:id', async (params) => {
//   const productId = params.id;
//   // Handler für DELETE /products/:id
// });

console.log('✅ Little Amazon API mit Router loaded!');
console.log('📚 Routen-Syntax: router.get("/products/:id", async (params) => { ... })');
console.log('ℹ️  Response-Format: { status: "success"|"error", data: [...], httpStatus: 200|404|500 }');
```
<script>
@input(0)

@input(1)
</script>

    --{{3}}--
Perfekt! Jetzt haben wir einen eleganten Router! Statt verschachtelter if/else nutzen Sie `router.get('/products/:id', handler)` – genau wie in Express.js oder Next.js!

## Teil 4: Hands-on – SELECT Queries

    --{{0}}--
Beginnen wir mit GET-Requests. Ihre Aufgabe: Schreiben Sie SQL-Queries für verschiedene API-Endpunkte!

### Aufgabe 1: Alle Produkte laden

    --{{0}}--
Implementieren Sie `GET /products` – zeigen Sie alle Produkte an.

    {{1}}
**TODO: Ersetzen Sie den Handler mit Ihrer SQL-Query**

    {{1}}
```javascript
// TODO: Implementieren Sie den Handler für GET /products
router.get('/products', async (params) => {
  // Ihre SQL-Query hier:
  const query = `
    -- SELECT alle Produkte, sortiert nach product_name
    
  `;
  
  const result = await db.query(query);
  return {
    status: 'success',
    data: result.rows,
    count: result.rows.length,
    httpStatus: 200
  };
});

console.debug('✅ GET /products implementiert');
```
@PGlite.js(online-shop)

    {{2}}
**Test: Rufen Sie die API auf!**

    {{2}}
``` javascript
try {
  const response = await fetch('http://little-amazon.com/products');
  const data = await response.json();

  if (data.status === 'error') {
    throw new Error(data.message || 'Unknown error');
  }

  console.table(data.data);
} catch (error) {
  console.error(error.message);
}
```
@async.eval

    --{{3}}--
Sobald Ihre Query funktioniert, sehen Sie die Produktliste! Falls "not implemented" erscheint, fehlt noch die SQL-Query.

### Aufgabe 2: Produkt nach ID

    --{{0}}--
Implementieren Sie `GET /products/{id}` – zeigen Sie ein einzelnes Produkt.

    {{1}}
**TODO: Erweitern Sie handleGET() um ID-Routing**

    {{1}}
```javascript
router.get('/products/:id', async (params) => {
  const productId = params.id;

  const query = `
    -- TODO: product_id = ${productId}
      
  `;

  const result = await db.query(query);

  if (result.rows.length === 0) {
    return { status: 'error', message: 'Product not found', httpStatus: 404 };
  }
  
  return { status: 'success', data: result.rows, httpStatus: 200 };
});

console.debug('✅ GET /products/:id implementiert');
```
@PGlite.js(online-shop)

---

    {{2}}
``` javascript
try {
  const response = await fetch('http://little-amazon.com/products/2');
  const data = await response.json();

  if (data.status === 'error') {
    throw new Error(data.message || 'Unknown error');
  }

  console.table(data.data);
} catch (error) {
  console.error(error.message);
}
```
@async.eval

### Aufgabe 3: Produkte einer Kategorie (JOIN)

    --{{0}}--
Implementieren Sie `GET /products/category/{name}` – nutzen Sie einen JOIN!

    {{1}}
**TODO: Erweitern Sie handleGET() um Kategorie-Filter**

    {{1}}
```javascript
router.get('/products/category/:name', async (params) => {
  const categoryName = decodeURIComponent(params.name);

  const query = `
    -- TODO: SELECT mit JOIN über product_categories und categories
    -- WHERE c.category_name = '${categoryName}'
  
  `;
  
  const result = await db.query(query);
  return { status: 'success', data: result.rows, count: result.rows.length };
});

console.debug('✅ GET /products/category/{name} implementiert');
```
@PGlite.js(online-shop)


    {{2}}
``` javascript
try {
  const response = await fetch('http://little-amazon.com/products/category/Electronics');
  const data = await response.json();

  if (data.status === 'error') {
    throw new Error(data.message || 'Unknown error');
  }

  console.table(data.data);
} catch (error) {
  console.error(error.message);
}
```
@async.eval


### Aufgabe 4: Kunden mit Bestellungen (JOIN + Aggregation)

    --{{0}}--
Implementieren Sie `GET /customers/{id}/orders` – zeigen Sie alle Bestellungen eines Kunden.


    {{1}}
```javascript
router.get('/customers', async () => {
  const query = `
    -- TODO: SELECT alle Kunden
  `;
  
  const result = await db.query(query);
  return { status: 'success', data: result.rows, count: result.rows.length };
});


console.debug('✅ GET /customers implementiert');

router.get('/customers/:id/orders', async (params) => {
  const customerId = params.id;
  
  const query = `
    -- WHERE c.customer_id = '${customerId}'
    
  `;

  const result = await db.query(query);
  return { status: 'success', data: result.rows, count: result.rows.length };
});

console.debug('✅ GET /customers/:id/orders implementiert');
```
@PGlite.js(online-shop)

---

    {{2}}
``` javascript
try {
  const response = await fetch('http://little-amazon.com/customers/1/orders');
  const data = await response.json();

  if (data.status === 'error') {
    throw new Error(data.message || 'Unknown error');
  }

  console.table(data.data);
} catch (error) {
  console.error(error.message);
}
```
@async.eval


## Teil 5: Hands-on – INSERT Queries

    --{{0}}--
Jetzt wird es spannend: POST-Requests erstellen neue Daten! Der Request-Body enthält die Werte als JSON.

### Aufgabe 5: Neues Produkt hinzufügen

    --{{0}}--
Implementieren Sie `POST /products` – erstellen Sie ein neues Produkt.

    {{1}}
**TODO: Implementieren Sie POST-Handler mit Body-Parsing**

    {{1}}
```javascript
// TODO: Implementieren Sie POST /products
router.post('/products', async (params) => {
  const data = router._requestBody || {};
  
  // Validierung
  if (!data.product_name || !data.price) {
    return { 
      status: 'error', 
      message: 'Missing required fields: product_name, price', 
      httpStatus: 400 
    };
  }
  
  if (data.price < 0) {
    return { 
      status: 'error', 
      message: 'Price must be positive', 
      httpStatus: 400 
    };
  }
  
  // TODO: INSERT-Query mit RETURNING
  const query = `
    -- Ihre INSERT-Query hier

    RETURNING product_id, product_name, price;
  `;
  
  const result = await db.query(query);
  return { 
    status: 'success', 
    message: 'Product created', 
    data: result.rows[0],
    httpStatus: 201
  };
});

console.debug('✅ POST /products implementiert');
```
@PGlite.js(online-shop)


    {{2}}
**Test: Produkt erstellen**

    {{2}}
<div id="test-post-product"></div>

    {{2}}
<div class="form-group">
  <label>Produktname:</label>
  <input type="text" id="new-product-name" value="Webcam" />
</div>

    {{2}}
<div class="form-group">
  <label>Preis (€):</label>
  <input type="number" id="new-product-price" value="89.99" step="0.01" />
</div>

    {{2}}
<button onclick="testPostProduct()" class="btn-primary">➕ Produkt erstellen</button>

    {{2}}
<script>
window.testPostProduct = async function () {
  const name = document.getElementById('new-product-name').value;
  const price = parseFloat(document.getElementById('new-product-price').value);
  
  try {
    const response = await fetch('http://little-amazon.com/products', {
      method: 'POST',
      body: JSON.stringify({ product_name: name, price: price })
    });
    const data = await response.json();
    
    let html = '<h4>📦 POST /products Response:</h4>';
    html += `<div class="api-response">${JSON.stringify(data, null, 2)}</div>`;
    
    if (data.status === 'success') {
      html += '<p style="color: green;">✅ Produkt erfolgreich erstellt!</p>';
    }
    
    send.lia("HTML: " + html);
  } catch (error) {
    send.lia(`HTML: <p style="color: red;">❌ Error: ${error.message}</p>`);
  }
}
""
</script>

**Hinweis:** In echten Systemen würden Sie Prepared Statements nutzen, um SQL-Injection zu verhindern!

</details>

### Aufgabe 6: Produkte löschen (DELETE)

    --{{0}}--
Implementieren Sie `POST /customers` – erstellen Sie einen neuen Kunden.


**DELETE-Handler**

```javascript
// TODO: Implementieren Sie DELETE /products/:id
router.delete('/products/:id', async (params) => {
  const productId = params.id;
  
  // Prüfen ob Produkt existiert
  const checkQuery = `SELECT product_id FROM products WHERE product_id = ${productId}`;
  const checkResult = await db.query(checkQuery);
  
  if (checkResult.rows.length === 0) {
    return { status: 'error', message: 'Product not found', httpStatus: 404 };
  }
  
  try {
    const deleteProductQuery = `
      -- Ihre DELETE-Query für products hier
      
    `;
    
    await db.query(deleteProductQuery);
    
    return { 
      status: 'success', 
      message: 'Product deleted', 
      deleted_id: parseInt(productId),
      httpStatus: 200
    };
  } catch (error) {
    // Foreign Key Constraint Fehler abfangen
    if (error.message.includes('foreign key constraint')) {
      return {
        status: 'error',
        message: 'Cannot delete product: still referenced in other tables',
        detail: error.message,
        httpStatus: 409  // Conflict
      };
    }
    throw error;
  }
});

console.debug('✅ DELETE /products/:id implementiert');
```
@PGlite.js(online-shop)

    {{2}}
**Test: Mini-Shop mit Löschen-Funktion**

    {{2}}
<div id="mini-shop"></div>

    {{2}}
<button onclick="loadMiniShop()" class="btn-primary">🛒 Shop laden</button>

    {{2}}
<script>
window.loadMiniShop = async function () {
  try {
    const response = await fetch('http://little-amazon.com/products');
    const data = await response.json();
    
    let html = '<h4>🛍️ Little Amazon Shop</h4>';
    
    if (data.data && data.data.length > 0) {
      data.data.forEach(p => {
        html += `
          <div class="product-card">
            <div style="background: #e9ecef; height: 100px; display: flex; align-items: center; justify-content: center; border-radius: 4px; margin-bottom: 10px;">
              📦
            </div>
            <h4>${p.product_name}</h4>
            <p class="price">${p.price}€</p>
            <button onclick="deleteProduct(${p.product_id})">🗑️ Löschen</button>
          </div>
        `;
      });
    } else {
      html += '<p>Keine Produkte verfügbar</p>';
    }
    
    document.getElementById('mini-shop').innerHTML = html;
  } catch (error) {
    document.getElementById('mini-shop').innerHTML = 
      `<p style="color: red;">❌ Error: ${error.message}</p>`;
  }
}

window.deleteProduct = async function (id) {
  if (!confirm(`Produkt ${id} wirklich löschen?`)) return;
  
  try {
    const response = await fetch(`http://little-amazon.com/products/${id}`, {
      method: 'DELETE'
    });
    const data = await response.json();
    
    if (data.status === 'success') {
      alert('✅ Produkt gelöscht!');
      loadMiniShop(); // Neu laden
    } else {
      alert(`❌ Fehler: ${data.message}`);
    }
  } catch (error) {
    alert(`❌ Error: ${error.message}`);
  }
}

""
</script>

<details>
<summary>💡 Wichtig</summary>

**Wichtig:** Produkte können nicht gelöscht werden, solange sie in `product_categories` oder `order_items` referenziert sind. Die Lösung:
1. Zuerst alle Referenzen löschen
2. Dann das Produkt löschen
3. Oder: Tabelle mit `ON DELETE CASCADE` definieren (dann automatisch)

</details>

### Aufgabe 8: Kunde löschen (CASCADE-Problem)

    --{{0}}--
Was passiert, wenn Sie einen Kunden löschen, der Bestellungen hat? Foreign Key Constraint! Genau wie beim Produkt-Löschen.

    {{1}}
**Probieren Sie es aus:**

    {{1}}
```javascript
router(.delete('/customers/:id', async (params) => {
  const customerId = params.id;
  
  // Prüfen ob Kunde existiert
  const checkQuery = `SELECT customer_id FROM customers WHERE customer_id = ${customerId}`;
  const checkResult = await db.query(checkQuery);
  
  if (checkResult.rows.length === 0) {
    return { status: 'error', message: 'Customer not found', httpStatus: 404 };
  }
  
  try {
    const result = await db.query(`DELETE FROM customers WHERE customer_id = ${customerId}`);
    return { 
      status: 'success', 
      message: 'Customer deleted', 
      deleted_id: parseInt(customerId),
      httpStatus: 200
    };
  } catch (error) {
    // Foreign Key Constraint Fehler abfangen
    if (error.message.includes('foreign key constraint')) {
      return {
        status: 'error',
        message: 'Cannot delete customer: still referenced in other tables',
        detail: error.message,
        httpStatus: 409  // Conflict
      };
    }
    throw error;
  }
});
```
@PGlite.js(online-shop)

```javascript
// Versuchen Sie Kunde 1 zu löschen (hat Bestellungen!)
const response = await fetch('http://little-amazon.com/customers/1', {
  method: 'DELETE'
});
const data = await response.json();
console.log(data);
```
@PGlite.js(online-shop)

    --{{2}}--
Sie bekommen einen Fehler! Die Datenbank verhindert das Löschen wegen der Foreign Key Referenzen in der `orders`-Tabelle. Das ist gewollt – Datenkonsistenz!

    {{3}}
**Lösungen für Foreign Key Probleme:**

    {{3}}
1. **Reihenfolge beachten**: Erst abhängige Daten löschen, dann Hauptdaten
   ```sql
   DELETE FROM product_categories WHERE product_id = 5;
   DELETE FROM products WHERE product_id = 5;
   ```

    {{3}}
2. **Soft Delete**: Setzen Sie `deleted = true` statt echtem DELETE
   ```sql
   UPDATE products SET deleted = true WHERE product_id = 5;
   ```

    {{3}}
3. **CASCADE**: `ON DELETE CASCADE` in der Tabellendefinition
   ```sql
   CREATE TABLE product_categories (
     product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
     ...
   );
   ```

    {{3}}
4. **Transaktionen**: Mehrere Deletes atomar ausführen
   ```sql
   BEGIN;
   DELETE FROM order_items WHERE product_id = 5;
   DELETE FROM product_categories WHERE product_id = 5;
   DELETE FROM products WHERE product_id = 5;
   COMMIT;
   ```

## Teil 7: Error-Handling

    --{{0}}--
Fehler gehören zur Realität! Lassen Sie uns verschiedene Fehlertypen simulieren und richtig behandeln.

### 404: Ressource nicht gefunden

    --{{0}}--
Wenn eine Query keine Daten zurückgibt, sollten Sie 404 zurückgeben.

    {{1}}
```javascript
// Beispiel: GET /products/9999
const result = await db.query('SELECT * FROM products WHERE product_id = 9999');

if (result.rows.length === 0) {
  return { 
    status: 'error', 
    message: 'Product not found', 
    httpStatus: 404 
  };
}
```
@PGlite.js(online-shop)

### 400: Ungültige Daten

    --{{0}}--
Validieren Sie Inputs, bevor Sie SQL ausführen!

    {{1}}
```javascript
// Beispiel: Negativer Preis
if (data.price < 0) {
  return { 
    status: 'error', 
    message: 'Price must be positive', 
    httpStatus: 400 
  };
}

// Beispiel: Fehlende Pflichtfelder
if (!data.product_name || !data.price) {
  return { 
    status: 'error', 
    message: 'Missing required fields: product_name, price', 
    httpStatus: 400 
  };
}
```

### 500: SQL-Fehler

    --{{0}}--
Foreign Key Constraints, Syntax-Fehler, etc. führen zu 500-Fehlern.

    {{1}}
**Beispiel: Foreign Key Constraint**

    {{1}}
```javascript
try {
  const result = await db.query(`SELECT * FROM product_list`);
  return { status: 'success', data: result.rows };
} catch (error) {
  console.error('SQL Error:', error);
  
  // Spezifische Fehlerbehandlung
  if (error.message.includes('foreign key constraint')) {
    return { 
      status: 'error', 
      message: 'Cannot delete: record is still referenced by other tables', 
      detail: error.message,
      httpStatus: 409  // Conflict
    };
  }
  
  return { 
    status: 'error', 
    message: `Database error: ${error.message}`, 
    httpStatus: 500 
  };
}
```

    --{{2}}--
HTTP 409 (Conflict) ist der richtige Code für Foreign Key Constraint Fehler – es ist kein Server-Fehler, sondern ein Konflikt mit der Datenintegrität!

## Wrap-up & Best Practices

    --{{0}}--
Fassen wir zusammen, was Sie heute gelernt haben!

    {{1}}
**HTTP → SQL Mapping:**

    {{1}}
- ✅ **GET** → SELECT (mit WHERE für Filter, JOIN für Relations)
- ✅ **POST** → INSERT (mit RETURNING für Response)
- ✅ **DELETE** → DELETE (mit Existenz-Check)
- ✅ **PUT** → UPDATE (optional, ähnlich zu POST)

    {{2}}
**Best Practices:**

    {{2}}
- ✅ **Routing-Pattern**: Nutzen Sie Router-Syntax wie `router.get('/products/:id', handler)`
- ✅ **Parameter-Extraktion**: Zugriff über `params.id` statt manueller Regex
- ✅ **Validierung**: Prüfen Sie Inputs, bevor Sie SQL ausführen
- ✅ **Error-Handling**: Nutzen Sie passende HTTP-Status Codes
- ✅ **RETURNING**: Bei INSERT/UPDATE/DELETE die geänderten Daten zurückgeben
- ✅ **Existenz-Checks**: Vor DELETE prüfen, ob Ressource existiert
- ⚠️ **SQL-Injection**: In echten Systemen IMMER Prepared Statements nutzen!
- ⚠️ **Transaktionen**: Bei Multi-Step-Operations (z.B. Bestellung + Items)

    {{3}}
**SQL-Injection Warnung:**

    {{3}}
```javascript
// ❌ GEFÄHRLICH (heute OK, weil nur lokal im Browser):
const query = `SELECT * FROM users WHERE email = '${userInput}'`;

// ✅ SICHER (echte Systeme):
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [userInput]);
```

    --{{4}}--
In echten Backends würden Sie niemals String-Interpolation nutzen! Heute geht es aber nur um das Konzept – die Daten bleiben im Browser.

    {{5}}
> **Pro-Tipp:** Lernen Sie ein echtes Backend-Framework (Express.js, FastAPI, Spring Boot) – die Konzepte von heute sind 1:1 übertragbar!

## Referenzen & Weiterführendes

- **REST-API Design**: Roy Fielding's Dissertation (2000)
- **Fake Store API**: https://fakestoreapi.com (zum Üben)
- **MDN Web Docs**: Fetch API & HTTP-Methoden
- **OWASP**: SQL-Injection Prevention
- **HTTP-Status Codes**: RFC 7231
