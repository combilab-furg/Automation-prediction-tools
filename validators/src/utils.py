import os
import numpy as np
import pandas as pd
import logging

from constants import FASTA_FILE, PDBS_PATH, RESULTS_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("saves.log"),
        logging.StreamHandler()
    ]
)

def get_models() -> list[str]:
    return [
        folder
        for folder in os.listdir(PDBS_PATH)
        if os.path.isdir(os.path.join(PDBS_PATH, folder))
    ]


def load_df(validator: str) -> pd.DataFrame:
    result_file = f"{RESULTS_PATH}/{validator}.csv"
    result_df = pd.read_csv(result_file, sep=";") if os.path.exists(result_file) else None
    df = pd.read_csv(FASTA_FILE, sep=";")
    models = get_models()
    all_rows = []

    for model in models:
        for _, row in df.iterrows():
            variant = row["variant"]
            gene = row["gene"]
            id_ = gene if variant == "wild" else variant
            if (
                result_df is not None
                and not result_df.loc[
                    (result_df["id"] == id_) & 
                    (result_df["model"] == model) & 
                    result_df["pdb"].notna() & 
                    (result_df[validator] == "ok")
                ].empty
            ):
                row_data = result_df.loc[
                    (result_df["id"] == id_) & (result_df["model"] == model)
                ].iloc[0].to_dict()
            else:
                file_name = f"{id_}.pdb"
                file_path = os.path.join(PDBS_PATH, model, file_name)
                pdb_path = file_path if os.path.exists(file_path) else np.nan
                row_data = {
                    "gene": gene,
                    "variant": variant,
                    "id": id_,
                    "fasta": row["fasta"],
                    "pdb": pdb_path,
                    "model": model,
                    validator: np.nan,
                }
                if result_df is not None:
                    for col in result_df.columns:
                        if col not in row_data:
                            row_data[col] = np.nan
            all_rows.append(row_data)
    updated_df = pd.DataFrame(all_rows)
    os.makedirs(RESULTS_PATH, exist_ok=True)
    updated_df.to_csv(result_file, sep=";", index=False)
    logging.info("[SUCCESS] - PDB paths updated.")
    return updated_df

def filter_df(df,validator) -> pd.DataFrame:
    filtered_df = df[df[validator] != "ok"]
    filtered_df = filtered_df[filtered_df["pdb"].notna()]
    filtered_df[["model", "variant", "pdb"]] = filtered_df[["model", "variant", "pdb"]].astype(str)
    return filtered_df