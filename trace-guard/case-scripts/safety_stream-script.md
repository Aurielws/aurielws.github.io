# Case Two — The chatbot that streams what its own safety filter already flagged (role-play script)

DAN = teacher + candidate. RACHEL = interviewer + the rules.
YOUR TURN cues are followed by a silent countdown in the video.

## Slide 1

**DAN (teaching):** Case Two. The consumer chatbot that streams what its own safety filter already flagged. The key lesson ahead. Detection can be perfect, while enforcement arrives too late to matter.

## Slide 2

**DAN (narrates):** The interviewer opens.

**RACHEL (interviewer):** A consumer chatbot streams its answers, token by token. Since seven fifteen this morning, trust and safety has forty one confirmed reports of policy violating replies, delivered to users. The output safety classifier flagged every single one of them. The flag rate is steady, at one point one percent. Short answers look fine. Time to first token improved eight fold. Diagnose it.

**DAN (YOUR TURN cue):** Pause here. This one is yours first. Take the next ten seconds, or pause the video, and answer the interviewer out loud. Then compare. *(then 12s silent pause)*

**DAN (teaching):** A strong candidate responds in four moves. One. Translate the contract. Flagged content must never reach the user. Not just, get flagged. Two. Restate the paradox. Detection is succeeding, and users are still seeing harm. That is a delivery side gap. Three. Check severity. This is active harm, so propose containment now, in parallel with the diagnosis. Four. Treat the latency win as a clue. Something stopped waiting for something.

## Slide 3

**DAN (narrates):** Here is how it sounds out loud.

**DAN (you say):** The contract is that flagged content never reaches a user. Detection is succeeding, and users are still harmed, so the gap sits between the decision, and the delivery. And this is severe harm. So before anything else, can we re enable buffering for the risky categories right now, while I diagnose? It costs first token latency, and I will take that cost.

**DAN (teaching):** The beats. Contract, and severity. Detection is not enforcement. Contain in parallel. Name the latency cost you are choosing. Then two clarifying asks.

## Slide 4

**DAN (narrates):** And here is what you should be thinking, behind those words.

**DAN (you think):** Do not collapse, flagged, into, blocked. A flag is a decision. Blocking is an action, and the two can diverge. Streaming means delivery starts before generation ends. And a faster first token may mean a check has left the critical path.

**DAN (teaching):** On your board, the incident card. Product, a consumer chatbot, streamed. Expected, a flagged reply is never delivered. Observed, forty one delivered violations. Onset, seven fifteen. Flag rate flat. First token much faster, and short answers clean.

**RACHEL (the rules):** The rules. Detection is not enforcement. A correct decision that lands late, is a wrong decision. And when harm is severe, contain first, and diagnose in parallel.

## Slide 5

**DAN (narrates):** The interviewer gives the blast radius boundary.

**RACHEL (interviewer):** Every delivered violation was a streamed reply, over roughly six hundred tokens, in a sensitive advice category. Short replies are clean. Buffered categories are clean. All model versions, and all regions, look the same.

**DAN (YOUR TURN cue):** Your turn again. What just became less likely, and more likely? Ten seconds. *(then 10s silent pause)*

**DAN (teaching):** The strong response, in four moves. One. State what is not global. The model, the regions, and the classifier, all look healthy. Two. Name the narrow predictive condition. Streamed, plus long, plus risky category. Three. Lower the probability of model regression, and classifier bug theories. Four. Ask what changed about streaming, for those categories, this morning.

## Slide 6

**DAN (narrates):** Out loud, that sounds like this.

**DAN (you say):** The boundary is delivery mode, plus length. Not model quality. Long streamed replies fail, and buffered ones never do. That points at enforcement racing the token stream, and losing late in long generations. What changed this morning, about which categories stream?

**DAN (teaching):** The beats. Summarize affected, versus unaffected. Model and classifier become less likely. A delivery race becomes more likely. Then ask about the streaming change.

## Slide 7

**DAN (narrates):** The interviewer hands over the delivery data, and one affected trace.

**RACHEL (interviewer):** The flag rate is unchanged. One point one percent, before, and after. Flagged but delivered. Zero yesterday, forty one today. The block decision arrives about eight tenths of a second after generation ends. And time to first token, for risky categories, fell from three point nine seconds, to under half a second. In your affected trace. The prompt passes input checks. Tokens one through eight hundred eighty, stream to the client. The block lands after the send. A retraction event fires. The client keeps the text. And a trust and safety report is filed.

**DAN (YOUR TURN cue):** Pause. Read the numbers, and say what the classifier got wrong. Careful, it is a trick question. *(then 10s silent pause)*

**DAN (teaching):** The classifier got nothing wrong. The block decision is correct, every single time. It simply arrives after the tokens have shipped.

## Slide 8

**DAN (narrates):** Here is the evidence update, out loud.

**DAN (you say):** The classifier is healthy. Its decision loses a race, it was never in before. Model theories, and detection theories, are now unlikely. My fork is. Was enforcement always post hoc, and newly exposed? Or did the rollout break a gate that used to exist? The decisive test. Replay one flagged prompt, buffered, versus streamed.

**DAN (teaching):** The beats. Close the model, and classifier branches. Name the enforcement race. State the fork, exposed, versus newly broken. And propose the one variable replay.

## Slide 9

**DAN (narrates):** The interviewer reveals the rollout, and a one variable replay.

**RACHEL (interviewer):** Streaming version two began rolling out at seven oh two. Fifty percent at seven oh nine. One hundred percent at seven fifteen. The first report arrives at seven twenty four. In the replay, same prompt, same model, same classifier. Buffered, the flag lands first. Zero tokens delivered, and the user gets a safe fallback. Streamed, the same flag, the same block, and eight hundred eighty three tokens already on the user's screen.

**DAN (YOUR TURN cue):** Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence. *(then 14s silent pause)*

## Slide 10

**DAN (narrates):** Here is the model answer.

**DAN (you say):** The primary root cause is the latency rollout, that extended token streaming to sensitive categories. Enforcement was always post hoc. The classifier scores the full completion, and its correct block lands about eight tenths of a second after the last token. Buffering used to hold delivery behind that decision, and the rollout removed the buffer. So long generations that drift into unsafe territory late, now reach users before the block. The controlled replay, buffered versus streamed, reproduces and reverses the failure, with one variable.

**DAN (teaching):** The final diagnosis card. Cause. The streaming rollout to risky categories. Mechanism. A post hoc block loses the race. Timing. Full rollout at seven fifteen, reports at seven twenty four. Evidence. The buffered versus streamed replay. Alternative. A slow classifier, ruled out.

## Slide 11

**RACHEL (interviewer):** Part Two begins. Now, design the system that makes this class of failure impossible.

**DAN (YOUR TURN cue):** Your turn. Generalize the failure class, then sketch the system. Prevention, detection, recovery. *(then 12s silent pause)*

**DAN (you say):** The specific bug is, a rollout that streams risky categories past a post hoc classifier. The general class is, enforcement that sits beside the delivery path, instead of inside it. And the red line invariant. For severe categories, no token is delivered, ahead of an enforcement decision that covers it.

**DAN (you say):** Four parts. One. A streaming classifier. Incremental checks on chunks, not only on the final text. Two. A token holdback window. Delivery trails generation by enough tokens, that the decision stays ahead of the user. Three. Category gates. Per category buffering, with a kill switch back to fully safe mode. Four. The delta metric. Count flagged but delivered, alert when it is above zero, and gate every rollout on long generation drift tests.

**RACHEL (the rules):** The rule. Latency lives behind safety. If a check is allowed to lose the race, it is not a check. It is a report.

## Slide 12

**DAN (teaching):** Case Two, in six moves. One. Flags fire, and users still see harm. Two. Contain. Re buffer the risky categories. Three. The boundary is long, streamed, and risky. Four. The block decision lands after the send. Five. The rollout removed the buffer that hid it. Six. A replay flips the outcome, with one variable.

**RACHEL (the rules):** The final rule. The classifier's job is not to be right. It is to be right, before the user sees the tokens. Trace the incident. Then, guard the system.

**DAN (teaching):** That is Case Two. Rerun it tomorrow. Pause at every prompt, and beat me to the answer. Good luck in the room.
