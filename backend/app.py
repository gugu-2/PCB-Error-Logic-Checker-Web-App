
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from checks.gerber_checks import run_gerber_checks
from checks.netlist_checks import run_netlist_checks

app = FastAPI(title="PCB Error & Logic Checker", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze")
async def analyze(files: List[UploadFile] = File(...)):
    gerbers, drills, netlists, others = [], [], [], []
    for f in files:
        name = (f.filename or "").lower()
        content = (await f.read()).decode(errors="ignore")
        if name.endswith((".gbr", ".ger", ".gtl", ".gbl", ".gts", ".gbs", ".gto", ".gbo", ".gko", ".gm1", ".gm2", ".gm", ".pho")):
            gerbers.append((name, content))
        elif name.endswith((".drl",)):
            drills.append((name, content))
        elif name.endswith((".net", ".xml", ".json")):
            netlists.append((name, content))
        else:
            others.append((name, content))

    findings = []
    for name, text in gerbers:
        findings.extend(run_gerber_checks(name, text))
    for name, text in drills:
        findings.extend(run_gerber_checks(name, text, is_drill=True))
    for name, text in netlists:
        findings.extend(run_netlist_checks(name, text))

    return {"files": [f for f,_ in gerbers+drills+netlists+others], "findings": findings}
