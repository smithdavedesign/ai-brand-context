# AI Brand Context System — Product Requirements Document

**Version:** 1.0 | **Status:** Draft | **Owner:** Engineering | **Date:** April 2025

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Non-Goals](#3-goals--non-goals)
4. [Users & Stakeholders](#4-users--stakeholders)
5. [System Architecture](#5-system-architecture)
6. [Feature Requirements](#6-feature-requirements)
7. [AI Tool Integrations](#7-ai-tool-integrations)
8. [Technical Requirements](#8-technical-requirements)
9. [Phased Roadmap](#9-phased-roadmap)
10. [Success Metrics](#10-success-metrics)
11. [Risks & Mitigations](#11-risks--mitigations)
12. [Open Questions](#12-open-questions)
13. [Appendix](#appendix--glossary)

---

## 1. Executive Summary

Design and engineering teams currently lack a reliable, machine-readable way to share brand and UI standards with AI tools. The result is inconsistent output, off-brand components, repeated manual correction, and AI-generated work that cannot safely ship without significant human review.

The AI Brand Context System solves this by creating a single source of truth for brand intelligence — structured, versioned, and queryable by both humans and AI agents. It consists of three integrated layers: a curated content package, a composer API that assembles task-scoped context payloads, and a public-facing documentation site.

> **Core Value Proposition:** Any AI tool — Claude, Cursor, Copilot, or a Figma plugin — can receive a single URL or API response containing everything it needs to produce on-brand, production-ready output for a specific task. No zip files. No copy-paste. No drift.

---

## 2. Problem Statement

### 2.1 Current State

AI tools are embedded in the daily workflow of designers and developers but operate without reliable brand context, leading to:

- Components that violate spacing, typography, or color standards
- Platform-specific rules (AEM field limits, React prop conventions) ignored
- Inconsistent application of "do not" rules across teams
- Significant manual review overhead before any AI output can ship
- Context re-entry every session — no persistent brand memory

### 2.2 Root Cause

Brand guidelines exist for humans. They are written in prose, stored in PDFs, and designed to be read — not ingested by language models. Design tokens may exist in Figma or a spreadsheet but are not machine-readable in context. There is no structured interface between the brand system and AI tools.

### 2.3 Impact by Stakeholder

| Stakeholder | Pain Point | Estimated Impact |
|---|---|---|
| Designers | AI tools ignore brand rules; manual correction required | 30–50% rework rate on AI-generated UI |
| Developers | No reliable component context for Cursor / Copilot | Inconsistent code patterns across projects |
| Brand / Marketing | Off-brand output reaches review too late | Brand dilution risk per launch |
| External agencies | No self-serve access to standards; email requests | Delays of days to weeks per project |

---

## 3. Goals & Non-Goals

### 3.1 Goals

1. Provide a single, authoritative source of brand context accessible to humans and AI agents
2. Enable any AI tool (Claude, Cursor, Copilot, Figma AI) to produce on-brand output without manual context setup
3. Allow task-scoped context delivery — return only what is relevant for a given platform and task type
4. Support non-technical stakeholders through a browsable documentation site built from the same source
5. Establish a versioned, maintainable content structure owned by the engineering team
6. Reduce AI-generated rework rate by providing enforceable design tokens and quality gates

### 3.2 Non-Goals (v1)

- Real-time Figma token sync (future integration, not v1)
- User authentication or role-based access control
- AI model fine-tuning or embeddings pipeline
- Automated quality gate enforcement (v1 provides the spec; linting is a future layer)
- Multi-brand or white-label support
- CMS authoring interface for non-technical content editors

---

## 4. Users & Stakeholders

### 4.1 Primary Users

**AI Agents & Tools**
- Who: Claude API, Cursor, Copilot, Figma AI
- Needs: Machine-readable context payloads via API. Task-scoped, flat, pre-composed. Never more than needed.

**Developers**
- Who: Frontend engineers using Cursor / Copilot, API integrators
- Needs: API documentation, platform-specific context, tokens.json, component specs, .cursorrules output.

**Designers**
- Who: Figma users, UI designers, design system contributors
- Needs: Browsable docs site, visual examples (good/bad), token reference with swatches.

### 4.2 Secondary Users

- Non-technical brand managers — docs site for reference and auditing
- External agencies & vendors — self-serve access without internal contact
- Product managers — reference for scope and compliance decisions

---

## 5. System Architecture

> **Design Principle:** Single source of truth. The content package is the authority. The API serves it. The site renders it. Neither introduces brand decisions — they only shape how content is delivered.

### 5.1 Layer 1 — Content Package

The structured file system that defines all brand intelligence. Maintained by the engineering team. All other layers are derived from this.

```
ai-brand-context/
│
├── branding.md              ← core brand rules (voice, visual identity, usage principles)
├── tokens.json              ← enforceable design tokens (W3C DTCG format)
├── components.md            ← approved UI patterns and component usage guidelines
├── donts.md                 ← hard constraints — what AI must never produce
├── quality-gates.yaml       ← validation rules for AI output
│
├── platforms/
│   ├── web-aem/
│   │   ├── constraints.md
│   │   ├── tokens-override.json
│   │   └── examples/
│   ├── web-react/
│   │   ├── constraints.md
│   │   ├── tokens-override.json
│   │   └── examples/
│   └── marketing/
│       ├── constraints.md
│       ├── tokens-override.json
│       └── examples/
│
├── examples/
│   ├── good/
│   └── bad/
│
└── ai/
    ├── system-prompt.md
    └── usage.md
```

### 5.2 Layer 2 — Composer API

A lightweight REST API that assembles task-scoped context payloads on demand. The primary AI-facing interface — one request returns exactly the content needed, pre-composed.

#### Core Endpoint

```
GET /context

Parameters:
  platform    web-react | web-aem | marketing
  task        component | page | copy | asset
  fidelity    prototype | production
  format      markdown | json  (default: markdown)
```

The composer selects and merges content slices in priority order: global brand rules → platform overrides → task-relevant patterns → applicable quality gates. Max payload: 32,000 tokens for LLM compatibility.

#### Additional Endpoints

- `GET /tokens` — full tokens.json for direct integration
- `GET /system-prompt` — pre-composed LLM system prompt
- `GET /health` — version, last-updated, and content hash
- `GET /platforms` — lists available platforms and their metadata

#### Response Format

Default response is Markdown — universally pasteable into any LLM context window. JSON format available for programmatic integration, includes structured metadata alongside the context payload.

### 5.3 Layer 3 — Documentation Site

A public-facing website rendered from the same content package. Designed for human navigation — designers, brand managers, and external agencies who need to browse rather than query.

- Full-text search across all brand content
- Platform selector — filters all docs to a specific platform context
- Visual examples gallery with good/bad annotation
- Token browser with visual swatches
- Copy-ready system prompts and API snippets per page
- Version history and changelog

---

## 6. Feature Requirements

### 6.1 Content Package

#### F-01 — Design Token Schema

`tokens.json` must conform to the W3C Design Tokens Community Group format. All tokens must include: name, value, type, and description. Token groups: color, typography, spacing, border-radius, shadow, motion.

> **Requirement:** All color tokens must pass WCAG 2.1 AA contrast validation as part of the quality gate. Tokens that fail must be flagged in `quality-gates.yaml` with the corrected value.

#### F-02 — Quality Gates Specification

`quality-gates.yaml` defines machine-checkable rules for AI output validation. Required gates for v1:

- Color contrast — minimum 4.5:1 for body text, 3:1 for large text and UI components
- Heading hierarchy — sequential order enforced (no skipping H2 to H4)
- Inline styles — flagged as violation; all styles must reference tokens
- Placeholder content — lorem ipsum and placeholder images rejected in production fidelity
- Font usage — only `tokens.typography` values permitted
- Spacing — only `tokens.spacing` values permitted for margin and padding

#### F-03 — Platform Context Files

Each platform subdirectory must contain:
- `constraints.md` — hard limits specific to the platform
- `tokens-override.json` — platform-specific token values
- `examples/` — minimum two good and two bad annotated examples

### 6.2 Composer API

#### F-04 — Context Composition Logic

The composer must assemble context in this priority order:
1. Global brand rules
2. Platform-specific overrides
3. Task-scoped component patterns
4. Fidelity-filtered quality gates

Later layers override earlier layers where conflicts exist. The resulting payload must never exceed 32,000 tokens.

#### F-05 — Versioning

All API responses must include an `X-Brand-Version` header and a `version` field in JSON responses. Semver format (MAJOR.MINOR.PATCH). Breaking changes to content structure increment MAJOR. Content updates increment MINOR. Corrections increment PATCH.

#### F-06 — Caching

Content payloads are static between version releases. CDN edge caching with `Cache-Control: public, max-age=86400`. Cache invalidated on content package update. ETag support required for efficient revalidation.

#### F-07 — CORS & Access

Publicly accessible with permissive CORS headers. No authentication required for v1. Rate limiting: 1,000 requests/hour per IP. No API key required — accessibility for AI agents is a core requirement.

### 6.3 Documentation Site

#### F-08 — Platform-Scoped Navigation

Platform context selector (web-react, web-aem, marketing) filters all documentation. Selection persisted in URL query parameter for shareability.

#### F-09 — Examples Gallery

Side-by-side annotated good/bad comparisons. Each example includes: platform, task type, violation category (bad examples), and the specific rule demonstrated. Sourced directly from content package `examples/` directories.

#### F-10 — API Integration Panel

Every docs page includes a collapsible panel showing:
- The API request that returns context relevant to the current page
- A copy-ready system prompt pre-loaded with the page content
- Integration snippets for Claude API, OpenAI API, and Cursor `.cursorrules` format

---

## 7. AI Tool Integrations

| Tool | Integration Method | Implementation |
|---|---|---|
| Claude API | System prompt injection | `GET /system-prompt` returns a pre-composed system prompt. Developers prepend this to every Claude API call. Platform and task params scope the content. |
| Cursor / Copilot | `.cursorrules` file | `GET /context?platform=web-react&format=cursorrules` returns a `.cursorrules`-compatible file. Teams commit to project root for automatic context. |
| Figma AI | Plugin (v2 scope) | A Figma plugin calls the API and injects token and component context into Figma AI prompts. v1 provides the API contract; plugin build is future scope. |

---

## 8. Technical Requirements

### 8.1 Stack Recommendations

- **API** — Node.js (Express or Fastify), hosted on Vercel or Cloudflare Workers for edge caching
- **Content** — Markdown + JSON files in a Git repository; single source of truth
- **Docs Site** — Next.js with static generation from content package; deployed to Vercel
- **CI/CD** — GitHub Actions; content validation runs on every PR before merge

### 8.2 Performance Requirements

- API p95 response time: <200ms (cached), <800ms (uncached)
- Docs site Lighthouse score: >90 performance, >95 accessibility
- API availability: 99.9% uptime SLA
- Maximum context payload: 32,000 tokens for LLM compatibility

### 8.3 Content Validation Pipeline

Every pull request to the content package triggers:

1. Schema validation — `tokens.json` checked against W3C token schema
2. Quality gate audit — all color tokens checked for WCAG compliance
3. Link integrity — all cross-references between content files verified
4. Payload size check — all composer permutations checked against 32k token limit
5. Diff summary — auto-generated changelog entry for review

---

## 9. Phased Roadmap

### Phase 1 — Foundation (Weeks 1–4)

- Migrate existing brand guidelines, UI styleguide, and assets into content package structure
- Define and validate `tokens.json` from existing design system
- Draft `quality-gates.yaml` covering the six required gates
- Author platform context files for web-react and web-aem
- Create initial good/bad examples — minimum four per platform

### Phase 2 — API (Weeks 5–8)

- Build and deploy composer API with core `GET /context` endpoint
- Implement versioning, caching, and CORS requirements
- Generate `.cursorrules` output format for Cursor integration
- Generate system-prompt output for Claude API integration
- Internal testing with real AI tool sessions against content

### Phase 3 — Docs Site (Weeks 9–12)

- Build Next.js documentation site from content package
- Implement platform selector and filtered navigation
- Build examples gallery with good/bad annotation
- Add API integration panel to all pages
- Soft launch to internal teams; gather feedback

### Phase 4 — Validation & Rollout (Weeks 13–16)

- Controlled comparison: AI output quality with vs. without system context
- Measure rework rate reduction against baseline
- Onboard external agencies with self-serve access
- Marketing platform context file authored and tested
- Public documentation site launch

---

## 10. Success Metrics

| Metric | Baseline | v1 Target |
|---|---|---|
| AI-generated UI rework rate | ~40% | <15% |
| Time to brand-compliant AI output | Manual, variable | <5 min with API |
| Context re-entry per session | Every session | 0 (persistent via API) |
| Agency onboarding time | Days (email required) | <30 min (self-serve) |
| API response time (cached) | N/A | <200ms p95 |
| Content package coverage | 0% | 100% of brand guidelines |

---

## 11. Risks & Mitigations

**R-01 — Content drift** `HIGH`
Brand guidelines updated without syncing to content package.
_Mitigation: Engineering owns the repo; brand updates require a PR with validation. Quarterly audit scheduled._

**R-02 — LLM context limits** `MEDIUM`
Full context payload exceeds model window for complex tasks.
_Mitigation: Composer enforces 32k token cap. Fidelity param allows prototype-level trimming for larger tasks._

**R-03 — Adoption resistance** `MEDIUM`
Teams continue using ad-hoc prompting instead of the API.
_Mitigation: API integration panel on every docs page reduces friction. Cursor `.cursorrules` is automatic once committed to project root._

**R-04 — AI tool API changes** `LOW`
Cursor or Claude API changes break integration format.
_Mitigation: Format output is template-driven; updating a single template file is sufficient to adapt._

---

## 12. Open Questions

- Should the docs site require SSO authentication, or remain fully public? _(Current assumption: public)_
- Who is the final approver for content package PRs — engineering lead, brand lead, or joint review?
- Should `quality-gates.yaml` be enforced programmatically in v1, or remain advisory spec only?
- Is a Figma plugin scoped to v2, or should it be explored as part of the v1 API contract?
- Should external agencies receive a read-only API token with higher rate limits than anonymous access?

---

## Appendix — Glossary

| Term | Definition |
|---|---|
| Composer | The API layer that assembles task-scoped context payloads from the content package. |
| Content Package | The structured file system of brand content — the single source of truth for all layers. |
| Context Payload | A single flat API response containing all brand context needed for a specific task. |
| Design Token | A named, versioned design decision (color, spacing, etc.) expressed as a machine-readable value. |
| Fidelity | The production-readiness level of requested output — prototype or production. |
| Quality Gate | A machine-checkable rule that AI output must satisfy before being considered brand-compliant. |
| Task Scope | The narrowing of context to a specific type of AI task — component, page, copy, or asset. |

---

## Document History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | April 2025 | Engineering | Initial draft |