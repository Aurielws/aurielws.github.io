# TRACE → GUARD — Vocabulary

New and load-bearing terms from the lesson, in plain language.

| Term | Meaning |
|---|---|
| **Symptom** | What the user sees go wrong. The starting point, never the answer. |
| **Mechanism** | *How* the failure produced the symptom — the causal chain. |
| **Root cause** | The specific change or defect that started the chain, plus why now. |
| **Boundary condition** | The smallest condition that predicts failure (e.g. "group-shared docs only"). |
| **Blast radius** | Who/what is affected — and, equally, who is not. |
| **Cohort** | A slice of traffic or users sharing one property (version, region, bucket). |
| **Control (matched healthy request)** | A near-identical healthy case used for stage-by-stage comparison. |
| **Earliest divergence** | The first stage where affected and healthy behavior differ. |
| **Conditional metric** | A stage metric given its input survived the previous stage ("survives permission, given retrieved"). |
| **Evidence-weighted search** | Starting the investigation in the region the symptom + scope make most likely. |
| **Containment** | A reversible action that cuts immediate harm before the diagnosis is done. |
| **Latent vulnerability vs trigger** | An old weakness vs the new event that activated it today. |
| **Ablation / replay** | Re-running the same request with exactly one variable changed. |
| **Rollout bucket / canary** | A small slice of traffic getting the new version first. |
| **Shadow deployment** | New version runs on real traffic, output compared but not served. |
| **Semantic shadowing** | Diffing old-vs-new *decisions* (e.g. authorization) before enforcing the new path. |
| **Principal** | An identity the permission system checks (user, group, alias). |
| **Canonicalization** | Normalizing identifiers to one standard form — can silently change semantics. |
| **ACL (access-control list)** | The list of principals allowed to touch a document or action. |
| **Idempotency (key)** | Running the same action twice has one effect; the key gives the action a stable identity. |
| **Fail open / fail closed** | On uncertainty: allow (availability) vs deny (safety). Irreversible harm → fail closed. |
| **Red-line invariant** | A property that must never break, and must never be averaged away. |
| **Four planes** | Serving (hot path), control (versions/flags), eval + observability, recovery + operations. |
| **Sufficiency check** | The RAG stage deciding whether surviving evidence is strong enough to answer. |
| **Drift** | Gradual degradation from slowly changing data, traffic, or behavior. |
| **Stop rule** | The moment the causal chain is complete — state the diagnosis and stop digging. |
