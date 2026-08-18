# TRACE -> GUARD role-play video, v2: animates the user's own deck (light mode).
# Script text: verbatim from the user's audio teaching script for the framework
# slides; case-study dialogue lifted from the deck's own slide text.
# Roles: DAN = teacher + the candidate (out-loud lines and private thinking).
#        RACHEL = the interviewer (openings/reveals) + reads the rules/nuggets.
#
# Each segment: speaker, kind, slideno (1-based, matches slides_png/s-NN.png),
# anchor (substring of a shape's text on that slide -> reveal + marker), text.
# spans: [(anchor, spoken_substring)] lights several shapes inside one segment,
# timed by the character-level timestamps.

SEGS = [
    # ---- Slide 1: title ----
    dict(id="v01", speaker="dan", kind="teach", slideno=1, anchor=None, text=(
        "Welcome. In this module, we are going to learn a practical framework "
        "for the system design interview.")),

    # ---- Slide 2: two halves (verbatim) ----
    dict(id="v02", speaker="dan", kind="teach", slideno=2,
         anchor="Something is broken in production.", text=(
        "The interview has two connected parts. In Part One, something is broken in "
        "production. Your job is to identify the root cause.")),
    dict(id="v03", speaker="dan", kind="teach", slideno=2,
         anchor="Design for the broader failure class.", text=(
        "In Part Two, your job is to design the more general system that prevents, "
        "detects, or safely handles this class of failure.")),
    dict(id="v04", speaker="dan", kind="teach", slideno=2, anchor=None, text=(
        "The framework is called, TRACE to GUARD. First, you trace the incident. "
        "Then, you guard the system.")),

    # ---- Slide 3: TRACE letters (verbatim) ----
    dict(id="v05", speaker="dan", kind="teach", slideno=3, anchor=None, text=(
        "The letters in TRACE stand for. "
        "T. Translate the problem. "
        "R. Restrict the blast radius. "
        "A. Aim at the relevant system path. "
        "C. Compare, and find the earliest divergence. "
        "E. Establish causality."),
        spans=[("Make the failure precise", "T. Translate"),
               ("Find the smallest affected boundary", "R. Restrict"),
               ("Choose the relevant system path", "A. Aim"),
               ("Find the earliest divergence", "C. Compare"),
               ("Run the decisive causal test", "E. Establish")]),

    # ---- Slide 4: GUARD letters (verbatim) ----
    dict(id="v06", speaker="dan", kind="teach", slideno=4, anchor=None, text=(
        "Then, in Part Two, GUARD stands for. "
        "G. Generalize the failure class. "
        "U. Understand the requirements, and red lines. "
        "A. Architect prevention, detection, and recovery. "
        "R. Reason through tradeoffs and failure modes. "
        "D. Deploy safely, and monitor."),
        spans=[("Name the broader failure class", "G. Generalize"),
               ("Set requirements and red lines", "U. Understand"),
               ("Prevention, detection, recovery", "A. Architect"),
               ("Tradeoffs and failure modes", "R. Reason"),
               ("Evaluation, rollout, monitoring", "D. Deploy")]),

    # ---- Slide 5: containment interrupt (verbatim) ----
    dict(id="v07", speaker="dan", kind="teach", slideno=5, anchor=None, text=(
        "There is also one special rule. If the incident involves severe safety risk, "
        "security, private data, financial loss, destructive tool actions, or another "
        "potentially irreversible harm, you run containment in parallel. You do not "
        "need to know the complete root cause before reducing immediate harm."),
        spans=[("Safety · privacy · financial loss · destructive actions",
                "If the incident involves"),
               ("Rollback · disable · safe fallback · human approval",
                "you run containment in parallel"),
               ("Full traces · examples · configuration · evidence for replay",
                "You do not need to know")]),
    dict(id="v08", speaker="dan", kind="say", slideno=5,
         anchor="Given the severity", text=(
        "In the room, that sounds like. Given the severity, I would run containment "
        "and diagnosis in parallel.")),
    dict(id="v09", speaker="dan", kind="teach", slideno=5, anchor=None, text=(
        "That is the whole structure. Now let us skip ahead, and watch the framework "
        "inside a real interview. Case One.")),

    # ---- Slide 52: case divider ----
    dict(id="v10", speaker="dan", kind="teach", slideno=52,
         anchor="Key lesson", text=(
        "Case One. The enterprise knowledge assistant that suddenly cannot find "
        "existing documents. The key lesson ahead. The user visible symptom looks "
        "like retrieval, but the failure happens in permission semantics."),
        spans=[("Broad complaint", "Case One."),
               ("Key lesson", "The key lesson ahead")]),

    # ---- Slide 53: interviewer opening ----
    dict(id="v11", speaker="dan", kind="attrib", slideno=53, anchor=None, text=(
        "The interviewer opens.")),
    dict(id="v12", speaker="rachel", kind="interviewer", slideno=53,
         anchor="An enterprise knowledge assistant answers employee questions", text=(
        "An enterprise knowledge assistant answers employee questions using internal "
        "documents. Since nine forty, users get, I couldn't find enough information, "
        "even when the answer exists in a document they can open. Answer with "
        "citations fell from ninety percent, to eighty two percent. Errors are flat. "
        "P ninety five latency improved slightly. Diagnose it.")),
    dict(id="v13", speaker="dan", kind="teach", slideno=53, anchor=None, text=(
        "A strong candidate responds in four moves. "
        "One. Translate the product contract. Authorized users should receive "
        "grounded answers, with citations. "
        "Two. Restate the observed outcome, and the exact metric change. "
        "Three. Keep, the user can open the source, separate from, the system "
        "indexed or retrieved it. "
        "Four. Treat faster latency as a clue that the system may be doing less work."),
        spans=[("Translate the product contract", "One."),
               ("Restate the observed outcome", "Two."),
               ("Keep “the user can open the source”", "Three."),
               ("Treat faster latency", "Four.")]),

    # ---- Slide 54: how it sounds out loud ----
    dict(id="v14", speaker="dan", kind="attrib", slideno=54, anchor=None, text=(
        "Here is how it sounds out loud.")),
    dict(id="v15", speaker="dan", kind="say", slideno=54,
         anchor="Let me first translate the incident", text=(
        "Let me first translate the incident into expected, versus observed behavior. "
        "Before I form technical hypotheses, I want to confirm whether the metric "
        "changed, and what, the source exists, actually proves.")),
    dict(id="v16", speaker="dan", kind="teach", slideno=54, anchor=None, text=(
        "The response beats. Name the product, and its goal. Expected versus "
        "observed. Metric, and onset. Qualify the source claim. Then ask two high "
        "value clarifiers."),
        spans=[("Name product + goal", "Name the product"),
               ("Expected vs observed", "Expected versus"),
               ("Metric + onset", "Metric, and onset"),
               ("Qualify the source claim", "Qualify the source"),
               ("Ask two high-value clarifiers", "ask two high")]),

    # ---- Slide 55: what you should be thinking ----
    dict(id="v17", speaker="dan", kind="attrib", slideno=55, anchor=None, text=(
        "And here is what you should be thinking, behind those words.")),
    dict(id="v18", speaker="dan", kind="think", slideno=55, anchor=None, text=(
        "Do not collapse, source exists, into, retrieval worked. A document can fail "
        "at ingestion, indexing, retrieval, permission, ranking, sufficiency, or "
        "generation. Fallback does not prove an empty candidate list. And faster plus "
        "worse, may mean fewer candidates survive, or generation is skipped."),
        spans=[("A document can fail at ingestion", "A document can fail"),
               ("Fallback does not prove an empty candidate list", "Fallback does not prove"),
               ("Faster + worse may mean fewer candidates", "And faster plus worse")]),
    dict(id="v19", speaker="dan", kind="teach", slideno=55,
         anchor="Product: enterprise document QA", text=(
        "On your board, the incident card. Product, enterprise document Q and A. "
        "Expected, an authorized, cited answer. Observed, fallback rising, ninety to "
        "eighty two percent. Onset, nine forty. Errors flat. Latency down.")),
    dict(id="v20", speaker="rachel", kind="rule", slideno=55, anchor=None, text=(
        "The rules. Source exists, is not the same as, source reached the model. "
        "Fallback is an outcome. And faster can mean skipped work."),
        spans=[("Source exists ≠ source reached model", "Source exists"),
               ("Fallback is an outcome", "Fallback is an outcome"),
               ("Faster can mean skipped work", "faster can mean skipped work")]),

    # ---- Slide 56: blast radius ----
    dict(id="v21", speaker="dan", kind="attrib", slideno=56, anchor=None, text=(
        "The interviewer gives the blast radius boundary.")),
    dict(id="v22", speaker="rachel", kind="interviewer", slideno=56,
         anchor="The metric definition is unchanged", text=(
        "The metric definition is unchanged. Failures concentrate in Google Workspace "
        "connectors, especially documents shared through group membership. Direct "
        "user grants are mostly healthy. Regions, and model versions, look similar.")),
    dict(id="v23", speaker="dan", kind="teach", slideno=56, anchor=None, text=(
        "The strong response, in four moves. "
        "One. State what is not global. "
        "Two. Name the narrow predictive condition. Group based access representation. "
        "Three. Lower the probability of model wide, or general retrieval theories. "
        "Four. Ask for a matched healthy request, that differs in permission shape."),
        spans=[("State what is not global.", "One."),
               ("Name the narrow predictive condition", "Two."),
               ("Lower the probability of model-wide", "Three."),
               ("Ask for a matched healthy request", "Four.")]),

    # ---- Slide 57: out loud ----
    dict(id="v24", speaker="dan", kind="attrib", slideno=57, anchor=None, text=(
        "Out loud, that sounds like this.")),
    dict(id="v25", speaker="dan", kind="say", slideno=57,
         anchor="The failure is concentrated in Google Workspace tenants", text=(
        "The failure is concentrated in Google Workspace tenants, where access "
        "depends on group membership. That makes a broad model regression less "
        "likely, and raises connector, identity, A C L, or permission enforcement "
        "explanations. I want a group grant affected request, and a direct grant "
        "healthy control.")),
    dict(id="v26", speaker="dan", kind="teach", slideno=57, anchor=None, text=(
        "The beats. Summarize affected, versus unaffected. Say what becomes less "
        "likely. Say what becomes more likely. Then request a matched control cohort."),
        spans=[("Summarize affected vs unaffected", "Summarize affected"),
               ("Say what becomes less likely", "less likely"),
               ("Say what becomes more likely", "more likely"),
               ("Request a matched control cohort", "request a matched")]),

    # ---- Slide 58: thinking + rules ----
    dict(id="v27", speaker="dan", kind="think", slideno=58, anchor=None, text=(
        "What you should be thinking. The failure is not, all of RAG. The same model "
        "versions work for healthy traffic. And the permission representation, not "
        "the document topic, best predicts failure."),
        spans=[("The failure is not “all RAG.”", "The failure is not"),
               ("Same model versions work for healthy traffic", "The same model versions"),
               ("The permission representation—not the document topic", "And the permission representation")]),
    dict(id="v28", speaker="rachel", kind="rule", slideno=58, anchor=None, text=(
        "The rules. Healthy controls constrain theory. A narrow boundary points to a "
        "narrow subsystem. And a model wide theory struggles here."),
        spans=[("Healthy controls constrain theory", "Healthy controls"),
               ("Narrow boundary → narrow subsystem", "A narrow boundary"),
               ("Model-wide theory struggles here", "And a model wide theory")]),
    dict(id="v29", speaker="dan", kind="teach", slideno=58, anchor=None, text=(
        "That is the end of this demo. The full lesson continues exactly like this, "
        "through the first divergence, the controlled replay, and the guarded system. "
        "See you in the room.")),
]

SAMPLE_LAST_ID = SEGS[-1]["id"]  # the demo IS the sample

PAUSE_DEFAULT = 0.45
PAUSE_SLIDE_CHANGE = 0.9
PAUSE_AFTER_NUGGET = 0.7
