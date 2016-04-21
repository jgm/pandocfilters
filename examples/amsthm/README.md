This is directly copy from `theorem.py` in [pandocfilters/examples at master · jgm/pandocfilters](https://github.com/jgm/pandocfilters/tree/master/examples).

`replace.sh` is written to generate any other combination. For example,

```bash
./replace.sh -f theorem -t lemma theorem.py
```

would copy `theorem.py` to `lemma.py` and replace both `theorem` and `Theorem` to `lemma` and `Lemma`.

I then used this script to generate the 13 environment that I used. This can be applied to any other environments.