<!-- ---
layout: default
title: Alphafold3
parent: Model Index
nav_order: 20
--- -->

# AlphaFold3

## Overview

This document details the step-by-step procedure for using AlphaFold3 with the Combilab-furg AutoFold project for protein modeling. The objective is to automate the modeling process for a set of variant sequences efficiently.

### Input

- A list of variant sequences (384 variants in this case)

### Output

- Modeled protein structures from AlphaFold3

## Steps Explanation

### Clone Combilab-furg AutoFold Repository

1. Visit the [Combilab-furg AutoFold GitHub repository](https://github.com/combilab-furg/AutoFold).
2. Clone the repository to your local machine using Git.

### Prepare Variant Sequences

1. Ensure all 384 variant sequences are prepared in the required format as specified by the AutoFold project.
2. Verify that the sequences are correctly formatted and ready for submission.

### Run AutoFold for Modeling

1. Follow the instructions provided in the AutoFold repository to run the modeling on your variant sequences.
2. Execute the automation script to process all the sequences through AlphaFold3.

### Retrieve Modeled Structures

1. After the modeling process is complete, retrieve the generated protein structures.
2. Organize and store the modeled structures for further analysis and use.