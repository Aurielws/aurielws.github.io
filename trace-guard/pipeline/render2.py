#!/usr/bin/env python3
"""Render the TRACE->GUARD video on top of the user's own deck (light mode).

Backgrounds are the deck's rendered slides (slides_png/s-NN.png). Shapes that a
segment anchors are ghosted at slide entry and fade to full strength exactly
when the narration reaches them (character-level timestamps). A rounded marker
outline in the speaker-layer color surrounds the shape being spoken. Quick
dip-to-white between slides. 1920x1080, 10 fps, h264 + aac.

Usage: python2 render2.py BUILD_DIR SHAPES_JSON SLIDES_PNG_DIR OUT.mp4
"""
import importlib, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SEGS = importlib.import_module(os.environ.get("SEGMENTS_MODULE", "segments2")).SEGS

W, H, FPS = 1920, 1080, 10
GHOST = 0.85          # how far ghosted shapes blend toward the background
REVEAL_S = 0.45       # fade-in duration
AUTO_SKIP = {1}       # slides that never ghost (title)
KIND_COLORS = {       # light-mode layer palette; teach matches the deck's coral
    "teach": (232, 93, 93), "attrib": (232, 93, 93),
    "interviewer": (71, 85, 105), "say": (13, 148, 136),
    "think": (200, 108, 8), "rule": (124, 58, 237),
    "yourturn": (200, 108, 8),
}
KIND_LABEL = {"teach": "DAN · TEACHING", "attrib": "DAN · NARRATOR",
              "interviewer": "RACHEL · INTERVIEWER", "say": "DAN · YOU SAY",
              "think": "DAN · YOU THINK", "rule": "RACHEL · THE RULES",
              "yourturn": "YOUR TURN · ANSWER OUT LOUD"}
F_CHIP = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)

SEG_BY_ID = {s["id"]: s for s in SEGS}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("“", '"').replace("”", '"')
                  .replace("‘", "'").replace("’", "'").replace("—", "-")
                  .replace("·", ".").replace("≠", "!=").replace("→", "->")).strip().lower()


def find_region(shapes, anchor):
    """Smallest shape whose text contains anchor; prefer its empty container box."""
    a = norm(anchor)
    hits = [s for s in shapes if s["text"] and a in norm(s["text"])]
    if not hits:
        raise KeyError(f"anchor not found: {anchor!r}")
    hit = min(hits, key=lambda s: s["w"] * s["h"])
    containers = [s for s in shapes if not s["text"]
                  and s["x"] <= hit["x"] + 4 and s["y"] <= hit["y"] + 4
                  and s["x"] + s["w"] >= hit["x"] + hit["w"] - 4
                  and s["y"] + s["h"] >= hit["y"] + hit["h"] - 4
                  and s["w"] * s["h"] < 0.45 * W * H]
    if containers:
        c = min(containers, key=lambda s: s["w"] * s["h"])
        return (c["x"], c["y"], c["w"], c["h"])
    padl = min(85, hit["x"])   # cover a numbered badge / bullet dot to the left
    return (hit["x"] - padl, hit["y"] - 10, hit["w"] + padl + 12, hit["h"] + 20)


def auto_regions(shapes):
    """Content rows for slides without hand anchors: leaf text shapes, top-to-bottom."""
    rows = []
    for s in shapes:
        if not s["text"] or not (200 < s["y"] < 945):
            continue
        padl = min(85, s["x"])
        rows.append((s["y"], s["x"], (s["x"] - padl, s["y"] - 8, s["w"] + padl + 10, s["h"] + 16)))
    rows.sort()
    return [r for _, _, r in rows]


def build_events(timing, shapes_by_slide):
    """Per-slide reveal events [(t, region)] and marker events [(t0,t1,slide,region,kind)]."""
    reveals, markers = {}, []
    anchored_slides = set()
    for seg in SEGS:
        if seg.get("spans") or seg.get("anchor"):
            anchored_slides.add(seg["slideno"])
    for t in timing:
        seg = SEG_BY_ID[t["id"]]
        sn = seg["slideno"]
        shapes = shapes_by_slide[str(sn)]
        t0, t1 = t["start"], t["start"] + t["dur"]
        regions = []
        if seg["kind"] == "yourturn":
            markers.append((t0, t1 + t.get("gap", 0) - 0.3, sn, None, "yourturn"))
        elif seg.get("spans"):
            text = seg["text"]
            for anchor, sub in seg["spans"]:
                idx = text.find(sub)
                ts = t["char_starts"][idx] if idx >= 0 else t0
                regions.append((ts, find_region(shapes, anchor)))
            regions.sort(key=lambda r: r[0])
            for j, (ts, reg) in enumerate(regions):
                te = regions[j + 1][0] if j + 1 < len(regions) else t1
                markers.append((ts, te, sn, reg, seg["kind"]))
        elif seg.get("anchor"):
            reg = find_region(shapes, seg["anchor"])
            regions = [(t0, reg)]
            markers.append((t0, t1, sn, reg, seg["kind"]))
        else:
            markers.append((t0, t1, sn, None, seg["kind"]))
        for ts, reg in regions:
            reveals.setdefault(sn, {})
            key = reg
            if key not in reveals[sn] or ts < reveals[sn][key]:
                reveals[sn][key] = ts

    # auto row-by-row reveal for slides with no hand-authored anchors
    first, last = {}, {}
    for t in timing:
        sn = SEG_BY_ID[t["id"]]["slideno"]
        first.setdefault(sn, t["start"])
        last[sn] = t["start"] + t["dur"]

    def kind_at(ts):
        for t in timing:
            if t["start"] <= ts < t["start"] + t["dur"] + t.get("gap", 0):
                return SEG_BY_ID[t["id"]]["kind"]
        return "teach"

    for sn in first:
        if sn in anchored_slides or sn in AUTO_SKIP:
            continue
        regs = auto_regions(shapes_by_slide[str(sn)])
        if not regs:
            continue
        a, b = first[sn] + 0.3, max(first[sn] + 0.3, last[sn] - 1.2)
        times = [a + (b - a) * i / max(1, len(regs) - 1) for i in range(len(regs))]
        for j, (ts, reg) in enumerate(zip(times, regs)):
            te = times[j + 1] if j + 1 < len(regs) else last[sn]
            k = kind_at(ts)
            if k == "yourturn":
                k = "teach"
            reveals.setdefault(sn, {})[reg] = ts
            markers.append((ts, te, sn, reg, k))
    return reveals, markers


def main(build_dir, shapes_json, png_dir, out_path):
    timing = json.load(open(os.path.join(build_dir, "timing.json")))
    shapes_by_slide = json.load(open(shapes_json))
    reveals, markers = build_events(timing, shapes_by_slide)

    # slide intervals in narration order
    order, first, last = [], {}, {}
    for t in timing:
        sn = SEG_BY_ID[t["id"]]["slideno"]
        if sn not in first:
            order.append(sn)
            first[sn] = t["start"]
        last[sn] = t["start"] + t["dur"]
    intervals = []
    for i, sn in enumerate(order):
        a = 0.0 if i == 0 else (last[order[i - 1]] + first[sn]) / 2
        b = (last[sn] + first[order[i + 1]]) / 2 if i + 1 < len(order) else last[sn] + 2.0
        intervals.append((sn, a, b))
    total = intervals[-1][2]

    slide_imgs = {sn: Image.open(os.path.join(png_dir, f"s-{sn:02d}.png")).convert("RGB")
                  for sn in order}
    bg_colors = {sn: img.getpixel((12, 620)) for sn, img in slide_imgs.items()}

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-i", os.path.join(build_dir, "audio.wav"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-shortest", out_path], stdin=subprocess.PIPE)

    nframes = int(total * FPS)
    for fi in range(nframes):
        now = fi / FPS
        sn, a, b = next(((s, x, y) for s, x, y in intervals if x <= now < y), intervals[-1])
        frame = slide_imgs[sn].copy()
        bgc = bg_colors[sn]

        # ghost / reveal anchored regions
        for (x, y, w2, h2), tr in reveals.get(sn, {}).items():
            if now >= tr + REVEAL_S:
                continue
            f = 0.0 if now < tr else (now - tr) / REVEAL_S
            alpha = GHOST * (1 - f) ** 2
            if alpha <= 0.01:
                continue
            x0, y0 = max(0, int(x)), max(0, int(y))
            x1, y1 = min(W, int(x + w2)), min(H, int(y + h2))
            crop = frame.crop((x0, y0, x1, y1))
            veil = Image.new("RGB", crop.size, bgc)
            frame.paste(Image.blend(crop, veil, alpha), (x0, y0))

        d = ImageDraw.Draw(frame)

        # marker + chip for the current segment
        active = [m for m in markers if m[2] == sn and m[0] <= now < m[1] + 0.15]
        if active:
            t0, t1, _, reg, kind = active[-1]
            col = KIND_COLORS[kind]
            if reg:
                x, y, w2, h2 = reg
                d.rounded_rectangle([x - 8, y - 8, x + w2 + 8, y + h2 + 8], radius=20,
                                    outline=tuple(min(255, int(v * 0.55 + 130)) for v in col),
                                    width=8)
                d.rounded_rectangle([x - 6, y - 6, x + w2 + 6, y + h2 + 6], radius=18,
                                    outline=col, width=4)
            chip = KIND_LABEL[kind]
            cw = d.textlength(chip, font=F_CHIP)
            cx = (W - cw) / 2 - 20
            d.rounded_rectangle([cx, H - 52, cx + cw + 40, H - 14], radius=19,
                                fill=(255, 255, 255), outline=col, width=2)
            d.text((cx + 20, H - 45), chip, font=F_CHIP, fill=col)
            if kind == "yourturn" and t1 > t0:
                remain = max(0.0, min(1.0, (t1 - now) / (t1 - t0)))
                d.rounded_rectangle([cx, H - 62, cx + (cw + 40) * remain, H - 57],
                                    radius=2, fill=col)

        # progress bar (deck coral)
        d.rectangle([0, H - 6, int(W * now / total), H], fill=(232, 93, 93))

        # dip-to-white between slides
        wa = 0.0
        for _, aa, _ in intervals[1:]:
            if aa - 0.25 <= now < aa:
                wa = (now - (aa - 0.25)) / 0.25
            elif aa <= now < aa + 0.35:
                wa = 1 - (now - aa) / 0.35
        if wa > 0:
            frame = Image.blend(frame, Image.new("RGB", (W, H), (255, 255, 255)), wa * 0.95)

        ff.stdin.write(frame.tobytes())
        if fi % 300 == 0:
            print(f"frame {fi}/{nframes} ({now:.0f}s)")

    ff.stdin.close()
    ff.wait()
    print("wrote", out_path)


if __name__ == "__main__":
    main(*sys.argv[1:5])
