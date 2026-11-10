import sys

# FASTQ 를 4줄씩 읽어 (이름, 서열, 품질) 튜플 리스트로 돌려준다
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records

# 위치별 평균 품질을 계산한다
# total[i] : i 번째 위치(0 부터 셈)의 품질 점수 합
# count[i] : i 번째 위치를 가진 read 의 개수 (read 길이가 다를 수 있으므로 따로 센다)
def qual_by_position(reads):
    total = []
    count = []
    for name, seq, qual in reads:          # 바깥 반복: read 하나씩
        for i in range(len(qual)):         # 안쪽 반복: 그 read 의 위치 하나씩
            if i == len(total):            # 지금까지 본 read 보다 길면 칸을 늘린다
                total.append(0)
                count.append(0)
            total[i] = total[i] + (ord(qual[i]) - 33)   # Phred+33
            count[i] = count[i] + 1

    means = []
    for i in range(len(total)):
        means.append(total[i] / count[i])
    return means

reads = read_fastq(sys.argv[1])
means = qual_by_position(reads)

# 위치는 FastQC 처럼 1 부터 출력한다
for i in range(len(means)):
    print(str(i + 1) + "\t" + str(round(means[i], 2)))
