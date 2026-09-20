# The lamp block — DECIDED 2026-09-20: bare LEDs

Scott chose bare high-brightness LEDs over 12 V C7 retrofits. See `TRAPS.md`
for the three findings that drove it (PWM unknowable from a listing; a faceted
bulb blurs the starburst; the bulbs are never seen anyway).

## Part

**1 W emitters on 20 mm round star MCPCBs**, 4 red / 4 green / 4 blue. The die
is about 1 mm square, which is as close to a true point source as anything
buyable — exactly what the prism panel wants. Cree XP-E2 is the known-good
part; generic "1 W star LED" 10-packs are a fraction of the price and are
fine here because we set the current ourselves.

**Do not buy 3 W.** It needs real heatsinking and we are throwing away most of
the output in a wooden box anyway.

## Operating point

Target **100 mA per LED**, not the 350 mA the part is rated for.

The original's twelve C7 bulbs put out roughly 300 lm total. Twelve 1 W LEDs at
100 mA give roughly 400 lm — already brighter than the thing we are copying,
while cutting ballast waste almost in half and removing the heatsink question
entirely (about 0.3 W per emitter; a bare 20 mm star in free air handles that).

## Strings and ballast — REVISED 2026-09-20 to uniform 2S2P

A 12 V rail is awkward: four green or blue in series does not fit (4 x 3.2 V >
12 V). The first cut kept red as a 4S string to save ballast heat. **Vendor Vf
data killed that.** Real listings quote red as **2.2-2.6 V**, not a single
number. At the top of that spread 4S is 10.4 V, leaving only 1.6 V across the
ballast — so current becomes a strong function of Vf bin and supply sag, and
the four red lamps would not match the other eight in brightness.

**All three channels are 2S2P.** Identical wiring, identical board section,
insensitive to Vf spread. It costs about 1 W more in total ballast heat than
the mixed scheme, which is not worth a brightness mismatch.

| Channel | Colour | Wavelength | Vf @100 mA (est) | Ballast, 2 off | R heat | Channel current |
|---|---|---|---|---|---|---|
| Bass | Red | 625 nm | ~2.1-2.3 V | **75 R 1 W** | 0.73 W ea | 200 mA |
| Mid | Green | 525 nm | ~3.0-3.2 V | **56 R 1 W** | 0.55 W ea | 200 mA |
| Treble | Blue | 460 nm | ~3.0-3.2 V | **56 R 1 W** | 0.55 W ea | 200 mA |

All-on worst case: **0.6 A**, about 3.7 W total in ballast.
Supply: **12 V 2 A** external brick (no mains inside the enclosure).

### These resistor values are a starting point, not a result
Vf varies by part and by bin, and the table uses vendor-range midpoints.
**Measure Vf on the actual LEDs at 100 mA and re-compute** before committing.
Buy a spread either side of each value.

### 4S red stays available as an efficiency option
If measured red Vf comes in at or below 2.2 V there is enough headroom for a
4S red string (39 R, 0.39 W, 100 mA channel). Lay the board out so red can be
strapped either way and decide after measuring — same philosophy as the
socketed crossover caps.

## Why this removes the PWM problem completely
The ballast resistor sets peak current; the PWM sets the average. There is no
driver IC anywhere in the path to argue with the gate signal. This is the whole
reason bare LEDs won — a retrofit bulb hides a driver we cannot inspect.

## Effect on the output stage
The spec's MOSFET stage said "~200 mA, no heatsink". With uniform 2S2P that is
**200 mA on every channel** — the original figure turns out to be right. An
IRLZ44N at 200 mA and 0.02 R Rds(on) dissipates under 1 mW. No change.

## Colour-to-position is a wiring decision, deferred
Electrically, all four reds are one channel, all four greens another, all four
blues the third. Where each lamp sits in the 3 x 4 grid is free — one colour per
column, or colours scattered. `ORIGINAL.md` records that the 1975 photo hints at
scattered rather than columnar, but that is unverified. Decide it with the
panel in hand.

## Open: the lamp-to-lens gap
Star size through a prismatic panel is set by how far the emitter sits behind
it. **Mount the LED plate on adjustable standoffs for the first build** and find
the gap by eye before fixing the cabinet depth. Do not derive it.
