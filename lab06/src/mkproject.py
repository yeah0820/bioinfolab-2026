#!/usr/bin/env python3
# mkproject.py — 프로젝트 기본 폴더 구조를 만드는 스크립트

import sys
import os

# 1. 인자가 없으면 사용법 출력 후 종료
if len(sys.argv) < 2:
    print("사용법: python3 mkproject.py <프로젝트이름>", file=sys.stderr)
    sys.exit(1)

name = sys.argv[1]

# 2. 같은 이름의 폴더가 이미 있으면 오류 후 종료
if os.path.isdir(name):
    print(f"오류: '{name}' 폴더가 이미 존재합니다.", file=sys.stderr)
    sys.exit(1)

# 3. 폴더 구조 생성
for sub in ["src", "data", "results"]:
    os.makedirs(os.path.join(name, sub))

# 4. 완료 메시지
print(f"'{name}' 프로젝트를 만들었습니다.")