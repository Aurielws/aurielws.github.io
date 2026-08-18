# TRACE -> GUARD, FULL VIDEO.
# Part A (slides 1-49): the user's audio teaching script, verbatim (TTS-spoken forms),
#   taught by DAN. Slides animate automatically row by row.
# Part B (slides 52-74): Case One as interactive role-play.
#   RACHEL = interviewer prompts + the rules. DAN = teaching, "how it sounds out
#   loud" (say), and "what you should be thinking" (think).
#   After every interviewer prompt: a YOUR TURN cue + silent countdown pause
#   (pause_extra seconds) so the viewer answers out loud first.

def S(id, slideno, text, kind="teach", speaker="dan", anchor=None, spans=None, pause_extra=0):
    d = dict(id=id, slideno=slideno, text=text, kind=kind, speaker=speaker)
    if anchor: d["anchor"] = anchor
    if spans: d["spans"] = spans
    if pause_extra: d["pause_extra"] = pause_extra
    return d

SEGS = [
# ======================= PART A — THE MODULE (slides 1-49) =======================
S("v01", 1, "Welcome. In this module, we are going to learn a practical framework for the system design interview."),

S("v02", 2, "The interview has two connected parts. In Part One, something is broken in production. Your job is to identify the root cause.",
  anchor="Something is broken in production."),
S("v03", 2, "In Part Two, your job is to design the more general system that prevents, detects, or safely handles this class of failure.",
  anchor="Design for the broader failure class."),
S("v04", 2, "The framework is called, TRACE to GUARD. First, you trace the incident. Then, you guard the system."),

S("v05", 3, "The letters in TRACE stand for. "
            "T. Translate the problem. "
            "R. Restrict the blast radius. "
            "A. Aim at the relevant system path. "
            "C. Compare, and find the earliest divergence. "
            "E. Establish causality.",
  spans=[("Make the failure precise", "T. Translate"),
         ("Find the smallest affected boundary", "R. Restrict"),
         ("Choose the relevant system path", "A. Aim"),
         ("Find the earliest divergence", "C. Compare"),
         ("Run the decisive causal test", "E. Establish")]),

S("v06", 4, "Then, in Part Two, GUARD stands for. "
            "G. Generalize the failure class. "
            "U. Understand the requirements, and red lines. "
            "A. Architect prevention, detection, and recovery. "
            "R. Reason through tradeoffs and failure modes. "
            "D. Deploy safely, and monitor.",
  spans=[("Name the broader failure class", "G. Generalize"),
         ("Set requirements and red lines", "U. Understand"),
         ("Prevention, detection, recovery", "A. Architect"),
         ("Tradeoffs and failure modes", "R. Reason"),
         ("Evaluation, rollout, monitoring", "D. Deploy")]),

S("v07", 5, "There is also one special rule. If the incident involves severe safety risk, "
            "security, private data, financial loss, destructive tool actions, or another "
            "potentially irreversible harm, you run containment in parallel. You do not "
            "need to know the complete root cause before reducing immediate harm.",
  spans=[("Safety · privacy · financial loss · destructive actions", "If the incident involves"),
         ("Rollback · disable · safe fallback · human approval", "you run containment in parallel"),
         ("Full traces · examples · configuration · evidence for replay", "You do not need to know")]),
S("v08", 5, "In the room, that sounds like. Given the severity, I would run containment "
            "and diagnosis in parallel.", kind="say", anchor="Given the severity"),
S("a05", 5, "That is the whole structure. Now let us slow it down, and learn how to use it."),

S("a06", 6, "Part One is not a trivia test. The interviewer is not asking. Do you happen to guess the secret bug? "
            "They are asking. Can you take an ambiguous production symptom, and systematically turn it into a "
            "defensible causal explanation?"),
S("a06b", 6, "A strong diagnosis contains five things. The failing component, or system decision. The mechanism "
             "that produced the symptom. The boundary condition that explains who was affected. The evidence that "
             "supports the conclusion. And the timing, or trigger, that explains why the incident began when it did."),

S("a07", 7, "Notice the difference between a symptom and a root cause. The classifier missed the request, is a "
            "symptom. The always on classifier evaluated only the latest turn, while the harmful intent was "
            "distributed across the conversation, is a mechanism. Principal canonicalization broke permission "
            "filtering, is a broad area. The canonicalization rollout removed an alias that still existed in "
            "document access control lists, causing authorized documents to be denied, is a root cause."),

S("a08", 8, "Your job is to keep moving from broad observation, toward specific mechanism. That movement, is TRACE."),

S("a09", 9, "The first step is Translate the problem. Before you diagnose the system, translate the interviewer's "
            "opening into a precise incident statement."),

S("a10", 10, "You want to understand four things. What the product is supposed to do. What actually happened. "
             "How the failure is being measured. And when the failure began. You are converting an ambiguous story "
             "into an observable difference between expected and actual behavior. For example, suppose the "
             "interviewer says.", ),
S("a10b", 10, "Users say the assistant cannot find answers that exist in their company documents. The answer rate "
              "fell from ninety percent to eighty two percent.", kind="interviewer", speaker="rachel"),
S("a10c", 10, "Do not immediately begin guessing about embeddings, retrieval, or model quality. First, translate it. "
              "You might say.", kind="attrib"),
S("a10d", 10, "Let me confirm the failure signal. The product is an enterprise knowledge assistant. Its goal is to "
              "find relevant internal information, and answer with citations. Expected behavior is that an "
              "authorized user receives an answer when sufficient evidence exists. Observed behavior is an increase "
              "in fallback responses, even when users believe the source exists. The answer with citations rate "
              "fell from ninety to eighty two percent, beginning this morning.", kind="say"),
S("a10e", 10, "That translation does several things. It identifies the product. It identifies the user visible "
              "contract. It names the observed metric. It separates confirmed facts from assumptions. And it gives "
              "you a timeline."),

S("a11", 11, "At this point, you should also ask whether the measurement itself is trustworthy. Did the metric "
             "definition change? Did logging change? Did the denominator change? Are these confirmed model outputs, "
             "user reports, or automated evaluations? Is the reported failure actually new? You do not need to "
             "spend ten minutes validating instrumentation. You are performing a quick sanity check before using "
             "the metric as evidence."),
S("a11b", 11, "What goes on your board. Write. Product. Goal. Expected. Observed. Measured by. Onset. Severity. "
              "That is all. Do not draw the entire architecture yet. A useful interview sentence. You can say."),
S("a11c", 11, "Before I form hypotheses, I want to make the failure signal precise. What should happen, what is "
              "happening instead, how we measure it, and when that changed.", kind="say"),
S("a11d", 11, "That sounds systematic, without becoming ceremonial."),

S("a12", 12, "Before moving to R, there is an important interrupt. Ask. Is the current harm severe enough that we "
             "need to contain it before we have complete certainty? For an ordinary answer quality regression, "
             "diagnosis may proceed before intervention. For dangerous chemical instructions, exposed private "
             "data, destructive agent actions, or unauthorized financial transactions, you should not wait for a "
             "perfect postmortem. You can say. Given the severity, I would run containment and diagnosis in parallel."),
S("a12b", 12, "Containment might mean. Rolling back a recent correlated change. Disabling one risky route, or "
              "tool. Routing the affected cohort through a safer fallback. Temporarily requiring human approval. "
              "Changing the system to read only mode. Buffering output until a safety decision completes. Or "
              "applying a temporary conservative policy to a narrow, high risk slice."),
S("a12c", 12, "Containment is not the permanent architecture. Containment is the reversible action that reduces "
              "immediate exposure, while preserving enough evidence to diagnose. Always name the tradeoff. For "
              "example, you can say."),
S("a12d", 12, "This may increase false refusals and latency. But I would accept that temporarily for this severe "
              "category, while we establish the root cause.", kind="say"),
S("a12e", 12, "On your board, containment should be a small red box at the top. Immediate harm? Temporary action? "
              "Tradeoff? Evidence preserved? Then, return to TRACE."),

S("a13", 13, "The second step is Restrict the blast radius. At the beginning, the incident appears large and "
             "vague. Your goal is to find the smallest condition that predicts failure."),

S("a14", 14, "Ask. Who is affected? And equally important. Who is not affected? Useful dimensions include. Model "
             "version. Region. Language. Tenant. Product surface. Request type. Conversation length. Single turn, "
             "versus multi turn. Tool enabled, versus ordinary chat. New sessions, versus old sessions. Streaming, "
             "versus non streaming. Rollout bucket. Document source. Permission type. Or runtime version. You are "
             "searching for a boundary condition."),
S("a14b", 14, "For example. If every safety category is degrading, the classifier, or enforcement system, may be "
              "broadly unhealthy. If only indirect chemical requests fail, while other categories remain stable, a "
              "broad outage becomes less likely. If only long, multi turn conversations fail, context handling, or "
              "conversation level enforcement, becomes more likely. If failures occur only in one rollout bucket, "
              "a new version becomes more likely. If users can access a document directly, but the assistant "
              "cannot retrieve it, the boundary may involve indexing, identity, or permissions, rather than the "
              "underlying document itself."),
S("a14c", 14, "The key is not to ask every segmentation question you know. Ask the cuts that divide your most "
              "plausible explanations. What goes on your board. Create two columns. Affected. Unaffected. For "
              "example. Affected. Multi turn. Model version B. English. Web surface. Unaffected. Single turn. "
              "Model version A. A P I surface. That table is much more useful than a list of fifteen possible causes."),

S("a15", 15, "How to interpret scope. If the failure affects everyone, look for a shared dependency, global "
             "configuration, or broad model change. If it affects one narrow cohort, ask what is unique about that "
             "cohort. If the failure is deterministic, replay and comparison become powerful. If it is "
             "intermittent, investigate routing, load, races, retries, caches, or partial dependencies. If it "
             "began suddenly, prioritize discrete changes, and traffic events. If it worsened gradually, "
             "prioritize drift, saturation, data accumulation, or adoption changes."),
S("a15b", 15, "A useful interview sentence. You can say."),
S("a15c", 15, "I want to identify the smallest condition that predicts the failure, because that will determine "
              "which portion of the system is worth expanding.", kind="say"),
S("a15d", 15, "That sentence bridges directly into the next step."),

S("a16", 16, "The third step is Aim at the relevant system path. This is where your evidence weighted search idea "
             "matters. You do not need to perform a linear search through every possible component. You also "
             "should not randomly jump to an exotic hypothesis. Instead, use the symptom, and the blast radius, to "
             "choose the most informative region of the request path."),

S("a17", 17, "Think of the architecture at three zoom levels. Zoom level one. The working path. Start with five to "
             "eight boxes."),

S("a18", 18, "For a generic chatbot, or A P I request, your path might be. Client. Gateway, and authentication. "
             "Context assembly. Input policy. Model routing, and inference. Output policy. Streaming, and final "
             "response."),

S("a19", 19, "For a coding agent, your path might be. User task. Agent runtime, and context assembly. Model "
             "request. Tool use proposal. Schema, and permission validation. Tool executor, or sandbox. Tool "
             "result returned to context. Next model turn, or final response."),

S("a20", 20, "For a retrieval system, your path might be. Request, and tenant context. Query processing. "
             "Retrieval. Permission filtering. Reranking. Evidence sufficiency. Generation. Final answer, with "
             "citations. These are working models, not claims about confidential internal implementation. You can "
             "say. I'll use this as my working request path. Please correct any major difference in the actual system."),
S("a20b", 20, "Zoom level two. The suspected region. Once the symptom and scope point toward a region, expand that "
              "region. For example. If latency rose, expand queueing, prefill, decode, tools, and streaming. If "
              "the model selected the wrong tool, expand context assembly, tool schemas, model output, validation, "
              "and routing. If the tool was correct, but caused the wrong side effect, expand permissions, "
              "executor behavior, retries, idempotency, and sandboxing. If retrieval found the right document, but "
              "the answer was still missing, expand permission filtering, reranking, sufficiency, and generation. "
              "If unsafe tokens reached the user, expand input classification, model behavior, output "
              "classification, enforcement, and streaming."),
S("a20c", 20, "Zoom level three. Component internals. Only expand component internals when the evidence points "
              "there. Tokenizer details, K V cache behavior, batching algorithms, embedding internals, or sampling "
              "parameters may matter. But they should not dominate your first drawing, unless the symptom gives "
              "you evidence that they matter. The rule is. Start broad enough to avoid tunnel vision, but zoom "
              "only where evidence raises the probability. That, is evidence weighted path search."),

S("a21", 21, "Here are a few examples. If quality decreases while latency improves, move up hypotheses involving "
             "skipped work, early exit, truncation, missing candidates, or a bypassed validation step. Faster is "
             "not automatically healthy. It may mean the system is doing less. If A P I errors spike, begin around "
             "gateways, dependencies, quotas, timeouts, and serving capacity. If the response is fluent, but "
             "factually wrong, investigate context, retrieval, model selection, and generation. If the response is "
             "a fallback, and generation never occurred, do not spend your time debugging sampling behavior."),
S("a21b", 21, "If an agent proposes a correct tool, but the action fails, the likely region is downstream of the "
              "model. Validation, permissions, executor, sandbox, or dependency. If an incorrect tool is proposed, "
              "the likely region is upstream. Context, tool descriptions, model behavior, or routing. The "
              "important word is, likely. You are choosing where to inspect first. You are not declaring the root cause."),

S("a22", 22, "The best first artifact. Once you have a likely path, ask for. One affected request, and one closely "
             "matched healthy request, including what entered and exited each relevant stage. This turns a top "
             "line metric into an observable failed trajectory."),
S("a22b", 22, "What goes on your board. Draw the path. Gray out the low probability region. Circle the region you "
              "intend to inspect. Write one sentence. Why I am starting here. For example. Failure is limited to "
              "tool enabled requests, so I am beginning at the model to tool boundary, rather than general "
              "inference. This shows prioritization."),

S("a23", 23, "The fourth step is Compare, and find the earliest divergence. This is the heart of the framework. "
             "You now have an affected request, and a healthy comparison. Walk them through the relevant path, and "
             "ask. Where is the first stage at which expected and actual behavior differ? Do not begin with the "
             "final failure. Begin with the earliest divergence. Why? Because downstream components often behave "
             "correctly, given the bad input they received."),
S("a23b", 23, "Suppose a retrieval system returns insufficient evidence. That does not mean the sufficiency "
              "checker is broken. The relevant document may have disappeared during permission filtering. The "
              "sufficiency check may be correctly rejecting the weak candidates it received. Similarly, if a tool "
              "executor runs a destructive command, the executor may have correctly performed a command that "
              "should never have passed the permission gate. The earliest divergence helps separate the root "
              "cause, from its downstream consequences."),

S("a24", 24, "Use these three rules.", kind="attrib"),
S("a24b", 24, "Rule one. Same input, different output. If healthy and affected cases enter a component with the "
              "same input, but produce different outputs, investigate that component's version, configuration, "
              "nondeterminism, state, capacity, or dependency. "
              "Rule two. Different input. If the component received different inputs, move upstream, and explain "
              "why. Do not blame the component for processing what it was given. "
              "Rule three. Same output, different user outcome. If the component behaves the same in both cases, "
              "but users see different results, move downstream.", kind="rule", speaker="rachel"),

S("a25", 25, "Questions to ask at a stage. Was the component invoked? What exact input did it receive? What "
             "output, or score, did it produce? What version, and configuration, were active? What decision was "
             "made? Was the decision enforced? Those questions work for many systems."),
S("a25b", 25, "For a safety classifier. Was it invoked? What text and context did it see? What scores did it "
              "return? Which threshold, and policy version, converted the scores into an action? Was the action "
              "applied before streaming? For a tool executor. Was a tool call proposed? Did the schema validate? "
              "Was permission granted? Did the executor run? Was there a retry? Was the action idempotent? What "
              "result came back to the agent runtime?"),

S("a26", 26, "Conditional metrics. Stage level metrics become more useful when they are conditional. Instead of "
             "asking only. How often did the system answer correctly? Ask. How often did the expected document "
             "survive permission filtering, conditional on being retrieved? How often did sufficiency pass, "
             "conditional on the correct source reaching the top three? How often did output enforcement block "
             "unsafe content, conditional on the classifier producing a block decision? Conditional metrics help "
             "you locate the first meaningful drop."),
S("a26b", 26, "What goes on your board. Mark the request path with. A green check through the last healthy stage. "
              "A red X at the first divergence. Then write. Healthy. Affected. First divergence. Current "
              "interpretation. This reduces the amount you must hold in working memory."),

S("a27", 27, "This is the section to practice most. Every time the interviewer gives you meaningful evidence, "
             "pause, and run this loop. What did I learn? What became less likely? What became more likely? What "
             "test best distinguishes the remaining explanations? Use this sentence."),
S("a27b", 27, "This evidence tells me blank. It makes blank less likely, and blank more likely. My next test is "
              "blank, because it distinguishes blank, from blank.", kind="say"),
S("a27c", 27, "For example.", kind="attrib"),
S("a27d", 27, "The expected document is still found during retrieval, but disappears during permission filtering. "
              "That makes retrieval quality, and answer generation, less likely as primary causes. It makes an "
              "authorization input, or permission filtering issue, more likely. I next want to compare resolved "
              "principals, and permission decisions, between an affected and a healthy request.", kind="say"),
S("a27e", 27, "That sentence makes your reasoning visible. It also gives you time to think."),

S("a28", 28, "When your brain blanks, do not immediately produce another hypothesis. Say."),
S("a28b", 28, "Let me take a moment to update my hypothesis from that evidence.", kind="say"),
S("a28c", 28, "Then write three words. Evidence. Meaning. Next. A short pause will feel much longer to you, than "
              "it looks to the interviewer."),

S("a29", 29, "The fifth step is Establish causality. At this point, you have found the earliest divergence, and "
             "formed a small number of hypotheses."),

S("a30", 30, "Keep no more than three active hypotheses. For each hypothesis, track. Evidence supporting it. "
             "Evidence against it. And the next test. The goal is not to collect every available log. The goal is "
             "to run the comparison that most clearly separates your top explanations. A high value test creates a "
             "fork. If the result is A, hypothesis one rises. If the result is B, hypothesis two rises. If both "
             "possible answers lead you to the same next action, the question probably has low information value."),

S("a31", 31, "Examples of decisive evidence. Replay the same request on the old, and new, configuration. Hold the "
             "query, user, model, data, and downstream system constant, while changing only one suspected "
             "component. Compare the affected rollout bucket, with the control bucket. Bypass one layer in a "
             "controlled environment. Run the same prompt as single turn, and multi turn. Compare raw model "
             "output, with post processed output. Disable retries, while holding the action constant. Run the same "
             "tool request with, and without, the new permission policy. Compare the same long context, before and "
             "after compaction. The strongest test changes one meaningful variable at a time. A test that changes "
             "five variables may produce a working demo. It does not produce a clean diagnosis."),

S("a32", 32, "Correlation, versus causation. A deployment near the onset is evidence. It is not automatically the "
             "cause. To raise causal confidence, you want some combination of. Temporal alignment. Cohort "
             "alignment. Mechanistic alignment. And reversal, or reproduction. Temporal alignment means the "
             "incident begins when the change, or traffic event, begins. Cohort alignment means the failure "
             "appears where the change was active. Mechanistic alignment means the change could produce the exact "
             "observed symptom. Reversal, or reproduction, means the failure disappears when the variable is "
             "removed. Or reappears when it is restored."),

S("a33", 33, "The timing question. Before closing the R C A, ask. Does my diagnosis explain why the incident began "
             "when it did? Sometimes the root mechanism is an old vulnerability, and the trigger is new. For "
             "example. The system may have always evaluated only the latest user turn. But the incident began "
             "today, because a new multi turn attack pattern spread. In that case. The latent vulnerability is "
             "limited conversation level safety coverage. The trigger is increased use of a newly discovered "
             "attack. Both matter."),

S("a34", 34, "The stop rule. You are ready to diagnose when you have. A failing component, or decision. A "
             "mechanism from that failure to the symptom. A boundary condition explaining the affected cohort. "
             "Evidence that distinguishes the leading explanation from alternatives. And a plausible account of "
             "the onset. You do not need mathematical certainty. You need a defensible diagnosis, with calibrated "
             "confidence. The final diagnosis template. Use."),
S("a34b", 34, "Since blank, the affected cohort fails at blank, because blank. This causes blank downstream. The "
              "strongest evidence is blank. The unaffected cohort is spared because blank. My confidence is blank, "
              "and the strongest remaining alternative is blank.", kind="say"),
S("a34c", 34, "A shorter version is."),
S("a34d", 34, "The root cause is blank. The mechanism is blank. The decisive evidence is blank.", kind="say"),
S("a34e", 34, "Then, stop. Do not keep exploring after a controlled, single variable test, reproduces and reverses "
              "the symptom."),

S("a35", 35, "Let us run TRACE on a concrete example. The product is an enterprise knowledge assistant. Users ask "
             "questions about company documents. The system should find relevant information, and return an answer "
             "with citations. The incident is. Users receive, I could not find enough information, even though "
             "they can open a document containing the answer. The answer with citations rate falls from ninety "
             "percent, to eighty two percent. A P I errors remain flat. Latency improves slightly."),

S("a36", 36, "T. Translate. Expected behavior. An authorized user receives an answer, when the connected documents "
             "contain sufficient evidence. Observed behavior. The system returns a fallback more often. Measured "
             "by. The answer with citations rate. Onset. Around nine forty in the morning. Interesting secondary "
             "signal. The system is slightly faster. That raises the possibility that a stage is being skipped, "
             "short circuited, or receiving fewer candidates."),
S("a36b", 36, "R. Restrict. We would ask whether the failure varies by. Tenant. Document connector. Permission "
              "type. Rollout bucket. Region. Model version. Or document age. We would also compare affected "
              "requests, with healthy requests that ask similar questions."),
S("a36c", 36, "A. Aim. The relevant working path is. Request. Tenant, and authentication context. Query "
              "processing. Hybrid retrieval. Permission filtering. Reranking. Evidence sufficiency. Generation. "
              "Final answer. Because the system returns a fallback, rather than an A P I error, and because "
              "latency is lower, we prioritize the middle of the evidence pipeline. We ask for one complete "
              "affected trace, and stage level canary metrics."),

S("a37", 37, "C. Compare. The expected document appears in hybrid retrieval, at rank two. That tells us retrieval "
             "found the relevant evidence. The document is then removed during permission filtering, with a no "
             "matching principal decision. The remaining documents rerank poorly. The evidence sufficiency check "
             "correctly fails. Generation is never invoked. The earliest divergence, is therefore, permission "
             "filtering. This makes model generation, sampling, and final answer formatting, unlikely as primary "
             "causes. The next question is. Did the permission filter behave incorrectly, given correct identity "
             "information? Or did it receive incorrect principal information from upstream? That, is the fork."),

S("a38", 38, "E. Establish. We learn that the permission filter service itself did not change. An upstream "
             "principal resolution version reached one hundred percent rollout, at the incident onset. We replay "
             "the exact same user, query, document index, A C L index, reranker, and sufficiency configuration. "
             "The only variable is principal canonicalization, version one, versus version two. Version one "
             "includes the group alias appearing in the document A C L. The document survives permission "
             "filtering. The system answers correctly. Version two omits that alias. The document is denied. The "
             "system falls back. That, is decisive evidence. A clean diagnosis is."),
S("a38b", 38, "The principal canonicalization rollout removed a group alias that remained in indexed document "
              "A C Ls. Authorized users therefore lost an A C L matching principal during permission filtering. "
              "The correct document was retrieved, but removed before reranking, causing sufficiency to fail, and "
              "generation to be skipped. The controlled, version one versus version two replay, reproduces and "
              "reverses the failure.", kind="say"),
S("a38c", 38, "At that point, Part One is complete. Do not continue asking broad diagnostic questions. Transition "
              "to Part Two."),

S("a39", 39, "Part Two is not. How do we patch this one document? Part Two is. How do we design the general system "
             "that prevents, detects, contains, and recovers from this class of failure?"),

S("a40", 40, "This is GUARD. G. Generalize the failure class. U. Understand requirements, and red lines. A. "
             "Architect prevention, detection, and recovery. R. Reason through tradeoffs, and failure modes. D. "
             "Deploy safely, and monitor."),

S("a41", 41, "Start by abstracting one level above the observed bug. The specific incident may be. A Google "
             "Workspace group alias disappeared. The general failure class is. A representation normalization "
             "change altered authorization semantics. The specific incident may be. A multi turn chemical request "
             "bypassed a latest turn classifier. The general failure class is. Risk accumulates across a "
             "conversation, but the enforcement path evaluates individual turns in isolation. The specific "
             "incident may be. A retry executed a payment twice. The general failure class is. Non idempotent side "
             "effects are retried without a stable action identity. A useful sentence is."),
S("a41b", 41, "I am going to generalize this, from the specific failure of blank, into the broader system problem "
              "of blank.", kind="say"),
S("a41c", 41, "This prevents overfitting your architecture to one example."),

S("a42", 42, "Before drawing the new architecture, state what it must accomplish. Include the normal functional "
             "requirement. For authorization. Authorized users retain access. Unauthorized users never gain "
             "access. For tool execution. Valid actions succeed once. Denied actions never execute. Retries do not "
             "duplicate side effects. For safety. Severe harmful requests are caught with sufficiently high "
             "recall. Benign educational, or defensive use, is not unnecessarily blocked. For retrieval. Relevant "
             "evidence remains available when the user has permission. Answers do not cite documents the user "
             "cannot access."),
S("a42b", 42, "Then state nonfunctional requirements. Latency. Availability. Cost. Scale. Privacy. Auditability. "
              "Recovery time. And reversibility. For catastrophic classes, name red lines. Do not average severe, "
              "irreversible failures, into a moderate aggregate score. A red line might be. No cross tenant data "
              "exposure. No external destructive action without valid permission. No rollout that changes "
              "authorization outcomes, without an explicit policy migration. What goes on your board. Write. Must "
              "do. Must never do. Latency, or cost budget. Scale. Recovery requirement. Red line invariant."),

S("a43", 43, "A strong general system usually needs more than one request time component. Think in four planes. "
             "The serving plane. This is the hot path that handles each request. Examples include. Context "
             "assembly. Policy decisions. Model routing. Inference. Tool validation. Permission checks. "
             "Execution. Streaming. The control plane. This manages. Versions. Configuration. Thresholds. "
             "Policies. Routing rules. Permissions. Feature flags. Rollout cohorts. And rollback."),
S("a43b", 43, "The evaluation, and observability plane. This tells you whether behavior is healthy. It includes. "
              "Offline evaluations. Canary requests. Shadow traffic. Stage level traces. Score distributions. "
              "Human review. User reports. And drift monitoring. The recovery, and operations plane. This lets "
              "the team respond when a failure still occurs. It includes. Circuit breakers. Safe fallbacks. Kill "
              "switches. Bounded retries. Idempotency. Audit logs. Replay tools. Rollback. Runbooks. And clear "
              "ownership. Your architecture should address three jobs. Prevent the failure where possible. Detect "
              "it quickly when prevention fails. Recover safely when detection fires. That is stronger than adding "
              "one more classifier, or one more test."),

S("a44", 44, "Every system choice has a cost. The interviewer wants to know whether you see it. Examples include. "
             "Safety coverage, versus latency. Recall, versus false refusals. Fail open, versus fail closed. "
             "Global consistency, versus regional availability. Human approval, versus autonomy. Strict "
             "permissions, versus usability. Frequent full context classification, versus compute cost. Output "
             "buffering, versus streaming responsiveness. More retrieval candidates, versus reranking cost. A "
             "useful way to speak is."),
S("a44b", 44, "I would choose blank, because this failure class has blank severity. The cost is blank. I would "
              "bound that cost through blank.", kind="say"),
S("a44c", 44, "For example."),
S("a44d", 44, "I would fail closed for ambiguous destructive tool permissions, because the downside is "
              "irreversible. The cost is additional blocked actions, which I would bound with clearer permission "
              "prompts, and a fast escalation path.", kind="say"),
S("a44e", 44, "Then, stress the system. What happens when the classifier is unavailable? What happens when a "
              "policy version, and a model version, are incompatible? What happens during partial rollout? What "
              "happens when a tool times out, after completing the action? What happens when metrics remain "
              "green, but one severe class regresses? What happens when traffic spikes? What happens when logs "
              "are missing? What happens when rollback itself is unsafe? You do not need to list every possible "
              "failure. Choose the failures most relevant to the architecture, and the severity of the domain."),

S("a45", 45, "The final step is Deploy safely, and monitor. A good design can still fail during rollout. Explain "
             "how you move from idea to production. A common sequence is. Offline regression evaluation. Replay "
             "on historical traffic. Shadow deployment. Small canary. Cohort comparison. Gradual ramp. Full "
             "rollout. Continuous monitoring. Rollback readiness. For a representation, or permissions change, "
             "compare old and new authorization decisions, before enforcing the new version. For a safety change, "
             "evaluate severe harm recall, and benign over refusal, by slice. For an agent runtime change, test "
             "retries, permission denial, timeout, and duplicate side effect cases. Define the success metric. "
             "Define guardrail metrics. Define the rollback trigger. Define the owner. A strong closing sentence is."),
S("a45b", 45, "I would not consider this system complete until we can detect a semantic regression before full "
              "rollout, identify the affected cohort quickly, and reverse the change without waiting for user "
              "reports.", kind="say"),
S("a45c", 45, "That completes GUARD."),

S("a46", 46, "Let us recap. Part One is TRACE. Translate the problem. State the product, expected behavior, "
             "observed behavior, measurement, onset, and severity. Restrict the blast radius. Find affected, and "
             "unaffected, cohorts. Aim at the relevant system path. Draw only enough architecture to guide the "
             "investigation, and begin in the region made most likely by the evidence. Compare, and find the "
             "earliest divergence. Use affected, versus healthy traces, and inspect stage inputs and outputs. "
             "Establish causality. Run the cleanest test that separates your leading hypotheses, and state the "
             "mechanism. Then, Part Two is GUARD. Generalize the failure class. Understand requirements, and red "
             "lines. Architect prevention, detection, and recovery. Reason through tradeoffs, and failure modes. "
             "Deploy safely, and monitor. And across both parts. Contain severe ongoing harm, in parallel."),

S("a47", 47, "Here is a concise opening you can use in the interview."),
S("a47b", 47, "I'll begin by aligning on the product's expected behavior, the exact failure signal, its severity, "
              "and the affected cohort. Then I'll sketch the relevant request path, and use an affected versus "
              "healthy comparison, to find the earliest divergence. From there, I'll prioritize a small number of "
              "hypotheses, and run the cleanest test that distinguishes them. If there is ongoing severe harm, "
              "I'll contain that in parallel. Once we have a defensible root cause, I'll generalize the failure "
              "class, and design the prevention, detection, and recovery system.", kind="say"),
S("a47c", 47, "You do not have to say every word. The purpose is to communicate that you have a plan. Then, begin."),

S("a48", 48, "When you receive evidence, and your brain blanks, use this sequence. First say."),
S("a48b", 48, "Let me take a moment to update my hypothesis from that.", kind="say"),
S("a48c", 48, "Then ask yourself. What did I just learn? What became less likely? What became more likely? What "
              "comparison changes what I would do next? Then say."),
S("a48d", 48, "This tells me blank. It makes blank less likely, and blank more likely. I want to test blank next, "
              "because it distinguishes blank, from blank.", kind="say"),
S("a48e", 48, "If you still cannot identify the next test, use one of these rescue questions. Can we compare one "
              "affected request, with one closely matched healthy request, at this stage? What exactly entered, "
              "and exited, the first component where behavior diverged? Were there any code, configuration, "
              "routing, policy, model, or traffic changes near the onset? Can we hold everything else constant, "
              "and change only the suspected variable? What is the single fact still preventing me from stating a "
              "diagnosis? Those questions are not junior. They are junior only if they are disconnected from the "
              "evidence. When you explain why the answer matters, they become senior diagnostic questions."),

S("a49", 49, "The system design interview is not asking you to know every possible failure beforehand. It is "
             "asking you to make steady progress. You begin with a broad production symptom. You narrow it into "
             "an affected cohort. You draw the relevant path. You find the first divergence. You inspect the "
             "decision at that boundary. You run a controlled comparison. You state the cause. Then, you "
             "generalize, and harden. The central movement is. Symptom. Scope. Path. Divergence. Decision. "
             "Evidence. Cause. And the central sentence is."),
S("a49b", 49, "This evidence makes one explanation less likely, and another more likely. Here is the next test "
              "that separates them.", kind="say"),
S("a49c", 49, "That is the muscle. You are not solving the whole system at once. You are reducing uncertainty, "
              "one meaningful step at a time. Trace the incident. Then, guard the system."),

# ======================= PART B — CASE ONE, LIVE (slides 52-74) =======================
S("b52", 52, "Now, the full case study, live. One change this time. When the interviewer finishes a prompt, it is "
             "your turn first. Pause the video, or use the silent countdown, and answer out loud. Then compare "
             "your answer with the model answer."),
S("v10", 52, "Case One. The enterprise knowledge assistant that suddenly cannot find "
             "existing documents. The key lesson ahead. The user visible symptom looks "
             "like retrieval, but the failure happens in permission semantics.",
  spans=[("Broad complaint", "Case One."),
         ("Key lesson", "The key lesson ahead")]),

# --- Slide 53: T, interviewer opening ---
S("v11", 53, "The interviewer opens.", kind="attrib"),
S("v12", 53, "An enterprise knowledge assistant answers employee questions using internal "
             "documents. Since nine forty, users get, I couldn't find enough information, "
             "even when the answer exists in a document they can open. Answer with "
             "citations fell from ninety percent, to eighty two percent. Errors are flat. "
             "P ninety five latency improved slightly. Diagnose it.",
  kind="interviewer", speaker="rachel",
  anchor="An enterprise knowledge assistant answers employee questions"),
S("yt1", 53, "Pause here. This one is yours first. Take the next ten seconds, or pause the video, and answer the "
             "interviewer out loud. Then compare.", kind="yourturn", pause_extra=12),
S("v13", 53, "A strong candidate responds in four moves. "
             "One. Translate the product contract. Authorized users should receive "
             "grounded answers, with citations. "
             "Two. Restate the observed outcome, and the exact metric change. "
             "Three. Keep, the user can open the source, separate from, the system "
             "indexed or retrieved it. "
             "Four. Treat faster latency as a clue that the system may be doing less work.",
  spans=[("Translate the product contract", "One."),
         ("Restate the observed outcome", "Two."),
         ("Keep “the user can open the source”", "Three."),
         ("Treat faster latency", "Four.")]),

# --- Slide 54: how it sounds out loud ---
S("v14", 54, "Here is how it sounds out loud.", kind="attrib"),
S("v15", 54, "Let me first translate the incident into expected, versus observed behavior. "
             "Before I form technical hypotheses, I want to confirm whether the metric "
             "changed, and what, the source exists, actually proves.",
  kind="say", anchor="Let me first translate the incident"),
S("v16", 54, "The response beats. Name the product, and its goal. Expected versus "
             "observed. Metric, and onset. Qualify the source claim. Then ask two high "
             "value clarifiers.",
  spans=[("Name product + goal", "Name the product"),
         ("Expected vs observed", "Expected versus"),
         ("Metric + onset", "Metric, and onset"),
         ("Qualify the source claim", "Qualify the source"),
         ("Ask two high-value clarifiers", "ask two high")]),

# --- Slide 55: what you should be thinking ---
S("v17", 55, "And here is what you should be thinking, behind those words.", kind="attrib"),
S("v18", 55, "Do not collapse, source exists, into, retrieval worked. A document can fail "
             "at ingestion, indexing, retrieval, permission, ranking, sufficiency, or "
             "generation. Fallback does not prove an empty candidate list. And faster plus "
             "worse, may mean fewer candidates survive, or generation is skipped.",
  kind="think",
  spans=[("A document can fail at ingestion", "A document can fail"),
         ("Fallback does not prove an empty candidate list", "Fallback does not prove"),
         ("Faster + worse may mean fewer candidates", "And faster plus worse")]),
S("v19", 55, "On your board, the incident card. Product, enterprise document Q and A. "
             "Expected, an authorized, cited answer. Observed, fallback rising, ninety to "
             "eighty two percent. Onset, nine forty. Errors flat. Latency down.",
  anchor="Product: enterprise document QA"),
S("v20", 55, "The rules. Source exists, is not the same as, source reached the model. "
             "Fallback is an outcome. And faster can mean skipped work.",
  kind="rule", speaker="rachel",
  spans=[("Source exists ≠ source reached model", "Source exists"),
         ("Fallback is an outcome", "Fallback is an outcome"),
         ("Faster can mean skipped work", "faster can mean skipped work")]),

# --- Slide 56: R, blast radius ---
S("v21", 56, "The interviewer gives the blast radius boundary.", kind="attrib"),
S("v22", 56, "The metric definition is unchanged. Failures concentrate in Google Workspace "
             "connectors, especially documents shared through group membership. Direct "
             "user grants are mostly healthy. Regions, and model versions, look similar.",
  kind="interviewer", speaker="rachel", anchor="The metric definition is unchanged"),
S("yt2", 56, "Your turn again. What just became less likely, and more likely? Ten seconds.",
  kind="yourturn", pause_extra=10),
S("v23", 56, "The strong response, in four moves. "
             "One. State what is not global. "
             "Two. Name the narrow predictive condition. Group based access representation. "
             "Three. Lower the probability of model wide, or general retrieval theories. "
             "Four. Ask for a matched healthy request, that differs in permission shape.",
  spans=[("State what is not global.", "One."),
         ("Name the narrow predictive condition", "Two."),
         ("Lower the probability of model-wide", "Three."),
         ("Ask for a matched healthy request", "Four.")]),

# --- Slide 57: out loud ---
S("v24", 57, "Out loud, that sounds like this.", kind="attrib"),
S("v25", 57, "The failure is concentrated in Google Workspace tenants, where access "
             "depends on group membership. That makes a broad model regression less "
             "likely, and raises connector, identity, A C L, or permission enforcement "
             "explanations. I want a group grant affected request, and a direct grant "
             "healthy control.",
  kind="say", anchor="The failure is concentrated in Google Workspace tenants"),
S("v26", 57, "The beats. Summarize affected, versus unaffected. Say what becomes less "
             "likely. Say what becomes more likely. Then request a matched control cohort.",
  spans=[("Summarize affected vs unaffected", "Summarize affected"),
         ("Say what becomes less likely", "less likely"),
         ("Say what becomes more likely", "more likely"),
         ("Request a matched control cohort", "request a matched")]),

# --- Slide 58: thinking + rules ---
S("v27", 58, "What you should be thinking. The failure is not, all of RAG. The same model "
             "versions work for healthy traffic. And the permission representation, not "
             "the document topic, best predicts failure.",
  kind="think",
  spans=[("The failure is not “all RAG.”", "The failure is not"),
         ("Same model versions work for healthy traffic", "The same model versions"),
         ("The permission representation—not the document topic", "And the permission representation")]),
S("v28", 58, "The rules. Healthy controls constrain theory. A narrow boundary points to a "
             "narrow subsystem. And a model wide theory struggles here.",
  kind="rule", speaker="rachel",
  spans=[("Healthy controls constrain theory", "Healthy controls"),
         ("Narrow boundary → narrow subsystem", "A narrow boundary"),
         ("Model-wide theory struggles here", "And a model wide theory")]),

# --- Slide 59: A, path confirm ---
S("b59a", 59, "The interviewer confirms the request path.", kind="attrib"),
S("b59b", 59, "User request. Then authentication, and tenant context. Then query processing. Then hybrid "
              "retrieval. Then permission filtering. Then reranking. Then evidence sufficiency. Then answer "
              "generation, with citations.",
  kind="interviewer", speaker="rachel", anchor="User request → authentication"),
S("yt3", 59, "Your turn. Where do you start on that path, and why? Answer out loud.",
  kind="yourturn", pause_extra=10),
S("b59c", 59, "The strong response. "
              "One. Use the actual path as your working model. "
              "Two. Start in the evidence pipeline. The request succeeds. The fallback is deliberate. Latency is "
              "lower. "
              "Three. Do not assume retrieval is the failing stage. "
              "Four. Ask for stage inputs, and outputs, for affected, versus healthy requests.",
  spans=[("Use the actual path as your working model", "One."),
         ("Start in the evidence pipeline", "Two."),
         ("Do not assume retrieval is the failing stage", "Three."),
         ("Ask for stage inputs and outputs", "Four.")]),

# --- Slide 60: out loud ---
S("b60a", 60, "Out loud.", kind="attrib"),
S("b60b", 60, "I'm going to begin in the evidence pipeline, rather than expanding general inference. The request "
              "completes normally, the fallback is deliberate, and latency is lower. I want stage level outputs, "
              "showing whether the expected source was present when it entered each stage, and whether it "
              "remained when it left.",
  kind="say", anchor="I’m going to begin in the evidence pipeline"),
S("b60c", 60, "The key move. Choose a region, not a root cause. Explain why that region is probable. Request one "
              "full trajectory. And track the expected source across stages.",
  spans=[("Choose a region—not a root cause", "Choose a region"),
         ("Explain why that region is probable", "Explain why"),
         ("Request one full trajectory", "Request one full"),
         ("Track the expected source across stages", "track the expected source")]),

# --- Slide 61: thinking + board + rules ---
S("b61a", 61, "What you should be thinking. A coherent fallback, plus flat errors, means the request path is "
              "completing. Lower latency means, perhaps generation is skipped, or candidates disappear. And the "
              "best evidence, is one stage by stage trace.",
  kind="think",
  spans=[("Coherent fallback + flat errors", "A coherent fallback"),
         ("Lower latency → perhaps generation is skipped", "Lower latency means"),
         ("The best evidence is one stage-by-stage trace", "the best evidence")]),
S("b61b", 61, "On your board. The path, request through cited answer. Circle retrieval, through sufficiency. And "
              "write why. Fallback, plus faster latency.",
  anchor="RELEVANT PATH"),
S("b61c", 61, "The rules. Choose where to inspect first. Do not declare cause yet. And track the expected artifact.",
  kind="rule", speaker="rachel",
  spans=[("Choose where to inspect first", "Choose where"),
         ("Do not declare cause yet", "Do not declare"),
         ("Track the expected artifact", "track the expected artifact")]),

# --- Slide 62: C, stage metrics ---
S("b62a", 62, "The interviewer hands over stage metrics, and one affected trace.", kind="attrib"),
S("b62b", 62, "Retrieved. One hundred ninety of two hundred, before. One hundred eighty nine, after. Surviving "
              "permission filtering. One hundred eighty four, falls to one hundred sixty four. Top three "
              "survival, and sufficiency, are stable, given their inputs. And in your affected trace. The query "
              "is processed. The expected source is at rank two. Then, no matching principal. Weak candidates. "
              "Sufficiency fails. Generation skipped.",
  kind="interviewer", speaker="rachel",
  spans=[("190/200 → 189/200", "Retrieved."),
         ("184/200 → 164/200", "Surviving permission filtering"),
         ("174/184 → 155/164", "Top three survival"),
         ("AFFECTED TRACE", "And in your affected trace"),
         ("NO_MATCHING_PRINCIPAL", "Then, no matching principal"),
         ("Generation skipped", "Generation skipped")]),
S("yt4", 62, "Pause. Read the numbers, and call the first divergence yourself.",
  kind="yourturn", pause_extra=10),
S("b62c", 62, "The first new loss is permission filtering. Not retrieval, reranking, sufficiency, or generation.",
  anchor="The first new loss is permission filtering"),

# --- Slide 63: evidence update out loud ---
S("b63a", 63, "Here is the evidence update, out loud.", kind="attrib"),
S("b63b", 63, "The expected document is still found during retrieval. The largest new loss occurs during "
              "permission filtering. That makes retrieval, reranking, sufficiency, and generation, less likely as "
              "primary causes. My next fork is. A wrong filter decision, from correct identity data? Or incorrect "
              "principals, supplied from upstream?",
  kind="say", anchor="The expected document is still found during retrieval"),
S("b63c", 63, "The beats. State the first divergence. Close downstream branches. Name the new two way fork. And "
              "request the exact principal, versus A C L, inputs.",
  spans=[("State the first divergence", "State the first"),
         ("Close downstream branches", "Close downstream"),
         ("Name the new two-way fork", "Name the new"),
         ("Request exact principal vs ACL inputs", "request the exact")]),

# --- Slide 64: thinking + board + rules ---
S("b64a", 64, "What you should be thinking. Sufficiency fails, because it receives weak evidence. Generation is "
              "skipped, because sufficiency fails. Now, inspect the data, and the configuration, that produced "
              "the permission decision.",
  kind="think",
  spans=[("Sufficiency fails because it receives weak evidence", "Sufficiency fails"),
         ("Generation is skipped because sufficiency fails", "Generation is skipped"),
         ("Now inspect the data and config", "Now, inspect the data")]),
S("b64b", 64, "On your board. Green checks through hybrid retrieval. A red X at permission filtering. Healthy, "
              "the expected source survives. Affected, no matching principal. The fork. The filter, versus user "
              "principals, versus the A C L.",
  anchor="FIRST DIVERGENCE"),
S("b64c", 64, "The rules. Downstream stages can be correct victims. Close branches explicitly. And move one level "
              "upstream.",
  kind="rule", speaker="rachel",
  spans=[("Downstream can be correct victims", "Downstream stages"),
         ("Close branches explicitly", "Close branches"),
         ("Move one level upstream", "And move one level")]),

# --- Slide 65: E, the reveal ---
S("b65a", 65, "The interviewer reveals the rollout, and a one variable replay.", kind="attrib"),
S("b65b", 65, "Version two of principal canonicalization begins rolling out at nine thirty two. Fifty percent at "
              "nine thirty six. One hundred percent at nine forty. The incident begins at nine forty. In the "
              "replay. Version one resolves twenty seven principals. The Workspace group alias is present. "
              "Permission allows. The answer is correct. Version two resolves nineteen principals. The alias is "
              "missing. Permission denies. Fallback.",
  kind="interviewer", speaker="rachel",
  spans=[("v2 rollout begins 9:32", "begins rolling out"),
         ("Incident begins at 9:40", "The incident begins"),
         ("27 principals", "Version one resolves"),
         ("19 principals", "Version two resolves")]),
S("yt5", 65, "Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence.",
  kind="yourturn", pause_extra=14),

# --- Slide 66: the diagnosis ---
S("b66a", 66, "Here is the model answer.", kind="attrib"),
S("b66b", 66, "The primary root cause is the principal canonicalization version two rollout. It removed a Google "
              "Workspace group alias from the user's resolved principals, while existing document A C Ls still "
              "used that alias. The permission filter therefore denied evidence the user was authorized to "
              "access, which caused sufficiency to fail, and generation to be skipped. The controlled, version "
              "one versus version two replay, reproduces and reverses the failure.",
  kind="say", anchor="The primary root cause is the principal-canonicalization-v2 rollout"),
S("b66c", 66, "The final diagnosis card. Cause. The version two representation change. Mechanism. No principal to "
              "A C L intersection. Timing. One hundred percent rollout, at nine forty. Evidence. The controlled "
              "replay. Alternative. A stale A C L index, weakened.",
  spans=[("Cause: v2 representation change", "Cause."),
         ("Mechanism: no principal / ACL intersection", "Mechanism."),
         ("Timing: 100% rollout at 9:40", "Timing."),
         ("Evidence: controlled replay", "Evidence."),
         ("Alternative: stale ACL index", "Alternative.")]),

# --- Slide 67: stopping point ---
S("b67a", 67, "What you should be thinking. You have the failing decision, the mechanism, the onset, the cohort, "
              "and a single variable test. Do not ask, what else should I look at. And do not start Part Two, "
              "before stating the diagnosis.",
  kind="think",
  spans=[("You have the failing decision", "You have the failing decision"),
         ("Do not ask “what else should I look at?”", "Do not ask"),
         ("Do not start Part II before stating the diagnosis", "And do not start Part Two")]),
S("b67b", 67, "And remember. A recent deployment gives correlation. A reversing replay gives much stronger causal "
              "evidence.",
  anchor="A recent deployment gives correlation"),
S("b67c", 67, "The rules. Cause, plus mechanism, plus timing. One ablation beats twenty questions. And when "
              "complete, diagnose.",
  kind="rule", speaker="rachel",
  spans=[("Cause + mechanism + timing", "Cause, plus mechanism"),
         ("One ablation > twenty questions", "One ablation"),
         ("When complete, diagnose", "And when complete")]),

# --- Slide 68: G ---
S("b68a", 68, "Part Two begins. The interviewer shifts.", kind="attrib"),
S("b68b", 68, "Now design the general system that prevents, or safely handles, this class of failure.",
  kind="interviewer", speaker="rachel", anchor="INTERVIEWER: “Now design the general system"),
S("yt6", 68, "Your turn. Generalize the failure class, before I do.", kind="yourturn", pause_extra=10),
S("b68c", 68, "The specific bug is. A Google Workspace group alias disappears from resolved principals. The "
              "general class is. Versioned identity normalization changes authorization semantics. Design for "
              "representation drift, not for one alias.",
  kind="say",
  spans=[("A GWS group alias disappears", "The specific bug is"),
         ("Versioned identity normalization changes authorization semantics", "The general class is")]),
S("b68d", 68, "The rule. Generalize by mechanism. And narrowly enough, to design against.",
  kind="rule", speaker="rachel", anchor="generalize narrowly enough"),

# --- Slide 69: U ---
S("b69a", 69, "What requirements would you establish?",
  kind="interviewer", speaker="rachel", anchor="INTERVIEWER: “What requirements"),
S("yt7", 69, "Pause. Name your requirements, and one red line.", kind="yourturn", pause_extra=10),
S("b69b", 69, "Must do. Preserve authorized access. Keep decisions consistent across connectors. Version the "
              "identity mapping, and keep it auditable. And explain the matching principal. Must never do. Create "
              "unauthorized access. Change effective access through, cleanup. Or hide semantic deltas behind "
              "latency wins. And the red line invariant. A representation only optimization cannot change the "
              "effective set of authorized documents, without an explicit, reviewed policy change.",
  kind="say",
  spans=[("Preserve authorized access", "Must do."),
         ("Create unauthorized access", "Must never do."),
         ("A representation-only optimization cannot change", "And the red line invariant")]),

# --- Slide 70: A ---
S("b70a", 70, "Walk me through your system.",
  kind="interviewer", speaker="rachel", anchor="INTERVIEWER: “Walk me through"),
S("yt8", 70, "Your turn. Sketch your system out loud. Prevention, detection, recovery.", kind="yourturn", pause_extra=12),
S("b70b", 70, "Four parts. One. An identity graph. A stable canonical I D, explicit aliases, and versioned "
              "mappings. Two. Compatible serving. During migration, emit the canonical identity, plus supported "
              "aliases. Three. Semantic shadowing. Diff old, versus new, authorization decisions, before "
              "enforcement. Four. Recovery. A feature flag, rollback, replay, and decision level audit logs.",
  kind="say",
  spans=[("Stable canonical ID + explicit aliases", "One. An identity graph"),
         ("Emit canonical identity plus supported aliases", "Two. Compatible serving"),
         ("Old vs new authorization decision diff", "Three. Semantic shadowing"),
         ("Feature flag · rollback · replay", "Four. Recovery")]),
S("b70c", 70, "The rule. Prevent. Detect. Recover. And the evaluation unit must match the product invariant.",
  kind="rule", speaker="rachel", anchor="the evaluation unit must match"),

# --- Slide 71: R ---
S("b71a", 71, "What tradeoffs concern you?",
  kind="interviewer", speaker="rachel", anchor="INTERVIEWER: “What tradeoffs"),
S("yt9", 71, "Pause. Pick one tradeoff, and defend it.", kind="yourturn", pause_extra=10),
S("b71b", 71, "Canonical purity, versus migration compatibility. I keep aliases temporarily. Fail open, versus "
              "fail closed. I fail closed for security, and detect false denies fast. Latency, versus semantic "
              "verification. I dual evaluate during rollout, and sample after stability.",
  kind="say",
  spans=[("Canonical purity ↔ Migration compatibility", "Canonical purity"),
         ("Fail open ↔ Fail closed", "Fail open, versus"),
         ("Latency ↔ Semantic verification", "Latency, versus semantic")]),
S("b71c", 71, "And I stress the failure modes. A bad merge. A stale identity map. A stale A C L cache. A partial "
              "regional rollout. And rollback that restores code, but not cached state.",
  kind="say", anchor="FAILURE MODES TO STRESS"),

# --- Slide 72: D ---
S("b72a", 72, "How would you roll this out?",
  kind="interviewer", speaker="rachel", anchor="INTERVIEWER: “How would you roll this out"),
S("yt10", 72, "Last one. Your turn. Design the rollout, and its rollback trigger.", kind="yourturn", pause_extra=10),
S("b72b", 72, "Historical replay. Shadow, old versus new. Canary. Gradual ramp. Then one hundred percent. The "
              "rollback triggers. Any unexplained deny to allow delta. A very low tolerance for allow to deny "
              "regression. And missing decision traceability. The monitoring. Authorization decision delta, by "
              "slice. Fallback answer rate, by connector. False deny, and false allow findings. And latency, plus "
              "matching principal trace rate.",
  kind="say",
  spans=[("Historical replay", "Historical replay"),
         ("ROLLBACK TRIGGERS", "The rollback triggers"),
         ("MONITORING", "The monitoring")]),

# --- Slide 73: memory close ---
S("b73", 73, "Case One, in six moves. One. Retrieval looks suspicious. Two. Scope points to group shared "
             "Workspace documents. Three. The trace shows the source survives retrieval. Four. The first "
             "divergence is permission filtering. Five. Version two removed the A C L matching alias. Six. A "
             "replay reproduces, and reverses, the failure.",
  spans=[("Retrieval looks suspicious", "One."),
         ("Scope points to group-shared GWS docs", "Two."),
         ("Trace shows source survives retrieval", "Three."),
         ("First divergence is permission filtering", "Four."),
         ("v2 removes ACL-matching alias", "Five."),
         ("Replay reproduces + reverses failure", "Six.")]),

# --- Slide 74: portable lesson + close ---
S("b74a", 74, "The portable lesson, in one breath.", kind="attrib"),
S("b74b", 74, "The system looked like it could not retrieve the answer. Retrieval was healthy. The correct source "
              "first disappeared at permission filtering. The filter received a principal representation that no "
              "longer matched the A C L. A version controlled replay reproduced, and reversed, the failure.",
  kind="say", anchor="The system looked like it could not retrieve the answer"),
S("b74c", 74, "The final rule. Find the earliest divergence. Then inspect the inputs to that decision. Trace the "
              "incident. Then, guard the system.",
  kind="rule", speaker="rachel", anchor="TRACE the incident. Then GUARD the system."),
S("b74d", 74, "That is the full lesson. Rerun the case tomorrow. Pause at every prompt, and beat me to the "
              "answer. Good luck in the room."),
]

SAMPLE_LAST_ID = SEGS[-1]["id"]

PAUSE_DEFAULT = 0.45
PAUSE_SLIDE_CHANGE = 0.9
PAUSE_AFTER_NUGGET = 0.7
