import sys

if len(sys.argv) != 2:
    print("Usage: python count_agent.py <fasta_file>")
    sys.exit(1)

count = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith(">"):
            count += 1

print(count)

