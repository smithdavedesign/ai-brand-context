# AI Brand Context PRD vs. SolidigmGPT Platform Fit

This document compares the goals of `Brand-AI-Context-PRD.md` with the capabilities already present in this repository. The intent is to answer a practical question:

How much of the PRD can be delivered inside the current SolidigmGPT platform, and what would need to be added?

## Short Answer

The PRD fits this repository well, but not as a one-to-one implementation of the original architecture.

The best path in this repo is not to treat the AI Brand Context System as only a standalone composer API plus docs site. Instead, the best fit is to treat brand context as a new platform capability delivered through the systems that already exist here:

- a native skill in `solidigm-skills`
- optional MCP tools in `mcp`
- optional web documentation surfaces in `solidigmgpt/apps/web`
- optional orchestrator integration in `orchestrator/solidigmgpt`
- optional plugin packaging in `plugins`

That means the PRD does not need to be discarded. It should be translated into this platform's primitives.

## Architectural Translation

The PRD proposes three layers:

1. content package
2. composer API
3. documentation site

Within this repository, the closest translation is:

1. **Content package**
   A versioned brand knowledge package stored in-repo, probably as markdown, JSON, and YAML assets under a dedicated directory.

2. **Delivery layer**
   A combination of:
   - a skill for prompt-time brand guidance
   - MCP tools for structured lookups and validation
   - optional API endpoints in the web app or skills runtime for direct programmatic access

3. **Human-facing documentation**
   A docs experience rendered by the existing web stack, or a simpler documentation surface generated from the same source files.

So the PRD still works conceptually. The main change is that this repo already has strong delivery mechanisms, and they are more capable than a single-purpose composer API alone.

## Goal-by-Goal Comparison

## Goal 1: Single authoritative source of brand context

**PRD goal**

Provide a single, authoritative source of brand context accessible to humans and AI agents.

**Fit with this repo**

Strong fit.

The repository already has a pattern for reusable AI-facing knowledge packages through `solidigm-skills`, and it already supports structured enterprise tooling through `mcp`. A brand content package can become a first-class source of truth here if the content is stored in a stable directory and exposed through those layers.

**What to build here**

- Create a dedicated brand-content package in the repo.
- Use that package as the backing source for both skill prompts and MCP responses.
- Optionally expose the same content in a web docs surface.

**Assessment**

This is directly achievable in the current architecture.

## Goal 2: Let AI tools produce on-brand output without manual context setup

**PRD goal**

Enable Claude, Cursor, Copilot, and similar tools to receive the right brand context automatically.

**Fit with this repo**

Very strong fit.

This repository already has the exact distribution primitives needed:

- lazy-loaded skills for prompt injection when relevant
- plugins for Copilot-style distribution
- MCP server integration for structured tool access

The lazy-loading skill pattern is especially well aligned with the PRD's token-efficiency objective. It means brand context does not need to be loaded on every request, only on requests that actually need design or brand guidance.

**What to build here**

- A `brand-context` skill with routing guidance and references.
- Optionally a `.cursorrules`-style export path if Cursor-specific output is still needed.
- Plugin packaging so external users can consume the skill without the full internal app.

**Assessment**

This is one of the strongest matches between the PRD and the current platform.

## Goal 3: Task-scoped context delivery

**PRD goal**

Return only the context relevant to a specific platform and task type.

**Fit with this repo**

Strong fit, but it should not rely only on a standalone REST composer.

The current platform already uses progressive disclosure. The web app gives the model summaries and routing hints, then loads the full skill only when needed. The MCP server can also expose narrowly scoped tools. Together, those two mechanisms already solve a large part of the context selection problem.

**What to build here**

- In the skill: keep the global brand rules and task-selection guidance.
- In MCP: expose granular queries such as `get_brand_tokens`, `get_platform_constraints`, and `get_quality_gates`.
- If direct external API access is still important, expose a thin composer endpoint backed by the same content package rather than making the API the primary abstraction.

**Assessment**

Achievable, but the repo suggests a hybrid approach instead of a pure composer-API-first design.

## Goal 4: Support non-technical stakeholders via browsable docs

**PRD goal**

Provide a documentation site built from the same source of truth.

**Fit with this repo**

Moderate to strong fit.

The web app stack can host this, but the current product is centered on chat, not on publishing docs. So this is feasible, but it is a more explicit product addition than the skill and MCP work.

**What to build here**

- Add a docs section in `solidigmgpt/apps/web` or a related docs surface.
- Render brand content from the same source package used by the skill and MCP layers.
- Add search, platform filtering, examples, and token visualization incrementally.

**Assessment**

Good fit, but not the lowest-lift first milestone.

## Goal 5: Versioned, maintainable content structure owned by engineering

**PRD goal**

Create a versioned content package with engineering ownership and CI validation.

**Fit with this repo**

Strong fit.

This repo already treats markdown, configuration, test assets, and validation harnesses as first-class citizens. The `solidigm-skills` eval harness shows that the team already has the right habits for content-as-code. The remaining work is to define the brand content schema and add the right validation checks.

**What to build here**

- A brand package directory with explicit structure.
- Validation scripts for schema, token integrity, and rule consistency.
- CI checks similar in spirit to skill validation.

**Assessment**

This is structurally very compatible with the repository.

## Goal 6: Reduce rework through enforceable tokens and quality gates

**PRD goal**

Improve AI output quality and reduce rework using tokens, constraints, and quality gates.

**Fit with this repo**

Strong fit if implemented in two layers.

The platform already has:

- skills for behavioral guidance
- MCP for structured lookups and validations
- eval infrastructure for measurement

That means brand compliance can be addressed through both generation-time guidance and evaluation-time enforcement.

**What to build here**

- Brand eval rubrics in the skill harness.
- Optional MCP validation tools such as `validate_against_quality_gates`.
- Later, optional automated linting or CI enforcement for generated artifacts.

**Assessment**

This is achievable and measurable inside the current system.

## PRD Non-Goals vs. Repo Reality

Several PRD non-goals align well with the current repo. A few do not.

### Good alignment

- No fine-tuning required.
- No embeddings pipeline required.
- No CMS required for v1.
- Advisory quality-gate spec can come before strict enforcement.

### Tensions to resolve

- The PRD assumes public, unauthenticated access as a default. This repo already has a strong identity and RBAC posture in `mcp`.
- External agency access is easier to solve through plugin packaging or a public docs surface than by exposing the internal MCP server directly.
- A standalone public API may still be useful, but it should be treated as a separate delivery surface, not as the only brand interface.

## Best-Fit Implementation Model For This Repo

If the goal is to get maximum value quickly with minimal architectural friction, the best implementation model is:

### Layer A: Brand content package

Create a versioned content package in-repo that contains:

- core brand rules
- design tokens
- platform constraints
- examples
- quality gates
- AI-facing usage guidance

This becomes the source of truth.

### Layer B: Brand skill

Create a `brand-context` skill in `solidigm-skills` that:

- explains how to apply the brand package
- tells the model when to ask for platform-specific details
- references structured brand assets
- optionally invokes tools for exact lookups and validation

This is the fastest useful product slice.

### Layer C: Brand MCP tools

Add a brand-oriented module to `mcp` that exposes structured functions such as:

- `get_brand_tokens`
- `get_platform_constraints`
- `get_component_guidelines`
- `get_brand_examples`
- `get_quality_gates`
- `validate_against_quality_gates`

This turns the system from prompt-only guidance into tool-assisted brand reasoning.

### Layer D: Docs and external access

If needed, add:

- a docs view in the web app
- plugin manifests for external Copilot consumption
- a direct API surface for non-chat integrations

This is likely phase 2 or 3, not day 1.

## Recommended Priority Order

Your proposed order is directionally correct. I would tighten it slightly for this repo.

### 1. Brand content package plus brand skill

Why first:

- lowest implementation friction
- immediately uses the platform's strongest existing primitive
- creates the source material every later phase depends on
- gives the fastest path to testable value

Deliverables:

- brand content directory
- `brand-context/SKILL.md`
- skill references and optional scripts
- trigger, execution, and rubric evals

### 2. Brand MCP tools

Why second:

- upgrades the capability from static prompting to structured lookups
- keeps token usage down by returning exact slices on demand
- fits the existing group-based registration model if access should be scoped

Deliverables:

- brand tool module
- tool registration and access model
- validation logic for quality gates

### 3. Plugin packaging

Why third:

- relatively low implementation cost once the skill exists
- directly addresses agency and external-consumer distribution
- does not require exposing internal infrastructure broadly

Deliverables:

- a plugin manifest that packages the new brand skill
- optional packaging of public-safe MCP endpoints if appropriate

### 4. Orchestrator integration

Why fourth:

- strategically powerful but not the first dependency
- depends on the brand package being stable enough to use as a constraint source
- should come after the guidance and query layers are already working

Deliverables:

- spec-generation prompts that reference brand constraints
- optional compliance checks during implementation workflows

## What Is Native vs. Net-New

## Already native in this repo

- skill packaging and lazy loading
- skill testing and rubric evaluation
- plugin packaging
- authenticated structured tool delivery via MCP
- web application surface for optional docs or configuration UX
- orchestrator hooks for future automation

## Needs moderate new work

- brand content schema and file layout
- skill content and evals
- brand-specific MCP tools
- direct API responses shaped for non-chat brand consumers
- documentation pages tailored to designers and agencies

## Truly net-new if you want the PRD exactly as written

- a standalone public composer API as the canonical entry point
- a dedicated public docs product with search and polished examples gallery
- anonymous high-scale public distribution with CDN-first semantics

Those are still possible, but they are no longer the shortest path once this repo is taken seriously as the host platform.

## Suggested Decision

The cleanest strategic decision is:

Use the PRD's **content package** idea as the system of record, but implement delivery through the existing SolidigmGPT platform primitives first.

In other words:

- keep the PRD's source-of-truth model
- do not overcommit to a composer-API-only architecture
- let skills, MCP, plugins, and later the orchestrator become the primary delivery channels

That would preserve the spirit of the PRD while taking maximum advantage of what this codebase already does well.

## Recommended First Milestone

If this were being scoped as an execution plan inside this repo, the first milestone should be:

**Brand Context Foundation**

Contents:

- Create a brand content package directory.
- Create a `brand-context` skill backed by that package.
- Add skill evals for correctness, token use, platform constraints, and forbidden patterns.
- Add a minimal plugin manifest so the capability can be distributed outside the internal web app.

Success criteria:

- The model loads brand guidance only when relevant.
- Brand-specific prompts become reusable across projects.
- The eval harness can measure compliance quality.
- The capability is distributable without inventing a new platform.

## Bottom Line

Your instinct is correct.

This repository already contains most of the infrastructure needed to deliver the AI Brand Context System. The biggest missing pieces are the brand content itself, the skill that wraps it, the evals that measure it, and the optional MCP tools that make it queryable and enforceable.

So the work is mostly content design and platform wiring, not foundational architecture.