# Sukum One-Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild Sukum as an accessible, responsive one-page brand and product site that presents Sukum 7, free resources, its creators, contact options, and legal drafts while remaining deployable on GitHub Pages.

**Architecture:** Keep the existing static architecture and progressively enhance it with one JavaScript file. The main page owns brand and product content; three standalone HTML documents own legal drafts; one standard-library Python test validates the site contract without introducing runtime dependencies.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python 3 `unittest`, GitHub Pages.

## Global Constraints

- Keep the site build-free and compatible with GitHub Pages.
- Do not expose the hidden meditation section or link the MP3 files.
- Do not copy code, text, imagery, or brand assets from The Wise Wellness.
- Do not publish images extracted from the DOCX requirements.
- Do not submit or store personal data before Brevo and reviewed legal text exist.
- Never place a Brevo API key in client-side code.
- Treat all legal documents as visible drafts requiring professional review.
- Use Cormorant Garamond for editorial headings and Montserrat for interface/body text.

---

### Task 1: Add an executable site contract

**Files:**
- Create: `tests/test_site.py`

**Interfaces:**
- Consumes: static files at the repository root.
- Produces: `python -m unittest tests.test_site -v`, the regression command used by every later task.

- [ ] **Step 1: Create the initial failing contract test**

```python
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.scripts = []
        self.forms = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values)
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"])
        if tag == "form":
            self.forms.append(values)
        if tag in {"h1", "h2", "h3"}:
            self.headings.append(tag)


def parse(name):
    parser = PageParser()
    parser.feed((ROOT / name).read_text(encoding="utf-8"))
    return parser


class SiteContractTests(unittest.TestCase):
    def test_main_page_has_required_sections(self):
        page = parse("index.html")
        self.assertTrue(
            {"inicio", "filosofia", "diario", "recursos", "nosotras", "contacto"}
            <= page.ids
        )

    def test_main_page_has_single_h1_and_site_script(self):
        page = parse("index.html")
        self.assertEqual(page.headings.count("h1"), 1)
        self.assertIn("scripts/site.js", page.scripts)

    def test_amazon_and_legal_links_exist(self):
        page = parse("index.html")
        hrefs = {link.get("href") for link in page.links}
        self.assertIn("https://www.amazon.es/dp/B0HQ4X8MDZ", hrefs)
        self.assertTrue(
            {"aviso-legal.html", "privacidad.html", "cookies.html"} <= hrefs
        )

    def test_meditations_are_not_exposed(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8").lower()
        self.assertNotIn("<audio", source)
        self.assertNotIn('id="meditaciones"', source)
        self.assertNotIn(".mp3", source)

    def test_pending_forms_do_not_submit_data(self):
        page = parse("index.html")
        self.assertGreaterEqual(len(page.forms), 1)
        for form in page.forms:
            self.assertNotIn("action", form)

    def test_legal_pages_exist_and_are_marked_as_drafts(self):
        for name in ("aviso-legal.html", "privacidad.html", "cookies.html"):
            source = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("Borrador", source)
            self.assertIn('href="index.html', source)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the contract and confirm it fails against the old site**

Run: `python -m unittest tests.test_site -v`

Expected: failures for missing sections, script, legal pages, Amazon link, and exposed audio.

- [ ] **Step 3: Commit the test contract**

```powershell
git add tests/test_site.py
git commit -m "Añade el contrato de la nueva web de Sukum"
```

### Task 2: Rebuild the one-page content and semantic structure

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: section IDs asserted by `tests/test_site.py`.
- Produces: semantic sections and hooks consumed by `styles.css` and `scripts/site.js`.

- [ ] **Step 1: Replace the current page with the approved content structure**

The document must contain:

```html
<header class="site-header" data-header>
  <a class="brand" href="#inicio" aria-label="Sukum, ir al inicio">SUKUM</a>
  <button class="menu-toggle" type="button" aria-expanded="false"
          aria-controls="primary-navigation" data-menu-toggle>
    <span class="sr-only">Abrir menú</span>
    <span aria-hidden="true"></span><span aria-hidden="true"></span>
  </button>
  <nav id="primary-navigation" class="primary-navigation"
       aria-label="Navegación principal" data-navigation>
    <a href="#inicio">Sukum</a>
    <a href="#diario">El diario</a>
    <a href="#recursos">Recursos gratuitos</a>
    <a href="#nosotras">Nosotras</a>
    <a href="#contacto">Contacto</a>
  </nav>
</header>
```

Use the exact section IDs `inicio`, `filosofia`, `diario`, `recursos`, `nosotras`, and `contacto`. Include:

- One `h1`: «La vida cambia cuando empiezas a mirarla de otra manera».
- Both hero calls to `#diario` and `#recursos`.
- Full philosophy copy and three pillars from the design spec.
- The Amazon URL twice, with `target="_blank"` and `rel="noopener noreferrer"`.
- Four diary benefit blocks.
- Three resource cards with buttons using `data-resource-open`.
- One accessible dialog with `data-resource-dialog`, a close button, explanatory text, and no data collection.
- Two creator profiles with neutral provisional copy and `data-content="provisional"`.
- A newsletter form with no `action`, `data-brevo-pending`, and a privacy link.
- Footer links to the three legal pages.
- JSON-LD for `Organization` and `Product` without price, ratings, or stock claims.

- [ ] **Step 2: Run the contract**

Run: `python -m unittest tests.test_site -v`

Expected: legal-page test still fails; all main-page tests pass.

- [ ] **Step 3: Validate the HTML parser can read the complete file**

Run:

```powershell
python -c "from html.parser import HTMLParser; from pathlib import Path; p=HTMLParser(); p.feed(Path('index.html').read_text(encoding='utf-8')); print('HTML OK')"
```

Expected: `HTML OK`.

- [ ] **Step 4: Commit the semantic rebuild**

```powershell
git add index.html
git commit -m "Reconstruye el contenido one-page de Sukum"
```

### Task 3: Implement the Sukum visual system and responsive layout

**Files:**
- Modify: `styles.css`

**Interfaces:**
- Consumes: semantic classes and data attributes from `index.html`.
- Produces: desktop, tablet, mobile, focus, dialog, and reduced-motion presentation.

- [ ] **Step 1: Replace the old style sheet with the approved design tokens**

The root tokens must be:

```css
:root {
  --green: #5f938d;
  --green-dark: #315e58;
  --beige: #eae1d2;
  --ivory: #f8f5ef;
  --gold: #b79a62;
  --ink: #4a3d36;
  --muted: #756a62;
  --line: rgba(74, 61, 54, 0.18);
  --white: #fffdf9;
  --radius-sm: 0.75rem;
  --radius-lg: 2rem;
  --shadow: 0 1.5rem 4rem rgba(49, 94, 88, 0.12);
  --content: 76rem;
}
```

Implement:

- Sticky translucent header with active-link underline.
- Full-height split hero and a branded photo placeholder.
- Alternating ivory, beige, green, and white section backgrounds.
- Editorial Cormorant Garamond headings and Montserrat interface/body copy.
- Line-art SVG pillar treatment.
- Two-column diary feature with responsive photo placeholder.
- Four-benefit grid.
- Three-card resources grid.
- Two creator profiles.
- High-contrast newsletter panel.
- Shared legal-document layout.
- Modal dialog and backdrop styling.
- `:focus-visible`, `.sr-only`, and skip-link styles.
- Breakpoints at `64rem` and `48rem`.
- `@media (prefers-reduced-motion: reduce)`.

- [ ] **Step 2: Run the contract**

Run: `python -m unittest tests.test_site -v`

Expected: only the legal-page test fails.

- [ ] **Step 3: Confirm no removed color variables remain**

Run:

```powershell
rg -- "--paper|--paper-light|--paper-deep" styles.css
```

Expected: no matches.

- [ ] **Step 4: Commit the visual system**

```powershell
git add styles.css
git commit -m "Aplica la nueva identidad visual de Sukum"
```

### Task 4: Add progressive interactions

**Files:**
- Create: `scripts/site.js`

**Interfaces:**
- Consumes: `[data-menu-toggle]`, `[data-navigation]`, section IDs, `[data-resource-open]`, and `[data-resource-dialog]`.
- Produces: active navigation, accessible mobile menu, and accessible resource dialog.

- [ ] **Step 1: Implement the interaction module**

```javascript
const menuButton = document.querySelector("[data-menu-toggle]");
const navigation = document.querySelector("[data-navigation]");
const navLinks = [...document.querySelectorAll('.primary-navigation a[href^="#"]')];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const closeMenu = () => {
  menuButton?.setAttribute("aria-expanded", "false");
  navigation?.removeAttribute("data-open");
};

menuButton?.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!open));
  navigation?.toggleAttribute("data-open", !open);
});

navLinks.forEach((link) => link.addEventListener("click", closeMenu));

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      navLinks.forEach((link) => {
        const active = link.getAttribute("href") === `#${visible.target.id}`;
        if (active) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-35% 0px -55%", threshold: [0, 0.25, 0.5] }
  );
  sections.forEach((section) => observer.observe(section));
}

const dialog = document.querySelector("[data-resource-dialog]");
let dialogTrigger = null;

document.querySelectorAll("[data-resource-open]").forEach((button) => {
  button.addEventListener("click", () => {
    dialogTrigger = button;
    dialog?.showModal();
  });
});

dialog?.querySelector("[data-dialog-close]")?.addEventListener("click", () => {
  dialog.close();
});

dialog?.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

dialog?.addEventListener("close", () => dialogTrigger?.focus());

document.querySelector("[data-brevo-pending]")?.addEventListener("submit", (event) => {
  event.preventDefault();
  const status = event.currentTarget.querySelector("[data-form-status]");
  if (status) {
    status.textContent =
      "La suscripción estará disponible cuando conectemos Sukum con Brevo.";
  }
});
```

- [ ] **Step 2: Validate JavaScript syntax**

Run: `node --check scripts/site.js`

Expected: exit code 0 and no output.

- [ ] **Step 3: Run the site contract**

Run: `python -m unittest tests.test_site -v`

Expected: only the legal-page test fails.

- [ ] **Step 4: Commit interactions**

```powershell
git add scripts/site.js
git commit -m "Añade navegación e interacciones accesibles"
```

### Task 5: Add legal drafts and operational documentation

**Files:**
- Create: `aviso-legal.html`
- Create: `privacidad.html`
- Create: `cookies.html`
- Modify: `README.md`

**Interfaces:**
- Consumes: shared `styles.css`.
- Produces: complete footer destinations and exact operational guidance for replacing provisional content and connecting Brevo.

- [ ] **Step 1: Create the legal-page shell in each document**

Each page must include:

```html
<body class="legal-page">
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header class="legal-header">
    <a class="brand" href="index.html">SUKUM</a>
    <a href="index.html">Volver a la web</a>
  </header>
  <main id="contenido" class="legal-document">
    <p class="legal-status">Borrador orientativo · Requiere revisión profesional</p>
  </main>
</body>
```

The notice must explain that ownership, tax identifier, registered address, registry data, and validated contact address must be inserted before commercial launch.

The privacy draft must explain:

- No personal data is currently transmitted because Brevo is not connected.
- Future purposes: resource delivery and optional newsletter.
- Newsletter consent must be separate from resource delivery.
- Rights: access, rectification, erasure, objection, restriction, and portability.
- Data processor and international-transfer details must be completed from the future Brevo account.

The cookie draft must explain:

- No analytics or advertising cookies are installed in this version.
- Essential browser/GitHub Pages behavior does not require a consent banner.
- Adding analytics, embedded media, or marketing scripts requires prior policy and consent changes.

- [ ] **Step 2: Rewrite README operations**

Document:

- Local preview and GitHub Pages deployment.
- Exact section IDs.
- How to replace hero, diary, guide, and creator placeholders.
- How to replace provisional creator copy.
- How to create Brevo lists/forms, paste public integration endpoints, and keep API keys out of Git.
- The legal review gate before enabling forms.
- That meditation MP3s are retained but intentionally unlinked.

- [ ] **Step 3: Run the complete contract**

Run: `python -m unittest tests.test_site -v`

Expected: all tests pass.

- [ ] **Step 4: Run static syntax and content checks**

Run:

```powershell
node --check scripts/site.js
rg --fixed-strings "https://www.amazon.es/dp/B0HQ4X8MDZ" index.html
rg -- "<audio|\\.mp3|id=\"meditaciones\"" index.html
```

Expected: JavaScript exits 0; Amazon has matches; meditation search has no matches.

- [ ] **Step 5: Preview through an HTTP server**

Run: `python -m http.server 8000`

Expected: `http://localhost:8000/`, all three legal URLs, CSS, and JavaScript return HTTP 200.

- [ ] **Step 6: Commit legal drafts and documentation**

```powershell
git add aviso-legal.html privacidad.html cookies.html README.md
git commit -m "Añade borradores legales y guía operativa"
```

### Task 6: Final review and publication readiness

**Files:**
- Review: all changed files.

**Interfaces:**
- Consumes: completed site.
- Produces: verified branch ready for user-approved push to GitHub Pages.

- [ ] **Step 1: Run the full verification set**

Run:

```powershell
python -m unittest tests.test_site -v
node --check scripts/site.js
git status --short
```

Expected: all tests pass; JavaScript exits 0; only intentional plan/spec files or no files remain uncommitted.

- [ ] **Step 2: Review the diff against the specification**

Run:

```powershell
git diff d8a386e..HEAD --stat
git log --oneline -8
```

Expected: the implementation covers the main page, visual system, JavaScript, legal drafts, tests, and README without adding external dependencies.

- [ ] **Step 3: Obtain explicit publication approval**

Do not push to `main` until the user approves publishing the completed redesign. A push to `main` automatically updates GitHub Pages.
