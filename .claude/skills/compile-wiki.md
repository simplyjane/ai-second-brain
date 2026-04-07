# Compile Wiki

Reads all raw source files in `knowledge/raw/` and builds a structured, interlinked wiki in `knowledge/wiki/`.

## When to use

- When Jing adds new sources to `knowledge/raw/` and says "compile" or "update wiki"
- When Jing says "build the wiki" or "process my sources"

## Instructions

1. **Scan** `knowledge/raw/` for all files (markdown, text, PDF, etc.)
2. **Read** every file completely
3. **Identify** the major concepts, themes, and topics across all sources
4. **For each concept**, write a standalone article in `knowledge/wiki/` that:
   - Summarizes what the evidence says across sources
   - Notes where sources agree
   - Flags where sources disagree and why
   - Links to related articles using `[[wikilinks]]`
   - Attributes key claims to their source
5. **Create or update** `knowledge/wiki/index.md` listing every article with a one-line description
6. **Report** what was created/updated and suggest gaps to fill

## Article Format

```markdown
# [Concept Name]

> Sources: [list of raw files that informed this article]

## Summary
[2-3 paragraph overview]

## Key Points
- [Point 1] — per [source]
- [Point 2] — per [source]

## Where Sources Disagree
- [Disagreement] — [Source A] says X, [Source B] says Y

## Related
- [[related-concept-1]]
- [[related-concept-2]]
```

## Rules

- Organize by CONCEPT, not by source or person
- Every article must link to at least one other article
- Keep articles focused — split large topics into sub-articles
- When updating an existing wiki, preserve existing articles and update/extend them
- Never delete existing wiki articles without explicit confirmation
- If a raw source doesn't clearly fit existing concepts, create a new article for it
- After compiling, run: `python3 scripts/caicai_engine.py xp wiki_compiled` to award Caicai XP
- After adding a new raw source, run: `python3 scripts/caicai_engine.py xp source_added` per source
