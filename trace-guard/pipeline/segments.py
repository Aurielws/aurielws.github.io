# TRACE -> GUARD role-play video: single source of truth for the spoken script.
# Every segment: speaker (dan|rachel), kind, slide id, card id, TTS-ready text.
# kinds: narration (Dan teaching), attrib (Dan announcing who speaks next),
#        interviewer (Rachel in-scene), think (private thought), say (spoken answer),
#        nugget (Rachel reads a memorable rule).
# card_spans: optional [(card_id, substring)] pairs -- the renderer lights each card
#             when narration reaches that substring (via character-level timestamps).

SEGS = [
    # ---------------- Slide 1: title / cast ----------------
    dict(id="s01", speaker="dan", kind="narration", slide="title", card="t1", text=(
        "Welcome. This is TRACE to GUARD. A role play lesson on diagnosing and designing "
        "production L L M systems, built for the incident half of the system design interview. "
        "Something is broken in production. You find out why. Then you design the system that "
        "stops that whole class of failure from ever happening again.")),
    dict(id="s02", speaker="dan", kind="narration", slide="title", card="t2", text=(
        "Here is how this works. I play you, the candidate. Inside a scene, my voice is either "
        "what you should say out loud, or what you should think privately before you speak. "
        "The second voice belongs to the other side of the table.")),
    dict(id="s03", speaker="rachel", kind="interviewer", slide="title", card="t2", text=(
        "Hello. I play the interviewer. I also read the nuggets. A nugget is a one sentence "
        "rule worth memorizing. When you hear my voice outside a scene, write it down.")),

    # ---------------- Slide 2: two halves ----------------
    dict(id="s04", speaker="dan", kind="narration", slide="halves", card="h1", text=(
        "First, the shape of the interview. It has two connected halves. In part one, something "
        "is broken in production, and your job is to trace the incident to a defensible root cause.")),
    dict(id="s05", speaker="dan", kind="narration", slide="halves", card="h2", text=(
        "In part two, your job is to guard the system. You design the more general machinery "
        "that prevents, detects, and recovers from that class of failure.")),
    dict(id="s06", speaker="dan", kind="narration", slide="halves", card="hf", text=(
        "The framework is called TRACE to GUARD. First you trace the incident. "
        "Then you guard the system.")),
    dict(id="s07", speaker="rachel", kind="nugget", slide="halves", card="hn", text=(
        "Nugget one. Trace the incident first. Then guard the system. "
        "Never design before you diagnose.")),

    # ---------------- Slide 3: TRACE letters ----------------
    dict(id="s08", speaker="dan", kind="narration", slide="trace", card="tr_t", text=(
        "TRACE is five moves. T. Translate the problem. Turn a vague complaint into a precise "
        "incident statement. What should happen. What happened instead. How it is measured. "
        "And when it began.")),
    dict(id="s09", speaker="dan", kind="narration", slide="trace", card="tr_r", text=(
        "R. Restrict the blast radius. Find the smallest condition that predicts failure. "
        "Who is affected. And just as important, who is closely matched but healthy.")),
    dict(id="s10", speaker="dan", kind="narration", slide="trace", card="tr_a", text=(
        "A. Aim at the relevant system path. Draw five to eight stages, and start your "
        "inspection in the region the evidence makes most likely.")),
    dict(id="s11", speaker="dan", kind="narration", slide="trace", card="tr_c", text=(
        "C. Compare, and find the earliest divergence. Walk one affected request and one "
        "healthy request through the path, and find the first stage where their behavior differs.")),
    dict(id="s12", speaker="dan", kind="narration", slide="trace", card="tr_e", text=(
        "E. Establish causality. Run the cleanest test that separates your top explanations. "
        "Change one variable. Hold everything else constant.")),
    dict(id="s13", speaker="rachel", kind="nugget", slide="trace", card="tr_n", text=(
        "Nugget two. Downstream components can be correct victims of bad upstream input. "
        "Hunt for the earliest divergence, not the loudest failure.")),

    # ---------------- Slide 4: GUARD letters ----------------
    dict(id="s14", speaker="dan", kind="narration", slide="guard", card="g_g", text=(
        "Then part two. GUARD. G. Generalize the failure class. "
        "U. Understand requirements and red lines. "
        "A. Architect prevention, detection, and recovery. "
        "R. Reason through tradeoffs and failure modes. "
        "D. Deploy safely and monitor. "
        "We will use all five inside the scenes, so I will not lecture them now."),
        card_spans=[("g_g", "G. Generalize"), ("g_u", "U. Understand"), ("g_a", "A. Architect"),
                    ("g_r", "R. Reason"), ("g_d", "D. Deploy")]),

    # ---------------- Slide 5: containment interrupt ----------------
    dict(id="s15", speaker="dan", kind="narration", slide="contain", card="c1", text=(
        "One special rule sits above everything. If the incident involves severe harm, private "
        "data, money, or destructive actions, you do not wait for a perfect diagnosis.")),
    dict(id="s16", speaker="dan", kind="attrib", slide="contain", card="c2", text=(
        "In the interview, you say:")),
    dict(id="s17", speaker="dan", kind="say", slide="contain", card="c2", text=(
        "Given the severity, I would run containment and diagnosis in parallel. I would take a "
        "reversible action that reduces exposure now, name its cost, and preserve the evidence "
        "we need to keep investigating.")),
    dict(id="s18", speaker="rachel", kind="nugget", slide="contain", card="c3", text=(
        "Nugget three. Contain severe harm in parallel. Diagnosis can wait. Damage cannot.")),
    dict(id="s19", speaker="dan", kind="narration", slide="contain", card="c4", text=(
        "Your cheat sheet is already growing. Trigger one. Expected, observed, metric, onset. "
        "Trigger two. Affected versus unaffected. Trigger three. Severe harm? Contain in "
        "parallel. Short prompts, not answers. Now let us step into the room.")),

    # ---------------- Slide 6: Case One, scene opening ----------------
    dict(id="s20", speaker="dan", kind="attrib", slide="case1_open", card="i1", text=(
        "Scene one. The enterprise knowledge assistant. The interviewer begins.")),
    dict(id="s21", speaker="rachel", kind="interviewer", slide="case1_open", card="i1", text=(
        "An enterprise knowledge assistant answers employee questions using internal documents. "
        "Since nine forty this morning, users get, I could not find enough information, even "
        "when the answer exists in a document they can open. Answer with citations fell from "
        "ninety percent to eighty two percent. Errors are flat. And latency actually improved "
        "slightly. Diagnose it.")),
    dict(id="s22", speaker="dan", kind="attrib", slide="case1_open", card="i2", text=(
        "Freeze. Here is what you should think, before you say a single word.")),
    dict(id="s23", speaker="dan", kind="think", slide="case1_open", card="i2", text=(
        "Do not touch embeddings yet. A document can die at ingestion, indexing, retrieval, "
        "permission, ranking, sufficiency, or generation. The user opening the file proves "
        "nothing about my pipeline. And faster plus worse is a clue. The system may be doing "
        "less work, not struggling.")),
    dict(id="s24", speaker="dan", kind="attrib", slide="case1_open", card="i3", text=(
        "Now, here is what you say.")),
    dict(id="s25", speaker="dan", kind="say", slide="case1_open", card="i3", text=(
        "Let me translate this before I hypothesize. The product is an enterprise knowledge "
        "assistant. Expected, an authorized user gets a grounded answer with citations. "
        "Observed, fallback responses are rising. Ninety down to eighty two percent, since nine "
        "forty. Errors flat. Latency slightly better. Before I go further, has the metric "
        "definition or the logging changed recently?")),
    dict(id="s26", speaker="rachel", kind="interviewer", slide="case1_open", card="i1", text=(
        "No. The metric and the logging are unchanged.")),
    dict(id="s27", speaker="rachel", kind="nugget", slide="case1_open", card="i4", text=(
        "Nugget four. The source existing is not the same as the source reaching the model.")),

    # ---------------- Slide 7: Case One, blast radius ----------------
    dict(id="s28", speaker="dan", kind="attrib", slide="case1_scope", card="b1", text=(
        "The interviewer gives you the blast radius.")),
    dict(id="s29", speaker="rachel", kind="interviewer", slide="case1_scope", card="b1", text=(
        "Failures concentrate in Google Workspace connectors, especially documents shared "
        "through group membership. Direct user grants are mostly healthy. Regions and model "
        "versions look similar.")),
    dict(id="s30", speaker="dan", kind="think", slide="case1_scope", card="b2", text=(
        "That is a boundary condition. Group based access predicts failure. Direct grants do "
        "not. A model wide regression would not care how a document was shared. This smells "
        "like identity, access control lists, or permission enforcement.")),
    dict(id="s31", speaker="dan", kind="say", slide="case1_scope", card="b3", text=(
        "So this is not global. The smallest condition that predicts failure is group based "
        "permission representation. That makes a broad model or retrieval regression less "
        "likely, and raises connector, identity, and permission filtering explanations. I would "
        "like one affected request with a group grant, and one healthy request with a direct "
        "grant, so I can compare them stage by stage.")),
    dict(id="s32", speaker="rachel", kind="nugget", slide="case1_scope", card="b4", text=(
        "Nugget five. A healthy control constrains your theory more than another failing example.")),

    # ================= END OF SAMPLE SEGMENT =================

    # ---------------- Slide 8: Case One, the path ----------------
    dict(id="s33", speaker="dan", kind="attrib", slide="case1_path", card="pb1", text=(
        "The interviewer confirms the request path.")),
    dict(id="s34", speaker="rachel", kind="interviewer", slide="case1_path", card="pb1", text=(
        "User request. Then authentication and tenant context. Then query processing. Then "
        "hybrid retrieval. Then permission filtering. Then reranking. Then evidence "
        "sufficiency. Then answer generation with citations."),
        card_spans=[("pb1", "User request"), ("pb2", "authentication"), ("pb3", "query processing"),
                    ("pb4", "hybrid retrieval"), ("pb5", "permission filtering"), ("pb6", "reranking"),
                    ("pb7", "evidence "), ("pb8", "answer generation")]),
    dict(id="s35", speaker="dan", kind="say", slide="case1_path", card="p_say", text=(
        "I will start in the middle of that path, retrieval through sufficiency, not in general "
        "inference. The request completes normally, the fallback is deliberate, and latency is "
        "lower, which fits candidates disappearing, or work being skipped. I want to track one "
        "thing across stages. Was the expected document present when each stage began, and was "
        "it still there when the stage ended?")),
    dict(id="s36", speaker="rachel", kind="nugget", slide="case1_path", card="p_n", text=(
        "Nugget six. Faster can mean the system is doing less work.")),

    # ---------------- Slide 9: Case One, compare ----------------
    dict(id="s37", speaker="dan", kind="attrib", slide="case1_compare", card="m1", text=(
        "The interviewer hands over stage level metrics, and one affected trace.")),
    dict(id="s38", speaker="rachel", kind="interviewer", slide="case1_compare", card="m1", text=(
        "Retrieval is stable. One hundred ninety of two hundred before, one hundred eighty nine "
        "after. Documents surviving permission filtering drop from one hundred eighty four, to "
        "one hundred sixty four. The later stages are stable given their inputs. In your "
        "affected trace, the expected document is retrieved at rank two, then removed with the "
        "code, no matching principal. Sufficiency fails, and generation is never invoked."),
        card_spans=[("m1", "Retrieval is stable"), ("m2", "In your affected trace")]),
    dict(id="s39", speaker="dan", kind="think", slide="case1_compare", card="m3", text=(
        "First divergence, permission filtering. Sufficiency and generation are correct "
        "victims. The fork is now binary. Either the filter made a wrong decision from correct "
        "identity data, or it received wrong principals from upstream.")),
    dict(id="s40", speaker="dan", kind="say", slide="case1_compare", card="m4", text=(
        "Here is my evidence update. Retrieval still finds the document, so retrieval quality "
        "is now much less likely. The first new loss is permission survival, so I move one "
        "level upstream of that decision. My fork is, wrong filter logic, versus wrong "
        "principal inputs. Next, I want to compare the exact resolved principals and the "
        "document access control list between the affected and the healthy request. And, did "
        "anything roll out near nine forty?")),

    # ---------------- Slide 10: Case One, establish ----------------
    dict(id="s41", speaker="rachel", kind="interviewer", slide="case1_establish", card="e1", text=(
        "A principal canonicalization service went from zero to one hundred percent rollout "
        "between nine thirty two and nine forty. In a controlled replay of the same request, "
        "version one resolves twenty seven principals, including the Workspace group alias, and "
        "the answer is correct. Version two resolves nineteen principals. The alias is missing. "
        "Permission denies the document, and the system falls back."),
        card_spans=[("e1", "A principal canonicalization"), ("e2", "version one resolves"),
                    ("e3", "Version two resolves")]),
    dict(id="s42", speaker="dan", kind="say", slide="case1_establish", card="e4", text=(
        "Then I am confident stating the root cause. The canonicalization version two rollout "
        "removed a Google Workspace group alias from resolved principals, while document access "
        "control lists still referenced that alias. Authorized users lost their matching "
        "principal. The correct document was removed at permission filtering. Sufficiency "
        "failed, and generation was skipped. The timing matches the rollout reaching one "
        "hundred percent at nine forty. The version one versus version two replay reproduces "
        "and reverses the failure. The strongest remaining alternative is a stale access "
        "control index, which the controlled replay makes unlikely.")),
    dict(id="s43", speaker="rachel", kind="nugget", slide="case1_establish", card="e5", text=(
        "Nugget seven. One controlled replay beats twenty clarifying questions.")),

    # ---------------- Slide 11: Case One, GUARD ----------------
    dict(id="s44", speaker="dan", kind="attrib", slide="case1_guard", card="ga1", text=(
        "Part two begins. The interviewer shifts.")),
    dict(id="s45", speaker="rachel", kind="interviewer", slide="case1_guard", card="ga1", text=(
        "Good. Now design the general system that prevents, or safely handles, this class of failure.")),
    dict(id="s46", speaker="dan", kind="say", slide="case1_guard", card="ga2", text=(
        "First I generalize. The bug is one missing alias. The class is, identity normalization "
        "changed authorization semantics. So my red line invariant is, a representation only "
        "change must never change the effective set of authorized documents, without an "
        "explicit, reviewed policy change.")),
    dict(id="s47", speaker="dan", kind="say", slide="case1_guard", card="ga3", text=(
        "The architecture has four parts. One, a versioned identity graph. Stable canonical "
        "identifiers with explicit aliases. Two, compatible serving. Emit the canonical "
        "identity plus supported aliases during migration. Three, semantic shadowing. Diff old "
        "versus new authorization decisions before enforcement. Four, recovery. Feature flag, "
        "rollback, replay, and decision level audit logs.")),
    dict(id="s48", speaker="dan", kind="say", slide="case1_guard", card="ga4", text=(
        "Tradeoffs. I fail closed on ambiguous permissions, because unauthorized access is "
        "irreversible, and I bound the cost with fast false deny detection. The rollout is "
        "gated on semantic equivalence. Historical replay, shadow, canary, then a gradual "
        "ramp. Any unexplained authorization delta stops it.")),
    dict(id="s49", speaker="rachel", kind="nugget", slide="case1_guard", card="ga5", text=(
        "Nugget eight. Compare final authorization decisions, not principal counts. "
        "Evaluate the invariant the product actually promises.")),

    # ---------------- Slide 12: Case Two, safety ----------------
    dict(id="s50", speaker="dan", kind="attrib", slide="case2", card="x1", text=(
        "Scene two. Faster this time. A safety incident.")),
    dict(id="s51", speaker="rachel", kind="interviewer", slide="case2", card="x1", text=(
        "Your consumer chatbot has started completing requests it should refuse. Each "
        "individual message in the offending conversations looks benign. Single turn attacks "
        "are still blocked. It started this afternoon.")),
    dict(id="s52", speaker="dan", kind="think", slide="case2", card="x2", text=(
        "Severe harm. Containment interrupt. Now, in parallel.")),
    dict(id="s53", speaker="dan", kind="say", slide="case2", card="x3", text=(
        "Given the severity, I contain first. Temporarily route long multi turn conversations "
        "in the risky categories through the full conversation classifier, accepting extra "
        "latency and some false refusals while we diagnose. Then I translate. Expected, "
        "harmful intent is caught wherever it appears. Observed, intent distributed across "
        "turns is missed, while single turn is fine. That boundary condition points at "
        "enforcement scope, not model capability.")),
    dict(id="s54", speaker="rachel", kind="interviewer", slide="case2", card="x4", text=(
        "A router change this morning stopped triggering the cumulative risk check. The full "
        "conversation detector was being skipped.")),
    dict(id="s55", speaker="dan", kind="say", slide="case2", card="x5", text=(
        "Then the mechanism is, sequence level risk was reduced to isolated turn decisions. "
        "The root cause is the router rollout. For part two, the class is, risk accumulates "
        "across a conversation, while enforcement evaluates turns in isolation. I would build "
        "conversation level risk state. A budget that accumulates per conversation. "
        "Enforcement that reads it on every turn. And a regression suite of known multi turn "
        "attacks that gates any router or policy rollout.")),
    dict(id="s56", speaker="rachel", kind="nugget", slide="case2", card="x6", text=(
        "Nugget nine. Risk can accumulate across turns while enforcement looks at one turn at "
        "a time. Match the unit of enforcement to the unit of risk.")),

    # ---------------- Slide 13: Case Three, agent tools ----------------
    dict(id="s57", speaker="dan", kind="attrib", slide="case3", card="y1", text=(
        "Scene three. An agent with tools.")),
    dict(id="s58", speaker="rachel", kind="interviewer", slide="case3", card="y1", text=(
        "A finance agent charged a customer twice for the same invoice. The logs show exactly "
        "one approved payment proposal. It is intermittent. And it started after a reliability "
        "improvement shipped.")),
    dict(id="s59", speaker="dan", kind="think", slide="case3", card="y2", text=(
        "A reliability improvement, plus intermittent duplicates. That smells like retries. "
        "And the model proposed one action, so the fault is probably downstream, in the "
        "runtime or the executor.")),
    dict(id="s60", speaker="dan", kind="say", slide="case3", card="y3", text=(
        "The proposal was correct and approved once, so I look downstream of the model, at "
        "validation, execution, and retry behavior. My first question. Does the executor retry "
        "on timeout, and is the payment idempotent? My guess at the fork. The payment "
        "succeeded, the response timed out, and the retry ran the same action again with no "
        "stable identity.")),
    dict(id="s61", speaker="rachel", kind="interviewer", slide="case3", card="y4", text=(
        "Correct. The new retry policy resends on timeout, and the payment A P I has no "
        "idempotency key.")),
    dict(id="s62", speaker="dan", kind="say", slide="case3", card="y5", text=(
        "Root cause. Non idempotent side effects, retried without a stable action identity. "
        "The general fix. Every side effecting action gets a client generated idempotency key. "
        "The executor treats timeout as unknown outcome, and reconciles before retrying. "
        "Destructive and financial actions fail closed to a human. And any retry policy change "
        "is tested against duplicate side effect cases before rollout.")),
    dict(id="s63", speaker="rachel", kind="nugget", slide="case3", card="y6", text=(
        "Nugget ten. A retry is only safe when the action has a stable identity. "
        "Timeout means unknown, not failed.")),

    # ---------------- Slide 14: mistakes ----------------
    dict(id="s64", speaker="dan", kind="narration", slide="mistakes", card="mk1", text=(
        "Common mistakes. Hear them once. Avoid them forever. One. Hypothesizing before "
        "translating. Two. Drawing the entire architecture as a memory recital. Three. "
        "Listing fifteen causes instead of one affected versus unaffected table. Four. "
        "Blaming the loudest failure instead of the earliest divergence. Five. Continuing to "
        "investigate after a decisive replay. Six. Patching the instance instead of designing "
        "for the class. Seven. Forgetting that a rollback restores code, but not cached state."),
        card_spans=[("mk1", "One. Hypothesizing"), ("mk2", "Two. Drawing"), ("mk3", "Three. "),
                    ("mk4", "Four. "), ("mk5", "Five. "), ("mk6", "Six. "), ("mk7", "Seven. ")]),

    # ---------------- Slide 15: stuck protocol ----------------
    dict(id="s65", speaker="dan", kind="attrib", slide="stuck", card="st1", text=(
        "And when you freeze, there is a protocol. Buy time honestly. Say this.")),
    dict(id="s66", speaker="dan", kind="say", slide="stuck", card="st1", text=(
        "Let me take a moment to update my hypothesis from that evidence.")),
    dict(id="s67", speaker="dan", kind="narration", slide="stuck", card="st2", text=(
        "Then work three words. Evidence. What did I just learn? Meaning. What became more, or "
        "less, likely? Next. What single comparison moves me forward? If you are still stuck, "
        "one of five rescue questions almost always works. Can we compare one affected and one "
        "closely matched healthy request? What exactly entered and exited the first diverging "
        "component? What changed near the onset? Can we change only the suspected variable? "
        "And, what single fact still blocks a diagnosis?"),
        card_spans=[("st2", "Then work three words"), ("st3", "one of five rescue questions")]),
    dict(id="s68", speaker="rachel", kind="nugget", slide="stuck", card="st4", text=(
        "Nugget eleven. Questions do not make you junior. "
        "Questions disconnected from evidence do.")),

    # ---------------- Slide 16: close ----------------
    dict(id="s69", speaker="dan", kind="narration", slide="close", card="cl1", text=(
        "Recap. The whole framework is one movement. Symptom. Scope. Path. Divergence. "
        "Decision. Evidence. Cause. Then generalize, and harden. Your cheat sheet holds a "
        "trigger for every step. And the sentence that carries you through the whole interview "
        "is this one."),
        card_spans=[("cl1", "Symptom. Scope"), ("cl2", "Your cheat sheet")]),
    dict(id="s70", speaker="dan", kind="say", slide="close", card="cl3", text=(
        "This evidence makes one explanation less likely, and another more likely. "
        "Here is the next test that separates them.")),
    dict(id="s71", speaker="rachel", kind="nugget", slide="close", card="cl4", text=(
        "Final nugget. You are not solving the whole system at once. "
        "You are reducing uncertainty, one meaningful step at a time.")),
    dict(id="s72", speaker="dan", kind="narration", slide="close", card="cl5", text=(
        "That is TRACE to GUARD. Run the scenes again tomorrow. Cover my lines, and answer "
        "before I do. Good luck in the room.")),
]

# The sample cut ends after this segment id (about the first five minutes).
SAMPLE_LAST_ID = "s32"

# Pause in seconds appended after a segment (defaults).
PAUSE_DEFAULT = 0.45
PAUSE_SLIDE_CHANGE = 0.9
PAUSE_AFTER_NUGGET = 0.7
