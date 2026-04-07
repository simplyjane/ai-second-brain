#!/usr/bin/env python3
"""
Index daily logs and wiki articles into SQLite FTS5 for full-text search.
No external dependencies — uses Python stdlib only.

Usage:
    python3 index_logs.py                    # Index everything
    python3 index_logs.py --logs-only        # Only index daily logs
    python3 index_logs.py --wiki-only        # Only index wiki articles
"""

import sqlite3
import os
import sys
import glob
from datetime import datetime
from pathlib import Path

BRAIN_DIR = Path.home() / "Documents" / "JingAIJourney" / "ai-second-brain"
DB_PATH = BRAIN_DIR / "brain.db"
LOGS_DIR = BRAIN_DIR / "daily-logs"
WIKI_DIR = BRAIN_DIR / "knowledge" / "wiki"
MEMORY_DIR = BRAIN_DIR / "memory"


def init_db(conn):
    """Create FTS5 virtual tables if they don't exist."""
    conn.executescript("""
        CREATE VIRTUAL TABLE IF NOT EXISTS brain_search USING fts5(
            source,
            title,
            content,
            date,
            path,
            tokenize='porter unicode61'
        );

        CREATE TABLE IF NOT EXISTS indexed_files (
            path TEXT PRIMARY KEY,
            mtime REAL,
            indexed_at TEXT
        );
    """)


def file_needs_indexing(conn, filepath):
    """Check if a file has been modified since last indexing."""
    mtime = os.path.getmtime(filepath)
    row = conn.execute(
        "SELECT mtime FROM indexed_files WHERE path = ?",
        (str(filepath),)
    ).fetchone()

    if row is None:
        return True
    return mtime > row[0]


def extract_date_from_log(filename):
    """Extract date from daily log filename like '2026-04-07.md'."""
    stem = Path(filename).stem
    try:
        datetime.strptime(stem, "%Y-%m-%d")
        return stem
    except ValueError:
        return ""


def chunk_content(content, chunk_size=500, overlap=100):
    """Split content into overlapping chunks for better search results."""
    lines = content.split("\n")
    chunks = []
    current_chunk = []
    current_size = 0

    for line in lines:
        line_size = len(line.split())
        if current_size + line_size > chunk_size and current_chunk:
            chunks.append("\n".join(current_chunk))
            # Keep overlap lines
            overlap_lines = []
            overlap_size = 0
            for l in reversed(current_chunk):
                overlap_size += len(l.split())
                if overlap_size > overlap:
                    break
                overlap_lines.insert(0, l)
            current_chunk = overlap_lines
            current_size = overlap_size
        current_chunk.append(line)
        current_size += line_size

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def index_file(conn, filepath, source, title=None, date=""):
    """Index a single file into the FTS5 table."""
    filepath = str(filepath)

    if not file_needs_indexing(conn, filepath):
        return 0

    # Remove old entries for this file
    conn.execute("DELETE FROM brain_search WHERE path = ?", (filepath,))

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, FileNotFoundError):
        return 0

    if not content.strip():
        return 0

    # Extract title from first heading if not provided
    if not title:
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            title = Path(filepath).stem

    # Chunk and index
    chunks = chunk_content(content)
    count = 0
    for i, chunk in enumerate(chunks):
        chunk_title = f"{title} (part {i+1})" if len(chunks) > 1 else title
        conn.execute(
            "INSERT INTO brain_search (source, title, content, date, path) VALUES (?, ?, ?, ?, ?)",
            (source, chunk_title, chunk, date, filepath)
        )
        count += 1

    # Mark as indexed
    mtime = os.path.getmtime(filepath)
    conn.execute(
        "INSERT OR REPLACE INTO indexed_files (path, mtime, indexed_at) VALUES (?, ?, ?)",
        (filepath, mtime, datetime.now().isoformat())
    )

    return count


def index_daily_logs(conn):
    """Index all daily log files."""
    count = 0
    log_files = sorted(glob.glob(str(LOGS_DIR / "*.md")))

    for log_file in log_files:
        date = extract_date_from_log(log_file)
        title = f"Daily Log: {date}" if date else Path(log_file).stem
        indexed = index_file(conn, log_file, "daily-log", title, date)
        if indexed > 0:
            count += indexed
            print(f"  Indexed: {Path(log_file).name} ({indexed} chunks)")

    return count


def index_wiki(conn):
    """Index all wiki articles."""
    count = 0
    wiki_files = sorted(glob.glob(str(WIKI_DIR / "*.md")))

    for wiki_file in wiki_files:
        indexed = index_file(conn, wiki_file, "wiki")
        if indexed > 0:
            count += indexed
            print(f"  Indexed: {Path(wiki_file).name} ({indexed} chunks)")

    return count


def index_memory(conn):
    """Index memory files (user.md, memory.md — not soul.md which is static)."""
    count = 0
    for filename in ["user.md", "memory.md"]:
        filepath = MEMORY_DIR / filename
        if filepath.exists():
            indexed = index_file(conn, filepath, "memory", date=datetime.now().strftime("%Y-%m-%d"))
            if indexed > 0:
                count += indexed
                print(f"  Indexed: {filename} ({indexed} chunks)")

    return count


def get_stats(conn):
    """Print index statistics."""
    total = conn.execute("SELECT COUNT(*) FROM brain_search").fetchone()[0]
    by_source = conn.execute(
        "SELECT source, COUNT(*) FROM brain_search GROUP BY source ORDER BY COUNT(*) DESC"
    ).fetchall()
    files = conn.execute("SELECT COUNT(*) FROM indexed_files").fetchone()[0]

    print(f"\n--- Brain Index Stats ---")
    print(f"Total chunks: {total}")
    print(f"Files indexed: {files}")
    for source, count in by_source:
        print(f"  {source}: {count} chunks")


def main():
    logs_only = "--logs-only" in sys.argv
    wiki_only = "--wiki-only" in sys.argv

    print(f"Brain Indexer — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Database: {DB_PATH}\n")

    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    total = 0

    if not wiki_only:
        print("Indexing daily logs...")
        total += index_daily_logs(conn)

    if not logs_only:
        print("Indexing wiki articles...")
        total += index_wiki(conn)

    if not logs_only and not wiki_only:
        print("Indexing memory files...")
        total += index_memory(conn)

    conn.commit()

    if total == 0:
        print("Everything up to date — no new content to index.")
    else:
        print(f"\nIndexed {total} new chunks.")

    get_stats(conn)
    conn.close()


if __name__ == "__main__":
    main()
