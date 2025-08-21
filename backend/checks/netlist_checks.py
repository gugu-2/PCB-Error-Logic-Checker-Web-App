
import re
import json
import xml.etree.ElementTree as ET
from .rules import make

POWER_NET_NAMES = {"gnd", "vss", "vcc", "+3v3", "+5v", "+1v8", "+12v", "vin"}


def parse_kicad_xml(text: str):
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    comps = {}
    for c in root.findall("components/comp"):
        ref = c.get("ref", "")
        value = (c.findtext("value") or "").strip()
        comps[ref] = {"value": value}
    nets = {}
    for n in root.findall("nets/net"):
        name = n.get("name", "")
        nodes = []
        for node in n.findall("node"):
            nodes.append({
                "ref": node.get("ref", ""),
                "pin": node.get("pin", ""),
            })
        nets[name] = nodes
    return comps, nets


def parse_simple_json(text: str):
    try:
        data = json.loads(text)
        return data.get("components", {}), data.get("nets", {})
    except Exception:
        return None


def classify_net(name: str):
    s = name.lower()
    for p in POWER_NET_NAMES:
        if p in s:
            return "power"
    return "signal"


def run_netlist_checks(filename: str, text: str):
    findings = []

    parsed = None
    if text.strip().startswith("<"):
        parsed = parse_kicad_xml(text)
    if parsed is None and text.strip().startswith("{"):
        parsed = parse_simple_json(text)

    if parsed is None:
        findings.append(make("warning", filename, "NET000", "Unrecognized netlist format. Provide KiCad XML (.net) or simple JSON schema.", suggestion="Export KiCad netlist or use provided JSON schema."))
        return findings

    components, nets = parsed

    # Duplicated reference designators
    seen = set()
    for ref in components.keys():
        if ref in seen:
            findings.append(make("error", filename, "NET001", f"Duplicate reference designator {ref}.", suggestion="Ensure unique refs (R1, R2, …)."))
        seen.add(ref)

    # Dangling nets (single pin)
    for name, nodes in nets.items():
        if len(nodes) <= 1:
            findings.append(make("warning", filename, "NET010", f"Net '{name}' has {len(nodes)} connection(s).", suggestion="Connect all intended pins or rename as 'NC_*'."))

    # Heuristic power short: net name mixes multiple power domains
    for name, nodes in nets.items():
        s = name.lower()
        if any(x in s for x in ["gnd"]) and any(y in s for y in ["vcc", "+3v3", "+5v", "+1v8", "+12v", "vin"]):
            findings.append(make("error", filename, "NET020", f"Net '{name}' suggests GND and VCC shorted.", suggestion="Split power nets and add proper labels."))

    # Test point naming convention
    for name, nodes in nets.items():
        if "test" in name.lower() and not name.upper().startswith("TP"):
            findings.append(make("info", filename, "NET030", f"Test net '{name}' should use 'TP*' prefix.", suggestion="Rename to TP* for fab/QA."))

    # Common typos
    for name in nets.keys():
        if re.search(r"g\s*n\s*d", name.lower()):
            findings.append(make("warning", filename, "NET040", f"Suspicious net name '{name}'. Did you mean 'GND'?", suggestion="Fix net label."))

    return findings
