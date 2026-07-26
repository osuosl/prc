#!/usr/bin/env python3
"""Cross-check the JLCPCB assembly files against the PCB layout they came from.

The BOM and pick-and-place CSVs are exported from the layout, but they are
exported *by hand* and then edited by hand, so they drift. This has already
happened at least once: R5 is 27k in both BOMs and in the rendered schematic,
but 72k in the layout, which moves the MP1584 input under-voltage lockout
between roughly 7.0 V and 3.6 V -- i.e. whether the board starts at the 5 V the
README advertises.

Nothing here needs an EDA tool; both formats are plain text.

Usage:  tools/check_bom.py            # check every known pcb/bom/xy set
        tools/check_bom.py --quiet    # only print problems
Exit status is non-zero if any mismatch is found.
"""

import argparse
import csv
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

# (layout, bom, xy). control2.pcb is deliberately absent -- see check_unexported().
SETS = [
    ("control.pcb", "control_bom.csv", "control_xy.csv"),
    ("control1.pcb", "control1_bom.csv", "control1_xy.csv"),
]

# Element["<flags>" "<footprint>" "<refdes>" "<value>" ...]
ELEMENT_RE = re.compile(r'^Element\["([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)"')


def norm(value):
    """Values are hand-typed, so compare them case- and space-insensitively.
    '100uF/6.3v' and '100UF/6.3V' are the same part; '27k' and '72k' are not."""
    return value.strip().lower().replace(" ", "")


def read_pcb(path):
    """refdes -> (footprint, value) for every placed element."""
    out = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = ELEMENT_RE.match(line)
        if not m:
            continue
        _flags, footprint, refdes, value = m.groups()
        if refdes:
            out[refdes] = (footprint, value)
    return out


def read_bom(path):
    """refdes -> (footprint, value).

    Column header says 'Description' but the column actually holds a
    space-separated list of reference designators. Upstream naming, left as-is
    so the file still matches what JLCPCB expects.
    """
    out = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for row in csv.reader(fh):
            if len(row) < 4 or row[0].strip().lower() == "quantity":
                continue
            footprint, value, refdes_field = row[1].strip(), row[2].strip(), row[3].strip()
            for refdes in refdes_field.split():
                out[refdes] = (footprint, value)
    return out


def read_xy(path):
    """refdes -> (footprint, value). Here 'Description' really is the refdes."""
    out = {}
    with path.open(encoding="utf-8", errors="replace") as fh:
        for row in csv.reader(fh):
            if len(row) < 3 or row[0].strip().lower() == "description":
                continue
            out[row[0].strip()] = (row[1].strip(), row[2].strip())
    return out


def compare(problems, layout_name, pcb, other_name, other):
    """Compare one exported file against the layout it was exported from."""
    only_pcb = sorted(set(pcb) - set(other))
    only_other = sorted(set(other) - set(pcb))

    # Parts legitimately absent from an assembly export: through-hole connectors,
    # the crystal (never populated -- the firmware runs the internal RC), and
    # anything hand-soldered. Report as info, not failure.
    if only_pcb:
        problems.append(
            ("info", f"{layout_name}: {len(only_pcb)} part(s) not in {other_name}: "
                     f"{', '.join(only_pcb)}")
        )
    if only_other:
        problems.append(
            ("error", f"{other_name} lists part(s) absent from {layout_name}: "
                      f"{', '.join(only_other)}")
        )

    for refdes in sorted(set(pcb) & set(other)):
        pcb_fp, pcb_val = pcb[refdes]
        oth_fp, oth_val = other[refdes]
        if norm(pcb_val) != norm(oth_val):
            problems.append(
                ("error", f"{refdes}: value differs -- {layout_name} says "
                          f"'{pcb_val}', {other_name} says '{oth_val}'")
            )
        if norm(pcb_fp) != norm(oth_fp):
            problems.append(
                ("error", f"{refdes}: footprint differs -- {layout_name} says "
                          f"'{pcb_fp}', {other_name} says '{oth_fp}'")
            )


def check_unexported(problems):
    """The newest layout must have assembly files, or a fab order will silently
    be placed from a stale export."""
    layouts = sorted(REPO.glob("control*.pcb"))
    exported = {s[0] for s in SETS}
    for layout in layouts:
        if layout.name not in exported:
            problems.append(
                ("warn", f"{layout.name} has no BOM/XY export. Anything sent to a "
                         f"fab must be re-exported from the newest layout.")
            )


def load_known(path):
    """Substrings of findings that are already tracked as issues. They are still
    printed, but do not fail the run -- so CI blocks on *new* drift without
    being permanently red over something already filed."""
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="only print problems")
    ap.add_argument(
        "--allow-known",
        action="store_true",
        help="downgrade findings listed in tools/known_bom_issues.txt",
    )
    args = ap.parse_args()
    known = load_known(REPO / "tools" / "known_bom_issues.txt") if args.allow_known else []

    problems = []
    for pcb_name, bom_name, xy_name in SETS:
        pcb_path, bom_path, xy_path = (REPO / n for n in (pcb_name, bom_name, xy_name))
        if not pcb_path.exists():
            problems.append(("error", f"{pcb_name} is missing"))
            continue
        pcb = read_pcb(pcb_path)
        if not args.quiet:
            print(f"{pcb_name}: {len(pcb)} placed elements")
        for name, path, reader in (
            (bom_name, bom_path, read_bom),
            (xy_name, xy_path, read_xy),
        ):
            if not path.exists():
                problems.append(("error", f"{name} is missing"))
                continue
            other = reader(path)
            if not args.quiet:
                print(f"  vs {name}: {len(other)} entries")
            compare(problems, pcb_name, pcb, name, other)

    check_unexported(problems)

    graded = []
    for level, msg in problems:
        if level == "error" and any(k in msg for k in known):
            level = "known"
        graded.append((level, msg))

    errors = [p for p in graded if p[0] == "error"]
    for level, msg in graded:
        if args.quiet and level == "info":
            continue
        prefix = {"error": "ERROR", "warn": "WARN ", "info": "info ", "known": "known"}[level]
        print(f"{prefix}  {msg}")

    print()
    print(f"{len(errors)} new error(s), "
          f"{len([p for p in graded if p[0] == 'known'])} known, "
          f"{len([p for p in graded if p[0] == 'warn'])} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
