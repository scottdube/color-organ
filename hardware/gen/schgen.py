"""One-time authoring aid: emit a KiCad 10 .kicad_sch from a net description.

THROWAWAY AFTER FIRST GENERATION. Once the .kicad_sch exists, KiCad owns it and
this script must not be re-run over it -- otherwise every hand edit Scott makes
in Eeschema gets silently reverted and the project has two sources of truth.
It exists only so the first ~80-component draft does not have to be placed by
hand.

Connectivity is by LABEL, not by drawn wire: every pin gets a short stub and a
local label. That is a legitimate schematic style, it reads well for a board
that is six near-identical blocks, and it removes the whole class of bugs where
a wire endpoint misses a pin by a grid step.

Symbol definitions are lifted verbatim out of KiCad's own .kicad_sym libraries
rather than retyped, so the cached lib_symbols block cannot drift from the
real library.
"""
import re
import uuid as _uuid
from pathlib import Path

SS = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols")
NS = _uuid.UUID("c010c0a0-0000-4000-8000-000000000000")


def uid(key):
    return str(_uuid.uuid5(NS, key))


# ---------------------------------------------------------------- lib access
def _split_top(body):
    """Yield top-level (...) forms inside an s-expression body."""
    depth = 0
    start = None
    instr = False
    i = 0
    while i < len(body):
        c = body[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "(":
            if depth == 0:
                start = i
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                yield body[start:i + 1]
        i += 1


_libcache = {}


def lib_text(libname):
    if libname not in _libcache:
        _libcache[libname] = (SS / f"{libname}.kicad_sym").read_text()
    return _libcache[libname]



def _body_of(libname, name):
    txt = lib_text(libname)
    m = re.search(r'\n\t\(symbol "%s"' % re.escape(name), txt)
    if not m:
        raise KeyError(f"symbol not found: {libname}:{name}")
    start = m.start() + 1
    depth = 0
    i = start
    instr = False
    while i < len(txt):
        c = txt[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return txt[start:i + 1]
        i += 1
    raise ValueError("unterminated symbol " + name)


def resolve(lib_id):
    """Full self-contained symbol body for Lib:Name, named after Lib:Name.

    KiCad ships most parts as DERIVED symbols: TL074 is
    (symbol "TL074" (extends "LM2902") ...) with no graphics and NO PINS of its
    own. Reading it directly yields a pinless part, and the netlist then shows
    the op-amp present as a component with not one pin on any net -- which is
    exactly what happened here. Follow `extends`, take the parent's geometry,
    and rename its unit children onto the derived name.
    """
    libname, name = lib_id.split(":", 1)
    body = _body_of(libname, name)
    m = re.search(r'\(extends "([^"]+)"\)', body)
    if not m:
        return body.replace('(symbol "%s"' % name, '(symbol "%s"' % lib_id, 1)
    parent = m.group(1)
    pbody = _body_of(libname, parent)
    # keep the derived symbol's own property block, take the parent's graphics
    graphics = re.findall(
        r'\n\t\t\(symbol "%s_\d+_\d+".*?(?=\n\t\t\(symbol "|\n\t\)$)'
        % re.escape(parent), pbody, re.S)
    props = body[body.index('(property'):body.rindex(')')] \
        if '(property' in body else ''
    out = '(symbol "%s"\n\t\t%s' % (lib_id, props.rstrip())
    for g in graphics:
        out += g.replace('"%s_' % parent, '"%s_' % name)
    out += '\n\t)'
    return out


def symbol_def(lib_id):
    return resolve(lib_id)


def pins_of(lib_id, unit=1):
    """[(number, name, x, y, angle)] for ONE unit, in library coords (Y up).

    Pins live in child sub-symbols "<Name>_<unit>_<bodystyle>", never at the
    top level of a multi-unit part. Reading the whole definition at once mixes
    every section's pins together and every stub lands on a coordinate
    belonging to some other section.
    """
    body = resolve(lib_id)
    name = lib_id.split(":", 1)[1]
    blocks = re.split(r'\n\t*\(symbol "%s_(\d+)_(\d+)"' % re.escape(name), body)
    chosen = []
    for i in range(1, len(blocks), 3):
        u, _bs, chunk = int(blocks[i]), blocks[i + 1], blocks[i + 2]
        if u in (unit, 0):
            chosen.append(chunk)
    src = "".join(chosen) if chosen else body
    out = []
    for m in re.finditer(
        r'\(pin\s+\S+\s+\S+\s*\n?\s*\(at\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\)'
        r'(.*?)\(number\s+"([^"]+)"', src, re.S
    ):
        x, y, ang, mid, num = m.groups()
        nm = re.search(r'\(name\s+"([^"]+)"', mid)
        out.append((num, nm.group(1) if nm else "", float(x), float(y),
                    float(ang)))
    return out


# ---------------------------------------------------------------- emit
class Sheet:
    def __init__(self, title, comment="", company="color-organ"):
        self.title, self.comment, self.company = title, comment, company
        self.instances = []   # (ref, lib_id, x, y, rot, value, footprint, pinmap)
        self.extras = []      # raw s-expr strings

    GRID = 1.27

    @classmethod
    def snap(cls, v):
        return round(round(v / cls.GRID) * cls.GRID, 4)

    def place(self, ref, lib_id, x, y, nets, value=None, footprint="",
              rot=0, unit=1, on_board=True):
        """nets: {pin_number: net_name}. Unlisted pins are left unconnected.

        x/y are snapped to the 1.27 mm connection grid. Placing on round
        millimetres looks tidy and is wrong: a resistor at y=60 puts its pins
        at 56.19 and 63.81, neither on grid, and ERC reports every pin and
        every stub as off-grid -- 60-odd warnings from pure cosmetics.
        """
        self.instances.append(
            dict(ref=ref, lib_id=lib_id, x=self.snap(x), y=self.snap(y),
                 rot=rot, unit=unit,
                 value=value if value is not None else ref,
                 footprint=footprint, nets=nets, on_board=on_board))

    # ---- geometry
    @staticmethod
    def _world(px, py, ang, ix, iy, rot):
        """Symbol-lib pin (px,py) -> schematic world coords for instance rot."""
        import math
        r = math.radians(rot)
        cx, sy = math.cos(r), math.sin(r)
        rx = px * cx - py * sy
        ry = px * sy + py * cx
        return (ix + rx, iy - ry)          # schematic Y is down-positive

    def render(self):
        L = ['(kicad_sch', '\t(version 20260306)', '\t(generator "eeschema")',
             '\t(generator_version "10.0")',
             f'\t(uuid "{uid("sheet:" + self.title)}")', '\t(paper "A4")',
             '\t(title_block', f'\t\t(title "{self.title}")',
             f'\t\t(company "{self.company}")']
        if self.comment:
            L.append(f'\t\t(comment 1 "{self.comment}")')
        L.append('\t)')

        libs = sorted({i["lib_id"] for i in self.instances})
        L.append('\t(lib_symbols')
        for lid in libs:
            body = symbol_def(lid)
            libname, name = lid.split(":", 1)
            body = body.replace(f'(symbol "{name}"', f'(symbol "{lid}"', 1)
            L.append("\t\t" + body.replace("\n\t", "\n\t\t"))
        L.append('\t)')

        wires, labels = [], []
        for inst in self.instances:
            pm = pins_of(inst["lib_id"], inst["unit"])
            for num, _nm, px, py, ang in pm:
                net = inst["nets"].get(num)
                if not net:
                    continue
                wx, wy = self._world(px, py, ang, inst["x"], inst["y"],
                                     inst["rot"])
                # stub 2.54 mm outward along the pin's own direction
                import math
                a = math.radians(ang + inst["rot"])
                ex = round(wx + 2.54 * math.cos(a), 4)
                ey = round(wy - 2.54 * math.sin(a), 4)
                k = f'{inst["ref"]}.{num}'
                wires.append(
                    f'\t(wire\n\t\t(pts\n\t\t\t(xy {wx} {wy}) (xy {ex} {ey})\n\t\t)'
                    f'\n\t\t(stroke (width 0) (type default))'
                    f'\n\t\t(uuid "{uid("w:" + k)}")\n\t)')
                just = "left" if math.cos(a) >= 0 else "right"
                labels.append(
                    f'\t(label "{net}"\n\t\t(at {ex} {ey} 0)'
                    f'\n\t\t(effects (font (size 1.27 1.27))'
                    f' (justify {just} bottom))'
                    f'\n\t\t(uuid "{uid("l:" + k)}")\n\t)')
        L += wires + labels

        for inst in self.instances:
            r, x, y = inst["ref"], inst["x"], inst["y"]
            L += [
                '\t(symbol',
                f'\t\t(lib_id "{inst["lib_id"]}")',
                f'\t\t(at {x} {y} {inst["rot"]})',
                f'\t\t(unit {inst["unit"]})',
                '\t\t(body_style 1)',
                '\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board %s)'
                '\n\t\t(in_pos_files yes)\n\t\t(dnp no)' % ('yes' if inst['on_board'] else 'no'),
                f'\t\t(uuid "{uid("s:%s.%d" % (r, inst["unit"]))}")',
                f'\t\t(property "Reference" "{r}"\n\t\t\t(at {x} {y - 6.35} 0)'
                '\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)',
                f'\t\t(property "Value" "{inst["value"]}"'
                f'\n\t\t\t(at {x} {y + 6.35} 0)'
                '\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)',
                f'\t\t(property "Footprint" "{inst["footprint"]}"'
                f'\n\t\t\t(at {x} {y} 0)\n\t\t\t(hide yes)'
                '\n\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)',
                '\t\t(instances\n\t\t\t(project "color-organ"'
                f'\n\t\t\t\t(path "/{uid("sheet:" + self.title)}"'
                f'\n\t\t\t\t\t(reference "{r}") (unit {inst["unit"]})\n\t\t\t\t)'
                '\n\t\t\t)\n\t\t)',
                '\t)',
            ]
        L += self.extras
        L.append(')')
        return "\n".join(L) + "\n"

    def write(self, path):
        Path(path).write_text(self.render())
        return path
