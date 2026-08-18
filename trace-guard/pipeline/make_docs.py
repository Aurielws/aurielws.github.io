#!/usr/bin/env python3
"""Generate the two script documents from the segments module (default: segments3)."""
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SEGS = importlib.import_module(os.environ.get("SEGMENTS_MODULE", "segments3")).SEGS

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KIND_LABEL = {"teach": "teaching", "attrib": "narrates", "interviewer": "interviewer",
              "think": "you think", "say": "you say", "rule": "the rules",
              "yourturn": "YOUR TURN cue"}

# --- Version 1: speaker-tagged role-play script -----------------------------
lines = ["# TRACE → GUARD — Role-Play Script (speaker-tagged)", "",
         "Voices: **DAN** = teacher + you/the candidate. **RACHEL** = interviewer + the rules.",
         "Slides refer to the study deck (v2). YOUR TURN cues are followed by a silent",
         "countdown in the video so you can answer out loud before the model answer.", ""]
prev = None
for s in SEGS:
    if s["slideno"] != prev:
        lines += [f"## Slide {s['slideno']}", ""]
        prev = s["slideno"]
    pause = f" *(then {s['pause_extra']}s silent pause)*" if s.get("pause_extra") else ""
    lines += [f"**{s['speaker'].upper()} ({KIND_LABEL[s['kind']]}):** {s['text']}{pause}", ""]
open(os.path.join(DOCS, "script-roleplay.md"), "w").write("\n".join(lines))

# --- Version 2: solo version with spoken slide cues (drop into ElevenLabs) --
out = ["# TRACE → GUARD — Solo Script with Spoken Slide Cues", "",
       "TTS-ready single-voice version. Paste the text below into ElevenLabs as one job",
       "(or per section). Slide cues are spoken so you can follow the deck hands-free.", "",
       "---", ""]
prev, prev_kind = None, None
for s in SEGS:
    if s["slideno"] != prev:
        out += [f"Slide cue. Switch to slide {s['slideno']}.", ""]
        prev = s["slideno"]
    prefix = ""
    if prev_kind != "attrib":
        if s["kind"] == "interviewer":
            prefix = "The interviewer says: "
        elif s["kind"] == "think":
            prefix = "What you should think: "
        elif s["kind"] == "say":
            prefix = "What you should say: "
    out += [prefix + s["text"], ""]
    prev_kind = s["kind"]
open(os.path.join(DOCS, "script-spoken-cues.md"), "w").write("\n".join(out))
print("wrote script-roleplay.md and script-spoken-cues.md")
