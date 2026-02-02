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
uv run ff zho-hant/pol list vocabulary[lingshailuo]
uv run ff zho-hant/pol list vocabulary[lingshailuo/2]
```

Import:

```sh
uv run ff zho-hant/pol import vocabulary ./dat/zho-hant
uv run ff zho-hant/pol import vocabulary[lingshailuo] ./dat/zho-hant
uv run ff zho-hant/pol import vocabulary[lingshailuo/2] ./dat/zho-hant
```

Export:

```sh
uv run ff zho-hant/pol export vocabulary ./out
uv run ff zho-hant/pol export vocabulary[lingshailuo] ./out
uv run ff zho-hant/pol export vocabulary[lingshailuo/2] ./out
```
