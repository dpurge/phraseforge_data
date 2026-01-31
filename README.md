# PhraseForge data

Help:

```sh
uv run ff --help
uv run ff import --help
uv run ff list --help
uv run ff export --help
```

List:

```sh
uv run ff zho-hant/pol list vocabulary
uv run ff zho-hant/pol list vocabulary[lingshailo]
uv run ff zho-hant/pol list vocabulary[lingshailo/2]
```

Import:

```sh
uv run ff zho-hant/pol import ./dat/zho-hant

uv run ff zho-hant/pol import vocabulary ./dat/zho-hant
uv run ff zho-hant/pol import vocabulary[lingshailo] ./dat/zho-hant
uv run ff zho-hant/pol import vocabulary[lingshailo/2] ./dat/zho-hant
```

Export:

```sh
uv run ff zho-hant/pol export vocabulary ./out
uv run ff zho-hant/pol export vocabulary[lingshailo] ./out
uv run ff zho-hant/pol export vocabulary[lingshailo/2] ./out
```
