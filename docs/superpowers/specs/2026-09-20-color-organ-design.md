# Color organ replica — design

Replica of **Radio Shack 28-4009 "Color Organ Kit"** (1975 catalog p.103,
$24.95 — about $155 in 2026 dollars). Identification evidence and the
ruled-out candidates are in `docs/ORIGINAL.md`; this file is the design.

## What it is

A three-channel color organ. Sound is split into bass, mid and treble bands;
each band's loudness drives four lamps behind a prismatic starburst lens.
Twelve lamps total, in a portrait wood cabinet.

## Deliberate departures from the original

| Original | Replica | Why |
|---|---|---|
| 120 VAC triacs, mains-referenced chassis | 12 V DC external brick, no mains inside the box | A microphone is something a person stands near and a cable someone grabs. Mains-referenced logic plus a mic is the one genuinely dangerous combination here. Removing mains removes the hazard outright instead of managing it with opto-isolation. |
| Hardwired to speaker terminals (1/4 W min, 80 W max) | Electret microphone | Scott's requested addition. Also decouples the unit from any particular stereo. |
| Incandescent lamps (thermal lag gives the swell) | LED lamps + selectable electronic decay | LEDs respond instantly, which reads as strobing. The decay network puts the swell back. |

Faithfully kept: three channels, twelve lamps, four per channel, prismatic
starburst front, per-channel intensity controls plus a master, portrait
wood-grained cabinet at roughly 11-1/2 W x 18 H x 5 D.

## Signal chain

```
electret -> preamp -> master -> +-> LP 250 Hz      -> pot -> rect -> [decay] -> cmp -> Q1 -> 4 lamps
                                +-> HP 250 / LP 2.5k -> pot -> rect -> [decay] -> cmp -> Q2 -> 4 lamps
                                +-> HP 2.5 kHz     -> pot -> rect -> [decay] -> cmp -> Q3 -> 4 lamps
                                                                                  ^
                                                                    triangle osc ~1 kHz
```

Single 12 V rail, everything referenced to a 6 V mid-rail.

### Component values

| Block | Topology | Values | Actual |
|---|---|---|---|
| Mic preamp | non-inverting, gain 101 | 1k / 100k, 1 uF in; electret biased 2k2 via 1k + 10 uF RC | — |
| Master | rotary pot | 10k lin | — |
| Bass LP | Sallen-Key lowpass | R 43k x2, **C1 22 nF, C2 10 nF** | 250 Hz, Q 0.74 |
| Mid HP | Sallen-Key highpass | **C 100 nF x2**, R1 4k7, R2 9k1 | 243 Hz, Q 0.70 |
| Mid LP | Sallen-Key lowpass | R 43k x2, **C1 2n2, C2 1 nF** | 2.50 kHz, Q 0.74 |
| Treble HP | Sallen-Key highpass | **C 10 nF x2**, R1 4k7, R2 9k1 | 2.43 kHz, Q 0.70 |
| Brilliance x3 | rotary pot | 10k lin, filter out -> rectifier in | — |
| Rectifier x3 | op-amp precision half-wave | 1N4148, 100 R series | — |
| Decay | jumpers | 0.1 uF fixed (~10 ms); +1 uF (~110 ms); +4u7 (~480 ms); across 100k | — |
| Triangle | relaxation oscillator | ~1 kHz, window trimmed to envelope range | — |
| PWM x3 | LM339 + 2k2 pull-up | — | — |
| Output x3 | N-channel MOSFET | IRLZ44N or equiv, ~300 mA worst case, no heatsink | — |

**The bold capacitors go in sockets.** They alone set the crossovers, and
whether the split feels right is a listening judgement that cannot be made on
paper. Swapping a socketed cap with music playing takes seconds.

Values repeat on purpose (43k, 4k7/9k1 appear twice each) to cut the number of
distinct parts to stock.

**Four ICs:** 2x TL074 (8 sections exactly: 1 preamp + 4 filters + 3
rectifiers), 1x TL072 (triangle), 1x LM339 (PWM). Single-sided, millable on the
Tormach per the pcb-design constraints — no vias, jumpers where traces cross.

### Why analog PWM rather than driving the MOSFETs linearly

Driving a MOSFET gate straight from the envelope voltage gives a very sharp
knee with LEDs — nearly off to nearly full over about half a volt of gate. PWM
dims smoothly across the whole range, runs the FETs cold, and works with
whatever lamp is finally chosen rather than only with lamps whose current
limiting we control. It costs one op-amp package and stays firmware-free.

### Ruled out: MSGEQ7

The obvious modern shortcut — seven bands of pre-filtered, peak-detected output
from a single chip. Its output is a multiplexed serial stream that only a
microcontroller can read, so it cannot exist in a no-firmware design. Recorded
so it is not re-proposed.

### Ruled out: the Instructables "Color Organ Triple Deluxe" circuit

The project that started this. Passive RC filters with no gain stage feeding
bare transistors, driving six small LEDs at 9 V. Its own comment section is
full of builders reporting all channels lit at once or channels that never
light — the predictable result of passive filters and 0.6 V of diode drop with
no gain to spend. Useful as a reference for the *idea*, not the circuit.

## Front panel

The starburst X shapes in the catalog photo are the lens acting on each lamp.
The original deliberately turned each bulb into a star, so the front is a
**prismatic / lenticular panel, not a flat diffuser**, and the lamps should be
point sources. An earlier pass in this project assumed a fluorescent-style
diffuser and sized cabinet depth to suppress hot spots — the opposite of what
this design wants.

Colours appear distributed across the 3 x 4 grid rather than grouped one colour
per column, so each channel's four lamps are probably scattered over the panel.
Read off a small catalog scan; confirm before committing wiring.

## Open items

1. **Lamps — the critical path.** Nothing else depends on which lamp is chosen,
   and nothing gets built until one is. Most C7-shaped LED retrofits are E12
   bulbs with a rectifier and dropper inside for 120 V strings; those will not
   light on 12 V and cannot be PWM'd. Resolution is a bench test, not a search:
   buy two or three candidate 12 V lamps, light them behind a prism panel
   sample, and look.
2. **Cabinet.** Construction method deferred by Scott until the original's
   proportions are settled. Target is roughly 11-1/2 W x 18 H x 5 D, portrait.
3. **Triangle window.** Must sit exactly on the envelope's silence-to-peak
   range or every control has dead travel at one end. Gets a trimmer and goes
   on the Rigol. Not solvable on paper.

## Cost

**[ESTIMATE — no price verified live, +40% applied per house rule]**
About **$240** buying everything, or about **$180** if the bench already covers
passives, ICs, sockets, hardware and the board blank. The lamps (~$50) and the
prism panel (~$42) carry most of the uncertainty and are the two least
verified lines.
