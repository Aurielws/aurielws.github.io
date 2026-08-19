# Case content spec — TRACE → GUARD role-play videos

You are writing ONE new RCA case as a Python content file. It plugs into an existing
video pipeline: 12 slides cloned from the study deck's Case One layouts (light mode,
coral accents), two ElevenLabs voices, animations timed to the narration.

Your file must define exactly three module-level names, no imports:

```python
CASE = dict(key="mycase", label="Case Two", title="Short case name")
SLOTS = { "s1": {...}, ..., "s12": {...} }   # slide text (schema below)
SEGS  = [ dict(...), ... ]                    # the spoken script (rules below)
```

## The cast and layers (same as Case One)

- **DAN** (narrator + the candidate): kinds `teach` (explains the strong response),
  `attrib` (one-line lead-ins like "The interviewer opens."), `say` (how it sounds
  out loud, first person, interview-quality answers), `think` (private thinking),
  `yourturn` (see below).
- **RACHEL** (the interviewer + the rules): kinds `interviewer` (prompts/reveals,
  realistic and specific, with numbers), `rule` (short memorable rules, start with
  "The rules." or "The rule.").

## Segment format

```python
dict(id="xx1", slideno=3, text="...", kind="teach", speaker="dan",
     anchor="substring of a slot text on that slide",        # optional
     spans=[("slot-text substring", "spoken substring"), ...], # optional
     pause_extra=10)                                          # yourturn only
```

- `slideno` is 1..12 (the slide sequence below).
- `anchor`: a substring of one of YOUR slot texts on that slide — the renderer
  reveals + outlines that shape when this segment plays. `spans` lights several
  shapes inside one segment: each pair is (slot-text substring, substring of THIS
  segment's spoken text where it should light up — must appear verbatim in `text`).
- Every slide's key content should be anchored or spanned so it animates.
- ids: prefix with your case key, unique.

## YOUR TURN mechanic (required)

After EVERY `interviewer` prompt/reveal segment, insert a segment
`kind="yourturn", speaker="dan"` — one short spoken cue telling the viewer to pause
and answer out loud first — with `pause_extra` of 10–14 (seconds of silence for the
viewer to answer). Vary the wording. Then Dan gives the model answer/lesson.

## TTS rules (the voices read text literally)

- No markdown, asterisks, arrows, colons-as-structure, or abbreviations.
- Spell letter-words spaced: "A P I", "A C L", "K V cache", "P ninety nine".
- All numbers as words: "nine forty", "ninety percent", "one hundred ninety of two hundred".
- Punctuate for speech rhythm (commas and periods, short sentences).
- Total spoken characters across all SEGS: 6,500–8,000.

## Slide sequence and SLOTS schema

Character limits are hard limits (the boxes don't grow). `\n` splits lines only
where noted. SLOT TEXTS (unlike SEGS) may use compact display style — digits,
symbols like → · ≠ %, abbreviations — mirroring the examples.

- **s1** divider — `case_label` ("CASE TWO", ≤12), `title` (the case name, ≤80),
  `key_lesson` ("Key lesson: ..." ≤110)
- **s2** interviewer opening — `title` (≤40), `quote` (the interviewer's opening,
  first person with metrics/onset, wrapped in “ ”, ≤330), `flow1..flow4`
  (strong-candidate response flow rows, ≤95 each)
- **s3** how it sounds out loud — `title` (≤52), `quote` (“ ”, ≤300),
  `beat1..beat5` (response beats, ≤28 each)
- **s4** what you should be thinking — `title` (≤55), `think1..think3` (≤75 each),
  `board_label` (≤16), `board` (exactly 5 lines joined by \n, ≤45 per line),
  `cheat` (cheat-sheet focus question ≤60), `senior` (senior note ≤75),
  `nug1..nug3` (nuggets ≤38 each)
- **s5** restrict reveal — `title` (≤45), `quote` (“ ”, ≤230), `flow1..flow4` (≤75)
- **s6** out loud — `title` (≤50), `quote` (“ ”, ≤300), `beat1..beat4` (≤32)
- **s7** compare data — `title` (≤50), `subtitle` (≤80), `m1..m4` (metric labels,
  ≤16, UPPERCASE), `v1..v4` (values like "190/200 → 189/200", ≤20),
  `trace_label` (≤16, UPPERCASE), `chip1..chip6` (affected-trace steps, ≤24),
  `bottom` (the conclusion line, ≤95).
  Layout note: the m2/v2 tile renders highlighted (the DROP metric) — put the
  metric that newly degraded there. chip3 renders as the red highlighted step —
  put the pivotal breaking step at chip3.
- **s8** evidence update out loud — `title` (≤35), `quote` (“ ”, ≤300),
  `beat1..beat4` (≤36)
- **s9** establish reveal — `title` (≤55), `subtitle` (≤72), three columns:
  `colA_label` (≤10) + `colA1..colA4` (≤22 each, e.g. timing),
  `colB_label` + `colB1..colB4` (≤18, healthy/old config),
  `colC_label` + `colC1..colC4` (≤18, broken/new config)
- **s10** diagnosis — `title` (≤32), `quote` (the full spoken diagnosis, “ ”, ≤380),
  `diag1..diag5` ("Cause: ...", "Mechanism: ...", "Timing: ...", "Evidence: ...",
  "Alternative: ...", ≤40 each)
- **s11** guard design — `title` (≤64), `subtitle` (≤58), `ask` (the interviewer's
  design question, plain text no quotes, ≤55), `arch1_label..arch4_label` (≤20,
  UPPERCASE) + `arch1..arch4` (≤62 each), `footer` ("Cheat sheet: ... Senior
  note: ..." ≤105)
- **s12** memory close — `title` ("Case N in six moves", ≤25), `subtitle` (≤55),
  `move1..move6` (≤38 each)

## Narrative structure to follow (mirrors Case One)

s1 Dan intro → s2 Rachel opening + YOUR TURN + Dan four moves → s3 Dan attrib +
say + beats → s4 Dan think + board + Rachel rules → s5 Rachel reveal + YOUR TURN +
Dan four moves → s6 Dan say + beats → s7 Rachel data reveal + YOUR TURN + Dan
conclusion → s8 Dan say (evidence update: less likely / more likely / fork /
next test) + beats → s9 Rachel reveal (rollout timing + one-variable replay) +
YOUR TURN → s10 Dan say the full diagnosis + diagnosis card → s11 Rachel ask +
YOUR TURN + Dan say generalization/invariant + say architecture (4 parts) +
Rachel rule → s12 Dan six moves + one closing rule from Rachel.

Quality bar: the case must be technically airtight — a real mechanism, a real
boundary condition (who is affected vs not), a decisive one-variable test, timing
that explains "why now" (latent vulnerability vs trigger), and a GUARD design with
prevention + detection + recovery and one red-line invariant. Study
`trace-guard/pipeline/segments3.py` (Part B) for tone and pacing before writing.
