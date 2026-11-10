# 🐧 Linux / Docker / Git 퀴즈 게임

> **진행 상태:** 설계 및 문서 초안. 기능과 테스트 결과는 구현 후 확인하여 갱신합니다.

## 1. 프로젝트 개요

Linux, Docker, Git의 기본 지식을 복습하는 **Python 콘솔 퀴즈 게임**입니다. Python 기초 문법과 객체지향, JSON 파일 입출력, 예외 처리, Git 버전 관리를 실습하는 코디세이 미션 2 프로젝트입니다.

## 2. 퀴즈 주제 및 선정 이유

- **주제:** Linux / Docker / Git
- **선정 이유:** 미션 1에서 학습한 명령어 및 개념을 복습하면서, 미션 2의 Python 구현에 집중하기 위해 선정했습니다.
- **기본 문제:** Linux 2문제, Docker 2문제, Git 2문제(총 6문제 예정)

## 3. 개발 환경

- Python 3.10 이상
- Python 표준 라이브러리만 사용 (`json`, `random`, `datetime`, `pathlib`, `unittest` 등)
- Git / GitHub
- 개발 환경 및 Python 버전: *구현 시 기입*

## 4. 실행 방법

저장소를 복제한 뒤 프로젝트 **루트 디렉터리**에서 다음 명령어를 실행하도록 구현할 예정입니다.

```bash
git clone https://github.com/Gaktsu/codyssey_mission_2.git
cd codyssey_mission_2
python -m src.main
```

> 위 실행 명령은 계획된 `src` 패키지 구조 기준이며, 실제 구현 완료 후 검증합니다. 가상환경 구성은 이 문서에서 다루지 않습니다.

## 5. 주요 기능

### 5.1 퀴즈 풀기
- 저장된 문제에서 **풀 문제 수(1~등록된 문제 수)** 선택
- `random.sample()`로 중복 없이 랜덤 출제
- 각 문제에 선택지 4개와 정답 입력(1~4) 제공
- 문제당 힌트 1회 사용 가능; 힌트 사용한 문제를 맞히면 해당 문항 점수에서 10점 감점
- 풀이 완료 시 정답 수, 힌트 사용 수, 최종 점수(100점 만점) 표시
- 문제가 하나도 없으면 안내 후 메뉴로 복귀

### 5.2 퀴즈 추가
- 질문, 선택지 4개, 정답 번호(1~4), 힌트 입력
- 빈 값 및 잘못된 번호 검증
- 퀴즈에 고유 ID 부여 후 `data/state.json`에 저장

### 5.3 퀴즈 목록
- 등록된 퀴즈의 ID, 질문 및 선택지 목록 확인
- 등록된 문제가 없으면 안내 메시지 표시

### 5.4 퀴즈 삭제
- 퀴즈 ID를 선택한 뒤 삭제 여부 확인
- 삭제된 결과를 `data/state.json`에 저장

### 5.5 최고 점수 확인
- 역대 최고 **최종 점수(0~100점)** 표시
- 아직 플레이하지 않았으면 기록 없음 안내

### 5.6 점수 기록 히스토리
- 게임 완료 날짜/시간, 전체 문제 수, 정답 수, 힌트 사용 수, 최종 점수 저장
- 지난 플레이 기록 조회

### 5.7 데이터 저장 및 불러오기
- `data/state.json`: 퀴즈와 힌트
- `data/scores.json`: 최고 점수 및 플레이 기록
- 첫 실행 시 기본 퀴즈 6개와 초기 점수 데이터 생성
- 파일별 누락·손상·읽기/쓰기 오류를 독립적으로 처리

### 5.8 예외 처리
- 입력 앞뒤 공백 제거, 빈 입력·문자·범위 초과 시 재입력
- `KeyboardInterrupt`, `EOFError` 발생 시 안내 후 가능한 범위에서 저장하고 안전 종료
- 저장 실패 시 오류 안내; 조용히 성공한 것처럼 표시하지 않음

## 6. 프로젝트 구조

```text
codyssey_mission_2/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── quiz.py
│   ├── quiz_game.py
│   ├── input_utils.py
│   └── default_quizzes.py
├── data/
│   ├── state.json          # 퀴즈 데이터
│   └── scores.json         # 최고 점수 및 기록
├── tests/
│   ├── __init__.py
│   ├── test_quiz.py
│   ├── test_quiz_game.py
│   ├── test_input_utils.py
│   ├── test_storage.py
│   └── test_score.py       # 점수 테스트
├── docs/
│   ├── 01_요구사항_및_설계.md
│   ├── 02_테스트_케이스.md
│   ├── 03_Git_작업_기록.md
│   ├── 04_트러블슈팅.md
│   └── screenshots/
│       ├── environment.png
│       ├── menu.png
│       ├── play.png
│       ├── add_quiz.png
│       ├── quiz_list.png
│       ├── delete_quiz.png
│       ├── score.png
│       ├── history.png
│       └── git_log.png
├── .gitignore
└── README.md
```

> 위 트리는 **목표 구조**입니다. 실제 파일은 기능 개발 및 검증 과정에서 생성합니다.

## 7. 데이터 파일 설명

### 7.1 저장 경로와 역할

| 파일 | 역할 |
| --- | --- |
| `data/state.json` | 퀴즈 ID, 문제, 보기, 정답 번호, 힌트 |
| `data/scores.json` | 최고 점수 및 게임별 플레이 기록 |

> ⚠️ **과제 원문과의 차이:** 원래 미션에는 **프로젝트 루트의 `state.json` 한 파일에 퀴즈와 최고 점수를 함께 저장**하도록 명시되어 있습니다. 현재 설계는 의도적으로 JSON을 폴더 안의 2개 파일로 분리한 **변형안**입니다. 평가 전 허용 여부를 확인하고, 허용되지 않으면 필수 데이터의 루트 `state.json` 통합 방식으로 조정해야 합니다.

### 7.2 JSON 데이터 구조

**`data/state.json` 예시**

```json
{
  "quizzes": [
    {
      "id": 1,
      "question": "현재 작업 경로를 확인하는 Linux 명령어는?",
      "choices": ["ls", "pwd", "cd", "mkdir"],
      "answer": 2,
      "hint": "현재 작업 중인 위치를 화면에 출력합니다."
    }
  ]
}
```

**`data/scores.json` 예시**

```json
{
  "best_score": 90,
  "history": [
    {
      "date": "2026-11-10 10:00:00",
      "total_questions": 1,
      "correct_answers": 1,
      "hints_used": 1,
      "score": 90
    }
  ]
}
```

- `best_score` 초기값: `null` (플레이 기록 없음)
- 점수 계산: `(정답 수 × 100 - 힌트를 사용하고 맞힌 문제 수 × 10) / 출제 문제 수`, 계산 결과를 **정수로 반올림**하여 저장(동점은 최고 점수 갱신 아님)
- `hints_used`: 전체 힌트 사용 횟수이며, **힌트 사용 후 정답 처리된 문항 수**는 감점 계산 시 별도로 셉니다.
- ID는 삭제 후에도 중복되지 않도록 기존 최대 ID보다 큰 값을 새 퀴즈에 부여합니다(마지막 퀴즈 삭제 후에도 ID 재사용을 피하려면 별도 `next_id` 관리 필요).

### 7.3 데이터 저장 및 복구 방식

- `encoding='utf-8'`, `ensure_ascii=False`, `indent=2` 사용 예정
- 파일이 없으면 해당 파일에 해당하는 초기값만 생성
- 손상되면 안내 후 해당 파일만 복구; 정상인 다른 파일은 유지
- 읽기/쓰기 실패 시 오류 정보를 안내하고, 저장 가능 여부를 분리해 처리

## 8. 기능 검증 및 실행 결과

> 실제 구현·테스트 완료 후 날짜, 명령어, 결과 및 스크린샷을 기록합니다. 아래는 **증빙 예정 목록**입니다.

- [ ] 메뉴 화면 — `docs/screenshots/menu.png`
- [ ] 랜덤 출제 및 문제 수 선택, 힌트 — `docs/screenshots/play.png`
- [ ] 퀴즈 추가 — `docs/screenshots/add_quiz.png`
- [ ] 목록 및 삭제 — `docs/screenshots/quiz_list.png`, `docs/screenshots/delete_quiz.png`
- [ ] 최고 점수 및 히스토리 — `docs/screenshots/score.png`, `docs/screenshots/history.png`
- [ ] 오류 입력 및 데이터 복구 — 증빙 추가 예정
- [ ] 개발 환경 — `docs/screenshots/environment.png`

자세한 테스트 케이스: [docs/02_테스트_케이스.md](docs/02_테스트_케이스.md)

## 9. 트러블슈팅

실제 발생한 오류만 발생 환경·재현·원인·해결·재검증 순으로 기록합니다.

[docs/04_트러블슈팅.md](docs/04_트러블슈팅.md)

## 10. Git 작업 이력

- 기능 단위 **의미 있는 커밋 10개 이상** 목표
- 별도 브랜치에서 퀴즈 풀기 기능 개발 후 `main` 병합
- `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 사용 증빙
- `clone`한 별도 디렉터리에서 수정·push → 원래 디렉터리에서 pull 실습
- `git log --oneline --graph --all` 캡처: `docs/screenshots/git_log.png`

진행 상황은 [docs/03_Git_작업_기록.md](docs/03_Git_작업_기록.md)에 실제 실행한 내용만 기록합니다.
