# Test Plan — Collapsible Sidebar Nav

# Test Plan — Sidebar (Desktop)

## Coverage Summary
7 E2E browser tests · 9 UX visual tests · 3 unit tests · 7 edge-case tests = 26 total covering the sidebar-desktop feature area.

## Sidebar Desktop

Desktop (≥768px) left sidebar: expanded (240px, icons+labels) ↔ collapsed (60px, icon-only strip), 11 navigation links, "Get Started" CTA, active-section highlighting via scroll-spy, smooth-scroll navigation.

- **SIDED-E2E-001** *(e2e_browser)* — Sidebar is visible and expanded on page load at 1280px viewport, 240px wide, with 11 links showing icons and labels.
- **SIDED-E2E-002** *(e2e_browser)* — Clicking the collapse toggle animates the sidebar from 240px to a 60px icon-only strip; labels disappear.
- **SIDED-E2E-003** *(e2e_browser)* — Clicking the expand toggle restores the sidebar from 60px back to 240px; labels reappear.
- **SIDED-E2E-004** *(e2e_browser)* — Clicking a sidebar link smooth-scrolls to its section; the active highlight moves to that link.
- **SIDED-E2E-012** *(e2e_browser)* — "Get Started" CTA scrolls to #overview; in collapsed state it shows as an icon-only button that also scrolls to #overview.
- **SIDED-UT-001** *(unit)* — Sidebar element exists in DOM with the `expanded` class on desktop load.
- **SIDED-UT-002** *(unit)* — Sidebar computed width is 240px when in expanded state.
- **SIDED-UT-003** *(unit)* — Sidebar computed width is 60px when in collapsed state.
- **SIDED-UX-A-001** *(ux_visual)* — Mockup A (expanded desktop): sidebar renders 11 links, each with an SVG icon and text label, on first load.
- **SIDED-UX-A-002** *(ux_visual)* — Mockup A (expanded desktop): sidebar labels are readable and properly aligned beside icons.
- **SIDED-UX-A-003** *(ux_visual)* — Mockup A (expanded desktop): "Get Started" CTA button is visible at the sidebar bottom with full-width styling.
- **SIDED-UX-B-001** *(ux_visual)* — Mockup B (collapsed desktop): sidebar shows 60px icon-only strip with no text labels visible.
- **SIDED-UX-B-002** *(ux_visual)* — Mockup B (collapsed desktop): icons are centered within the 60px strip; each link is still clickable.
- **SIDED-UX-B-003** *(ux_visual)* — Mockup B (collapsed desktop): "Get Started" CTA appears as icon-only at the bottom.
- **SIDED-UX-E-001** *(ux_visual)* — Mockup E (active highlight): active sidebar link has purple/violet background and white text.
- **SIDED-UX-E-002** *(ux_visual)* — Mockup E (active highlight): only one sidebar link has the active class at a time; inactive links remain default style.
- **SIDED-UX-E-003** *(ux_visual)* — Mockup E (active highlight): active indicator bar (left border) is visible on the active link.
- **SIDED-EDGE-001** *(e2e_browser)* — Clicking sidebar link when already at that section does not cause errors or unexpected scroll.
- **SIDED-EDGE-002** *(e2e_browser)* — Rapid toggle clicks result in sidebar reaching a stable expanded or collapsed state.
- **SIDED-EDGE-003** *(e2e_browser)* — At 768px viewport (minimum desktop) with sidebar expanded, no horizontal overflow occurs.
- **SIDED-EDGE-004** *(e2e_browser)* — With `prefers-reduced-motion: reduce`, sidebar width change is instant (no 0.3s animation).
- **SIDED-EDGE-005** *(e2e_browser)* — Fast scrolling through multiple sections — active highlight settles on the correct section after scroll ends.
- **SIDED-EDGE-006** *(e2e_browser)* — Collapsing and re-expanding the sidebar preserves the current active link highlight.
- **SIDED-EDGE-007** *(e2e_browser)* — Active link highlight still works in collapsed icon-only state (icon styling changes).

## Gaps & Open Questions

- **GAP-1** Should collapsed-state icon-only links show a tooltip on hover? Recommendation: Not tested — spec marks tooltips as out of scope / nice-to-have.
- **GAP-2** Should sidebar state persist across page reloads via localStorage? Recommendation: Not tested — spec explicitly says no persistence (§18); sidebar resets to expanded on each load.
# Test Plan — Sidebar Mobile

## Coverage Summary
12 test tasks: 3 unit, 4 E2E browser, 3 UX visual, 2 edge-case — covering mobile drawer open/close, backdrop dismiss, link navigation, scroll, body scroll lock, and Escape-key recovery.

## Mobile Drawer Open/Close

- **SIDM-E2E-06** *(e2e_browser)* — At 375×700 viewport, tapping the hamburger button slides the sidebar drawer in from the left with a backdrop overlay; all 11 links with icons + labels are visible.
- **SIDM-E2E-07** *(e2e_browser)* — With the drawer open, tapping the semi-transparent backdrop closes the drawer and hides the backdrop.
- **SIDM-E2E-08** *(e2e_browser)* — With the drawer open, tapping a sidebar link ("Pipeline") closes the drawer and smooth-scrolls to the Pipeline section.
- **SIDM-E2E-09** *(e2e_browser)* — At 375×700 viewport without opening the drawer, the sidebar is off-canvas (not visible), content is full-width, and only the top bar with brand + hamburger is visible.

## Unit Tests (CSS/JS Class Assertions)

- **SIDM-UT-04** *(unit)* — At viewport <768px, the sidebar has `transform: translateX(-100%)` by default (off-canvas, not visible) — verified via computed style.
- **SIDM-UT-05** *(unit)* — Adding `.open` class to `#sidebar` sets `transform: translateX(0)` (visible) — verified via computed style.
- **SIDM-UT-06** *(unit)* — When the mobile drawer is open, `document.body` computed `overflow` is `hidden`; when closed, it is restored to the default (empty/visible).

## UX Visual Tests (Per Mockup)

- **SIDM-UX-F-001** *(ux_visual)* — Mockup F: Mobile top bar with brand + hamburger, no sidebar visible, content full-width.
- **SIDM-UX-F-002** *(ux_visual)* — Mockup F: Hamburger button has visible touch-target area ≥44×44px and `aria-label` attribute.
- **SIDM-UX-F-003** *(ux_visual)* — Mockup F: Content area has `margin-left: 0` — no sidebar space reserved on mobile.
- **SIDM-UX-C-001** *(ux_visual)* — Mockup C: Drawer slides in from left; semi-transparent backdrop is visible during transition.
- **SIDM-UX-D-001** *(ux_visual)* — Mockup D: Drawer fully open showing all 11 sidebar links with icons + text labels + "Get Started" CTA at bottom.
- **SIDM-UX-D-002** *(ux_visual)* — Mockup D: Backdrop covers full viewport with `rgba(0,0,0,0.5)` background while drawer is open.
- **SIDM-UX-D-003** *(ux_visual)* — Mockup D: Active section link has violet accent highlight consistent with desktop expanded state.

## Edge Cases

- **SIDM-EDGE-001** *(e2e_browser)* — Rapid hamburger taps (5×) — sidebar ends in the correct final state matching the last toggle; no stuck mid-animation state.
- **SIDM-EDGE-002** *(e2e_browser)* — Resize to desktop (≥768px) while mobile drawer is open — `.open` is removed, backdrop hidden, sidebar transitions to desktop expanded state, body overflow restored.

## Mandatory E2E Coverage

- **SIDM-E2E-SMOKE-001** *(e2e_browser)* — Realistic golden-path mobile session: load at 375px → tap hamburger to open drawer → tap "Agents" link → verify page scrolls to Agents + drawer closes → tap hamburger to reopen → tap backdrop to close → verify sidebar is off-canvas again.
- **SIDM-E2E-ESC** *(e2e_browser)* — Error + recovery: open the drawer, press Escape, verify the drawer closes and backdrop disappears (Escape-dismiss recovery path).

## Gaps & Open Questions

- **GAP-SIDM-1** Question: Should the "Get Started" CTA inside the mobile drawer also close the drawer and scroll to `#overview`, just like a regular sidebar link? Recommendation: Yes — same behavior as other links, add SIDM-E2E-08-CTA as an explicit test.
# Test Plan — Sidebar Scroll-Spy & Back-to-Top

## Coverage Summary

4 E2E browser tests · 4 UX visual tests · 5 unit tests · 3 integration tests = 16 total covering the sidebar-scroll-spy feature area (scroll-spy targeting & active highlighting, back-to-top visibility/position/behavior).

## Scroll-Spy Active Highlighting

The scroll-spy retargets from the old `.nav-link` / `.nav-mobile a` selectors to `.sidebar-link`. As the user scrolls, the sidebar link whose corresponding section is in the viewport receives an `.active` class with violet accent. Only one link is active at a time.

- **SIDSP-E2E-005** *(e2e_browser)* — Scroll-spy highlights correct sidebar link on manual scroll through multiple sections.
- **SIDSP-SS-001** *(unit)* — Scroll-spy targets `.sidebar-link` elements, not `.nav-link`, for active highlighting.
- **SIDSP-SS-002** *(unit)* — Scrolling to `#agents` adds `.active` to `.sidebar-link[href="#agents"]` only.
- **SIDSP-SS-003** *(unit)* — Only one `.sidebar-link` has the `.active` class at any scroll position.
- **SIDSP-SS-004** *(unit)* — The active sidebar link has a violet accent color matching the spec.
- **SIDSP-INT-001** *(integration)* — Click sidebar link → scroll completes → spy updates active class to match scrolled-to section.
- **SIDSP-INT-003** *(integration)* — Scrolling across section boundaries updates active highlight from one link to the next.
- **SIDSP-UX-E-001** *(ux_visual)* — Mockup E: active section highlight renders with violet accent on expanded sidebar.
- **SIDSP-UX-E-002** *(ux_visual)* — Mockup E: inactive sidebar links are not highlighted — only the in-view section gets accent.
- **SIDSP-UX-E-003** *(ux_visual)* — Mockup E: active link left border or background highlight is visually distinct from inactive links.

## Scroll-Spy in Collapsed Sidebar

When the sidebar is collapsed to the 60px icon-only strip, the scroll-spy still highlights the correct section's icon.

- **SIDSP-E2E-014** *(e2e_browser)* — Scroll-spy updates active icon highlight in collapsed sidebar state after scrolling.
- **SIDSP-UX-B-002** *(ux_visual)* — Mockup B: active icon is visually highlighted in the collapsed icon-only sidebar.

## Back-to-Top Button

The back-to-top button appears after scrolling past the hero section. On desktop, it is positioned relative to the content area (`right` = sidebar width + 32px gutter). On mobile, it sits at the viewport bottom-right (16px). Clicking it smooth-scrolls to the top.

- **SIDSP-E2E-010** *(e2e_browser)* — Back-to-top button appears after scrolling past hero; positioned correctly on desktop (272px right expanded, 92px collapsed) and mobile (16px right).
- **SIDSP-E2E-011** *(e2e_browser)* — Clicking back-to-top smooth-scrolls to page top and button hides after arrival.
- **SIDSP-E2E-015** *(e2e_browser)* — Back-to-top repositions smoothly during sidebar collapse/expand transition, not teleporting.
- **SIDSP-BTT-001** *(unit)* — Back-to-top computed `right` is 272px when sidebar expanded, 92px when collapsed, 16px on mobile.
- **SIDSP-BTT-002** *(unit)* — Back-to-top button is hidden when scroll position is at or above hero section, visible after scrolling past hero.
- **SIDSP-BTT-003** *(unit)* — Back-to-top `right` property has a CSS transition that animates during sidebar state changes.
- **SIDSP-INT-002** *(integration)* — Collapse sidebar → back-to-top repositions → expand sidebar → back-to-top repositions back; position matches sidebar width at each state.
- **SIDSP-UX-C-001** *(ux_visual)* — Mockup C: back-to-top button visible in the bottom-right of the content area when scrolled past hero.
- **SIDSP-UX-C-002** *(ux_visual)* — Mockup C: back-to-top does not overlap the sidebar or the viewport edge on desktop.
- **SIDSP-UX-C-003** *(ux_visual)* — Mockup C: back-to-top button position relative to content area, not viewport, on desktop.

## Default State (Page Load)

- **SIDSP-UX-A-001** *(ux_visual)* — Mockup A: sidebar shows "Overview" as the default active link on page load.
- **SIDSP-UX-A-002** *(ux_visual)* — Mockup A: only the first section link has `.active` at scroll position 0; no other links highlighted.
- **SIDSP-UX-A-003** *(ux_visual)* — Mockup A: back-to-top button is not visible at page top (scroll position 0).

## Collapsed Sidebar Visual

- **SIDSP-UX-B-001** *(ux_visual)* — Mockup B: collapsed icon-only sidebar shows icons centered with no labels.
- **SIDSP-UX-B-003** *(ux_visual)* — Mockup B: back-to-top button is repositioned rightward when sidebar is collapsed.

## Edge Cases

- **SIDSP-EDGE-001** *(e2e_browser)* — Rapid scrolling through multiple sections: active highlight settles on correct section after scroll ends.

## Gaps & Open Questions

- **GAP-1** Question: Should we E2E-test scroll-spy with hash-change navigation (e.g., loading `index.html#agents` directly)? Recommendation: Yes — add a test that verifies the sidebar highlights the correct section on page load with a URL hash. This is a common user entry point and can break if the scroll-spy only runs on `scroll` events, not on initial hash resolution.
# Test Plan — Sidebar Responsive

## Coverage Summary
2 E2E browser tests · 4 UX visual tests · 2 unit tests · 2 edge-case tests = 10 total covering responsive breakpoint crossing for the sidebar.

## Sidebar Responsive Breakpoint Crossing

When the browser viewport crosses the 768px breakpoint, the sidebar must transition between desktop mode (expanded/collapsed, persistent) and mobile mode (off-canvas drawer) without leaving residual classes, CSS custom properties, or body scroll locks in a broken state.

- **SIDR-E2E-015** *(e2e_browser)* — Resize desktop (1280px) → mobile (375px): sidebar goes off-canvas, content goes full-width, no broken state.
- **SIDR-E2E-016** *(e2e_browser)* — Resize mobile (375px, drawer open) → desktop (1280px): drawer closes, sidebar appears expanded, content shifts right.
- **SIDR-UT-008** *(unit)* — matchMedia listener exists and fires on 768px breakpoint crossing.
- **SIDR-UT-009** *(unit)* — Sidebar state resets correctly on breakpoint crossing: classes, CSS custom property, content margin, and body overflow all reconcile.
- **SIDR-UX-F-001** *(ux_visual)* — Mockup F: mobile top bar with no sidebar visible after desktop→mobile resize.
- **SIDR-UX-F-002** *(ux_visual)* — Mockup F: content is full-width after desktop→mobile resize with no residual margin.
- **SIDR-UX-A-001** *(ux_visual)* — Mockup A: sidebar appears expanded after mobile→desktop resize (drawer was closed).
- **SIDR-UX-A-002** *(ux_visual)* — Mockup A: content area is shifted right with correct margin after mobile→desktop resize.
- **SIDR-EDGE-001** *(e2e_browser)* — Rapid resize back-and-forth across 768px breakpoint leaves sidebar in a valid state (no hybrid classes, no stuck overflow).
- **SIDR-EDGE-002** *(e2e_browser)* — Viewport set exactly to 768px puts sidebar into desktop EXPANDED state (breakpoint is ≥768px).

## Gaps & Open Questions
- **GAP-SIDR-1** Question: Should the resize handler be debounced? Recommendation: Yes — debounce to ~150ms to avoid thrashing layout during drag-resize, but ensure the final state is always correct even after rapid resizing. The test SIDR-EDGE-001 covers the outcome regardless of implementation detail.
# Test Plan — Sidebar A11y Preserved

## Coverage Summary
6 test tasks: 2 unit, 3 e2e, 1 integration covering accessibility (prefers-reduced-motion, no-JS fallback) and preserved features (pipeline lighting, scroll reveal, footer links).

## Sidebar Accessibility & Preserved Features

This area covers the `prefers-reduced-motion` media query behavior (sidebar toggle instant, reveals instant), the no-JS fallback (sidebar expanded, toggle hidden, reveals visible), and three preserved-feature guarantees: pipeline phase lighting on scroll, scroll-reveal animations triggering, and footer navigation links still smooth-scrolling.

- **SIDA-E2E-017** *(e2e_browser)* — With prefers-reduced-motion enabled, toggling the sidebar is instant and scroll reveals appear instantly with no animation.
- **SIDA-E2E-013** *(e2e_browser)* — Scrolling through the Pipeline section lights up phases progressively — existing behavior preserved after sidebar restructure.
- **SIDA-E2E-014** *(e2e_browser)* — Scrolling down slowly triggers scroll-reveal fade-in on cards and sections — existing behavior preserved after sidebar restructure.
- **SIDA-E2E-018** *(e2e_browser)* — Clicking a footer navigation link smooth-scrolls to the corresponding section — footer links are not sidebar links and must still function.
- **SIDA-UT-011** *(unit)* — With prefers-reduced-motion: sidebar elements have transition-duration of 0s and no transition property; reveal elements are visible immediately.
- **SIDA-UT-012** *(unit)* — With JavaScript disabled: sidebar is visible in expanded state on desktop, all .reveal content is visible, and the collapse toggle is hidden.

## Gaps & Open Questions

- **GAP-SIDA-1** Question: Should the no-JS test (SIDA-UT-012) also verify that mobile sidebar appears as a simple vertical nav above content (as stated in implementation-plan §1.6)? Recommendation: Yes — add a viewport-375px no-JS check in a future mobile-a11y area run. This area is desktop-scoped for no-JS per UT-12 spec definition.
