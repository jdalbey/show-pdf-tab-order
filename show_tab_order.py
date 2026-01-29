#!/usr/bin/env python3
"""
Display PDF form fields in the order Evince/Firefox will tab through them.
Uses the same visual/geometric sorting that Evince/Firefox uses.
Output appears in terminal in multi-column format that includes coordinates.
Dependencies:  qpdf
MIT License
by John Dalbey
Version 2026-01-28
"""

import subprocess
import re
import sys
from pathlib import Path

def get_form_fields(pdf_path):
    """Extract form field info using qpdf."""
    # Convert to QDF format for easier parsing
    qdf_path = pdf_path.with_suffix(".temp.qdf")
    subprocess.run([
        "qpdf",
        "--qdf",
        "--object-streams=disable",
        str(pdf_path),
        str(qdf_path)
    ], check=True, capture_output=True)

    # Read QDF text
    text = qdf_path.read_text(encoding="latin1")

    # Find all widget annotations (form fields)
    fields = []
    for match in re.finditer(r"(\d+\s+\d+)\s+obj.*?endobj", text, re.DOTALL):
        obj_text = match.group(0)

        # Check if this is a form field widget
        if "/Subtype /Widget" not in obj_text:
            continue

        # Extract field name
        name_match = re.search(r"/T\s*\((.*?)\)", obj_text)
        name = name_match.group(1) if name_match else "Unknown"

        # Extract rectangle coordinates
        rect_match = re.search(r"/Rect\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", obj_text)
        if not rect_match:
            continue

        x1, y1, x2, y2 = map(float, rect_match.groups())

        # Calculate center point (same as Evince does)
        center_x = x1 + (x2 - x1) / 2
        center_y = y1 + (y2 - y1) / 2

        fields.append({
            "name": name,
            "center_x": center_x,
            "center_y": center_y,
            "rect": (x1, y1, x2, y2)
        })

    # Clean up temp file
    qdf_path.unlink()

    return fields

def sort_by_evince_order(fields):
    """Sort fields the same way Evince does: top-to-bottom, then left-to-right."""
    # Evince sorts by Y descending (higher Y = top of page in PDF coords),
    # then by X ascending (left to right)
    return sorted(fields, key=lambda f: (-f["center_y"], f["center_x"]))

def main(pdf_path):
    pdf = Path(pdf_path)
    if not pdf.exists():
        print(f"Error: {pdf_path} not found")
        sys.exit(1)

    print(f"Analyzing: {pdf_path}")
    print("=" * 70)

    # Get and sort fields
    fields = get_form_fields(pdf)
    sorted_fields = sort_by_evince_order(fields)

    # Display results
    print("\nEvince tab order (top to bottom, left to right):\n")
    print(f"{'#':<4} {'Field Name':<20} {'Center X':>10} {'Center Y':>10} {'Rect (x1, y1, x2, y2)'}")
    print("-" * 100)

    for idx, field in enumerate(sorted_fields, 1):
        rect_str = f"({field['rect'][0]:.2f}, {field['rect'][1]:.2f}, {field['rect'][2]:.2f}, {field['rect'][3]:.2f})"
        print(f"{idx:<4} {field['name']:<20} {field['center_x']:>10.2f} {field['center_y']:>10.2f} {rect_str}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: show_tab_order.py <input.pdf>")
        sys.exit(1)
    main(sys.argv[1])
