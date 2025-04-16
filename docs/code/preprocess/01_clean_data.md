<!-- ---
layout: default
title: Clean Data
parent: Preprocess Index
nav_order: 8
--- -->

# Clean Data

## Overview

This document provides a step-by-step guide for cleaning and preprocessing the protein sequence datasets. The primary goal of this process is to filter and merge datasets, remove duplicates, and prepare the data for further analysis and modeling.

## Input and Output

### Input

- `complete_dataset.csv`: Contains the complete dataset of the "Catalogue of Mutations in *Mycobacterium tuberculosis* Complex and Their Association with Drug Resistance," available on GitHub at: [GitHub Repository] (https://github.com/GTB-tbsequencing/mutation-catalogue-2023). The path to the file is: `Final Result Files/WHO-UCN-TB-2023.7-eng.xlsx`.
- `gene_identifier.csv`: Contains gene identifiers required for merging with the complete dataset.

### Output

- **`wild.csv`**: A CSV file containing the filtered and cleaned dataset for wild-type genes with missense variants correlated. It contains the following columns: `gene`, `identifier`, and `mycobrowser_url`.
- **`variant.csv`**: A CSV file containing the filtered and cleaned dataset for missense variants (proteins with mutations). The columns present in this dataset are: `gene`, `identifier`, and `variant`.
- **`complete_wild.csv`**: A CSV file containing the complete dataset for all wild-type genes with additional Mycobrowser URL links. The dataset contains the following columns: `gene`, `identifier`, and `mycobrowser_url`.
- **`complete_variant.csv`**: A CSV file containing the complete dataset for all genes and variants. The dataset contains the following columns: `gene`, `identifier`, `variant`, `effect`, and `final_confidence_grading`.

## Code Explanation

### Import Libraries and Install Dependencies

```python
import pandas as pd
```

### Define Global Variables

```python
CSV_PATH = "../../data/csv/"  # Path to CSV files
```

### Load Datasets into Dataframes

```python
data_df = pd.read_csv(f'{CSV_PATH}complete_dataset.csv', sep=';')
identifier_df = pd.read_csv(f'{CSV_PATH}gene_identifier.csv', sep=';')
```

### Preprocessing Datasets

```python
data_df.head()  # Display the first few rows of the dataset
print(f"Dataset shape: {data_df.shape}")  # Print the shape of the dataset
print(f"Rows: {data_df.shape[0]}")  # Print the number of rows
print(f"Columns: {data_df.shape[1]}")  # Print the number of columns
```

### Filter Wanted Columns

```python
columns = ['gene', 'variant', 'effect', 'FINAL CONFIDENCE GRADING']  # Define the columns to keep
data_df = data_df[columns]  # Filter the dataset to keep only the wanted columns
data_df.head()  # Display the first few rows of the filtered dataset
data_df.describe()  # Display summary statistics of the filtered dataset
```

We filter the dataset to retain only the relevant columns for our analysis and display the first few rows and summary statistics.

### Merge Identifiers with Data

```python
data_df = data_df.merge(identifier_df, on='gene', how='inner')  # Merge the dataframes on the 'gene' column
data_df.head()  # Display the first few rows of the merged dataset
print(f"Dataset shape: {data_df.shape}")  # Print the shape of the merged dataset
print(f"Rows: {data_df.shape[0]}")  # Print the number of rows in the merged dataset
print(f"Columns: {data_df.shape[1]}")  # Print the number of columns in the merged dataset
data_df.describe()  # Display summary statistics of the merged dataset
```

We merge the complete dataset with the gene identifier dataset based on the 'gene' column to create a combined dataset.

### Create Wild-Type Dataset

```python
complete_wild_df = data_df[['gene', 'identifier']].copy()  # Create a copy of the 'gene' and 'identifier' columns
complete_wild_df = complete_wild_df.drop_duplicates(subset='gene')  # Drop duplicate rows based on the 'gene' column
complete_wild_df['mycobrowser_url'] = 'https://mycobrowser.epfl.ch/genes/' + complete_wild_df['identifier']  # Add a new column with URLs
complete_wild_df.head()  # Display the first few rows of the complete wild dataset
print(f"Dataset shape: {complete_wild_df.shape}")  # Print the shape of the complete wild dataset
print(f"Rows: {complete_wild_df.shape[0]}")  # Print the number of rows in the complete wild dataset
print(f"Columns: {complete_wild_df.shape[1]}")  # Print the number of columns in the complete wild dataset
complete_wild_df.describe()  # Display summary statistics of the complete wild dataset
```

We create a dataset for all wild-type genes, remove duplicates, add a column with URLs, and display the summary statistics.

### Create Variant Dataset

```python
complete_variant_df = data_df[['gene', 'identifier', 'variant', 'effect', 'FINAL CONFIDENCE GRADING']].copy()  # Create a copy of the relevant columns
complete_variant_df = complete_variant_df.rename(columns={'FINAL CONFIDENCE GRADING': 'final_confidence_grading'})  # Rename a column
complete_variant_df.head()  # Display the first few rows of the complete variant dataset
print(f"Dataset shape: {complete_variant_df.shape}")  # Print the shape of the complete variant dataset
print(f"Rows: {complete_variant_df.shape[0]}")  # Print the number of rows in the complete variant dataset
print(f"Columns: {complete_variant_df.shape[1]}")  # Print the number of columns in the complete variant dataset
complete_variant_df.describe()  # Display summary statistics of the complete variant dataset
```

We create a dataset for all variants, rename a column for better readability, and display the summary statistics.

### Analyze Columns

```python
print(f"Unique genes: {data_df['gene'].unique()}")  # Print unique genes
print(f"Unique final confidence: {data_df['FINAL CONFIDENCE GRADING'].unique()}")  # Print unique final confidence gradings
print(f"Unique effect: {data_df['effect'].unique()}")  # Print unique effects
```

We print the unique values for genes, final confidence grading, and effects to understand the dataset better.

### Filter Specific Values

```python
data_df = data_df[(data_df['effect'] == 'missense_variant') & (data_df['FINAL CONFIDENCE GRADING'].isin(['2) Assoc w R - Interim', '1) Assoc w R']))]  # Filter the dataset based on specific conditions
```

We filter the dataset to include only rows with specific conditions for the effect and final confidence grading.

### Remove Duplicates

```python
duplicated_variant = data_df[data_df.duplicated(subset=['variant'], keep=False)]  # Identify duplicated variants
duplicated_variant  # Display duplicated variants
data_df = data_df.drop_duplicates(subset=['variant'])  # Remove duplicated variants
```

We identify and remove duplicated variants from the dataset.

```python
data_df.head()  # Display the first few rows of the dataset after removing duplicates
print(f"Dataset shape: {data_df.shape}")  # Print the shape of the dataset after removing duplicates
print(f"Rows: {data_df.shape[0]}")  # Print the number of rows in the dataset after removing duplicates
print(f"Columns: {data_df.shape[1]}")  # Print the number of columns in the dataset after removing duplicates
data_df.describe()  # Display summary statistics of the dataset after removing duplicates
print(f"Unique genes: {data_df['gene'].unique()}")  # Print unique genes in the dataset after removing duplicates
```

We display the summary statistics of the dataset after removing duplicates.

### Create Filtered Wild-Type Dataset

```python
wild_df = data_df[['gene', 'identifier']].copy()  # Create a copy of the 'gene' and 'identifier' columns
wild_df = wild_df.drop_duplicates(subset='gene')  # Drop duplicate rows based on the 'gene' column
wild_df['mycobrowser_url'] = 'https://mycobrowser.epfl.ch/genes/' + wild_df['identifier']  # Add a new column with URLs
wild_df.head()  # Display the first few rows of the filtered wild dataset
print(f"Dataset shape: {wild_df.shape}")  # Print the shape of the filtered wild dataset
print(f"Rows: {wild_df.shape[0]}")  # Print the number of rows in the filtered wild dataset
print(f"Columns: {wild_df.shape[1]}")  # Print the number of columns in the filtered wild dataset
wild_df.describe()  # Display summary statistics of the filtered wild dataset
```

We create a filtered dataset for wild-type genes and add a column with URLs.

### Create Variant Dataset

```python
variant_df = data_df[['gene', 'identifier', 'variant']].copy()  # Create a copy of the relevant columns
```

### Save Datasets

```python
wild_df.to_csv(f'{CSV_PATH}wild.csv', sep=';', index=False)  # Save the filtered wild dataset to a CSV file
variant_df.to_csv(f'{CSV_PATH}variant.csv', sep=';', index=False)  # Save the variant dataset to a CSV file
complete_wild_df.to_csv(f'{CSV_PATH}complete_wild.csv', sep=';', index=False)  # Save the complete wild dataset to a CSV file
complete_variant_df.to_csv(f'{CSV_PATH}complete_variant.csv', sep=';', index=False)  # Save the complete variant dataset to a CSV file
```

Finally, we save the cleaned and filtered datasets to CSV files for further analysis and modeling.