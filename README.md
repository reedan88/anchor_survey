# ⚓ Anchor Triangulation Tool

Interactive Python tool for estimating seafloor anchor positions from ship survey data.

---

## Features
- Upload `.dat` station files
- Specify drop latitude/longitude
- Adjustable ship transducer depth and sound speed
- Computes estimated anchor location and fallback distance
- Displays results with an interactive Matplotlib plot

## Installation
```bash
git clone git@github.com:reedan88/anchor_survey.git
cd anchor_survey
pip install -r requirements.txt
```

## Usage
#### Launch Gui
```
panel serve gui/survey_gui.py --show
```

#### Run from Python
```
from survey.survey import calculate_anchor_position
```

#### Example data

An example ```stations.dat``` file is provided in data/.
```
from setuptools import setup, find_packages

setup(
    name="anchor-triangulation",
    version="0.1.0",
    author="Andrew Reed",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "panel>=1.4.0"
    ],
)
```
Then you can install locally for development:
```
pip install -e .
```


## Repository Organization
```
anchor_survey/
│
├── survey/       
│   ├── __init__.py
│   ├── survey.py                    
│   ├── utils.py                     
│
├── gui/
│   ├── __init__.py
│   ├── survey_gui.py                
│
├── data/
│   ├── example_stations.dat         
│
├── tests/
│   ├── __init__.py
│   ├── test_survey.py               
│
├── notebooks/
│   ├── exploration.ipynb            
│
├── requirements.txt                 
├── environment.yml                  
├── .gitignore
├── README.md
├── LICENSE                          
└── setup.py                         
```