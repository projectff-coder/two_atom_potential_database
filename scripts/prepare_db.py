from mendeleev import element
import os
import pandas as pd
import numpy as np

from ase import Atoms
from gpaw import GPAW, PW, Mixer
##import matplotlib.pyplot as plt
import time
import shutil

def get_single_atom_data(filename):
    single_atom_data = pd.read_csv(filename)

    radius = []
    for name in single_atom_data['name']:
        rd = element(name).atomic_radius
        if rd is None:
            rd = 100.0
        rd = rd*10**(-2) #to angstrom
        radius.append(rd)
        
    single_atom_data['atomic_radius'] = radius
    #print(single_atom_data)

    return single_atom_data

class prepare_inter_atom:
    def prepare_single_atom(self):
        filename = FILE_AVAI_ATOM
        self.single_atom_data = get_single_atom_data(filename)

        print(self.single_atom_data)

    def construct_pair_name(self):
        num =  len(self.single_atom_data)
        count = 0
        self.pair_data ={}
        for l in range(num):
            for k in range(num):
                if (k >= l):
                    count = count +1
                    pairname = self.single_atom_data.loc[l, 'name'] +'_' +self.single_atom_data.loc[k, 'name']
                    bondlength_approx = round(self.single_atom_data.loc[l, 'atomic_radius'] +self.single_atom_data.loc[k, 'atomic_radius'], 4)
                    #print(count, pairname, f'{bondlength_approx:0.4f}')

                    self.pair_data[pairname] = {'R':[], 'Energy':[], 'Force':[], 'Force_z2':[], 'sum_atom_radius':bondlength_approx}

    def construct_pair_distance(self, alpha1=0.5, alpha2=0.5, dR=0.02):
        names = list(self.pair_data.keys())
        numr = []
        for name in names:
            r0 = self.pair_data[name]['sum_atom_radius']
            rmin = round(r0 - alpha1*r0, 4)
            rmax = round(r0 + alpha2*r0, 4)

            R = np.arange(rmin, rmax, dR)
            self.pair_data[name]['R'] = R


def cal_energy_gpaw(material, params):
    material.calc = GPAW(**params)
    en = material.get_potential_energy()
    f = material.get_forces()
    fz2 = f[1,2] #force direction in z axis act on atom2
    return en, f, fz2
    
class twobody_interaction_potential(prepare_inter_atom):
    def __init__(self):
        self.prepare_single_atom()
        self.construct_pair_name()
        self.construct_pair_distance(alpha1=0.5, alpha2=2.0, dR=0.05)
        
        params ={'xc':'PBE',
                 'mode':'lcao',
                 'basis':'dzp',
                 'hund':True,
                 'occupations':{'name': 'fermi-dirac', 'width': 0.0},
        }
        self.cal_loop(params)

    def cal_loop(self, params, vacuum_val = 4.0):
        names = list(self.pair_data.keys())
        Num = len(names)
        Ncut = 2 #for testing
        
        count = 0
        for l in range(Num):
            pair_name = names[l].replace('_', '')
            R = self.pair_data[names[l]]['R']
            E = []
            F = []
            Fz2 = []

            t_i = time.time()
            for r0 in R:
                outfilename = str(l).zfill(4) +'_' +names[l] +'_' +((f'{r0:0.4f}').replace('.', 'd')).zfill(7)  +'.txt'
                #outfilename = GPAW_OUT_DIR +outfilename
                params['txt'] = outfilename
                
                material = Atoms(pair_name, [(0, 0, 0), (0, 0, r0)])
                material.center(vacuum=vacuum_val)
                try:
                    value = cal_energy_gpaw(material, params)
                    #value = [0, 0, 0]
                except:
                    value = [np.nan, np.nan, np.nan]

                E.append(value[0])
                F.append(value[1])
                Fz2.append(value[2])
                shutil.move(WORK_DIR+outfilename, GPAW_OUT_DIR+outfilename)
                

            t_f = time.time()
            self.pair_data[names[l]]['Energy']=E
            self.pair_data[names[l]]['Force']=F
            self.pair_data[names[l]]['Force_z2']=Fz2
            
            tmp_pair_data = f"\'{names[l]}\':"+ str(self.pair_data[names[l]])+',\n'
            with open(POTENTIAL_OUT_DIR +'tmp_pair_data.txt', 'a') as f:
                f.write(tmp_pair_data)

            text_log = f'{l} {names[l]} cal_time = {t_f-t_i:0.2f} s'
            print(text_log)
            with open(POTENTIAL_OUT_DIR+'log.txt', 'a') as f:
                f.write(text_log+'\n')

            count = count+1
            #if count == Ncut:
                #break

        #####save interacion potential
        file_output_potential = POTENTIAL_OUT_DIR +'pair_data.txt'
        with open(file_output_potential, 'w') as f:
            f.write(str(self.pair_data))

if __name__ == "__main__":
    WORK_DIR = os.path.dirname(os.path.abspath(__file__)) +'/'
    FILE_AVAI_ATOM = WORK_DIR + '../data/raw/available_PBE_atom.csv'
    
    ##please create result directory as show below before run this script. 
    GPAW_OUT_DIR = WORK_DIR + 'result/01_log_GPAW/'
    POTENTIAL_OUT_DIR = WORK_DIR + 'result/02_keep_potential/'

    trun1 = time.time()
    twobody_interaction_potential()
    trun2 = time.time()

    print(f'\n\nRun time = {(trun2-trun1)/3600:0.4f} h.')
