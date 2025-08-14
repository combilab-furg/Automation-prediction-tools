from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

def connect_url(driver, url):
    timeout = WebDriverWait(driver, 12600000000)
    driver.get(url)
    return driver, timeout

def get_custom_timeout(driver, timeout=5):
    return WebDriverWait(driver, timeout)
    

def click_button_by_xpath(xpath, timeout, driver):
	button = timeout.until(EC.element_to_be_clickable((By.XPATH, xpath)))
	try:
		button.click()
	except ElementClickInterceptedException:
		driver.execute_script("arguments[0].scrollIntoView(true);", button)
		sleep(1)
		try:
			button.click()
		except ElementClickInterceptedException:
			raise Exception("Element is still not clickable after scrolling.")

def click_button_by_name(name, timeout):
    button = timeout.until(EC.presence_of_element_located((By.NAME,name)))
    button.click()

def click_button_by_id(id, driver, timeout):
    button = timeout.until(EC.presence_of_element_located((By.ID, id)))
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()

def click_radio_button_by_xpath(xpath, driver, timeout):
    radio_button = timeout.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView();", radio_button)
    actions = ActionChains(driver)
    actions.move_to_element(radio_button).click().perform()

def click_radio_button_by_name(name, driver, timeout):
    radio_button = timeout.until(EC.presence_of_element_located((By.NAME, name)))
    driver.execute_script("arguments[0].scrollIntoView();", radio_button)
    driver.execute_script("arguments[0].click();", radio_button)

def click_radio_button_by_id(id, driver, timeout):
    radio_button = timeout.until(EC.presence_of_element_located((By.ID, id)))
    driver.execute_script("arguments[0].scrollIntoView();", radio_button)
    driver.execute_script("arguments[0].click();", radio_button)

def get_value_by_xpath(xpath, timeout):
    return timeout.until(EC.presence_of_element_located((By.XPATH, xpath))).text

def fill_field_by_xpath(xpath, value, timeout):
    file_field = timeout.until(EC.presence_of_element_located((By.XPATH, xpath)))
    file_field.send_keys(value)

def fill_field_by_id(id, value, timeout):
    file_field = timeout.until(EC.presence_of_element_located((By.ID, id)))
    file_field.send_keys(value)

def wait_element(xpath, timeout):
    timeout.until(EC.presence_of_element_located((By.XPATH, xpath)))

def dismiss_alert(driver):
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = Alert(driver)
    alert.dismiss()