# Strategic Report — The Agentic Brand Operating System

*A review of where Solidigm's brand context system stands, what the leading edge of the industry is doing, and where to point this project to keep the company a step ahead as agentic AI becomes the default authoring surface.*

**Author:** David Smith · **Date:** April 2026 · **Status:** Draft 1 — for discussion

> This is a strategy doc, not a roadmap. It's meant to provoke decisions about
> *what to invest in next* and *what to refuse to build*. The accompanying
> [`roadmap.md`](./roadmap.md) tracks executable line items.

---

## 1. TL;DR

Solidigm has, in the span of a few months, gone from "brand lives in a PDF and
five `colors.ts` files" to having a **codified, AI-queryable brand system** —
the kind of foundation most Fortune-500 design teams will spend the next two
years trying to build. The core thesis is right, the architecture is sound, and
the ground floor is in place.

What separates *good* from *durable* now is whether we treat the next wave —
agentic AI as the default authoring surface — as a series of feature requests
or as a forcing function. The companies that will win the agentic decade are
the ones whose brand systems are **structured for agents first and humans
second**, while still being legible and useful to humans.

This doc lays out:

- **Where we are** (§2) — an honest grade of the current stack
- **Where the leading edge is** (§3) — what Anthropic, Figma, GitHub, Shopify,
  Atlassian, and a handful of design-system shops are actually shipping
- **Where the gaps are** (§4) — including some uncomfortable ones
- **Strategic plays** (§5) — Now / Next / Later, with reasoning
- **Anti-patterns** (§6) — what we should refuse to build
- **KPIs** (§7) — how we'll know the strategy is working

The throughline: **stay simple, stay opinionated, and let agents do the
boring parts so humans get the creative parts back**.

---

## 2. State of the foundation — an honest grade

The system today has six concentric layers. Here's how each grades against
what a 2026-era enterprise brand system should look like:

| # | Layer | What we have | Grade | Why |
|---|-------|--------------|-------|-----|
| 1 | **Tokens** | W3C DTCG JSON, compiles to CSS / SCSS / TS / Tailwind / Figma; published as `@solidigm/brand-tokens` on GitHub Packages | **A** | DTCG is the right standard. Multi-format compile is the right output. NPM-distributed is the right delivery. |
| 2 | **Toolkit** | `tk-*` CSS utility classes, consumed by the site | **B+** | Works. Still hand-maintained as `docs/ui-toolkit.min.css`; should be compiled from tokens. (Already on the deferred list.) |
| 3 | **Assets** | 87 local + ~373 SharePoint files, federated through one `list_assets` manifest with category inference, fuzzy `get_asset`, Graph thumbnail URLs, server-side proxy fallback | **A−** | Federation works. Cache pre-warming + Graph `$expand=thumbnails` is current best practice. Still missing write-back. |
| 4 | **Guidelines** | 11 topic markdown files (`brand/*.md`), narrative split out of the 120-page PDF; 16 quality gates as YAML | **A** | Topic-scoped markdown is exactly the right shape for both human reading and LLM ingestion. Quality gates as YAML are durable. |
| 5 | **MCP server** | 15 tools, 8 resources, 4 prompts, 7 HTTP routes; Python FastMCP; OAuth client-credentials + delegated PKCE; cache pre-warm; CI smoke test | **A−** | This is the spine. Read-only by design. Prompts shipped (Phase 9); Sampling and Elicitation are future primitives. |
| 6 | **Skill / agent layer** | `copilot-instructions.md` (always-on), scoped `instructions/*.md`, `/brand-check` prompt, `brand-compliance` audit Skill | **A−** | Every Copilot interaction in this repo is brand-grounded by default. Skill audit emits a graded markdown report. Could go further with auto-fix workflows. |

**Overall stack grade: A−.** The bones are excellent. The gaps are mostly
about *depth in primitives we haven't yet adopted* and *write-side workflows
we deliberately deferred*, not about anything that's broken.

### Verifiable claims (so we don't fool ourselves)

- The Astro site dogfoods the system: it imports tokens from the package and
  calls the MCP at runtime for the assets browser.
- The audit Skill runs end-to-end and produces a graded markdown report;
  current site grade is **B** (11/16 pages A+).
- A 24-test Playwright suite covers the asset MCP + UI; CI runs a smoke test
  on every PR.
- The brand quality gates YAML is the *only* place certain rules
  (palette, accent ratio, trademark, heading case) live — there's no
  duplicated rule set in JS or Python.

---

## 3. Where the leading edge is

I want to be clear about what's marketing and what's actually shipped. This
section is grounded in primary sources, not analyst decks.

### 3.1 The Model Context Protocol is no longer optional

MCP (introduced by Anthropic in November 2024) is now the *de facto* standard
for AI–system integration. The 2025-06 spec defines six core primitives:

| Direction | Primitive | What it is | Solidigm status |
|-----------|-----------|-----------|-----------------|
| Server → Client | **Resources** | URIs the model can read | ✅ 8 (`brand://tokens/*`, `brand://guidelines/*`, `brand://toolkit/*`, `brand://assets/*`) |
| Server → Client | **Tools** | Functions the model can call | ✅ 15 |
| Server → Client | **Prompts** | Templated workflows the user can invoke | ✅ 4 (`brand_check`, `generate_brand_compliant_copy`, `audit_built_site`, `propose_color`) |
| Client → Server | **Sampling** | Server-initiated recursive LLM calls (e.g. for reasoning sub-tasks) | ❌ none |
| Client → Server | **Roots** | Filesystem/URI boundaries the server may operate in | n/a (read-only) |
| Client → Server | **Elicitation** | Server-initiated requests for user input mid-flow | ❌ none |

We've shipped the three server → client primitives. The remaining client → server
primitives (Sampling, Elicitation) are where the next wave of differentiation
lives — see §5.

### 3.2 What Figma did with their MCP server (June 2025)

Figma's [MCP server post](https://www.figma.com/blog/introducing-figma-mcp-server/)
is required reading for anyone building an asset/design MCP. Their core
insight, paraphrased:

> *"The context you **exclude** matters as much as what you provide. LLMs have
> finite context windows. Every token you spend on noise is a token not spent
> on signal."*

What they built (and what we should learn from):

- **Pattern metadata** — when an LLM asks about a component, return the
  *variable names, the component path in code, and the design token*, not
  pixels. This is **Code Connect**: a mapping between Figma components and
  the codebase's actual import path.
- **Screenshots are supplemental, not primary** — they're useful for
  *intent* (does this look like a hero section?) but worse than metadata for
  *spec* (what's the exact spacing?).
- **Interactivity is pseudocode** — to describe a stateful component to an
  LLM, give it a code-shaped prototype, not a description.
- **Per-tool toggles** — let consumers configure how much context each tool
  returns. The server doesn't have one global verbosity; each tool is dialed
  individually.

The Solidigm parallel: **our `list_assets` returns names, categories, and
URLs — but it doesn't yet return the Tailwind class, CSS custom property, or
component path that *uses* that asset**. That's the next gap to close (§5).

### 3.3 What other design-system leaders are doing

Patterns I've seen converge across Shopify Polaris, Atlassian Design System,
GitHub Primer, Adobe Spectrum, IBM Carbon, and Salesforce Lightning in the
last 12 months:

1. **Tokens-as-API** — every system now publishes a tokens NPM package and a
   JSON-over-HTTP endpoint. We have this.
2. **Topic-scoped guidelines** — nobody ships a 120-page PDF anymore; it's
   topic markdown that links downward. We have this.
3. **Quality gates as code** — Carbon and Polaris both publish ESLint rule
   packs *and* runtime validators. We have ESLint + the validation MCP tool.
4. **AI-aware system prompts** — Atlassian and Shopify both ship "drop-in
   system prompts" for their design system. We have `get_brand_system_prompt`.
5. **Audit-as-a-service** — Polaris ships a CLI that audits a built site
   against the design system. We have the `brand-compliance` Skill.
6. **Code Connect / component-path mapping** — Figma (and now Polaris) map
   design components to code import paths. **We don't have this yet.** This
   is the biggest competitive gap.
7. **Bi-directional Figma sync** — every leading system is wiring this up;
   currently one-way (code → Figma) for everyone, including Solidigm.
8. **Skill packs / Slash commands** — GitHub, Atlassian, and Anthropic all
   ship reusable agent workflows as installable packs. We have `/brand-check`
   and the audit Skill. **The pattern of distributing Skills is converging**
   — investing here looks correct.

### 3.4 What's coming that we should plan for

Reading current Anthropic, OpenAI, GitHub, and Figma roadmaps + the MCP spec:

- **Skills become first-class artifacts.** Anthropic's recent push around
  Claude Skills, GitHub's Copilot Skills, and Cursor's commands all point the
  same way: agent workflows packaged as files, version-controlled, shareable
  across teams. We're ahead here. Stay ahead.
- **Multi-agent / agent-to-agent.** Brand validation is going to be invoked
  not just by humans typing in IDEs, but by *other agents* mid-task. A
  Salesforce agent generating an outreach email will call our
  `validate_brand_output` before sending. The MCP server needs to keep being
  the source of truth, but it also needs to be **reachable from outside the
  IDE** (HTTP, auth-gated, audit-logged).
- **Generative imagery becomes a brand-compliance problem.** When marketing
  generates a hero image with DALL·E or Midjourney, "is this on-brand?" is
  the first question. CLIP-style embedding similarity to the approved
  illustration set is becoming the standard answer. We don't have this.
- **Token spaces explode.** Sound tokens, voice tokens (LLM
  tone), and density tokens are all becoming part of the design system. We
  now have 10 categories (color, type, space, breakpoints, radius, shape,
  motion, elevation, semantic, icons). The schema is ready (DTCG); remaining
  gaps are sound, voice, and density.
- **Telemetry is table stakes.** The next conversation in every brand-system
  team is "which tools are agents calling, which guidelines are getting
  cited, which rules are getting violated?". If we can't answer those, we
  can't prioritize.
- **Provenance / C2PA on AI-generated content.** Increasing regulatory
  pressure (EU AI Act, US executive orders) requires AI-generated marketing
  imagery to carry cryptographic provenance metadata. Adobe, Microsoft, and
  the BBC have all shipped C2PA. We don't address this; we will need to.

---

## 4. The honest gap list

These are the gaps that, if we don't address them in the next 6–12 months,
will turn into liabilities.

### 4.1 No Code Connect–style mapping (high impact)

When an agent asks "give me the hero illustration for the HPC use case,"
`list_assets` returns a filename and a URL. It doesn't return:

- the Astro/React component path that already uses it
- the `tk-*` CSS class that's the canonical wrapper
- the design token(s) that color it
- whether there's an existing variant for dark mode

This is the single biggest "agent asks the right question, gets a half-useful
answer" problem we have today. Closing it transforms the MCP from a *catalog*
into a *system map*.

### 4.2 No write-side workflows (medium impact, high political cost)

Every change to the brand system today is a human PR. That's safe, but it
means:

- Designers can't propose a new shade from Figma without context-switching to GitHub.
- Marketers can't request a new illustration without filing a Jira ticket that gets ignored.
- Agents can't auto-fix violations they detect — they can only flag them.

The right answer is *not* "let agents YOLO into the brand repo." The right
answer is **agent-mediated change requests** with structured proposals,
approval gates, and audit logs. This is a 2026 problem, not a 2027 problem.

### 4.3 No telemetry (medium impact, low cost)

We don't know:

- which tools agents call most (and which we could deprecate)
- which guidelines are most-read (and which need rewriting)
- which quality-gate rules trigger most violations (and which need clarification)
- which assets are most-downloaded (and which are dead weight)

A tiny amount of structured logging on the MCP — written to a SQLite/Parquet
file behind a feature flag — would unlock prioritization for the next two
phases of work. We should build this before we build anything else
ambitious.

### 4.4 No image / generative-content brand compliance (high future impact)

The validation gates today work on text, hex codes, and font names. They do
*not* work on:

- AI-generated images (is the composition on-brand? is the color palette
  approximated? is there a fake person? is the "purple" the right purple?)
- Real photography (is it in the approved illustration style?)
- Video / motion content (does the easing match brand motion tokens?)

CLIP embeddings + a vector DB of approved imagery is the industry-standard
answer. It's a 2-week build, not a 2-quarter build, and it punches well above
its weight.

### 4.5 No voice / density tokens

Motion tokens shipped in Phase 10 (10 categories total). Remaining gaps:
voice tokens (LLM tone calibration) and density tokens. DTCG supports them;
the schema is ready. The narrative (`brand/`) doesn't yet have authoritative
content for them, so we shouldn't fake tokens that don't exist. This is a
flag for the brand team: **the schema is waiting on the policy**, not the
other way around.

### 4.6 Single-instance MCP, no Redis, no horizontal scale

Today the MCP runs on one host with in-memory caching. Fine for dev, fine
for VPN-internal use. Not fine when:

- the marketing automation team starts calling it from cron
- partner-facing chatbots embed it
- a multi-region deployment is desired

This is plumbing — boring, important, deferred.

### 4.7 No provenance metadata on AI-generated content

If we tell the world "we're using AI responsibly," our outputs need to be
verifiably AI-generated (or verifiably not). C2PA / Content Credentials is
the standard. Microsoft, Adobe, and TikTok all stamp their AI outputs.
Solidigm should plan to.

---

## 5. Strategic plays — Now / Next / Later

The framing principle: **simple but effective** beats *complete but
unmaintained* every time. Each play below has a clear "smallest version that
ships" so we never let ambition outrun delivery.

### 🟢 NOW (next 6 weeks)

These are high-leverage, low-cost plays where the foundation already does
80% of the work.

#### N1. ~~Add MCP **Prompts**~~ ✅ Shipped (Phase 9)

Four prompts shipped as MCP `@mcp.prompt()`: `brand_check`,
`generate_brand_compliant_copy`, `audit_built_site`, `propose_color`.
Available across every MCP client.

#### N2. ~~Implement **Code Connect for assets**~~ ✅ Shipped (Phase 9)

Every asset record now includes `code_paths` — an array of every file in the
repo that references it. Built by `scripts/build-asset-index.mjs`, consumed
by the MCP's `_build_asset_record()` composer.

#### N3. ~~Ship **telemetry behind a flag**~~ ✅ Shipped (Phase 9)

JSONL telemetry logs every tool call. `GET /api/stats` aggregates last
30 days. `/admin/stats` page visualizes top tools, colors, and headline
metrics. Controlled by `BRAND_MCP_TELEMETRY_ENABLED=1` (default off).

#### N4. ~~Write **`AGENTS.md`** at the repo root~~ ✅ Shipped (Phase 9)

Created `/AGENTS.md` — identity, MCP tool table, no-go zones, validation
flow, PR checklist. Cross-linked from `.github/copilot-instructions.md`
and root `README.md`.

#### N5. ~~**Auto-fix mode** in the audit Skill~~ ✅ Shipped (Phase 9)

`audit-pages.mjs` now supports `--fix` (preview patch) and `--apply` (apply
auto-class fixes). Handles trademark, off-palette hex, and headline-case
violations.

### 🟡 NEXT (3–6 months)

Larger investments where the foundation is mostly there but the surface area
is bigger.

#### X1. **Image brand compliance via embeddings**

A vector DB (LanceDB or sqlite-vec, both file-based, zero ops) seeded with
the embeddings of every approved illustration / photo / logo. New tool:
`validate_brand_image(url_or_bytes)` returns:

- nearest approved asset + similarity
- dominant color extraction → palette compliance check
- "is this AI-generated?" probability

Bolt onto the existing `validate_brand_output` so agents validate text *and*
image in one call.

**Tech:** OpenAI CLIP or open-source SigLIP for embeddings, ~500MB model,
runs on the same host as the MCP. No new infra.

#### X2. **Voice tokens**

Brand team writes `brand/voice.md`. We add a `voice` collection to
`tokens/`. The validator gets a `check: voice_alignment` rule.
Motion tokens already shipped (Phase 10 — `tokens/motion.json`,
`/tokens/motion` page, `get_motion` tool).

**Why next, not now:** the schema is trivial — the *content* is what matters,
and that's a brand-team decision, not an engineering one. We should put it
on the brand team's roadmap, not block on it.

#### X3. **Bi-directional Figma sync via Figma plugin**

A Figma plugin that lets a designer:

- propose a token change (writes a JSON proposal)
- propose a new asset upload (writes a SharePoint upload + a PR with the
  manifest entry)
- audit a frame against quality gates (calls `/api/validate`)

The plugin and the MCP share the validator code (or the plugin calls
`/api/validate`). This closes the design-→-code-→-design loop.

#### X4. **Multi-tenant MCP deployment**

Run the MCP on a Solidigm internal VM with TLS, Entra SSO gate, audit log
to Azure Monitor. Publish the URL internally; let any team in the company
point any agent at it. This is the "make it boringly available" play.

#### X5. **Skill marketplace inside the repo**

Add 5–10 more skills under `.github/skills/`:

- `copy-rewrite` — take draft marketing copy, return brand-compliant version
- `deck-audit` — audit a Google Slides / PPT export against gates
- `asset-search-fuzzy` — semantic search over assets via embeddings
- `palette-extract` — extract dominant colors from an image, check palette
- `figma-frame-audit` — call Figma MCP + ours, cross-validate

Each is ~150 lines. They become Solidigm's library of agent workflows.

### 🔴 LATER (6–12 months)

Bigger bets that depend on earlier plays paying off.

#### L1. **Agent-mediated brand evolution**

When marketing wants a new accent color, an agent (a) drafts the proposal
markdown, (b) generates mock-ups using the proposed color, (c) runs them
through validators, (d) opens a PR with the diff and a one-page rationale.
Brand team approves or rejects. The brand becomes a **conversational, version-
controlled artifact**, not a set of decrees.

#### L2. **C2PA / Content Credentials integration**

Every AI-generated asset Solidigm publishes carries cryptographic provenance
metadata. Required for: marketing imagery, product render variants, social
content. Not required for: internal use, design-time exploration.

#### L3. **Cross-org federation**

Partner co-marketing produces lots of "is this co-branded asset on-brand?"
questions. Expose a public, tightly-scoped subset of the MCP to approved
partners (Dell, HP, AWS) so their agents can auto-validate co-branded
collateral against Solidigm gates.

#### L4. **Localized brand validation**

The validators today assume English. A globalized version:

- validates Mandarin / Japanese / German product names against locale-
  specific naming rules
- validates locale-specific typography (Noto Sans regional variants)
- understands locale-specific tone (German formal `Sie`, Japanese `keigo`)

This is *significant* work. Worth deferring until we have telemetry showing
non-English usage.

---

## 6. Anti-patterns — what we should refuse to build

Equally important. The fastest way to ruin a system this clean is to bolt on
things that look like progress but actually add maintenance debt.

1. **A second source of truth.** Nobody gets to spin up a parallel "brand
   API" outside this repo. Every additional consumer reads from the MCP or
   imports `@solidigm/brand-tokens`.

2. **A custom UI for editing brand content.** GitHub's PR flow is the editor.
   A bespoke "brand admin" web app is a 2027 distraction with 2030 maintenance.

3. **An LLM in the loop for things that don't need one.** `get_color` should
   never call an LLM — it's a JSON lookup. Same for `get_logo`, `list_assets`.
   Reserve LLM calls for the validators, the rewrites, and the proposals.

4. **A "brand AI" chatbot product.** The world doesn't need another chat UI.
   The tools already work in Claude, Cursor, Copilot, ChatGPT. Investing in
   our own UI duplicates work and underperforms specialized clients.

5. **Pre-emptive scaling.** Don't move to Redis / Kubernetes / a queue
   because *maybe* someday. Move when telemetry shows the load.

6. **More than ~25 quality gates.** We have 16. Past ~25, the rules
   contradict each other and agents get stuck in fix loops. Pruning matters
   more than adding.

7. **Brand voice classifiers we can't explain.** A "brand voice score: 73%"
   is a number nobody trusts. A *list of specific lines that don't match the
   voice rules* is a number people fix. Stay on the side of explainability.

---

## 7. KPIs — how we'll know this is working

Concrete, falsifiable, measurable inside 12 months. Some require the
telemetry play (N3) to land first.

### Adoption

- **Internal MCP traffic** — number of distinct agent IDs / week calling the
  server. Target: **>10 distinct agents within 6 months of internal release.**
- **NPM token package installs** — distinct repos pulling
  `@solidigm/brand-tokens`. Target: **all 5 primary marketing/web repos
  within 3 months.**

### Quality

- **Site brand grade** — current site grade is **B**; target is **A within
  one quarter** of N5 (auto-fix) shipping.
- **Median time-to-fix** for a flagged brand violation. Target: **<1 day
  with auto-fix; <1 week without.** Should drop sharply when N5 lands.

### Velocity

- **New brand surface onboarding time.** Target: **a new microsite is on
  brand on day one** without manual brand-team review. Measured via
  audit-grade on first deploy.
- **Token change propagation time.** From PR-merged to consumer-rebuilt:
  target **<24 hours** end to end (NPM publish + downstream rebuild).

### Coverage

- **% of brand-facing PRs reviewed by `/brand-check`.** Target: **>80%.**
  Requires a GitHub Action that auto-comments on every PR touching
  `.astro/.css/.tsx/.md`.
- **% of brand assets with `code_path` populated.** Target: **>60%** after
  N2 ships.

### Trust

- **Number of validator false-positives reported per quarter.** Target:
  **<3.** False positives are how rule sets lose credibility — track them
  ruthlessly.

---

## 8. Why "simple but effective" is the right strategy

The user's instinct here was correct: keep this project simple. Simple
**doesn't** mean basic. Simple means **opinionated** — every decision is
reviewable in one paragraph, every layer is replaceable, and every consumer
can read the source if they want to.

The biggest risk to this project isn't under-investing. It's over-investing
into a custom platform that competes with the open ecosystem. Every place
we've leaned on a standard (DTCG tokens, MCP, W3C Custom Properties, NPM,
markdown, YAML) is a place we get the ecosystem's improvements for free.
Every place we've invented (the topic-scoped `brand/` markdown, the
quality-gates YAML, the Skills layer wiring) is a place where the invention
is **clearly thinner than the underlying standard** and could be replaced if
something better emerges.

That's the durable shape: **thin, opinionated wrappers over open standards,
exposed through a single backend, dogfooded on a public site, audited by
the same agents that will consume it.**

If we keep that shape, the company gets a springboard. Every new project,
deck, microsite, partner asset, customer email, sales motion, AI agent —
starts from "what's our purple?" being a tool call, not a meeting.

That's the win. The rest is execution.

---

## 9. Decisions I'm asking for

To unblock the next 6 weeks of work:

1. **Greenlight N1–N5** (Now plays) as the next sprint's content. Cost: ~3
   engineering weeks. Output: 4 new MCP prompts, asset code-path index,
   telemetry, `AGENTS.md`, audit auto-fix.
2. **Sponsor the brand team to write `brand/motion.md` and `brand/voice.md`.**
   Tokens are blocked on policy, not engineering.
3. **Confirm appetite for X3 (Figma plugin) in Q3.** It's the largest of the
   "Next" investments and needs design-team buy-in before we start.
4. **Defer L1–L4 explicitly.** Not committing to them this year is a decision;
   say it out loud so we don't drift.
5. **Name an owner.** This system has been built by one engineer with help.
   To survive past the founder, it needs a maintainer of record. Assign one.

---

## Appendix A — primary sources

- [Model Context Protocol spec, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [Anthropic — Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [Figma — Introducing our MCP server (June 2025)](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [W3C Design Tokens Community Group — DTCG format](https://www.designtokens.org/)
- [C2PA — Content Authenticity specification](https://c2pa.org/)
- This repo: [`README.md`](../README.md), [`docs/architecture.md`](./architecture.md),
  [`docs/roadmap.md`](./roadmap.md),
  [`docs/one-stop-shop-brand-system.md`](./one-stop-shop-brand-system.md),
  [`brand/quality-gates.yaml`](../brand/quality-gates.yaml),
  [`brand_mcp/server.py`](../brand_mcp/server.py).

## Appendix B — companies referenced and what they ship

| Company | What they ship that's relevant | What we should learn |
|---------|--------------------------------|----------------------|
| Anthropic (MCP, Claude Skills) | The protocol; reusable Skill artifacts | We're already on MCP; lean further into Skills as the distribution unit |
| Figma (MCP server, Code Connect) | Design-context-as-MCP; component → code mapping | Adopt Code Connect-shaped thinking for our assets (N2) |
| GitHub (Copilot Skills, AGENTS.md) | Skill packaging; convention for agent-facing docs | Ship `AGENTS.md` (N4); keep our Skills layer aligned with their conventions |
| Shopify Polaris | Tokens NPM, ESLint pack, audit CLI | We have token NPM + ESLint; close the audit-CLI loop with N5 |
| Atlassian Design System | Drop-in system prompts, topic markdown | We have both; track their evolution |
| Adobe Spectrum | Multi-platform tokens, motion + density tokens | Plan motion & density into our token schema (X2) |
| IBM Carbon | Quality gates, contribution playbooks | We have gates; copy their contribution playbook style |
| Microsoft / BBC / Adobe (C2PA) | Provenance metadata on AI-generated content | Plan for L2 within 12 months |

---

*— David Smith, Solidigm · April 2026*
