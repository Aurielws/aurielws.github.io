#!/usr/bin/env python3
"""ElevenLabs audio for the TRACE->GUARD role-play video.

Uses the /with-timestamps endpoint so every response carries audio_base64 plus
character-level alignment; the timestamps drive the slide animations.

Usage:
  python3 tts.py estimate                 # character/credit count, no API calls
  python3 tts.py fake   [--sample] OUT    # no-API preview timing (+silent audio)
  python3 tts.py generate [--sample] OUT  # real TTS; needs XI_API_KEY env var

OUT is a build directory. Never hardcode the API key here.
"""
import base64, hashlib, importlib, json, os, struct, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_seg_mod = importlib.import_module(os.environ.get("SEGMENTS_MODULE", "segments"))
SEGS = _seg_mod.SEGS
SAMPLE_LAST_ID = _seg_mod.SAMPLE_LAST_ID
PAUSE_DEFAULT = _seg_mod.PAUSE_DEFAULT
PAUSE_SLIDE_CHANGE = _seg_mod.PAUSE_SLIDE_CHANGE
PAUSE_AFTER_NUGGET = _seg_mod.PAUSE_AFTER_NUGGET

VOICES = {
    "dan": "Fahco4VZzobUeiPqni1S",     # narrator / candidate (user-supplied voice id)
    "rachel": "21m00Tcm4TlvDq8ikWAM",  # Rachel — ElevenLabs premade, calm female
}
MODEL_ID = os.environ.get("XI_MODEL", "eleven_multilingual_v2")  # ~1 credit/char
SAMPLE_RATE = 22050
OUTPUT_FORMAT = f"pcm_{SAMPLE_RATE}"
VOICE_SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.25}
FAKE_CPS = 14.0  # chars/sec for preview timing when no API key is available


def seg_list(sample_only):
    out = []
    for s in SEGS:
        out.append(s)
        if sample_only and s["id"] == SAMPLE_LAST_ID:
            break
    return out


def pause_after(seg, nxt):
    if nxt is None:
        return 1.2
    if nxt.get("slide", nxt.get("slideno")) != seg.get("slide", seg.get("slideno")):
        return PAUSE_SLIDE_CHANGE
    if seg["kind"] in ("nugget", "rule"):
        return PAUSE_AFTER_NUGGET
    return PAUSE_DEFAULT


def estimate():
    total = sum(len(s["text"]) for s in SEGS)
    sample = sum(len(s["text"]) for s in seg_list(True))
    print(f"segments: {len(SEGS)}  total chars: {total}")
    print(f"sample chars (through {SAMPLE_LAST_ID}): {sample}")
    print(f"credits @1/char (multilingual v2): full={total}  sample={sample}")
    print(f"credits @0.5/char (turbo v2.5):    full={total//2}  sample={sample//2}")


def call_tts(seg, key, cache_dir):
    h = hashlib.sha1((seg["text"] + VOICES[seg["speaker"]] + MODEL_ID + OUTPUT_FORMAT).encode()).hexdigest()[:12]
    cache = os.path.join(cache_dir, f"{h}.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[seg['speaker']]}"
           f"/with-timestamps?output_format={OUTPUT_FORMAT}")
    body = json.dumps({"text": seg["text"], "model_id": MODEL_ID,
                       "voice_settings": VOICE_SETTINGS}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "xi-api-key": key, "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            break
        except Exception as e:
            if attempt == 3:
                raise
            print(f"  retry {seg['id']} after error: {e}")
            time.sleep(2 ** (attempt + 1))
    json.dump(data, open(cache, "w"))
    return data


def fake_alignment(text):
    starts, t = [], 0.0
    for ch in text:
        starts.append(round(t, 4))
        t += 1.0 / FAKE_CPS
        if ch in ".?!":
            t += 0.30
        elif ch in ",;:":
            t += 0.12
    return {"characters": list(text),
            "character_start_times_seconds": starts,
            "character_end_times_seconds": starts[1:] + [round(t, 4)]}, t + 0.15


def run(mode, sample_only, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cache_dir = os.path.join(out_dir, "tts")
    os.makedirs(cache_dir, exist_ok=True)
    key = os.environ.get("XI_API_KEY", "")
    if mode == "generate" and not key.startswith("sk_"):
        sys.exit("XI_API_KEY missing or not an sk_ key. Aborting before any API call.")

    segs = seg_list(sample_only)
    pcm = bytearray(b"\x00\x00" * int(0.5 * SAMPLE_RATE))  # lead-in
    timeline = []
    for i, seg in enumerate(segs):
        if mode == "generate":
            data = call_tts(seg, key, cache_dir)
            audio = base64.b64decode(data["audio_base64"])
            align = data["alignment"]
            dur = align["character_end_times_seconds"][-1]
        else:
            align, dur = fake_alignment(seg["text"])
            audio = b"\x00\x00" * int(dur * SAMPLE_RATE)
        start = len(pcm) / 2 / SAMPLE_RATE
        pcm += audio
        gap = pause_after(seg, segs[i + 1] if i + 1 < len(segs) else None) + seg.get("pause_extra", 0)
        pcm += b"\x00\x00" * int(gap * SAMPLE_RATE)
        timeline.append(dict(id=seg["id"], start=round(start, 4), dur=round(dur, 4), gap=round(gap, 3),
                             chars=align["characters"],
                             char_starts=[round(start + t, 4) for t in align["character_start_times_seconds"]]))
        print(f"{seg['id']} {seg['speaker']:6s} {dur:6.2f}s  @{start:7.2f}s  {len(seg['text'])} chars")

    json.dump(timeline, open(os.path.join(out_dir, "timing.json"), "w"))
    wav_path = os.path.join(out_dir, "audio.wav")
    with open(wav_path, "wb") as f:
        n = len(pcm)
        f.write(b"RIFF" + struct.pack("<I", 36 + n) + b"WAVEfmt " +
                struct.pack("<IHHIIHH", 16, 1, 1, SAMPLE_RATE, SAMPLE_RATE * 2, 2, 16) +
                b"data" + struct.pack("<I", n) + bytes(pcm))
    total = len(pcm) / 2 / SAMPLE_RATE
    print(f"\nwrote {wav_path} ({total/60:.1f} min) and timing.json")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "estimate":
        estimate()
    else:
        mode = args[0]
        sample_only = "--sample" in args
        out = [a for a in args[1:] if not a.startswith("--")]
        run(mode, sample_only, out[0] if out else "build")
