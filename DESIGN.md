# Design System — Μεζονέτα Καβροχωρίου

**Aesthetic direction:** Estate Editorial  
**Target:** A buyer who reads Wallpaper*, not someone scrolling Spitogatos.  
The site should feel like a curated property feature, not a real estate portal listing.

---

## Typography

### Fonts

| Role | Family | Source |
|---|---|---|
| Display / headings | Cormorant Garamond | Google Fonts |
| Body / UI | DM Sans | Google Fonts (replace current Inter) |

**Why DM Sans over Inter:** Geometric but warm. Inter feels cold and techy; DM Sans keeps the editorial feel without softening the editorial edge. The contrast between Cormorant (serif, literary) and DM Sans (geometric sans) is the typographic identity.

### Scale

```
h1: clamp(2.2rem, 5vw, 3.8rem) — Cormorant, weight 500
h2: clamp(1.8rem, 3.5vw, 2.6rem) — Cormorant, weight 500
h3: 1.4rem — Cormorant, weight 500
body: 16px — DM Sans, weight 300
small / labels: 0.85rem — DM Sans
section-kicker: 0.85rem, uppercase, letter-spacing 0.15em — DM Sans
```

### Load order (Google Fonts URL)

```
Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600
```

**Action required:** Replace the `Inter` import in `index.html` line 12 with `DM+Sans`.  
Update `font-family` stack in `body` rule (line 28) to `'DM Sans'`.  
Update `.feature h4` font-family (line 191) to `'DM Sans'` (already `Inter`, will update automatically).

---

## Color Palette

### Tokens

```css
:root {
  /* Backgrounds */
  --bg:          #fafaf7;   /* warm off-white */
  --bg-alt:      #f2efe8;   /* section alternation */
  --card:        #ffffff;

  /* Text */
  --text:        #2a2a28;   /* near-black, warm */
  --text-muted:  #6b6b66;   /* secondary copy */

  /* Brand greens */
  --accent:      #5c6d4c;   /* sage — main accent, borders, kickers */
  --accent-dark: #3e4c32;   /* dark sage — headings, links, numbers */

  /* Terracotta — NEW in Variant B */
  --terracotta:  #b07d54;   /* warm accent for kickers, dividers, highlights */

  /* Structure */
  --border:      #d9d5c9;
  --shadow:      0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
}
```

### Usage rules

- **Sage (`--accent`, `--accent-dark`):** Primary brand color. Use for borders, nav links hover, distance numbers, section heading accents, bullet dashes (`::before`), bus badges.
- **Terracotta (`--terracotta`):** Secondary accent. Use for `.section-kicker` text, decorative horizontal rules between hero stats, `border-left` on highlighted callout cards where sage is overused.
- **Never mix terracotta and sage in the same component.** One accent per element.

### Where to apply terracotta first

1. `.section-kicker` — change `color: var(--accent)` → `color: var(--terracotta)` for visual differentiation from body links
2. `.audience-card .distance` — the large number at top of proximity cards (currently `--accent-dark`)
3. `.key-facts .num` — the hero stat numbers (currently `--accent-dark`)
4. Optional: thin `border-top: 2px solid var(--terracotta)` on `.feature` cards in the documentation section

---

## Spacing

8px base grid. All spacing values are multiples of 8.

```
4px  — tight internal (badge padding, list item gap)
8px  — default gap
16px — component internal padding (small)
24px — card padding (tight)
32px — card padding (comfortable)
48px — between related sections
80px — section vertical padding (currently 5rem)
96px — large section breathing room
```

Current `section { padding: 5rem 0 }` = 80px. Keep.  
Container max-width 1200px with 1.5rem side padding. Keep.

---

## Motion

### Principle
Fade in on scroll. No bounces, no slides from side. Vertical reveal only (subtle).

### Pattern

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 300ms ease-out, transform 300ms ease-out;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### IntersectionObserver (JS)

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### Apply `.reveal` to
- Section `h2` elements
- `.audience-card` (stagger: `transition-delay: calc(var(--i, 0) * 80ms)`)
- `.space` cards
- `.feature` cards
- `.key-facts .grid` children

**Not** on nav, hero (above fold), or contact form inputs (would feel broken on interaction).

---

## Components

### Section kicker

```html
<span class="section-kicker" lang="el">Τεκμηρίωση</span>
```

```css
.section-kicker {
  font-size: 0.85rem;
  color: var(--terracotta);   /* CHANGED from --accent */
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin-bottom: 1rem;
  display: block;
  font-family: 'DM Sans', sans-serif;
}
```

### Feature card (documentation section)

```css
.feature {
  padding: 1.5rem;
  background: var(--card);
  border-radius: 8px;
  border: 1px solid var(--border);
  border-top: 2px solid var(--terracotta);  /* NEW: top accent */
}
.feature h4 {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  margin-bottom: 0.8rem;
  color: var(--accent-dark);
  font-weight: 500;
}
```

### Document list inside feature card

```html
<ul style="list-style:none; padding:0.6rem 0 0; margin:0;">
  <li style="font-size:0.82rem; color:var(--text-muted); padding:0.2rem 0 0.2rem 1.1rem; position:relative;">
    <span style="position:absolute;left:0;color:var(--accent);">—</span>
    Συμβόλαιο αγοράς (1995)
  </li>
</ul>
```

Inline styles — these lists are one-off, no new class needed.

### Nav

Keep as-is. Sticky, backdrop blur, sage hover. No changes needed.

### Hero

- Background image with dual gradient overlay (keep existing pattern)
- `h1`, subtitle in `#fff` with text-shadow (keep)
- `.hero-meta` strip: consider adding `border-top: 1px solid rgba(255,255,255,0.2)` and `padding-top: 1.5rem` for cleaner separation from subtitle

### Contact section

Background: `var(--accent-dark)` (#3e4c32). Keep.

**Specificity trap:** The global rule `section:nth-child(even)` has specificity (0,1,1). Use `section.contact-section` (not just `.contact-section`) to override it — same specificity, last-defined wins.  
Text: explicit `color: rgba(255,255,255,0.92)` — not `opacity` (avoid compounding).  
Form fields: `background: rgba(255,255,255,0.15)`, `border: 1px solid rgba(255,255,255,0.4)`.  
These are already fixed. Do not revert to opacity-based approach.

---

## Current vs Target State

| Area | Current (index.html) | Target |
|---|---|---|
| Body font | Inter | DM Sans |
| Section kickers | color: var(--accent) / rgba(255,255,255,0.88) | color: var(--terracotta) |
| Stat numbers | color: var(--accent-dark) | color: var(--terracotta) |
| Feature cards | plain border | border-top: 2px solid var(--terracotta) |
| Scroll animation | none | .reveal + IntersectionObserver |
| Contact section opacity | FIXED (rgba colors) | — |

---

## What This Site Is Not

- Not a Spitogatos listing — no price tag in the hero, no room count badges
- Not a real estate agent portfolio — no agent photo, no "call me" CTA dominating
- Not a generic landing page — no hero with centered text and two buttons

The buyer should feel they're reading an editorial feature about a property. The site earns the asking price aesthetically before they see the number.

---

## Files

```
kavrochori-website/
├── index.html       main file — all CSS and JS inline
├── images/          JPG/PNG property photos
└── DESIGN.md        this file
```

No build system. No framework. Single-file HTML. Keep it that way.  
Add DM Sans to the Google Fonts import URL. All other changes are CSS/JS within `<style>` and `<script>` in `index.html`.
