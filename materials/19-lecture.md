<!--
author:   André Dietrich
email:    LiaScript@web.de
version:  1.0.0
language: de
narrator: Deutsch Female

logo:     ../assets/img/logo/19-lecture.jpg

comment:  Graph-Datenbanken & Semantic Web – RDF, SPARQL und DBpedia. Von Triples über interaktive SPARQL-Queries bis zu echten Knowledge Graphs.

import: https://raw.githubusercontent.com/LiaTemplates/Comunica/0.0.3/README.md

-->

# L19: Graph-Datenbanken & Semantic Web

> **Session 19 – Lecture**
>
> **Dauer:** 90 Minuten
>
> **Lernziele:** LZ 1 (Paradigmen & Einsatzszenarien verstehen), LZ 5 (Stärken/Schwächen bewerten)
>
> **Block:** 4 – Theorie, Optimierung & Polyglot

    --{{0}}--
Willkommen zur neunzehnten Session! Sie haben bereits Property Graphs mit Cypher kennengelernt. Heute tauchen wir in eine andere Graph-Welt ein: das Semantic Web mit RDF und SPARQL. Klingt akademisch? Ist es – aber auch extrem praktisch!

    --{{1}}--
Stellen Sie sich vor: Die gesamte Wikipedia als strukturierte Datenbank, die Sie mit SQL-ähnlichen Queries abfragen können. Das ist DBpedia – und genau damit arbeiten wir heute!

## Motivation: Vom Property Graph zum Knowledge Graph

    --{{0}}--
In Lecture 17 haben Sie Property Graphs kennengelernt: Knoten mit Labels und Properties, verbunden durch Relationships. Heute lernen Sie RDF – ein anderes Graph-Modell mit einem revolutionären Ziel: das Semantic Web!

### Property Graph vs. RDF

    {{1}}
**Property Graph (Neo4j, Cypher):**

    {{1}}
```cypher
(:Person {name: "Alice", age: 30})
  -[:KNOWS {since: 2020}]->
(:Person {name: "Bob", age: 28})
```

    {{2}}
**RDF (Resource Description Framework):**

    {{2}}
```turtle
<http://example.org/alice> a <http://example.org/Person> .
<http://example.org/alice> <http://example.org/name> "Alice" .
<http://example.org/alice> <http://example.org/age> 30 .
<http://example.org/alice> <http://example.org/knows> <http://example.org/bob> .
```

    --{{3}}--
Der große Unterschied? Property Graphs sind flexibel und pragmatisch. RDF ist strikt strukturiert und standardisiert – perfekt für das Web!

### Die Vision: Linked Open Data

    --{{0}}--
Warum ist RDF wichtig? Weil es das Web maschinenlesbar macht!

    {{1}}
**Das Problem heute:**

    {{1}}
```
Wikipedia   →  Nur für Menschen lesbar (HTML)
Google      →  Eigenes Schema (Knowledge Graph)
Wikidata    →  Eigenes Format
```

    {{2}}
**Die Vision: Semantic Web**

    {{2}}
```
Alle Daten    →  RDF (standardisiert!)
Alle Queries  →  SPARQL (standardisiert!)
Alle Links    →  URIs (eindeutig!)
```

    --{{3}}--
Stellen Sie sich vor: Jede Website stellt ihre Daten als RDF bereit. Ihr SPARQL-Query kann Wikipedia, Wikidata, DBpedia und Ihre eigene Datenbank gleichzeitig abfragen. Das ist Linked Open Data!

    {{3}}
**Reale Use Cases:**

    {{3}}
- **DBpedia** – Wikipedia als Knowledge Graph (15 Millionen Entities!)
- **Wikidata** – Kollaborative Wissensdatenbank (100 Millionen Items!)
- **Schema.org** – Strukturierte Daten für Suchmaschinen
- **Bio2RDF** – Biomedizinische Datenbanken vernetzt
- **GeoNames** – Geografische Daten weltweit

## Teil 1: RDF-Grundlagen

    --{{0}}--
RDF basiert auf einem einfachen Konzept: Alles ist ein Triple! Subject – Predicate – Object. Das war's.

### Triples: Subject – Predicate – Object

    --{{0}}--
Ein Triple ist wie eine Mini-Aussage in der Form "A tut B" oder "A ist B".

    {{1}}
**Beispiel: The Beatles**

    {{1}}
```
Subject               Predicate        Object
────────────────────  ───────────────  ─────────────────
:TheBeatles           rdf:type         :Band
:TheBeatles           :foundedIn       1960
:TheBeatles           :genre           :Rock
:TheBeatles           :hasMember       :JohnLennon
:JohnLennon           rdf:type         :Person
:JohnLennon           :name            "John Lennon"
```

    --{{2}}--
Sehen Sie das Pattern? Jedes Triple beschreibt eine Beziehung. Zusammen bilden sie einen Graph!

    {{2}}
**RDF = Flexible Tabelle:**

    {{2}}
| Subject      | Predicate   | Object        |
|--------------|-------------|---------------|
| :TheBeatles  | rdf:type    | :Band         |
| :TheBeatles  | :foundedIn  | 1960          |
| :TheBeatles  | :genre      | :Rock         |
| :TheBeatles  | :hasMember  | :JohnLennon   |
| :JohnLennon  | rdf:type    | :Person       |
| :JohnLennon  | :name       | "John Lennon" |

    --{{3}}--
RDF ist eigentlich nur eine große Tabelle mit drei Spalten. Aber durch die Verknüpfungen entsteht ein Graph!

### URIs: Globale Identifikatoren

    --{{0}}--
Der Schlüssel zum Semantic Web: Statt `id=42` verwenden wir URIs – eindeutig im gesamten Web!

    {{1}}
**Beispiel:**

    {{1}}
```
Schlecht:  id=12345, name="London"
Gut:       <http://dbpedia.org/resource/London>
```

    {{2}}
**Warum URIs?**

    {{2}}
- **Eindeutig:** London (UK) vs. London (Ontario) – verschiedene URIs
- **Verlinkbar:** URIs können auf andere Datensätze zeigen
- **Dereferencable:** URI aufrufen → Daten erhalten!

    {{3}}
```turtle
<http://dbpedia.org/resource/London>
  a dbo:City ;
  dbo:country <http://dbpedia.org/resource/United_Kingdom> ;
  dbo:population 8982000 ;
  rdfs:label "London"@en ;
  owl:sameAs <http://www.wikidata.org/entity/Q84> .
```

    --{{4}}--
Die letzte Zeile ist Gold wert: `owl:sameAs` verlinkt DBpedia-London mit Wikidata-London. So entsteht das Linked Data Web!

### Turtle-Syntax: RDF für Menschen

    --{{0}}--
Turtle ist eine lesbare Syntax für RDF. Viel besser als XML!

    {{1}}
**Volle URI-Form (unleserlich!):**

    {{1}}
```turtle
<http://example.org/TheBeatles> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/Band> .
<http://example.org/TheBeatles> <http://example.org/foundedIn> 1960 .
```

    {{2}}
**Mit Prefixes (lesbar!):**

    {{2}}
```turtle
@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:TheBeatles rdf:type ex:Band .
ex:TheBeatles ex:foundedIn 1960 .
```

    {{3}}
**Noch kompakter (Shortcuts!):**

    {{3}}
```turtle
@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:TheBeatles
  a ex:Band ;           # 'a' = rdf:type
  ex:foundedIn 1960 ;
  ex:genre ex:Rock ;
  ex:hasMember ex:JohnLennon , ex:PaulMcCartney , ex:GeorgeHarrison .
```

    --{{4}}--
Das Semikolon bedeutet "gleiches Subject, neues Predicate". Das Komma bedeutet "gleiches Subject + Predicate, neues Object". Elegant!

### Interaktiv: Euer erstes RDF

    --{{0}}--
Jetzt seid ihr dran! Hier ist ein kleines Musik-Knowledge-Graph. Schaut euch die Turtle-Syntax an – gleich fragen wir es mit SPARQL ab!

```turtle +Turtle: Musik-Bands
@prefix : <http://example.org/music#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:TheBeatles
  a :Band ;
  :name "The Beatles" ;
  :foundedIn 1960 ;
  :genre :Rock ;
  :hasMember :JohnLennon , :PaulMcCartney , :GeorgeHarrison , :RingoStarr ;
  :album :SgtPeppers , :AbbeyRoad .

:PinkFloyd
  a :Band ;
  :name "Pink Floyd" ;
  :foundedIn 1965 ;
  :genre :ProgressiveRock ;
  :hasMember :DavidGilmour , :RogerWaters , :NickMason , :RichardWright ;
  :album :DarkSideOfTheMoon , :TheWall .

:Radiohead
  a :Band ;
  :name "Radiohead" ;
  :foundedIn 1985 ;
  :genre :AlternativeRock ;
  :hasMember :ThomYorke , :JonnyGreenwood ;
  :album :OKComputer .

:JohnLennon
  a :Person ;
  :name "John Lennon" ;
  :birthYear 1940 .

:PaulMcCartney
  a :Person ;
  :name "Paul McCartney" ;
  :birthYear 1942 .

:GeorgeHarrison
  a :Person ;
  :name "George Harrison" ;
  :birthYear 1943 .

:RingoStarr
  a :Person ;
  :name "Ringo Starr" ;
  :birthYear 1940 .

:ThomYorke
  a :Person ;
  :name "Thom Yorke" ;
  :birthYear 1968 .

:DavidGilmour
  a :Person ;
  :name "David Gilmour" ;
  :birthYear 1946 .

:SgtPeppers
  a :Album ;
  :title "Sgt. Pepper's Lonely Hearts Club Band" ;
  :releaseYear 1967 .

:AbbeyRoad
  a :Album ;
  :title "Abbey Road" ;
  :releaseYear 1969 .

:DarkSideOfTheMoon
  a :Album ;
  :title "The Dark Side of the Moon" ;
  :releaseYear 1973 .

:OKComputer
  a :Album ;
  :title "OK Computer" ;
  :releaseYear 1997 .
```
```sparql -SPARQL: Alle Bands
SELECT ?band ?name ?year
WHERE {
  ?band a :Band .
  ?band :name ?name .
  ?band :foundedIn ?year .
}
ORDER BY ?year
```
@Comunica.RDF_SPARQL

    --{{1}}--
Perfekt! Ihr seht das Pattern? Das RDF definiert die Daten (Triples), SPARQL fragt sie ab (wie SQL SELECT). Gleich lernt ihr die SPARQL-Syntax!

## Teil 2: SPARQL – Die Query Language

    --{{0}}--
SPARQL ist für RDF, was SQL für relationale Datenbanken ist. Aber mit Graph-Semantik!

### SELECT: Grundstruktur

    --{{0}}--
Die Basis-Syntax ähnelt SQL – aber statt Tabellen matchen wir Triple-Patterns!

    {{1}}
**SQL-Reminder:**

    {{1}}
```sql
SELECT name, price
FROM products
WHERE category = 'Electronics';
```

    {{2}}
**SPARQL-Äquivalent:**

    {{2}}
```sparql
SELECT ?name ?price
WHERE {
  ?product :name ?name .
  ?product :price ?price .
  ?product :category :Electronics .
}
```

    --{{3}}--
Verstehen Sie den Unterschied? In SQL beschreiben Sie Tabellen und Spalten. In SPARQL beschreiben Sie Triple-Patterns: "Finde alles, wo Subject-Predicate-Object passt!"

### Pattern Matching: Das Herzstück

    --{{0}}--
SPARQL funktioniert durch Pattern Matching. Variables (`?variable`) werden an passende Werte gebunden.

    {{1}}
**Beispiel: Alle Mitglieder einer Band**

    {{1}}
```turtle +Daten (RDF)
:TheBeatles :hasMember :JohnLennon .
:TheBeatles :hasMember :PaulMcCartney .
:PinkFloyd :hasMember :DavidGilmour .
```
```sparql -Query (SPARQL)
SELECT ?member
WHERE {
  :TheBeatles :hasMember ?member .
}
```
@Comunica.RDF_SPARQL

    --{{2}}--
Das Pattern `:TheBeatles :hasMember ?member` matcht alle Triples mit diesem Subject und Predicate. Die Object-Werte werden an `?member` gebunden!

### Variables & Joins

    --{{0}}--
Mehrere Patterns in einer Query? Das ist ein JOIN – nur implizit durch gemeinsame Variables!

    {{1}}
**Beispiel: Bands mit ihren Mitgliedern UND deren Geburtsjahr**

    {{1}}
```turtle +Daten
:TheBeatles :hasMember :JohnLennon .
:JohnLennon :name "John Lennon" .
:JohnLennon :birthYear 1940 .

:TheBeatles :hasMember :PaulMcCartney .
:PaulMcCartney :name "Paul McCartney" .
:PaulMcCartney :birthYear 1942 .
```
```sparql -Query: Band-Mitglieder mit Geburtsjahr
SELECT ?bandName ?memberName ?birthYear
WHERE {
  ?band a :Band .
  ?band :name ?bandName .
  ?band :hasMember ?member .
  ?member :name ?memberName .
  ?member :birthYear ?birthYear .
  FILTER(?bandName = "The Beatles")
}
ORDER BY ?birthYear
```
@Comunica.RDF_SPARQL

    --{{2}}--
Sehen Sie die Magie? `?member` ist die gemeinsame Variable – sie verbindet beide Pattern-Gruppen. Das ist ein impliziter JOIN!

### SPARQL vs. SQL

    {{1}}
**Vergleichstabelle:**

    {{1}}
| Feature               | SQL                          | SPARQL                        |
|-----------------------|------------------------------|-------------------------------|
| **Datenmodell**       | Tabellen (relational)        | Triples (Graph)               |
| **SELECT**            | `SELECT col1, col2`          | `SELECT ?var1 ?var2`          |
| **FROM**              | `FROM table`                 | Implizit (Pattern matching)   |
| **WHERE**             | `WHERE col = value`          | `WHERE { pattern }`           |
| **JOIN**              | Explizit (`INNER JOIN`)      | Implizit (shared variables)   |
| **FILTER**            | `WHERE col > 100`            | `FILTER(?var > 100)`          |
| **ORDER BY**          | `ORDER BY col`               | `ORDER BY ?var`               |
| **LIMIT**             | `LIMIT 10`                   | `LIMIT 10`                    |
| **DISTINCT**          | `SELECT DISTINCT`            | `SELECT DISTINCT`             |
| **Aggregation**       | `COUNT()`, `SUM()`, `AVG()`  | `COUNT()`, `SUM()`, `AVG()`   |
| **GROUP BY**          | `GROUP BY col`               | `GROUP BY ?var`               |

    --{{2}}--
SPARQL ist SQL sehr ähnlich – aber statt Tabellen-Joins nutzen Sie Triple-Pattern-Matching. Das macht es flexibler für Graph-Daten!

### FILTER: Bedingungen wie SQL WHERE

    --{{0}}--
Mit FILTER schränken Sie Ergebnisse ein – wie SQL WHERE nach dem JOIN!

```turtle +Daten: Bands mit Gründungsjahr
@prefix : <http://example.org/music#> .

:TheBeatles a :Band ; :name "The Beatles" ; :foundedIn 1960 .
:PinkFloyd a :Band ; :name "Pink Floyd" ; :foundedIn 1965 .
:LedZeppelin a :Band ; :name "Led Zeppelin" ; :foundedIn 1968 .
:Radiohead a :Band ; :name "Radiohead" ; :foundedIn 1985 .
:Nirvana a :Band ; :name "Nirvana" ; :foundedIn 1987 .
```
```sparql -Query: Bands vor 1970
SELECT ?name ?year
WHERE {
  ?band a :Band .
  ?band :name ?name .
  ?band :foundedIn ?year .
  FILTER(?year < 1970)
}
ORDER BY ?year
```
@Comunica.RDF_SPARQL

    --{{1}}--
FILTER funktioniert wie SQL WHERE – aber nach dem Pattern Matching! Sie können `<`, `>`, `=`, `!=`, `&&`, `||` und Funktionen wie `REGEX()` nutzen.

### OPTIONAL: Wie SQL LEFT JOIN

    --{{0}}--
Manchmal fehlen Daten. OPTIONAL macht ein Pattern optional – wie LEFT JOIN!

```turtle +Daten: Bands (manche ohne Genre)
@prefix : <http://example.org/music#> .

:TheBeatles a :Band ; :name "The Beatles" ; :genre :Rock .
:PinkFloyd a :Band ; :name "Pink Floyd" ; :genre :ProgressiveRock .
:Radiohead a :Band ; :name "Radiohead" .
```
```sparql -Query: Alle Bands, Genre optional
SELECT ?name ?genre
WHERE {
  ?band a :Band .
  ?band :name ?name .
  OPTIONAL { ?band :genre ?genre . }
}
```
@Comunica.RDF_SPARQL

    --{{1}}--
Ohne OPTIONAL würde Radiohead nicht im Ergebnis erscheinen (weil kein Genre vorhanden). Mit OPTIONAL wird `?genre` einfach leer gelassen!

### Aggregation & GROUP BY

    --{{0}}--
Wie in SQL können Sie aggregieren und gruppieren!

```turtle +Daten: Bands mit mehreren Alben
@prefix : <http://example.org/music#> .

:TheBeatles a :Band ; :name "The Beatles" ; :album :A1 , :A2 , :A3 , :A4 .
:PinkFloyd a :Band ; :name "Pink Floyd" ; :album :A5 , :A6 .
:Radiohead a :Band ; :name "Radiohead" ; :album :A7 , :A8 , :A9 .
```
```sparql -Query: Anzahl Alben pro Band
SELECT ?name (COUNT(?album) AS ?albumCount)
WHERE {
  ?band a :Band .
  ?band :name ?name .
  ?band :album ?album .
}
GROUP BY ?name
ORDER BY DESC(?albumCount)
```
@Comunica.RDF_SPARQL

    --{{1}}--
Wie in SQL: GROUP BY gruppiert nach Variable, COUNT/SUM/AVG/MIN/MAX aggregieren. Die AS-Syntax ist identisch!

## Teil 3: DBpedia Showcase

    --{{0}}--
Jetzt wird es real! DBpedia ist Wikipedia als RDF – 15 Millionen Entities, 13 Milliarden Triples. Alles abfragbar mit SPARQL!

### Showcase 1: Bands mit nur einem Mitglied

    --{{0}}--
Euer Beispiel! Welche Bands haben nur ein einziges Mitglied? Das ist ungewöhnlich – schauen wir nach!

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?band (SAMPLE(?member) AS ?theMember)
WHERE {
  ?band a dbo:Band .
  ?band dbo:bandMember ?member .
}
GROUP BY ?band
HAVING (COUNT(?member) = 1)
LIMIT 20
```
@Comunica.SPARQL

    --{{1}}--
Interessant! Viele Solo-Projekte nutzen den Begriff "Band". Die Query gruppiert nach Band, zählt Mitglieder und filtert mit HAVING – wie in SQL!

### Showcase 2: Filme eines Regisseurs

    --{{0}}--
Christopher Nolan ist bekannt für komplexe Filme. Wie viele hat er gemacht?

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?filmName ?releaseYear
WHERE {
  ?director rdfs:label "Christopher Nolan"@en .
  ?film dbo:director ?director .
  ?film rdfs:label ?filmName .
  ?film dbo:releaseDate ?releaseDate .
  
  FILTER(LANG(?filmName) = "en")
  
  BIND(YEAR(?releaseDate) AS ?releaseYear)
}
ORDER BY ?releaseYear
LIMIT 30
```
@Comunica.SPARQL

    --{{1}}--
Sehen Sie die neuen Features? `LANG()` filtert nach Sprache (nur englische Labels), `BIND()` erstellt neue Variablen, `YEAR()` extrahiert das Jahr!

### Showcase 3: Größte Städte in Deutschland

    --{{0}}--
Welche deutschen Städte haben mehr als 500.000 Einwohner?

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?cityName ?population
WHERE {
  ?city a dbo:City .
  ?city dbo:country dbr:Germany .
  ?city rdfs:label ?cityName .
  ?city dbo:populationTotal ?population .
  
  FILTER(LANG(?cityName) = "de")
  FILTER(?population > 500000)
}
ORDER BY DESC(?population)
LIMIT 20
```
@Comunica.SPARQL

    --{{1}}--
Das ist die Power von DBpedia! Gleiche Query-Logik wie SQL – aber auf einem riesigen Knowledge Graph mit strukturierten Wikipedia-Daten!

### Showcase 4: Fußballspieler nach Land

    --{{0}}--
Wie viele Fußballspieler aus verschiedenen Ländern kennt DBpedia?

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?countryName (COUNT(?player) AS ?playerCount)
WHERE {
  ?player a dbo:SoccerPlayer .
  ?player dbo:birthPlace ?birthPlace .
  ?birthPlace dbo:country ?country .
  ?country rdfs:label ?countryName .
  
  FILTER(LANG(?countryName) = "en")
}
GROUP BY ?countryName
ORDER BY DESC(?playerCount)
LIMIT 15
```
@Comunica.SPARQL

    --{{1}}--
Aggregation über mehrere Joins! Das Pattern matcht Spieler → Geburtsort → Land, dann gruppiert und zählt. Wie SQL – nur mit Graph-Traversal!

### Showcase 5: Filme mit Budgets

    --{{0}}--
Welche Filme hatten die höchsten Budgets? Und wie viel haben sie eingespielt?

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?filmName ?budget ?gross
WHERE {
  ?film a dbo:Film .
  ?film rdfs:label ?filmName .
  ?film dbo:budget ?budget .
  ?film dbo:gross ?gross .
  
  FILTER(LANG(?filmName) = "en")
  FILTER(?budget > 200000000)
}
ORDER BY DESC(?budget)
LIMIT 20
```
@Comunica.SPARQL

    --{{1}}--
Optional könnten Sie hier auch `OPTIONAL { ?film dbo:gross ?gross }` nutzen, falls manche Filme kein Einspielergebnis haben. Dann würden sie trotzdem erscheinen!

### Showcase 6: Property Paths – Tiefe Beziehungen

    --{{0}}--
Property Paths sind ein SPARQL-Feature ohne SQL-Äquivalent! Sie traversieren Graphen in beliebiger Tiefe.

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?personName
WHERE {
  dbr:The_Beatles dbo:bandMember ?member .
  ?member dbo:associatedBand/dbo:bandMember ?person .
  ?person rdfs:label ?personName .
  
  FILTER(?person != ?member)
  FILTER(LANG(?personName) = "en")
}
LIMIT 30
```
@Comunica.SPARQL

    --{{1}}--
Das `/` bedeutet "folge dem Pfad": Beatles-Mitglied → andere Band → deren Mitglieder. Das ist Graph-Traversal – in SQL bräuchten Sie rekursive CTEs!

### Showcase 7: Federated Queries

    --{{0}}--
Das Killer-Feature! Eine Query über mehrere SPARQL-Endpoints hinweg – DBpedia + Wikidata gleichzeitig!

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?cityName ?dbpediaPop ?wikidataPop
WHERE {
  ?city a dbo:City .
  ?city dbo:country <http://dbpedia.org/resource/Germany> .
  ?city rdfs:label ?cityName .
  ?city dbo:populationTotal ?dbpediaPop .
  
  # Federated Query zu Wikidata!
  SERVICE <https://query.wikidata.org/sparql> {
    ?wikidataCity wdt:P31 wd:Q515 .
    ?wikidataCity rdfs:label ?cityName .
    ?wikidataCity wdt:P1082 ?wikidataPop .
  }
  
  FILTER(LANG(?cityName) = "en")
  FILTER(?dbpediaPop > 500000)
}
LIMIT 10
```
@Comunica.SPARQL

    --{{1}}--
SERVICE ist das Federated-Query-Feature! Es fragt einen anderen SPARQL-Endpoint ab. So können Sie Daten aus verschiedenen Quellen kombinieren – das Linked Data Prinzip in Aktion!

### Showcase 8: Komplexe Analyse – Alben pro Dekade

    --{{0}}--
Zum Abschluss eine komplexere Analyse: Wie viele Alben wurden pro Dekade veröffentlicht?

```sparql
# format: table
# source: https://dbpedia.org/sparql

PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?decade (COUNT(?album) AS ?albumCount)
WHERE {
  ?album a dbo:Album .
  ?album dbo:releaseDate ?releaseDate .
  
  FILTER(?releaseDate >= "1950-01-01"^^xsd:date)
  FILTER(?releaseDate < "2030-01-01"^^xsd:date)
  
  BIND(FLOOR(YEAR(?releaseDate) / 10) * 10 AS ?decade)
}
GROUP BY ?decade
ORDER BY ?decade
```
@Comunica.SPARQL

    --{{1}}--
Mathematik in SPARQL! `FLOOR(YEAR() / 10) * 10` rundet auf Dekaden. Das Ergebnis zeigt Trends in der Musikindustrie!

## Teil 4: Semantic Web & Linked Data

    --{{0}}--
Sie haben SPARQL in Aktion gesehen. Jetzt verstehen Sie, warum das Semantic Web wichtig ist!

### Die vier Linked Data Prinzipien

    {{1}}
**Tim Berners-Lee's Regeln für Linked Data:**

    {{1}}
1. **Nutze URIs** für Dinge (nicht IDs!)
2. **Nutze HTTP URIs** (dereferencable – auflösbar!)
3. **Biete nützliche Informationen** wenn jemand die URI aufruft (RDF!)
4. **Verlinke zu anderen Dingen** (externe URIs)

    --{{2}}--
Stellen Sie sich vor: Jede Website folgt diesen Regeln. Dann könnten Sie Daten aus beliebigen Quellen verknüpfen und abfragen – ohne APIs, ohne Integration!

### Real-World Use Cases

    {{1}}
**Wo wird RDF/SPARQL produktiv eingesetzt?**

    {{1}}
- **Google Knowledge Graph** – Schema.org Markup auf Websites
- **BBC** – Nachrichtenartikel als RDF verknüpft
- **Pharma & Life Sciences** – Bio2RDF verbindet Forschungsdatenbanken
- **Regierungen** – Open Government Data (UK, US)
- **Libraries** – BIBFRAME für Bibliothekskataloge
- **E-Commerce** – Schema.org für Produktdaten (SEO!)

    --{{2}}--
RDF ist keine akademische Spielerei – es steckt überall, wo strukturierte Daten im Web verknüpft werden!

### SPARQL Endpoints: Überall abfragbar

    {{1}}
**Öffentliche SPARQL-Endpoints (probiert sie aus!):**

    {{1}}
- **DBpedia:** https://dbpedia.org/sparql
- **Wikidata:** https://query.wikidata.org/
- **Bio2RDF:** http://bio2rdf.org/sparql
- **GeoNames:** http://factforge.net/sparql
- **OpenStreetMap:** https://sophox.org/sparql

    --{{2}}--
Jeder Endpoint ist wie eine öffentliche SQL-Datenbank – nur standardisiert mit SPARQL!

### RDF vs. Property Graphs: Der Vergleich

    {{1}}
| Aspekt                | RDF (Semantic Web)            | Property Graph (Neo4j)          |
|-----------------------|-------------------------------|---------------------------------|
| **Modell**            | Triples (S-P-O)               | Nodes + Relationships           |
| **Standardisierung**  | W3C Standard                  | Vendor-spezifisch               |
| **Schema**            | RDFS, OWL (optional)          | Schema-frei                     |
| **Query Language**    | SPARQL (Standard)             | Cypher / Gremlin (proprietär)   |
| **Flexibilität**      | Starr (Triples only)          | Flexibel (Properties auf allem) |
| **Linked Data**       | ✅ Core Feature                | ❌ Nicht vorgesehen              |
| **Performance**       | Langsamer (viele Joins)       | Schneller (Index-free adjacency)|
| **Use Case**          | Knowledge Graphs, Integration | Social Networks, Recommendations|
| **Tooling**           | Reif (Jena, Virtuoso)         | Sehr gut (Neo4j, ArangoDB)      |

    --{{2}}--
Es gibt kein "besser" – nur "besser für X"! RDF für offene, verlinkte Daten. Property Graphs für Performance und Flexibilität.

## Wrap-up & Quiz

    --{{0}}--
Sie haben heute eine komplett neue Welt kennengelernt: das Semantic Web mit RDF und SPARQL!

### Was Sie gelernt haben

    {{1}}
✅ **RDF-Konzept:** Triples, URIs, Turtle-Syntax  
✅ **SPARQL-Syntax:** SELECT, WHERE, FILTER, OPTIONAL, GROUP BY  
✅ **Pattern Matching:** Implizite JOINs durch gemeinsame Variablen  
✅ **DBpedia:** Real-world Knowledge Graph mit 15M Entities  
✅ **Linked Data:** Vision des maschinenlesbaren Webs  
✅ **Property Paths:** Graph-Traversal ohne SQL-Rekursion  
✅ **Federated Queries:** Multiple Endpoints in einer Query

### Quiz: RDF & SPARQL

    {{1}}
**1) Was ist ein RDF Triple?**

    {{1}}
- [( )] Eine dreifache Beziehung zwischen Tabellen
- [(X)] Subject – Predicate – Object
- [( )] Ein dreifach normalisiertes Schema
- [( )] Drei verknüpfte Graphenknoten

    {{2}}
**2) Wie funktionieren JOINs in SPARQL?**

    {{2}}
- [( )] Mit `INNER JOIN` wie in SQL
- [(X)] Implizit durch gemeinsame Variablen
- [( )] Mit `MATCH` wie in Cypher
- [( )] Gar nicht – SPARQL hat keine JOINs

    {{3}}
**3) Was macht `OPTIONAL { }` in SPARQL?**

    {{3}}
- [( )] Markiert optionale Felder im Schema
- [(X)] Funktioniert wie LEFT JOIN (Pattern kann fehlen)
- [( )] Optimiert die Query-Performance
- [( )] Definiert Fallback-Werte

    {{4}}
**4) Was ist DBpedia?**

    {{4}}
- [( )] Eine neue SQL-Datenbank von Wikipedia
- [(X)] Wikipedia-Inhalte als RDF Knowledge Graph
- [( )] Ein Python-Library für Datenbankzugriff
- [( )] Ein Property-Graph-Datenbank-System

    {{5}}
**5) Was bedeutet Linked Data?**

    {{5}}
- [( )] Datenbanken mit Foreign Keys
- [( )] Mehrere Nodes mit Relationships
- [(X)] Web-Ressourcen verknüpft mit URIs und RDF
- [( )] GraphQL-APIs mit Nested Queries

### Reflexion

    {{1}}
**1-Minute-Paper:**

    {{1}}
?[Was ist der größte Vorteil von RDF gegenüber Property Graphs – und was ist der größte Nachteil?]

    {{2}}
**Diskussion:**

    {{2}}
Wann würdet ihr für ein Projekt RDF/SPARQL wählen, wann Neo4j/Cypher? Begründet eure Wahl mit Use Cases!

## Ausblick & Vertiefung

    --{{0}}--
RDF und SPARQL sind ein Einstieg in eine größere Welt!

### Nächste Schritte

    {{1}}
**Wenn ihr tiefer einsteigen wollt:**

    {{1}}
- **Tools ausprobieren:**
  - Apache Jena (Java RDF Framework)
  - Virtuoso (High-Performance Triple Store)
  - GraphDB (kommerzielle Lösung)
  - Stardog (Knowledge Graph Platform)

    {{1}}
- **Ontologien lernen:**
  - RDFS (Schema-Layer für RDF)
  - OWL (Web Ontology Language – Logik & Reasoning)
  - SHACL (Schema-Validation für RDF)

    {{1}}
- **Datasets erkunden:**
  - Wikidata Query Service (benutzerfreundlich!)
  - Bio2RDF (Life Sciences)
  - GeoNames (Geografische Daten)

### Graph-Paradigmen im Vergleich

    {{1}}
**Die drei Graph-Welten:**

    {{1}}
| Paradigma          | Beispiel        | Use Case                      |
|--------------------|-----------------|-------------------------------|
| **Property Graph** | Neo4j (Cypher)  | Social Networks, Fraud        |
| **RDF Graph**      | DBpedia (SPARQL)| Knowledge Graphs, Linked Data |
| **Hypergraph**     | TigerGraph      | Multi-dimensional Relations   |

    --{{2}}--
Ihr habt jetzt beide Hauptparadigmen gesehen: Property Graphs (L17) und RDF (heute). Nächste Session: Wie man beide in einer Architektur nutzt!

### Resources

    {{1}}
**Zum Weiterlesen:**

    {{1}}
- **W3C SPARQL Spec:** https://www.w3.org/TR/sparql11-query/
- **DBpedia SPARQL Endpoint:** https://dbpedia.org/sparql
- **Wikidata Query Service:** https://query.wikidata.org/
- **"Learning SPARQL"** (Bob DuCharme, O'Reilly)
- **LOD Cloud Diagram:** https://lod-cloud.net/

---

    --{{0}}--
Das war's für heute! Ihr habt das Semantic Web kennengelernt – eine Vision eines maschinenlesbaren Webs mit strukturierten, verlinkten Daten. In der nächsten Vorlesung schauen wir uns an, wie man verschiedene Datenbank-Paradigmen in einer Architektur kombiniert: Polyglot Persistence!

**Bis zur nächsten Session! 🎓**
