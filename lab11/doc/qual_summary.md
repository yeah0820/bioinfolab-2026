# qual_summary.py 사용 설명서

## 1. 개요

`lab11/src/qual_summary.py` 는 FASTQ 파일의 품질 점수를 읽어서 **전체 read 의 평균 품질**을 숫자 하나로 출력하는 스크립트이다. read 마다 평균 품질을 구한 뒤, 그 값들을 다시 평균 낸다.

## 2. 실행 방법

```
cd lab11
python3 src/qual_summary.py <FASTQ 파일>
```

- 인자는 FASTQ 파일 경로 하나만 받는다.
- 압축 파일(`.fq.gz`)은 바로 읽지 못한다. 먼저 `gunzip -k` 로 풀어서 쓴다.
- 외부 라이브러리 없이 파이썬 표준 기능만 쓴다.
- 품질 문자는 Phred+33 인코딩(현재 Illumina 표준)이라고 가정한다.

## 3. 입력 형식

read 하나가 정확히 4줄로 된 FASTQ 를 받는다. 이 스크립트는 4번째 줄(품질)만 계산에 쓴다.

```
@read1 sample=A
ATGCGTACGTTAGC
+
IIIIIHHHGGFFEE
```

## 4. 실행 예시

read 4개짜리 샘플 파일로 실행한 결과이다.

```
$ python3 src/qual_summary.py sample.fastq
전체 read 평균 품질: 29.583333333333336
```

샘플 파일의 read 별 품질은 아래와 같다.

| read | 품질 문자열 | 길이 | read 평균 품질 |
|---|---|---|---|
| read1 | `IIIIIHHHGGFFEE` | 14 | 38.50 |
| read2 | `IIIIHHHGGFFE` | 12 | 38.58 |
| read3 | `IIIIIIIIHHHHGGGG` | 16 | 39.25 |
| read4 | `####` | 4 | 2.00 |
| 출력값 | (38.50 + 38.58 + 39.25 + 2.00) / 4 | | 29.58 |

## 5. Phred 품질 점수

품질 문자 하나는 염기 하나의 정확도를 나타낸다. 문자의 ASCII 코드에서 33 을 빼면 Phred 점수 Q 가 된다.

| 문자 | ASCII | Q = ASCII - 33 | 오류 확률 |
|---|---|---|---|
| `#` | 35 | 2 | 약 63% |
| `+` | 43 | 10 | 10% |
| `5` | 53 | 20 | 1% |
| `?` | 63 | 30 | 0.1% |
| `I` | 73 | 40 | 0.01% |

- 오류 확률 = 10^(-Q/10)
- 보통 Q20 이상이면 쓸 만하고, Q30 이상이면 품질이 좋다고 본다.

## 6. 코드 설명

### `read_fastq(filename)`

`parse_fastq.py` 의 함수와 같다. 파일 전체를 `readlines()` 로 읽고, 4줄씩 끊어서 `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다. 3번째 줄(`+`)은 건너뛴다.

### `mean_quality(qual)`

1. 품질 문자열의 글자를 하나씩 꺼낸다.
2. `ord(ch) - 33` 으로 Phred 점수로 바꿔 리스트에 모은다.
3. `sum(scores) / len(scores)` 로 평균을 돌려준다.

예: `mean_quality("II##")` → (40 + 40 + 2 + 2) / 4 = 21.0

### 메인 부분

1. `sys.argv[1]` 의 파일을 `read_fastq` 로 읽는다.
2. read 마다 `mean_quality` 를 구해서 `total` 에 더한다.
3. `total / len(reads)` 를 출력한다.

## 7. 결과를 해석할 때 주의할 점

출력값은 **read 평균들의 평균**이지 **모든 염기의 평균**이 아니다. read 길이와 상관없이 read 하나가 같은 비중을 가진다.

- 위 샘플에서 모든 염기 46개의 품질을 한꺼번에 평균 내면 **35.61** 이다.
- 그런데 스크립트 출력은 **29.58** 이다. 길이가 4 인 짧은 read4 의 낮은 품질이 read 하나 몫(1/4)을 통째로 차지하기 때문이다.
- 실제 Illumina 데이터처럼 read 길이가 모두 같으면 두 값은 같다. fastp 같은 도구로 trimming 해서 길이가 제각각이면 차이가 날 수 있다.

## 8. 오류가 나는 경우

| 상황 | 결과 |
|---|---|
| 파일 이름을 주지 않고 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 빈 파일 | `ZeroDivisionError: division by zero` (`len(reads)` 가 0) |
| 품질 줄이 빈 read 가 있음 | `mean_quality` 에서 `ZeroDivisionError` |
| 파일 끝에 빈 줄이 더 있음 | 4줄 묶음이 어긋나 `IndexError` 가 나거나 값이 틀어짐 |
| 서열이 여러 줄로 나뉜 FASTQ | 4줄 고정이라고 가정하므로 잘못 읽음 |
| Phred+64 인코딩(오래된 Illumina) | 오류는 없지만 점수가 31 씩 높게 나옴 |
| 아주 큰 파일 | `readlines()` 가 파일 전체를 메모리에 올리므로 느리거나 메모리가 부족할 수 있음 |

- 서열과 품질 문자열의 길이가 같은지는 확인하지 않는다.
- read 이름과 서열은 읽기만 하고 쓰지 않는다.
