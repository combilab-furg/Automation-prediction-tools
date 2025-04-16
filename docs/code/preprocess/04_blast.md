<!-- ---
layout: default
title: BLAST Sequence Analysis
parent: Preprocess Index
nav_order: 11
--- -->

# BLAST Sequence Analysis

## Overview

This document guides you through generating and analyzing FASTA sequences for BLAST against the PDB database using Python libraries such as pandas for data manipulation, requests for HTTP requests, and Bio.Blast for BLAST operations. The process involves loading the dataset, retrieving FASTA sequences, submitting sequences to BLAST, downloading PDB files, and saving the results to CSV files.

## Input

- `fasta_wild.csv`: A CSV file containing wild-type genes and their sequences.

## Output

- PDB files: Downloaded PDB files for each gene.
- BLAST XML results: XML files containing the BLAST results for each gene.
- `fasta_wild.csv`: Updated CSV file with the status of the BLAST process.

### Import Libraries and Load Dependencies

```python
import pandas as pd  # Importing pandas for data manipulation
import requests  # Importing requests for making HTTP requests
import os  # Importing os for file and directory management
from Bio.Blast import NCBIWWW  # Importing NCBIWWW for BLAST operations
import re  # Importing re for regular expression operations

from pandarallel import pandarallel  # Importing pandarallel for parallel processing
pandarallel.initialize(progress_bar=True)  # Initializing pandarallel with a progress bar
```

### Define Global Variables

```python
CSV_PATH = "../../data/csv/"  # Path to the directory containing CSV files
PDB_PATH = "../../data/pdb/blast/"  # Path to save downloaded PDB files
FASTA_PATH = '../../data/fasta/wild'  # Path to the directory containing FASTA files
BLAST_PATH = "../../data/blast"  # Path to save BLAST results
```

### Load Dataset

```python
wild_df = pd.read_csv(f'{CSV_PATH}fasta_wild.csv', sep=';')
wild_df.head()
```

### Define Function to Retrieve FASTA Sequence

```python
def get_fasta(gene):  # Function to retrieve the FASTA sequence for a given gene
    fasta_file = os.path.join(FASTA_PATH, f'{gene}.fasta')  # Constructing the file path for the FASTA file
    if os.path.isfile(fasta_file):  # Checking if the file exists
        with open(fasta_file, 'r') as file:  # Opening the file in read mode
            fasta = file.read()  # Reading the file content
            return fasta  # Returning the FASTA sequence
    else:
        print(f'File {fasta_file} does not exist.')
```

### Filter Dataset and Initialize FASTA Sequences

```python
wild_df.head()

fasta_sequences = {} # Initializing a dictionary to store FASTA sequences
filtered_df = wild_df[wild_df['blast'] == 'not_concluded'] # Filtering rows where the blast status is 'not_concluded'
for index, row in filtered_df.iterrows(): # Iterating over the filtered rows
    gene = row['gene']  # Extracting the gene name
    fasta = get_fasta(gene)  # Retrieving the FASTA sequence for the gene
    fasta_sequences[gene] = fasta  # Storing the sequence in the dictionary

print(fasta_sequences) # Printing the dictionary of FASTA sequences
len(fasta_sequences) # Getting the number of FASTA sequences
```

### Submit Sequences to BLAST and Download PDB Files

```python
for gene, fasta in fasta_sequences.items(): # Iterating over the FASTA sequences
    print(f"Submitting Sequence from gene {gene} to BLAST...")  # Logging the BLAST submission
    result_handle = NCBIWWW.qblast("blastp", "pdb", fasta)  # Submitting the sequence to BLAST (protein to PDB database)

    blast_result = result_handle.read()  # Reading the BLAST result
    result_handle.close()  # Closing the result handle

    pdb_ids = re.findall(r'<Hit_id>pdb\|(\w+)\|', blast_result)  # Extracting PDB IDs from the result using regex
    download_successful = False  # Initializing a flag for download success

    for pdb_id in pdb_ids:  # Iterating over the extracted PDB IDs
        pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"  # Constructing the URL for the PDB file
        response = requests.get(pdb_url)  # Sending a GET request to download the PDB file

        if response.status_code == 200:  # Checking if the download was successful
            output_file = os.path.join(PDB_PATH, f"{gene}.pdb")  # Constructing the output file path
            with open(output_file, "wb") as out:  # Opening the file in write-binary mode
                out.write(response.content)  # Writing the downloaded content to the file
            print(f"Downloaded {gene}.pdb")  # Logging the successful download
            wild_df.loc[wild_df['gene'] == gene, 'blast'] = 'concluded'  # Updating the blast status in the DataFrame
            download_successful = True  # Updating the flag
            break  # Exiting the loop after a successful download
        else:
            print(f"Failed to download {pdb_id}.pdb for gene {gene}")

    if not download_successful:
        print(f"Failed to download any PDB file for gene {gene}")
        wild_df.loc[wild_df['gene'] == gene, 'blast'] = 'error'  # Updating the blast status in the DataFrame
```

### Save BLAST Results

```python
output_file = os.path.join(BLAST_PATH, f"{gene}.xml") # Constructing the output file path for the BLAST result
with open(output_file, "w") as out: # Opening the file in write mode
    out.write(blast_result)  # Writing the BLAST result to the file
print("BLAST submissions completed!")
```

ERROR on [tlyA, rpsL]

For those two cases, we downloaded manually