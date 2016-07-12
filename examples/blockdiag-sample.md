Use this


```
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

to get

```blockdiag
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```

with Äüö

```blockdiag
blockdiag {
   Ä -> Bü -> Cö -> D;
   Ä -> E -> F -> G;
}
```

See [(this is a link to whatever)](#whatever) for an example with options `{.plantuml #whatever caption="this is the caption" width=65%}`

```{.blockdiag #whatever caption="this is the caption" width=65%}
blockdiag {
   A -> B -> C -> D;
   A -> E -> F -> G;
}
```
