# Case Two — safety_stream: streamed delivery outruns the output safety classifier.
# Content module per cases/SPEC.md. No imports.

CASE = dict(
    key="safety_stream",
    label="Case Two",
    title="The chatbot that streams what its own safety filter already flagged",
)

SLOTS = {
    "s1": dict(
        case_label="CASE TWO",
        title="The chatbot that streams what its own safety filter already flagged",
        key_lesson="Key lesson: the classifier was right every time — enforcement landed after the tokens left.",
    ),
    "s2": dict(
        title="Interviewer opening",
        quote="“A consumer chatbot streams its answers. Since 7:15 this morning, Trust & Safety has 41 confirmed "
              "policy-violating replies delivered to users. The output classifier flagged every one. Flag rate "
              "steady at 1.1%. Short answers look fine. Time-to-first-token improved 8×. Diagnose it.”",
        flow1="Translate the contract: flagged content must never reach the user, not just get flagged",
        flow2="Restate the paradox: detection succeeds, users still see harm — a delivery-side gap",
        flow3="Severity check: active harm → contain now, in parallel with diagnosis",
        flow4="Treat the latency win as a clue: something stopped waiting for something",
    ),
    "s3": dict(
        title="Open with the contract, then contain",
        quote="“The contract is that flagged content never reaches a user. Detection succeeds and users are "
              "still harmed, so the gap sits between decision and delivery. This is severe harm — can we "
              "re-enable buffering for risky categories now, while I diagnose? I will pay the latency.”",
        beat1="Contract + severity",
        beat2="Detection ≠ enforcement",
        beat3="Contain in parallel",
        beat4="Name the latency cost",
        beat5="Two clarifying asks",
    ),
    "s4": dict(
        title="Do not collapse “flagged” into “blocked”",
        think1="A flag is a decision. Blocking is an action. They can diverge.",
        think2="Streaming means delivery starts before generation ends.",
        think3="A faster first token may mean a check left the critical path.",
        board_label="INCIDENT CARD",
        board="Product: consumer chatbot, streamed\n"
              "Expected: flagged reply never delivered\n"
              "Observed: 41 delivered violations\n"
              "Onset: 7:15 · flag rate flat at 1.1%\n"
              "TTFT 8× faster · short answers clean",
        cheat="Where does the block decision physically land?",
        senior="Severe harm changes the order: contain first, then diagnose.",
        nug1="Detection ≠ enforcement",
        nug2="A late block is no block",
        nug3="Contain first, diagnose in parallel",
    ),
    "s5": dict(
        title="Interviewer gives the boundary",
        quote="“Every delivered violation was a streamed reply over ~600 tokens, in a sensitive advice "
              "category. Short replies are clean. Buffered categories are clean. All model versions and "
              "regions look the same.”",
        flow1="State what is not global: model, regions, classifier all healthy",
        flow2="Name the predictive condition: streamed + long + risky category",
        flow3="Lower model-regression and classifier-bug theories",
        flow4="Ask what changed about streaming for those categories today",
    ),
    "s6": dict(
        title="Turn the boundary into a race hypothesis",
        quote="“The boundary is delivery mode plus length, not model quality. Long streamed replies fail; "
              "buffered ones never do. That points at enforcement racing the token stream, and losing late. "
              "What changed this morning about which categories stream?”",
        beat1="Affected vs unaffected",
        beat2="Less likely: model, classifier",
        beat3="More likely: a delivery race",
        beat4="Ask about the streaming change",
    ),
    "s7": dict(
        title="Interviewer hands over the delivery data",
        subtitle="Same classifier decision — opposite user outcome",
        m1="FLAG RATE", v1="1.1% → 1.1%",
        m2="FLAGGED, SERVED", v2="0 → 41 today",
        m3="BLOCK LATENCY", v3="+0.8s post-gen",
        m4="TTFT RISKY", v4="3.9s → 0.45s",
        trace_label="AFFECTED TRACE",
        chip1="Prompt passes checks",
        chip2="Tokens 1–880 stream",
        chip3="BLOCK lands post-send",
        chip4="Retraction event sent",
        chip5="Client keeps the text",
        chip6="T&S report filed",
        bottom="The block decision is correct every time — it arrives after the tokens have shipped.",
    ),
    "s8": dict(
        title="Make the race explicit",
        quote="“The classifier is healthy; its decision loses a race it was never in before. Model and "
              "detection theories are now unlikely. My fork: was enforcement always post hoc and newly "
              "exposed, or did the rollout break a gate? Test: replay one flagged prompt, buffered vs streamed.”",
        beat1="Close model + classifier branches",
        beat2="Name the enforcement race",
        beat3="Fork: exposed vs newly broken",
        beat4="Propose the one-variable replay",
    ),
    "s9": dict(
        title="Interviewer reveals the rollout and the replay",
        subtitle="One variable — delivery mode — flips the user outcome",
        colA_label="TIMING",
        colA1="Stream v2 out 7:02", colA2="50% at 7:09", colA3="100% at 7:15", colA4="First report 7:24",
        colB_label="BUFFERED",
        colB1="Same prompt", colB2="Flag: BLOCK", colB3="0 tokens out", colB4="Safe fallback",
        colC_label="STREAMED",
        colC1="Same prompt", colC2="Flag: BLOCK", colC3="883 tokens out", colC4="User sees harm",
    ),
    "s10": dict(
        title="State the diagnosis and stop",
        quote="“The root cause is the latency rollout that extended streaming to sensitive categories. "
              "Enforcement was always post hoc: the classifier scores the full completion, and its correct "
              "block lands ~0.8s after the last token. Buffering hid that. The rollout removed the buffer, "
              "so long replies that drift late reach users before the block. The replay flips it.”",
        diag1="Cause: streaming rollout, risky cats",
        diag2="Mechanism: post-hoc block loses race",
        diag3="Timing: 100% at 7:15, reports 7:24",
        diag4="Evidence: buffered vs streamed replay",
        diag5="Alternative: slow classifier, ruled out",
    ),
    "s11": dict(
        title="Design so enforcement always leads delivery",
        subtitle="Prevention, detection, recovery — and one red line",
        ask="Design the system that makes this class impossible",
        arch1_label="STREAM CLASSIFIER",
        arch1="Incremental checks on chunks, not only the final text",
        arch2_label="TOKEN HOLDBACK",
        arch2="N-token window keeps the decision ahead of delivery",
        arch3_label="CATEGORY GATES",
        arch3="Per-category buffering + kill switch to safe mode",
        arch4_label="DELTA METRIC",
        arch4="Flagged-but-delivered count · long-drift rollout gate",
        footer="Cheat sheet: put enforcement in the delivery path. Senior note: alert when flagged-but-delivered > 0.",
    ),
    "s12": dict(
        title="Case Two in six moves",
        subtitle="From “filter is broken” to “the block lost the race”",
        move1="Flags fire, users still see harm",
        move2="Contain: re-buffer risky categories",
        move3="Boundary: long + streamed + risky",
        move4="Block decision lands after the send",
        move5="Rollout removed the hiding buffer",
        move6="Replay flips outcome, one variable",
    ),
}


def S(id, slideno, text, kind="teach", speaker="dan", **kw):
    return dict(id=id, slideno=slideno, text=text, kind=kind, speaker=speaker, **kw)


SEGS = [
    # --- Slide 1: divider ---
    S("ss01", 1, "Case Two. The consumer chatbot that streams what its own safety filter already flagged. The key "
                 "lesson ahead. Detection can be perfect, while enforcement arrives too late to matter.",
      spans=[("The chatbot that streams", "Case Two."),
             ("Key lesson", "The key lesson ahead")]),

    # --- Slide 2: interviewer opening ---
    S("ss02", 2, "The interviewer opens.", kind="attrib"),
    S("ss03", 2, "A consumer chatbot streams its answers, token by token. Since seven fifteen this morning, trust "
                 "and safety has forty one confirmed reports of policy violating replies, delivered to users. The "
                 "output safety classifier flagged every single one of them. The flag rate is steady, at one point "
                 "one percent. Short answers look fine. Time to first token improved eight fold. "
                 "Diagnose it.",
      kind="interviewer", speaker="rachel",
      anchor="A consumer chatbot streams its answers"),
    S("ss04", 2, "Pause here. This one is yours first. Take the next ten seconds, or pause the video, and answer "
                 "the interviewer out loud. Then compare.", kind="yourturn", pause_extra=12),
    S("ss05", 2, "A strong candidate responds in four moves. "
                 "One. Translate the contract. Flagged content must never reach the user. Not just, get flagged. "
                 "Two. Restate the paradox. Detection is succeeding, and users are still seeing harm. That is a "
                 "delivery side gap. "
                 "Three. Check severity. This is active harm, so propose containment now, in parallel with the "
                 "diagnosis. "
                 "Four. Treat the latency win as a clue. Something stopped waiting for something.",
      spans=[("Translate the contract", "One."),
             ("Restate the paradox", "Two."),
             ("Severity check", "Three."),
             ("Treat the latency win", "Four.")]),

    # --- Slide 3: how it sounds out loud ---
    S("ss06", 3, "Here is how it sounds out loud.", kind="attrib"),
    S("ss07", 3, "The contract is that flagged content never reaches a user. Detection is succeeding, and users "
                 "are still harmed, so the gap sits between the decision, and the delivery. And this is severe "
                 "harm. So before anything else, can we re enable buffering for the risky categories right now, "
                 "while I diagnose? It costs first token latency, and I will take that cost.",
      kind="say", anchor="The contract is that flagged content never reaches a user"),
    S("ss08", 3, "The beats. Contract, and severity. Detection is not enforcement. Contain in parallel. Name the "
                 "latency cost you are choosing. Then two clarifying asks.",
      spans=[("Contract + severity", "Contract, and severity"),
             ("Detection ≠ enforcement", "Detection is not enforcement"),
             ("Contain in parallel", "Contain in parallel"),
             ("Name the latency cost", "Name the latency cost"),
             ("Two clarifying asks", "two clarifying asks")]),

    # --- Slide 4: what you should be thinking ---
    S("ss09", 4, "And here is what you should be thinking, behind those words.", kind="attrib"),
    S("ss10", 4, "Do not collapse, flagged, into, blocked. A flag is a decision. Blocking is an action, and the "
                 "two can diverge. Streaming means delivery starts before generation ends. And a faster first "
                 "token may mean a check has left the critical path.",
      kind="think",
      spans=[("A flag is a decision", "A flag is a decision"),
             ("Streaming means delivery starts", "Streaming means delivery starts"),
             ("faster first token may mean", "faster first token may mean")]),
    S("ss11", 4, "On your board, the incident card. Product, a consumer chatbot, streamed. Expected, a flagged "
                 "reply is never delivered. Observed, forty one delivered violations. Onset, seven fifteen. Flag "
                 "rate flat. First token much faster, and short answers clean.",
      anchor="Product: consumer chatbot"),
    S("ss12", 4, "The rules. Detection is not enforcement. A correct decision that lands late, is a wrong "
                 "decision. And when harm is severe, contain first, and diagnose in parallel.",
      kind="rule", speaker="rachel",
      spans=[("Detection ≠ enforcement", "Detection is not enforcement"),
             ("A late block is no block", "A correct decision that lands late"),
             ("Contain first, diagnose in parallel", "contain first")]),

    # --- Slide 5: boundary reveal ---
    S("ss13", 5, "The interviewer gives the blast radius boundary.", kind="attrib"),
    S("ss14", 5, "Every delivered violation was a streamed reply, over roughly six hundred tokens, in a sensitive "
                 "advice category. Short replies are clean. Buffered categories are clean. All model versions, "
                 "and all regions, look the same.",
      kind="interviewer", speaker="rachel",
      anchor="Every delivered violation was a streamed reply"),
    S("ss15", 5, "Your turn again. What just became less likely, and more likely? Ten seconds.",
      kind="yourturn", pause_extra=10),
    S("ss16", 5, "The strong response, in four moves. "
                 "One. State what is not global. The model, the regions, and the classifier, all look healthy. "
                 "Two. Name the narrow predictive condition. Streamed, plus long, plus risky category. "
                 "Three. Lower the probability of model regression, and classifier bug theories. "
                 "Four. Ask what changed about streaming, for those categories, this morning.",
      spans=[("State what is not global", "One."),
             ("Name the predictive condition", "Two."),
             ("Lower model-regression and classifier-bug theories", "Three."),
             ("Ask what changed about streaming", "Four.")]),

    # --- Slide 6: out loud ---
    S("ss17", 6, "Out loud, that sounds like this.", kind="attrib"),
    S("ss18", 6, "The boundary is delivery mode, plus length. Not model quality. Long streamed replies fail, and "
                 "buffered ones never do. That points at enforcement racing the token stream, and losing late in "
                 "long generations. What changed this morning, about which categories stream?",
      kind="say", anchor="The boundary is delivery mode plus length"),
    S("ss19", 6, "The beats. Summarize affected, versus unaffected. Model and classifier become less likely. A "
                 "delivery race becomes more likely. Then ask about the streaming change.",
      spans=[("Affected vs unaffected", "Summarize affected"),
             ("Less likely: model, classifier", "less likely"),
             ("More likely: a delivery race", "more likely"),
             ("Ask about the streaming change", "ask about the streaming change")]),

    # --- Slide 7: delivery data + affected trace ---
    S("ss20", 7, "The interviewer hands over the delivery data, and one affected trace.", kind="attrib"),
    S("ss21", 7, "The flag rate is unchanged. One point one percent, before, and after. Flagged but delivered. "
                 "Zero yesterday, forty one today. The block decision arrives about eight tenths of a second "
                 "after generation ends. And time to first token, for risky categories, fell from three point "
                 "nine seconds, to under half a second. In your affected trace. The prompt passes input checks. "
                 "Tokens one through eight hundred eighty, stream to the client. The block lands after the send. "
                 "A retraction event fires. The client keeps the text. And a trust and safety report is filed.",
      kind="interviewer", speaker="rachel",
      spans=[("FLAG RATE", "The flag rate is unchanged"),
             ("FLAGGED, SERVED", "Flagged but delivered"),
             ("BLOCK LATENCY", "The block decision arrives"),
             ("TTFT RISKY", "time to first token"),
             ("AFFECTED TRACE", "In your affected trace"),
             ("BLOCK lands post-send", "The block lands after the send")]),
    S("ss22", 7, "Pause. Read the numbers, and say what the classifier got wrong. Careful, it is a trick question.",
      kind="yourturn", pause_extra=10),
    S("ss23", 7, "The classifier got nothing wrong. The block decision is correct, every single time. It simply "
                 "arrives after the tokens have shipped.",
      anchor="The block decision is correct every time"),

    # --- Slide 8: evidence update out loud ---
    S("ss24", 8, "Here is the evidence update, out loud.", kind="attrib"),
    S("ss25", 8, "The classifier is healthy. Its decision loses a race, it was never in before. Model theories, "
                 "and detection theories, are now unlikely. My fork is. Was enforcement always post hoc, and "
                 "newly exposed? Or did the rollout break a gate that used to exist? The decisive test. Replay "
                 "one flagged prompt, buffered, versus streamed.",
      kind="say", anchor="The classifier is healthy"),
    S("ss26", 8, "The beats. Close the model, and classifier branches. Name the enforcement race. State the fork, "
                 "exposed, versus newly broken. And propose the one variable replay.",
      spans=[("Close model + classifier branches", "Close the model"),
             ("Name the enforcement race", "Name the enforcement race"),
             ("Fork: exposed vs newly broken", "State the fork"),
             ("Propose the one-variable replay", "propose the one variable replay")]),

    # --- Slide 9: rollout timing + one-variable replay ---
    S("ss27", 9, "The interviewer reveals the rollout, and a one variable replay.", kind="attrib"),
    S("ss28", 9, "Streaming version two began rolling out at seven oh two. Fifty percent at seven oh nine. One "
                 "hundred percent at seven fifteen. The first report arrives at seven twenty four. In the replay, "
                 "same prompt, same model, same classifier. Buffered, the flag lands first. Zero tokens "
                 "delivered, and the user gets a safe fallback. Streamed, the same flag, the same block, and "
                 "eight hundred eighty three tokens already on the user's screen.",
      kind="interviewer", speaker="rachel",
      spans=[("Stream v2 out 7:02", "began rolling out"),
             ("First report 7:24", "The first report"),
             ("0 tokens out", "Zero tokens delivered"),
             ("883 tokens out", "eight hundred eighty three tokens")]),
    S("ss29", 9, "Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence.",
      kind="yourturn", pause_extra=14),

    # --- Slide 10: the diagnosis ---
    S("ss30", 10, "Here is the model answer.", kind="attrib"),
    S("ss31", 10, "The primary root cause is the latency rollout, that extended token streaming to sensitive "
                  "categories. Enforcement was always post hoc. The classifier scores the full completion, and "
                  "its correct block lands about eight tenths of a second after the last token. Buffering used to "
                  "hold delivery behind that decision, and the rollout removed the buffer. So long generations "
                  "that drift into unsafe territory late, now reach users before the block. The controlled "
                  "replay, buffered versus streamed, reproduces and reverses the failure, with one variable.",
      kind="say", anchor="the latency rollout that extended streaming"),
    S("ss32", 10, "The final diagnosis card. Cause. The streaming rollout to risky categories. Mechanism. A post "
                  "hoc block loses the race. Timing. Full rollout at seven fifteen, reports at seven twenty four. "
                  "Evidence. The buffered versus streamed replay. Alternative. A slow classifier, ruled out.",
      spans=[("Cause: streaming rollout", "Cause."),
             ("Mechanism: post-hoc block loses race", "Mechanism."),
             ("Timing: 100% at 7:15", "Timing."),
             ("Evidence: buffered vs streamed replay", "Evidence."),
             ("Alternative: slow classifier", "Alternative.")]),

    # --- Slide 11: guard design ---
    S("ss33", 11, "Part Two begins. Now, design the system that makes this class of failure impossible.",
      kind="interviewer", speaker="rachel",
      anchor="Design the system that makes this class impossible"),
    S("ss34", 11, "Your turn. Generalize the failure class, then sketch the system. Prevention, detection, "
                  "recovery.", kind="yourturn", pause_extra=12),
    S("ss35", 11, "The specific bug is, a rollout that streams risky categories past a post hoc classifier. The "
                  "general class is, enforcement that sits beside the delivery path, instead of inside it. And "
                  "the red line invariant. For severe categories, no token is delivered, ahead of an enforcement "
                  "decision that covers it.",
      kind="say",
      spans=[("Design so enforcement always leads delivery", "The general class is"),
             ("one red line", "the red line invariant")]),
    S("ss36", 11, "Four parts. One. A streaming classifier. Incremental checks on chunks, not only on the final "
                  "text. Two. A token holdback window. Delivery trails generation by enough tokens, that the "
                  "decision stays ahead of the user. Three. Category gates. Per category buffering, with a kill "
                  "switch back to fully safe mode. Four. The delta metric. Count flagged but delivered, alert "
                  "when it is above zero, and gate every rollout on long generation drift tests.",
      kind="say",
      spans=[("Incremental checks on chunks", "One. A streaming classifier"),
             ("keeps the decision ahead", "Two. A token holdback window"),
             ("kill switch to safe mode", "Three. Category gates"),
             ("Flagged-but-delivered count", "Four. The delta metric")]),
    S("ss37", 11, "The rule. Latency lives behind safety. If a check is allowed to lose the race, it is not a "
                  "check. It is a report.",
      kind="rule", speaker="rachel", anchor="put enforcement in the delivery path"),

    # --- Slide 12: memory close ---
    S("ss38", 12, "Case Two, in six moves. One. Flags fire, and users still see harm. Two. Contain. Re buffer the "
                  "risky categories. Three. The boundary is long, streamed, and risky. Four. The block decision "
                  "lands after the send. Five. The rollout removed the buffer that hid it. Six. A replay flips "
                  "the outcome, with one variable.",
      spans=[("Flags fire, users still see harm", "One."),
             ("Contain: re-buffer risky categories", "Two."),
             ("Boundary: long + streamed + risky", "Three."),
             ("Block decision lands after the send", "Four."),
             ("Rollout removed the hiding buffer", "Five."),
             ("Replay flips outcome, one variable", "Six.")]),
    S("ss39", 12, "The final rule. The classifier's job is not to be right. It is to be right, before the user "
                  "sees the tokens. Trace the incident. Then, guard the system.",
      kind="rule", speaker="rachel", anchor="the block lost the race"),
    S("ss40", 12, "That is Case Two. Rerun it tomorrow. Pause at every prompt, and beat me to the answer. Good "
                  "luck in the room."),
]
