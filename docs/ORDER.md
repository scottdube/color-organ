# Order list — first build

Prices **verified live 2026-09-20** unless marked ESTIMATE. Anything marked
ESTIMATE carries the +40% house escalator already applied.

## Buy now

| # | Item | Qty | Unit | Total | Source |
|---|---|---|---|---|---|
| 1 | OPTIX **1A20083A** Clear Acrylic Prismatic panel, 23.75 x 47.75 | 1 | $17.98 | **$17.98** | HD Portsmouth, 20 in stock, Aisle 19 |
| 2 | Cleiscry 1 W star LED, **Red 625 nm**, 20 pc, pre-wired 15 cm | 1 | $10.99 | **$10.99** | Amazon **B0H984C2BN** |
| 3 | Cleiscry 1 W star LED, **Green 525 nm**, 20 pc, pre-wired | 1 | $10.99 | **$10.99** | Amazon **B0H988PC77** |
| 4 | Cleiscry 1 W star LED, **Blue 460 nm**, 20 pc, pre-wired | 1 | $10.39 | **$10.39** | Amazon **B0H986Z3SC** |
| ~~5~~ | ~~12 V 2 A DC brick~~ | — | — | **$0 — in stock** | see below |
| ~~6~~ | ~~Ballast resistors 1 W~~ | — | — | **$0 — buildable from stock** | see below |

All three LED variants confirmed **in stock, "usually ships within 2 to 3
days"**, prices read directly off each variant page 2026-09-20.

**Total to buy: $50.35.** The supply and the ballast both came out of the
InvenTree check below, so the two ESTIMATE lines are gone and the build cost is
now entirely verified.

### Why these LEDs
Pre-mounted on a 20 mm star **and** pre-soldered with 15 cm leads — that is 24
fiddly joints on small star pads we do not have to make. 625/525/460 nm is the
right set for a colour organ. 20 pc per colour is far more than the 4 needed,
which is the point: spares, and Vf-matching within each string.

**Caveat:** the seller has no review history. Each variant's own page now reads
"In stock, usually ships within 2 to 3 days", which is better than the Oct 1-13
figure the search page showed — the search page was quoting a slower default.

**Fallback if that seller disappoints:** CHANZON 1 W chips (4.0-4.5 stars,
hundreds of reviews) plus CHANZON 25 pc 20 mm star plates, ~$8 each — but then
you solder every chip to its own star.

## Already specified, order with the board

From the design spec: 2x TL074, 1x TL072, 1x LM339, 3x IRLZ44N, electret mic
capsule, 4x 10k linear rotary pots, 1N4148s, and the **socketed** crossover
caps (22 nF, 10 nF, 100 nF, 2n2, 1 nF, 10 nF). Not priced here — these are
stock-check items first.

## InvenTree check — done 2026-09-20, both items covered

Searched the requirement, not a part number (`shop-inventory/scripts/
color_organ_stock_0920.py`). Full result set printed; nothing capped.

### Supply — on the shelf, buy nothing
| Part | Stock | Verdict |
|---|---|---|
| **PS-009 Power Adapter 12 V 1.5 A, 5.5 x 2.1 C+** — [part 1218](http://192.168.50.10:8001/web/part/1218/) | 1 | **Use this.** 1.5 A against a 0.6 A load, and the barrel is documented: 5.5 x 2.1, centre positive. |
| Power Adapter 12 V 3 A, model 1230 — [part 1102](http://192.168.50.10:8001/web/part/1102/) | 1 | Alternate. More headroom than needed; barrel not recorded. |
| S-360-12 Switching PSU 12 V 30 A enclosed — [part 1202](http://192.168.50.10:8001/web/part/1202/) | 1 | **Rejected.** Open-frame with mains terminals. Using it would put mains back in the enclosure, which this project forbids. |

### Ballast — build it from 150R, buy nothing
The catalogue is almost entirely **1/4 W**, which is not enough for a ballast
dissipating 0.55-0.73 W. But there are **81x Resistor 150R 1% 1/2W**
([part 949](http://192.168.50.10:8001/web/part/949/)), and 150R parallels
straight onto the values we want:

| Need | Build | Each part dissipates | Rating | Qty |
|---|---|---|---|---|
| Red, 75 R | **2 x 150R in parallel** = 75 R exactly | 0.37 W | 1/2 W | 4 |
| Green/Blue, ~56 R | **3 x 150R in parallel** = 50 R | 0.20 W | 1/2 W | 12 |

16 of 81 used. At 50 R instead of 56 R the green/blue strings run ~110 mA
rather than 98 mA, which is inside the target either way.

**Why this matters more than the $12 saved:** the ballast values cannot be
final until Vf is measured on the real LEDs. Having 81 x 150R on hand means
that measure-then-choose step happens at the bench with no order in between —
1, 2, 3 and 4 in parallel give 150 / 75 / 50 / 37.5 R, which brackets the whole
plausible range.

**Buy 1 W parts anyway if you want it tidy.** Three resistors per position is
free and thermally fine, but it is three resistors per position.

## Deliberately NOT on this list
- **Cabinet materials.** Depth depends on the lamp-to-lens gap, which is found
  by eye on adjustable standoffs. Buying wood now would fix a dimension we
  have not measured.
- **A second lens panel.** 1A20083A is decided; the comparison is closed.

## Direct links

- Red 625 nm 1 W — https://www.amazon.com/dp/B0H984C2BN
- Green 525 nm 1 W — https://www.amazon.com/dp/B0H988PC77
- Blue 460 nm 1 W — https://www.amazon.com/dp/B0H986Z3SC
- Lens panel 1A20083A — https://www.homedepot.com/s/prismatic%20ceiling%20light%20panel (first result; I did not capture a stable product URL, the one I guessed 404'd)

**Pick 1 W, not 3 W.** Every colour in that listing is sold in both sizes and
the swatch defaults are not consistent — check the Size selector on each page
before adding to cart. 3 W parts want real heatsinking for output we throw
away inside a wooden box.
