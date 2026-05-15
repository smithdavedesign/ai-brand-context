# Solidigm Brand Voice

## Personality: The Seasoned Challenger

Solidigm is a thought leader with a thoughtful outlook for partners, employees, the environment, and the world at large. We take pride in what we do and relish every challenge. We are inspired by the possibilities of unsolved problems. We see every interaction as an opportunity for an act of service for our customers and employees.

This personality frames everything we write and say. The voice traits below are the tactical expression of it — each trait has a definition, a "but not" guardrail, practical writing guidance, and examples of what it looks like in practice.

---

## The Five Voice Traits

### 1. Optimistic
**Definition:** Upbeat and enthusiastic devotees of possibility thinking.
**But not:** Unrealistic day-dreamers or empty hype.

We lead with what's possible, not what's blocked. We use active constructions and forward-looking language. We acknowledge challenges directly, then pivot to solutions.

**Do:**
- "Storage limitations don't have to limit your data strategy."
- "Every density milestone unlocks something that wasn't possible before."

**Don't:**
- "Despite the difficult market conditions…" (lead with the problem, not the pivot)
- "We're the best." (assertion without substance)
- Superlatives without evidence: "the most", "unmatched", "revolutionary"

---

### 2. Analytical
**Definition:** Thoughtful, intelligent, and deliberate in everything we do and say.
**But not:** Robotic or staid.

We back claims with specifics. We cite specs, ratios, densities, and benchmarks when they're relevant. We don't pad with filler adjectives when a number can do the job.

**Do:**
- "3D NAND at 328 layers — the density that makes the eSSD possible."
- "4.5:1 compression ratio, validated against enterprise workloads."

**Don't:**
- "Incredibly fast" (fast by what measure?)
- "State-of-the-art" (state of whose art, when?)
- Long paragraphs of technical jargon with no payoff for the reader

---

### 3. Passionate
**Definition:** Spirited and energized by technology, excited to engage.
**But not:** Argumentative or confrontational.

We care about the technology and about the people who use it. That passion shows in the specificity of our language, not in aggression toward competitors. We don't punch down or position ourselves as the only sane option.

**Do:**
- "This is the density we've been engineering toward for a decade."
- "We obsess over endurance so your workloads don't have to."

**Don't:**
- Competitor comparisons that belittle rather than differentiate
- Hyped-up verbs: "crushed", "destroyed", "obliterated" (engineering vocabulary, not combat)
- Exclamation points in body copy (acceptable sparingly in social; never in datasheets or docs)

---

### 4. Genuine
**Definition:** Authentic, honest, and straightforward, human and dynamic.
**But not:** Trivial or unprepared.

We write like a knowledgeable colleague, not a press release. We use plain language. We admit uncertainty when it exists. We don't over-promise. "Genuine" also means we don't perform personality — the writing should feel earned, not affected.

**Do:**
- "This drives power higher than some deployments can absorb. Here's how to right-size."
- "The Gen 5 jump is real — but only for workloads that can saturate a PCIe 5 interface."

**Don't:**
- Corporate throat-clearing: "It is our pleasure to announce…"
- Hollow emotion: "We're thrilled/delighted/excited to share…"
- Hedging every claim into meaninglessness: "may potentially offer possible improvements"

---

### 5. Ambitious
**Definition:** Confident and determined, appreciative of the hard work.
**But not:** Arrogant or dismissive.

We set high targets and we name them. We're proud of what we've built. But we don't pretend the work was easy or that customers should simply trust us. Confidence is backed by evidence; ambition is expressed through what we're building, not what we're claiming.

**Do:**
- "Our goal: #1 NAND business by 2030. This is the engineering that gets us there."
- "We've scaled 3D NAND to 328 layers. The next milestone is on the roadmap."

**Don't:**
- "Our competitors simply can't…" (dismissive framing)
- "We dominate…" (arrogance without context)
- Claiming industry firsts without verifiable citations

---

## Quick-reference: the guardrail matrix

| Trait | Be this | Not this |
|-------|---------|----------|
| Optimistic | Possibility-forward, solution-led | Hype, empty superlatives |
| Analytical | Specific, evidence-backed | Robotic, jargon-dense, padded |
| Passionate | Energized, technology-driven | Combative, hyperbolic |
| Genuine | Plain, honest, human | Corporate, hedged, hollow |
| Ambitious | Confident with evidence | Arrogant, dismissive |

---

## Voice in Practice: Content-Type Guide

### Product headlines and taglines
Lead with the technical claim or customer benefit. Title Case. No trailing punctuation.
- ✅ "228-Layer 3D NAND. Storage Without Compromise."
- ❌ "THE FUTURE IS HERE!"

### Datasheets and product briefs
Analytical first. Specs before prose. Use the feature → benefit structure:
"[Feature] — [why this matters to the customer]."
- ✅ "QLC 3D NAND at 228 layers — delivers the GB/$ needed for AI training datasets at petabyte scale."

### Blog and thought leadership
Lead with the insight, back with evidence, close with the forward implication.
Conversational but precise. Occasional first-person plural ("we") is appropriate.
- ✅ Three-paragraph structure: claim → substantiation → implication.
- ❌ Ten paragraphs of scene-setting before the point.

### Marketing copy and web
Optimistic and genuine in equal measure. Short sentences. Subject-verb-object.
Avoid em-dashes in body copy (they can read as hedging or parenthetical excess).
- ✅ "Data has no limits. Neither does our NAND."
- ❌ "In a world where data — increasingly central to every business — continues to expand at an unprecedented rate…"

### Press releases
Formal but human. Lead paragraph: news, significance, date. Quote paragraph: one human quote per release — genuine, not robotic. End with boilerplate.
- ✅ Quote: "228 layers is what we've been engineering toward for three years. It changes the economics of cold storage."
- ❌ Quote: "We are pleased to announce this exciting milestone on our journey to becoming the industry's number-one NAND business."

---

## Words we avoid

| Avoid | Prefer |
|-------|--------|
| Revolutionary | Specific capability claim + evidence |
| World-class | Name the class, name the metric |
| Cutting-edge | Name the technology generation |
| State-of-the-art | Current best / industry-leading + metric |
| Seamless | Specify what's simplified and how |
| Leverage (as a verb) | Use |
| Synergy | Collaboration / partnership |
| Thrilled / excited / delighted | Drop the emotion, let the news carry weight |
| Unique | Name what distinguishes it |
| Solutions (standalone) | Name the actual product or capability |

---

## Notes for AI-generated copy

When generating Solidigm brand copy, the LLM should:

1. Call `get_brand_context(platform=..., task="copy")` to load the scoped context.
2. Draft using the five traits as a mental filter: would a "Seasoned Challenger" say this?
3. Call `validate_brand_output(content=...)` before presenting output.
4. If validation flags `brand-voice`, review the specific lines flagged and apply the guardrail matrix above.

Voice validation in `quality-gates.yaml` checks for prohibited phrases (listed under "Words we avoid"), empty superlatives, hollow corporate boilerplate, and trademark/casing errors. It does **not** score "how optimistic" the copy sounds — that judgment stays with the human reviewer.

---

*Source: Solidigm Brand Overview deck, slide 6 — Brand Tone and Voice. ©2026, Solidigm. All rights reserved. Confidential.*
