<!-- ---
layout: default
title: Format ALI
parent: Preprocess Index
nav_order: 13
--- -->

# Format .ALI

## Overview

This document provides a step-by-step guide to generate .ALI files for protein alignment using Modeller. You need to switch the kernel to a Python kernel where Modeller is installed on your machine.

## Input

- `fasta_variant.csv`: A CSV file containing variant data, including gene names and FASTA sequences.

## Output

- `.ali` files: Generated alignment files for each variant.

## Import Libraries and Load Dependencies

```python
import pandas as pd
from modeller import *
from modeller.automodel import *
from pandarallel import pandarallel
import os

pandarallel.initialize() # Initializing pandarallel for parallel processing
```

## Define Global Variables

```python
env = Environ()  # Create a Modeller environment object

CSV_PATH = "../../data/csv/"
PDB_PATH = '../../data/pdb/blast/'
PIR_PATH = '../../data/pir/'
ALI_PATH = '../../data/ali/'
```

## Load Dataset

```python
variant_df = pd.read_csv(f'{CSV_PATH}fasta_variant.csv', sep=';')  # Load data into a pandas DataFrame
variant_df.head()
```

## Generate .ALI Files

```python
def process_variant(row): # Function to process each variant and generate .ali files
    gene = row['gene']  # Extract the gene name from the current row
    variant_raw = row['variant']  # Extract the raw variant name from the current row
    variant = row['variant'].replace("_p.", "_")  # Replace "_p." in the variant name with "_"
    ali_file_path = os.path.join(ALI_PATH, f"{variant}.ali")  # Construct the .ali file path
    
    if not os.path.exists(ali_file_path): # Check if the .ali file already exists
        aln = Alignment(env)  # Create a new alignment object for this variant

        # Add the model to the alignment object using the PDB file
        md1 = Model(env, file=f'{PDB_PATH}{gene}.pdb')
        aln.append_model(md1, align_codes=gene, atom_files=f'{PDB_PATH}{gene}.pdb')
    
        aln.append(file=f'{PIR_PATH}{variant}.txt', align_codes=variant_raw) # Add the PIR file to the alignment object
    
        aln.align2d() # Perform the alignment
    
        aln.write(file=ali_file_path, alignment_format='PIR') # Write the alignment to a .ali file in PIR format

        print(f"Generated alignment file for {variant}")  # Notify the user of the generated file
    else:    
        print(f"Alignment file for {variant} already exists. Skipping.")

    return row  # Return the processed row

print(f"Number of sequences in CSV: {len(variant_df)}")  # Print the total number of sequences in the CSV
print(f"Number of .ali files: {len([name for name in os.listdir(ALI_PATH) if name.endswith('.ali')])}")  # Count and print the number of .ali files in the directory
print(f"Number of missing files: {len(variant_df) - len([name for name in os.listdir(ALI_PATH)])}")  # Calculate and print the number of missing files

variant_df.parallel_apply(process_variant, axis=1) # Apply the process_variant function to each row in the DataFrame using parallel processing

# Display the updated number of sequences and .ali files after processing
print(f"Number of sequences in CSV: {len(variant_df)}")
print(f"Number of .ali files: {len([name for name in os.listdir(ALI_PATH) if name.endswith('.ali')])}")
```