#!/usr/bin/env python3
import sys
import zipfile
import copy
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def qn(tag):
    return f"{{{W}}}{tag}"


MAPPING = {
    "ElsDocumenttitle": "Title",
    "ElsAuthor": "Author",
    "ElsAbstractText": "Abstract",
    "ElsAbstractHead": "AbstractTitle",
    "ElsReferences": "Bibliography",
    "ElsParagraph": "BodyText",
    "ElsHeading1": "Heading1",
    "ElsHeading2": "Heading2",
    "ElsHeading3": "Heading3",
    "ElsHeading4": "Heading4",
    "ElsHeading5": "Heading5",
}
EXTRA_TARGETS = {"ElsParagraph": ["BodyText", "FirstParagraph"]}


def find_style(root, style_id):
    return root.find(f'.//w:style[@w:styleId="{style_id}"]', namespaces=NS)


def remap(src_path, dst_path):
    with zipfile.ZipFile(src_path) as zin:
        styles_xml = zin.read("word/styles.xml")

    root = etree.fromstring(styles_xml)
    report = []

    for els_id, base_target in MAPPING.items():
        targets = EXTRA_TARGETS.get(els_id, [base_target])
        els_style = find_style(root, els_id)
        if els_style is None:
            report.append(f"SKIP   {els_id}: not found in this file")
            continue

        renamed_in_place = False
        for target_id in targets:
            target_style = find_style(root, target_id)
            if target_style is None:
                if not renamed_in_place:
                    els_style.set(qn("styleId"), target_id)
                    name_el = els_style.find("w:name", NS)
                    if name_el is not None:
                        name_el.set(qn("val"), target_id)
                    report.append(f"RENAME {els_id} -> {target_id} (no prior style existed)")
                    renamed_in_place = True
                else:
                    report.append(f"SKIP   {target_id}: not present, nothing to transplant onto")
                continue

            for tag in ("w:pPr", "w:rPr"):
                old = target_style.find(tag, NS)
                new = els_style.find(tag, NS)
                if old is not None:
                    target_style.remove(old)
                if new is not None:
                    target_style.insert(0, copy.deepcopy(new))
            report.append(f"MERGE  {els_id} formatting -> existing {target_id} style")

        if not renamed_in_place and els_style.get(qn("styleId")) == els_id:
            parent = els_style.getparent()
            parent.remove(els_style)

    old_to_new = {k: EXTRA_TARGETS.get(k, [v])[0] for k, v in MAPPING.items()}
    for ref_tag in ("w:basedOn", "w:next", "w:link"):
        for el in root.findall(f'.//{ref_tag}', NS):
            val = el.get(qn("val"))
            if val in old_to_new:
                el.set(qn("val"), old_to_new[val])

    new_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)

    with zipfile.ZipFile(src_path) as zin:
        contents = {n: zin.read(n) for n in zin.namelist()}
    contents["word/styles.xml"] = new_xml
    with zipfile.ZipFile(dst_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for n, data in contents.items():
            zout.writestr(n, data)

    print("\n".join(report))
    print(f"\nwrote {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: remap_styles.py src.docx dst.docx")
        sys.exit(1)
    remap(sys.argv[1], sys.argv[2])
