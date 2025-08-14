# FASTA Sequence Processing Project

## Overview

This project processes **wild-type** and **variant** datasets to generate **FASTA sequences** and save them into CSV files. It includes functionality to fetch wild-type FASTA sequences from **MycoBrowser** and generate mutated FASTA sequences for variants.

---
## Setup

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Dependencies**: Install the required Python libraries using:

```bash
pip install -r @requirements.txt@
```

---

## Workflow

### 1. Data Preparation

- **Input Files**:
  - `mutations-raw.xlsx`: Raw mutation data.
  - `identifier.csv`: Gene identifiers and their corresponding MycoBrowser URLs.

- **Output Files**:
  - `wild.csv`: Contains wild-type genes and their FASTA sequences.
  - `variant.csv`: Contains variant genes and their mutated FASTA sequences.

### 2. Data Cleaning

- Use `src/01_clean_up.ipynb` to:
  - Filter and clean the raw mutation data.
  - Merge gene identifiers from @identifier.csv@.
  - Create separate datasets for wild-type and variant genes.

### 3. FASTA Sequence Generation

- Use `src/02_fasta_sequence.ipynb` to:
  - Fetch wild-type FASTA sequences from MycoBrowser.
  - Generate mutated FASTA sequences for variants.

---
