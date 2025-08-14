import pandas as pd

molprobity = pd.read_csv("assets/results/molprobity.csv", sep=";")
qmean_disco = pd.read_csv("assets/results/qmean_disco.csv", sep=";")
qmean = pd.read_csv("assets/results/qmean.csv", sep=";")
saves = pd.read_csv("assets/results/saves.csv", sep=";")
voromqa = pd.read_csv("assets/results/voromqa.csv", sep=";")
# identifier_df = pd.read_csv("identifier.csv", sep=";")

merged_df = molprobity.merge(qmean_disco, on=['gene', 'variant', 'id', 'fasta', 'pdb', 'model'], how='outer')
merged_df = merged_df.merge(qmean, on=['gene', 'variant', 'id', 'fasta', 'pdb', 'model'], how='outer')
merged_df = merged_df.merge(saves, on=['gene', 'variant', 'id', 'fasta', 'pdb', 'model'], how='outer')
merged_df = merged_df.merge(voromqa, on=['gene', 'variant', 'id', 'fasta', 'pdb', 'model'], how='outer')
# merged_df = merged_df.merge(identifier_df, on="gene", how="left")
# remove lines with wild in variant column
# merged_df = merged_df[~merged_df['variant'].str.contains("wild", case=False, na=False)]

merged_df.to_csv("results.csv", sep=";", index=False)

print("Merged data saved to 'merged_data.csv'")


