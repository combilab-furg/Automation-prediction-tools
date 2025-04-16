<!-- ---
layout: default
title: Modeller
parent: Model Index
nav_order: 16
--- -->

# Modeller

## Overview

This document provides a detailed step-by-step guide for using Modeller to predict protein structures and process variant sequences efficiently. The objective is to automate the modeling process, checking and updating statuses, filtering and processing variants in parallel, and updating the CSV file, ensuring a streamlined and effective workflow.

## Input

- `CSV_PATH`: The path to a CSV file containing variant sequences and related information.

## Output

- Updated `CSV_PATH`: The CSV file with updated statuses post-modeling.

## Import Dataset

We start by reading the dataset containing variant sequences and related information into a DataFrame.

```python
variant_df = pd.read_csv(CSV_PATH, sep=';')
```

## Update Modeller Status

We update the status of each variant to check if it has already been processed by Modeller.

```python
variant_df = update_status(variant_df, 'modeller')
```

## Print Total Count and Status

Print the total count of rows and the distribution of the `modeller` status.

```python
print(f"Total count: {len(variant_df)}")
print(variant_df['modeller'].value_counts())
input("\nPress Enter to continue...")
```

## Filter Not Concluded

Filter the rows where the `modeller` status is 'not_concluded' to identify the variants that need processing.

```python
not_concluded_df = variant_df[variant_df['modeller'] == 'not_concluded']
```

## Run Parallel Processing

Apply the `process_variant` function in parallel to process the filtered variants that have not been concluded.

```python
not_concluded_df = not_concluded_df.parallel_apply(process_variant, axis=1)
input()
```

## Update and Save CSV

Update the original DataFrame with the processed rows and save the updated DataFrame back to the CSV file.

```python
variant_df.update(not_concluded_df)
variant_df.to_csv(CSV_PATH, sep=';', index=False)
```

## Print Final Counts and Status

Print the final total count of rows and the distribution of the `modeller` status after processing.

```python
print(f"\n\nTotal count: {len(variant_df)}")
print(variant_df['modeller'].value_counts())
```