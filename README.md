# Anchor Survey

Interactive Python tool for estimating seafloor anchor positions from ship survey data using acoustic triangulation.

---

## Features

- **Interactive GUI**: Panel-based web interface for easy data input and visualization
- **Robust Algorithms**: Iterative least-squares solver (Gauss-Newton method) for anchor triangulation
- **Coordinate Conversion**: DMS to decimal degrees, lat/lon to local x,y (meters)
- **Error Reporting**: RMS error calculation and fallback distance metrics
- **Input Validation**: Validates station geometry and depth differences
- **CI/CD**: Pytest suite with GitHub Actions

---

## Installation

### From PyPI

```bash
pip install anchor-survey
```

### From source

```bash
git clone https://github.com/reedan88/anchor_survey.git
cd anchor_survey
pip install -e .
```

### Conda environment (includes dev tools)

```bash
git clone https://github.com/reedan88/anchor_survey.git
cd anchor_survey
conda env create -f environment.yml
conda activate anchor_survey
```

---

## Quick Start

### Launch the GUI

```bash
panel serve gui/survey_gui.py --show
```

The GUI will open at http://localhost:5006.

### Use the Python API

```python
from survey import calculate_anchor_position
import numpy as np

x = np.array([0.0, 100.0, 0.0])
y = np.array([0.0, 0.0, 100.0])
d = np.array([70.71, 70.71, 70.71])  # distances to anchor in meters

anchor_x, anchor_y, iterations = calculate_anchor_position(x, y, d)
print(f"Anchor position: ({anchor_x:.2f}, {anchor_y:.2f}) m")
```

---

## Package Structure

```
anchor_survey/
├── survey/              # Core computation module
│   ├── __init__.py
│   └── survey.py        # Algorithms (DMS conversion, triangulation)
├── gui/                 # Interactive web interface
│   ├── __init__.py
│   └── survey_gui.py    # Panel-based GUI
├── data/                # Example data files
│   ├── example_data.dat
│   └── drop_points.dat
├── tests/
│   └── test_survey.py
├── environment.yml      # Conda environment definition
├── pyproject.toml
└── Makefile
```

---

## Usage

### GUI Workflow

1. Upload a `.dat` file with station measurements
2. Enter drop point coordinates (DMS format)
3. Set transducer depth, drop depth, and sound speed
4. Click **Run Triangulation** to calculate anchor position
5. View results with visualization

### Data Format

**Station file** (whitespace-delimited):

```
LAT_DEG  LAT_MIN  LON_DEG  LON_MIN  ACOUSTIC_TIME_SEC
35       56.962   75       7.548    0.672
35       56.872   75       8.150    0.775
```

**Drop points file:**

```
LAT_DEG  LAT_MIN  LAT_DIR  LON_DEG  LON_MIN  LON_DIR  DEPTH_M
35       57.068   N        75       7.822    W        36
```

---

## API Reference

| Function | Description |
|----------|-------------|
| `dms_to_dd(degrees, minutes, seconds, direction)` | Convert DMS to decimal degrees |
| `latlon_to_xy(lat, lon, ref_lat, ref_lon)` | Convert lat/lon to local x,y (meters) |
| `xy_to_latlon(x, y, ref_lat, ref_lon)` | Convert local x,y back to lat/lon |
| `calculate_anchor_position(x, y, d)` | Triangulate anchor position |
| `rms_error(anchor_pos, x, y, dist)` | Calculate RMS error |
| `calculate_fallback(anchor_x, anchor_y, drop_x, drop_y)` | Calculate fallback distance |
| `validate_survey_input(x, y, d)` | Validate input data |

---

## Development

```bash
# Run tests
make test
# or: pytest -v

# Run linting
make lint
# or: flake8 survey gui tests

# Clean build artifacts
make clean
```

---

## License

BSD-3-Clause — see [LICENSE](LICENSE) for details.

---

## Citation

If you use this tool in a publication, please cite:

> Reed, A. (2025). Anchor Survey: Python Implementation of Acoustic Survey Positioning. GitHub Repository. https://github.com/reedan88/anchor_survey
