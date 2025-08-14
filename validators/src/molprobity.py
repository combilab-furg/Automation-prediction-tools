import logging
import time
import os
import numpy as np
import pandas as pd
from constants import BACKOFF_FACTOR, MAX_RETRIES, RESULTS_PATH
from logs import setup_logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium_utils import (
	click_button_by_xpath,
	connect_url,
	dismiss_alert,
	fill_field_by_xpath,
	get_value_by_xpath,
	get_custom_timeout,
	wait_element,
)

from utils import filter_df, load_df

VALIDATOR = "molprobity"
MOLPROBITY_URL = "http://molprobity.biochem.duke.edu/"


options = webdriver.ChromeOptions() 
options.add_argument('--headless') 
options.add_argument('--no-sandbox') 
options.add_argument('--disable-dev-shm-usage') 

setup_logging()

def process_file(driver, row):
	try:
		pdb_path = row["pdb"]
		file_path = os.path.abspath(pdb_path)
		driver, timeout = connect_url(driver, MOLPROBITY_URL)
		custom_timeout = get_custom_timeout(driver, 5)
		fill_field_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div[1]/form/div/table/tbody/tr[3]/td[1]/input',file_path, timeout)
		# input("1")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div[1]/form/div/table/tbody/tr[3]/td[3]/input', timeout, driver)
		# input("2")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/input[3]', timeout, driver)
		# input("3")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/a', timeout, driver)
		# input("4")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/p[4]/table/tbody/tr/td[1]/input', timeout, driver)
		# input("5")
		try:
			click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/p[2]/input', custom_timeout, driver) 
		except Exception as e:
			click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/p/input', timeout, driver)
		# input("6")
		dismiss_alert(driver) 
		# input("7")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/input[3]', timeout, driver)
		# input("8")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td[2]/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/a', timeout, driver)
		# input("9")
		click_button_by_xpath('/html/body/table/tbody/tr[2]/td/div/form/p[2]/table/tbody/tr/td[1]/input', custom_timeout, driver)
		# input("10")
		wait_element('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody', timeout)
		poor_rotamers = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[3]/td[3]',timeout)
		poor_rotamers_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[3]/td[4]',timeout).split('%')[0])
		poor_rotamers_result = "good" if poor_rotamers_percentage <= 0.3 else "warning" if poor_rotamers_percentage >= 1.5 else "caution"
		favored_rotamers = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[4]/td[2]', timeout)
		favored_rotamers_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[4]/td[3]', timeout).split('%')[0])
		favored_rotamers_result = "good" if favored_rotamers_percentage >= 98 else "warning" if favored_rotamers_percentage < 95 else "caution"
		ramachandran_outliers = int(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[5]/td[2]', timeout))
		ramachandran_outliers_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[5]/td[3]', timeout).split('%')[0])
		ramachandran_result = "good" if ramachandran_outliers_percentage <= 0.05 else "warning" if ramachandran_outliers_percentage >= 0.5 and ramachandran_outliers >= 2 else "caution"
		ramachandran_favored = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[6]/td[2]', timeout)
		ramachandran_favored_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[6]/td[3]', timeout).split('%')[0])
		ramachandran_favored_result = "good" if ramachandran_favored_percentage >= 98 else "warning" if ramachandran_favored_percentage < 95 else "caution"
		ramachandran_distribution_complete_z_score = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[7]/td[2]', timeout)
		ramachandran_distribution_z_score = float(ramachandran_distribution_complete_z_score.split(' ')[0])
		ramachandran_distribution_z_score_result = "good" if ramachandran_distribution_z_score <= 1.0 else "warning" if ramachandran_distribution_z_score <= 2.0 else "caution"
		molprobity_score = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[8]/td[2]', timeout)
		percentile = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[8]/td[3]', timeout).split(" ")[0].rstrip('stndrdth'))
		molprobity_result = "good" if percentile >= 66 else "warning" if percentile < 33 else "caution"	
		cb_deviations = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[9]/td[2]', timeout)
		cb_deviations_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[9]/td[3]', timeout).split('%')[0])
		cb_deviations_result = "good" if cb_deviations_percentage == 0 else "warning" if cb_deviations_percentage <= 5 else "caution"
		bad_bonds = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[10]/td[2]', timeout)
		bad_bonds_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[10]/td[3]', timeout).split('%')[0])
		bad_bonds_result = "good" if bad_bonds_percentage <= 0.01 else "warning" if bad_bonds_percentage >= 0.2 else "caution"
		bad_angles = get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[11]/td[2]', timeout)
		bad_angles_percentage = float(get_value_by_xpath('/html/body/table/tbody/tr[2]/td/div/p[1]/table/tbody/tr[11]/td[3]', timeout).split('%')[0])
		bad_angles_result = "good" if bad_angles_percentage <= 0.1 else "warning" if bad_angles_percentage >= 0.5 else "caution"	
		result = {
			"poor_rotamers": poor_rotamers,
			"poor_rotamers_percentage": poor_rotamers_percentage,
			"poor_rotamers_result": poor_rotamers_result,
			"favored_rotamers": favored_rotamers,
			"favored_rotamers_percentage": favored_rotamers_percentage,
			"favored_rotamers_result": favored_rotamers_result,
			"ramachandran_outliers": ramachandran_outliers,
			"ramachandran_outliers_percentage": ramachandran_outliers_percentage,
			"ramachandran_result": ramachandran_result,
			"ramachandran_favored": ramachandran_favored,
			"ramachandran_favored_percentage": ramachandran_favored_percentage,
			"ramachandran_favored_result": ramachandran_favored_result,
			"ramachandran_distribution_complete_z_score": ramachandran_distribution_complete_z_score,
			"ramachandran_distribution_z_score": ramachandran_distribution_z_score,
			"ramachandran_distribution_z_score_result": ramachandran_distribution_z_score_result,
			"molprobity_score": molprobity_score,
			"percentile": percentile,
			"molprobity_result": molprobity_result,
			"cb_deviations": cb_deviations,
			"cb_deviations_percentage": cb_deviations_percentage,
			"cb_deviations_result": cb_deviations_result,
			"bad_bonds": bad_bonds,
			"bad_bonds_percentage": bad_bonds_percentage,
			"bad_bonds_result": bad_bonds_result,
			"bad_angles": bad_angles,
			"bad_angles_percentage": bad_angles_percentage,
			"bad_angles_result": bad_angles_result,
		}
		return result

	except Exception as e:
		print(e)
		return {
			"poor_rotamers": np.nan,
			"poor_rotamers_percentage": np.nan,
			"poor_rotamers_result": "error",
			"favored_rotamers": np.nan,
			"favored_rotamers_percentage": np.nan,
			"favored_rotamers_result": "error",
			"ramachandran_outliers": np.nan,
			"ramachandran_outliers_percentage": np.nan,
			"ramachandran_result": "error",
			"ramachandran_favored": np.nan,
			"ramachandran_favored_percentage": np.nan,
			"ramachandran_favored_result": "error",
			"ramachandran_distribution_complete_z_score": np.nan,
			"ramachandran_distribution_z_score": np.nan,
			"ramachandran_distribution_z_score_result": "error",
			"molprobity_score": np.nan,
			"percentile": np.nan,
			"molprobity_result": "error",
			"cb_deviations": np.nan,
			"cb_deviations_percentage": np.nan,
			"cb_deviations_result": "error",
			"bad_bonds": np.nan,
			"bad_bonds_percentage": np.nan,
			"bad_bonds_result": "error",
			"bad_angles": np.nan,
			"bad_angles_percentage": np.nan,
			"bad_angles_result": "error"
		}

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
			result = process_file(driver, row)
			for key, value in result.items():
				df.loc[index, key] = value
				if value == "error":
					df.loc[index, VALIDATOR] = "error"
			if df.loc[index, VALIDATOR] != "error":
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