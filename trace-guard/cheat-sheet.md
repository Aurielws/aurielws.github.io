# TRACE → GUARD — One-Page Cheat Sheet

Trigger prompts only — not answers. Rehearse until each line fires the full move.

## Part One — TRACE the incident

| Move | Trigger prompts |
|---|---|
| **T · Translate** | Expected? Observed? Metric? Onset? Severity? · Is the metric itself trustworthy (definition, logging, denominator)? |
| **R · Restrict** | Affected vs unaffected — two columns. · Smallest condition that predicts failure? · Sudden or gradual? Deterministic or intermittent? |
| **A · Aim** | 5–8 boxes. Circle the evidence-weighted region. Say *why* you start there. · Ask for one affected + one matched healthy request. |
| **C · Compare** | Earliest divergence, not loudest failure. · Same input, different output → inspect here. Different input → go upstream. Same output, different outcome → go downstream. · Six questions: invoked? input? output? version? decision? enforced? |
| **E · Establish** | Max 3 hypotheses (for / against / next test). · One-variable replay. · Four alignments: temporal, cohort, mechanistic, reversal. · Does the diagnosis explain the *onset*? · Stop when the chain is complete. |

## The Interrupt

**Severe harm → contain in parallel.** Reversible action · name the cost · preserve evidence.

## Part Two — GUARD the system

| Move | Trigger prompts |
|---|---|
| **G · Generalize** | One level above the bug. Mechanism, not topic. |
| **U · Understand** | Must do / must never do / constraints. Red-line invariant, stated as a sentence. |
| **A · Architect** | Prevent · detect · recover. Four planes: serving, control, eval/observability, recovery/ops. |
| **R · Reason** | "I choose ___ because severity is ___. The cost is ___. I bound it with ___." · Stress: classifier down? partial rollout? timeout-after-success? green metrics, red class? |
| **D · Deploy** | Offline eval → replay → shadow → canary → ramp → 100%. · Success metric, guardrails, rollback trigger, owner. |

## Sentences that carry you

- **Opening:** "I'll align on expected behavior and the exact failure signal, sketch the relevant path, find the earliest divergence with an affected-vs-healthy comparison, then run the cleanest test that separates my top hypotheses. Severe harm gets contained in parallel."
- **Evidence update:** "This makes ___ less likely and ___ more likely. My next test is ___ because it distinguishes ___ from ___."
- **Diagnosis:** "The root cause is ___. The mechanism is ___. The decisive evidence is ___."

## When you get stuck

Say: *"Let me take a moment to update my hypothesis from that evidence."* Then: **Evidence → Meaning → Next.**

Rescue questions: ① affected vs matched healthy? ② what entered/exited the first diverging component? ③ what changed near the onset? ④ change only the suspected variable? ⑤ what single fact still blocks a diagnosis?

## Nuggets

1. Trace first. Then guard. Never design before you diagnose.
2. Downstream components can be correct victims — hunt the *earliest* divergence.
3. Contain severe harm in parallel. Diagnosis can wait; damage cannot.
4. Source exists ≠ source reached the model.
5. A healthy control constrains your theory more than another failing example.
6. Faster can mean the system is doing less work.
7. One controlled replay beats twenty clarifying questions.
8. Compare final authorization decisions, not principal counts.
9. Match the unit of enforcement to the unit of risk.
10. A retry is only safe when the action has a stable identity. Timeout = unknown, not failed.
11. Questions don't make you junior — questions disconnected from evidence do.
12. You are reducing uncertainty one meaningful step at a time.
