# Swiss-Model Protein Structure Modeling Automation

---

## 1. Overview

### 1.1 Idea

This project is designed for **modeling protein structures** by generating **3D PDB files** from **FASTA sequences** using the **Swiss-Model** tool.

---

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

---

### 2.3 Installation

Install all dependencies running the following command in the root directory:

```sh
pip3 install --no-cache-dir -r requirements.txt
```


---

## 3. Running the Project

Run the modeling script using Docker:

```sh
SWISS_MODEL_TOKEN=<Swiss model token> python3 main.py
```

Replace <```Swiss model token```> with your Swiss model token.

---

## 4. Output

The output will be a directory named `results` containing the generated PDB files for each FASTA sequence provided in the `fasta.csv` file. Each PDB file will be named according to the gene and variant specified in the CSV.
