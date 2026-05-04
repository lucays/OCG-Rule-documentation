# AGENTS.md

This repository is a Yu-Gi-Oh! OCG ruling documentation project. Agents working here should optimize for deterministic, locally consistent edits rather than freeform translation.

## Harness-style workflow

1. Read the neighboring entries in the target `.rst` file before editing.
2. Infer the local format from the current month/day block instead of inventing a new layout.
3. Make the smallest edit that preserves chronological order and source labeling.
4. After editing, re-read the changed block and verify wording, source label, date link, and quote markup.

## Source classification

- If the FAQ URL is from `yugioh-wiki.net`, add it under `| wiki:`.
- If the FAQ URL is from `db.yugioh-card.com`, add it under `| 数据库：`.
- If the user only provides Q/A text without a URL, treat it as mail content and add it under `| 邮件：`.
- Linked entries should follow the existing project style and end with the short date link, for example:
  - ``\ `26/4/25 <https://...>`__``

## Card name sourcing

- Card names inside Japanese `「」` or `《》` should be resolved from the external file:
  - `D:\codes\ygocdb-data\cards.json`
- Do not rely on the repository-local `cards.json` for this step.
- Use the `cn_name` field as the default Chinese card name for new FAQ translations.
- Do not default to `cnocg_n` when `cn_name` exists.
- If a card cannot be found immediately, first verify the lookup method before assuming the card is missing.

## Correct search method for `cards.json`

- Use Python with UTF-8 when querying the external card database, for example `python -X utf8 -`.
- Open the file with `encoding='utf-8'`.
- Prefer exact lookup by stable keys when available:
  - direct dict access by `cid`
  - exact `jp_name`
  - exact `wiki_en` / `en_name`
- If exact `jp_name` lookup fails, check whether the query string was corrupted by shell or terminal encoding.
- Also check for punctuation/normalization differences such as full-width vs half-width symbols, especially `－` vs `-`.
- A reliable fallback is:
  1. search by an ASCII field such as `wiki_en` or `en_name`
  2. confirm the matched `jp_name`
  3. take the corresponding `cn_name`
- Previous failure mode to avoid: passing Japanese literals through a shell path that produced mojibake, which made exact `jp_name` matching falsely return no result.

## Translation rules for FAQ entries

- Match the existing FAQ prose in `docs/c06/*.rst`.
- When the Japanese text contrasts `自分` and `相手`, translate `自分` as `我方`.
- `テキスト通り処理を行います` should be rendered as `正常适用`, not `按文本处理`.
- For returning cards to a location, prefer `让...回到某个场所` instead of `把...返回某个场所`.
- Keep ruling prose concise and declarative. Avoid adding explanation not present in the source.
- If effect text is quoted with `『』`, nested `「」` or `《》` inside that quoted effect text must **not** be wrapped with `` ` `` and `_`.
- Outside quoted effect text, card names should continue to use the repository's normal RST markup such as `「\`卡名\`_」`.

## Historical FAQ reconciliation

- Search for recent older FAQ entries involving the same card/ruling pattern before adding a new one.
- If the new FAQ changes or confirms an older FAQ that was previously different:
  - mark the old entry with `:strike:\`...\``
  - mark the new entry with `裁定变更：`
- If the old entry was `调整中` and the new FAQ resolves it:
  - mark the old entry with `:strike:\`...\``
  - mark the new entry with `调整中确认：`
- Only do this when the old and new entries are clearly the same ruling topic. If an older line bundles multiple cards or scenarios and the new FAQ only resolves part of it, split carefully or leave it untouched rather than over-editing.

## Edit checklist

- Correct month/day heading exists and order remains chronological.
- Source label matches the URL or absence of URL.
- Date link format matches neighboring entries.
- Card names match project usage.
- `我方/对方` wording is consistent.
- `正常适用` is used where the source says to process according to text.
- Returning cards to a location uses `让...回到某个场所` wording, not `把...返回某个场所`.
- Nested quoted effect text does not contain inappropriate card markup.
