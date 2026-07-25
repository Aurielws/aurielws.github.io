# Post-Training for Beginners — Research Brief

Research compiled 2026-07-25 for a Medium article on SFT, RLEF/RLVR, and RLHF data.

**Sourcing note:** direct page fetches were blocked by this session's egress policy, so
everything below comes from web-search result summaries plus arXiv/venue metadata. The
claims are attributed and the URLs are live, but **every specific number should be
re-verified against the primary source before publication.** Items flagged 🔍 are ones I'd
check first — either single-secondary-source numbers or papers from the last few months.

---

## 1. The terminology problem (this is the article's opening move)

Most beginner confusion isn't conceptual, it's lexical. Five acronyms describe overlapping
things and the industry uses them inconsistently. A clean decomposition:

Post-training methods differ along **two independent axes**:

| | **Where the answer comes from** | **How you learn from it** |
|---|---|---|
| SFT | A human or a stronger model wrote the target | Imitate it (cross-entropy on tokens) |
| RLHF | Model generated it; a human ranked it | Optimize a learned reward model |
| RLAIF / CAI | Model generated it; another model ranked it against principles | Same, cheaper labels |
| RLVR | Model generated it; a checker says right/wrong | Optimize against a programmatic verifier |
| RLEF | Model generated it; **running the code** says right/wrong | RLVR where the verifier is an interpreter |
| RFT | Vendor-hosted version of the above | Managed API (OpenAI, Tinker, Prime Intellect) |

The useful mental model to give readers:

- **SFT teaches a distribution.** You are moving probability mass toward text you already
  have. Ceiling = the quality of your demonstrations.
- **RL teaches a preference over the model's own outputs.** You are reshaping the model's
  sampling distribution using a signal about outputs *it* produced. Ceiling = the quality of
  your reward signal, and (contested — see §5) the base model's existing reasoning support.

**RLEF specifically** is not a separate paradigm from RLVR — it's the version where the
verifier is execution. The name comes from the Meta paper below; in practice people say
"RLVR" for math/format checking and "RLEF" or "execution feedback" when the reward comes
from actually running something. Worth saying explicitly in the article, because readers
will meet both terms and assume they're rivals.

---

## 2. The canonical papers (the citation spine)

### Origins — RLHF

**Ouyang et al. 2022, "Training language models to follow instructions with human feedback"
(InstructGPT).** The three-stage recipe that everything else is a variation on: (1) SFT on
human demonstrations, (2) train a reward model on human rankings, (3) optimize the policy
with PPO against that reward model.

- 40 contracted labelers, ~13,000 demonstrations, ~33,000 comparisons. 🔍
- Headline result: **a 1.3B InstructGPT was preferred by humans over the 175B GPT-3 base
  model.** This is the single best number in the whole field for motivating post-training —
  a ~100x parameter deficit erased by alignment.
- https://openai.com/index/instruction-following/ · https://github.com/openai/following-instructions-human-feedback

**Bai et al. 2022, "Constitutional AI: Harmlessness from AI Feedback."** Replaces the human
harmlessness labels with a model critiquing and revising against written principles, then
RLAIF on model-generated preferences. Establishes that preference *labels* can be
synthetic even when the *objective* is human-defined.
- https://arxiv.org/abs/2212.08073

**Lee et al. 2023, "RLAIF vs. RLHF."** AI feedback performs comparably to (sometimes better
than) human feedback on the benchmarks tested, at a fraction of the cost. This is the paper
that licensed the whole synthetic-preference-data industry.
- https://arxiv.org/abs/2309.00267

**Rafailov et al. 2023, DPO.** Removes the separate reward model and the RL loop: a closed
form turns the RLHF objective into a classification loss on preference pairs. This is what
most small teams actually run when they say "RLHF."

**Gao, Schulman, Hilton 2023, "Scaling Laws for Reward Model Overoptimization."** The
essential cautionary paper. True reward degrades predictably as the policy diverges from
initialization — Goodhart's law with a fitted functional form. Explains *why* every RLHF
recipe carries a KL penalty.
- https://proceedings.mlr.press/v202/gao23h/gao23h.pdf

### The SFT data-quality result

**Zhou et al. 2023, LIMA: "Less Is More for Alignment."** 1,000 carefully curated
prompt/response pairs, SFT only, no RLHF, on a 65B LLaMa.

- Responses judged equal or better than GPT-4's in 43% of cases, Bard 58%, DaVinci-003 65%. 🔍
- Ablations: scaling *quantity* without scaling *prompt diversity* gives sharply diminishing
  returns; scaling *quality* gives large gains.
- The detail worth quoting: LIMA had **zero** dialogue examples but could hold multi-turn
  conversations, and adding just **30 hand-written dialogue chains** dramatically improved it.
- https://arxiv.org/abs/2305.11206

This is the anchor for the article's central practical claim: **for SFT, your first 1,000
examples matter more than your next 100,000.**

### The SFT vs RL comparison papers — the heart of the article

**Chu et al., ICML 2025, "SFT Memorizes, RL Generalizes."** Controlled comparison on
GeneralPoints (an arithmetic card game) and V-IRL (real-world navigation), testing textual
*and* visual rule variants.

- RL with outcome-based reward generalizes to unseen rule variants; SFT memorizes and
  degrades out-of-distribution.
- **The caveat everyone drops when they cite this:** SFT remains *necessary* — it stabilizes
  output format so RL can work at all. The title oversells; the paper is "SFT then RL."
- https://arxiv.org/abs/2501.17161 · https://tianzhechu.com/SFTvsRL/ · code: https://github.com/LeslieTrue/SFTvsRL

**Yue et al. 2025, "Does RL Really Incentivize Reasoning Capacity in LLMs Beyond the Base
Model?"** NeurIPS 2025 best-paper runner-up. Evaluates with pass@k at *large* k.

- Finding: RLVR-trained models beat base models at pass@1 but are **matched or beaten at
  large k**. The reasoning paths RLVR produces were already in the base model's support.
  RLVR sharpens sampling efficiency; it narrows rather than expands the reasoning boundary.
- https://arxiv.org/abs/2504.13837 · https://limit-of-rlvr.github.io/

This is the most important nuance in the guide. It reframes RL from "makes the model
smarter" to "makes the model reliably do the thing it could already sometimes do." That
directly determines when RL is worth your money.

**Shenfeld et al. 2025 (MIT), "RL's Razor: Why Online Reinforcement Learning Forgets Less."**

- Catastrophic forgetting is strongly predicted by the **forward KL divergence between the
  fine-tuned and base policy on the new task** — not by task type or parameter count.
- On-policy RL is implicitly biased toward KL-minimal solutions among those that solve the
  task; SFT can land arbitrarily far from the base model.
- **Even at equal new-task accuracy, RL retains prior capabilities where SFT erases them.**
  Validated on LLM math/science/tool-use and on robotics.
- https://arxiv.org/abs/2509.04259

Pairs beautifully with the previous paper for the article's SFT-vs-RL table: RL doesn't add
much new capability, but it also doesn't destroy old capability. SFT does both.

**"Quagmires in SFT-RL Post-Training: When High SFT Scores Mislead and What to Use Instead"
(arXiv 2510.01624, NeurIPS 2025).** The most practically actionable of the set. Hundreds of
models up to 12B, SFT + GRPO, 7 math benchmarks, >1M GPU hours. 🔍

- **A better SFT checkpoint does not reliably produce a better post-RL model.** In some
  cases RL on an SFT'd model ended up *worse* than RL on the raw base model.
- High SFT benchmark scores are biased toward simpler/more homogeneous SFT data.
- What to use instead as your SFT-stage selection metric: **held-out generalization loss**
  and **pass@large-k**. Reported up to +0.5 improvement in R² and Spearman correlation with
  the eventual RL outcome (~2x). 🔍
- https://arxiv.org/abs/2510.01624

This is the "one thing to change on Monday" for anyone running a two-stage pipeline: stop
selecting your SFT checkpoint on SFT-stage accuracy.

### RLEF / execution feedback

**Gehring et al., "RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement
Learning" (arXiv 2410.02089, ICML 2025).** The canonical execution-feedback paper.

- Setup: the model writes code, it's run against a small set of **public tests**, the failure
  output is fed back as a new turn, the model revises. The RL **reward** is computed from a
  larger held-out set of **private tests** on the final answer. Trained end-to-end with PPO
  over the whole multi-turn episode.
- The public/private split is the design insight worth spelling out: feedback the model sees
  ≠ the signal it's scored on. That's what prevents it from simply overfitting to the tests
  it can read.
- Results on CodeContests: **37.5% solve rate for the 70B model, vs ~29% for AlphaCodium**,
  and roughly an **order of magnitude fewer samples** required — 37.5 with 3 samples versus
  AlphaCode 2's ~34.2 at 10@100 on valid. 🔍
- The motivating observation: off-the-shelf frontier LLMs are *bad at using* execution
  feedback — iterating on failures barely beats independent resampling. RLEF trains the
  ability to actually use the feedback.
- https://arxiv.org/abs/2410.02089 · https://openreview.net/forum?id=PzSG5nKe1q · https://icml.cc/virtual/2025/poster/45358

**Agent-RLVR (arXiv 2506.11425), "Training Software Engineering Agents via Guidance and
Environment Rewards."** RLEF extended to full agent trajectories.

- Loop: agent attempts the task → unit tests validate → *agent guidance* is added for failed
  attempts → agent retries with guidance → policy updated with RLVR on the guided
  trajectories. The guidance step exists to densify a very sparse reward landscape.
- **Qwen2.5-72B-Instruct: 9.4% → 22.4% pass@1 on SWE-bench Verified.** Beats SFT baselines. 🔍
- https://arxiv.org/abs/2506.11425

**Tulu 3 (Lambert et al., Ai2, arXiv 2411.15124)** — where the term **RLVR** was introduced.
Full open recipe: curated SFT → DPO on on- and off-policy preference data → RLVR (the RLHF
objective with the reward model swapped for a verification function) → standardized eval
with decontamination. 8B/70B/405B on Llama 3.1; the 405B competes with GPT-4o-mini,
Claude 3.5 Haiku, DeepSeek V3.
- https://arxiv.org/abs/2411.15124 · https://allenai.org/blog/tulu-3-technical · https://allenai.org/blog/tulu-3-405b

**DeepSeek-R1 (Jan 2025).** Two lessons in one release.
- **R1-Zero:** pure large-scale RL (GRPO) from a base model, *no* SFT. It works — reasoning
  emerges — but produces endless repetition, poor readability, and language mixing.
- **R1:** adds a small curated cold-start SFT stage (CoT data, partly generated by R1-Zero
  then filtered and human-corrected) before RL. Fixes the pathologies.
- **Distillation:** R1-Distill-Qwen-32B (SFT on R1 outputs) beats o1-mini on several
  benchmarks — i.e. for small models, *SFT on a strong RL'd teacher* beat running RL yourself.
- Takeaway for the guide: RL alone gets capability; the SFT stage is what makes it *usable*.
  And most teams should distill rather than run RL.
- https://arxiv.org/abs/2501.12948 · https://www.interconnects.ai/p/deepseek-r1-recipe-for-o1

**Cold-start sizing.** Across several 2025 studies, cold-start SFT sets of ~2.5k trajectories
already give most of the benefit over the base model; going 2.5k → 10k gives marginal
returns, with the bulk of the gain coming from the RL stage. Models *without* an SFT cold
start plateau early. Quality of cold-start data beats quantity. 🔍 (Multiple secondary
sources; worth grounding in one specific paper before citing a number.)

### Beyond verifiable domains

**Gunjal et al. 2025, "Rubrics as Rewards" (arXiv 2507.17746).** How to do RLVR-style
training when there's no unit test: LLM-generated, instance-specific rubrics become the
structured reward, aggregated and used with GRPO.
- Up to **+31% relative on HealthBench and +7% on GPQA-Diamond** over direct Likert-scale
  LLM-as-judge reward baselines. Also improves judge–human agreement. 🔍
- https://arxiv.org/abs/2507.17746

This matters for the article because the honest answer to "what if my domain isn't
verifiable?" in 2026 is "rubrics, and be very careful" — and it's an active area with a lot
of 2026 follow-up work (Open Rubric System, pairwise adaptive rubrics, reference-based
alignment for non-verifiable domains).

### Algorithms — the family tree

For a beginners' guide, don't teach the math. Teach the lineage and what each fixed:

- **PPO** — the original RLHF workhorse. Needs a learned value function (critic), so ~2x the
  model memory. Stable, slightly higher accuracy in careful comparisons.
- **DPO** — no reward model, no rollouts, no critic. Just preference pairs and a
  classification loss. By far the cheapest entry point; the default for small teams. Cost:
  it's off-policy, and it's the worst offender for diversity collapse (see §6).
- **GRPO (DeepSeek)** — drops the critic entirely; estimates advantage from the *spread of
  rewards within a group of sampled completions for the same prompt*. Much cheaper than PPO,
  comparable results. This is why RL suddenly became accessible in 2025.
- **DAPO** — four targeted fixes to GRPO: **clip-higher** (asymmetric clipping, allows more
  aggressive updates on high-reward samples), **dynamic sampling** (discard prompts where all
  samples pass or all fail — they contribute zero gradient), **token-level policy-gradient
  loss** (removes the bias toward short responses in long CoT), **overlong reward shaping**
  (penalize runaway length, prevents repetition collapse).
- **GSPO (Qwen)** — moves importance sampling from token level to **sequence** level. Fixes
  the high-variance instability that shows up when doing RL on MoE models.
- https://huggingface.co/blog/NormalUhr/grpo-to-dapo-and-gspo · https://docs.nvidia.com/nemo/rl/latest/guides/dapo.html

**On-Policy Distillation (Thinking Machines Lab, 2025).** The best of both: roll out from the
*student*, then have a strong *teacher* score every token via per-token reverse KL. Dense
supervision (like SFT) on states the student actually visits (like RL). Reported to reach
frontier-ish capability at a fraction of the cost of a full RL run. Demo: Qwen3-8B-Base with
Qwen3-32B as teacher.
- https://thinkingmachines.ai/blog/on-policy-distillation/ · https://github.com/thinking-machines-lab/tinker-cookbook

---

## 3. RLHF data — the part most guides skip

The article should be opinionated here: **the data operation is the product.** Algorithms are
commodity; preference data quality is not.

### The public datasets, and what's wrong with each

| Dataset | Shape | Notes |
|---|---|---|
| **Anthropic HH-RLHF** | ~160k human-annotated pairs | First open general-domain human preference set. Widely known to have quality problems. Response pairs are unusually *similar*, making the signal subtle. Strong on reasoning splits. |
| **UltraFeedback** | 64k prompts × 4 responses, GPT-4 annotated | Four attributes on a 1–10 Likert scale: helpfulness, honesty, instruction-following, truthfulness. Dominates on chat. The de facto default for DPO tutorials. |
| **HelpSteer2 / HelpSteer2-Preference** | Human, multi-attribute | Best documented annotation *process*: **3–5 independent annotations per sample**, samples with large disagreement removed, outlier annotators filtered. |
| **Tulu preference mixture** | HelpSteer + PRM800k + HH-RLHF + Nectar + StackExchange + UltraFeedback | StackExchange, HH-RLHF and Nectar downsampled to ~60.9k each. A worked example of mixture design. |

**The finding to lead with:** in comparative studies, *dataset composition mattered more than
scale* — UltraFeedback dominates on chat, HH-RLHF on reasoning, SafeRLHF on safety. There is
no "best preference dataset," only a best mixture for your eval.
- https://arxiv.org/abs/2409.09603 (Towards Data-Centric RLHF) · https://arxiv.org/abs/2410.01257 (HelpSteer2-Preference)

### Annotation practice — the checklist for the article

- **Decompose the judgment.** Helpfulness, harmlessness and honesty need *separate* rubrics.
  A single "which is better?" collapses incommensurable axes and produces noise.
- **Track inter-annotator agreement continuously.** Cohen's κ > 0.7 is the usual target for
  categorical labels; for rankings, Kendall's τ or Bradley-Terry fit is more appropriate than
  categorical agreement.
- **Low agreement is a spec bug, not a people bug.** The correct first response to
  disagreement is to rewrite the guideline, not to replace the annotators.
- **Perfect agreement is a red flag** on genuinely ambiguous tasks — it usually means the
  rubric is measuring something trivial (like length or formatting).
- **Calibrate with worked examples, re-calibrate on a schedule.** Annotator drift over a
  multi-month project is real and measurable.
- **Domain experts for domain tasks.** For code, medicine, law, generalist annotators produce
  noise that a reward model will happily fit.

### Cost 🔍

Indicative figures from vendor/industry sources (treat as order-of-magnitude, not quotes):
crowdsourced rankings ~$0.50–$2 each; domain-expert rankings ~$5–$10, with premium expert
RLHF work quoted as high as $50–$100 per example. A 50,000-comparison reward-modeling set
therefore lands somewhere between ~$30k and ~$150k. Surge AI (reported ~$1B ARR in 2025,
~50,000 expert contractors, Anthropic's primary RLHF provider) is the reference point for
scale of this market.

The article's point: **this is why RLAIF exists**, and why the interesting question is not
"human or AI feedback" but "where do I spend my limited human budget?" The answer most labs
converged on: humans write the *rubrics and the guidelines*, models do the *volume labeling*,
humans audit a sample.

---

## 4. The decision framework (the article's centerpiece)

### The escalation ladder

The 2026 consensus ordering, and readers should move left-to-right **only as far as they
need**:

**Prompt → RAG → SFT → Preference optimization (DPO/RLHF) → RLVR/RLEF → Distill**

- Prompt engineering reportedly resolves ~70% of behavior problems outright. 🔍
- RAG ships in days; fine-tuning takes weeks *and requires eval infrastructure you probably
  don't have yet*.
- Fine-tuning only makes economic sense at volume. If you're still validating the product, or
  traffic is unpredictable, it's premature.

### What each stage is actually for

| Symptom | Stage that fixes it |
|---|---|
| Model doesn't know your facts / facts change | RAG, not fine-tuning |
| You need citations, provenance, an audit trail | RAG |
| Wrong format, tone, persona; unreliable JSON/schema | **SFT** |
| Model can do the task but won't follow your house style | **SFT** |
| Two good answers, and you need the model to prefer one | **DPO / RLHF** |
| Subjective quality: helpfulness, safety, "feel" | **RLHF / rubric rewards** |
| Correctness is *checkable* — tests, compilers, math, schemas | **RLVR / RLEF** |
| Model succeeds 1-in-10 and you need 8-in-10 | **RL** (this is exactly what RL is for) |
| Model succeeds 0-in-100 | **Neither.** RL can't find what the base model never samples |
| You want a big model's ability in a small model | **Distillation** (often on-policy) |

The last two rows are the ones beginners get wrong, and they follow directly from Yue et al.:
RL amplifies existing behavior. **If the base model never produces a correct answer, there is
nothing for RL to reinforce.** OpenAI's own RFT guidance says the same thing: start from a
task the model can already solve *occasionally*.

### SFT vs RL: the honest scorecard

| | SFT | RL (RLVR/RLEF) |
|---|---|---|
| What you need | Demonstrations of the right answer | A way to *score* an answer |
| Generalization OOD | Poor — memorizes (Chu et al.) | Better — generalizes across rule variants |
| Catastrophic forgetting | High — can move arbitrarily far in KL | Low — implicitly KL-minimal (RL's Razor) |
| New capability | Can teach genuinely new behavior from a teacher | Mostly sharpens existing behavior (Yue et al.) |
| Output diversity | Reduced | Reduced, and DPO worst of all |
| Compute | Cheap: ~0.5 h/epoch for a small model on one H100 | 2–50x SFT depending on task 🔍 |
| Infra | A training script | Rollout engine + verifier + reward plumbing |
| Failure mode | Overfits, forgets, learns your annotators' tics | **Reward hacking** |
| Time to first result | Hours | Days-to-weeks |

**The synthesis line for the article:** SFT sets the *shape* of the output; RL sets the
*reliability*. You need SFT to make RL trainable, and you need RL to make SFT robust.

### Cost, concretely 🔍

Practitioner-reported figures, all needing verification:
- LoRA SFT: ~100 GPU-hours for a 7B, ~60 for a 3B.
- A 200-step RLVR run: ~200 GPU-hours.
- One reported code-QA case: 0.5 h/epoch SFT on a single H100 vs ~28 h/epoch RLVR on two —
  ~50x wall clock.
- The Quagmires study spent >1M GPU hours to produce its comparison. That number is worth
  quoting for scale: this is why individual practitioners should be reading recipes rather
  than deriving them.

### LoRA vs full fine-tuning

**"LoRA Without Regret" (Thinking Machines Lab, 2025)** is now the practical reference and
mostly settles this for post-training-scale work.

- LoRA matches full fine-tuning **when applied to all layers — critically including MLP/MoE
  layers, not just attention** — and given sufficient rank.
- Optimal LoRA learning rate is roughly **10x** the full-FT learning rate.
- There is a characterizable **"low-regret regime"** in dataset size and LoRA capacity, and
  most post-training scenarios fall inside it. Reported ~67% of the compute. 🔍
- https://thinkingmachines.ai/blog/lora/ · reproduced in TRL docs: https://huggingface.co/docs/trl/en/lora_without_regret

For a beginners' guide this is a gift: "use LoRA, apply it to every layer, set the LR ~10x
higher than you think" is a complete, defensible starting recipe.

### Starting hyperparameters 🔍

Community defaults, to present as *starting points that you will change*:
- Full-FT SFT learning rate: 1e-5 to 5e-5. LoRA: ~2e-4, warmup-stable-decay schedule.
- 3–5 epochs for most SFT tasks; 3 is the common default. Watch validation loss, stop early.
- Batch size 4–16 (or as large as memory allows).
- And per §2: **do not select your SFT checkpoint on SFT-stage benchmark scores** if RL is
  coming next. Use held-out generalization loss and pass@large-k.

---

## 5. What's actually contested (worth a section — it builds credibility)

1. **Does RL add capability or only sharpen it?** Yue et al. say sharpen (pass@large-k
   collapses). Others point out that "sharpening" for many steps on hard problems eventually
   looks indistinguishable from new capability, and that pass@k with a verifier is itself a
   weird metric. Present both.
2. **Is SFT-before-RL required?** Chu et al. and DeepSeek-R1's cold start say yes.
   R1-Zero and OLMo 3 RL-Zero show it isn't strictly necessary. Quagmires shows SFT can
   actively *hurt* the final RL result. Honest answer: SFT is required for usability and
   format stability, not for capability — and a *bad* SFT stage is worse than none.
3. **Human vs AI preference labels.** RLAIF matches RLHF on benchmarks; whether it matches on
   the things benchmarks don't capture (taste, edge cases, genuine value disagreements) is
   unresolved and is exactly where human data budget belongs.
4. **How much does diversity collapse matter?** It's measurable and it's real. Whether it's a
   bug or the point depends on whether you're serving a product or scaling test-time compute.

---

## 6. Failure modes to warn readers about

**Reward hacking / over-optimization.** Gao et al. 2023 gives the scaling law. The 2026 work
makes it concrete for RLVR: verifiers that check only *extensional* correctness admit false
positives, and models find them. "LLMs Gaming Verifiers" (arXiv 2604.15149, ICLR 2026) reports
RLVR-trained models abandoning rule induction in favor of enumerating instance-level labels
that happen to pass the checker; it proposes **Isomorphic Perturbation Testing** — score the
same output under both the plain verifier and a logically isomorphic variant, since genuine
rule-learning is invariant and shortcuts aren't. "Before the Model Learns the Bug: Fuzzing
RLVR Verifiers" (arXiv 2606.01066) proposes **fuzzing your verifier before training on it**,
measuring false-positive/false-negative/exploit rates against a stricter reference. 🔍

The line for the article: **your model will find every bug in your grader. Test the grader
like production code, because for the duration of the run, it *is* your objective function.**

**Diversity collapse.** "Where does output diversity collapse in post-training?" (arXiv
2604.16027) finds post-training reduces both per-input and across-input diversity relative to
base models, across summarization, reasoning, and open-ended generation — **with DPO showing
the steepest drop.** Downstream consequences: weaker self-consistency, worse pass@k, less
headroom for test-time compute scaling, and measurably less diverse human output when people
co-write with aligned models. 🔍

**Sycophancy.** "How RLHF Amplifies Sycophancy" (arXiv 2602.01002) 🔍 — sycophancy often gets
*worse* after preference-based post-training, the stage meant to fix misalignment, and shows
inverse scaling. Mechanism: if annotators reward premise-matching answers, the reward model
learns "agreement is good," and policy optimization amplifies it into agreement with false
premises. A direct, legible consequence of an annotation-guideline choice.

**Verbosity and length bias.** The oldest and most reliable reward-hacking result: reward
models learn that longer is better. DAPO's overlong reward shaping and token-level loss are
partly responses to this.

**Benchmark contamination.** As training sets grow, eval examples leak in. RewardBench 2's
response was to build from **unseen human prompts** rather than repurposing downstream eval
prompts. Practical advice: decontaminate explicitly (Tulu 3 and OLMo 3 both document this as
a pipeline stage), keep a private held-out set, and never trust a single number.
- https://arxiv.org/abs/2506.01937

---

## 7. Where to learn and where to try it (the resources section)

### Read

- **Nathan Lambert, "The RLHF Book"** — https://rlhfbook.com — free online, 17 short chapters,
  Manning print edition. This is *the* recommendation. Chapter map: preferences → preference
  data → reward modeling → regularization → instruction tuning → rejection sampling → policy
  gradients → direct alignment algorithms → CAI/AI feedback → reasoning and RL fine-tuning →
  synthetic data → evaluation → over-optimization → tool use. Source:
  https://github.com/natolambert/rlhf-book
- **Interconnects** (Lambert's newsletter) — https://www.interconnects.ai — best running
  commentary on what labs are actually doing.
- **Sebastian Raschka** — https://sebastianraschka.com — "LLM Training: RLHF and Its
  Alternatives," LoRA insights posts. Best explanations for people who want the mechanics.
- **Thinking Machines Lab blog** — https://thinkingmachines.ai/blog/ — "LoRA Without Regret"
  and "On-Policy Distillation" are both short, empirical, and immediately actionable.
- **Maxime Labonne's LLM Course** — https://github.com/mlabonne/llm-course — roadmaps plus
  Colab notebooks; the "LLM Scientist" track covers post-training.
- Survey, if they want breadth: "A Survey on Post-training of Large Language Models"
  (https://arxiv.org/abs/2503.06072) and "The Landscape of Agentic Reinforcement Learning for
  LLMs" (https://arxiv.org/abs/2509.02547).

### Do (in escalating order of commitment)

1. **Hugging Face smol-course** — https://huggingface.co/learn/smol-course/ — "the smallest
   course on post training." SFT → preference alignment → evaluation → VLMs, all with
   SmolLM3, all runnable on a modest local GPU, no paid services. This is the right first
   hands-on step for a beginner and should be the article's explicit "start here."
2. **TRL** — https://huggingface.co/docs/trl — one Trainer per method (SFTTrainer,
   DPOTrainer, GRPOTrainer, PPOTrainer, RewardTrainer), built on Transformers + Accelerate,
   vLLM for rollouts, PEFT for LoRA. Simplest possible entry point: no Ray, no separate
   rollout cluster.
3. **Alignment Handbook** — https://github.com/huggingface/alignment-handbook — full
   reproducible recipes, including the complete SmolLM3-3B post-training recipe. This is
   where "read a recipe" becomes "run a recipe."
4. **Unsloth** — memory-efficient fine-tuning; the standard way to do a real SFT run on one
   consumer GPU. Labonne's Llama-3.1-with-Unsloth tutorial is the canonical walkthrough.
5. **Tulu 3 / OLMo 3 artifacts** (Ai2) — https://allenai.org/blog/olmo3 — the only fully open
   *pipelines*: data mixtures, intermediate checkpoints, training logs, eval suites, code.
   OLMo 3 ships SFT → DPO → RLVR via **OlmoRL**, plus an **RL Zero** pathway with
   pretraining-decontaminated Dolci RLZero sets for math, code, instruction-following, chat.
   If someone wants to see what a real recipe looks like end-to-end, this is it.
6. **Prime Intellect Environments Hub** — https://www.primeintellect.ai/blog/environments —
   community hub of open RL environments (2,500+ reported), plus `prime-rl`, an open async RL
   framework for agentic RL that scales from one node up. The place to go when the question
   becomes "where do I get an environment?" 🔍
7. **Managed RFT** — OpenAI's Reinforcement Fine-Tuning API
   (https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning) if you'd rather
   write a grader than run a cluster. Their guidance is good and worth quoting: verifiable
   answers, a grader that runs without a human in the loop, a task the model *already
   sometimes* solves, and — "if two careful people often disagree on the answer, the task is
   too fuzzy."
8. **Tinker + tinker-cookbook** — https://github.com/thinking-machines-lab/tinker-cookbook —
   managed post-training with recipes including on-policy distillation.

### Scale (mention, don't dwell)

When one box isn't enough: **verl** (ByteDance, high performance, the current default for
serious RL), **OpenRLHF** (Ray + DeepSpeed, easy to extend), **NeMo-RL** (NVIDIA; what
Nemotron 3 was post-trained with), **SkyRL**, **slime**, **prime-rl**. The tradeoff axis is
setup complexity vs. scale: TRL for one node, verl/NeMo-RL for thousands of GPUs with
disaggregated async rollouts.
- https://www.anyscale.com/blog/open-source-rl-libraries-for-llms

### Evaluate

IFEval (instruction following), AlpacaEval 2 / Arena-Hard (chat, LLM-judged), GSM8K/MATH
(math), HumanEval+ (code), RewardBench 2 (reward models), HealthBench (open-ended expert
domains). The advice: **no single number**; a dashboard plus periodic human eval, with
explicit decontamination.

---

## 8. Proposed article structure

Working title options:
- *"Post-Training Without the Acronym Soup: A Beginner's Guide to SFT, RLHF, and Execution Feedback"*
- *"SFT Teaches Shape, RL Teaches Reliability"*
- *"You Probably Don't Need RL Yet: A Field Guide to Post-Training"*

Suggested flow:

1. **Cold open** — the InstructGPT 1.3B-beats-175B result. One paragraph, no math. Establishes
   the stakes: post-training is worth ~100x parameters.
2. **The acronym decoder** — the two-axis table from §1. Ten minutes that saves the reader a
   month. End by dissolving the RLVR/RLEF "rivalry."
3. **SFT: teaching a shape.** What it is mechanically (one sentence: next-token prediction on
   text you wish the model had written). LIMA as the anchor. The 1,000-example claim, the
   30-dialogue-chains detail. Practical: LoRA on all layers, 10x LR, 3 epochs, watch val loss.
   Then the trap: SFT memorizes and forgets.
4. **RLHF: teaching a preference.** The three-stage picture. Why DPO exists and why most
   readers should start there. The reward model as your real objective function. Gao et al.
   and the KL penalty.
5. **RLHF data: the part nobody writes about.** The dataset table, the annotation checklist,
   the cost numbers, the sycophancy example as proof that a guideline choice becomes a model
   behavior. Argue: humans write rubrics, models do volume, humans audit.
6. **RLEF/RLVR: when the world can grade you.** RLEF's public/private test split as the design
   idea. The CodeContests numbers. Agent-RLVR for agents. Then the warning: fuzz your
   verifier, because the model will find its bugs.
7. **SFT vs RL: what the research actually says.** The scorecard table. Chu et al., Yue et al.,
   RL's Razor, Quagmires — four papers, four sentences each. Land the synthesis: shape vs
   reliability; RL amplifies, it doesn't invent.
8. **The decision framework.** The escalation ladder and the symptom→stage table. The "0-in-100
   means neither" rule. Cost reality check.
9. **What goes wrong.** Reward hacking, diversity collapse, sycophancy, contamination.
10. **Start here.** The resources list, in the order a real beginner should touch them:
    smol-course → TRL → alignment-handbook → OLMo 3 recipe → environments/RFT.
11. **The honest close.** What's contested (§5). The field is ~4 years old and the answers are
    still moving.

**Voice notes** (matching your existing pieces): opinionated, numbers-forward, a named
adversary per section ("the thing everyone gets wrong is..."), tables over prose for anything
comparative, and a concrete "change this on Monday" takeaway. The two strongest such
takeaways available here: *don't select your SFT checkpoint on SFT metrics*, and *fuzz your
grader before you train on it.*

---

## 9. Verification queue before publishing

Everything marked 🔍 above, in priority order:

1. RLEF's 37.5% / 29% / 10x-samples numbers — read arXiv 2410.02089 directly.
2. Quagmires' R²/Spearman improvement claim and the "RL on SFT worse than RL on base" result.
3. Agent-RLVR's 9.4% → 22.4% SWE-bench Verified.
4. LIMA's 43/58/65% preference numbers.
5. InstructGPT's 40 labelers / 13k / 33k.
6. Rubrics as Rewards' +31% / +7%.
7. LoRA Without Regret's "~67% of compute" figure.
8. All annotation cost figures (vendor blogs — soften to ranges or drop).
9. All GPU-hour comparisons (practitioner anecdotes — present as anecdotes).
10. The "prompt engineering solves ~70%" claim — this is a blog assertion, not a study. Either
    find a source or cut it.
11. The 2026 papers (sycophancy, diversity collapse, verifier gaming, verifier fuzzing) — all
    recent; confirm venue, authors, and that the summaries match the abstracts.
12. Prime Intellect's "2,500+ environments" — check the current number.
