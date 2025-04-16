<!-- ---
layout: default
title: Swiss Model
parent: Model Index
nav_order: 14
--- -->

# Swiss Model

## Overview

This documentation provides a comprehensive guide to automating the process of managing and generating protein models using SwissModel service. 
It explains how to check and update statuses, initiate modeling, wait for completion, download PDB files, and update the dataset appropriately.

## Input and Output

### Input

- `fasta_variant.csv`: A CSV file containing fasta sequences and variant information.

### Output

- Updated `fasta_variant.csv`: A CSV file with updated statuses post-modeling.
- PDB files: Generated protein models in PDB format, saved into the specified path.

### Import Libraries and Load Dependencies

```python
import time
import pandas as pd
import requests
import gzip
import os
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)
```

### Define Global Variables

```python
CSV_PATH = "../../data/csv/"  # Path to the CSV files
PDB_PATH = "../../data/pdb/swiss_model/"  # Path to save PDB files
ONE_MINUTE = 60  # One minute in seconds
SIX_HOURS = 6 * 60 * 60  # Six hours in seconds
TOKEN = "e76e1cfea901a4497d7b6007a379939340126b4a"  # Authorization token for the SwissModel API
# TOKEN = "3292b97d245ba99f1f80ad03ab8de69c8ef909f2" Alternative token (commented out)
```

We define paths, constants, and the authorization token for the SwissModel API.

### importing the dataset containing variant and FASTA sequence information.

```python
variant_df = pd.read_csv(f'{CSV_PATH}fasta_variant.csv', sep=';')
variant_df.head()
```

### Functions to check the existence of PDB files for each variant and update the status in the dataset accordingly. 

```python
def check_and_update_status(row):
    variant = row["variant"]
    filename = variant.replace('_p.', '_')
    file_path = f"{PDB_PATH}{filename}.pdb"
    if os.path.isfile(file_path):
        return 'concluded'
    return 'not_concluded'

def update_swiss_model_status(df):
    if 'swiss_model' not in df.columns:
        df['swiss_model'] = 'not_concluded'
    df['swiss_model'] = df.apply(check_and_update_status, axis=1)
    df.to_csv(f'{CSV_PATH}fasta_variant.csv', index=False, sep=';')
    print("Status updated based on existing files")
```

# Get Model Functions: 

Functions to handle model generation, wait for completion, download PDB files, and obtain model details.

### Function to start a modeling job on SwissModel

```python
def start_modeling(title, sequence): # Send a POST request to the SwissModel API to start the modeling job
    response = requests.post(
        "https://swissmodel.expasy.org/automodel", # API endpoint for modeling
        headers={"Authorization": f"Token {TOKEN}"},
        json={
            "target_sequences": sequence, # Protein sequence to be modeled
            "project_title": title # Title of the modeling project
        }
    )
    project_id = response.json().get("project_id")
    return project_id
```

### Function to wait for the modeling job to complete

```python
def wait_modeling(project_id): # Infinite loop to periodically check the job status.
    while True:
        response = requests.get( # Send a GET request to check the status of the modeling job.
            f"https://swissmodel.expasy.org/project/{project_id}/models/summary/", # API endpoint for job status.
            headers={"Authorization": f"Token {TOKEN}"} # Authorization header with token.
        )
        status = response.json().get("status", "UNKNOWN") # Extract the job status from the JSON response (default to "UNKNOWN" if not found).
        if status in ["COMPLETED", "FAILED"]: # If the job is completed or failed, exit the loop.
            break
        time.sleep(10) # Wait for 10 seconds before checking again.
    if status == "COMPLETED":
        model = response.json().get("models", [])[0] # Extract the first model from the list of models in the response.
        return model # Return the model details.
    else:
        print("Modeling failed\n")
        return None # Return None to indicate failure
```

### Function to download and extract the PDB file

```python
def download_pdb(title, model): 
    filename = title.replace('_p.', '_') # Create a filename by replacing 'p.' with '' in the title.
    url = model["coordinates_url"] # Extract the URL of the PDB file from the model dictionary.
    response = requests.get(url)  # Send a GET request to download the PDB file.
    if response.status_code == 200:
        with open(f'{PDB_PATH}{filename}.pdb.gz', 'wb') as file: # Write the downloaded content to a gzipped file.
            file.write(response.content)
        with gzip.open(f'{PDB_PATH}{filename}.pdb.gz', 'rb') as gz_file: # Open the gzipped file for reading.
            with open(f'{PDB_PATH}{filename}.pdb', 'wb') as extracted_file: # Write the extracted content to a new PDB file.
                extracted_file.write(gz_file.read())
        os.remove(f'{PDB_PATH}{filename}.pdb.gz')  # Delete the gzipped file after extraction
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
```

### Function to orchestrate the modeling and downloading process

```python
def get_pdb(title, sequence):
    project_id = start_modeling(title, sequence) # Start the modeling job and get the project ID
    model = wait_modeling(project_id) # Wait for the modeling job to complete and get the model details
    return model # Return the model details
```

### Function to process each row of the dataset, initiate modeling, retrieve model details, and download PDB files.

```python
def process_row(row):
    title = row["variant"]
    sequence = [row["fasta"]]
    model = get_pdb(title, sequence)
    download_pdb(title, model)
    return True
```

### Run the Modeling

```python
update_swiss_model_status(variant_df) # Update the Swiss model status in the DataFrame.
not_concluded_df = variant_df[variant_df['swiss_model'] == 'not_concluded'] # Filter rows with 'not_concluded' status.
print("Starting modeling...")
results = not_concluded_df.parallel_apply(process_row, axis=1) # Apply the 'process_row' function in parallel to each row of 'not_concluded_df'.
variant_df.loc[not_concluded_df.index, 'swiss_model'] = results.apply(lambda x: 'concluded' if x else 'not_concluded')  # Update the status based on results.
print("Successfully modeled")
```

We update the Swiss model status, identify rows marked as 'not concluded', and start the modeling process. The statuses are then updated based on the results of the modeling process.