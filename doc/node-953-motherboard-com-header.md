# Serial Dupont Header on the Motherboard

> **English translation of** https://bjlx.org.cn/node/953
> Original title: **主板上的串口杜邦座**
> Author: 刘世伟 (Liu Shiwei) · Published Saturday, 2021-09-18 22:05
> Site: 北京龙芯＆debian用户俱乐部 (Beijing Loongson & Debian User Club)
>
> Translated 2026-07-25.

This is an **image-only page** on the original site — a photo gallery node with
a title and no body text. It is linked from the
[hardware manual](node-914-hardware-manual.md) as the reference for the
motherboard's internal COM header.

---

![Motherboard internal COM header pinout](img/9pin_com.png)

The diagram is the standard internal **COM** header found on most ATX
motherboards: a 2×5 header with pin 10 keyed (absent).

| Row | Pins, left to right |
|---|---|
| Bottom (pin 1 first) | `DCD` (1), `TXD` (3), `GND` (5), `RTS` (7), `RI` (9) |
| Top | `RXD` (2), `DTR` (4), `DSR` (6), `CTS` (8), *(pin 10 keyed/absent)* |

## How this maps to PROC

PROC-V1 ships two serial lead options — an external 9-pin D-sub cable and an
internal 2×5 Dupont shell for this header. The mapping from
[../link.txt](../link.txt):

| Signal | DB9 male | DB9 female | PROC 6-pin header |
|---|---|---|---|
| GND (地) | 5 | 5 | 3 |
| TX | 2 | 3 | 4 |
| RX | 3 | 2 | 5 |
| DTR | 8 | 7 | 6 |

Remember that PROC's `HTX` / `HRX` / `RTS` lines are **RS-232 level** — this
motherboard header is also RS-232 level, so they connect directly. Do **not**
connect them to PROC's `TX_TTL` / `RX_TTL` pads. See
[../AGENTS.md](../AGENTS.md) §6.4.
