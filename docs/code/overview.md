<!-- ---
layout: default
title: Code Overview
nav_order: 6
--- -->

# Project Overview

## Project Purpose

The primary aim of this project is to automate the process of generating and analyzing protein structure models using various bioinformatics tools. It integrates multiple computational methods and services, facilitating the comparison of these tools for accurate protein structure prediction.

## Key Functions

### Data Preprocessing

Before predicting the protein structures, various preprocessing steps are carried out:

- **Data Cleaning**: Ensures the datasets are formatted correctly and removes any invalid data.
- **Sequence Alignment Formatting**: Formats alignment files for specific tools like Modeller.
- **FASTA Sequence Extraction**: Extracts and processes FASTA sequences for both wild-type and variant sequences.

These preprocessing scripts ensure that the input data is correctly formatted and optimized for each modeling tool.

### Model Generation

We utilize several advanced bioinformatics tools and services to generate protein structure models from sequence data:

1. **Colab Alphafold2**:
   - Leverages the powerful Alphafold2 employed via Google Colab to predict protein structures from sequence data.

2. **Alphafold3**:
   - Utilizes Alphafold3 framework for protein modeling, further enhancing the predictive accuracy.

3. **Swiss Model**:
   - A web-based tool that automates the process of homology modeling, generating protein models based on sequence alignments with known structures.

4. **Modeller**:
   - Generates 3D structures by satisfaction of spatial restraints, derived from known homologous protein structures.

5. **Rosetta**:
   - Comprehensive suite for macromolecular modeling, predicting and designing protein structures, protein folding mechanisms, and protein-protein interactions.

6. **Phyre2**:
   - Web-based tool for protein structure prediction using homology modeling techniques, providing results via email.

7. **I-TASSER**:
   - An iterative threading assembly refinement method that generates full-length structural models from threading alignments and iterative fragment assembly simulations.


```
To-Do: Documentation about model evaluation
```

## Conclusion

By integrating these diverse bioinformatics tools into a single automated workflow, the project enables efficient protein structure prediction and robust comparative analysis. 