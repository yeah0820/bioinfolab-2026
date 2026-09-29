#FASTA 파일 이름을 인자로 받아 이래 4가지를 출력한다.
#파일 이름
#서열 개수
#서열 이름 목록 (꺾쇠 없이, 첫 단어만)
#헤더를 뺀 줄의 총 글자 수
#!/usr/bin/bash

#!/usr/bin/bash

echo "파일: $1"
echo "서열 개수: $(grep -c ">" $1)"
echo "서열 이름:"
grep ">" $1 | cut -d " " -f 1 | tr -d ">"
echo "총 염기 수(대략): $(grep -v ">" $1 | tr -d "\n" | wc -c)"

