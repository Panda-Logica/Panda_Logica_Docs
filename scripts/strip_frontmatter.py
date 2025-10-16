#!/usr/bin/env python3
import argparse
from pathlib import Path
import re

FRONTMATTER_PATTERN = re.compile(
    r"(?s)\A---\s*\n.*?\n---\s*\n"
)  # match YAML front matter block only at start

def clean_file(md_path: Path) -> bool:
    """Remove YAML front matter if present. Returns True if changed."""
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    new_text = FRONTMATTER_PATTERN.sub("", text, count=1)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Remove YAML front matter from Markdown files safely.")
    parser.add_argument(
        "root",
        help="Root folder to scan (e.g., snippets/mbi/V1.0.0.2)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root folder not found: {root}")

    md_files = list(root.rglob("*.md"))
    total = len(md_files)
    changed = 0

    for md in md_files:
        if clean_file(md):
            changed += 1
            print(f"Cleaned: {md.relative_to(root)}")

    print(f"\nProcessed {total} Markdown files.")
    print(f"Removed front matter from {changed} files.")

if __name__ == "__main__":
    main()
