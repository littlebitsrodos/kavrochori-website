# Kavrochori Property Website

Static FSBO (for-sale-by-owner) landing page for a residential property in Καβροχώρι, Γάζι, Ηράκλειο. Single `index.html` file with inline CSS and vanilla JS. No build step, no backend, no dependencies.

Deployed as a static site at kavrochori.gr (GitHub Pages via CNAME).

## Deliberate non-features

This is a single-property landing page with low change frequency and no commercial
processing. The following are intentionally absent — do **not** propose adding them
without a clear new reason:

- **Analytics / tracking pixels.** No GA, no GTM, no Plausible. Privacy + simplicity
  + avoids needing a cookie banner. Owner does not need traffic stats.
- **Cookie banner.** Direct consequence of "no analytics" — there are no consent-
  required cookies to disclose.
- **Service Worker / PWA / `manifest.json`.** One static page; offline value is zero.
  Adds cache-invalidation footguns in exchange for nothing.
- **Booking flow / calendar / payment integration.** This is a sale, not a rental.
  Conversion is "buyer emails owner."
- **AI chat widget.** Vendor-skewed selection bias on serious property inquiries;
  buyers want a human at this price point.
- **`Review` JSON-LD on first-party content.** Google's 2019 self-serving-review
  rule disallows it. The existing `RealEstateListing` schema is the right type.
- **Test suite, CI, Lighthouse-CI, error tracking.** Single page, ~weekly edits,
  visual regression noticed on next visit. Premature for the scope.
- **`llms.txt`.** Bot logs show ~zero fetches; low signal.
- **Multiple HTML pages.** `/privacy.html` and `/404.html` are the only exceptions.
  Anything new should fit on the index or be argued for explicitly.

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
