#!/usr/bin/env python3
"""
Search across the entire brain — daily logs, wiki, and memory.
Uses SQLite FTS5 for fast full-text search with ranking.

Usage:
    python3 search_brain.py "query terms"
    python3 search_brain.py "query terms" --source daily-log
    python3 search_brain.py "query terms" --source wiki
    python3 search_brain.py "query terms" --limit 20
    python3 search_brain.py "query terms" --after 2026-04-01
    python3 search_brain.py "query terms" --json
"""

import sqlite3
import sys
import json
import argparse
from pathlib import Path

BRAIN_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BRAIN_DIR / "brain.db"


def search(query, source=None, limit=10, after=None, output_json=False):
    """Search the brain index and return ranked results."""
    if not DB_PATH.exists():
        print("Brain index not found. Run index_logs.py first.")
        sys.exit(1)

    conn = sqlite3.connect(str(DB_PATH))

    # Build FTS5 query — support phrase search with quotes
    # FTS5 supports AND, OR, NOT, phrases in quotes, prefix with *
    fts_query = query

    sql = """
        SELECT
            source,
            title,
            snippet(brain_search, 2, '>>>', '<<<', '...', 40) as snippet,
            date,
            path,
            rank
        FROM brain_search
        WHERE brain_search MATCH ?
    """
    params = [fts_query]

    if source:
        sql += " AND source = ?"
        params.append(source)

    if after:
        sql += " AND date >= ?"
        params.append(after)

    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    try:
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        # If FTS5 query syntax fails, try wrapping in quotes for literal search
        params[0] = f'"{query}"'
        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError:
            print(f"Search error: {e}")
            conn.close()
            sys.exit(1)

    conn.close()

    if output_json:
        results = []
        for source_type, title, snippet, date, path, rank in rows:
            results.append({
                "source": source_type,
                "title": title,
                "snippet": snippet,
                "date": date,
                "path": path,
                "relevance": round(-rank, 4)
            })
        print(json.dumps(results, indent=2))
        return results

    if not rows:
        print(f"No results for: {query}")
        return []

    print(f"Found {len(rows)} results for: {query}\n")

    for i, (source_type, title, snippet, date, path, rank) in enumerate(rows, 1):
        source_label = {
            "daily-log": "LOG",
            "wiki": "WIKI",
            "memory": "MEM"
        }.get(source_type, source_type.upper())

        date_str = f" ({date})" if date else ""
        snippet_clean = snippet.replace(">>>", "\033[1m").replace("<<<", "\033[0m")

        print(f"  [{source_label}]{date_str} {title}")
        print(f"    {snippet_clean}")
        print(f"    → {path}")
        print()

    return rows


def main():
    parser = argparse.ArgumentParser(description="Search your AI Second Brain")
    parser.add_argument("query", nargs="+", help="Search terms (supports FTS5 syntax: AND, OR, NOT, \"phrases\")")
    parser.add_argument("--source", choices=["daily-log", "wiki", "memory"], help="Filter by source type")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--after", help="Only results after this date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for piping to Claude)")

    args = parser.parse_args()
    query_str = " ".join(args.query)

    search(query_str, source=args.source, limit=args.limit, after=args.after, output_json=args.json)


if __name__ == "__main__":
    main()
