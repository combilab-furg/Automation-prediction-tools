<!-- ---
layout: default
title: PDB MycoBrowser Analysis
parent: Preprocess Index
nav_order: 9
--- -->

# PDB Information Extraction from Mycobrowser

## Overview

This document guides you through extracting PDB information from Mycobrowser using _Selenium_ for web scraping and _pandas_ for data manipulation. 
The process involves loading the dataset, defining functions to fetch PDB information, processing each gene to extract information, and saving the results to a CSV file.

## Input and Output

### Input

- `complete_wild.csv`: Contains the complete wild dataset with gene information and Mycobrowser URLs.

### Output

- `complete_wild_pdb_mycobrowser.csv`: A CSV file containing PDB information for each gene from Mycobrowser.

## Code Explanation

### Import Libraries and Load Dependencies

```python
import pandas as pd

from selenium import webdriver # Import selenium libraries for web scraping and browser automation
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions() # Initialize Chrome options
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')  # Disable the sandbox for Chrome
options.add_argument('--disable-dev-shm-usage')  # Disable the /dev/shm usage for Chrome

driver = webdriver.Chrome(options=options) # Create a new instance of the Chrome driver with the specified options
```

### Define Global Variables

```python
CSV_PATH = "../../data/csv/"
```

### Load Dataset

```python
wild_df = pd.read_csv(f'{CSV_PATH}complete_wild.csv', sep=';')
```

### Display Initial Dataset Information

```python
wild_df.head()
print(f"Dataset shape: {wild_df.shape}")
print(f"Rows: {wild_df.shape[0]}")
print(f"Columns: {wild_df.shape[1]}")
wild_df.describe()
```

### Define Functions to Fetch PDB URL

#### Function to Wait Until the Column Menu is Present

```python
def wait_column_menu(driver):
    column_xpath = '//*[@id="main"]/div[5]/div[1]'  # XPath for the column menu
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, column_xpath))  # Wait until the column menu is present
    )
```

#### Function to Find Structural Information Section

```python
def find_structural_information(driver):
    structural_information_xpath = "//div[@class='panel-heading' and contains(text(), 'Structural information')]"  # XPath for structural information
    elements = driver.find_elements(By.XPATH, structural_information_xpath)  # Find elements matching the XPath
    return elements[0] if elements else None  # Return the first element if found, otherwise return None
```

#### Function to Find PDB Information

```python
def find_pdb_information(structural_information):
    parent_div = structural_information.find_element(By.XPATH, "..")  # Find the parent div of the structural information
    pdb_information_xpath = ".//tr[td[contains(text(), 'Protein Data Bank')]]"  # XPath for PDB information
    elements = parent_div.find_elements(By.XPATH, pdb_information_xpath)  # Find elements matching the XPath
    return elements[0] if elements else None  # Return the first element if found, otherwise return None
```

#### Function to Find PDB Links

```python
def find_pdb_links(pdb_information):
    links = pdb_information.find_elements(By.XPATH, ".//td[2]//a")  # Find links within the PDB information
    return links if links else None  # Return the links if found, otherwise return None
```

#### Main Function to Get PDB Information

```python
def get_pdb_info(driver):
    wait_column_menu(driver)  # Wait for the column menu to be present
    structural_information = find_structural_information(driver)  # Find structural information
    if not structural_information:
        return "No structural information found"  # Return message if no structural information is found
    else:
        pdb_information = find_pdb_information(structural_information)  # Find PDB information
        if not pdb_information:
            return "No PDB information found"  # Return message if no PDB information is found
        else:
            links = find_pdb_links(pdb_information)  # Find PDB links
            if links:
                return "PDB information found"  # Return message if PDB links are found
            else:
                return "No url found."  # Return message if no PDB links are found
```

#### Process Each Gene in the Dataset

```python
pdb_table = [] # Initialize an empty list to store PDB information

for index, row in wild_df.iterrows(): # Iterate through each row in the dataset
    print(f"Processing genes... ({index+1} from {wild_df.shape[0]})")  # Print the progress
    gene = row["gene"]  # Get the gene name
    url = row["mycobrowser_url"]  # Get the MycoBrowser URL
    
    try:
        driver.get(url)  # Navigate to the URL
        
        pdb_info = get_pdb_info(driver)  # Get PDB information
        
        # Append the information to the list
        pdb_table.append({
            "gene": gene,  # Add gene name to the dictionary
            "mycobrowser_URL": url,  # Add MycoBrowser URL to the dictionary
            "has_PDB_info": pdb_info,  # Add PDB information status to the dictionary
        })
    
    except Exception as e:
        print(f"Error processing gene {gene}: {e}")  # Print error message if an exception occurs
```

### Create a DataFrame from the PDB Information

```python
pdb_df = pd.DataFrame(pdb_table) # Convert the list of dictionaries to a DataFrame
pdb_df.head()
pdb_df.describe()
pdb_df["has_PDB_info"].value_counts() # Count the occurrences of each PDB information status
```

### Save the PDB Information to a CSV File

```python
# Save the DataFrame to a CSV file
pdb_df.to_csv(f"{CSV_PATH}complete_wild_pdb_mycobrowser.csv", index=False, sep=';')
```