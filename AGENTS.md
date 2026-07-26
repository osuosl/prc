# AGENTS.md — PRC / PROC-V1 PC Remote Control Card

Orientation and reference for agents (and humans) working in this repository.
Everything upstream is written in Chinese; this file is the English working
translation plus the analysis that is not written down anywhere else.

**Last verified:** 2026-07-25 against `lshw/prc` @ `5bf428b`, `lshw/proc` @ `a8f458f`,
`lshw/procV2` @ 2025-07-28, and https://bjlx.org.cn/node/914 + /node/926.

---

## 1. Read this first: the firmware is not in this repository

This repo (`lshw/prc`) is **the hardware design plus an abandoned prototype sketch.**
It has not been touched since 2020-01-31.

The sketch at [control/control.ino](control/control.ino) is a 182-line
TCP-to-serial pass-through with no menu, no authentication, no DHCP, no
configuration and no temperature support. It is *not* what ships on the boards.

The production firmware lives in a **different repository**, `lshw/proc`, which
was seeded from this very file on 2020-01-02 (the two files still differ by only
11 lines) and then developed for another five years. Verified:

- `git cat-file -t d58845a` and `4b34ae9` — the commit IDs baked into the
  released `.hex` images — **do not exist in this repository**.
- `lshw/proc` commit `fc48b63` ("init", 2020-01-02) is byte-comparable to
  [control/control.ino](control/control.ino).

> **If the task is "improve the software", the work belongs in
> [../proc](../proc/AGENTS.md), not here.**

**This file is the hardware reference.** Firmware build, EEPROM layout, menu,
scripting and the bug list live in [../proc/AGENTS.md](../proc/AGENTS.md).

---

## 2. Where this sits in the workspace

Full map: [../AGENTS.md](../AGENTS.md). The short version:

| Directory | Relevance to this repo |
|---|---|
| [../proc](../proc/AGENTS.md) | **The firmware that runs on this hardware.** Seeded from `control/control.ino` on 2020-01-02 |
| [../procV2](../procV2/AGENTS.md) | The ESP8266 successor. Different board, different firmware |
| [../jlc_gEDA_pcb](../jlc_gEDA_pcb/AGENTS.md) | Footprint library the author used for some parts of this board |
| [../pcb](../pcb/AGENTS.md), [../geda-pcb](../geda-pcb/AGENTS.md) | Forks of the layout tool that reads `control*.pcb`. Debian's `pcb-rnd` also works |
| [../ATmega328PB](../ATmega328PB/AGENTS.md) | Arduino core for the MCU on this board. **Not** used by production builds |

Author: **Liu Shiwei (刘世伟)** `<liushiwei@gmail.com>`, Beijing Loongson &
Debian User Club (北京龙芯＆debian用户俱乐部, https://bjlx.org.cn/).

Existing third-party forks of this repo: `winthundr/loongsonprc`, `WSYUTeam/prc`
— both stale (2019–2020) and contain nothing useful. Fork planning for OSU OSL
is in [../AGENTS.md](../AGENTS.md) §7.

---

## 3. This repository, file by file

| Path | What it is |
|---|---|
| [README.md](README.md) | 19-line Chinese product blurb — see §4 for translation |
| [control/control.ino](control/control.ino) | Abandoned prototype sketch (2020-01-02). Historical only |
| [control.sch](control.sch) / [control.pcb](control.pcb) | gEDA `gschem` schematic / `pcb` layout — **rev 1** (has an on-board DB9) |
| [control1.sch](control1.sch) / [control1.pcb](control1.pcb) | **rev 2** — ATmega328PB TQFP32 swap, adds L1 |
| [control2.sch](control2.sch) / [control2.pcb](control2.pcb) | **rev 3, the final layout** in this repo. DB9 removed, R17 added |
| [control_bom.csv](control_bom.csv), [control1_bom.csv](control1_bom.csv) | JLCPCB assembly BOM (`编号` column = JLCPCB part number, e.g. `C38896`) |
| [control_xy.csv](control_xy.csv), [control1_xy.csv](control1_xy.csv) | JLCPCB pick-and-place centroid files |
| [20191222.zip](20191222.zip), [20191223.zip](20191223.zip) | Gerber + drill sets sent to fab |
| [control.pdf](control.pdf), [control.png](control.png) | Rendered schematic + PCB (the PNG is the best single overview) |
| [com.pdf](com.pdf), [w5500.pdf](w5500.pdf) | Footprint/mechanical drawings (image-only, no text layer) |
| [link.txt](link.txt) | Serial cable pin mapping — see §6.4 |
| [update.sh](update.sh) | One-line `avrdude` invocation. Superseded by the version in `lshw/proc` |
| [LICENSE](LICENSE) | LGPL-3.0 |

**Note:** there is no `control2_bom.csv` / `control2_xy.csv`. The final layout was
never re-exported for assembly in this repo.

### Working with the EDA files

All of the required tools are already installed on this machine:

```bash
lepton-schematic control2.sch    # gEDA/gschem-format schematic (lepton-eda 1.9.18)
pcb-rnd          control2.pcb    # gEDA pcb-format layout   (pcb-rnd 3.1.6)
gerbv            20191223/*.gbr  # Gerber viewer
```

`geda-pcb` itself is no longer in Debian; `pcb-rnd` and `lepton-eda` are the
maintained successors and read these files. The author uses his own forks
(`lshw/pcb`, `lshw/geda-pcb`) and the `lshw/jlc_gEDA_pcb` footprint library.

The `.pcb` file carries an embedded `NetList()` block — that is the fastest way
to answer connectivity questions without opening a GUI:

```bash
sed -n '/^NetList/,$p' control2.pcb
grep -o '^Element\[[^]]*\]' control2.pcb   # refdes + footprint + value
```

---

## 4. Translations of the upstream Chinese documentation

> **Fork divergence:** in this fork the in-repo Chinese has already been
> translated in place — [README.md](README.md),
> [control/control.ino](control/control.ino), [link.txt](link.txt) and the
> `编号` column header in both BOMs are now English. Upstream is still Chinese,
> so **expect conflicts on those files when rebasing on `upstream/master`**.
> The translation is one isolated commit; `git log --oneline -- README.md
> control/control.ino link.txt` finds it if it needs to be replayed or dropped.

### 4.1 [README.md](README.md)

> **PC Remote Control Card**
>
> Uses a W5500 10M/100M network chip to expose a PC's serial port on a TCP port,
> which makes remote Linux maintenance convenient. It can also drive the reset
> and power buttons, provides one 20 A switched voltage output, and provides
> chassis temperature monitoring supporting up to 32 temperature probes.
>
> Input voltage 5–30 V.
> Serial speeds 300–921600 bps.
> Development environment: Arduino.
>
> Seven units were donated to the Debian MIPS build machine cluster; they work well.
>
> Taobao item: https://item.taobao.com/item.htm?id=611681003797
> Taobao shop: https://shop316166779.taobao.com

Two claims in this README do not match the shipping firmware: "up to 32
temperature probes" — the firmware supports **10** — and "20 A output", which is
a MOSFET/copper rating, not something the firmware knows about. See §8 issue H4.

### 4.2 Commit log, translated

Read newest-first. This is the whole history of this repo.

| Date | Commit | Chinese | English |
|---|---|---|---|
| 2020-02-01 | `5bf428b` | 成品样机完成,增加淘宝链接 | Finished prototype complete; add Taobao links |
| 2020-01-21 | `6f18abf` | firmware升级脚本 | Firmware update script |
| 2020-01-02 | `1fef6fe` | 初步的RJ45-串口透传程序 | Preliminary RJ45-to-serial pass-through program |
| 2020-01-01 | `3afd16c` | 调整pcb | Adjust PCB |
| 2020-01-01 | `0686cb0` | w5500测试 | W5500 test |
| 2019-12-30 | `9471b27` | pcb2 | PCB rev 2 |
| 2019-12-30 | `2598147` | ardino程序 | Arduino program |
| 2019-12-28 | `a3ad509` | 根据贴片进行调整 | Adjust according to (SMT) assembly |
| 2019-12-23 | `f3beeac` | 修改cpu 封装格式 | Change the CPU package format (TQFN32 → TQFP32, 328P → 328PB) |
| 2019-12-23 | `16ac95b` | fix bom xy file | — |
| 2019-12-22 | `6743553` | 最终pcb稿 20191222 | Final PCB draft 2019-12-22 |
| 2019-12-22 | `3096ff0` | w5500封装 | W5500 footprint |
| 2019-12-21 | `627081a` | 根据嘉立创的规范， 调整元件型号和方向 | Adjust part numbers and orientations to JLCPCB's rules |
| 2019-12-21 | `38e7797` | mos管背靠背，防止电源进出接反,通过寄生二极管损坏mos管 | Back-to-back MOSFETs, to stop a reversed supply from destroying them through the body diode |
| 2019-12-21 | `9065fb9` | 增加S1复位开关 | Add reset switch S1 |
| 2019-12-21 | `4044844` | Initial commit | — |

### 4.3 Hardware manual — https://bjlx.org.cn/node/914 (2020-04-25)

*Abridged. Full translation with images: [doc/node-914-hardware-manual.md](doc/node-914-hardware-manual.md).*

> **PROC-V1 Remote Controller Hardware User Manual**
>
> PROC (PC remote operation controller) can control a PC's reset button and power
> button over the network, for remote power on/off and remote restart. It can also
> enter the serial port and interact with the BIOS, bootloader and Linux console
> to complete OS installation, network configuration, fault recovery, remote
> maintenance and so on.
>
> PROC-V1 is the RJ45 version. PROC-V2 is the WiFi version. Installation of V1 follows.
>
> **Installation** (the pinout photo is an early revision; the newer PROC V1.1 no
> longer distinguishes switch polarity):
>
> Take power from the power supply's purple wire (standby 5 V) and black wire
> (ground). The purple wire supplies 5 V while the computer is off.
>
> Motherboard front-panel switches usually look like this. PROC provides two sets
> of switch leads: an ordinary 2-pin Dupont lead, and a 2×5 shell — you can pull
> the HDD-LED and power-LED wires out of their Dupont shells, fit them into the
> 2×5 shell, and plug the whole thing onto the motherboard.
>
> That completes the installation. For a router or a mini PC with a separate 12 V
> input, you have to solder your own leads.
>
> The serial port is **RS-232 level — do not connect it to a TTL-level serial
> port**. Two sets of leads are provided: an external 9-pin serial cable and an
> internal 2×5 Dupont header for the motherboard. Any other cable shape you make
> yourself.

Board-photo annotations (translated):

- 5-30V电源输入 — 5–30 V power input
- 大电流输入直接焊在这里 — solder the high-current input directly here
- 大电流输出焊点 — high-current output solder pad
- 大电流负极焊点在背面 — the high-current negative pad is on the back side
- 去主板的电源开关，分正负 — to the motherboard power switch; polarity matters
- 去主板的复位开关 分 正 负 — to the motherboard reset switch; polarity matters
- 插原来的按键开关杜邦线 — plug in the original button-switch Dupont lead
- 串口 — serial port
- 复位线和开机线连接方式，如果出现按键不可控，把极性反转一下 — how to wire the
  reset and power lines; if the buttons do not respond, reverse the polarity

Attachments on that page:

- https://bjlx.org.cn/system/files/update_0.sh — flashing script
- https://bjlx.org.cn/system/files/prc.ino__0.hex — `PROC-V1-20210201-4b34ae9` firmware
- Images: `proc_v1.1.png` (V1.1 board pinout), `9pin_com.png` (motherboard COM header),
  `proc_pcb.preview.jpeg`, `power.preview.jpeg`, `mb_switch.jpeg`, `proc_com_0.jpeg`,
  `proc_ok_0.jpeg` — all under https://bjlx.org.cn/system/files/images/

### 4.4 Software manual — https://bjlx.org.cn/node/926 (2020-04-26)

*Abridged. Full translation, annotated with every point where it no longer
matches the firmware: [../proc/doc/node-926-software-manual.md](../proc/doc/node-926-software-manual.md).*

> **PROC software instructions**
>
> Default IP is **192.168.1.2/24**. For initial setup, log in over the serial port,
> or configure your PC onto that subnet and `telnet 192.168.1.2`.
>
> There is **no password by default**. You can set one; the password only applies
> to network logins.
>
> To log in over serial: `minicom -D /dev/ttyS0 -b 115200 -R utf-8`, then type
> seven `+` and seven `U` followed by Enter. If nothing happens, PROC may be busy
> doing DHCP — wait 30 seconds and try again.
> *(See §8 issue 9 — the current firmware wants **six** of each.)*
>
> Set telnet to character mode by default; in the default line mode nothing is
> sent until you press Enter. Create `~/.telnetrc` with these three lines — no
> leading space on the first line, leading spaces on the other two:
>
> ```
> default
>   mode character
>   set binary
> ```
>
> then `telnet 192.168.1.2`. Besides telnet you can also connect with PuTTY.
>
> When logging in over serial you must first type `+++++++UUUUUUU` and Enter
> before it responds. This is to stop serial output during PC boot from
> interfering with the boot process.
>
> After login the main menu appears. It is very simple: `0` enters serial
> pass-through; `r`, `R`, `p`, `P` control the PC's power switch and reset.
> If the PWM option is fitted, `<`, `,`, `.`, `>` control the PWM output.
> There are also user scripts 1–9 (documented on a separate page), plus network
> setup, password setup, serial setup, script setup, factory reset and reboot.
>
> After setting the network to DHCP you can enable **active outbound mode** to
> work around not having a public IP or VPN. In active outbound mode you set a
> remote server (IP or hostname); PROC periodically connects to that server's
> port, and on the server you just listen with `nc` or `socat` to reach PROC's
> menu, control the machine, and log in over serial.
> *(See §8 issue 10 — this feature was **removed** from the firmware in 2024.)*
>
> **PROC script commands** — main menu `f`, then pick a script (1–9). Each script
> is at most 50 characters:
>
> | Cmd | Meaning |
> |---|---|
> | `P` | press the power switch; optional following number (1–65536) = hold in ms. Non-blocking — the next command runs immediately |
> | `p` | release the power switch |
> | `R` | press the reset switch; optional following number (1–65536) = hold in ms. Non-blocking |
> | `r` | release the reset switch |
> | `V` | turn the (5–28 V) output on |
> | `v` | turn the (5–28 V) output off |
> | `M` | followed by a number (0–255): set PWM output |
> | `T` | followed by a number (1–65536): wait this many ms. **Blocking** — the next command runs only after the delay |
>
> **Serial-console setup on the managed machine** (this is the genuinely useful part):
>
> *Redirect BIOS output to serial* — needs motherboard support, e.g.
> `Server Management → Console Redirection → Console Redirection = "Serial Port A"`.
>
> *PMON output on serial* — needs no setup; PMON supports serial directly. The
> `boot.cfg` menu is not drawn but keyboard input works. LoongArch board firmware
> outputs on serial as long as no monitor is plugged in — but release firmware
> usually lacks serial support, so use a `dbg` build.
>
> *GRUB 1* (`/boot/grub/menu.list`):
> `GRUB_CMDLINE_LINUX_DEFAULT="console=tty0 console=ttyS0,115200n8"`
>
> *GRUB 2* (`/etc/default/grub` or `/etc/default/grub.d/serial.cfg`):
> ```
> GRUB_TERMINAL="serial console"
> GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
> GRUB_CMDLINE_LINUX="console=ttyS0,115200n8 console=tty"
> ```
>
> *Kernel boot messages on serial* — add `console=ttyS0,115200n8 console=tty0`
> to the kernel command line via GRUB.
>
> *Login shell on serial* — non-systemd: add to `/etc/inittab` then `kill -1 1`:
> `T0:23:respawn:/sbin/getty -L ttyS0 115200 vt100`
> systemd: `systemctl start getty@ttyS0 && systemctl enable getty@ttyS0`

Attachments on that page:

- https://bjlx.org.cn/system/files/procv1_20200523.zip — three firmware builds:
  `prcv1.hex` (minimal), `prcv1_pwm.hex`, `prcv1_pwm_autolink.hex`
- https://bjlx.org.cn/system/files/telnetrc. — the `~/.telnetrc` above

---

## 5. Released firmware binaries (for comparison / rollback)

Version strings extracted with `strings` from the Intel-HEX images:

| File | Version string | Flash used | % of 30720 |
|---|---|---|---|
| `prcv1.hex` | `PROC-V1-20200523-d58845a` | 30452 | 99.1% |
| `prcv1_pwm.hex` | `PROC-V1-20200523-d58845a` | 30672 | 99.8% |
| `prcv1_pwm_autolink.hex` | `PROC-V1-20200523-d58845a` | 31406 | 102.2% (!) |
| `prc.ino__0.hex` | `PROC-V1-20210201-4b34ae9` | 30642 | 99.7% |
| current `lshw/proc` HEAD (`a8f458f`) | `PROC-V1-20241103-a8f458f` | **29062** | **94.6%** |

The `autolink` image exceeds the 30720 bytes left by a 2 KB bootloader, so that
2020 build must have been paired with a 512-byte bootloader (hfuse `0xDE`) rather
than the 2 KB one (`0xDA`) the current build assumes. Check the fuses on any
board before flashing an old image onto it.

Useful one-liner for pulling strings out of a `.hex`:

```bash
python3 -c "
import sys
d=bytearray();base=0
for l in open(sys.argv[1]):
    l=l.strip()
    if not l.startswith(':'): continue
    b=bytes.fromhex(l[1:]); n,a,t=b[0],(b[1]<<8)|b[2],b[3]
    if t==0:
        a+=base
        if len(d)<a+n: d.extend(b'\xff'*(a+n-len(d)))
        d[a:a+n]=b[4:4+n]
    elif t==4: base=((b[4]<<8)|b[5])<<16
sys.stdout.buffer.write(d)" prcv1.hex > prcv1.bin
strings -n 4 prcv1.bin
avr-objdump -D -m avr5 -b binary prcv1.bin | less   # binutils-avr is installed
```

---

## 6. Hardware reference

Derived from the `NetList()` block in [control2.pcb](control2.pcb) (rev 3, the
final layout here), cross-checked against [control.png](control.png) and the
V1.1 board photo at https://bjlx.org.cn/system/files/images/proc_v1.1.png.

Board size: **52.0 × 36.0 mm**, 2 layers.

### 6.1 Major parts

| Ref | Part | Role |
|---|---|---|
| U3 | **ATmega328PB**, TQFP-32 | MCU. Runs at **3.3 V / 8 MHz on the internal RC oscillator** |
| U7 | **W5500** | 10/100 Ethernet MAC+PHY with hardware TCP/IP, on SPI |
| U2 | **SP3232** (SSOP-16) | RS-232 transceiver (2× TX, 2× RX) |
| U1 | **MP1584** (SO-8) | Buck converter, VIN → 3.3 V |
| U4, U5, U10, U11 | **AO4407A** P-ch MOSFET ×4 | High-side VOUT switch, wired **source-to-source (back-to-back)** so the body diodes block reverse current in both directions |
| Q1 | **AO3400A** N-ch MOSFET | Level shifter driving the P-FET gate node |
| U8, U9 | **EL357N** optocouplers | Isolated dry-contact outputs to the PC's power / reset switch headers |
| U6 | 8 MHz crystal + C11/C12 22 pF | **Footprint present but not populated** — it is absent from both BOMs, which is why the firmware calibrates `OSCCAL` (see §7.5) |
| D3 | **DS18B20** (TO-92) | On-board 1-Wire temperature sensor — **also the device's identity** (see §6.5) |
| L1 | 10 µH, D1 SS34 | Buck inductor + catch diode |
| D2 | 20 V zener | Gate-source clamp on the P-FET bank |
| S1 | Pushbutton | MCU hardware reset |
| LED1 blue / LED2, LED3 red | | See §6.3 |

### 6.2 MCU pin map

Package pins confirmed against the netlist (GND on 3/5/21, VCC on 4/6, AVCC on 18,
crystal on 7/8 — the standard 32-pin ATmega328P/PB arrangement).

| Net | Pkg pin | Port | Arduino | Function |
|---|---|---|---|---|
| `_24V_OUT` | 1 | PD3 | **D3** | Drives Q1 → P-FET bank → VOUT. `HIGH` = output on |
| `NET_RESET` | 2 | PD4 | **D4** | W5500 `/RST` |
| `INT` | 32 | PD2 | **D2** | W5500 `/INT` — **wired but unused by the firmware** |
| `CS` | 14 | PB2 | **D10** | W5500 `SCS` |
| `MOSI` | 15 | PB3 | **D11** | SPI MOSI — also ISP |
| `MISO` | 16 | PB4 | **D12** | SPI MISO — also ISP |
| `CLK` | 17 | PB5 | **D13** | SPI SCK — also ISP — **and LED1 (blue) via R9** |
| `RX` | 30 | PD0 | **D0** | UART RX ← SP3232 R1OUT |
| `TX` | 31 | PD1 | **D1** | UART TX → SP3232 T1IN |
| `DS` | 26 | PC3 | **A3** | 1-Wire bus, R10 3.3 kΩ pull-up to 3V3 |
| `PC_RESET` | 27 | PC4 | **A4** | → R15 → opto U9 → reset header; **and LED3 (red) via R14** |
| `PC_POWER` | 28 | PC5 | **A5** | → R13 → opto U8 → power header; **and LED2 (red) via R12** |
| `RESET` | 29 | PC6 | `/RESET` | S1, R11 10 kΩ pull-up, and the CONN3 auto-reset jumper |
| — | 9 | PD5 | **D5** | **PWM output on V1.1 boards** (firmware `#define PWM 5`). Not routed on the rev-3 layout in this repo |

### 6.3 LEDs

| LED | Colour | Driven by | Meaning |
|---|---|---|---|
| LED1 | blue | `CLK` / D13 via R9 10 kΩ | Flickers with SPI traffic to the W5500 — effectively a network-activity light |
| LED2 | red | `PC_POWER` / A5 via R12 10 kΩ | Lit while the PC power button is being "pressed" |
| LED3 | red | `PC_RESET` / A4 via R14 10 kΩ | Lit while the PC reset button is being "pressed" |

### 6.4 Connectors

| Ref | Pins | Purpose |
|---|---|---|
| CONN1 | 2 | **VIN**, 5–30 V DC. Large solder pads alongside for high current |
| CONN4 | 2 | **VOUT**, switched, 5–28 V. Large solder pads; **the negative pad is on the back of the board** |
| CONN5 | 3 | External 1-Wire probes: 3V3 / DQ / GND |
| CONN3 | 2 | **"Update" jumper.** SP3232 R2OUT → C5 100 nF → MCU `/RESET`. Closed = the host's RTS/DTR can reset the MCU (needed for `avrdude -c arduino`). Leave open in normal service so the managed PC cannot reset the controller |
| CONN6 + CONN8 | 2 + 2 | **PC POWER switch**, opto U8 collector/emitter. Two headers in parallel: plain 2-pin Dupont and the 2×5 shell |
| CONN7 + CONN9 | 2 + 2 | **PC RESET switch**, opto U9. Same pairing |
| CONN10 | 6 | Serial header — see below |
| CONN2 | DB9 | **rev 1 only** — the on-board 9-pin D-sub was deleted in rev 3 |

CONN10 pinout (silkscreen on the V1.1 board reads `RTS TX_232 RX_232 GND RX_TTL TX_TTL`):

| Pin | Net | Level | Goes to |
|---|---|---|---|
| 1 | `TX` | **TTL** | MCU PD1 and SP3232 T1IN |
| 2 | `RX` | **TTL** | MCU PD0 and SP3232 R1OUT |
| 3 | `GND` | — | |
| 4 | `HRX` | **RS-232** | SP3232 R1IN — the host's TX comes in here |
| 5 | `HTX` | **RS-232** | SP3232 T1OUT — goes out to the host's RX |
| 6 | `RTS` | **RS-232** | SP3232 R2IN → R2OUT → C5 → CONN3 → MCU `/RESET` |

Cable mapping from [link.txt](link.txt) — 9-pin male / 9-pin female / the 6-pin header:

| Signal | DB9 male | DB9 female | 6-pin |
|---|---|---|---|
| GND | 5 | 5 | 3 |
| TX | 2 | 3 | 4 |
| RX | 3 | 2 | 5 |
| DTR | 8 | 7 | 6 |

The motherboard's internal 2×5 COM header (image `9pin_com.png`) is the standard
layout: bottom row pin 1 `DCD`, `TXD`, `GND`, `RTS`, `RI`; top row `RXD`, `DTR`,
`DSR`, `CTS`.

### 6.5 Power tree and the VOUT switch

```
CONN1 VIN (5-30V) ─ C1 10uF/50V ─┬─ R4 100k / R5 ── MP1584 EN   (under-voltage lockout)
                                 ├─ MP1584 (U1) ── L1 10uH ── C2 100uF ── Vcc 3.3V
                                 │     D1 SS34 catch diode
                                 │     R1 120k / R2 39k feedback:  0.8V * (1 + 120/39) = 3.26V
                                 └─ U10/U11 (P-FET, source) ══╗
                                                              ║  gates tied, R7 1M to VIN,
                                                              ║  D2 20V zener clamp,
                                                              ║  pulled down through R8 47k by Q1
                                    U4/U5 (P-FET, source) ════╝
                                            └─ CONN4 VOUT (switched)

Vcc 3.3V ─ ATmega328PB, W5500, SP3232, DS18B20
```

R17 (1 MΩ, added in rev 3) pulls the `_24V_OUT` gate net down so the output stays
off while the MCU is in reset.

> **Component-value discrepancy:** R5 (the MP1584 enable divider) is `27k` in
> [control_bom.csv](control_bom.csv), [control1_bom.csv](control1_bom.csv) and the
> rendered schematic, but `72k` in the `Element[]` line of both
> [control.pcb](control.pcb) and [control2.pcb](control2.pcb). This changes the
> input under-voltage lockout from ~7.0 V to ~3.6 V — i.e. whether the board
> actually starts at the 5 V the README claims. **Measure a real board before
> respinning.** Similarly C4 is `0.01uF` on the schematic (MP1584 bootstrap) but
> is ordered as `100nF` in both BOMs. Tracked as §8 issues H1 and H2.

### 6.6 Device identity — the DS18B20 is the serial number

This is non-obvious and matters for a fleet. On first boot the firmware:

1. Enumerates the 1-Wire bus. If exactly one probe is found, its 64-bit ROM code
   is written to EEPROM as the device **serial number** (`SN0..SN7`).
2. Builds the **MAC address** as `DC:AD:BE:<SN[5]>:<SN[6]>:<SN[7]>`.
3. Sets the default **device name** to `PROC` + the same three bytes in hex.

So the on-board DS18B20 (D3) is what makes each unit unique. Consequences:

- The `#SN:` line in the banner is the DS18B20 ROM code.
- Probe index 0 is reserved for the identity probe and is excluded from the
  temperature display.
- `DC:AD:BE` is not an IEEE-assigned OUI **and has the locally-administered bit
  clear**, so these boards claim a globally-unique OUI they do not own. Setting
  bit 1 of the first octet (e.g. `DE:AD:BE`) would be correct. Worth fixing in a fork.
- If the probe is missing or fails, see §8 issue 5 — the unit factory-resets on
  every boot.

---

## 7. Firmware — see [../proc/AGENTS.md](../proc/AGENTS.md)

The firmware reference used to live here. It now lives with the code:

| Topic | Where |
|---|---|
| Building (`arduino-cli`, FQBN, libraries, flash budget) | [../proc/AGENTS.md](../proc/AGENTS.md) §3 |
| Bootloader and fuses (why the crystal is unpopulated) | [../proc/AGENTS.md](../proc/AGENTS.md) §3 |
| Flashing with `avrdude` (and the CONN3 "Update" jumper) | [../proc/AGENTS.md](../proc/AGENTS.md) §3 and §6.4 below |
| EEPROM layout, factory defaults | [../proc/AGENTS.md](../proc/AGENTS.md) §4.2 |
| Device identity from the DS18B20 | §6.6 below, and [../proc/AGENTS.md](../proc/AGENTS.md) §4.3 |
| RC-oscillator calibration | [../proc/AGENTS.md](../proc/AGENTS.md) §4.4 |
| Menu, banner, escape sequences, script language | [../proc/AGENTS.md](../proc/AGENTS.md) §4.5–4.7 |
| **Verified bug list and improvement targets** | [../proc/AGENTS.md](../proc/AGENTS.md) §5 |

## 8. Hardware-side issues found while reading these files

Firmware bugs are in [../proc/AGENTS.md](../proc/AGENTS.md) §5. These are the
problems that live in *this* repository:

> **Tracked as GitHub issues** — <https://github.com/osuosl/prc/issues>.
> H1 → [#1](https://github.com/osuosl/prc/issues/1) ·
> H3 → [#2](https://github.com/osuosl/prc/issues/2) ·
> H5 → [#3](https://github.com/osuosl/prc/issues/3).
> H2 (C4) is folded into #1; H4 was fixed by the README rewrite.
> `tools/check_bom.py` enforces H1 and H3 in CI.

| # | Severity | Issue |
|---|---|---|
| H1 | **Check before respin** | **R5 disagrees between the BOM and the layout.** `27k` in [control_bom.csv](control_bom.csv), [control1_bom.csv](control1_bom.csv) and the rendered schematic; `72k` in the `Element[]` line of both [control.pcb](control.pcb) and [control2.pcb](control2.pcb). R5 is the MP1584 enable divider, so this moves the input under-voltage lockout between roughly 7.0 V and 3.6 V — i.e. whether the board starts at the 5 V the README claims. **Measure a real board.** |
| H2 | Low | **C4 disagrees too** — `0.01uF` on the schematic (the MP1584 bootstrap cap, where 10 nF is conventional) but ordered as `100nF` in both BOMs |
| H3 | Medium | **The final layout was never re-exported for assembly.** `control2.pcb` is rev 3, but there is no `control2_bom.csv` / `control2_xy.csv`, and the Gerber zips ([20191222.zip](20191222.zip), [20191223.zip](20191223.zip)) predate it. Anything sent to a fab must be re-exported from rev 3 |
| H4 | Low | **The README overstates the firmware.** "Up to 32 temperature probes" — the firmware supports 10. "20 A output" is a MOSFET/copper rating, not something the firmware knows about |
| H5 | Note | **This repo is rev 1.0 hardware.** The vendor sells **V1.1**, which adds a PWM pad (Arduino D5), a W5500 SPI breakout header and TTL serial pads, and — per the vendor page — no longer distinguishes switch polarity. **No V1.1 design files are published anywhere.** If OSL has V1.1 boards, the files here do not fully describe them |

## 9. Chinese → English glossary

Terms you will hit constantly in commits, comments and the vendor pages.

| Chinese | English |
|---|---|
| 远程控制卡 / 远程控制器 | remote control card / remote controller |
| 串口 | serial port |
| 透传 | pass-through (transparent forwarding) |
| 开关机 | power on/off |
| 重启 / 复位 | restart / reset |
| 电源开关 | power switch |
| 看门狗 | watchdog |
| 主动外联 | active outbound connection ("autolink" / dial-out) |
| 固件 | firmware |
| 编译 / 编译机 | compile / build machine |
| 引导程序 / 烧录引导程序 | bootloader / burn bootloader |
| 校准 | calibration |
| 晶振 | crystal oscillator |
| 温度探头 | temperature probe |
| 封装 | (component) footprint / package |
| 贴片 | SMT assembly |
| 嘉立创 | JLCPCB (the fab) |
| 杜邦线 / 杜邦座 | Dupont jumper wire / Dupont header |
| 主板 | motherboard |
| 恢复出厂设置 | restore factory defaults |
| 脚本 | script |
| 菜单 | menu |
| 密码 | password |
| 网段 | subnet |
| 寄生二极管 | (MOSFET) body diode |
| 背靠背 | back-to-back |
| 龙芯 | Loongson (the CPU vendor) |
| 淘宝 | Taobao (the shop) |

---

## 10. Conventions when working in this repo

- **Do not "fix" the hardware files casually.** `.sch` and `.pcb` are gEDA
  formats where a GUI round-trip rewrites the entire file. Edit with `pcb-rnd` /
  `lepton-schematic` and keep the diff reviewable, or don't touch them.
- **The final layout here is `control2.*`**, not `control.*`. Anything you export
  (BOM, XY, Gerbers) should come from rev 3.
- **Never regenerate the Gerber zips** unless you are actually respinning the
  board — they are the record of what was fabricated.
- **Upstream commit messages are Chinese.** In an OSL fork, write commit messages
  in English; if a patch is intended for upstream, a bilingual subject line is a
  courtesy.
- **Do not edit [control/control.ino](control/control.ino).** It is a dead
  prototype kept for history. Firmware changes go in
  [../proc](../proc/AGENTS.md), which has its own conventions.
- **The pin assignments are a hardware contract.** `_24V_OUT`=D3, `NET_RESET`=D4,
  W5500 SPI on D10–D13, `DS`=A3, `PC_RESET`=A4, `PC_POWER`=A5 (§6.2). Changing
  them here means changing the firmware too, and vice versa.

## 11. Source documents

Every vendor page has a **full English translation checked in under
[doc/](doc/)**, with the images mirrored locally. The abridged versions in §4.3
and §4.4 above are kept for reading in context; the files below are complete.

| Source | Original title | Translation |
|---|---|---|
| https://bjlx.org.cn/node/914 | PROC-V1 远程控制器硬件用户手册 | [doc/node-914-hardware-manual.md](doc/node-914-hardware-manual.md) |
| https://bjlx.org.cn/node/926 | proc软件使用说明 | [../proc/doc/node-926-software-manual.md](../proc/doc/node-926-software-manual.md) |
| https://bjlx.org.cn/node/953 | 主板上的串口杜邦座 | [doc/node-953-motherboard-com-header.md](doc/node-953-motherboard-com-header.md) |
| https://bjlx.org.cn/node/954 | procv1.1 hardware | [doc/node-954-procv1.1-hardware.md](doc/node-954-procv1.1-hardware.md) |
| https://bjlx.org.cn/node/929 | PROC-V2 用户手册 | [../procV2/doc/node-929-v2-user-manual.md](../procV2/doc/node-929-v2-user-manual.md) |

Downloadable artefacts on those pages (not mirrored — they are binaries):

| URL | What |
|---|---|
| https://bjlx.org.cn/system/files/prc.ino__0.hex | firmware `PROC-V1-20210201-4b34ae9` |
| https://bjlx.org.cn/system/files/procv1_20200523.zip | three 2020-05-23 firmware builds |
| https://bjlx.org.cn/system/files/update_0.sh | flashing script |
| https://bjlx.org.cn/system/files/telnetrc. | `~/.telnetrc` for character-mode telnet |
| https://item.taobao.com/item.htm?id=611681003797 | product listing |
