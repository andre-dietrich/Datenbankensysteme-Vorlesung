<!--
language: de
narrator: German Male

logo:     ../assets/img/logo/3-lecture.jpg

import:   https://raw.githubusercontent.com/LiaTemplates/PouchDB/main/README.md
-->


# Document Stores: JSON Persistenz, Queries & Offline-Sync

    --{{0}}--
Willkommen zur dritten Session! Nachdem wir in Session 1 die Grenzen von Flat Files erlebt und in Session 2 Key-Value Stores als erste Lösung kennengelernt haben, machen wir heute den nächsten evolutionären Schritt: Document Stores. JSON wird nicht mehr nur als Datenformat verwendet, sondern als natives Datenmodell persistiert – mit all seinen verschachtelten Strukturen, Arrays und flexiblen Schemas.

    {{0-1}}
<section>

**Rückblick Sessions 1–2:**

> - **Session 1:** CSV/JSON als Flat Files – flexibel, aber ohne Abfragemechanismen
> - **Session 2:** Key-Value Stores – O(1) Zugriff per Schlüssel, aber keine strukturierten Queries

**Die zentrale Frage heute:**

> Wie speichern und durchsuchen wir **strukturierte, verschachtelte Daten** effizient?

</section>

    --{{1}}--
Document Stores sind die natürliche Evolution von Key-Value Systemen: Statt opake Werte zu speichern, versteht die Datenbank die Struktur der Dokumente. JSON-Objekte werden nicht mehr als Strings abgelegt, sondern als First-Class Citizens behandelt. Das ermöglicht Queries auf verschachtelte Felder, Indexierung von Objekt-Properties und flexible Schema-Evolution – ohne die Flexibilität von NoSQL aufzugeben.

    {{1}}
<section>

## 🎯 Lernziele dieser Session

Nach dieser Session können Sie:

1. **Document Store Konzepte** erklären und von Key-Value Stores abgrenzen
2. **PouchDB im Browser** nutzen für lokale Datenpersistenz
3. **Mango-Queries** schreiben (Selektoren, logische Operatoren, verschachtelte Felder)
4. **Index-Strategien** anwenden für Performance-Optimierung
5. **Offline-First Synchronisation** verstehen und Konflikte auflösen
6. **Use Cases** bewerten: Wann Document Store, wann Alternative?

</section>

---

## Block 1: Document Store Grundlagen

    --{{0}}--
Starten wir mit den Basics: Was macht einen Document Store aus? Der Kernunterschied zu Key-Value Stores liegt nicht nur darin, dass wir JSON speichern – das könnten wir auch in Redis. Der Unterschied ist, dass die Datenbank die JSON-Struktur versteht und darauf operieren kann.

### Was ist ein Document Store?

    {{0-1}}
<section>

**Definition:**

> Ein **Document Store** ist eine NoSQL-Datenbank, die semi-strukturierte Dokumente (meist JSON/BSON) als atomare Einheiten speichert und durchsuchbar macht.

**Kernmerkmale:**

- **Dokument = Atomare Einheit**: Ein JSON-Objekt ist die kleinste Speichereinheit
- **Schema-optional**: Dokumente können unterschiedliche Felder haben
- **Verschachtelung nativ**: Arrays und Objekte sind First-Class Citizens
- **Sekundäre Indizes**: Abfragen auf beliebige Felder, nicht nur den Key

</section>

    --{{1}}--
Der entscheidende Unterschied: In einem Key-Value Store ist `{"name": "Alice", "age": 30}` nur ein String. In einem Document Store versteht das System, dass dort ein Objekt mit Feldern `name` und `age` liegt – und Sie können direkt danach suchen.

    {{1-2}}
<section>

### Document Store vs. Key-Value Store

| Aspekt                 | Key-Value Store       | Document Store            |
| ---------------------- | --------------------- | ------------------------- |
| **Wert-Typ**           | Opak (String, Binary) | Strukturiert (JSON/BSON)  |
| **Abfragen**           | Nur per Key           | Per Key **und** Felder    |
| **Indizes**            | Primärschlüssel       | Primär + Sekundär         |
| **Schema**             | Keine Validierung     | Optional validierbar      |
| **Typisches Beispiel** | Redis, Memcached      | MongoDB, CouchDB, PouchDB |

**Analogie:**

- **KV:** Schließfach – Sie brauchen den Schlüssel, Inhalt ist egal
- **Document:** Bibliothekskatalog – Suche nach Autor, Titel, Jahr, ...

</section>

    --{{2}}--
Diese Flexibilität hat ihren Preis: Document Stores sind komplexer und oft langsamer als reine Key-Value Stores. Aber sie lösen ein fundamentales Problem: Wie finde ich alle Nutzer über 18? Wie finde ich alle Produkte in Kategorie "Electronics"? In KV müssten Sie alle Keys kennen oder alle Werte laden und filtern. In Document Stores nutzen Sie Queries.

### PouchDB: Document Store im Browser

    {{2-3}}
<section>

**Warum PouchDB für diese Vorlesung?**

- ✅ Läuft nativ im Browser (keine Server-Installation)
- ✅ CouchDB-kompatibel (Sync zu Remote-DB möglich)
- ✅ Offline-First Design (perfekt für moderne Web-Apps)
- ✅ Mango-Query-Language (MongoDB-ähnlich)
- ✅ IndexedDB als Storage-Backend

**Setup (HTML):**

``` js
// Datenbank erstellen
const db = new PouchDB('my_database', {adapter: 'memory'});

// Dokument einfügen
await db.put({
  _id: 'user_alice',
  name: 'Alice',
  age: 30,
  email: 'alice@example.com'
});

await db.destroy(); // Datenbank löschen (optional)
```
@PouchDB.terminal

</section>

    --{{3}}--
PouchDB speichert Daten in IndexedDB – einer Browser-nativen Key-Value API. Aber PouchDB abstrahiert die Komplexität und bietet ein Document-Modell. Jedes Dokument braucht eine `_id` (ähnlich wie ein Key), kann aber beliebige weitere Felder haben. Das Präfix-Underscore (`_id`, `_rev`) markiert System-Felder.

    {{3}}
<section>

### Live-Demo: Erste Schritte mit PouchDB

**Öffnen Sie die Browser DevTools Console und führen Sie aus:**

```javascript
// Datenbank erstellen
const db = new PouchDB('lecture_demo');

// Dokument einfügen
await db.put({
  _id: 'product_001',
  name: 'Laptop',
  price: 999,
  category: 'Electronics',
  tags: ['computer', 'portable']
});

// Dokument abrufen
const doc = await db.get('product_001');
console.log(doc);

// Alle Dokumente auflisten
const result = await db.allDocs({ include_docs: true });
console.log(result.rows);
```

**Was Sie beobachten sollten:**

- Jedes Dokument hat automatisch `_id` und `_rev` (Revision für Versionierung)
- Verschachtelte Strukturen (Arrays) werden direkt gespeichert
- `allDocs()` gibt Metadaten + Dokumente zurück

</section>

---

## Block 2: Von Scans zu strukturierten Queries

    --{{0}}--
Bevor wir in die Details von Mango-Queries einsteigen, sollten wir einen Moment innehalten und uns fragen: Was haben wir eigentlich gewonnen gegenüber CSV-Dateien und Key-Value Stores? In Session 1 konnten wir CSV-Dateien abfragen – aber nur durch vollständiges Durchscannen. In Session 2 lernten wir Key-Value Stores kennen – brillant für direkte Lookups, aber hilflos bei komplexen Filtern. Document Stores sind der nächste evolutionäre Schritt: Sie verstehen die Struktur Ihrer Daten und ermöglichen strukturierte Abfragen. Aber ohne Indizes zahlen wir dafür einen hohen Preis.

### Wiederholung: Das Scan-Problem

    {{0-1}}
<section>

**Rückblick Session 1 (CSV):**

```javascript
// CSV: Alle Produkte mit stock < 10 finden
const rows = Papa.parse(csvText, { header: true }).data;
const results = [];

for (let i = 0; i < rows.length; i++) {
  if (parseInt(rows[i].stock) < 10) {  // Manueller Filter
    results.push(rows[i]);
  }
}
// Zeitkomplexität: O(n) – JEDE Zeile wird geprüft
```

**Rückblick Session 2 (Key-Value):**

```javascript
// Key-Value Store: Direkter Zugriff O(1)
const product = await redis.get('product_001');  // ✅ Schnell!

// Aber: Filter über Werte? Zurück zu O(n)!
const allKeys = await redis.keys('product_*');
const results = [];
for (const key of allKeys) {
  const product = JSON.parse(await redis.get(key));
  if (product.stock < 10) {  // JEDES Dokument laden & prüfen!
    results.push(product);
  }
}
// Problem: Keine strukturierten Queries möglich
```

> **Das fundamentale Problem:** Ohne Kenntnis der Datenstruktur kann das System nicht effizient filtern.

</section>

    --{{1}}--
Dieses Problem zieht sich durch alle bisherigen Ansätze: CSV kennt keine Struktur – nur Text. Key-Value Stores kennen nur Schlüssel – der Wert ist eine opake Blackbox. Beide zwingen uns zu Full-Table-Scans für jede Filteroperation. Bei 1.000 Datensätzen ist das tolerierbar. Bei 100.000 wird es schmerzhaft. Bei 10 Millionen unmöglich.

### Document Stores: Struktur wird zum Vorteil

    {{1-2}}
<section>

**Der Durchbruch:**

```ascii
CSV / Key-Value Store:         Document Store:
┌─────────────────────┐        ┌─────────────────────┐
│ Daten = Opak        │        │ Daten = Strukturiert│
│                     │        │                     │
│ "P001,Laptop,999"   │        │ {                   │
│                     │   →    │   _id: "P001",      │
│ System versteht:    │        │   name: "Laptop",   │
│ ❌ Keine Felder     │        │   price: 999        │
│ ❌ Keine Typen      │        │ }                   │
│ ❌ Keine Queries    │        │                     │
│                     │        │ System versteht:    │
│ → Nur Scan möglich  │        │ ✅ Felder (price)   │
│                     │        │ ✅ Typen (Number)   │
│                     │        │ ✅ Queries möglich! │
└─────────────────────┘        └─────────────────────┘
```

**PouchDB kann jetzt:**

```javascript
// Query auf Feldebene – keine manuelle Iteration nötig!
const result = await db.find({
  selector: {
    stock: { $lt: 10 }  // PouchDB versteht "stock" als Feld
  }
});

console.log(result.docs);  // Nur passende Dokumente
```

> **Wichtig:** Das funktioniert – aber **erstmal immer noch als Scan**! Der Unterschied: Das System übernimmt den Scan für Sie. Wirkliche Performance kommt erst mit Indizes.

</section>

    --{{2}}--
Hier ist der entscheidende Punkt: Document Stores machen Queries bequemer und deklarativer – aber ohne Indizes sind sie nicht magisch schneller als Ihre CSV-Schleife. Der wahre Durchbruch kommt im nächsten Schritt: Wenn das System die Struktur kennt, kann es Indizes darauf bauen.

### Das Index-Konzept: Von O(n) zu O(log n)

    {{2-3}}
<section>

**Problem ohne Index:**

```javascript
// PouchDB OHNE Index
await db.find({
  selector: { category: 'Electronics' }
});

// Interner Ablauf:
// 1. Lade ALLE Dokumente aus IndexedDB
// 2. Für jedes Dokument:
//    - Parse JSON
//    - Prüfe: doc.category === 'Electronics'
// 3. Sammle Treffer
// Komplexität: O(n)
// Bei 10.000 Docs: ~10.000 Operationen
```

**Lösung mit Index:**

```javascript
// Index erstellen (einmalig)
await db.createIndex({
  index: { fields: ['category'] }
});

// Gleiche Query – jetzt mit Index
await db.find({
  selector: { category: 'Electronics' }
});

// Interner Ablauf:
// 1. Lookup in Index: category='Electronics' → [Doc-IDs]
// 2. Lade nur diese Dokumente
// Komplexität: O(log n) + O(k)  // k = Anzahl Treffer
// Bei 10.000 Docs, 100 Treffer: ~14 + 100 Operationen
```

**Visualisierung:**

```ascii
Ohne Index (Full Scan):
┌────┬────┬────┬────┬────┬────┬────┬────┐
│Doc1│Doc2│Doc3│Doc4│Doc5│...│Doc │Doc │
│    │    │    │    │    │   │9999│10k │
└────┴────┴────┴────┴────┴────┴────┴────┘
  ↓    ↓    ↓    ↓    ↓         ↓    ↓
Prüfe jeden einzelnen (10.000 Checks)

Mit Index (B-Tree Lookup):
         Index: category
              ┌─────┐
              │Root │
              └──┬──┘
        ┌───────┴───────┐
     ┌──┴──┐         ┌──┴──┐
     │Books│         │Elec.│ ← Ziel gefunden!
     └─────┘         └──┬──┘
                  ┌─────┴─────┐
            [Doc42, Doc123, Doc789]
                  ↓
Lade nur diese 3 Dokumente (3 Loads statt 10.000!)
```

</section>

    --{{3}}--
Das ist das Kernprinzip von Indizes: Statt alle Dokumente zu durchsuchen, bauen wir eine separate Datenstruktur – meist einen B-Tree –, die von Feldwerten zu Dokument-IDs verweist. Das kostet Speicherplatz und macht Writes langsamer, aber beschleunigt Reads dramatisch. Dieser Trade-off ist fundamental für alle Datenbanksysteme.

### Live-Demo: Mit und ohne Index

    {{3-4}}
<section>

**Führen Sie dieses Experiment in der Browser Console aus:**

```javascript
// Setup: 1000 Produkte generieren
const db = new PouchDB('performance_test');

const products = [];
for (let i = 0; i < 1000; i++) {
  products.push({
    _id: `product_${String(i).padStart(4, '0')}`,
    name: `Product ${i}`,
    category: ['Electronics', 'Books', 'Clothing'][i % 3],
    price: Math.floor(Math.random() * 500) + 10,
    stock: Math.floor(Math.random() * 100)
  });
}

await db.bulkDocs(products);
console.log('✅ 1000 Produkte eingefügt');

// Test 1: Query OHNE Index
console.time('⏱️  Ohne Index');
const result1 = await db.find({
  selector: { 
    category: 'Electronics',
    stock: { $lt: 10 }
  }
});
console.timeEnd('⏱️  Ohne Index');
console.log(`   Gefunden: ${result1.docs.length} Produkte`);

// Index erstellen
await db.createIndex({
  index: { fields: ['category', 'stock'] }
});
console.log('✅ Index auf [category, stock] erstellt');

// Test 2: Query MIT Index
console.time('⏱️  Mit Index');
const result2 = await db.find({
  selector: { 
    category: 'Electronics',
    stock: { $lt: 10 }
  }
});
console.timeEnd('⏱️  Mit Index');
console.log(`   Gefunden: ${result2.docs.length} Produkte`);

// Cleanup
await db.destroy();
```

**Erwartetes Ergebnis:**

```
✅ 1000 Produkte eingefügt
⏱️  Ohne Index: ~80-150ms
   Gefunden: ~11 Produkte
✅ Index auf [category, stock] erstellt
⏱️  Mit Index: ~10-25ms
   Gefunden: ~11 Produkte
```

**Beobachtung:**

- Speedup: **~5-10x** bei nur 1.000 Dokumenten
- Bei 10.000 Docs: Speedup **~50-100x**
- Bei 100.000 Docs: Speedup **~500-1000x**

> **Die Moral:** Indizes sind nicht optional für Production-Datenbanken – sie sind essentiell!

</section>

    --{{4}}--
Diese Live-Demo sollte den Unterschied greifbar machen. Bei kleinen Datenmengen wirken Indizes wie Overhead – aber sie skalieren logarithmisch, während Scans linear wachsen. Das ist der Unterschied zwischen einer App, die bei 10.000 Nutzern zusammenbricht, und einer, die auf 10 Millionen skaliert.

### Sekundärindizes: Das neue Werkzeug

    {{4}}
<section>

**Was sind Sekundärindizes?**

```ascii
Primärschlüssel (_id):        Sekundärindex (category):
────────────────────          ────────────────────────
_id → Dokument                Feldwert → [_ids]

"product_001" → {             "Electronics" → [
  name: "Laptop",               "product_001",
  category: "Electronics"       "product_003",
}                               "product_042"
                              ]

"product_002" → {             "Books" → [
  name: "Novel",                "product_002",
  category: "Books"             "product_017"
}                             ]
```

**Arten von Indizes:**

| Index-Typ | Beschreibung | Beispiel |
|-----------|--------------|----------|
| **Single-Field** | Index auf einem Feld | `['category']` |
| **Composite** | Index auf mehreren Feldern | `['category', 'price']` |
| **Sparse** | Nur Dokumente mit dem Feld | Automatisch in PouchDB |
| **Unique** | Werte müssen eindeutig sein | Nicht nativ in PouchDB |

**Wichtig:**

- ✅ Jedes Feld kann indexiert werden (außer Arrays, Nested Objects haben Einschränkungen)
- ✅ Mehrere Indizes pro Datenbank möglich
- ⚠️ Jeder Index kostet Speicher + verlangsamt Writes
- ⚠️ Zu viele Indizes = Performance-Regression!

**Faustregel:**

> Indexiere Felder, die in `selector` und `sort` häufig auftauchen – aber nicht alle!

</section>

---

## Block 3: Mango Query Language im Detail

    --{{0}}--
Jetzt, da Sie verstehen, warum Document Stores strukturierte Queries ermöglichen und warum Indizes essentiell sind, schauen wir uns die Mango Query Language im Detail an. Mango ist JSON-basiert, deklarativ und MongoDB-Nutzern vertraut. Sie beschreiben, WAS Sie suchen – nicht WIE.

### Mango Query Language: Grundlagen

    {{0-1}}
<section>

**Konzept:**

> Mango-Queries sind JSON-Objekte, die Filterkriterien beschreiben. PouchDB durchsucht Dokumente und gibt nur passende zurück.

**Basis-Syntax:**

```javascript
await db.find({
  selector: {
    field: value  // Einfache Gleichheit
  }
});
```

**Beispiel:**

```javascript
// Finde alle Produkte in Kategorie "Electronics"
const result = await db.find({
  selector: {
    category: 'Electronics'
  }
});

console.log(result.docs);  // Array von passenden Dokumenten
```

</section>

    --{{1}}--
Diese Basis-Query funktioniert – aber PouchDB führt einen Full-Table-Scan durch. Bei 10 Dokumenten kein Problem, bei 100.000 katastrophal. Deshalb behandeln wir gleich Indizes. Aber zuerst: komplexere Queries.

### Selektoren: Vergleichsoperatoren

    {{1-2}}
<section>

**Mango bietet reichhaltige Operatoren:**

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `$eq` | Gleich | `{age: {$eq: 30}}` |
| `$ne` | Ungleich | `{status: {$ne: 'deleted'}}` |
| `$gt` | Größer als | `{price: {$gt: 100}}` |
| `$gte` | Größer oder gleich | `{age: {$gte: 18}}` |
| `$lt` | Kleiner als | `{stock: {$lt: 10}}` |
| `$lte` | Kleiner oder gleich | `{rating: {$lte: 3}}` |
| `$in` | Ist in Liste | `{category: {$in: ['A', 'B']}}` |
| `$nin` | Nicht in Liste | `{status: {$nin: ['draft', 'deleted']}}` |

**Beispiel: Produkte zwischen 100€ und 500€:**

```javascript
await db.find({
  selector: {
    price: {
      $gte: 100,
      $lte: 500
    }
  }
});
```

</section>

    --{{2}}--
Diese Operatoren sollten SQL-Nutzern vertraut vorkommen – aber in JSON-Notation. Der Vorteil: Queries sind selbst Daten und können programmatisch generiert werden. Kein String-Concatenation wie bei SQL-Injection-Risiken.

### Logische Operatoren: AND, OR, NOT

    {{2-3}}
<section>

**Komplexe Bedingungen kombinieren:**

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `$and` | Alle Bedingungen müssen wahr sein | `{$and: [{a: 1}, {b: 2}]}` |
| `$or` | Mindestens eine Bedingung wahr | `{$or: [{a: 1}, {b: 2}]}` |
| `$not` | Negation | `{age: {$not: {$lt: 18}}}` |
| `$nor` | Keine Bedingung wahr | `{$nor: [{a: 1}, {b: 2}]}` |

**Beispiel: Produkte in "Electronics" ODER "Books" mit Preis > 20€:**

```javascript
await db.find({
  selector: {
    $and: [
      {
        $or: [
          { category: 'Electronics' },
          { category: 'Books' }
        ]
      },
      {
        price: { $gt: 20 }
      }
    ]
  }
});
```

</section>

    --{{3}}--
Beachten Sie die Verschachtelung: AND auf oberster Ebene, OR darunter. Diese Struktur reflektiert die logische Priorität. In SQL wäre das: WHERE (category = 'Electronics' OR category = 'Books') AND price > 20. Mango ist expliziter, aber auch verboseiser.

### Verschachtelte Felder & Arrays

    {{3-4}}
<section>

**Dot-Notation für verschachtelte Objekte:**

```javascript
// Dokument:
{
  _id: 'user_001',
  name: 'Alice',
  address: {
    city: 'Berlin',
    zip: '10115'
  }
}

// Query:
await db.find({
  selector: {
    'address.city': 'Berlin'  // Achtung: String mit Punkt!
  }
});
```

**Array-Operatoren:**

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| `$elemMatch` | Mindestens ein Array-Element erfüllt Bedingung | `{tags: {$elemMatch: {$eq: 'urgent'}}}` |
| `$size` | Array hat bestimmte Länge | `{tags: {$size: 3}}` |
| `$all` | Array enthält alle Werte | `{tags: {$all: ['red', 'blue']}}` |

**Beispiel: Produkte mit Tag "computer":**

```javascript
await db.find({
  selector: {
    tags: 'computer'  // Vereinfachte Schreibweise
  }
});

// Oder explizit:
await db.find({
  selector: {
    tags: { $elemMatch: { $eq: 'computer' } }
  }
});
```

</section>

    --{{4}}--
Arrays sind tricky: PouchDB prüft automatisch, ob der Wert im Array enthalten ist. `tags: 'computer'` findet Dokumente mit `tags: ['computer', 'laptop']`. Für komplexere Bedingungen – etwa "Array enthält Objekt mit property X" – brauchen Sie `$elemMatch`.

### Sortierung, Limitierung & Pagination

    {{4}}
<section>

**Zusätzliche Query-Optionen:**

```javascript
await db.find({
  selector: {
    category: 'Electronics'
  },
  sort: [{ price: 'asc' }],  // Sortierung (erfordert Index!)
  limit: 10,                 // Max. 10 Ergebnisse
  skip: 20                   // Überspringe erste 20 (Pagination)
});
```

**Wichtig:**

- `sort` erfordert einen Index auf dem Sortierfeld
- `skip` ist ineffizient bei großen Offsets (besser: Cursor-basierte Pagination)
- `fields` kann genutzt werden, um nur bestimmte Felder zu laden

**Beispiel: Top 5 teuerste Produkte:**

```javascript
await db.find({
  selector: {
    price: { $exists: true }
  },
  sort: [{ price: 'desc' }],
  limit: 5
});
```

</section>

---

## Block 4: Index-Strategien für Performance

    --{{0}}--
Jetzt die entscheidende Frage: Brauchen Sie für Mango-Queries immer Indizes? Nein – aber ohne Indizes führt PouchDB einen Full-Table-Scan durch. Bei 100 Dokumenten merken Sie das nicht, bei 100.000 wird Ihre App unbenutzbar. Lassen Sie uns den Unterschied messen.

### Warum Indizes? Full-Scan vs. Index-Lookup

    {{0-1}}
<section>

**Ohne Index:**

```javascript
// Query ohne Index
await db.find({
  selector: { category: 'Electronics' }
});

// PouchDB macht:
// 1. Lädt ALLE Dokumente aus IndexedDB
// 2. Filtert im Speicher: if (doc.category === 'Electronics')
// 3. Gibt passende zurück
// Komplexität: O(n) – linear zur Dokumentenanzahl
```

**Mit Index:**

```javascript
// Index erstellen
await db.createIndex({
  index: { fields: ['category'] }
});

// Gleiche Query – jetzt mit Index
await db.find({
  selector: { category: 'Electronics' }
});

// PouchDB macht:
// 1. Nutzt Index: Lookup in B-Tree-ähnlicher Struktur
// 2. Lädt nur passende Dokumente
// Komplexität: O(log n) + O(k) – k = Anzahl Treffer
```

</section>

    --{{1}}--
Der Unterschied wird dramatisch bei wachsenden Datenmengen. Bei 1.000 Dokumenten: Full-Scan ~10ms, Index ~2ms. Bei 100.000 Dokumenten: Full-Scan ~1000ms, Index ~5ms. Indizes sind nicht optional für Production-Systeme – sie sind essentiell.

### PouchDB Index-Erstellung

    {{1-2}}
<section>

**Syntax:**

```javascript
await db.createIndex({
  index: {
    fields: ['field1', 'field2', ...]  // Array von Feldnamen
  }
});
```

**Einfacher Index (ein Feld):**

```javascript
// Index auf "category"
await db.createIndex({
  index: { fields: ['category'] }
});

// Beschleunigt Queries wie:
await db.find({
  selector: { category: 'Electronics' }
});
```

**Composite Index (mehrere Felder):**

```javascript
// Index auf "category" UND "price"
await db.createIndex({
  index: { fields: ['category', 'price'] }
});

// Beschleunigt Queries wie:
await db.find({
  selector: {
    category: 'Electronics',
    price: { $gt: 100 }
  },
  sort: [{ price: 'asc' }]
});
```

</section>

    --{{2}}--
Composite Indizes sind mächtig, aber subtil: Die Reihenfolge der Felder ist wichtig! Ein Index `['category', 'price']` beschleunigt Queries auf "category" oder "category + price", aber NICHT nur "price". Das ist wie ein Telefonbuch: sortiert nach Nachname, dann Vorname – Sie finden "Schmidt, Anna" schnell, aber "alle Annas" nicht.

### Index-Planung: Welche Felder indexieren?

    {{2-3}}
<section>

**Entscheidungskriterien:**

1. **Häufigkeit:** Wird das Feld oft in Queries verwendet?
2. **Selektivität:** Hat das Feld viele unterschiedliche Werte? (Hoch = gut für Index)
3. **Sortierung:** Wird nach dem Feld sortiert?
4. **Kosten:** Indizes verlangsamen Writes und verbrauchen Speicher

**Beispiel-Bewertung (Produktkatalog):**

| Feld | Häufigkeit | Selektivität | Index? | Begründung |
|------|------------|--------------|--------|------------|
| `category` | Hoch | Mittel (10 Kategorien) | ✅ Ja | Häufige Filterung |
| `price` | Mittel | Hoch (viele Preise) | ✅ Ja | Sortierung + Range Queries |
| `sku` | Hoch | Sehr hoch (unique) | ✅ Ja | Einzelabfragen |
| `inStock` | Niedrig | Niedrig (boolean) | ❌ Nein | Nur 2 Werte, selten Query |
| `description` | Niedrig | Hoch | ❌ Nein | Fulltext-Index nötig (anders) |

**Faustregel:**

> Indexiere Felder, die in `selector` und `sort` auftauchen – aber nicht alle!

</section>

    --{{3}}--
Zu viele Indizes sind schädlich: Jeder Write muss alle Indizes aktualisieren. Ein häufiger Fehler: "Ich erstelle Indizes auf alle Felder, dann bin ich safe." Falsch! Sie zahlen mit Schreib-Performance und Speicher für Indizes, die nie genutzt werden. Indexieren Sie gezielt basierend auf realen Query-Patterns.

### Live-Performance-Demo

    {{3}}
<section>

**Experiment: Messen wir den Unterschied!**

```javascript
// Setup: 1000 Produkte einfügen
const products = [];
for (let i = 0; i < 1000; i++) {
  products.push({
    _id: `product_${i}`,
    name: `Product ${i}`,
    category: ['Electronics', 'Books', 'Clothing'][i % 3],
    price: Math.floor(Math.random() * 500) + 10,
    tags: ['tag1', 'tag2', 'tag3']
  });
}
await db.bulkDocs(products);

// Test 1: Query OHNE Index
console.time('Without Index');
await db.find({
  selector: { category: 'Electronics', price: { $gt: 100 } }
});
console.timeEnd('Without Index');

// Index erstellen
await db.createIndex({
  index: { fields: ['category', 'price'] }
});

// Test 2: Query MIT Index
console.time('With Index');
await db.find({
  selector: { category: 'Electronics', price: { $gt: 100 } }
});
console.timeEnd('With Index');
```

**Erwartetes Ergebnis:**

- Ohne Index: ~50-100ms (Full-Scan über 1000 Docs)
- Mit Index: ~5-15ms (Index-Lookup + Laden der Treffer)

**Speedup: ~5-10x** bei nur 1000 Dokumenten!

</section>

---

## Block 5: Schema-Evolution & Versionierung

    --{{0}}--
Ein großer Vorteil von Document Stores: Schema-Flexibilität. Aber Flexibilität bedeutet nicht Chaos. Wie gehen Sie mit Dokumenten um, die unterschiedliche Strukturen haben? Wie migrieren Sie von Version 1 zu Version 2?

### Schema-Evolution: Das Problem

    {{0-1}}
<section>

**Szenario:**

Ihre App speichert User-Profile:

```javascript
// Version 1 (Launch):
{
  _id: 'user_001',
  name: 'Alice',
  email: 'alice@example.com'
}

// Version 2 (nach 6 Monaten – neue Features):
{
  _id: 'user_042',
  name: 'Bob',
  email: 'bob@example.com',
  preferences: {
    theme: 'dark',
    language: 'de'
  },
  subscriptionTier: 'premium'
}
```

**Problem:**

- Alte Dokumente haben keine `preferences` oder `subscriptionTier`
- Code muss mit beiden Versionen umgehen
- Queries müssen unterschiedliche Strukturen berücksichtigen

**Ohne Strategie:**

- ❌ Code voller `if (doc.preferences)` Checks
- ❌ Inkonsistente Datenqualität
- ❌ Schwierige Analyse (manche Felder fehlen)

</section>

    --{{1}}--
Schema-Evolution ist unvermeidlich in langlebigen Systemen. Die Frage ist nicht ob, sondern wie Sie damit umgehen. Document Stores erlauben Evolution, aber erzwingen sie nicht – Sie müssen aktiv managen.

### Migration-Patterns

    {{1-2}}
<section>

**Pattern 1: Lazy Migration (on-read)**

```javascript
async function getUser(id) {
  const doc = await db.get(id);
  
  // Migriere, falls alte Version
  if (!doc.schemaVersion || doc.schemaVersion < 2) {
    doc.preferences = doc.preferences || { theme: 'light', language: 'en' };
    doc.subscriptionTier = doc.subscriptionTier || 'free';
    doc.schemaVersion = 2;
    
    // Speichere migrierte Version
    await db.put(doc);
  }
  
  return doc;
}
```

**Vorteile:**

- ✅ Keine Downtime (keine Batch-Migration)
- ✅ Dokumente werden nur bei Bedarf migriert

**Nachteile:**

- ❌ Code muss weiterhin alte Versionen verstehen
- ❌ Queries sehen gemischte Strukturen

---

**Pattern 2: Eager Migration (batch)**

```javascript
async function migrateAllUsers() {
  const result = await db.allDocs({ include_docs: true });
  
  const migrations = result.rows
    .filter(row => !row.doc.schemaVersion || row.doc.schemaVersion < 2)
    .map(row => {
      const doc = row.doc;
      doc.preferences = doc.preferences || { theme: 'light', language: 'en' };
      doc.subscriptionTier = doc.subscriptionTier || 'free';
      doc.schemaVersion = 2;
      return doc;
    });
  
  await db.bulkDocs(migrations);
  console.log(`Migrated ${migrations.length} documents`);
}
```

**Vorteile:**

- ✅ Konsistente Datenstruktur nach Migration
- ✅ Code kann alte Versionen vergessen

**Nachteile:**

- ❌ Erfordert Wartungsfenster bei großen Datenmengen
- ❌ Alle Dokumente werden geändert (Revision-History wächst)

</section>

    --{{2}}--
In der Praxis kombinieren Sie oft beide: Lazy Migration für graduelle Änderungen, Eager Migration für Breaking Changes vor Major-Releases. Wichtig: Versionsnummern im Dokument (`schemaVersion` Feld) machen Migrationen nachvollziehbar.

### Schema-Validierung (optional)

    {{2}}
<section>

**PouchDB unterstützt keine native Validierung** – aber Sie können es in der App-Schicht implementieren:

```javascript
// JSON Schema Definition
const userSchema = {
  type: 'object',
  required: ['name', 'email'],
  properties: {
    name: { type: 'string', minLength: 1 },
    email: { type: 'string', format: 'email' },
    age: { type: 'number', minimum: 0 },
    preferences: {
      type: 'object',
      properties: {
        theme: { enum: ['light', 'dark'] },
        language: { type: 'string' }
      }
    }
  }
};

// Validierung vor Save (mit Ajv library)
const Ajv = require('ajv');
const ajv = new Ajv();
const validate = ajv.compile(userSchema);

async function saveUser(user) {
  if (!validate(user)) {
    throw new Error(`Validation failed: ${JSON.stringify(validate.errors)}`);
  }
  await db.put(user);
}
```

**Trade-off:**

- ✅ Explizite Kontrakte
- ✅ Frühe Fehlerkennung
- ❌ Mehr Boilerplate
- ❌ Schema-Evolution erfordert Code-Updates

</section>

---

## Block 6: Offline-First & Synchronisation

    --{{0}}--
Jetzt kommen wir zu einem der mächtigsten Features von PouchDB: Offline-First Architektur. Ihre App funktioniert ohne Netzwerk, Daten werden lokal gespeichert, und sobald Verbindung besteht, synchronisiert alles automatisch. Klingt magisch – aber es gibt Tücken.

### Offline-First Architektur

    {{0-1}}
<section>

**Konzept:**

```ascii
┌─────────────┐           ┌─────────────┐
│   Browser   │           │   Server    │
│             │           │             │
│  PouchDB    │  <---->   │  CouchDB    │
│  (local)    │   Sync    │  (remote)   │
└─────────────┘           └─────────────┘
     │                          │
     │ Offline:                 │ Immer verfügbar
     │ Writes → local           │
     │ Reads ← local            │
     │                          │
     │ Online:                  │
     │ Bi-direktionale Sync     │
     └──────────────────────────┘
```

**Vorteile:**

- ✅ App funktioniert ohne Internet
- ✅ Instant Writes (keine Latenz)
- ✅ Automatische Sync bei Reconnect

**Use Cases:**

- Mobile Apps (flaky connections)
- Collaborative Tools (Google Docs-Style)
- Field Service Apps (Techniker ohne Netz)

</section>

    --{{1}}--
Offline-First ist kein Nischen-Feature mehr – es ist Best Practice für moderne Web-Apps. Nutzer erwarten, dass Apps funktionieren, egal ob im Flugzeug oder im Funkloch. PouchDB macht das trivial – zumindest auf der Happy-Path.

### Sync Setup: PouchDB ↔ CouchDB

    {{1-2}}
<section>

**Einmalige Sync (Pull):**

```javascript
const localDB = new PouchDB('my_local_db');
const remoteDB = new PouchDB('https://myserver.com/my_remote_db');

// Daten vom Server holen
await localDB.replicate.from(remoteDB);
```

**Einmalige Sync (Push):**

```javascript
// Lokale Änderungen zum Server senden
await localDB.replicate.to(remoteDB);
```

**Bidirektionale Live-Sync:**

```javascript
// Kontinuierliche Synchronisation in beide Richtungen
const sync = localDB.sync(remoteDB, {
  live: true,           // Bleibt offen, hört auf Änderungen
  retry: true           // Reconnect bei Verbindungsabbruch
});

// Events
sync.on('change', info => {
  console.log('Sync change:', info);
});

sync.on('error', err => {
  console.error('Sync error:', err);
});

sync.on('active', () => {
  console.log('Sync resumed');
});

sync.on('paused', err => {
  console.log('Sync paused', err);
});
```

</section>

    --{{2}}--
Live-Sync ist der Kern von Offline-First: Lokale Änderungen werden automatisch hochgeladen, Remote-Änderungen heruntergeladen. Das funktioniert asynchron – Ihre App blockiert nie. Aber: Was passiert bei Konflikten?

### Konfliktauflösung: Das Problem

    {{2-3}}
<section>

**Szenario:**

Alice und Bob editieren dasselbe Dokument offline:

```javascript
// Initiales Dokument (Server):
{
  _id: 'doc_001',
  _rev: '1-abc',
  title: 'Original'
}

// Alice's Änderung (offline):
{
  _id: 'doc_001',
  _rev: '2-alice',
  title: 'Updated by Alice'
}

// Bob's Änderung (offline):
{
  _id: 'doc_001',
  _rev: '2-bob',
  title: 'Updated by Bob'
}

// Beide syncen → KONFLIKT!
```

**Wie entscheidet das System?**

- ❌ **Nicht möglich:** Beide Versionen gleichzeitig richtig
- ⚠️ **Last-Write-Wins:** Einfach, aber Daten gehen verloren
- ✅ **CouchDB-Ansatz:** Deterministischer Gewinner + Conflict-Flag

</section>

    --{{3}}--
CouchDB/PouchDB nutzen einen cleveren Ansatz: Das System wählt deterministisch einen "Gewinner" (basierend auf Revisions-IDs), behält aber BEIDE Versionen. Ihre App sieht standardmäßig den Gewinner, kann aber Konflikte erkennen und manuell auflösen.

### Konfliktauflösung: Implementierung

    {{3-4}}
<section>

**Konflikte erkennen:**

```javascript
const doc = await db.get('doc_001', { conflicts: true });

if (doc._conflicts) {
  console.log('Konflikt erkannt!', doc._conflicts);
  // doc._conflicts = ['2-bob', '2-alice']  // Verlierer-Revisions
}
```

**Manuelle Auflösung:**

```javascript
async function resolveConflict(id) {
  // Lade Dokument mit Konflikten
  const doc = await db.get(id, { conflicts: true });
  
  if (!doc._conflicts) {
    return; // Kein Konflikt
  }
  
  // Lade alle konfliktierenden Versionen
  const conflicts = await Promise.all(
    doc._conflicts.map(rev => db.get(id, { rev }))
  );
  
  // Merge-Strategie (Beispiel: Neueste Änderung gewinnt)
  const merged = {
    ...doc,
    title: doc.title,  // Nutze Gewinner-Version
    lastModified: new Date().toISOString()
  };
  delete merged._conflicts;
  
  // Speichere Merge-Ergebnis
  await db.put(merged);
  
  // Lösche verlierende Revisionen
  await Promise.all(
    doc._conflicts.map(rev =>
      db.remove(id, rev)
    )
  );
}
```

**Custom Merge (intelligenter):**

```javascript
// Merge-Logik: Felder vergleichen
function mergeDocuments(winner, loser) {
  return {
    _id: winner._id,
    _rev: winner._rev,
    title: winner.title,
    // Merge-Regel: Nutze neuere Änderung
    content: winner._rev > loser._rev ? winner.content : loser.content,
    tags: [...new Set([...winner.tags, ...loser.tags])]  // Vereinigung
  };
}
```

</section>

    --{{4}}--
Konfliktauflösung ist komplex – es gibt keine universelle Lösung. Last-Write-Wins ist simpel, aber naiv. Operational Transformation (wie in Google Docs) ist mächtig, aber extrem komplex. CRDTs (Conflict-free Replicated Data Types) sind elegant, aber spezialisiert. Für die meisten Apps reicht: Konflikte erkennen, UI zeigen ("Alice und Bob haben gleichzeitig editiert"), Nutzer entscheiden lassen.

### Live-Demo: Zwei Browser-Tabs synchronisieren

    {{4}}
<section>

**Experiment:**

1. **Tab 1:** Öffne DevTools Console
2. **Tab 2:** Öffne weitere DevTools Console

**Tab 1:**

```javascript
const db1 = new PouchDB('sync_demo');
await db1.put({ _id: 'shared_doc', content: 'Initial' });

// Simuliere Remote-DB (Tab 2)
const remote = new PouchDB('sync_demo_remote');
db1.sync(remote, { live: true, retry: true });
```

**Tab 2:**

```javascript
const db2 = new PouchDB('sync_demo_remote');

// Watch für Änderungen
db2.changes({ live: true, since: 'now', include_docs: true })
  .on('change', change => {
    console.log('Received:', change.doc);
  });

// Update Dokument
await db2.put({ _id: 'shared_doc', _rev: '...', content: 'Updated!' });
```

**Beobachtung:**

- Änderung in Tab 2 erscheint automatisch in Tab 1
- Live-Sync funktioniert bidirektional
- Keine manuelle Refresh nötig

</section>

---

## Block 7: Use Cases & Abgrenzung

    --{{0}}--
Abschließend: Wann sollten Sie Document Stores einsetzen – und wann nicht? Lassen Sie uns typische Szenarien durchgehen und Entscheidungskriterien entwickeln.

### Typische Use Cases

    {{0-1}}
<section>

**Perfekt für Document Stores:**

1. **Content Management Systeme**
   - Flexible Dokument-Strukturen (Posts, Pages, Comments)
   - Schema evolviert mit Features
   - Beispiel: Blog-Plattformen, Wikis

2. **User Profiles & Session Data**
   - Heterogene Nutzer-Daten (nicht alle haben gleiche Felder)
   - Schnelle Reads/Writes
   - Beispiel: E-Commerce User Profiles

3. **Mobile Apps (Offline-First)**
   - Lokale Persistenz + Remote Sync
   - Flaky Connections
   - Beispiel: Notiz-Apps, Field Service Tools

4. **Event Logging & Analytics**
   - Flexible Event-Schemas
   - Append-only Workload
   - Beispiel: Application Logs, User Events

5. **Kataloge & Produktdaten**
   - Semi-strukturierte Daten
   - Viele Reads, wenige Writes
   - Beispiel: E-Commerce Produktkataloge

</section>

    --{{1}}--
Der gemeinsame Nenner: Flexible Schemas, hierarchische Daten, und Lesefokus mit gelegentlichen Writes. Document Stores glänzen, wenn Ihre Daten natürlich als JSON modelliert werden – nicht als Tabellen.

### Wann NICHT Document Stores?

    {{1-2}}
<section>

**Besser Relational:**

1. **Komplexe Transaktionen**
   - Bankgeschäfte, Bestellungen mit Inventory-Updates
   - Brauchen ACID-Garantien über mehrere Entities
   - Document Stores: Transaktionen nur pro Dokument

2. **Viele Joins über Entities**
   - Relationale Queries mit 5+ Tables
   - Document Stores: Joins sind teuer/unmöglich
   - Normalisierung ist besser

3. **Strikte Schema-Validierung**
   - Regulatorische Anforderungen (GDPR, Finance)
   - Explizite Kontrakte über Teams
   - Document Stores: Validierung ist optional

**Besser Key-Value:**

1. **Pure Caching**
   - Session-Speicher, Rate-Limiting
   - Nur Key-Lookups, keine Queries
   - Document Stores sind Overkill

**Besser Graph:**

1. **Beziehungsintensive Queries**
   - Social Networks, Recommendations
   - Traversals ("Freunde von Freunden")
   - Document Stores: Graph-Queries ineffizient

</section>

    --{{2}}--
Die Frage ist nie "Ist MongoDB besser als PostgreSQL?", sondern "Welche Probleme habe ich, und welches Tool passt?" Document Stores sind mächtig für flexible, hierarchische Daten – aber keine Allzweckwaffe.

### Entscheidungsmatrix

    {{2}}
<section>

| Kriterium | Document Store | Relational | Key-Value | Graph |
|-----------|----------------|------------|-----------|-------|
| **Schema-Flexibilität** | ✅✅✅ | ❌ | ✅✅ | ✅✅ |
| **Komplexe Queries** | ✅✅ | ✅✅✅ | ❌ | ✅ (Traversals) |
| **Transaktionen** | ⚠️ (Single-Doc) | ✅✅✅ | ❌ | ⚠️ |
| **Skalierung (Horizontal)** | ✅✅ | ⚠️ | ✅✅✅ | ⚠️ |
| **Performance (Reads)** | ✅✅ | ✅✅ | ✅✅✅ | ✅ |
| **Performance (Writes)** | ✅✅ | ✅ | ✅✅✅ | ✅ |
| **Offline-First** | ✅✅✅ | ❌ | ⚠️ | ❌ |
| **Lernkurve** | ✅✅ | ✅ | ✅✅✅ | ⚠️ |

**Legende:** ✅✅✅ = Exzellent, ✅✅ = Gut, ✅ = Okay, ⚠️ = Eingeschränkt, ❌ = Ungeeignet

</section>

---

## Zusammenfassung & Reflexion

    --{{0}}--
Fassen wir zusammen: Document Stores sind die natürliche Evolution von Key-Value Systemen für strukturierte Daten. Sie bieten Flexibilität ohne Chaos – wenn Sie bewusst mit Schemas, Indizes und Sync umgehen.

    {{0-1}}
<section>

### Kernerkenntnisse

1. **Document Stores = Strukturierte NoSQL**
   - JSON als First-Class Citizen
   - Sekundäre Indizes für flexible Queries
   - Schema-optional, aber kontrollierbar

2. **Mango-Queries = Deklarative Suche**
   - Operatoren: `$eq`, `$gt`, `$in`, `$and`, `$or`, ...
   - Verschachtelte Felder & Arrays unterstützt
   - Indizes sind essentiell für Performance

3. **Offline-First = Killer-Feature**
   - PouchDB + CouchDB = Seamless Sync
   - Konflikte unvermeidlich bei Kollaboration
   - Manuelle Auflösung nötig für kritische Fälle

4. **Use Case abhängig:**
   - ✅ Flexible Schemas, hierarchische Daten, Offline-Apps
   - ❌ Komplexe Joins, strikte Transaktionen

</section>

    --{{1}}--
Document Stores füllen eine wichtige Lücke zwischen simplen Key-Value Stores und rigiden relationalen Datenbanken. Sie sind nicht "besser" oder "schlechter" – sie lösen andere Probleme. Ihre Aufgabe als Entwickler: Erkennen Sie, welche Probleme Sie haben.

    {{1}}
<section>

### 🤔 Reflexionsfragen (2 Minuten)

> **Persönliche Reflexion:**
>
> 1. Haben Sie ein aktuelles Projekt, das von Document Stores profitieren würde?
> 2. Wo würden Sie Key-Value NICHT durch Document Store ersetzen?
> 3. Wie würden Sie Offline-Konflikte in einer Kollaborations-App lösen?

**Nächste Schritte:**

- Projekt MS1: Implementieren Sie einen Document-Layer für Ihre Daten
- Vergleichen Sie: Wann KV, wann Document?

</section>

---

## Ausblick: Session 4 – Column Stores

    --{{0}}--
In der nächsten Session wechseln wir die Perspektive: Bisher fokussierten wir auf Transaktionen und Reads einzelner Dokumente. Column Stores optimieren für eine völlig andere Workload: Aggregationen über Millionen Zeilen. Statt "Finde User 42" fragen wir: "Was ist der Durchschnittspreis aller Produkte in Kategorie X?"

    {{0}}
<section>

### Session 4 Preview: Column Stores

**Fokus:**

- **Spaltenorientierte Speicherung** (vs. Zeilen in KV/Document)
- **Kompression** (warum Column Stores 10x weniger Platz brauchen)
- **Analytics-Queries** (SUM, AVG, GROUP BY über große Datasets)
- **OLAP vs. OLTP** (wann welches Paradigma?)

**Demo-System:**

- DuckDB (SQL-basiert, läuft im Browser via WebAssembly)
- Parquet-Format (Column-Storage)

**Lernziel:**

> Verstehen Sie den Trade-off: Column Stores sind brillant für Analytics, aber langsam für Punkt-Abfragen

</section>

---

## Referenzen & Vertiefung

    --{{0}}--
Für alle, die tiefer einsteigen möchten – hier die wichtigsten Ressourcen zu Document Stores, PouchDB und verwandten Themen.

    {{0}}
<section>

### Offizielle Dokumentation

- **PouchDB Guides:** [https://pouchdb.com/guides/](https://pouchdb.com/guides/)
- **PouchDB Find Plugin (Mango):** [https://pouchdb.com/guides/mango-queries.html](https://pouchdb.com/guides/mango-queries.html)
- **CouchDB Mango Query Reference:** [https://docs.couchdb.org/en/stable/api/database/find.html](https://docs.couchdb.org/en/stable/api/database/find.html)
- **CouchDB Replication Protocol:** [https://docs.couchdb.org/en/stable/replication/protocol.html](https://docs.couchdb.org/en/stable/replication/protocol.html)

### Konzeptuelle Ressourcen

- **JSON Schema Specification:** [https://json-schema.org/](https://json-schema.org/)
- **IndexedDB API (Browser):** [https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- **MongoDB Query Language** (Vergleich): [https://www.mongodb.com/docs/manual/tutorial/query-documents/](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- **Offline-First Principles:** [https://offlinefirst.org/](https://offlinefirst.org/)

### Bücher

- **"CouchDB: The Definitive Guide"** (Anderson, Lehnardt, Slater)
- **"Designing Data-Intensive Applications"** (Kleppmann) – Kapitel 5: Replication

### Verwandte Technologien

- **MongoDB:** Document Store mit großem Ecosystem
- **Firebase/Firestore:** Google's Document Store (Cloud-hosted)
- **RxDB:** Reactive Database auf PouchDB-Basis

</section>

---

## Anhang: Praktische Code-Snippets

    --{{0}}--
Zum Abschluss: Eine Sammlung wiederverwendbarer Snippets für Ihre eigenen Projekte.

    {{0}}
<section>

### Setup-Boilerplate

```javascript
// PouchDB mit allen Plugins
import PouchDB from 'pouchdb';
import PouchDBFind from 'pouchdb-find';

PouchDB.plugin(PouchDBFind);

const db = new PouchDB('my_app_db');

// Remote-Sync konfigurieren
const remoteDB = new PouchDB('https://myserver.com/db', {
  auth: {
    username: 'user',
    password: 'pass'
  }
});

// Bidirektionale Live-Sync
const sync = db.sync(remoteDB, {
  live: true,
  retry: true
});

sync.on('change', info => console.log('Synced:', info));
sync.on('error', err => console.error('Sync error:', err));
```

### CRUD-Operationen

```javascript
// Create
await db.put({
  _id: 'user_001',
  name: 'Alice',
  email: 'alice@example.com'
});

// Read
const user = await db.get('user_001');

// Update (benötigt _rev!)
user.email = 'newemail@example.com';
await db.put(user);

// Delete
await db.remove(user);

// Bulk Insert
await db.bulkDocs([
  { _id: 'doc1', data: 'a' },
  { _id: 'doc2', data: 'b' }
]);
```

### Query-Pattern

```javascript
// Index erstellen (nur einmal nötig)
await db.createIndex({
  index: { fields: ['category', 'price'] }
});

// Query ausführen
const result = await db.find({
  selector: {
    category: 'Electronics',
    price: { $gt: 100, $lt: 500 }
  },
  sort: [{ price: 'asc' }],
  limit: 10
});

console.log(result.docs);
```

### Error-Handling

```javascript
try {
  await db.put(doc);
} catch (err) {
  if (err.status === 409) {
    // Conflict (Document wurde zwischenzeitlich geändert)
    const latest = await db.get(doc._id);
    // Merge und retry
  } else if (err.status === 404) {
    // Document nicht gefunden
  } else {
    // Anderer Fehler
    throw err;
  }
}
```

</section>

---

    --{{0}}--
Vielen Dank für Ihre Aufmerksamkeit! Sie haben heute Document Stores von Grund auf kennengelernt – von JSON-Persistenz über komplexe Queries bis zu Offline-Sync. In Session 4 wechseln wir die Perspektive und schauen auf Column Stores: Wie speichern und analysieren wir Daten, wenn wir nicht einzelne Dokumente lesen, sondern Millionen Zeilen aggregieren? Bis dahin: Experimentieren Sie mit PouchDB in Ihren eigenen Projekten!
