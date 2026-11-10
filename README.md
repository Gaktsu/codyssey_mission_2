# 🐧 Linux / Docker / Git 퀴즈 게임

> **진행 상태:** 설계 및 문서 초안. 기능과 테스트 결과는 구현 후 확인하여 갱신합니다.

## 1. 프로젝트 개요

Linux, Docker, Git의 기본 지식을 복습하는 **Python 콘솔 퀴즈 게임**입니다. Python 기초 문법과 객체지향, JSON 파일 입출력, 예외 처리, Git 버전 관리를 실습하는 코디세이 미션 2 프로젝트입니다.

## 2. 퀴즈 주제 및 선정 이유

- **주제:** Linux / Docker / Git
- **선정 이유:** 미션 1에서 학습한 명령어 및 개념을 복습하면서, 미션 2의 Python 구현에 집중하기 위해 선정했습니다.
- **기본 문제:** Linux 10문제, Docker 10문제, Git 10문제(총 30문제 예정)

## 3. 개발 환경

- Python 3.10 이상
- Python 표준 라이브러리만 사용 (`json`, `random`, `datetime`, `pathlib` 등)
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
- **10 / 20 / 30문제 모드** 중 선택 (등록된 문제가 부족한 모드는 안내 후 재선택)
- `random.sample()`로 중복 없이 랜덤 출제
- 각 문제에 선택지 4개와 정답 입력(1~4) 제공
- 문제당 힌트 1회 사용 가능; 힌트 사용한 문제를 맞히면 해당 문항 점수에서 10점 감점
- 풀이 완료 시 정답 수, 힌트 사용 수, 최종 점수(100점 만점) 표시
- 게임 도중에는 저장하지 않으며, 완료된 게임만 기록

### 5.2 퀴즈 추가
- 질문, 선택지 4개, 정답 번호(1~4), 힌트 입력
- 빈 값 및 잘못된 번호 검증
- 추가한 퀴즈를 `data/state.json`에 저장

### 5.3 퀴즈 목록
- 등록된 퀴즈의 번호, 질문 및 선택지 목록 확인 (**정답은 표시하지 않음**)
- 등록된 문제가 없으면 안내 메시지 표시

### 5.4 퀴즈 삭제
- 목록 번호를 선택한 뒤 삭제 여부 확인(`y`/`n`, 그 외 입력은 재입력)
- 삭제된 결과를 `data/state.json`에 저장

### 5.5 최고 점수 확인
- **10 / 20 / 30문제 모드별** 최고 **최종 점수(0~100점)** 표시
- 아직 플레이하지 않은 모드는 기록 없음 안내

### 5.6 점수 기록 히스토리
- 게임 완료 날짜/시간, 모드(문제 수), 정답 수, 힌트 사용 수, 최종 점수 저장
- 지난 플레이 기록 조회

### 5.7 데이터 저장 및 불러오기
- `data/state.json`: 퀴즈와 힌트
- `data/scores.json`: 모드별 최고 점수 및 플레이 기록
- 첫 실행 시 기본 퀴즈 30개와 초기 점수 데이터 생성
- 퀴즈 추가·삭제·게임 완료 시점마다 즉시 저장
- 파일별 누락·손상·읽기/쓰기 오류를 독립적으로 처리

### 5.8 예외 처리
- 입력 앞뒤 공백 제거, 빈 입력·문자·범위 초과 시 재입력
- 번호 그대로의 숫자만 인정 (`02`, `+2` 등은 거부)
- `KeyboardInterrupt`, `EOFError` 발생 시 안내 메시지 출력 후 종료 (데이터는 변경 시점마다 이미 저장됨)
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
├── docs/
│   ├── 01_요구사항_및_설계.md
│   ├── 02_Git_작업_기록.md
│   ├── learning/
│   │   └── learning_notes.md   # 과제 목표 개념 정리
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
| `data/state.json` | 퀴즈 문제, 보기, 정답 번호, 힌트 |
| `data/scores.json` | 모드별 최고 점수 및 게임별 플레이 기록 |

> **과제 원문과의 차이(의도된 설계):** 원래 미션은 프로젝트 루트의 `state.json` 한 파일에 퀴즈와 최고 점수를 함께 저장하도록 되어 있습니다. 이 프로젝트는 성격이 다른 데이터를 한 파일에 섞지 않기 위해 **의도적으로 2개 파일로 분리**했습니다.
>
> - `state.json`은 사용자가 추가·삭제할 때만 바뀌는 **문제 콘텐츠**, `scores.json`은 게임마다 쌓이는 **플레이 결과**입니다.
> - 한쪽 파일이 손상되어 초기화되더라도 다른 쪽 데이터(예: 직접 추가한 퀴즈)는 유지됩니다.

### 7.2 JSON 데이터 구조

**`data/state.json` 예시**

```json
{
  "quizzes": [
    {
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
  "best_scores": {"10": 90, "20": null, "30": null},
  "history": [
    {
      "date": "2026-11-10 10:00:00",
      "total_questions": 10,
      "correct_answers": 9,
      "hints_used": 1,
      "score": 90
    }
  ]
}
```

- `best_scores` 초기값: 모든 모드 `null` (플레이 기록 없음), 키는 JSON 규칙상 문자열(`"10"`)
- 점수 계산: `(정답 수 × 100 - 힌트를 사용하고 맞힌 문제 수 × 10) / 출제 문제 수`를 정수로 변환하여 저장(반올림 방식은 구현하면서 결정, 동점은 최고 점수 갱신 아님)
- `hints_used`: 전체 힌트 사용 횟수이며, **힌트 사용 후 정답 처리된 문항 수**는 감점 계산 시 별도로 셉니다.
- `"quizzes": []`(퀴즈 전부 삭제)는 정상 상태로 취급하며 기본 문제를 되살리지 않습니다.

### 7.3 데이터 저장 및 복구 방식

- `encoding='utf-8'`, `ensure_ascii=False`, `indent=2` 사용
- 파일이 없으면 해당 파일의 초기값만 생성
- JSON 문법·구조·내용이 손상되면 안내 후 해당 파일만 초기화
- 읽기 권한·입출력 오류는 안내만 하고 파일을 덮어쓰지 않음
- 저장 실패 시 오류 안내

자세한 판단 기준은 [docs/01_요구사항_및_설계.md](docs/01_요구사항_및_설계.md) 6.2절 참고.

## 8. 기능 검증 및 실행 결과

> 실제 구현·테스트 완료 후 날짜, 명령어, 결과 및 스크린샷을 기록합니다. 아래는 **증빙 예정 목록**입니다.

- [ ] 메뉴 화면 — `docs/screenshots/menu.png`
- [ ] 랜덤 출제 및 문제 수 선택, 힌트 — `docs/screenshots/play.png`
- [ ] 퀴즈 추가 — `docs/screenshots/add_quiz.png`
- [ ] 목록 및 삭제 — `docs/screenshots/quiz_list.png`, `docs/screenshots/delete_quiz.png`
- [ ] 최고 점수 및 히스토리 — `docs/screenshots/score.png`, `docs/screenshots/history.png`
- [ ] 오류 입력 및 데이터 복구 — 증빙 추가 예정
- [ ] 개발 환경(VSCode, `python --version`, `git config --list`) — `docs/screenshots/environment.png`

## 9. Git 작업 이력

- 기능 단위 **의미 있는 커밋 10개 이상** 목표
- 별도 브랜치에서 퀴즈 풀기 기능 개발 후 `main` 병합
- `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 사용 증빙
- `clone`한 별도 디렉터리에서 수정·push → 원래 디렉터리에서 pull 실습
- `git log --oneline --graph --all` 캡처: `docs/screenshots/git_log.png`

**제출 전 할 일**

- [ ] `git init` 실습 및 캡처 (이 저장소는 `clone`으로 시작했으므로 별도 실습 필요)
- [ ] `git log --oneline --graph` 스크린샷

진행 상황은 [docs/02_Git_작업_기록.md](docs/02_Git_작업_기록.md)에 실제 실행한 내용만 기록합니다.

## 10. 학습 정리

과제 목표(Python 기초, 클래스, 파일 입출력, Git)의 개념과 이 프로젝트 코드에서 쓰인 위치: [docs/learning/learning_notes.md](docs/learning/learning_notes.md)
