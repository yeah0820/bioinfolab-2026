#!/usr/bin/env bash
# mkproject2.sh — 프로젝트 기본 폴더 구조를 만드는 스크립트

# 1. 인자가 없으면 사용법 출력 후 종료
if [[ $# -eq 0 ]]; then
    echo "사용법: $0 <프로젝트이름>" >&2
    exit 1
fi

NAME=$1

# 2. 같은 이름의 폴더가 이미 있으면 오류 후 종료
if [[ -d "$NAME" ]]; then
    echo "오류: '$NAME' 폴더가 이미 존재합니다." >&2
    exit 1
fi

# 폴더 구조 생성
mkdir -p "$NAME"/{src,data,results}

# 3. 정상 종료 시 만들어진 구조 출력
echo "'$NAME' 프로젝트를 만들었습니다."
find "$NAME" -print | sort | sed 's|[^/]*/|  |g'