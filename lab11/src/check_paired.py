import re
import sys

# paired-end FASTQ 두 파일(_1, _2)이 제대로 짝을 이루는지 확인한다.
#  1) 두 파일의 read 개수가 같은지
#  2) 같은 순서(i 번째)에 있는 read 끼리 이름이 짝을 이루는지
#
# 사용법: python3 check_paired.py <read1.fastq> <read2.fastq>

# 이름 끝의 짝 표시: 구분 기호(/ . _ :) 바로 뒤에 1 또는 2 가 오는 경우
# 예) read/1 - read/2, read.1 - read.2, read_1 - read_2
# 구분 기호를 꼭 요구하는 이유: SRR1553607.11 과 SRR1553607.12 처럼
# 번호의 마지막 숫자만 다른 서로 다른 read 를 짝으로 잘못 판정하지 않기 위해서이다.
MATE_SUFFIX = re.compile(r"[/._:]([12])$")


# FASTQ 를 4줄씩 읽어 (헤더 첫 단어, 전체 헤더) 를 하나씩 돌려준다.
# 파일이 커서 한 번에 다 읽지 않고 한 레코드씩 흘려보낸다(generator).
def read_names(filename):
    with open(filename) as f:
        while True:
            header = f.readline()
            if not header:
                break                      # 파일 끝
            f.readline()                   # 서열
            f.readline()                   # '+'
            f.readline()                   # 품질
            header = header.rstrip()
            if not header.startswith("@"):
                sys.exit(f"오류: {filename} 의 헤더 형식이 이상합니다: {header}")
            full = header[1:]
            yield full.split()[0], full


# 두 이름이 짝인지 판정한다.
#  - 첫 단어가 완전히 같으면 짝 (fasterq-dump --split-files 의 기본 형태)
#  - 아니면 끝의 짝 표시(/1, /2 등)를 떼고 비교한다.
#    이때 1번 파일 쪽은 1, 2번 파일 쪽은 2 로 끝나야 한다.
def is_pair(name1, name2):
    if name1 == name2:
        return True
    m1 = MATE_SUFFIX.search(name1)
    m2 = MATE_SUFFIX.search(name2)
    if m1 and m2 and m1.group(1) == "1" and m2.group(1) == "2":
        return name1[:m1.start()] == name2[:m2.start()]
    return False


def main():
    if len(sys.argv) != 3:
        sys.exit("사용법: python3 check_paired.py <read1.fastq> <read2.fastq>")
    file1, file2 = sys.argv[1], sys.argv[2]

    reads1 = read_names(file1)
    reads2 = read_names(file2)

    n1 = 0            # 1번 파일 read 개수
    n2 = 0            # 2번 파일 read 개수
    mismatch = 0      # 이름이 짝을 이루지 않는 위치 개수
    examples = []     # 짝이 안 맞는 예시 (처음 5개만 저장)

    # 두 파일을 동시에 한 read 씩 읽으며 비교한다
    while True:
        r1 = next(reads1, None)
        r2 = next(reads2, None)
        if r1 is None and r2 is None:
            break
        if r1 is not None:
            n1 += 1
        if r2 is not None:
            n2 += 1
        # 한쪽이 먼저 끝났으면 이름 비교는 하지 않고 개수만 센다
        if r1 is None or r2 is None:
            continue
        if not is_pair(r1[0], r2[0]):
            mismatch += 1
            if len(examples) < 5:
                examples.append((n1, r1[1], r2[1]))

    print(f"{file1}\t{n1} reads")
    print(f"{file2}\t{n2} reads")

    ok = True
    if n1 == n2:
        print("read 개수: 같음")
    else:
        print(f"read 개수: 다름 (차이 {abs(n1 - n2)})")
        ok = False

    compared = min(n1, n2)
    if mismatch == 0:
        print(f"이름 짝: 비교한 {compared} 쌍 모두 일치")
    else:
        print(f"이름 짝: {compared} 쌍 중 {mismatch} 쌍 불일치")
        for idx, h1, h2 in examples:
            print(f"  {idx}번째 read\n    1: {h1}\n    2: {h2}")
        ok = False

    print("결과: 정상적인 paired-end 파일" if ok else "결과: 짝이 맞지 않음")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
