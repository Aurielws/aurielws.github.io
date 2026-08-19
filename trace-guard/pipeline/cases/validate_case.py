#!/usr/bin/env python3
"""Validate a case content file: slot limits, SEGS rules, anchors vs built shapes.

Usage:
  python3 validate_case.py cases/mycase.py                 # content-only checks
  python3 validate_case.py cases/mycase.py BUILD/shapes.json  # + anchor checks
"""
import importlib.util, json, re, sys

LIMITS = {
 "s1": dict(case_label=12, title=80, key_lesson=110),
 "s2": dict(title=40, quote=330, flow1=95, flow2=95, flow3=95, flow4=95),
 "s3": dict(title=52, quote=300, beat1=28, beat2=28, beat3=28, beat4=28, beat5=28),
 "s4": dict(title=55, think1=75, think2=75, think3=75, board_label=16, board=None,
            cheat=60, senior=75, nug1=38, nug2=38, nug3=38),
 "s5": dict(title=45, quote=230, flow1=75, flow2=75, flow3=75, flow4=75),
 "s6": dict(title=50, quote=300, beat1=32, beat2=32, beat3=32, beat4=32),
 "s7": dict(title=50, subtitle=80, m1=16, m2=16, m3=16, m4=16, v1=20, v2=20, v3=20,
            v4=20, trace_label=16, chip1=24, chip2=24, chip3=24, chip4=24, chip5=24,
            chip6=24, bottom=95),
 "s8": dict(title=35, quote=300, beat1=36, beat2=36, beat3=36, beat4=36),
 "s9": dict(title=55, subtitle=72, colA_label=10, colA1=22, colA2=22, colA3=22,
            colA4=22, colB_label=10, colB1=18, colB2=18, colB3=18, colB4=18,
            colC_label=10, colC1=18, colC2=18, colC3=18, colC4=18),
 "s10": dict(title=32, quote=380, diag1=40, diag2=40, diag3=40, diag4=40, diag5=40),
 "s11": dict(title=64, subtitle=58, ask=55, arch1_label=20, arch2_label=20,
             arch3_label=20, arch4_label=20, arch1=62, arch2=62, arch3=62, arch4=62,
             footer=105),
 "s12": dict(title=25, subtitle=55, move1=38, move2=38, move3=38, move4=38,
             move5=38, move6=38),
}
KINDS = {"teach", "attrib", "interviewer", "say", "think", "rule", "yourturn"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("“", '"').replace("”", '"').replace("’", "'")
                  .replace("—", "-")).strip().lower()


def main(case_py, shapes_json=None):
    spec = importlib.util.spec_from_file_location("case_content", case_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    errs = []

    for sid, limits in LIMITS.items():
        slots = mod.SLOTS.get(sid, {})
        for k, lim in limits.items():
            if k not in slots:
                errs.append(f"{sid}: missing slot '{k}'")
            elif k == "board":
                lines = slots[k].split("\n")
                if len(lines) != 5:
                    errs.append(f"{sid}.board: needs exactly 5 lines, got {len(lines)}")
                for ln in lines:
                    if len(ln) > 45:
                        errs.append(f"{sid}.board line too long ({len(ln)}): {ln!r}")
            elif lim and len(str(slots[k])) > lim:
                errs.append(f"{sid}.{k}: {len(str(slots[k]))} chars > {lim}: {str(slots[k])[:60]!r}")
        for k in slots:
            if k not in limits:
                errs.append(f"{sid}: unknown slot '{k}'")

    ids = set()
    total = 0
    prev_kind = None
    for s in mod.SEGS:
        if s["id"] in ids:
            errs.append(f"dup seg id {s['id']}")
        ids.add(s["id"])
        total += len(s["text"])
        if s["kind"] not in KINDS:
            errs.append(f"{s['id']}: bad kind {s['kind']}")
        if s["speaker"] not in ("dan", "rachel"):
            errs.append(f"{s['id']}: bad speaker")
        if s["kind"] in ("interviewer", "rule") and s["speaker"] != "rachel":
            errs.append(f"{s['id']}: {s['kind']} must be rachel")
        if s["kind"] == "yourturn" and not s.get("pause_extra"):
            errs.append(f"{s['id']}: yourturn needs pause_extra")
        if prev_kind == "interviewer" and s["kind"] != "yourturn":
            errs.append(f"{s['id']}: every interviewer segment must be followed by a yourturn")
        if not 1 <= s["slideno"] <= 12:
            errs.append(f"{s['id']}: slideno out of range")
        for _, sub in s.get("spans", []):
            if sub not in s["text"]:
                errs.append(f"{s['id']}: span substring not in text: {sub!r}")
        prev_kind = s["kind"]

    slot_text = {i: " || ".join(norm(str(v)) for v in mod.SLOTS.get(f"s{i}", {}).values())
                 for i in range(1, 13)}
    for s in mod.SEGS:
        anchors = [a for a, _ in s.get("spans", [])] + ([s["anchor"]] if s.get("anchor") else [])
        for a in anchors:
            if norm(a) not in slot_text[s["slideno"]]:
                errs.append(f"{s['id']}: anchor not found in slide s{s['slideno']} slots: {a!r}")

    if shapes_json:
        shapes = json.load(open(shapes_json))
        for s in mod.SEGS:
            anchors = [a for a, _ in s.get("spans", [])] + ([s["anchor"]] if s.get("anchor") else [])
            for a in anchors:
                if not any(norm(a) in norm(sh["text"]) for sh in shapes[str(s["slideno"])] if sh["text"]):
                    errs.append(f"{s['id']}: anchor not found in BUILT slide {s['slideno']}: {a!r}")

    if not (5500 <= total <= 8500):
        errs.append(f"total spoken chars {total} outside 5500-8500 (target 6500-8000)")
    for e in errs:
        print("ERROR:", e)
    print(f"{'PASS' if not errs else 'FAIL'}: {len(mod.SEGS)} segments, {total} spoken chars")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main(*sys.argv[1:3])
