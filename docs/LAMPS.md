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

## Strings and ballast

A 12 V rail is awkward: four red in series fits, four blue or green does not
(4 x 3.0 V = 12 V, no headroom). So the topology differs by colour. That is
fine — it is wiring, not complexity.

| Channel | Colour | Vf @100 mA | Topology | Ballast | R dissipation | Channel current |
|---|---|---|---|---|---|---|
| Bass | Red | ~2.0 V | **4S** | 39 R 1 W x1 | 0.39 W | 100 mA |
| Mid | Green | ~3.0 V | **2S2P** | 56 R 1 W x2 | 0.59 W ea | 200 mA |
| Treble | Blue | ~2.9 V | **2S2P** | 62 R 1 W x2 | 0.61 W ea | 200 mA |

All-on worst case: **0.5 A**, about 2.8 W total in the ballast resistors.
Supply: **12 V 2 A** external brick (no mains inside the enclosure).

### These resistor values are a starting point, not a result
Vf varies by part and by bin, and the table above uses datasheet-typical
numbers. **Measure Vf on the actual LEDs at 100 mA and re-compute** before
ordering resistors in quantity. Buy a handful either side of each value.

## Why this removes the PWM problem completely
The ballast resistor sets peak current; the PWM sets the average. There is no
driver IC anywhere in the path to argue with the gate signal. This is the whole
reason bare LEDs won — a retrofit bulb hides a driver we cannot inspect.

## Effect on the output stage
The spec's MOSFET stage said "~200 mA, no heatsink". Revised: **300 mA worst
case** on the green and blue channels. An IRLZ44N at 300 mA and 0.02 R Rds(on)
dissipates under 2 mW. No change to the part, only to the stated number.

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
