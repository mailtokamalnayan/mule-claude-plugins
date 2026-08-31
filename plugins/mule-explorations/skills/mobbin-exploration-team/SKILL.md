---
description: Generate a standalone exploration on the mule-ui design system — one subject from a Figma link, a screenshot, or a phrase; three different design concepts, live and clickable, in a single HTML file under ~/Developer/explorations
argument-hint: <figma link | screenshot path | phrase> [--page] [--mobile] [--fresh] [--count N] [--width Npx] (e.g. "order summary card", "~/Desktop/shot.png --count 5", "https://figma.com/design/... --mobile")
---

You are producing a **standalone exploration**: one self-contained HTML file that renders **three distinct design concepts** for one subject, stacked down the page, live and clickable, so a human can pick a direction. Every concept is styled with the **mule-ui design system tokens** bundled with this skill — this run does not depend on any repo.

The user wants an exploration of: **$ARGUMENTS**

If `$ARGUMENTS` is empty, ask what to explore, then proceed.

## Subject intake — three input kinds

Decide what the input is, in this order:

1. **A Figma URL** (`figma.com/design/...`). Extract `fileKey` and `node-id`, call the Figma MCP's `get_screenshot` tool on that node (the tool's full name varies by install — find the available tool whose name contains `figma` and `screenshot`), download the PNG, and read it. That image is the **current design** of the subject. Name the subject from what the image shows, not from the node name alone. If no Figma MCP is available, tell the user once: "No Figma access — paste a screenshot path instead, or set Figma up with `claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp` and restart." Then ask for a screenshot or a phrase and continue.
2. **A local image path** (ends in `.png`/`.jpg`/`.webp`, or the file exists). Read it. Same rule: the image is the current design.
3. **Anything else is a phrase.** There is no current design; go straight to concepts.

When a current design exists (case 1 or 2), **recreate its structure once at the top of the page as an unnumbered "Current" reference** — built from the tokens, faithful in layout and hierarchy, not pixel-perfect. This keeps all three concepts new ideas instead of one slot restating the status quo. Read measurable facts off the image (what is promoted, where the CTA sits, what the chrome costs) and let the concepts argue with those facts.

## Scope — a component, not a page

**By default the subject is a single component**, and the exploration is about how that component looks and behaves — its states and its interactions. Do not redesign the surrounding page, and do not invent page chrome around it. Render each concept on a neutral canvas with only as much surrounding context as spacing and hierarchy need to read honestly.

Only explore a whole page when the user passes `--page` or the subject is plainly a page ("checkout screen", "settings page").

**States and behaviour both matter.**

- **States** — show the component's real state set: default, hover, focus, active, loading, error, empty, disabled — whatever applies. States are shown *on the page*, not described in a note.
- **Behaviour** — the component actually works. The dropdown opens, the tabs switch, the toggle flips, validation fires. Vanilla JS, no framework, no build step.

**When the component is too big to stack every state**, put the states behind tabs or a dropdown *inside* that concept's frame, so the page stays scannable. Small components: lay the states out in a row or grid, labelled.

Motion and micro-interaction are **not** the subject. Transitions should feel right but they aren't what's being explored.

## Three concepts, no ranking

- **Three by default, desktop by default.** Override count with `--count N` or plain language.
- **No safe→bold ordering, no "current default" slot.** The concepts are peers — inspiration, not a recommendation ladder.
- **Each concept is a real bet**, not a tint of the same thought. Vary the actual approach: layout, hierarchy, density, how the interaction is triggered, what gets promoted and what gets hidden. If two concepts could be described by the same sentence, one of them isn't earning its slot.
- **Go wide before going deep.** Before designing anything, enumerate the candidate *paradigms* — where the control could live, how it could be triggered, which pattern family it belongs to (menu vs. toggle vs. dedicated button vs. inline vs. panel…). Spend one concept per paradigm until paradigms run out; only then vary composition within a paradigm.
- **Hold everything else constant** — same content, same data, same copy across all concepts, so only the explored dimension changes.

## Output — one HTML file

Write `~/Developer/explorations/<kebab-subject>/01.html`. Create the folders if they do not exist. If the subject folder already exists, write the next number (`02.html`, `03.html`) — **never overwrite a previous pass**. No dates, no suffixes. If the user names a different output folder, use it with the same structure.

Every exploration file starts with a `<title>` tag (`<title><Subject> — Mule explorations</title>`, right after the doc comment) — these are raw static files; without it, tabs are indistinguishable.

Then update `~/Developer/explorations/index.html`: a **card grid, not a text list** — one block per pass in a three-column grid (`grid grid-cols-3 gap-4`). Each card links to its file (relative link, `<subject>/01.html`) and carries, top to bottom: the vignette, the pass number + concept count as an uppercase kicker, and the subject as the card title. **Nothing else.** Create the index if it doesn't exist; backfill a vignette for any existing card that lacks one.

### The vignette

An abstract mini-sketch of the subject that a person recognizes in a scan — not a faithful miniature. **No screenshots, no images, no iframes.** Hand-built primitives stay crisp and on-token forever.

Build every vignette from exactly these three CSS primitives (defined once in the index `<style>`):

```css
/* 128px muted stage the sketch sits on */
.vg { height: 128px; background: var(--color-neutral-bg-alt-soft); border-bottom: 1px solid var(--color-neutral-border); display: flex; align-items: center; justify-content: center; overflow: hidden; }
/* white mini-surface (a card, a menu, a toolbar) */
.vg-card { background: var(--color-neutral-bg); border: 1px solid var(--color-neutral-border); border-radius: 4px; box-shadow: var(--shadow-card); }
/* grey bar standing in for a line of text */
.vg-bar { background: var(--color-neutral-bg-alt); border-radius: 2px; height: 6px; }
```

Construction procedure, per card:

1. **Name the subject's one signature element** — the thing you'd point at in the real screen. The vignette shows that element and nothing else.
2. **Compose it on one `.vg-card` ~220px wide** inside the `.vg` stage, using `.vg-bar`s for all text. Never write real sentences.
3. **Spend at most 2 real glyphs** where identity needs them: one `fa-light` icon, a ✓, or one tiny labeled chip at 7–9px. (Add the kit script to the index file too.)
4. **Structure over decoration**: recreate the element's layout facts with plain divs and the border/surface tokens — no colors beyond the tokens.

**Hard constraint — touch nothing else.** The exploration file and the index are the only files you write. No app code, no repos.

### File scaffolding

```html
<!-- Standalone exploration — mule-ui tokens, not wired into any app.
     Subject: <subject>
     01 <name> — <one line>
     02 <name> — <one line>
     03 <name> — <one line> -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<script src="https://kit.fontawesome.com/f8a570160d.js" crossorigin="anonymous"></script>
<style type="text/tailwindcss">
  @theme { /* paste the FULL contents of tokens.css from this skill's folder — see next section */ }
  body {
    font-family: var(--font-body);
    color: var(--color-neutral-fg);
    background: var(--color-neutral-bg);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
  }
  h1, h2, h3, h4 { font-family: var(--font-heading); }
</style>
```

- Tailwind v4 via the browser CDN. It compiles at page load. Needs a connection to open the file — accepted trade.
- **Everything in one file.** No imports, no local CSS files, no npm, no React.
- Page layout: centered container, **max-width 960px by default**, overridable with `--width`. Concepts stacked full-width down the page, one band each, generous vertical separation.
- Page header: the subject as a heading, one line on how to interact with the frames as the subheading. Nothing else.
- **Per concept, exactly three text elements**: a **heading** (number + a terse quotable name), a one-line **subheading**, and — after the live thing itself with its states — a small **references line**: `References: <a>Duolingo</a> · <a>Airbnb</a>` — the app names from the survey, each linking to its Mobbin screen. **No rationale notes, no trade-off paragraphs, no "when to use this" copy** — the live render argues for itself, and the reasoning goes in the chat hand-off instead. Make names distinct and quotable (`Inline edit · "no modal"`, `Split rail`) — the user refers to concepts by name.
- Icons: **Font Awesome via the team kit** (the second script in the scaffolding — it is the design system's own icon font, per the library's `ffActiveIcon` token). Two styles only, mirroring the two type weights: `fa-light` is the default for UI icons; `fa-solid` for emphasis — active states, filled badges, the selected item. Never `fa-regular`, `fa-thin`, or duotone. Logos use `fa-brands`. Size with text utilities, color with `currentColor` — never a hardcoded fill. No other icon source: no emoji as icons, no inline-SVG substitutes, no base64.

## Tokens — the design system source (replaces any repo survey)

Read `tokens.css` in this skill's folder (`~/.claude/skills/mobbin-exploration-team/tokens.css`) and paste its `@theme` block contents verbatim into the exploration's inline `<style>`. **Never invent a hex value where a token exists** — this is what makes the exploration look like the Sticker Mule system instead of default Tailwind. The tokens are the stickermule (orange) light theme only.

Token utilities you get for free: `bg-primary-bg`, `hover:bg-primary-bg-hover`, `text-neutral-fg-muted`, `border-neutral-border`, `rounded-xs` (4px), `h-control-sm` (38px), `shadow-card`, `text-lg` (20px, the DS scale), `font-heading`.

### mule-ui conventions (from the Figma library — follow these, they carry the system's feel)

- **Type**: headings in `font-heading` (Proxima Nova, local font with Helvetica fallback — never load a webfont), body in `font-body` at 14px (`text-sm`). Weights: regular and bold only — no medium, no semibold.
- **Buttons**: three styles — filled, outline, ghost. Bold label, `rounded-xs` (4px). Heights: `h-control-xs` 26 / `h-control-sm` 38 / `h-control-md` 56. Default intent is primary orange (`bg-primary-bg`, hover `bg-primary-bg-hover`, active `bg-primary-bg-active`, white bold text). Disabled = the `*-disabled` token (40% alpha), never a custom grey. Loading = spinner replacing the label.
- **Inputs**: white bg, `border-neutral-border` 1px, `rounded-xs`, `h-control-sm`, placeholder in `text-neutral-fg-muted`. Label sits **above** the field, 14px, `text-neutral-fg`. Error state uses `border-danger-border` + `text-danger-fg`.
- **Menus / dropdowns**: white surface, `border-neutral-border-soft`, `rounded-xs`, `shadow-overlay`, 1px `border-neutral-border-soft` dividers between rows. Hover and selected rows use `bg-secondary-weaker-bg` (light blue), not grey.
- **Surfaces**: cards are `bg-neutral-bg` + `border-neutral-border` + `shadow-card`; the muted page ground is `bg-neutral-bg-alt-soft`. Dark surfaces (tooltips, toasts) use the `neutral-stronger-*` set.
- **Links**: `text-utility-link`, hover `text-utility-link-hover`.

Where the conventions don't cover a case, extend the logic of the nearest token group; do not import an outside aesthetic.

### Refreshing the tokens

When the library changes, export variables from Figma to JSON again and run:

```
python3 ~/.claude/skills/mobbin-exploration-team/build-tokens.py <export.json>
```

It rewrites `tokens.css` (stickermule light only, legacy groups stripped). Do this only when the user asks.

## `--mobile`

Not "the desktop concepts squeezed to 390px." A mobile run asks: **what are three different ways this subject works on a phone?**

- Render each concept in a 390px stage, fixed height, so what survives the fold is directly comparable.
- Touch targets ≥44px. **No hover-only affordances.**
- Keep the primary action reachable in the thumb zone.
- Where the concept is a container bet (bottom sheet vs. push vs. inline expand), show it in its bet state — the sheet open over its dimmed parent, the row mid-swipe — so the pattern is legible on sight.
- Name the phone-specific cost of each concept in the chat hand-off: what falls below the fold, what a gesture costs in discoverability, what permanent chrome it spends.

Without `--mobile`, design desktop-first at a comfortable desktop width and don't reason about breakpoints.

## Mobbin survey (required)

Every exploration runs a Mobbin survey — it is what separates real pattern research from generic output. **If the Mobbin MCP is not connected, stop before designing anything.** Tell the user: "This skill needs Mobbin. Run `claude mcp add --scope user --transport http mobbin https://api.mobbin.com/mcp`, restart Claude Code, then authenticate via `/mcp`, and run the command again." Offer to run the `claude mcp add` command for them. Do not produce an exploration without the survey.

Run the survey **after** the subject intake, so the baseline is fixed before outside patterns enter.

- `mcp__mobbin__search_screens` (`mode: "deep"`, `limit` 6–8) — the workhorse. Query one screen or one component in plain UI language. Pass ids already seen in `exclude_screen_ids` to dig deeper. Match `platform` to the run: `"web"` by default, `"ios"` on `--mobile`.
- `mcp__mobbin__search_flows` (`limit` 2–3, same platform rule) — the only source of sequence. Use it when the subject has a before/after or an arc.
- `mcp__mobbin__search_sections` is web-only marketing sections; only for marketing-page subjects.

**Run one targeted query per concept you intend to bet on**, phrased as the pattern ("swipe to reply in a chat thread", "bottom sheet detail from a feed row"). Avoid negations and style adjectives.

**The survey is looking at the screenshots, not collecting app names.** Read measurable structure off the image and carry that into the design itself. On the page, the survey surfaces only as each concept's references line: the app names, each linking to the `mobbin_url` that informed it. Save the structural facts for the chat hand-off. Never copy markup or source assets from Mobbin — tokens and conventions still come from this skill.

If the Mobbin MCP isn't connected, continue without it — the exploration still works. Tell the user once: "For pattern research from real apps, add Mobbin: `claude mcp add --transport http mobbin https://api.mobbin.com/mcp`, restart, then authenticate via `/mcp`." Do not repeat this in later runs.

## `--fresh`

An independent take, blind to what's already been explored.

- **Do not open any existing file in the explorations folder** — not for style, not for scaffolding, not for "what did we already try".
- **Do not carry prior concepts forward,** and don't define the new set as the opposite of the last one — inverting a prior is still anchoring on it.
- **Subject intake still runs.** `--fresh` means no prior exploration, never no current-design baseline.
- Numbering works as usual. Note in the doc block that this was a fresh pass.
- Say in the hand-off that you deliberately didn't read the earlier pass, so overlap is convergence, not copying.

## Go-deeper mode

If the request points at an existing concept ("go deeper on 02 Inline edit — four more variations"), don't produce a new set of three. Hold that concept fixed and vary only the finish — spacing, weight, colour treatment, balance, composition — into the next numbered file in the same subject folder.

## Taste bar

The user rewards **clean professional UI, strong hierarchy, deliberate spacing and grouping, sleek, well balanced** — and says *"spend some time and execute it well."* What gets sent back: **too blank** (washed-out empty backdrops), **cramped** spacing, and **poor balance** (two elements crammed side by side because there was room). Give each frame room to breathe. Copy inside the frames is tight and minimal — no filler labels, no repeated words between a heading and the control beneath it.

## Hand-off

No verification step — don't start a server, don't screenshot, don't run the build. The user opens the file themselves.

The reasoning lives here, not on the page. Report the file path, then per concept, by name: the bet, the trade-off, and when you'd pick it — one or two lines each, with the structural fact from its Mobbin reference. Frame any recommendation as a **recipe rather than a winner** — the pick is usually a blend ("02's layout with 03's disclosure").
