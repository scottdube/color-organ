"""Sheet 1 -- INPUT: electret preamp, master control, mid-rail, supply entry.

Values come from the design spec's component table. Two things here are NOT in
that table and are additions made during capture:

  * VMID is BUFFERED by the spare TL072 section (U3B). The spec allocated 8
    TL074 sections exactly (1 preamp + 4 filters + 3 rectifiers) and only one
    of the TL072's two sections (the triangle oscillator), leaving U3B idle.
    An unbuffered 100k/100k divider has 50k source impedance, and the master
    pot's lower end sits on it and draws signal current -- so the reference
    would move with the music. The spare section is free; use it.

  * R2/C6 form the electret's supply RC, which the spec called for in words
    ("biased 2k2 via 1k + 10uF RC") but never gave designators.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from schgen import Sheet                                        # noqa: E402

R_FP = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
C_FP = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"
CP_FP = "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"
TB2 = "TerminalBlock:TerminalBlock_MaiXu_MX126-5.0-02P_1x02_P5.00mm"
TB3 = "TerminalBlock:TerminalBlock_MaiXu_MX126-5.0-03P_1x03_P5.00mm"

s = Sheet("Color Organ - Input",
          "Electret preamp, master level, buffered mid-rail, supply entry")

# ---- supply entry -------------------------------------------------------
s.place("J2", "Connector_Generic:Conn_01x02", 30, 30,
        {"1": "+12V", "2": "GND"}, "DC IN 12V", TB2)
s.place("C4", "Device:C", 50, 35, {"1": "+12V", "2": "GND"}, "100n", C_FP)
s.place("C5", "Device:C_Polarized", 62, 35, {"1": "+12V", "2": "GND"},
        "100u/25V", CP_FP)

# ---- buffered mid-rail --------------------------------------------------
s.place("R6", "Device:R", 30, 60, {"1": "+12V", "2": "VMID_RAW"}, "100k", R_FP)
s.place("R7", "Device:R", 30, 75, {"1": "VMID_RAW", "2": "GND"}, "100k", R_FP)
s.place("C3", "Device:C_Polarized", 45, 70, {"1": "VMID_RAW", "2": "GND"},
        "10u", CP_FP)
# U3B: spare TL072 section as the mid-rail buffer (unity-gain follower)
s.place("U3", "Amplifier_Operational:TL072", 75, 65,
        {"5": "VMID_RAW", "6": "VMID", "7": "VMID"}, "TL072", "", unit=2)

# ---- electret supply RC + capsule --------------------------------------
s.place("R2", "Device:R", 30, 100, {"1": "+12V", "2": "MIC_VCC"}, "1k", R_FP)
s.place("C6", "Device:C_Polarized", 45, 105, {"1": "MIC_VCC", "2": "GND"},
        "10u", CP_FP)
s.place("R1", "Device:R", 60, 100, {"1": "MIC_VCC", "2": "MIC+"}, "2k2", R_FP)
s.place("J1", "Connector_Generic:Conn_01x02", 30, 120,
        {"1": "MIC+", "2": "GND"}, "ELECTRET", TB2)

# ---- non-inverting preamp, AC gain 101 ---------------------------------
s.place("C1", "Device:C", 85, 100, {"1": "MIC+", "2": "MIC_AC"}, "1u", C_FP)
s.place("R3", "Device:R", 100, 112, {"1": "MIC_AC", "2": "VMID"}, "100k", R_FP)
s.place("U1", "Amplifier_Operational:TL074", 125, 100,
        {"1": "PRE_OUT", "2": "FB", "3": "MIC_AC"}, "TL074", "", unit=1)
s.place("R5", "Device:R", 125, 85, {"1": "FB", "2": "PRE_OUT"}, "100k", R_FP)
s.place("R4", "Device:R", 110, 130, {"1": "FB", "2": "GAIN_LEG"}, "1k", R_FP)
s.place("C2", "Device:C_Polarized", 125, 140, {"1": "GAIN_LEG", "2": "VMID"},
        "10u", CP_FP)

# ---- master level -------------------------------------------------------
# The master control is a ROTARY pot on the REAR PANEL, not a board part. The
# board carries a 3-way terminal; RV1 is drawn so the schematic shows what is on
# the other end of those wires, and is marked off-board so it never asks for a
# footprint or lands in the placement files.
s.place("J3", "Connector_Generic:Conn_01x03", 160, 100,
        {"1": "PRE_OUT", "2": "MASTER", "3": "VMID"}, "MASTER POT", TB3)
s.place("RV1", "Device:R_Potentiometer", 190, 100,
        {"1": "PRE_OUT", "2": "MASTER", "3": "VMID"}, "10k lin", "",
        on_board=False)

# ---- ERC power sources -------------------------------------------------
# +12V and GND arrive from an external brick through J2. Nothing in the
# schematic is an *output* power pin, so ERC calls every IC supply pin
# undriven. PWR_FLAG is the standard way to tell it these rails are fed from
# off-sheet; it is a marker, not a part.
s.place("#FLG1", "power:PWR_FLAG", 45, 20, {"1": "+12V"}, "PWR_FLAG", "")
s.place("#FLG2", "power:PWR_FLAG", 62, 20, {"1": "GND"}, "PWR_FLAG", "")

# ---- TL074 #1 power pins (unit 5 is the power unit on multi-unit symbols)
s.place("U1", "Amplifier_Operational:TL074", 190, 40,
        {"4": "+12V", "11": "GND"}, "TL074", "Package_DIP:DIP-14_W7.62mm",
        unit=5)
s.place("U3", "Amplifier_Operational:TL072", 215, 40,
        {"8": "+12V", "4": "GND"}, "TL072", "Package_DIP:DIP-8_W7.62mm",
        unit=3)

out = Path(__file__).resolve().parents[2] / "kicad" / "color-organ.kicad_sch"
s.write(out)
print("wrote", out)
