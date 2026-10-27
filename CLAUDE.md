# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.


## 저장소 성격

생물정보학실험 수업의 학생 실습 저장소이다. 빌드, 린트, 테스트 프레임워크는 없다. 주차별 폴더(`lab05`, `lab06`, …)에 bash/파이썬 연습 스크립트가 쌓여 있고, 각 스크립트는 직접 실행해서 결과를 확인한다. 설명과 주석, 커밋 메시지는 한국어로 쓴다.

## 폴더 규칙 (README 기준)

- 새 주차 폴더는 `cp -r lab-template labNN` 으로 만든다. 하위 폴더는 `data/`(데이터), `doc/`(보고서·결과 요약), `src/`(직접 작성한 `.sh`, `.py`) 이다.
- `resources/` 는 강의자가 준 공용 예제 데이터와 스크립트이다.
- 시퀀싱 원본(`*.fastq`, `*.fq.gz`, `*.sra`)과 shovill/prokka/spades/flye 결과 폴더, FastQC 보고서는 `.gitignore` 로 제외된다. 필요하면 `wget` 으로 다시 받는다.
- 필요한 도구가 없어도 직접 설치하지 않는다. conda 실습 주차만 예외이다.

## 실행 환경

`.devcontainer/` 에 Codespaces 설정 4개가 있고 주차마다 고른다. 1-basic(02~07주: 파이썬), 2-conda(micromamba), 3-seq(08~09, 12~14주: seqkit, blast, mafft, iqtree, fastqc, fastp), 4-genome(10~11주: 위 도구 + shovill, prokka). `.devcontainer/check.sh` 가 어떤 도구가 설치되어 있는지 보여 준다.

## lab07 `fasta.py` 모듈

`lab07/src/fasta.py` 는 이후 스크립트들이 공유하는 함수 모음이다. `read_fasta`, `write_fasta`, `gc_content`, `reverse_complement`, `length_stats` 가 들어 있다. 같은 폴더의 스크립트(`summary.py`, `test.py`, `filter_fasta.py` 등)는 `from fasta import ...` 로 불러 쓰므로 `lab07/src` 안에서 실행해야 한다.

```
cd lab07/src
python3 summary.py ../../lab06/data/seqs.fasta out.tsv   # 이름, 길이, GC 를 TSV 로 저장
python3 test.py ../../lab06/data/seqs.fasta              # length_stats 출력
python3 fasta.py <fasta>                                 # __main__ 자체 점검
```

동작상 주의할 점:
- `read_fasta` 는 헤더의 첫 단어만 이름으로 쓰고, 여러 줄로 된 서열은 이어 붙인다.
- `gc_content` 는 대문자 `G`/`C` 만 센다.
- `reverse_complement` 는 `ATGC` 외의 문자(소문자, `N`)가 있으면 `KeyError` 를 낸다.

함수 설명은 `lab07/src/README.md` 에 있고, 주차 요약은 `lab07/doc/`, `lab09/doc/lab07.md` 에 있다.

## 코드를 쓸 때
- FASTA 파일은 lab07/src/fasta.py 의 read_fasta 로 읽는다.
- 새 라이브러리(Biopython 등)를 쓰기 전에 먼저 물어본다.
- 주석은 한국어로 쓴다.
 
## 하지 말 것
- rm 으로 파일을 지우지 않는다.
- pip install 로 무언가를 설치하지 않는다.
- git 명령어를 실행하지 않는다.
- 파일 덮어쓰기(`>`) 전에 반드시 확인

## 추가 규칙
- 코드 수정 전 반드시 현재 파일 내용을 먼저 보여줄 것
- 작업 완료 후 `git status`로 변경사항 확인할 것