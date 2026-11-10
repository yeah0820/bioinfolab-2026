import sys

# FASTQ 를 4줄씩 읽어 (이름, 서열, 품질) 튜플 리스트로 돌려준다
# 이름은 헤더의 첫 단어만 쓴다 (lab07 read_fasta 와 같은 방식)
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:].split()[0]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records

# GC 비율을 0과 1 사이의 수로 돌려준다 (lab07 fasta.py 의 gc_content 와 같은 기준)
# 소문자도 세도록 대문자로 바꾼 뒤 센다. N 같은 문자는 길이에만 들어간다.
def gc_ratio(seq):
    if len(seq) == 0:
        return 0.0
    gc = 0
    for base in seq.upper():          # 안쪽 반복 1: 서열 글자 하나씩
        if base == "G" or base == "C":
            gc = gc + 1
    return gc / len(seq)

# 품질 문자열의 평균 Phred 점수를 돌려준다 (Phred+33)
def mean_quality(qual):
    if len(qual) == 0:
        return 0.0
    total = 0
    for ch in qual:                   # 안쪽 반복 2: 품질 글자 하나씩
        total = total + (ord(ch) - 33)
    return total / len(qual)

# 리스트의 평균
def average(values):
    return sum(values) / len(values)

# GC 가 극단적인 read 묶음과 전체 평균 품질을 비교해 stderr 로 출력한다
# (stdout 은 TSV 결과 전용이므로 > 로 저장해도 비교 결과가 섞이지 않는다)
def report_extremes(results, n=10):
    err = sys.stderr
    n = min(n, len(results))
    by_gc = sorted(results, key=lambda r: r[1])   # GC 비율 오름차순 정렬
    low = by_gc[:n]                               # GC 가 가장 낮은 n 개
    high = by_gc[::-1][:n]                        # GC 가 가장 높은 n 개 (높은 순)
    all_q = average([r[2] for r in results])

    print("", file=err)
    print("== GC 극단 read 와 전체 평균 품질 비교 (read " + str(len(results)) + " 개) ==", file=err)
    for title, group in [("GC 가 가장 낮은 " + str(n) + " 개", low), ("GC 가 가장 높은 " + str(n) + " 개", high)]:
        print("", file=err)
        print("[" + title + "]", file=err)
        print("name\tgc\tmean_qual", file=err)
        for name, gc, q in group:
            print(name + "\t" + str(round(gc, 4)) + "\t" + str(round(q, 2)), file=err)
        group_q = average([r[2] for r in group])
        diff = group_q - all_q
        print("묶음 평균 품질: " + str(round(group_q, 2)) +
              "  (전체 평균 대비 " + ("+" if diff >= 0 else "") + str(round(diff, 2)) + ")", file=err)
    print("", file=err)
    print("전체 read 평균 품질: " + str(round(all_q, 2)), file=err)
    if len(results) < 2 * n:
        print("주의: read 가 " + str(2 * n) + " 개보다 적어 두 묶음이 겹친다.", file=err)

reads = read_fastq(sys.argv[1])

results = []
print("name\tgc\tmean_qual")
for name, seq, qual in reads:         # 바깥 반복: read 하나씩
    gc = gc_ratio(seq)
    q = mean_quality(qual)
    results.append((name, gc, q))
    print(name + "\t" + str(round(gc, 4)) + "\t" + str(round(q, 2)))

if len(results) > 0:
    report_extremes(results)
