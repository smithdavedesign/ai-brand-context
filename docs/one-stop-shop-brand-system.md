# The One-Stop-Shop Brand System

*An opinionated take on why a modern company's brand belongs in one repo, one backend, and six concentric layers — and what it costs, delivers, and enables when AI agents are first-class consumers.*

---

> **Executive summary** — [one-page TL;DR](./one-stop-shop-brand-system.exec.md)

---

## 1. The problem: brand sprawl is the default

Every company I've worked with has the same pattern. The brand "lives" in five or six places at once, none of them authoritative, all of them quietly drifting:

- A **PDF** from 2022 in a SharePoint folder, cited by marketing.
- A **Figma library** that designers trust — but its tokens haven't been re-exported since Q1.
- A **Confluence page** written by the last person who cared, now ~18 months stale.
- A **`colors.ts` file** in the marketing site repo, copy-pasted to four other repos.
- A **screenshot** in a pinned Slack message that the sales team keeps sending to partners.
- A **Zeplin / Abstract / Frontify** tenant someone bought a license for three years ago.

Each of these is plausibly "correct." None of them agrees. The purple is `#4F00B5` in the PDF, `#4f00b5` in Figma, `#5000B3` in that one `colors.ts`, and "close enough" in the Slack screenshot. The trademark is `™` in the guidelines and `®` everywhere else. The headlines are title case in the deck template and `TEXT-TRANSFORM: UPPERCASE` in CSS. This isn't anyone's fault. It's the entropy of not having a single source of truth that **all six personas** — executive, marketer, designer, engineer, partner, and (now) AI agent — can consume identically.

The cost compounds. Every new surface (a microsite, a pitch deck, a conference booth, a chatbot) re-litigates "what's our purple?" Every rebrand propagates at the speed of human attention. Every AI tool that comes online — and there will be more of them — hallucinates when asked, because there's no authoritative endpoint to ground it.

## 2. The thesis: six concentric layers, one repo, one backend

A modern brand system should be **a codebase, not a document library**. Inside that codebase, everything a consumer could want lives in six concentric layers, each wrapping the previous:

```
                    ┌────────────────────────────────┐
                    │      6. Skills / Agents        │  Copilot, CI, LLMs
                    │   ┌──────────────────────┐     │
                    │   │   5. MCP Server      │     │  Unified API
                    │   │ ┌──────────────────┐ │     │
                    │   │ │ 4. Guidelines    │ │     │  Narrative rules
                    │   │ │┌────────────────┐│ │     │
                    │   │ ││ 3. Assets      ││ │     │  Logos, illustrations, docs
                    │   │ ││┌──────────────┐││ │     │
                    │   │ │││ 2. Toolkit   │││ │     │  CSS / components
                    │   │ │││┌────────────┐│││ │     │
                    │   │ ││││ 1. Tokens  ││││ │     │  Primitives (colors, type, spacing)
                    │   │ │││└────────────┘│││ │     │
                    │   │ ││└──────────────┘││ │     │
                    │   │ │└────────────────┘│ │     │
                    │   │ └──────────────────┘ │     │
                    │   └──────────────────────┘     │
                    └────────────────────────────────┘
```

Every outer layer is built from the layers beneath it. Every consumer enters at the outermost layer appropriate to them and reaches in as deep as they need.

### Layer 1 — Tokens (the primitives)

W3C DTCG JSON. Colors, typography, spacing, motion. No opinions, no composition — just the atomic values. **Who consumes this**: build scripts (NPM, Figma sync), design tool plugins, advanced engineers. Compiled to CSS custom properties, SCSS, TypeScript, Tailwind preset, and Figma Token Studio format — all from one source.

### Layer 2 — Toolkit (the compositions)

CSS utility classes and component primitives. `tk-btn`, `tk-card`, `tk-type-hero`. Built from tokens only; no raw hex or pixel values allowed. **Who consumes this**: web engineers. They import one CSS file and get the whole system, already wired to tokens.

### Layer 3 — Assets (the binary artifacts)

Logos (variant × color × format), illustrations, iconography, source documents. Organized in a predictable hierarchy and referenced by a manifest. **Who consumes this**: designers, marketers, partner enablement. Served both as files-on-disk (local, fast) and as a federated view of the SharePoint / DAM brand library (complete, authoritative).

### Layer 4 — Guidelines (the narrative)

Topic-scoped markdown: `brand.md`, `color.md`, `typography.md`, `voice.md`, `do-nots.md`, `generative-ai.md`. One file per topic; every file is short enough to read end-to-end. Not a 120-page PDF. **Who consumes this**: humans reading, humans writing briefs, and — critically — AI agents assembling context.

### Layer 5 — MCP (the unified API)

A single backend service that exposes layers 1-4 as tools and resources over the Model Context Protocol. One URL, 15 tools, 8 resources, 4 prompts: `get_design_tokens`, `get_color`, `get_spacing`, `get_breakpoints`, `get_motion`, `get_icon`, `get_brand_guidelines`, `get_ui_toolkit_class`, `list_assets`, `get_asset`, `get_logo`, `search_brand_source_documents`, `get_brand_context`, `get_brand_system_prompt`, `validate_brand_output`. **Who consumes this**: AI agents (Claude, Cursor, Copilot, ChatGPT), the public documentation site, internal tools, downstream services. The MCP is the compiler of the brand system — it takes the source layers and emits whatever the consumer needs.

### Layer 6 — Skills / agents (the workflows)

Reusable, shareable Copilot Skills, prompts, and file-instructions that sit on top of the MCP and give agents opinionated entry points. A `brand-compliance` Skill that audits a built site. A `/brand-check` prompt that validates any file. A `solidigm-brand.instructions.md` that enforces the rules every time a `.astro` or `.css` file is opened. **Who consumes this**: every developer in the org, every CI run, every LLM call.

## 3. What "AI-native" actually means

"AI-native" is the current hype adjective for everything, which means it means nothing. In the context of a brand system, it has a precise definition: **the AI is a first-class consumer, not a bolted-on feature.**

Concretely:

- **The MCP is the compiler.** An LLM should never be asked "what's Solidigm's purple?" and have to guess. It should call `get_color("solidigm purple")` and get `#4f00b5` with context ("Primary brand color — lead with this"). The canonical value is one tool call away.
- **The Skills are the linter.** Before an LLM emits a hero component, it should call `validate_brand_output` on its draft. If the draft contains `#ff0000` or `Comic Sans`, validation fails, the LLM retries with approved values, validation passes. This is the same loop a human developer runs with ESLint.
- **The site is the preview.** The public documentation site is the eyes-on rendering of what the MCP says is true. When they disagree, one of them is wrong and it's fixed in the same PR.
- **The tokens are the contract.** Any agent, any tool, any human, reads the same tokens. Every surface is derived from them. When tokens change, the NPM package, the Figma library, the MCP response, and the Skill validators all move together in one commit.

This changes the economics of brand work. Instead of "publish guidelines, hope people read them, police violations after the fact," you get **per-keystroke brand enforcement** at the authoring surface, fact-checked by the same source that the CEO's deck is built from.

## 4. Cost-to-benefit

### Cost

- **Setup** — a few weeks of engineering, once. Decide the token schema, pick the MCP framework, wire one CI gate.
- **Maintenance** — one PR per brand change. The PR updates tokens; everything downstream (NPM, Figma, site, MCP responses, Skill rules) follows automatically.
- **Discipline** — no more backdoor `colors.ts` files in product repos. Everyone imports from the token package or calls the MCP. This is the hardest part, and it's social, not technical.

### Benefit

- **One commit propagates everywhere.** Change a hex, push, merge. NPM consumers rebuild with the new value; the Figma library updates on the next sync; the MCP returns the new value to every agent starting right now; the audit Skill immediately catches the old value anywhere it's still hard-coded.
- **AI stops hallucinating.** Every brand question has a tool call, which means every answer is grounded. `get_color` is cheaper than an LLM token by three orders of magnitude and is always correct.
- **The audit is evidence.** Before a release, run the `brand-compliance` Skill. Get a report with a letter grade and per-page findings. Ship with confidence, or defer with a list of specific fixes.
- **New surfaces onboard in hours, not weeks.** A new microsite, a new partner portal, a new chatbot — point it at the MCP and the token package. Day one, it's on-brand.

## 5. What's still missing (from Solidigm's current stack)

Honesty section. This repo is strong on reads. It is deliberately thin on writes:

- **Write-back tools.** The MCP is read-only. Uploading a new asset to SharePoint, or proposing a new color variant, still requires a human PR. This is a safety feature right now, but long-term it should be an agent-mediated workflow with approval gates.
- **Figma round-trip.** Tokens flow from code → Figma. They don't flow back. A designer experimenting with a new shade in Figma can't open a PR from the design tool. The missing half is a Figma plugin that writes into `tokens/` and opens a PR.
- **Motion and voice as enforceable systems.** We have motion guidance as narrative markdown. We don't have motion tokens (durations, easings) or a voice model fine-tuned on Solidigm copy. Next phase.
- **Localization.** All current copy is English. A real global system needs a i18n layer over the guidelines and a locale-scoped variant of `validate_brand_output` that knows Mandarin product naming rules differ from English ones.
- **Usage analytics.** We don't know which tools agents call most often, which pages get audited, which guidelines are cited in PRs. Telemetry is the next maturity step.

These are listed so readers stealing this design know what to budget for version 2.

## 6. Steal this — a starter kit

If you're standing this up at your company, the minimum viable version is:

1. **Pick a token schema.** W3C DTCG is the right answer. Don't reinvent.
2. **Stand up a monorepo** with `tokens/`, `brand/` (narrative markdown + data), `site/` (Astro or similar), and `mcp_server/` (Python + FastMCP or equivalent).
3. **Write a build script** that compiles tokens to CSS/SCSS/TS/Tailwind/Figma.
4. **Write the MCP tools in this order**: `get_design_tokens` → `get_color` → `get_brand_guidelines` → `list_assets` → `validate_brand_output`. The last one is where the magic lives.
5. **Write a quality-gates YAML** with ≤ 20 rules. Don't try to enforce voice and tone algorithmically at first — enforce the mechanical rules (palette, typography, trademark, heading case, accent ratio). Voice comes later with a tuned model.
6. **Add a Copilot Skill** that runs a site audit and emits a markdown report. Report-only at first. Promote to a CI gate once your baseline is clean.
7. **Dogfood it.** The documentation site should import from the token package and call the MCP. If it can't, your consumers won't either.
8. **Publicize the MCP URL and the NPM registry inside the company**. The minute someone can `npm install @yourco/brand-tokens` or point Claude at `brand-mcp.internal.yourco.com`, adoption explodes.

Everything above can be built by a team of two in six weeks. The ROI shows up the first time a new microsite is on-brand on day one without a single conversation with the brand team.

## 7. Closing

The most valuable thing in a brand is consistency. The most expensive thing about consistency is discipline. A one-stop-shop brand system collapses that cost by making "the right thing to do" and "the easy thing to do" the same action: call a tool, import a token, read a markdown file. Humans do it because it's convenient. Machines do it because it's structured. Everyone meets at the same source.

Build it once. Maintain it in one place. Every surface, every consumer, every commit — on-brand by default.

---

*— David Smith, Solidigm · April 2026*

*Related reading in this repo: [architecture](./architecture.md) · [roadmap](./roadmap.md) · [brand foundation](../brand/brand.md) · [quality gates](../brand/quality-gates.yaml)*
