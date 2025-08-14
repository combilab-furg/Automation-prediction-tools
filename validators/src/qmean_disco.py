import logging
import os
import time

import pandas as pd
from constants import BACKOFF_FACTOR, MAX_RETRIES, RESULTS_PATH
from logs import setup_logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium_utils import (
	click_button_by_xpath,
	connect_url,
	fill_field_by_id,
	get_value_by_xpath,
)
from utils import filter_df, load_df

VALIDATOR = "qmean_disco"
QMEAN_URL = "https://swissmodel.expasy.org/qmean/"

options = webdriver.ChromeOptions() 
options.add_argument('--headless') 
options.add_argument('--no-sandbox') 
options.add_argument('--disable-dev-shm-usage') 

setup_logging()

def process_file(driver, row):
    pdb_file = row['pdb']
    file_path = os.path.abspath(pdb_file)
    driver, timeout = connect_url(driver, QMEAN_URL)
    fill_field_by_id('structureFile', file_path, timeout)
    click_button_by_xpath('/html/body/div[2]/div[2]/div/form/div[6]/button', timeout, driver)
    return float(get_value_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div/span/span[2]', timeout))

def main():
	df = load_df(VALIDATOR)
	filtered_df = filter_df(df,VALIDATOR)
	model_counts = filtered_df["model"].value_counts()
	logging.info("[INFO] - Files per model:")
	logging.info(model_counts)
	logging.info(f"[INFO] - Processing {len(filtered_df)} files")

	for i, (index, row) in enumerate(filtered_df.iterrows()):
		
		try:
			driver = webdriver.Chrome(options=options)
			# driver = webdriver.Chrome()
			logging.info(f"[INFO] - Processing {i + 1}/{len(filtered_df)}: {row['gene']} - {row['variant']}")
			qmean_disco_value = process_file(driver, row)
			df.loc[index, "qmean_disco_value"] = qmean_disco_value
			df.loc[index, VALIDATOR] = "ok"
		except WebDriverException as e:
			logging.error(f"[ERROR] - WebDriver error for {row['variant']}: {e}")
		except RuntimeError as e:
			logging.error(f"[ERROR] - Processing error for {row['variant']}: {e}")
		except Exception as e:
			logging.error(f"[ERROR] - Unexpected error for {row['variant']}: {e}")
		finally:
			driver.quit()
			
		result_file = f"{RESULTS_PATH}/{VALIDATOR}.csv"
		df.to_csv(result_file, sep=";", index=False)
	logging.info("[SUCCESS] - Processing complete.")

if __name__ == "__main__":
	main()