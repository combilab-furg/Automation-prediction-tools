<!-- ---
layout: default
title: Directory Structure
nav_order: 3
--- -->

# Directory Structure

**mestrado/**
- **Makefile**: Commands for installing requirements and enabling Jupyter notebook extensions.

**/mestrado/docs/**: 
- Directory intended for documentation files.

**/mestrado/results/**: 
- Directory intended for the results of your experiments and analyses.

**/mestrado/data/**: 
- Directory intended for data files used in the project.

  **/mestrado/data/pir/**:
  - Directory to store PIR format data files.

  **/mestrado/data/fasta/**: 
  - Directory to store FASTA format data files.
    - **/mestrado/data/fasta/wild/**: Wild type FASTA sequences.
    - **/mestrado/data/fasta/variant/**: Variant FASTA sequences.
    - **/mestrado/data/fasta/complete_wild/**: Complete wild-type FASTA sequences.

  **/mestrado/data/csv/**: 
  - Directory to store CSV files.

  **/mestrado/data/blast/**: 
  - Directory to store BLAST results.

  **/mestrado/data/pdb/**: 
  - Directory to store PDB (Protein Data Bank) files.
    - **/mestrado/data/pdb/colab_alphafold2/**: PDB files from Colab Alphafold2.
    - **/mestrado/data/pdb/swiss_model/**: PDB files from Swiss Model.
    - **/mestrado/data/pdb/alphafold3/**: PDB files from Alphafold3.
    - **/mestrado/data/pdb/modeller/**: PDB files from Modeller.
    - **/mestrado/data/pdb/rosetta/**: PDB files from Rosetta.
    - **/mestrado/data/pdb/phyre2/**: PDB files from Phyre2.
    - **/mestrado/data/pdb/blast/**: PDB files from BLAST.
    - **/mestrado/data/pdb/i_tasser/**: PDB files from I-TASSER.
  
  **/mestrado/data/saves/**:
  - Directory to store screenshot of saves evaluation.
    - **/mestrado/data/saves/colab_alphafold2/**: Screenshot of saves from Colab Alphafold2.
    - **/mestrado/data/saves/swiss_model/**: Screenshot of saves from Swiss Model.
    - **/mestrado/data/saves/alphafold3/**: Screenshot of saves from Alphafold3.
    - **/mestrado/data/saves/modeller/**: Screenshot of saves from Modeller.
    - **/mestrado/data/saves/rosetta/**: Screenshot of saves from Rosetta.
    - **/mestrado/data/saves/phyre2/**: Screenshot of saves from Phyre2.
    - **/mestrado/data/saves/i_tasser/**: Screenshot of saves from I-TASSER.
  
  **/mestrado/data/ali/**: 
  - Directory to store alignment files.

**/mestrado/src/**: 
- Directory containing source code.

  **/mestrado/src/preprocess/**: 
  - Directory for data preprocessing scripts.
    - **format_ali.py**: Script to format alignment files for Modeller.
    - **blast.ipynb**: Notebook to run BLAST and fetch PDB files.
    - **pdb_mycobrowser_analysis.ipynb**: Notebook for analyzing PDB data from Mycobrowser.
    - **format_pir.ipynb**: Notebook to format PIR files.
    - **clean_data.ipynb**: Notebook to clean datasets.
    - **fasta_sequence.ipynb**: Notebook to fetch FASTA sequences from Mycobrowser.

  **/mestrado/src/model/**: 
  - Directory for model scripts.
    - **colab_alphafold2.ipynb**: Notebook for Colab Alphafold2 processing.
    - **alphafold3.ipynb**: Instructions for using Alphafold3.
    - **swiss_model.ipynb**: Notebook for Swiss Model processing.
    - **modeller_model.py**: Script to process sequences with Modeller.
    - **rosetta.ipynb**: Notebook for Rosetta processing.
    - **phyre2.ipynb**: Instructions for using Phyre2.
    - **i_tasser.ipynb**: Notebook for I-TASSER processing.

  **/mestrado/src/helper/**: 
  - Directory for helper scripts.
    - **helper_functions.ipynb**: Notebook containing various helper functions.
    - **input/**: Directory for input helper files.
    - **output/**: Directory for output helper files.