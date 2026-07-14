# Implementation Plan — Collapsible Left Sidebar Navigation

**Run ID:** 2b3dada2-7364-4a39-aeb6-7251193c4ff7
**Spec:** `spec.md` (same directory)
**Source file:** `index.html` (same directory) — single-file static site, no build step
**Date:** 2026-07-13
**Status:** Ready for development

---

## 1. Architecture Decisions

### 1.1 Modification, not rebuild

The entire site is one `index.html` (~853 lines): inline `<style>` in `<head>`, hardcoded HTML body, single IIFE `<script>` before `</body>`. Every change is an in-place modification to this file. No new files, no build step, no dependencies added.

### 1.2 CSS custom property drives sidebar width

A single `--sidebar-width` custom property on `:root` (or `.sidebar`) controls the width. Expanded = `240px`, collapsed = `60px`, mobile = `0px` (content full-width). The content area uses `margin-left: var(--sidebar-width)` and the back-to-top button uses `right: calc(var(--sidebar-width) + 32px)`. JS toggles the property value alongside the `.expanded`/`.collapsed` class. This avoids hardcoding the width in three places and keeps the 0.3s transition in sync across sidebar, content, and back-to-top.

### 1.3 Sidebar is always in the DOM; state is class-driven

The `<aside class="sidebar">` is present on all viewports. On desktop it's persistent (expanded/collapsed). On mobile it's off-canvas via `transform: translateX(-100%)` and slides in with `.open` class. No DOM manipulation, no cloning — just CSS classes. This simplifies the resize handler: it only manages classes, not element creation.

### 1.4 Top bar stays sticky, slimmed down

The existing `<nav class="nav" id="navbar">` remains `position: sticky; top: 0`. Section links (`.nav-links`) and the CTA (`.nav-cta`) are removed from it. On desktop it shows brand + collapse toggle; on mobile it shows brand + hamburger. The collapse toggle is a new button inside the nav; the existing hamburger button is repurposed (its click handler changes from toggling `.nav-mobile` to toggling `.sidebar.open`).

### 1.5 Scroll-spy selector swap

The existing scroll-spy builds its section-link map from `.nav .nav-link` and `.nav-mobile a`. After restructure, both are gone. The spy is retargeted to `.sidebar-link` — a single set of links that serves both desktop and mobile. The matching algorithm (find section whose `offsetTop` range contains scroll position) is unchanged.

### 1.6 No-JS fallback via `<noscript>` CSS

The existing `<noscript>` block reveals `.reveal` content and hides `.back-to-top`. It's extended to force the sidebar to its expanded state (override `--sidebar-width: 240px`, force `.content` margin, show labels) and hide the collapse toggle. On mobile without JS, the sidebar is forced visible as a simple vertical nav above content.

---

## 2. Per-Repo Changes

All changes are in `/root/projects/runs/2b3dada2-7364-4a39-aeb6-7251193c4ff7/index.html`.

| # | File | Change | Why |
|---|---|---|---|
| 1 | `index.html` — HTML body | Remove `.nav-links` div (11 links) and `.nav-cta` button from `<nav>`. Add collapse toggle button to `<nav>`. Repurpose existing hamburger (keep `id="hamburger"`). Remove entire `.nav-mobile` div. Add `<aside class="sidebar" id="sidebar">` with 11 `.sidebar-link` entries (each = SVG icon + `.label` span) and a `.sidebar-cta` "Get Started" button at the bottom. Add `<div class="sidebar-backdrop" id="sidebarBackdrop">`. Wrap hero + all sections + footer in `<main class="content" id="content">`. | Core structural restructure (SB-01, SB-02, SB-03) |
| 2 | `index.html` — `<style>` | Add `.sidebar`, `.sidebar.expanded`, `.sidebar.collapsed`, `.sidebar-link`, `.sidebar-link.active`, `.sidebar-link .label`, `.sidebar-cta`, `.sidebar-toggle` CSS. Add `--sidebar-width` custom property. | Sidebar visual states (SB-04, SB-05, SB-09, SB-10) |
| 3 | `index.html` — `<style>` | Add `.content { margin-left: var(--sidebar-width); transition: margin-left 0.3s ease; }`. Update `.back-to-top` `right` to `calc(var(--sidebar-width) + 32px)` with `transition: right 0.3s ease`. Add mobile override (`margin-left: 0`, `right: 16px`). | Content shift + back-to-top reposition (SB-06, SB-11, GAP-5) |
| 4 | `index.html` — `<style>` | Add mobile (`max-width: 767px`) sidebar rules: off-canvas default (`transform: translateX(-100%)`), `.sidebar.open` (`transform: translateX(0)`), `.sidebar-backdrop` overlay, slim top bar (hide collapse toggle, show hamburger). Add desktop (`min-width: 768px`) rules: hide hamburger, show collapse toggle, sidebar persistent. Remove old `.nav-links`/`.nav-cta`/`.nav-mobile` mobile rules (they no longer exist). | Mobile drawer + responsive top bar (SB-07, SB-08) |
| 5 | `index.html` — `<script>` | Add sidebar toggle handler: clicking `.sidebar-toggle` swaps `.expanded`/`.collapsed` on `#sidebar` and updates `--sidebar-width` (`240px` ↔ `60px`). | Collapse/expand (SB-12) |
| 6 | `index.html` — `<script>` | Add mobile drawer handler: hamburger click toggles `.open` on `#sidebar` and backdrop visibility. Backdrop click closes. Sidebar link click closes. Body scroll lock (`overflow: hidden`) on open. Escape key closes. | Mobile drawer (SB-13, SB-17, GAP-4) |
| 7 | `index.html` — `<script>` | Retarget scroll-spy: replace `.nav .nav-link` / `.nav-mobile a` selectors with `.sidebar-link`. Update smooth-scroll handler to include `.sidebar-link`. Remove `.nav-mobile` references. | Scroll-spy + smooth-scroll (SB-14, SB-15) |
| 8 | `index.html` — `<script>` | Add resize listener using `matchMedia('(min-width: 768px)')`: on desktop, remove `.open`, ensure `.expanded` is set (reset to expanded per §18). On mobile, remove `.expanded`/`.collapsed`, ensure sidebar is off-canvas, restore body overflow. | Responsive state management (SB-16, GAP-2) |
| 9 | `index.html` — `<noscript>` + ARIA | Extend `<noscript>` CSS to force sidebar expanded + content margin on desktop, force sidebar visible above content on mobile, hide toggle. Add `aria-label` to toggle/hamburger, `role="navigation"` to sidebar, `role="list"`/`listitem` on nav structure. | No-JS fallback + accessibility (SB-21, a11y checklist) |

---

## 3. API Contract

N/A — this is a static single-file HTML enhancement with no API, no backend, no build step. No external contracts change. Tailwind Play CDN and Google Fonts loads are unchanged.

---

## 4. New Files Needed

None. All changes are modifications to the existing `index.html`.

---

## 5. Risk Flags

| Risk | Severity | Mitigation |
|---|---|---|
| **Content horizontal overflow** when sidebar width + content `max-width: 1280px` + margin exceed viewport | Medium | Use `margin-left` (not `width: calc(...)`) on `.content` so content shrinks naturally. Existing `html, body { max-width: 100% }` prevents horizontal scroll. Verify at 768–1024px. |
| **Scroll-spy breakage** if section IDs don't match sidebar `href` attributes | Medium | Sidebar links must use the exact same `href="#<id>"` values as the existing nav. All 11 IDs verified: overview, pipeline, agents, orchestration, skills, memory, gates, environments, board, integrations, customization. |
| **Back-to-top position jump** during transition if `right` has no transition | Low | Add `transition: right 0.3s ease` to `.back-to-top` (GAP-5). |
| **Body scroll lock not cleaned up** on resize-to-desktop while drawer open | Low | Resize handler must restore `document.body.style.overflow = ''` when crossing to desktop. |
| **`prefers-reduced-motion`** — sidebar transitions should be instant | Low | Existing global `@media (prefers-reduced-motion: reduce)` rule already nukes all transitions via `transition: none !important`. No additional work needed — the new `transition` properties are covered. |
| **Existing hamburger click handler** references `.nav-mobile` which is being removed | Medium | The old handler (`hm.addEventListener('click', ... nm.classList.toggle('open')`) must be replaced entirely in task 6. If the old `.nav-mobile` element is removed in task 1 but the JS isn't updated until task 6, the page is broken between tasks. **Task 6 must be done immediately after task 1** or the developer doing Task 1 should also stub the hamburger handler. See dependency notes. |
| **Footer nav links** use `.nav-link` class — the smooth-scroll handler and scroll-spy must not break footer links | Low | Footer links keep `.nav-link` class. The smooth-scroll handler currently selects `a.nav-link` — after restructure, sidebar links use `.sidebar-link` (different class), so footer links need to be included in the smooth-scroll selector separately. Task 7 handles this. |

---

## 6. Test Strategy

### Existing tests
The run directory contains many `test_*.py` and `run_test_*.py` files from the original build (TASK-005). These test the *current* top-nav layout. After the sidebar restructure, any test that asserts on `.nav-links`, `.nav-mobile`, or top-nav active highlighting will fail and must be updated or replaced. The QA phase will produce new tests per the spec's §12–13 test plan.

### New tests (per spec §12)
| File | Coverage |
|---|---|
| `tests/test_sidebar_desktop.py` | UT-01–03, E2E-01–05, E2E-12 — expanded/collapsed states, toggle, CTA |
| `tests/test_sidebar_mobile.py` | UT-04–06, E2E-06–09 — drawer open/close, backdrop, link navigation |
| `tests/test_scroll_spy.py` | UT-07, E2E-05, E2E-14 — active highlighting on scroll |
| `tests/test_responsive.py` | UT-08–09, E2E-15–16 — breakpoint crossing both directions |
| `tests/test_back_to_top.py` | UT-10, E2E-10–11 — position + visibility + click |
| `tests/test_accessibility.py` | UT-11–12, E2E-17 — reduced motion, no-JS fallback |
| `tests/test_preserved_features.py` | E2E-13–14, E2E-18 — pipeline lighting, reveal, footer links |

Tests use Playwright (Python) with `executable_path="/usr/local/bin/chromium"` and `args=["--no-sandbox"]`, loading `index.html` via `file://` protocol. No server needed.

---

## 7. Scope Estimate

| Change group | Scope |
|---|---|
| HTML restructure (task 1) | Medium — ~80 lines added, ~30 removed, structural shift |
| CSS sidebar states (task 2) | Medium — ~60 lines of new CSS |
| CSS content + back-to-top (task 3) | Small — ~15 lines |
| CSS mobile + responsive top bar (task 4) | Medium — ~50 lines, breakpoint logic |
| JS sidebar toggle (task 5) | Small — ~15 lines |
| JS mobile drawer (task 6) | Small-Medium — ~30 lines |
| JS scroll-spy retarget (task 7) | Small — ~10 lines changed |
| JS resize handler (task 8) | Small — ~20 lines |
| No-JS + a11y (task 9) | Small — ~15 lines |

**Overall: Medium** — the feature touches HTML, CSS, and JS but is contained to a single file with no external dependencies.

---

## 8. Task Dependency Graph

```
Task 1 (HTML restructure)
  ├── Task 2 (CSS sidebar states)        — can start in parallel, same file
  ├── Task 3 (CSS content + back-to-top) — can start in parallel
  └── Task 4 (CSS mobile + responsive)   — can start in parallel
       │
       (Tasks 2–4 are CSS-only and independent of each other,
        but all depend on Task 1's HTML existing for selectors to match)
       │
Task 5 (JS sidebar toggle)        — depends on 1, 2
Task 6 (JS mobile drawer)         — depends on 1, 4 (replaces old hamburger handler)
Task 7 (JS scroll-spy retarget)   — depends on 1
Task 8 (JS resize handler)        — depends on 1, 5, 6
Task 9 (No-JS + a11y)             — depends on 1, 2, 4
```

**Critical path:** 1 → 2 → 5 → 8. Tasks 3, 4, 6, 7, 9 branch off.

**Important ordering note:** Task 1 removes `.nav-mobile` and the old hamburger handler breaks. Task 6 replaces the hamburger handler. To avoid a broken intermediate state, Task 6 should immediately follow Task 1 (or the developer doing Task 1 should also stub the hamburger handler). The `depends_on` field reflects this.
