<!-- ---
layout: default
title: Phyre2
parent: Model Index
nav_order: 17
--- -->

# Phyre2

## Overview

This document provides a detailed step-by-step guide for using Phyre2 for batch processing of multiple protein structure predictions. The goal is to streamline the workflow of submitting sequences, generating zip files of results, and extracting PDB files efficiently.

## Input

- FASTA formatted sequences for batch processing
- A `fasta_variant.csv` file for sequence and variant information

## Output

- Zip files containing prediction results from Phyre2
- Extracted PDB files from the zip file
- Updated `fasta_variant.csv` with paths to PDB files

## Steps Explanation

### Log In to Phyre2

1. Visit the [Phyre2 website](http://www.sbg.bio.ic.ac.uk/phyre2/html/page.cgi?id=index).
2. Log in using your Phyre2 account credentials. If you don’t have an account, create one by following the registration steps.

### Access Advanced Tools

1. Once logged in, navigate to the **Advanced Tools** section.
2. Select the **Batch Processing** option to proceed.

### Submit Sequences for Batch Processing

1. Prepare your sequences in FASTA format.
2. Submit sequences in batches of up to 100 at a time.
   - Use a provided helper script for automating the submission process if dealing with numerous sequences.

### Generate Zip Files

1. Upon completion of batch processing, an option to generate a zip file will appear.
2. Select this option, and an email with the download link will be sent to you.

### Download Zip File

1. Access your email and click the provided link to download the zip file containing the results.

### Extract PDB Files

1. Use a helper function to extract PDB files from the downloaded zip file.
   - This function extracts the PDB files, renames them according to gene and variant, and updates the CSV file with the new paths.

### Update CSV File

1. The helper function will update the `fasta_variant.csv` file, annotating each sequence with the path to its corresponding PDB file.