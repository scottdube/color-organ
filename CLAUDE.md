# color-organ

Replica of the **Radio Shack 28-4009 "Color Organ Kit"** (1975) that Scott built
as a kid. Three channels — bass / mid / treble — twelve lamps, four per channel,
behind a prismatic starburst lens in a portrait wood cabinet.

Read `docs/superpowers/specs/2026-09-20-color-organ-design.md` first. It is the
design of record. `docs/ORIGINAL.md` is the catalog evidence for what the
original actually was, including two candidates that were ruled out.

## State

Design approved, nothing built. **KiCad project started 2026-09-20: sheet 1 of
6 captured and ERC-clean** (0 errors). See `docs/PCB.md` for the milling design
rules, the capture traps, and what the remaining sheets are.

## The shape of the thing

Analog, no firmware, by Scott's choice. Electret mic -> preamp -> three
Sallen-Key active filters -> op-amp precision rectifiers -> selectable decay ->
analog PWM (triangle + comparators) -> one MOSFET per channel driving four
lamps. Four ICs, single 12 V rail, single-sided board for the Tormach.

**No mains inside the enclosure.** The original was a 120 VAC triac design with
a mains-referenced chassis. That was survivable when the only thing you touched
was a speaker lead; it is not, once a microphone and its cable are in the box.
12 V external brick. This is not a preference — do not reintroduce mains.

## Traps

- **The front is a starburst LENS, not a diffuser.** The X shapes in the catalog
  photo are the lens acting on each lamp. It wants point sources. An early pass
  here sized cabinet depth to SUPPRESS hot spots, which is backwards.
- **The 18 in dimension is HEIGHT.** Radio Shack listed these height-first and
  the cabinet stands portrait. Reading it as width inverts which catalog unit is
  "the wider one" and cost a whole pass down a false trail.
- **Most C7-shaped LED "retrofits" are 120 V E12 bulbs** with a rectifier and
  dropper inside. They will not light on 12 V and cannot be PWM'd. Verify the
  lamp runs on 12 V DC before buying twelve.
- **Crossover caps are socketed on purpose.** Whether the band split feels right
  is a listening judgement. Swap caps with music playing; don't recalculate.

## Critical path

**The lamps.** Nothing else in the design depends on which lamp is chosen and
nothing gets built until one is in hand. Buy two or three candidate 12 V lamps,
light them behind a prism panel sample, and look. Measure, don't model.

## Decided 2026-09-20 — the lamps are bare LEDs, not C7 retrofits

1 W emitters on 20 mm stars, 4 red / 4 green / 4 blue, run at **100 mA** (not
the rated 350 mA). **All three channels are 2S2P** -- four green or blue in
series does not fit under 12 V, and vendor Vf for red is a RANGE (2.2-2.6 V)
wide enough that a 4S red string would leave only 1.6 V across the ballast and
drift against the other eight lamps. Full table and ballast values in
`docs/LAMPS.md`. **The resistor values there are datasheet-typical and must be
re-computed against measured Vf before ordering in quantity.**

This reversed the early "LED lamps that look like C7s" choice. Three reasons,
all in `docs/TRAPS.md`: a retrofit bulb hides a driver that may refuse PWM; a
faceted bulb is a diffuse source and blurs the starburst; and the bulbs sit
behind the lens where nobody ever sees them.

## The front lens — DECIDED: OPTIX 1A20083A Prismatic

$17.98, coarse 3/16 in square pyramids, 23.75 x 47.75, 20 in stock at HD
Portsmouth as of 2026-09-20. One sheet yields ~10 fronts at 11.5 x 18.
**Settled — do not re-open it.** Micro Prism Glaze (1A90001A) and Prisma Square
(1A00702A) were compared and rejected; `docs/LENS.md` keeps the why.

**Do not fix cabinet depth yet.** Star size is set by the lamp-to-lens gap;
mount the LED plate on adjustable standoffs and find it by eye.
