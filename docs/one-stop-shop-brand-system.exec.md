# One-Stop-Shop Brand System — Executive Summary

*A one-page brief. Full essay: [one-stop-shop-brand-system.md](./one-stop-shop-brand-system.md)*

## The problem

Every company's brand lives in 5-6 places at once: a PDF, a Figma library, a Confluence page, a handful of `colors.ts` files, a Slack screenshot. Each is plausibly "correct." None agrees. The purple drifts, the trademark drifts, the headlines drift, and every new surface — microsite, deck, chatbot, partner portal — re-litigates the basics.

The cost is invisible but compounding: every rebrand propagates at the speed of human attention, and every AI tool that comes online hallucinates when asked about the brand.

## The thesis

A modern brand system is **a codebase, not a document library.** Inside it, six concentric layers serve every consumer with zero duplication:

| # | Layer | What it is | Who consumes it |
|---|-------|-----------|-----------------|
| 1 | **Tokens** | W3C DTCG JSON — colors, typography, spacing | Build scripts, Figma, engineers |
| 2 | **Toolkit** | CSS utilities & components built from tokens | Web engineers |
| 3 | **Assets** | Logos, illustrations, iconography | Designers, marketers, partners |
| 4 | **Guidelines** | Topic-scoped markdown (voice, logo, color, do-nots) | Humans, LLMs, brand briefs |
| 5 | **MCP** | Unified API — 15 tools, 8 resources, 4 prompts | AI agents, site, internal tools |
| 6 | **Skills** | On-demand workflows (audit, validate, system prompt) | Every developer, every CI run, every LLM |

Each outer layer is built from the ones beneath it. **One PR to layer 1 propagates to all six.**

## What "AI-native" actually means

AI agents are a first-class consumer, not a bolt-on.

- **MCP is the compiler** — every brand question is a tool call. No hallucinated hex values, fonts, or trademark symbols.
- **Skills are the linter** — LLMs validate drafts before shipping them. Same loop engineers run with ESLint.
- **Tokens are the contract** — when they change, NPM, Figma, the site, the MCP, and the Skills all move together.

## ROI

| Investment | Return |
|------------|--------|
| Weeks of one-time engineering | One PR propagates everywhere — npm, Figma, site, MCP, CI all move together |
| Social discipline — no more backdoor `colors.ts` | AI stops hallucinating brand values |
| One quality-gates YAML | Pre-release audit produces a letter-graded report with per-page findings |
| Tokens imported, not copied | New surfaces onboard in hours, on-brand day one |

## What Solidigm has today

- **Tokens** — `tokens/*.json`, published as `@solidigm/brand-tokens` on GitHub Packages
- **Toolkit** — CSS utility library (`tk-*` classes), consumed by the site
- **Assets** — 87 local + 373 SharePoint files, federated through one manifest
- **Guidelines** — 11 topic markdown files under `brand/`, 16 quality gates in YAML
- **MCP** — 15 tools, 8 resources, 4 prompts, 7 HTTP routes — Python FastMCP on `:8080`
- **Skills** — `copilot-instructions.md` (always-on), `solidigm-brand.instructions.md` (scoped), `/brand-check` prompt, `brand-compliance` audit Skill
- **Audit** — Current site grade: **B** (11/16 pages A+, 5 pages with 1-5 hex-palette violations, all on pages that intentionally display off-brand colors as examples)

## What's next

- Write-back tools (upload assets, propose token changes, approval-gated)
- Figma round-trip (design → PR)
- Motion tokens + voice model
- Localization (i18n layer over guidelines + rules)
- Usage telemetry

## Steal this — minimum viable version, ~6 weeks with two engineers

1. W3C DTCG tokens in a monorepo.
2. Build script that compiles to CSS/SCSS/TS/Tailwind/Figma.
3. FastMCP server with 5 tools: `get_design_tokens`, `get_color`, `get_brand_guidelines`, `list_assets`, `validate_brand_output`.
4. Quality-gates YAML with ≤ 20 mechanical rules (palette, fonts, trademark, heading case, accent ratio).
5. Copilot Skill that audits a built site, emits a graded markdown report. Report-only first; promote to CI gate after baseline is clean.
6. Dogfood — the docs site must import the token package and call the MCP. If it can't, your consumers won't either.

**Day one after shipping:** agents, engineers, designers, and marketers are on-brand by default. Every commit to layer 1 propagates to every surface in the company.

---

*— David Smith, Solidigm · April 2026*
