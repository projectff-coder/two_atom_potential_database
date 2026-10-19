# Two-atom Interaction Potential Database from DFT Calculation

This repository contains the supplementary data and Python scripts for the research paper: 
**"Two-atom interaction potential database supporting physics-informed features for machine learning and material property prediction"**. 

If you use this data or code in your work, please cite our paper:
> **Citation:**
[Aniwat Kesorn, Cheewawut Na Talang, Asawin Sinsarp, Sujin Suwanna, Suraphong Yuma; Two-atom interaction potential database supporting physics-informed features for machine learning and material property prediction. J. Chem. Phys. 14 October 2026; 165 (14): 144119. https://doi.org/10.1063/5.0350327] 

---

## Repository Structure

```text
two_atom_potential_database/
│
├── data/
│   ├── raw/                 # Original CSV input data
│   │   └── input_data.csv   
│   └── processed/           # Generated database for queries
│       └── 2adb.txt         # Atom pair energy potential database
│
├── scripts/
│   ├── prepare_db.py        # Script to process CSV into database file (e.g., 2adb.txt)
│   └── read_2adb.py         # Script to query the 2adb.txt database
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Dataset Overview
The `2adb.txt` file acts as a database storing the energy potentials, force of atom pairs as a fuction of inter-atomic distance calculated using Density Functional Theory (DFT). The data format inside the text file is structured as a Python dictionary.

* **Calculated with:** DFT via the GPAW package, Perdew–Burke–Ernzerhof exchange–correlation functional, linear
combination of atomic orbitals (LCAO) method with a double-zeta polarized (dzp) basis set, and spin-polarized calculations.  
* **Key Contents:** single_atom, R, Energy, Force, Force_z2, sum_atom_radius, Potential_Energy

---

## Getting Started

### 1. Prerequisites
Ensure you have Python installed and required dependencies in requirements.txt.

### 2. Database Preparation (Optional)
If you want to reproduce the `2adb.txt` database from the raw CSV file,

create directory `script/result/01_log_GPAW/` and `result/02_keep_potential/`
to keep results files,

run the preparation script:
```bash
python scripts/prepare_db.py
```
*Note: This will read `data/raw/input_data.csv` and generate the two-atom potential database.*

### 3. Querying the Database
The `read_2adb.py` provide pre-defined functions alongside usage examples for data extraction.
To fetch and query energy potentials from the database, use the `read_2adb.py` script:
```bash
python scripts/read_2adb.py
```

---

## Usage Example
Inside `read_2adb.py`, you can query specific atom pairs like this:

```python
# Quick concept example
from scripts.read_2adb import read_2adb, query_pair

# Query potential for a specific atom pair
filepath = '../data/processed/2adb.txt'
db_2a = read_2adb(filepath)

#query atom pair (data in dictionary format)
pair = query_pair(db_2a, ['H', 'Cl'])

print(pair['Potential_Energy'])
print(pair['R'])
```

---
