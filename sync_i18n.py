#!/usr/bin/env python3
"""
sync_i18n.py — regenerate en/, de/, nl/ from master index.html.

Run this after editing the master index.html (Greek default) to keep
the 3 language variants in sync. Each variant is a near-identical copy
with:
  - <html lang="XX">
  - <body class="XX">
  - canonical + og:url pointing to /XX/
  - og:locale swapped for the target locale

Relative image paths in master are also converted to root-absolute
(e.g. images/foo.jpg -> /images/foo.jpg) so they resolve correctly from
any subdirectory.

Usage: python3 sync_i18n.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(ROOT, "index.html")

VARIANTS = {
    "en": {"locale": "en_US"},
    "de": {"locale": "de_DE"},
    "nl": {"locale": "nl_NL"},
}


def normalize_asset_paths(html: str) -> str:
    """Convert relative 'images/...' refs to root-absolute '/images/...'.

    Idempotent: skips matches already starting with '/images/' because the
    regex requires 'images/' preceded by '="' (no leading slash).
    """
    return re.sub(
        r'((?:src|href|data-full|data-thumb)=")images/',
        r"\1/images/",
        html,
    )


def generate_variant(master_html: str, lang: str, locale: str) -> str:
    html = master_html
    # 1. <html lang="el"> -> <html lang="XX">
    html = html.replace('<html lang="el">', f'<html lang="{lang}">', 1)
    # 2. <body> -> <body class="XX">
    html = html.replace("<body>", f'<body class="{lang}">', 1)
    # 3. canonical
    html = html.replace(
        '<link rel="canonical" href="https://kavrochori.gr/">',
        f'<link rel="canonical" href="https://kavrochori.gr/{lang}/">',
    )
    # 4. og:url
    html = html.replace(
        '<meta property="og:url" content="https://kavrochori.gr/">',
        f'<meta property="og:url" content="https://kavrochori.gr/{lang}/">',
    )
    # 5. og:locale (swap primary; leave alternates list alone)
    html = html.replace(
        '<meta property="og:locale" content="el_GR">',
        f'<meta property="og:locale" content="{locale}">',
    )
    # 6. Move `class="active"` from ΕΛ button to the target-lang button
    #    so the toggle UI reflects which variant the user is on.
    html = html.replace(
        "<button class=\"active\" onclick=\"setLang('el', event)\">",
        "<button onclick=\"setLang('el', event)\">",
    )
    html = html.replace(
        f"<button onclick=\"setLang('{lang}', event)\">",
        f"<button class=\"active\" onclick=\"setLang('{lang}', event)\">",
    )
    return html


def main() -> int:
    if not os.path.isfile(MASTER):
        print(f"ERROR: master not found at {MASTER}", file=sys.stderr)
        return 1

    with open(MASTER, encoding="utf-8") as f:
        master = f.read()

    # Mutate master: normalize image paths in-place, write back if changed.
    normalized = normalize_asset_paths(master)
    if normalized != master:
        with open(MASTER, "w", encoding="utf-8") as f:
            f.write(normalized)
        print(f"Normalized asset paths in {MASTER}")
        master = normalized

    for lang, cfg in VARIANTS.items():
        outdir = os.path.join(ROOT, lang)
        os.makedirs(outdir, exist_ok=True)
        variant = generate_variant(master, lang, cfg["locale"])
        outpath = os.path.join(outdir, "index.html")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(variant)
        print(f"Wrote {outpath}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
