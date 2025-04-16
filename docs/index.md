<!-- ---
layout: default
title: Home
nav_order: 1
--- -->

# Welcome to the project documentation

Welcome to the official documentation for this project. This documentation is designed to help you understand, set up, and run the various scripts and tools included in this project. Whether you're a new user or an experienced developer, you'll find detailed guides and tutorials to assist you in every step of the way.

## Project Overview

This project is a comprehensive pipeline for processing and analyzing protein data. The project includes multiple preprocessing scripts, model generation tools, evaluating models fot those tools and helper functions to streamline your workflow. 

### Key Features

- **Preprocessing Scripts:** Tools for data cleaning, formatting, and analysis.
- **Model Generation:** Integration with various protein modeling tools like AlphaFold, SwissModel, Modeller, and more.
- **Model Evaluation:** Integration with various model evaluation tools like MolProbity and more.
- **Utilities and Helpers:** Additional scripts to manage and process data.

## Table of Contents

### Installation
- [Installation Guide](installation.md)

### Directory Structure
- [Directory Layout and Explanation](directory_structure.md)

### Code
- [Code Overview](code/overview.md)

#### Preprocessing Scripts
- [Preprocess Index](code/models/preprocess_index.md)
  - [Clean Data](code/preprocess/01_clean_data.md)
  - [PDB MycoBrowser Analysis](code/preprocess/02_pdb_mycobrowser_analysis.md)
  - [FASTA Sequence](code/preprocess/03_fasta_sequence.md)
  - [BLAST](code/preprocess/04_blast.md)
  - [Format PIR](code/preprocess/05_format_pir.md)
  - [Format Ali](code/preprocess/06_format_ali.md)


#### Model Generation
- [Model Index](code/models/model_index.md)
  - [SwissModel](code/models/01_swiss_model.md)
  - [Colab AlphaFold2](code/models/02_colab_alphafold2.md)
  - [Modeller](code/models/03_modeller.md)
  - [Phyre2](code/models/04_phyre2.md)
  - [I-TASSER](code/models/05_i_tasser.md)
  - [Rosetta](code/models/06_rosetta.md)
  - [AlphaFold3](code/models/07_alphafold3.md)

#### Helper Functions
- [Helper Functions](code/helpers/helper_functions.md)




### Data
- [Data](data.md)

### Additional Resources
- [References](references.md)

We hope you find this documentation helpful. If you have any questions or feedback, please don't hesitate to contact us.