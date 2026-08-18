# TRACE → GUARD — Role-Play Video Guide

Study video where two ElevenLabs voices act out interview scenes while slides animate in sync.

- `script-roleplay.md` — speaker-tagged script (DAN = narrator/candidate, RACHEL = interviewer/nuggets)
- `script-spoken-cues.md` — solo version with spoken slide cues, ready to paste into ElevenLabs
- `cheat-sheet.md` — one-page trigger prompts
- `vocab.md` — vocabulary list
- `pipeline/` — everything needed to (re)build the video:
  - `segments.py` — the script as data (single source of truth)
  - `slides.py` — 16 animated slide layouts (1920×1080)
  - `tts.py` — ElevenLabs `/with-timestamps` calls (cached). Needs `XI_API_KEY` env var (an `sk_...` key). Never commit the key.
  - `render.py` — animation renderer (10 fps, h264+aac)
  - `make_docs.py` — regenerates the two script markdown files

Build:

```bash
cd trace-guard/pipeline
python3 tts.py estimate                       # credit estimate
XI_API_KEY=sk_... python3 tts.py generate --sample build   # sample audio + timing
python3 render.py build sample.mp4            # render
```
