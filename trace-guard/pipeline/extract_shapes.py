#!/usr/bin/env python3
"""Extract per-slide shape bounding boxes + text from the study deck pptx.

Writes shapes.json: {slide_number: [{x,y,w,h,text}, ...]} in 1920x1080 pixel space.
Top-level shapes and groups only — these are the deck's visual "rows"/cards.
"""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
EMU_W, EMU_H = 12192000, 6858000
SX, SY = 1920 / EMU_W, 1080 / EMU_H


def shape_bbox_text(el):
    xfrm = el.find(".//a:xfrm", NS)
    if xfrm is None:
        return None
    off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    x, y = int(off.get("x")) * SX, int(off.get("y")) * SY
    w, h = int(ext.get("cx")) * SX, int(ext.get("cy")) * SY
    text = " ".join(t.text or "" for t in el.findall(".//a:t", NS))
    return dict(x=round(x), y=round(y), w=round(w), h=round(h),
                text=re.sub(r"\s+", " ", text).strip())


def main(pptx, out):
    z = zipfile.ZipFile(pptx)
    result = {}
    for name in z.namelist():
        m = re.match(r"ppt/slides/slide(\d+)\.xml$", name)
        if not m:
            continue
        tree = ET.fromstring(z.read(name))
        sptree = tree.find(".//p:cSld/p:spTree", NS)
        shapes = []
        for el in sptree:
            tag = el.tag.split("}")[1]
            if tag not in ("sp", "grpSp", "pic", "graphicFrame", "cxnSp"):
                continue
            info = shape_bbox_text(el)
            if info and info["w"] > 8 and info["h"] > 8:
                shapes.append(info)
        result[int(m.group(1))] = shapes
    json.dump(result, open(out, "w"))
    print(f"wrote {out}: {len(result)} slides")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
