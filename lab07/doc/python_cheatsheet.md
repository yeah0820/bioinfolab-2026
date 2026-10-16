# fasta.py 도구 상자

## 함수 목록

### read_fasta(filename)
- **받는 것**: FASTA 파일 경로
- **돌려주는 것**: {서열이름: 서열} 딕셔너리
- **예**: `seqs = read_fasta("data/seqs.fasta")`

### write_fasta(seqs, filename)
- **받는 것**: {서열이름: 서열} 딕셔너리, 저장할 파일 경로
- **돌려주는 것**: 없음 (파일로 저장)
- **예**: `write_fasta(seqs, "data/output.fasta")`

### gc_content(seq)
- **받는 것**: 서열 문자열
- **돌려주는 것**: GC 비율 (0.0 ~ 1.0)
- **예**: `gc_content("ATGC")  # 0.5`

### reverse_complement(seq)
- **받는 것**: 서열 문자열
- **돌려주는 것**: 역상보 서열 문자열
- **예**: `reverse_complement("ATGC")  # "GCAT"`

### length_stats(seqs)
- **받는 것**: {서열이름: 서열} 딕셔너리
- **돌려주는 것**: 서열 개수, 전체 길이, 평균 길이, 최단, 최장 딕셔너리
- **예**: `stats = length_stats(seqs); print(stats["max"])`

## 부족한 점 / 추가하고 싶은 함수
- 소문자 서열 외에 N 같은 애매한 염기도 처리할 수 있으면 좋겠다
- 서열을 60글자씩 줄바꿈해서 저장하는 기능이 없다
- GC 비율을 서열 전체가 아니라 구간별로 계산하는 함수가 있으면 좋겠다

## 함수 정의
def 함수이름(매개변수):
    """설명"""
    return 결과

## print vs return
print: 화면에 출력만 함 / return: 값을 돌려줘서 다른 곳에 쓸 수 있음

## 모듈 불러오기
from fasta import read_fasta, gc_content

## __main__
if __name__ == "__main__":
    # 이 파일을 직접 실행할 때만 동작, import 할 때는 실행 안 됨

## 파일 쓰기 모드
open(filename, "w")  # 새로 쓰기 (파일 있으면 덮어씀) → bash의 >
open(filename, "a")  # 이어 쓰기 (파일 끝에 추가)      → bash의 >>

## 오늘 겪은 오류
# 1. ZeroDivisionError: 빈 서열을 gc_content에 넣었을 때
#    → if len(seq) == 0: return 0.0 으로 해결

# 2. TypeError: int()없이 sys.argv 값을 숫자와 비교했을 때
#    → sys.argv는 항상 문자열이므로 int()로 변환 필요