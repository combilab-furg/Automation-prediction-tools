<!-- ---
layout: default
title: Helper functions
parent: Code Overview
nav_order: 22
--- -->

# Helper functions

## **Note:** 

Be careful, all the files in `input_directory` will be deleted after the execution of the code.

## Overview

This document provides a detailed step-by-step guide to process protein structure data by extracting and updating files and statuses across multiple tools including Swiss Model, Colab AlphaFold2, Phyre2, Blast, and AlphaFold3.

## Input and Output

### Input

- `input_dir`: Directory containing input files.
- `CSV_PATH`: Path to CSV files containing sequence and variant information.

### Output

- Updated CSV files and PDB files for various tools saved in the specified paths.

## Code Explanation

### Import Libraries and Load Dependencies

We import necessary libraries for data manipulation, file handling, web scraping, and parallel processing with pandas.

```python
import os
import zipfile
import glob
import shutil
import pandas as pd
```

### Define Variables

We define paths and directories required for processing data.

```python
input_dir = 'input'
output_dir = 'output'
CSV_PATH = "../../data/csv"
```

### Check and Update Status

Common functions to check if a PDB file exists for each variant and update the status in the DataFrame accordingly.

```python
def check_and_update_status(row):
    variant = row["variant"]
    filename = variant.replace('_p.', '_')
    file_path = f"{PDB_PATH}/{filename}.pdb"
    print(file_path)
    if os.path.isfile(file_path):
        return 'concluded'
    return 'not_concluded'

def update_status(df, column):
    if column not in df.columns:
        df[column] = 'not_concluded'
    df[column] = df.apply(check_and_update_status, axis=1)
    print("Status updated based on existing files")
    return df
```

### Swiss Model - Update CSV with Files

Read the CSV, update the status for Swiss Model, and save the updated DataFrame.

```python
PDB_PATH = "../../data/pdb/swiss_model"
df = pd.read_csv(f'{CSV_PATH}/fasta_variant.csv', sep=';')
df = update_status(df, "swiss_model")
print(df['swiss_model'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_variant.csv', index=False, sep=';')
```

### Colab AlphaFold2 - Extract PDB from Zip Files

Extract PDB files from Colab AlphaFold2 zip files in the input directory.

```python
extract_dir = '../../data/pdb/colab_alphafold2'
os.makedirs(extract_dir, exist_ok=True)

zip_files = glob.glob(os.path.join(input_dir, '*.zip'))

for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        temp_dir = os.path.join(input_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        zip_ref.extractall(temp_dir)
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.pdb'):
                    dest_path = os.path.join(extract_dir, file)
                    if not os.path.exists(dest_path):
                        shutil.move(os.path.join(root, file), dest_path)
        shutil.rmtree(temp_dir)
    os.remove(zip_file)

print("Extraction complete.")
```

### Colab AlphaFold2 - Update CSV with Files

Update the CSV with the extracted PDB files from Colab AlphaFold2.

```python
PDB_PATH = "../../data/pdb/colab_alphafold2"
df = pd.read_csv(f'{CSV_PATH}/fasta_variant.csv', sep=';')
df = update_status(df, "colab_alphafold2")
print(df['colab_alphafold2'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_variant.csv', index=False, sep=';')
```

### Phyre2 - Extract FASTA Files

Function to extract FASTA files to use as input for Phyre2.

```python
def extract_fasta_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    fasta_files = glob.glob(os.path.join(input_dir, '**/*.fasta'), recursive=True)
    concatenated_content = []
    file_count = 0
    variant_index = 1
    start_index = 1

    for fasta_file in fasta_files:
        with open(fasta_file, 'r') as f:
            lines = f.readlines()
            concatenated_content.extend(lines)
            concatenated_content.append('\n')
            file_count += 1

            if file_count == 100:
                end_index = start_index + file_count - 1
                output_file = os.path.join(output_dir, f'variant_{start_index}_{end_index}.fasta')
                with open(output_file, 'w') as out_f:
                    out_f.writelines(concatenated_content)
                concatenated_content = []
                file_count = 0
                start_index = end_index + 1
                variant_index += 1
        os.remove(fasta_file)

    if concatenated_content:
        end_index = start_index + file_count - 1
        output_file = os.path.join(output_dir, f'variant_{start_index}_{end_index}.fasta')
        with open(output_file, 'w') as out_f:
            out_f.writelines(concatenated_content)

    print("Extraction complete.")
    shutil.rmtree(input_dir)

extract_fasta_files(input_dir, output_dir)
```

### Extract PDB files from Phyre2 result

Function to extract PDB files from Phyre2 results.

```python
def extract_pdb_files_from_phyre2(input_dir, csv_path, output_dir):
    summary_dict = {}

    os.makedirs(output_dir, exist_ok=True)

    zip_files = glob.glob(os.path.join(input_dir, '*.zip'))
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            temp_dir = os.path.join(input_dir, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            zip_ref.extractall(temp_dir)

            summaryinfo_path = os.path.join(temp_dir, 'summaryinfo')
            if os.path.isfile(summaryinfo_path):
                with open(summaryinfo_path, 'r') as summary_file:
                    for line in summary_file:
                        if line.startswith('#'):
                            continue
                        parts = line.strip().split('|')
                        if len(parts) >= 4:
                            description = f"{parts[1].strip()}_{parts[2].strip()}"
                            sequence_identity = parts[3].strip()
                            summary_dict[sequence_identity] = description

            for pdb_file in glob.glob(os.path.join(temp_dir, '*.final.pdb')):
                pdb_filename = os.path.basename(pdb_file)
                pdb_key = os.path.splitext(pdb_filename)[0].split(".")[0]
                if pdb_key in summary_dict:
                    description = summary_dict[pdb_key]
                    value1, value2 = description.split('_')
                    csv_file_path = os.path.join(csv_path, 'fasta_variant.csv')
                    df = pd.read_csv(csv_file_path, sep=';')
                    gene = df.loc[df['identifier'] == value1, 'gene'].values[0]
                    new_pdb_filename = f"{gene}_{value2}.pdb"
                    new_pdb_path = os.path.join(output_dir, new_pdb_filename)
                    shutil.move(pdb_file, new_pdb_path)

            shutil.rmtree(temp_dir)
        os.remove(zip_file)

    csv_file_path = os.path.join(csv_path, 'fasta_variant.csv')
    df = pd.read_csv(csv_file_path, sep=';')

    for sequence_identity, description in summary_dict.items():
        value1, value2 = description.split('_')
        gene = df.loc[df['identifier'] == value1, 'gene'].values[0]
        new_description = f"{gene}_{value2}"
        if os.path.isfile(os.path.join(output_dir, f"{new_description}.pdb")):
            df.loc[df['identifier'] == value1, 'phyre2'] = 'concluded'
        else:
            df.loc[df['identifier'] == value1, 'phyre2'] = 'not_concluded'

    df.to_csv(csv_file_path, sep=';', index=False)
    return summary_dict

input_dir = 'input'
csv_path = '../../data/csv'
output_dir = '../../data/pdb/phyre2'

summary_dict = extract_pdb_files_from_phyre2(input_dir, csv_path, output_dir)
```

### Phyre2 - Update CSV with Files

Update the CSV with the extracted PDB files from Phyre2.

```python
PDB_PATH = "../../data/pdb/phyre2"
df = pd.read_csv(f'{CSV_PATH}/fasta_variant.csv', sep=';')
df = update_status(df, "phyre2")
print(df['phyre2'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_variant.csv', index=False, sep=';')
```

### Blast - Update Blast Column

Update the Blast status in the DataFrame based on the existence of PDB files.

```python
def check_and_update_blast_status(row):
    gene = row["gene"]
    file_path = f"{PDB_PATH}/{gene}.pdb"
    print(file_path)
    if os.path.isfile(file_path):
        return 'concluded'
    return 'not_concluded'

PDB_PATH = "../../data/pdb/blast"
df = pd.read_csv(f'{CSV_PATH}/fasta_wild.csv', sep=';')
if "blast" not in df.columns:
    df["blast"] = 'not_concluded'
df["blast"] = df.apply(check_and_update_blast_status, axis=1)
print("Status updated based on existing files")
print(df['blast'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_wild.csv', index=False, sep=';')
```

### AlphaFold3 - Process PDB Files

Process PDB files for AlphaFold3 by moving them to the appropriate directory and updating filenames.

```python
def process_pdb_files():
    destination_folder = os.path.abspath("../../data/pdb/alphafold3")
    os.makedirs(destination_folder, exist_ok=True)
    pdb_files = glob.glob(os.path.join(input_dir, "*.pdb"))
    for pdb_file in pdb_files:
        new_filename = os.path.basename(pdb_file).replace("_p.", "_").replace("_model0", "")
        destination_file = os.path.join(destination_folder, new_filename)

        shutil.move(pdb_file, destination_file)
        print(f"Moved file: {pdb_file} to {destination_file}")
    all_files = glob.glob(os.path.join(input_dir, "*.*"))
    for file in all_files:
        if not file.endswith(".pdb"):
            os.remove(file)
            print(f"Deleted file: {file}")

process_pdb_files()
```

### AlphaFold3 - Update CSV with Files

Update the CSV with the processed PDB files from AlphaFold3.

```python
PDB_PATH = "../../data/pdb/alphafold3"
df = pd.read_csv(f'{CSV_PATH}/fasta_variant.csv', sep=';')
df = update_status(df, "alphafold3")
print(df['alphafold3'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_variant.csv', index=False, sep=';')
```

### Modeller - Update CSV with Files

Update the CSV with the processed PDB files from Modeller.

```python
PDB_PATH = "../../data/pdb/modeller"
df = pd.read_csv(f'{CSV_PATH}/fasta_variant.csv', sep=';')
df = update_status(df, "modeller")
print(df['modeller'].value_counts())
df.to_csv(f'{CSV_PATH}/fasta_variant.csv', index=False, sep=';')
```

### Clean Up

Function to rename files in the directory by removing specific substrings.

```python
def rename_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            new_filename = file.replace("_p.", "_")
            os.rename(os.path.join(root, file), os.path.join(root, new_filename))
            print(f"Renamed file: {file} to {new_filename}")

rename_files("../../data")
```