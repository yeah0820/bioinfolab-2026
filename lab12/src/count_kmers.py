# 길이 L 인 서열에서 k-mer 개수를 구하는 함수와 그 검증
# 실행: python3 count_kmers.py


def count_kmers(L, k):
    # 길이 k 인 창을 한 칸씩 밀면 시작 위치는 0 ~ L-k 이므로 개수는 L - k + 1
    if k <= 0:
        raise ValueError("k 는 1 이상이어야 한다")
    if L < 0:
        raise ValueError("L 은 0 이상이어야 한다")

    # k > L 이면 창이 서열 안에 한 번도 들어가지 않으므로 k-mer 는 0 개이다.
    # 공식을 그대로 쓰면 음수(예: L=3, k=5 → -1)가 나오므로 0 으로 막는다.
    # 에러 대신 0 을 돌려주는 이유: 여러 read/contig 를 반복 처리할 때
    # 짧은 서열 하나 때문에 전체가 멈추지 않고, 합계 계산에도 그대로 쓸 수 있다.
    if k > L:
        return 0
    return L - k + 1


def count_by_hand(L, k):
    # 공식을 쓰지 않고 실제 서열을 만들어 k-mer 를 하나씩 잘라서 센다
    seq = ("ATGC" * (L // 4 + 1))[:L]
    count = 0
    for i in range(len(seq)):
        piece = seq[i:i + k]
        if len(piece) == k:    # 끝부분에서 k 보다 짧게 잘린 조각은 제외
            count = count + 1
    return count


# 확인할 (L, k) 조합: 일반 / 경계 / k > L
cases = [(10, 3), (7, 1), (100, 21), (5, 5), (0, 1), (3, 5)]

print("L\tk\t함수\t직접\t일치")
all_ok = True
for L, k in cases:
    f = count_kmers(L, k)
    h = count_by_hand(L, k)
    ok = f == h
    if not ok:
        all_ok = False
    print(f"{L}\t{k}\t{f}\t{h}\t{'O' if ok else 'X'}")

print("모두 일치" if all_ok else "불일치 있음")
