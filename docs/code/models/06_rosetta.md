<!-- ---
layout: default
title: Rosetta
parent: Model Index
nav_order: 19
--- -->
# Rosetta

## Overview

This document provides a detailed step-by-step guide for using Rosetta to predict protein structures. Initially, the approach involved web scraping using Selenium to automate the process for a set of variant sequences and manage the resultant PDB files. However, due to constraints such as FASTA sequence size limitations imposed by the Rosetta service, we will not pursue this web scraping approach. Given that, we will use the software instead of the server.

## Input

- `fasta_variant.csv`: CSV file containing variant sequences and related information.

## Output

- PDB files: Predicted protein models saved in the specified path.
- `fasta_variant_2.csv`: Updated CSV file with statuses post-modeling.

## Import Libraries and Load Dependencies

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

We define paths, URLs, and options required for accessing and processing data with Rosetta.

```python
CSV_PATH = "../../data/csv/"  # Path to the CSV files
PDB_PATH = "../../data/pdb/rosetta/"  # Path to save PDB files
FASTA_PATH = '../../data/fasta/variant'  # Path to the FASTA files
DOWNLOAD_PATH = os.path.expanduser("~/Downloads")  # Download path
ROSETTA_URL = "https://yanglab.qd.sdu.edu.cn/trRosetta/"  # Rosetta URL

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

    current_status = row.get("rosetta", "not_concluded")
    if current_status != "not_concluded":
        return current_status
    
    return "not_concluded"

def update_rosetta_status(df):
    if 'rosetta' not in df.columns:
        df['rosetta'] = 'not_concluded'
    df['rosetta'] = df.apply(check_and_update_status, axis=1)
    print("Status updated based on existing files")
    return df
```

### Submit Variants to Rosetta

Functions to submit variants to Rosetta using Selenium for web scraping.

```python
def get_fasta(variant):
    fasta_file = os.path.join(FASTA_PATH, f'{variant}.fasta')
    if os.path.isfile(fasta_file):
        with open(fasta_file, 'r') as file:
            fasta = file.read()
            return fasta
    else:
        print(f'File {fasta_file} does not exist.')

def submit_to_rosetta(driver, fasta_content, variant):
    driver.get(ROSETTA_URL)
    wait = WebDriverWait(driver, 600)

    fasta_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="PDB"]')))
    fasta_input.send_keys(fasta_content)

    infas_radio_button = driver.find_element(By.XPATH, '//*[@id="infas"]')
    infas_radio_button.click()

    msa_select = driver.find_element(By.XPATH, '//*[@id="form1"]/select')
    msa_select.click()
    msa_option = driver.find_element(By.XPATH, '//*[@id="msafas"]')
    msa_option.click()

    variant_input = driver.find_element(By.XPATH, '//*[@id="form1"]/input[3]')
    variant_input.send_keys(variant.replace("_p.", "_"))

    checkbox1 = driver.find_element(By.XPATH, '//*[@id="form1"]/p[1]/input')
    checkbox1.click()
    checkbox2 = driver.find_element(By.XPATH, '//*[@id="form1"]/p[2]/input')
    checkbox2.click()

    submit_button = driver.find_element(By.XPATH, '//*[@id="submit"]')
    submit_button.click()

    result_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'The job has been submitted successfully')]")))
    result_url = result_element.get_attribute("href")
    
    return result_url
```

### Check Submission Status

Functions to monitor and confirm the submission status of variants on Rosetta.

```python
def filter_not_concluded(df):
    return df[~df['rosetta'].str.contains("concluded") & (df['rosetta'] != "not_concluded")]

def check_submission_status(driver, url):
    driver.get(url)
    try:
        processed = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Processing complete')]"))
        )
        return True
    except Exception as e:
        print(f"Submission for URL {url} not yet processed. Error: {e}")
        return False
```

### Retrieve and Save PDB Files

We execute the modeling process for each variant and retrieve the results.

```python
variant_df = update_rosetta_status(variant_df)
variant_df['rosetta'].value_counts()

not_concluded_df = variant_df[variant_df['rosetta'] == 'not_concluded']
not_concluded_df['rosetta'].value_counts()

driver = webdriver.Chrome(options=options)

try:
    for i, (index, row) in enumerate(not_concluded_df.iterrows()):
        variant = row['variant'].replace("_p.", "_")
        print(f"Processing variant {variant} ---------------- {i+1} from {len(not_concluded_df)} not concluded")
        fasta = get_fasta(variant)
        print(f"Submitting variant {variant} to Rosetta")
        url = submit_to_rosetta(driver, fasta, variant)
        variant_df.at[index, 'rosetta'] = str(url)
        print(f"URL: {url}")
except Exception as e:
    print(f"Error processing variants: {e}")
finally:
    driver.quit()

variant_df['rosetta'].value_counts()
```

### Update CSV File

A final step to save the updated DataFrame to a CSV file.

```python
for i in range(len(variant_df)):
    if variant_df['rosetta'][i] == "https://yanglab.qd.sdu.edu.cn/trRosetta":
        variant_df['rosetta'][i] = "not_concluded"

not_concluded_df = variant_df.head(1)

not_finished_df = filter_not_concluded(variant_df)

driver = webdriver.Chrome()

try:
    while len(not_finished_df) > 0:
        for index, row in not_finished_df.iterrows():
            url = row['rosetta']
            driver.get(url)
            if check_submission_status(driver, url):
                variant_df.at[index, 'rosetta'] = f"concluded_{url}"
                print(f"Submission for variant {row['variant']} concluded at {url}")
            else:
                print(f"Submission for variant {row['variant']} is still being processed")

        not_finished_df = filter_not_concluded(variant_df)

except Exception as e:
    print(f"Error checking submission status: {e}")

finally:
    driver.quit()

variant_df.to_csv(f'{CSV_PATH}fasta_variant_2.csv', sep=';', index=False)
```