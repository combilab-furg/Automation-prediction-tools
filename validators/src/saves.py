import logging
import os
import time
import pandas as pd
from constants import BACKOFF_FACTOR, MAX_RETRIES, RESULTS_PATH
from logs import setup_logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium_utils import (
	click_button_by_id,
	click_button_by_xpath,
	connect_url,
	fill_field_by_id,
	get_custom_timeout,
	get_value_by_xpath,
	wait_element,
)
from utils import filter_df, load_df

VALIDATOR = "saves"
SAVES_URL = "https://saves.mbi.ucla.edu/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

setup_logging()

def process_file(driver: webdriver.Chrome, row: pd.Series) -> tuple[str, str]:
	try:
		pdb_file = row["pdb"]
		file_path = os.path.abspath(pdb_file)
		driver, timeout = connect_url(driver, SAVES_URL)
		fill_field_by_id("pdbfile", file_path, timeout)
		click_button_by_id("startjob", driver, timeout)
		click_button_by_id("startjob", driver, timeout)
		click_button_by_xpath("/html/body/table/tbody/tr[1]/td[1]/div[2]/span[2]", timeout, driver)
		click_button_by_xpath("/html/body/table/tbody/tr[1]/td[2]/div[2]/span[2]", timeout, driver)
		wait_element("//u[text()='Overall Quality Factor']", timeout)
		wait_element("/html/body/table/tbody/tr[1]/td[2]/div[1]/div/span", timeout)
		errat_value = get_value_by_xpath(
			"/html/body/table/tbody/tr[1]/td[1]/div[1]/div/center/center/h1", timeout
		)
		errat_result = "rejected" if errat_value < 95 else "accepted"
		raw_verify_value = get_value_by_xpath('/html/body/table/tbody/tr[1]/td[2]/div[1]/div/center/div[1]', timeout)
		verify_value = f"{raw_verify_value.split(' ')[0]} {raw_verify_value.split(' ')[-2]} {raw_verify_value.split(' ')[-1]}"
		verify_result = get_value_by_xpath(
			"/html/body/table/tbody/tr[1]/td[2]/div[1]/div/center/div[2]", timeout
		)
		return errat_value, errat_result, verify_value, verify_result
	except Exception as e:
		raise RuntimeError(f"Error processing file: {e}")

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
			errat_value, errat_result, verify_value, verify_result = process_file(driver, row)
			df.loc[index, "errat_value"] = errat_value
			df.loc[index, "errat_result"] = errat_result
			df.loc[index, "verify_value"] = verify_value
			df.loc[index, "verify_result"] = verify_result
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