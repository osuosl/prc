# prc — PROC-V1 remote management board (hardware)

[![CI](https://github.com/osuosl/prc/actions/workflows/ci.yml/badge.svg)](https://github.com/osuosl/prc/actions/workflows/ci.yml)

Hardware design for **PROC-V1**, a small board that gives a PC out-of-band
management: network-controlled power and reset buttons, and the machine's serial
console exposed over TCP. Roughly "poor man's IPMI" for hardware without a BMC.

gEDA schematic and PCB, Gerbers, BOM and pick-and-place files.

![PROC-V1 schematic and board](control.png)

## ⚠ The firmware is not in this repository

`control/control.ino` here is an **abandoned 182-line prototype** — no menu, no
authentication, no DHCP, no temperature support. It is not what runs on the
boards.

The firmware lives in **[osuosl/proc](https://github.com/osuosl/proc)**. It was
seeded from this file on 2020-01-02 and developed for another five years; the
two still differ by only 11 lines. The commit IDs baked into the released `.hex`
images don't exist in this repository at all.

## What the board does

| | |
|---|---|
| MCU | ATmega328PB, TQFP-32, **3.3 V / 8 MHz on the internal RC oscillator** |
| Network | W5500 10/100 Ethernet with hardware TCP/IP, on SPI |
| Serial | SP3232, RS-232 level, 300–921600 bps. TTL pads also broken out |
| Switch outputs | 2× EL357N optocouplers → host power and reset headers |
| Power output | 4× AO4407A P-FETs, back-to-back, switched 5–28 V |
| Input | 5–30 V, MP1584 buck to 3.3 V |
| Temperature | DS18B20 on 1-Wire — **also the device's identity** |
| Board | 52.0 × 36.0 mm, 2 layers |

The on-board DS18B20's 64-bit ROM code becomes the serial number, the MAC
address and the default hostname, which is what makes each unit unique.

## Fork status

OSU Open Source Lab's maintained fork of
[`lshw/prc`](https://github.com/lshw/prc) by Liu Shiwei
(刘世伟, [bjlx.org.cn](https://bjlx.org.cn/)), who designed the board. **All
credit for the design is his.** OSL runs several of these and forked to document
the hardware in English and track discrepancies.

What differs from upstream: all Chinese text translated (README, prototype
comments, `link.txt`, the BOM part-number column); English documentation added;
a BOM-versus-layout consistency check in CI.

## ⚠ Two things to know before ordering boards

1. **`control2.*` is the final layout here, but it was never exported for
   assembly.** There is no `control2_bom.csv` or `control2_xy.csv`, and the
   Gerber zips predate it. Anything sent to a fab must be re-exported from
   rev 3.
2. **R5 disagrees between the files.** It is `27k` in both BOMs and in the
   rendered schematic, but `72k` in all three layouts. R5 sets the MP1584
   under-voltage lockout, so this is the difference between the board starting
   at ~7.0 V and at ~3.6 V — i.e. whether it works at the 5 V this README used
   to advertise. **Measure a real board before any respin.**

`tools/check_bom.py` checks for exactly this class of drift and runs in CI.

## Working with the design files

Everything needed is packaged in Debian; you do **not** need to build the
author's `pcb` forks:

```bash
lepton-schematic control2.sch          # schematic (lepton-eda)
pcb-rnd          control2.pcb          # layout (pcb-rnd)
gerbv            20191223/*.gbr        # fabrication output
python3 tools/check_bom.py             # BOM vs layout consistency
```

Both files open cleanly; `pcb-rnd` emits one benign warning about Q1's rotation
reference pin.

The `.pcb` file carries an embedded `NetList()` block, which is the fastest way
to answer connectivity questions without opening a GUI:

```bash
sed -n '/^NetList/,$p' control2.pcb
```

## Revisions

| Files | Revision | Notes |
|---|---|---|
| `control.*` | rev 1 | on-board DB9, ATmega328 TQFN32 |
| `control1.*` | rev 2 | ATmega328PB TQFP32, adds L1 |
| `control2.*` | **rev 3, final here** | DB9 removed, R17 added |
| — | **V1.1, sold** | adds a PWM pad, W5500 SPI breakout, TTL serial pads. **No design files published** |

If you have V1.1 boards, the files here do not fully describe them. See
[doc/node-954-procv1.1-hardware.md](doc/node-954-procv1.1-hardware.md).

## Documentation

| | |
|---|---|
| [AGENTS.md](AGENTS.md) | Full hardware reference — pin map, connectors, power tree, identity |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Sign-off requirement, EDA file conventions, upstream sync |
| [CHANGELOG.md](CHANGELOG.md) | What changed |
| [doc/](doc/) | Vendor manuals, translated, with images mirrored locally |
| [osuosl/proc](https://github.com/osuosl/proc) | The firmware that runs on this board |

## License

LGPL-3.0, inherited from upstream. See [LICENSE](LICENSE).
