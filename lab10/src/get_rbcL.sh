#!/bin/bash
# NCBI E-utilities 로 식물 8종의 rbcL 서열(FASTA, GenBank)을 받는다.
# 사용법: cd lab10/src && bash get_rbcL.sh

BASE="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT="../data"

# "학명|파일 이름" 목록
SPECIES=(
  "Arabidopsis thaliana|rbcL_arabidopsis"
  "Panax ginseng|rbcL_ginseng"
  "Oryza sativa|rbcL_rice"
  "Zea mays|rbcL_maize"
  "Ginkgo biloba|rbcL_ginkgo"
  "Pinus thunbergii|rbcL_pine"
  "Adiantum capillus-veneris|rbcL_fern"
  "Marchantia polymorpha|rbcL_liverwort"
)

for entry in "${SPECIES[@]}"; do
  sp="${entry%%|*}"      # 학명
  name="${entry##*|}"    # 파일 이름

  # 검색어: 공백을 + 로 바꿔 URL 에 넣는다
  term="rbcL[Gene] AND ${sp}[Organism] AND 1300:1500[SLEN]"
  term="${term// /+}"

  # 1) esearch: 첫 번째 결과(retmax=1)의 ID 만 뽑는다
  id=$(wget -q -O - "${BASE}/esearch.fcgi?db=nuccore&term=${term}&retmax=1" \
       | grep -o '<Id>[0-9]*</Id>' | head -1 | sed 's/<[^>]*>//g')
  sleep 1

  if [ -z "$id" ]; then
    echo "[경고] ${sp}: 검색 결과 없음, 건너뜀"
    continue
  fi
  echo "${sp} -> ID ${id}"

  # 2) efetch: FASTA
  wget -q -O "${OUT}/${name}.fa" "${BASE}/efetch.fcgi?db=nuccore&id=${id}&rettype=fasta&retmode=text"
  sleep 1

  # 3) efetch: GenBank
  wget -q -O "${OUT}/${name}.gb" "${BASE}/efetch.fcgi?db=nuccore&id=${id}&rettype=gb&retmode=text"
  sleep 1
done
