# lab07 요약: 함수와 파일 저장

## 핵심 개념

| 개념 | 내용 |
|------|------|
| 함수 정의 | `def 이름(매개변수):` + docstring + `return` |
| print vs return | `print`는 화면 출력만 함(반환값은 `None`), `return`은 값을 돌려줘서 다른 곳에서 쓸 수 있음 (`fseqlen.py`) |
| 모듈 | 함수를 `fasta.py`에 모아 두고 `from fasta import read_fasta, gc_content`로 불러 씀 |
| `__main__` | `if __name__ == "__main__":` 아래 코드는 파일을 직접 실행할 때만 동작하고, import할 때는 실행되지 않음 (`tool.py`) |
| 파일 쓰기 | `open(f, "w")` 새로 쓰기(덮어씀, bash `>`), `open(f, "a")` 이어 쓰기(bash `>>`) |
| 명령행 인자 | `sys.argv`는 항상 문자열이므로 숫자로 비교하려면 `int()` 변환 필요 |

## fasta.py 모듈 함수

| 함수 | 받는 것 | 돌려주는 것 |
|------|---------|-------------|
| `read_fasta(filename)` | FASTA 파일 경로 | `{이름: 서열}` 딕셔너리 (헤더의 첫 단어를 이름으로 사용, 여러 줄 서열은 이어 붙임) |
| `write_fasta(seqs, filename)` | 서열 딕셔너리, 저장 경로 | 없음 (파일로 저장) |
| `gc_content(seq)` | 서열 문자열 | GC 비율 0.0~1.0 (빈 서열이면 0.0) |
| `reverse_complement(seq)` | 서열 문자열 | 역상보 서열 (`"ATGC"` → `"GCAT"`) |
| `length_stats(seqs)` | 서열 딕셔너리 | `count`, `total`, `mean`, `min`, `max` 딕셔너리 |

## 스크립트 (lab07/src)

| 파일 | 하는 일 | 실행 예 |
|------|---------|---------|
| `fgc.py` | `gc_content` 함수 정의 연습 | `python fgc.py` |
| `fseqlen.py` | print 와 return 차이 확인 | `python fseqlen.py` |
| `tool.py` | `__main__` 동작 확인 | `python tool.py` |
| `countseq2.py` | 서열 개수 출력 | `python countseq2.py ../data/seqs.fasta` |
| `seqlen2.py` | 서열별 이름·길이 출력 | `python seqlen2.py ../data/seqs.fasta` |
| `test.py` | `length_stats`로 길이 통계 출력 | `python test.py ../data/seqs.fasta` |
| `filter_fasta.py` | 최소 길이 이상 서열만 FASTA로 저장 | `python filter_fasta.py ../data/seqs.fasta 20 ../doc/long.fasta` |
| `summary.py` | 서열별 이름·길이·GC를 TSV로 저장 | `python summary.py ../data/seqs.fasta ../doc/summary.tsv` |
| `batchinfo2.py` | 폴더 안 모든 `.fasta` 파일의 개수·총길이·평균 GC를 TSV로 저장 | `python batchinfo2.py ../data ../doc/batchinfo.tsv` |

## 결과 파일 (lab07/doc)

`summary.tsv` (seqs.fasta)

| name | length | gc |
|------|--------|----|
| gene1 | 30 | 0.5 |
| gene2 | 15 | 0.4667 |
| gene3 | 22 | 0.5455 |

`batchinfo.tsv` (data 폴더 전체)

| filename | count | total | mean_gc |
|----------|-------|-------|---------|
| seqs2.fasta | 2 | 16 | 0.25 |
| seqs.fasta | 3 | 67 | 0.504 |
| lower.fasta | 2 | 20 | 0.2 |

## 겪은 오류

1. **ZeroDivisionError**: 빈 서열을 `gc_content`에 넣었을 때 → `if len(seq) == 0: return 0.0`으로 해결
2. **TypeError**: `sys.argv` 값을 `int()` 없이 숫자와 비교했을 때 → `int(sys.argv[2])`로 변환

## 개선할 점

- `gc_content`와 `reverse_complement`는 대문자만 처리한다. `lower.fasta`의 평균 GC가 0.2로 낮게 나온 것도 소문자 g/c를 세지 않았기 때문이며, 소문자가 들어가면 `reverse_complement`는 KeyError가 난다 → `seq.upper()` 적용 필요
- N 같은 애매한 염기 처리
- 서열을 60글자씩 줄바꿈해서 저장하는 기능
- 구간별(sliding window) GC 비율 계산 함수
