#!/usr/bin/env python3
"""Build a new RCA case's slides by cloning the study deck's Case One layouts.

Takes a case content module (see cases/SPEC.md) and produces:
  <out>/case.pptx        12 slides cloned from deck templates, text swapped
  <out>/png/s-01..12.png rasterized 1920x1080 slides
  <out>/shapes.json      shape bboxes+text keyed "1".."12" (render2-compatible)

Usage: python3 build_case.py DECK.pptx cases/mycase.py OUT_DIR
"""
import importlib.util, json, os, re, shutil, subprocess, sys, zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))

# template slide -> ordered slot map: slot key -> unique substring of the
# template shape's text (matched against concatenated <a:t> runs)
TEMPLATES = [
    (52, dict(case_label="CASE ONE",
              title="The enterprise knowledge assistant that suddenly",
              key_lesson="Key lesson: the user-visible symptom")),
    (53, dict(title="Interviewer opening",
              quote="An enterprise knowledge assistant answers employee questions",
              flow1="Translate the product contract", flow2="Restate the observed outcome",
              flow3="Keep “the user can open the source”", flow4="Treat faster latency")),
    (54, dict(title="How a strong candidate opens",
              quote="Let me first translate the incident",
              beat1="Name product + goal", beat2="Expected vs observed", beat3="Metric + onset",
              beat4="Qualify the source claim", beat5="Ask two high-value clarifiers")),
    (55, dict(title="Do not collapse “source exists”",
              think1="A document can fail at ingestion", think2="Fallback does not prove",
              think3="Faster + worse may mean",
              board_label="INCIDENT CARD", board="Product: enterprise document QA",
              cheat="Clarify the exact failure signal", senior="Clarify the user contract",
              nug1="Source exists ≠ source reached model", nug2="Fallback is an outcome",
              nug3="Faster can mean skipped work")),
    (56, dict(title="Interviewer gives the blast-radius boundary",
              quote="The metric definition is unchanged",
              flow1="State what is not global", flow2="Name the narrow predictive condition",
              flow3="Lower the probability of model-wide", flow4="Ask for a matched healthy request")),
    (57, dict(title="Turn the cohort split into a subsystem hypothesis",
              quote="The failure is concentrated in Google Workspace tenants",
              beat1="Summarize affected vs unaffected", beat2="Say what becomes less likely",
              beat3="Say what becomes more likely", beat4="Request a matched control cohort")),
    (62, dict(title="Interviewer gives stage metrics",
              subtitle="The expected document survives retrieval",
              m1="RETRIEVED", v1="190/200", m2="AFTER PERMISSION", v2="184/200",
              m3="TOP 3", v3="174/184", m4="SUFFICIENCY", v4="169/174",
              trace_label="AFFECTED TRACE",
              chip1="Query processed", chip2="Expected source rank #2",
              chip3="NO_MATCHING_PRINCIPAL", chip4="Weak candidates",
              chip5="Sufficiency fail", chip6="Generation skipped",
              bottom="The first new loss is permission filtering")),
    (63, dict(title="Make the evidence update explicit",
              quote="The expected document is still found",
              beat1="State the first divergence", beat2="Close downstream branches",
              beat3="Name the new two-way fork", beat4="Request exact principal vs ACL inputs")),
    (65, dict(title="Interviewer reveals the rollout",
              subtitle="Canonicalization v1 succeeds",
              colA_label="TIMING", colA1="v2 rollout begins 9:32", colA2="50% at 9:36",
              colA3="100% at 9:40", colA4="Incident begins at 9:40",
              colB_label="V1", colB1="27 principals", colB2="GWS alias present",
              colB3="Permission ALLOW", colB4="Correct answer",
              colC_label="V2", colC1="19 principals", colC2="GWS alias missing",
              colC3="Permission DENY", colC4="Fallback")),
    (66, dict(title="State the causal chain and stop",
              quote="The primary root cause",
              diag1="Cause: v2 representation change", diag2="Mechanism: no principal",
              diag3="Timing: 100% rollout", diag4="Evidence: controlled replay",
              diag5="Alternative: stale ACL index")),
    (70, dict(title="Design for compatibility, semantic comparison",
              subtitle="Compare final authorization outcomes",
              ask="Walk me through your system",
              arch1_label="IDENTITY GRAPH", arch1="Stable canonical ID + explicit aliases",
              arch2_label="COMPATIBLE SERVING", arch2="Emit canonical identity plus supported aliases",
              arch3_label="SEMANTIC SHADOWING", arch3="Old vs new authorization decision diff",
              arch4_label="RECOVERY", arch4="Feature flag · rollback · replay",
              footer="Cheat sheet: Prevent · detect · recover")),
    (73, dict(title="Case One in six moves",
              subtitle="From “cannot find it”",
              move1="Retrieval looks suspicious", move2="Scope points to group-shared",
              move3="Trace shows source survives", move4="First divergence is permission filtering",
              move5="v2 removes ACL-matching alias", move6="Replay reproduces + reverses")),
]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("“", '"').replace("”", '"').replace("’", "'")
                  .replace("—", "-")).strip().lower()


def replace_in_shape_xml(sp_xml, new_text):
    """Distribute new_text lines across the shape's <a:t> runs (extras blanked)."""
    lines = new_text.split("\n")
    parts = re.split(r"(<a:t>.*?</a:t>)", sp_xml, flags=re.S)
    n_ts = sum(1 for p in parts if p.startswith("<a:t>"))
    vals = []
    if n_ts >= len(lines):
        vals = lines + [""] * (n_ts - len(lines))
    else:
        vals = lines[:n_ts - 1] + [" ".join(lines[n_ts - 1:])]
    ti = 0
    for i, p in enumerate(parts):
        if p.startswith("<a:t>"):
            parts[i] = "<a:t>" + escape(vals[ti]) + "</a:t>"
            ti += 1
    return "".join(parts)


def apply_slots(xml, slotmap, values, ctx):
    # split into top-level-ish sp blocks; <a:t> only lives inside sp/txBody
    blocks = re.split(r"(<p:sp>.*?</p:sp>)", xml, flags=re.S)
    used = set()
    for key, orig in slotmap.items():
        if key not in values:
            continue
        target = norm(orig)
        hit = None
        for i, b in enumerate(blocks):
            if not b.startswith("<p:sp>") or i in used:
                continue
            text = norm(" ".join(re.findall(r"<a:t>(.*?)</a:t>", b, flags=re.S)))
            if target in text:
                hit = i
                break
        if hit is None:
            raise KeyError(f"{ctx}: slot '{key}' original not found: {orig!r}")
        blocks[hit] = replace_in_shape_xml(blocks[hit], str(values[key]))
        used.add(hit)
    return "".join(blocks)


def auto_slots(xml, template_no, seq_no, case_label):
    """Footer 'Case One' -> case label; page number -> sequence number."""
    xml = xml.replace("<a:t>Case One</a:t>", f"<a:t>{escape(case_label)}</a:t>")
    xml = xml.replace(f"<a:t>{template_no}</a:t>", f"<a:t>{seq_no:02d}</a:t>")
    return xml


def main(deck, case_py, out_dir):
    spec = importlib.util.spec_from_file_location("case_content", case_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    SLOTS, CASE = mod.SLOTS, mod.CASE

    os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "unpacked")
    if os.path.exists(work):
        shutil.rmtree(work)
    zipfile.ZipFile(deck).extractall(work)

    add_slide = "/root/.claude/skills/synced/pptx/scripts/add_slide.py"
    new_files = []
    for tno, _ in TEMPLATES:
        r = subprocess.run([sys.executable, add_slide, work, f"slide{tno}.xml"],
                           capture_output=True, text=True, check=True)
        m = re.search(r"(ppt/slides/slide\d+\.xml)", r.stdout)
        new_files.append(m.group(1))

    # rewrite sldIdLst to only the new slides, in order
    pres_path = os.path.join(work, "ppt/presentation.xml")
    rels_path = os.path.join(work, "ppt/_rels/presentation.xml.rels")
    rels = open(rels_path).read()
    rid_by_file = {m.group(2): m.group(1) for m in
                   re.finditer(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels)}
    for m in re.finditer(r'Target="slides/(slide\d+\.xml)"[^>]*Id="(rId\d+)"', rels):
        rid_by_file[m.group(1)] = m.group(2)
    pres = open(pres_path).read()
    ids = re.findall(r'<p:sldId id="(\d+)"', pres)
    next_id = max(int(i) for i in ids) + 100
    entries = "".join(
        f'<p:sldId id="{next_id + i}" r:id="{rid_by_file[os.path.basename(f)]}"/>'
        for i, f in enumerate(new_files))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{entries}</p:sldIdLst>",
                  pres, flags=re.S)
    open(pres_path, "w").write(pres)

    # apply text replacements
    for i, ((tno, slotmap), f) in enumerate(zip(TEMPLATES, new_files)):
        p = os.path.join(work, f)
        xml = open(p).read()
        vals = SLOTS.get(f"s{i+1}", {})
        xml = apply_slots(xml, slotmap, vals, f"s{i+1} (template {tno})")
        xml = auto_slots(xml, tno, i + 1, CASE["label"])
        open(p, "w").write(xml)

    subprocess.run([sys.executable, "/root/.claude/skills/synced/pptx/scripts/clean.py", work],
                   check=True, capture_output=True)
    pptx = os.path.join(out_dir, "case.pptx")
    if os.path.exists(pptx):
        os.remove(pptx)
    subprocess.run(["zip", "-Xrq", os.path.abspath(pptx), "."], cwd=work, check=True)

    # rasterize
    png_dir = os.path.join(out_dir, "png")
    os.makedirs(png_dir, exist_ok=True)
    for f in os.listdir(png_dir):
        os.remove(os.path.join(png_dir, f))
    subprocess.run(["soffice", "--headless",
                    f"-env:UserInstallation=file://{out_dir}/loprofile",
                    "--convert-to", "pdf", "--outdir", out_dir, pptx],
                   check=True, capture_output=True)
    subprocess.run(["pdftoppm", "-png", "-scale-to-x", "1920", "-scale-to-y", "1080",
                    os.path.join(out_dir, "case.pdf"), os.path.join(png_dir, "s")], check=True)

    # shapes.json keyed by sequence position
    sys.path.insert(0, HERE)
    import extract_shapes
    tmp = os.path.join(out_dir, "_shapes_raw.json")
    extract_shapes.main(pptx, tmp)
    raw = json.load(open(tmp))
    seq = {}
    ordered = sorted(raw.keys(), key=int)
    for i, k in enumerate(ordered):
        seq[str(i + 1)] = raw[k]
    json.dump(seq, open(os.path.join(out_dir, "shapes.json"), "w"))
    print(f"built {pptx}: {len(new_files)} slides, PNGs in {png_dir}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
