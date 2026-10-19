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
from read_2adb import read_2adb, query_pair

# Query potential for a specific atom pair
filepath = '../data/processed/2adb.txt'
db_2a = read_2adb(filepath)

#query atom pair (data in dictionary format)
pair = query_pair(db_2a, ['H', 'Cl'])

print(pair['Potential_Energy'])
print(pair['R'])
```

```text
[26.7461658  19.18081271 13.23433254  8.59388047  5.00481518  2.25814492
  0.17989982 -1.36849266 -2.502179   -3.31444436 -3.8749929  -4.241962
 -4.47107934 -4.57276272 -4.58586115 -4.53247163 -4.42562254 -4.28070307
 -4.10799901 -3.91693485 -3.7130928  -3.49972448 -3.2838537  -3.06451245
 -2.84530691 -2.6299401  -2.41951823 -2.21547489 -2.02856186 -1.83666882
 -1.65225536 -1.47556777 -1.30823675 -1.16287346 -1.03684506 -0.92773172
 -0.83273662 -0.7504083  -0.67877471 -0.61390754 -0.55793382 -0.50755943
 -0.4637063  -0.4239449  -0.39895872 -0.3681412  -0.34022446 -0.31333075
         nan         nan         nan         nan -0.21560105 -0.20060107
 -0.18774527         nan -0.16591883         nan         nan         nan
 -0.14154846         nan         nan]
[0.625 0.675 0.725 0.775 0.825 0.875 0.925 0.975 1.025 1.075 1.125 1.175
 1.225 1.275 1.325 1.375 1.425 1.475 1.525 1.575 1.625 1.675 1.725 1.775
 1.825 1.875 1.925 1.975 2.025 2.075 2.125 2.175 2.225 2.275 2.325 2.375
 2.425 2.475 2.525 2.575 2.625 2.675 2.725 2.775 2.825 2.875 2.925 2.975
 3.025 3.075 3.125 3.175 3.225 3.275 3.325 3.375 3.425 3.475 3.525 3.575
 3.625 3.675 3.725]
```

---
