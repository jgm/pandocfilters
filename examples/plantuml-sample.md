Use this


```
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: another authentication Response
```

to get

```plantuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: another authentication Response
```

with Äüö

```plantuml
Älöc -> Bob: Authentication Request
Bob --> Älöc: Authentication Response

Älöc -> Bob: Another authentication Request
Älöc <-- Bob: another authentication Response
```

See [(this is a link to whatever)](#whatever) for an example with options `{.plantuml #whatever caption="this is the caption" width=65%}`

```{.plantuml #whatever caption="this is the caption" width=65%}
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response
```
