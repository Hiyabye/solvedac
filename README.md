# 프로젝트 solved.ac

[solved.ac](https://solved.ac/)는 [Baekjoon Online Judge](https://www.acmicpc.net/)에 수록된 문제들의 난이도를 제공하는 사이트입니다. 이 프로젝트는 solved.ac의 API를 활용하여 여러 기능을 수행하고자 합니다.

solved.ac의 API에 대한 자세한 문서는 [여기](https://solvedac.github.io/unofficial-documentation/#/)에서 확인할 수 있습니다.

## 목차

- 기능 1: [BOJ 문제 데이터 수집](#boj-문제-데이터-수집)
- 정리하며: [자동화 시간 계산](#자동화-시간-계산)

## BOJ 문제 데이터 수집

- 내용: Baekjoon Online Judge의 문제 데이터를 수집하여 JSON 파일로 저장합니다. `data` 디렉토리에서 확인할 수 있습니다.
- API: [ID 목록으로 문제 목록 가져오기](https://solvedac.github.io/unofficial-documentation/#/operations/getProblemByIdArray)
- 스크립트: [boj-data.py](scripts/boj-data.py)

API 호출 제한으로 인해 데이터는 매일 한 번씩 업데이트되며, 업데이트 과정이 세 부분으로 나뉩니다. 각 업데이트의 정보는 다음과 같습니다:

| 작업 | 대상 문제 | 시각 (UTC) | 시각 (한국) |
|:---:|:---:|:---:|:---:|
| 데이터 1차 업데이트 | 1000번~12999번 | 06:00 | 15:00 |
| 데이터 2차 업데이트 | 13000번~24999번 | 12:00 | 21:00 |
| 데이터 3차 업데이트 | 25000번~36999번 | 18:00 | 03:00 |

## 자동화 시간 계산

solved.ac의 API 호출 제한과 GitHub Actions의 런타임 제한을 고려하여, 원활한 자동화를 위한 시간을 계산해야 합니다.

solved.ac API의 호출 제한은 15분에 256회입니다. GitHub Actions는 Pro 계정 사용자에게 30일에 3000분의 런타임을 제공합니다.

| 시각 (UTC) | 시각 (한국) | 작업 | API 호출 횟수 | GitHub Actions 런타임 (30일) |
|:---:|:---:|:---:|:---:|:---:|
| 06:00 | 15:00 | 데이터 1차 업데이트 | 120회 | 60분 |
| 12:00 | 21:00 | 데이터 2차 업데이트 | 120회 | 60분 |
| 18:00 | 03:00 | 데이터 3차 업데이트 | 120회 | 60분 |

GitHub Actions 런타임을 모두 계산하면 총 180분이 소요되며, 이는 3000분의 제한 안에 들어갑니다.
