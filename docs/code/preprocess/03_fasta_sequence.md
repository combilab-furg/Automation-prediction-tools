<!-- ---
layout: default
title: FASTA Sequence Extraction
parent: Preprocess Index
nav_order: 10
--- -->

# FASTA Sequence Extraction from Mycobrowser

## Overview

This document guides you through extracting FASTA sequences from Mycobrowser using `requests` for HTTP requests and `BeautifulSoup` for parsing HTML. 
The process involves loading the datasets, defining functions to fetch and save FASTA sequences, processing each gene to extract the sequence, and saving the results to CSV files.

## Input

- `wild.csv`: Contains information about filtered wild-type genes.
- `complete_wild.csv`: Contains the complete dataset for wild-type genes.
- `variant.csv`: Contains information about variant genes.

## Output

- `fasta_wild.csv`: A CSV file containing the FASTA sequences for filtered wild-type genes.
- `fasta_complete_wild.csv`: A CSV file containing the FASTA sequences for complete wild-type genes.
- `fasta_variant.csv`: A CSV file containing the FASTA sequences for variant genes.

## Code Explanation

### Import Libraries and Load Dependencies

```python
import requests  # Library for sending HTTP requests to fetch data from URLs.
import pandas as pd
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents.
```

### Define Global Variables

```python
CSV_PATH = "../../data/csv/"
FASTA_PATH = "../../data/fasta/"  # Path to the folder for storing FASTA files.
WILD_FASTA_PATH = f"{FASTA_PATH}wild"  # Path for wild-type FASTA files.
COMPLETE_WILD_FASTA_PATH = f"{FASTA_PATH}complete_wild"  # Path for complete wild FASTA files.
VARIANT_FASTA_PATH = f"{FASTA_PATH}variant"  # Path for variant FASTA files.

AMINO_ACIDS = { # Dictionary mapping single-letter amino acid codes to their full names.
    'A': 'Ala',
    'C': 'Cys',
    'D': 'Asp',
    'E': 'Glu',
    'F': 'Phe',
    'G': 'Gly',
    'H': 'His',
    'I': 'Ile',
    'K': 'Lys',
    'L': 'Leu',
    'M': 'Met',
    'N': 'Asn',
    'P': 'Pro',
    'Q': 'Gln',
    'R': 'Arg',
    'S': 'Ser',
    'T': 'Thr',
    'V': 'Val',
    'W': 'Trp',
    'Y': 'Tyr',
}

# Reverse dictionary for mapping full names to single-letter codes.
AMINO_ACIDS_REVERSE = {value: key for key, value in AMINO_ACIDS.items()}
```

### Load Datasets

```python
wild_df = pd.read_csv(f'{CSV_PATH}wild.csv', sep=';')
complete_wild_df = pd.read_csv(f'{CSV_PATH}complete_wild.csv', sep=';')
variant_df = pd.read_csv(f'{CSV_PATH}variant.csv', sep=';')
```

### Define Function to Fetch Wild FASTA Sequence from MycoBrowser and Save into a File

```python
def save_fasta_sequence_wild(df, path):
    for index, row in df.iterrows(): # Iterate through each row in the DataFrame.
        print(f"Saving FASTA sequence... ({index+1} from {df.shape[0]})")  # Log progress.
        gene = row["gene"]  # Extract gene name from the current row.
        url = row["mycobrowser_url"]  # Extract Mycobrowser URL.
        response = requests.get(url)  # Send GET request to fetch HTML content.
        if response.status_code == 200:  # Check if the request was successful.
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse HTML content.
            fasta_section = soup.find_all('pre')  # Find all <pre> tags, which may contain FASTA sequences.
            if fasta_section:  # Check if any <pre> tags were found.
                for section in fasta_section:
                    if "Mycobacterium tuberculosis H37Rv|" in section.text:  # Ensure the section contains the correct FASTA sequence.
                        fasta_sequence = section.text.strip()  # Get the FASTA sequence and remove extra spaces.
                        filename = f'{path}/{gene}.fasta'  # Create the file path for saving the sequence.
                        with open(filename, 'w') as f:  # Open the file in write mode.
                            f.write(fasta_sequence)  # Write the FASTA sequence to the file.
                        fasta_sequence = fasta_sequence.split("\n")[1]  # Extract only the sequence part (ignoring the header).
                        df.loc[index, "fasta"] = fasta_sequence  # Add the sequence to the DataFrame.
            else:
                print(f"FASTA sequence not available")  # Log if no FASTA section was found.
        else:
            print(f"Gene information not found")  # Log if the request failed.
```

### Save Wild FASTA Sequence from Mycobrowser for Complete Wild Types

```python
save_fasta_sequence_wild(complete_wild_df, COMPLETE_WILD_FASTA_PATH) # Fetch and save FASTA sequences for complete wild types.

print(complete_wild_df[complete_wild_df["fasta"].isnull()]) # Log genes without FASTA sequences due to their rRNA type.
```
### *PS: There are two genes that do not have a FASTA sequence, because they are of rRNA type: `rrs` and `rrl`. So we will remove them.*

```python
# Remove rows for `rrs` and `rrl` genes that lack FASTA sequences.
complete_wild_df = complete_wild_df[complete_wild_df.gene != "rrs"]
complete_wild_df = complete_wild_df[complete_wild_df.gene != "rrl"]

complete_wild_df.head()

print(f"Dataset shape: {complete_wild_df.shape}")
print(f"Rows: {complete_wild_df.shape[0]}")
print(f"Columns: {complete_wild_df.shape[1]}")
complete_wild_df.describe()

complete_wild_df.to_csv(f"{CSV_PATH}fasta_complete_wild.csv", index=False, sep=';') # Save the updated DataFrame with FASTA sequences to a CSV file.
```

### Save Wild FASTA Sequence from Mycobrowser for Filtered Wild Types

```python
save_fasta_sequence_wild(wild_df, WILD_FASTA_PATH) # Fetch and save FASTA sequences for filtered wild types.

wild_df.head()
print(f"Dataset shape: {wild_df.shape}")
print(f"Rows: {wild_df.shape[0]}")
print(f"Columns: {wild_df.shape[1]}")
wild_df.describe()

wild_df.to_csv(f"{CSV_PATH}fasta_wild.csv", index=False, sep=';') # Save the updated DataFrame with FASTA sequences to a CSV file.
```

### Getting FASTA Sequence for Mutations

```python
variant_df.head()
print(f"Dataset shape: {variant_df.shape}")
print(f"Rows: {variant_df.shape[0]}")
print(f"Columns: {variant_df.shape[1]}")
variant_df.describe()
```

### Define Function to Mutate a FASTA Sequence Based on a Given Mutation

```python
def get_fasta_mutation(fasta_selvagem, mutation):
    position = int(mutation[3:-3])  # Extract the position of the mutation.
    amino_acid = fasta_selvagem[position-1]  # Get the original amino acid at the position.
    if mutation[:3] != AMINO_ACIDS[amino_acid]:  # Check if the amino acid matches the expected value.
        print(f"Error converting fasta sequence")  # Log an error if the amino acid does not match.
        return "ERROR: amino-acid is not the same as expected"
    fasta_mutated = list(fasta_selvagem)  # Convert the FASTA sequence to a list for mutation.
    fasta_mutated[position-1] = AMINO_ACIDS_REVERSE[mutation[-3:]]  # Replace the amino acid at the position.
    fasta_mutated = ''.join(fasta_mutated)  # Convert the mutated list back to a string.
    return fasta_mutated  # Return the mutated FASTA sequence.
```

### Define Function to Fetch and Save FASTA Sequences for Variants

```python
def save_fasta_sequence_variant(df, path):
    for index, row in df.iterrows():
        print(f"Saving FASTA sequence... ({index+1} from {df.shape[0]})")  # Log progress.
        wild_row = wild_df[wild_df['gene'] == row['gene']]  # Find the corresponding wild type row.
        if wild_row.empty:  # Check if the wild type gene is not found.
            print(f"Gene {row['gene']} not found in wild_df")  # Log a warning.
            continue  # Skip to the next row.
        wild_fasta = wild_row['fasta'].values[0]  # Get the FASTA sequence for the wild type.
        variant = row['variant'].split('.')[1]  # Extract the mutation from the variant column.
        mutated_fasta = get_fasta_mutation(wild_fasta, variant)  # Generate the mutated FASTA sequence.
        df.at[index, 'fasta'] = mutated_fasta  # Add the mutated sequence to the DataFrame.
        identifier = row['identifier']  # Get the variant identifier.
        fasta_content = f">Mycobacterium tuberculosis H37Rv|{identifier}|{variant}\n{mutated_fasta}"  # Create the FASTA header and sequence.
        with open(f"{path}/{row['variant']}.fasta", "w") as f:  # Open the file in write mode.
            f.write(fasta_content)  # Write the FASTA content to the file.
```

### Save Mutated FASTA Sequences for Variants

```python
save_fasta_sequence_variant(variant_df, VARIANT_FASTA_PATH) # Fetch and save FASTA sequences for variants.
variant_df.head()
print(f"Dataset shape: {variant_df.shape}")
print(f"Rows: {variant_df.shape[0]}")
print(f"Columns: {variant_df.shape[1]}")
variant_df.describe()
variant_df.to_csv(f"{CSV_PATH}fasta_variant.csv", index=False, sep=';')
```