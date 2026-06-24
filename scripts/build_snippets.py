import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
from urllib.parse import quote, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "docs"
OUT_DIR = ROOT / "public" / "snippets"

DOCS_VERSION = os.environ.get("DOCS_VERSION", "V1.0.0.2")
GITHUB_ORG = os.environ.get("DOCS_GITHUB_ORG", "Panda-Logica")
GITHUB_REPO = os.environ.get("DOCS_GITHUB_REPO", "Panda_Logica_Docs")
GITHUB_BRANCH = os.environ.get("DOCS_GITHUB_BRANCH", "gh-pages")

# Top-level folders produced from docs/mbi/*.md (replaced on each build).
USER_DOC_SECTION_SLUGS = {
    "admin-guides",
    "getting-started",
    "user-guides",
    "advanced",
    "reference",
    "troubleshooting",
    "release-notes",
}

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def github_raw_base(docset: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{GITHUB_ORG}/{GITHUB_REPO}/"
        f"{GITHUB_BRANCH}/snippets/{docset}/{DOCS_VERSION}"
    )


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "-")
        .replace(")", "")
        .replace("(", "")
        .replace("/", "-")
        .replace(":", "")
        .replace("&", "and")
    )


def encode_asset_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in path.replace("\\", "/").split("/"))


def rewrite_image_urls(md_text: str, md_file: pathlib.Path, docset: str) -> str:
    """Rewrite relative image paths to absolute GitHub raw URLs."""

    docset_root = SRC_DIR / docset
    base = github_raw_base(docset)

    def replace_match(match: re.Match) -> str:
        alt = match.group(1)
        url = unquote(match.group(2).strip())
        if not url or url.startswith(("http://", "https://", "data:")):
            return match.group(0)

        resolved = (md_file.parent / url).resolve()
        try:
            rel_to_docset = resolved.relative_to(docset_root.resolve())
        except ValueError:
            return match.group(0)

        asset_url = f"{base}/{encode_asset_path(str(rel_to_docset))}"
        return f"![{alt}]({asset_url})"

    return IMAGE_RE.sub(replace_match, md_text)


def sectionize(md_text: str):
    """Split MD into (heading, body, heading_level) tuples for each ## or ### section."""
    parts = re.split(r"(^#{2,3} .*$)", md_text, flags=re.MULTILINE)
    for i in range(1, len(parts), 2):
        heading_line = parts[i].strip()
        body = parts[i] + parts[i + 1]
        heading_level = heading_line.count("#")
        heading = heading_line.strip("# ").strip()
        yield heading, body, heading_level


def copy_doc_assets(docset: str, version_out_dir: pathlib.Path) -> None:
    """Copy screenshots and other image assets into the published version folder."""

    docset_root = SRC_DIR / docset
    screenshots_src = docset_root / "screenshots"
    if screenshots_src.exists():
        shutil.copytree(
            screenshots_src,
            version_out_dir / "screenshots",
            dirs_exist_ok=True,
        )

    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
    for image_path in docset_root.rglob("*"):
        if not image_path.is_file() or image_path.suffix.lower() not in image_exts:
            continue
        if screenshots_src in image_path.parents or image_path.parent == screenshots_src:
            continue
        rel_path = image_path.relative_to(docset_root)
        target = version_out_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image_path, target)


def write_snippet(
    version_out_dir: pathlib.Path,
    md_file: pathlib.Path,
    docset: str,
    heading: str,
    body: str,
    heading_level: int,
    order: int,
    tree: dict,
) -> None:
    rel_path = md_file.relative_to(SRC_DIR / docset).with_suffix("")
    slug = slugify(heading)

    body = rewrite_image_urls(body, md_file, docset)

    outfile = version_out_dir / rel_path.parent / f"{rel_path.name}-{slug}.snippet.md"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(body.strip() + "\n", encoding="utf-8")

    sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    last_modified = datetime.datetime.utcfromtimestamp(md_file.stat().st_mtime).isoformat() + "Z"

    section = rel_path.parts[0] if rel_path.parts else "root"

    if section not in tree:
        tree[section] = {
            "title": section.replace("-", " ").title(),
            "slug": section,
            "children": [],
        }

    tree[section]["children"].append(
        {
            "title": heading,
            "slug": str(outfile.relative_to(version_out_dir)).replace("\\", "/"),
            "sha256": sha256,
            "order": order,
            "heading_level": heading_level,
            "last_modified": last_modified,
        }
    )


def build_docset(docset: str) -> None:
    version_out_dir = OUT_DIR / docset / DOCS_VERSION
    if version_out_dir.exists():
        shutil.rmtree(version_out_dir)
    version_out_dir.mkdir(parents=True, exist_ok=True)

    copy_doc_assets(docset, version_out_dir)

    tree = {}
    docset_src = SRC_DIR / docset
    for md_file in sorted(docset_src.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        order = 1
        for heading, body, heading_level in sectionize(text):
            write_snippet(
                version_out_dir,
                md_file,
                docset,
                heading,
                body,
                heading_level,
                order,
                tree,
            )
            order += 1

    manifest_file = version_out_dir / "manifest.json"
    manifest_list = list(tree.values())
    manifest_file.write_text(json.dumps(manifest_list, indent=2), encoding="utf-8")


def merge_with_prior_manifest(docset: str) -> None:
    """
    Keep InAppHelp (and other non-user-doc sections) from the deployed manifest
    while replacing user-facing guide sections with the freshly built tree.
    """

    prior_path = os.environ.get("PRIOR_MANIFEST_PATH")
    if not prior_path:
        return

    prior_file = pathlib.Path(prior_path)
    if not prior_file.is_file():
        return

    version_out_dir = OUT_DIR / docset / DOCS_VERSION
    manifest_file = version_out_dir / "manifest.json"
    if not manifest_file.is_file():
        return

    try:
        prior_manifest = json.loads(prior_file.read_text(encoding="utf-8"))
        new_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return

    if not isinstance(prior_manifest, list):
        return

    kept_sections = [
        section
        for section in prior_manifest
        if section.get("slug") not in USER_DOC_SECTION_SLUGS
    ]
    merged = kept_sections + new_manifest
    manifest_file.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        f"Merged manifest: kept {len(kept_sections)} existing sections, "
        f"added {len(new_manifest)} user-doc sections"
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index = []

    for docset_dir in sorted(SRC_DIR.iterdir()):
        if docset_dir.is_dir():
            build_docset(docset_dir.name)
            merge_with_prior_manifest(docset_dir.name)
            index.append(
                {
                    "title": docset_dir.name.replace("-", " ").title() + " Documentation",
                    "slug": docset_dir.name,
                    "manifest": f"snippets/{docset_dir.name}/{DOCS_VERSION}/manifest.json",
                }
            )

    index_file = OUT_DIR / "index.json"
    index_file.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Built docs for version {DOCS_VERSION} into {OUT_DIR}")


if __name__ == "__main__":
    main()
