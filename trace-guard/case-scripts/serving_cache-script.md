# Case Four — The prompt change that melted the cache (role-play script)

DAN = teacher + candidate. RACHEL = interviewer + the rules.
YOUR TURN cues are followed by a silent countdown in the video.

## Slide 1

**DAN (teaching):** Case Four. The chat product whose latency doubled, while every answer stayed the same. The key lesson ahead. Identical outputs can hide a broken compute path. When latency explodes and quality does not move, trace the serving stack, not the model.

## Slide 2

**DAN (narrates):** The interviewer opens.

**RACHEL (interviewer):** Our consumer chat product is timing out. Since two ten yesterday afternoon, peak P ninety five latency went from two point one seconds, to four point six seconds, and the timeout rate went from a fifth of a percent, to three percent. Off peak looks almost normal. Answer quality evals, and thumbs down rates, are flat. The G P Us are pegged at peak. Diagnose it.

**DAN (YOUR TURN cue):** Pause here. This one is yours first. Take ten seconds, or pause the video, and open the case out loud. Then compare. *(then 12s silent pause)*

**DAN (teaching):** A strong candidate responds in four moves. One. Translate the contract. Fast, correct answers, even at peak load. Two. Restate the split. Latency and timeouts are up, quality is flat. Three. A load shaped failure points at capacity and queues, not correctness. Four. Ask what changed yesterday, and who is not affected.

## Slide 3

**DAN (narrates):** Here is how it sounds out loud.

**DAN (you say):** Quality is flat, while tail latency and timeouts scale with load. That points at the serving path, throughput and queues, not the model's outputs. I want the latency breakdown, queue wait, prefill, decode, and I want everything that shipped yesterday afternoon.

**DAN (teaching):** The response beats. Name the product, and its goal. Split quality from latency. Call the failure load shaped, not global. Ask for the latency breakdown. And ask what shipped.

## Slide 4

**DAN (narrates):** And here is what you should be thinking, behind those words.

**DAN (you think):** Serving one oh one. A request pays prefill, where the G P U reads the whole prompt, then decode, where it writes tokens one at a time. A prefix cache, the K V cache, reuses computed attention state when requests share the same leading tokens. And peak only pain means a capacity cliff. Some resource newly saturates under load.

**DAN (teaching):** On your board, the incident card. Product, consumer chat, on a shared G P U pool. Observed, peak P ninety five, two point one, to four point six seconds, with timeouts. Quality flat. Onset, two ten yesterday, right after an afternoon deploy. And the shape. It scales with traffic.

**RACHEL (the rules):** The rules. Flat quality clears the output, not the compute. Peak only pain is a capacity cliff. And latency has stages, so get the breakdown before you name a component.

## Slide 5

**DAN (narrates):** The interviewer gives the blast radius boundary.

**RACHEL (interviewer):** Only the consumer web surface is slow. A P I partners, who send their own prompts to the same G P U pool, are healthy. The mobile app lags web by one release, and it is fine. Severity tracks traffic. Worst at peak, mild off peak.

**DAN (YOUR TURN cue):** Your turn again. What just became less likely, and more likely? Ten seconds. *(then 10s silent pause)*

**DAN (teaching):** The strong response, in four moves. One. The same G P Us serve partners with no pain, so hardware, and the model, are unlikely. Two. Name the narrow predictive condition. Requests built with our web prompt template. Three. Lower every model wide, and infra wide theory. Four. Ask exactly what changed in the web template yesterday.

## Slide 6

**DAN (narrates):** Out loud, that sounds like this.

**DAN (you say):** The same pool serves partners with no pain, so the G P Us and the model are fine. What separates victims from healthy traffic, is the prompt our web surface builds. A prompt side change that makes each request more expensive to serve, would hit only this surface, and only at peak.

**DAN (teaching):** The beats. Summarize affected, versus unaffected. Clear the shared layers explicitly. Suspect the prompt build. And frame it as cost per request, not quality.

## Slide 7

**DAN (narrates):** The interviewer hands over the serving metrics, and one affected trace.

**RACHEL (interviewer):** Queue wait, at P ninety five. One hundred twenty milliseconds before. Two point nine seconds after. Prefix cache hit rate. Ninety two percent, falls to three percent. Prefill tokens per request. Two hundred ten, jumps to three thousand four hundred. Decode speed. Unchanged, at thirty eight tokens per second. And in your affected trace. The request is built. The prompt is assembled. Prefix cache miss. Full prefill of the entire system prompt. Three point one seconds in the queue. Then, decode normal.

**DAN (YOUR TURN cue):** Pause. Read the numbers, and call the divergence yourself. *(then 10s silent pause)*

**DAN (teaching):** The new cost is upstream of decode. Every request now re pays full prefill for a large system prompt, and the queue is where the time goes.

## Slide 8

**DAN (narrates):** Here is the evidence update, out loud.

**DAN (you say):** Decode is unchanged, so generation is healthy. That is why quality never moved. The prefix cache stopped hitting, prefill work went up roughly sixteen fold, and the queue is where the latency lives. The queue is a symptom of saturation, not a cause. My fork is. Did the cache itself break, or did our prompts stop being cacheable?

**DAN (teaching):** The beats. Close decode explicitly. Name the cache collapse as the first divergence. Call the queue a symptom, not a cause. And state the two way fork. A broken cache, versus a changed key.

## Slide 9

**DAN (narrates):** The interviewer reveals the rollout, and a one variable replay.

**RACHEL (interviewer):** Template version nine went to one hundred percent of web, at two oh five yesterday. The incident begins at two ten. Version nine adds a per request timestamp, at the very top of the system prompt. In the replay, same traffic, one change. With the timestamp moved to the end, requests share a three thousand two hundred token prefix. Cache hits are ninety one percent. P ninety five is two point two seconds. With the timestamp on top, no two requests share a prefix. Hits are three percent. P ninety five is four point six.

**DAN (YOUR TURN cue):** Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence. *(then 14s silent pause)*

## Slide 10

**DAN (narrates):** Here is the model answer.

**DAN (you say):** The root cause is template version nine, which inserts a per request timestamp at the top of the system prompt. The prefix cache keys on leading tokens, so no two requests share a prefix anymore. Hits fell from ninety two percent, to three, and every request re pays full prefill. At peak, prefill saturates the G P Us, queues build, and tail latency and timeouts explode. Outputs are identical, because the tokens produced never changed. Only the compute path broke. The one variable replay, moving the timestamp to the end, restores hits and latency.

**DAN (teaching):** The final diagnosis card. Cause. A timestamp atop the system prompt. Mechanism. The prefix cache key is broken. Timing. Version nine hit one hundred percent of web, at two oh five. Evidence. The one variable replay. Alternative. Cache eviction pressure, ruled out by that replay.

## Slide 11

**DAN (narrates):** Part Two. The interviewer shifts.

**RACHEL (interviewer):** Now design the system that prevents, or safely handles, this class of failure.

**DAN (YOUR TURN cue):** Your turn. Prevention, detection, recovery. Sketch it out loud. *(then 12s silent pause)*

**DAN (you say):** The general class is. Prompt construction silently changing the cache key. The capacity plan always assumed high hit rates, so this was a latent vulnerability, and the template was just the trigger. My red line invariant. No prompt template change ships, without passing the cache hit, and tail latency gate.

**DAN (you say):** Four parts. One. Prompt rules. Stable prefix first, dynamic content last, enforced by a template linter in C I. Two. A guarded S L O. Cache hit rate gets alerts, so a collapse pages someone before users feel it. Three. A rollout gate. Replay production like traffic, and check hits, and tail latency, before one hundred percent. Four. Capacity. Prefill headroom, and load shedding, for when saturation hits anyway.

**RACHEL (the rules):** The rule. Prevent, detect, recover. And remember. Your capacity plan encodes cache assumptions. Guard them like an S L O.

## Slide 12

**DAN (teaching):** Case Four, in six moves. One. Quality flat, latency load shaped. Two. Only the new template surface hurts. Three. Cache hits collapse, prefill up sixteen fold. Four. Queue wait dominates, decode is normal. Five. The timestamp on top broke the shared prefix. Six. The replay that moves it, restores latency.

**RACHEL (the rules):** The final rule. Identical outputs can hide a broken compute path. Put what changes last. Trace the incident. Then, guard the system.

**DAN (teaching):** That is Case Four. Rerun it tomorrow, pause at every prompt, and beat me to the answer. Good luck in the room.
