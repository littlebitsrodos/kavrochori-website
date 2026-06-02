# Kavrochori Property Website

Static FSBO (for-sale-by-owner) property site for a residential house in Καβροχώρι, Γάζι, Ηράκλειο.

Live site: `https://kavrochori.gr` via GitHub Pages / `CNAME`.

## Project shape

- No build step, backend, package manager, database, or runtime dependencies.
- Main public page: `index.html` in Greek (`el`).
- Generated language variants: `en/`, `de/`, `nl/`, `he/`, `fr/`.
- Supporting static pages: `privacy.html`, `404.html`, `brochure.html`, `agency-pack.html`.
- SEO/static files: `sitemap.xml`, `robots.txt`, `CNAME`, Google verification file.
- Images live under `images/` and `images/thumbs/`.
- Strategy/ops docs: `strategy.md`, `TODO.md`, `controlled-exposure-pack.md`, `lead-feedback-tracker.md`, `lead-feedback-template.csv`.

## Current business context

The property is in pre-public readiness / controlled exposure mode:

- Price target in strategy: **€610,000**.
- Primary reliable inquiry path: `visitor -> home@kavrochori.gr -> personal email`.
- FormSubmit/form paths are secondary until proven reliable.
- Real lead data must stay private and outside this public repo.
- Do not infer market feedback from zero traffic before real external distribution.
- Do not recommend price changes without actual buyer signals.

## Deliberate non-features

This is a single-property landing site with low change frequency and no commercial processing. These are intentionally absent; do **not** propose or add them without a clear new reason:

- **Analytics / tracking pixels**: no GA, GTM, Plausible, Meta pixel, etc.
- **Cookie banner**: no consent-required cookies are intentionally used.
- **Service Worker / PWA / `manifest.json`**: offline value is near zero and cache invalidation risk is not worth it.
- **Booking/payment flow**: this is a property sale, not a rental.
- **AI chat widget**: serious buyers should reach a human directly.
- **Self-serving `Review` JSON-LD**: avoid Google policy issues; use appropriate real-estate schema instead.
- **Backend, CI, test suite, Lighthouse-CI, error tracking**: premature for this static scope.
- **`llms.txt`**: previously judged low signal for this project.
- **Extra public pages** beyond the existing static pages unless explicitly justified.

## Agent workflow

Default to read-only inspection unless the user explicitly asks for edits.

Before editing:

1. Check `git status --short` and avoid mixing unrelated changes.
2. Read the relevant file/range first.
3. Preserve the static, no-build nature of the site.
4. Keep the site privacy-first: no analytics, tracking, cookies, or third-party widgets unless explicitly approved.
5. Do not deploy, push, change remotes, or alter GitHub Pages settings without explicit approval.

When editing:

- Keep changes minimal and localized.
- If public content/SEO changes affect the main page, preserve all language variants.
- Edit `index.html` first for shared page structure/content, then run:

  ```bash
  python3 sync_i18n.py
  ```

  This regenerates `en/`, `de/`, `nl/`, `he/`, `fr/` and updates `sitemap.xml` lastmod values.
- Be careful with Hebrew: keep `dir="rtl"` and avoid breaking quoted Hebrew metadata.
- Keep image references compatible with subdirectory language pages; `sync_i18n.py` normalizes `images/...` to `/images/...`.
- Never commit real names, emails, phone numbers, or lead notes from private inquiries.

## Validation

For HTML/SEO/content changes, run the smallest relevant checks before reporting done:

```bash
python3 sync_i18n.py
python3 - <<'PY'
from pathlib import Path
for p in [Path('index.html'), *Path('.').glob('*/index.html'), Path('brochure.html'), Path('agency-pack.html'), Path('privacy.html'), Path('404.html')]:
    if p.exists():
        p.read_text(encoding='utf-8')
print('ok: utf-8 readable html')
PY
git diff --stat
git diff --check
```

If JSON-LD is touched, additionally inspect/parse the changed `<script type="application/ld+json">` blocks.

## Source of truth / Git policy

- GitHub is the single point of truth for the project: `https://github.com/littlebitsrodos/kavrochori-website`.
- Treat `origin/main` as canonical for the public site and project docs.
- Local working copies, Discord notes, generated patches, and files under `/Users/Shared` are handoff/workspace artifacts until committed and merged/applied to GitHub.
- Before editing, compare local state with GitHub when relevant (`git fetch origin`, `git status --short`, `git log --oneline origin/main..HEAD`).
- Local commits are allowed only when requested or clearly part of an approved patch handoff.
- Do not push from this machine unless the user explicitly approves it.
- Preferred external handoff: create a patch under `/Users/hermes/sandbox/patches` and copy to `/Users/Shared` for external pickup.
- Do not access another user’s home directory.

## Communication

- Prefer concise Greek replies unless the user asks otherwise.
- State assumptions and risks explicitly.
- Summarize changed files, validation run, and whether anything remains uncommitted.
