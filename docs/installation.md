<!-- ---
layout: default
title: Installation Guide
nav_order: 2
--- -->

# Installation Guide

Welcome to the installation guide for the Mestrado project. This guide will take you through the steps required to set up the environment and install all necessary dependencies to run the project, including Modeller.

## Requirements

Before we start with the installation, ensure you have the following software installed on your machine:

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Homebrew (for macOS users)](https://brew.sh/)
- [Modeller](https://salilab.org/modeller/)

## Step-by-Step Installation Guide

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone \<Add git URL here\>
cd mestrado
```

### 2. Set Up a Virtual Environment
We highly recommend using a virtual environment to isolate dependencies, for that run the following commands:
```bash
python3 -m venv .venv
source .venv/bin/activate  
```
On Windows, use `.venv\Scripts\activate` to activate

### 3. Install Dependencies
Install the required main dependencies running the following command:
```bash
make install
```

### 4. Install Modeller
You need to install Modeller manually as it is not available via pip. You can find the step by step on [modeller instalation](https://salilab.org/modeller/download_installation.html)


### 5. Install Jupyter Notebook Extensions
Enable Jupyter Notebook extensions for better functionality:
```bash
jupyter nbextension enable --py widgetsnbextension
jupyter nbextension install --py widgetsnbextension
```

### Conclusion

After install all the extensions and dependencies, you are ready to start using the project.
You can now proceed to explore the various scripts and functionalities provided by the project.