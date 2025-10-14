__author__='rpgv'


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import argparse
import json
import pandas as pd
import re

parser = argparse.ArgumentParser(prog='AutoHaddock', 
                                 description='''Pipeline for automatic 
                                 submission of HADDOCK DNA-Protein pairs''')
parser.add_argument('creds', default='credentials_.json',type=str,help='''
                    \nPath to credentials file contains in json format your login information to access HADDOCK servers\n''')
parser.add_argument('docking_pairs', default='dna_protein.csv',type=str,help=''' 
                    \n Path to csv file that contains protein and respective dna file names \n''')
parser.add_argument('structures',default='/Structures/',type=str,help=''' 
                    \n Path to directory containing protein and dna structures \n
                    Directory must contain sub-dirs Protein/ and DNA/''')
parser.add_argument('wait', nargs="?", default=7200,type=int,help=''' 
                    \n Wait interval for each 10 submissions - to avoid queueing errors and server overload \n''')
args = parser.parse_args()

##############
# This file describes a pipeline that automates HADDOCK (docking tool) submission of 
# DNA/Proteins for COARSED GRAINED docking, optimized for bioinformatic prediction while following an ab-initio approach; 
###############

def auto_haddock(driver, protein, DNA, name="SingleCoarse"):
    #Reloading first page(firstrun only requires login)
    driver.get("https://wenmr.science.uu.nl/haddock2.4/submit/1")
    print("Waiting for first page to load...")
    time.sleep(10)
    print(f"Starting Docking - ID: {name}")
    #Defining experiment name based on an external variable c;
    
    run_name = f'{name}'
    haddock_run = driver.find_element(By.XPATH, '//*[@id="runname"]')
    haddock_run.send_keys(run_name)

    #This page is dynamic, so scrolling towards the general areas is key - defining function
    #Note: Scroll to the element imediatly above the one you aim to find
    def scroll_to(element):
        try:
            js_code = "arguments[0].scrollIntoView();" #Scroll to it
            driver.execute_script(js_code, element) #Scroll to it
        except Exception as e:
            print(f'Failed to scroll into view\n{e}')

    target = driver.find_element(By.XPATH, '//*[@id="p1_pdb_chain"]')
    scroll_to(target)
    time.sleep(5)

    #Sending complete path to file: 
    file01 = driver.find_element(By.XPATH, '//*[@id="p1_pdb_file"]')
    file01.send_keys(protein)

    #Coarse Graining Toggle Wish me luck
    cg_toggle = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="collapse1"]/div/div[4]/div[1]/div')))
    cg_toggle.click()
    time.sleep(30)

    #Moving to next section:
    target = driver.find_element(By.XPATH, '//*[@id="p2_pdb_chain"]')
    scroll_to(target)
    time.sleep(5)

    #Submitting file 2:
    file02 = driver.find_element(By.XPATH, '//*[@id="p2_pdb_file"]')
    file02.send_keys(DNA)

    #Selecting chemistry
    chemistry = driver.find_element(By.XPATH, '//*[@id="p2_moleculetype"]/option[5]')
    chemistry.click()

    #Press next 
    next = driver.find_element(By.XPATH, '//*[@id="submit"]')
    next.click()
    time.sleep(10)

    #Scroll to: 
    try:
        #target = driver.find_element(By.XPATH, '//*[@id="input-params"]/form/div[3]')
        target = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-params"]/form/div[3]')))
        scroll_to(target)
        time.sleep(5)

        #Press next: 
        next = driver.find_element(By.XPATH, '//*[@id="submit"]')
        next.click()
        time.sleep(10)

        #Defining docking parameters
        #Scroll to: 
        target = driver.find_element(By.XPATH, '//*[@id="collapse1"]/div/div[1]/div/div[1]')
        scroll_to(target)
        time.sleep(5)

        #Defining center of mass restraints
        cemrest = driver.find_element(By.XPATH, '//*[@id="collapse1"]/div/div[8]/div')
        cemrest.click()
        driver.execute_script("arguments[0].click();", cemrest)
        time.sleep(5)

        #Missing in this iteration - AIRS restraints set to 20%

        #Scroll to: 
        target = driver.find_element(By.XPATH, '//*[@id="collapse1"]/div/div[15]/div/div[1]')
        scroll_to(target)
        time.sleep(5)

        #Open sampling parameters
        sampling_header = driver.find_element(By.XPATH, '//*[@id="submitHaddock"]/div[2]/div[1]/h4/a')
        sampling_header.click()
        time.sleep(5)

        #Setting sampling parameters
        sampling_number0 = driver.find_element(By.XPATH, '//*[@id="structures_0"]')
        sampling_number0.clear()
        sampling_number0.send_keys('10000')
        time.sleep(1)

        sampling_number1 = driver.find_element(By.XPATH, '//*[@id="structures_1"]')
        sampling_number1.clear()
        sampling_number1.send_keys('400')
        time.sleep(1)

        sampling_number2 = driver.find_element(By.XPATH, '//*[@id="waterrefine"]')
        sampling_number2.clear()
        sampling_number2.send_keys('400')
        time.sleep(1)

        #Scroll to: 
        target = driver.find_element(By.XPATH, '//*[@id="submitHaddock"]/div[15]/div[1]/h4')
        scroll_to(target)
        time.sleep(5)

        #Press next: 
        next = driver.find_element(By.XPATH, '//*[@id="submit"]')
        next.click()
        time.sleep(5)

        #Is research covid related - DEFAULT: NO
        covid = driver.find_element(By.XPATH, '//*[@id="covidConfirmNo"]')
        covid.click()
        time.sleep(10)
    except TimeoutException:
        print(f"Timeout Exception occured - possibly due to PDB formatting issues:\n{TimeoutException}")

    except NoSuchElementException:
        print(f"NoSuchElementException:\n{NoSuchElementException}")

    except Exception as e:
        print(f"An unexpected exception occurred: {e}")

def load_creds(fpath):
    with open(fpath, 'r') as op:
        data = json.load(op)
    return data['email'], data['password']

def login(driver, email_cred, pwd_cred):
    driver.get("https://wenmr.science.uu.nl/haddock2.4/submit/1")
    print("Waiting for LOGIN page to load...")
    time.sleep(10)

    print("Logging in ...")
    email = driver.find_element(By.XPATH, '//*[@id="email"]')
    pwd = driver.find_element(By.XPATH, '//*[@id="password"]')

    email.send_keys(email_cred)
    pwd.send_keys(pwd_cred)

    pwd.send_keys(Keys.RETURN)

    time.sleep(10)
    print("Logged in !")
    print("Proceed with defining the experiment...")
    return driver

if __name__ =='__main__':
    PROTEIN_DIR = f"{args.structures}/Protein" #post pdb_docking_prep dir
    DNA_DIR = f"{args.structures}/DNA" #directory containing 3D DNAs
    ##Start by defining your login for the HADDOCK platform 
    email_cred, pwd_cred = load_creds(args.creds)
    ####################
    driver = webdriver.Chrome()
    driver = login(driver, email_cred, pwd_cred)
    #File .5 - introduced due to errors on the initial run - related with element loading time
    df = pd.read_csv(args.docking_pairs) 
    # structures names, respectively
    c = 0
    for i, r in df.iterrows(): 
        pdb = r["PDB_id"]
        dna_fname = r["DNA_id"]
        protein = f'{PROTEIN_DIR}/{pdb}' #Here define path to where ALL protein structures are stored; 
        dna = f'{DNA_DIR}/{dna_fname}' #Here define path to where ALL DNA structures are stored;
        dna_fname = re.sub('\W+', '',dna_fname).replace("_","")
        print(f'Starting with {dna_fname} Run...')
        auto_haddock(driver, protein, dna, dna_fname) #Very important, apt argument will be the run name
        c += 1 
        if c % 10 == 0:
            print(f"Pause started at: {time.asctime()}") 
            time.sleep(args.wait) #Wait two hours every 10 entries: this value was obtained by trial and error, due to queuing times accumulating on server
            # A larger pause in between submissions allows for a better queuing organization from the server 
    driver.close()

