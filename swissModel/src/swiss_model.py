import time
import pandas as pd
import os
import requests
import gzip
import logging
from datetime import datetime

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[logging.StreamHandler()],
)

RESULTS_PATH = "results"
FASTA_FILE = "fastas.csv"
MODEL = "swiss_model"
SWISS_MODEL_URL = "https://swissmodel.expasy.org/automodel"

def start_modeling(swiss_model_token, title, fasta):
	response = requests.post(
		SWISS_MODEL_URL,
		headers={"Authorization": f"Token {swiss_model_token}"},
		json={"target_sequences": fasta, "project_title": title},
	)
	return response.json().get("project_id")

def wait_modeling(swiss_model_token, project_id):
	while True:
		response = requests.get(
			f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
			headers={"Authorization": f"Token {swiss_model_token}"},
		)
		status = response.json().get("status", "UNKNOWN")
		if status in ["COMPLETED", "FAILED"]:
			break
		time.sleep(10)
	if status == "COMPLETED":
		return response.json().get("models", [])[0]
	else:
		logging.error("Modeling failed.")
		return None

def download_model(gene, variant, model):
	url = model["coordinates_url"]
	response = requests.get(url)
	protein_id = gene if variant == "wild" else variant
	if response.status_code == 200:
		pdb_gz_path = os.path.join(RESULTS_PATH, f"{protein_id}.pdb.gz")
		pdb_path = os.path.join(RESULTS_PATH, f"{protein_id}.pdb")
		with open(pdb_gz_path, "wb") as file:
			file.write(response.content)
		with gzip.open(pdb_gz_path, "rb") as gz_file:
			with open(pdb_path, "wb") as extracted_file:
				extracted_file.write(gz_file.read())
		os.remove(pdb_gz_path)
	else:
		logging.error("Failed to download PDB file for %s. Status code: %d", variant, response.status_code)

def get_pdb(gene, variant, fasta):
	swiss_model_token = os.getenv("SWISS_MODEL_TOKEN")
	try:
		project_id = start_modeling(swiss_model_token, variant, fasta)
		if project_id:
			model = wait_modeling(swiss_model_token, project_id)
			if model:
				download_model(gene, variant, model)
	except Exception as e:
		logging.error("Failed to get PDB for %s. Error: %s", variant, e)

def get_pdbs():
	start_time = datetime.now()
	df = pd.read_csv(FASTA_FILE, sep=";")
	logging.info("Starting PDB generation.")
	if not os.path.exists(RESULTS_PATH):
		os.makedirs(RESULTS_PATH)
		logging.info("Created results directory: %s", RESULTS_PATH)
	if MODEL not in df.columns:
		df[MODEL] = "Pending"
		logging.info("Added MODEL column to DataFrame.")
	remaining_df = df[df[MODEL] != "Completed"]
	logging.info("Found %d completed entries. Processing %d remaining entries.", len(df)-len(remaining_df), len(remaining_df))
	if not remaining_df.empty:
		for counter, (index, row) in enumerate(remaining_df.iterrows(), start=1):
			logging.info("Processing entry %d of %d: gene=%s, variant=%s", counter, len(remaining_df), row["gene"], row["variant"])
			get_pdb(row["gene"], row["variant"], row["fasta"])
			logging.info("Completed modeling for gene=%s, variant=%s.", row["gene"], row["variant"])
			df.at[index, MODEL] = "Completed"
			df.to_csv(FASTA_FILE, sep=";", index=False)  
	else:
		logging.warning("No models to process.")
	duration = (datetime.now() - start_time).total_seconds()
	logging.info("PDB generation completed in %.2f seconds.", duration)