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
- `一時的に除外` should be rendered as `一时除外`, not `暂时除外`.
- For returning cards to a location, prefer `让...回到某个场所` instead of `把...返回某个场所`.
- When translating effect costs, use `cost` directly (e.g. `作为cost送去墓地`) instead of translating to `成本`.
- Do not use `该` in ruling prose. Render `この～` as `这个/这次/这只/这张` and `その～` as `那个/那次/那只/那张`, choosing the word that matches the referent (卡/效果/怪兽/场合 etc.).
- When `同调`/`超量`/`连接` appear outside card names and quoted effect text, use `S`/`X`/`L` shorthand instead, e.g. `S怪兽`、`X素材`、`S召唤` or `S·X·L`. Inside card names and `『』` effect text, keep the full Chinese terms from the official card text.
- Punctuation: Japanese `、` performs **two** jobs (coordinate nouns **and** clause/predicate separation via 連用中止形 `～し、～して、～たり、`). Only the first maps to Chinese `、`; carrying the second over as `、` is the most common defect in this repo. Use `，` at clause and predicate boundaries, in action sequences (e.g. `发动「`卡名`_」的效果，解放自身并以…为对象`), across chained chain links (e.g. `我方连锁1发动A，对方连锁2发动B`) and in state/condition descriptions (e.g. `我方手卡7张，我方场上存在「`卡名`_」，对方场上存在…`). Reserve `、` for short coordinate words/phrases only: enumerated card names with effect markers (e.g. `「`卡名A`_」①、「`卡名B`_」②`) and short parallel terms (e.g. `L召唤、X召唤或S召唤`). Do not put `、` directly before `或`/`或者` when the joined parts are clauses or long phrases. See **`## Punctuation: 、 vs ，`** below for the decision table, real defects, self-check script and fix procedure.
- If the official/mail answer only says to discuss with the opponent or proceed by judge decision instead of giving a ruling, summarize the pending question and mark it with ``\ :ref:`调整中`\ 。`` rather than translating the customer-service wording.
- Keep ruling prose concise and declarative. Avoid adding explanation not present in the source.
- If effect text is quoted with `『』`, do not freely translate the Japanese text. Identify the card whose effect text is being quoted, look it up in the external `D:\codes\ygocdb-data\cards.json`, and use the corresponding Chinese effect text from `text.desc` / `text.pdesc` as the source for the quoted wording.
- If effect text is quoted with `『』`, nested `「」` or `《》` inside that quoted effect text must **not** be wrapped with `` ` `` and `_`.
- Outside quoted effect text, card names should continue to use the repository's normal RST markup such as `「\`卡名\`_」`.

## Punctuation: `、` (顿号) vs `，` (逗号)

Japanese `、` does **two different jobs**. Translating it mechanically as Chinese `、` is the single most frequent defect in this repository.

1. **Coordinate listing** (nouns, short terms) → Chinese keeps `、`.
2. **Clause / predicate separation** (`～し、～して、～たり、～なり、` "連用中止法", or an adverb clause like `その後～`, `そのターン中に～`) → Chinese must use `，`.

Decide by asking **what the `、` is joining**:

| The `、` joins… | Use | Example (from this repo) |
|---|---|---|
| coordinate **nouns / short terms** | `、` | `「`卡名A`_」①、「`卡名B`_」②`；`L召唤、X召唤或S召唤`；`送去墓地、除外、从场上离开、加入手卡`；`上级召唤、S召唤、仪式召唤、融合召唤` |
| **predicates / actions / state changes** | `，` | `变成里侧守备表示，之后又变回表侧表示`；`一时除外，那个回合中以表侧表示回到怪兽区` |
| **chain links** | `，` | `我方连锁1发动A，对方连锁2发动B` |
| **state / condition description** | `，` | `我方手卡7张，我方场上存在「`卡名`_」，对方场上存在…` |
| **action sequence in one effect** | `，` | `发动「`卡名`_」的效果，解放自身并以…为对象` |

Hard rules:

- **A `、` must never join two predicates.** If either side can stand alone as a clause (has its own subject/predicate), use `，`.
- **Right side starts with a clause connector / time adverb** → that `、` is a clause boundary, use `，`. Trigger words: `之后`、`然后`、`那之后`、`此后`、`随后`、`因此`、`因而`、`所以`、`并且`、`而且`、`但是`、`不过`、`同时`、`这时`、`此时`、`这次`、`另外`、`此外`、`再`、`也`、`才`、`就`、`并`、`而`、`同样`、`那个回合`、`这个回合`.
  (Right side starting with `「` / `『` / `①②③④⑤` is a normal list — keep `、`.)
- Long **descriptive** items (`…的效果`, `…的怪兽`) may keep `、` while they remain noun phrases; once an item contains a finite predicate, switch to `，`.
- **Stacked pre-noun modifiers on ONE head noun use `，`, not `、`.** When two modifier phrases both attach to the same head noun (pattern: `A的、B的 + 核心名词` or `因…效果特殊召唤、作为…使用的 + 卡名`), separate them with `，` — the `、` would wrongly read as two separate entities. Examples (fixed 2026-10-05): `因「归光之旅-『塞尼特』」的效果特殊召唤，作为通常怪兽卡使用的「三眼小巫师」`；`变成魔法师族的，原本种族是植物族的怪兽`；`以因自身效果特殊召唤，适用『从场上离开的场合回到卡组最下面』的「亡龙之战栗-死欲龙」为对象`. Quoted card text `『…』` inside such modifiers does not change the ruling. Topic-page copies (e.g. `docs/c03/特定效果的处理方法.rst`) must be fixed in sync.
- Do **not** put `、` directly before `或` / `或者` when the joined parts are clauses or long phrases.

Real defects found in `docs/c06/2026.rst` (2026-10-05) and how they were fixed:

| bad | good |
|---|---|
| `从表侧表示变成里侧守备表示、之后又变回表侧表示` | `从表侧表示变成里侧守备表示，之后又变回表侧表示` |
| `…的效果一时除外、那个回合中以表侧表示回到怪兽区` | `…的效果一时除外，那个回合中以表侧表示回到怪兽区` |

Do **not** "fix" these — they are correct `、`:

- `「`卡名A`_」、「`卡名B`_」` (card-name list)
- `「`卡名A`_」①、「`卡名B`_」②` (card name + effect marker)
- `L召唤、X召唤或S召唤`、`A·P怪兽、B·P怪兽` (short parallel terms)
- `把魔法·陷阱卡盖放的效果、把怪兽里侧表示特殊召唤的效果、…的效果` (long but still noun phrases)

### Self-check (run after every edit)

High-precision detector — flags every `、` whose right side is a clause connector:

```python
# python -X utf8 check_dunhao.py   (writes nothing, only reports)
import glob, io, os, re
ROOT = r'D:\codes\OCG-Rule-documentation'
RIGHT = ('之后', '然后', '那之后', '此后', '随后', '因此', '因而', '所以',
         '并且', '而且', '但是', '不过', '同时', '这时', '此时', '这次',
         '另外', '此外', '再', '也', '才', '就', '并', '而', '同样',
         '那个回合', '这个回合')
hits = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'docs', '**', '*.rst'), recursive=True)):
    if f.endswith('links.rst'):
        continue
    for i, ln in enumerate(io.open(f, encoding='utf-8', newline='').read().split('\n')):
        if '、' not in ln or ln.lstrip().startswith('.. _'):
            continue
        for m in re.finditer(r'、(?=[^「『①②③④⑤])', ln):
            if ln[m.end():m.end() + 12].startswith(RIGHT):
                hits += 1
                print('%s L%d %s' % (os.path.relpath(f, ROOT), i + 1,
                                     ln[max(0, m.start() - 20):m.end() + 20]))
print('total suspicious 、:', hits)
```

A second, recall-oriented pass (both sides contain a verb) is useful when auditing an older file — expect many false positives from legitimate noun lists, so review by hand:

```python
VERB = re.compile(r'(发动|召唤|特殊召唤|变成|回到|除外|送去|加入|破坏|适用|进行|选择|处理|解放|丢弃|盖放|翻开|存在|成为|完成|结束|无效|受到|支付|确认|观看|使用|当作|得到|失去|放置|移动|离开|攻击|宣言|作为)')
# for each '、':  segL = ln[:k].split first by [，。；|] last part ; segR likewise
# if len(segL)>=5 and len(segR)>=5 and VERB.search(segL) and VERB.search(segR)
#    and not segR.lstrip().startswith(('「','『','①②③④⑤'))  -> candidate
```

### Fix procedure

1. Replace **only the offending `、`**; never rewrite the surrounding sentence.
2. Use a **byte-level** replace so EOL is untouched:
   ```python
   raw = io.open(p, 'rb').read()
   raw = raw.replace('……、……'.encode('utf-8'), '……，……'.encode('utf-8'))
   io.open(p, 'wb').write(raw)
   ```
   `docs/**/*.rst` is CRLF, but `docs/c03/里侧·一时除外.rst` is **LF-only** — byte-level replace is safe for both.
3. The same ruling is often duplicated between the yearly file (`docs/c06/*.rst`) and a topic page (`docs/c02/`, `docs/c03/`). After fixing one, grep the fixed phrase across `docs/**` and fix the copy too (2026-10-05: `2026.rst:1476` ↔ `c03/里侧·一时除外.rst:155`).
4. Re-run the self-check and confirm `total suspicious 、: 0`.

## RST entry format

Each FAQ entry in `docs/c06/*.rst` must follow these formatting rules:

- Each ruling is a standalone `| ` line. No Q&A structure (no `Q.` / `A.`).
- Never use question marks or interrogative phrasing (e.g. `可以...吗？`) inside a ruling line. Answers must be stated declaratively (e.g. `不能连锁发动` instead of `可以连锁发动吗？都不能发动。`).
- When the Japanese source has `(A)`/`(B)`/`(C)` sub-questions, translate them together in a single `| ` line, separating each case with `；` (e.g. `（A）的情况...；这种情况...`). Do not split them into separate `| ` lines and do not repeat the whole question; just state each scenario and its ruling declaratively.
- When listing multiple card names in a ruling, separate them with `、` (e.g. `「`卡名A`_」、「`卡名B`_」④、「`卡名C`_」③`).
- Multiple entries under the same source label (e.g. `| 数据库：`) are separate `| ` lines. Each line is self-contained.
- New card names referenced via `「\`卡名\`_」` must have a matching entry in `docs/links.rst` for the RST reference to resolve. Add it alphabetically using the format ``.. _`卡名`: https://ygocdb.com/card/name/卡名``.

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
- Non-ruling customer-service answers are condensed to `调整中` wording.
- Quoted `『』` effect text is based on the matching card's Chinese `text.desc` / `text.pdesc` from the external `cards.json`.
- Nested quoted effect text does not contain inappropriate card markup.
- Each entry is a standalone `| ` line with no Q&A structure or sub-question labels.
- `(A)`/`(B)`/`(C)` multi-case QAs are combined into a single `| ` line separated by `；`, not split into separate lines.
- No question marks or interrogative phrasing in ruling lines.
- `该` is not used in ruling prose; referent pronouns use `这个/这次/这只/这张` or `那个/那次/那只/那张` matching the referent.
- 同调/超量/连接 outside card names and `『』` effect text uses `S`/`X`/`L` shorthand.
- Multiple card names listed in a ruling are separated by `、`.
- `、`(顿号) appears only between short coordinate words/phrases (card-name lists, short parallel terms); clause/predicate boundaries, action sequences, chained chain links and state descriptions use `，`(逗号), never `、`. Run the self-check in `## Punctuation: 、 vs ，` and confirm `total suspicious 、: 0`.
- No `、` joins two predicates, and no `、` is immediately followed by a clause connector (`之后/然后/因此/此时/再/也/就/并/而/同样/那个回合/…`).
- New card names referenced via `「\`卡名\`_」` have matching entries in `docs/links.rst`.
