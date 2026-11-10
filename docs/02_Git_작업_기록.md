# Git 및 GitHub 작업 기록

> **원칙:** 이 문서의 명령어는 **실습 계획/예시**입니다. 실행하지 않은 명령이나 커밋을 완료했다고 기록하지 않습니다.

## 1. Git 저장소 초기화

### 1.1 로컬 저장소 설정

이미 GitHub 저장소가 만들어져 있으므로, 현재 로컬 폴더가 `git init`으로 시작했는지 `git clone`으로 시작했는지 **실제 이력에 따라** 기입합니다.

```bash
# 로컬에서 새 저장소를 시작한 경우에만
git init
```

- 실제 사용한 명령어:
- 실행 결과:
- 관련 스크린샷:

### 1.2 GitHub 원격 저장소 연결

```bash
git remote -v
# 필요할 때만: git remote add origin https://github.com/Gaktsu/codyssey_mission_2.git
```

- 실제 사용한 명령어 및 결과:

### 1.3 첫 Commit 및 Push

```bash
git status
git log --oneline -5
```

- 초기 커밋 해시/메시지:
- 최초 push 명령어/결과:

## 2. 기능별 커밋 기록

최소 10개 **의미 있는 커밋**을 목표로 합니다. 다음은 추천 메시지이며 실제 커밋 해시를 나중에 기록합니다.

| 작업 | 예시 커밋 메시지 | 실제 해시 | 상태 |
| --- | --- | --- | --- |
| 메뉴 | `Feat: 콘솔 메뉴와 종료 기능 구현` | - | 미기록 |
| 입력 검증 | `Feat: 공통 입력값 검증 추가` | - | 미기록 |
| Quiz 클래스 | `Feat: 퀴즈 데이터 모델과 정답 판정 구현` | - | 미기록 |
| 기본 퀴즈 | `Data: Linux Docker Git 기본 문제 추가` | - | 미기록 |
| 플레이 | `Feat: 퀴즈 플레이 기능 구현` | - | 미기록 |
| 랜덤 출제 | `Feat: 랜덤 출제와 문제 수 선택 추가` | - | 미기록 |
| 퀴즈 추가 | `Feat: 퀴즈 등록과 파일 저장 구현` | - | 미기록 |
| 퀴즈 목록 | `Feat: 퀴즈 목록 조회 구현` | - | 미기록 |
| 퀴즈 삭제 | `Feat: 퀴즈 삭제 구현` | - | 미기록 |
| 힌트 | `Feat: 힌트 기능과 점수 차감 구현` | - | 미기록 |
| 점수·히스토리 | `Feat: 최고 점수와 플레이 기록 저장` | - | 미기록 |
| 파일 복구 | `Fix: JSON 손상 및 저장 오류 처리` | - | 미기록 |
| 테스트 | `Test: 기능 및 예외 테스트 추가` | - | 미기록 |
| 문서 | `Docs: README와 검증 문서 보완` | - | 미기록 |

> 위 표는 예정 커밋 목록이지, 현재 GitHub 커밋 실적이 아닙니다. 이미 만든 문서 커밋은 실제 `git log`를 확인하여 별도 기록합니다.

## 3. 브랜치 작업

### 3.1 브랜치 생성

```bash
git checkout -b feature/quiz-play
```

- 작업 일시:
- 생성 결과:

### 3.2 브랜치에서 기능 개발 및 커밋

```bash
git add src/
git commit -m "Feat: 퀴즈 풀기 기능 구현"
```

- 실제 커밋 해시:
- 변경 파일 및 구현 내용:
- 검증 결과:

### 3.3 Main 브랜치 병합

```bash
git checkout main
git merge feature/quiz-play
```

- 병합 일시:
- 충돌 여부 및 해결 내용:

### 3.4 병합 결과 검증

```bash
git log --oneline --graph --all
git push origin main
```

- 결과:
- 스크린샷:

## 4. Clone 실습

### 4.1 별도 디렉터리 복제

```bash
# 기존 프로젝트 디렉터리의 상위 폴더에서 실행
git clone https://github.com/Gaktsu/codyssey_mission_2.git codyssey_mission_2_clone
cd codyssey_mission_2_clone
```

- 실행 일시:
- 실행 결과:

### 4.2 복제된 저장소 수정

- 실제 수정 내용(예: README 한 줄):

### 4.3 Commit 및 Push

```bash
git add README.md
git commit -m "Docs: clone 실습 변경사항 추가"
git push origin main
```

- 실제 커밋 해시:
- 실행 결과:

## 5. Pull 실습

### 5.1 원래 로컬 저장소에서 Pull

```bash
# 원래 로컬 프로젝트 폴더로 돌아간 뒤
git pull origin main
```

- 실행 일시:
- 실행 결과:

### 5.2 변경사항 반영 확인

```bash
git log --oneline -5
git status
```

- README 변경 확인 결과:
- 스크린샷:

## 6. Git 최종 검증

### 6.1 커밋 개수 및 명령어 수행 확인

```bash
git rev-list --count HEAD
git log --oneline --graph --all
```

| 검증 항목 | 실제 결과 |
| --- | --- |
| 의미 있는 커밋 10개 이상 | 미검증 |
| 새 브랜치 생성 | 미검증 |
| 브랜치 병합 | 미검증 |
| `git init` | 실제 수행 기록 확인 필요 |
| `git add/commit/push` | 실제 수행 기록 확인 필요 |
| `git checkout` | 미검증 |
| `git clone` | 미검증 |
| `git pull` | 미검증 |

### 6.2 Git Log 및 브랜치 그래프

- 증빙 이미지: `docs/screenshots/git_log.png`
- 촬영 시각:

### 6.3 GitHub 업로드 확인

- 저장소: https://github.com/Gaktsu/codyssey_mission_2
- 최종 확인 결과:
