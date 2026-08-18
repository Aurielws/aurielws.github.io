#!/usr/bin/env python3
"""Generate the two script documents from segments.py (single source of truth)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import SEGS
from slides import SLIDES

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIND_LABEL = {"narration": "narrates", "attrib": "narrates", "interviewer": "interviewer",
              "think": "you think", "say": "you say", "nugget": "nugget"}

# --- Version 1: speaker-tagged role-play script -----------------------------
lines = ["# TRACE → GUARD — Role-Play Script (speaker-tagged)", "",
         "Voices: **DAN** = narrator + you/the candidate. **RACHEL** = interviewer + nuggets.",
         "Tags: every line is `SPEAKER (layer)`. Layers: narrates / interviewer / you think / you say / nugget.", ""]
prev_slide = None
for s in SEGS:
    if s["slide"] != prev_slide:
        spec = SLIDES[s["slide"]]
        lines += [f"## Slide {spec['num']:02d} — {spec['title']}", ""]
        prev_slide = s["slide"]
    lines += [f"**{s['speaker'].upper()} ({KIND_LABEL[s['kind']]}):** {s['text']}", ""]
open(os.path.join(DOCS, "script-roleplay.md"), "w").write("\n".join(lines))

# --- Version 2: solo version with spoken slide cues (drop into ElevenLabs) --
out = ["# TRACE → GUARD — Solo Script with Spoken Slide Cues", "",
       "TTS-ready single-voice version. Paste the text below into ElevenLabs as one job",
       "(or per section). Slide cues are spoken so you can follow the deck hands-free.", "",
       "---", ""]
prev_slide, prev_kind = None, None
for s in SEGS:
    if s["slide"] != prev_slide:
        spec = SLIDES[s["slide"]]
        out += [f"Slide cue. Switch to slide {spec['num']}.", ""]
        prev_slide = s["slide"]
    prefix = ""
    if prev_kind not in ("attrib",):
        if s["kind"] == "interviewer" and not s["text"].startswith("Hello"):
            prefix = "The interviewer says: "
        elif s["kind"] == "think":
            prefix = "What you should think: "
        elif s["kind"] == "say":
            prefix = "What you should say: "
    out += [prefix + s["text"], ""]
    prev_kind = s["kind"]
open(os.path.join(DOCS, "script-spoken-cues.md"), "w").write("\n".join(out))
print("wrote script-roleplay.md and script-spoken-cues.md")
