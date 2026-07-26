# Changelog

**This file is maintained by [release-please](https://github.com/googleapis/release-please).**
Do not edit the generated sections by hand — write
[conventional commits](CONTRIBUTING.md#commit-messages) and they will appear
here on the next release.

A release here is a snapshot of the **design and its documentation**, not a
fabricated board revision. Board revisions are `control.*`, `control1.*`,
`control2.*` and the unpublished V1.1; see [README.md](README.md).

<!-- release-please inserts new versions directly below this line -->

## Fork baseline

Context for everything above, written by hand before release automation existed.

OSU OSL's fork of [`lshw/prc`](https://github.com/lshw/prc) by Liu Shiwei, who
designed the board. Fork point is
[`5bf428b`](https://github.com/lshw/prc/commit/5bf428b) (2020-02-01); upstream
has not changed since.

The baseline translated all Chinese text (README, prototype sketch comments,
`link.txt`, the BOM part-number column — no schematic, layout, footprint, BOM
value or centroid data was touched), added `AGENTS.md` as a hardware reference
derived from the layout's embedded `NetList()`, translated the vendor manuals
under `doc/` with images mirrored locally, and added `tools/check_bom.py` plus
CI.

It also corrected the README, which claimed support for 32 temperature probes
where the firmware supports 10.

### Open hardware questions from the baseline

- **R5 is `27k` in both BOMs and the rendered schematic, `72k` in all three
  layouts.** It sets the MP1584 under-voltage lockout, so that is a ~7.0 V
  versus ~3.6 V minimum input — whether the board starts at the advertised 5 V.
  Needs measuring on a physical board. Baselined in
  `tools/known_bom_issues.txt` so CI blocks on new drift meanwhile.
- **`control2.*`, the final layout, was never exported for assembly** — no BOM,
  no XY, and the Gerber zips predate it.
- **C4** is `0.01uF` on the schematic but ordered as `100nF` in both BOMs.
- **No design files exist for V1.1**, which is the revision actually sold.
