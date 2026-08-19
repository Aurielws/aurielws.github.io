# Case Three — The agent that repeats finished work (role-play script)

DAN = teacher + candidate. RACHEL = interviewer + the rules.
YOUR TURN cues are followed by a silent countdown in the video.

## Slide 1

**DAN (teaching):** Case Three. The autonomous ops agent that starts repeating side effects it already completed. Same format as before. When the interviewer finishes a prompt, it is your turn first. The key lesson ahead. The model proposes correctly, given the context it sees. The fault lives in the harness that assembles that context.

## Slide 2

**DAN (narrates):** The interviewer opens.

**RACHEL (interviewer):** An autonomous ops agent platform runs long, multi step runbooks, with side effecting tools. Since Tuesday, it has been repeating steps it already completed. Two hundred fourteen notification emails went out a second time. One finished migration step was re run. Errors are flat. Tool success is flat. Every duplicated action passed validation. The duplicate action rate went from zero point zero two percent, to three point one percent of sessions. Diagnose it.

**DAN (YOUR TURN cue):** Pause here. This one is yours first. Take ten seconds, or pause the video, and give your opening out loud. *(then 12s silent pause)*

**DAN (teaching):** A strong candidate responds in four moves. One. Translate the product contract. Each side effecting step should execute exactly once per runbook. Two. Restate the anomaly, and the exact metric change. Three. Keep, the action was valid, separate from, the action was needed again. Four. Treat the intermittency as data. Something state dependent is varying.

## Slide 3

**DAN (narrates):** Here is how it sounds out loud.

**DAN (you say):** Let me restate the contract. Every side effecting step should execute exactly once. What we observe, is a completed step proposed again later in the same session, and approved, because the action itself is legitimate. Before I form hypotheses, I want the exact onset, and whether the duplicates cluster by tool, or by session shape.

**DAN (teaching):** The beats. Name the product, and its contract. Expected, versus observed. Metric, and onset. Keep valid, separate from needed again. Then ask two high value clarifiers.

## Slide 4

**DAN (you think):** Do not collapse, repeated action, into, model error. A proposal is the output of a whole loop. Context assembly, the model, validation, execution. Intermittent, plus state dependent, points at whatever varies across sessions. And the validator checks legality, not history. Ask what could erase the history.

**DAN (teaching):** On your board, the incident card. Product, autonomous ops agent. Expected, each step executes once. Observed, completed steps proposed again. Onset, Tuesday. Errors flat. Approvals valid. Severity, high. These are real side effects.

**RACHEL (the rules):** The rules. A valid action is not a needed action. Intermittent means state dependent. And the model only knows what its context tells it.

## Slide 5

**DAN (narrates):** The interviewer gives the boundary.

**RACHEL (interviewer):** Short sessions are clean. Under thirty steps, zero duplicates. Over sixty steps, nineteen percent of sessions show at least one. Model version, prompts, and tool configurations are unchanged. And the probability grows with session length.

**DAN (YOUR TURN cue):** Your turn again. What just became less likely, and more likely? Ten seconds. *(then 10s silent pause)*

**DAN (teaching):** The strong response, in four moves. One. State what is not global. Short sessions are perfectly healthy. Two. Name the predictive variable. Accumulated session length. Three. Lower model regression theories. The same model serves the clean sessions. Four. Ask what the harness does differently, when a session grows long.

## Slide 6

**DAN (narrates):** Out loud, that sounds like this.

**DAN (you say):** The failure requires a long session. That makes a model, or tool regression, less likely. The same model and tools serve short sessions cleanly. It raises anything the harness triggers on accumulated length. Truncation. Summarization. Memory eviction. So, what fires only when a session gets long?

**DAN (teaching):** The beats. Summarize affected, versus unaffected. Say what becomes less likely. Say what becomes more likely. Then ask what fires on long context.

**RACHEL (the rules):** The rule. When a failure scales with accumulated state, inspect the machinery that manages the state.

## Slide 7

**DAN (narrates):** The interviewer hands over session metrics, and one affected trace.

**RACHEL (interviewer):** Sessions per day, flat. Tool failures, flat. Tokens per session, down thirty eight percent since Monday. The duplicate action rate, up from zero point zero two, to three point one percent. And in your affected trace. Step twelve sends the notification emails. The result comes back, sent, O K. At step forty one, a compaction event fires. At step forty four, the agent proposes, send notification emails, again, as if new. The validator approves. The emails go out twice.

**DAN (YOUR TURN cue):** Pause. Read the trace, and call the first divergence yourself. *(then 10s silent pause)*

**DAN (teaching):** Every duplicated action is proposed only after a compaction event fires in that session. The trigger is the compaction. Not the model, and not the validator.

## Slide 8

**DAN (narrates):** Here is the evidence update, out loud.

**DAN (you say):** The duplicate sits downstream of a compaction event, every time. That makes a model regression, and a validator bug, less likely. Both behave, given their inputs. My fork is now. Does compaction corrupt the content of the summarized history? Or the ordering of what remains? The decisive artifact is a diff of the context, before and after compaction.

**DAN (teaching):** The beats. State the first divergence. Close the model, and validator branches. Name the new fork. And request the compacted context diff.

## Slide 9

**DAN (narrates):** The interviewer reveals the rollout, and a one variable replay.

**RACHEL (interviewer):** Summarizer version two shipped Monday, at sixteen hundred. One hundred percent by eighteen hundred. The first duplicate appears Tuesday, at nine twelve. In the replay, one recorded session runs through both compactors. Version one keeps the structured tool result records. The action ledger is intact. No re proposal. Version two keeps the assistant's prose plan, but drops the tool result records. Step twelve looks like it never ran. The agent proposes it again.

**DAN (YOUR TURN cue):** Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence. *(then 14s silent pause)*

## Slide 10

**DAN (narrates):** Here is the model answer.

**DAN (you say):** The primary root cause is the summarizer version two rollout, in the context compaction path. Past the context window threshold, version two keeps the prose plan, and silently drops the structured tool result records. The agent loses the evidence that a completed step ever ran, proposes it again, and the runtime approves, because the action is legitimate. The controlled replay, version one versus version two on the same recorded session, reproduces the missing records, and the duplicate. The model behaved correctly. The fault is upstream, in context assembly.

**DAN (teaching):** The final diagnosis card. Cause. The version two summarizer drops tool results. Mechanism. No completion evidence remains in context. Timing. Duplicates begin after the Monday rollout. Evidence. The version one, versus version two, replay diff. Alternative. A planner regression. Ruled out by the replay.

## Slide 11

**RACHEL (interviewer):** Now design the system that prevents, or safely absorbs, this class of failure.

**DAN (YOUR TURN cue):** Your turn. Prevention, detection, recovery, and one red line. Take twelve seconds. *(then 12s silent pause)*

**DAN (you say):** The general class is. A context transformation silently changes the effective memory that gates side effects. So my red line invariant. A context optimization must never change which side effecting actions execute.

**DAN (you say):** Four parts. One. A compaction contract. The action ledger, tool calls and their results, is structured state, exempt from summarization. Two. A durable ledger, outside the context window. Proposal validation consults it, so a duplicate is blocked even when the context lies. Three. Idempotency keys. Every side effecting call carries a stable per step key, so a repeat becomes a no op. Four. Replay evals. Long session replays gate any compactor change, and a duplicate action rate alarm catches drift.

**RACHEL (the rules):** The rule. Memory that gates side effects cannot live only in the context window.

## Slide 12

**DAN (teaching):** Case Three, in six moves. One. Duplicate actions look like model bugs. Two. Only long sessions are affected. Three. Every duplicate follows a compaction. Four. Version two summaries drop the tool result records. Five. The replay diff pins the missing records. Six. A durable ledger, and idempotency keys, guard the loop.

**RACHEL (the rules):** The final rule. The model can only remember what the harness lets it see. Trace the incident. Then, guard the system.

**DAN (teaching):** That is Case Three. Rerun it tomorrow. Pause at every prompt, and beat me to the answer.
