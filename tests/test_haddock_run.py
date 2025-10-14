__author__='rpgv'

from ..haddock_run import *
from selenium import webdriver
import time
import argparse
import json
import pandas as pd
import pytest




@pytest.mark.parametrize("creds", ['../templates/mycreds.json'])
@pytest.mark.parametrize("docking_pairs", ['../templates/docking_pairs.csv'])
@pytest.mark.parametrize("structures", ['../templates/Structures/'])
@pytest.mark.parametrize("wait", [70])

def test_run_haddock(creds,docking_pairs,structures,wait):
    """
    Test haddock_run pipeline
    """
    PROTEIN_DIR = f"{structures}/Protein/" #post pdb_docking_prep dir
    DNA_DIR = f"{structures}/DNA/" #directory containing 3D DNAs
    ##Start by defining your login for the HADDOCK platform 
    email_cred, pwd_cred = load_creds(creds)
    ####################
    driver = webdriver.Chrome()
    driver = login(driver, email_cred, pwd_cred)
    #File .5 - introduced due to errors on the initial run - related with element loading time
    df = pd.read_csv(docking_pairs) 
    # structures names, respectively
    c = 0
    for i, r in df.iterrows(): 
        pdb = r["PDB_id"]
        dna_fname = r["DNA_id"]
        protein = f'{PROTEIN_DIR}/{pdb}.pdb' #Here define path to where ALL protein structures are stored; 
        dna = f'{DNA_DIR}/{dna_fname}.pdb' #Here define path to where ALL DNA structures are stored;
        auto_haddock(driver, protein, dna, dna_fname) #dna_fname argument will be the name of the run
        c += 1 
        if c % 10 == 0:
            print(f"Pause started at: {time.asctime()}") 
            time.sleep(args['wait']) #Wait two hours every 10 entries: this value was obtained by trial and error, due to queuing times accumulating on server
            # A larger pause in between submissions allows for a better queuing organization from the server 
    driver.close()