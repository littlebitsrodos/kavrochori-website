#!/usr/bin/env python3
"""
sync_i18n.py — regenerate en/, de/, nl/, he/, fr/ from master index.html.

Run this after editing the master index.html (Greek default) to keep
the language variants in sync. Each variant is a near-identical copy
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

import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(ROOT, "index.html")
SITEMAP = os.path.join(ROOT, "sitemap.xml")

VARIANTS = {
    "en": {
        "locale": "en_US",
        "title": "Maisonette with self-contained garden apartment — Kavrochori, Heraklion, Crete",
        "description": "Independent 262 sqm home on a 617 sqm plot west of Heraklion. 7 minutes from the University Hospital (PAGNI), FORTH, and the University of Crete. Ideal for doctors, researchers, and academics.",
        "og_title": "Maisonette — Kavrochori, Heraklion, Crete",
        "og_description": "Independent home with a self-contained garden-level apartment. 617 sqm plot, wood-fired oven, mountain views.",
        "og_image_alt": "Maisonette with garden in Kavrochori, Heraklion, Crete",
    },
    "de": {
        "locale": "de_DE",
        "title": "Freistehendes Haus mit eigenständiger Gartenwohnung — Kavrochori, Heraklion, Kreta",
        "description": "Freistehendes Wohnhaus, 262 m² auf 617 m² Grundstück westlich von Heraklion. 7 Minuten vom Universitätsklinikum, FORTH und der Universität Kreta. Ideal für Ärzte, Forscher und Akademiker.",
        "og_title": "Freistehendes Haus — Kavrochori, Heraklion, Kreta",
        "og_description": "Freistehendes Haus mit eigenständiger Gartenwohnung im Souterrain. 617 m² Grundstück, Holzofen, Bergblick.",
        "og_image_alt": "Freistehendes Haus mit Garten in Kavrochori, Heraklion, Kreta",
    },
    "nl": {
        "locale": "nl_NL",
        "title": "Vrijstaand huis met zelfstandig tuinappartement — Kavrochori, Heraklion, Kreta",
        "description": "Vrijstaand huis, 262 m² op 617 m² perceel ten westen van Heraklion. 7 minuten van het Universiteitsziekenhuis (PAGNI), FORTH en de Universiteit van Kreta. Ideaal voor artsen, onderzoekers en academici.",
        "og_title": "Vrijstaand huis — Kavrochori, Heraklion, Kreta",
        "og_description": "Vrijstaande woning met een zelfstandig tuinappartement op het souterrain. 617 m² perceel, houtgestookte oven, bergzicht.",
        "og_image_alt": "Vrijstaand huis met tuin in Kavrochori, Heraklion, Kreta",
    },
    "he": {
        "locale": "he_IL",
        # Note: Hebrew uses גרש (geresh) / quotation for abbreviations (e.g. מ״ר = sqm).
        # We use the proper Unicode geresh ״ (U+05F4) instead of ASCII " to avoid
        # needing to escape within HTML attribute content="...".
        "title": "בית פרטי עם דירת גן עצמאית — קאברוכורי, הרקליון, כרתים",
        "description": "בית עצמאי בשטח 262 מ״ר על מגרש של 617 מ״ר ממערב להרקליון. שבע דקות מבית החולים האוניברסיטאי (PAGNI), ממכון המחקר FORTH ומאוניברסיטת כרתים. מתאים לרופאים, חוקרים ואנשי אקדמיה.",
        "og_title": "בית פרטי — קאברוכורי, הרקליון, כרתים",
        "og_description": "בית עצמאי עם דירת גן נפרדת במפלס התחתון. מגרש 617 מ״ר, טאבון עצים, נוף להרים.",
        "og_image_alt": "בית פרטי עם גן בקאברוכורי, הרקליון, כרתים",
    },
    "fr": {
        "locale": "fr_FR",
        "title": "Maison indépendante avec appartement de jardin autonome — Kavrochori, Héraklion, Crète",
        "description": "Maison indépendante de 262 m² sur un terrain de 617 m² à l'ouest d'Héraklion. À 7 minutes du CHU (PAGNI), de FORTH et de l'Université de Crète. Idéale pour médecins, chercheurs et universitaires.",
        "og_title": "Maison indépendante — Kavrochori, Héraklion, Crète",
        "og_description": "Maison individuelle avec appartement de jardin autonome au niveau inférieur. Terrain de 617 m², four à bois, vue sur les montagnes.",
        "og_image_alt": "Maison avec jardin à Kavrochori, Héraklion, Crète",
    },
}


def normalize_asset_paths(html: str) -> str:
    """Convert relative 'images/...' refs to root-absolute '/images/...'.

    Covers every context that references images/ in the markup:
      - attrs: src=, href=, data-full=, data-thumb=, srcset= (first value)
      - srcset continuations (comma-separated values)
      - inline CSS `url(images/...)` / `url('images/...')` / `url("images/...")`

    Idempotent: regexes require the 'images/' to have NO leading slash,
    so re-running after normalization is a no-op.
    """
    # 1. Simple attributes
    html = re.sub(
        r'((?:src|href|data-full|data-thumb|srcset)=")images/',
        r"\1/images/",
        html,
    )
    # 2. srcset comma-separated continuations: `, images/...` or `,images/...`
    html = re.sub(r"(,\s*)images/", r"\1/images/", html)
    # 3. CSS url() — optional quote around the URL
    html = re.sub(r"(url\(['\"]?)images/", r"\1/images/", html)
    return html


def _swap_meta(html: str, attr: str, value: str, new_content: str) -> str:
    """Replace the `content="..."` of a <meta attr="value">. Regex-safe."""
    pattern = (
        rf'(<meta\s+{attr}="{re.escape(value)}"\s+content=")[^"]*(")'
    )
    return re.sub(pattern, lambda m: f"{m.group(1)}{new_content}{m.group(2)}", html)


def generate_variant(master_html: str, lang: str, cfg: dict) -> str:
    html = master_html
    locale = cfg["locale"]

    # 1. <html lang="el"> -> <html lang="XX"> (RTL for Hebrew)
    if lang == "he":
        html = html.replace('<html lang="el">', '<html lang="he" dir="rtl">', 1)
    else:
        html = html.replace('<html lang="el">', f'<html lang="{lang}">', 1)
    # 2. <body> -> <body class="XX">
    html = html.replace("<body>", f'<body class="{lang}">', 1)
    # 3. canonical + og:url
    html = html.replace(
        '<link rel="canonical" href="https://kavrochori.gr/">',
        f'<link rel="canonical" href="https://kavrochori.gr/{lang}/">',
    )
    html = html.replace(
        '<meta property="og:url" content="https://kavrochori.gr/">',
        f'<meta property="og:url" content="https://kavrochori.gr/{lang}/">',
    )
    # 4. og:locale (swap primary; alternates list stays)
    html = html.replace(
        '<meta property="og:locale" content="el_GR">',
        f'<meta property="og:locale" content="{locale}">',
    )
    # 5. Localize <title> — only the first occurrence (head title).
    html = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{cfg['title']}</title>",
        html,
        count=1,
    )
    # 6. Localize meta description / og:title / og:description / twitter:*
    html = _swap_meta(html, 'name',     'description',         cfg["description"])
    html = _swap_meta(html, 'property', 'og:title',            cfg["og_title"])
    html = _swap_meta(html, 'property', 'og:description',      cfg["og_description"])
    html = _swap_meta(html, 'property', 'og:image:alt',        cfg["og_image_alt"])
    html = _swap_meta(html, 'name',     'twitter:title',       cfg["og_title"])
    html = _swap_meta(html, 'name',     'twitter:description', cfg["og_description"])
    # 7. Move `class="active"` from ΕΛ button to the target-lang button.
    html = html.replace(
        "<button class=\"active\" onclick=\"setLang('el', event)\">",
        "<button onclick=\"setLang('el', event)\">",
    )
    html = html.replace(
        f"<button onclick=\"setLang('{lang}', event)\">",
        f"<button class=\"active\" onclick=\"setLang('{lang}', event)\">",
    )
    return html


def bump_sitemap_lastmod() -> None:
    if not os.path.isfile(SITEMAP):
        return
    today = datetime.date.today().isoformat()
    with open(SITEMAP, encoding="utf-8") as f:
        xml = f.read()
    new_xml = re.sub(
        r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
        f"<lastmod>{today}</lastmod>",
        xml,
    )
    if new_xml != xml:
        with open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(new_xml)
        print(f"Bumped <lastmod> to {today} in {SITEMAP}")


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
        variant = generate_variant(master, lang, cfg)
        outpath = os.path.join(outdir, "index.html")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(variant)
        print(f"Wrote {outpath}")

    bump_sitemap_lastmod()
    return 0


if __name__ == "__main__":
    sys.exit(main())
