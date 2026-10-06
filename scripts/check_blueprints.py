#!/usr/bin/env python3
"""Validate blueprint YAML and the import badge links that point at it.

Checks:
  1. Every .yaml/.yml file parses. Home Assistant tags (!input, !secret, ...)
     are accepted. Files with a top-level `blueprint:` key must define
     `name` and `domain`.
  2. Every blueprint import link in a Markdown file points at a file that
     exists in this repo (case-sensitive, as raw.githubusercontent.com is).
  3. Every blueprint is linked from the root README and from the README in
     its own folder.

Exits non-zero and prints one line per problem if anything fails.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = "savantrials/Home_Assistant_Blueprints"
BRANCH = "main"

# Matches the blueprint_url in a my.home-assistant.io import link, e.g.
# ...?blueprint_url=https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/main/<path>
IMPORT_URL = re.compile(
    r"blueprint_import/?\?blueprint_url=(?P<url>[^)\s\"'>]+)", re.IGNORECASE
)
RAW_URL = re.compile(
    r"https://raw\.githubusercontent\.com/(?P<repo>[^/]+/[^/]+)/"
    r"(?:refs/heads/)?(?P<branch>[^/]+)/(?P<path>.+)"
)
GITHUB_BLOB_URL = re.compile(
    r"https://github\.com/(?P<repo>[^/]+/[^/]+)/blob/(?P<branch>[^/]+)/(?P<path>.+)"
)


class HALoader(yaml.SafeLoader):
    """SafeLoader that tolerates Home Assistant's custom YAML tags."""


HALoader.add_multi_constructor("!", lambda loader, suffix, node: None)


def tracked_files(pattern):
    return sorted(
        p for p in ROOT.rglob(pattern) if ".git" not in p.relative_to(ROOT).parts
    )


def check_yaml(errors):
    """Parse every YAML file; return the repo-relative paths of blueprints."""
    blueprints = []
    for path in tracked_files("*.y*ml"):
        if path.suffix not in (".yaml", ".yml"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".github/"):
            # Workflow files are not blueprints, but still must parse.
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as err:
                errors.append(f"{rel}: invalid YAML: {err}")
            continue
        try:
            data = yaml.load(path.read_text(encoding="utf-8"), Loader=HALoader)
        except yaml.YAMLError as err:
            errors.append(f"{rel}: invalid YAML: {err}")
            continue
        if not isinstance(data, dict) or "blueprint" not in data:
            continue
        meta = data["blueprint"]
        if not isinstance(meta, dict):
            errors.append(f"{rel}: `blueprint:` must be a mapping")
            continue
        for key in ("name", "domain"):
            if not meta.get(key):
                errors.append(f"{rel}: blueprint is missing `{key}`")
        blueprints.append(rel)
    return blueprints


def resolve_link(url):
    """Map an import URL to a repo-relative path, or return an error string."""
    url = unquote(url)
    match = RAW_URL.match(url) or GITHUB_BLOB_URL.match(url)
    if not match:
        return None, f"not a GitHub file URL: {url}"
    if match["repo"].lower() != REPO.lower():
        return None, f"points at another repo ({match['repo']}): {url}"
    if match["branch"] != BRANCH:
        return None, f"points at branch '{match['branch']}', expected '{BRANCH}'"
    return match["path"], None


def exists_case_sensitive(rel):
    """True if rel exists with exactly this casing (safe on macOS too)."""
    current = ROOT
    for part in rel.split("/"):
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current = current / part
    return current.is_file()


def check_badges(blueprints, errors):
    linked_from = {}  # blueprint path -> set of README paths linking to it
    for md in tracked_files("*.md"):
        md_rel = md.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for m in IMPORT_URL.finditer(line):
                target, problem = resolve_link(m["url"])
                where = f"{md_rel}:{lineno}"
                if problem:
                    errors.append(f"{where}: import badge {problem}")
                    continue
                if not exists_case_sensitive(target):
                    errors.append(
                        f"{where}: import badge points to missing file '{target}'"
                    )
                    continue
                if target not in blueprints:
                    errors.append(
                        f"{where}: import badge points to '{target}', "
                        "which is not a blueprint"
                    )
                    continue
                linked_from.setdefault(target, set()).add(md_rel)

    for bp in blueprints:
        folder_readme = f"{Path(bp).parent.as_posix()}/README.md"
        for readme in ("README.md", folder_readme):
            if readme not in linked_from.get(bp, set()):
                errors.append(f"{bp}: no import badge for it in {readme}")


def main():
    errors = []
    blueprints = check_yaml(errors)
    check_badges(blueprints, errors)
    if errors:
        for err in errors:
            print(f"::error::{err}" if "--github" in sys.argv else err)
        print(f"\n{len(errors)} problem(s) found.", file=sys.stderr)
        return 1
    print(f"OK: {len(blueprints)} blueprints, all YAML valid, all badges resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
