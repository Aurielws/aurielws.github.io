# TRACE → GUARD — Solo Script with Spoken Slide Cues

TTS-ready single-voice version. Paste the text below into ElevenLabs as one job
(or per section). Slide cues are spoken so you can follow the deck hands-free.

---

Slide cue. Switch to slide 1.

Welcome. This is TRACE to GUARD. A role play lesson on diagnosing and designing production L L M systems, built for the incident half of the system design interview. Something is broken in production. You find out why. Then you design the system that stops that whole class of failure from ever happening again.

Here is how this works. I play you, the candidate. Inside a scene, my voice is either what you should say out loud, or what you should think privately before you speak. The second voice belongs to the other side of the table.

Hello. I play the interviewer. I also read the nuggets. A nugget is a one sentence rule worth memorizing. When you hear my voice outside a scene, write it down.

Slide cue. Switch to slide 2.

First, the shape of the interview. It has two connected halves. In part one, something is broken in production, and your job is to trace the incident to a defensible root cause.

In part two, your job is to guard the system. You design the more general machinery that prevents, detects, and recovers from that class of failure.

The framework is called TRACE to GUARD. First you trace the incident. Then you guard the system.

Nugget one. Trace the incident first. Then guard the system. Never design before you diagnose.

Slide cue. Switch to slide 3.

TRACE is five moves. T. Translate the problem. Turn a vague complaint into a precise incident statement. What should happen. What happened instead. How it is measured. And when it began.

R. Restrict the blast radius. Find the smallest condition that predicts failure. Who is affected. And just as important, who is closely matched but healthy.

A. Aim at the relevant system path. Draw five to eight stages, and start your inspection in the region the evidence makes most likely.

C. Compare, and find the earliest divergence. Walk one affected request and one healthy request through the path, and find the first stage where their behavior differs.

E. Establish causality. Run the cleanest test that separates your top explanations. Change one variable. Hold everything else constant.

Nugget two. Downstream components can be correct victims of bad upstream input. Hunt for the earliest divergence, not the loudest failure.

Slide cue. Switch to slide 4.

Then part two. GUARD. G. Generalize the failure class. U. Understand requirements and red lines. A. Architect prevention, detection, and recovery. R. Reason through tradeoffs and failure modes. D. Deploy safely and monitor. We will use all five inside the scenes, so I will not lecture them now.

Slide cue. Switch to slide 5.

One special rule sits above everything. If the incident involves severe harm, private data, money, or destructive actions, you do not wait for a perfect diagnosis.

In the interview, you say:

Given the severity, I would run containment and diagnosis in parallel. I would take a reversible action that reduces exposure now, name its cost, and preserve the evidence we need to keep investigating.

Nugget three. Contain severe harm in parallel. Diagnosis can wait. Damage cannot.

Your cheat sheet is already growing. Trigger one. Expected, observed, metric, onset. Trigger two. Affected versus unaffected. Trigger three. Severe harm? Contain in parallel. Short prompts, not answers. Now let us step into the room.

Slide cue. Switch to slide 6.

Scene one. The enterprise knowledge assistant. The interviewer begins.

An enterprise knowledge assistant answers employee questions using internal documents. Since nine forty this morning, users get, I could not find enough information, even when the answer exists in a document they can open. Answer with citations fell from ninety percent to eighty two percent. Errors are flat. And latency actually improved slightly. Diagnose it.

Freeze. Here is what you should think, before you say a single word.

Do not touch embeddings yet. A document can die at ingestion, indexing, retrieval, permission, ranking, sufficiency, or generation. The user opening the file proves nothing about my pipeline. And faster plus worse is a clue. The system may be doing less work, not struggling.

Now, here is what you say.

Let me translate this before I hypothesize. The product is an enterprise knowledge assistant. Expected, an authorized user gets a grounded answer with citations. Observed, fallback responses are rising. Ninety down to eighty two percent, since nine forty. Errors flat. Latency slightly better. Before I go further, has the metric definition or the logging changed recently?

The interviewer says: No. The metric and the logging are unchanged.

Nugget four. The source existing is not the same as the source reaching the model.

Slide cue. Switch to slide 7.

The interviewer gives you the blast radius.

Failures concentrate in Google Workspace connectors, especially documents shared through group membership. Direct user grants are mostly healthy. Regions and model versions look similar.

What you should think: That is a boundary condition. Group based access predicts failure. Direct grants do not. A model wide regression would not care how a document was shared. This smells like identity, access control lists, or permission enforcement.

What you should say: So this is not global. The smallest condition that predicts failure is group based permission representation. That makes a broad model or retrieval regression less likely, and raises connector, identity, and permission filtering explanations. I would like one affected request with a group grant, and one healthy request with a direct grant, so I can compare them stage by stage.

Nugget five. A healthy control constrains your theory more than another failing example.

Slide cue. Switch to slide 8.

The interviewer confirms the request path.

User request. Then authentication and tenant context. Then query processing. Then hybrid retrieval. Then permission filtering. Then reranking. Then evidence sufficiency. Then answer generation with citations.

What you should say: I will start in the middle of that path, retrieval through sufficiency, not in general inference. The request completes normally, the fallback is deliberate, and latency is lower, which fits candidates disappearing, or work being skipped. I want to track one thing across stages. Was the expected document present when each stage began, and was it still there when the stage ended?

Nugget six. Faster can mean the system is doing less work.

Slide cue. Switch to slide 9.

The interviewer hands over stage level metrics, and one affected trace.

Retrieval is stable. One hundred ninety of two hundred before, one hundred eighty nine after. Documents surviving permission filtering drop from one hundred eighty four, to one hundred sixty four. The later stages are stable given their inputs. In your affected trace, the expected document is retrieved at rank two, then removed with the code, no matching principal. Sufficiency fails, and generation is never invoked.

What you should think: First divergence, permission filtering. Sufficiency and generation are correct victims. The fork is now binary. Either the filter made a wrong decision from correct identity data, or it received wrong principals from upstream.

What you should say: Here is my evidence update. Retrieval still finds the document, so retrieval quality is now much less likely. The first new loss is permission survival, so I move one level upstream of that decision. My fork is, wrong filter logic, versus wrong principal inputs. Next, I want to compare the exact resolved principals and the document access control list between the affected and the healthy request. And, did anything roll out near nine forty?

Slide cue. Switch to slide 10.

The interviewer says: A principal canonicalization service went from zero to one hundred percent rollout between nine thirty two and nine forty. In a controlled replay of the same request, version one resolves twenty seven principals, including the Workspace group alias, and the answer is correct. Version two resolves nineteen principals. The alias is missing. Permission denies the document, and the system falls back.

What you should say: Then I am confident stating the root cause. The canonicalization version two rollout removed a Google Workspace group alias from resolved principals, while document access control lists still referenced that alias. Authorized users lost their matching principal. The correct document was removed at permission filtering. Sufficiency failed, and generation was skipped. The timing matches the rollout reaching one hundred percent at nine forty. The version one versus version two replay reproduces and reverses the failure. The strongest remaining alternative is a stale access control index, which the controlled replay makes unlikely.

Nugget seven. One controlled replay beats twenty clarifying questions.

Slide cue. Switch to slide 11.

Part two begins. The interviewer shifts.

Good. Now design the general system that prevents, or safely handles, this class of failure.

What you should say: First I generalize. The bug is one missing alias. The class is, identity normalization changed authorization semantics. So my red line invariant is, a representation only change must never change the effective set of authorized documents, without an explicit, reviewed policy change.

What you should say: The architecture has four parts. One, a versioned identity graph. Stable canonical identifiers with explicit aliases. Two, compatible serving. Emit the canonical identity plus supported aliases during migration. Three, semantic shadowing. Diff old versus new authorization decisions before enforcement. Four, recovery. Feature flag, rollback, replay, and decision level audit logs.

What you should say: Tradeoffs. I fail closed on ambiguous permissions, because unauthorized access is irreversible, and I bound the cost with fast false deny detection. The rollout is gated on semantic equivalence. Historical replay, shadow, canary, then a gradual ramp. Any unexplained authorization delta stops it.

Nugget eight. Compare final authorization decisions, not principal counts. Evaluate the invariant the product actually promises.

Slide cue. Switch to slide 12.

Scene two. Faster this time. A safety incident.

Your consumer chatbot has started completing requests it should refuse. Each individual message in the offending conversations looks benign. Single turn attacks are still blocked. It started this afternoon.

What you should think: Severe harm. Containment interrupt. Now, in parallel.

What you should say: Given the severity, I contain first. Temporarily route long multi turn conversations in the risky categories through the full conversation classifier, accepting extra latency and some false refusals while we diagnose. Then I translate. Expected, harmful intent is caught wherever it appears. Observed, intent distributed across turns is missed, while single turn is fine. That boundary condition points at enforcement scope, not model capability.

The interviewer says: A router change this morning stopped triggering the cumulative risk check. The full conversation detector was being skipped.

What you should say: Then the mechanism is, sequence level risk was reduced to isolated turn decisions. The root cause is the router rollout. For part two, the class is, risk accumulates across a conversation, while enforcement evaluates turns in isolation. I would build conversation level risk state. A budget that accumulates per conversation. Enforcement that reads it on every turn. And a regression suite of known multi turn attacks that gates any router or policy rollout.

Nugget nine. Risk can accumulate across turns while enforcement looks at one turn at a time. Match the unit of enforcement to the unit of risk.

Slide cue. Switch to slide 13.

Scene three. An agent with tools.

A finance agent charged a customer twice for the same invoice. The logs show exactly one approved payment proposal. It is intermittent. And it started after a reliability improvement shipped.

What you should think: A reliability improvement, plus intermittent duplicates. That smells like retries. And the model proposed one action, so the fault is probably downstream, in the runtime or the executor.

What you should say: The proposal was correct and approved once, so I look downstream of the model, at validation, execution, and retry behavior. My first question. Does the executor retry on timeout, and is the payment idempotent? My guess at the fork. The payment succeeded, the response timed out, and the retry ran the same action again with no stable identity.

The interviewer says: Correct. The new retry policy resends on timeout, and the payment A P I has no idempotency key.

What you should say: Root cause. Non idempotent side effects, retried without a stable action identity. The general fix. Every side effecting action gets a client generated idempotency key. The executor treats timeout as unknown outcome, and reconciles before retrying. Destructive and financial actions fail closed to a human. And any retry policy change is tested against duplicate side effect cases before rollout.

Nugget ten. A retry is only safe when the action has a stable identity. Timeout means unknown, not failed.

Slide cue. Switch to slide 14.

Common mistakes. Hear them once. Avoid them forever. One. Hypothesizing before translating. Two. Drawing the entire architecture as a memory recital. Three. Listing fifteen causes instead of one affected versus unaffected table. Four. Blaming the loudest failure instead of the earliest divergence. Five. Continuing to investigate after a decisive replay. Six. Patching the instance instead of designing for the class. Seven. Forgetting that a rollback restores code, but not cached state.

Slide cue. Switch to slide 15.

And when you freeze, there is a protocol. Buy time honestly. Say this.

Let me take a moment to update my hypothesis from that evidence.

Then work three words. Evidence. What did I just learn? Meaning. What became more, or less, likely? Next. What single comparison moves me forward? If you are still stuck, one of five rescue questions almost always works. Can we compare one affected and one closely matched healthy request? What exactly entered and exited the first diverging component? What changed near the onset? Can we change only the suspected variable? And, what single fact still blocks a diagnosis?

Nugget eleven. Questions do not make you junior. Questions disconnected from evidence do.

Slide cue. Switch to slide 16.

Recap. The whole framework is one movement. Symptom. Scope. Path. Divergence. Decision. Evidence. Cause. Then generalize, and harden. Your cheat sheet holds a trigger for every step. And the sentence that carries you through the whole interview is this one.

What you should say: This evidence makes one explanation less likely, and another more likely. Here is the next test that separates them.

Final nugget. You are not solving the whole system at once. You are reducing uncertainty, one meaningful step at a time.

That is TRACE to GUARD. Run the scenes again tomorrow. Cover my lines, and answer before I do. Good luck in the room.
