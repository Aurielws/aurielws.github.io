#!/usr/bin/env python3
"""Render the TRACE->GUARD role-play video from timing.json + slide specs.

1920x1080, 10 fps, h264 + aac. Cards start ghosted and fade in when the
narration reaches them (character-level timestamps). A rounded marker outline
in the speaker's color surrounds the card currently being discussed. Quick
dip-to-white between slides.

Usage: python3 render.py BUILD_DIR OUT.mp4
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import SEGS
from slides import SLIDES, SLIDE_ORDER

W, H, FPS = 1920, 1080, 10
BG = (14, 17, 22)
CARD_BG = (23, 28, 36)
CARD_BORDER = (42, 50, 64)
TEXT = (232, 237, 244)
MUTED = (154, 167, 184)
ACCENT = (125, 211, 252)

TYPE_COLORS = {
    "narration": (125, 211, 252), "interviewer": (148, 163, 184),
    "think": (245, 158, 11), "say": (45, 212, 191),
    "nugget": (167, 139, 250), "data": (100, 116, 139), "alert": (248, 113, 113),
}
KIND_COLORS = {
    "narration": (125, 211, 252), "attrib": (125, 211, 252),
    "interviewer": (148, 163, 184), "think": (245, 158, 11),
    "say": (45, 212, 191), "nugget": (167, 139, 250),
}
SPEAKER_LABEL = {"dan": "DAN", "rachel": "RACHEL"}

FD = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=False):
    return ImageFont.truetype(FD + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

F_KICK, F_TITLE, F_BODY = font(22, True), font(34, True), font(25)
F_LETTER = font(100, True)
F_HKICK, F_HTITLE, F_HMETA = font(24, True), font(44, True), font(24)
F_CHIP = font(24, True)

SEG_BY_ID = {s["id"]: s for s in SEGS}


def fit_font(draw, text, f, max_w, bold=True):
    size = f.size
    while size > 16 and draw.textlength(text, font=font(size, bold)) > max_w:
        size -= 2
    return font(size, bold)


def render_card(c, lit_lines):
    """Card surface with the first lit_lines body lines at full brightness."""
    img = Image.new("RGBA", (c["w"], c["h"]), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    col = TYPE_COLORS[c["type"]]
    d.rounded_rectangle([0, 0, c["w"] - 1, c["h"] - 1], radius=18,
                        fill=CARD_BG + (255,), outline=CARD_BORDER + (255,), width=2)
    pad = 26
    y = pad
    if len(c["kicker"]) <= 2:  # letter / number cards
        d.text((pad, y - 12), c["kicker"], font=F_LETTER, fill=col + (255,))
        y += 108
    else:
        d.text((pad, y), c["kicker"], font=F_KICK, fill=col + (255,))
        y += 40
    tf = fit_font(d, c["title"], F_TITLE, c["w"] - 2 * pad)
    d.text((pad, y), c["title"], font=tf, fill=TEXT + (255,))
    y += tf.size + 18
    for i, line in enumerate(c["lines"]):
        bright = i < lit_lines
        fill = (TEXT if bright else tuple(int(v * 0.55) for v in TEXT)) + (255,)
        bf = fit_font(d, line, F_BODY, c["w"] - 2 * pad, bold=False)
        d.text((pad, y), line, font=bf, fill=fill)
        y += 37
    return img


CARD_CACHE = {}
def card_img(sid, cid, lit):
    key = (sid, cid, lit)
    if key not in CARD_CACHE:
        CARD_CACHE[key] = render_card(SLIDES[sid]["cards"][cid], lit)
    return CARD_CACHE[key]


def build_timeline(timing):
    """Per-slide intervals, card activation times, and marker events."""
    slide_first, slide_last = {}, {}
    for t in timing:
        sl = SEG_BY_ID[t["id"]]["slide"]
        slide_first.setdefault(sl, t["start"])
        slide_last[sl] = t["start"] + t["dur"]
    order = [s for s in SLIDE_ORDER if s in slide_first]
    intervals = []
    for i, sl in enumerate(order):
        a = 0.0 if i == 0 else (slide_last[order[i - 1]] + slide_first[sl]) / 2
        b = (slide_last[sl] + slide_first[order[i + 1]]) / 2 if i + 1 < len(order) else slide_last[sl] + 2.0
        intervals.append((sl, a, b))

    activate, markers = {}, []
    for t in timing:
        seg = SEG_BY_ID[t["id"]]
        sl, t0, t1 = seg["slide"], t["start"], t["start"] + t["dur"]
        col = KIND_COLORS[seg["kind"]]
        spans = seg.get("card_spans")
        if spans:
            text = seg["text"]
            times = []
            for cid, sub in spans:
                idx = text.find(sub)
                times.append((cid, t["char_starts"][idx] if idx >= 0 else t0))
            times.sort(key=lambda x: x[1])
            for j, (cid, ts) in enumerate(times):
                te = times[j + 1][1] if j + 1 < len(times) else t1
                activate.setdefault((sl, cid), ts)
                markers.append((ts, te, sl, cid, col, None))
        else:
            activate.setdefault((sl, seg["card"]), t0)
            markers.append((t0, t1, sl, seg["card"], col, t))
    return intervals, activate, markers, order


def main(build_dir, out_path):
    timing = json.load(open(os.path.join(build_dir, "timing.json")))
    intervals, activate, markers, order = build_timeline(timing)
    total = intervals[-1][2]
    seg_at = {t["id"]: t for t in timing}

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", os.path.join(build_dir, "audio.wav"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-shortest", out_path], stdin=subprocess.PIPE)

    nframes = int(total * FPS)
    for fi in range(nframes):
        now = fi / FPS
        sl, a, b = next(((s, a, b) for s, a, b in intervals if a <= now < b), intervals[-1])
        spec = SLIDES[sl]
        frame = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(frame)

        # header
        d.text((70, 42), spec["kicker"], font=F_HKICK, fill=ACCENT)
        d.text((70, 76), spec["title"], font=F_HTITLE, fill=TEXT)
        meta = f"TRACE → GUARD · {spec['num']:02d}"
        d.text((W - 70 - d.textlength(meta, font=F_HMETA), 60), meta, font=F_HMETA, fill=MUTED)

        # current segment (for marker + speaker chip + karaoke)
        active = [(t0, t1, s, cid, col, t) for (t0, t1, s, cid, col, t) in markers
                  if s == sl and t0 <= now < t1 + 0.15]
        cur = active[-1] if active else None

        # cards
        for cid, c in spec["cards"].items():
            act = activate.get((sl, cid))
            if act is None:
                alpha = 0.12
            elif now < act:
                alpha = 0.12
            else:
                f = min(1.0, (now - act) / 0.5)
                alpha = 0.12 + 0.88 * (1 - (1 - f) ** 3)
            lit = 0
            if act is not None and now >= act:
                lit = len(c["lines"])
                if cur and cur[3] == cid and cur[5] is not None:
                    t = cur[5]
                    spoken = sum(1 for ct in t["char_starts"] if ct <= now)
                    frac = spoken / max(1, len(t["chars"]))
                    lit = max(1, round(frac * len(c["lines"]) + 0.4))
            img = card_img(sl, cid, lit)
            if alpha >= 0.999:
                frame.paste(img, (c["x"], c["y"]), img)
            else:
                faded = img.copy()
                faded.putalpha(faded.getchannel("A").point(lambda v: int(v * alpha)))
                frame.paste(faded, (c["x"], c["y"]), faded)

        # marker outline on the card being discussed
        if cur:
            _, _, _, cid, col, _ = cur
            c = spec["cards"][cid]
            x, y, w2, h2 = c["x"], c["y"], c["w"], c["h"]
            d.rounded_rectangle([x - 7, y - 7, x + w2 + 6, y + h2 + 6], radius=24,
                                outline=tuple(int(v * 0.45) for v in col), width=9)
            d.rounded_rectangle([x - 5, y - 5, x + w2 + 4, y + h2 + 4], radius=22,
                                outline=col, width=4)
            # speaker chip
            seg = next((s for s in SEGS if s["slide"] == sl and s["card"] == cid), None)
            for t in [m[5] for m in active if m[5] is not None][-1:]:
                seg = SEG_BY_ID[t["id"]]
            if seg:
                label = SPEAKER_LABEL[seg["speaker"]]
                kindlab = {"say": "YOU SAY", "think": "YOU THINK", "nugget": "NUGGET",
                           "interviewer": "INTERVIEWER", "narration": "NARRATOR",
                           "attrib": "NARRATOR"}[seg["kind"]]
                chip = f"{label} · {kindlab}"
                cw = d.textlength(chip, font=F_CHIP) + 40
                d.rounded_rectangle([70, H - 66, 70 + cw, H - 26], radius=20,
                                    fill=tuple(int(v * 0.22) for v in col), outline=col, width=2)
                d.text((90, H - 59), chip, font=F_CHIP, fill=col)

        # progress bar
        d.rectangle([0, H - 8, int(W * now / total), H], fill=(45, 212, 191))

        # dip-to-white at slide boundaries
        wa = 0.0
        for _, aa, _ in intervals[1:]:
            if aa - 0.25 <= now < aa:
                wa = (now - (aa - 0.25)) / 0.25
            elif aa <= now < aa + 0.35:
                wa = 1 - (now - aa) / 0.35
        if wa > 0:
            frame = Image.blend(frame, Image.new("RGB", (W, H), (245, 248, 252)), wa * 0.92)

        ff.stdin.write(frame.tobytes())
        if fi % 300 == 0:
            print(f"frame {fi}/{nframes} ({now:.0f}s)")

    ff.stdin.close()
    ff.wait()
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
