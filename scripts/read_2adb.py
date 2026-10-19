import numpy as np
from numpy import array
from numpy import nan

def read_2adb(filename):
    nan = np.nan
    with open(filename, 'r') as f:
        db = f.read()
    db = eval(db)
    return db

def query_pair(db, atom_name):
    name1 = atom_name[0] +'_' +atom_name[1]
    name2 = atom_name[1] +'_' +atom_name[0]
    pair = db.get(name1, db.get(name2, {}))
    return pair

## example ##
if __name__ == "__main__":
    filepath = '../data/processed/2adb.txt'
    #get db_2a in dictionary format
    db_2a = read_2adb(filepath)

    #get dictionary of single atom energy (unit eV)
    single_atom_en = db_2a['single_atom']
    print('single atom energy\n', single_atom_en, '\n')

    #query atom pair (data in dictionary format)
    pair = query_pair(db_2a, ['H', 'Cl'])
    print('keys of atom-pair: ', pair.keys())
    
    """
    Keys
    The two atoms are aligned along the z-axis
    and separated by distance R (one as origin).
    Energy and force are in a function of R.

    R: distance between the two atoms. (Angstrom)
    Energy: DFT energy of two atoms calculated using GPAW. (eV)
    Force: force act on each atom in cartesian coordinate. (eV/Angstrom)
    Force_z2: Force magnitude on each atom, positive for repulsion, negative for attraction. (eV/Angstrom)
    sum_atom_radius: sum of atomic radius, use for approximating equilibrium. (Angstrom)
    Potential_Energy: the DFT energy of the atom pair minus the sum of the single atom energies. (eV)
    """

    print('\nPotential Energy of H-Cl pair\n', pair['Potential_Energy'])

    
