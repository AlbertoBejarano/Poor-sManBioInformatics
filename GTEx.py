import pandas as pd
import time
import timeit
import os

# Retrieve data from GTEx Download (GTEx Analysis V8)
expression_link     = "https://storage.googleapis.com/gtex_analysis_v8/rna_seq_data/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz"
# expression_link     = 'Data/Input/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.csv'
annotations_link    = 'Data/Input/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'
GoI                 = 'Data/Input/Genes_of_Interest.csv'

# print(f'File Size is {round(os.stat(expression_link).st_size / (1024 * 1024),0)} MB', "\n")

GoI = open(GoI).read().split()
len_GoI = len(GoI)
print("\nSearching", len_GoI, "Genes of Interest:\n")

if len(GoI) % 2 != 0:
    GoI.append(" ")
split = int(len(GoI) / 2)
l1 = GoI[0:split]
l2 = GoI[split:]
for key, value in zip(l1, l2):
    print("{0:<20s} {1}".format(key, value))

time.sleep(2)

chunk_size = 100
batch_no = 1
GoI_found = 0
chunks = pd.DataFrame()
tic = timeit.default_timer()

for chunk in pd.read_csv(expression_link, sep='\t', chunksize=chunk_size):
    chunk = chunk[chunk['Description'].isin(GoI)]
    chunks = pd.concat([chunks, chunk], ignore_index=True)
    GoI_found += len(chunk)
    print("\n", GoI_found, "Genes of Interest found so far\n")
    print("\n", "Chunk number:", batch_no, "\n")
    print(chunk)
    batch_no += 1

print(chunks)

print("\n", "The file was split in", (batch_no-1), "chunks")
toc = timeit.default_timer()
print("\n", GoI_found, "Genes of Interest of", len_GoI, "have been found in", round(toc - tic, 2), "seconds")
chunks.to_csv('Data/Output/Output_GoI.tsv', sep='\t', index=False)
