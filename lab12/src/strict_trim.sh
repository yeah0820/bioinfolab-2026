#!/usr/bin/env bash
# 더 엄격한 기준으로 fastp 트리밍 → shovill 어셈블리 → 기존 결과와 비교
# 실행: bash src/strict_trim.sh   (어느 위치에서 실행해도 lab12 폴더 기준으로 동작)

set -euo pipefail

# 스크립트 위치(lab12/src)의 상위 폴더인 lab12 로 이동
cd "$(dirname "$0")/.."

R1_OUT=data/R1.strict.fastq
R2_OUT=data/R2.strict.fastq
ASM_OUT=doc/shovill_strict_out

# 기존 결과를 덮어쓰지 않도록 출력이 이미 있으면 멈춘다
for f in "$R1_OUT" "$R2_OUT" doc/fastp_strict.json doc/fastp_strict.html "$ASM_OUT"; do
    if [ -e "$f" ]; then
        echo "이미 존재함: $f  (덮어쓰지 않기 위해 중단합니다)"
        exit 1
    fi
done

echo "== 1) 엄격한 트리밍 (fastp) =="
# --cut_front --cut_tail -W 4 -M 25 : 양 끝에서 4bp 창 평균 품질 25 미만이면 잘라 냄 (실제 트리밍)
# -q 25 -u 10 : Q25 미만 염기가 10% 를 넘는 read 는 버림 (기본값 Q15, 40%)
# -e 30       : read 평균 품질 30 미만이면 버림
# -n 0        : N 이 하나라도 있으면 버림 (기본값 5)
# -l 100      : 트리밍 후 100bp 미만 read 는 버림 (기존 50)
# --detect_adapter_for_pe : paired-end adapter 탐지 강화
fastp -i data/R1.fastq -I data/R2.fastq \
      -o "$R1_OUT" -O "$R2_OUT" \
      --detect_adapter_for_pe \
      --cut_front --cut_tail -W 4 -M 25 \
      -q 25 -u 10 \
      -e 30 \
      -n 0 \
      -l 100 \
      -j doc/fastp_strict.json -h doc/fastp_strict.html

echo
echo "== 2) read 비교: 원본 / 기존 트리밍 / 엄격한 트리밍 =="
seqkit stats -a data/R1.fastq data/R1.trim.fastq "$R1_OUT"

echo
echo "== 3) 어셈블리 (shovill) =="
shovill --R1 "$R1_OUT" --R2 "$R2_OUT" --outdir "$ASM_OUT"

echo
echo "== 4) 어셈블리 비교: contig 개수(num_seqs), 전체 길이(sum_len), N50 =="
seqkit stats -a doc/shovill_out/contigs.fa \
                doc/shovill_trim_out/contigs.fa \
                "$ASM_OUT/contigs.fa"
