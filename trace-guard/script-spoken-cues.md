# TRACE → GUARD — Solo Script with Spoken Slide Cues

TTS-ready single-voice version. Paste the text below into ElevenLabs as one job
(or per section). Slide cues are spoken so you can follow the deck hands-free.

---

Slide cue. Switch to slide 1.

Welcome. In this module, we are going to learn a practical framework for the system design interview.

Slide cue. Switch to slide 2.

The interview has two connected parts. In Part One, something is broken in production. Your job is to identify the root cause.

In Part Two, your job is to design the more general system that prevents, detects, or safely handles this class of failure.

The framework is called, TRACE to GUARD. First, you trace the incident. Then, you guard the system.

Slide cue. Switch to slide 3.

The letters in TRACE stand for. T. Translate the problem. R. Restrict the blast radius. A. Aim at the relevant system path. C. Compare, and find the earliest divergence. E. Establish causality.

Slide cue. Switch to slide 4.

Then, in Part Two, GUARD stands for. G. Generalize the failure class. U. Understand the requirements, and red lines. A. Architect prevention, detection, and recovery. R. Reason through tradeoffs and failure modes. D. Deploy safely, and monitor.

Slide cue. Switch to slide 5.

There is also one special rule. If the incident involves severe safety risk, security, private data, financial loss, destructive tool actions, or another potentially irreversible harm, you run containment in parallel. You do not need to know the complete root cause before reducing immediate harm.

What you should say: In the room, that sounds like. Given the severity, I would run containment and diagnosis in parallel.

That is the whole structure. Now let us slow it down, and learn how to use it.

Slide cue. Switch to slide 6.

Part One is not a trivia test. The interviewer is not asking. Do you happen to guess the secret bug? They are asking. Can you take an ambiguous production symptom, and systematically turn it into a defensible causal explanation?

A strong diagnosis contains five things. The failing component, or system decision. The mechanism that produced the symptom. The boundary condition that explains who was affected. The evidence that supports the conclusion. And the timing, or trigger, that explains why the incident began when it did.

Slide cue. Switch to slide 7.

Notice the difference between a symptom and a root cause. The classifier missed the request, is a symptom. The always on classifier evaluated only the latest turn, while the harmful intent was distributed across the conversation, is a mechanism. Principal canonicalization broke permission filtering, is a broad area. The canonicalization rollout removed an alias that still existed in document access control lists, causing authorized documents to be denied, is a root cause.

Slide cue. Switch to slide 8.

Your job is to keep moving from broad observation, toward specific mechanism. That movement, is TRACE.

Slide cue. Switch to slide 9.

The first step is Translate the problem. Before you diagnose the system, translate the interviewer's opening into a precise incident statement.

Slide cue. Switch to slide 10.

You want to understand four things. What the product is supposed to do. What actually happened. How the failure is being measured. And when the failure began. You are converting an ambiguous story into an observable difference between expected and actual behavior. For example, suppose the interviewer says.

The interviewer says: Users say the assistant cannot find answers that exist in their company documents. The answer rate fell from ninety percent to eighty two percent.

Do not immediately begin guessing about embeddings, retrieval, or model quality. First, translate it. You might say.

Let me confirm the failure signal. The product is an enterprise knowledge assistant. Its goal is to find relevant internal information, and answer with citations. Expected behavior is that an authorized user receives an answer when sufficient evidence exists. Observed behavior is an increase in fallback responses, even when users believe the source exists. The answer with citations rate fell from ninety to eighty two percent, beginning this morning.

That translation does several things. It identifies the product. It identifies the user visible contract. It names the observed metric. It separates confirmed facts from assumptions. And it gives you a timeline.

Slide cue. Switch to slide 11.

At this point, you should also ask whether the measurement itself is trustworthy. Did the metric definition change? Did logging change? Did the denominator change? Are these confirmed model outputs, user reports, or automated evaluations? Is the reported failure actually new? You do not need to spend ten minutes validating instrumentation. You are performing a quick sanity check before using the metric as evidence.

What goes on your board. Write. Product. Goal. Expected. Observed. Measured by. Onset. Severity. That is all. Do not draw the entire architecture yet. A useful interview sentence. You can say.

What you should say: Before I form hypotheses, I want to make the failure signal precise. What should happen, what is happening instead, how we measure it, and when that changed.

That sounds systematic, without becoming ceremonial.

Slide cue. Switch to slide 12.

Before moving to R, there is an important interrupt. Ask. Is the current harm severe enough that we need to contain it before we have complete certainty? For an ordinary answer quality regression, diagnosis may proceed before intervention. For dangerous chemical instructions, exposed private data, destructive agent actions, or unauthorized financial transactions, you should not wait for a perfect postmortem. You can say. Given the severity, I would run containment and diagnosis in parallel.

Containment might mean. Rolling back a recent correlated change. Disabling one risky route, or tool. Routing the affected cohort through a safer fallback. Temporarily requiring human approval. Changing the system to read only mode. Buffering output until a safety decision completes. Or applying a temporary conservative policy to a narrow, high risk slice.

Containment is not the permanent architecture. Containment is the reversible action that reduces immediate exposure, while preserving enough evidence to diagnose. Always name the tradeoff. For example, you can say.

What you should say: This may increase false refusals and latency. But I would accept that temporarily for this severe category, while we establish the root cause.

On your board, containment should be a small red box at the top. Immediate harm? Temporary action? Tradeoff? Evidence preserved? Then, return to TRACE.

Slide cue. Switch to slide 13.

The second step is Restrict the blast radius. At the beginning, the incident appears large and vague. Your goal is to find the smallest condition that predicts failure.

Slide cue. Switch to slide 14.

Ask. Who is affected? And equally important. Who is not affected? Useful dimensions include. Model version. Region. Language. Tenant. Product surface. Request type. Conversation length. Single turn, versus multi turn. Tool enabled, versus ordinary chat. New sessions, versus old sessions. Streaming, versus non streaming. Rollout bucket. Document source. Permission type. Or runtime version. You are searching for a boundary condition.

For example. If every safety category is degrading, the classifier, or enforcement system, may be broadly unhealthy. If only indirect chemical requests fail, while other categories remain stable, a broad outage becomes less likely. If only long, multi turn conversations fail, context handling, or conversation level enforcement, becomes more likely. If failures occur only in one rollout bucket, a new version becomes more likely. If users can access a document directly, but the assistant cannot retrieve it, the boundary may involve indexing, identity, or permissions, rather than the underlying document itself.

The key is not to ask every segmentation question you know. Ask the cuts that divide your most plausible explanations. What goes on your board. Create two columns. Affected. Unaffected. For example. Affected. Multi turn. Model version B. English. Web surface. Unaffected. Single turn. Model version A. A P I surface. That table is much more useful than a list of fifteen possible causes.

Slide cue. Switch to slide 15.

How to interpret scope. If the failure affects everyone, look for a shared dependency, global configuration, or broad model change. If it affects one narrow cohort, ask what is unique about that cohort. If the failure is deterministic, replay and comparison become powerful. If it is intermittent, investigate routing, load, races, retries, caches, or partial dependencies. If it began suddenly, prioritize discrete changes, and traffic events. If it worsened gradually, prioritize drift, saturation, data accumulation, or adoption changes.

A useful interview sentence. You can say.

What you should say: I want to identify the smallest condition that predicts the failure, because that will determine which portion of the system is worth expanding.

That sentence bridges directly into the next step.

Slide cue. Switch to slide 16.

The third step is Aim at the relevant system path. This is where your evidence weighted search idea matters. You do not need to perform a linear search through every possible component. You also should not randomly jump to an exotic hypothesis. Instead, use the symptom, and the blast radius, to choose the most informative region of the request path.

Slide cue. Switch to slide 17.

Think of the architecture at three zoom levels. Zoom level one. The working path. Start with five to eight boxes.

Slide cue. Switch to slide 18.

For a generic chatbot, or A P I request, your path might be. Client. Gateway, and authentication. Context assembly. Input policy. Model routing, and inference. Output policy. Streaming, and final response.

Slide cue. Switch to slide 19.

For a coding agent, your path might be. User task. Agent runtime, and context assembly. Model request. Tool use proposal. Schema, and permission validation. Tool executor, or sandbox. Tool result returned to context. Next model turn, or final response.

Slide cue. Switch to slide 20.

For a retrieval system, your path might be. Request, and tenant context. Query processing. Retrieval. Permission filtering. Reranking. Evidence sufficiency. Generation. Final answer, with citations. These are working models, not claims about confidential internal implementation. You can say. I'll use this as my working request path. Please correct any major difference in the actual system.

Zoom level two. The suspected region. Once the symptom and scope point toward a region, expand that region. For example. If latency rose, expand queueing, prefill, decode, tools, and streaming. If the model selected the wrong tool, expand context assembly, tool schemas, model output, validation, and routing. If the tool was correct, but caused the wrong side effect, expand permissions, executor behavior, retries, idempotency, and sandboxing. If retrieval found the right document, but the answer was still missing, expand permission filtering, reranking, sufficiency, and generation. If unsafe tokens reached the user, expand input classification, model behavior, output classification, enforcement, and streaming.

Zoom level three. Component internals. Only expand component internals when the evidence points there. Tokenizer details, K V cache behavior, batching algorithms, embedding internals, or sampling parameters may matter. But they should not dominate your first drawing, unless the symptom gives you evidence that they matter. The rule is. Start broad enough to avoid tunnel vision, but zoom only where evidence raises the probability. That, is evidence weighted path search.

Slide cue. Switch to slide 21.

Here are a few examples. If quality decreases while latency improves, move up hypotheses involving skipped work, early exit, truncation, missing candidates, or a bypassed validation step. Faster is not automatically healthy. It may mean the system is doing less. If A P I errors spike, begin around gateways, dependencies, quotas, timeouts, and serving capacity. If the response is fluent, but factually wrong, investigate context, retrieval, model selection, and generation. If the response is a fallback, and generation never occurred, do not spend your time debugging sampling behavior.

If an agent proposes a correct tool, but the action fails, the likely region is downstream of the model. Validation, permissions, executor, sandbox, or dependency. If an incorrect tool is proposed, the likely region is upstream. Context, tool descriptions, model behavior, or routing. The important word is, likely. You are choosing where to inspect first. You are not declaring the root cause.

Slide cue. Switch to slide 22.

The best first artifact. Once you have a likely path, ask for. One affected request, and one closely matched healthy request, including what entered and exited each relevant stage. This turns a top line metric into an observable failed trajectory.

What goes on your board. Draw the path. Gray out the low probability region. Circle the region you intend to inspect. Write one sentence. Why I am starting here. For example. Failure is limited to tool enabled requests, so I am beginning at the model to tool boundary, rather than general inference. This shows prioritization.

Slide cue. Switch to slide 23.

The fourth step is Compare, and find the earliest divergence. This is the heart of the framework. You now have an affected request, and a healthy comparison. Walk them through the relevant path, and ask. Where is the first stage at which expected and actual behavior differ? Do not begin with the final failure. Begin with the earliest divergence. Why? Because downstream components often behave correctly, given the bad input they received.

Suppose a retrieval system returns insufficient evidence. That does not mean the sufficiency checker is broken. The relevant document may have disappeared during permission filtering. The sufficiency check may be correctly rejecting the weak candidates it received. Similarly, if a tool executor runs a destructive command, the executor may have correctly performed a command that should never have passed the permission gate. The earliest divergence helps separate the root cause, from its downstream consequences.

Slide cue. Switch to slide 24.

Use these three rules.

Rule one. Same input, different output. If healthy and affected cases enter a component with the same input, but produce different outputs, investigate that component's version, configuration, nondeterminism, state, capacity, or dependency. Rule two. Different input. If the component received different inputs, move upstream, and explain why. Do not blame the component for processing what it was given. Rule three. Same output, different user outcome. If the component behaves the same in both cases, but users see different results, move downstream.

Slide cue. Switch to slide 25.

Questions to ask at a stage. Was the component invoked? What exact input did it receive? What output, or score, did it produce? What version, and configuration, were active? What decision was made? Was the decision enforced? Those questions work for many systems.

For a safety classifier. Was it invoked? What text and context did it see? What scores did it return? Which threshold, and policy version, converted the scores into an action? Was the action applied before streaming? For a tool executor. Was a tool call proposed? Did the schema validate? Was permission granted? Did the executor run? Was there a retry? Was the action idempotent? What result came back to the agent runtime?

Slide cue. Switch to slide 26.

Conditional metrics. Stage level metrics become more useful when they are conditional. Instead of asking only. How often did the system answer correctly? Ask. How often did the expected document survive permission filtering, conditional on being retrieved? How often did sufficiency pass, conditional on the correct source reaching the top three? How often did output enforcement block unsafe content, conditional on the classifier producing a block decision? Conditional metrics help you locate the first meaningful drop.

What goes on your board. Mark the request path with. A green check through the last healthy stage. A red X at the first divergence. Then write. Healthy. Affected. First divergence. Current interpretation. This reduces the amount you must hold in working memory.

Slide cue. Switch to slide 27.

This is the section to practice most. Every time the interviewer gives you meaningful evidence, pause, and run this loop. What did I learn? What became less likely? What became more likely? What test best distinguishes the remaining explanations? Use this sentence.

What you should say: This evidence tells me blank. It makes blank less likely, and blank more likely. My next test is blank, because it distinguishes blank, from blank.

For example.

The expected document is still found during retrieval, but disappears during permission filtering. That makes retrieval quality, and answer generation, less likely as primary causes. It makes an authorization input, or permission filtering issue, more likely. I next want to compare resolved principals, and permission decisions, between an affected and a healthy request.

That sentence makes your reasoning visible. It also gives you time to think.

Slide cue. Switch to slide 28.

When your brain blanks, do not immediately produce another hypothesis. Say.

What you should say: Let me take a moment to update my hypothesis from that evidence.

Then write three words. Evidence. Meaning. Next. A short pause will feel much longer to you, than it looks to the interviewer.

Slide cue. Switch to slide 29.

The fifth step is Establish causality. At this point, you have found the earliest divergence, and formed a small number of hypotheses.

Slide cue. Switch to slide 30.

Keep no more than three active hypotheses. For each hypothesis, track. Evidence supporting it. Evidence against it. And the next test. The goal is not to collect every available log. The goal is to run the comparison that most clearly separates your top explanations. A high value test creates a fork. If the result is A, hypothesis one rises. If the result is B, hypothesis two rises. If both possible answers lead you to the same next action, the question probably has low information value.

Slide cue. Switch to slide 31.

Examples of decisive evidence. Replay the same request on the old, and new, configuration. Hold the query, user, model, data, and downstream system constant, while changing only one suspected component. Compare the affected rollout bucket, with the control bucket. Bypass one layer in a controlled environment. Run the same prompt as single turn, and multi turn. Compare raw model output, with post processed output. Disable retries, while holding the action constant. Run the same tool request with, and without, the new permission policy. Compare the same long context, before and after compaction. The strongest test changes one meaningful variable at a time. A test that changes five variables may produce a working demo. It does not produce a clean diagnosis.

Slide cue. Switch to slide 32.

Correlation, versus causation. A deployment near the onset is evidence. It is not automatically the cause. To raise causal confidence, you want some combination of. Temporal alignment. Cohort alignment. Mechanistic alignment. And reversal, or reproduction. Temporal alignment means the incident begins when the change, or traffic event, begins. Cohort alignment means the failure appears where the change was active. Mechanistic alignment means the change could produce the exact observed symptom. Reversal, or reproduction, means the failure disappears when the variable is removed. Or reappears when it is restored.

Slide cue. Switch to slide 33.

The timing question. Before closing the R C A, ask. Does my diagnosis explain why the incident began when it did? Sometimes the root mechanism is an old vulnerability, and the trigger is new. For example. The system may have always evaluated only the latest user turn. But the incident began today, because a new multi turn attack pattern spread. In that case. The latent vulnerability is limited conversation level safety coverage. The trigger is increased use of a newly discovered attack. Both matter.

Slide cue. Switch to slide 34.

The stop rule. You are ready to diagnose when you have. A failing component, or decision. A mechanism from that failure to the symptom. A boundary condition explaining the affected cohort. Evidence that distinguishes the leading explanation from alternatives. And a plausible account of the onset. You do not need mathematical certainty. You need a defensible diagnosis, with calibrated confidence. The final diagnosis template. Use.

What you should say: Since blank, the affected cohort fails at blank, because blank. This causes blank downstream. The strongest evidence is blank. The unaffected cohort is spared because blank. My confidence is blank, and the strongest remaining alternative is blank.

A shorter version is.

What you should say: The root cause is blank. The mechanism is blank. The decisive evidence is blank.

Then, stop. Do not keep exploring after a controlled, single variable test, reproduces and reverses the symptom.

Slide cue. Switch to slide 35.

Let us run TRACE on a concrete example. The product is an enterprise knowledge assistant. Users ask questions about company documents. The system should find relevant information, and return an answer with citations. The incident is. Users receive, I could not find enough information, even though they can open a document containing the answer. The answer with citations rate falls from ninety percent, to eighty two percent. A P I errors remain flat. Latency improves slightly.

Slide cue. Switch to slide 36.

T. Translate. Expected behavior. An authorized user receives an answer, when the connected documents contain sufficient evidence. Observed behavior. The system returns a fallback more often. Measured by. The answer with citations rate. Onset. Around nine forty in the morning. Interesting secondary signal. The system is slightly faster. That raises the possibility that a stage is being skipped, short circuited, or receiving fewer candidates.

R. Restrict. We would ask whether the failure varies by. Tenant. Document connector. Permission type. Rollout bucket. Region. Model version. Or document age. We would also compare affected requests, with healthy requests that ask similar questions.

A. Aim. The relevant working path is. Request. Tenant, and authentication context. Query processing. Hybrid retrieval. Permission filtering. Reranking. Evidence sufficiency. Generation. Final answer. Because the system returns a fallback, rather than an A P I error, and because latency is lower, we prioritize the middle of the evidence pipeline. We ask for one complete affected trace, and stage level canary metrics.

Slide cue. Switch to slide 37.

C. Compare. The expected document appears in hybrid retrieval, at rank two. That tells us retrieval found the relevant evidence. The document is then removed during permission filtering, with a no matching principal decision. The remaining documents rerank poorly. The evidence sufficiency check correctly fails. Generation is never invoked. The earliest divergence, is therefore, permission filtering. This makes model generation, sampling, and final answer formatting, unlikely as primary causes. The next question is. Did the permission filter behave incorrectly, given correct identity information? Or did it receive incorrect principal information from upstream? That, is the fork.

Slide cue. Switch to slide 38.

E. Establish. We learn that the permission filter service itself did not change. An upstream principal resolution version reached one hundred percent rollout, at the incident onset. We replay the exact same user, query, document index, A C L index, reranker, and sufficiency configuration. The only variable is principal canonicalization, version one, versus version two. Version one includes the group alias appearing in the document A C L. The document survives permission filtering. The system answers correctly. Version two omits that alias. The document is denied. The system falls back. That, is decisive evidence. A clean diagnosis is.

What you should say: The principal canonicalization rollout removed a group alias that remained in indexed document A C Ls. Authorized users therefore lost an A C L matching principal during permission filtering. The correct document was retrieved, but removed before reranking, causing sufficiency to fail, and generation to be skipped. The controlled, version one versus version two replay, reproduces and reverses the failure.

At that point, Part One is complete. Do not continue asking broad diagnostic questions. Transition to Part Two.

Slide cue. Switch to slide 39.

Part Two is not. How do we patch this one document? Part Two is. How do we design the general system that prevents, detects, contains, and recovers from this class of failure?

Slide cue. Switch to slide 40.

This is GUARD. G. Generalize the failure class. U. Understand requirements, and red lines. A. Architect prevention, detection, and recovery. R. Reason through tradeoffs, and failure modes. D. Deploy safely, and monitor.

Slide cue. Switch to slide 41.

Start by abstracting one level above the observed bug. The specific incident may be. A Google Workspace group alias disappeared. The general failure class is. A representation normalization change altered authorization semantics. The specific incident may be. A multi turn chemical request bypassed a latest turn classifier. The general failure class is. Risk accumulates across a conversation, but the enforcement path evaluates individual turns in isolation. The specific incident may be. A retry executed a payment twice. The general failure class is. Non idempotent side effects are retried without a stable action identity. A useful sentence is.

What you should say: I am going to generalize this, from the specific failure of blank, into the broader system problem of blank.

This prevents overfitting your architecture to one example.

Slide cue. Switch to slide 42.

Before drawing the new architecture, state what it must accomplish. Include the normal functional requirement. For authorization. Authorized users retain access. Unauthorized users never gain access. For tool execution. Valid actions succeed once. Denied actions never execute. Retries do not duplicate side effects. For safety. Severe harmful requests are caught with sufficiently high recall. Benign educational, or defensive use, is not unnecessarily blocked. For retrieval. Relevant evidence remains available when the user has permission. Answers do not cite documents the user cannot access.

Then state nonfunctional requirements. Latency. Availability. Cost. Scale. Privacy. Auditability. Recovery time. And reversibility. For catastrophic classes, name red lines. Do not average severe, irreversible failures, into a moderate aggregate score. A red line might be. No cross tenant data exposure. No external destructive action without valid permission. No rollout that changes authorization outcomes, without an explicit policy migration. What goes on your board. Write. Must do. Must never do. Latency, or cost budget. Scale. Recovery requirement. Red line invariant.

Slide cue. Switch to slide 43.

A strong general system usually needs more than one request time component. Think in four planes. The serving plane. This is the hot path that handles each request. Examples include. Context assembly. Policy decisions. Model routing. Inference. Tool validation. Permission checks. Execution. Streaming. The control plane. This manages. Versions. Configuration. Thresholds. Policies. Routing rules. Permissions. Feature flags. Rollout cohorts. And rollback.

The evaluation, and observability plane. This tells you whether behavior is healthy. It includes. Offline evaluations. Canary requests. Shadow traffic. Stage level traces. Score distributions. Human review. User reports. And drift monitoring. The recovery, and operations plane. This lets the team respond when a failure still occurs. It includes. Circuit breakers. Safe fallbacks. Kill switches. Bounded retries. Idempotency. Audit logs. Replay tools. Rollback. Runbooks. And clear ownership. Your architecture should address three jobs. Prevent the failure where possible. Detect it quickly when prevention fails. Recover safely when detection fires. That is stronger than adding one more classifier, or one more test.

Slide cue. Switch to slide 44.

Every system choice has a cost. The interviewer wants to know whether you see it. Examples include. Safety coverage, versus latency. Recall, versus false refusals. Fail open, versus fail closed. Global consistency, versus regional availability. Human approval, versus autonomy. Strict permissions, versus usability. Frequent full context classification, versus compute cost. Output buffering, versus streaming responsiveness. More retrieval candidates, versus reranking cost. A useful way to speak is.

What you should say: I would choose blank, because this failure class has blank severity. The cost is blank. I would bound that cost through blank.

For example.

What you should say: I would fail closed for ambiguous destructive tool permissions, because the downside is irreversible. The cost is additional blocked actions, which I would bound with clearer permission prompts, and a fast escalation path.

Then, stress the system. What happens when the classifier is unavailable? What happens when a policy version, and a model version, are incompatible? What happens during partial rollout? What happens when a tool times out, after completing the action? What happens when metrics remain green, but one severe class regresses? What happens when traffic spikes? What happens when logs are missing? What happens when rollback itself is unsafe? You do not need to list every possible failure. Choose the failures most relevant to the architecture, and the severity of the domain.

Slide cue. Switch to slide 45.

The final step is Deploy safely, and monitor. A good design can still fail during rollout. Explain how you move from idea to production. A common sequence is. Offline regression evaluation. Replay on historical traffic. Shadow deployment. Small canary. Cohort comparison. Gradual ramp. Full rollout. Continuous monitoring. Rollback readiness. For a representation, or permissions change, compare old and new authorization decisions, before enforcing the new version. For a safety change, evaluate severe harm recall, and benign over refusal, by slice. For an agent runtime change, test retries, permission denial, timeout, and duplicate side effect cases. Define the success metric. Define guardrail metrics. Define the rollback trigger. Define the owner. A strong closing sentence is.

What you should say: I would not consider this system complete until we can detect a semantic regression before full rollout, identify the affected cohort quickly, and reverse the change without waiting for user reports.

That completes GUARD.

Slide cue. Switch to slide 46.

Let us recap. Part One is TRACE. Translate the problem. State the product, expected behavior, observed behavior, measurement, onset, and severity. Restrict the blast radius. Find affected, and unaffected, cohorts. Aim at the relevant system path. Draw only enough architecture to guide the investigation, and begin in the region made most likely by the evidence. Compare, and find the earliest divergence. Use affected, versus healthy traces, and inspect stage inputs and outputs. Establish causality. Run the cleanest test that separates your leading hypotheses, and state the mechanism. Then, Part Two is GUARD. Generalize the failure class. Understand requirements, and red lines. Architect prevention, detection, and recovery. Reason through tradeoffs, and failure modes. Deploy safely, and monitor. And across both parts. Contain severe ongoing harm, in parallel.

Slide cue. Switch to slide 47.

Here is a concise opening you can use in the interview.

What you should say: I'll begin by aligning on the product's expected behavior, the exact failure signal, its severity, and the affected cohort. Then I'll sketch the relevant request path, and use an affected versus healthy comparison, to find the earliest divergence. From there, I'll prioritize a small number of hypotheses, and run the cleanest test that distinguishes them. If there is ongoing severe harm, I'll contain that in parallel. Once we have a defensible root cause, I'll generalize the failure class, and design the prevention, detection, and recovery system.

You do not have to say every word. The purpose is to communicate that you have a plan. Then, begin.

Slide cue. Switch to slide 48.

When you receive evidence, and your brain blanks, use this sequence. First say.

What you should say: Let me take a moment to update my hypothesis from that.

Then ask yourself. What did I just learn? What became less likely? What became more likely? What comparison changes what I would do next? Then say.

What you should say: This tells me blank. It makes blank less likely, and blank more likely. I want to test blank next, because it distinguishes blank, from blank.

If you still cannot identify the next test, use one of these rescue questions. Can we compare one affected request, with one closely matched healthy request, at this stage? What exactly entered, and exited, the first component where behavior diverged? Were there any code, configuration, routing, policy, model, or traffic changes near the onset? Can we hold everything else constant, and change only the suspected variable? What is the single fact still preventing me from stating a diagnosis? Those questions are not junior. They are junior only if they are disconnected from the evidence. When you explain why the answer matters, they become senior diagnostic questions.

Slide cue. Switch to slide 49.

The system design interview is not asking you to know every possible failure beforehand. It is asking you to make steady progress. You begin with a broad production symptom. You narrow it into an affected cohort. You draw the relevant path. You find the first divergence. You inspect the decision at that boundary. You run a controlled comparison. You state the cause. Then, you generalize, and harden. The central movement is. Symptom. Scope. Path. Divergence. Decision. Evidence. Cause. And the central sentence is.

What you should say: This evidence makes one explanation less likely, and another more likely. Here is the next test that separates them.

That is the muscle. You are not solving the whole system at once. You are reducing uncertainty, one meaningful step at a time. Trace the incident. Then, guard the system.

Slide cue. Switch to slide 52.

Now, the full case study, live. One change this time. When the interviewer finishes a prompt, it is your turn first. Pause the video, or use the silent countdown, and answer out loud. Then compare your answer with the model answer.

Case One. The enterprise knowledge assistant that suddenly cannot find existing documents. The key lesson ahead. The user visible symptom looks like retrieval, but the failure happens in permission semantics.

Slide cue. Switch to slide 53.

The interviewer opens.

An enterprise knowledge assistant answers employee questions using internal documents. Since nine forty, users get, I couldn't find enough information, even when the answer exists in a document they can open. Answer with citations fell from ninety percent, to eighty two percent. Errors are flat. P ninety five latency improved slightly. Diagnose it.

Pause here. This one is yours first. Take the next ten seconds, or pause the video, and answer the interviewer out loud. Then compare.

A strong candidate responds in four moves. One. Translate the product contract. Authorized users should receive grounded answers, with citations. Two. Restate the observed outcome, and the exact metric change. Three. Keep, the user can open the source, separate from, the system indexed or retrieved it. Four. Treat faster latency as a clue that the system may be doing less work.

Slide cue. Switch to slide 54.

Here is how it sounds out loud.

Let me first translate the incident into expected, versus observed behavior. Before I form technical hypotheses, I want to confirm whether the metric changed, and what, the source exists, actually proves.

The response beats. Name the product, and its goal. Expected versus observed. Metric, and onset. Qualify the source claim. Then ask two high value clarifiers.

Slide cue. Switch to slide 55.

And here is what you should be thinking, behind those words.

Do not collapse, source exists, into, retrieval worked. A document can fail at ingestion, indexing, retrieval, permission, ranking, sufficiency, or generation. Fallback does not prove an empty candidate list. And faster plus worse, may mean fewer candidates survive, or generation is skipped.

On your board, the incident card. Product, enterprise document Q and A. Expected, an authorized, cited answer. Observed, fallback rising, ninety to eighty two percent. Onset, nine forty. Errors flat. Latency down.

The rules. Source exists, is not the same as, source reached the model. Fallback is an outcome. And faster can mean skipped work.

Slide cue. Switch to slide 56.

The interviewer gives the blast radius boundary.

The metric definition is unchanged. Failures concentrate in Google Workspace connectors, especially documents shared through group membership. Direct user grants are mostly healthy. Regions, and model versions, look similar.

Your turn again. What just became less likely, and more likely? Ten seconds.

The strong response, in four moves. One. State what is not global. Two. Name the narrow predictive condition. Group based access representation. Three. Lower the probability of model wide, or general retrieval theories. Four. Ask for a matched healthy request, that differs in permission shape.

Slide cue. Switch to slide 57.

Out loud, that sounds like this.

The failure is concentrated in Google Workspace tenants, where access depends on group membership. That makes a broad model regression less likely, and raises connector, identity, A C L, or permission enforcement explanations. I want a group grant affected request, and a direct grant healthy control.

The beats. Summarize affected, versus unaffected. Say what becomes less likely. Say what becomes more likely. Then request a matched control cohort.

Slide cue. Switch to slide 58.

What you should think: What you should be thinking. The failure is not, all of RAG. The same model versions work for healthy traffic. And the permission representation, not the document topic, best predicts failure.

The rules. Healthy controls constrain theory. A narrow boundary points to a narrow subsystem. And a model wide theory struggles here.

Slide cue. Switch to slide 59.

The interviewer confirms the request path.

User request. Then authentication, and tenant context. Then query processing. Then hybrid retrieval. Then permission filtering. Then reranking. Then evidence sufficiency. Then answer generation, with citations.

Your turn. Where do you start on that path, and why? Answer out loud.

The strong response. One. Use the actual path as your working model. Two. Start in the evidence pipeline. The request succeeds. The fallback is deliberate. Latency is lower. Three. Do not assume retrieval is the failing stage. Four. Ask for stage inputs, and outputs, for affected, versus healthy requests.

Slide cue. Switch to slide 60.

Out loud.

I'm going to begin in the evidence pipeline, rather than expanding general inference. The request completes normally, the fallback is deliberate, and latency is lower. I want stage level outputs, showing whether the expected source was present when it entered each stage, and whether it remained when it left.

The key move. Choose a region, not a root cause. Explain why that region is probable. Request one full trajectory. And track the expected source across stages.

Slide cue. Switch to slide 61.

What you should think: What you should be thinking. A coherent fallback, plus flat errors, means the request path is completing. Lower latency means, perhaps generation is skipped, or candidates disappear. And the best evidence, is one stage by stage trace.

On your board. The path, request through cited answer. Circle retrieval, through sufficiency. And write why. Fallback, plus faster latency.

The rules. Choose where to inspect first. Do not declare cause yet. And track the expected artifact.

Slide cue. Switch to slide 62.

The interviewer hands over stage metrics, and one affected trace.

Retrieved. One hundred ninety of two hundred, before. One hundred eighty nine, after. Surviving permission filtering. One hundred eighty four, falls to one hundred sixty four. Top three survival, and sufficiency, are stable, given their inputs. And in your affected trace. The query is processed. The expected source is at rank two. Then, no matching principal. Weak candidates. Sufficiency fails. Generation skipped.

Pause. Read the numbers, and call the first divergence yourself.

The first new loss is permission filtering. Not retrieval, reranking, sufficiency, or generation.

Slide cue. Switch to slide 63.

Here is the evidence update, out loud.

The expected document is still found during retrieval. The largest new loss occurs during permission filtering. That makes retrieval, reranking, sufficiency, and generation, less likely as primary causes. My next fork is. A wrong filter decision, from correct identity data? Or incorrect principals, supplied from upstream?

The beats. State the first divergence. Close downstream branches. Name the new two way fork. And request the exact principal, versus A C L, inputs.

Slide cue. Switch to slide 64.

What you should think: What you should be thinking. Sufficiency fails, because it receives weak evidence. Generation is skipped, because sufficiency fails. Now, inspect the data, and the configuration, that produced the permission decision.

On your board. Green checks through hybrid retrieval. A red X at permission filtering. Healthy, the expected source survives. Affected, no matching principal. The fork. The filter, versus user principals, versus the A C L.

The rules. Downstream stages can be correct victims. Close branches explicitly. And move one level upstream.

Slide cue. Switch to slide 65.

The interviewer reveals the rollout, and a one variable replay.

Version two of principal canonicalization begins rolling out at nine thirty two. Fifty percent at nine thirty six. One hundred percent at nine forty. The incident begins at nine forty. In the replay. Version one resolves twenty seven principals. The Workspace group alias is present. Permission allows. The answer is correct. Version two resolves nineteen principals. The alias is missing. Permission denies. Fallback.

Big moment. Pause, and state the full diagnosis out loud. Cause. Mechanism. Timing. Evidence.

Slide cue. Switch to slide 66.

Here is the model answer.

The primary root cause is the principal canonicalization version two rollout. It removed a Google Workspace group alias from the user's resolved principals, while existing document A C Ls still used that alias. The permission filter therefore denied evidence the user was authorized to access, which caused sufficiency to fail, and generation to be skipped. The controlled, version one versus version two replay, reproduces and reverses the failure.

The final diagnosis card. Cause. The version two representation change. Mechanism. No principal to A C L intersection. Timing. One hundred percent rollout, at nine forty. Evidence. The controlled replay. Alternative. A stale A C L index, weakened.

Slide cue. Switch to slide 67.

What you should think: What you should be thinking. You have the failing decision, the mechanism, the onset, the cohort, and a single variable test. Do not ask, what else should I look at. And do not start Part Two, before stating the diagnosis.

And remember. A recent deployment gives correlation. A reversing replay gives much stronger causal evidence.

The rules. Cause, plus mechanism, plus timing. One ablation beats twenty questions. And when complete, diagnose.

Slide cue. Switch to slide 68.

Part Two begins. The interviewer shifts.

Now design the general system that prevents, or safely handles, this class of failure.

Your turn. Generalize the failure class, before I do.

What you should say: The specific bug is. A Google Workspace group alias disappears from resolved principals. The general class is. Versioned identity normalization changes authorization semantics. Design for representation drift, not for one alias.

The rule. Generalize by mechanism. And narrowly enough, to design against.

Slide cue. Switch to slide 69.

The interviewer says: What requirements would you establish?

Pause. Name your requirements, and one red line.

What you should say: Must do. Preserve authorized access. Keep decisions consistent across connectors. Version the identity mapping, and keep it auditable. And explain the matching principal. Must never do. Create unauthorized access. Change effective access through, cleanup. Or hide semantic deltas behind latency wins. And the red line invariant. A representation only optimization cannot change the effective set of authorized documents, without an explicit, reviewed policy change.

Slide cue. Switch to slide 70.

The interviewer says: Walk me through your system.

Your turn. Sketch your system out loud. Prevention, detection, recovery.

What you should say: Four parts. One. An identity graph. A stable canonical I D, explicit aliases, and versioned mappings. Two. Compatible serving. During migration, emit the canonical identity, plus supported aliases. Three. Semantic shadowing. Diff old, versus new, authorization decisions, before enforcement. Four. Recovery. A feature flag, rollback, replay, and decision level audit logs.

The rule. Prevent. Detect. Recover. And the evaluation unit must match the product invariant.

Slide cue. Switch to slide 71.

The interviewer says: What tradeoffs concern you?

Pause. Pick one tradeoff, and defend it.

What you should say: Canonical purity, versus migration compatibility. I keep aliases temporarily. Fail open, versus fail closed. I fail closed for security, and detect false denies fast. Latency, versus semantic verification. I dual evaluate during rollout, and sample after stability.

What you should say: And I stress the failure modes. A bad merge. A stale identity map. A stale A C L cache. A partial regional rollout. And rollback that restores code, but not cached state.

Slide cue. Switch to slide 72.

The interviewer says: How would you roll this out?

Last one. Your turn. Design the rollout, and its rollback trigger.

What you should say: Historical replay. Shadow, old versus new. Canary. Gradual ramp. Then one hundred percent. The rollback triggers. Any unexplained deny to allow delta. A very low tolerance for allow to deny regression. And missing decision traceability. The monitoring. Authorization decision delta, by slice. Fallback answer rate, by connector. False deny, and false allow findings. And latency, plus matching principal trace rate.

Slide cue. Switch to slide 73.

Case One, in six moves. One. Retrieval looks suspicious. Two. Scope points to group shared Workspace documents. Three. The trace shows the source survives retrieval. Four. The first divergence is permission filtering. Five. Version two removed the A C L matching alias. Six. A replay reproduces, and reverses, the failure.

Slide cue. Switch to slide 74.

The portable lesson, in one breath.

The system looked like it could not retrieve the answer. Retrieval was healthy. The correct source first disappeared at permission filtering. The filter received a principal representation that no longer matched the A C L. A version controlled replay reproduced, and reversed, the failure.

The final rule. Find the earliest divergence. Then inspect the inputs to that decision. Trace the incident. Then, guard the system.

That is the full lesson. Rerun the case tomorrow. Pause at every prompt, and beat me to the answer. Good luck in the room.
