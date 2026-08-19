# Case Four — LLM serving / prefix-cache failure (see cases/SPEC.md)

CASE = dict(key="serving_cache", label="Case Four",
            title="The prompt change that melted the cache")

SLOTS = {
 "s1": dict(
    case_label="CASE FOUR",
    title="The chat product whose latency doubled while every answer stayed the same",
    key_lesson="Key lesson: identical outputs can hide a broken compute path — trace the cache, not the model.",
 ),
 "s2": dict(
    title="Interviewer opening",
    quote="“Our consumer chat product is timing out. Since 2:10pm yesterday, peak P95 went 2.1s → 4.6s and timeouts 0.2% → 3.1%. Off-peak is almost normal. Quality evals and thumbs rates are flat. GPUs pegged at peak. Diagnose it.”",
    flow1="Translate the contract: fast, correct answers even at peak load",
    flow2="Restate the split: latency + timeouts up, quality flat",
    flow3="Load-shaped failure → think capacity and queues, not correctness",
    flow4="Ask what changed yesterday, and who is not affected",
 ),
 "s3": dict(
    title="How a strong candidate opens",
    quote="“Quality is flat while tail latency and timeouts scale with load. That points at the serving path — throughput and queues — not the model's outputs. I want the latency breakdown: queue wait, prefill, decode, and everything that shipped yesterday afternoon.”",
    beat1="Name product + goal",
    beat2="Split quality from latency",
    beat3="Load-shaped, not global",
    beat4="Ask for latency breakdown",
    beat5="Ask what shipped",
 ),
 "s4": dict(
    title="Flat quality does not clear the serving stack",
    think1="A request pays prefill (read the prompt) then decode (write tokens)",
    think2="Prefix / KV cache reuses attention state for shared prompt prefixes",
    think3="Peak-only pain = a capacity cliff: some resource newly saturates",
    board_label="INCIDENT CARD",
    board="Product: consumer chat, shared GPU pool\nObserved: peak P95 2.1s → 4.6s, timeouts\nQuality: evals + thumbs flat\nOnset: 2:10pm, after an afternoon deploy\nShape: scales with traffic, off-peak ~ok",
    cheat="Which stage newly saturates at peak, and why now?",
    senior="Get the latency breakdown before naming any component",
    nug1="Flat quality clears output not compute",
    nug2="Peak-only pain is a capacity cliff",
    nug3="Latency has stages; get the breakdown",
 ),
 "s5": dict(
    title="Interviewer gives the blast-radius boundary",
    quote="“Only the consumer web surface is slow. API partners send their own prompts to the same GPU pool and are healthy. Mobile lags web by one release and is fine. Severity tracks traffic — worst at peak.”",
    flow1="Same GPUs healthy for partners → not hardware, not model",
    flow2="Predictive condition: requests built with our web template",
    flow3="Lower model-wide and infra-wide theories",
    flow4="Ask what changed in the web template yesterday",
 ),
 "s6": dict(
    title="Turn the boundary into a hypothesis",
    quote="“The same pool serves partners with no pain, so the GPUs and the model are fine. What separates victims is the prompt our web surface builds. A prompt-side change that makes each request more expensive would hit only this surface, and only at peak.”",
    beat1="Affected vs unaffected",
    beat2="Clear the shared layers",
    beat3="Suspect the prompt build",
    beat4="Cost per request, not quality",
 ),
 "s7": dict(
    title="Interviewer hands over the serving metrics",
    subtitle="One affected trace, and the before/after serving counters",
    m1="QUEUE WAIT P95", v1="120ms → 2.9s",
    m2="CACHE HIT RATE", v2="92% → 3%",
    m3="PREFILL TOK/REQ", v3="210 → 3,400",
    m4="DECODE SPEED", v4="38 tok/s → 38",
    trace_label="AFFECTED TRACE",
    chip1="Request built",
    chip2="Prompt assembled",
    chip3="PREFIX CACHE MISS",
    chip4="Full 3.4k prefill",
    chip5="Queue 3.1s",
    chip6="Decode normal",
    bottom="The new cost is upstream of decode: every request re-pays full prefill for the system prompt",
 ),
 "s8": dict(
    title="Make the evidence update explicit",
    quote="“Decode is unchanged, so generation is healthy — that is why quality never moved. The prefix cache stopped hitting, prefill went up ~16x, and the queue is where the latency lives. My fork: did the cache break, or did our prompts stop being cacheable?”",
    beat1="Decode healthy, close it",
    beat2="Cache collapse is the divergence",
    beat3="Queue is symptom, not cause",
    beat4="Fork: cache broken vs key changed",
 ),
 "s9": dict(
    title="Interviewer reveals the rollout and a replay",
    subtitle="Same traffic replayed, one variable: timestamp position",
    colA_label="TIMING",
    colA1="Template v9 at 2:05pm", colA2="100% web at 2:05pm",
    colA3="Incident from 2:10pm", colA4="Peak load 2pm-6pm",
    colB_label="REPLAY FIX",
    colB1="Timestamp at end", colB2="Shared 3.2k prefix",
    colB3="Cache hits 91%", colB4="P95 2.2s",
    colC_label="V9 LIVE",
    colC1="Timestamp on top", colC2="No shared prefix",
    colC3="Cache hits 3%", colC4="P95 4.6s",
 ),
 "s10": dict(
    title="State the causal chain and stop",
    quote="“Template v9 put a per-request timestamp at the top of the system prompt. The prefix cache keys on leading tokens, so no two requests share a prefix: hits fell 92% → 3% and every request re-pays full prefill. At peak that saturates the GPUs, queues build, tails and timeouts explode. Outputs identical — only compute wasted. The replay moving the timestamp restores both.”",
    diag1="Cause: timestamp atop system prompt",
    diag2="Mechanism: prefix-cache key broken",
    diag3="Timing: v9 100% web at 2:05pm",
    diag4="Evidence: one-variable replay",
    diag5="Alternative: cache eviction, ruled out",
 ),
 "s11": dict(
    title="Design cache-aware prompting and a gated rollout",
    subtitle="Stable prefix first, dynamic content last",
    ask="Now design the system that prevents this class",
    arch1_label="PROMPT RULES", arch1="Template linter in CI: dynamic tokens go last",
    arch2_label="GUARDED SLO", arch2="Cache hit rate is an SLO with alerts on collapse",
    arch3_label="ROLLOUT GATE", arch3="Replay prod-like traffic; check hits + tail latency",
    arch4_label="CAPACITY", arch4="Prefill headroom + load shedding at saturation",
    footer="Cheat sheet: prevent · detect · recover. Senior note: capacity plans encode cache assumptions",
 ),
 "s12": dict(
    title="Case Four in six moves",
    subtitle="From “it got slow” to a broken cache key",
    move1="Quality flat, latency load-shaped",
    move2="Only the new-template surface hurts",
    move3="Cache hits 92% → 3%, prefill 16x",
    move4="Queue wait dominates, decode normal",
    move5="Timestamp on top broke the prefix",
    move6="Replay moving it restores latency",
 ),
}

SEGS = [
 # --- Slide 1: divider ---
 dict(id="sc01", slideno=1, kind="teach", speaker="dan",
      text="Case Four. The chat product whose latency doubled, while every answer stayed the same. "
           "The key lesson ahead. Identical outputs can hide a broken compute path. When latency "
           "explodes and quality does not move, trace the serving stack, not the model.",
      spans=[("CASE FOUR", "Case Four."),
             ("latency doubled while every answer", "latency doubled, while every answer"),
             ("Key lesson", "The key lesson ahead")]),

 # --- Slide 2: interviewer opening ---
 dict(id="sc02", slideno=2, kind="attrib", speaker="dan",
      text="The interviewer opens."),
 dict(id="sc03", slideno=2, kind="interviewer", speaker="rachel",
      anchor="Our consumer chat product is timing out",
      text="Our consumer chat product is timing out. Since two ten yesterday afternoon, peak P ninety "
           "five latency went from two point one seconds, to four point six seconds, and the timeout "
           "rate went from a fifth of a percent, to three percent. Off peak looks almost normal. "
           "Answer quality evals, and thumbs down rates, are flat. The G P Us are pegged at peak. "
           "Diagnose it."),
 dict(id="sc04", slideno=2, kind="yourturn", speaker="dan", pause_extra=12,
      text="Pause here. This one is yours first. Take ten seconds, or pause the video, and open the "
           "case out loud. Then compare."),
 dict(id="sc05", slideno=2, kind="teach", speaker="dan",
      text="A strong candidate responds in four moves. "
           "One. Translate the contract. Fast, correct answers, even at peak load. "
           "Two. Restate the split. Latency and timeouts are up, quality is flat. "
           "Three. A load shaped failure points at capacity and queues, not correctness. "
           "Four. Ask what changed yesterday, and who is not affected.",
      spans=[("Translate the contract", "One."),
             ("Restate the split", "Two."),
             ("Load-shaped failure", "Three."),
             ("Ask what changed yesterday", "Four.")]),

 # --- Slide 3: how it sounds out loud ---
 dict(id="sc06", slideno=3, kind="attrib", speaker="dan",
      text="Here is how it sounds out loud."),
 dict(id="sc07", slideno=3, kind="say", speaker="dan",
      anchor="Quality is flat while tail latency",
      text="Quality is flat, while tail latency and timeouts scale with load. That points at the "
           "serving path, throughput and queues, not the model's outputs. I want the latency "
           "breakdown, queue wait, prefill, decode, and I want everything that shipped yesterday "
           "afternoon."),
 dict(id="sc08", slideno=3, kind="teach", speaker="dan",
      text="The response beats. Name the product, and its goal. Split quality from latency. Call the "
           "failure load shaped, not global. Ask for the latency breakdown. And ask what shipped.",
      spans=[("Name product + goal", "Name the product"),
             ("Split quality from latency", "Split quality from latency"),
             ("Load-shaped, not global", "load shaped, not global"),
             ("Ask for latency breakdown", "Ask for the latency breakdown"),
             ("Ask what shipped", "ask what shipped")]),

 # --- Slide 4: thinking + board + rules ---
 dict(id="sc09", slideno=4, kind="attrib", speaker="dan",
      text="And here is what you should be thinking, behind those words."),
 dict(id="sc10", slideno=4, kind="think", speaker="dan",
      text="Serving one oh one. A request pays prefill, where the G P U reads the whole prompt, then "
           "decode, where it writes tokens one at a time. A prefix cache, the K V cache, reuses "
           "computed attention state when requests share the same leading tokens. And peak only pain "
           "means a capacity cliff. Some resource newly saturates under load.",
      spans=[("A request pays prefill", "A request pays prefill"),
             ("KV cache reuses attention state", "A prefix cache"),
             ("Peak-only pain = a capacity cliff", "peak only pain")]),
 dict(id="sc11", slideno=4, kind="teach", speaker="dan",
      anchor="Product: consumer chat",
      text="On your board, the incident card. Product, consumer chat, on a shared G P U pool. "
           "Observed, peak P ninety five, two point one, to four point six seconds, with timeouts. "
           "Quality flat. Onset, two ten yesterday, right after an afternoon deploy. And the shape. "
           "It scales with traffic."),
 dict(id="sc12", slideno=4, kind="rule", speaker="rachel",
      text="The rules. Flat quality clears the output, not the compute. Peak only pain is a capacity "
           "cliff. And latency has stages, so get the breakdown before you name a component.",
      spans=[("Flat quality clears output not compute", "Flat quality clears"),
             ("Peak-only pain is a capacity cliff", "Peak only pain is a capacity cliff"),
             ("Latency has stages", "latency has stages")]),

 # --- Slide 5: blast radius ---
 dict(id="sc13", slideno=5, kind="attrib", speaker="dan",
      text="The interviewer gives the blast radius boundary."),
 dict(id="sc14", slideno=5, kind="interviewer", speaker="rachel",
      anchor="Only the consumer web surface is slow",
      text="Only the consumer web surface is slow. A P I partners, who send their own prompts to the "
           "same G P U pool, are healthy. The mobile app lags web by one release, and it is fine. "
           "Severity tracks traffic. Worst at peak, mild off peak."),
 dict(id="sc15", slideno=5, kind="yourturn", speaker="dan", pause_extra=10,
      text="Your turn again. What just became less likely, and more likely? Ten seconds."),
 dict(id="sc16", slideno=5, kind="teach", speaker="dan",
      text="The strong response, in four moves. "
           "One. The same G P Us serve partners with no pain, so hardware, and the model, are "
           "unlikely. "
           "Two. Name the narrow predictive condition. Requests built with our web prompt template. "
           "Three. Lower every model wide, and infra wide theory. "
           "Four. Ask exactly what changed in the web template yesterday.",
      spans=[("Same GPUs healthy for partners", "One."),
             ("requests built with our web template", "Two."),
             ("Lower model-wide and infra-wide theories", "Three."),
             ("Ask what changed in the web template", "Four.")]),

 # --- Slide 6: out loud ---
 dict(id="sc17", slideno=6, kind="attrib", speaker="dan",
      text="Out loud, that sounds like this."),
 dict(id="sc18", slideno=6, kind="say", speaker="dan",
      anchor="The same pool serves partners",
      text="The same pool serves partners with no pain, so the G P Us and the model are fine. What "
           "separates victims from healthy traffic, is the prompt our web surface builds. A prompt "
           "side change that makes each request more expensive to serve, would hit only this "
           "surface, and only at peak."),
 dict(id="sc19", slideno=6, kind="teach", speaker="dan",
      text="The beats. Summarize affected, versus unaffected. Clear the shared layers explicitly. "
           "Suspect the prompt build. And frame it as cost per request, not quality.",
      spans=[("Affected vs unaffected", "Summarize affected"),
             ("Clear the shared layers", "Clear the shared layers"),
             ("Suspect the prompt build", "Suspect the prompt build"),
             ("Cost per request, not quality", "cost per request, not quality")]),

 # --- Slide 7: serving metrics + trace ---
 dict(id="sc20", slideno=7, kind="attrib", speaker="dan",
      text="The interviewer hands over the serving metrics, and one affected trace."),
 dict(id="sc21", slideno=7, kind="interviewer", speaker="rachel",
      text="Queue wait, at P ninety five. One hundred twenty milliseconds before. Two point nine "
           "seconds after. Prefix cache hit rate. Ninety two percent, falls to three percent. "
           "Prefill tokens per request. Two hundred ten, jumps to three thousand four hundred. "
           "Decode speed. Unchanged, at thirty eight tokens per second. And in your affected trace. "
           "The request is built. The prompt is assembled. Prefix cache miss. Full prefill of the "
           "entire system prompt. Three point one seconds in the queue. Then, decode normal.",
      spans=[("QUEUE WAIT P95", "Queue wait, at P ninety five"),
             ("CACHE HIT RATE", "Prefix cache hit rate"),
             ("PREFILL TOK/REQ", "Prefill tokens per request"),
             ("DECODE SPEED", "Decode speed. Unchanged"),
             ("AFFECTED TRACE", "And in your affected trace"),
             ("PREFIX CACHE MISS", "Prefix cache miss"),
             ("Full 3.4k prefill", "Full prefill of the entire system prompt"),
             ("Queue 3.1s", "Three point one seconds in the queue"),
             ("Decode normal", "decode normal")]),
 dict(id="sc22", slideno=7, kind="yourturn", speaker="dan", pause_extra=10,
      text="Pause. Read the numbers, and call the divergence yourself."),
 dict(id="sc23", slideno=7, kind="teach", speaker="dan",
      anchor="The new cost is upstream of decode",
      text="The new cost is upstream of decode. Every request now re pays full prefill for a large "
           "system prompt, and the queue is where the time goes."),

 # --- Slide 8: evidence update out loud ---
 dict(id="sc24", slideno=8, kind="attrib", speaker="dan",
      text="Here is the evidence update, out loud."),
 dict(id="sc25", slideno=8, kind="say", speaker="dan",
      anchor="Decode is unchanged",
      text="Decode is unchanged, so generation is healthy. That is why quality never moved. The "
           "prefix cache stopped hitting, prefill work went up roughly sixteen fold, and the queue "
           "is where the latency lives. The queue is a symptom of saturation, not a cause. My fork "
           "is. Did the cache itself break, or did our prompts stop being cacheable?"),
 dict(id="sc26", slideno=8, kind="teach", speaker="dan",
      text="The beats. Close decode explicitly. Name the cache collapse as the first divergence. "
           "Call the queue a symptom, not a cause. And state the two way fork. A broken cache, "
           "versus a changed key.",
      spans=[("Decode healthy, close it", "Close decode explicitly"),
             ("Cache collapse is the divergence", "Name the cache collapse"),
             ("Queue is symptom, not cause", "Call the queue a symptom"),
             ("Fork: cache broken vs key changed", "And state the two way fork")]),

 # --- Slide 9: rollout + one-variable replay ---
 dict(id="sc27", slideno=9, kind="attrib", speaker="dan",
      text="The interviewer reveals the rollout, and a one variable replay."),
 dict(id="sc28", slideno=9, kind="interviewer", speaker="rachel",
      text="Template version nine went to one hundred percent of web, at two oh five yesterday. The "
           "incident begins at two ten. Version nine adds a per request timestamp, at the very top "
           "of the system prompt. In the replay, same traffic, one change. With the timestamp moved "
           "to the end, requests share a three thousand two hundred token prefix. Cache hits are "
           "ninety one percent. P ninety five is two point two seconds. With the timestamp on top, "
           "no two requests share a prefix. Hits are three percent. P ninety five is four point six.",
      spans=[("Template v9 at 2:05pm", "Template version nine"),
             ("Incident from 2:10pm", "The incident begins at two ten"),
             ("Timestamp at end", "With the timestamp moved to the end"),
             ("Shared 3.2k prefix", "share a three thousand two hundred token prefix"),
             ("Cache hits 91%", "Cache hits are ninety one percent"),
             ("Timestamp on top", "With the timestamp on top"),
             ("Cache hits 3%", "Hits are three percent")]),
 dict(id="sc29", slideno=9, kind="yourturn", speaker="dan", pause_extra=14,
      text="Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. "
           "Evidence."),

 # --- Slide 10: the diagnosis ---
 dict(id="sc30", slideno=10, kind="attrib", speaker="dan",
      text="Here is the model answer."),
 dict(id="sc31", slideno=10, kind="say", speaker="dan",
      anchor="The prefix cache keys on leading tokens",
      text="The root cause is template version nine, which inserts a per request timestamp at the "
           "top of the system prompt. The prefix cache keys on leading tokens, so no two requests "
           "share a prefix anymore. Hits fell from ninety two percent, to three, and every request "
           "re pays full prefill. At peak, prefill saturates the G P Us, queues build, and tail "
           "latency and timeouts explode. Outputs are identical, because the tokens produced never "
           "changed. Only the compute path broke. The one variable replay, moving the timestamp to "
           "the end, restores hits and latency."),
 dict(id="sc32", slideno=10, kind="teach", speaker="dan",
      text="The final diagnosis card. Cause. A timestamp atop the system prompt. Mechanism. The "
           "prefix cache key is broken. Timing. Version nine hit one hundred percent of web, at two "
           "oh five. Evidence. The one variable replay. Alternative. Cache eviction pressure, ruled "
           "out by that replay.",
      spans=[("Cause: timestamp atop system prompt", "Cause."),
             ("Mechanism: prefix-cache key broken", "Mechanism."),
             ("Timing: v9 100% web at 2:05pm", "Timing."),
             ("Evidence: one-variable replay", "Evidence."),
             ("Alternative: cache eviction, ruled out", "Alternative.")]),

 # --- Slide 11: guard design ---
 dict(id="sc33", slideno=11, kind="attrib", speaker="dan",
      text="Part Two. The interviewer shifts."),
 dict(id="sc34", slideno=11, kind="interviewer", speaker="rachel",
      anchor="Now design the system that prevents this class",
      text="Now design the system that prevents, or safely handles, this class of failure."),
 dict(id="sc35", slideno=11, kind="yourturn", speaker="dan", pause_extra=12,
      text="Your turn. Prevention, detection, recovery. Sketch it out loud."),
 dict(id="sc36", slideno=11, kind="say", speaker="dan",
      anchor="cache-aware prompting",
      text="The general class is. Prompt construction silently changing the cache key. The capacity "
           "plan always assumed high hit rates, so this was a latent vulnerability, and the template "
           "was just the trigger. My red line invariant. No prompt template change ships, without "
           "passing the cache hit, and tail latency gate."),
 dict(id="sc37", slideno=11, kind="say", speaker="dan",
      text="Four parts. One. Prompt rules. Stable prefix first, dynamic content last, enforced by a "
           "template linter in C I. Two. A guarded S L O. Cache hit rate gets alerts, so a collapse "
           "pages someone before users feel it. Three. A rollout gate. Replay production like "
           "traffic, and check hits, and tail latency, before one hundred percent. Four. Capacity. "
           "Prefill headroom, and load shedding, for when saturation hits anyway.",
      spans=[("Stable prefix first, dynamic content last", "Stable prefix first, dynamic content last"),
             ("Template linter in CI", "One. Prompt rules"),
             ("Cache hit rate is an SLO", "Two. A guarded S L O"),
             ("Replay prod-like traffic", "Three. A rollout gate"),
             ("Prefill headroom + load shedding", "Four. Capacity")]),
 dict(id="sc38", slideno=11, kind="rule", speaker="rachel",
      anchor="capacity plans encode cache assumptions",
      text="The rule. Prevent, detect, recover. And remember. Your capacity plan encodes cache "
           "assumptions. Guard them like an S L O."),

 # --- Slide 12: memory close ---
 dict(id="sc39", slideno=12, kind="teach", speaker="dan",
      text="Case Four, in six moves. One. Quality flat, latency load shaped. Two. Only the new "
           "template surface hurts. Three. Cache hits collapse, prefill up sixteen fold. Four. "
           "Queue wait dominates, decode is normal. Five. The timestamp on top broke the shared "
           "prefix. Six. The replay that moves it, restores latency.",
      spans=[("Quality flat, latency load-shaped", "One."),
             ("Only the new-template surface hurts", "Two."),
             ("Cache hits 92% → 3%", "Three."),
             ("Queue wait dominates, decode normal", "Four."),
             ("Timestamp on top broke the prefix", "Five."),
             ("Replay moving it restores latency", "Six.")]),
 dict(id="sc40", slideno=12, kind="rule", speaker="rachel",
      anchor="to a broken cache key",
      text="The final rule. Identical outputs can hide a broken compute path. Put what changes last. "
           "Trace the incident. Then, guard the system."),
 dict(id="sc41", slideno=12, kind="teach", speaker="dan",
      text="That is Case Four. Rerun it tomorrow, pause at every prompt, and beat me to the answer. "
           "Good luck in the room."),
]
