# Automation-prediction-tools
This directory contains the code and data used during the development of my dissertation, which aimed to automate protein prediction tools to generate mutated proteins of Mycobacterium tuberculosis H37Rv, as well as to automate tools for validating the quality of the generated models.

This project involves bioinformatics preprocessing, modeling, and analysis. The scripts provided here help automate the process of obtaining protein models using various tools and validating them.

## Directory Structure

```
Makefile
data/
|-- pir/
|-- fasta/
|   |-- wild/
|   |-- variant/
|   |-- complete_wild/
|-- results/
|-- csv/
|-- blast/
|-- pdb/
|   |-- colab_alphafold2/
|   |-- swiss_model/
|   |-- alphafold3/
|   |-- modeller/
|   |-- rosetta/
|   |-- phyre2/
|   |-- blast/
|   |-- i_tasser/
|-- ali/
docs/
src/
|-- preprocess/
|   |-- 01_clean_data.ipynb
|   |-- 02_pdb_mycobrowser_analysis.ipynb
|   |-- 03_fasta_sequence.ipynb
|   |-- 04_blast.ipynb
|   |-- 05_format_pir.ipynb
|   |-- 06_format_ali.ipynb
|-- models/
|   |-- 01_swiss_model.ipynb
|   |-- 02_colab_alphafold2.ipynb
|   |-- 03_modeller.ipynb
|   |-- 04_phyre2.ipynb
|   |-- 05_i_tasser.ipynb
|   |-- 06_rosetta.ipynb
|   |-- 07_alphafold3.ipynb
|-- helper/
|   |-- helper_functions.ipynb
|-- validation/
|   |-- 01_result_dataframe.ipynb
|   |-- 02_saves.ipynb
|   |-- 03_molprobity.ipynb
```

## Setup

To install the necessary dependencies and setup the project, you need to run the following:

```sh
make install
```

This will install the necessary Python packages and tools required for running the scripts.

## Usage

### Preprocess

The preprocessing scripts are located in `src/preprocess/` and include:

- `01_clean_data.ipynb` - Cleans the input data and prepares datasets.
- `02_pdb_mycobrowser_analysis.ipynb` - Analyzes PDB information from MycoBrowser.
- `03_fasta_sequence.ipynb` - Retrieves FASTA sequences for wild and variant types.
- `04_blast.ipynb` - Performs BLAST to obtain homologous proteins.
- `05_format_pir.ipynb` - Formats PIR files.
- `06_format_ali.ipynb` - Formats ALI files.

To execute these scripts, navigate to the appropriate directory and run:

```sh
jupyter notebook <script_name>.ipynb
```

### Model

The modeling scripts are located in `src/model/` and include:

- `01_swiss_model.ipynb`
- `02_colab_alphafold2.ipynb`
- `03_modeller.ipynb`
- `04_phyre2.ipynb`
- `05_i_tasser.ipynb`
- `06_rosetta.ipynb`
- `07_alphafold3.ipynb`

To run these scripts, navigate to the appropriate directory and run:

```sh
jupyter notebook <script_name>.ipynb
```

### Helper

The helper functions are located in `src/helper/` and provide additional utilities used throughout the project.

## Results

All results, including models and analysis, are stored in the `data/results/` and respective directories for each modeling tool.

## Documentation
For more information, see the documentation in [here](docs/index.md).
