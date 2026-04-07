# Find Gaps

Analyzes the knowledge base and identifies what's missing or underrepresented.

## When to use

- When Jing says "what am I missing", "find gaps", or "what should I learn next"
- After compiling a wiki to suggest what to research next

## Instructions

1. **Read** `knowledge/wiki/index.md` to see all current articles
2. **Scan** each article for topics that are mentioned but not deeply covered
3. **Check** for broken `[[wikilinks]]` — topics referenced but no article exists
4. **Identify**:
   - Topics mentioned by multiple articles but with no dedicated article
   - Areas where all sources agree (might be missing contrarian views)
   - Practical/applied topics that are missing (e.g., lots of theory, no how-to)
   - Recency gaps (wiki covers old info but not latest developments)
5. **Recommend** specific sources to fill the top 3-5 gaps

## Output Format

```
## Knowledge Gaps

### High Priority (referenced but not covered)
1. [Topic] — mentioned in [[article-a]], [[article-b]] but no dedicated article
2. [Topic] — [reason it matters]

### Medium Priority (shallow coverage)
1. [Topic] — covered briefly in [[article]] but deserves deeper treatment
2. [Topic] — only one source, needs more perspectives

### Suggested Sources to Add
- [Specific article/video/paper to find] — would fill [gap]
- [Specific expert to look up] — covers [underrepresented perspective]
```
