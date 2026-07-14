# Clarifications — Collapsible Sidebar Nav for JackHamr Documentation Website

## Mode: Build (feature enhancement to existing index.html)

## Original Request
Convert the top nav bar to a collapsible left sidebar for the documentation website. The sidebar should be collapsible.

## Q/A from Gate 0

### Q1: Collapsed state appearance?
**A: Icon-only strip** — VS Code activity bar style. Just the section icons visible in a narrow strip (~60px), no text labels.

### Q2: Default state on desktop?
**A: Expanded by default** — Full sidebar (~240px) with icons + labels visible on page load on desktop.

### Q3: Mobile behavior?
**A: Slide-out drawer** — Hamburger toggles a drawer that slides in from the left. No persistent sidebar on mobile.

## Assumptions (confirmed by user)

1. Expanded sidebar width ~240px, collapsed (icon strip) ~60px.
2. Main content area shifts right when sidebar expands, slides left when collapsed — content respects the sidebar (no longer full-bleed).
3. Smooth width transition (0.3s ease) on expand/collapse.
4. Nav active-section highlighting moves from top nav links to sidebar links.
5. The existing hamburger button (top-right on mobile) toggles the slide-out drawer; on desktop a collapse/expand toggle button sits at the sidebar.
6. The sticky top bar stays but becomes a slim top bar (brand + hamburger on mobile, brand + collapse toggle on desktop) — section links move into the sidebar.
7. Back-to-top button repositions to the content area.
8. Pipeline progress indicator stays in the hero section as-is.
9. The "Get Started" CTA moves into the sidebar at the bottom.
10. Mobile breakpoint: below 768px the sidebar becomes a slide-out drawer (off-canvas, slides in on hamburger tap).
11. Desktop (≥768px): sidebar is persistent — either expanded (240px) or collapsed (60px icon strip).
12. Dark theme unchanged: slate-900 (#0f172a) background, violet (#7c3aed) primary.
13. Inter + JetBrains Mono fonts unchanged.
14. Scroll reveal animations, pipeline phase lighting, and all existing interactivity preserved.
15. The existing index.html at /root/projects/runs/2b3dada2-7364-4a39-aeb6-7251193c4ff7/index.html is the starting point.
