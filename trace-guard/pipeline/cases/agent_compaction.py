# Case Three — agentic harness failure: context compaction drops tool results,
# the agent repeats already-completed side-effecting actions.

CASE = dict(key="agent_compaction", label="Case Three",
            title="The agent that repeats finished work")

SLOTS = {
 "s1": dict(
    case_label="CASE THREE",
    title="The autonomous agent that repeats side effects it already completed",
    key_lesson="Key lesson: the model proposed correctly — the harness rebuilt its memory wrong."),

 "s2": dict(
    title="Interviewer opening",
    quote="“An autonomous ops agent runs long runbooks with side-effecting tools. Since Tuesday it "
          "repeats completed steps — 214 notification emails re-sent, a finished migration step "
          "re-run. Errors flat. Tool success flat. Approvals valid. Duplicate-action rate "
          "0.02% → 3.1% of sessions. Diagnose it.”",
    flow1="Translate the contract: each side-effecting step executes exactly once per runbook.",
    flow2="Restate the anomaly and the exact metric change.",
    flow3="Keep “the action was valid” separate from “the action was needed again.”",
    flow4="Treat the intermittency as data — something state-dependent varies across sessions."),

 "s3": dict(
    title="How a strong candidate opens",
    quote="“Every side-effecting step should execute exactly once. A completed step is being "
          "proposed again later in the same session — and approved, because the action itself is "
          "legitimate. I want the exact onset, and where the duplicates cluster.”",
    beat1="Name product + contract",
    beat2="Expected vs observed",
    beat3="Metric + onset",
    beat4="Valid ≠ needed again",
    beat5="Ask two clarifiers"),

 "s4": dict(
    title="Do not collapse “repeated action” into “model error”",
    think1="A proposal is the output of a loop: context assembly, model, validation.",
    think2="Intermittent + state-dependent points at what varies across sessions.",
    think3="The validator checks legality, not history. What could erase history?",
    board_label="INCIDENT CARD",
    board="Product: autonomous ops agent\n"
          "Expected: each step executes once\n"
          "Observed: completed steps proposed again\n"
          "Onset: Tue · errors flat · approvals valid\n"
          "Severity: high — real side effects",
    cheat="What does the agent see when it decides a step is new?",
    senior="Ask where the agent's memory of completions actually lives.",
    nug1="Valid action ≠ needed action",
    nug2="Intermittent means state-dependent",
    nug3="The model only knows its context"),

 "s5": dict(
    title="Interviewer gives the boundary",
    quote="“Short sessions are clean. Under 30 steps, zero duplicates. Over 60 steps, 19% of "
          "sessions show one. Model, prompts, tools unchanged. Probability grows with session "
          "length.”",
    flow1="State what is not global: short sessions are perfectly healthy.",
    flow2="Name the predictive variable: accumulated session length.",
    flow3="Lower model-regression theories: the same model serves clean sessions.",
    flow4="Ask what the harness does differently when sessions grow long."),

 "s6": dict(
    title="Turn the length gradient into a hypothesis",
    quote="“A long session is required. That lowers model or tool regressions — the same model "
          "serves short sessions cleanly. It raises anything the harness triggers on accumulated "
          "length: truncation, summarization, memory eviction. What fires only when a session "
          "gets long?”",
    beat1="Affected vs unaffected",
    beat2="Less likely: model, tools",
    beat3="More likely: length-triggered",
    beat4="What fires on long context?"),

 "s7": dict(
    title="Interviewer hands over one affected trace",
    subtitle="Session metrics before and after Monday, plus one duplicated-email trace",
    m1="SESSIONS", v1="12k/day, flat",
    m2="DUP ACTIONS", v2="0.02% → 3.1%",
    m3="TOOL FAILS", v3="flat",
    m4="TOKENS/SESSION", v4="down 38%",
    trace_label="AFFECTED TRACE",
    chip1="Step 12: send emails",
    chip2="Result: sent OK",
    chip3="Compaction at step 41",
    chip4="Step 44: proposes again",
    chip5="Validator approves",
    chip6="Emails sent twice",
    bottom="Every duplicated action is proposed only after a compaction event fires in that session."),

 "s8": dict(
    title="Make the update explicit",
    quote="“The duplicate sits downstream of a compaction event, every time. Model and validator "
          "behave, given their inputs. The fork: does compaction corrupt the content of history, "
          "or its ordering? The decisive artifact is a context diff across compaction.”",
    beat1="First divergence: post-compaction",
    beat2="Close model + validator branches",
    beat3="Fork: content vs ordering",
    beat4="Request the compacted-context diff"),

 "s9": dict(
    title="Interviewer reveals the rollout and the replay",
    subtitle="One recorded session, replayed through both compactors, diffed",
    colA_label="TIMING",
    colA1="v2 ships Mon 16:00", colA2="100% by Mon 18:00",
    colA3="First dup Tue 09:12", colA4="Rate grows w/ length",
    colB_label="V1 REPLAY",
    colB1="Keeps tool results", colB2="Ledger intact",
    colB3="No re-proposal", colB4="Dup rate 0.02%",
    colC_label="V2 REPLAY",
    colC1="Drops tool results", colC2="Keeps prose plan",
    colC3="Step 12 looks new", colC4="Dup rate 3.1%"),

 "s10": dict(
    title="State the causal chain and stop",
    quote="“The root cause is the summarizer v2 rollout in the compaction path. Past the context "
          "threshold, v2 keeps the prose plan but drops the structured tool-result records. The "
          "agent loses the evidence that a step completed, re-proposes it, and the runtime "
          "approves a legitimate action. The v1 vs v2 replay diff shows the missing records.”",
    diag1="Cause: v2 summarizer drops tool results",
    diag2="Mechanism: no completion evidence left",
    diag3="Timing: dups begin after Mon rollout",
    diag4="Evidence: v1 vs v2 replay diff",
    diag5="Alternative: planner regression"),

 "s11": dict(
    title="Design so a context optimization cannot change what executes",
    subtitle="Prevention, detection, recovery — and one red line",
    ask="Now design the system that prevents this class",
    arch1_label="COMPACTION CONTRACT",
    arch1="Action ledger — tool calls + results — exempt from summary",
    arch2_label="DURABLE LEDGER",
    arch2="Completions stored outside context, checked at validation",
    arch3_label="IDEMPOTENCY KEYS",
    arch3="Side-effecting calls carry stable per-step keys",
    arch4_label="REPLAY EVALS",
    arch4="Long-session replays gate changes · dup-rate alarm",
    footer="Cheat sheet: What must survive compaction? Senior note: gate side effects outside "
           "the context window."),

 "s12": dict(
    title="Case Three in six moves",
    subtitle="From “the agent went rogue” to a context-assembly bug",
    move1="Duplicate actions look like model bugs",
    move2="Only long sessions are affected",
    move3="Every duplicate follows a compaction",
    move4="v2 summaries drop tool-result records",
    move5="Replay diff pins the missing records",
    move6="Durable ledger + idempotency keys"),
}

SEGS = [
 # --- Slide 1: divider ---
 dict(id="ac01", slideno=1, kind="teach", speaker="dan",
      text="Case Three. The autonomous ops agent that starts repeating side effects it already "
           "completed. Same format as before. When the interviewer finishes a prompt, it is your "
           "turn first. The key lesson ahead. The model proposes correctly, given the context it "
           "sees. The fault lives in the harness that assembles that context.",
      spans=[("The autonomous agent that repeats side effects", "Case Three."),
             ("Key lesson", "The key lesson ahead")]),

 # --- Slide 2: interviewer opening ---
 dict(id="ac02", slideno=2, kind="attrib", speaker="dan",
      text="The interviewer opens."),
 dict(id="ac03", slideno=2, kind="interviewer", speaker="rachel",
      text="An autonomous ops agent platform runs long, multi step runbooks, with side effecting "
           "tools. Since Tuesday, it has been repeating steps it already completed. Two hundred "
           "fourteen notification emails went out a second time. One finished migration "
           "step was re run. Errors are flat. Tool success is flat. Every duplicated action "
           "passed validation. The duplicate action rate went from zero point zero two percent, "
           "to three point one percent of sessions. Diagnose it.",
      anchor="An autonomous ops agent runs long runbooks"),
 dict(id="ac04", slideno=2, kind="yourturn", speaker="dan", pause_extra=12,
      text="Pause here. This one is yours first. Take ten seconds, or pause the video, and give "
           "your opening out loud."),
 dict(id="ac05", slideno=2, kind="teach", speaker="dan",
      text="A strong candidate responds in four moves. One. Translate the product contract. Each "
           "side effecting step should execute exactly once per runbook. Two. Restate the "
           "anomaly, and the exact metric change. Three. Keep, the action was valid, separate "
           "from, the action was needed again. Four. Treat the intermittency as data. Something "
           "state dependent is varying.",
      spans=[("Translate the contract", "One."),
             ("Restate the anomaly", "Two."),
             ("Keep “the action was valid”", "Three."),
             ("Treat the intermittency as data", "Four.")]),

 # --- Slide 3: how it sounds out loud ---
 dict(id="ac06", slideno=3, kind="attrib", speaker="dan",
      text="Here is how it sounds out loud."),
 dict(id="ac07", slideno=3, kind="say", speaker="dan",
      text="Let me restate the contract. Every side effecting step should execute exactly once. "
           "What we observe, is a completed step proposed again later in the same session, and "
           "approved, because the action itself is legitimate. Before I form hypotheses, I want "
           "the exact onset, and whether the duplicates cluster by tool, or by session shape.",
      anchor="Every side-effecting step should execute exactly once"),
 dict(id="ac08", slideno=3, kind="teach", speaker="dan",
      text="The beats. Name the product, and its contract. Expected, versus observed. Metric, "
           "and onset. Keep valid, separate from needed again. Then ask two high value "
           "clarifiers.",
      spans=[("Name product + contract", "Name the product"),
             ("Expected vs observed", "Expected, versus"),
             ("Metric + onset", "Metric, and onset"),
             ("Valid ≠ needed again", "Keep valid"),
             ("Ask two clarifiers", "ask two high value")]),

 # --- Slide 4: what you should be thinking ---
 dict(id="ac09", slideno=4, kind="think", speaker="dan",
      text="Do not collapse, repeated action, into, model error. A proposal is the output of a "
           "whole loop. Context assembly, the model, validation, execution. Intermittent, plus "
           "state dependent, points at whatever varies across sessions. And the validator checks "
           "legality, not history. Ask what could erase the history.",
      spans=[("A proposal is the output of a loop", "A proposal is the output"),
             ("Intermittent + state-dependent", "Intermittent, plus state dependent"),
             ("The validator checks legality, not history", "And the validator checks")]),
 dict(id="ac10", slideno=4, kind="teach", speaker="dan",
      text="On your board, the incident card. Product, autonomous ops agent. Expected, each step "
           "executes once. Observed, completed steps proposed again. Onset, Tuesday. Errors "
           "flat. Approvals valid. Severity, high. These are real side effects.",
      anchor="Product: autonomous ops agent"),
 dict(id="ac11", slideno=4, kind="rule", speaker="rachel",
      text="The rules. A valid action is not a needed action. Intermittent means state "
           "dependent. And the model only knows what its context tells it.",
      spans=[("Valid action ≠ needed action", "A valid action"),
             ("Intermittent means state-dependent", "Intermittent means"),
             ("The model only knows its context", "And the model only knows")]),

 # --- Slide 5: boundary reveal ---
 dict(id="ac12", slideno=5, kind="attrib", speaker="dan",
      text="The interviewer gives the boundary."),
 dict(id="ac13", slideno=5, kind="interviewer", speaker="rachel",
      text="Short sessions are clean. Under thirty steps, zero duplicates. Over sixty steps, "
           "nineteen percent of sessions show at least one. Model version, prompts, and tool "
           "configurations are unchanged. And the probability grows with session length.",
      anchor="Short sessions are clean"),
 dict(id="ac14", slideno=5, kind="yourturn", speaker="dan", pause_extra=10,
      text="Your turn again. What just became less likely, and more likely? Ten seconds."),
 dict(id="ac15", slideno=5, kind="teach", speaker="dan",
      text="The strong response, in four moves. One. State what is not global. Short sessions "
           "are perfectly healthy. Two. Name the predictive variable. Accumulated session "
           "length. Three. Lower model regression theories. The same model serves the clean "
           "sessions. Four. Ask what the harness does differently, when a session grows long.",
      spans=[("State what is not global", "One."),
             ("Name the predictive variable", "Two."),
             ("Lower model-regression theories", "Three."),
             ("Ask what the harness does differently", "Four.")]),

 # --- Slide 6: out loud ---
 dict(id="ac16", slideno=6, kind="attrib", speaker="dan",
      text="Out loud, that sounds like this."),
 dict(id="ac17", slideno=6, kind="say", speaker="dan",
      text="The failure requires a long session. That makes a model, or tool regression, less "
           "likely. The same model and tools serve short sessions cleanly. It raises "
           "anything the harness triggers on accumulated length. Truncation. Summarization. "
           "Memory eviction. So, what fires only when a session gets long?",
      anchor="A long session is required"),
 dict(id="ac18", slideno=6, kind="teach", speaker="dan",
      text="The beats. Summarize affected, versus unaffected. Say what becomes less likely. Say "
           "what becomes more likely. Then ask what fires on long context.",
      spans=[("Affected vs unaffected", "Summarize affected"),
             ("Less likely: model, tools", "less likely"),
             ("More likely: length-triggered", "more likely"),
             ("What fires on long context?", "what fires on long context")]),
 dict(id="ac19", slideno=6, kind="rule", speaker="rachel",
      text="The rule. When a failure scales with accumulated state, inspect the machinery that "
           "manages the state.",
      anchor="What fires on long context?"),

 # --- Slide 7: metrics + affected trace ---
 dict(id="ac20", slideno=7, kind="attrib", speaker="dan",
      text="The interviewer hands over session metrics, and one affected trace."),
 dict(id="ac21", slideno=7, kind="interviewer", speaker="rachel",
      text="Sessions per day, flat. Tool failures, flat. Tokens per "
           "session, down thirty eight percent since Monday. The duplicate action rate, up from "
           "zero point zero two, to three point one percent. And in your affected trace. Step "
           "twelve sends the notification emails. The result comes back, sent, O K. At step "
           "forty one, a compaction event fires. At step forty four, the agent proposes, send "
           "notification emails, again, as if new. The validator approves. The emails go out "
           "twice.",
      spans=[("SESSIONS", "Sessions per day"),
             ("TOOL FAILS", "Tool failures"),
             ("TOKENS/SESSION", "Tokens per session"),
             ("0.02% → 3.1%", "The duplicate action rate"),
             ("AFFECTED TRACE", "And in your affected trace"),
             ("Step 12: send emails", "Step twelve sends"),
             ("Result: sent OK", "The result comes back"),
             ("Compaction at step 41", "At step forty one"),
             ("Step 44: proposes again", "At step forty four"),
             ("Validator approves", "The validator approves"),
             ("Emails sent twice", "The emails go out twice")]),
 dict(id="ac22", slideno=7, kind="yourturn", speaker="dan", pause_extra=10,
      text="Pause. Read the trace, and call the first divergence yourself."),
 dict(id="ac23", slideno=7, kind="teach", speaker="dan",
      text="Every duplicated action is proposed only after a compaction event fires in that "
           "session. The trigger is the compaction. Not the model, and not the validator.",
      anchor="Every duplicated action is proposed only after a compaction event"),

 # --- Slide 8: evidence update out loud ---
 dict(id="ac24", slideno=8, kind="attrib", speaker="dan",
      text="Here is the evidence update, out loud."),
 dict(id="ac25", slideno=8, kind="say", speaker="dan",
      text="The duplicate sits downstream of a compaction event, every time. That makes a model "
           "regression, and a validator bug, less likely. Both behave, given their inputs. My "
           "fork is now. Does compaction corrupt the content of the summarized history? Or the "
           "ordering of what remains? The decisive artifact is a diff of the context, before "
           "and after compaction.",
      anchor="The duplicate sits downstream of a compaction event"),
 dict(id="ac26", slideno=8, kind="teach", speaker="dan",
      text="The beats. State the first divergence. Close the model, and validator branches. Name "
           "the new fork. And request the compacted context diff.",
      spans=[("First divergence: post-compaction", "State the first divergence"),
             ("Close model + validator branches", "Close the model"),
             ("Fork: content vs ordering", "Name the new fork"),
             ("Request the compacted-context diff", "request the compacted context diff")]),

 # --- Slide 9: rollout + one-variable replay ---
 dict(id="ac27", slideno=9, kind="attrib", speaker="dan",
      text="The interviewer reveals the rollout, and a one variable replay."),
 dict(id="ac28", slideno=9, kind="interviewer", speaker="rachel",
      text="Summarizer version two shipped Monday, at sixteen hundred. One hundred percent by "
           "eighteen hundred. The first duplicate appears Tuesday, at nine twelve. In "
           "the replay, one recorded session runs through both compactors. Version one keeps the "
           "structured tool result records. The action ledger is intact. No re proposal. Version "
           "two keeps the assistant's prose plan, but drops the tool result records. Step twelve "
           "looks like it never ran. The agent proposes it again.",
      spans=[("v2 ships Mon 16:00", "Summarizer version two shipped"),
             ("First dup Tue 09:12", "The first duplicate appears"),
             ("Keeps tool results", "Version one keeps"),
             ("Drops tool results", "drops the tool result records"),
             ("Step 12 looks new", "Step twelve looks")]),
 dict(id="ac29", slideno=9, kind="yourturn", speaker="dan", pause_extra=14,
      text="Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. "
           "Evidence."),

 # --- Slide 10: the diagnosis ---
 dict(id="ac30", slideno=10, kind="attrib", speaker="dan",
      text="Here is the model answer."),
 dict(id="ac31", slideno=10, kind="say", speaker="dan",
      text="The primary root cause is the summarizer version two rollout, in the context "
           "compaction path. Past the context window threshold, version two keeps the prose "
           "plan, and silently drops the structured tool result records. The agent loses the "
           "evidence that a completed step ever ran, proposes it again, and the runtime "
           "approves, because the action is legitimate. The controlled replay, version one "
           "versus version two on the same recorded session, reproduces the missing records, and "
           "the duplicate. The model behaved correctly. The fault is upstream, in context "
           "assembly.",
      anchor="The root cause is the summarizer v2 rollout"),
 dict(id="ac32", slideno=10, kind="teach", speaker="dan",
      text="The final diagnosis card. Cause. The version two summarizer drops tool results. "
           "Mechanism. No completion evidence remains in context. Timing. Duplicates begin after "
           "the Monday rollout. Evidence. The version one, versus version two, replay diff. "
           "Alternative. A planner regression. Ruled out by the replay.",
      spans=[("Cause: v2 summarizer drops tool results", "Cause."),
             ("Mechanism: no completion evidence left", "Mechanism."),
             ("Timing: dups begin after Mon rollout", "Timing."),
             ("Evidence: v1 vs v2 replay diff", "Evidence."),
             ("Alternative: planner regression", "Alternative.")]),

 # --- Slide 11: guard design ---
 dict(id="ac33", slideno=11, kind="interviewer", speaker="rachel",
      text="Now design the system that prevents, or safely absorbs, this class of failure.",
      anchor="Now design the system that prevents this class"),
 dict(id="ac34", slideno=11, kind="yourturn", speaker="dan", pause_extra=12,
      text="Your turn. Prevention, detection, recovery, and one red line. Take twelve seconds."),
 dict(id="ac35", slideno=11, kind="say", speaker="dan",
      text="The general class is. A context transformation silently changes the effective memory "
           "that gates side effects. So my red line invariant. A context optimization must never "
           "change which side effecting actions execute.",
      anchor="one red line"),
 dict(id="ac36", slideno=11, kind="say", speaker="dan",
      text="Four parts. One. A compaction contract. The action ledger, tool calls and their "
           "results, is structured state, exempt from summarization. Two. A durable ledger, "
           "outside the context window. Proposal validation consults it, so a duplicate is "
           "blocked even when the context lies. Three. Idempotency keys. Every side effecting "
           "call carries a stable per step key, so a repeat becomes a no op. Four. Replay evals. "
           "Long session replays gate any compactor change, and a duplicate action rate alarm "
           "catches drift.",
      spans=[("COMPACTION CONTRACT", "One. A compaction contract"),
             ("DURABLE LEDGER", "Two. A durable ledger"),
             ("IDEMPOTENCY KEYS", "Three. Idempotency keys"),
             ("REPLAY EVALS", "Four. Replay evals")]),
 dict(id="ac37", slideno=11, kind="rule", speaker="rachel",
      text="The rule. Memory that gates side effects cannot live only in the context window.",
      anchor="gate side effects outside the context window"),

 # --- Slide 12: memory close ---
 dict(id="ac38", slideno=12, kind="teach", speaker="dan",
      text="Case Three, in six moves. One. Duplicate actions look like model bugs. Two. Only "
           "long sessions are affected. Three. Every duplicate follows a compaction. Four. "
           "Version two summaries drop the tool result records. Five. The replay diff pins the "
           "missing records. Six. A durable ledger, and idempotency keys, guard the loop.",
      spans=[("Duplicate actions look like model bugs", "One."),
             ("Only long sessions are affected", "Two."),
             ("Every duplicate follows a compaction", "Three."),
             ("v2 summaries drop tool-result records", "Four."),
             ("Replay diff pins the missing records", "Five."),
             ("Durable ledger + idempotency keys", "Six.")]),
 dict(id="ac39", slideno=12, kind="rule", speaker="rachel",
      text="The final rule. The model can only remember what the harness lets it see. Trace the "
           "incident. Then, guard the system.",
      anchor="to a context-assembly bug"),
 dict(id="ac40", slideno=12, kind="teach", speaker="dan",
      text="That is Case Three. Rerun it tomorrow. Pause at every prompt, and beat me to the "
           "answer."),
]
