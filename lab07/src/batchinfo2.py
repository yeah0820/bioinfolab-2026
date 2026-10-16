#모듈 이

import sys
import os
from fasta import read_fasta, length_stats, gc_content

folder = sys.argv[1]
outfile = sys.argv[2]

with open(outfile, "w") as out:
    out.write("filename\tcount\ttotal\tmean_gc\n")
    for filename in os.listdir(folder):
        if filename.endswith(".fasta"):
            path = os.path.join(folder, filename)
            seqs = read_fasta(path)
            stats = length_stats(seqs)
            gc_list = [gc_content(seq) for seq in seqs.values()]
            mean_gc = round(sum(gc_list) / len(gc_list), 3)
            out.write(f"{filename}\t{stats['count']}\t{stats['total']}\t{mean_gc}\n")

print("저장 완료:", outfile)