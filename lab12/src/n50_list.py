# contig 길이 목록으로 N50 을 계산하는 스크립트
# 실행: python3 n50_list.py

def n50(lengths):
    # 긴 contig 부터 차례로 더해서 전체 길이의 절반 이상이 되는 순간의 길이를 돌려준다
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    half = total / 2

    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length


# 입력값: contig 길이
lengths = [12, 3, 20, 8, 1, 15, 6]

print("contig 길이:", lengths)
print("정렬(내림차순):", sorted(lengths, reverse=True))
print("contig 개수:", len(lengths))
print("전체 길이:", sum(lengths))
print("절반 길이:", sum(lengths) / 2)
print("N50:", n50(lengths))
