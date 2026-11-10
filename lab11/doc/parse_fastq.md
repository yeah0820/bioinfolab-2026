# parse_fastq.py 사용 설명서

## 1. 개요

`lab11/src/parse_fastq.py` 는 FASTQ 파일을 읽어서 read 개수와 첫 번째 read 의 이름, 서열, 길이를 화면에 출력하는 스크립트이다. 안에 있는 `read_fastq` 함수는 FASTQ 를 `(이름, 서열, 품질)` 튜플의 리스트로 바꿔 준다.

## 2. 실행 방법

```
cd lab11
python3 src/parse_fastq.py <FASTQ 파일>
```

- 인자는 FASTQ 파일 경로 하나만 받는다.
- 압축 파일(`.fq.gz`)은 바로 읽지 못한다. 먼저 `gunzip -k` 로 풀어서 쓴다.
- 외부 라이브러리 없이 파이썬 표준 기능만 쓴다.

## 3. 입력 형식

read 하나가 정확히 4줄로 된 FASTQ 를 받는다.

```
@read1 sample=A
ATGCGTACGTTAGC
+
IIIIIHHHGGFFEE
```

| 줄 | 예 | 내용 |
|---|---|---|
| 1줄 | `@read1 sample=A` | `@` + 이름 |
| 2줄 | `ATGCGTACGTTAGC` | 서열 |
| 3줄 | `+` | 구분자 (읽지 않고 건너뜀) |
| 4줄 | `IIIIIHHHGGFFEE` | 품질 점수 (서열과 길이가 같음) |

## 4. 실행 예시

read 4개짜리 샘플 파일로 실행한 결과이다.

```
$ python3 src/parse_fastq.py sample.fastq
read 개수: 4
첫 read 이름: read1 sample=A
첫 read 서열: ATGCGTACGTTAGC
첫 read 길이: 14
```

| 출력 항목 | 의미 |
|---|---|
| read 개수 | 파일 안 read(4줄 묶음)의 수 |
| 첫 read 이름 | 첫 헤더에서 `@` 를 뗀 나머지 전체 |
| 첫 read 서열 | 첫 read 의 2번째 줄 |
| 첫 read 길이 | 첫 read 서열의 글자 수 |

## 5. 코드 설명

### `read_fastq(filename)`

1. `f.readlines()` 로 파일의 모든 줄을 한꺼번에 리스트로 읽는다.
2. `range(0, len(lines), 4)` 로 4줄씩 건너뛰며 read 하나씩 처리한다.
3. 각 read 에서
   - `lines[i]` → 끝의 줄바꿈을 지우고(`rstrip()`) 첫 글자 `@` 를 뗀다(`[1:]`) → 이름
   - `lines[i + 1]` → 서열
   - `lines[i + 2]` → `+` 줄이므로 쓰지 않는다
   - `lines[i + 3]` → 품질 문자열
4. `(이름, 서열, 품질)` 튜플을 리스트에 모아서 돌려준다.

다른 스크립트에서 쓰면 반환값은 아래와 같다.

```
[('read1 sample=A', 'ATGCGTACGTTAGC', 'IIIIIHHHGGFFEE'),
 ('read2 sample=A', 'GGCCTTAAGGCA',   'IIIIHHHGGFFE'),
 ...]
```

### 메인 부분

`sys.argv[1]` 로 받은 파일을 `read_fastq` 로 읽고, `len(reads)` 와 `reads[0]` 의 값들을 출력한다.

## 6. 주의할 점

| 상황 | 결과 |
|---|---|
| 파일 이름을 주지 않고 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 빈 파일 | `reads[0]` 에서 `IndexError` |
| 파일 끝에 빈 줄이 더 있음 | 4줄 묶음이 어긋나 `IndexError` 가 나거나 이상한 read 가 생김 |
| 서열이 여러 줄로 나뉜 FASTQ | 4줄 고정이라고 가정하므로 잘못 읽음 |
| 헤더에 공백이 있음 | 이름에 공백 뒤 내용까지 포함됨 (`lab07` 의 `read_fasta` 는 첫 단어만 씀) |
| 아주 큰 파일 | `readlines()` 가 파일 전체를 메모리에 올리므로 느리거나 메모리가 부족할 수 있음 |

- `@` 로 시작하는지, `+` 줄이 맞는지, 서열과 품질 길이가 같은지는 확인하지 않는다.
- 품질 문자열(`qual`)은 읽어서 저장만 하고 출력에는 쓰지 않는다.
- 품질 점수를 숫자로 바꾸려면 Phred+33 기준으로 `ord(문자) - 33` 을 쓴다. 예: `I` → 40.
