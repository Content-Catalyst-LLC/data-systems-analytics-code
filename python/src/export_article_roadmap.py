#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--output", default="outputs/article-roadmap.md")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = list(conn.execute("SELECT * FROM v_article_roadmap;"))
    conn.close()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        f.write("# Data Systems & Analytics Article Roadmap\n\n")
        f.write("| Priority | Status | Domain | Title | Slug |\n")
        f.write("|---:|---|---|---|---|\n")
        for row in rows:
            f.write(f"| {row['priority']} | {row['status']} | {row['domain_name']} | {row['title']} | {row['slug']} |\n")

    print(f"Exported {len(rows)} article records to {out}")


if __name__ == "__main__":
    main()
