# Kavrochori Property Website

Static FSBO (for-sale-by-owner) property site for a residential house in Καβροχώρι, Γάζι, Ηράκλειο.

Live site: `https://kavrochori.gr` via GitHub Pages / `CNAME`.

## Project shape

- No build step, backend, package manager, database, or runtime dependencies.
- Main public page and source of shared structure/content: `index.html` in Greek (`el`).
- Generated language variants: `en/`, `de/`, `nl/`, `he/`, `fr/`.
- Supporting static pages: `privacy.html`, `404.html`, `brochure.html`, `agency-pack.html`.
- SEO/static files: `sitemap.xml`, `robots.txt`, `CNAME`, `google482fce562e91ba4b.html`, favicons, and `og-image.jpg`.
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
- Priority #1 is first controlled exposure, not generic polish; see `TODO.md` and `controlled-exposure-pack.md`.

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

## Source of truth / workspace policy

- GitHub is the single point of truth: `https://github.com/littlebitsrodos/kavrochori-website`.
- Treat `origin/main` as canonical for the public site and project docs.
- Before any edit, update the clean local source checkout from GitHub:

  ```bash
  cd /Users/hermes/projects/kavrochori-website
  git status --short --branch
  git pull --ff-only
  ```

  If that checkout is unavailable on this Mac, check `/Users/hermes/Projects/kavrochori-website` before declaring it missing.
- Do **not** work directly on `main`. Create a task branch/worktree under `/Users/hermes/workspaces/<task-name>` for edits, for example:

  ```bash
  git worktree add -b agent/<task-name> /Users/hermes/workspaces/<task-name> main
  ```

- If `git pull --ff-only` is blocked by local changes or divergence, stop and report the state before editing.
- Do not push, deploy, change remotes, or alter GitHub Pages settings without explicit approval.
- Do not access another user’s home directory.
- Do not use `/Users/Shared` unless the user explicitly asks for a handoff there. Preferred local scratch/patch output is under `/Users/hermes/sandbox/patches`.

## Agent workflow

Default to read-only inspection unless the user explicitly asks for edits.

Before editing:

1. Verify branch/worktree with `git status --short --branch`.
2. Read the relevant file/range first.
3. Preserve the static, no-build nature of the site.
4. Keep the site privacy-first: no analytics, tracking, cookies, or third-party widgets unless explicitly approved.
5. Keep real lead data, private names, phone numbers, emails, and inquiry notes out of this public repo.

When editing:

- Keep changes minimal and localized.
- If public content/SEO changes affect the main page, preserve all language variants.
- Edit `index.html` first for shared page structure/content, then run:

  ```bash
  python3 sync_i18n.py
  ```

  This regenerates `en/`, `de/`, `nl/`, `he/`, `fr/` and updates `sitemap.xml` lastmod values.
- Do not hand-edit generated language pages for shared content unless the task is specifically about variant-only metadata or language-specific markup.
- If metadata for language variants changes, update `sync_i18n.py` first, then run `python3 sync_i18n.py`.
- Be careful with Hebrew: keep `dir="rtl"` and avoid breaking quoted Hebrew metadata.
- Keep image references compatible with subdirectory language pages; `sync_i18n.py` normalizes `images/...` to `/images/...`.
- Price, area, room-count, contact, and JSON-LD changes must be checked across every public surface they affect.

## Validation

Use the smallest check set that proves the change.

For **AGENTS/docs-only changes**:

```bash
git diff --check
git diff --stat
```

For **HTML/SEO/content changes**:

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

If JSON-LD is touched, additionally parse every changed `<script type="application/ld+json">` block before reporting done:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import json

class LDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_ld = False
        self.blocks = []
        self.buf = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_ld = True
            self.buf = []
    def handle_data(self, data):
        if self.in_ld:
            self.buf.append(data)
    def handle_endtag(self, tag):
        if tag == 'script' and self.in_ld:
            self.blocks.append(''.join(self.buf))
            self.in_ld = False

for p in [Path('index.html'), *Path('.').glob('*/index.html'), Path('brochure.html'), Path('agency-pack.html')]:
    if not p.exists():
        continue
    parser = LDParser()
    parser.feed(p.read_text(encoding='utf-8'))
    for block in parser.blocks:
        json.loads(block)
print('ok: json-ld parses')
PY
```

For **privacy/contact changes**, also search the diff for accidental tracking/private-data leaks and verify `home@kavrochori.gr` / `mailto:` remains present where expected.

## Reporting

Final replies should be concise Greek and include:

- branch/worktree path,
- changed files,
- validation commands actually run,
- whether anything remains uncommitted,
- whether push/deploy/live verification was not done because it was not approved.
