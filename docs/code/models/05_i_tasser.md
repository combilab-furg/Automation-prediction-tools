<!-- ---
layout: default
title: I-Tasser
parent: Model Index
nav_order: 18
--- -->

# I-Tasser

## Overview
 
This document provides a detailed step-by-step guide to automating the process for using I-Tasser to predict protein structures via web scraping using Selenium. 
The steps include checking and updating the status, submitting variants, monitoring results, retrieving PDB files, and updating the CSV file, which ensures a streamlined and effective workflow.

## Input

- `fasta_variant.csv`: CSV file containing variant sequences and related information.

## Output

- PDB files: Predicted protein models saved in the specified path.
- `fasta_variant_2.csv`: Updated CSV file with statuses post-modeling.

## Import Libraries and Load Dependencies

We import necessary libraries for data manipulation, web scraping, file handling, and parallel processing with pandas.

```python
import time
import pandas as pd
import requests
import gzip
import os
import shutil
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

### Define Global Variables

We define paths, URLs, and login credentials required for accessing and processing data with I-Tasser.

```python
CSV_PATH = "../../data/csv/"  # Path to the CSV files
PDB_PATH = "../../data/pdb/i_tasser/"  # Path to save PDB files
FASTA_PATH = '../../data/fasta/variant'  # Path to the FASTA files
DOWNLOAD_PATH = os.path.expanduser("~/Downloads")  # Download path
I_TASSER_URL = 'https://zhanglab.comp.nus.edu.sg/I-TASSER/'  # I-TASSER URL

EMAIL = "veri.piva@furg.br"  # Email for I-TASSER login
PASSWORD = "IT_lnu1i"  # Password for I-TASSER login

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

### Load Dataset

We load the dataset containing variant sequences and related information into a DataFrame.

```python
variant_df = pd.read_csv(f'{CSV_PATH}fasta_variant.csv', sep=';')
variant_df.head()
```

### Check and Update Status

Functions to check if a PDB file exists for each variant and update the status in the DataFrame accordingly.

```python
def check_and_update_status(row):
    variant = row["variant"]
    filename = variant.replace('p.', '')
    file_path = f"{PDB_PATH}{filename}.pdb"
    
    if os.path.isfile(file_path):
        return 'concluded'

    current_status = row.get("i_tasser", "not_concluded")
    if current_status != "not_concluded":
        return current_status
    
    return "not_concluded"

def update_i_tasser_status(df):
    if 'i_tasser' not in df.columns:
        df['i_tasser'] = 'not_concluded'
    df['i_tasser'] = df.apply(check_and_update_status, axis=1)
    print("Status updated based on existing files")
    return df
```

### Submit Variants to I-Tasser

Functions to submit variants to I-Tasser using Selenium for web scraping.

```python
def get_fasta(variant):
    fasta_file = os.path.join(FASTA_PATH, f'{variant}.fasta')
    if os.path.isfile(fasta_file):
        with open(fasta_file, 'r') as file:
            fasta = file.read()
            return fasta
    else:
        print(f'File {fasta_file} does not exist.')

def submit_to_itasser(driver, fasta_content, variant):
    driver.get(I_TASSER_URL)
    wait = WebDriverWait(driver, 600)
    fasta_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/textarea')))
    fasta_input = driver.find_element(By.XPATH, '//*[@id="form1"]/textarea')
    fasta_input.send_keys(fasta_content)

    email_input = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="form1"]/p[2]/input')))
    email_input = driver.find_element(By.XPATH, '//*[@id="form1"]/p[2]/input')
    email_input.send_keys(EMAIL)
    
    id_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/p[3]/input')))
    id_input = driver.find_element(By.XPATH, '//*[@id="form1"]/p[3]/input')
    id_input.send_keys(variant)

    submit_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/p[8]/input[1]')))
    submit_button = driver.find_element(By.XPATH, '//*[@id="form1"]/p[8]/input[1]')
    submit_button.click()

    try:
        success_message = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/text()[1][contains(., "The sequence has been successfully submitted to the I-TASSER server.")]')))
        link_element = driver.find_element(By.XPATH, '/html/body/p/a')
        href_value = link_element.getAttribute('href')
        return href_value
    except:
        return "error"
```

### Wait for Results

Function to monitor and download results, ensuring the modeling process is complete.

```python
def wait_result(driver, result_url, variant):
    download_dir = os.path.expanduser("~/Downloads")
    driver.get(result_url)
    while True:
        try:
            element = WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='model1.pdb' and @download]"))
            )
            break
        except Exception as e:
            print(f"Result not ready yet. Waiting 10 seconds. {e}")
            time.sleep(10)
            
    pdb_url = element.getAttribute("href")
    driver.get(pdb_url)

    time.sleep(10)
    pdb_file = os.path.join(download_dir, "model1.pdb")
    if os.path.exists(pdb_file):
        os.makedirs(PDB_PATH, exist_ok=True)
        shutil.move(pdb_file, os.path.join(PDB_PATH, f"{variant}.pdb"))
        print(f"Moved file: {pdb_file} to {PDB_PATH}")
        return True
    else:
        print("PDB file not found in the download directory.")
        return False
```

### Retrieve and Save PDB Files

We execute the modeling process for each variant and retrieve the results.

```python
variant_df = update_i_tasser_status(variant_df)
variant_df['i_tasser'].value_counts()
variant_df["i_tasser"] = "not_concluded"
variant_df.loc[0, 'i_tasser'] = 'concluded'
variant_df.loc[1, 'i_tasser'] = 'https://zhanglab.comp.nus.edu.sg/I-TASSER/output/S44/'
driver = webdriver.Chrome(options=options)

filtered_df = variant_df[variant_df['i_tasser'] != 'concluded']

try:
    for i, (index, row) in enumerate(filtered_df.iterrows()):
        variant = row['variant']
        print(f"Processing variant {variant} ---------------- {i+1} from {len(filtered_df)}")
        if row['i_tasser'] == 'not_concluded':
            print("Model not processed yet.")
            fasta = get_fasta(variant)
            print(f"Submitting variant {variant} to I-TASSER")
            id = submit_to_itasser(driver, fasta, variant).split('/')[-2]
            result_url = f"https://zhanglab.comp.nus.edu.sg/I-TASSER/output/{id}/"
        else:
            print("Model already submitted to I-TASSER")
            result_url = row['i_tasser']
        print(f"Model processing... You can check the current status on {result_url}")
        if wait_result(driver, result_url, variant):
            print(f"Model processed successfully for variant {variant}")
            variant_df.at[index, 'i_tasser'] = f"concluded"
            filtered_df.at[index, 'i_tasser'] = f"concluded"
except Exception as e:
    print(f"Error processing variants: {e}")
finally:
    driver.quit()
```

### Update CSV File

A final step to save the updated DataFrame to a CSV file.

```python
variant_df['i_tasser'].value_counts()
variant_df.to_csv(f'{CSV_PATH}fasta_variant_2.csv', sep=';', index=False)
```