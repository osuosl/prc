# Changelog

Notable changes to OSU OSL's fork of [`lshw/prc`](https://github.com/lshw/prc).
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

This repository holds a hardware design, so releases are rare — a version here
would correspond to a board revision actually fabricated, not to a code drop.

## [Unreleased]

### Changed

- **All Chinese text translated to English** — `README.md`,
  `control/control.ino`, the `link.txt` cable table, and the `编号` (part
  number) column header in both BOMs. No schematic, layout, footprint, BOM value
  or pick-and-place data was touched.
- `README.md` rewritten for a maintained fork, and corrected: it previously
  claimed support for 32 temperature probes, where the shipped firmware supports
  10.

### Added

- `AGENTS.md` — hardware reference derived from the layout's embedded
  `NetList()`: MCU pin map, connector pinouts, power tree, the back-to-back
  MOSFET output switch, and how the DS18B20 ROM code becomes the device
  identity.
- `doc/` — vendor pages translated with images mirrored locally:
  the [hardware manual](doc/node-914-hardware-manual.md),
  the [motherboard COM header](doc/node-953-motherboard-com-header.md), and
  the [V1.1 board render](doc/node-954-procv1.1-hardware.md).
- `tools/check_bom.py` — cross-checks the BOM and pick-and-place exports against
  the layout they came from. Pure stdlib, no EDA tooling. Runs in CI.
- CI: BOM/layout consistency and a markdown link check.
- `CONTRIBUTING.md` and this changelog.

### Known issues

Tracked at <https://github.com/osuosl/prc/issues>:

- **R5 disagrees between the files** — `27k` in both BOMs and the rendered
  schematic, `72k` in all three layouts. It sets the MP1584 under-voltage
  lockout, so this is ~7.0 V versus ~3.6 V minimum input. Needs measuring on a
  physical board. Baselined in `tools/known_bom_issues.txt` until resolved.
- **`control2.*` was never exported for assembly** — no BOM or XY files exist
  for the final layout, and the Gerber zips predate it.
- **C4** is `0.01uF` on the schematic but ordered as `100nF` in both BOMs.
- **No V1.1 design files exist anywhere**, though V1.1 is what is sold. The
  render on the vendor site is the only public artefact.

---

Upstream history before the fork is in `git log`. The fork point is
[`5bf428b`](https://github.com/lshw/prc/commit/5bf428b) (2020-02-01); upstream
has not changed since.
