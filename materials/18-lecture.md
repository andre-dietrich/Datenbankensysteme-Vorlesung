<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  1.0.0
language: de
narrator: Deutsch Female

logo:     ../assets/img/logo/18-lecture.jpg

comment:  GraphQL & SQL – Flexible Datenabfragen mit Schema, Resolver und PGlite. Hands-on Übungen mit interaktiven GraphQL-Queries im E-Commerce-Kontext.

@async.eval
<script>
setTimeout(async function() {
try {
  @input
} catch (error) {
    console.error('Error in async block:', error);
}
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

.graphql-response {
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

.query-box {
  background: #282c34;
  color: #abb2bf;
  border-radius: 4px;
  padding: 15px;
  margin: 10px 0;
  font-family: 'Courier New', monospace;
}

.result-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.highlight {
  background-color: #fff3cd;
  padding: 2px 4px;
  border-radius: 3px;
}
@end

@onload
import('https://cdn.skypack.dev/graphql')
.then((module) => {
  window.graphql = module
  console.log('✅ GraphQL library loaded')
})
.catch((error) => {
  console.error('❌ Error loading GraphQL library:', error)
})
@end

import: https://raw.githubusercontent.com/LiaTemplates/PGlite/refs/heads/main/README.md

-->

# L18: GraphQL & SQL – Flexible Datenabfragen

> **Session 18 – Lecture**
>
> **Dauer:** 90 Minuten
>
> **Lernziele:** LZ 2 (Relationale DB & SQL praktisch anwenden)
>
> **Block:** 4 – Theorie, Optimierung & Polyglot

    --{{0}}--
Willkommen zur achtzehnten Session! In der letzten Vorlesung haben Sie gelernt, wie RESTful APIs HTTP-Requests in SQL-Queries übersetzen. Heute machen wir den nächsten Schritt: GraphQL! Eine moderne Alternative zu REST, die dem Client maximale Flexibilität gibt.

    --{{1}}--
Stellen Sie sich vor: Statt mehrere REST-Endpoints anzufragen, schreiben Sie eine einzige Query, die exakt die Daten liefert, die Sie brauchen – nicht mehr, nicht weniger. Das ist GraphQL! Und das Beste: Ihre SQL-Skills sind direkt übertragbar.

## Motivation: REST vs. GraphQL

    --{{0}}--
Bevor wir in die Praxis einsteigen, schauen wir uns an, warum GraphQL entstanden ist und welche Probleme es löst.

### Das Over-fetching Problem

    --{{0}}--
Erinnern Sie sich an REST? Ein typisches Problem: Sie wollen nur den Namen und Preis eines Produkts, bekommen aber alle Felder.

    {{1}}
**REST-Request:**

    {{1}}
```http
GET /products/5
```

    {{2}}
**REST-Response (zu viel!):**

    {{2}}
```json
{
  "product_id": 5,
  "product_name": "Desk Chair",
  "price": 199.99,
  "description": "Ergonomic office chair...",
  "stock_quantity": 25,
  "supplier_id": 42,
  "created_at": "2024-01-10",
  "updated_at": "2024-02-01"
}
```

    --{{3}}--
Sie brauchen nur Name und Preis, bekommen aber 8 Felder! Das verschwendet Bandbreite und Performance.

    {{3}}
**GraphQL-Alternative:**

    {{3}}
```graphql
{
  product(id: 5) {
    name
    price
  }
}
```

    {{4}}
**GraphQL-Response (genau richtig!):**

    {{4}}
```json
{
  "data": {
    "product": {
      "name": "Desk Chair",
      "price": 199.99
    }
  }
}
```

    --{{5}}--
Sehen Sie den Unterschied? GraphQL gibt Ihnen exakt das, was Sie anfordern – nicht mehr, nicht weniger!

### Das Under-fetching Problem

    --{{0}}--
Zweites Problem bei REST: Verschachtelte Daten erfordern multiple Requests.

    {{1}}
**Szenario:** Kunde mit seinen Bestellungen abrufen

    {{2}}
**REST-Approach (3 Requests!):**

    {{2}}
```http
GET /customers/1              → Kunde
GET /customers/1/orders        → Bestellungen
GET /orders/101/items          → Bestellpositionen
```

    --{{3}}--
Drei separate Requests! Das erhöht Latenz und Komplexität im Frontend-Code.

    {{3}}
**GraphQL-Alternative (1 Request!):**

    {{3}}
```graphql
{
  customer(id: 1) {
    firstName
    lastName
    orders {
      orderDate
      totalAmount
      items {
        quantity
        product {
          name
          price
        }
      }
    }
  }
}
```

    --{{4}}--
Eine Query, alle Daten! GraphQL löst verschachtelte Daten elegant auf – genau wie SQL-Joins!

### Vergleichstabelle

    {{1}}
| Aspekt                  | REST                                 | GraphQL                                |
| ----------------------- | ------------------------------------ | -------------------------------------- |
| **Endpoints**           | Multiple (`/products`, `/customers`) | Single (`/graphql`)                    |
| **Data Fetching**       | Fixed structure                      | Flexible, client-defined               |
| **Over-fetching**       | Häufig (alle Felder)                 | Nein (nur gewünschte Felder)           |
| **Under-fetching**      | Multiple Requests nötig              | Eine Query mit Nested Fields           |
| **Versionierung**       | URL-basiert (`/v1/`, `/v2/`)         | Schema-Evolution (deprecation)         |
| **Dokumentation**       | Manuell (Swagger/OpenAPI)            | Automatisch (introspection)            |
| **SQL-Übersetzung**     | Einfach (1:1 Mapping)                | Komplex (Resolver + Query-Optimierung) |
| **Caching**             | HTTP-basiert (einfach)               | Komplex (benötigt Strategie)           |
| **Best Use Case**       | CRUD, einfache Ressourcen            | Komplexe Daten-Graphen, Mobile Apps    |

    --{{2}}--
GraphQL ist kein REST-Ersatz, sondern eine Alternative für komplexe Daten-Szenarien. Beide haben ihre Berechtigung!

## Teil 1: GraphQL-Grundlagen

    --{{0}}--
Jetzt lernen Sie die drei Kernkonzepte von GraphQL: Schema, Queries und Resolver.

### Das Schema: Type System

    --{{0}}--
GraphQL ist stark typisiert. Das Schema definiert, welche Daten verfügbar sind und welche Beziehungen existieren.

    {{1}}
**Beispiel-Schema (Online-Shop):**

    {{1}}
```graphql
type Product {
  id: Int!
  name: String!
  price: Float!
  categories: [Category]
}

type Category {
  id: Int!
  name: String!
  products: [Product]
}

type Customer {
  id: Int!
  firstName: String!
  lastName: String!
  email: String
  orders: [Order]
}

type Order {
  id: Int!
  orderDate: String
  totalAmount: Float
  items: [OrderItem]
}

type OrderItem {
  quantity: Int
  product: Product
  lineTotal: Float
}

type Query {
  products: [Product]
  product(id: Int!): Product
  customers: [Customer]
  customer(id: Int!): Customer
}
```

    --{{2}}--
Wichtige Syntax: `!` bedeutet "required" (NOT NULL in SQL), `[]` bedeutet Array/Liste. Das Schema ist wie ein ER-Diagramm – nur maschinenlesbar!

    {{3}}
**Schema = SQL-Schema Mapping:**

    {{3}}
| GraphQL Type | SQL Equivalent          |
| ------------ | ----------------------- |
| `type`       | `TABLE`                 |
| `field`      | `COLUMN`                |
| `!`          | `NOT NULL`              |
| `[Type]`     | One-to-Many Relation    |
| `Type`       | Many-to-One / Join      |

    --{{4}}--
Sehen Sie die Parallele? GraphQL-Typen entsprechen Tabellen, Fields entsprechen Spalten, und Relationen werden durch verschachtelte Typen dargestellt!

### Queries: Daten abfragen

    --{{0}}--
Queries sind wie SELECT-Statements – aber mit verschachtelter Struktur.

    {{1}}
**Beispiel 1: Alle Produkte**

    {{1}}
```graphql
{
  products {
    id
    name
    price
  }
}
```

    {{2}}
**SQL-Äquivalent:**

    {{2}}
```sql
SELECT product_id AS id, 
       product_name AS name, 
       price
FROM products;
```

    {{3}}
**Beispiel 2: Ein Produkt mit Kategorien (JOIN!)**

    {{3}}
```graphql
{
  product(id: 1) {
    name
    price
    categories {
      name
    }
  }
}
```

    {{4}}
**SQL-Äquivalent:**

    {{4}}
```sql
-- Produkt
SELECT product_name, price FROM products WHERE product_id = 1;

-- Kategorien (separate Query!)
SELECT c.category_name
FROM categories c
INNER JOIN product_categories pc ON c.category_id = pc.category_id
WHERE pc.product_id = 1;
```

    --{{5}}--
GraphQL-Queries sehen aus wie die Response-Struktur, die Sie zurückbekommen – das macht sie extrem intuitiv!

### Resolver: SQL-Übersetzung

    --{{0}}--
Resolver sind Funktionen, die GraphQL-Felder in SQL-Queries übersetzen. Das ist der Kern Ihrer Implementierung!

    {{1}}
**Resolver-Konzept:**

    {{1}}
```js
const resolvers = {
  Query: {
    products: async () => {
      // SQL-Query ausführen
      const result = await db.query('SELECT * FROM products');
      return result.rows;
    },

    product: async (parent, args) => {
      // args.id kommt aus der GraphQL-Query
      const result = await db.query(
        'SELECT * FROM products WHERE product_id = $1',
        [args.id]
      );
      return result.rows[0];
    }
  },

  Product: {
    categories: async (parent) => {
      // parent enthält das Produkt-Objekt
      const result = await db.query(`
        SELECT c.*
        FROM categories c
        INNER JOIN product_categories pc ON c.category_id = pc.category_id
        WHERE pc.product_id = $1
      `, [parent.product_id]);
      return result.rows;
    }
  }
};
```

    --{{2}}--
Verstehen Sie das Pattern? Jedes GraphQL-Feld bekommt einen Resolver, der eine SQL-Query ausführt. Verschachtelte Felder lösen weitere Queries aus!

## Datenbank-Setup: Online-Shop

    --{{0}}--
Wir nutzen das gleiche Schema wie in Lecture 17 – so können Sie REST und GraphQL direkt vergleichen!

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
INSERT INTO locations VALUES 
  (1, 'Berlin', '10115', 'Germany'), 
  (2, 'Hamburg', '20095', 'Germany'),
  (3, 'Munich', '80331', 'Germany');

INSERT INTO categories VALUES 
  (1, 'Electronics', 'Electronic devices'), 
  (2, 'Furniture', 'Office furniture'),
  (3, 'Accessories', 'Computer accessories');

INSERT INTO customers VALUES 
  (1, 'Alice', 'Smith', 'alice@example.com', 'Main St', '42', 1),
  (2, 'Bob', 'Johnson', 'bob@example.com', 'Oak Ave', '15', 2),
  (3, 'Carol', 'Williams', 'carol@example.com', 'Elm St', '7', 3);

INSERT INTO products (product_name, price) VALUES 
  ('Laptop', 999.99), 
  ('Mouse', 29.99), 
  ('Keyboard', 79.99),
  ('Monitor', 299.99), 
  ('Desk Chair', 199.99),
  ('Webcam', 89.99),
  ('Headset', 149.99);

INSERT INTO product_categories VALUES 
  (1, 1), (2, 1), (2, 3), (3, 1), (3, 3), 
  (4, 1), (5, 2), (6, 1), (6, 3), (7, 1), (7, 3);

INSERT INTO orders VALUES 
  (101, 1, '2024-01-15', 299.99, 'delivered'), 
  (102, 2, '2024-01-22', 999.99, 'delivered'),
  (103, 1, '2024-02-01', 109.98, 'shipped'),
  (104, 3, '2024-02-03', 349.98, 'processing');

INSERT INTO order_items VALUES 
  (1, 101, 4, 1, 299.99),
  (2, 102, 1, 1, 999.99),
  (3, 103, 2, 1, 29.99),
  (4, 103, 3, 1, 79.99),
  (5, 104, 5, 1, 199.99),
  (6, 104, 7, 1, 149.99);
```
@PGlite.eval(online-shop)

    --{{1}}--
Perfekt! Unsere Datenbank ist bereit. Jetzt bauen wir die GraphQL-Schicht!

## Teil 2: GraphQL-Setup mit PGlite

    --{{0}}--
Jetzt implementieren wir eine vollständige GraphQL-Schicht – direkt im Browser mit PGlite!

### Schema definieren

    --{{0}}--
Zuerst erstellen wir das GraphQL-Schema. Es beschreibt alle verfügbaren Typen und Queries.

``` graphqlschema
type Product {
  id: Int!
  name: String!
  price: Float!
  categories: [Category]
}

type Category {
  id: Int!
  name: String!
  description: String
}

type Customer {
  id: Int!
  firstName: String!
  lastName: String!
  email: String
  location: Location
  orders: [Order]
}

type Location {
  id: Int!
  city: String!
  postalCode: String!
  country: String!
}

type Order {
  id: Int!
  orderDate: String
  totalAmount: Float
  status: String
  items: [OrderItem]
}

type OrderItem {
  quantity: Int
  lineTotal: Float
  product: Product
}

type Query {
  products: [Product]
  product(id: Int!): Product
  categories: [Category]
  customers: [Customer]
  customer(id: Int!): Customer
}
```
<script>
const { buildSchema, graphql } = window.graphql;

// GraphQL Schema definieren
window.schema = buildSchema(`
@input
`);
console.log('✅ Schema created');
</script>

    --{{1}}--
Das Schema ist wie ein Vertrag: Es definiert, welche Daten der Client abfragen kann und welche Typen existieren.

### Resolver mit PGlite implementieren

    --{{0}}--
Jetzt kommt der spannende Teil: Wir verbinden GraphQL mit SQL!

```js
// Root Resolver (Top-Level Queries)
window.rootResolver = {
  // Alle Produkte
  products: async () => {
    const result = await db.query(`
      SELECT product_id AS id,
             product_name AS name,
             price
      FROM products
      ORDER BY product_name
    `);
    return result.rows;
  },

  // Ein Produkt nach ID
  product: async ({ id }) => {
    const result = await db.query(`
      SELECT product_id AS id,
             product_name AS name,
             price
      FROM products
      WHERE product_id = $1
    `, [id]);
    return result.rows[0];
  },

  // Alle Kategorien
  categories: async () => {
    const result = await db.query(`
      SELECT category_id AS id,
             category_name AS name,
             description
      FROM categories
      ORDER BY category_name
    `);
    return result.rows;
  },

  // Alle Kunden
  customers: async () => {
    const result = await db.query(`
      SELECT customer_id AS id,
             first_name AS "firstName",
             last_name AS "lastName",
             email,
             location_id AS "locationId"
      FROM customers
      ORDER BY last_name, first_name
    `);
    return result.rows;
  },

  // Ein Kunde nach ID
  customer: async ({ id }) => {
    const result = await db.query(`
      SELECT customer_id AS id,
             first_name AS "firstName",
             last_name AS "lastName",
             email,
             location_id AS "locationId"
      FROM customers
      WHERE customer_id = $1
    `, [id]);
    return result.rows[0];
  }
};

console.log('✅ Resolver created');
```
@PGlite.js(online-shop)

    --{{1}}--
Sehen Sie das Pattern? Jeder Resolver führt eine SQL-Query aus und gibt das Ergebnis zurück. GraphQL kümmert sich um den Rest!

### Erste GraphQL-Query ausführen

    --{{0}}--
Jetzt testen wir unsere Implementierung mit einer einfachen Query!

``` sql
{
  products {
    id
    name
    price
  }
}
```
<script>
setTimeout(async function() {
try {

const query = `
  @input
`;

const result = await graphql.graphql({
    schema,
  source: query,
  rootValue: rootResolver
});

console.log(JSON.stringify(result, null, 2));
} catch (error) {
    console.error('Error executing GraphQL query:', error);
}
send.lia("LIA: stop")
}, 100);

"LIA: wait"
</script>

    --{{1}}--
Fantastisch! GraphQL hat die Query ausgeführt, unseren Resolver aufgerufen, der eine SQL-Query ausgeführt hat – und das Ergebnis zurückgegeben!

## Teil 3: Nested Resolver (Joins!)

    --{{0}}--
Jetzt wird es spannend: Verschachtelte Daten! Das ist die Stärke von GraphQL.

### Lösung: Field Resolver mit parent-Objekt

    --{{0}}--
Die elegante Lösung: Field-Resolver! GraphQL übergibt automatisch das Parent-Objekt, sodass wir `parent.id` für SQL-Queries nutzen können.

```js
// Field-Resolver: GraphQL ruft sie automatisch auf!
window.nestedResolver = {
  // Query-Resolver (Top-Level) - nur eine SQL-Query!
  ...rootResolver,

  // Field-Resolver: Werden automatisch von GraphQL aufgerufen!
  Product: {
    categories: async (parent) => {
      // parent = { id: 1, name: "Laptop", price: 999.99 }
      console.log(`🔍 Loading categories for product ${parent.id} (${parent.name})...`);
      const result = await db.query(`
        SELECT c.category_id AS id,
               c.category_name AS name,
               c.description
        FROM categories c
        INNER JOIN product_categories pc ON c.category_id = pc.category_id
        WHERE pc.product_id = $1
      `, [parent.id]);
      console.log(`  ✅ Found ${result.rows.length} categories for ${parent.name}`);
      return result.rows;
    }
  },

  Customer: {
    location: async (parent) => {
      if (!parent.locationId) return null;
      
      const result = await db.query(`
        SELECT location_id AS id,
               city,
               postal_code AS "postalCode",
               country
        FROM locations
        WHERE location_id = $1
      `, [parent.locationId]);
      return result.rows[0];
    },

    orders: async (parent) => {
      console.log(`🔍 Loading orders for customer ${parent.id}...`);
      const result = await db.query(`
        SELECT order_id AS id,
               order_date AS "orderDate",
               total_amount AS "totalAmount",
               status
        FROM orders
        WHERE customer_id = $1
        ORDER BY order_date DESC
      `, [parent.id]);
      return result.rows;
    }
  },

  Order: {
    items: async (parent) => {
      console.log(`🔍 Loading items for order ${parent.id}...`);
      const result = await db.query(`
        SELECT oi.quantity,
               oi.line_total AS "lineTotal",
               oi.product_id AS "productId"
        FROM order_items oi
        WHERE oi.order_id = $1
      `, [parent.id]);
      return result.rows;
    }
  },

  OrderItem: {
    product: async (parent) => {
      const result = await db.query(`
        SELECT product_id AS id,
               product_name AS name,
               price
        FROM products
        WHERE product_id = $1
      `, [parent.productId]);
      return result.rows[0];
    }
  }
};

console.log('✅ Field-Resolver mit parent-Objekten erstellt!');
console.log('💡 GraphQL ruft Product.categories(parent) automatisch auf');
console.log('💡 Achten Sie auf die Console-Ausgaben beim Query-Test!');
```
@PGlite.js(online-shop)

    --{{1}}--
Das ist die elegante Lösung! Jeder Resolver hat nur eine SQL-Query. GraphQL ruft die Field-Resolver automatisch auf und übergibt das Parent-Objekt. So funktioniert es in Production!

### Query: Produkte mit Kategorien

    --{{0}}--
Testen wir es: Produkte mit ihren Kategorien abrufen. Achten Sie auf die Console – Sie sehen die Field-Resolver in Aktion!

```js
{
  products {
    name
    price
    categories {
      name
    }
  }
}
```
<script>
  const fieldResolver = (source, args, context, info) => {
  const typeName = info.parentType.name;     // z.B. "Product"
  const fieldName = info.fieldName;          // z.B. "categories"

  // 1) Query-Resolver aus rootValue
  if (typeName === "Query" && window.nestedResolver[fieldName]) {
    return window.nestedResolver[fieldName](args, context, info);
  }

  // 2) Type-Resolver aus nestedResolver[TypeName][fieldName]
  const typeResolvers = window.nestedResolver[typeName];
  const resolverFn = typeResolvers?.[fieldName];
  if (resolverFn) {
    return resolverFn(source, args, context, info);
  }

  // 3) Fallback: default behavior (parent[field])
  return graphql.defaultFieldResolver(source, args, context, info);
};

setTimeout(async function() {
try {
  const query = `@input`;

  const result = await graphql.graphql({
    schema,
    source: query,
    rootValue: nestedResolver,
    fieldResolver
  });

  console.log(JSON.stringify(result, null, 2));
} catch (error) {
    console.error('Error executing GraphQL query:', error);
}
send.lia("LIA: stop")
}, 100);

"LIA: wait"
</script>

    --{{1}}--
Sehen Sie das N+1-Problem? Für 7 Produkte haben wir 8 SQL-Queries ausgeführt! Jedes Produkt löst eine separate Kategorien-Query aus
Perfekt! GraphQL hat automatisch die Resolver-Kette aufgerufen: erst `products`, dann für jedes Produkt `categories`.

### Query: Kunde mit Bestellungen (Deep Nesting!)

    --{{0}}--
Jetzt testen wir eine tief verschachtelte Query – das ist die wahre Stärke von GraphQL!

``` sql
{
  customer(id: 1) {
    firstName
    lastName
    email
    location {
      city
      country
    }
    orders {
      orderDate
      totalAmount
      status
      items {
        quantity
        lineTotal
        product {
          name
          price
        }
      }
    }
  }
}
```
<script>
  const fieldResolver = (source, args, context, info) => {
  const typeName = info.parentType.name;     // z.B. "Product"
  const fieldName = info.fieldName;          // z.B. "categories"

  // 1) Query-Resolver aus rootValue
  if (typeName === "Query" && window.nestedResolver[fieldName]) {
    return window.nestedResolver[fieldName](args, context, info);
  }

  // 2) Type-Resolver aus nestedResolver[TypeName][fieldName]
  const typeResolvers = window.nestedResolver[typeName];
  const resolverFn = typeResolvers?.[fieldName];
  if (resolverFn) {
    return resolverFn(source, args, context, info);
  }

  // 3) Fallback: default behavior (parent[field])
  return graphql.defaultFieldResolver(source, args, context, info);
};

setTimeout(async function() {
try {
  const query = `@input`;

  const result = await graphql.graphql({
    schema,
    source: query,
    rootValue: nestedResolver,
    fieldResolver
  });

  console.log(JSON.stringify(result, null, 2));
} catch (error) {
    console.error('Error executing GraphQL query:', error);
}
send.lia("LIA: stop")
}, 100);

"LIA: wait"
</script>

    --{{1}}--
Beeindruckend! Eine Query, fünf Ebenen tief – aber achten Sie auf die Anzahl der SQL-Queries. Jede Verschachtelungsebene löst weitere Queries aus. Das ist das N+1-Problem in Aktion
    --{{1}}--
Beeindruckend! Eine Query, fünf Ebenen tief – und GraphQL hat automatisch alle SQL-Queries koordiniert!

## Teil 4: Interaktive Übungen

    --{{0}}--
Jetzt sind Sie dran! Erweitern Sie die GraphQL-API mit eigenen Queries.

### Aufgabe 1: Query erstellen ⭐

    --{{0}}--
Schreiben Sie eine GraphQL-Query, die alle Kategorien mit den zugehörigen Produkten abruft.

    {{1}}
**Hinweis:** Sie benötigen einen neuen Field Resolver `Category.products`.

    {{2}}
<details>
<summary>💡 Lösung anzeigen</summary>

```js
// 1. Resolver erweitern
rootWithNested.Category = {
  products: async (category) => {
    const result = await db.query(`
      SELECT p.product_id AS id,
             p.product_name AS name,
             p.price
      FROM products p
      INNER JOIN product_categories pc ON p.product_id = pc.product_id
      WHERE pc.category_id = $1
      ORDER BY p.product_name
    `, [category.id]);
    return result.rows;
  }
};

// 2. Query ausführen
const query = `
  {
    categories {
      name
      products {
        name
        price
      }
    }
  }
`;

const result = await graphql({
  schema,
  source: query,
  rootValue: rootWithNested
});

console.log('📂 Categories with products:');
result.data.categories.forEach(cat => {
  console.log(`\n${cat.name}:`);
  cat.products.forEach(p => console.log(`  • ${p.name} (${p.price}€)`));
});
```

</details>

    {{3}}
**Playground:**

```js
// Ihr Code hier!


```
@PGlite.js(online-shop)

### Aufgabe 2: Filtering & Pagination ⭐⭐

    --{{0}}--
Erweitern Sie das Schema, um gefilterte Produkte abzurufen (z.B. nur Produkte unter 100€).

    {{1}}
**Hinweis:** Fügen Sie dem Schema neue Query-Parameter hinzu:

    {{1}}
```graphql
type Query {
  products(maxPrice: Float): [Product]
}
```

    {{2}}
<details>
<summary>💡 Lösung anzeigen</summary>

```js
// 1. Schema mit Parametern erweitern
const schemaWithFilter = buildSchema(`
  type Product {
    id: Int!
    name: String!
    price: Float!
    categories: [Category]
  }

  type Category {
    id: Int!
    name: String!
    description: String
    products: [Product]
  }

  type Query {
    products(maxPrice: Float, category: String): [Product]
    product(id: Int!): Product
    categories: [Category]
  }
`);

// 2. Resolver anpassen
const rootFiltered = {
  products: async ({ maxPrice, category }) => {
    let query = `
      SELECT DISTINCT p.product_id AS id,
             p.product_name AS name,
             p.price
      FROM products p
    `;
    
    const conditions = [];
    const params = [];
    
    if (category) {
      query += `
        INNER JOIN product_categories pc ON p.product_id = pc.product_id
        INNER JOIN categories c ON pc.category_id = c.category_id
      `;
      conditions.push(`c.category_name = $${params.length + 1}`);
      params.push(category);
    }
    
    if (maxPrice) {
      conditions.push(`p.price <= $${params.length + 1}`);
      params.push(maxPrice);
    }
    
    if (conditions.length > 0) {
      query += ` WHERE ` + conditions.join(' AND ');
    }
    
    query += ` ORDER BY p.product_name`;
    
    const result = await db.query(query, params);
    return result.rows;
  },
  
  // Andere Resolver von oben...
  product: rootWithNested.product,
  categories: rootWithNested.categories,
  
  Product: rootWithNested.Product,
  Category: rootWithNested.Category
};

// 3. Testen
const query = `
  {
    affordable: products(maxPrice: 100) {
      name
      price
    }
    electronics: products(category: "Electronics") {
      name
      price
    }
  }
`;

const result = await graphql({
  schema: schemaWithFilter,
  source: query,
  rootValue: rootFiltered
});

console.log('💰 Affordable products (< 100€):');
result.data.affordable.forEach(p => console.log(`  ${p.name}: ${p.price}€`));

console.log('\n💻 Electronics:');
result.data.electronics.forEach(p => console.log(`  ${p.name}: ${p.price}€`));
```

</details>

    {{3}}
**Playground:**

```js
// Ihr Code hier!


```
@PGlite.js(online-shop)

### Aufgabe 3: Mutations (CREATE) ⭐⭐⭐

    --{{0}}--
Bisher haben wir nur Queries (READ) implementiert. Jetzt fügen Sie eine Mutation hinzu, um Produkte zu erstellen!

    {{1}}
**Hinweis:** Mutations sind wie POST-Requests in REST.

    {{1}}
```graphql
type Mutation {
  createProduct(name: String!, price: Float!): Product
}
```

    {{2}}
<details>
<summary>💡 Lösung anzeigen</summary>

```js
// 1. Schema mit Mutation erweitern
const schemaWithMutation = buildSchema(`
  type Product {
    id: Int!
    name: String!
    price: Float!
  }

  type Query {
    products: [Product]
    product(id: Int!): Product
  }

  type Mutation {
    createProduct(name: String!, price: Float!): Product
    deleteProduct(id: Int!): Boolean
  }
`);

// 2. Mutation Resolver implementieren
const rootWithMutation = {
  // Query Resolver
  products: async () => {
    const result = await db.query(`
      SELECT product_id AS id, product_name AS name, price
      FROM products
      ORDER BY product_name
    `);
    return result.rows;
  },
  
  product: async ({ id }) => {
    const result = await db.query(`
      SELECT product_id AS id, product_name AS name, price
      FROM products
      WHERE product_id = $1
    `, [id]);
    return result.rows[0];
  },

  // Mutation Resolver
  createProduct: async ({ name, price }) => {
    const result = await db.query(`
      INSERT INTO products (product_name, price)
      VALUES ($1, $2)
      RETURNING product_id AS id, product_name AS name, price
    `, [name, price]);
    
    console.log(`✅ Created product: ${name}`);
    return result.rows[0];
  },

  deleteProduct: async ({ id }) => {
    await db.query(`
      DELETE FROM products WHERE product_id = $1
    `, [id]);
    
    console.log(`🗑️ Deleted product ID ${id}`);
    return true;
  }
};

// 3. Mutation ausführen
const mutation = `
  mutation {
    newProduct: createProduct(name: "External SSD", price: 129.99) {
      id
      name
      price
    }
  }
`;

const result = await graphql({
  schema: schemaWithMutation,
  source: mutation,
  rootValue: rootWithMutation
});

console.log('🎉 New product created:', result.data.newProduct);

// 4. Überprüfen
const checkQuery = `{ products { name price } }`;
const checkResult = await graphql({
  schema: schemaWithMutation,
  source: checkQuery,
  rootValue: rootWithMutation
});

console.log(`\n📦 Total products: ${checkResult.data.products.length}`);
```

</details>

    {{3}}
**Playground:**

```js
// Ihr Code hier!


```
<script>@async.eval</script>

## Teil 5: Best Practices & Optimierung

    --{{0}}--
GraphQL ist mächtig – aber mit großer Macht kommt große Verantwortung! Hier lernen Sie, wie Sie Performance-Probleme vermeiden.

Unsere einfache Implementierung zeigt das N+1-Problem deutlich: Verschachtelte Daten lösen kaskadierend Queries aus.

    {{1}}
**Beispiel: 3 Kunden mit je 2 Bestellungen**

    {{1}}
```
Query: customers { orders { ... } }

Queries ausgeführt:
1. SELECT * FROM customers                    (3 Kunden)
2. SELECT * FROM orders WHERE customer_id = 1 (Kunde 1)
3. SELECT * FROM orders WHERE customer_id = 2 (Kunde 2)
4. SELECT * FROM orders WHERE customer_id = 3 (Kunde 3)

Total: 4 Queries (1 + N)
```

    {{2}}
**Lösung: DataLoader Pattern (Production)**

    --{{2}}--
Professionelle GraphQL-Server nutzen "DataLoader" – ein Pattern, das Queries bündelt:

    {{2}}
```js
// Pseudo-Code: DataLoader sammelt IDs und bündelt Queries
const orderLoader = new DataLoader(async (customerIds) => {
  const result = await db.query(`
    SELECT * FROM orders 
    WHERE customer_id = ANY($1)
  `, [customerIds]);
  
  // Gruppieren nach customer_id
  return groupBy(result.rows, 'customer_id');
});

// Field Resolver in Production (Apollo Server)
Customer: {
  orders: (parent) => orderLoader.load(parent.id)
  // GraphQL sammelt alle parent.id Werte → 1× gebündelte Query!
}
```

    --{{3}}--
Mit DataLoader: Nur 2 Queries für 3 Kunden! Das ist die Production-Lösung. Für unsere Übung reicht das Verständnis des Problems

    --{{3}}--
Das ist fortgeschritten! Für Produktionssysteme sollten Sie Libraries wie `dataloader` nutzen.

### Problem 2: Query Depth Limiting

    --{{0}}--
Clients könnten böswillige Queries schicken:

    {{1}}
```graphql
{
  customer {
    orders {
      items {
        product {
          categories {
            products {
              categories {
                products {
                  # ... 100 Ebenen tief!
                }
              }
            }
          }
        }
      }
    }
  }
}
```

    --{{2}}--
Das würde tausende SQL-Queries auslösen! Lösung: Max-Depth Validation.

    {{2}}
```js
// Depth Limiting (vereinfacht)
const maxDepth = 5;

function validateQueryDepth(query) {
  const depth = calculateDepth(query);
  if (depth > maxDepth) {
    throw new Error(`Query too deep! Max: ${maxDepth}`);
  }
}
```

### Problem 3: Caching

    --{{0}}--
REST hat einfaches HTTP-Caching. GraphQL ist komplexer:

    {{1}}
```graphql
# Zwei unterschiedliche Queries, beide wollen Produkt 1
{
  product(id: 1) { name price }
}

{
  product(id: 1) { name price categories { name } }
}
```

    --{{2}}--
Beide Queries treffen den gleichen `/graphql` Endpoint – HTTP-Caching funktioniert nicht! Lösung: Normalisierter Cache (Apollo Client, urql).

### Best Practices (Zusammenfassung)

    {{1}}
| Problem                 | Lösung                            |
| ----------------------- | --------------------------------- |
| **N+1 Queries**         | DataLoader Pattern                |
| **Unbounded Queries**   | Query Depth & Complexity Limiting |
| **Caching**             | Normalized Cache (Client-side)    |
| **Overfetching**        | Schema-Design: Granulare Types    |
| **Error Handling**      | Structured Errors in Response     |
| **Security**            | Query Cost Analysis, Rate Limiting|

## Zusammenfassung & Vergleich

    --{{0}}--
Was haben Sie heute gelernt? GraphQL als moderne Alternative zu REST – mit direktem SQL-Bezug!

### REST vs. GraphQL – Recap

    {{1}}
| Aspekt                  | REST                                    | GraphQL                                        |
| ----------------------- | --------------------------------------- | ---------------------------------------------- |
| **Endpunkte**           | Multiple (`/products`, `/customers`)    | Single (`/graphql`)                            |
| **Datenstruktur**       | Server-defined (fixed)                  | Client-defined (flexible)                      |
| **Over-fetching**       | Ja (alle Felder immer)                  | Nein (nur gewünschte Felder)                   |
| **Under-fetching**      | Multiple Requests                       | Eine Query mit Nesting                         |
| **SQL-Übersetzung**     | Einfach (URL → WHERE)                   | Komplex (Resolver-Kette)                       |
| **Performanz-Risiken**  | Wenige                                  | N+1 Problem, unbounded queries                 |
| **Lernkurve**           | Einfach                                 | Mittel-Hoch                                    |
| **Best Use Case**       | CRUD, einfache APIs                     | Komplexe Daten-Graphen, Mobile Apps            |

### GraphQL ↔ SQL Mapping (Kern-Takeaways)

    {{1}}
```
GraphQL Type       →  SQL Table
GraphQL Field      →  SQL Column
GraphQL Relation   →  SQL Foreign Key + JOIN
GraphQL Query      →  SELECT (mit dynamischen WHERE/JOIN)
GraphQL Mutation   →  INSERT / UPDATE / DELETE
Resolver Function  →  SQL Query Executor
```

### Wann GraphQL, wann REST?

    {{1}}
**Nutzen Sie REST, wenn:**

    {{1}}
- Einfache CRUD-Operationen
- HTTP-Caching wichtig ist
- Backend-Kontrolle über Datenstruktur gewünscht
- Team mit REST-Expertise

    {{2}}
**Nutzen Sie GraphQL, wenn:**

    {{2}}
- Komplexe, verschachtelte Daten
- Mobile Apps (Bandbreiten-Optimierung)
- Verschiedene Clients mit unterschiedlichen Anforderungen
- Stark typgef Schnittstelle gewünscht
- Rapid Prototyping (selbst-dokumentierendes Schema)

## Ausblick: GraphQL in der Praxis

    --{{0}}--
Heute haben Sie GraphQL im Browser implementiert – aber wie sieht es in echten Systemen aus?

### Production-Grade GraphQL

    {{1}}
**Typische Architektur:**

    {{1}}
```ascii
┌────────────┐
│   Client   │ (Apollo Client, urql)
└─────┬──────┘
      │ GraphQL Query
      │
┌─────▼────────┐
│ GraphQL      │ (Apollo Server, Yoga)
│ Server       │
└─────┬────────┘
      │
      ├──→ DataLoader (Batch & Cache)
      │
      ├──→ Resolver (mit Authorization)
      │
┌─────▼────────┐
│  PostgreSQL  │
│  Database    │
└──────────────┘
```

### Beliebte GraphQL-Frameworks

    {{1}}
| Framework        | Sprache    | Besonderheit                     |
| ---------------- | ---------- | -------------------------------- |
| **Apollo Server**| JavaScript | Most popular, viele Features     |
| **GraphQL Yoga** | JavaScript | Modern, lightweight              |
| **Hasura**       | Haskell    | Auto-generates GraphQL from DB   |
| **Postgraphile** | JavaScript | PostgreSQL → GraphQL (auto)      |
| **graphene**     | Python     | Django/Flask Integration         |

    --{{2}}--
Besonders spannend: Hasura und Postgraphile generieren GraphQL-APIs **automatisch** aus Ihrem Datenbankschema – ohne manuellen Resolver-Code!

### Nächste Schritte

    {{1}}
Wenn Sie GraphQL vertiefen möchten:

    {{1}}
1. **Subscriptions** (Real-time Updates via WebSocket)
2. **Fragments** (Wiederverwendbare Query-Teile)
3. **Interfaces & Unions** (Polymorphe Typen)
4. **Schema Stitching** (Multiple GraphQL-APIs kombinieren)
5. **Federation** (Microservices mit GraphQL)

## Aufgabe für zu Hause 🏠

    --{{0}}--
Vertiefen Sie Ihr Wissen mit dieser Hausaufgabe!

**Aufgabenstellung:**

1. Erweitern Sie das Schema um einen neuen Typ `Review`:

```graphql
type Review {
  id: Int!
  rating: Int!          # 1-5 Sterne
  comment: String
  createdAt: String
  product: Product
  customer: Customer
}
```

2. Erstellen Sie die entsprechende SQL-Tabelle mit Constraints
3. Implementieren Sie Resolver für:
   - `product.reviews` (alle Reviews eines Produkts)
   - `customer.reviews` (alle Reviews eines Kunden)
   - Mutation `createReview(productId: Int!, customerId: Int!, rating: Int!, comment: String): Review`

4. Schreiben Sie eine Query, die:
   - Alle Produkte abruft
   - Mit durchschnittlicher Bewertung (Aggregation!)
   - Und den Top-3 Reviews

**Bonus:** Implementieren Sie Paginierung (`limit` und `offset` Parameter).

---

    --{{1}}--
Das war's für heute! Sie haben gelernt, wie GraphQL funktioniert, wie Sie Resolver mit SQL verknüpfen, und welche Trade-offs es gegenüber REST gibt. GraphQL ist ein mächtiges Werkzeug – nutzen Sie es weise!

    {{2}}
**Nächste Session:** Wir schauen uns Time-Series Datenbanken an – spezialisierte Systeme für zeitbasierte Daten wie IoT-Sensoren und Logs.

    {{2}}
Viel Erfolg! 🚀