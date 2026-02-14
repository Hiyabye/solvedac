# 프로젝트 solved.ac

[solved.ac](https://solved.ac)는 [Baekjoon Online Judge](https://www.acmicpc.net)에 수록된 문제들의 난이도를 제공하는 사이트입니다. 이 프로젝트는 solved.ac의 API를 활용하여 여러 기능을 수행하고자 합니다.

solved.ac의 API에 대한 자세한 문서는 [여기](https://solvedac.github.io/unofficial-documentation)에서 확인할 수 있습니다.

## 시작하며

git을 사용하여 이 저장소를 클론할 때, shallow 옵션을 강력히 권장합니다. 전체 커밋 기록은 용량이 너무 큽니다.

```bash
git clone https://github.com/Hiyabye/solvedac.git --depth 1
```

## BOJ 문제 데이터 수집

- 내용: Baekjoon Online Judge의 문제 데이터를 수집하여 JSON 파일로 저장합니다. `data` 디렉토리에서 확인할 수 있습니다.
- API: [ID 목록으로 문제 목록 가져오기](https://solvedac.github.io/unofficial-documentation/#/operations/getProblemByIdArray)
- 스크립트: [boj-data.py](scripts/boj-data.py)

데이터는 매일 한 번씩 업데이트되며, API 호출 제한으로 인해 업데이트 과정이 세 부분으로 나뉩니다. 각 업데이트의 정보는 다음과 같습니다:

| 작업 | 대상 문제 | 시각 (UTC) | 시각 (한국) |
|:---:|:---:|:---:|:---:|
| 데이터 1차 업데이트 | 1000번~10999번 | 00:00 | 09:00 |
| 데이터 2차 업데이트 | 11000번~20999번 | 06:00 | 15:00 |
| 데이터 3차 업데이트 | 21000번~30999번 | 12:00 | 21:00 |
| 데이터 4차 업데이트 | 31000번~40999번 | 18:00 | 03:00 |

## 사용 예시: Baekjoon README 자동 업데이트

- 내용: 솔루션 저장소인 [Hiyabye/Baekjoon](https://github.com/Hiyabye/Baekjoon)의 `README.md` 파일을 자동으로 업데이트합니다.
- API: [사용자 정보 가져오기](https://solvedac.github.io/unofficial-documentation/#/operations/getUser), [문제 검색하기](https://solved.ac/api/v3/search/problem)
- 스크립트: [update_readme.py](https://github.com/Hiyabye/Baekjoon/blob/main/scripts/update_readme.py)
