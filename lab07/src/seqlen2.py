import sys
from fasta import read_fasta

seqs = read_fasta(sys.argv[1])
for name, seq in seqs.items():
    print(name, len(seq))