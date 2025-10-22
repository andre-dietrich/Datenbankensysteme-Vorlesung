<!--
language: de
narrator: German Male

script:   https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js
link:     https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.css

@eval
<script>@input

""</script>
@end
-->

import: https://raw.githubusercontent.com/LiaScript/CodeRunner/master/README.md

# JavaScript Essentials – Ein Primer für Database-Beispiele

    --{{0}}--
Willkommen zum JavaScript-Primer! Dieses Tutorial ist speziell für alle, die wenig oder keine JavaScript-Erfahrung haben, aber die Code-Beispiele in unserer Datenbank-Vorlesung verstehen möchten. Sie müssen kein JavaScript-Experte werden – aber Sie sollten die Grundkonzepte kennen, um die Datenbankoperationen nachvollziehen zu können.

## 🎯 Was Sie hier lernen

    {{0}}
<section>

**Ziel dieses Primers:**

> Verstehen Sie JavaScript gut genug, um Database-Code zu lesen, zu verstehen und anzupassen – ohne Frontend-Entwickler zu werden.

**Was behandelt wird:**

- ✅ Variablen & Datentypen
- ✅ Kontrollstrukturen (if/else, Schleifen)
- ✅ Funktionen & Arrow Functions
- ✅ Objekte & Arrays (mit wichtigen Methoden)
- ✅ Asynchronität (async/await, Promises)
- ✅ JSON & Datenformate
- ✅ Classes (Bonus)
- ✅ Console & Debugging

**Was NICHT behandelt wird:**

- ❌ DOM-Manipulation (HTML/CSS)
- ❌ Frontend-Frameworks (React, Vue, etc.)
- ❌ Node.js-spezifische APIs
- ❌ Fortgeschrittene Patterns (Closures, Prototypes, etc.)

**Geschätzter Zeitaufwand:** 60-90 Minuten

</section>

    --{{1}}--
JavaScript ist die Sprache des Webs – und damit perfekt für unsere Browser-basierten Datenbank-Demos. Wir nutzen moderne JavaScript-Syntax (ES6+), die Sie in allen aktuellen Browsern ausführen können. Keine Installation nötig – öffnen Sie einfach die Browser DevTools Console und experimentieren Sie!

---

## Kapitel 1: Grundlagen – Variablen & Datentypen

    --{{0}}--
Starten wir mit den absoluten Basics: Wie speichern wir Daten in JavaScript? Welche Arten von Daten gibt es? Variablen sind Container für Werte – wie beschriftete Boxen, in die Sie Dinge legen können. JavaScript ist dynamisch typisiert, das heißt: Sie müssen nicht im Voraus festlegen, welchen Datentyp eine Variable haben wird. Das macht die Sprache flexibel, aber auch fehleranfällig, wenn Sie nicht aufpassen.

### 1.1 Variablen deklarieren

    {{0}}
<section>

**Drei Arten, Variablen zu deklarieren:**

```javascript
console.log("=== Beispiel 1: Variablen-Deklaration ===");

// 1. const - Kann NICHT neu zugewiesen werden (Konstante)
const name = "Alice";
console.log("const name:", name);
// name = "Bob";  // ❌ Fehler: Assignment to constant variable

// 2. let - Kann neu zugewiesen werden (Block-Scope)
let age = 30;
console.log("let age (initial):", age);
age = 31;  // ✅ Funktioniert
console.log("let age (nach Änderung):", age);

// 3. var - ALT, vermeiden! (Function-Scope, Hoisting-Probleme)
var city = "Berlin";  // ⚠️ Nur für Legacy-Code
console.log("var city:", city);

console.log("\n💡 Empfehlung: Nutzen Sie const als Standard, let nur wenn nötig!");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Welche sollten Sie nutzen?**

| Keyword | Verwendung | Empfehlung |
|---------|------------|------------|
| `const` | Wert ändert sich nicht | ✅ **Standard** – nutzen Sie immer, wenn möglich |
| `let` | Wert ändert sich | ✅ Nur wenn Neuzuweisung nötig |
| `var` | Legacy | ❌ **Nie nutzen** in modernem Code |

**Faustregel:**

> Nutzen Sie **immer `const`** – außer Sie wissen sicher, dass sich der Wert ändern wird. Dann `let`.

</section>

    --{{1}}--
Der Unterschied zwischen const und let ist wichtig: const verhindert Neuzuweisungen, aber bei Objekten und Arrays können Sie trotzdem die Inhalte ändern – dazu später mehr. Var sollten Sie komplett vergessen – es hat verwirrende Scoping-Regeln und wurde durch let/const ersetzt.

    {{1}}
<section>

**Beispiel: const vs. let in der Praxis**

```javascript
console.log("=== Beispiel 2: const vs. let in der Praxis ===");

// Datenbankverbindung - ändert sich nie
const DB_NAME = "products_db";
const API_URL = "https://api.example.com";
console.log("Konstanten definiert:");
console.log("  DB_NAME:", DB_NAME);
console.log("  API_URL:", API_URL);

// Counter, der hochgezählt wird
let productCount = 0;
console.log("\nCounter initial:", productCount);
productCount++;  // ✅ OK mit let
console.log("Counter nach Inkrement:", productCount);

// Wichtig: const verhindert nur Neuzuweisung, nicht Mutation!
const products = [];
console.log("\nArray initial:", products);

products.push({ name: "Laptop" });  // ✅ OK - Array wird modifiziert
console.log("Array nach push:", products);

// products = [];  // ❌ Fehler - Neuzuweisung nicht erlaubt
console.log("\n💡 const verhindert Neuzuweisung, nicht Mutation von Objekten/Arrays!");
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Live-Test in der Console:**

```javascript
console.log("=== Live-Test: const Neuzuweisung ===");
const x = 10;
console.log("x initial:", x);

try {
  x = 20;  // Was passiert?
  console.log("x nach Zuweisung:", x);
} catch (error) {
  console.log("❌ Fehler:", error.message);
}
console.log("--- Ende Test ---");
```
@eval

</section>

    --{{2}}--
Dieser Unterschied ist subtil, aber zentral: const bedeutet "die Referenz ändert sich nicht", nicht "der Inhalt ändert sich nicht". Bei primitiven Werten wie Zahlen oder Strings ist das egal. Bei Objekten und Arrays können Sie Inhalte ändern, aber nicht das ganze Objekt ersetzen.

### 1.2 Primitive Datentypen

    {{2}}
<section>

**JavaScript hat 7 primitive Datentypen:**

| Typ | Beschreibung | Beispiele |
|-----|--------------|-----------|
| `Number` | Ganzzahlen & Dezimalzahlen | `42`, `3.14`, `-100`, `Infinity` |
| `String` | Text (in `""`, `''` oder Backticks) | `"Hello"`, `'World'`, `` `Hi` `` |
| `Boolean` | Wahr oder Falsch | `true`, `false` |
| `null` | Absichtlich leerer Wert | `null` |
| `undefined` | Variable ohne Wert | `undefined` |
| `BigInt` | Sehr große Ganzzahlen | `9007199254740991n` |
| `Symbol` | Eindeutiger Identifier | `Symbol("id")` |

**Wichtig für unsere Vorlesung:** Die ersten 5 reichen völlig! BigInt und Symbol sind Spezialfälle.

</section>

    --{{3}}--
Schauen wir uns die wichtigsten Typen im Detail an. Number, String und Boolean werden Sie ständig nutzen. Null und undefined sind oft verwirrend – aber wichtig zu verstehen, weil sie in Datenbank-Queries vorkommen können.

    {{3}}
<section>

**1. Number – Zahlen**

```javascript
console.log("=== Beispiel 3: Number-Datentyp ===");

// Ganzzahlen
const count = 42;
const negative = -17;
console.log("Ganzzahlen:");
console.log("  count:", count, "| typeof:", typeof count);
console.log("  negative:", negative);

// Dezimalzahlen (Floats)
const price = 19.99;
const pi = 3.14159;
console.log("\nDezimalzahlen:");
console.log("  price:", price);
console.log("  pi:", pi);

// Besondere Werte
const infinity = Infinity;
const notANumber = NaN;
console.log("\nBesondere Werte:");
console.log("  Infinity:", infinity);
console.log("  NaN:", notANumber, "| typeof:", typeof notANumber);

// Rechnen
const sum = 10 + 5;
const product = 10 * 5;
const division = 10 / 3;
console.log("\nBerechnungen:");
console.log("  10 + 5 =", sum);
console.log("  10 × 5 =", product);
console.log("  10 ÷ 3 =", division);

// Achtung: Floating Point Probleme!
const floatCalc = 0.1 + 0.2;
console.log("\n⚠️  Floating Point Problem:");
console.log("  0.1 + 0.2 =", floatCalc);
console.log("  (erwartet: 0.3, tatsächlich:", floatCalc, ")");

console.log("\n💡 Bei Geld: Mit Cents (Integer) rechnen!");
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Wichtig:**

- Kein Unterschied zwischen Integer und Float (alles `Number`)
- `NaN` ist technisch vom Typ `Number` (paradox!)
- Floating Point Arithmetik ist ungenau → bei Geld mit Cents rechnen!

</section>

    --{{4}}--
JavaScript hat nur einen Zahlentyp – das vereinfacht vieles, kann aber bei Präzision Probleme machen. Für Datenbank-Beispiele reicht das völlig, aber merken Sie sich: Bei Geldbeträgen niemals direkt mit Dezimalzahlen rechnen, sondern in Cents umrechnen.

    {{4}}
<section>

**2. String – Text**

```javascript
console.log("=== Beispiel 4: String-Datentyp ===");

// Drei Arten, Strings zu schreiben
const single = 'Einfache Anführungszeichen';
const double = "Doppelte Anführungszeichen";
const backtick = `Backticks (Template Literals)`;
console.log("Drei String-Varianten:");
console.log("  single:", single);
console.log("  double:", double);
console.log("  backtick:", backtick);

// String-Verkettung (alt)
const firstName = "Alice";
const lastName = "Smith";
const fullName = firstName + " " + lastName;
console.log("\nString-Verkettung (alt):");
console.log("  firstName + ' ' + lastName =", fullName);

// Template Literals (modern, empfohlen!)
const greeting = `Hello, ${firstName}!`;
const multi = `Zeile 1
Zeile 2`;
console.log("\nTemplate Literals (modern):");
console.log("  greeting:", greeting);
console.log("  multi:", multi);

// String-Eigenschaften & Methoden
console.log("\nString-Methoden:");
console.log("  firstName.length:", firstName.length);
console.log("  firstName.toUpperCase():", firstName.toUpperCase());
console.log("  firstName.toLowerCase():", firstName.toLowerCase());
console.log("  firstName.includes('li'):", firstName.includes("li"));

console.log("\n💡 Template Literals sind modern und lesbar!");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Template Literals (Backticks) sind modern und mächtig:**

```javascript
console.log("=== Beispiel 5: Template Literals im Detail ===");

const product = "Laptop";
const price = 999;

// Alt (mühsam):
const message1 = "Product: " + product + ", Price: " + price + "€";
console.log("Alt (String-Konkatenation):");
console.log("  ", message1);

// Modern (lesbar):
const message2 = `Product: ${product}, Price: ${price}€`;
console.log("\nModern (Template Literal):");
console.log("  ", message2);

// Mit Berechnungen
const taxRate = 0.19;
const priceWithTax = price * (1 + taxRate);
const message3 = `Product: ${product}, Price: ${price}€, With Tax: ${priceWithTax.toFixed(2)}€`;
console.log("\nMit Berechnungen:");
console.log("  ", message3);

console.log("\n💡 ${} kann beliebige JavaScript-Ausdrücke enthalten!");
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

    --{{5}}--
Template Literals mit Backticks werden Sie in unseren Beispielen ständig sehen – sie machen String-Interpolation so viel einfacher! Statt plus-Zeichen zu jonglieren, schreiben Sie einfach geschweifte Klammern mit Dollarzeichen. Gewöhnen Sie sich das direkt an.

    {{5}}
<section>

**3. Boolean – Wahr oder Falsch**

```javascript
console.log("=== Beispiel 6: Boolean-Datentyp ===");

// Nur zwei mögliche Werte
const isActive = true;
const isDeleted = false;
console.log("Boolean-Werte:");
console.log("  isActive:", isActive, "| typeof:", typeof isActive);
console.log("  isDeleted:", isDeleted);

// Oft Ergebnis von Vergleichen
const age = 25;
const stock = 10;
const isAdult = age >= 18;
const hasStock = stock > 0;
const isEqual = (5 === 5);
console.log("\nVergleiche (ergeben Boolean):");
console.log("  age >= 18:", isAdult);
console.log("  stock > 0:", hasStock);
console.log("  5 === 5:", isEqual);

// Boolean-Operatoren
const isAdmin = true;
const isPremium = false;
const canBuy = isAdult && hasStock;
const hasAccess = isAdmin || isPremium;
const isInactive = !isActive;
console.log("\nBoolean-Operatoren:");
console.log("  isAdult && hasStock (AND):", canBuy);
console.log("  isAdmin || isPremium (OR):", hasAccess);
console.log("  !isActive (NOT):", isInactive);

console.log("\n💡 Boolean = true/false, Grundlage für Bedingungen!");
console.log("--- Ende Beispiel 6 ---");
```
@eval

**Truthy & Falsy (wichtig!):**

JavaScript konvertiert Werte automatisch zu Boolean in Bedingungen:

```javascript
console.log("=== Beispiel 7: Truthy & Falsy ===");

console.log("Falsy-Werte (werden zu false):");
console.log("  if (0) →", Boolean(0), "→ nicht ausgeführt");
console.log("  if ('') →", Boolean(""), "→ nicht ausgeführt");
console.log("  if (null) →", Boolean(null), "→ nicht ausgeführt");
console.log("  if (undefined) →", Boolean(undefined), "→ nicht ausgeführt");
console.log("  if (NaN) →", Boolean(NaN), "→ nicht ausgeführt");
console.log("  if (false) →", Boolean(false), "→ nicht ausgeführt");

console.log("\nTruthy-Werte (werden zu true):");
console.log("  if (1) →", Boolean(1), "→ ausgeführt");
console.log("  if ('text') →", Boolean("text"), "→ ausgeführt");
console.log("  if ([]) →", Boolean([]), "→ ausgeführt (⚠️ auch leere Arrays!)");
console.log("  if ({}) →", Boolean({}), "→ ausgeführt (⚠️ auch leere Objekte!)");

console.log("\n⚠️  Wichtig: Leere Arrays/Objekte sind truthy!");
console.log("💡 Boolean(wert) zeigt die Konvertierung");
console.log("--- Ende Beispiel 7 ---");
```
@eval

</section>

    --{{6}}--
Truthy und Falsy sind extrem wichtig zu verstehen – viele Bugs entstehen, weil Entwickler vergessen, dass leere Arrays oder Objekte als true gelten! In Datenbank-Code prüfen Sie oft, ob ein Wert existiert – und da müssen Sie wissen, was JavaScript als "wahr" oder "falsch" ansieht.

    {{6}}
<section>

**4. null & undefined – Leere Werte**

```javascript
console.log("=== Beispiel 8: null & undefined ===");

// undefined - Variable existiert, hat aber keinen Wert
let product;
console.log("let product (ohne Zuweisung):");
console.log("  Wert:", product);
console.log("  typeof:", typeof product);

// null - Absichtlich leerer Wert
let user = null;
console.log("\nlet user = null:");
console.log("  Wert:", user);
console.log("  typeof:", typeof user, "(⚠️ historischer Bug!)");

// Typischer Use Case in Datenbanken
console.log("\nDatabase-Kontext:");
console.log("  const result = await db.get('user_123');");
console.log("  if (result === null) { /* User nicht gefunden */ }");

console.log("\n💡 undefined = automatisch, null = explizit leer");
console.log("--- Ende Beispiel 8 ---");
```
@eval

**Unterschied:**

| Wert | Bedeutung | Verwendung |
|------|-----------|------------|
| `undefined` | "Wert nicht gesetzt" | Automatisch von JavaScript |
| `null` | "Absichtlich leer" | Explizit von Entwicklern |

**Häufiger Fehler:**

```javascript
console.log("=== Beispiel 9: null vs. undefined Vergleich ===");

// Vorsicht beim Vergleich!
console.log("Lose Gleichheit (==):");
console.log("  null == undefined:", null == undefined);  // true

console.log("\nStrikte Gleichheit (===):");
console.log("  null === undefined:", null === undefined);  // false

console.log("\nPraxis-Tipp - beide prüfen:");
const result = null;
console.log("  result:", result);
console.log("  result == null:", result == null, "(prüft null UND undefined)");
console.log("  Äquivalent zu: result === null || result === undefined");

console.log("\n💡 'value == null' ist der akzeptierte Shortcut!");
console.log("--- Ende Beispiel 9 ---");
```
@eval

</section>

    --{{7}}--
Null versus undefined verwirrt Anfänger oft. Merken Sie sich: undefined ist JavaScript's Art zu sagen "da ist nichts", null ist Ihre Art zu sagen "ich will, dass da nichts ist". In Datenbank-Operationen nutzen wir oft null für fehlende Werte – das ist expliziter und besser nachvollziehbar.

### 1.3 typeof Operator

    {{7}}
<section>

**Wie finden Sie heraus, welchen Typ ein Wert hat?**

```javascript
console.log("=== Beispiel 10: typeof Operator ===");

// typeof gibt den Typ als String zurück
console.log("typeof für verschiedene Datentypen:");
console.log("  typeof 42:", typeof 42);
console.log("  typeof 'Hello':", typeof "Hello");
console.log("  typeof true:", typeof true);
console.log("  typeof undefined:", typeof undefined);
console.log("  typeof null:", typeof null, "(⚠️ Bug!)");
console.log("  typeof {}:", typeof {});
console.log("  typeof []:", typeof []);
console.log("  typeof function(){}:", typeof function(){});

console.log("\n💡 typeof ist nützlich, aber hat Quirks!");
console.log("--- Ende Beispiel 10 ---");
```
@eval

**Wichtige Quirks:**

| Expression | Ergebnis | Kommentar |
|------------|----------|-----------|
| `typeof null` | `"object"` | ⚠️ Historischer Bug, kann nicht gefixt werden |
| `typeof []` | `"object"` | Arrays sind spezielle Objekte |
| `typeof NaN` | `"number"` | Paradox: "Not a Number" ist vom Typ Number |

**Praktischer Check für Arrays:**

```javascript
console.log("=== Beispiel 11: Arrays richtig prüfen ===");

const data = [1, 2, 3];
console.log("const data = [1, 2, 3]");
console.log("\ntypeof data:", typeof data, "(nicht hilfreich für Arrays!)");
console.log("Array.isArray(data):", Array.isArray(data), "(✅ richtige Methode!)");

const notArray = { length: 3 };
console.log("\nconst notArray = { length: 3 }");
console.log("typeof notArray:", typeof notArray);
console.log("Array.isArray(notArray):", Array.isArray(notArray));

console.log("\n💡 Für Arrays: Array.isArray() nutzen, nicht typeof!");
console.log("--- Ende Beispiel 11 ---");
```
@eval

</section>

    --{{8}}--
Typeof ist nützlich, aber nicht perfekt. Der größte Stolperstein: typeof null gibt "object" zurück – ein historischer Fehler, der aus Kompatibilitätsgründen nie gefixt werden kann. Für Arrays nutzen Sie Array.isArray, nicht typeof.

### 1.4 Type Coercion & Equality

    {{8}}
<section>

**JavaScript konvertiert Typen automatisch – manchmal hilfreich, oft verwirrend!**

**Implizite Konvertierung:**

```javascript
console.log("=== Beispiel 12: Type Coercion ===");

// Zahlen + Strings
console.log("Type Coercion bei Operationen:");
console.log("  5 + '5' =", 5 + "5", "(Number → String)");
console.log("  5 - '2' =", 5 - "2", "(String → Number)");
console.log("  '10' * '2' =", "10" * "2", "(beide → Number)");

// Boolean zu Number
console.log("\nBoolean zu Number:");
console.log("  true + 1 =", true + 1, "(true → 1)");
console.log("  false + 1 =", false + 1, "(false → 0)");

// Vergleiche
console.log("\nVergleiche (lose vs. strikte Gleichheit):");
console.log("  5 == '5':", 5 == "5", "(lose, konvertiert!)");
console.log("  5 === '5':", 5 === "5", "(strikt, keine Konvertierung)");

console.log("\n⚠️  Type Coercion kann verwirrend sein!");
console.log("--- Ende Beispiel 12 ---");
```
@eval

**Zwei Arten von Gleichheit:**

| Operator | Name | Konvertiert Typen? | Empfehlung |
|----------|------|-------------------|------------|
| `==` | Lose Gleichheit | ✅ Ja | ❌ Vermeiden |
| `===` | Strikte Gleichheit | ❌ Nein | ✅ **Immer nutzen** |
| `!=` | Lose Ungleichheit | ✅ Ja | ❌ Vermeiden |
| `!==` | Strikte Ungleichheit | ❌ Nein | ✅ **Immer nutzen** |

**Warum immer `===` nutzen?**

```javascript
console.log("=== Beispiel 13: Verwirrende Fälle mit == ===");

// Verwirrende Fälle mit ==
console.log("Lose Gleichheit (==) - verwirrend:");
console.log("  0 == false:", 0 == false, "😵");
console.log("  '' == false:", "" == false, "😵");
console.log("  null == undefined:", null == undefined, "😵");
console.log("  '0' == false:", "0" == false, "😵");

// Mit === klar und vorhersagbar
console.log("\nStrikte Gleichheit (===) - vorhersagbar:");
console.log("  0 === false:", 0 === false, "✅");
console.log("  '' === false:", "" === false, "✅");
console.log("  null === undefined:", null === undefined, "✅");
console.log("  '0' === false:", "0" === false, "✅");

console.log("\n💡 Nutzen Sie IMMER === (drei Gleichheitszeichen)!");
console.log("--- Ende Beispiel 13 ---");
```
@eval

**Faustregel:**

> Nutzen Sie **immer `===` und `!==`** – außer Sie prüfen explizit auf null/undefined:

```javascript
console.log("=== Beispiel 14: Einzige Ausnahme für == ===");

const value = null;
console.log("const value = null");

// Einzige Ausnahme: Prüfung auf null/undefined
console.log("\nvalue == null:", value == null, "(prüft null UND undefined)");

console.log("\nÄquivalent zu:");
console.log("  value === null || value === undefined");

// Praktischer Test
const testValues = [null, undefined, 0, false, ""];
console.log("\nTest verschiedener Werte mit '== null':");
testValues.forEach(val => {
  console.log(`  ${String(val).padEnd(10)} == null:`, val == null);
});

console.log("\n💡 'value == null' ist der akzeptierte Shortcut!");
console.log("--- Ende Beispiel 14 ---");
```
@eval

</section>

    --{{9}}--
Type Coercion ist eine der größten Fehlerquellen in JavaScript. Die goldene Regel: Nutzen Sie immer dreifaches Gleichheitszeichen. Das macht Ihren Code vorhersagbar und vermeidet 90 Prozent der verwirrenden Bugs. Die einzige Ausnahme: Das Prüfen auf null/undefined mit doppeltem Gleichheitszeichen ist ein akzeptierter Shortcut.

### 1.5 Übung: Datentypen

    {{9}}
<section>

**Probieren Sie diese Aufgaben direkt in der Browser Console aus:**

**Aufgabe 1: Variablen deklarieren**

```javascript
// Deklarieren Sie:
// 1. Eine Konstante 'userName' mit Ihrem Namen
// 2. Eine Variable 'score', die sich ändern kann, Start: 0
// 3. Eine Konstante 'maxScore' mit Wert 100

// Ihre Lösung hier:
```
@eval

**Aufgabe 2: Datentypen erkennen**

```javascript
// Was gibt typeof zurück? Raten Sie erst, dann testen Sie:
typeof "123"
typeof 123
typeof true
typeof null
typeof undefined
typeof []
typeof {}
```
@eval

**Aufgabe 3: Vergleiche**

```javascript
// Was ist das Ergebnis? Raten Sie, dann testen Sie:
5 == "5"
5 === "5"
0 == false
0 === false
null == undefined
null === undefined
```
@eval

**Aufgabe 4: Template Literals**

```javascript
// Schreiben Sie einen String mit Template Literals:
const product = "Laptop";
const price = 999;
const stock = 5;

// Erstellen Sie: "Product: Laptop, Price: 999€, Stock: 5 units"
// Ihre Lösung hier:
```
@eval

**Aufgabe 5: Truthy/Falsy**

```javascript
// Welche dieser if-Bedingungen werden ausgeführt?
if (0) { console.log("A"); }
if ("") { console.log("B"); }
if ("0") { console.log("C"); }
if ([]) { console.log("D"); }
if (null) { console.log("E"); }
```
@eval

</section>

    --{{10}}--
Nehmen Sie sich Zeit für diese Übungen – sie sind das Fundament für alles Weitere. Wenn Sie die Lösungen nicht sofort wissen, ist das normal! Experimentieren Sie in der Console, machen Sie Fehler, beobachten Sie, was passiert. Das ist der beste Weg, JavaScript zu lernen.

    {{10}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (klicken zum Aufklappen)</summary>

```javascript
const userName = "Alice";  // const, weil Name sich nicht ändert
let score = 0;             // let, weil Score hochgezählt wird
const maxScore = 100;      // const, weil Maximum fix ist
```

</details>

<details>
<summary>Lösung Aufgabe 2</summary>

```javascript
typeof "123"      // "string"
typeof 123        // "number"
typeof true       // "boolean"
typeof null       // "object" (Bug!)
typeof undefined  // "undefined"
typeof []         // "object"
typeof {}         // "object"
```

</details>

<details>
<summary>Lösung Aufgabe 3</summary>

```javascript
5 == "5"              // true  (konvertiert String zu Number)
5 === "5"             // false (verschiedene Typen)
0 == false            // true  (0 ist falsy)
0 === false           // false (verschiedene Typen)
null == undefined     // true  (spezielle Regel)
null === undefined    // false (verschiedene Typen)
```

</details>

<details>
<summary>Lösung Aufgabe 4</summary>

```javascript
const message = `Product: ${product}, Price: ${price}€, Stock: ${stock} units`;
console.log(message);
```

</details>

<details>
<summary>Lösung Aufgabe 5</summary>

```javascript
if (0) { console.log("A"); }       // ❌ nicht ausgeführt (0 ist falsy)
if ("") { console.log("B"); }      // ❌ nicht ausgeführt ("" ist falsy)
if ("0") { console.log("C"); }     // ✅ ausgeführt (String mit Inhalt ist truthy!)
if ([]) { console.log("D"); }      // ✅ ausgeführt (leere Arrays sind truthy!)
if (null) { console.log("E"); }    // ❌ nicht ausgeführt (null ist falsy)

// Ausgabe: C, D
```

</details>

</section>

    --{{11}}--
Geschafft! Sie haben jetzt die Grundlagen von Variablen und Datentypen verstanden. Das sind die Bausteine für alles Weitere. Wenn etwas unklar ist, kommen Sie zu diesem Kapitel zurück – es ist Ihre Referenz. Bereit für Kapitel 2?

---

## Kapitel 2: Kontrollstrukturen – Entscheidungen & Wiederholungen

    --{{0}}--
Programme müssen Entscheidungen treffen und Aktionen wiederholen. Dafür gibt es Kontrollstrukturen. In Datenbank-Anwendungen nutzen Sie diese ständig: Prüfen Sie, ob ein Datensatz existiert? Iterieren Sie über Suchergebnisse? Validieren Sie Eingaben? All das sind Kontrollstrukturen. Wir zeigen Ihnen jede mit vielen console.log-Ausgaben, damit Sie den Programmfluss verstehen.

    {{0}}
<section>

**Was sind Kontrollstrukturen?**

- **Verzweigungen** (`if`, `else`, `switch`): Programme treffen Entscheidungen
- **Schleifen** (`for`, `while`, `for...of`): Programme wiederholen Aktionen
- **Sprünge** (`break`, `continue`): Programme überspringen oder beenden Iterationen

</section>

---

### 2.1 if/else/else if

    --{{0}}--
Die if-Anweisung ist die grundlegendste Kontrollstruktur. Sie prüft eine Bedingung und führt Code aus, wenn diese wahr ist. Mit else und else if können Sie Alternativen definieren. Schauen wir uns an, wie das in der Praxis funktioniert – mit vielen console.log-Ausgaben, um den Fluss zu sehen.

    {{0}}
<section>

**Grundform:**

```javascript
console.log("=== Beispiel 1: Einfaches if ===");
const age = 20;
console.log("Alter:", age);

if (age >= 18) {
  console.log("✅ Volljährig");
}
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Mit else:**

```javascript
console.log("=== Beispiel 2: if...else ===");
const stock = 0;
console.log("Lagerbestand:", stock);

if (stock > 0) {
  console.log("✅ Produkt verfügbar");
} else {
  console.log("❌ Ausverkauft");
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Mit else if (mehrere Bedingungen):**

```javascript
console.log("=== Beispiel 3: if...else if...else ===");
const score = 75;
console.log("Punktzahl:", score);

if (score >= 90) {
  console.log("🏆 Note: Sehr gut");
} else if (score >= 75) {
  console.log("👍 Note: Gut");
} else if (score >= 60) {
  console.log("✔️ Note: Befriedigend");
} else if (score >= 50) {
  console.log("⚠️ Note: Ausreichend");
} else {
  console.log("❌ Note: Nicht bestanden");
}
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Praxis-Beispiel: Datenbank-Validierung**

```javascript
console.log("=== Beispiel 4: User-Validierung ===");
const username = "alice";
const password = "1234";

console.log("Eingabe - Username:", username);
console.log("Eingabe - Password:", password);

if (!username) {
  console.log("❌ Fehler: Username fehlt");
} else if (username.length < 3) {
  console.log("❌ Fehler: Username zu kurz (min. 3 Zeichen)");
} else if (!password) {
  console.log("❌ Fehler: Password fehlt");
} else if (password.length < 8) {
  console.log("⚠️ Warnung: Schwaches Passwort (min. 8 Zeichen empfohlen)");
  console.log("✅ Login erlaubt (mit Warnung)");
} else {
  console.log("✅ Login erfolgreich");
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Verschachtelte if-Statements:**

```javascript
console.log("=== Beispiel 5: Verschachtelt ===");
const user = { name: "Bob", role: "admin", active: true };
console.log("User:", user);

if (user.active) {
  console.log("→ User ist aktiv");
  
  if (user.role === "admin") {
    console.log("  → Admin-Rechte erkannt");
    console.log("  ✅ Zugriff auf Admin-Panel gewährt");
  } else {
    console.log("  → Standard-User");
    console.log("  ✅ Zugriff auf User-Panel gewährt");
  }
} else {
  console.log("❌ User ist deaktiviert – kein Zugriff");
}
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 2.2 Ternary Operator (Kurzform)

    --{{0}}--
Der Ternary Operator ist eine kompakte Alternative zu if-else für einfache Fälle. Die Syntax lautet: Bedingung Fragezeichen Wert-wenn-wahr Doppelpunkt Wert-wenn-falsch. Sehr praktisch für Zuweisungen oder kurze Ausgaben.

    {{0}}
<section>

**Syntax: `bedingung ? wahr : falsch`**

```javascript
console.log("=== Beispiel 1: Ternary Basics ===");
const age = 16;
console.log("Alter:", age);

const status = age >= 18 ? "volljährig" : "minderjährig";
console.log("Status:", status);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Vergleich: if vs. Ternary**

```javascript
console.log("=== Beispiel 2: if vs. Ternary ===");
const stock = 5;
console.log("Lagerbestand:", stock);

// Mit if/else
let message1;
if (stock > 0) {
  message1 = "verfügbar";
} else {
  message1 = "ausverkauft";
}
console.log("if/else → Message:", message1);

// Mit Ternary (kürzer)
const message2 = stock > 0 ? "verfügbar" : "ausverkauft";
console.log("Ternary → Message:", message2);

console.log("--- Ende Beispiel 2 ---");
```
@eval

**Ternary in console.log:**

```javascript
console.log("=== Beispiel 3: Inline in console.log ===");
const price = 99;
console.log("Preis:", price);
console.log("Bewertung:", price > 100 ? "🔴 Teuer" : "🟢 Günstig");

const discount = 0;
console.log("Rabatt:", discount);
console.log("Aktion:", discount > 0 ? `${discount}% Rabatt!` : "Kein Rabatt");

console.log("--- Ende Beispiel 3 ---");
```
@eval

**Verschachtelter Ternary (⚠️ nicht übertreiben!):**

```javascript
console.log("=== Beispiel 4: Verschachtelter Ternary ===");
const score = 85;
console.log("Punktzahl:", score);

const grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
console.log("Note:", grade);

// ⚠️ Bei mehr als 2 Ebenen besser if/else nutzen!
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Datenbank-Query-Ergebnis**

```javascript
console.log("=== Beispiel 5: DB-Query simuliert ===");
const queryResult = { found: true, data: { id: 123, name: "Laptop" } };
console.log("Query-Ergebnis:", queryResult);

const product = queryResult.found 
  ? queryResult.data 
  : { id: null, name: "Nicht gefunden" };

console.log("→ Produkt:", product);
console.log("→ Name:", product.name);
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 2.3 switch/case (Optional)

    --{{0}}--
Switch-Case ist nützlich, wenn Sie einen Wert gegen viele Möglichkeiten prüfen wollen. Statt vieler else-if-Blöcke schreiben Sie switch mit case-Labels. Wichtig: Vergessen Sie nicht break, sonst läuft der Code in den nächsten Case weiter – das nennt man Fall-Through.

    {{0}}
<section>

**Syntax:**

```javascript
console.log("=== Beispiel 1: switch Basics ===");
const day = 3;
console.log("Tag-Nummer:", day);

switch (day) {
  case 1:
    console.log("→ Montag");
    break;
  case 2:
    console.log("→ Dienstag");
    break;
  case 3:
    console.log("→ Mittwoch");
    break;
  case 4:
    console.log("→ Donnerstag");
    break;
  case 5:
    console.log("→ Freitag");
    break;
  case 6:
  case 7:
    console.log("→ Wochenende! 🎉");
    break;
  default:
    console.log("→ Ungültige Eingabe");
}
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Fall-Through demonstriert:**

```javascript
console.log("=== Beispiel 2: Fall-Through (ohne break) ===");
const role = "editor";
console.log("User-Rolle:", role);

let permissions = [];
console.log("Sammle Rechte...");

switch (role) {
  case "admin":
    console.log("  → Admin-Rechte");
    permissions.push("delete");
  case "editor":
    console.log("  → Editor-Rechte");
    permissions.push("edit");
  case "viewer":
    console.log("  → Viewer-Rechte");
    permissions.push("read");
    break;
  default:
    console.log("  → Keine Rechte");
}

console.log("Finale Rechte:", permissions);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Praxis: HTTP-Status-Codes**

```javascript
console.log("=== Beispiel 3: HTTP-Status-Handler ===");
const statusCode = 404;
console.log("HTTP Status:", statusCode);

switch (statusCode) {
  case 200:
    console.log("✅ OK – Anfrage erfolgreich");
    break;
  case 201:
    console.log("✅ Created – Ressource erstellt");
    break;
  case 400:
    console.log("❌ Bad Request – Ungültige Anfrage");
    break;
  case 401:
    console.log("❌ Unauthorized – Keine Berechtigung");
    break;
  case 404:
    console.log("❌ Not Found – Ressource nicht gefunden");
    break;
  case 500:
    console.log("💥 Internal Server Error");
    break;
  default:
    console.log("⚠️ Unbekannter Status:", statusCode);
}
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Vergleich: if vs. switch**

```javascript
console.log("=== Beispiel 4: if vs. switch ===");
const dbType = "postgres";
console.log("Datenbank-Typ:", dbType);

// Mit if/else
console.log("\nMit if/else:");
if (dbType === "postgres") {
  console.log("  → PostgreSQL Port: 5432");
} else if (dbType === "mysql") {
  console.log("  → MySQL Port: 3306");
} else if (dbType === "mongodb") {
  console.log("  → MongoDB Port: 27017");
} else {
  console.log("  → Unbekannter Typ");
}

// Mit switch (übersichtlicher bei vielen Cases)
console.log("\nMit switch:");
switch (dbType) {
  case "postgres":
    console.log("  → PostgreSQL Port: 5432");
    break;
  case "mysql":
    console.log("  → MySQL Port: 3306");
    break;
  case "mongodb":
    console.log("  → MongoDB Port: 27017");
    break;
  default:
    console.log("  → Unbekannter Typ");
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

</section>

---

### 2.4 for-Schleife

    --{{0}}--
Die for-Schleife ist der Klassiker für Wiederholungen mit Zähler. Sie besteht aus drei Teilen: Initialisierung, Bedingung, Inkrement. Sehr nützlich, wenn Sie wissen, wie oft etwas wiederholt werden soll. Schauen wir uns an, wie der Zähler bei jeder Iteration fortschreitet.

    {{0}}
<section>

**Syntax: `for (init; bedingung; inkrement)`**

```javascript
console.log("=== Beispiel 1: for-Schleife Basics ===");
console.log("Zähle von 1 bis 5:");

for (let i = 1; i <= 5; i++) {
  console.log(`  Iteration ${i}`);
}
console.log("Schleife beendet");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Array durchlaufen (klassisch):**

```javascript
console.log("=== Beispiel 2: Array mit Index ===");
const products = ["Laptop", "Maus", "Tastatur", "Monitor"];
console.log("Produkte:", products);
console.log("Anzahl:", products.length);
console.log("\nDurchlaufe Array:");

for (let i = 0; i < products.length; i++) {
  console.log(`  [${i}] → ${products[i]}`);
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Rückwärts zählen:**

```javascript
console.log("=== Beispiel 3: Countdown ===");
console.log("Starte Countdown:");

for (let i = 10; i >= 1; i--) {
  console.log(`  ${i}...`);
}
console.log("🚀 Start!");
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Schrittweite ändern:**

```javascript
console.log("=== Beispiel 4: Nur gerade Zahlen ===");
console.log("Gerade Zahlen von 0 bis 20:");

for (let i = 0; i <= 20; i += 2) {
  console.log(`  ${i}`);
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Daten verarbeiten**

```javascript
console.log("=== Beispiel 5: Preis-Berechnung ===");
const prices = [19.99, 29.99, 49.99, 99.99];
console.log("Preise:", prices);

let total = 0;
console.log("\nBerechne Summe:");

for (let i = 0; i < prices.length; i++) {
  console.log(`  Produkt ${i + 1}: ${prices[i]}€`);
  total += prices[i];
  console.log(`    → Zwischensumme: ${total.toFixed(2)}€`);
}

console.log(`\n✅ Gesamtsumme: ${total.toFixed(2)}€`);
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Verschachtelte Schleifen:**

```javascript
console.log("=== Beispiel 6: Verschachtelt (Multiplikationstabelle) ===");
console.log("2x2 Tabelle:");

for (let row = 1; row <= 2; row++) {
  console.log(`\nZeile ${row}:`);
  for (let col = 1; col <= 2; col++) {
    const result = row * col;
    console.log(`  ${row} × ${col} = ${result}`);
  }
}
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 2.5 for...of-Schleife

    --{{0}}--
Die for-of-Schleife ist die moderne, elegante Art, Arrays zu durchlaufen. Sie gibt Ihnen direkt die Werte, nicht die Indices. Viel lesbarer als die klassische for-Schleife, wenn Sie keinen Index brauchen. Perfect für Datenbank-Resultate!

    {{0}}
<section>

**Syntax: `for (element of array)`**

```javascript
console.log("=== Beispiel 1: for...of Basics ===");
const fruits = ["🍎 Apfel", "🍌 Banane", "🍇 Trauben"];
console.log("Früchte:", fruits);
console.log("\nDurchlaufe mit for...of:");

for (const fruit of fruits) {
  console.log(`  → ${fruit}`);
}
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Vergleich: for vs. for...of**

```javascript
console.log("=== Beispiel 2: for vs. for...of ===");
const colors = ["rot", "grün", "blau"];
console.log("Farben:", colors);

console.log("\nMit klassischer for-Schleife:");
for (let i = 0; i < colors.length; i++) {
  console.log(`  [${i}] ${colors[i]}`);
}

console.log("\nMit for...of (einfacher!):");
for (const color of colors) {
  console.log(`  ${color}`);
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Praxis: Datenbank-Ergebnisse verarbeiten**

```javascript
console.log("=== Beispiel 3: DB-Results simuliert ===");
const users = [
  { id: 1, name: "Alice", active: true },
  { id: 2, name: "Bob", active: false },
  { id: 3, name: "Charlie", active: true }
];
console.log("Users aus Datenbank:", users);
console.log("\nVerarbeite jeden User:");

for (const user of users) {
  console.log(`\n→ User ${user.id}: ${user.name}`);
  console.log(`  Status: ${user.active ? "✅ aktiv" : "❌ inaktiv"}`);
  
  if (user.active) {
    console.log(`  Aktion: Sende Willkommens-Email an ${user.name}`);
  }
}
console.log("\n--- Ende Beispiel 3 ---");
```
@eval

**Strings durchlaufen:**

```javascript
console.log("=== Beispiel 4: String-Iteration ===");
const word = "JavaScript";
console.log("Wort:", word);
console.log("\nBuchstabe für Buchstabe:");

let position = 1;
for (const char of word) {
  console.log(`  Position ${position}: '${char}'`);
  position++;
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Summen und Aggregationen:**

```javascript
console.log("=== Beispiel 5: Aggregation ===");
const orders = [
  { id: 101, amount: 50 },
  { id: 102, amount: 120 },
  { id: 103, amount: 80 }
];
console.log("Bestellungen:", orders);
console.log("\nBerechne Statistiken:");

let totalAmount = 0;
let orderCount = 0;

for (const order of orders) {
  console.log(`  Order #${order.id}: ${order.amount}€`);
  totalAmount += order.amount;
  orderCount++;
  console.log(`    → Laufende Summe: ${totalAmount}€`);
}

const average = totalAmount / orderCount;
console.log(`\n✅ Gesamt: ${totalAmount}€`);
console.log(`✅ Durchschnitt: ${average.toFixed(2)}€`);
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 2.6 while-Schleife

    --{{0}}--
Die while-Schleife wiederholt Code, solange eine Bedingung wahr ist. Anders als for hat sie keinen eingebauten Zähler – Sie müssen selbst aufpassen, dass die Bedingung irgendwann falsch wird, sonst läuft die Schleife ewig! Gut für unbekannte Wiederholungszahlen.

    {{0}}
<section>

**Syntax: `while (bedingung)`**

```javascript
console.log("=== Beispiel 1: while Basics ===");
let count = 1;
console.log("Startwert:", count);
console.log("\nZähle bis 5:");

while (count <= 5) {
  console.log(`  Iteration ${count}`);
  count++;
}
console.log("Endwert:", count);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Vorsicht: Endlosschleife vermeiden!**

```javascript
console.log("=== Beispiel 2: Endlosschleife (VORSICHT!) ===");
console.log("⚠️ Dieses Beispiel ist deaktiviert, weil es ewig läuft:");
console.log(`
let i = 0;
while (i < 10) {
  console.log(i);
  // ❌ FEHLER: i++ fehlt → Endlosschleife!
}
`);

console.log("\n✅ Richtig mit Inkrement:");
let i = 0;
while (i < 5) {
  console.log(`  ${i}`);
  i++; // ✅ Wichtig!
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**do...while (führt mindestens 1x aus):**

```javascript
console.log("=== Beispiel 3: do...while ===");
let num = 10;
console.log("Startwert:", num);
console.log("\ndo...while läuft MINDESTENS 1x:");

do {
  console.log(`  num ist ${num}`);
  num--;
} while (num > 8);

console.log("Endwert:", num);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Praxis: Verarbeitung bis Bedingung erfüllt**

```javascript
console.log("=== Beispiel 4: Queue-Processing simuliert ===");
const queue = ["Task 1", "Task 2", "Task 3", "Task 4"];
console.log("Queue:", queue);
console.log("Verarbeite Tasks:");

while (queue.length > 0) {
  const task = queue.shift(); // Entfernt erstes Element
  console.log(`  → Verarbeite: ${task}`);
  console.log(`    Verbleibend: ${queue.length} Tasks`);
}

console.log("✅ Queue leer!");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Paginierung simuliert**

```javascript
console.log("=== Beispiel 5: Pagination ===");
let currentPage = 1;
const totalPages = 4;
const results = [];

console.log(`Lade Daten von Seite 1 bis ${totalPages}:`);

while (currentPage <= totalPages) {
  console.log(`\n→ Lade Seite ${currentPage}...`);
  const pageData = `Daten-Seite-${currentPage}`;
  results.push(pageData);
  console.log(`  ✅ Geladen: ${pageData}`);
  console.log(`  Fortschritt: ${currentPage}/${totalPages}`);
  currentPage++;
}

console.log("\n✅ Alle Seiten geladen!");
console.log("Ergebnis:", results);
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 2.7 break & continue

    --{{0}}--
Break und continue sind Kontrollbefehle innerhalb von Schleifen. Break bricht die Schleife komplett ab. Continue überspringt nur die aktuelle Iteration und macht mit der nächsten weiter. Sehr nützlich für vorzeitige Abbrüche oder Filter-Logik.

    {{0}}
<section>

**break: Schleife abbrechen**

```javascript
console.log("=== Beispiel 1: break ===");
console.log("Suche Zahl 7 im Array:");
const numbers = [2, 5, 7, 9, 12, 15];
console.log("Array:", numbers);

for (const num of numbers) {
  console.log(`  Prüfe: ${num}`);
  
  if (num === 7) {
    console.log(`  ✅ Gefunden! Breche ab.`);
    break; // Stoppt die Schleife hier
  }
}
console.log("Nach der Schleife");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**continue: Iteration überspringen**

```javascript
console.log("=== Beispiel 2: continue ===");
console.log("Gebe nur gerade Zahlen aus:");

for (let i = 1; i <= 10; i++) {
  console.log(`  Prüfe: ${i}`);
  
  if (i % 2 !== 0) {
    console.log(`    → Ungerade, überspringe`);
    continue; // Springt zur nächsten Iteration
  }
  
  console.log(`    ✅ Gerade: ${i}`);
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Praxis: User-Validierung mit continue**

```javascript
console.log("=== Beispiel 3: Validierung mit continue ===");
const users = [
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob", email: "" },
  { name: "", email: "charlie@example.com" },
  { name: "David", email: "david@example.com" }
];
console.log("Users:", users);
console.log("\nValidiere Users:");

const validUsers = [];

for (const user of users) {
  console.log(`\n→ Prüfe User: ${user.name || "(leer)"}`);
  
  if (!user.name) {
    console.log(`  ❌ Name fehlt – überspringe`);
    continue;
  }
  
  if (!user.email) {
    console.log(`  ❌ Email fehlt – überspringe`);
    continue;
  }
  
  console.log(`  ✅ Valid!`);
  validUsers.push(user);
}

console.log("\n✅ Valide Users:", validUsers);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Praxis: Suche mit break**

```javascript
console.log("=== Beispiel 4: Produkt-Suche ===");
const products = [
  { id: 1, name: "Laptop", price: 999 },
  { id: 2, name: "Maus", price: 29 },
  { id: 3, name: "Tastatur", price: 79 }
];
console.log("Produkte:", products);

const searchId = 2;
console.log(`\nSuche Produkt mit ID ${searchId}:`);

let found = null;

for (const product of products) {
  console.log(`  Prüfe: ${product.name} (ID: ${product.id})`);
  
  if (product.id === searchId) {
    console.log(`  ✅ Gefunden!`);
    found = product;
    break; // Schleife beenden
  }
}

if (found) {
  console.log(`\nErgebnis:`, found);
} else {
  console.log(`\n❌ Produkt nicht gefunden`);
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Kombination: break & continue**

```javascript
console.log("=== Beispiel 5: break & continue kombiniert ===");
console.log("Summiere Zahlen, aber:");
console.log("  - Überspringe negative Zahlen");
console.log("  - Stoppe bei Summe > 50\n");

const values = [10, -5, 20, 15, -3, 30, 10];
console.log("Werte:", values);

let sum = 0;

for (const value of values) {
  console.log(`\n→ Aktueller Wert: ${value}`);
  
  if (value < 0) {
    console.log(`  ⚠️ Negativ – überspringe (continue)`);
    continue;
  }
  
  sum += value;
  console.log(`  Addiere: ${value}`);
  console.log(`  → Neue Summe: ${sum}`);
  
  if (sum > 50) {
    console.log(`  🛑 Summe > 50 erreicht – breche ab (break)`);
    break;
  }
}

console.log(`\n✅ Finale Summe: ${sum}`);
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 2.8 Übung: Kontrollstrukturen

    --{{0}}--
Jetzt sind Sie dran! Diese Übungen testen Ihr Verständnis von if, Schleifen, break und continue. Nutzen Sie console.log ausgiebig, um zu sehen, was passiert.

    {{0}}
<section>

**Aufgabe 1: FizzBuzz (Klassiker!)**

```javascript
// Schreiben Sie eine for-Schleife von 1 bis 15:
// - Bei Zahlen teilbar durch 3: geben Sie "Fizz" aus
// - Bei Zahlen teilbar durch 5: geben Sie "Buzz" aus
// - Bei Zahlen teilbar durch 3 UND 5: geben Sie "FizzBuzz" aus
// - Sonst: geben Sie die Zahl aus

// Ihr Code hier:
console.log("=== FizzBuzz ===");
```
@eval

**Aufgabe 2: Array filtern**

```javascript
// Gegeben ist dieses Array:
const numbers = [5, 12, 8, 21, 3, 17, 14, 9];

// Durchlaufen Sie es mit for...of und:
// - Überspringen Sie (continue) alle ungeraden Zahlen
// - Geben Sie gerade Zahlen aus
// - Brechen Sie ab (break), wenn Sie eine Zahl > 15 finden

console.log("=== Filter Array ===");
console.log("Input:", numbers);
// Ihr Code hier:
```
@eval

**Aufgabe 3: Login-Validierung**

```javascript
// Schreiben Sie eine Funktion, die Username und Password prüft:
// - Username: min. 3 Zeichen, darf nicht leer sein
// - Password: min. 6 Zeichen, darf nicht leer sein
// Nutzen Sie if/else und console.log für Feedback

console.log("=== Login-Validator ===");
const testUser = "ab";
const testPass = "12345";

console.log("Test:", testUser, testPass);
// Ihr Code hier:
```
@eval

**Aufgabe 4: Summe bis Schwellwert**

```javascript
// Gegeben:
const values = [10, 20, 15, 30, 5, 40];
const threshold = 50;

// Aufgabe:
// - Summieren Sie die Werte mit einer Schleife
// - Geben Sie bei jedem Schritt die Zwischensumme aus
// - Brechen Sie ab, sobald die Summe >= threshold ist

console.log("=== Summe mit Schwellwert ===");
console.log("Values:", values);
console.log("Threshold:", threshold);
// Ihr Code hier:
```
@eval

**Aufgabe 5: Status-Mapper**

```javascript
// Gegeben sind Bestellstatus-Codes:
const statuses = [1, 2, 3, 4, 99];

// Schreiben Sie eine for...of-Schleife mit switch:
// 1 → "Bestellt"
// 2 → "In Bearbeitung"
// 3 → "Versandt"
// 4 → "Geliefert"
// default → "Unbekannter Status"

console.log("=== Status-Mapper ===");
console.log("Codes:", statuses);
// Ihr Code hier:
```
@eval

</section>

    --{{1}}--
Diese Übungen kombinieren alles aus Kapitel zwei. Experimentieren Sie! Wenn etwas nicht funktioniert, lesen Sie die Fehlermeldung und versuchen Sie zu verstehen, was schief ging. Fehler sind Ihre besten Lehrer.

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (FizzBuzz)</summary>

```javascript
console.log("=== FizzBuzz ===");

for (let i = 1; i <= 15; i++) {
  console.log(`\nPrüfe: ${i}`);
  
  if (i % 3 === 0 && i % 5 === 0) {
    console.log("  → FizzBuzz");
  } else if (i % 3 === 0) {
    console.log("  → Fizz");
  } else if (i % 5 === 0) {
    console.log("  → Buzz");
  } else {
    console.log(`  → ${i}`);
  }
}
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Array filtern)</summary>

```javascript
console.log("=== Filter Array ===");
const numbers = [5, 12, 8, 21, 3, 17, 14, 9];
console.log("Input:", numbers);

for (const num of numbers) {
  console.log(`\nPrüfe: ${num}`);
  
  if (num % 2 !== 0) {
    console.log("  → Ungerade, überspringe");
    continue;
  }
  
  console.log(`  ✅ Gerade: ${num}`);
  
  if (num > 15) {
    console.log("  🛑 Zahl > 15 gefunden, breche ab");
    break;
  }
}
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Login-Validierung)</summary>

```javascript
console.log("=== Login-Validator ===");
const testUser = "ab";
const testPass = "12345";

console.log("Test:", testUser, testPass);
console.log("\nValidierung:");

if (!testUser) {
  console.log("❌ Username fehlt");
} else if (testUser.length < 3) {
  console.log("❌ Username zu kurz (min. 3 Zeichen)");
  console.log(`   Aktuell: ${testUser.length} Zeichen`);
} else if (!testPass) {
  console.log("❌ Password fehlt");
} else if (testPass.length < 6) {
  console.log("❌ Password zu kurz (min. 6 Zeichen)");
  console.log(`   Aktuell: ${testPass.length} Zeichen`);
} else {
  console.log("✅ Login erfolgreich!");
}
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 4 (Summe bis Schwellwert)</summary>

```javascript
console.log("=== Summe mit Schwellwert ===");
const values = [10, 20, 15, 30, 5, 40];
const threshold = 50;

console.log("Values:", values);
console.log("Threshold:", threshold);
console.log("\nBerechnung:");

let sum = 0;

for (const value of values) {
  console.log(`\n→ Aktueller Wert: ${value}`);
  sum += value;
  console.log(`  Zwischensumme: ${sum}`);
  
  if (sum >= threshold) {
    console.log(`  ✅ Schwellwert erreicht! (${sum} >= ${threshold})`);
    break;
  }
}

console.log(`\nFinale Summe: ${sum}`);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 5 (Status-Mapper)</summary>

```javascript
console.log("=== Status-Mapper ===");
const statuses = [1, 2, 3, 4, 99];
console.log("Codes:", statuses);
console.log("\nMapping:");

for (const code of statuses) {
  console.log(`\nCode ${code}:`);
  
  switch (code) {
    case 1:
      console.log("  → Bestellt");
      break;
    case 2:
      console.log("  → In Bearbeitung");
      break;
    case 3:
      console.log("  → Versandt");
      break;
    case 4:
      console.log("  → Geliefert");
      break;
    default:
      console.log("  → Unbekannter Status");
  }
}
```
@eval

</details>

</section>

    --{{2}}--
Hervorragend! Sie haben jetzt ein solides Verständnis von Kontrollstrukturen. if-else für Entscheidungen, for und for-of für Schleifen, break und continue für Steuerung. Das sind die Werkzeuge, mit denen Sie komplexe Logik bauen. Bereit für Kapitel drei: Funktionen?

---

## Kapitel 3: Funktionen – Wiederverwendbarer Code

    --{{0}}--
Funktionen sind das Herzstück jeder Programmiersprache. Sie kapseln Logik und machen Code wiederverwendbar. Stellen Sie sich vor, Sie müssen dieselbe Berechnung an zehn Stellen durchführen – mit Funktionen schreiben Sie den Code nur einmal und rufen ihn auf. In Datenbank-Anwendungen nutzen Sie Funktionen ständig: Daten laden, validieren, transformieren, speichern. Alles sind Funktionen. Lernen wir die verschiedenen Arten kennen.

    {{0}}
<section>

**Was sind Funktionen?**

- **Wiederverwendbar**: Code einmal schreiben, oft aufrufen
- **Parameter**: Funktionen akzeptieren Eingaben
- **Return**: Funktionen geben Ergebnisse zurück
- **Drei Schreibweisen**: Declaration, Expression, Arrow Function

</section>

---

### 3.1 Function Declaration

    --{{0}}--
Die klassische Funktionsdeklaration. Sie beginnt mit dem Keyword function, gefolgt vom Namen, Parametern in Klammern und dem Funktionskörper in geschweiften Klammern. Diese Funktionen werden "gehoisted", das heißt, Sie können sie aufrufen, bevor sie definiert sind.

    {{0}}
<section>

**Syntax: `function name(parameter) { ... }`**

```javascript
console.log("=== Beispiel 1: Einfache Funktion ===");

function greet() {
  console.log("  → Hallo aus der Funktion!");
}

console.log("Vor dem Aufruf");
greet(); // Funktion aufrufen
console.log("Nach dem Aufruf");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Mit Parameter:**

```javascript
console.log("=== Beispiel 2: Funktion mit Parameter ===");

function greetUser(name) {
  console.log(`  → Hallo, ${name}!`);
}

console.log("Rufe Funktion mit verschiedenen Namen auf:");
greetUser("Alice");
greetUser("Bob");
greetUser("Charlie");
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Mit mehreren Parametern:**

```javascript
console.log("=== Beispiel 3: Mehrere Parameter ===");

function calculatePrice(basePrice, taxRate) {
  console.log(`  Input: Basispreis=${basePrice}, Steuer=${taxRate}`);
  const totalPrice = basePrice + (basePrice * taxRate);
  console.log(`  Berechnung: ${basePrice} + (${basePrice} × ${taxRate}) = ${totalPrice}`);
  console.log(`  Ergebnis: ${totalPrice.toFixed(2)}€`);
}

console.log("\nBerechne Preise:");
calculatePrice(100, 0.19);
console.log();
calculatePrice(50, 0.07);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Hoisting demonstriert:**

```javascript
console.log("=== Beispiel 4: Hoisting ===");

console.log("Rufe Funktion auf, BEVOR sie definiert ist:");
sayHello(); // ✅ Funktioniert wegen Hoisting!

function sayHello() {
  console.log("  → Hello from hoisted function!");
}

console.log("Jetzt ist die Funktion definiert");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Datenbank-Helper**

```javascript
console.log("=== Beispiel 5: DB-Helper ===");

function logQuery(operation, table, id) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}]`);
  console.log(`  Operation: ${operation}`);
  console.log(`  Table: ${table}`);
  console.log(`  ID: ${id || "N/A"}`);
}

console.log("Simuliere DB-Operationen:");
logQuery("SELECT", "users", 123);
console.log();
logQuery("INSERT", "products", null);
console.log();
logQuery("DELETE", "orders", 456);
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 3.2 Function Expression

    --{{0}}--
Bei einer Function Expression weisen Sie eine Funktion einer Variable zu. Der Unterschied: Diese Funktionen werden NICHT gehoisted, Sie können sie also erst nach der Definition aufrufen. Oft sehen Sie diese Form bei Callbacks oder wenn Funktionen dynamisch zugewiesen werden.

    {{0}}
<section>

**Syntax: `const name = function(parameter) { ... };`**

```javascript
console.log("=== Beispiel 1: Function Expression Basics ===");

const sayGoodbye = function() {
  console.log("  → Auf Wiedersehen!");
};

console.log("Funktion definiert");
sayGoodbye(); // Jetzt aufrufen
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Kein Hoisting:**

```javascript
console.log("=== Beispiel 2: Kein Hoisting ===");

console.log("Versuche Funktion vor Definition aufzurufen:");

try {
  testFunction(); // ❌ Fehler!
} catch (error) {
  console.log("  ❌ Fehler:", error.message);
}

const testFunction = function() {
  console.log("  → Diese Nachricht sehen Sie nicht");
};

console.log("\nJetzt ist die Funktion definiert:");
testFunction(); // ✅ Jetzt funktioniert es
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Mit Parametern:**

```javascript
console.log("=== Beispiel 3: Mit Parametern ===");

const multiply = function(a, b) {
  console.log(`  Multipliziere: ${a} × ${b}`);
  const result = a * b;
  console.log(`  Ergebnis: ${result}`);
  return result;
};

console.log("Berechne Produkte:");
const r1 = multiply(5, 3);
console.log(`Rückgabewert: ${r1}`);
console.log();
const r2 = multiply(10, 7);
console.log(`Rückgabewert: ${r2}`);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Anonyme Funktionen (häufig bei Callbacks):**

```javascript
console.log("=== Beispiel 4: Anonyme Funktion als Callback ===");

const numbers = [1, 2, 3, 4, 5];
console.log("Array:", numbers);
console.log("\nVerdopple jede Zahl:");

const doubled = numbers.map(function(num) {
  console.log(`  ${num} → ${num * 2}`);
  return num * 2;
});

console.log("\nErgebnis:", doubled);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Validator-Funktion**

```javascript
console.log("=== Beispiel 5: Email-Validator ===");

const validateEmail = function(email) {
  console.log(`\nValidiere: "${email}"`);
  
  if (!email) {
    console.log("  ❌ Email fehlt");
    return false;
  }
  
  if (!email.includes("@")) {
    console.log("  ❌ Kein @ gefunden");
    return false;
  }
  
  if (!email.includes(".")) {
    console.log("  ❌ Kein Punkt gefunden");
    return false;
  }
  
  console.log("  ✅ Email valide");
  return true;
};

const testEmails = ["user@example.com", "invalid", "test@", "@test.com"];
console.log("Test-Emails:", testEmails);

for (const email of testEmails) {
  const isValid = validateEmail(email);
  console.log(`  → Return: ${isValid}`);
}
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 3.3 Arrow Functions (=>)

    --{{0}}--
Arrow Functions sind die moderne, kompakte Schreibweise seit ES6. Statt function schreiben Sie einen Pfeil. Sie sind kürzer und haben ein spezielles Verhalten bei "this" – dazu später mehr. In der Praxis sehen Sie Arrow Functions überall, besonders bei Array-Methoden und Callbacks.

    {{0}}
<section>

**Syntax: `(parameter) => { ... }` oder `parameter => ...`**

```javascript
console.log("=== Beispiel 1: Arrow Function Basics ===");

const greet = () => {
  console.log("  → Hallo aus Arrow Function!");
};

console.log("Rufe Arrow Function auf:");
greet();
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Mit einem Parameter (Klammern optional):**

```javascript
console.log("=== Beispiel 2: Ein Parameter ===");

// Mit Klammern
const double1 = (x) => {
  console.log(`  Input: ${x}`);
  return x * 2;
};

// Ohne Klammern (bei genau 1 Parameter erlaubt)
const double2 = x => {
  console.log(`  Input: ${x}`);
  return x * 2;
};

console.log("Mit Klammern:");
console.log("Ergebnis:", double1(5));
console.log("\nOhne Klammern:");
console.log("Ergebnis:", double2(5));
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Implizites Return (ohne Klammern):**

```javascript
console.log("=== Beispiel 3: Implizites Return ===");

// Mit explizitem return
const add1 = (a, b) => {
  return a + b;
};

// Ohne Klammern = implizites return (kürzer!)
const add2 = (a, b) => a + b;

console.log("Mit explizitem return:");
console.log("  5 + 3 =", add1(5, 3));
console.log("\nMit implizitem return:");
console.log("  5 + 3 =", add2(5, 3));
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Vergleich: Alle drei Schreibweisen**

```javascript
console.log("=== Beispiel 4: Vergleich aller Schreibweisen ===");

// 1. Function Declaration
function square1(x) {
  return x * x;
}

// 2. Function Expression
const square2 = function(x) {
  return x * x;
};

// 3. Arrow Function
const square3 = x => x * x;

console.log("Berechne 7²:");
console.log("  Declaration:", square1(7));
console.log("  Expression:", square2(7));
console.log("  Arrow:", square3(7));
console.log("Alle liefern dasselbe Ergebnis!");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Array-Methoden mit Arrow Functions**

```javascript
console.log("=== Beispiel 5: Array-Methoden ===");

const products = [
  { name: "Laptop", price: 999 },
  { name: "Maus", price: 29 },
  { name: "Tastatur", price: 79 }
];

console.log("Produkte:", products);

// filter: Nur Produkte > 50€
console.log("\nFilter (Preis > 50€):");
const expensive = products.filter(p => {
  console.log(`  Prüfe: ${p.name} (${p.price}€)`);
  return p.price > 50;
});
console.log("Ergebnis:", expensive);

// map: Nur Namen extrahieren
console.log("\nMap (Namen):");
const names = products.map(p => {
  console.log(`  Extrahiere: ${p.name}`);
  return p.name;
});
console.log("Ergebnis:", names);

// forEach: Ausgabe
console.log("\nforEach (Ausgabe):");
products.forEach(p => {
  console.log(`  → ${p.name}: ${p.price}€`);
});

console.log("--- Ende Beispiel 5 ---");
```
@eval

**Mehrzeilige Arrow Functions:**

```javascript
console.log("=== Beispiel 6: Mehrzeilig ===");

const processOrder = (orderId, amount) => {
  console.log(`\n→ Verarbeite Bestellung #${orderId}`);
  console.log(`  Betrag: ${amount}€`);
  
  if (amount > 100) {
    console.log("  🎁 Gratisversand!");
  }
  
  const tax = amount * 0.19;
  console.log(`  Steuer: ${tax.toFixed(2)}€`);
  
  const total = amount + tax;
  console.log(`  Gesamt: ${total.toFixed(2)}€`);
  
  return total;
};

console.log("Verarbeite Bestellungen:");
processOrder(101, 150);
processOrder(102, 50);
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 3.4 Parameter & Default Values

    --{{0}}--
Funktionen können Parameter haben – Eingabewerte, die Sie beim Aufruf übergeben. Seit ES6 können Sie Default-Werte definieren, die verwendet werden, wenn kein Argument übergeben wird. Das macht Funktionen flexibler und verhindert undefined-Fehler.

    {{0}}
<section>

**Grundlagen:**

```javascript
console.log("=== Beispiel 1: Parameter Basics ===");

const greet = (name, greeting) => {
  console.log(`  ${greeting}, ${name}!`);
};

console.log("Mit allen Parametern:");
greet("Alice", "Hallo");

console.log("\nMit fehlenden Parametern:");
greet("Bob"); // greeting ist undefined
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Default Values (ES6):**

```javascript
console.log("=== Beispiel 2: Default Values ===");

const greet = (name = "Gast", greeting = "Hallo") => {
  console.log(`  ${greeting}, ${name}!`);
};

console.log("Mit allen Parametern:");
greet("Alice", "Guten Tag");

console.log("\nNur 1 Parameter:");
greet("Bob"); // greeting = "Hallo" (default)

console.log("\nKeine Parameter:");
greet(); // name = "Gast", greeting = "Hallo" (defaults)

console.log("--- Ende Beispiel 2 ---");
```
@eval

**Default Values mit Berechnungen:**

```javascript
console.log("=== Beispiel 3: Berechnete Defaults ===");

const createUser = (name, role = "user", createdAt = new Date().toISOString()) => {
  console.log("\nErstelle User:");
  console.log(`  Name: ${name}`);
  console.log(`  Role: ${role}`);
  console.log(`  Created: ${createdAt}`);
  return { name, role, createdAt };
};

console.log("Alle Werte explizit:");
createUser("Alice", "admin", "2025-01-01T00:00:00Z");

console.log("\n\nMit Defaults:");
createUser("Bob"); // role und createdAt werden generiert

console.log("--- Ende Beispiel 3 ---");
```
@eval

**Rest Parameter (`...args`):**

```javascript
console.log("=== Beispiel 4: Rest Parameter ===");

const sum = (...numbers) => {
  console.log("  Erhaltene Argumente:", numbers);
  console.log("  Typ:", Array.isArray(numbers) ? "Array" : "kein Array");
  
  let total = 0;
  for (const num of numbers) {
    console.log(`    Addiere: ${num}`);
    total += num;
  }
  
  console.log(`  Summe: ${total}`);
  return total;
};

console.log("Mit 3 Zahlen:");
sum(10, 20, 30);

console.log("\nMit 5 Zahlen:");
sum(1, 2, 3, 4, 5);

console.log("\nMit 1 Zahl:");
sum(100);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Flexible Query-Builder**

```javascript
console.log("=== Beispiel 5: Query Builder ===");

const buildQuery = (table, options = {}) => {
  console.log(`\n→ Baue Query für Tabelle: ${table}`);
  console.log("  Options:", options);
  
  const limit = options.limit || 10;
  const offset = options.offset || 0;
  const orderBy = options.orderBy || "id";
  
  const query = `SELECT * FROM ${table} ORDER BY ${orderBy} LIMIT ${limit} OFFSET ${offset}`;
  console.log(`  ✅ Query: ${query}`);
  return query;
};

console.log("Ohne Options:");
buildQuery("users");

console.log("\n\nMit Options:");
buildQuery("products", { limit: 20, orderBy: "price" });

console.log("\n\nMit teilweisen Options:");
buildQuery("orders", { offset: 100 });
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Destructuring in Parametern:**

```javascript
console.log("=== Beispiel 6: Destructuring ===");

// Statt: function(user) { user.name, user.email }
// Schreiben: function({ name, email })

const displayUser = ({ name, email, role = "user" }) => {
  console.log("\n→ User-Info:");
  console.log(`  Name: ${name}`);
  console.log(`  Email: ${email}`);
  console.log(`  Role: ${role}`);
};

const user1 = { name: "Alice", email: "alice@example.com", role: "admin" };
const user2 = { name: "Bob", email: "bob@example.com" };

console.log("User 1:");
displayUser(user1);

console.log("\nUser 2 (ohne role):");
displayUser(user2); // role = "user" (default)
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 3.5 Return Values

    --{{0}}--
Funktionen können Werte zurückgeben mit dem return-Keyword. Das Ergebnis können Sie in einer Variable speichern oder direkt weiterverwenden. Ohne return gibt eine Funktion undefined zurück. Return stoppt die Funktion sofort – Code danach wird nicht mehr ausgeführt.

    {{0}}
<section>

**Einfaches Return:**

```javascript
console.log("=== Beispiel 1: Return Basics ===");

const add = (a, b) => {
  console.log(`  Berechne: ${a} + ${b}`);
  const result = a + b;
  console.log(`  Ergebnis: ${result}`);
  return result;
};

console.log("Rufe Funktion auf:");
const sum = add(5, 3);
console.log("Rückgabewert:", sum);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Ohne Return = undefined:**

```javascript
console.log("=== Beispiel 2: Ohne Return ===");

const logMessage = (msg) => {
  console.log(`  → ${msg}`);
  // Kein return!
};

console.log("Rufe Funktion auf:");
const result = logMessage("Hallo");
console.log("Rückgabewert:", result); // undefined
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Frühes Return (Guard Clauses):**

```javascript
console.log("=== Beispiel 3: Frühes Return ===");

const divide = (a, b) => {
  console.log(`\nTeile: ${a} ÷ ${b}`);
  
  if (b === 0) {
    console.log("  ❌ Division durch Null!");
    return null; // Früher Abbruch
  }
  
  // Dieser Code wird nur ausgeführt, wenn b !== 0
  const result = a / b;
  console.log(`  ✅ Ergebnis: ${result}`);
  return result;
};

console.log("Test 1:");
const r1 = divide(10, 2);
console.log("Return:", r1);

console.log("\nTest 2 (Division durch 0):");
const r2 = divide(10, 0);
console.log("Return:", r2);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Return-Objekte:**

```javascript
console.log("=== Beispiel 4: Objekte zurückgeben ===");

const calculateStats = (numbers) => {
  console.log("\nBerechne Statistiken für:", numbers);
  
  const sum = numbers.reduce((acc, num) => acc + num, 0);
  console.log(`  Summe: ${sum}`);
  
  const average = sum / numbers.length;
  console.log(`  Durchschnitt: ${average.toFixed(2)}`);
  
  const min = Math.min(...numbers);
  const max = Math.max(...numbers);
  console.log(`  Min: ${min}, Max: ${max}`);
  
  return { sum, average, min, max }; // Objekt zurückgeben
};

const data = [10, 20, 30, 40, 50];
const stats = calculateStats(data);
console.log("\nRückgabe-Objekt:", stats);
console.log("Zugriff auf average:", stats.average);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Validierung mit Boolean-Return**

```javascript
console.log("=== Beispiel 5: Boolean-Return ===");

const isValidProduct = (product) => {
  console.log(`\nValidiere Produkt:`, product);
  
  if (!product.name) {
    console.log("  ❌ Name fehlt");
    return false;
  }
  
  if (!product.price || product.price <= 0) {
    console.log("  ❌ Ungültiger Preis");
    return false;
  }
  
  if (product.stock < 0) {
    console.log("  ❌ Negativer Lagerbestand");
    return false;
  }
  
  console.log("  ✅ Produkt valide");
  return true;
};

const products = [
  { name: "Laptop", price: 999, stock: 5 },
  { name: "", price: 50, stock: 10 },
  { name: "Maus", price: -10, stock: 20 },
  { name: "Tastatur", price: 79, stock: 0 }
];

console.log("Validiere Produkte:");
products.forEach((product, index) => {
  console.log(`\n→ Produkt ${index + 1}:`);
  const valid = isValidProduct(product);
  console.log(`  Return: ${valid}`);
});
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Multiple Returns (verschiedene Ergebnisse):**

```javascript
console.log("=== Beispiel 6: Multiple Returns ===");

const getUserStatus = (user) => {
  console.log(`\nPrüfe User:`, user);
  
  if (!user) {
    console.log("  → User ist null/undefined");
    return "unknown";
  }
  
  if (!user.active) {
    console.log("  → User ist inaktiv");
    return "inactive";
  }
  
  if (user.role === "admin") {
    console.log("  → User ist Admin");
    return "admin";
  }
  
  console.log("  → Standard-User");
  return "user";
};

const users = [
  { name: "Alice", active: true, role: "admin" },
  { name: "Bob", active: false, role: "user" },
  { name: "Charlie", active: true, role: "user" },
  null
];

users.forEach((user, index) => {
  const status = getUserStatus(user);
  console.log(`  ✅ Status: "${status}"\n`);
});
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 3.6 Scope & Closures (Kurzüberblick)

    --{{0}}--
Scope bestimmt, wo Variablen sichtbar sind. Es gibt Global Scope – überall sichtbar – und Function Scope – nur innerhalb der Funktion. Closures sind ein fortgeschrittenes Konzept: Eine innere Funktion "erinnert" sich an Variablen aus der äußeren Funktion, selbst wenn die äußere Funktion schon fertig ist. Klingt kompliziert, ist aber sehr mächtig.

    {{0}}
<section>

**Global vs. Function Scope:**

```javascript
console.log("=== Beispiel 1: Scope Basics ===");

const globalVar = "Ich bin global";
console.log("Global Scope:", globalVar);

function testScope() {
  const localVar = "Ich bin lokal";
  console.log("  Inside Function:");
  console.log("    globalVar:", globalVar); // ✅ Zugriff auf global
  console.log("    localVar:", localVar);   // ✅ Zugriff auf local
}

testScope();

console.log("\nOutside Function:");
console.log("  globalVar:", globalVar); // ✅ Funktioniert
// console.log("  localVar:", localVar); // ❌ Error! localVar existiert hier nicht
console.log("  localVar: (nicht zugänglich von außen)");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Block Scope (let/const):**

```javascript
console.log("=== Beispiel 2: Block Scope ===");

console.log("Vor dem if-Block:");
const x = "außen";
console.log("  x =", x);

if (true) {
  console.log("\nInside if-Block:");
  const x = "innen"; // Neue Variable!
  console.log("  x =", x);
  
  const y = "nur im Block";
  console.log("  y =", y);
}

console.log("\nNach dem if-Block:");
console.log("  x =", x); // "außen" (äußeres x)
// console.log("  y =", y); // ❌ Error! y existiert nur im Block
console.log("  y: (nicht zugänglich)");
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Closure: Innere Funktion erinnert sich:**

```javascript
console.log("=== Beispiel 3: Closure ===");

function createCounter() {
  console.log("→ createCounter() wird ausgeführt");
  let count = 0; // Private Variable
  
  console.log("  Erstelle innere Funktion");
  
  return function() {
    count++; // Zugriff auf äußere Variable!
    console.log(`    Counter: ${count}`);
    return count;
  };
}

console.log("\nErstelle Counter 1:");
const counter1 = createCounter();
console.log("\nRufe Counter 1 auf:");
counter1(); // 1
counter1(); // 2
counter1(); // 3

console.log("\nErstelle Counter 2:");
const counter2 = createCounter();
console.log("\nRufe Counter 2 auf:");
counter2(); // 1 (eigener count!)
counter2(); // 2

console.log("\nJeder Counter hat seinen eigenen count!");
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Praxis: Private Variablen simulieren:**

```javascript
console.log("=== Beispiel 4: Private Variablen ===");

const createWallet = (initialBalance) => {
  console.log(`\n→ Erstelle Wallet mit ${initialBalance}€`);
  let balance = initialBalance; // Private!
  
  return {
    deposit: (amount) => {
      console.log(`  → Einzahlung: ${amount}€`);
      balance += amount;
      console.log(`    Neuer Stand: ${balance}€`);
    },
    
    withdraw: (amount) => {
      console.log(`  → Auszahlung: ${amount}€`);
      if (amount > balance) {
        console.log(`    ❌ Nicht genug Guthaben (${balance}€)`);
        return false;
      }
      balance -= amount;
      console.log(`    Neuer Stand: ${balance}€`);
      return true;
    },
    
    getBalance: () => {
      console.log(`  → Kontostand: ${balance}€`);
      return balance;
    }
  };
};

console.log("Erstelle Wallet:");
const myWallet = createWallet(100);

console.log("\nOperationen:");
myWallet.deposit(50);
myWallet.withdraw(30);
myWallet.withdraw(200); // Fehlschlag
myWallet.getBalance();

console.log("\n⚠️ balance ist nicht direkt zugänglich:");
console.log("myWallet.balance =", myWallet.balance); // undefined
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Closure in Schleifen (häufiger Fehler!):**

```javascript
console.log("=== Beispiel 5: Closure in Schleifen ===");

console.log("❌ Falsch mit var:");
const functions1 = [];
for (var i = 0; i < 3; i++) {
  functions1.push(function() {
    console.log(`  Wert: ${i}`);
  });
}
console.log("Rufe Funktionen auf:");
functions1[0](); // 3 (nicht 0!)
functions1[1](); // 3 (nicht 1!)
functions1[2](); // 3 (nicht 2!)
console.log("Alle zeigen 3, weil var function-scoped ist\n");

console.log("✅ Richtig mit let:");
const functions2 = [];
for (let j = 0; j < 3; j++) {
  functions2.push(function() {
    console.log(`  Wert: ${j}`);
  });
}
console.log("Rufe Funktionen auf:");
functions2[0](); // 0 ✅
functions2[1](); // 1 ✅
functions2[2](); // 2 ✅
console.log("let erzeugt für jede Iteration eigenen Scope");
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 3.7 Übung: Funktionen

    --{{0}}--
Zeit, Ihr Wissen zu testen! Diese Übungen kombinieren alle Funktionstypen, Parameter, Return-Values und sogar Closures. Nutzen Sie console.log, um Ihre Lösungen zu debuggen.

    {{0}}
<section>

**Aufgabe 1: Temperatur-Konverter**

```javascript
// Schreiben Sie eine Arrow Function, die Celsius in Fahrenheit umrechnet
// Formel: F = C × 9/5 + 32
// Geben Sie Eingabe und Ergebnis mit console.log aus

console.log("=== Temperatur-Konverter ===");
// Ihr Code hier:
// const celsiusToFahrenheit = ...

// Test:
// celsiusToFahrenheit(0);    // 32°F
// celsiusToFahrenheit(100);  // 212°F
// celsiusToFahrenheit(37);   // 98.6°F
```
@eval

**Aufgabe 2: Array-Statistiken**

```javascript
// Schreiben Sie eine Funktion, die ein Array von Zahlen nimmt und
// ein Objekt mit {min, max, sum, average} zurückgibt
// Nutzen Sie console.log für Zwischenschritte

console.log("=== Array-Statistiken ===");
// Ihr Code hier:
// const getStats = (numbers) => { ... }

// Test:
// const testData = [10, 5, 20, 15, 30];
// const stats = getStats(testData);
// console.log("Ergebnis:", stats);
```
@eval

**Aufgabe 3: Produkt-Filter mit Default Values**

```javascript
// Schreiben Sie eine Funktion filterProducts(products, minPrice = 0, maxPrice = Infinity)
// Sie soll nur Produkte im Preisbereich zurückgeben
// Nutzen Sie filter() und Arrow Functions

console.log("=== Produkt-Filter ===");
const products = [
  { name: "Laptop", price: 999 },
  { name: "Maus", price: 29 },
  { name: "Tastatur", price: 79 },
  { name: "Monitor", price: 299 }
];

// Ihr Code hier:
// const filterProducts = ...

// Tests:
// filterProducts(products);             // Alle
// filterProducts(products, 50);         // Preis >= 50
// filterProducts(products, 50, 300);    // 50 <= Preis <= 300
```
@eval

**Aufgabe 4: Countdown mit Closure**

```javascript
// Schreiben Sie eine Funktion createCountdown(start),
// die eine Funktion zurückgibt, welche bei jedem Aufruf
// den Zähler um 1 reduziert und ausgibt
// Bei 0 soll "🚀 Start!" ausgegeben werden

console.log("=== Countdown ===");
// Ihr Code hier:
// const createCountdown = (start) => { ... }

// Test:
// const countdown = createCountdown(5);
// countdown(); // 5
// countdown(); // 4
// countdown(); // 3
// countdown(); // 2
// countdown(); // 1
// countdown(); // 🚀 Start!
```
@eval

**Aufgabe 5: User-Validator mit Guard Clauses**

```javascript
// Schreiben Sie eine Funktion validateUser(user),
// die true/false zurückgibt
// Prüfungen:
// - user.name muss existieren (min. 2 Zeichen)
// - user.email muss @ enthalten
// - user.age muss >= 18 sein
// Nutzen Sie frühe returns (Guard Clauses)

console.log("=== User-Validator ===");
// Ihr Code hier:
// const validateUser = (user) => { ... }

// Tests:
const users = [
  { name: "Alice", email: "alice@test.com", age: 25 },
  { name: "B", email: "bob@test.com", age: 20 },
  { name: "Charlie", email: "charlie.com", age: 30 },
  { name: "David", email: "david@test.com", age: 16 }
];

// users.forEach(user => {
//   console.log(`\n${user.name}:`, validateUser(user) ? "✅" : "❌");
// });
```
@eval

</section>

    --{{1}}--
Diese Übungen fordern Sie heraus! Wenn Sie nicht weiterkommen, schauen Sie sich die Beispiele aus den vorherigen Abschnitten an. Funktionen sind wie Werkzeuge – je mehr Sie üben, desto geschickter werden Sie. Closure ist besonders knifflig, lassen Sie sich nicht entmutigen!

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (Temperatur-Konverter)</summary>

```javascript
console.log("=== Temperatur-Konverter ===");

const celsiusToFahrenheit = (celsius) => {
  console.log(`\nInput: ${celsius}°C`);
  const fahrenheit = celsius * 9/5 + 32;
  console.log(`Berechnung: ${celsius} × 9/5 + 32 = ${fahrenheit}`);
  console.log(`Ergebnis: ${fahrenheit}°F`);
  return fahrenheit;
};

// Tests
celsiusToFahrenheit(0);    // 32°F
celsiusToFahrenheit(100);  // 212°F
celsiusToFahrenheit(37);   // 98.6°F
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Array-Statistiken)</summary>

```javascript
console.log("=== Array-Statistiken ===");

const getStats = (numbers) => {
  console.log("\nInput:", numbers);
  
  const min = Math.min(...numbers);
  console.log(`  Min: ${min}`);
  
  const max = Math.max(...numbers);
  console.log(`  Max: ${max}`);
  
  const sum = numbers.reduce((acc, num) => acc + num, 0);
  console.log(`  Sum: ${sum}`);
  
  const average = sum / numbers.length;
  console.log(`  Average: ${average.toFixed(2)}`);
  
  return { min, max, sum, average };
};

// Test
const testData = [10, 5, 20, 15, 30];
const stats = getStats(testData);
console.log("\nErgebnis:", stats);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Produkt-Filter)</summary>

```javascript
console.log("=== Produkt-Filter ===");
const products = [
  { name: "Laptop", price: 999 },
  { name: "Maus", price: 29 },
  { name: "Tastatur", price: 79 },
  { name: "Monitor", price: 299 }
];

const filterProducts = (products, minPrice = 0, maxPrice = Infinity) => {
  console.log(`\nFilter: ${minPrice} <= Preis <= ${maxPrice}`);
  
  const filtered = products.filter(p => {
    const inRange = p.price >= minPrice && p.price <= maxPrice;
    console.log(`  ${p.name} (${p.price}€): ${inRange ? "✅" : "❌"}`);
    return inRange;
  });
  
  console.log(`Ergebnis: ${filtered.length} Produkte`);
  return filtered;
};

// Tests
console.log("\nAlle Produkte:");
filterProducts(products);

console.log("\nPreis >= 50:");
filterProducts(products, 50);

console.log("\n50 <= Preis <= 300:");
filterProducts(products, 50, 300);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 4 (Countdown mit Closure)</summary>

```javascript
console.log("=== Countdown ===");

const createCountdown = (start) => {
  console.log(`→ Initialisiere Countdown bei ${start}\n`);
  let count = start;
  
  return function() {
    if (count > 0) {
      console.log(`  ${count}`);
      count--;
    } else {
      console.log("  🚀 Start!");
    }
  };
};

// Test
const countdown = createCountdown(5);
countdown(); // 5
countdown(); // 4
countdown(); // 3
countdown(); // 2
countdown(); // 1
countdown(); // 🚀 Start!
countdown(); // 🚀 Start! (bleibt bei 0)
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 5 (User-Validator)</summary>

```javascript
console.log("=== User-Validator ===");

const validateUser = (user) => {
  console.log(`\nValidiere:`, user);
  
  if (!user.name) {
    console.log("  ❌ Name fehlt");
    return false;
  }
  
  if (user.name.length < 2) {
    console.log("  ❌ Name zu kurz");
    return false;
  }
  
  if (!user.email || !user.email.includes("@")) {
    console.log("  ❌ Ungültige Email");
    return false;
  }
  
  if (user.age < 18) {
    console.log("  ❌ Zu jung (min. 18)");
    return false;
  }
  
  console.log("  ✅ Valid");
  return true;
};

// Tests
const users = [
  { name: "Alice", email: "alice@test.com", age: 25 },
  { name: "B", email: "bob@test.com", age: 20 },
  { name: "Charlie", email: "charlie.com", age: 30 },
  { name: "David", email: "david@test.com", age: 16 }
];

users.forEach(user => {
  const valid = validateUser(user);
  console.log(`→ ${user.name}: ${valid ? "✅" : "❌"}`);
});
```
@eval

</details>

</section>

    --{{2}}--
Fantastisch! Sie beherrschen jetzt Funktionen – von einfachen Deklarationen über Arrow Functions bis zu fortgeschrittenen Closures. Funktionen sind Ihre Bausteine für wiederverwendbaren, wartbaren Code. Bereit für das Wichtigste: Objekte und Arrays in Kapitel vier?

---

---

## Kapitel 4: Objekte & Arrays – Strukturierte Daten

    --{{0}}--
Objekte und Arrays sind die fundamentalen Datenstrukturen in JavaScript – und essentiell für Datenbank-Operationen. Datenbanken speichern Dokumente als Objekte, Query-Ergebnisse sind Arrays von Objekten. Fast jede DB-Operation arbeitet mit diesen Strukturen. Dieses Kapitel ist DAS WICHTIGSTE für Ihre Datenbank-Arbeit. Nehmen Sie sich Zeit, die Beispiele zu verstehen!

    {{0}}
<section>

**Warum sind Objekte & Arrays so wichtig?**

- **Datenbanken = Objekte**: Jeder Datensatz ist ein Objekt `{ id: 1, name: "Alice" }`
- **Query-Results = Arrays**: `[{user1}, {user2}, {user3}]`
- **Array-Methoden**: `map`, `filter`, `find` sind Ihre täglichen Werkzeuge
- **JSON**: Das universelle Datenformat basiert auf Objekten & Arrays

</section>

---

### 4.1 Objekte: Grundlagen

    --{{0}}--
Objekte sind Sammlungen von Key-Value-Paaren. Denken Sie an eine Tabellzeile in einer Datenbank: Jede Spalte ist ein Property. Objekte werden mit geschweiften Klammern erstellt, Properties mit Doppelpunkt zugewiesen. Sie sind DIE Datenstruktur für strukturierte Informationen.

    {{0}}
<section>

**Syntax: `{ key: value }`**

```javascript
console.log("=== Beispiel 1: Objekt erstellen ===");

const user = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  age: 28,
  active: true
};

console.log("User-Objekt:", user);
console.log("Typ:", typeof user);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Verschachtelte Objekte:**

```javascript
console.log("=== Beispiel 2: Verschachtelt ===");

const product = {
  id: 101,
  name: "Laptop",
  price: 999,
  specs: {
    cpu: "Intel i7",
    ram: "16GB",
    storage: "512GB SSD"
  },
  tags: ["electronics", "computers", "new"]
};

console.log("Produkt:", product);
console.log("\nNested Object:");
console.log("  specs:", product.specs);
console.log("  CPU:", product.specs.cpu);
console.log("\nNested Array:");
console.log("  tags:", product.tags);
console.log("  Erster Tag:", product.tags[0]);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Objekte dynamisch erstellen:**

```javascript
console.log("=== Beispiel 3: Dynamisch erstellen ===");

const createUser = (id, name, role) => {
  console.log(`\nErstelle User: ${name}`);
  return {
    id: id,
    name: name,
    role: role,
    createdAt: new Date().toISOString()
  };
};

const user1 = createUser(1, "Bob", "admin");
console.log("User 1:", user1);

const user2 = createUser(2, "Charlie", "user");
console.log("\nUser 2:", user2);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Shorthand Property Names (ES6):**

```javascript
console.log("=== Beispiel 4: Shorthand Syntax ===");

const id = 123;
const name = "David";
const active = true;

// Alt: { id: id, name: name, active: active }
// Neu (wenn Variablenname = Key):
const user = { id, name, active };

console.log("User:", user);
console.log("\nDies ist identisch mit:");
console.log("{ id: id, name: name, active: active }");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: DB-Dokument simuliert:**

```javascript
console.log("=== Beispiel 5: Datenbank-Dokument ===");

const dbDocument = {
  _id: "507f1f77bcf86cd799439011",
  collection: "orders",
  data: {
    orderId: 1001,
    customer: {
      name: "Alice",
      email: "alice@example.com"
    },
    items: [
      { productId: 1, name: "Laptop", price: 999, quantity: 1 },
      { productId: 2, name: "Maus", price: 29, quantity: 2 }
    ],
    total: 1057,
    status: "paid"
  },
  meta: {
    createdAt: "2025-10-21T10:00:00Z",
    updatedAt: "2025-10-21T10:15:00Z"
  }
};

console.log("DB-Dokument:", dbDocument);
console.log("\nZugriff auf verschachtelte Daten:");
console.log("  Customer Name:", dbDocument.data.customer.name);
console.log("  Anzahl Items:", dbDocument.data.items.length);
console.log("  Erstes Item:", dbDocument.data.items[0].name);
console.log("  Total:", dbDocument.data.total, "€");
console.log("--- Ende Beispiel 5 ---");
```
@eval

</section>

---

### 4.2 Property-Zugriff

    --{{0}}--
Es gibt zwei Arten, auf Objekt-Properties zuzugreifen: Dot-Notation mit Punkt und Bracket-Notation mit eckigen Klammern. Dot ist üblicher und lesbarer, aber Brackets sind flexibler – Sie können damit dynamische Keys oder Keys mit Leerzeichen verwenden. Beides ist wichtig für Datenbank-Arbeit!

    {{0}}
<section>

**Dot-Notation vs. Bracket-Notation:**

```javascript
console.log("=== Beispiel 1: Zwei Arten des Zugriffs ===");

const user = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  "first login": "2025-01-15" // Key mit Leerzeichen
};

console.log("Objekt:", user);

console.log("\nDot-Notation:");
console.log("  user.name =", user.name);
console.log("  user.email =", user.email);

console.log("\nBracket-Notation:");
console.log('  user["name"] =', user["name"]);
console.log('  user["email"] =', user["email"]);

console.log("\nBei Leerzeichen nur Brackets:");
console.log('  user["first login"] =', user["first login"]);
// console.log("  user.first login =", "FEHLER!"); // ❌ Syntaxfehler
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Dynamischer Zugriff mit Variablen:**

```javascript
console.log("=== Beispiel 2: Dynamischer Zugriff ===");

const product = {
  id: 101,
  name: "Laptop",
  price: 999,
  stock: 5
};

console.log("Produkt:", product);

const fields = ["name", "price", "stock"];
console.log("\nLese Felder dynamisch:");

for (const field of fields) {
  console.log(`  ${field}: ${product[field]}`); // Bracket mit Variable!
}

console.log("\nSuche nach Feld:");
const searchField = "price";
console.log(`  Feld "${searchField}" hat Wert:`, product[searchField]);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Properties hinzufügen & ändern:**

```javascript
console.log("=== Beispiel 3: Modify Properties ===");

const user = {
  name: "Bob",
  age: 25
};

console.log("Start:", user);

console.log("\nFüge Property hinzu:");
user.email = "bob@example.com";
console.log("  Nach user.email =", user);

console.log("\nÄndere existierendes Property:");
user.age = 26;
console.log("  Nach user.age = 26:", user);

console.log("\nFüge mit Brackets hinzu:");
user["role"] = "admin";
console.log("  Nach user['role'] =", user);

console.log("--- Ende Beispiel 3 ---");
```
@eval

**Properties löschen:**

```javascript
console.log("=== Beispiel 4: Delete Properties ===");

const user = {
  id: 1,
  name: "Charlie",
  email: "charlie@example.com",
  tempToken: "abc123"
};

console.log("Vorher:", user);

console.log("\nLösche tempToken:");
delete user.tempToken;
console.log("Nachher:", user);

console.log("\nPrüfe ob Property existiert:");
console.log("  'name' in user:", "name" in user);
console.log("  'tempToken' in user:", "tempToken" in user);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Datenbank-Query-Builder:**

```javascript
console.log("=== Beispiel 5: Query-Builder ===");

const buildQuery = (table, conditions) => {
  console.log(`\nBaue Query für Tabelle: ${table}`);
  console.log("Conditions:", conditions);
  
  const whereClauses = [];
  
  for (const key in conditions) {
    const value = conditions[key];
    console.log(`  → Prüfe: ${key} = ${value}`);
    
    if (typeof value === "string") {
      whereClauses.push(`${key} = '${value}'`);
    } else {
      whereClauses.push(`${key} = ${value}`);
    }
  }
  
  const whereString = whereClauses.join(" AND ");
  const query = `SELECT * FROM ${table} WHERE ${whereString}`;
  
  console.log(`\n✅ Query: ${query}`);
  return query;
};

buildQuery("users", { active: true, role: "admin" });
buildQuery("products", { category: "electronics", price: 999 });
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Optional Chaining (?.):**

```javascript
console.log("=== Beispiel 6: Optional Chaining ===");

const users = [
  { name: "Alice", address: { city: "Berlin" } },
  { name: "Bob", address: null },
  { name: "Charlie" } // Kein address-Feld
];

console.log("Users:", users);

console.log("\nOhne Optional Chaining (⚠️ kann crashen):");
for (const user of users) {
  console.log(`\n${user.name}:`);
  // console.log("  Stadt:", user.address.city); // ❌ Crash bei Bob/Charlie
  
  // ✅ Manueller Check:
  if (user.address && user.address.city) {
    console.log("  Stadt:", user.address.city);
  } else {
    console.log("  Stadt: N/A");
  }
}

console.log("\n\nMit Optional Chaining (✅ sicher):");
for (const user of users) {
  console.log(`${user.name}: Stadt =`, user.address?.city || "N/A");
}
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.3 Object Methods

    --{{0}}--
Objekte können nicht nur Daten speichern, sondern auch Funktionen – diese nennt man Methoden. Das ist zentral für objektorientierte Programmierung. Besonders wichtig: Die eingebauten Object-Methoden wie Object.keys, Object.values und Object.entries zum Durchlaufen von Objekten.

    {{0}}
<section>

**Methoden in Objekten:**

```javascript
console.log("=== Beispiel 1: Object Methods ===");

const user = {
  name: "Alice",
  age: 28,
  
  greet: function() {
    console.log(`  → Hallo, ich bin ${this.name}!`);
  },
  
  // Shorthand Syntax (ES6):
  getInfo() {
    console.log(`  → ${this.name}, ${this.age} Jahre alt`);
  }
};

console.log("User-Objekt:", user);

console.log("\nRufe Methoden auf:");
user.greet();
user.getInfo();
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Object.keys() - Alle Keys:**

```javascript
console.log("=== Beispiel 2: Object.keys() ===");

const product = {
  id: 101,
  name: "Laptop",
  price: 999,
  stock: 5
};

console.log("Produkt:", product);

console.log("\nAlle Keys:");
const keys = Object.keys(product);
console.log("  Keys:", keys);
console.log("  Typ:", Array.isArray(keys) ? "Array" : "kein Array");

console.log("\nIteriere über Keys:");
for (const key of keys) {
  console.log(`  ${key}: ${product[key]}`);
}
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Object.values() - Alle Werte:**

```javascript
console.log("=== Beispiel 3: Object.values() ===");

const scores = {
  Alice: 95,
  Bob: 87,
  Charlie: 92,
  David: 88
};

console.log("Scores:", scores);

console.log("\nAlle Werte:");
const values = Object.values(scores);
console.log("  Values:", values);

console.log("\nBerechne Durchschnitt:");
const sum = values.reduce((acc, val) => acc + val, 0);
const average = sum / values.length;
console.log(`  Summe: ${sum}`);
console.log(`  Durchschnitt: ${average.toFixed(2)}`);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Object.entries() - Key-Value-Paare:**

```javascript
console.log("=== Beispiel 4: Object.entries() ===");

const config = {
  host: "localhost",
  port: 5432,
  database: "mydb",
  user: "admin"
};

console.log("Config:", config);

console.log("\nAlle Entries:");
const entries = Object.entries(config);
console.log("  Entries:", entries);
console.log("  Format: Array von [key, value] Paaren");

console.log("\nIteriere mit Destructuring:");
for (const [key, value] of entries) {
  console.log(`  ${key}: ${value}`);
}
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Praxis: Objekt-Validierung:**

```javascript
console.log("=== Beispiel 5: Validierung ===");

const validateProduct = (product) => {
  console.log("\nValidiere Produkt:", product);
  
  const requiredFields = ["id", "name", "price"];
  const keys = Object.keys(product);
  
  console.log("  Erforderlich:", requiredFields);
  console.log("  Vorhanden:", keys);
  
  for (const field of requiredFields) {
    if (!keys.includes(field)) {
      console.log(`  ❌ Fehlt: ${field}`);
      return false;
    }
  }
  
  console.log("  ✅ Alle Pflichtfelder vorhanden");
  return true;
};

const products = [
  { id: 1, name: "Laptop", price: 999 },
  { id: 2, name: "Maus" }, // price fehlt
  { name: "Tastatur", price: 79 } // id fehlt
];

products.forEach((p, i) => {
  console.log(`\n→ Produkt ${i + 1}:`);
  validateProduct(p);
});
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Object.assign() & Spread Operator:**

```javascript
console.log("=== Beispiel 6: Objekte zusammenführen ===");

const defaults = {
  theme: "light",
  notifications: true,
  language: "en"
};

const userSettings = {
  theme: "dark",
  language: "de"
};

console.log("Defaults:", defaults);
console.log("User Settings:", userSettings);

console.log("\nMit Object.assign():");
const merged1 = Object.assign({}, defaults, userSettings);
console.log("  Merged:", merged1);

console.log("\nMit Spread Operator (moderner):");
const merged2 = { ...defaults, ...userSettings };
console.log("  Merged:", merged2);

console.log("\nUser-Werte überschreiben Defaults!");
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.4 Destructuring (Objekte)

    --{{0}}--
Destructuring ist eine elegante Syntax, um Werte aus Objekten zu extrahieren. Statt mehrere Zeilen mit user.name, user.email zu schreiben, extrahieren Sie alles in einer Zeile. Besonders praktisch bei Funktionsparametern und API-Responses. Moderne Datenbank-Libraries nutzen das intensiv!

    {{0}}
<section>

**Grundlagen:**

```javascript
console.log("=== Beispiel 1: Destructuring Basics ===");

const user = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  age: 28
};

console.log("User:", user);

console.log("\nOhne Destructuring:");
const name1 = user.name;
const email1 = user.email;
console.log(`  ${name1}, ${email1}`);

console.log("\nMit Destructuring:");
const { name, email } = user;
console.log(`  ${name}, ${email}`);

console.log("\nBeide sind identisch!");
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Mit Umbenennung:**

```javascript
console.log("=== Beispiel 2: Umbenennen ===");

const product = {
  id: 101,
  name: "Laptop",
  price: 999
};

console.log("Produkt:", product);

console.log("\nDestructuring mit Rename:");
const { name: productName, price: productPrice } = product;
console.log(`  productName: ${productName}`);
console.log(`  productPrice: ${productPrice}`);

console.log("\nOriginal 'name' existiert nicht in diesem Scope:");
// console.log("  name:", name); // ❌ ReferenceError
console.log("  (nur productName ist definiert)");
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Mit Default Values:**

```javascript
console.log("=== Beispiel 3: Default Values ===");

const user = {
  name: "Bob",
  email: "bob@example.com"
  // role fehlt!
};

console.log("User:", user);

console.log("\nDestructuring mit Defaults:");
const { name, email, role = "user", active = true } = user;
console.log(`  name: ${name}`);
console.log(`  email: ${email}`);
console.log(`  role: ${role} (default)`);
console.log(`  active: ${active} (default)`);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Nested Destructuring:**

```javascript
console.log("=== Beispiel 4: Verschachtelt ===");

const order = {
  orderId: 1001,
  customer: {
    name: "Charlie",
    address: {
      city: "Berlin",
      zip: "10115"
    }
  },
  total: 199
};

console.log("Order:", order);

console.log("\nNested Destructuring:");
const {
  orderId,
  customer: {
    name: customerName,
    address: { city }
  }
} = order;

console.log(`  Order: ${orderId}`);
console.log(`  Customer: ${customerName}`);
console.log(`  City: ${city}`);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**In Funktionsparametern:**

```javascript
console.log("=== Beispiel 5: In Funktionen ===");

// Ohne Destructuring:
const displayUser1 = (user) => {
  console.log(`\n→ ${user.name} (${user.email})`);
};

// Mit Destructuring (eleganter):
const displayUser2 = ({ name, email, role = "user" }) => {
  console.log(`\n→ ${name} (${email}) - Role: ${role}`);
};

const users = [
  { name: "Alice", email: "alice@test.com", role: "admin" },
  { name: "Bob", email: "bob@test.com" }
];

console.log("Ohne Destructuring:");
users.forEach(displayUser1);

console.log("\nMit Destructuring:");
users.forEach(displayUser2);
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Praxis: API-Response verarbeiten:**

```javascript
console.log("=== Beispiel 6: API-Response ===");

const apiResponse = {
  status: 200,
  data: {
    users: [
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" }
    ],
    pagination: {
      page: 1,
      totalPages: 5,
      totalItems: 47
    }
  },
  meta: {
    timestamp: "2025-10-21T10:00:00Z",
    version: "1.0"
  }
};

console.log("API-Response:", apiResponse);

console.log("\nExtrahiere wichtige Daten:");
const {
  status,
  data: {
    users,
    pagination: { page, totalPages }
  }
} = apiResponse;

console.log(`  Status: ${status}`);
console.log(`  Users gefunden: ${users.length}`);
console.log(`  Seite ${page} von ${totalPages}`);

console.log("\nVerarbeite Users:");
users.forEach(({ id, name }) => {
  console.log(`  [${id}] ${name}`);
});
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.5 Arrays: Grundlagen

    --{{0}}--
Arrays sind geordnete Listen von Werten. In Datenbanken sind Query-Ergebnisse fast immer Arrays von Dokumenten. Arrays sind nullbasiert – das erste Element hat Index null. Sie können verschiedene Typen mischen, aber in der Praxis enthalten DB-Results meist gleichartige Objekte.

    {{0}}
<section>

**Array erstellen:**

```javascript
console.log("=== Beispiel 1: Arrays erstellen ===");

const numbers = [1, 2, 3, 4, 5];
console.log("Numbers:", numbers);
console.log("  Länge:", numbers.length);
console.log("  Typ:", Array.isArray(numbers) ? "Array" : "kein Array");

const mixed = [1, "text", true, null, { key: "value" }];
console.log("\nGemischte Typen:", mixed);

const empty = [];
console.log("\nLeeres Array:", empty);
console.log("  Länge:", empty.length);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Zugriff mit Index:**

```javascript
console.log("=== Beispiel 2: Index-Zugriff ===");

const fruits = ["🍎 Apfel", "🍌 Banane", "🍇 Trauben", "🍊 Orange"];
console.log("Fruits:", fruits);

console.log("\nZugriff per Index (0-basiert):");
console.log("  [0]:", fruits[0]);
console.log("  [1]:", fruits[1]);
console.log("  [2]:", fruits[2]);

console.log("\nLetztes Element:");
console.log("  [-1] geht nicht in JS!"); // ❌ Nicht wie Python
console.log("  [length-1]:", fruits[fruits.length - 1]);

console.log("\nUngültiger Index:");
console.log("  [99]:", fruits[99]); // undefined
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Elemente hinzufügen & entfernen:**

```javascript
console.log("=== Beispiel 3: Modify Arrays ===");

const stack = [1, 2, 3];
console.log("Start:", stack);

console.log("\npush() - Hinten anfügen:");
stack.push(4);
console.log("  Nach push(4):", stack);

console.log("\npop() - Letztes entfernen:");
const last = stack.pop();
console.log(`  Entfernt: ${last}`);
console.log("  Nach pop():", stack);

console.log("\nunshift() - Vorne einfügen:");
stack.unshift(0);
console.log("  Nach unshift(0):", stack);

console.log("\nshift() - Erstes entfernen:");
const first = stack.shift();
console.log(`  Entfernt: ${first}`);
console.log("  Nach shift():", stack);

console.log("--- Ende Beispiel 3 ---");
```
@eval

**splice() - Einfügen & Löschen:**

```javascript
console.log("=== Beispiel 4: splice() ===");

const letters = ["A", "B", "E", "F"];
console.log("Start:", letters);

console.log("\nFüge 'C' und 'D' bei Index 2 ein:");
letters.splice(2, 0, "C", "D"); // Ab Index 2, 0 löschen, 2 einfügen
console.log("  Nach splice:", letters);

console.log("\nLösche 1 Element bei Index 4:");
const removed = letters.splice(4, 1); // Ab Index 4, 1 löschen
console.log(`  Entfernt: ${removed}`);
console.log("  Nach splice:", letters);

console.log("--- Ende Beispiel 4 ---");
```
@eval

**Array of Objects (DB-Results!):**

```javascript
console.log("=== Beispiel 5: DB-Results simuliert ===");

const users = [
  { id: 1, name: "Alice", active: true },
  { id: 2, name: "Bob", active: false },
  { id: 3, name: "Charlie", active: true }
];

console.log("DB-Query-Result:", users);
console.log("  Anzahl:", users.length);

console.log("\nDurchlaufe Ergebnisse:");
for (let i = 0; i < users.length; i++) {
  const user = users[i];
  console.log(`  [${i}] ${user.name} (ID: ${user.id})`);
  console.log(`      Status: ${user.active ? "✅ aktiv" : "❌ inaktiv"}`);
}
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Spread Operator mit Arrays:**

```javascript
console.log("=== Beispiel 6: Spread Operator ===");

const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];

console.log("Array 1:", arr1);
console.log("Array 2:", arr2);

console.log("\nKombinieren mit Spread:");
const combined = [...arr1, ...arr2];
console.log("  Combined:", combined);

console.log("\nKopieren:");
const copy = [...arr1];
console.log("  Original:", arr1);
console.log("  Copy:", copy);

console.log("\nSind unterschiedliche Arrays:");
copy.push(999);
console.log("  Nach copy.push(999):");
console.log("    Original:", arr1);
console.log("    Copy:", copy);
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.6 Array-Iteration

    --{{0}}--
Es gibt viele Wege, Arrays zu durchlaufen. Die klassische for-Schleife kennen Sie schon. Jetzt lernen Sie die modernen Array-Methoden – forEach ist der einfachste Einstieg. Diese Methoden sind der Schlüssel zu eleganter Datenverarbeitung!

    {{0}}
<section>

**forEach() - Für jedes Element:**

```javascript
console.log("=== Beispiel 1: forEach() ===");

const numbers = [10, 20, 30, 40];
console.log("Array:", numbers);

console.log("\nDurchlaufe mit forEach:");
numbers.forEach((num, index) => {
  console.log(`  [${index}] Wert: ${num}, Verdoppelt: ${num * 2}`);
});

console.log("--- Ende Beispiel 1 ---");
```
@eval

**Praxis: DB-Results ausgeben:**

```javascript
console.log("=== Beispiel 2: forEach mit Objekten ===");

const products = [
  { id: 1, name: "Laptop", price: 999, stock: 5 },
  { id: 2, name: "Maus", price: 29, stock: 150 },
  { id: 3, name: "Tastatur", price: 79, stock: 0 }
];

console.log("Produkte:", products);
console.log("\nAusgabe formatiert:");

products.forEach((product, index) => {
  console.log(`\n[${index + 1}] ${product.name}`);
  console.log(`    ID: ${product.id}`);
  console.log(`    Preis: ${product.price}€`);
  console.log(`    Lager: ${product.stock > 0 ? `${product.stock} Stück` : "❌ Ausverkauft"}`);
});

console.log("--- Ende Beispiel 2 ---");
```
@eval

</section>

---

### 4.7 Array-Methoden: forEach, map, filter, find

    --{{0}}--
Jetzt kommen die WICHTIGSTEN Array-Methoden für Datenbank-Arbeit. Map transformiert Daten, filter selektiert Daten, find sucht einzelne Elemente. Diese Methoden sind funktional – sie ändern das Original-Array nicht, sondern geben ein neues zurück. Das ist sicherer und lesbarer als Schleifen!

    {{0}}
<section>

**map() - Transformieren:**

```javascript
console.log("=== Beispiel 1: map() ===");

const numbers = [1, 2, 3, 4, 5];
console.log("Original:", numbers);

console.log("\nVerdopple mit map:");
const doubled = numbers.map(num => {
  console.log(`  ${num} → ${num * 2}`);
  return num * 2;
});

console.log("\nErgebnis:", doubled);
console.log("Original unverändert:", numbers);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**map() mit Objekten (Praxis!):**

```javascript
console.log("=== Beispiel 2: map() - Daten extrahieren ===");

const users = [
  { id: 1, name: "Alice", email: "alice@example.com" },
  { id: 2, name: "Bob", email: "bob@example.com" },
  { id: 3, name: "Charlie", email: "charlie@example.com" }
];

console.log("Users:", users);

console.log("\nExtrahiere nur Namen:");
const names = users.map(user => {
  console.log(`  Extrahiere: ${user.name}`);
  return user.name;
});
console.log("Names:", names);

console.log("\nErstelle Email-Liste:");
const emails = users.map(u => u.email);
console.log("Emails:", emails);

console.log("\nTransformiere zu neuem Format:");
const simplified = users.map(({ id, name }) => ({
  userId: id,
  displayName: name.toUpperCase()
}));
console.log("Simplified:", simplified);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**filter() - Selektieren:**

```javascript
console.log("=== Beispiel 3: filter() ===");

const numbers = [1, 5, 10, 15, 20, 25, 30];
console.log("Zahlen:", numbers);

console.log("\nFilter: Nur Zahlen > 15");
const filtered = numbers.filter(num => {
  const keep = num > 15;
  console.log(`  ${num}: ${keep ? "✅ behalten" : "❌ verwerfen"}`);
  return keep;
});

console.log("\nErgebnis:", filtered);
console.log("Original unverändert:", numbers);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**filter() mit Objekten (DB-Query!):**

```javascript
console.log("=== Beispiel 4: filter() - WHERE clause simuliert ===");

const products = [
  { id: 1, name: "Laptop", price: 999, category: "electronics", stock: 5 },
  { id: 2, name: "Maus", price: 29, category: "electronics", stock: 150 },
  { id: 3, name: "Stuhl", price: 199, category: "furniture", stock: 10 },
  { id: 4, name: "Monitor", price: 299, category: "electronics", stock: 0 }
];

console.log("Alle Produkte:", products);

console.log("\nQuery 1: Elektronik + Preis >= 100 + Lager > 0");
const query1 = products.filter(p => {
  const match = p.category === "electronics" && p.price >= 100 && p.stock > 0;
  console.log(`  ${p.name}: ${match ? "✅" : "❌"}`);
  return match;
});
console.log("Ergebnis:", query1);

console.log("\nQuery 2: Ausverkaufte Produkte");
const outOfStock = products.filter(p => p.stock === 0);
console.log("Ergebnis:", outOfStock.map(p => p.name));
console.log("--- Ende Beispiel 4 ---");
```
@eval

**find() - Erstes Element finden:**

```javascript
console.log("=== Beispiel 5: find() ===");

const users = [
  { id: 1, name: "Alice", role: "user" },
  { id: 2, name: "Bob", role: "admin" },
  { id: 3, name: "Charlie", role: "user" }
];

console.log("Users:", users);

console.log("\nSuche User mit ID 2:");
const user = users.find(u => {
  console.log(`  Prüfe: ${u.name} (ID: ${u.id})`);
  return u.id === 2;
});
console.log("Gefunden:", user);

console.log("\nSuche ersten Admin:");
const admin = users.find(u => u.role === "admin");
console.log("Admin:", admin.name);

console.log("\nSuche nicht-existierenden User:");
const notFound = users.find(u => u.id === 999);
console.log("Ergebnis:", notFound); // undefined
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Kombination: map + filter:**

```javascript
console.log("=== Beispiel 6: map + filter kombiniert ===");

const orders = [
  { id: 1, customer: "Alice", amount: 150, status: "paid" },
  { id: 2, customer: "Bob", amount: 80, status: "pending" },
  { id: 3, customer: "Charlie", amount: 200, status: "paid" },
  { id: 4, customer: "David", amount: 50, status: "cancelled" }
];

console.log("Orders:", orders);

console.log("\nPipeline: paid orders → amounts → sum");

console.log("\n1. Filter: Nur bezahlte Orders");
const paidOrders = orders.filter(o => {
  console.log(`  ${o.id}: ${o.status} → ${o.status === "paid" ? "✅" : "❌"}`);
  return o.status === "paid";
});

console.log("\n2. Map: Extrahiere amounts");
const amounts = paidOrders.map(o => {
  console.log(`  Order ${o.id}: ${o.amount}€`);
  return o.amount;
});

console.log("\n3. Reduce: Summiere");
const total = amounts.reduce((sum, amount) => {
  const newSum = sum + amount;
  console.log(`  ${sum} + ${amount} = ${newSum}`);
  return newSum;
}, 0);

console.log(`\n✅ Gesamtumsatz (paid): ${total}€`);

console.log("\nOder in einer Chain:");
const totalChained = orders
  .filter(o => o.status === "paid")
  .map(o => o.amount)
  .reduce((sum, amt) => sum + amt, 0);
console.log(`Total (chained): ${totalChained}€`);
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.8 Array-Methoden: reduce, some, every

    --{{0}}--
Reduce ist die mächtigste Array-Methode – sie kann alles, was map und filter können, und mehr. Some und every sind Prüf-Methoden, die true oder false zurückgeben. Diese drei Methoden vervollständigen Ihr Array-Werkzeugkasten für komplexe Datenverarbeitung.

    {{0}}
<section>

**reduce() - Akkumulieren:**

```javascript
console.log("=== Beispiel 1: reduce() - Summe ===");

const numbers = [10, 20, 30, 40, 50];
console.log("Zahlen:", numbers);

console.log("\nBerechne Summe:");
const sum = numbers.reduce((accumulator, current) => {
  console.log(`  Acc: ${accumulator}, Current: ${current}`);
  const newAcc = accumulator + current;
  console.log(`    → Neuer Acc: ${newAcc}`);
  return newAcc;
}, 0); // Start bei 0

console.log(`\n✅ Summe: ${sum}`);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**reduce() - Komplexe Aggregation:**

```javascript
console.log("=== Beispiel 2: reduce() - Statistiken ===");

const products = [
  { name: "Laptop", price: 999, sold: 5 },
  { name: "Maus", price: 29, sold: 150 },
  { name: "Tastatur", price: 79, sold: 80 }
];

console.log("Produkte:", products);

console.log("\nBerechne Gesamt-Umsatz:");
const totalRevenue = products.reduce((acc, product) => {
  const revenue = product.price * product.sold;
  console.log(`  ${product.name}: ${product.price}€ × ${product.sold} = ${revenue}€`);
  console.log(`    Acc: ${acc} → ${acc + revenue}`);
  return acc + revenue;
}, 0);

console.log(`\n✅ Gesamt-Umsatz: ${totalRevenue}€`);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**reduce() - Objekt aufbauen (Group By):**

```javascript
console.log("=== Beispiel 3: reduce() - Gruppieren ===");

const users = [
  { name: "Alice", role: "admin" },
  { name: "Bob", role: "user" },
  { name: "Charlie", role: "admin" },
  { name: "David", role: "user" },
  { name: "Eve", role: "moderator" }
];

console.log("Users:", users);

console.log("\nGruppiere nach Rolle:");
const grouped = users.reduce((acc, user) => {
  console.log(`\n  Verarbeite: ${user.name} (${user.role})`);
  
  if (!acc[user.role]) {
    console.log(`    Neue Gruppe: ${user.role}`);
    acc[user.role] = [];
  }
  
  acc[user.role].push(user.name);
  console.log(`    ${user.role}:`, acc[user.role]);
  
  return acc;
}, {});

console.log("\n✅ Gruppiert:", grouped);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**some() - Mindestens eines:**

```javascript
console.log("=== Beispiel 4: some() ===");

const numbers = [1, 3, 5, 7, 10, 11];
console.log("Zahlen:", numbers);

console.log("\nGibt es eine gerade Zahl?");
const hasEven = numbers.some(num => {
  const isEven = num % 2 === 0;
  console.log(`  ${num}: ${isEven ? "✅ gerade" : "ungerade"}`);
  if (isEven) console.log("    → some() stoppt hier!");
  return isEven;
});

console.log(`\nErgebnis: ${hasEven}`);

console.log("\nGibt es eine Zahl > 100?");
const hasLarge = numbers.some(num => num > 100);
console.log(`Ergebnis: ${hasLarge}`);
console.log("--- Ende Beispiel 4 ---");
```
@eval

**every() - Alle müssen zutreffen:**

```javascript
console.log("=== Beispiel 5: every() ===");

const ages = [21, 25, 30, 28, 19];
console.log("Alters-Daten:", ages);

console.log("\nSind alle volljährig (>= 18)?");
const allAdults = ages.every(age => {
  const isAdult = age >= 18;
  console.log(`  ${age}: ${isAdult ? "✅ volljährig" : "❌ minderjährig"}`);
  if (!isAdult) console.log("    → every() stoppt hier!");
  return isAdult;
});

console.log(`\nErgebnis: ${allAdults}`);

console.log("\nSind alle >= 21?");
const all21Plus = ages.every(age => age >= 21);
console.log(`Ergebnis: ${all21Plus} (19 ist < 21)`);
console.log("--- Ende Beispiel 6 ---");
```
@eval

**Praxis: Validierung mit every():**

```javascript
console.log("=== Beispiel 6: Batch-Validierung ===");

const products = [
  { id: 1, name: "Laptop", price: 999, stock: 5 },
  { id: 2, name: "Maus", price: 29, stock: 150 },
  { id: 3, name: "", price: 79, stock: 10 }, // ❌ Name fehlt
  { id: 4, name: "Monitor", price: -50, stock: 20 } // ❌ Negativer Preis
];

console.log("Produkte:", products);

console.log("\nValidiere alle Produkte:");
const allValid = products.every(product => {
  console.log(`\n→ Prüfe: ${product.name || "(leer)"}`);
  
  if (!product.name) {
    console.log("  ❌ Name fehlt");
    return false;
  }
  
  if (product.price <= 0) {
    console.log("  ❌ Ungültiger Preis");
    return false;
  }
  
  console.log("  ✅ Valide");
  return true;
});

console.log(`\n${allValid ? "✅ Alle valide" : "❌ Validierung fehlgeschlagen"}`);
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.9 Array Destructuring & Spread Operator

    --{{0}}--
Wie bei Objekten gibt es auch bei Arrays Destructuring – extrahieren von Werten basierend auf Position. Der Spread Operator ist extrem nützlich zum Kopieren, Kombinieren und als Funktions-Argumente. Diese modernen Syntax-Features machen Ihren Code kürzer und lesbarer.

    {{0}}
<section>

**Array Destructuring:**

```javascript
console.log("=== Beispiel 1: Array Destructuring ===");

const colors = ["rot", "grün", "blau", "gelb"];
console.log("Colors:", colors);

console.log("\nOhne Destructuring:");
const first1 = colors[0];
const second1 = colors[1];
console.log(`  Erste: ${first1}, Zweite: ${second1}`);

console.log("\nMit Destructuring:");
const [first, second, third] = colors;
console.log(`  Erste: ${first}`);
console.log(`  Zweite: ${second}`);
console.log(`  Dritte: ${third}`);

console.log("\nÜberspringen mit Kommas:");
const [, , blue] = colors; // Erste 2 überspringen
console.log(`  Dritte (blau): ${blue}`);
console.log("--- Ende Beispiel 1 ---");
```
@eval

**Rest Operator in Arrays:**

```javascript
console.log("=== Beispiel 2: Rest Operator ===");

const numbers = [1, 2, 3, 4, 5, 6];
console.log("Numbers:", numbers);

console.log("\nErstes + Rest:");
const [first, ...rest] = numbers;
console.log(`  Erstes: ${first}`);
console.log(`  Rest:`, rest);

console.log("\nErste 3 + Rest:");
const [a, b, c, ...remaining] = numbers;
console.log(`  a: ${a}, b: ${b}, c: ${c}`);
console.log(`  Remaining:`, remaining);
console.log("--- Ende Beispiel 2 ---");
```
@eval

**Spread Operator - Kombinieren:**

```javascript
console.log("=== Beispiel 3: Arrays kombinieren ===");

const fruits = ["🍎", "🍌"];
const vegetables = ["🥕", "🥦"];
const dairy = ["🥛", "🧀"];

console.log("Fruits:", fruits);
console.log("Vegetables:", vegetables);
console.log("Dairy:", dairy);

console.log("\nKombiniere mit Spread:");
const allFood = [...fruits, ...vegetables, ...dairy];
console.log("All Food:", allFood);

console.log("\nMit zusätzlichen Elementen:");
const shopping = ["🍞", ...fruits, "🥩", ...vegetables];
console.log("Shopping:", shopping);
console.log("--- Ende Beispiel 3 ---");
```
@eval

**Spread Operator - Kopieren (shallow):**

```javascript
console.log("=== Beispiel 4: Shallow Copy ===");

const original = [1, 2, 3];
console.log("Original:", original);

const copy = [...original];
console.log("Copy:", copy);

console.log("\nÄndere Copy:");
copy.push(4);
console.log("  Copy nach push:", copy);
console.log("  Original:", original);
console.log("  → Original unverändert!");

console.log("\n⚠️ Bei verschachtelten Arrays/Objekten:");
const nested = [[1, 2], [3, 4]];
const nestedCopy = [...nested];

console.log("Nested:", nested);
console.log("Nested Copy:", nestedCopy);

nestedCopy[0].push(999);
console.log("\nNach nestedCopy[0].push(999):");
console.log("  Nested:", nested); // ❌ Auch geändert!
console.log("  → Innere Arrays sind referenziert!");
console.log("--- Ende Beispiel 4 ---");
```
@eval

**Spread als Funktions-Argumente:**

```javascript
console.log("=== Beispiel 5: Spread in Funktionen ===");

const numbers = [5, 12, 3, 18, 7];
console.log("Numbers:", numbers);

console.log("\nMath.max() braucht einzelne Argumente:");
// Math.max([5, 12, 3, 18, 7]) // ❌ Funktioniert nicht
// Math.max(5, 12, 3, 18, 7) // ✅ So muss es sein

const max = Math.max(...numbers); // Spread!
console.log(`  Max: ${max}`);

const min = Math.min(...numbers);
console.log(`  Min: ${min}`);

console.log("\nEigene Funktion:");
const sum = (...nums) => {
  console.log("  Erhaltene Args:", nums);
  return nums.reduce((a, b) => a + b, 0);
};

console.log("  Sum:", sum(...numbers));
console.log("--- Ende Beispiel 5 ---");
```
@eval

**Praxis: DB-Results erweitern:**

```javascript
console.log("=== Beispiel 6: Results erweitern ===");

const existingUsers = [
  { id: 1, name: "Alice" },
  { id: 2, name: "Bob" }
];

const newUsers = [
  { id: 3, name: "Charlie" },
  { id: 4, name: "David" }
];

console.log("Existing Users:", existingUsers);
console.log("New Users:", newUsers);

console.log("\nKombiniere Results:");
const allUsers = [...existingUsers, ...newUsers];
console.log("All Users:", allUsers);

console.log("\nFüge Meta-Data hinzu:");
const withMeta = allUsers.map(user => ({
  ...user,
  fetchedAt: new Date().toISOString(),
  source: "database"
}));

console.log("With Meta:", withMeta[0]);
console.log("--- Ende Beispiel 6 ---");
```
@eval

</section>

---

### 4.10 Übung: Objekte & Arrays

    --{{0}}--
Das ist DAS zentrale Kapitel! Diese Übungen simulieren echte Datenbank-Szenarien. Nutzen Sie map, filter, find, reduce und console.log ausgiebig. Wenn Sie diese Aufgaben beherrschen, können Sie jede DB-Query in JavaScript verarbeiten!

    {{0}}
<section>

**Aufgabe 1: Daten extrahieren (map)**

```javascript
// Gegeben sind User-Daten:
const users = [
  { id: 1, firstName: "Alice", lastName: "Smith", age: 28 },
  { id: 2, firstName: "Bob", lastName: "Jones", age: 34 },
  { id: 3, firstName: "Charlie", lastName: "Brown", age: 22 }
];

// Aufgabe: Erstellen Sie ein Array mit vollständigen Namen
// Ergebnis: ["Alice Smith", "Bob Jones", "Charlie Brown"]

console.log("=== Aufgabe 1: Namen extrahieren ===");
console.log("Users:", users);

// Ihr Code hier:
// const fullNames = ...

// console.log("Full Names:", fullNames);
```
@eval

**Aufgabe 2: Filtern (filter)**

```javascript
// Gegeben sind Produkte:
const products = [
  { id: 1, name: "Laptop", price: 999, category: "electronics", inStock: true },
  { id: 2, name: "Maus", price: 29, category: "electronics", inStock: false },
  { id: 3, name: "Stuhl", price: 199, category: "furniture", inStock: true },
  { id: 4, name: "Monitor", price: 299, category: "electronics", inStock: true },
  { id: 5, name: "Tisch", price: 399, category: "furniture", inStock: false }
];

// Aufgabe: Finden Sie alle Elektronik-Produkte, die:
// - in stock sind
// - Preis >= 200
// Geben Sie nur die Namen aus

console.log("=== Aufgabe 2: Filtern ===");
console.log("Produkte:", products);

// Ihr Code hier:
```
@eval

**Aufgabe 3: Summen berechnen (reduce)**

```javascript
// Gegeben sind Bestellungen:
const orders = [
  { id: 101, customer: "Alice", items: [
    { product: "Laptop", price: 999, quantity: 1 },
    { product: "Maus", price: 29, quantity: 2 }
  ]},
  { id: 102, customer: "Bob", items: [
    { product: "Monitor", price: 299, quantity: 1 }
  ]},
  { id: 103, customer: "Charlie", items: [
    { product: "Tastatur", price: 79, quantity: 1 },
    { product: "Maus", price: 29, quantity: 1 }
  ]}
];

// Aufgabe: Berechnen Sie den Gesamtumsatz aller Bestellungen
// (Summe aller: price × quantity)
// Nutzen Sie reduce (eventuell verschachtelt)

console.log("=== Aufgabe 3: Gesamtumsatz ===");
console.log("Orders:", orders);

// Ihr Code hier:
```
@eval

**Aufgabe 4: Group By (reduce + Objekt aufbauen)**

```javascript
// Gegeben sind Transactions:
const transactions = [
  { id: 1, type: "income", amount: 1000, category: "salary" },
  { id: 2, type: "expense", amount: 50, category: "food" },
  { id: 3, type: "income", amount: 200, category: "freelance" },
  { id: 4, type: "expense", amount: 100, category: "transport" },
  { id: 5, type: "expense", amount: 30, category: "food" },
  { id: 6, type: "income", amount: 500, category: "salary" }
];

// Aufgabe: Gruppieren Sie nach 'type' und berechnen Sie die Summe pro Gruppe
// Ergebnis: { income: 1700, expense: 180 }

console.log("=== Aufgabe 4: Group By Type ===");
console.log("Transactions:", transactions);

// Ihr Code hier:
```
@eval

**Aufgabe 5: Chain-Operations (map + filter + reduce)**

```javascript
// Gegeben sind Students mit Noten:
const students = [
  { name: "Alice", grades: [85, 90, 92, 88] },
  { name: "Bob", grades: [70, 75, 72] },
  { name: "Charlie", grades: [95, 98, 97, 99, 94] },
  { name: "David", grades: [60, 65, 58] }
];

// Aufgabe (mehrstufig):
// 1. Berechnen Sie für jeden Student den Durchschnitt
// 2. Filtern Sie nur Students mit Durchschnitt >= 80
// 3. Extrahieren Sie nur die Namen
// Ergebnis: ["Alice", "Charlie"]

console.log("=== Aufgabe 5: Chain Operations ===");
console.log("Students:", students);

// Ihr Code hier:
```
@eval

</section>

    --{{1}}--
Diese Übungen sind anspruchsvoll, aber sie spiegeln echte Datenbank-Arbeit wider! Bei Schwierigkeiten: Arbeiten Sie Schritt für Schritt, nutzen Sie console.log nach jedem Schritt, schauen Sie sich die Beispiele aus den vorherigen Abschnitten an. Map, filter und reduce sind Ihre wichtigsten Werkzeuge!

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (map - Namen extrahieren)</summary>

```javascript
console.log("=== Aufgabe 1: Namen extrahieren ===");
const users = [
  { id: 1, firstName: "Alice", lastName: "Smith", age: 28 },
  { id: 2, firstName: "Bob", lastName: "Jones", age: 34 },
  { id: 3, firstName: "Charlie", lastName: "Brown", age: 22 }
];

console.log("Users:", users);

const fullNames = users.map(user => {
  const fullName = `${user.firstName} ${user.lastName}`;
  console.log(`  ${user.id}: ${fullName}`);
  return fullName;
});

console.log("\nFull Names:", fullNames);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (filter - Elektronik)</summary>

```javascript
console.log("=== Aufgabe 2: Filtern ===");
const products = [
  { id: 1, name: "Laptop", price: 999, category: "electronics", inStock: true },
  { id: 2, name: "Maus", price: 29, category: "electronics", inStock: false },
  { id: 3, name: "Stuhl", price: 199, category: "furniture", inStock: true },
  { id: 4, name: "Monitor", price: 299, category: "electronics", inStock: true },
  { id: 5, name: "Tisch", price: 399, category: "furniture", inStock: false }
];

console.log("Produkte:", products);

console.log("\nFilterung:");
const filtered = products
  .filter(p => {
    const match = p.category === "electronics" && p.inStock && p.price >= 200;
    console.log(`  ${p.name}: ${match ? "✅" : "❌"}`);
    return match;
  })
  .map(p => p.name);

console.log("\nErgebnis:", filtered);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (reduce - Gesamtumsatz)</summary>

```javascript
console.log("=== Aufgabe 3: Gesamtumsatz ===");
const orders = [
  { id: 101, customer: "Alice", items: [
    { product: "Laptop", price: 999, quantity: 1 },
    { product: "Maus", price: 29, quantity: 2 }
  ]},
  { id: 102, customer: "Bob", items: [
    { product: "Monitor", price: 299, quantity: 1 }
  ]},
  { id: 103, customer: "Charlie", items: [
    { product: "Tastatur", price: 79, quantity: 1 },
    { product: "Maus", price: 29, quantity: 1 }
  ]}
];

console.log("Orders:", orders);

const totalRevenue = orders.reduce((total, order) => {
  console.log(`\n→ Order ${order.id} (${order.customer}):`);
  
  const orderTotal = order.items.reduce((orderSum, item) => {
    const itemTotal = item.price * item.quantity;
    console.log(`  ${item.product}: ${item.price}€ × ${item.quantity} = ${itemTotal}€`);
    return orderSum + itemTotal;
  }, 0);
  
  console.log(`  Order Total: ${orderTotal}€`);
  return total + orderTotal;
}, 0);

console.log(`\n✅ Gesamtumsatz: ${totalRevenue}€`);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 4 (Group By)</summary>

```javascript
console.log("=== Aufgabe 4: Group By Type ===");
const transactions = [
  { id: 1, type: "income", amount: 1000, category: "salary" },
  { id: 2, type: "expense", amount: 50, category: "food" },
  { id: 3, type: "income", amount: 200, category: "freelance" },
  { id: 4, type: "expense", amount: 100, category: "transport" },
  { id: 5, type: "expense", amount: 30, category: "food" },
  { id: 6, type: "income", amount: 500, category: "salary" }
];

console.log("Transactions:", transactions);

const grouped = transactions.reduce((acc, transaction) => {
  console.log(`\n→ ${transaction.type}: ${transaction.amount}€`);
  
  if (!acc[transaction.type]) {
    console.log(`  Initialisiere ${transaction.type} bei 0`);
    acc[transaction.type] = 0;
  }
  
  acc[transaction.type] += transaction.amount;
  console.log(`  ${transaction.type} total: ${acc[transaction.type]}€`);
  
  return acc;
}, {});

console.log("\n✅ Gruppiert:", grouped);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 5 (Chain Operations)</summary>

```javascript
console.log("=== Aufgabe 5: Chain Operations ===");
const students = [
  { name: "Alice", grades: [85, 90, 92, 88] },
  { name: "Bob", grades: [70, 75, 72] },
  { name: "Charlie", grades: [95, 98, 97, 99, 94] },
  { name: "David", grades: [60, 65, 58] }
];

console.log("Students:", students);

console.log("\n1. Berechne Durchschnitte:");
const withAverages = students.map(student => {
  const sum = student.grades.reduce((a, b) => a + b, 0);
  const average = sum / student.grades.length;
  console.log(`  ${student.name}: ${average.toFixed(2)}`);
  return { ...student, average };
});

console.log("\n2. Filter: Durchschnitt >= 80:");
const passed = withAverages.filter(student => {
  const pass = student.average >= 80;
  console.log(`  ${student.name}: ${pass ? "✅" : "❌"}`);
  return pass;
});

console.log("\n3. Extrahiere Namen:");
const names = passed.map(s => s.name);
console.log("  Names:", names);

console.log("\nOder als Chain:");
const result = students
  .map(s => ({
    ...s,
    average: s.grades.reduce((a, b) => a + b, 0) / s.grades.length
  }))
  .filter(s => s.average >= 80)
  .map(s => s.name);

console.log("Result (chained):", result);
```
@eval

</details>

</section>

    --{{2}}--
Exzellent! Sie haben jetzt die wichtigsten Werkzeuge für Datenverarbeitung gemeistert. Objekte speichern strukturierte Daten, Arrays organisieren Sammlungen, und die Array-Methoden map, filter, reduce sind Ihre täglichen Begleiter in der Datenbank-Programmierung. Dieses Wissen ist fundamental – jede weitere Arbeit mit Datenbanken baut darauf auf!

---

## Kapitel 5: Asynchronität – Der Event Loop

    --{{0}}--
JavaScript ist singlethreaded – aber asynchron! Das ist FUNDAMENTAL für Datenbank-Operationen. Jede DB-Abfrage dauert einige Millisekunden bis Sekunden. Ohne Asynchronität würde Ihre App währenddessen einfrieren. Dieses Kapitel erklärt, wie JavaScript mit Wartezeiten umgeht und wie Sie modernen async/await-Code schreiben.

---

### 5.1 Blockierender vs. asynchroner Code

    --{{0}}--
Der Unterschied zwischen synchronem und asynchronem Code ist entscheidend. Synchron bedeutet: Warten, bis eine Operation fertig ist. Asynchron bedeutet: Weitermachen und später das Ergebnis verarbeiten.

    {{0}}
<section>

**=== Beispiel 1: Synchroner Code (blockierend) ===**

```javascript
console.log("=== Beispiel 1: Synchroner Code ===");

console.log("1. Start");

// Simuliere langsame Berechnung (blockierend)
function slowCalculation() {
  console.log("  → Berechnung startet...");
  const start = Date.now();
  // Warte 2 Sekunden (blockiert!)
  while (Date.now() - start < 2000) {
    // Busy waiting - BAD PRACTICE!
  }
  console.log("  → Berechnung fertig (nach 2s)");
  return 42;
}

const result = slowCalculation();
console.log("2. Ergebnis:", result);
console.log("3. Ende");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Hier wird der gesamte Thread blockiert! Die Zeile "3. Ende" erscheint erst nach 2 Sekunden. Im Browser würde die UI einfrieren. Das ist problematisch.

</section>

    {{1}}
<section>

**=== Beispiel 2: Asynchroner Code (nicht-blockierend) ===**

```javascript
console.log("=== Beispiel 2: Asynchroner Code ===");

console.log("1. Start");

// setTimeout ist asynchron
setTimeout(() => {
  console.log("  → Callback nach 2 Sekunden");
  console.log("  → Ergebnis: 42");
}, 2000);

console.log("2. Weiter (ohne zu warten)");
console.log("3. Ende");

console.log("--- Ende Beispiel 2 ---");
// Achtung: Der Callback kommt NACH "Ende"!
```
@eval

    --{{2}}--
Jetzt läuft der Code sofort weiter! Die Ausgabe ist: 1, 2, 3, Ende, dann nach 2 Sekunden der Callback. Das ist asynchron: Der Code wartet nicht, sondern registriert einen Callback, der später ausgeführt wird.

</section>

    {{2}}
<section>

**=== Beispiel 3: Mehrere asynchrone Operationen ===**

```javascript
console.log("=== Beispiel 3: Mehrere async Ops ===");

console.log("Start");

setTimeout(() => {
  console.log("  → Timeout 1 (1000ms)");
}, 1000);

setTimeout(() => {
  console.log("  → Timeout 2 (500ms)");
}, 500);

setTimeout(() => {
  console.log("  → Timeout 3 (1500ms)");
}, 1500);

console.log("Alle Timeouts registriert");
console.log("--- Code läuft weiter ---");
```
@eval

    --{{3}}--
Die Ausgabe zeigt: Erst die synchronen Zeilen, dann die Callbacks in der Reihenfolge ihrer Verzögerung (500ms, 1000ms, 1500ms). JavaScript merkt sich die Callbacks und ruft sie zur richtigen Zeit auf.

</section>

---

### 5.2 Event Loop (Konzept)

    --{{0}}--
Der Event Loop ist das Herzstück von JavaScript. Er sorgt dafür, dass asynchrone Operationen funktionieren, obwohl JavaScript single-threaded ist. Verstehen Sie dieses Konzept, und Sie verstehen, warum Ihr Code manchmal "in falscher Reihenfolge" läuft!

    {{0}}
<section>

**=== Beispiel 1: Call Stack vs. Callback Queue ===**

```javascript
console.log("=== Beispiel 1: Event Loop Visualisierung ===");

console.log("1. Synchroner Code (Call Stack)");

setTimeout(() => {
  console.log("3. Callback aus Timeout (Callback Queue → Call Stack)");
}, 0); // 0ms Verzögerung!

console.log("2. Noch synchroner Code");

console.log("--- Ende Beispiel 1 ---");
// Warum ist "3." am Ende, obwohl timeout 0ms?
```
@eval

    --{{1}}--
Obwohl setTimeout 0ms hat, kommt der Callback NACH dem synchronen Code! Warum? Der Event Loop funktioniert so: 1) Call Stack komplett abarbeiten (synchroner Code), 2) dann Callbacks aus der Queue holen. setTimeout legt den Callback in die Queue, aber die wird erst NACH dem synchronen Code geleert.

</section>

    {{1}}
<section>

**=== Beispiel 2: Event Loop-Phasen ===**

```javascript
console.log("=== Beispiel 2: Event Loop Phasen ===");

// Phase 1: Synchroner Code
console.log("→ Phase 1: Call Stack (sync)");

// Phase 2: Microtasks (Promises)
Promise.resolve().then(() => {
  console.log("→ Phase 2a: Microtask (Promise)");
});

// Phase 3: Macrotasks (setTimeout)
setTimeout(() => {
  console.log("→ Phase 3: Macrotask (setTimeout)");
}, 0);

// Phase 2 nochmal
Promise.resolve().then(() => {
  console.log("→ Phase 2b: Noch ein Microtask");
});

console.log("→ Phase 1: Letzter sync Code");
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Die Reihenfolge ist: 1) Synchroner Code komplett, 2) ALLE Microtasks (Promises), 3) DANN Macrotasks (setTimeout). Promises haben höhere Priorität als setTimeout! Das ist wichtig für Datenbank-Code, denn fast alle DB-Libraries nutzen Promises.

</section>

    {{2}}
<section>

**=== Beispiel 3: Visualisierung mit DB-Query ===**

```javascript
console.log("=== Beispiel 3: Simulierte DB-Query ===");

function queryDatabase(id) {
  console.log(`  → DB-Query gestartet für ID ${id}`);
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → DB antwortet für ID ${id}`);
      resolve({ id, name: `User ${id}` });
    }, 1000);
  });
}

console.log("1. App startet");
console.log("2. Query wird abgeschickt");

queryDatabase(42).then((user) => {
  console.log("4. Daten empfangen:", user);
});

console.log("3. App läuft weiter (ohne zu blockieren)");
console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Perfekt! Die App startet die Query, läuft SOFORT weiter und verarbeitet das Ergebnis, wenn es ankommt. So funktionieren alle modernen Datenbank-Operationen: async, non-blocking, mit Promises.

</section>

---

### 5.3 Callbacks (alte Methode)

    --{{0}}--
Callbacks waren die erste Methode für asynchronen Code. Sie funktionieren, führen aber zu verschachteltem "Callback Hell". Moderne Projekte nutzen Promises und async/await, aber Sie sollten Callbacks verstehen, weil Sie ihnen noch begegnen werden.

    {{0}}
<section>

**=== Beispiel 1: Einfacher Callback ===**

```javascript
console.log("=== Beispiel 1: Einfacher Callback ===");

function fetchUser(id, callback) {
  console.log(`  → Lade User ${id}...`);
  setTimeout(() => {
    const user = { id, name: `User ${id}` };
    console.log(`  → User geladen:`, user);
    callback(user); // Callback aufrufen
  }, 1000);
}

console.log("Start");

fetchUser(1, (user) => {
  console.log("Callback erhält:", user);
  console.log(`Willkommen, ${user.name}!`);
});

console.log("Weiter...");
console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Der Callback wird als Funktion übergeben und später aufgerufen, wenn die Daten da sind. Das Prinzip ist einfach, aber...

</section>

    {{1}}
<section>

**=== Beispiel 2: Callback Hell (verschachtelt) ===**

```javascript
console.log("=== Beispiel 2: Callback Hell ===");

function getUser(id, callback) {
  setTimeout(() => callback({ id, name: `User ${id}` }), 500);
}

function getOrders(userId, callback) {
  setTimeout(() => callback([
    { orderId: 101, total: 99 },
    { orderId: 102, total: 149 }
  ]), 500);
}

function getOrderDetails(orderId, callback) {
  setTimeout(() => callback({ orderId, items: 3 }), 500);
}

console.log("Start verschachtelte Callbacks:");

getUser(1, (user) => {
  console.log("1. User:", user);
  getOrders(user.id, (orders) => {
    console.log("2. Orders:", orders);
    getOrderDetails(orders[0].orderId, (details) => {
      console.log("3. Details:", details);
      console.log("Fertig (nach 1.5s)");
    });
  });
});

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Das ist "Callback Hell" oder "Pyramid of Doom"! Jede asynchrone Operation ist eine Ebene tiefer verschachtelt. Das wird schnell unleserlich und fehleranfällig. Deshalb wurden Promises erfunden.

</section>

    {{2}}
<section>

**=== Beispiel 3: Error Handling mit Callbacks ===**

```javascript
console.log("=== Beispiel 3: Error Handling ===");

function fetchData(id, callback) {
  console.log(`  → Lade Daten für ID ${id}...`);
  setTimeout(() => {
    if (id < 0) {
      // Error als erstes Argument (Node.js-Konvention)
      callback(new Error("Ungültige ID"), null);
    } else {
      callback(null, { id, data: "Erfolg" });
    }
  }, 500);
}

fetchData(5, (error, data) => {
  if (error) {
    console.log("❌ Fehler:", error.message);
  } else {
    console.log("✅ Daten:", data);
  }
});

fetchData(-1, (error, data) => {
  if (error) {
    console.log("❌ Fehler:", error.message);
  } else {
    console.log("✅ Daten:", data);
  }
});

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Die Node.js-Konvention ist: Erster Parameter ist Error (oder null), zweiter ist Data. Sie müssen bei JEDEM Callback prüfen, ob ein Fehler vorliegt. Das ist fehleranfällig und mühsam. Promises machen das eleganter!

</section>

---

### 5.4 Promises (moderne Methode)

    --{{0}}--
Promises sind das moderne Gegenstück zu Callbacks. Ein Promise ist ein Objekt, das einen zukünftigen Wert repräsentiert. Promises können "pending", "fulfilled" (Erfolg) oder "rejected" (Fehler) sein. Sie verketten sich elegant mit .then() und .catch().

    {{0}}
<section>

**=== Beispiel 1: Promise erstellen ===**

```javascript
console.log("=== Beispiel 1: Promise erstellen ===");

const myPromise = new Promise((resolve, reject) => {
  console.log("  → Promise wird ausgeführt (sofort!)");
  setTimeout(() => {
    const success = true;
    if (success) {
      resolve("Erfolg! Hier sind die Daten.");
    } else {
      reject("Fehler! Etwas ist schief gelaufen.");
    }
  }, 1000);
});

console.log("Promise erstellt:", myPromise);
console.log("Status: pending (wartend)");

myPromise.then((data) => {
  console.log("✅ Promise fulfilled:", data);
});

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Ein Promise wird sofort ausgeführt (der Code im Constructor läuft synchron). Das Ergebnis kommt später. Mit .then() registrieren wir einen Handler für den Erfolgsfall.

</section>

    {{1}}
<section>

**=== Beispiel 2: Promise-Verkettung (Chaining) ===**

```javascript
console.log("=== Beispiel 2: Promise Chaining ===");

function getUser(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → User ${id} geladen`);
      resolve({ id, name: `User ${id}` });
    }, 500);
  });
}

function getOrders(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → Orders für User ${userId} geladen`);
      resolve([{ orderId: 101, total: 99 }]);
    }, 500);
  });
}

console.log("Start Chaining:");

getUser(1)
  .then((user) => {
    console.log("1. User:", user);
    return getOrders(user.id); // Nächstes Promise!
  })
  .then((orders) => {
    console.log("2. Orders:", orders);
    console.log("Fertig!");
  });

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Kein Callback Hell mehr! Promises verketten sich flach mit .then(). Jedes .then() kann ein neues Promise zurückgeben, und die Kette läuft automatisch weiter. Das ist deutlich lesbarer.

</section>

    {{2}}
<section>

**=== Beispiel 3: Error Handling mit .catch() ===**

```javascript
console.log("=== Beispiel 3: Promise Error Handling ===");

function fetchData(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id < 0) {
        reject(new Error(`Ungültige ID: ${id}`));
      } else {
        resolve({ id, data: "Erfolg" });
      }
    }, 500);
  });
}

console.log("Test 1: Gültige ID");
fetchData(5)
  .then((data) => {
    console.log("  ✅ Daten:", data);
  })
  .catch((error) => {
    console.log("  ❌ Fehler:", error.message);
  });

console.log("\nTest 2: Ungültige ID");
fetchData(-1)
  .then((data) => {
    console.log("  ✅ Daten:", data);
  })
  .catch((error) => {
    console.log("  ❌ Fehler:", error.message);
  });

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Mit .catch() fangen Sie alle Fehler in der Promise-Kette ab. Sie müssen nicht bei jedem .then() prüfen – ein .catch() am Ende reicht. Das ist eleganter und weniger fehleranfällig als Callbacks!

</section>

    {{3}}
<section>

**=== Beispiel 4: Promise.all() (parallel) ===**

```javascript
console.log("=== Beispiel 4: Promise.all() ===");

function fetchUser(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → User ${id} geladen`);
      resolve({ id, name: `User ${id}` });
    }, Math.random() * 1000);
  });
}

console.log("Lade 3 Users parallel:");

const promises = [
  fetchUser(1),
  fetchUser(2),
  fetchUser(3)
];

Promise.all(promises).then((users) => {
  console.log("\n✅ Alle Users geladen:");
  users.forEach(u => console.log(`  ${u.id}: ${u.name}`));
});

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{4}}--
Promise.all() startet mehrere Promises parallel und wartet, bis ALLE fertig sind. Das ist perfekt, wenn Sie mehrere Datenbank-Queries parallel ausführen wollen. Wenn ein Promise fehlschlägt, schlägt das ganze Promise.all() fehl.

</section>

    {{4}}
<section>

**=== Beispiel 5: Promise.race() (erster gewinnt) ===**

```javascript
console.log("=== Beispiel 5: Promise.race() ===");

function slowServer() {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("  → Slow Server antwortet (2s)");
      resolve("Slow Data");
    }, 2000);
  });
}

function fastServer() {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("  → Fast Server antwortet (500ms)");
      resolve("Fast Data");
    }, 500);
  });
}

console.log("Race zwischen zwei Servern:");

Promise.race([slowServer(), fastServer()]).then((result) => {
  console.log("✅ Erster Antwort:", result);
});

console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{5}}--
Promise.race() nimmt das Ergebnis des ERSTEN Promises, das fertig wird. Nützlich für Timeouts: Starten Sie eine Query und ein Timeout-Promise parallel, und wenn das Timeout zuerst fertig ist, brechen Sie ab.

</section>

---

### 5.5 async/await (modernste Methode)

    --{{0}}--
async/await ist syntaktischer Zucker über Promises. Es macht asynchronen Code aussehen wie synchronen Code – aber ohne zu blockieren! Das ist der Standard für moderne JavaScript-Entwicklung und das, was Sie in Ihrem Datenbank-Code verwenden werden.

    {{0}}
<section>

**=== Beispiel 1: async-Funktion basics ===**

```javascript
console.log("=== Beispiel 1: async/await basics ===");

// async-Funktion gibt IMMER ein Promise zurück
async function fetchData() {
  console.log("  → Funktion startet");
  return "Daten"; // Wird automatisch in Promise.resolve("Daten") gewrappt
}

console.log("Vor Aufruf");
const promise = fetchData();
console.log("Promise:", promise);

promise.then((data) => {
  console.log("Daten erhalten:", data);
});

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Jede Funktion mit async davor gibt automatisch ein Promise zurück. Das return-Statement wird zu resolve(). Das ist die Basis von async/await.

</section>

    {{1}}
<section>

**=== Beispiel 2: await (auf Promise warten) ===**

```javascript
console.log("=== Beispiel 2: await ===");

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
  console.log("  → Start");
  
  console.log("  → Warte 1 Sekunde...");
  await delay(1000); // Wartet auf Promise
  console.log("  → 1 Sekunde vorbei");
  
  console.log("  → Warte noch 1 Sekunde...");
  await delay(1000);
  console.log("  → 2 Sekunden vorbei");
  
  return "Fertig!";
}

console.log("Vor Aufruf");
demo().then(result => console.log("Ergebnis:", result));
console.log("Nach Aufruf (läuft weiter!)");
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
await pausiert die Funktion, bis das Promise fertig ist – OHNE den Thread zu blockieren! Der Code danach läuft sofort weiter ("Nach Aufruf"). Innerhalb von demo() sieht der Code synchron aus, ist aber asynchron.

</section>

    {{2}}
<section>

**=== Beispiel 3: DB-Query mit async/await ===**

```javascript
console.log("=== Beispiel 3: DB-Query ===");

function queryDB(sql) {
  return new Promise((resolve) => {
    console.log(`  → Query: ${sql}`);
    setTimeout(() => {
      resolve([{ id: 1, name: "Alice" }, { id: 2, name: "Bob" }]);
    }, 1000);
  });
}

async function getUsers() {
  console.log("→ Lade Users...");
  const users = await queryDB("SELECT * FROM users");
  console.log("→ Users geladen:", users.length);
  return users;
}

console.log("Start");
getUsers().then((users) => {
  console.log("✅ Ergebnis:");
  users.forEach(u => console.log(`  ${u.id}: ${u.name}`));
});
console.log("Weiter...");
console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Perfekt! Der Code in getUsers() sieht synchron aus: Zeile für Zeile. Aber er blockiert nicht! Das ist der große Vorteil von async/await: Lesbarkeit wie synchroner Code, Verhalten von asynchronem Code.

</section>

    {{3}}
<section>

**=== Beispiel 4: Sequentielle Operationen ===**

```javascript
console.log("=== Beispiel 4: Sequentiell ===");

function query(name, delay) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → ${name} fertig`);
      resolve(`Data from ${name}`);
    }, delay);
  });
}

async function sequential() {
  console.log("→ Start (sequentiell)");
  const start = Date.now();
  
  const a = await query("Query A", 1000); // Wartet 1s
  const b = await query("Query B", 1000); // Wartet 1s
  const c = await query("Query C", 1000); // Wartet 1s
  
  const duration = Date.now() - start;
  console.log(`✅ Fertig nach ${duration}ms`);
  return [a, b, c];
}

sequential().then(results => console.log("Results:", results));
console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{4}}--
Achtung! Hier dauert es 3 Sekunden, weil jedes await nacheinander wartet. Wenn die Queries unabhängig sind, ist das ineffizient. Besser: parallel ausführen!

</section>

    {{4}}
<section>

**=== Beispiel 5: Parallele Operationen ===**

```javascript
console.log("=== Beispiel 5: Parallel ===");

function query(name, delay) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → ${name} fertig`);
      resolve(`Data from ${name}`);
    }, delay);
  });
}

async function parallel() {
  console.log("→ Start (parallel)");
  const start = Date.now();
  
  // Queries SOFORT starten (nicht awaiten!)
  const promiseA = query("Query A", 1000);
  const promiseB = query("Query B", 1000);
  const promiseC = query("Query C", 1000);
  
  // DANN auf alle warten
  const results = await Promise.all([promiseA, promiseB, promiseC]);
  
  const duration = Date.now() - start;
  console.log(`✅ Fertig nach ${duration}ms`);
  return results;
}

parallel().then(results => console.log("Results:", results));
console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{5}}--
Jetzt nur 1 Sekunde! Die Queries laufen parallel. Merken Sie sich: Promises SOFORT starten (ohne await), DANN mit Promise.all() auf alle warten. Das ist ein häufiges Pattern in Datenbank-Code.

</section>

---

### 5.6 Error Handling mit try/catch

    --{{0}}--
Mit async/await können Sie try/catch nutzen – wie bei synchronem Code! Das ist ein großer Vorteil gegenüber Promise-Chaining mit .catch().

    {{0}}
<section>

**=== Beispiel 1: try/catch mit async/await ===**

```javascript
console.log("=== Beispiel 1: try/catch ===");

function riskyQuery(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id < 0) {
        reject(new Error(`Ungültige ID: ${id}`));
      } else {
        resolve({ id, data: "Erfolg" });
      }
    }, 500);
  });
}

async function fetchData(id) {
  try {
    console.log(`→ Lade Daten für ID ${id}...`);
    const data = await riskyQuery(id);
    console.log("✅ Erfolg:", data);
    return data;
  } catch (error) {
    console.log("❌ Fehler gefangen:", error.message);
    return null;
  }
}

fetchData(5);
fetchData(-1);
console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Perfekt! try/catch funktioniert mit await wie mit normalem synchronem Code. Wenn das Promise rejected wird, fliegt eine Exception, die Sie mit catch abfangen.

</section>

    {{1}}
<section>

**=== Beispiel 2: Multiple Queries mit Error Handling ===**

```javascript
console.log("=== Beispiel 2: Multiple Queries ===");

function query(name, shouldFail = false) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error(`${name} failed`));
      } else {
        resolve(`Data from ${name}`);
      }
    }, 500);
  });
}

async function loadAll() {
  try {
    console.log("→ Lade User...");
    const user = await query("User");
    console.log("  ✅", user);
    
    console.log("→ Lade Orders...");
    const orders = await query("Orders", true); // Fails!
    console.log("  ✅", orders);
    
    console.log("→ Lade Profile...");
    const profile = await query("Profile");
    console.log("  ✅", profile);
    
  } catch (error) {
    console.log("❌ Ein Query ist fehlgeschlagen:", error.message);
    console.log("   Folgende Queries werden nicht ausgeführt!");
  }
}

loadAll();
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Wichtig! Wenn ein await fehlschlägt, springt der Code sofort in den catch-Block. Die folgenden Queries (Profile) werden nicht ausgeführt. Das ist oft gewollt, aber manchmal wollen Sie weitermachen...

</section>

    {{2}}
<section>

**=== Beispiel 3: Einzelne Fehler abfangen ===**

```javascript
console.log("=== Beispiel 3: Einzelne Fehler ===");

function query(name, shouldFail = false) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error(`${name} failed`));
      } else {
        resolve(`Data from ${name}`);
      }
    }, 500);
  });
}

async function loadAllRobust() {
  let user, orders, profile;
  
  try {
    user = await query("User");
    console.log("✅ User:", user);
  } catch (error) {
    console.log("❌ User fehlgeschlagen:", error.message);
  }
  
  try {
    orders = await query("Orders", true); // Fails!
    console.log("✅ Orders:", orders);
  } catch (error) {
    console.log("❌ Orders fehlgeschlagen:", error.message);
  }
  
  try {
    profile = await query("Profile");
    console.log("✅ Profile:", profile);
  } catch (error) {
    console.log("❌ Profile fehlgeschlagen:", error.message);
  }
  
  console.log("\n→ Ergebnis:");
  console.log("  User:", user || "null");
  console.log("  Orders:", orders || "null");
  console.log("  Profile:", profile || "null");
}

loadAllRobust();
console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Jetzt läuft alles durch! Jede Query hat ihr eigenes try/catch. Wenn eine fehlschlägt, geht es mit der nächsten weiter. Das ist robuster, wenn Sie unabhängige Queries haben.

</section>

---

### 5.7 Übung: Asynchronität

    --{{0}}--
Jetzt sind Sie dran! Diese Übungen simulieren echte Datenbank-Szenarien mit async/await. Nutzen Sie try/catch für Fehler und Promise.all() für parallele Queries.

    {{0}}
<section>

**Aufgabe 1: Sequentielle DB-Queries**

```javascript
// Gegeben:
function getUser(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id, name: `User ${id}`, roleId: id * 10 });
    }, 500);
  });
}

function getRole(roleId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const roles = { 10: "Admin", 20: "Editor", 30: "Viewer" };
      resolve({ roleId, name: roles[roleId] || "Unknown" });
    }, 500);
  });
}

// Aufgabe: Schreiben Sie eine async-Funktion getUserWithRole(id),
// die zuerst den User lädt, dann dessen Role lädt und beides kombiniert zurückgibt.
// Ergebnis: { id: 1, name: "User 1", role: "Admin" }

console.log("=== Aufgabe 1 ===");

// Ihr Code hier:
// async function getUserWithRole(id) { ... }

// Test:
// getUserWithRole(1).then(result => console.log("Result:", result));
```
@eval

**Aufgabe 2: Parallele Queries mit Promise.all()**

```javascript
// Gegeben:
function fetchProduct(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id, name: `Product ${id}`, price: id * 100 });
    }, Math.random() * 1000);
  });
}

// Aufgabe: Laden Sie die Produkte mit IDs [1, 2, 3, 4, 5] PARALLEL
// und geben Sie die Gesamtsumme aller Preise aus.

console.log("=== Aufgabe 2 ===");

// Ihr Code hier:
```
@eval

**Aufgabe 3: Error Handling**

```javascript
// Gegeben:
function riskyQuery(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id === 3) {
        reject(new Error(`Query für ID ${id} fehlgeschlagen`));
      } else {
        resolve({ id, data: `Data ${id}` });
      }
    }, 500);
  });
}

// Aufgabe: Laden Sie Daten für IDs [1, 2, 3, 4] nacheinander.
// Wenn eine Query fehlschlägt, loggen Sie den Fehler und machen Sie weiter.
// Am Ende: Zeigen Sie, welche Queries erfolgreich waren.

console.log("=== Aufgabe 3 ===");

// Ihr Code hier:
```
@eval

</section>

    --{{1}}--
Diese Übungen sind realistisch! Fast jede Datenbank-Interaktion folgt diesem Muster: Queries starten, auf Ergebnisse warten, Fehler behandeln. Wenn Sie das können, sind Sie bereit für echten DB-Code!

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (Sequentielle Queries)</summary>

```javascript
console.log("=== Aufgabe 1: Sequentiell ===");

function getUser(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → User ${id} geladen`);
      resolve({ id, name: `User ${id}`, roleId: id * 10 });
    }, 500);
  });
}

function getRole(roleId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const roles = { 10: "Admin", 20: "Editor", 30: "Viewer" };
      console.log(`  → Role ${roleId} geladen`);
      resolve({ roleId, name: roles[roleId] || "Unknown" });
    }, 500);
  });
}

async function getUserWithRole(id) {
  console.log(`→ Lade User ${id}...`);
  const user = await getUser(id);
  
  console.log(`→ Lade Role ${user.roleId}...`);
  const role = await getRole(user.roleId);
  
  const result = {
    id: user.id,
    name: user.name,
    role: role.name
  };
  
  console.log("✅ Ergebnis:", result);
  return result;
}

getUserWithRole(1);
getUserWithRole(2);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Parallel mit Promise.all)</summary>

```javascript
console.log("=== Aufgabe 2: Parallel ===");

function fetchProduct(id) {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(`  → Product ${id} geladen`);
      resolve({ id, name: `Product ${id}`, price: id * 100 });
    }, Math.random() * 1000);
  });
}

async function getTotalPrice() {
  console.log("→ Lade Produkte parallel...");
  
  const ids = [1, 2, 3, 4, 5];
  const promises = ids.map(id => fetchProduct(id));
  
  const products = await Promise.all(promises);
  
  console.log("\n→ Alle Produkte geladen:");
  products.forEach(p => console.log(`  ${p.name}: ${p.price}€`));
  
  const total = products.reduce((sum, p) => sum + p.price, 0);
  console.log(`\n✅ Gesamtsumme: ${total}€`);
  
  return total;
}

getTotalPrice();
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Error Handling)</summary>

```javascript
console.log("=== Aufgabe 3: Error Handling ===");

function riskyQuery(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id === 3) {
        reject(new Error(`Query für ID ${id} fehlgeschlagen`));
      } else {
        resolve({ id, data: `Data ${id}` });
      }
    }, 500);
  });
}

async function loadAllWithErrorHandling() {
  const ids = [1, 2, 3, 4];
  const results = [];
  
  for (const id of ids) {
    try {
      console.log(`\n→ Lade ID ${id}...`);
      const data = await riskyQuery(id);
      console.log(`  ✅ Erfolg:`, data);
      results.push(data);
    } catch (error) {
      console.log(`  ❌ Fehler:`, error.message);
      console.log(`  → Weiter mit nächster Query...`);
    }
  }
  
  console.log(`\n✅ Fertig: ${results.length}/${ids.length} erfolgreich`);
  console.log("Erfolgreiche Queries:", results);
}

loadAllWithErrorHandling();
```
@eval

</details>

</section>

    --{{2}}--
Hervorragend! Sie haben jetzt das Rüstzeug für asynchrone Programmierung. async/await ist der moderne Standard, und Sie werden es in JEDER Datenbank-Operation nutzen. PouchDB, IndexedDB, REST-APIs – alles basiert auf Promises und async/await!

---

## Kapitel 6: JSON – Das Datenformat des Web

    --{{0}}--
JSON (JavaScript Object Notation) ist DAS Austauschformat für Datenbanken und APIs. Fast jede moderne Datenbank arbeitet mit JSON: REST-APIs senden JSON, NoSQL-Datenbanken speichern JSON, und selbst SQL-Datenbanken haben JSON-Spalten. Dieses Kapitel ist kurz aber absolut essenziell!

---

### 6.1 JSON Syntax – Die Regeln

    --{{0}}--
JSON sieht aus wie JavaScript-Objekte, hat aber strengere Regeln. Verstehen Sie die Unterschiede, um Fehler zu vermeiden!

    {{0}}
<section>

**=== Beispiel 1: Gültiges JSON ===**

```javascript
console.log("=== Beispiel 1: Gültiges JSON ===");

const validJSON = `{
  "name": "Alice",
  "age": 28,
  "isActive": true,
  "roles": ["admin", "editor"],
  "address": {
    "city": "Berlin",
    "zip": "10115"
  },
  "salary": null
}`;

console.log("JSON String:");
console.log(validJSON);

console.log("\nJSON-Regeln:");
console.log("✅ Property-Namen in doppelten Anführungszeichen");
console.log("✅ Strings in doppelten Anführungszeichen");
console.log("✅ Zahlen, Booleans, null erlaubt");
console.log("✅ Arrays und Objekte verschachtelt erlaubt");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Die wichtigsten Regeln: Property-Namen MÜSSEN in doppelten Anführungszeichen sein. Strings MÜSSEN in doppelten Anführungszeichen sein. Kein trailing comma, keine Kommentare, keine Funktionen, kein undefined.

</section>

    {{1}}
<section>

**=== Beispiel 2: Ungültiges JSON (häufige Fehler) ===**

```javascript
console.log("=== Beispiel 2: Ungültiges JSON ===");

// Fehler 1: Einfache Anführungszeichen
const invalid1 = `{ 'name': 'Alice' }`;
console.log("❌ Einfache Quotes:", invalid1);

// Fehler 2: Keine Quotes bei Property-Namen
const invalid2 = `{ name: "Alice" }`;
console.log("❌ Keine Quotes bei Key:", invalid2);

// Fehler 3: Trailing Comma
const invalid3 = `{ "name": "Alice", }`;
console.log("❌ Trailing Comma:", invalid3);

// Fehler 4: undefined (nicht erlaubt)
const invalid4 = `{ "name": undefined }`;
console.log("❌ undefined:", invalid4);

// Fehler 5: Funktionen (nicht erlaubt)
const invalid5 = `{ "getName": function() {} }`;
console.log("❌ Funktion:", invalid5);

console.log("\n→ Keines dieser Beispiele ist gültiges JSON!");
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Diese Fehler passieren ständig! JavaScript-Objekte sind permissiver als JSON. Wenn Sie JSON.parse() mit diesen Strings aufrufen, gibt es einen SyntaxError.

</section>

    {{2}}
<section>

**=== Beispiel 3: Was JSON NICHT kann ===**

```javascript
console.log("=== Beispiel 3: JSON Einschränkungen ===");

console.log("JSON kann NICHT darstellen:");
console.log("  ❌ undefined");
console.log("  ❌ Funktionen");
console.log("  ❌ Symbol");
console.log("  ❌ Date-Objekte (werden zu Strings)");
console.log("  ❌ RegExp");
console.log("  ❌ Map, Set");
console.log("  ❌ Zirkuläre Referenzen");
console.log("  ❌ NaN, Infinity (werden zu null)");

console.log("\nJSON kann darstellen:");
console.log("  ✅ Strings");
console.log("  ✅ Numbers");
console.log("  ✅ Booleans (true/false)");
console.log("  ✅ null");
console.log("  ✅ Arrays");
console.log("  ✅ Objects (Plain Objects)");

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
JSON ist ein Datenaustauschformat, kein vollständiger Ersatz für JavaScript-Objekte. Es ist absichtlich einfach gehalten, damit es sprachunabhängig ist (Python, Java, C# können es auch verarbeiten).

</section>

---

### 6.2 JSON.parse() und JSON.stringify()

    --{{0}}--
Die beiden wichtigsten Funktionen: JSON.stringify() verwandelt JavaScript-Objekte in JSON-Strings. JSON.parse() verwandelt JSON-Strings zurück in JavaScript-Objekte. Sie werden diese Funktionen ständig nutzen!

    {{0}}
<section>

**=== Beispiel 1: JSON.stringify() – Objekt zu String ===**

```javascript
console.log("=== Beispiel 1: JSON.stringify() ===");

const user = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  roles: ["admin", "editor"],
  settings: {
    theme: "dark",
    language: "de"
  }
};

console.log("JavaScript-Objekt:");
console.log(user);

const jsonString = JSON.stringify(user);
console.log("\nJSON String:");
console.log(jsonString);

console.log("\nTyp:");
console.log("  user:", typeof user);
console.log("  jsonString:", typeof jsonString);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
JSON.stringify() konvertiert das Objekt in einen String. Dieser String kann über das Netzwerk geschickt, in einer Datei gespeichert oder in einer Datenbank abgelegt werden.

</section>

    {{1}}
<section>

**=== Beispiel 2: JSON.parse() – String zu Objekt ===**

```javascript
console.log("=== Beispiel 2: JSON.parse() ===");

const jsonString = `{
  "id": 42,
  "name": "Bob",
  "isActive": true,
  "scores": [85, 92, 78]
}`;

console.log("JSON String:");
console.log(jsonString);
console.log("Typ:", typeof jsonString);

const obj = JSON.parse(jsonString);
console.log("\nGeparst als Objekt:");
console.log(obj);
console.log("Typ:", typeof obj);

console.log("\nZugriff auf Properties:");
console.log("  Name:", obj.name);
console.log("  Scores:", obj.scores);
console.log("  Erster Score:", obj.scores[0]);

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
JSON.parse() verwandelt den String zurück in ein nutzbares JavaScript-Objekt. Jetzt können Sie mit den Daten arbeiten: Properties lesen, Arrays durchlaufen, etc.

</section>

    {{2}}
<section>

**=== Beispiel 3: Prettify mit stringify() ===**

```javascript
console.log("=== Beispiel 3: Prettify ===");

const data = {
  users: [
    { id: 1, name: "Alice", age: 28 },
    { id: 2, name: "Bob", age: 34 }
  ],
  total: 2
};

console.log("Ohne Formatierung:");
console.log(JSON.stringify(data));

console.log("\nMit Formatierung (Indent 2):");
const pretty = JSON.stringify(data, null, 2);
console.log(pretty);

console.log("\nMit Formatierung (Indent 4):");
const prettyWide = JSON.stringify(data, null, 4);
console.log(prettyWide);

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Der dritte Parameter von JSON.stringify() ist der Indent. Mit 2 oder 4 Leerzeichen wird das JSON lesbar formatiert. Das ist nützlich zum Debuggen oder wenn Sie JSON-Dateien per Hand editieren.

</section>

    {{3}}
<section>

**=== Beispiel 4: Roundtrip (hin und zurück) ===**

```javascript
console.log("=== Beispiel 4: Roundtrip ===");

const original = {
  product: "Laptop",
  price: 999,
  tags: ["electronics", "computers"]
};

console.log("1. Original Object:");
console.log(original);

const json = JSON.stringify(original);
console.log("\n2. Als JSON String:");
console.log(json);

const parsed = JSON.parse(json);
console.log("\n3. Zurück als Object:");
console.log(parsed);

console.log("\n4. Vergleich:");
console.log("  Sind gleich (Werte)?", 
  JSON.stringify(original) === JSON.stringify(parsed));
console.log("  Sind gleich (Referenz)?", original === parsed);

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{4}}--
Wichtig! Nach dem Roundtrip haben Sie ein neues Objekt mit denselben Werten, aber einer anderen Referenz. Das ist kein Problem – die Daten sind identisch.

</section>

    {{4}}
<section>

**=== Beispiel 5: API-Response simulieren ===**

```javascript
console.log("=== Beispiel 5: API Response ===");

// Simuliere eine API-Response (als String vom Server)
const apiResponse = `{
  "status": "success",
  "data": {
    "users": [
      { "id": 1, "name": "Alice", "email": "alice@example.com" },
      { "id": 2, "name": "Bob", "email": "bob@example.com" }
    ]
  },
  "timestamp": "2024-10-21T10:30:00Z"
}`;

console.log("API Response (String):");
console.log(apiResponse);

const response = JSON.parse(apiResponse);
console.log("\nGeparst:");
console.log("  Status:", response.status);
console.log("  User-Count:", response.data.users.length);

response.data.users.forEach(user => {
  console.log(`  → ${user.name} (${user.email})`);
});

console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{5}}--
Das ist das typische Pattern: Server sendet JSON-String, Sie parsen ihn mit JSON.parse(), verarbeiten die Daten. Später stringify Sie Ihre Antwort und senden sie zurück. Das ist der Standard für REST-APIs!

</section>

---

### 6.3 JSON vs. JavaScript-Objekte

    --{{0}}--
JSON und JavaScript-Objekte sehen ähnlich aus, sind aber NICHT dasselbe! Dieser Unterschied ist wichtig zu verstehen.

    {{0}}
<section>

**=== Beispiel 1: Unterschiede im Detail ===**

```javascript
console.log("=== Beispiel 1: JSON vs. JS-Objekt ===");

// JavaScript-Objekt (permissiv)
const jsObject = {
  name: "Alice",              // Keine Quotes bei Key
  'age': 28,                  // Einfache Quotes OK
  "email": "alice@ex.com",    // Doppelte Quotes OK
  isActive: true,
  greet: function() {         // Funktionen OK
    return "Hello!";
  },
  metadata: undefined,        // undefined OK
  tags: ["admin", "editor",]  // Trailing comma OK
};

console.log("JavaScript-Objekt:");
console.log(jsObject);
console.log("  Function:", jsObject.greet());

// Zu JSON konvertieren
const json = JSON.stringify(jsObject);
console.log("\nAls JSON:");
console.log(json);

console.log("\n❌ Verloren beim Konvertieren:");
console.log("  - greet() Funktion");
console.log("  - metadata (war undefined)");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Beim Konvertieren nach JSON gehen Funktionen und undefined verloren! JSON.stringify() ignoriert sie einfach. Das ist kein Bug, sondern beabsichtigt – JSON ist für Daten, nicht für Code.

</section>

    {{1}}
<section>

**=== Beispiel 2: Date-Objekte in JSON ===**

```javascript
console.log("=== Beispiel 2: Date in JSON ===");

const event = {
  title: "Meeting",
  date: new Date("2024-10-21T10:00:00"),
  location: "Berlin"
};

console.log("Original:");
console.log("  Date:", event.date);
console.log("  Typ:", typeof event.date);
console.log("  getFullYear():", event.date.getFullYear());

const json = JSON.stringify(event);
console.log("\nAls JSON:");
console.log(json);

const parsed = JSON.parse(json);
console.log("\nZurück geparst:");
console.log("  Date:", parsed.date);
console.log("  Typ:", typeof parsed.date);
console.log("  ❌ getFullYear() existiert nicht mehr!");

console.log("\nLösung: Manuell zurück konvertieren");
parsed.date = new Date(parsed.date);
console.log("  Date:", parsed.date);
console.log("  getFullYear():", parsed.date.getFullYear());

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Date-Objekte werden zu ISO-Strings konvertiert. Nach dem Parsen sind sie einfache Strings! Sie müssen sie manuell zurück in Date-Objekte konvertieren. Das ist ein häufiger Stolperstein.

</section>

    {{2}}
<section>

**=== Beispiel 3: NaN und Infinity ===**

```javascript
console.log("=== Beispiel 3: NaN und Infinity ===");

const numbers = {
  normal: 42,
  notANumber: NaN,
  infinite: Infinity,
  negInfinite: -Infinity
};

console.log("Original:");
console.log(numbers);

const json = JSON.stringify(numbers);
console.log("\nAls JSON:");
console.log(json);

const parsed = JSON.parse(json);
console.log("\nZurück geparst:");
console.log(parsed);

console.log("\n❌ NaN und Infinity wurden zu null!");
console.log("  notANumber:", parsed.notANumber);
console.log("  infinite:", parsed.infinite);

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
NaN und Infinity gibt es in JSON nicht! Sie werden zu null konvertiert. Wenn Sie diese Werte brauchen, müssen Sie sie anders kodieren (z.B. als Strings).

</section>

---

### 6.4 Deep Copy mit JSON

    --{{0}}--
Ein cleverer Trick: JSON.stringify() + JSON.parse() erzeugt eine tiefe Kopie eines Objekts. Aber Vorsicht: Funktionen und andere nicht-JSON-Typen gehen verloren!

    {{0}}
<section>

**=== Beispiel 1: Shallow vs. Deep Copy ===**

```javascript
console.log("=== Beispiel 1: Shallow vs. Deep Copy ===");

const original = {
  name: "Alice",
  scores: [85, 90, 92]
};

// Shallow Copy (Spread)
const shallow = { ...original };

// Deep Copy (JSON Trick)
const deep = JSON.parse(JSON.stringify(original));

console.log("Original:", original);
console.log("Shallow Copy:", shallow);
console.log("Deep Copy:", deep);

console.log("\nÄndere original.scores[0]:");
original.scores[0] = 999;

console.log("  Original:", original.scores);
console.log("  Shallow:", shallow.scores);  // AUCH geändert! ❌
console.log("  Deep:", deep.scores);        // NICHT geändert! ✅

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Shallow Copy kopiert nur die erste Ebene. Nested Arrays/Objects werden referenziert! Deep Copy mit JSON erzeugt eine komplette Kopie. Änderungen am Original beeinflussen die Deep Copy nicht.

</section>

    {{1}}
<section>

**=== Beispiel 2: Deep Copy mit komplexen Daten ===**

```javascript
console.log("=== Beispiel 2: Deep Copy komplexer Daten ===");

const dbResult = {
  users: [
    { id: 1, name: "Alice", meta: { lastLogin: "2024-10-20" } },
    { id: 2, name: "Bob", meta: { lastLogin: "2024-10-19" } }
  ],
  pagination: {
    page: 1,
    perPage: 10,
    total: 2
  }
};

console.log("Original DB Result:");
console.log(dbResult);

// Deep Copy für Verarbeitung
const workingCopy = JSON.parse(JSON.stringify(dbResult));

console.log("\nModifiziere Working Copy:");
workingCopy.users[0].name = "ALICE (Modified)";
workingCopy.pagination.page = 2;

console.log("\nOriginal (unverändert):");
console.log("  User 1:", dbResult.users[0].name);
console.log("  Page:", dbResult.pagination.page);

console.log("\nWorking Copy (geändert):");
console.log("  User 1:", workingCopy.users[0].name);
console.log("  Page:", workingCopy.pagination.page);

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Das ist nützlich, wenn Sie mit Datenbank-Resultaten arbeiten! Sie können eine Deep Copy machen, die Daten transformieren, ohne das Original zu beeinflussen. Perfekt für "Dry Run" Tests oder Vorschau-Funktionen.

</section>

    {{2}}
<section>

**=== Beispiel 3: Grenzen des JSON-Copy-Tricks ===**

```javascript
console.log("=== Beispiel 3: Grenzen des JSON-Tricks ===");

const complex = {
  name: "Test",
  date: new Date("2024-10-21"),
  regex: /test/gi,
  func: function() { return "Hello"; },
  undef: undefined,
  nan: NaN,
  inf: Infinity
};

console.log("Original:");
console.log(complex);

const copy = JSON.parse(JSON.stringify(complex));

console.log("\nCopy:");
console.log(copy);

console.log("\n❌ Verloren/Verändert:");
console.log("  date: Date → String");
console.log("  regex: Verschwunden");
console.log("  func: Verschwunden");
console.log("  undef: Verschwunden");
console.log("  nan: NaN → null");
console.log("  inf: Infinity → null");

console.log("\n→ Für Plain Objects (Daten) OK");
console.log("→ Für komplexe Objekte: structuredClone() nutzen!");

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Der JSON-Trick funktioniert nur für Plain Objects! Für komplexe Objekte mit Dates, RegExp, etc. gibt es seit 2022 structuredClone() im Browser. Aber für typische Datenbank-Daten (Plain Objects) ist der JSON-Trick perfekt.

</section>

---

### 6.5 Häufige Fehler mit JSON

    --{{0}}--
Diese Fehler passieren ständig! Lernen Sie sie kennen, damit Sie sie schnell erkennen und fixen können.

    {{0}}
<section>

**=== Beispiel 1: SyntaxError beim Parsen ===**

```javascript
console.log("=== Beispiel 1: SyntaxError ===");

const invalidJSON = `{
  "name": "Alice",
  "age": 28,
}`;  // Trailing Comma!

console.log("Versuche zu parsen:");
console.log(invalidJSON);

try {
  const parsed = JSON.parse(invalidJSON);
  console.log("✅ Erfolgreich:", parsed);
} catch (error) {
  console.log("❌ Fehler:", error.message);
  console.log("   Problem: Trailing Comma nach age");
}

console.log("\nKorrektur:");
const validJSON = `{ "name": "Alice", "age": 28 }`;
const parsed = JSON.parse(validJSON);
console.log("✅", parsed);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Trailing Commas sind in JavaScript-Objekten OK, aber in JSON verboten! JSON.parse() wirft einen SyntaxError. Immer mit try/catch abfangen, wenn JSON von außen kommt!

</section>

    {{1}}
<section>

**=== Beispiel 2: Zirkuläre Referenzen ===**

```javascript
console.log("=== Beispiel 2: Zirkuläre Referenzen ===");

const user = {
  name: "Alice",
  friends: []
};

const friend = {
  name: "Bob",
  friends: []
};

// Zirkulär: user → friend → user
user.friends.push(friend);
friend.friends.push(user);

console.log("User:", user.name);
console.log("  Friend:", user.friends[0].name);
console.log("  Friend's Friend:", user.friends[0].friends[0].name);

console.log("\nVersuche zu stringifyen:");
try {
  const json = JSON.stringify(user);
  console.log("✅", json);
} catch (error) {
  console.log("❌ Fehler:", error.message);
  console.log("   → JSON kann keine zirkulären Referenzen!");
}

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Zirkuläre Referenzen (A zeigt auf B, B zeigt auf A) werfen einen TypeError. JSON kann das nicht darstellen. Lösung: Referenzen durch IDs ersetzen oder spezielle Libraries nutzen.

</section>

    {{2}}
<section>

**=== Beispiel 3: Vergessenes Parse/Stringify ===**

```javascript
console.log("=== Beispiel 3: Vergessenes Parse ===");

// API gibt JSON-String zurück
const apiResponse = `{"status":"success","count":5}`;

console.log("API Response (String):");
console.log(apiResponse);
console.log("Typ:", typeof apiResponse);

// Häufiger Fehler: Direkt zugreifen
console.log("\n❌ Versuch ohne Parse:");
console.log("  apiResponse.status:", apiResponse.status);
console.log("  → undefined! Es ist ein String!");

// Richtig: Erst parsen
console.log("\n✅ Mit Parse:");
const data = JSON.parse(apiResponse);
console.log("  data.status:", data.status);
console.log("  data.count:", data.count);

// Umgekehrt: Vergessenes Stringify
console.log("\nSenden an Server:");
const requestData = { query: "users", limit: 10 };
console.log("  ❌ Objekt senden:", requestData);
console.log("  ✅ JSON senden:", JSON.stringify(requestData));

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Das ist der häufigste Anfängerfehler! JSON-Strings sind Strings, keine Objekte. Sie müssen erst parsen. Und beim Senden müssen Sie stringify. Merksatz: Empfangen → parse(), Senden → stringify().

</section>

---

### 6.6 Übung: JSON

    --{{0}}--
Jetzt sind Sie dran! Diese Übungen simulieren typische JSON-Operationen mit Datenbanken und APIs.

    {{0}}
<section>

**Aufgabe 1: API Response verarbeiten**

```javascript
// Gegeben: API-Response als JSON-String
const apiResponse = `{
  "status": "success",
  "data": {
    "products": [
      { "id": 1, "name": "Laptop", "price": 999, "stock": 5 },
      { "id": 2, "name": "Mouse", "price": 29, "stock": 0 },
      { "id": 3, "name": "Keyboard", "price": 79, "stock": 12 }
    ]
  }
}`;

// Aufgabe:
// 1. Parse den JSON-String
// 2. Filtere nur Produkte mit stock > 0
// 3. Erstelle ein neues Objekt mit verfügbaren Produkten
// 4. Stringify das Ergebnis (pretty printed mit Indent 2)

console.log("=== Aufgabe 1 ===");

// Ihr Code hier:
```
@eval

**Aufgabe 2: Deep Copy und Modifikation**

```javascript
// Gegeben: Datenbank-Dokument
const dbDocument = {
  _id: "user_123",
  name: "Alice",
  email: "alice@example.com",
  orders: [
    { orderId: 101, total: 99, items: ["Laptop"] },
    { orderId: 102, total: 29, items: ["Mouse", "Pad"] }
  ],
  metadata: {
    createdAt: "2024-01-15",
    updatedAt: "2024-10-20"
  }
};

// Aufgabe:
// 1. Erstelle eine Deep Copy des Dokuments
// 2. Ändere in der Copy: name zu "ALICE", email zu "alice.new@example.com"
// 3. Füge einen neuen Order hinzu: { orderId: 103, total: 149, items: ["Monitor"] }
// 4. Zeige, dass das Original unverändert ist

console.log("=== Aufgabe 2 ===");

// Ihr Code hier:
```
@eval

**Aufgabe 3: Error Handling beim Parsen**

```javascript
// Gegeben: Mehrere API-Responses (einige ungültig)
const responses = [
  `{"status":"success","data":{"count":5}}`,
  `{"status":"success","data":{"count":10},}`,  // Trailing comma!
  `{'status':'error'}`,  // Single quotes!
  `{"status":"success","data":null}`
];

// Aufgabe:
// 1. Versuche jede Response zu parsen
// 2. Bei Erfolg: Logge den status
// 3. Bei Fehler: Logge den Fehler und mache weiter
// 4. Zähle am Ende: Wie viele waren valid, wie viele invalid?

console.log("=== Aufgabe 3 ===");

// Ihr Code hier:
```
@eval

</section>

    --{{1}}--
Diese Übungen sind praxisnah! Fast jede API-Interaktion folgt diesem Muster: JSON empfangen, parsen, verarbeiten, stringify, senden. Wenn Sie das können, sind Sie bereit für echte Datenbank-Arbeit!

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (API Response)</summary>

```javascript
console.log("=== Aufgabe 1: API Response ===");

const apiResponse = `{
  "status": "success",
  "data": {
    "products": [
      { "id": 1, "name": "Laptop", "price": 999, "stock": 5 },
      { "id": 2, "name": "Mouse", "price": 29, "stock": 0 },
      { "id": 3, "name": "Keyboard", "price": 79, "stock": 12 }
    ]
  }
}`;

console.log("1. Parse Response:");
const response = JSON.parse(apiResponse);
console.log("  Status:", response.status);
console.log("  Products:", response.data.products.length);

console.log("\n2. Filter verfügbare Produkte:");
const available = response.data.products.filter(p => {
  const isAvailable = p.stock > 0;
  console.log(`  ${p.name}: ${isAvailable ? "✅" : "❌"} (stock: ${p.stock})`);
  return isAvailable;
});

console.log("\n3. Erstelle Ergebnis:");
const result = {
  status: "success",
  data: {
    availableProducts: available,
    count: available.length
  }
};

console.log("\n4. Stringify (pretty):");
const jsonResult = JSON.stringify(result, null, 2);
console.log(jsonResult);
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Deep Copy)</summary>

```javascript
console.log("=== Aufgabe 2: Deep Copy ===");

const dbDocument = {
  _id: "user_123",
  name: "Alice",
  email: "alice@example.com",
  orders: [
    { orderId: 101, total: 99, items: ["Laptop"] },
    { orderId: 102, total: 29, items: ["Mouse", "Pad"] }
  ],
  metadata: {
    createdAt: "2024-01-15",
    updatedAt: "2024-10-20"
  }
};

console.log("Original:");
console.log(JSON.stringify(dbDocument, null, 2));

console.log("\n1. Deep Copy erstellen:");
const copy = JSON.parse(JSON.stringify(dbDocument));
console.log("  ✅ Copy erstellt");

console.log("\n2. Modifikationen:");
copy.name = "ALICE";
copy.email = "alice.new@example.com";
console.log("  Name:", copy.name);
console.log("  Email:", copy.email);

console.log("\n3. Neuen Order hinzufügen:");
copy.orders.push({ orderId: 103, total: 149, items: ["Monitor"] });
console.log("  Orders in Copy:", copy.orders.length);

console.log("\n4. Original unverändert:");
console.log("  Name:", dbDocument.name);
console.log("  Email:", dbDocument.email);
console.log("  Orders:", dbDocument.orders.length);
console.log("  ✅ Original ist unverändert!");
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Error Handling)</summary>

```javascript
console.log("=== Aufgabe 3: Error Handling ===");

const responses = [
  `{"status":"success","data":{"count":5}}`,
  `{"status":"success","data":{"count":10},}`,
  `{'status':'error'}`,
  `{"status":"success","data":null}`
];

let validCount = 0;
let invalidCount = 0;

responses.forEach((response, index) => {
  console.log(`\n→ Response ${index + 1}:`);
  console.log(`  ${response.substring(0, 40)}...`);
  
  try {
    const parsed = JSON.parse(response);
    console.log(`  ✅ Valid - Status: ${parsed.status}`);
    validCount++;
  } catch (error) {
    console.log(`  ❌ Invalid - Fehler: ${error.message}`);
    invalidCount++;
  }
});

console.log(`\n📊 Statistik:`);
console.log(`  Valid: ${validCount}`);
console.log(`  Invalid: ${invalidCount}`);
console.log(`  Total: ${responses.length}`);
```
@eval

</details>

</section>

    --{{2}}--
Hervorragend! Sie haben jetzt JSON gemeistert. JSON ist das Fundament für moderne Datenbank-Arbeit. Jede NoSQL-Datenbank, jede REST-API, jeder Microservice nutzt JSON. Mit diesem Wissen können Sie problemlos mit realen APIs und Datenbanken arbeiten!

---

## Kapitel 7: Classes – Objektorientierung (Optional)

    --{{0}}--
Classes sind das objektorientierte Programmierparadigma in JavaScript. Während Sie für einfache Datenbank-Operationen oft mit Objekten und Funktionen auskommen, sind Classes extrem nützlich für strukturierte, wiederverwendbare Code-Architekturen. Denken Sie an eine Database-Connection-Klasse, eine Query-Builder-Klasse oder Model-Klassen für Ihre Daten. In diesem Kapitel lernen Sie die Grundlagen der OOP in JavaScript – kompakt und praxisnah!

    {{0}}
<section>

**Was sind Classes?**

- **Blueprint (Bauplan)**: Eine Klasse definiert die Struktur und das Verhalten von Objekten
- **Instanzen**: Aus einer Klasse können Sie viele Objekte (Instanzen) erzeugen
- **Kapselung**: Daten und Funktionen gehören zusammen
- **Vererbung**: Klassen können von anderen Klassen erben

**Wann Classes nutzen?**

- ✅ Wiederverwendbare Komponenten (z. B. Database-Connection)
- ✅ Komplexe Datenmodelle mit Logik
- ✅ API-Wrapper und Service-Klassen
- ❌ Nicht für einfache Daten-Container (dafür reichen Objekte)

</section>

---

### 7.1 Class Syntax

    --{{0}}--
Die Class-Syntax wurde mit ES6 (2015) eingeführt. Sie ist syntaktischer Zucker über JavaScript's Prototypen-System – macht aber den Code viel lesbarer. Schauen wir uns die Grundstruktur an.

    {{0}}
<section>

**Syntax: `class ClassName { ... }`**

```javascript
console.log("=== Beispiel 1: Erste Klasse ===");

// Klasse definieren
class User {
  // Constructor wird beim Erstellen aufgerufen
  constructor(name, email) {
    this.name = name;
    this.email = email;
    console.log(`  → User erstellt: ${name}`);
  }
  
  // Methode
  greet() {
    return `Hello, I'm ${this.name}`;
  }
}

console.log("Erstelle User-Instanzen:");

// Instanzen erstellen mit 'new'
const user1 = new User("Alice", "alice@example.com");
const user2 = new User("Bob", "bob@example.com");

console.log("\nMethoden aufrufen:");
console.log(user1.greet());
console.log(user2.greet());

console.log("\nProperties zugreifen:");
console.log("user1.name:", user1.name);
console.log("user1.email:", user1.email);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Das Keyword class definiert die Klasse, der constructor ist eine spezielle Methode, die beim Erstellen einer Instanz automatisch aufgerufen wird. Mit new erstellen Sie eine konkrete Instanz der Klasse.

</section>

    {{1}}
<section>

**Vergleich: Object vs. Class**

```javascript
console.log("=== Beispiel 2: Object vs. Class ===");

console.log("❌ Mit einfachen Objekten (unstrukturiert):");

const user1 = {
  name: "Alice",
  email: "alice@example.com",
  greet: function() {
    return `Hello, I'm ${this.name}`;
  }
};

const user2 = {
  name: "Bob",
  email: "bob@example.com",
  greet: function() {
    return `Hello, I'm ${this.name}`;
  }
};

console.log(user1.greet());
console.log(user2.greet());
console.log("→ Code-Duplikation! greet() ist 2x definiert.");

console.log("\n✅ Mit Class (strukturiert):");

class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
  
  greet() {
    return `Hello, I'm ${this.name}`;
  }
}

const user3 = new User("Charlie", "charlie@example.com");
const user4 = new User("Diana", "diana@example.com");

console.log(user3.greet());
console.log(user4.greet());
console.log("→ greet() ist nur 1x definiert, alle Instanzen nutzen sie.");

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Der große Vorteil von Classes: Die Methode greet() ist nur einmal im Code definiert, aber alle Instanzen können sie nutzen. Das spart Speicher und macht den Code wartbarer!

</section>

    {{2}}
<section>

**Praxis: Database-Connection-Klasse (Konzept)**

```javascript
console.log("=== Beispiel 3: Database-Connection (simuliert) ===");

class DatabaseConnection {
  constructor(host, database, user) {
    this.host = host;
    this.database = database;
    this.user = user;
    this.connected = false;
    console.log(`  → DB-Connection konfiguriert: ${database}@${host}`);
  }
  
  connect() {
    // Simuliere Verbindungsaufbau
    console.log(`  → Verbinde zu ${this.database}...`);
    this.connected = true;
    console.log(`  ✅ Verbunden als ${this.user}`);
  }
  
  disconnect() {
    if (this.connected) {
      console.log(`  → Trenne Verbindung zu ${this.database}`);
      this.connected = false;
      console.log(`  ✅ Getrennt`);
    } else {
      console.log(`  ⚠️ Nicht verbunden`);
    }
  }
  
  query(sql) {
    if (!this.connected) {
      console.log(`  ❌ Fehler: Nicht verbunden!`);
      return null;
    }
    console.log(`  → Query: ${sql}`);
    console.log(`  ✅ Query ausgeführt`);
    return { success: true };
  }
}

console.log("Erstelle zwei verschiedene DB-Connections:");

const prodDB = new DatabaseConnection("prod.example.com", "products_db", "admin");
const testDB = new DatabaseConnection("localhost", "test_db", "dev");

console.log("\nNutze prod DB:");
prodDB.connect();
prodDB.query("SELECT * FROM users");
prodDB.disconnect();

console.log("\nNutze test DB:");
testDB.connect();
testDB.query("SELECT * FROM test_data");
testDB.disconnect();

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Sehen Sie den Vorteil? Jede Database-Connection ist eine eigene Instanz mit eigenem Zustand (connected, host, etc.), aber alle teilen sich die gleichen Methoden. Das ist elegante Code-Organisation!

</section>

---

### 7.2 Constructor

    --{{0}}--
Der Constructor ist eine spezielle Methode, die beim Erstellen einer Instanz mit new automatisch aufgerufen wird. Hier initialisieren Sie die Properties des Objekts. Der Constructor ist optional – wenn Sie keinen definieren, gibt es einen leeren Standard-Constructor.

    {{0}}
<section>

**Constructor-Grundlagen**

```javascript
console.log("=== Beispiel 4: Constructor im Detail ===");

class Product {
  constructor(name, price, category) {
    console.log(`  → Constructor aufgerufen für: ${name}`);
    
    // Properties setzen
    this.name = name;
    this.price = price;
    this.category = category;
    
    // Berechnete Properties
    this.taxRate = 0.19;
    this.priceWithTax = price * (1 + this.taxRate);
    
    // Initialisierungs-Logik
    this.createdAt = new Date();
    
    console.log(`  ✅ Produkt initialisiert`);
  }
  
  getInfo() {
    return `${this.name} (${this.category}): ${this.price.toFixed(2)}€`;
  }
}

console.log("Erstelle Produkte:");
const laptop = new Product("Laptop Pro", 999, "Electronics");
const book = new Product("JavaScript Guide", 29.99, "Books");

console.log("\nProdukt-Infos:");
console.log(laptop.getInfo());
console.log("Preis mit MwSt:", laptop.priceWithTax.toFixed(2) + "€");
console.log("Erstellt am:", laptop.createdAt.toLocaleString());

console.log("\n" + book.getInfo());

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{1}}--
Der Constructor ist der perfekte Ort für Initialisierungs-Logik: Properties setzen, Berechnungen durchführen, Validierung, Timestamps setzen. Alles, was beim Erstellen des Objekts passieren muss!

</section>

    {{1}}
<section>

**Constructor mit Validierung**

```javascript
console.log("=== Beispiel 5: Constructor mit Validierung ===");

class User {
  constructor(username, email, age) {
    console.log(`\n  → Validiere User: ${username}`);
    
    // Validierung: Username
    if (!username || username.length < 3) {
      throw new Error("Username muss mindestens 3 Zeichen haben");
    }
    
    // Validierung: Email
    if (!email || !email.includes("@")) {
      throw new Error("Ungültige Email-Adresse");
    }
    
    // Validierung: Alter
    if (age < 0 || age > 150) {
      throw new Error("Ungültiges Alter");
    }
    
    this.username = username;
    this.email = email;
    this.age = age;
    
    console.log(`  ✅ User valide`);
  }
  
  getProfile() {
    return `${this.username} (${this.age}J) - ${this.email}`;
  }
}

console.log("Test 1: Valider User");
try {
  const alice = new User("alice", "alice@example.com", 28);
  console.log(alice.getProfile());
} catch (error) {
  console.error("❌", error.message);
}

console.log("\nTest 2: Username zu kurz");
try {
  const invalid1 = new User("ab", "test@example.com", 25);
} catch (error) {
  console.error("❌", error.message);
}

console.log("\nTest 3: Ungültige Email");
try {
  const invalid2 = new User("testuser", "invalid-email", 30);
} catch (error) {
  console.error("❌", error.message);
}

console.log("\nTest 4: Ungültiges Alter");
try {
  const invalid3 = new User("youngster", "test@example.com", -5);
} catch (error) {
  console.error("❌", error.message);
}

console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{2}}--
Validierung im Constructor ist Best Practice! Wenn ein Objekt erstellt wird, sollte es in einem validen Zustand sein. Werfen Sie Errors bei ungültigen Inputs, damit Fehler sofort erkannt werden.

</section>

    {{2}}
<section>

**Constructor mit Default-Werten**

```javascript
console.log("=== Beispiel 6: Default-Werte im Constructor ===");

class QueryOptions {
  constructor(table, limit = 10, offset = 0, orderBy = "id") {
    console.log(`  → QueryOptions für Tabelle: ${table}`);
    
    this.table = table;
    this.limit = limit;
    this.offset = offset;
    this.orderBy = orderBy;
    
    console.log(`  ✅ Limit=${limit}, Offset=${offset}, OrderBy=${orderBy}`);
  }
  
  buildQuery() {
    return `SELECT * FROM ${this.table} ORDER BY ${this.orderBy} LIMIT ${this.limit} OFFSET ${this.offset}`;
  }
}

console.log("\nQuery 1: Mit allen Defaults");
const query1 = new QueryOptions("users");
console.log(query1.buildQuery());

console.log("\nQuery 2: Mit custom Limit");
const query2 = new QueryOptions("products", 50);
console.log(query2.buildQuery());

console.log("\nQuery 3: Mit allen custom Werten");
const query3 = new QueryOptions("orders", 100, 200, "created_at");
console.log(query3.buildQuery());

console.log("--- Ende Beispiel 6 ---");
```
@eval

    --{{3}}--
Default-Parameter im Constructor sind super praktisch! Sie definieren sinnvolle Standardwerte, die Nutzer überschreiben können. Das macht Ihre API flexibel und benutzerfreundlich.

</section>

---

### 7.3 Methods

    --{{0}}--
Methoden sind Funktionen, die zu einer Klasse gehören. Sie definieren das Verhalten der Instanzen. Im Gegensatz zu Properties (Daten) sind Methoden Actions, die auf den Daten operieren.

    {{0}}
<section>

**Methoden-Grundlagen**

```javascript
console.log("=== Beispiel 7: Methoden ===");

class BankAccount {
  constructor(owner, initialBalance = 0) {
    this.owner = owner;
    this.balance = initialBalance;
    this.transactions = [];
    console.log(`  → Konto erstellt für ${owner} mit ${initialBalance}€`);
  }
  
  // Methode: Einzahlen
  deposit(amount) {
    console.log(`\n  → ${this.owner} zahlt ${amount}€ ein`);
    
    if (amount <= 0) {
      console.log(`  ❌ Betrag muss positiv sein!`);
      return false;
    }
    
    this.balance += amount;
    this.transactions.push({ type: "deposit", amount, date: new Date() });
    console.log(`  ✅ Neuer Stand: ${this.balance}€`);
    return true;
  }
  
  // Methode: Abheben
  withdraw(amount) {
    console.log(`\n  → ${this.owner} hebt ${amount}€ ab`);
    
    if (amount <= 0) {
      console.log(`  ❌ Betrag muss positiv sein!`);
      return false;
    }
    
    if (amount > this.balance) {
      console.log(`  ❌ Nicht genug Guthaben! Aktuell: ${this.balance}€`);
      return false;
    }
    
    this.balance -= amount;
    this.transactions.push({ type: "withdraw", amount, date: new Date() });
    console.log(`  ✅ Neuer Stand: ${this.balance}€`);
    return true;
  }
  
  // Methode: Kontostand anzeigen
  getBalance() {
    return this.balance;
  }
  
  // Methode: Transaktionshistorie
  printStatement() {
    console.log(`\n  Kontoauszug für ${this.owner}`);
    console.log(`  Aktueller Stand: ${this.balance}€`);
    console.log(`  Transaktionen: ${this.transactions.length}`);
    
    this.transactions.forEach((tx, i) => {
      const sign = tx.type === "deposit" ? "+" : "-";
      console.log(`    ${i + 1}. ${tx.type}: ${sign}${tx.amount}€`);
    });
  }
}

console.log("Erstelle Konto:");
const account = new BankAccount("Alice", 100);

account.deposit(50);
account.withdraw(30);
account.withdraw(200);  // Sollte fehlschlagen
account.deposit(100);

account.printStatement();

console.log("--- Ende Beispiel 7 ---");
```
@eval

    --{{1}}--
Methoden kapseln Logik! Die BankAccount-Klasse stellt sicher, dass Transaktionen valide sind (kein negatives Guthaben), speichert History und bietet ein sauberes Interface. Das ist bessere Code-Organisation als lose Funktionen!

</section>

    {{1}}
<section>

**Methoden, die andere Methoden aufrufen**

```javascript
console.log("=== Beispiel 8: Methoden-Komposition ===");

class DataValidator {
  constructor() {
    this.errors = [];
  }
  
  // Private Helper-Methode (Konvention: _ prefix)
  _addError(field, message) {
    this.errors.push({ field, message });
    console.log(`  ⚠️ Validierungsfehler: ${field} - ${message}`);
  }
  
  // Einzel-Validierungen
  validateEmail(email) {
    console.log(`  → Prüfe Email: ${email}`);
    if (!email || !email.includes("@")) {
      this._addError("email", "Ungültige Email-Adresse");
      return false;
    }
    return true;
  }
  
  validateAge(age) {
    console.log(`  → Prüfe Alter: ${age}`);
    if (age < 18) {
      this._addError("age", "Mindestens 18 Jahre erforderlich");
      return false;
    }
    return true;
  }
  
  validateUsername(username) {
    console.log(`  → Prüfe Username: ${username}`);
    if (!username || username.length < 3) {
      this._addError("username", "Min. 3 Zeichen erforderlich");
      return false;
    }
    return true;
  }
  
  // Haupt-Methode nutzt andere Methoden
  validateUser(user) {
    console.log(`\nValidiere User-Objekt:`);
    this.errors = []; // Reset errors
    
    const emailValid = this.validateEmail(user.email);
    const ageValid = this.validateAge(user.age);
    const usernameValid = this.validateUsername(user.username);
    
    const allValid = emailValid && ageValid && usernameValid;
    
    if (allValid) {
      console.log(`\n  ✅ Alle Validierungen bestanden!`);
    } else {
      console.log(`\n  ❌ Validierung fehlgeschlagen: ${this.errors.length} Fehler`);
    }
    
    return allValid;
  }
  
  getErrors() {
    return this.errors;
  }
}

const validator = new DataValidator();

console.log("Test 1: Valider User");
validator.validateUser({
  username: "alice",
  email: "alice@example.com",
  age: 25
});

console.log("\n" + "=".repeat(50));
console.log("Test 2: Invalider User");
validator.validateUser({
  username: "ab",
  email: "invalid",
  age: 16
});

console.log("\nFehler-Details:");
console.table(validator.getErrors());

console.log("--- Ende Beispiel 8 ---");
```
@eval

    --{{2}}--
Methoden-Komposition ist mächtig! Eine komplexe Methode (validateUser) nutzt einfachere Methoden (validateEmail, validateAge, etc.). Das macht den Code modular, testbar und wartbar.

</section>

---

### 7.4 Getter & Setter

    --{{0}}--
Getter und Setter sind spezielle Methoden, die wie Properties aussehen, aber als Funktionen fungieren. Mit get definieren Sie berechnete Properties, mit set kontrollieren Sie Zuweisungen. Das ist perfekt für Validierung und abgeleitete Werte!

    {{0}}
<section>

**Getter: Berechnete Properties**

```javascript
console.log("=== Beispiel 9: Getter ===");

class Rectangle {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }
  
  // Getter: Wird wie ein Property genutzt, ist aber eine Methode
  get area() {
    console.log(`  → Berechne Fläche: ${this.width} × ${this.height}`);
    return this.width * this.height;
  }
  
  get perimeter() {
    console.log(`  → Berechne Umfang: 2 × (${this.width} + ${this.height})`);
    return 2 * (this.width + this.height);
  }
  
  get isSquare() {
    return this.width === this.height;
  }
}

const rect = new Rectangle(10, 5);

console.log("Zugriff auf Getter (OHNE Klammern!):");
console.log("Fläche:", rect.area);  // Kein (), aber Methode wird aufgerufen!
console.log("Umfang:", rect.perimeter);
console.log("Ist Quadrat?", rect.isSquare);

console.log("\nÄndere Dimensionen:");
rect.width = 5;
rect.height = 5;

console.log("Neue Fläche:", rect.area);
console.log("Ist jetzt Quadrat?", rect.isSquare);

console.log("--- Ende Beispiel 9 ---");
```
@eval

    --{{1}}--
Getter sind elegant! Sie sehen aus wie Properties (kein Klammern-Aufruf), verhalten sich aber wie Funktionen. Perfekt für berechnete Werte, die sich dynamisch ändern, wenn sich die Basis-Properties ändern.

</section>

    {{1}}
<section>

**Setter: Kontrollierte Zuweisungen**

```javascript
console.log("=== Beispiel 10: Setter ===");

class Temperature {
  constructor(celsius) {
    this._celsius = celsius;  // _ signalisiert: interner Wert
    console.log(`  → Temperatur initialisiert: ${celsius}°C`);
  }
  
  // Getter für Celsius
  get celsius() {
    return this._celsius;
  }
  
  // Setter für Celsius (mit Validierung!)
  set celsius(value) {
    console.log(`  → Setze Celsius auf ${value}°C`);
    
    if (value < -273.15) {
      console.log(`  ❌ Fehler: Unter absolutem Nullpunkt!`);
      throw new Error("Temperatur unter -273.15°C ist physikalisch unmöglich");
    }
    
    this._celsius = value;
    console.log(`  ✅ Temperatur gesetzt`);
  }
  
  // Getter für Fahrenheit (berechneter Wert)
  get fahrenheit() {
    return (this._celsius * 9/5) + 32;
  }
  
  // Setter für Fahrenheit (konvertiert und setzt Celsius)
  set fahrenheit(value) {
    console.log(`  → Setze Fahrenheit auf ${value}°F`);
    this.celsius = (value - 32) * 5/9;  // Nutzt Celsius-Setter
  }
}

const temp = new Temperature(20);

console.log("\nZugriff:");
console.log("Celsius:", temp.celsius);
console.log("Fahrenheit:", temp.fahrenheit);

console.log("\nÄndere auf 100°C:");
temp.celsius = 100;
console.log("Celsius:", temp.celsius);
console.log("Fahrenheit:", temp.fahrenheit);

console.log("\nÄndere auf 32°F:");
temp.fahrenheit = 32;
console.log("Celsius:", temp.celsius);
console.log("Fahrenheit:", temp.fahrenheit);

console.log("\nVersuch: Ungültiger Wert");
try {
  temp.celsius = -300;  // Setter wirft Error
} catch (error) {
  console.error("❌", error.message);
}

console.log("--- Ende Beispiel 10 ---");
```
@eval

    --{{2}}--
Setter ermöglichen kontrollierte Zuweisungen! Sie können Validierung einbauen, Werte transformieren oder Side-Effects auslösen. Das ist viel besser als direkter Property-Zugriff ohne Kontrolle!

</section>

    {{2}}
<section>

**Praxis: User-Klasse mit Getter/Setter**

```javascript
console.log("=== Beispiel 11: User mit Getter/Setter ===");

class User {
  constructor(firstName, lastName, email) {
    this._firstName = firstName;
    this._lastName = lastName;
    this._email = email;
  }
  
  // Getter: Vollständiger Name (berechnet)
  get fullName() {
    return `${this._firstName} ${this._lastName}`;
  }
  
  // Setter: Vollständiger Name (parsed)
  set fullName(name) {
    console.log(`  → Parse fullName: "${name}"`);
    const parts = name.split(" ");
    if (parts.length < 2) {
      console.log(`  ❌ Name muss Vor- und Nachname enthalten`);
      return;
    }
    this._firstName = parts[0];
    this._lastName = parts.slice(1).join(" ");
    console.log(`  ✅ firstName="${this._firstName}", lastName="${this._lastName}"`);
  }
  
  // Getter: Email-Domain
  get emailDomain() {
    return this._email.split("@")[1];
  }
  
  // Getter: Initialen
  get initials() {
    return `${this._firstName[0]}${this._lastName[0]}`.toUpperCase();
  }
  
  // Setter: Email (mit Validierung)
  set email(value) {
    console.log(`  → Setze Email: ${value}`);
    if (!value.includes("@")) {
      console.log(`  ❌ Ungültige Email`);
      return;
    }
    this._email = value;
    console.log(`  ✅ Email gesetzt`);
  }
  
  get email() {
    return this._email;
  }
}

const user = new User("Alice", "Smith", "alice@example.com");

console.log("\nGetter nutzen:");
console.log("Full Name:", user.fullName);
console.log("Initialen:", user.initials);
console.log("Email-Domain:", user.emailDomain);

console.log("\nSetter nutzen:");
user.fullName = "Bob Johnson";
console.log("Neuer Full Name:", user.fullName);
console.log("Neue Initialen:", user.initials);

user.email = "bob@newdomain.com";
console.log("Neue Email:", user.email);
console.log("Neue Domain:", user.emailDomain);

console.log("--- Ende Beispiel 11 ---");
```
@eval

    --{{3}}--
Getter und Setter machen Ihre Klassen elegant! Nutzer können mit Properties arbeiten, aber Sie haben volle Kontrolle über Validierung, Berechnung und Transformation. Das ist professionelle API-Gestaltung!

</section>

---

### 7.5 Static Methods

    --{{0}}--
Static Methods gehören zur Klasse selbst, nicht zu Instanzen. Sie werden mit dem Keyword static definiert und mit ClassName.methodName() aufgerufen. Perfekt für Utility-Funktionen, Factory-Methods oder Funktionen, die keine Instanz-Daten brauchen!

    {{0}}
<section>

**Static Methods Grundlagen**

```javascript
console.log("=== Beispiel 12: Static Methods ===");

class MathUtils {
  // Static Method: Gehört zur Klasse, nicht zu Instanzen
  static add(a, b) {
    console.log(`  → Static add: ${a} + ${b}`);
    return a + b;
  }
  
  static multiply(a, b) {
    console.log(`  → Static multiply: ${a} × ${b}`);
    return a * b;
  }
  
  static average(numbers) {
    console.log(`  → Static average von ${numbers.length} Zahlen`);
    const sum = numbers.reduce((acc, n) => acc + n, 0);
    return sum / numbers.length;
  }
}

console.log("Static Methods direkt auf Klasse aufrufen:");
console.log("Ergebnis:", MathUtils.add(5, 3));
console.log("Ergebnis:", MathUtils.multiply(4, 7));
console.log("Ergebnis:", MathUtils.average([10, 20, 30, 40]));

console.log("\n❌ NICHT auf Instanzen:");
try {
  const utils = new MathUtils();
  utils.add(1, 2);  // Fehler!
} catch (error) {
  console.error("Fehler:", error.message);
  console.log("→ Static methods sind nur auf der Klasse verfügbar!");
}

console.log("--- Ende Beispiel 12 ---");
```
@eval

    --{{1}}--
Static Methods sind wie "namespaced functions". Sie gruppieren verwandte Funktionen unter einem Klassen-Namen, brauchen aber keine Instanzen. Denken Sie an Math.random() oder Array.isArray() – das sind auch static methods!

</section>

    {{1}}
<section>

**Factory Methods mit static**

```javascript
console.log("=== Beispiel 13: Factory Methods ===");

class User {
  constructor(name, email, role) {
    this.name = name;
    this.email = email;
    this.role = role;
    console.log(`  → User erstellt: ${name} (${role})`);
  }
  
  // Normale Methode
  getInfo() {
    return `${this.name} - ${this.role}`;
  }
  
  // Static Factory Method: Erstellt Admin
  static createAdmin(name, email) {
    console.log(`  → Factory: Erstelle Admin`);
    return new User(name, email, "admin");
  }
  
  // Static Factory Method: Erstellt Standard-User
  static createGuest(name) {
    console.log(`  → Factory: Erstelle Guest`);
    const email = `${name.toLowerCase()}@guest.com`;
    return new User(name, email, "guest");
  }
  
  // Static Factory Method: Von JSON
  static fromJSON(json) {
    console.log(`  → Factory: Parse JSON`);
    const data = JSON.parse(json);
    return new User(data.name, data.email, data.role);
  }
}

console.log("Normale Erstellung:");
const user1 = new User("Alice", "alice@example.com", "user");

console.log("\nMit Factory Methods:");
const admin = User.createAdmin("Bob", "bob@example.com");
const guest = User.createGuest("Charlie");

console.log("\nVon JSON:");
const jsonUser = '{"name":"Diana","email":"diana@example.com","role":"moderator"}';
const user4 = User.fromJSON(jsonUser);

console.log("\nAlle Users:");
console.log(user1.getInfo());
console.log(admin.getInfo());
console.log(guest.getInfo());
console.log(user4.getInfo());

console.log("--- Ende Beispiel 13 ---");
```
@eval

    --{{2}}--
Factory Methods sind ein Design-Pattern! Statt direkt new User() zu nutzen, bieten Sie benannte Konstruktoren wie createAdmin(), createGuest(). Das macht Ihren Code selbsterklärender und flexibler!

</section>

    {{2}}
<section>

**Praxis: Database Query Builder**

```javascript
console.log("=== Beispiel 14: Query Builder mit Static Methods ===");

class QueryBuilder {
  constructor(table) {
    this.table = table;
    this.conditions = [];
    this.limitValue = null;
    this.orderValue = null;
  }
  
  where(field, value) {
    this.conditions.push(`${field} = '${value}'`);
    return this;  // Fluent Interface (method chaining)
  }
  
  limit(n) {
    this.limitValue = n;
    return this;
  }
  
  orderBy(field) {
    this.orderValue = field;
    return this;
  }
  
  build() {
    let query = `SELECT * FROM ${this.table}`;
    
    if (this.conditions.length > 0) {
      query += ` WHERE ${this.conditions.join(" AND ")}`;
    }
    
    if (this.orderValue) {
      query += ` ORDER BY ${this.orderValue}`;
    }
    
    if (this.limitValue) {
      query += ` LIMIT ${this.limitValue}`;
    }
    
    return query;
  }
  
  // Static Factory Methods für häufige Queries
  static select(table) {
    console.log(`  → QueryBuilder.select("${table}")`);
    return new QueryBuilder(table);
  }
  
  static selectAll(table, limit = 100) {
    console.log(`  → QueryBuilder.selectAll("${table}", ${limit})`);
    return new QueryBuilder(table).limit(limit);
  }
  
  static selectById(table, id) {
    console.log(`  → QueryBuilder.selectById("${table}", ${id})`);
    return new QueryBuilder(table).where("id", id).limit(1);
  }
}

console.log("Query 1: Manual Builder");
const query1 = QueryBuilder.select("users")
  .where("role", "admin")
  .where("active", "true")
  .orderBy("created_at")
  .limit(10)
  .build();
console.log(query1);

console.log("\nQuery 2: Factory selectAll");
const query2 = QueryBuilder.selectAll("products", 50).build();
console.log(query2);

console.log("\nQuery 3: Factory selectById");
const query3 = QueryBuilder.selectById("orders", 123).build();
console.log(query3);

console.log("--- Ende Beispiel 14 ---");
```
@eval

    --{{3}}--
Das ist professionelles API-Design! Static Factory Methods bieten bequeme Shortcuts für häufige Use-Cases, während der normale Constructor/Builder maximale Flexibilität bietet. Best of both worlds!

</section>

---

### 7.6 Inheritance (Kurzüberblick)

    --{{0}}--
Vererbung ermöglicht es, eine Klasse von einer anderen abzuleiten. Die Kindklasse erbt Properties und Methoden der Elternklasse und kann sie erweitern oder überschreiben. Das ist nützlich für hierarchische Strukturen und Code-Wiederverwendung.

    {{0}}
<section>

**Inheritance mit extends**

```javascript
console.log("=== Beispiel 15: Inheritance Basics ===");

// Basisklasse (Parent)
class Animal {
  constructor(name, age) {
    this.name = name;
    this.age = age;
    console.log(`  → Animal erstellt: ${name}`);
  }
  
  speak() {
    return `${this.name} macht ein Geräusch`;
  }
  
  getInfo() {
    return `${this.name} ist ${this.age} Jahre alt`;
  }
}

// Kindklasse (Child) erbt von Animal
class Dog extends Animal {
  constructor(name, age, breed) {
    super(name, age);  // Ruft Parent-Constructor auf
    this.breed = breed;
    console.log(`  → Dog erstellt: ${breed}`);
  }
  
  // Überschreibt speak()
  speak() {
    return `${this.name} bellt: Wuff!`;
  }
  
  // Neue Methode (nur in Dog)
  fetch() {
    return `${this.name} holt den Stock`;
  }
}

class Cat extends Animal {
  constructor(name, age, indoor) {
    super(name, age);
    this.indoor = indoor;
    console.log(`  → Cat erstellt: ${indoor ? "Wohnungskatze" : "Freigänger"}`);
  }
  
  speak() {
    return `${this.name} miaut: Miau!`;
  }
}

console.log("\nErstelle Tiere:");
const generic = new Animal("Generic", 5);
const dog = new Dog("Bello", 3, "Golden Retriever");
const cat = new Cat("Whiskers", 2, true);

console.log("\nMethoden aufrufen:");
console.log(generic.speak());
console.log(generic.getInfo());

console.log("\n" + dog.speak());
console.log(dog.getInfo());  // Geerbt von Animal
console.log(dog.fetch());    // Nur in Dog

console.log("\n" + cat.speak());
console.log(cat.getInfo());

console.log("--- Ende Beispiel 15 ---");
```
@eval

    --{{1}}--
Inheritance schafft "is-a"-Beziehungen: Dog IS-A Animal, Cat IS-A Animal. Sie erben gemeinsame Funktionalität (getInfo), können aber spezifisches Verhalten überschreiben (speak) oder hinzufügen (fetch).

</section>

    {{1}}
<section>

**Praxis: Database Models mit Inheritance**

```javascript
console.log("=== Beispiel 16: DB-Models mit Inheritance ===");

// Basis-Model mit gemeinsamer Funktionalität
class BaseModel {
  constructor(id) {
    this.id = id;
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }
  
  // Gemeinsame Methoden für alle Models
  save() {
    this.updatedAt = new Date();
    console.log(`  → Speichere ${this.constructor.name} #${this.id}`);
    return true;
  }
  
  delete() {
    console.log(`  → Lösche ${this.constructor.name} #${this.id}`);
    return true;
  }
  
  toJSON() {
    return JSON.stringify(this, null, 2);
  }
}

// Spezifische Models erben von BaseModel
class User extends BaseModel {
  constructor(id, username, email) {
    super(id);
    this.username = username;
    this.email = email;
  }
  
  // User-spezifische Methode
  sendEmail(subject, body) {
    console.log(`  → Sende Email an ${this.email}: "${subject}"`);
    return true;
  }
}

class Product extends BaseModel {
  constructor(id, name, price, stock) {
    super(id);
    this.name = name;
    this.price = price;
    this.stock = stock;
  }
  
  // Product-spezifische Methode
  updateStock(quantity) {
    console.log(`  → Update Stock für ${this.name}: ${this.stock} → ${this.stock + quantity}`);
    this.stock += quantity;
    this.save();
  }
  
  isAvailable() {
    return this.stock > 0;
  }
}

console.log("Erstelle Models:");
const user = new User(1, "alice", "alice@example.com");
const product = new Product(101, "Laptop", 999, 5);

console.log("\nGemeinsame Methoden (geerbt):");
user.save();
product.save();

console.log("\nSpezifische Methoden:");
user.sendEmail("Welcome", "Hello Alice!");
product.updateStock(-2);
console.log("Verfügbar?", product.isAvailable());

console.log("\nJSON-Export (geerbt):");
console.log(user.toJSON());

console.log("--- Ende Beispiel 16 ---");
```
@eval

    --{{2}}--
Das ist das DRY-Prinzip (Don't Repeat Yourself) in Action! Gemeinsame Funktionalität (save, delete, timestamps) ist einmal in BaseModel definiert, alle Child-Klassen erben sie automatisch. Das reduziert Code-Duplikation massiv!

</section>

---

### 7.7 Übung: Classes

    --{{0}}--
Jetzt sind Sie dran! Diese Übungen testen Ihr Verständnis von Classes, Constructor, Methoden, Getter/Setter und Inheritance.

    {{0}}
<section>

**Aufgabe 1: Book-Klasse**

```javascript
console.log("=== Aufgabe 1: Book-Klasse ===");

// Aufgabe: Erstellen Sie eine Book-Klasse mit:
// - Constructor: title, author, pages, currentPage (default 0)
// - Methode read(pages): erhöht currentPage
// - Methode reset(): setzt currentPage auf 0
// - Getter progress: gibt Prozentsatz zurück (currentPage / pages * 100)
// - Getter isFinished: true wenn currentPage >= pages

// Ihr Code hier:


// Test-Code (auskommentiert bis Sie fertig sind):
/*
const book = new Book("JavaScript Guide", "John Doe", 300);
console.log("Buch:", book.title);
console.log("Fortschritt:", book.progress + "%");

book.read(50);
console.log("Nach 50 Seiten:", book.progress + "%");

book.read(250);
console.log("Nach 250 weiteren Seiten:", book.progress + "%");
console.log("Fertig?", book.isFinished);

book.reset();
console.log("Nach Reset:", book.progress + "%");
*/

console.log("--- Ende Aufgabe 1 ---");
```
@eval

**Aufgabe 2: Shopping Cart**

```javascript
console.log("=== Aufgabe 2: Shopping Cart ===");

// Aufgabe: Erstellen Sie eine ShoppingCart-Klasse mit:
// - Constructor: items Array (leer)
// - Methode addItem(name, price, quantity): fügt Item hinzu
// - Methode removeItem(name): entfernt Item
// - Getter total: berechnet Gesamtpreis
// - Getter itemCount: zählt Gesamt-Anzahl (sum of quantities)
// - Methode printReceipt(): gibt formatierte Liste aus

// Ihr Code hier:


// Test-Code:
/*
const cart = new ShoppingCart();
cart.addItem("Laptop", 999, 1);
cart.addItem("Mouse", 25, 2);
cart.addItem("USB Cable", 10, 3);

console.log("Items:", cart.itemCount);
console.log("Total:", cart.total + "€");
cart.printReceipt();

cart.removeItem("Mouse");
console.log("\nNach Entfernung:");
console.log("Total:", cart.total + "€");
*/

console.log("--- Ende Aufgabe 2 ---");
```
@eval

**Aufgabe 3: Inheritance – Vehicle Hierarchy**

```javascript
console.log("=== Aufgabe 3: Vehicle Hierarchy ===");

// Aufgabe: Erstellen Sie eine Klassen-Hierarchie:
//
// Vehicle (Basis):
// - Constructor: brand, model, year
// - Methode getInfo(): gibt formatted string zurück
// - Methode start(): gibt "${brand} ${model} startet" zurück
//
// Car (erbt von Vehicle):
// - Constructor: brand, model, year, doors
// - Überschreibt start(): gibt "Auto startet: ..." zurück
// - Methode honk(): gibt "Huuup!" zurück
//
// Motorcycle (erbt von Vehicle):
// - Constructor: brand, model, year, hasHelmetStorage
// - Überschreibt start(): gibt "Motorrad brummt: ..." zurück

// Ihr Code hier:


// Test-Code:
/*
const car = new Car("VW", "Golf", 2020, 5);
const bike = new Motorcycle("Harley", "Sportster", 2019, true);

console.log(car.getInfo());
console.log(car.start());
console.log(car.honk());

console.log("\n" + bike.getInfo());
console.log(bike.start());
*/

console.log("--- Ende Aufgabe 3 ---");
```
@eval

</section>

    --{{1}}--
Diese Übungen decken alle wichtigen Class-Konzepte ab! Experimentieren Sie, machen Sie Fehler, lernen Sie daraus. Classes sind mächtig, aber brauchen Übung, um sie effektiv einzusetzen.

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (Book-Klasse)</summary>

```javascript
console.log("=== Aufgabe 1: Lösung ===");

class Book {
  constructor(title, author, pages, currentPage = 0) {
    this.title = title;
    this.author = author;
    this.pages = pages;
    this.currentPage = currentPage;
    console.log(`  → Buch erstellt: "${title}" von ${author}`);
  }
  
  read(pagesToRead) {
    console.log(`  → Lese ${pagesToRead} Seiten...`);
    this.currentPage += pagesToRead;
    
    // Nicht über Gesamtseitenzahl hinaus
    if (this.currentPage > this.pages) {
      this.currentPage = this.pages;
    }
    
    console.log(`  ✅ Aktuell bei Seite ${this.currentPage}/${this.pages}`);
  }
  
  reset() {
    console.log(`  → Reset Lesefortschritt`);
    this.currentPage = 0;
  }
  
  get progress() {
    if (this.pages === 0) return 0;
    return ((this.currentPage / this.pages) * 100).toFixed(1);
  }
  
  get isFinished() {
    return this.currentPage >= this.pages;
  }
}

const book = new Book("JavaScript Guide", "John Doe", 300);
console.log("Buch:", book.title);
console.log("Fortschritt:", book.progress + "%");

book.read(50);
console.log("Nach 50 Seiten:", book.progress + "%");

book.read(250);
console.log("Nach 250 weiteren Seiten:", book.progress + "%");
console.log("Fertig?", book.isFinished);

book.reset();
console.log("Nach Reset:", book.progress + "%");
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Shopping Cart)</summary>

```javascript
console.log("=== Aufgabe 2: Lösung ===");

class ShoppingCart {
  constructor() {
    this.items = [];
    console.log("  → Warenkorb erstellt");
  }
  
  addItem(name, price, quantity) {
    console.log(`  → Füge hinzu: ${quantity}× ${name} à ${price}€`);
    this.items.push({ name, price, quantity });
  }
  
  removeItem(name) {
    console.log(`  → Entferne: ${name}`);
    const index = this.items.findIndex(item => item.name === name);
    if (index !== -1) {
      this.items.splice(index, 1);
      console.log(`  ✅ Entfernt`);
    } else {
      console.log(`  ⚠️ Item nicht gefunden`);
    }
  }
  
  get total() {
    return this.items.reduce((sum, item) => {
      return sum + (item.price * item.quantity);
    }, 0);
  }
  
  get itemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }
  
  printReceipt() {
    console.log("\n  === RECHNUNG ===");
    this.items.forEach(item => {
      const lineTotal = item.price * item.quantity;
      console.log(`  ${item.quantity}× ${item.name.padEnd(15)} ${item.price.toFixed(2)}€ → ${lineTotal.toFixed(2)}€`);
    });
    console.log(`  ${"=".repeat(35)}`);
    console.log(`  ${"TOTAL".padEnd(25)} ${this.total.toFixed(2)}€`);
  }
}

const cart = new ShoppingCart();
cart.addItem("Laptop", 999, 1);
cart.addItem("Mouse", 25, 2);
cart.addItem("USB Cable", 10, 3);

console.log("\nItems:", cart.itemCount);
console.log("Total:", cart.total + "€");
cart.printReceipt();

cart.removeItem("Mouse");
console.log("\nNach Entfernung:");
console.log("Total:", cart.total + "€");
cart.printReceipt();
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Vehicle Hierarchy)</summary>

```javascript
console.log("=== Aufgabe 3: Lösung ===");

class Vehicle {
  constructor(brand, model, year) {
    this.brand = brand;
    this.model = model;
    this.year = year;
    console.log(`  → Vehicle erstellt: ${brand} ${model}`);
  }
  
  getInfo() {
    return `${this.year} ${this.brand} ${this.model}`;
  }
  
  start() {
    return `${this.brand} ${this.model} startet`;
  }
}

class Car extends Vehicle {
  constructor(brand, model, year, doors) {
    super(brand, model, year);
    this.doors = doors;
    console.log(`  → Car: ${doors} Türen`);
  }
  
  start() {
    return `Auto startet: ${this.brand} ${this.model} (${this.doors} Türen)`;
  }
  
  honk() {
    return "Huuup!";
  }
}

class Motorcycle extends Vehicle {
  constructor(brand, model, year, hasHelmetStorage) {
    super(brand, model, year);
    this.hasHelmetStorage = hasHelmetStorage;
    console.log(`  → Motorcycle: Helmfach=${hasHelmetStorage}`);
  }
  
  start() {
    return `Motorrad brummt: ${this.brand} ${this.model} (Brrrmm!)`;
  }
}

const car = new Car("VW", "Golf", 2020, 5);
const bike = new Motorcycle("Harley", "Sportster", 2019, true);

console.log("\n" + car.getInfo());
console.log(car.start());
console.log(car.honk());

console.log("\n" + bike.getInfo());
console.log(bike.start());
```
@eval

</details>

</section>

    --{{2}}--
Exzellent! Sie haben jetzt alle Grundlagen der objektorientierten Programmierung in JavaScript verstanden. Classes sind mächtige Werkzeuge für strukturierte, wartbare Codebases. In Datenbank-Anwendungen sehen Sie Classes oft für Models, Connections, Query Builders und Service-Layer. Sie sind bereit für professionelle JavaScript-Entwicklung!

---

## Kapitel 8: Console & Debugging – Ihre besten Freunde

    --{{0}}--
Die Browser DevTools Console ist Ihr wichtigstes Werkzeug zum Lernen und Debuggen. Wenn Sie nicht wissen, was in Ihrem Code passiert, nutzen Sie console.log()! Dieses Kapitel zeigt Ihnen alle wichtigen Debugging-Techniken.

---

### 8.1 Browser DevTools öffnen

    --{{0}}--
Die DevTools sind in jedem modernen Browser eingebaut. Sie brauchen nichts zu installieren!

    {{0}}
<section>

**=== Beispiel 1: DevTools öffnen ===**

```javascript
console.log("=== Beispiel 1: DevTools öffnen ===");

console.log("🔧 Browser DevTools öffnen:");
console.log("");
console.log("Chrome/Edge:");
console.log("  • Windows/Linux: F12 oder Ctrl+Shift+I");
console.log("  • Mac: Cmd+Option+I");
console.log("");
console.log("Firefox:");
console.log("  • Windows/Linux: F12 oder Ctrl+Shift+K");
console.log("  • Mac: Cmd+Option+K");
console.log("");
console.log("Safari:");
console.log("  • Mac: Cmd+Option+C");
console.log("  • Erst aktivieren: Einstellungen → Erweitert → Entwicklermenü");
console.log("");
console.log("→ Oder Rechtsklick → 'Untersuchen' → Tab 'Console'");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Die Console ist Ihre Debug-Kommandozentrale! Hier sehen Sie alle console.log()-Ausgaben, Fehler, Warnungen und können direkt JavaScript ausführen. Gewöhnen Sie sich an, die DevTools immer offen zu haben!

</section>

    {{1}}
<section>

**=== Beispiel 2: Console Features ===**

```javascript
console.log("=== Beispiel 2: Console Features ===");

console.log("📋 Was die Console kann:");
console.log("");
console.log("✅ Code-Ausgaben (console.log)");
console.log("✅ Fehler anzeigen (mit Stack Trace)");
console.log("✅ Code direkt ausführen (REPL)");
console.log("✅ Objekte inspizieren (aufklappbar)");
console.log("✅ Netzwerk-Requests debuggen");
console.log("✅ Performance messen");
console.log("✅ Breakpoints setzen");
console.log("");
console.log("💡 Tipp: Nutzen Sie die Console täglich!");

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Die Console ist nicht nur für Ausgaben! Sie können Code direkt eingeben und ausführen. Probieren Sie: Tippen Sie "2 + 2" in die Console und drücken Sie Enter. Oder: "document.title = 'Test'". Die Console ist ein interaktives JavaScript-Labor!

</section>

---

### 8.2 console.log & Varianten

    --{{0}}--
console.log() kennen Sie bereits. Aber es gibt viele Varianten für verschiedene Zwecke!

    {{0}}
<section>

**=== Beispiel 1: console.log Basics ===**

```javascript
console.log("=== Beispiel 1: console.log Basics ===");

const user = { name: "Alice", age: 28 };
const scores = [85, 90, 92];

console.log("Einfacher Text");
console.log("Name:", user.name);
console.log("User:", user);
console.log("Scores:", scores);

console.log("\nMehrere Argumente:");
console.log("User", user, "hat Scores", scores);

console.log("\nMit Template Literals:");
console.log(`User ${user.name} ist ${user.age} Jahre alt`);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
console.log() nimmt beliebig viele Argumente. Objekte und Arrays werden schön formatiert angezeigt und sind aufklappbar. Das ist perfekt zum Inspizieren von Datenbank-Resultaten!

</section>

    {{1}}
<section>

**=== Beispiel 2: console.error & console.warn ===**

```javascript
console.log("=== Beispiel 2: error & warn ===");

console.log("Normal: Alles OK");
console.warn("⚠️ Warnung: Dieser Wert könnte problematisch sein");
console.error("❌ Fehler: Etwas ist schief gelaufen!");

console.log("\nNutzung:");
console.log("  console.log() → Normale Infos");
console.log("  console.warn() → Warnungen (gelb)");
console.log("  console.error() → Fehler (rot)");

const value = -5;
if (value < 0) {
  console.warn("Negativer Wert!", value);
}

try {
  throw new Error("Test-Fehler");
} catch (error) {
  console.error("Fehler gefangen:", error.message);
}

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
warn() und error() sind farblich hervorgehoben in der Console (gelb/rot). error() zeigt zusätzlich einen Stack Trace. Nutzen Sie diese, um verschiedene Log-Level zu unterscheiden!

</section>

    {{2}}
<section>

**=== Beispiel 3: console.dir (Objekt-Details) ===**

```javascript
console.log("=== Beispiel 3: console.dir ===");

const user = {
  name: "Alice",
  age: 28,
  greet() {
    return `Hello, ${this.name}`;
  }
};

console.log("Mit console.log():");
console.log(user);

console.log("\nMit console.dir():");
console.dir(user);

console.log("\n💡 Unterschied:");
console.log("  log() → Schöne Darstellung");
console.log("  dir() → Alle Properties/Methoden sichtbar");

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
console.dir() zeigt ALLE Properties eines Objekts, inklusive Prototyp-Methoden. Das ist nützlich, wenn Sie wissen wollen, welche Methoden ein Objekt hat.

</section>

    {{3}}
<section>

**=== Beispiel 4: console.group (Gruppierung) ===**

```javascript
console.log("=== Beispiel 4: console.group ===");

console.group("User-Daten");
console.log("Name: Alice");
console.log("Age: 28");
console.log("Email: alice@example.com");
console.groupEnd();

console.group("Bestellungen");
console.log("Order 1: 99€");
console.log("Order 2: 149€");

console.group("Order 2 Details");
console.log("  Item 1: Laptop");
console.log("  Item 2: Mouse");
console.groupEnd();

console.groupEnd();

console.log("→ Gruppen sind aufklappbar in der Console!");

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{4}}--
console.group() und console.groupEnd() organisieren Ausgaben in aufklappbare Gruppen. Perfekt für komplexe Logs mit vielen Daten! Sie können Gruppen auch verschachteln.

</section>

    {{4}}
<section>

**=== Beispiel 5: console.clear (Aufräumen) ===**

```javascript
console.log("=== Beispiel 5: console.clear ===");

console.log("Viele Logs...");
console.log("Noch mehr Logs...");
console.log("Noch mehr...");

console.log("\n→ Console wird gleich geleert...");

// Uncomment to actually clear:
// console.clear();

console.log("💡 console.clear() löscht die Console");
console.log("   Nützlich für einen sauberen Start");

console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{5}}--
console.clear() räumt die Console auf. Nützlich, wenn Sie einen frischen Start wollen. Achtung: In LiaScript bleibt die History erhalten, aber im Browser wird alles gelöscht!

</section>

---

### 8.3 console.table (für Arrays/Objekte)

    --{{0}}--
console.table() ist ein Geheimtipp! Es zeigt Arrays und Objekte als schöne Tabelle – perfekt für Datenbank-Resultate.

    {{0}}
<section>

**=== Beispiel 1: Array von Objekten als Tabelle ===**

```javascript
console.log("=== Beispiel 1: console.table ===");

const users = [
  { id: 1, name: "Alice", age: 28, role: "admin" },
  { id: 2, name: "Bob", age: 34, role: "editor" },
  { id: 3, name: "Charlie", age: 22, role: "viewer" }
];

console.log("Mit console.log():");
console.log(users);

console.log("\nMit console.table():");
console.table(users);

console.log("\n💡 Viel übersichtlicher als log()!");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
console.table() zeigt die Daten als Tabelle mit Spalten! Sie können Spalten sortieren und filtern. Das ist EXTREM hilfreich beim Debuggen von Datenbank-Queries.

</section>

    {{1}}
<section>

**=== Beispiel 2: Nur bestimmte Spalten ===**

```javascript
console.log("=== Beispiel 2: Spalten auswählen ===");

const products = [
  { id: 1, name: "Laptop", price: 999, stock: 5, category: "electronics" },
  { id: 2, name: "Mouse", price: 29, stock: 12, category: "electronics" },
  { id: 3, name: "Desk", price: 299, stock: 3, category: "furniture" }
];

console.log("Alle Spalten:");
console.table(products);

console.log("\nNur name und price:");
console.table(products, ["name", "price"]);

console.log("\nNur stock und category:");
console.table(products, ["stock", "category"]);

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Der zweite Parameter von console.table() ist ein Array mit den gewünschten Spalten. So können Sie große Datenmengen auf die wichtigen Felder reduzieren!

</section>

    {{2}}
<section>

**=== Beispiel 3: Objekt als Tabelle ===**

```javascript
console.log("=== Beispiel 3: Objekt als Tabelle ===");

const stats = {
  totalUsers: 1523,
  activeUsers: 892,
  newToday: 23,
  averageAge: 31.5,
  conversionRate: 0.12
};

console.log("Mit console.log():");
console.log(stats);

console.log("\nMit console.table():");
console.table(stats);

console.log("\n→ Jede Property wird eine Zeile!");

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Auch einfache Objekte können als Tabelle dargestellt werden. Jedes Property wird eine Zeile. Nützlich für Statistiken oder Konfigurationsobjekte!

</section>

---

### 8.4 console.time & console.timeEnd

    --{{0}}--
Performance messen ist wichtig! console.time() und console.timeEnd() zeigen, wie lange ein Code-Block dauert.

    {{0}}
<section>

**=== Beispiel 1: Einfaches Timing ===**

```javascript
console.log("=== Beispiel 1: console.time ===");

console.time("Berechnung");

let sum = 0;
for (let i = 0; i < 1000000; i++) {
  sum += i;
}

console.timeEnd("Berechnung");

console.log("Summe:", sum);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
console.time("label") startet einen Timer. console.timeEnd("label") stoppt ihn und zeigt die Dauer in Millisekunden. Perfekt, um langsame Code-Stellen zu finden!

</section>

    {{1}}
<section>

**=== Beispiel 2: Mehrere Timer parallel ===**

```javascript
console.log("=== Beispiel 2: Mehrere Timer ===");

console.time("Total");
console.time("Step 1");

// Step 1: Filter
const numbers = Array.from({ length: 100000 }, (_, i) => i);
const even = numbers.filter(n => n % 2 === 0);

console.timeEnd("Step 1");
console.time("Step 2");

// Step 2: Map
const doubled = even.map(n => n * 2);

console.timeEnd("Step 2");
console.time("Step 3");

// Step 3: Reduce
const sum = doubled.reduce((a, b) => a + b, 0);

console.timeEnd("Step 3");
console.timeEnd("Total");

console.log("Summe:", sum);

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Sie können mehrere Timer gleichzeitig laufen lassen! Jeder Timer braucht ein eindeutiges Label. So sehen Sie, welcher Schritt am längsten dauert.

</section>

    {{2}}
<section>

**=== Beispiel 3: DB-Query Performance ===**

```javascript
console.log("=== Beispiel 3: Query Performance ===");

function simulateDBQuery(name, delay) {
  return new Promise(resolve => {
    setTimeout(() => resolve(`Data from ${name}`), delay);
  });
}

async function measureQueries() {
  console.time("Query A");
  const a = await simulateDBQuery("Query A", 500);
  console.timeEnd("Query A");
  console.log("  →", a);
  
  console.time("Query B");
  const b = await simulateDBQuery("Query B", 300);
  console.timeEnd("Query B");
  console.log("  →", b);
  
  console.time("Query C");
  const c = await simulateDBQuery("Query C", 700);
  console.timeEnd("Query C");
  console.log("  →", c);
}

console.time("Total Queries");
measureQueries().then(() => {
  console.timeEnd("Total Queries");
  console.log("✅ Alle Queries fertig");
});

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Das ist das typische Pattern für Datenbank-Performance-Messung! Sie sehen genau, welche Query am langsamsten ist. In echten Apps können Sie so Optimierungs-Kandidaten identifizieren.

</section>

---

### 8.5 Debugging-Strategien

    --{{0}}--
Debugging ist eine Kunst! Hier sind bewährte Strategien, die Ihnen Zeit sparen.

    {{0}}
<section>

**=== Beispiel 1: Binary Search Debugging ===**

```javascript
console.log("=== Beispiel 1: Binary Search Debugging ===");

function processData(data) {
  console.log("→ Start processData");
  
  // Step 1
  const filtered = data.filter(x => x > 0);
  console.log("  1. Nach Filter:", filtered);
  
  // Step 2
  const doubled = filtered.map(x => x * 2);
  console.log("  2. Nach Map:", doubled);
  
  // Step 3
  const sum = doubled.reduce((a, b) => a + b, 0);
  console.log("  3. Nach Reduce:", sum);
  
  console.log("→ Ende processData");
  return sum;
}

const input = [1, -5, 3, -2, 4];
console.log("Input:", input);

const result = processData(input);
console.log("Result:", result);

console.log("\n💡 Strategie: Log nach jedem Schritt!");
console.log("   So sehen Sie genau, wo ein Fehler passiert.");

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
Binary Search Debugging: Setzen Sie console.log() in die Mitte Ihres Codes. Läuft er bis dahin? Ja → Fehler ist danach. Nein → Fehler ist davor. Dann wieder in die Mitte, bis Sie die fehlerhafte Zeile haben!

</section>

    {{1}}
<section>

**=== Beispiel 2: Objekte visualisieren ===**

```javascript
console.log("=== Beispiel 2: Objekte visualisieren ===");

const dbResult = {
  status: "success",
  data: {
    users: [
      { id: 1, name: "Alice", orders: [{ total: 99 }, { total: 149 }] },
      { id: 2, name: "Bob", orders: [{ total: 29 }] }
    ]
  },
  meta: { timestamp: "2024-10-22", count: 2 }
};

console.log("Methode 1: console.log");
console.log(dbResult);

console.log("\nMethode 2: JSON.stringify (pretty)");
console.log(JSON.stringify(dbResult, null, 2));

console.log("\nMethode 3: console.table (users)");
console.table(dbResult.data.users, ["id", "name"]);

console.log("\nMethode 4: Einzelne Werte");
console.log("Status:", dbResult.status);
console.log("User-Count:", dbResult.data.users.length);
dbResult.data.users.forEach(user => {
  const total = user.orders.reduce((sum, o) => sum + o.total, 0);
  console.log(`  ${user.name}: ${total}€`);
});

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
Verschiedene Visualisierungs-Methoden für verschiedene Zwecke! log() für schnelles Inspizieren, stringify() für Copy-Paste, table() für Listen, Einzelwerte für gezielte Checks.

</section>

    {{2}}
<section>

**=== Beispiel 3: Defensive Checks ===**

```javascript
console.log("=== Beispiel 3: Defensive Checks ===");

function processUser(user) {
  console.log("→ processUser aufgerufen");
  console.log("  user:", user);
  
  // Defensive Checks
  if (!user) {
    console.error("❌ user ist undefined/null!");
    return null;
  }
  
  if (!user.name) {
    console.warn("⚠️ user.name fehlt!");
  }
  
  if (!Array.isArray(user.orders)) {
    console.error("❌ user.orders ist kein Array!");
    return null;
  }
  
  console.log("✅ Alle Checks OK");
  
  const total = user.orders.reduce((sum, o) => sum + o.total, 0);
  console.log("  Total:", total);
  
  return total;
}

console.log("\nTest 1: Valider User");
processUser({ name: "Alice", orders: [{ total: 99 }] });

console.log("\nTest 2: Fehlende orders");
processUser({ name: "Bob" });

console.log("\nTest 3: null");
processUser(null);

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
Defensive Programming: Prüfen Sie Ihre Annahmen! Ist das Objekt definiert? Ist das Property vorhanden? Ist es vom richtigen Typ? Diese Checks finden 90% der Bugs sofort!

</section>

---

### 8.6 Häufige Fehler & Fehlermeldungen

    --{{0}}--
Diese Fehler sehen Sie ständig! Lernen Sie, sie zu erkennen und zu fixen.

    {{0}}
<section>

**=== Beispiel 1: TypeError – Cannot read property ===**

```javascript
console.log("=== Beispiel 1: TypeError ===");

const user = null;

console.log("Versuch 1: user.name");
try {
  console.log(user.name);
} catch (error) {
  console.error("❌", error.message);
  console.log("   → user ist null/undefined!");
}

console.log("\nLösung 1: Optional Chaining");
console.log("user?.name:", user?.name);

console.log("\nLösung 2: Check vor Zugriff");
if (user && user.name) {
  console.log("Name:", user.name);
} else {
  console.log("User oder Name fehlt");
}

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{1}}--
"Cannot read property 'x' of undefined/null" ist DER häufigste Fehler! Ursache: Sie greifen auf ein Property eines undefined/null-Objekts zu. Lösung: Optional Chaining (?.) oder Check vor Zugriff.

</section>

    {{1}}
<section>

**=== Beispiel 2: ReferenceError – Not defined ===**

```javascript
console.log("=== Beispiel 2: ReferenceError ===");

console.log("Versuch: undefinedVariable");
try {
  console.log(undefinedVariable);
} catch (error) {
  console.error("❌", error.message);
  console.log("   → Variable wurde nicht deklariert!");
}

console.log("\nTypische Ursachen:");
console.log("  • Tippfehler im Variablennamen");
console.log("  • Variable außerhalb des Scopes");
console.log("  • Vergessen zu deklarieren (const/let/var)");

console.log("\nLösung:");
const myVariable = 42;
console.log("myVariable:", myVariable);

console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{2}}--
"ReferenceError: X is not defined" bedeutet: Die Variable existiert nicht. Häufigste Ursache: Tippfehler! Prüfen Sie die Schreibweise oder ob die Variable im richtigen Scope ist.

</section>

    {{2}}
<section>

**=== Beispiel 3: SyntaxError – Unexpected token ===**

```javascript
console.log("=== Beispiel 3: SyntaxError ===");

console.log("Häufige Syntax-Fehler:");
console.log("");

console.log("❌ Fehlende Klammer:");
console.log("  const arr = [1, 2, 3;  // ] fehlt");

console.log("\n❌ Fehlende geschweifte Klammer:");
console.log("  if (x > 0) {");
console.log("    console.log('ok');  // } fehlt");

console.log("\n❌ Komma statt Semikolon:");
console.log("  const a = 1,  // Sollte ; sein");
console.log("  const b = 2;");

console.log("\n❌ JSON mit einfachen Quotes:");
console.log("  JSON.parse(\"{'name':'Alice'}\")");

console.log("\n✅ Lösung: Syntax-Checker nutzen!");
console.log("   → ESLint, VS Code zeigen Fehler sofort");

console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{3}}--
SyntaxError bedeutet: Ihr Code ist grammatikalisch falsch. JavaScript kann ihn nicht parsen. Häufigste Ursachen: Fehlende Klammern, falsche Quotes, fehlende Kommas. Ein guter Editor (VS Code) zeigt diese Fehler sofort!

</section>

    {{3}}
<section>

**=== Beispiel 4: TypeError – X is not a function ===**

```javascript
console.log("=== Beispiel 4: Not a function ===");

const obj = {
  name: "Alice",
  age: 28
};

console.log("Versuch: obj.toUpperCase()");
try {
  console.log(obj.toUpperCase());
} catch (error) {
  console.error("❌", error.message);
  console.log("   → obj ist kein String, hat keine toUpperCase()!");
}

console.log("\nRichtig:");
console.log("obj.name.toUpperCase():", obj.name.toUpperCase());

console.log("\nAnderes Beispiel:");
const notAFunction = 42;
try {
  notAFunction();
} catch (error) {
  console.error("❌", error.message);
  console.log("   → notAFunction ist eine Zahl, keine Funktion!");
}

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{4}}--
"X is not a function" bedeutet: Sie versuchen, etwas als Funktion aufzurufen, das keine ist. Häufige Ursache: Tippfehler oder falscher Typ. Prüfen Sie mit typeof, was Sie tatsächlich haben!

</section>

---

### 8.7 Übung: Debugging

    --{{0}}--
Jetzt sind Sie dran! Finden Sie die Bugs in diesen Code-Snippets.

    {{0}}
<section>

**Aufgabe 1: Finde den Fehler**

```javascript
console.log("=== Aufgabe 1 ===");

function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i <= items.length; i++) {
    total += items[i].price;
  }
  return total;
}

const cart = [
  { name: "Laptop", price: 999 },
  { name: "Mouse", price: 29 }
];

console.log("Cart:", cart);

try {
  const total = calculateTotal(cart);
  console.log("Total:", total);
} catch (error) {
  console.error("Fehler:", error.message);
  console.log("\n❓ Was ist der Fehler?");
  console.log("💡 Tipp: Schauen Sie auf die Schleifenbedingung");
}

// Ihr Code hier: Fixen Sie calculateTotal()
```
@eval

**Aufgabe 2: Defensive Checks**

```javascript
console.log("=== Aufgabe 2 ===");

function getUserEmail(user) {
  return user.contact.email.toLowerCase();
}

const users = [
  { name: "Alice", contact: { email: "ALICE@EXAMPLE.COM" } },
  { name: "Bob", contact: {} },
  { name: "Charlie" }
];

console.log("Users:", users);

users.forEach(user => {
  try {
    const email = getUserEmail(user);
    console.log(`${user.name}: ${email}`);
  } catch (error) {
    console.error(`Fehler bei ${user.name}:`, error.message);
  }
});

console.log("\n❓ Aufgabe: Machen Sie getUserEmail() robust");
console.log("💡 Nutzen Sie Optional Chaining oder Defensive Checks");

// Ihr Code hier: Schreiben Sie eine robuste Version
```
@eval

**Aufgabe 3: Performance messen**

```javascript
console.log("=== Aufgabe 3 ===");

function processDataSlow(data) {
  let result = [];
  for (let i = 0; i < data.length; i++) {
    if (data[i] % 2 === 0) {
      result.push(data[i] * 2);
    }
  }
  return result;
}

function processDataFast(data) {
  return data.filter(x => x % 2 === 0).map(x => x * 2);
}

const bigArray = Array.from({ length: 100000 }, (_, i) => i);

console.log("Array-Größe:", bigArray.length);

console.log("\n❓ Aufgabe: Messen Sie die Performance beider Funktionen");
console.log("💡 Nutzen Sie console.time() / console.timeEnd()");

// Ihr Code hier: Messen Sie die Zeiten
```
@eval

</section>

    --{{1}}--
Diese Übungen sind realistisch! Solche Bugs und Performance-Probleme begegnen Ihnen täglich. Nutzen Sie die gelernten Debugging-Techniken!

    {{1}}
<section>

**Lösungen:**

<details>
<summary>Lösung Aufgabe 1 (Finde den Fehler)</summary>

```javascript
console.log("=== Aufgabe 1: Lösung ===");

console.log("Problem:");
console.log("  for (let i = 0; i <= items.length; i++)");
console.log("                    ^^");
console.log("  <= geht einen Schritt zu weit!");
console.log("  Bei i = items.length ist items[i] undefined");

function calculateTotalFixed(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {  // < statt <=
    console.log(`  [${i}] ${items[i].name}: ${items[i].price}€`);
    total += items[i].price;
  }
  return total;
}

const cart = [
  { name: "Laptop", price: 999 },
  { name: "Mouse", price: 29 }
];

const total = calculateTotalFixed(cart);
console.log("✅ Total:", total);

console.log("\n💡 Merke: Arrays von 0 bis length-1");
console.log("   Schleife: i < length (nicht <=)");
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 2 (Defensive Checks)</summary>

```javascript
console.log("=== Aufgabe 2: Lösung ===");

// Lösung 1: Optional Chaining
function getUserEmailSafe(user) {
  const email = user?.contact?.email;
  if (!email) {
    return "keine E-Mail";
  }
  return email.toLowerCase();
}

// Lösung 2: Defensive Checks
function getUserEmailDefensive(user) {
  if (!user) {
    console.log("  ⚠️ user ist undefined/null");
    return "keine E-Mail";
  }
  if (!user.contact) {
    console.log(`  ⚠️ ${user.name}: contact fehlt`);
    return "keine E-Mail";
  }
  if (!user.contact.email) {
    console.log(`  ⚠️ ${user.name}: email fehlt`);
    return "keine E-Mail";
  }
  return user.contact.email.toLowerCase();
}

const users = [
  { name: "Alice", contact: { email: "ALICE@EXAMPLE.COM" } },
  { name: "Bob", contact: {} },
  { name: "Charlie" }
];

console.log("Mit Optional Chaining:");
users.forEach(user => {
  const email = getUserEmailSafe(user);
  console.log(`  ${user.name}: ${email}`);
});

console.log("\nMit Defensive Checks:");
users.forEach(user => {
  const email = getUserEmailDefensive(user);
  console.log(`  ${user.name}: ${email}`);
});
```
@eval

</details>

<details>
<summary>Lösung Aufgabe 3 (Performance)</summary>

```javascript
console.log("=== Aufgabe 3: Lösung ===");

function processDataSlow(data) {
  let result = [];
  for (let i = 0; i < data.length; i++) {
    if (data[i] % 2 === 0) {
      result.push(data[i] * 2);
    }
  }
  return result;
}

function processDataFast(data) {
  return data.filter(x => x % 2 === 0).map(x => x * 2);
}

const bigArray = Array.from({ length: 100000 }, (_, i) => i);

console.log("Teste Slow Version:");
console.time("Slow");
const resultSlow = processDataSlow(bigArray);
console.timeEnd("Slow");
console.log("  Result-Länge:", resultSlow.length);

console.log("\nTeste Fast Version:");
console.time("Fast");
const resultFast = processDataFast(bigArray);
console.timeEnd("Fast");
console.log("  Result-Länge:", resultFast.length);

console.log("\n💡 Beide sollten ähnlich schnell sein");
console.log("   Modern: filter/map ist lesbarer");
console.log("   Performance: Meist vernachlässigbar");
```
@eval

</details>

</section>

    --{{2}}--
Exzellent! Sie haben jetzt alle wichtigen Debugging-Techniken. Die Console ist Ihr bester Freund beim Programmieren. Nutzen Sie console.log() ausgiebig, console.table() für Daten, console.time() für Performance. Und denken Sie daran: Defensive Checks vermeiden 90% der Bugs!

---

## Kapitel 9: Template Literals & String-Operationen

    --{{0}}--
Moderne String-Verarbeitung mit Backticks – unverzichtbar für lesbare Query-Ausgaben, dynamische SQL-Statements und formatierte Datenbank-Resultate. In diesem Kapitel lernen Sie, wie Sie mit Template Literals arbeiten und Strings effizient manipulieren.


### 9.1 Template Literals (Backticks)

    --{{0}}--
Template Literals sind Strings mit Superkräften! Statt einfacher oder doppelter Anführungszeichen verwenden Sie Backticks. Das ermöglicht String-Interpolation, mehrzeilige Strings und eingebettete Ausdrücke. Perfekt für dynamische Query-Ausgaben!

    --{{1}}--
Schauen wir uns zuerst den Unterschied zwischen klassischen Strings und Template Literals an.

      {{1}}
```javascript
console.log("=== Beispiel 1: Klassische Strings vs. Template Literals ===");

// Klassische Strings - umständlich bei Variablen
const name = "Alice";
const age = 25;
const klassisch = "Hallo, ich bin " + name + " und " + age + " Jahre alt.";
console.log("Klassisch:", klassisch);

// Template Literals - elegant und lesbar
const modern = `Hallo, ich bin ${name} und ${age} Jahre alt.`;
console.log("Modern:", modern);

// Berechnungen direkt im String
const rechnung = `${name} ist in 5 Jahren ${age + 5} Jahre alt.`;
console.log("Berechnung:", rechnung);

console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{2}}--
Template Literals können beliebige JavaScript-Ausdrücke enthalten: Variablen, Berechnungen, Funktionsaufrufe, sogar ternäre Operatoren!

      {{2}}
```javascript
console.log("=== Beispiel 2: Ausdrücke in Template Literals ===");

const user = {
  username: "alice_db",
  role: "admin",
  loginCount: 42
};

// Verschiedene Ausdrücke in einem Template Literal
const info = `
Benutzer: ${user.username}
Rolle: ${user.role.toUpperCase()}
Status: ${user.loginCount > 0 ? "aktiv" : "inaktiv"}
Login-Quote: ${(user.loginCount / 30).toFixed(2)} pro Tag
`;

console.log(info);
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{3}}--
In Datenbank-Anwendungen sind Template Literals perfekt für dynamische Query-Ausgaben und Log-Statements.

      {{3}}
```javascript
console.log("=== Beispiel 3: DB-Query-Logging ===");

function queryDatabase(table, condition, limit = 10) {
  // Simuliere Query-Ausführung
  const startTime = Date.now();
  
  // Template Literal für lesbare Log-Ausgabe
  console.log(`
🔍 Query gestartet
   Tabelle: ${table}
   Bedingung: ${condition}
   Limit: ${limit}
   Zeitstempel: ${new Date().toLocaleTimeString()}
  `);
  
  // Simuliere Verarbeitung
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  console.log(`✅ Query abgeschlossen in ${duration}ms`);
  
  return { success: true, duration };
}

queryDatabase("users", "age > 18", 50);
console.log("--- Ende Beispiel 3 ---");
```
@eval


### 9.2 String Interpolation

    --{{0}}--
String Interpolation bedeutet, dass Variablen und Ausdrücke direkt in den String eingebettet werden können. Mit der Syntax ${...} können Sie alles einbetten, was JavaScript berechnen kann.

    --{{1}}--
Schauen wir uns verschiedene Anwendungsfälle für String-Interpolation an.

      {{1}}
```javascript
console.log("=== Beispiel 4: String-Interpolation für DB-Resultate ===");

const products = [
  { id: 1, name: "Laptop", price: 999, stock: 5 },
  { id: 2, name: "Mouse", price: 25, stock: 150 },
  { id: 3, name: "Keyboard", price: 79, stock: 0 }
];

// Formatierte Ausgabe jedes Produkts
products.forEach(product => {
  const status = product.stock > 0 ? "verfügbar" : "ausverkauft";
  const priceFormatted = product.price.toFixed(2);
  
  const output = `
Produkt #${product.id}: ${product.name}
├─ Preis: ${priceFormatted} EUR
├─ Lagerbestand: ${product.stock} Stück
└─ Status: ${status}
  `;
  
  console.log(output);
});

console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{2}}--
Bei komplexeren Ausdrücken können Sie auch Funktionen innerhalb der Interpolation aufrufen.

      {{2}}
```javascript
console.log("=== Beispiel 5: Funktionsaufrufe in Interpolation ===");

function formatCurrency(amount, currency = "EUR") {
  return `${amount.toFixed(2)} ${currency}`;
}

function calculateTax(price, taxRate = 0.19) {
  return price * taxRate;
}

const item = {
  name: "Server",
  netPrice: 5000,
  taxRate: 0.19
};

// Funktionsaufrufe direkt in der Interpolation
const invoice = `
Rechnung
--------
Artikel: ${item.name}
Nettopreis: ${formatCurrency(item.netPrice)}
MwSt (${(item.taxRate * 100).toFixed(0)}%): ${formatCurrency(calculateTax(item.netPrice, item.taxRate))}
Bruttopreis: ${formatCurrency(item.netPrice + calculateTax(item.netPrice, item.taxRate))}
`;

console.log(invoice);
console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{3}}--
Vorsicht bei komplexen Ausdrücken! Zu viel Logik im Template Literal macht den Code schwer lesbar. Lagern Sie komplexe Berechnungen lieber in Variablen oder Funktionen aus.

      {{3}}
```javascript
console.log("=== Beispiel 6: Gut vs. Schlecht strukturiert ===");

const order = {
  items: [
    { name: "Laptop", price: 999, quantity: 1 },
    { name: "Mouse", price: 25, quantity: 2 },
    { name: "USB-C Cable", price: 15, quantity: 3 }
  ],
  customer: "Bob"
};

// ❌ SCHLECHT: Zu viel Logik im Template Literal
const bad = `Kunde ${order.customer} hat ${order.items.length} Artikel bestellt für insgesamt ${order.items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2)} EUR`;
console.log("❌ Schlecht lesbar:", bad);

// ✅ GUT: Berechnungen vorher durchführen
const itemCount = order.items.length;
const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
const totalFormatted = total.toFixed(2);

const good = `Kunde ${order.customer} hat ${itemCount} Artikel bestellt für insgesamt ${totalFormatted} EUR`;
console.log("✅ Gut lesbar:", good);

console.log("--- Ende Beispiel 6 ---");
```
@eval


### 9.3 Multiline Strings

    --{{0}}--
Mit Template Literals können Sie mehrzeilige Strings schreiben, ohne + oder \n verwenden zu müssen. Das ist perfekt für SQL-Queries, JSON-Templates oder formatierte Ausgaben.

    --{{1}}--
Klassische Strings erfordern mühsame Konkatenation für mehrzeilige Texte. Template Literals sind hier viel eleganter.

      {{1}}
```javascript
console.log("=== Beispiel 7: Multiline Strings ===");

// ❌ Klassisch: umständlich
const classicSQL = 
  "SELECT users.name, orders.total\n" +
  "FROM users\n" +
  "JOIN orders ON users.id = orders.user_id\n" +
  "WHERE orders.total > 100\n" +
  "ORDER BY orders.total DESC";

console.log("Klassisch:");
console.log(classicSQL);
console.log();

// ✅ Modern: lesbar und wartbar
const modernSQL = `
SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id
WHERE orders.total > 100
ORDER BY orders.total DESC
`;

console.log("Modern:");
console.log(modernSQL);

console.log("--- Ende Beispiel 7 ---");
```
@eval

    --{{2}}--
Multiline Strings sind auch perfekt für HTML-Templates, Email-Texte oder formatierte Reports.

      {{2}}
```javascript
console.log("=== Beispiel 8: Report-Template ===");

function generateReport(user, stats) {
  return `
╔══════════════════════════════════════╗
║       MONTHLY ACTIVITY REPORT        ║
╠══════════════════════════════════════╣
║ User: ${user.padEnd(28)} ║
║ Period: ${stats.month.padEnd(26)} ║
╠══════════════════════════════════════╣
║ Logins: ${String(stats.logins).padEnd(27)} ║
║ Queries: ${String(stats.queries).padEnd(26)} ║
║ Errors: ${String(stats.errors).padEnd(27)} ║
╚══════════════════════════════════════╝
  `;
}

const report = generateReport(
  "alice@example.com",
  { month: "October 2025", logins: 42, queries: 1337, errors: 3 }
);

console.log(report);
console.log("--- Ende Beispiel 8 ---");
```
@eval

    --{{3}}--
Bei SQL-Queries mit Parametern können Sie Template Literals mit echten Werten kombinieren. Achtung: In Produktion nie ungefilterte User-Inputs direkt einsetzen (SQL-Injection-Gefahr)!

      {{3}}
```javascript
console.log("=== Beispiel 9: Dynamische SQL-Query (nur für Bildungszwecke!) ===");

function buildQuery(table, filters = {}, limit = 10) {
  // Baue WHERE-Klausel
  const whereConditions = Object.entries(filters)
    .map(([key, value]) => `${key} = '${value}'`)
    .join(" AND ");
  
  const whereClause = whereConditions ? `WHERE ${whereConditions}` : "";
  
  // Template Literal für komplette Query
  const query = `
SELECT *
FROM ${table}
${whereClause}
LIMIT ${limit}
  `.trim();
  
  return query;
}

// Beispiel-Aufrufe
console.log("Query 1:");
console.log(buildQuery("products"));
console.log();

console.log("Query 2:");
console.log(buildQuery("users", { role: "admin", active: "true" }));
console.log();

console.log("Query 3:");
console.log(buildQuery("orders", { status: "pending" }, 50));

console.log("\n⚠️  WICHTIG: In Produktion immer Prepared Statements verwenden!");
console.log("--- Ende Beispiel 9 ---");
```
@eval


### 9.4 String-Methoden (split, join, trim, etc.)

    --{{0}}--
JavaScript bietet viele eingebaute String-Methoden für Manipulation und Verarbeitung. Diese sind unverzichtbar beim Parsen von Daten, Validieren von Eingaben und Formatieren von Ausgaben.

    --{{1}}--
Beginnen wir mit den häufigsten String-Methoden: split, join, trim und Case-Konvertierung.

      {{1}}
```javascript
console.log("=== Beispiel 10: Basis String-Methoden ===");

const rawInput = "  alice@example.com  ";
console.log("Raw input:", `"${rawInput}"`);

// trim() - Leerzeichen entfernen
const trimmed = rawInput.trim();
console.log("Trimmed:", `"${trimmed}"`);

// toLowerCase() / toUpperCase()
console.log("Lowercase:", trimmed.toLowerCase());
console.log("Uppercase:", trimmed.toUpperCase());

// split() - String in Array aufteilen
const email = "alice@example.com";
const parts = email.split("@");
console.log("\nEmail aufgeteilt:", parts);
console.log("Username:", parts[0]);
console.log("Domain:", parts[1]);

// join() - Array zu String zusammenführen
const words = ["Hello", "Database", "World"];
const sentence = words.join(" ");
console.log("\nWords:", words);
console.log("Sentence:", sentence);

console.log("--- Ende Beispiel 10 ---");
```
@eval

    --{{2}}--
Die Methoden replace, includes, startsWith und endsWith sind sehr nützlich für Suchen und Validierung.

      {{2}}
```javascript
console.log("=== Beispiel 11: Suchen & Ersetzen ===");

const url = "https://api.example.com/users/123/profile";

// includes() - prüft Vorhandensein
console.log("URL contains 'api':", url.includes("api"));
console.log("URL contains 'admin':", url.includes("admin"));

// startsWith() / endsWith()
console.log("\nURL starts with 'https':", url.startsWith("https"));
console.log("URL ends with 'profile':", url.endsWith("profile"));

// replace() - Ersetzung (nur erste Übereinstimmung)
const urlHttp = url.replace("https", "http");
console.log("\nOriginal:", url);
console.log("Replaced:", urlHttp);

// replaceAll() - alle Übereinstimmungen
const text = "foo bar foo baz foo";
console.log("\nOriginal:", text);
console.log("Replace first:", text.replace("foo", "XXX"));
console.log("Replace all:", text.replaceAll("foo", "XXX"));

console.log("--- Ende Beispiel 11 ---");
```
@eval

    --{{3}}--
Die Methoden slice, substring und substr extrahieren Teilstrings. Slice ist die modernste und flexibelste Variante.

      {{3}}
```javascript
console.log("=== Beispiel 12: Teilstrings extrahieren ===");

const dateString = "2025-10-22T14:30:00Z";
console.log("Original:", dateString);

// slice(start, end) - flexibel und modern
const year = dateString.slice(0, 4);
const month = dateString.slice(5, 7);
const day = dateString.slice(8, 10);
const time = dateString.slice(11, 19);

console.log("\nExtrahiert:");
console.log("Jahr:", year);
console.log("Monat:", month);
console.log("Tag:", day);
console.log("Zeit:", time);

// Negative Indizes - von hinten zählen
const lastFive = dateString.slice(-5);
console.log("\nLetzte 5 Zeichen:", lastFive);

// substring(start, end) - ähnlich wie slice, aber keine negativen Indizes
const protocol = dateString.substring(0, 4);
console.log("Substring (0,4):", protocol);

console.log("--- Ende Beispiel 12 ---");
```
@eval

    --{{4}}--
Die Methoden padStart und padEnd sind perfekt für formatierte Tabellen und alignierte Ausgaben.

      {{4}}
```javascript
console.log("=== Beispiel 13: Padding für Formatierung ===");

const users = [
  { id: 1, name: "Alice", score: 95 },
  { id: 42, name: "Bob", score: 1337 },
  { id: 999, name: "Charlie", score: 7 }
];

console.log("ID    | Name       | Score");
console.log("------|------------|------");

users.forEach(user => {
  // padStart() - links auffüllen
  const idPadded = String(user.id).padStart(5);
  
  // padEnd() - rechts auffüllen
  const namePadded = user.name.padEnd(10);
  const scorePadded = String(user.score).padStart(5);
  
  console.log(`${idPadded} | ${namePadded} | ${scorePadded}`);
});

console.log("--- Ende Beispiel 13 ---");
```
@eval

    --{{5}}--
Komplexere String-Operationen: Split mit Limit, Match mit RegEx, und praktische Kombinationen.

      {{5}}
```javascript
console.log("=== Beispiel 14: Fortgeschrittene String-Operationen ===");

// CSV-Parsing (einfach)
const csvLine = "Alice,alice@example.com,25,Admin";
const fields = csvLine.split(",");
console.log("CSV-Felder:", fields);

// Split mit Limit
const longText = "one,two,three,four,five";
const limited = longText.split(",", 3);
console.log("\nMit Limit 3:", limited);

// Mehrfaches Split für verschachtelte Daten
const config = "server:localhost:5432,user:admin,password:secret";
const configPairs = config.split(",");
console.log("\nConfig Pairs:", configPairs);

const configObject = {};
configPairs.forEach(pair => {
  const [key, ...values] = pair.split(":");
  configObject[key] = values.join(":");
});
console.log("Config Object:", configObject);

// Whitespace normalisieren
const messyText = "  Too    many     spaces   ";
const normalized = messyText.trim().split(/\s+/).join(" ");
console.log("\nMessy:", `"${messyText}"`);
console.log("Normalized:", `"${normalized}"`);

console.log("--- Ende Beispiel 14 ---");
```
@eval


### 9.5 Praktische String-Patterns für DB-Arbeit

    --{{0}}--
Jetzt kombinieren wir alle String-Techniken für typische Datenbank-Szenarien: Validierung, Formatierung, Parsing und Transformation.

    --{{1}}--
Email-Validierung ist ein klassischer Anwendungsfall. Hier eine einfache aber praktische Implementierung.

      {{1}}
```javascript
console.log("=== Beispiel 15: Email-Validierung ===");

function isValidEmail(email) {
  // Basic checks ohne komplexe RegEx
  const trimmed = email.trim().toLowerCase();
  
  // Muss @ enthalten
  if (!trimmed.includes("@")) {
    return { valid: false, reason: "Kein @ gefunden" };
  }
  
  // Aufteilen in local und domain
  const parts = trimmed.split("@");
  if (parts.length !== 2) {
    return { valid: false, reason: "Mehr als ein @ gefunden" };
  }
  
  const [local, domain] = parts;
  
  // Local part nicht leer
  if (local.length === 0) {
    return { valid: false, reason: "Local part fehlt" };
  }
  
  // Domain muss Punkt enthalten
  if (!domain.includes(".")) {
    return { valid: false, reason: "Domain ohne TLD" };
  }
  
  // Domain parts prüfen
  const domainParts = domain.split(".");
  if (domainParts.some(part => part.length === 0)) {
    return { valid: false, reason: "Leere Domain-Komponente" };
  }
  
  return { valid: true, email: trimmed };
}

// Tests
const testEmails = [
  "alice@example.com",
  "  BOB@EXAMPLE.COM  ",
  "invalid.email",
  "no-domain@",
  "@no-local.com",
  "double@@at.com",
  "no-tld@domain"
];

testEmails.forEach(email => {
  const result = isValidEmail(email);
  console.log(`"${email}"`);
  console.log("  →", result.valid ? `✅ Valid: ${result.email}` : `❌ ${result.reason}`);
});

console.log("--- Ende Beispiel 15 ---");
```
@eval

    --{{2}}--
SQL-Identifier müssen oft escaped oder validiert werden. Hier ein Beispiel für sichere Identifier-Formatierung.

      {{2}}
```javascript
console.log("=== Beispiel 16: SQL-Identifier formatieren ===");

function escapeIdentifier(identifier) {
  // Entferne gefährliche Zeichen, erlaube nur: a-z A-Z 0-9 _ -
  const cleaned = identifier.replace(/[^a-zA-Z0-9_-]/g, "_");
  
  // Darf nicht mit Zahl beginnen
  if (/^[0-9]/.test(cleaned)) {
    return `_${cleaned}`;
  }
  
  return cleaned;
}

function buildTableName(prefix, entity, suffix = null) {
  const parts = [prefix, entity, suffix].filter(p => p !== null);
  return parts.map(escapeIdentifier).join("_");
}

// Tests
console.log("Einzelne Identifier:");
console.log("user table →", escapeIdentifier("user table"));
console.log("my-column →", escapeIdentifier("my-column"));
console.log("123invalid →", escapeIdentifier("123invalid"));
console.log("valid_name →", escapeIdentifier("valid_name"));

console.log("\nKombinierte Tabellennamen:");
console.log(buildTableName("app", "users"));
console.log(buildTableName("app", "user orders", "archive"));
console.log(buildTableName("db", "products", "2024"));

console.log("--- Ende Beispiel 16 ---");
```
@eval

    --{{3}}--
Bei CSV-Export müssen Strings oft escaped werden, wenn sie Kommas oder Anführungszeichen enthalten.

      {{3}}
```javascript
console.log("=== Beispiel 17: CSV-Escaping ===");

function escapeCSVField(field) {
  const str = String(field);
  
  // Wenn Komma, Anführungszeichen oder Newline enthalten: in Quotes setzen
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    // Anführungszeichen verdoppeln
    const escaped = str.replace(/"/g, '""');
    return `"${escaped}"`;
  }
  
  return str;
}

function arrayToCSV(headers, rows) {
  // Header-Zeile
  const headerLine = headers.map(escapeCSVField).join(",");
  
  // Daten-Zeilen
  const dataLines = rows.map(row => {
    return row.map(escapeCSVField).join(",");
  });
  
  return [headerLine, ...dataLines].join("\n");
}

// Test-Daten
const headers = ["ID", "Name", "Description", "Price"];
const products = [
  [1, "Simple Product", "No special chars", 9.99],
  [2, 'Product "Pro"', "Contains quotes", 19.99],
  [3, "Combo Pack", "Mouse, Keyboard, Headset", 99.99],
  [4, "Special\nItem", "Multi-line description", 49.99]
];

const csv = arrayToCSV(headers, products);
console.log("Generiertes CSV:");
console.log(csv);

console.log("--- Ende Beispiel 17 ---");
```
@eval

    --{{4}}--
URL-Parameter parsen ist ein häufiger Task in Web-Anwendungen mit Datenbanken.

      {{4}}
```javascript
console.log("=== Beispiel 18: URL-Parameter parsen ===");

function parseQueryString(url) {
  // Finde Query-String nach ?
  const queryStart = url.indexOf("?");
  if (queryStart === -1) {
    return {};
  }
  
  const queryString = url.slice(queryStart + 1);
  
  // Split by & für einzelne Parameter
  const pairs = queryString.split("&");
  
  const params = {};
  pairs.forEach(pair => {
    const [key, value] = pair.split("=");
    
    // Decode URI components
    const decodedKey = decodeURIComponent(key);
    const decodedValue = decodeURIComponent(value || "");
    
    // Wenn Key bereits existiert, mache Array daraus
    if (params[decodedKey]) {
      if (Array.isArray(params[decodedKey])) {
        params[decodedKey].push(decodedValue);
      } else {
        params[decodedKey] = [params[decodedKey], decodedValue];
      }
    } else {
      params[decodedKey] = decodedValue;
    }
  });
  
  return params;
}

// Test-URLs
const testURLs = [
  "https://api.example.com/users?page=1&limit=10",
  "https://api.example.com/search?q=laptop&category=electronics&sort=price",
  "https://api.example.com/filter?tag=sale&tag=new&tag=featured",
  "https://api.example.com/user?name=Alice%20Cooper&age=25"
];

testURLs.forEach(url => {
  console.log("\nURL:", url);
  const params = parseQueryString(url);
  console.log("Parsed params:", params);
});

console.log("--- Ende Beispiel 18 ---");
```
@eval


### 9.6 Übungen: Strings

    --{{0}}--
Zeit zum Üben! Hier sind fünf Aufgaben, die typische String-Operationen im Datenbank-Kontext abdecken. Versuchen Sie zuerst selbst eine Lösung, bevor Sie die Musterlösung anschauen.

    --{{1}}--
**Übung 1: Username-Normalisierer**


Schreiben Sie eine Funktion `normalizeUsername(input)`, die:

- Leerzeichen am Anfang/Ende entfernt
- Alles zu lowercase konvertiert
- Nur Buchstaben, Zahlen, `-` und `_` erlaubt (Rest durch `_` ersetzen)
- Mindestens 3 Zeichen lang ist (sonst `null` zurückgeben)

      {{1}}
```javascript
console.log("=== Übung 1: Username-Normalisierer ===");

// IHRE LÖSUNG HIER
function normalizeUsername(input) {
  // TODO: Implementieren Sie die Funktion
}

// Test-Cases
const testUsers = [
  "  Alice123  ",
  "Bob@Example",
  "charlie-99",
  "ab",
  "TestUser_007",
  "Invalid User!"
];

testUsers.forEach(user => {
  const normalized = normalizeUsername(user);
  console.log(`"${user}" → ${normalized}`);
});

console.log("--- Ende Übung 1 ---");
```
@eval

      {{2}}
**************************

<details>
<summary>**Lösung zu Übung 1**</summary>

```javascript
console.log("=== Lösung zu Übung 1: Username-Normalisierer ===");

function normalizeUsername(input) {
  // 1. Leerzeichen entfernen und lowercase
  let normalized = input.trim().toLowerCase();
  
  // 2. Nur erlaubte Zeichen behalten
  normalized = normalized.replace(/[^a-z0-9_-]/g, "_");
  
  // 3. Mindestlänge prüfen
  if (normalized.length < 3) {
    return null;
  }
  
  return normalized;
}

// Test-Cases
const testUsers = [
  "  Alice123  ",      // → alice123
  "Bob@Example",       // → bob_example
  "charlie-99",        // → charlie-99
  "ab",                // → null (zu kurz)
  "TestUser_007",      // → testuser_007
  "Invalid User!"      // → invalid_user_
];

testUsers.forEach(user => {
  const normalized = normalizeUsername(user);
  console.log(`"${user}" → ${normalized}`);
});

console.log("--- Ende Lösung 1 ---");
```
@eval

</details>

**************************

    {{3}}
**************************

**Übung 2: CSV zu JSON**

Schreiben Sie eine Funktion `csvToJSON(csvString)`, die:

- Erste Zeile als Header interpretiert
- Folgezeilen als Datensätze interpretiert
- Array von Objekten zurückgibt
- Leere Zeilen ignoriert


```javascript
console.log("=== Übung 2: CSV zu JSON ===");

const csvData = `name,email,age
Alice,alice@example.com,25
Bob,bob@example.com,30

Charlie,charlie@example.com,28`;

// IHRE LÖSUNG HIER
function csvToJSON(csvString) {
  // TODO: Implementieren Sie die Funktion
  return [];
}

const result = csvToJSON(csvData);
console.log("Ergebnis:");
console.table(result);

console.log("--- Ende Übung 2 ---");
```
@eval

*************************

      {{4}}
**************************

<details>
<summary>**Lösung zu Übung 2**</summary>

```javascript
console.log("=== Lösung zu Übung 2: CSV zu JSON ===");

function csvToJSON(csvString) {
  // 1. In Zeilen aufteilen
  const lines = csvString.split("\n").filter(line => line.trim().length > 0);
  
  if (lines.length === 0) {
    return [];
  }
  
  // 2. Erste Zeile sind die Header
  const headers = lines[0].split(",").map(h => h.trim());
  
  // 3. Rest sind Daten
  const dataLines = lines.slice(1);
  
  // 4. Jede Zeile in Objekt umwandeln
  const result = dataLines.map(line => {
    const values = line.split(",").map(v => v.trim());
    
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = values[index] || "";
    });
    
    return obj;
  });
  
  return result;
}

const csvData = `name,email,age
Alice,alice@example.com,25
Bob,bob@example.com,30

Charlie,charlie@example.com,28`;

const result = csvToJSON(csvData);
console.log("Ergebnis:");
console.table(result);

console.log("--- Ende Lösung 2 ---");
```
@eval

</details>

**************************

    {{5}}
**************************

**Übung 3: Slug-Generator**

Schreiben Sie eine Funktion `generateSlug(title)`, die aus einem Titel einen URL-freundlichen Slug erzeugt:

- Lowercase
- Leerzeichen durch `-` ersetzen
- Umlaute ersetzen (ä→ae, ö→oe, ü→ue, ß→ss)
- Nur Buchstaben, Zahlen und `-` erlaubt
- Mehrfache `-` durch einzelnes ersetzen
- Keine `-` am Anfang/Ende

```javascript
console.log("=== Übung 3: Slug-Generator ===");

// IHRE LÖSUNG HIER
function generateSlug(title) {
  // TODO: Implementieren Sie die Funktion
  return "";
}

// Test-Cases
const titles = [
  "Hello World",
  "Über uns",
  "Produkt-Übersicht 2024",
  "  Extra   Spaces  ",
  "Special & Characters!",
  "Große Größen verfügbar"
];

titles.forEach(title => {
  const slug = generateSlug(title);
  console.log(`"${title}" → "${slug}"`);
});

console.log("--- Ende Übung 3 ---");
```
@eval

**************************

      {{6}}
**************************

<details>
<summary>**Lösung zu Übung 3**</summary>

```javascript
console.log("=== Lösung zu Übung 3: Slug-Generator ===");

function generateSlug(title) {
  // 1. Umlaute ersetzen
  let slug = title
    .replace(/ä/g, "ae")
    .replace(/ö/g, "oe")
    .replace(/ü/g, "ue")
    .replace(/ß/g, "ss")
    .replace(/Ä/g, "Ae")
    .replace(/Ö/g, "Oe")
    .replace(/Ü/g, "Ue");
  
  // 2. Lowercase
  slug = slug.toLowerCase();
  
  // 3. Alle Nicht-Alphanumerischen (außer Leerzeichen) durch "-" ersetzen
  slug = slug.replace(/[^a-z0-9\s-]/g, "-");
  
  // 4. Leerzeichen durch "-" ersetzen
  slug = slug.replace(/\s+/g, "-");
  
  // 5. Mehrfache "-" durch einzelnes ersetzen
  slug = slug.replace(/-+/g, "-");
  
  // 6. Trim "-" am Anfang/Ende
  slug = slug.replace(/^-+|-+$/g, "");
  
  return slug;
}

// Test-Cases
const titles = [
  "Hello World",                    // → hello-world
  "Über uns",                       // → ueber-uns
  "Produkt-Übersicht 2024",         // → produkt-uebersicht-2024
  "  Extra   Spaces  ",             // → extra-spaces
  "Special & Characters!",          // → special-characters
  "Große Größen verfügbar"          // → grosse-groessen-verfuegbar
];

titles.forEach(title => {
  const slug = generateSlug(title);
  console.log(`"${title}" → "${slug}"`);
});

console.log("--- Ende Lösung 3 ---");
```
@eval

</details>

**************************

      {{7}}
**************************

**Übung 4: SQL-Query-Builder**

Schreiben Sie eine Funktion `buildSelectQuery(options)`, die ein SQL-SELECT-Statement generiert:

- `options.table`: Tabellenname (required)
- `options.columns`: Array von Spalten (default: `["*"]`)
- `options.where`: Objekt mit Bedingungen (default: `{}`)
- `options.limit`: Anzahl (optional)

```javascript
console.log("=== Übung 4: SQL-Query-Builder ===");

// IHRE LÖSUNG HIER
function buildSelectQuery(options) {
  // TODO: Implementieren Sie die Funktion
  return "";
}

// Test-Cases
console.log(buildSelectQuery({ table: "users" }));
console.log();

console.log(buildSelectQuery({ 
  table: "products", 
  columns: ["id", "name", "price"] 
}));
console.log();

console.log(buildSelectQuery({
  table: "orders",
  columns: ["id", "total"],
  where: { status: "pending", amount_gt: "100" },
  limit: 10
}));

console.log("--- Ende Übung 4 ---");
```
@eval

**************************

      {{8}}
**************************

<details>
<summary>**Lösung zu Übung 4**</summary>

```javascript
console.log("=== Lösung zu Übung 4: SQL-Query-Builder ===");

function buildSelectQuery(options) {
  const { 
    table, 
    columns = ["*"], 
    where = {}, 
    limit 
  } = options;
  
  // SELECT Teil
  const selectClause = `SELECT ${columns.join(", ")}`;
  
  // FROM Teil
  const fromClause = `FROM ${table}`;
  
  // WHERE Teil
  let whereClause = "";
  const conditions = Object.entries(where);
  if (conditions.length > 0) {
    const conditionStrings = conditions.map(([key, value]) => {
      return `${key} = '${value}'`;
    });
    whereClause = `WHERE ${conditionStrings.join(" AND ")}`;
  }
  
  // LIMIT Teil
  const limitClause = limit ? `LIMIT ${limit}` : "";
  
  // Zusammenbauen
  const parts = [selectClause, fromClause, whereClause, limitClause]
    .filter(p => p.length > 0);
  
  return parts.join("\n");
}

// Test-Cases
console.log("Query 1:");
console.log(buildSelectQuery({ table: "users" }));
console.log();

console.log("Query 2:");
console.log(buildSelectQuery({ 
  table: "products", 
  columns: ["id", "name", "price"] 
}));
console.log();

console.log("Query 3:");
console.log(buildSelectQuery({
  table: "orders",
  columns: ["id", "total"],
  where: { status: "pending", amount_gt: "100" },
  limit: 10
}));

console.log("--- Ende Lösung 4 ---");
```
@eval

</details>

**************************

      {{9}}
**************************

**Übung 5: Log-Message-Formatter**

Schreiben Sie eine Funktion `formatLogMessage(level, message, meta)`, die Log-Nachrichten formatiert:

- `level`: "INFO", "WARN", "ERROR"
- `message`: Die Nachricht
- `meta`: Optional Objekt mit zusätzlichen Infos
- Format: `[TIMESTAMP] [LEVEL] message | meta as JSON`
- Timestamp im Format: `2025-10-22 14:30:45`

      {{9}}
```javascript
console.log("=== Übung 5: Log-Message-Formatter ===");

// IHRE LÖSUNG HIER
function formatLogMessage(level, message, meta = null) {
  // TODO: Implementieren Sie die Funktion
  return "";
}

// Test-Cases
console.log(formatLogMessage("INFO", "Database connected"));
console.log(formatLogMessage("WARN", "Slow query detected", { duration: 5000, table: "users" }));
console.log(formatLogMessage("ERROR", "Connection failed", { host: "localhost", port: 5432 }));

console.log("--- Ende Übung 5 ---");
```
@eval

*************************

      {{10}}
**************************

<details>
<summary>**Lösung zu Übung 5**</summary>

```javascript
console.log("=== Lösung zu Übung 5: Log-Message-Formatter ===");

function formatLogMessage(level, message, meta = null) {
  // 1. Timestamp erstellen
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  
  const timestamp = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  
  // 2. Level formatieren (feste Breite für Alignment)
  const levelPadded = level.padEnd(5);
  
  // 3. Meta-Infos als JSON (falls vorhanden)
  const metaPart = meta ? ` | ${JSON.stringify(meta)}` : "";
  
  // 4. Zusammenbauen
  return `[${timestamp}] [${levelPadded}] ${message}${metaPart}`;
}

// Test-Cases
console.log(formatLogMessage("INFO", "Database connected"));
console.log(formatLogMessage("WARN", "Slow query detected", { duration: 5000, table: "users" }));
console.log(formatLogMessage("ERROR", "Connection failed", { host: "localhost", port: 5432 }));

console.log("--- Ende Lösung 5 ---");
```
@eval

</details>

**************************

    --{{2}}--
Hervorragend! Sie beherrschen jetzt moderne String-Verarbeitung mit Template Literals und alle wichtigen String-Methoden. Diese Techniken werden Sie täglich beim Arbeiten mit Datenbanken einsetzen – für formatierte Ausgaben, Validierung, Parsing und Query-Building!



## Kapitel 10: IndexedDB – Alle Konzepte in der Praxis

    --{{0}}--
Jetzt kombinieren wir ALLE JavaScript-Konzepte aus den vorherigen Kapiteln! In diesem Capstone-Kapitel sehen Sie, wie Variablen, Objekte, Arrays, Async/Await, JSON und String-Operationen zusammenwirken, um mit IndexedDB – der Browser-Datenbank – zu arbeiten. Dies ist ein realistisches Beispiel, wie Sie in der Vorlesung Code sehen werden.

    {{0}}
<section>

**Was Sie in diesem Kapitel lernen:**

- IndexedDB öffnen und Schema erstellen
- Daten einfügen (INSERT), lesen (SELECT), aktualisieren (UPDATE), löschen (DELETE)
- Array-Methoden auf DB-Resultaten anwenden
- Error Handling und Transaktionen
- Komplettes User-Management-Beispiel

</section>

---

### 10.1 IndexedDB Basics – Die Browser-Datenbank

    --{{0}}--
IndexedDB ist eine NoSQL-Datenbank, die direkt im Browser läuft. Sie speichert JavaScript-Objekte persistent und bietet Indizes für schnelle Suchen. Alle Operationen sind asynchron – perfekt, um unser Async/Await-Wissen anzuwenden!

    {{0}}
<section>

**Datenbank öffnen:**

```javascript
console.log("=== Beispiel 1: Datenbank öffnen ===");

// Funktion zum Öffnen/Erstellen einer Datenbank
function openDatabase() {
  return new Promise((resolve, reject) => {
    console.log("🔄 Öffne Datenbank 'MyAppDB'...");
    
    // indexedDB.open(name, version)
    const request = indexedDB.open("MyAppDB", 1);
    
    // Bei Fehler
    request.onerror = () => {
      console.error("❌ Fehler beim Öffnen:", request.error);
      reject(request.error);
    };
    
    // Bei Erfolg
    request.onsuccess = () => {
      console.log("✅ Datenbank erfolgreich geöffnet");
      const db = request.result;
      console.log("Datenbank-Name:", db.name);
      console.log("Version:", db.version);
      resolve(db);
    };
    
    // Beim ersten Mal oder bei Version-Upgrade
    request.onupgradeneeded = (event) => {
      console.log("🔨 Datenbank-Schema wird erstellt/aktualisiert...");
      const db = event.target.result;
      
      // Object Store erstellen (= Tabelle in SQL)
      if (!db.objectStoreNames.contains("users")) {
        const objectStore = db.createObjectStore("users", { 
          keyPath: "id",      // Primary Key
          autoIncrement: true // Auto-Inkrement wie in SQL
        });
        
        // Index erstellen (für schnelle Suchen)
        objectStore.createIndex("email", "email", { unique: true });
        objectStore.createIndex("name", "name", { unique: false });
        
        console.log("✅ Object Store 'users' erstellt");
      }
    };
  });
}

// Async/Await verwenden (Kapitel 5!)
async function main() {
  try {
    const db = await openDatabase();
    console.log("Datenbank bereit:", db.name);
    db.close(); // Verbindung schließen
  } catch (error) {
    console.error("Fehler:", error);
  }
}

main();
console.log("--- Ende Beispiel 1 ---");
```
@eval

    --{{2}}--
Schauen wir uns an, was hier passiert: Wir nutzen **Promises** (Kapitel 5), **async/await** (Kapitel 5), **try/catch** (Kapitel 8), und **Objekte** (Kapitel 4). Das ist typischer Datenbank-Code!

      {{2}}
```javascript
console.log("=== Beispiel 2: Daten einfügen (CREATE) ===");

// Hilfsfunktion: DB öffnen
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// Funktion zum Einfügen eines Users
async function addUser(userData) {
  console.log(`📝 Füge User ein:`, userData);
  
  const db = await openDB();
  
  // Promise für die Transaktion
  return new Promise((resolve, reject) => {
    // Transaktion starten (readwrite = Schreibzugriff)
    const transaction = db.transaction(["users"], "readwrite");
    const objectStore = transaction.objectStore("users");
    
    // Daten hinzufügen
    const request = objectStore.add(userData);
    
    request.onsuccess = () => {
      const id = request.result; // Auto-generierte ID
      console.log(`✅ User eingefügt mit ID: ${id}`);
      resolve(id);
    };
    
    request.onerror = () => {
      console.error("❌ Fehler beim Einfügen:", request.error);
      reject(request.error);
    };
    
    // Transaktion abgeschlossen
    transaction.oncomplete = () => {
      db.close();
    };
  });
}

// Mehrere Users einfügen (async/await!)
async function insertUsers() {
  try {
    const id1 = await addUser({ name: "Alice", email: "alice@example.com", age: 25 });
    const id2 = await addUser({ name: "Bob", email: "bob@example.com", age: 30 });
    const id3 = await addUser({ name: "Charlie", email: "charlie@example.com", age: 28 });
    
    console.log(`\n✅ Alle Users eingefügt! IDs: ${id1}, ${id2}, ${id3}`);
  } catch (error) {
    console.error("❌ Fehler:", error.message);
  }
}

insertUsers();
console.log("--- Ende Beispiel 2 ---");
```
@eval

    --{{3}}--
Wichtig: Hier sehen Sie **Transaktionen** (wie in SQL!), **Promises verschachtelt in async/await**, und **Error Handling**. Alles, was Sie in Kapitel 5 und 8 gelernt haben!

</section>

---

### 10.2 Daten lesen – Array-Methoden auf DB-Resultaten

    --{{0}}--
Jetzt lesen wir Daten aus der Datenbank und nutzen Array-Methoden wie map, filter und reduce darauf – genau wie in Kapitel 4 gelernt!

    {{0}}
<section>

**Alle User auslesen:**

```javascript
console.log("=== Beispiel 3: Alle User auslesen (READ) ===");

// DB öffnen (gleiche Hilfsfunktion wie vorher)
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// Alle User auslesen
async function getAllUsers() {
  console.log("🔍 Lese alle User aus...");
  
  const db = await openDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["users"], "readonly");
    const objectStore = transaction.objectStore("users");
    
    // Alle Einträge holen
    const request = objectStore.getAll();
    
    request.onsuccess = () => {
      const users = request.result; // Array von Objekten!
      console.log(`✅ ${users.length} User gefunden`);
      resolve(users);
    };
    
    request.onerror = () => {
      console.error("❌ Fehler beim Lesen:", request.error);
      reject(request.error);
    };
    
    transaction.oncomplete = () => {
      db.close();
    };
  });
}

// Array-Methoden auf DB-Resultaten anwenden (Kapitel 4!)
async function analyzeUsers() {
  try {
    const users = await getAllUsers();
    
    // forEach - Alle ausgeben
    console.log("\n📋 Alle User:");
    users.forEach(user => {
      console.log(`  - ${user.name} (${user.email}), ${user.age} Jahre`);
    });
    
    // filter - Nur Erwachsene über 25
    const adults = users.filter(user => user.age > 25);
    console.log(`\n👥 User über 25: ${adults.length}`);
    adults.forEach(u => console.log(`  - ${u.name}: ${u.age}`));
    
    // map - Nur Namen extrahieren
    const names = users.map(user => user.name);
    console.log(`\n📝 Alle Namen: ${names.join(", ")}`);
    
    // reduce - Durchschnittsalter berechnen
    const avgAge = users.reduce((sum, user) => sum + user.age, 0) / users.length;
    console.log(`\n📊 Durchschnittsalter: ${avgAge.toFixed(1)} Jahre`);
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

analyzeUsers();
console.log("--- Ende Beispiel 3 ---");
```
@eval

    --{{2}}--
Sehen Sie? Die Datenbank gibt uns ein **Array von Objekten** zurück. Dann nutzen wir **forEach, filter, map, reduce** – genau wie in Kapitel 4! Das ist das typische Pattern.

      {{2}}
```javascript
console.log("=== Beispiel 4: Suche mit Index (WHERE-Klausel) ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// User nach Email suchen (Index nutzen!)
async function findUserByEmail(email) {
  console.log(`🔍 Suche User mit Email: ${email}`);
  
  const db = await openDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["users"], "readonly");
    const objectStore = transaction.objectStore("users");
    
    // Index verwenden (schnelle Suche!)
    const index = objectStore.index("email");
    const request = index.get(email);
    
    request.onsuccess = () => {
      const user = request.result;
      if (user) {
        console.log(`✅ User gefunden:`, user);
      } else {
        console.log(`❌ Kein User mit dieser Email`);
      }
      resolve(user);
    };
    
    request.onerror = () => reject(request.error);
    
    transaction.oncomplete = () => db.close();
  });
}

// Mehrere Suchen parallel (Promise.all aus Kapitel 5!)
async function searchMultiple() {
  try {
    console.time("Parallele Suche");
    
    const results = await Promise.all([
      findUserByEmail("alice@example.com"),
      findUserByEmail("bob@example.com"),
      findUserByEmail("unknown@example.com")
    ]);
    
    console.timeEnd("Parallele Suche");
    
    console.log("\n📊 Ergebnisse:");
    results.forEach((user, index) => {
      console.log(`Suche ${index + 1}:`, user ? user.name : "Nicht gefunden");
    });
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

searchMultiple();
console.log("--- Ende Beispiel 4 ---");
```
@eval

    --{{3}}--
Hier nutzen wir **Indizes** (wie in SQL!), **Promise.all()** für parallele Queries (Kapitel 5), und **console.time()** für Performance-Messung (Kapitel 8). Alles zusammen!

</section>

---

### 10.3 Daten aktualisieren & löschen (UPDATE & DELETE)

    --{{0}}--
CRUD ist komplett: Create, Read, Update, Delete. Schauen wir uns die letzten beiden Operationen an.

    {{0}}
<section>

**User aktualisieren (UPDATE):**

```javascript
console.log("=== Beispiel 5: User aktualisieren (UPDATE) ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// User aktualisieren
async function updateUser(id, updates) {
  console.log(`📝 Update User #${id}:`, updates);
  
  const db = await openDB();
  
  return new Promise(async (resolve, reject) => {
    try {
      const transaction = db.transaction(["users"], "readwrite");
      const objectStore = transaction.objectStore("users");
      
      // 1. Zuerst alten User holen
      const getRequest = objectStore.get(id);
      
      getRequest.onsuccess = () => {
        const user = getRequest.result;
        
        if (!user) {
          console.error(`❌ User #${id} nicht gefunden`);
          reject(new Error("User not found"));
          return;
        }
        
        console.log("📄 Alter Stand:", user);
        
        // 2. Objekt aktualisieren (Spread Operator aus Kapitel 4!)
        const updatedUser = { ...user, ...updates };
        console.log("📄 Neuer Stand:", updatedUser);
        
        // 3. Zurückschreiben
        const putRequest = objectStore.put(updatedUser);
        
        putRequest.onsuccess = () => {
          console.log("✅ User aktualisiert");
          resolve(updatedUser);
        };
        
        putRequest.onerror = () => {
          console.error("❌ Update fehlgeschlagen:", putRequest.error);
          reject(putRequest.error);
        };
      };
      
      getRequest.onerror = () => reject(getRequest.error);
      
      transaction.oncomplete = () => db.close();
      
    } catch (error) {
      reject(error);
    }
  });
}

// Beispiel-Updates
async function performUpdates() {
  try {
    // User #1 aktualisieren (nur Alter)
    await updateUser(1, { age: 26 });
    
    // User #2 aktualisieren (Name und Alter)
    await updateUser(2, { name: "Robert", age: 31 });
    
    console.log("\n✅ Alle Updates abgeschlossen");
    
  } catch (error) {
    console.error("❌ Fehler:", error.message);
  }
}

performUpdates();
console.log("--- Ende Beispiel 5 ---");
```
@eval

    --{{2}}--
Wichtig: Wir nutzen den **Spread Operator** `{ ...user, ...updates }` aus Kapitel 4, um das Objekt zu mergen. So bleiben nicht-aktualisierte Felder erhalten!

      {{2}}
```javascript
console.log("=== Beispiel 6: User löschen (DELETE) ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// User löschen
async function deleteUser(id) {
  console.log(`🗑️  Lösche User #${id}...`);
  
  const db = await openDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["users"], "readwrite");
    const objectStore = transaction.objectStore("users");
    
    const request = objectStore.delete(id);
    
    request.onsuccess = () => {
      console.log(`✅ User #${id} gelöscht`);
      resolve();
    };
    
    request.onerror = () => {
      console.error("❌ Löschen fehlgeschlagen:", request.error);
      reject(request.error);
    };
    
    transaction.oncomplete = () => db.close();
  });
}

// Alle User eines bestimmten Alters löschen (filter + forEach!)
async function deleteUsersByAge(minAge) {
  console.log(`🗑️  Lösche alle User über ${minAge} Jahre...`);
  
  try {
    // 1. Alle User holen
    const db = await openDB();
    const transaction = db.transaction(["users"], "readonly");
    const objectStore = transaction.objectStore("users");
    const users = await new Promise((resolve, reject) => {
      const request = objectStore.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
    db.close();
    
    // 2. Filtern (Kapitel 4!)
    const toDelete = users.filter(user => user.age >= minAge);
    console.log(`📋 ${toDelete.length} User gefunden`);
    
    // 3. Nacheinander löschen (for...of aus Kapitel 2!)
    for (const user of toDelete) {
      console.log(`  - Lösche ${user.name} (${user.age} Jahre)`);
      await deleteUser(user.id);
    }
    
    console.log("✅ Alle Löschungen abgeschlossen");
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

deleteUsersByAge(30);
console.log("--- Ende Beispiel 6 ---");
```
@eval

    --{{3}}--
Hier kombinieren wir **filter()** (Kapitel 4) mit **for...of** (Kapitel 2) und **async/await** (Kapitel 5). Das ist ein realistisches Pattern: Erst filtern, dann iterativ verarbeiten!

</section>

---

### 10.4 Error Handling & Transaktionen

    --{{0}}--
In Produktion müssen Fehler robust behandelt werden. Schauen wir uns defensive Programmierung und Transaktions-Rollback an.

    {{0}}
<section>

**Robustes Error Handling:**

```javascript
console.log("=== Beispiel 7: Robustes Error Handling ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// Funktion mit vollständigem Error Handling
async function addUserSafely(userData) {
  console.log(`\n📝 Versuche User einzufügen:`, userData);
  
  // Defensive Checks (Kapitel 8!)
  if (!userData) {
    throw new Error("userData darf nicht null sein");
  }
  
  if (!userData.name || typeof userData.name !== "string") {
    throw new Error("name ist required und muss ein String sein");
  }
  
  if (!userData.email || !userData.email.includes("@")) {
    throw new Error("Ungültige Email-Adresse");
  }
  
  if (typeof userData.age !== "number" || userData.age < 0) {
    throw new Error("age muss eine positive Zahl sein");
  }
  
  console.log("✅ Validierung erfolgreich");
  
  let db;
  try {
    db = await openDB();
    
    return await new Promise((resolve, reject) => {
      const transaction = db.transaction(["users"], "readwrite");
      const objectStore = transaction.objectStore("users");
      
      // Transaction Events
      transaction.oncomplete = () => {
        console.log("✅ Transaktion erfolgreich abgeschlossen");
      };
      
      transaction.onerror = () => {
        console.error("❌ Transaktion fehlgeschlagen:", transaction.error);
      };
      
      transaction.onabort = () => {
        console.error("🚫 Transaktion abgebrochen");
      };
      
      const request = objectStore.add(userData);
      
      request.onsuccess = () => {
        const id = request.result;
        console.log(`✅ User eingefügt mit ID: ${id}`);
        resolve(id);
      };
      
      request.onerror = () => {
        console.error("❌ Fehler beim Einfügen:", request.error);
        // Bei unique constraint violation auf Email
        if (request.error.name === "ConstraintError") {
          reject(new Error(`Email ${userData.email} bereits vergeben`));
        } else {
          reject(request.error);
        }
      };
    });
    
  } catch (error) {
    console.error("❌ Fehler:", error.message);
    throw error;
  } finally {
    // DB immer schließen (auch bei Fehler!)
    if (db) {
      db.close();
      console.log("🔒 Datenbank geschlossen");
    }
  }
}

// Test mit verschiedenen Szenarien
async function testErrorHandling() {
  try {
    // ✅ Valider User
    await addUserSafely({ name: "David", email: "david@example.com", age: 35 });
    
    // ❌ Fehlende Email
    await addUserSafely({ name: "Eve", age: 28 });
    
  } catch (error) {
    console.error("Test-Fehler:", error.message);
  }
  
  try {
    // ❌ Ungültiges Alter
    await addUserSafely({ name: "Frank", email: "frank@example.com", age: -5 });
    
  } catch (error) {
    console.error("Test-Fehler:", error.message);
  }
  
  try {
    // ❌ Doppelte Email (Constraint Violation)
    await addUserSafely({ name: "Alice2", email: "alice@example.com", age: 26 });
    
  } catch (error) {
    console.error("Test-Fehler:", error.message);
  }
}

testErrorHandling();
console.log("--- Ende Beispiel 7 ---");
```
@eval

    --{{2}}--
Das ist **defensive Programmierung** aus Kapitel 8: Alle Inputs validieren, alle Fehler catchen, Ressourcen im `finally`-Block freigeben. So schreibt man produktionsreifen Code!

      {{2}}
```javascript
console.log("=== Beispiel 8: Batch-Operationen mit Progress ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("name", "name", { unique: false });
      }
    };
  });
}

// Viele User auf einmal einfügen
async function batchInsert(users) {
  console.log(`📦 Batch-Insert von ${users.length} Users...`);
  console.time("Batch-Insert");
  
  const db = await openDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["users"], "readwrite");
    const objectStore = transaction.objectStore("users");
    
    let successCount = 0;
    let errorCount = 0;
    const results = [];
    
    // Alle Requests starten (asynchron!)
    users.forEach((user, index) => {
      const request = objectStore.add(user);
      
      request.onsuccess = () => {
        successCount++;
        const id = request.result;
        results.push({ success: true, id, user });
        
        // Progress ausgeben (Template Literal aus Kapitel 9!)
        const progress = ((successCount + errorCount) / users.length * 100).toFixed(1);
        console.log(`  [${progress}%] User ${index + 1}/${users.length}: ${user.name} → ID ${id}`);
      };
      
      request.onerror = () => {
        errorCount++;
        results.push({ success: false, user, error: request.error.message });
        console.error(`  ❌ User ${index + 1} fehlgeschlagen: ${request.error.message}`);
      };
    });
    
    transaction.oncomplete = () => {
      console.timeEnd("Batch-Insert");
      console.log(`\n✅ Batch abgeschlossen: ${successCount} erfolgreich, ${errorCount} Fehler`);
      db.close();
      resolve(results);
    };
    
    transaction.onerror = () => {
      console.error("❌ Transaktion fehlgeschlagen");
      db.close();
      reject(transaction.error);
    };
  });
}

// Test-Daten generieren (Array.from + map aus Kapitel 4!)
async function testBatchInsert() {
  const testUsers = Array.from({ length: 10 }, (_, i) => ({
    name: `User${i + 1}`,
    email: `user${i + 1}@batch.com`,
    age: 20 + (i % 40) // Alter zwischen 20 und 59
  }));
  
  try {
    const results = await batchInsert(testUsers);
    
    // Analyse mit reduce (Kapitel 4!)
    const summary = results.reduce((acc, r) => {
      if (r.success) {
        acc.successful.push(r.id);
      } else {
        acc.failed.push(r.error);
      }
      return acc;
    }, { successful: [], failed: [] });
    
    console.log("\n📊 Zusammenfassung:");
    console.log(`Erfolgreich: ${summary.successful.length} IDs`);
    console.log(`Fehlgeschlagen: ${summary.failed.length}`);
    
  } catch (error) {
    console.error("Batch-Fehler:", error);
  }
}

testBatchInsert();
console.log("--- Ende Beispiel 8 ---");
```
@eval

    --{{3}}--
Hier kombinieren wir: **Array.from()** zur Generierung, **forEach()** für Iteration, **reduce()** für Aggregation (alle Kapitel 4), **console.time()** für Performance (Kapitel 8), und **Template Literals** für Progress-Ausgabe (Kapitel 9)!

</section>

---

### 10.5 Komplexes Beispiel – User-Verwaltung komplett

    --{{0}}--
Jetzt bauen wir eine kleine User-Verwaltungs-API, die ALLE Konzepte vereint: CRUD, Error Handling, Array-Methoden, async/await, JSON, String-Operationen.

    {{0}}
<section>

**Vollständige User-Verwaltung:**

```javascript
console.log("=== Beispiel 9: Vollständige User-Verwaltung ===");

// ====== 1. DATABASE LAYER ======

class UserDatabase {
  constructor(dbName = "UserManagementDB") {
    this.dbName = dbName;
    this.version = 1;
  }
  
  // DB öffnen
  async open() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        
        if (!db.objectStoreNames.contains("users")) {
          const store = db.createObjectStore("users", { 
            keyPath: "id", 
            autoIncrement: true 
          });
          store.createIndex("email", "email", { unique: true });
          store.createIndex("role", "role", { unique: false });
        }
      };
    });
  }
  
  // User einfügen
  async create(userData) {
    const db = await this.open();
    
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(["users"], "readwrite");
      const store = transaction.objectStore("users");
      const request = store.add(userData);
      
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  }
  
  // Alle User lesen
  async readAll() {
    const db = await this.open();
    
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(["users"], "readonly");
      const store = transaction.objectStore("users");
      const request = store.getAll();
      
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  }
  
  // User nach ID lesen
  async readById(id) {
    const db = await this.open();
    
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(["users"], "readonly");
      const store = transaction.objectStore("users");
      const request = store.get(id);
      
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  }
  
  // User aktualisieren
  async update(id, updates) {
    const db = await this.open();
    
    return new Promise(async (resolve, reject) => {
      const transaction = db.transaction(["users"], "readwrite");
      const store = transaction.objectStore("users");
      
      const getRequest = store.get(id);
      getRequest.onsuccess = () => {
        const user = getRequest.result;
        if (!user) {
          reject(new Error("User not found"));
          return;
        }
        
        const updated = { ...user, ...updates };
        const putRequest = store.put(updated);
        
        putRequest.onsuccess = () => resolve(updated);
        putRequest.onerror = () => reject(putRequest.error);
      };
      
      getRequest.onerror = () => reject(getRequest.error);
      transaction.oncomplete = () => db.close();
    });
  }
  
  // User löschen
  async delete(id) {
    const db = await this.open();
    
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(["users"], "readwrite");
      const store = transaction.objectStore("users");
      const request = store.delete(id);
      
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  }
}

// ====== 2. BUSINESS LOGIC LAYER ======

class UserService {
  constructor() {
    this.db = new UserDatabase();
  }
  
  // User validieren (Kapitel 3 + 8!)
  validateUser(userData) {
    const errors = [];
    
    if (!userData.name || typeof userData.name !== "string" || userData.name.trim().length < 2) {
      errors.push("Name muss mindestens 2 Zeichen haben");
    }
    
    if (!userData.email || !userData.email.includes("@") || !userData.email.includes(".")) {
      errors.push("Ungültige Email-Adresse");
    }
    
    if (!userData.role || !["admin", "user", "guest"].includes(userData.role)) {
      errors.push("Rolle muss admin, user oder guest sein");
    }
    
    if (typeof userData.age !== "number" || userData.age < 0 || userData.age > 150) {
      errors.push("Alter muss zwischen 0 und 150 liegen");
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  // User erstellen (mit Validierung)
  async createUser(userData) {
    const validation = this.validateUser(userData);
    if (!validation.valid) {
      throw new Error(`Validierung fehlgeschlagen: ${validation.errors.join(", ")}`);
    }
    
    // Email normalisieren (Kapitel 9!)
    const normalized = {
      ...userData,
      email: userData.email.toLowerCase().trim(),
      name: userData.name.trim()
    };
    
    const id = await this.db.create(normalized);
    return { id, ...normalized };
  }
  
  // User-Statistiken (Array-Methoden aus Kapitel 4!)
  async getStats() {
    const users = await this.db.readAll();
    
    return {
      total: users.length,
      byRole: users.reduce((acc, user) => {
        acc[user.role] = (acc[user.role] || 0) + 1;
        return acc;
      }, {}),
      avgAge: users.reduce((sum, user) => sum + user.age, 0) / users.length,
      emails: users.map(u => u.email),
      oldestUser: users.reduce((oldest, user) => 
        user.age > oldest.age ? user : oldest
      , users[0])
    };
  }
  
  // User exportieren als JSON (Kapitel 6!)
  async exportUsersJSON() {
    const users = await this.db.readAll();
    return JSON.stringify(users, null, 2); // Pretty-print
  }
  
  // User importieren aus JSON
  async importUsersJSON(jsonString) {
    try {
      const users = JSON.parse(jsonString);
      
      if (!Array.isArray(users)) {
        throw new Error("JSON muss ein Array sein");
      }
      
      const results = [];
      for (const user of users) {
        try {
          const created = await this.createUser(user);
          results.push({ success: true, user: created });
        } catch (error) {
          results.push({ success: false, user, error: error.message });
        }
      }
      
      return results;
    } catch (error) {
      throw new Error(`JSON-Parse-Fehler: ${error.message}`);
    }
  }
}

// ====== 3. ANWENDUNG ======

async function demoUserManagement() {
  console.log("🚀 User-Verwaltung Demo startet...\n");
  
  const service = new UserService();
  
  try {
    // 1. User erstellen
    console.log("📝 Erstelle Test-User...");
    await service.createUser({ name: "Admin User", email: "admin@demo.com", role: "admin", age: 35 });
    await service.createUser({ name: "Normal User", email: "user@demo.com", role: "user", age: 28 });
    await service.createUser({ name: "Guest User", email: "guest@demo.com", role: "guest", age: 22 });
    console.log("✅ User erstellt\n");
    
    // 2. Statistiken anzeigen
    console.log("📊 Statistiken:");
    const stats = await service.getStats();
    console.log(`Total: ${stats.total} User`);
    console.log(`Nach Rolle:`, stats.byRole);
    console.log(`Durchschnittsalter: ${stats.avgAge.toFixed(1)} Jahre`);
    console.log(`Ältester User: ${stats.oldestUser.name} (${stats.oldestUser.age} Jahre)\n`);
    
    // 3. JSON-Export
    console.log("💾 JSON-Export:");
    const json = await service.exportUsersJSON();
    console.log(json);
    console.log();
    
    // 4. Fehlerhafte Validierung testen
    console.log("🧪 Teste Validierung (ungültiger User):");
    try {
      await service.createUser({ name: "X", email: "invalid", role: "hacker", age: -5 });
    } catch (error) {
      console.log("❌ Erwarteter Fehler:", error.message);
    }
    
    console.log("\n✅ Demo abgeschlossen!");
    
  } catch (error) {
    console.error("❌ Fehler in Demo:", error);
  }
}

demoUserManagement();
console.log("--- Ende Beispiel 9 ---");
```
@eval

    --{{2}}--
WOW! Das ist ein VOLLSTÄNDIGES Beispiel mit: **Klassen** (OOP), **async/await** überall, **CRUD-Operationen**, **Validierung**, **Array-Methoden** (map, reduce, filter), **Spread-Operator**, **JSON** (parse/stringify), **String-Normalisierung**, **Error Handling**, **Template Literals** – ALLES was Sie gelernt haben!

</section>

---

### 10.6 Übungen – IndexedDB Praxis

    --{{0}}--
Zeit, Ihr Wissen zu testen! Diese Übungen kombinieren alle Konzepte aus den vorherigen Kapiteln.

    {{0}}
<section>

**Übung 1: Produkt-Datenbank**

Erstellen Sie eine Produkt-Datenbank mit folgenden Features:
- Object Store "products" mit Auto-Increment ID
- Index auf "category"
- Funktion `addProduct(name, price, category, stock)`
- Funktion `getProductsByCategory(category)` – gibt Array zurück
- Funktion `getLowStockProducts(threshold)` – filtert Produkte mit wenig Lagerbestand

      {{1}}
```javascript
console.log("=== Übung 1: Produkt-Datenbank ===");

// IHRE LÖSUNG HIER

// Test-Code
async function testProductDB() {
  // TODO: Implementieren Sie Ihre Lösung und testen Sie hier
  console.log("Test läuft...");
}

testProductDB();
console.log("--- Ende Übung 1 ---");
```
@eval

      {{2}}
**************************

<details>
<summary>**Lösung zu Übung 1**</summary>

```javascript
console.log("=== Lösung zu Übung 1: Produkt-Datenbank ===");

function openProductDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("ProductDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      const store = db.createObjectStore("products", { keyPath: "id", autoIncrement: true });
      store.createIndex("category", "category", { unique: false });
    };
  });
}

async function addProduct(name, price, category, stock) {
  const db = await openProductDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["products"], "readwrite");
    const store = transaction.objectStore("products");
    const request = store.add({ name, price, category, stock });
    
    request.onsuccess = () => {
      console.log(`✅ Produkt "${name}" hinzugefügt (ID: ${request.result})`);
      resolve(request.result);
    };
    request.onerror = () => reject(request.error);
    transaction.oncomplete = () => db.close();
  });
}

async function getProductsByCategory(category) {
  const db = await openProductDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["products"], "readonly");
    const store = transaction.objectStore("products");
    const index = store.index("category");
    const request = index.getAll(category);
    
    request.onsuccess = () => {
      console.log(`✅ ${request.result.length} Produkte in Kategorie "${category}" gefunden`);
      resolve(request.result);
    };
    request.onerror = () => reject(request.error);
    transaction.oncomplete = () => db.close();
  });
}

async function getLowStockProducts(threshold) {
  const db = await openProductDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["products"], "readonly");
    const store = transaction.objectStore("products");
    const request = store.getAll();
    
    request.onsuccess = () => {
      // Filter mit Array-Methode!
      const lowStock = request.result.filter(p => p.stock <= threshold);
      console.log(`⚠️  ${lowStock.length} Produkte mit Lagerbestand <= ${threshold}`);
      resolve(lowStock);
    };
    request.onerror = () => reject(request.error);
    transaction.oncomplete = () => db.close();
  });
}

// Test
async function testProductDB() {
  try {
    await addProduct("Laptop", 999, "Electronics", 5);
    await addProduct("Mouse", 25, "Electronics", 150);
    await addProduct("Desk", 299, "Furniture", 2);
    await addProduct("Chair", 199, "Furniture", 0);
    
    console.log("\n📦 Elektronik-Produkte:");
    const electronics = await getProductsByCategory("Electronics");
    electronics.forEach(p => console.log(`  - ${p.name}: ${p.stock} Stück`));
    
    console.log("\n⚠️  Produkte mit niedrigem Lagerbestand (<=5):");
    const lowStock = await getLowStockProducts(5);
    lowStock.forEach(p => console.log(`  - ${p.name}: nur ${p.stock} Stück!`));
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

testProductDB();
console.log("--- Ende Lösung 1 ---");
```
@eval

</details>

**************************

    --{{3}}--
**Übung 2: Suchfunktion mit mehreren Kriterien**

Implementieren Sie `searchUsers(criteria)`, das nach mehreren Kriterien sucht:

- `criteria.minAge`, `criteria.maxAge` – Altersbereich
- `criteria.roles` – Array von erlaubten Rollen
- `criteria.emailDomain` – nur bestimmte Domain (z.B. "example.com")

Nutzen Sie `filter()` und String-Methoden!

      {{3}}
```javascript
console.log("=== Übung 2: Multi-Kriterien-Suche ===");

// IHRE LÖSUNG HIER

// Test-Code
async function testSearch() {
  // TODO: Ihre Tests hier
  console.log("Test läuft...");
}

testSearch();
console.log("--- Ende Übung 2 ---");
```
@eval

      {{4}}
**************************

<details>
<summary>**Lösung zu Übung 2**</summary>

```javascript
console.log("=== Lösung zu Übung 2: Multi-Kriterien-Suche ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("MyAppDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("users")) {
        const store = db.createObjectStore("users", { keyPath: "id", autoIncrement: true });
        store.createIndex("email", "email", { unique: true });
        store.createIndex("role", "role", { unique: false });
      }
    };
  });
}

async function searchUsers(criteria) {
  console.log("🔍 Suche mit Kriterien:", criteria);
  
  const db = await openDB();
  
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(["users"], "readonly");
    const store = transaction.objectStore("users");
    const request = store.getAll();
    
    request.onsuccess = () => {
      let results = request.result;
      
      // Filter 1: Altersbereich
      if (criteria.minAge !== undefined) {
        results = results.filter(u => u.age >= criteria.minAge);
      }
      if (criteria.maxAge !== undefined) {
        results = results.filter(u => u.age <= criteria.maxAge);
      }
      
      // Filter 2: Rollen
      if (criteria.roles && Array.isArray(criteria.roles)) {
        results = results.filter(u => criteria.roles.includes(u.role));
      }
      
      // Filter 3: Email-Domain (String-Methoden!)
      if (criteria.emailDomain) {
        results = results.filter(u => {
          const domain = u.email.split("@")[1];
          return domain === criteria.emailDomain;
        });
      }
      
      console.log(`✅ ${results.length} User gefunden`);
      resolve(results);
    };
    
    request.onerror = () => reject(request.error);
    transaction.oncomplete = () => db.close();
  });
}

// Test
async function testSearch() {
  try {
    console.log("\nTest 1: Alter 25-30");
    const result1 = await searchUsers({ minAge: 25, maxAge: 30 });
    result1.forEach(u => console.log(`  - ${u.name}: ${u.age} Jahre`));
    
    console.log("\nTest 2: Nur Admins");
    const result2 = await searchUsers({ roles: ["admin"] });
    result2.forEach(u => console.log(`  - ${u.name} (${u.role})`));
    
    console.log("\nTest 3: Email von 'example.com'");
    const result3 = await searchUsers({ emailDomain: "example.com" });
    result3.forEach(u => console.log(`  - ${u.name}: ${u.email}`));
    
    console.log("\nTest 4: Kombiniert (25-35 + admin/user + example.com)");
    const result4 = await searchUsers({ 
      minAge: 25, 
      maxAge: 35, 
      roles: ["admin", "user"],
      emailDomain: "example.com"
    });
    result4.forEach(u => console.log(`  - ${u.name}: ${u.age}, ${u.role}, ${u.email}`));
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

testSearch();
console.log("--- Ende Lösung 2 ---");
```
@eval

</details>

**************************

    --{{5}}--
**Übung 3: Performance-Vergleich**

Vergleichen Sie die Performance von:

1. Sequentieller Einfügung (await in Schleife)
2. Paralleler Einfügung (Promise.all)
3. Batch-Einfügung (eine Transaktion)

Nutzen Sie `console.time()` und fügen Sie jeweils 50 Test-Datensätze ein!

      {{5}}
```javascript
console.log("=== Übung 3: Performance-Vergleich ===");

// IHRE LÖSUNG HIER

async function performanceTest() {
  // TODO: Implementieren Sie die drei Methoden und messen Sie die Zeit
  console.log("Performance-Test läuft...");
}

performanceTest();
console.log("--- Ende Übung 3 ---");
```
@eval

      {{6}}
**************************

<details>
<summary>**Lösung zu Übung 3**</summary>

```javascript
console.log("=== Lösung zu Übung 3: Performance-Vergleich ===");

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("PerfTestDB", 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("items")) {
        db.createObjectStore("items", { keyPath: "id", autoIncrement: true });
      }
    };
  });
}

// Methode 1: Sequentiell
async function sequentialInsert(items) {
  console.log("\n🐌 Methode 1: Sequentiell");
  console.time("Sequential");
  
  for (const item of items) {
    const db = await openDB();
    await new Promise((resolve, reject) => {
      const transaction = db.transaction(["items"], "readwrite");
      const store = transaction.objectStore("items");
      const request = store.add(item);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  }
  
  console.timeEnd("Sequential");
}

// Methode 2: Parallel (Promise.all)
async function parallelInsert(items) {
  console.log("\n🚀 Methode 2: Parallel (Promise.all)");
  console.time("Parallel");
  
  const promises = items.map(async (item) => {
    const db = await openDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(["items"], "readwrite");
      const store = transaction.objectStore("items");
      const request = store.add(item);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
      transaction.oncomplete = () => db.close();
    });
  });
  
  await Promise.all(promises);
  console.timeEnd("Parallel");
}

// Methode 3: Batch (eine Transaktion)
async function batchInsert(items) {
  console.log("\n⚡ Methode 3: Batch (eine Transaktion)");
  console.time("Batch");
  
  const db = await openDB();
  
  await new Promise((resolve, reject) => {
    const transaction = db.transaction(["items"], "readwrite");
    const store = transaction.objectStore("items");
    
    items.forEach(item => {
      store.add(item);
    });
    
    transaction.oncomplete = () => {
      db.close();
      resolve();
    };
    transaction.onerror = () => reject(transaction.error);
  });
  
  console.timeEnd("Batch");
}

// Performance-Test
async function performanceTest() {
  const COUNT = 50;
  
  // Test-Daten generieren
  const generateItems = () => Array.from({ length: COUNT }, (_, i) => ({
    name: `Item ${i + 1}`,
    value: Math.random() * 1000
  }));
  
  try {
    // DB vorher leeren
    const db = await openDB();
    const clearTx = db.transaction(["items"], "readwrite");
    clearTx.objectStore("items").clear();
    await new Promise(resolve => { clearTx.oncomplete = resolve; });
    db.close();
    
    console.log(`📊 Performance-Test mit ${COUNT} Einträgen`);
    
    // Test 1: Sequentiell
    await sequentialInsert(generateItems());
    
    // Test 2: Parallel
    await parallelInsert(generateItems());
    
    // Test 3: Batch
    await batchInsert(generateItems());
    
    console.log("\n✅ Performance-Test abgeschlossen!");
    console.log("💡 Ergebnis: Batch ist am schnellsten, Parallel gut, Sequentiell am langsamsten");
    
  } catch (error) {
    console.error("❌ Fehler:", error);
  }
}

performanceTest();
console.log("--- Ende Lösung 3 ---");
```
@eval

</details>

**************************

</section>

    --{{2}}--
Fantastisch! Sie haben jetzt ein vollständiges Capstone-Kapitel durchgearbeitet, das ALLE JavaScript-Konzepte aus diesem Tutorial vereint. Von Variablen über Objekte und Arrays, async/await, JSON, String-Operationen bis hin zu Error Handling und Performance-Optimierung – alles in einem realistischen IndexedDB-Beispiel. Sie sind jetzt bereit für die Datenbank-Vorlesung!

---

## Zusammenfassung & Cheat Sheet

    --{{0}}--
Glückwunsch, Sie haben das Tutorial abgeschlossen! Hier ist eine kompakte Zusammenfassung aller wichtigen Konzepte. Nutzen Sie dieses Kapitel als Schnellreferenz, wenn Sie während der Vorlesung etwas nachschlagen möchten.

    {{0}}
<section>

**Was Sie in diesem Kapitel finden:**

- JavaScript Syntax Cheat Sheet (alle Basics)
- CRUD-Pattern für IndexedDB
- Häufige Fehler und wie man sie vermeidet
- Weiterführende Ressourcen

</section>

---

### 11.1 JavaScript Syntax Cheat Sheet

    --{{0}}--
Alle wichtigen Syntax-Elemente auf einen Blick – perfekt zum schnellen Nachschlagen während der Vorlesung.

    {{0}}
<section>

**Variablen & Datentypen:**

```javascript
console.log("=== Variablen & Datentypen – Quick Reference ===");

// Variablen-Deklaration
const constant = 42;           // Nicht änderbar, Block-Scope
let variable = "text";         // Änderbar, Block-Scope
var oldStyle = true;           // Vermeiden! Function-Scope

// Primitive Typen
const num = 123;               // Number
const str = "Hello";           // String
const bool = true;             // Boolean
const nothing = null;          // Null (explizit leer)
const undef = undefined;       // Undefined (nicht initialisiert)

// Typ prüfen
console.log(typeof num);       // "number"
console.log(typeof str);       // "string"
console.log(typeof bool);      // "boolean"

// Type Coercion vermeiden
console.log(5 === "5");        // false (strict equality)
console.log(5 == "5");         // true (loose equality - vermeiden!)

console.log("--- Ende ---");
```
@eval

    --{{2}}--
**Kontrollstrukturen**

      {{2}}
```javascript
console.log("=== Kontrollstrukturen – Quick Reference ===");

const age = 25;
const role = "admin";
const users = ["Alice", "Bob", "Charlie"];

// if/else
if (age >= 18) {
  console.log("Erwachsen");
} else {
  console.log("Minderjährig");
}

// Ternary Operator
const status = age >= 18 ? "adult" : "minor";
console.log("Status:", status);

// Switch
switch (role) {
  case "admin":
    console.log("Voller Zugriff");
    break;
  case "user":
    console.log("Eingeschränkter Zugriff");
    break;
  default:
    console.log("Kein Zugriff");
}

// for-Loop
for (let i = 0; i < users.length; i++) {
  console.log(`User ${i + 1}: ${users[i]}`);
}

// for...of (moderner!)
for (const user of users) {
  console.log(`User: ${user}`);
}

// while
let count = 0;
while (count < 3) {
  console.log(`Count: ${count}`);
  count++;
}

console.log("--- Ende ---");
```
@eval

    --{{3}}--
**Funktionen**

      {{3}}
```javascript
console.log("=== Funktionen – Quick Reference ===");

// Function Declaration
function add(a, b) {
  return a + b;
}

// Function Expression
const subtract = function(a, b) {
  return a - b;
};

// Arrow Function (kurz)
const multiply = (a, b) => a * b;

// Arrow Function (mehrzeilig)
const divide = (a, b) => {
  if (b === 0) return null;
  return a / b;
};

// Default Parameters
const greet = (name = "Guest") => `Hello, ${name}!`;

// Rest Parameters
const sum = (...numbers) => numbers.reduce((a, b) => a + b, 0);

// Tests
console.log("add(5, 3):", add(5, 3));
console.log("multiply(4, 7):", multiply(4, 7));
console.log("greet():", greet());
console.log("sum(1,2,3,4,5):", sum(1, 2, 3, 4, 5));

console.log("--- Ende ---");
```
@eval

    --{{4}}--
**Objekte & Arrays**

      {{4}}
```javascript
console.log("=== Objekte & Arrays – Quick Reference ===");

// Objekt erstellen
const user = {
  name: "Alice",
  age: 25,
  email: "alice@example.com",
  greet() {
    return `Hi, I'm ${this.name}`;
  }
};

console.log("User:", user.name, user["email"]);
console.log(user.greet());

// Destructuring
const { name, age } = user;
console.log(`${name} ist ${age} Jahre alt`);

// Spread Operator
const userCopy = { ...user, age: 26 };
console.log("Copy:", userCopy);

// Arrays
const numbers = [1, 2, 3, 4, 5];

// map - transformieren
const doubled = numbers.map(n => n * 2);
console.log("Doubled:", doubled);

// filter - filtern
const even = numbers.filter(n => n % 2 === 0);
console.log("Even:", even);

// reduce - aggregieren
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log("Sum:", sum);

// find - ersten finden
const found = numbers.find(n => n > 3);
console.log("First > 3:", found);

// some/every - Bedingungen prüfen
console.log("Some > 4:", numbers.some(n => n > 4));
console.log("All > 0:", numbers.every(n => n > 0));

console.log("--- Ende ---");
```
@eval

    --{{5}}--
**Asynchronität**

      {{5}}
```javascript
console.log("=== Asynchronität – Quick Reference ===");

// Promise erstellen
const fetchUser = (id) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: `User${id}` });
      } else {
        reject(new Error("Invalid ID"));
      }
    }, 100);
  });
};

// async/await (empfohlen!)
async function loadUser(id) {
  try {
    const user = await fetchUser(id);
    console.log("User geladen:", user);
    return user;
  } catch (error) {
    console.error("Fehler:", error.message);
    return null;
  }
}

// Promise.all() - parallel
async function loadMultiple() {
  try {
    const users = await Promise.all([
      fetchUser(1),
      fetchUser(2),
      fetchUser(3)
    ]);
    console.log("Alle Users:", users);
  } catch (error) {
    console.error("Fehler:", error);
  }
}

// Tests
loadUser(1);
loadUser(-1);
loadMultiple();

console.log("--- Ende ---");
```
@eval

    --{{6}}--
**JSON**

      {{6}}
```javascript
console.log("=== JSON – Quick Reference ===");

// JavaScript Object
const data = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  roles: ["admin", "user"]
};

// Object → JSON String
const jsonString = JSON.stringify(data);
console.log("JSON String:", jsonString);

// JSON String → Object
const parsed = JSON.parse(jsonString);
console.log("Parsed Object:", parsed);

// Pretty-Print JSON
const pretty = JSON.stringify(data, null, 2);
console.log("Pretty JSON:\n" + pretty);

// Deep Copy Trick
const deepCopy = JSON.parse(JSON.stringify(data));
deepCopy.name = "Bob";
console.log("Original:", data.name);
console.log("Copy:", deepCopy.name);

console.log("--- Ende ---");
```
@eval

    --{{7}}--
**Template Literals & Strings**

      {{7}}
```javascript
console.log("=== Template Literals & Strings – Quick Reference ===");

const name = "Alice";
const age = 25;

// Template Literal (Backticks!)
const message = `Hello, ${name}! You are ${age} years old.`;
console.log(message);

// Multiline String
const sql = `
SELECT * 
FROM users 
WHERE age > ${age}
LIMIT 10
`;
console.log(sql);

// String-Methoden
const email = "  Alice@Example.COM  ";
console.log("Original:", `"${email}"`);
console.log("trim():", `"${email.trim()}"`);
console.log("toLowerCase():", email.toLowerCase());
console.log("includes('@'):", email.includes("@"));
console.log("split('@'):", email.split("@"));

const text = "foo,bar,baz";
console.log("split(','):", text.split(","));
console.log("join('-'):", text.split(",").join("-"));

console.log("--- Ende ---");
```
@eval

    --{{8}}--
**Console & Debugging**

      {{8}}
```javascript
console.log("=== Console & Debugging – Quick Reference ===");

// Basis-Ausgabe
console.log("Normal log");
console.error("Fehler!");
console.warn("Warnung!");

// Objekte visualisieren
const user = { name: "Alice", age: 25, role: "admin" };
console.dir(user);

// Tabellen (perfekt für Arrays!)
const users = [
  { id: 1, name: "Alice", age: 25 },
  { id: 2, name: "Bob", age: 30 }
];
console.table(users);

// Gruppierung
console.group("User Details");
console.log("Name:", user.name);
console.log("Age:", user.age);
console.groupEnd();

// Performance messen
console.time("Operation");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("Operation");

// Assertions
console.assert(user.age > 18, "User muss erwachsen sein");

console.log("--- Ende ---");
```
@eval

</section>

---

### 11.2 Häufige Stolpersteine & Best Practices

    --{{0}}--
Diese Fehler machen Anfänger am häufigsten. Lernen Sie aus ihnen, bevor Sie darüber stolpern!

    {{0}}
<section>

**Stolperstein 1: var vs. let/const:**

```javascript
console.log("=== Stolperstein 1: var vs. let/const ===");

// ❌ SCHLECHT: var hat Function-Scope und Hoisting-Probleme
console.log("Mit var:");
for (var i = 0; i < 3; i++) {
  console.log(`Loop: ${i}`);
}
console.log(`Nach Loop: ${i}`); // i ist noch sichtbar! ❌

// ✅ GUT: let hat Block-Scope
console.log("\nMit let:");
for (let j = 0; j < 3; j++) {
  console.log(`Loop: ${j}`);
}
// console.log(j); // ReferenceError! ✅

// ✅ BEST PRACTICE: const für alles, was nicht geändert wird
const MAX_RETRIES = 3;
const API_URL = "https://api.example.com";

console.log("\n💡 Regel: const first, let wenn nötig, var NIE!");
console.log("--- Ende ---");
```
@eval

    --{{2}}--
**Stolperstein 2: == vs. ===**

      {{2}}
```javascript
console.log("=== Stolperstein 2: == vs. === ===");

// ❌ SCHLECHT: == macht Type Coercion
console.log("Mit == (loose equality):");
console.log("5 == '5':", 5 == "5");           // true ❌
console.log("0 == false:", 0 == false);       // true ❌
console.log("'' == false:", "" == false);     // true ❌
console.log("null == undefined:", null == undefined); // true ❌

// ✅ GUT: === prüft Typ UND Wert
console.log("\nMit === (strict equality):");
console.log("5 === '5':", 5 === "5");         // false ✅
console.log("0 === false:", 0 === false);     // false ✅
console.log("'' === false:", "" === false);   // false ✅
console.log("null === undefined:", null === undefined); // false ✅

console.log("\n💡 Regel: IMMER === und !== verwenden!");
console.log("--- Ende ---");
```
@eval

    --{{3}}--
**Stolperstein 3: Async-Funktionen nicht awaiten**

      {{3}}
```javascript
console.log("=== Stolperstein 3: Async nicht awaiten ===");

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchData() {
  await delay(100);
  return { data: "Wichtige Daten" };
}

// ❌ SCHLECHT: Async-Funktion ohne await
console.log("❌ Ohne await:");
const result1 = fetchData(); // Gibt Promise zurück!
console.log("Result:", result1); // Promise { <pending> }

// ✅ GUT: Mit await
async function correctWay() {
  console.log("\n✅ Mit await:");
  const result2 = await fetchData();
  console.log("Result:", result2); // { data: "Wichtige Daten" }
}

correctWay();

console.log("\n💡 Regel: Async-Funktionen IMMER mit await aufrufen!");
console.log("--- Ende ---");
```
@eval

    --{{4}}--
**Stolperstein 4: Array-Mutation vs. neue Arrays**

      {{4}}
```javascript
console.log("=== Stolperstein 4: Array-Mutation ===");

const original = [1, 2, 3, 4, 5];

// ❌ SCHLECHT: Mutiert das Original-Array
console.log("❌ Mit push() - mutiert:");
const bad = original;
bad.push(6);
console.log("Original:", original); // [1,2,3,4,5,6] - VERÄNDERT! ❌
console.log("Bad:", bad);           // [1,2,3,4,5,6]

// ✅ GUT: Erstellt neues Array
const original2 = [1, 2, 3, 4, 5];
console.log("\n✅ Mit Spread-Operator - neu:");
const good = [...original2, 6];
console.log("Original2:", original2); // [1,2,3,4,5] - UNVERÄNDERT! ✅
console.log("Good:", good);           // [1,2,3,4,5,6]

// ✅ GUT: map, filter, reduce erstellen neue Arrays
const doubled = original2.map(n => n * 2);
console.log("Doubled:", doubled);
console.log("Original2 immer noch:", original2);

console.log("\n💡 Regel: map/filter/reduce statt push/splice!");
console.log("--- Ende ---");
```
@eval

    --{{5}}--
**Stolperstein 5: Fehlendes Error Handling**

      {{5}}
```javascript
console.log("=== Stolperstein 5: Fehlendes Error Handling ===");

async function riskyOperation(value) {
  if (value < 0) {
    throw new Error("Negative Werte nicht erlaubt");
  }
  return value * 2;
}

// ❌ SCHLECHT: Kein Error Handling
console.log("❌ Ohne try/catch:");
async function badWay() {
  const result = await riskyOperation(-5); // Wirft Fehler!
  console.log("Result:", result); // Wird nie erreicht
}

badWay().catch(err => console.error("Unbehandelter Fehler:", err.message));

// ✅ GUT: Mit try/catch
console.log("\n✅ Mit try/catch:");
async function goodWay() {
  try {
    const result = await riskyOperation(-5);
    console.log("Result:", result);
  } catch (error) {
    console.error("Fehler behandelt:", error.message);
    // Fallback oder Wiederholung möglich
  }
}

goodWay();

console.log("\n💡 Regel: Async-Code IMMER in try/catch wrappen!");
console.log("--- Ende ---");
```
@eval

    --{{6}}--
**Stolperstein 6: Vergessenes JSON.parse()**

      {{6}}
```javascript
console.log("=== Stolperstein 6: Vergessenes JSON.parse() ===");

const jsonString = '{"name":"Alice","age":25}';

// ❌ SCHLECHT: String als Objekt behandeln
console.log("❌ Ohne JSON.parse():");
console.log("Type:", typeof jsonString);
console.log("String:", jsonString);
// console.log(jsonString.name); // undefined! ❌

// ✅ GUT: JSON parsen
console.log("\n✅ Mit JSON.parse():");
const obj = JSON.parse(jsonString);
console.log("Type:", typeof obj);
console.log("Object:", obj);
console.log("Name:", obj.name); // "Alice" ✅

// Umgekehrt: Object → JSON
console.log("\n✅ Mit JSON.stringify():");
const newObj = { name: "Bob", age: 30 };
const newJson = JSON.stringify(newObj);
console.log("Type:", typeof newJson);
console.log("JSON:", newJson);

console.log("\n💡 Regel: API-Response → parse(), vor API-Send → stringify()!");
console.log("--- Ende ---");
```
@eval

    --{{7}}--
**Stolperstein 7: Callback Hell**

      {{7}}
```javascript
console.log("=== Stolperstein 7: Callback Hell ===");

function delay(ms, callback) {
  setTimeout(callback, ms);
}

// ❌ SCHLECHT: Callback Hell (Pyramid of Doom)
console.log("❌ Callback Hell:");
delay(100, () => {
  console.log("Step 1");
  delay(100, () => {
    console.log("Step 2");
    delay(100, () => {
      console.log("Step 3");
      delay(100, () => {
        console.log("Step 4 - Unleserlich!");
      });
    });
  });
});

// ✅ GUT: async/await
console.log("\n✅ async/await:");
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function cleanWay() {
  await wait(100);
  console.log("Step 1");
  await wait(100);
  console.log("Step 2");
  await wait(100);
  console.log("Step 3");
  await wait(100);
  console.log("Step 4 - Lesbar!");
}

cleanWay();

console.log("\n💡 Regel: Promises + async/await statt Callbacks!");
console.log("--- Ende ---");
```
@eval

</section>

---

### 11.3 IndexedDB Pattern-Referenz

    --{{0}}--
Die wichtigsten IndexedDB-Patterns für die Datenbank-Vorlesung – kurz und prägnant.

    {{0}}
<section>

**CRUD-Operationen Cheat Sheet:**

```javascript
console.log("=== IndexedDB CRUD Cheat Sheet ===");

// Helper: DB öffnen
function openDB(name, version = 1) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(name, version);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains("items")) {
        db.createObjectStore("items", { keyPath: "id", autoIncrement: true });
      }
    };
  });
}

// CREATE - Einfügen
async function create(data) {
  const db = await openDB("CheatSheetDB");
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["items"], "readwrite");
    const store = tx.objectStore("items");
    const request = store.add(data);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
    tx.oncomplete = () => db.close();
  });
}

// READ - Alle lesen
async function readAll() {
  const db = await openDB("CheatSheetDB");
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["items"], "readonly");
    const store = tx.objectStore("items");
    const request = store.getAll();
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
    tx.oncomplete = () => db.close();
  });
}

// UPDATE - Aktualisieren
async function update(id, updates) {
  const db = await openDB("CheatSheetDB");
  return new Promise(async (resolve, reject) => {
    const tx = db.transaction(["items"], "readwrite");
    const store = tx.objectStore("items");
    const getReq = store.get(id);
    getReq.onsuccess = () => {
      const item = getReq.result;
      if (!item) {
        reject(new Error("Not found"));
        return;
      }
      const updated = { ...item, ...updates };
      const putReq = store.put(updated);
      putReq.onsuccess = () => resolve(updated);
      putReq.onerror = () => reject(putReq.error);
    };
    tx.oncomplete = () => db.close();
  });
}

// DELETE - Löschen
async function deleteItem(id) {
  const db = await openDB("CheatSheetDB");
  return new Promise((resolve, reject) => {
    const tx = db.transaction(["items"], "readwrite");
    const store = tx.objectStore("items");
    const request = store.delete(id);
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
    tx.oncomplete = () => db.close();
  });
}

// Demo
async function demo() {
  try {
    const id = await create({ name: "Test Item", value: 100 });
    console.log("✅ Created with ID:", id);
    
    const items = await readAll();
    console.log("✅ All items:", items);
    
    await update(id, { value: 200 });
    console.log("✅ Updated ID:", id);
    
    await deleteItem(id);
    console.log("✅ Deleted ID:", id);
  } catch (error) {
    console.error("❌ Error:", error);
  }
}

demo();
console.log("--- Ende ---");
```
@eval

</section>

---

### 11.4 Weiterführende Ressourcen

    --{{0}}--
Möchten Sie tiefer einsteigen? Hier sind die besten Ressourcen für fortgeschrittenes JavaScript-Lernen.

    {{0}}
<section>

**Offizielle Dokumentation:**
- **MDN Web Docs** (Mozilla Developer Network)  
  [https://developer.mozilla.org/de/docs/Web/JavaScript](https://developer.mozilla.org/de/docs/Web/JavaScript)  
  Die beste JavaScript-Referenz mit Beispielen und Browser-Kompatibilität

- **JavaScript.info**  
  [https://javascript.info](https://javascript.info)  
  Modernes Tutorial mit interaktiven Beispielen

- **IndexedDB API**  
  [https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)  
  Vollständige IndexedDB-Dokumentation

    --{{2}}--
**Interaktive Lernplattformen**

      {{2}}
- **freeCodeCamp**  
  [https://www.freecodecamp.org](https://www.freecodecamp.org)  
  Kostenlose Kurse mit praktischen Projekten

- **Exercism**  
  [https://exercism.org/tracks/javascript](https://exercism.org/tracks/javascript)  
  Code-Übungen mit Mentor-Feedback

- **JavaScript30**  
  [https://javascript30.com](https://javascript30.com)  
  30 Projekte in 30 Tagen (Vanilla JS)

    --{{3}}--
**Bücher & Videos**

      {{3}}
- **"Eloquent JavaScript"** von Marijn Haverbeke  
  Kostenlos online: [https://eloquentjavascript.net](https://eloquentjavascript.net)

- **"You Don't Know JS"** von Kyle Simpson  
  Deep-Dive in JavaScript-Mechanismen  
  [https://github.com/getify/You-Dont-Know-JS](https://github.com/getify/You-Dont-Know-JS)

- **JavaScript Mastery (YouTube)**  
  Moderne JavaScript-Tutorials und Projekte

    --{{4}}--
**Tools & Playground**

      {{4}}
- **CodePen**  
  [https://codepen.io](https://codepen.io)  
  Online-Editor für schnelles Experimentieren

- **JSFiddle**  
  [https://jsfiddle.net](https://jsfiddle.net)  
  Code teilen und testen

- **RunKit**  
  [https://runkit.com](https://runkit.com)  
  Node.js-Playground im Browser

- **VS Code**  
  Der beste Code-Editor für JavaScript  
  Mit Extensions: ESLint, Prettier, Bracket Pair Colorizer

    --{{5}}--
**Community & Hilfe**

      {{5}}
- **Stack Overflow**  
  [https://stackoverflow.com/questions/tagged/javascript](https://stackoverflow.com/questions/tagged/javascript)  
  Q&A für konkrete Probleme

- **Reddit /r/javascript**  
  [https://reddit.com/r/javascript](https://reddit.com/r/javascript)  
  News und Diskussionen

- **JavaScript Weekly Newsletter**  
  [https://javascriptweekly.com](https://javascriptweekly.com)  
  Wöchentliche Updates zu JavaScript

</section>

    --{{2}}--
Perfekt! Sie haben jetzt eine kompakte Referenz, die Sie während der gesamten Vorlesung nutzen können. Kommen Sie zurück zu diesem Cheat Sheet, wann immer Sie etwas schnell nachschlagen müssen!

---

    --{{3}}--
🎉 **Herzlichen Glückwunsch!** Sie haben das JavaScript-Tutorial erfolgreich abgeschlossen! Sie kennen jetzt alle Grundlagen, die Sie für die Datenbank-Vorlesung brauchen: Von Variablen über Objekte und Arrays, async/await, JSON, bis hin zu kompletten IndexedDB-Anwendungen. Nutzen Sie dieses Dokument als Nachschlagewerk während des Semesters. Viel Erfolg in der Vorlesung! 🚀
