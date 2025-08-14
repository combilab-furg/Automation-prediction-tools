import logging
import time
import os
import pandas as pd
import numpy as np
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium WebDriver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

PDB_PATH = f"results/"
FASTA_FILE = "fastas.csv"
MODEL = 'tr_roseta'
ROSETTA_URL = "https://yanglab.qd.sdu.edu.cn/trRosetta/"

def update_fasta_dataset(df, column):
    try:
        logging.info("Updating FASTA dataset.")
        original_df = pd.read_csv(FASTA_FILE, sep=';')
        df.to_csv(FASTA_FILE, index=False, sep=';')
        for index, row in df.iterrows():
            if index in original_df.index:
                original_df.loc[index, column] = row[column]
        original_df.to_csv(FASTA_FILE, sep=';', index=False)
        logging.info("FASTA dataset updated successfully.")
    except Exception as e:
        logging.error(f"Error updating FASTA dataset: {e}")

def submit_pdb(driver, fasta, variant):
    try:
        logging.info(f"Submitting model for variant: {variant}")
        time.sleep(10)
        driver.get(ROSETTA_URL)
        wait = WebDriverWait(driver, 600)
        fasta = f">seq\n{fasta}"
        fasta_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="PDB"]')))
        fasta_input.send_keys(fasta)
        infas_radio_button = driver.find_element(By.XPATH, '//*[@id="infas"]')
        infas_radio_button.click()
        variant_input = driver.find_element(By.XPATH, '//*[@id="form1"]/input[3]')
        variant_input.send_keys(variant.replace("_p.", "_"))
        time.sleep(5)
        submit_button = driver.find_element(By.XPATH, '//*[@id="submit"]')
        submit_button.click()
        time.sleep(10)
        result_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/a")))
        result_url = result_element.get_attribute("href")
        if "output" not in result_url:
            result_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/p[1]")))
            text = result_element.text
            logging.error(f"Submission error: {text}")
            return np.nan
        logging.info(f"Model submitted successfully. Result URL: {result_url}")
        return result_url
    except Exception as e:
        logging.error(f"Error submitting model for variant {variant}: {e}")
        return np.nan


def download_pdb(driver, url, protein_id):
    try:
        logging.info(f"Downloading PDB for protein ID: {protein_id}")
        time.sleep(3)
        driver.get(url)
        result_element = driver.find_element(By.XPATH, "//a[contains(@href, 'model1.pdb')]")
        result_url = result_element.get_attribute("href")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(result_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to download file: {response.status_code}")
        with open(f'{PDB_PATH}{protein_id}.pdb', 'wb') as file:
            file.write(response.content)
        logging.info(f"File saved at {PDB_PATH}{protein_id}.pdb. URL: {url}")
        return "concluded"
    except Exception as e:
        logging.warning(f"Error downloading PDB for protein ID {protein_id}: {e}")
        return url


def check_ip_limit(df):
    try:
        logging.info("Checking IP submission limit.")
        submitted_df = df[df[MODEL].str.contains('output', na=False)]
        limit = 50 - len(submitted_df)
        logging.info(f"Remaining submission limit: {limit}")
        return limit
    except Exception as e:
        logging.error(f"Error checking IP limit: {e}")
        return 0


def download_pdbs(df):
    driver = None
    try:
        logging.info("Connecting to TrRosetta for downloading models.")
        driver = webdriver.Chrome(options=options)
        submitted_df = df[df[MODEL].str.contains('output', na=False)]
        if submitted_df.empty:
            logging.info("No models to download.")
        else:
            for i, (index, row) in enumerate(submitted_df.iterrows()):
                gene = row['gene']
                variant = row['variant']
                protein_id = gene if variant == 'wild' else variant
                logging.info(f"Downloading {i + 1}/{len(submitted_df)}: {variant}")
                url = row[MODEL]
                result = download_pdb(driver, url, protein_id)
                if result == "concluded":
                    df.at[index, MODEL] = 'ok'
                    update_fasta_dataset(df, MODEL)
            logging.info("All models downloaded successfully.")
    except Exception as e:
        logging.error(f"Error during PDB download: {e}")
    finally:
        if driver:
            driver.quit()


def submit_pdbs(df):
    driver = None
    try:
        logging.info("Connecting to TrRosetta for submitting models.")
        driver = webdriver.Chrome(options=options)
        limit = check_ip_limit(df)
        if limit > 0:
            logging.info(f"You can submit {limit} models.")
            if df[MODEL].dtype != 'object':
                df[MODEL] = df[MODEL].astype('object')
            todo_df = df[(df[MODEL] != 'ok') & (~df[MODEL].astype(str).str.contains('output', na=False))]
            logging.info(f"{len(todo_df)} models to be submitted.")
            if not todo_df.empty:
                for i, (index, row) in enumerate(todo_df.iterrows()):
                    logging.info(f"Submitting model {i + 1}/{len(todo_df)}: {row['variant']}")
                    url = submit_pdb(driver, row['fasta'], row['variant'])
                    df.at[index, MODEL] = url
                    update_fasta_dataset(df, column=MODEL)
                    limit -= 1
                    if limit <= 0:
                        logging.warning("IP submission limit reached.")
                        break
            else:
                logging.info("All models are already submitted.")
        else:
            logging.error("IP limit reached. Please try again later.")
    except Exception as e:
        logging.error(f"Error during PDB submission: {e}")
    finally:
        if driver:
            driver.quit()
    return df

def get_pdbs():
    try:
        logging.info("Starting PDB generation process.")
        df = pd.read_csv(FASTA_FILE, sep=';')
        if not os.path.exists(PDB_PATH):
            os.makedirs(PDB_PATH)
            logging.info(f"Created PDB directory: {PDB_PATH}")
        if not df.empty:
            submit_pdbs(df)
            download_pdbs(df)
        else:
            logging.warning("No models to be created.")
    except Exception as e:
        logging.error(f"Error in PDB generation process: {e}")