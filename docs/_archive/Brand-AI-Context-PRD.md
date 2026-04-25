# AI Brand Context for SolidigmGPT — Product Requirements Document

**Version:** 2.0  
**Status:** Draft  
**Owner:** Engineering  
**Date:** April 2026

---

## Table of Contents

1. Executive Summary
2. Problem Statement
3. Product Framing in This Repository
4. Goals and Non-Goals
5. Users and Stakeholders
6. Current Platform Fit
7. Proposed System Architecture
8. Functional Requirements
9. Content Model
10. Delivery Surfaces
11. Validation and Quality Model
12. Phased Roadmap
13. Success Metrics
14. Risks and Mitigations
15. Open Questions

---

## 1. Executive Summary

Solidigm teams increasingly use AI systems to generate UI, code, content, and design artifacts, but those systems do not consistently operate with reliable brand and platform context. The result is predictable: off-brand output, repeated manual correction, inconsistent implementation patterns, and avoidable review churn.

This PRD defines an **AI Brand Context capability** built inside the existing SolidigmGPT platform. Rather than introducing a separate standalone product as the primary delivery path, this capability will use the platform primitives already present in this repository:

- a structured brand content package as the source of truth
- a native `brand-context` skill in `solidigm-skills`
- optional brand query and validation tools in `mcp`
- plugin packaging for external Copilot-style consumption
- optional web documentation surfaces for human browsing
- later orchestrator integration so autonomous implementation workflows can inherit brand constraints

The core product idea remains the same as the original concept: AI systems should be able to retrieve only the brand context they need, when they need it, in a format that is reusable, versioned, and measurable.

The key change is architectural: in this repository, the fastest and most defensible implementation is **content package first, platform-native delivery second**, not a composer-API-only design.

---

## 2. Problem Statement

### 2.1 Current State

AI tools are already embedded in design and engineering workflows, but they operate without a stable, machine-readable brand layer. As a result:

- generated UI violates spacing, typography, or color standards
- platform-specific constraints are missed
- component usage is inconsistent across teams and projects
- off-brand output survives too long before review catches it
- users repeatedly re-explain the same standards in each session

### 2.2 Root Cause

Brand and UI standards mostly exist as human-readable material: prose docs, Figma files, PDF guidelines, scattered examples, and team memory. Those materials are useful to humans but weak as runtime context for AI systems.

There is currently no single system that does all of the following well:

- stores brand guidance as versioned content
- makes it consumable by AI tools
- scopes the content to the task at hand
- validates whether generated output followed the rules

### 2.3 Impact

| Stakeholder | Pain Point | Impact |
|---|---|---|
| Designers | AI output ignores visual standards | High rework on layouts and components |
| Developers | No reliable brand-aware guidance in AI tooling | Inconsistent implementation patterns |
| Brand / Marketing | Brand review happens too late | Off-brand artifacts reach late-stage review |
| External partners | No self-serve delivery path | Slow onboarding and repeated manual support |
| Engineering | No measurable compliance loop | Quality depends on reviewer vigilance |

---

## 3. Product Framing in This Repository

This capability is not a separate standalone product by default. In this repository it should be framed as a **new platform capability inside SolidigmGPT**.

That means:

- the **source of truth** is a versioned brand content package in the repo
- the **primary AI delivery surface** is a native skill
- the **structured query and validation surface** is MCP
- the **external distribution surface** is plugins
- the **human-readable surface** is optional docs in the web app
- the **automation surface** is later orchestrator integration

This framing matters because it reuses systems the platform already does well:

- lazy-loaded skills to preserve token efficiency
- eval harnesses to measure output quality
- MCP tools for structured, queryable data access
- plugin manifests for external distribution
- an existing web product for optional human browsing

---

## 4. Goals and Non-Goals

### 4.1 Goals

1. Create a single, versioned source of truth for brand rules, tokens, platform constraints, examples, and quality gates.
2. Allow AI tools using SolidigmGPT surfaces to retrieve brand context without manual re-entry.
3. Deliver brand guidance with progressive disclosure so only relevant context is loaded.
4. Enable structured lookups for tokens, platform constraints, examples, and quality gates.
5. Measure brand compliance quality with repeatable evals.
6. Provide a path for external distribution through plugin packaging.
7. Create a future integration point for orchestrator workflows so generated specs and implementations can inherit brand constraints.

### 4.2 Non-Goals for v1

- Real-time Figma synchronization
- Fine-tuning a model on brand data
- Building a separate CMS for brand authors
- Full automatic enforcement of all brand rules in CI
- Multi-brand support
- A public anonymous API as the only delivery model

---

## 5. Users and Stakeholders

### 5.1 Primary Users

**AI systems using the platform**
- Need scoped brand context during chat, code generation, design generation, and document generation.

**Frontend developers**
- Need reliable brand-aware rules for components, pages, tokens, and platform-specific implementation constraints.

**Designers and design system contributors**
- Need reusable brand guidance, token definitions, examples, and quality rules.

### 5.2 Secondary Users

**Brand and marketing reviewers**
- Need confidence that outputs are aligned earlier in the process.

**External agencies and vendors**
- Need a safe self-serve distribution path that does not require access to the full internal application.

**Engineering leadership**
- Needs measurable quality improvement and reduced review churn.

---

## 6. Current Platform Fit

The existing platform already provides most of the delivery infrastructure needed.

### 6.1 What Already Exists

**Skill system**
- `solidigm-skills` stores markdown-based skills and eval definitions.
- `solidigmgpt/apps/skills-runtime` serves skill metadata, full prompts, tool definitions, and tool execution.
- `solidigmgpt/apps/web` already uses progressive disclosure so full skill content is loaded only when relevant.

**MCP system**
- `mcp` already supports secure tool delivery, group-based access, and dynamic tool registration.
- It is a natural place for structured brand queries and later validation tools.

**Plugin system**
- `plugins` already packages skills and MCP server definitions for external Copilot-style consumption.

**Orchestrator**
- `orchestrator/solidigmgpt` already generates specs and implementation workstreams.
- It can later consume brand context as a constraint source.

### 6.2 Main Architectural Insight

The brand system should not begin as a parallel product stack. It should begin as:

1. brand content package
2. brand skill
3. brand evals
4. brand MCP tools

That sequence delivers value fastest and fits the existing codebase cleanly.

---

## 7. Proposed System Architecture

## 7.1 Layer 1 — Brand Content Package

The brand content package is the system of record.

Proposed structure:

```text
brand-context/
├── branding.md
├── components.md
├── fonts.md
├── tokens.json
├── quality-gates.yaml
├── ai/
│   ├── system-guidance.md
│   └── usage.md
├── platforms/
│   ├── web-react/
│   │   ├── constraints.md
│   │   ├── tokens-override.json
│   │   └── examples/
│   ├── web-nextjs/
│   │   ├── constraints.md
│   │   ├── tokens-override.json
│   │   └── examples/
│   └── marketing/
│       ├── constraints.md
│       ├── tokens-override.json
│       └── examples/
└── examples/
    ├── good/
    └── bad/
```

This content package will be referenced by the skill, queried by MCP tools, and optionally rendered in the web app.

## 7.2 Layer 2 — Brand Skill

Create a `brand-context` skill under `solidigm-skills/skills/brand-context/`.

Purpose:

- teach the model how to apply brand rules
- define when to load brand context
- explain how to use platform-specific constraints
- route the model toward exact lookups when full context is not needed

The skill is the fastest path to runtime value because the current platform already supports:

- skill discovery
- lazy loading
- routing hints
- tool registration per skill
- eval coverage

## 7.3 Layer 3 — Brand MCP Tools

Add a brand-oriented tool module in `mcp/tools/`.

Candidate tools:

- `get_brand_tokens`
- `get_platform_constraints`
- `get_component_guidelines`
- `get_brand_examples`
- `get_quality_gates`
- `validate_against_quality_gates`

These tools should read from the same content package as the skill.

## 7.4 Layer 4 — Plugin Packaging

Add a plugin manifest that packages the brand skill for external Copilot-style use.

This provides:

- low-friction distribution
- agency-friendly onboarding
- reuse outside the internal web app

## 7.5 Layer 5 — Optional Web Documentation

If human browsing is needed in v2 or later, add a docs view in `solidigmgpt/apps/web` that renders the brand content package.

This should be treated as a consumer of the same source of truth, not the source itself.

## 7.6 Layer 6 — Later Orchestrator Integration

Once the brand system is stable, the orchestrator can use it as a constraint layer during:

- roadmap-to-spec decomposition
- implementation prompt generation
- post-generation quality checks

This is strategically valuable but should not be the first milestone.

---

## 8. Functional Requirements

## 8.1 Content Package Requirements

### F-01 — Source of Truth

All brand rules, tokens, examples, platform constraints, and quality gates must live in a versioned package in the repository.

### F-02 — Structured Tokens

`tokens.json` must use a stable machine-readable schema and support token groups such as:

- color
- typography
- spacing
- radius
- shadow
- motion

### F-03 — Platform Constraints

Each supported platform must define:

- hard constraints
- overrides where needed
- examples of correct and incorrect usage

### F-04 — Hard “Don’t” Rules

The system must include explicit “never do this” rules for common failure modes, not just positive guidance.

## 8.2 Skill Requirements

### F-05 — Lazy-Loadable Brand Skill

The brand context must be deliverable as a skill that the platform can load only when the task requires brand-aware behavior.

### F-06 — Task Guidance

The skill must explain how to apply brand rules across at least these task types:

- component generation
- page generation
- marketing content generation
- brand-aware review and critique

### F-07 — Platform Awareness

The skill must describe how platform-specific constraints modify generic brand rules.

## 8.3 MCP Requirements

### F-08 — Structured Queries

MCP tools must support exact retrieval of brand slices so the model does not need the full brand package in prompt context.

### F-09 — Validation Queries

At least one MCP tool must support validation-oriented output against the defined quality gates.

### F-10 — Access Model

Brand MCP tools must support an access model appropriate for the organization. Public anonymous access is not assumed for the internal MCP server.

## 8.4 Plugin Requirements

### F-11 — External Distribution

The brand capability must support packaging through the repository’s existing plugin model so users can consume it outside the main web app.

## 8.5 Optional Web Requirements

### F-12 — Human Browsing Surface

If implemented, the web app should render the same source content in a format useful for humans, including:

- platform filtering
- example browsing
- token reference browsing
- copyable integration snippets

---

## 9. Content Model

The brand content package should contain at minimum:

### 9.1 Global Brand Rules

- brand principles
- voice and tone
- visual rules
- approved patterns

### 9.2 Design Tokens

- canonical values
- descriptions
- grouping by token type
- override support per platform

### 9.3 Component Guidance

- approved component patterns
- composition rules
- misuse patterns

### 9.4 Platform Constraints

- technical constraints
- implementation conventions
- delivery-specific requirements

### 9.5 Examples

- good examples with annotations
- bad examples with explanations

### 9.6 Quality Gates

Examples of initial quality gates:

- spacing must map to approved tokens
- typography must map to approved tokens
- color usage must map to approved tokens
- placeholder content must not appear in production-oriented output
- explicit banned patterns must be flagged
- platform-specific constraints must not be violated

---

## 10. Delivery Surfaces

## 10.1 Primary Surface: Skill Delivery

For the current platform, the primary delivery mechanism should be the brand skill.

Why:

- lowest lift
- strongest existing support in the platform
- best match for lazy loading and token efficiency

## 10.2 Secondary Surface: MCP Delivery

MCP should provide exact, structured retrieval and later validation.

Why:

- keeps prompts smaller
- enables dynamic queries
- allows later enforcement-oriented workflows

## 10.3 Distribution Surface: Plugin Packaging

Plugins should package the capability for external users without forcing them into the full internal web application.

## 10.4 Optional Human Surface: Web Docs

The web app may expose the content to humans, but that should be treated as a later consumer surface, not the first dependency.

## 10.5 Optional Direct API Surface

If direct external API use is still required, it should be implemented as a thin adapter over the same content package rather than becoming a separate parallel source of truth.

---

## 11. Validation and Quality Model

## 11.1 Skill Evals

The initial quality loop should use the existing `solidigm-skills` eval harness.

Required eval coverage:

- trigger tests to ensure brand skill activates on the right prompts
- execution tests to ensure brand rules are actually applied
- rubric grading to measure compliance quality

Example rubric dimensions:

- correct use of tokens
- respect for platform constraints
- adherence to “don’t” rules
- avoidance of generic off-brand output
- clarity of reasoning when tradeoffs exist

## 11.2 MCP Validation

In a second phase, MCP tools should return structured findings for quality-gate checks.

## 11.3 CI Validation

Brand content should be validated in CI for:

- schema correctness
- missing references
- token integrity
- example completeness
- payload size or prompt-size constraints where relevant

---

## 12. Phased Roadmap

## Phase 1 — Foundation

Deliver:

- brand content package structure
- initial token set
- initial rules, examples, and quality gates
- first version of `brand-context` skill
- skill evals

Outcome:

Brand-aware guidance exists as a native platform capability.

## Phase 2 — Structured Query Layer

Deliver:

- brand MCP tools for retrieval
- initial validation-oriented tool output
- shared content access between skill and MCP layers

Outcome:

Brand context becomes queryable, not just prompt-driven.

## Phase 3 — Distribution and Human Access

Deliver:

- plugin packaging
- optional web docs surface
- optional lightweight API adapters if needed

Outcome:

The capability becomes easier to consume inside and outside the internal app.

## Phase 4 — Automation Integration

Deliver:

- orchestrator prompt integration
- optional compliance checks in spec or implementation workflows

Outcome:

Autonomous generation workflows inherit brand constraints upstream.

---

## 13. Success Metrics

| Metric | Baseline | Target |
|---|---|---|
| Rework rate on AI-generated brand-sensitive output | High / inconsistent | Meaningful reduction after rollout |
| Time to get usable on-brand AI output | Manual and repeated | Reduced through reusable skill and tool delivery |
| Need to restate brand rules per session | Frequent | Near zero for supported workflows |
| Brand compliance measurability | Minimal | Eval-based scoring available |
| External onboarding friction | High | Lower through plugin packaging or docs |

Quantitative thresholds can be added once baseline measurement exists.

---

## 14. Risks and Mitigations

| Risk | Description | Mitigation |
|---|---|---|
| Content drift | Brand knowledge changes without package updates | Treat brand content as code with clear ownership and PR review |
| Over-scoping v1 | Trying to build docs site, public API, skill, MCP, and orchestrator integration at once | Sequence delivery: content + skill first |
| Weak eval quality | The system exists but compliance is not measurable | Define brand-specific rubrics early |
| Access model mismatch | Public PRD assumptions conflict with internal RBAC posture | Separate internal MCP from external plugin/docs distribution |
| Token bloat | Too much brand content injected too often | Use lazy loading plus structured MCP retrieval |

---

## 15. Open Questions

1. Where should the canonical brand content package live in the repo?
2. Which teams own approval for updates: engineering, brand, or joint review?
3. Should brand MCP tools be available to all users or only scoped groups?
4. Is a human-facing docs surface required for v1, or can plugin and skill delivery cover the first release?
5. Do external agencies need only plugin distribution, or also a public read-only documentation experience?
6. Which supported platforms should be in v1: `web-react`, `web-nextjs`, `marketing`, or a smaller subset?

---

## Bottom Line

The AI Brand Context System is a strong fit for this repository, but it should be implemented as a **SolidigmGPT-native capability**, not as a parallel architecture competing with the platform already in place.

The recommended implementation order is:

1. build the brand content package
2. ship the `brand-context` skill and evals
3. add MCP retrieval and validation tools
4. package for external consumption
5. integrate with the orchestrator later

That path preserves the intent of the original idea while using the actual strengths of this system: lazy-loaded skills, structured tools, measurable evals, and reusable distribution surfaces.
