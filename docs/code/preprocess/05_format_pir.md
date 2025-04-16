<!-- ---
layout: default
title: Format PIR
parent: Preprocess Index
nav_order: 12
--- -->

# Format PIR

## Overview

This document guides you through generating PIR-formatted alignment files for protein sequences using pandas for data manipulation and analysis. The process involves loading the dataset, iterating over each row to extract gene and variant information, and generating the PIR-formatted files.

## Input

- `fasta_variant.csv`: Contains variant data, including gene names and FASTA sequences.

## Output

- PIR files: Generated PIR-formatted `.ali` files for each variant.

## Import Libraries and Load Dependencies

```python
import pandas as pd
import os
```

## Define Global Variables

```python
CSV_PATH = "../../data/csv/"  # Directory containing CSV files
PDB_PATH = '../../data/pdb/blast'  # Directory containing PDB files
PIR_PATH = '../../data/pir'  # Directory for storing generated PIR files
```

## Load Dataset

```python
variant_df = pd.read_csv(f'{CSV_PATH}fasta_variant.csv', sep=';')
variant_df.head()
```

## Generate PIR-formatted Files

```python
def generate_ali_files(df): # Function to generate PIR-formatted alignment (.ali) files    
    for index, row in df.iterrows(): # Iterate over each row in the DataFrame
        gene = row['gene']  # Extract gene name from the current row
        variant = row['variant']  # Extract variant name from the current row
        target_fasta_content = row['fasta']  # Extract the fasta sequence content from the current row
        pdb_file = os.path.join(PDB_PATH, f"{gene}.pdb")  # Construct the path to the PDB file for the gene
        
        if os.path.isfile(pdb_file): # Check if the PDB file exists
            # Create the content for the .ali file in PIR format
            ali_content = f""">P1;{variant}
sequence:{variant}:::::::0.00: 0.00
{target_fasta_content}*
"""            
            ali_file = os.path.join(PIR_PATH, f"{variant}.txt") # Define the path for the .ali file   
            with open(ali_file, 'w') as out: # Write the .ali content to the file
                out.write(ali_content)
            print(f"Generated {ali_file}")  # Notify the user that the file was generated successfully
        else:            
            print(f"PDB file for gene {variant} not found.")

generate_ali_files(variant_df) # Call the function to generate .ali files using the variant DataFrame
```