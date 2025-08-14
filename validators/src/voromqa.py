import logging
import os
import time
import numpy as np

from constants import BACKOFF_FACTOR, MAX_RETRIES, RESULTS_PATH
from logs import setup_logging
from selenium_utils import click_button_by_xpath, fill_field_by_xpath, webdriver
from selenium.common.exceptions import WebDriverException
from selenium_utils import (
    connect_url,
    get_value_by_xpath,
)
from utils import filter_df, load_df

VALIDATOR = "voromqa"
VOROMQA_URL = "https://bioinformatics.lt/wtsam/voromqa/submit"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

setup_logging()

def process_file(driver, row):
    try:
        pdb_path = row['pdb']
        file_path = os.path.abspath(pdb_path)
        driver, wait = connect_url(driver, VOROMQA_URL)
        fill_field_by_xpath('/html/body/div/div[2]/div/div[3]/div/div[3]/div[1]/div[1]/div/div[3]/div[2]/form/input', file_path, wait)        
        click_button_by_xpath('/html/body/div/div[2]/div/div[3]/div/div[3]/div[1]/div[1]/div/div[11]/button', wait, driver)
        return {
            'voromqa_score': get_value_by_xpath('/html/body/div/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[1]/div[3]/div[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td[4]/span', wait),
            'residues': get_value_by_xpath('/html/body/div/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[1]/div[3]/div[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td[6]/span', wait),
            'atoms': get_value_by_xpath('/html/body/div/div[2]/div/div[3]/div/div[3]/div[2]/div[3]/div/div[1]/div[3]/div[2]/table/tbody/tr/td/div/table[1]/tbody/tr/td[8]/span', wait),
        }
    except Exception as e:
        print(e)
        return {
            'voromqa_score': np.nan,
            'residues': np.nan,
            'atoms': np.nan,
        }

def main():
    df = load_df(VALIDATOR)
    filtered_df = filter_df(df, VALIDATOR)
    model_counts = filtered_df["model"].value_counts()
    logging.info("[INFO] - Files per model:")
    logging.info(model_counts)
    logging.info(f"[INFO] - Processing {len(filtered_df)} files")
    for i, (index, row) in enumerate(filtered_df.iterrows()):
        try:
            driver = webdriver.Chrome(options=options)
            logging.info(f"[INFO] - Processing {i + 1}/{len(filtered_df)}: {row['gene']} - {row['variant']}")
            result = process_file(driver, row)
            df.loc[index, "voro_score"] = result['voromqa_score']
            df.loc[index, "residues"] = result['residues']
            df.loc[index, "atoms"] = result['atoms']
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