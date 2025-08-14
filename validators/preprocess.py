# read fastas.csv and save into a df

import pandas as pd
import os

def main():
    try:
        identifyer = pd.read_csv("identifier.csv", sep=";")
        pdb_files = os.listdir("assets/pdbs/omegafold")
        for name in pdb_files:
            if name[6] == 'c':
                identifyer_name = name[:7]
                mutation = name[7:]
            else:
                identifyer_name = name[:6]
                mutation = name[6:]
            
            print(f"Identifier: {identifyer_name}, Mutation: {mutation}")
            gene = identifyer.loc[identifyer['identifier'] == identifyer_name, 'gene'].values
            print(f"Gene: {gene}")
            old_name = f"assets/pdbs/omegafold/{name}"
            
            # Remove [ ], ' from gene and mutation
            gene_cleaned = str(gene).replace("[", "").replace("]", "").replace("'", "")
            mutation_cleaned = mutation.replace("[", "").replace("]", "").replace("'", "")
            
            new_name = f"assets/pdbs/omegafold/{gene_cleaned}_{mutation_cleaned}"
            try:
                os.rename(old_name, new_name)
            except FileNotFoundError:
                print(f"File {old_name} not found. Skipping...")
            except Exception as e:
                print(f"Error renaming file {old_name}: {e}")
                
    except FileNotFoundError:
        print("identifyer.csv not found. Please ensure the file exists in the current directory.")

if __name__ == "__main__":
    main()