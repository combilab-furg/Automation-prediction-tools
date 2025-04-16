<!-- ---
layout: default
title: Colab Alphafold2
parent: Model Index
nav_order: 15
--- -->

# Colab Alphafold2

## Overview

This document provides a comprehensive guide for batch processing of protein structure predictions using Colab Alphafold2. It includes steps to set up the environment, process each sequence batch, and save the results.

## Input

- `fasta_variant.csv`: Contains variant information and fasta sequences.
- `colab_alphafold2`: Folder to save results and intermediate files.

## Output

- A .zip file containing all .pdb files generated.
- Updated `fasta_variant.csv` with processing status.
  
## How to Run

1. Ensure that the `notebook`, `fasta_variant.csv`, and `colab_alphafold2` folder are the only files in the directory.
2. Select `Runtime` on the top menu and then `Run all`.

## Code Explanation

### Connect with Google Drive

We mount Google Drive to store and retrieve files.

```python
import glob
import os
from google.colab import drive

drive.mount('/content/drive', force_remount=True)
filename = 'AlphaFold2.ipynb'
drive_root = '/content/drive/MyDrive/'
pattern = drive_root + '**/' + filename
file_list = glob.glob(pattern, recursive=True)
notebook_dir = os.path.dirname(file_list[0])
os.chdir(notebook_dir)
print(f"Add the input files on {notebook_dir}")
for filename in os.listdir():
    if filename != "fasta_variant.csv" and filename != "colab_alphafold2":
        file_path = os.path.join(notebook_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                !rm -rf "{file_path}"
        except Exception as e:
            print(f"Failed to delete {filename}: {e}")
```

### Setup Environment

We set up the necessary environment by installing required dependencies.

```python
%%time
!pip install --upgrade pandas
!pip install pandarallel -U
import os
import pandas as pd
import shutil
from google.colab import files

from sys import version_info
import re
import hashlib
import random

PYTHON_VERSION = f"{version_info.major}.{version_info.minor}"

if not os.path.isfile("COLABFOLD_READY"):
    print("installing colabfold...")
    os.system("pip install -q --no-warn-conflicts 'colabfold[alphafold-minus-jax] @ git+https://github.com/sokrypton/ColabFold'")
    if os.environ.get('TPU_NAME', False) != False:
        os.system("pip uninstall -y jax jaxlib")
        os.system("pip install --no-warn-conflicts --upgrade dm-haiku==0.0.10 'jax[cuda12_pip]'==0.3.25 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html")
    os.system("ln -s /usr/local/lib/python3.*/dist-packages/colabfold colabfold")
    os.system("ln -s /usr/local/lib/python3.*/dist-packages/alphafold alphafold")
    os.system("touch COLABFOLD_READY")

if not os.path.isfile("CONDA_READY"):
    print("installing conda...")
    os.system("wget -qnc https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh")
    os.system("bash Miniforge3-Linux-x86_64.sh -bfp /usr/local")
    os.system("mamba config --set auto_update_conda false")
    os.system("touch CONDA_READY")

if not os.path.isfile("HH_READY") and not os.path.isfile("AMBER_READY"):
    print("installing hhsuite and amber...")
    os.system(f"mamba install -y -c conda-forge -c bioconda kalign2=2.04 hhsuite=3.3.0 openmm=7.7.0 python='{PYTHON_VERSION}' pdbfixer")
    os.system("touch HH_READY")
    os.system("touch AMBER_READY")
else:
    if not os.path.isfile("HH_READY"):
        print("installing hhsuite...")
        os.system(f"mamba install -y -c conda-forge -c bioconda kalign2=2.04 hhsuite=3.3.0 python='{PYTHON_VERSION}'")
        os.system("touch HH_READY")
    if not os.path.isfile("AMBER_READY"):
        print("installing amber...")
        os.system(f"mamba install -y -c conda-forge openmm=7.7.0 python='{PYTHON_VERSION}' pdbfixer")
        os.system("touch AMBER_READY")
```

### Load Dataset

We load the dataset containing variant and sequence information.

```python
variant_df = pd.read_csv('fasta_variant.csv', sep=';')
```

### Check and Update Status

Functions to check if the PDB file already exists for each variant and update the status in the dataset.

```python
def check_and_update_status(row):
    variant = row["variant"]
    filename = variant.replace('_p.', '_')
    file_path = f"{PDB_PATH}/{filename}.pdb"
    if os.path.isfile(file_path) or row["colab_alphafold2"] == 'concluded':
        return 'concluded'
    return 'not_concluded'

def update_colab_alphafold_status(df):
    if 'colab_alphafold2' not in df.columns:
        df['colab_alphafold2'] = 'not_concluded'
    df['colab_alphafold2'] = df.apply(check_and_update_status, axis=1)
    print("Status updated based on existing files")
    return df
```

### Run Colab Alphafold2

We set up the functions needed to run Colab Alphafold2 for each batch of sequences.

```python
def add_hash(x, y):
    return x + "_" + hashlib.sha1(y.encode()).hexdigest()[:5]

def check(folder):
    if os.path.exists(folder):
        return False
    else:
        return True

def create_repository(name, sequence):
    python_version = f"{version_info.major}.{version_info.minor}"
    query_sequence = sequence
    name = name
    num_relax = 0
    template_mode = "pdb100"
    use_amber = num_relax > 0

    query_sequence = "".join(query_sequence.split())

    if not check(name):
        n = 0
        while not check(f"{name}_{n}"): n += 1
        name = f"{name}_{n}"
    os.makedirs(name, exist_ok=True)
    queries_path = os.path.join(name, f"{name}.csv")
    with open(queries_path, "w") as text_file:
        text_file.write(f"id,sequence\n{name},{query_sequence}")

def create_a3m_file(name, sequence):
    a3m_file = os.path.join(name, f"{name}.single_sequence.a3m")
    with open(a3m_file, "w") as text_file:
        text_file.write(">1\n%s" % sequence)

def prediction_callback(protein_obj, length, prediction_result, input_features, mode):
    model_name, relaxed = mode

def delete_folder(folder_name):
    if os.path.exists(folder_name):
        try:
            shutil.rmtree(folder_name)
            print(f"Folder '{folder_name}' deleted successfully.")
        except OSError as e:
            print(f"Error deleting folder '{folder_name}': {e}")
    else:
        print(f"Folder '{folder_name}' does not exist.")

def run_colab_alphafold2(name, sequence):
    filename = name.replace('_p.', '_')
    basejobname = "".join(name.split())
    basejobname = re.sub(r'\W+', '', basejobname)
    name = add_hash(basejobname, sequence)
    create_repository(name, sequence)
    create_a3m_file(name, sequence)
    queries_path = os.path.join(name, f"{name}.csv")
    python_version = f'{sys.version_info.major}.{sys.version_info.minor}'
    if f"/usr/local/lib/python{python_version}/site-packages/" not in sys.path:
        sys.path.insert(0, f"/usr/local/lib/python{python_version}/site-packages/")
    queries, is_complex = get_queries(queries_path)
    model_type = set_model_type(is_complex, "auto")
    use_cluster_profile = not ("multimer" in model_type and max_msa is not None)
    download_alphafold_params(model_type, Path("."))
    results = run(
        queries=queries,
        result_dir=name,
        use_templates=True,
        custom_template_path=None,
        num_relax=0,
        msa_mode="mmseqs2_uniref_env",
        model_type=model_type,
        num_models=1,
        num_recycles=num_recycles,
        relax_max_iterations=relax_max_iterations,
        recycle_early_stop_tolerance=recycle_early_stop_tolerance,
        num_seeds=num_seeds,
        use_dropout=use_dropout,
        model_order=[1],
        is_complex=is_complex,
        data_dir=Path("."),
        keep_existing_results=False,
        rank_by="auto",
        pair_mode=pair_mode,
        pairing_strategy=pairing_strategy,
        stop_at_score=float(100),
        prediction_callback=prediction_callback,
        dpi=dpi,
        zip_results=False,
        save_all=save_all,
        max_msa=max_msa,
        use_cluster_profile=use_cluster_profile,
        input_features_callback=None,
        save_recycles=save_recycles,
        user_agent="colabfold/google-colab-main",
        calc_extra_ptm=calc_extra_ptm,
    )
    pdb_files = [f for f in os.listdir(name) if f.endswith('.pdb')]
    if not pdb_files:
        print(f"No .pdb files found in {name}")
        return
    pdb_file = pdb_files[0]
    pdb_file_path = os.path.join(name, pdb_file)
    destination_path = os.path.join(PDB_PATH, filename + ".pdb")
    os.rename(pdb_file_path, destination_path)
    # files.download(destination_path)
    delete_folder(name)
    print(f"Model prediction saved to {destination_path}")
```

### Running the Batch

We execute the script to process the sequences in batches and update the dataframe.

```python
PDB_PATH = "colab_alphafold2"
if not os.path.exists(PDB_PATH):
    os.makedirs(PDB_PATH)
variant_df = pd.read_csv('fasta_variant.csv', sep=';')
variant_df = update_colab_alphafold_status(variant_df)
variant_df.head()

variant_df['colab_alphafold2'].value_counts()
not_concluded_df = variant_df[variant_df['colab_alphafold2'] == 'not_concluded']
for i, (index, row) in enumerate(not_concluded_df.iterrows()):
    print(f"Processing {row['variant']} ------- {i+1} of {len(not_concluded_df)}")
    run_colab_alphafold2(row['variant'], row['fasta'])
```

### Save and Download Results

We zip the results and download the final output files.

```python
!zip -r colab_alphafold2.zip colab_alphafold2
files.download("colab_alphafold2.zip")
variant_df.to_csv('variant_df.csv', index=False, sep=';')
files.download('variant_df.csv')
```