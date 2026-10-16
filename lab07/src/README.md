# fasta.py 도구 상자

## 함수 목록

### read_fasta(filename)
- **받는 것**: FASTA 파일 경로
- **돌려주는 것**: {서열이름: 서열} 딕셔너리
- **예**: `seqs = read_fasta("data/seqs.fasta")`

### write_fasta(seqs, filename)
- **받는 것**: {서열이름: 서열} 딕셔너리, 저장할 파일 경로
- **돌려주는 것**: 없음 (파일로 저장)
- **예**: `write_fasta(seqs, "data/output.fasta")`

### gc_content(seq)
- **받는 것**: 서열 문자열
- **돌려주는 것**: GC 비율 (0.0 ~ 1.0)
- **예**: `gc_content("ATGC")  # 0.5`

### reverse_complement(seq)
- **받는 것**: 서열 문자열
- **돌려주는 것**: 역상보 서열 문자열
- **예**: `reverse_complement("ATGC")  # "GCAT"`

### length_stats(seqs)
- **받는 것**: {서열이름: 서열} 딕셔너리
- **돌려주는 것**: 서열 개수, 전체 길이, 평균 길이, 최단, 최장 딕셔너리
- **예**: `stats = length_stats(seqs); print(stats["max"])`

## 부족한 점 / 추가하고 싶은 함수
- 소문자 서열 외에 N 같은 애매한 염기도 처리할 수 있으면 좋겠다
- 서열을 60글자씩 줄바꿈해서 저장하는 기능이 없다
- GC 비율을 서열 전체가 아니라 구간별로 계산하는 함수가 있으면 좋겠다