# Traps

## A "12 V" retrofit bulb may not PWM
Measured indirectly 2026-09-20 from vendor listings. The Tupolife DC 12V
colored E26 globes state **"Not-Dimmable"** right in the Amazon spec block.
A retrofit lamp's internals are unknown from the outside:

- resistor-fed LED -> PWM works perfectly
- constant-current driver IC -> may flicker, stair-step, or ignore PWM
- bridge rectifier + cap (for the AC 12 V versions) -> PWM badly smoothed

Nothing on a product page reliably says which. **The only way to know is to
buy one and put it on the Rigol.** Do not order twelve of anything before
one has been PWM'd on the bench.

## The bulbs are invisible — don't pay for bulb shape
The lamps sit BEHIND a prismatic starburst lens. The viewer never sees a bulb,
only the star it throws. The original used C7 Christmas bulbs because that was
the cheap 1975 light source, not because the shape shows. So C7/C9 form factor,
faceted finish and "nickel-plated brass base" are all cost with no visible
return — unless Scott wants to see Christmas bulbs when the case is open, which
is a legitimate reason but should be a deliberate choice, not a default.

Corollary: a **faceted or frosted** retrofit bulb is a DIFFUSE source, which
blurs the starburst. If a retrofit bulb is used anyway, prefer clear/smooth.

## 12 V colored C7 is a thin market
Searched 2026-09-20: Amazon, eBay, christmas-light-source.com, noveltylights
.com, s4lights, sival. Colored C7 LED bulbs are plentiful but almost all
**120 V**. The 12 V versions found were warm-white only (Imaginary Colours C7,
currently unavailable) or non-C7 shapes. NOT exhausted — the specialty holiday
vendors' own 12 V/RV categories were not each opened individually.
