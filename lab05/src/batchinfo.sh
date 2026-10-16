#!/usr/bin/env bash

dir=$1

if [[ ! -d "$dir" ]]; then
    echo "오류: '$dir' 폴더를 찾을 수 없습니다." >&2
    exit 1
fi

echo -e "file\tcount"
for f in "$dir"/*.fasta; do
    if [[ ! -f "$f" ]]; then
        echo "경고: '$dir' 안에 FASTA 파일이 없습니다." >&2
        break
    fi
    echo -e "$f\t$(grep -c '^>' "$f")"
done