# The board

KiCad 10.0.3. Project at `kicad/color-organ.kicad_pro`. Single-sided, copper on
**B.Cu**, milled on the Tormach 1100MX through the `pcbmill` pipeline.

## Design rules and why they differ from deskhack

deskhack (the last milled board here) runs `min_clearance` and
`min_track_width` at **0.4 mm**. This board uses **0.8 mm** for both, plus
0.8 mm copper-edge clearance and a 0.8 mm minimum hole.

The reason is the isolation pass. `pcb2gcode` clears a channel about 0.030 in
(0.76 mm) wide; where two nets sit closer than that, the tool cannot clear the
whole gap and leaves a floating sliver of copper between them. deskhack lived
with 0.4 mm because an ESP32 module forced the pitch, and handled the slivers
with pour-exclusion rule areas. **This board has no such constraint** -- DIP
ICs and axial passives on a board with room to spare -- so setting the DRC
minimum at the isolation width means no sliver can form in the first place.

Wide tracks are free on a milled board: only the boundary is cut, so a 2 mm
track costs exactly the same machining as a 0.8 mm one and gives more copper.
Track width menu is 1 / 2 / 3 mm.

Everything else in `tormach-pcb-milling` still applies and is not repeated
here: G54 Z0 on the backer, tool numbers >= 600, fixed frame (zero-start is
forbidden), drilled test points rather than flat pads, a process test coupon,
and `F.Silkscreen` carrying everything that gets lasered.

## Schematic capture

`hardware/gen/` holds a one-time authoring aid that emits the `.kicad_sch` from
a net description. **It is throwaway.** Once the schematic exists KiCad owns
it; re-running the generator over a hand-edited schematic would silently revert
the edits and give the project two sources of truth.

Connectivity is by **label**, not drawn wire -- each pin gets a stub and a
local label. For a board that is six near-identical blocks this reads well and
removes the class of bug where a wire endpoint misses a pin by a grid step.

### Traps found during capture

**Most KiCad symbols are DERIVED and have no pins of their own.** `TL074` is
`(symbol "TL074" (extends "LM2902") ...)` -- properties only, no geometry, no
pins. Reading it directly produces a pinless part, and the netlist then lists
the op-amp as a present component with **not one pin on any net**. It does not
error; it just quietly wires nothing. Follow `extends` and take the parent's
geometry. Same for TL072, LM339 and IRLZ44N.

**Pins live in per-unit child symbols**, `<Name>_<unit>_<bodystyle>`, never at
the top level of a multi-unit part. Collecting pins from the whole definition
mixes all four op-amp sections together and every stub lands on a coordinate
belonging to a different section.

**Each unit of a multi-unit part needs its own UUID.** Two `(symbol ...)`
entries sharing a UUID read as one symbol annotated twice; KiCad reports
"annotation errors" and drops one, so the power pins vanish from the netlist.

**Snap placements to the 1.27 mm connection grid.** Placing on round
millimetres looks tidy and is wrong: a resistor at y=60 puts its pins at 56.19
and 63.81, and ERC flags every pin and every stub. That alone was 60-odd
warnings.

## State -- sheet 1 of 6 captured

**Input sheet done and verified:** electret supply RC, preamp at AC gain 101,
master level, buffered mid-rail, supply entry. Netlist exported and read back
pin by pin; every node is on its intended net.

**ERC: 0 errors, 8 warnings**, all accounted for:
- 4 x `missing_unit` / `missing_input_pin` -- TL074 sections B/C/D and TL072
  section A are genuinely unplaced; they are the filters and the triangle
  oscillator, on sheets not yet captured. Self-resolving.
- 4 x `lib_symbol_mismatch` -- the cached symbol differs from the library copy
  because the generator reconstructs derived symbols from their parent. Benign;
  clears on the first Tools > Update Symbols from Library.

### Design addition made during capture
**VMID is buffered by the spare TL072 section (U3B).** The spec allocated all
eight TL074 sections and only one of the TL072's two, leaving one idle. An
unbuffered 100k/100k divider has 50k source impedance and the master pot's
lower end sits on it, so the reference would move with the music. The spare
section is free.

### Remaining sheets
2 bass/mid/treble filters, 3 rectifiers + decay, 4 triangle + PWM,
5 MOSFET outputs + lamp terminals, 6 front-panel wiring.
