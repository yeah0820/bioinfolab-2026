"""FASTA 파일의 서열 개수를 출력한다."""
import os
import sys

# lab07/src 의 fasta 모듈을 불러오기 위해 경로를 추가한다
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "..", "..", "lab07", "src"))
from fasta import read_fasta

if len(sys.argv) != 2:
    print("Usage: python3 count_agent2.py <fasta_file>")
    sys.exit(1)

seqs = read_fasta(sys.argv[1])
print(len(seqs))
