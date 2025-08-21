# PCB-Error-Logic-Checker-Web-App

A lightweight, web‑based tool to run automated checks on PCB design files. It performs basic DRC/ERC/logic sanity checks on uploaded Gerber and netlist files, surfaces issues in a table, and lets you download a JSON report.

> **Stack**: React (Vite, TypeScript) frontend · FastAPI (Python) backend · Simple rule engine

---

## 1) Features

* Upload Gerber layers (`.gbr`, `.ger`, `.gm*`, `.gt*`, `.gb*`, `.gko`, `.drl`) and netlist files (`.net` KiCad XML, or a simple JSON netlist format) in one go
* Server parses files and runs checks:

  * **Gerber/Manufacturing**: basic syntax, unit spec, aperture table presence, end‑of‑file token, drill file sanity, min trace width & annular ring heuristics
  * **Connectivity/ERC**: nets with a single pin (dangling), power‑to‑power shorts by name heuristic (e.g., `GND` with `VCC`), duplicated reference designators, unconnected ground pour marker strings
  * **Logic/Semantic** (heuristic): conflicting net name patterns (`GND` attached to `+3V3`), reserved test pad nets missing `TP` prefix (by pattern), common naming typos (e.g., `GND1` vs `GN D`)
* Result list with severity, file, line, rule, suggestion
* Download findings as JSON

> ⚠️ **Note**: This is a starter you can extend. PCB formats are complex; for production, integrate full parsers (e.g., `pcb-tools` for Gerber/Excellon, real ERC from EDA exports).

---

## 2) Project Structure

```
pcb-checker/
  backend/
    app.py
    checks/
      __init__.py
      gerber_checks.py
      netlist_checks.py
      rules.py
    requirements.txt
  frontend/
    index.html
    package.json
    tsconfig.json
    vite.config.ts
    src/
      main.tsx
      App.tsx
      components/ErrorTable.tsx
      components/FileDrop.tsx
      services/api.ts
  sample_files/
    example_top_copper.gbr
    example_drill.drl
    example.net (KiCad XML)
    simple_netlist.json
  README.md
```

## 3-5 are coading part so i skipped

## 6) Run Instructions

### Backend

```bash
cd pcb-checker/backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd pcb-checker/frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) and upload files. The frontend posts to `http://localhost:8000/analyze`.

---

## 7) Extending the Checker (Next Steps)

* **Real parsers**: integrate `pcb-tools` (Python) for Gerber/Excellon geometry to compute true clearances, solder mask slivers, copper-to-edge distances, annular rings, etc.
* **EDA exports**: accept KiCad PCB (`.kicad_pcb`) and Schematic (`.kicad_sch`) to run robust ERC (driver/receiver types, power flags).
* **Rule config**: add `rules.yaml` so users can tune min widths, allowed layer names, drill sizes, power domains.
* **Visualization**: draw 2D previews of layers and highlight violations (use WebGL/Canvas with `traces` from backend geometry).
* **CI mode**: CLI that returns non‑zero exit code on errors to gate releases in pipelines.

---

## 8) Disclaimer

This is a minimal, educational starter. Always validate against your EDA’s built‑in DRC/ERC and your PCB fab’s design rules.




# PCB Error & Logic Checker — Web App

A lightweight, web-based tool to run automated checks on PCB design files (Gerbers, drills) and netlists. It performs basic DRC/ERC/logic sanity checks and outputs findings in a table or downloadable JSON.

## Run

### Backend
```bash
cd pcb-checker/backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd pcb-checker/frontend
npm install
npm run dev
```

Open http://localhost:5173 and upload files. The frontend posts to http://localhost:8000/analyze.

## Notes
- This is a starter; real-world PCB checks require full parsers and geometry.
- Extend rules in `backend/checks/*` and add config as needed.

