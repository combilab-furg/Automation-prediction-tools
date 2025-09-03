## 1. Overview

### 1.1 Idea

This project is designed for **Automation of the following protein 3D structure validation tools:**

* MolProbity
* SAVES (ERRAT and VERIFY3D)
* QMEAN and QMEANDisCo
* VoroMQA

We used Selenium to perform this process.

## 2. Setup

### 2.1 Create an virtual environment

To ensure a clean and isolated environment for the project, create a virtual environment. This step is crucial to avoid conflicts with other Python packages.

#### Linux / MacOS
```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows
```sh
python -m venv .venv
.\.venv\Scripts\activate
```

### 2.2 Data Preparation

To prepare the data for modeling, create a `fasta.csv` file in the `root` directory with the following structure:

| Column      | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `gene`      | The gene name or identifier.                                               |
| `variant`   | The variant type (e.g., wild or mutation).                                 |
| `fasta`     | The FASTA sequence of the protein.                                         |

#### Example:
`csv`
gene;variant;fasta
atpE;wild;MDPTIAAGALIGGGLIMAGGAIGAGIGDGVAGNALISGVARQPEAQGRLFTPFFITVGLVEAAYFINLAFMALFVFATPVK;
Rv0678;wild;VSVNDGVDQMGAEPDIMEFVEQMGGYFESRSLTRLAGRLLGWLLVCDPERQSSEELATALAASSGGISTNARMLIQFGFIERLAVAGDRRTYFRLRPNAFAAGERERIRAMAELQDLADVGLRALGDAPPQRSRRLREMRDLLAYMENVVSDALGRYSQRTGEDD;
ddn;ddn_Leu49Pro;MPKSPPRFLNSPLSDFFIKWMSRINTWMYRRNDGEGLGGTFQKIPVALPTTTGRKTGQPRVNPLYFLRDGGRVIVAASKGGAEKNPMWYLNLKANPKVQVQIKKEVLDLTARDATDEERAEYWPQLVTMYPSYQDYQSWTDRTIPIVVCEP;
`end`

You also need to create a folder at the following path: assets/pdbs/<model_name>, containing the resulting .PDB files. Here, <model_name> should correspond to the name of the tool used to generate the PDB file.

### 2.3 Installation

Install all dependencies running the following command in the root directory:

```sh
pip3 install --no-cache-dir -r requirements.txt
```

## 3. Running the Project

Run the modeling script using Docker:

```sh
python3 main.py
```

## 4. Output

The output will be a directory named `results` containing multiple csv files, one for each validation tool.
