
import re
from .rules import make

GERBER_REQUIRED_TOKENS = ["%FS", "%MOIN", "%MOMM", "%AD"]  # format, units(in or mm), apertures
END_TOKEN = "M02*"

TRACE_MIN_WIDTH_MM = 0.15  # heuristic
ANNULAR_MIN_MM = 0.20      # heuristic

DRILL_HEADER = re.compile(r"M48|;FILE_FORMAT|METRIC|INCH", re.IGNORECASE)


def run_gerber_checks(filename: str, text: str, is_drill: bool = False):
    findings = []

    if is_drill:
        if not DRILL_HEADER.search(text):
            findings.append(make("error", filename, "DRL001", "Drill file missing header/units (M48/METRIC/INCH).", suggestion="Export Excellon with units header."))
        if "T01" not in text:
            findings.append(make("warning", filename, "DRL002", "No tool definitions found (e.g., T01).", suggestion="Define drill tools."))
        if "M30" not in text and "M95" not in text:
            findings.append(make("warning", filename, "DRL003", "No program end (M30/M95).", suggestion="Ensure proper file termination."))
        return findings

    # Gerber layer
    header = text.splitlines()[:80]
    header_text = "\n".join(header)

    # must have end token
    if END_TOKEN not in text:
        findings.append(make("error", filename, "GBR001", "Missing end-of-file token 'M02*'.", suggestion="Enable 'End of File' in export."))

    # units/apertures
    if not any(tok in header_text for tok in ("%MOIN%", "%MOMM%")):
        findings.append(make("error", filename, "GBR002", "Units not specified (%MOIN% or %MOMM%).", suggestion="Include units in Gerber export."))
    if "%AD" not in header_text:
        findings.append(make("error", filename, "GBR003", "Aperture table missing (%AD).", suggestion="Do not use deprecated RS-274D; export RS-274X."))

    # basic width heuristic: look for D01 draws with likely aperture sizes smaller than min
    # this is very heuristic; real check needs geometry. We flag if we find any width like 0.08mm
    mm_widths = re.findall(r"(\d+\.?\d*)\s?mm", header_text.lower())
    for w in mm_widths:
        try:
            if float(w) < TRACE_MIN_WIDTH_MM:
                findings.append(make("warning", filename, "GBR010", f"Trace width {w}mm below recommended {TRACE_MIN_WIDTH_MM}mm.", suggestion="Increase min track width or relax fab capability."))
        except:
            pass

    # annular ring heuristic via comments like 'Via: drill 0.3mm, pad 0.5mm'
    ring = re.findall(r"drill\s*(\d+\.?\d*)mm.*pad\s*(\d+\.?\d*)mm", text.lower())
    for d, p in ring:
        try:
            ann = (float(p) - float(d)) / 2.0
            if ann < ANNULAR_MIN_MM:
                findings.append(make("warning", filename, "GBR011", f"Annular ring {ann:.2f}mm below {ANNULAR_MIN_MM}mm.", suggestion="Use larger pad or smaller drill."))
        except:
            pass

    # common layer mismatches
    if any(k in filename for k in ["gtl", "top"]):
        if "bottom" in text.lower():
            findings.append(make("warning", filename, "GBR020", "Top layer file contains 'bottom' text — possible layer mixup.", suggestion="Verify layer-to-file mapping."))

    return findings
