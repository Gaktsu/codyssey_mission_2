"""퀴즈 게임 전체 흐름 관리."""

import json
import random
from datetime import datetime
from pathlib import Path

from src.default_quizzes import create_default_quizzes
from src.input_utils import read_initials, read_int, read_text, read_yes_no
from src.quiz import CHOICE_COUNT, Quiz

# 실행 위치(현재 디렉터리)와 상관없이 항상 같은 파일을 찾도록
# 이 파일(src/quiz_game.py) 위치를 기준으로 프로젝트 루트의 data 폴더 경로를 계산한다.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATE_FILE = DATA_DIR / "state.json"    # 퀴즈 문제 (사용자가 추가·삭제할 때만 바뀜)
SCORES_FILE = DATA_DIR / "scores.json"  # 모드별 최고 점수와 기록 (게임마다 쌓임)
# 문제 콘텐츠와 플레이 결과는 바뀌는 시점과 성격이 달라 파일을 나눴다.
# 한쪽 파일이 손상되어도 다른 쪽 데이터(예: 직접 추가한 퀴즈)는 영향을 받지 않는다.

MODES = ("10", "20", "30")   # JSON 객체의 키는 문자열만 가능하므로 모드도 문자열로 둔다
MAX_RECORDS = 10             # 모드별 기록은 최근 10개까지만 보관
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

MENU = """
========== Linux / Docker / Git 퀴즈 ==========
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 퀴즈 삭제
5. 최고 점수
6. 점수 기록
7. 종료
================================================"""

# 종료 메뉴 번호. 숫자 7을 여러 곳에 직접 쓰지 않고 이름을 붙여 의미를 드러내고,
# 메뉴 구성이 바뀌어도 이 값만 고치면 되게 한다.
EXIT_CHOICE = 7


def create_empty_records():
    """아직 아무도 플레이하지 않은 상태의 모드별 기록."""
    return {mode: {"best_score": None, "scores": []} for mode in MODES}


def check_name(value):
    # 이니셜은 비어 있지 않은 문자열이어야 한다 (null 불가)
    if not isinstance(value, str) or not value.strip():
        raise ValueError("이름(이니셜)이 비어 있습니다.")


def check_score(value):
    # bool은 int의 하위 타입이라 True/False가 통과하지 않도록 type()으로 확인
    if type(value) is not int or not 0 <= value <= 100:
        raise ValueError("점수는 0~100 사이의 정수여야 합니다.")


def validate_scores(data):
    """scores.json 내용이 올바른지 검사한다. 문제가 있으면 ValueError."""
    if not isinstance(data, dict) or not isinstance(data.get("mode"), dict):
        raise ValueError("mode 항목이 없습니다.")
    for mode in MODES:
        record = data["mode"].get(mode)
        if not isinstance(record, dict) or not isinstance(record.get("scores"), list):
            raise ValueError(f"{mode}문제 모드 기록 형식이 올바르지 않습니다.")

        # best_score가 null이면 아직 이 모드를 플레이하지 않은 것 → 정상
        best = record.get("best_score")
        if best is not None:
            if not isinstance(best, dict):
                raise ValueError(f"{mode}문제 모드 최고 점수 형식이 올바르지 않습니다.")
            check_name(best.get("name"))
            check_score(best.get("score"))

        for entry in record["scores"]:
            if not isinstance(entry, dict):
                raise ValueError(f"{mode}문제 모드 기록 형식이 올바르지 않습니다.")
            # 날짜에 년/월/일(과 시각)이 정해진 형식으로 들어 있는지 확인
            try:
                datetime.strptime(entry.get("date"), DATE_FORMAT)
            except (TypeError, ValueError):
                raise ValueError("기록의 날짜 형식이 올바르지 않습니다.") from None
            check_name(entry.get("name"))
            total = entry.get("total_questions")
            if type(total) is not int or total < 0:
                raise ValueError("푼 문제 수는 0 이상의 정수여야 합니다.")
            check_score(entry.get("score"))


# 게임 전체 흐름(메뉴, 각 기능 실행)과 데이터 저장/불러오기를 담당한다.
# 문제 하나의 데이터와 동작은 Quiz가 담당한다.
class QuizGame:
    def __init__(self):
        # 객체를 만들 때 두 파일을 각각 불러와 속성을 준비한다.
        # 한 파일의 오류 처리가 다른 파일에 영향을 주지 않도록 메서드를 나눴다.
        self.quizzes = []   # Quiz 객체 목록
        self.records = {}   # 모드("10"/"20"/"30")별 {"best_score": ..., "scores": [...]}
        self.load_quizzes()
        self.load_scores()
        print(f"\n📂 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

    def load_quizzes(self):
        """state.json에서 퀴즈를 불러온다. 문제가 있으면 기본 퀴즈로 시작한다."""
        try:
            with open(STATE_FILE, encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("quizzes 목록이 없습니다.")
            # 항목 하나라도 잘못되면 Quiz()가 ValueError를 내므로 파일 전체를 손상으로 본다
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            return
        except FileNotFoundError:
            print("⚠️ 퀴즈 파일이 없어 기본 퀴즈로 시작합니다.")
        # json.JSONDecodeError(JSON 문법 오류)도 ValueError의 하위 클래스라 여기서 함께 처리된다
        except ValueError as error:
            print(f"⚠️ 퀴즈 파일이 손상되어 기본 퀴즈로 시작합니다. ({error})")
        # 권한 오류 등 파일을 읽을 수 없는 경우 (FileNotFoundError는 위에서 먼저 처리됨)
        except OSError as error:
            print(f"⚠️ 퀴즈 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. ({error.strerror})")
        # state.json은 사용자가 직접 넣은 문제가 들어 있는 파일이라 여기서 덮어쓰지 않는다.
        # 기본 퀴즈는 메모리에서만 사용하고, 퀴즈를 추가·삭제할 때 저장된다.
        self.quizzes = create_default_quizzes()

    def load_scores(self):
        """scores.json에서 기록을 불러온다. 없거나 손상되면 빈 기록으로 새로 만든다."""
        try:
            with open(SCORES_FILE, encoding="utf-8") as file:
                data = json.load(file)
            validate_scores(data)
            self.records = data["mode"]
            return
        except FileNotFoundError:
            print("📄 점수 파일이 없어 새로 만듭니다.")
        except ValueError as error:
            print(f"⚠️ 점수 파일이 손상되어 초기화합니다. ({error})")
        except OSError as error:
            # 읽을 수 없는 파일은 덮어쓰지 않고 이번 실행만 빈 기록으로 진행한다
            print(f"⚠️ 점수 파일을 읽을 수 없어 빈 기록으로 시작합니다. ({error.strerror})")
            self.records = create_empty_records()
            return
        # 점수 파일은 플레이 결과만 담고 있어, 없거나 손상되면 빈 기록으로 바로 다시 만든다
        self.records = create_empty_records()
        self.save_scores()

    def save_quizzes(self):
        """현재 퀴즈 목록을 state.json에 저장한다. 성공하면 True."""
        # Quiz 객체는 JSON으로 바로 저장할 수 없어 to_dict()로 dict로 바꾼다
        data = {"quizzes": [quiz.to_dict() for quiz in self.quizzes]}
        return self.write_json(STATE_FILE, data)

    def save_scores(self):
        """현재 모드별 기록을 scores.json에 저장한다. 성공하면 True."""
        return self.write_json(SCORES_FILE, {"mode": self.records})

    def write_json(self, path, data):
        # 두 파일의 저장 방식이 같으므로 한 메서드로 묶었다.
        # 성공 여부를 bool로 돌려줘, 호출한 쪽이 저장에 성공했을 때만 완료 안내를 하게 한다.
        try:
            DATA_DIR.mkdir(exist_ok=True)  # data 폴더가 없으면 만든다
            # ensure_ascii=False: 한글을 \uXXXX로 바꾸지 않고 그대로 저장 / indent=2: 읽기 쉽게 들여쓰기
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except OSError as error:
            print(f"⚠️ {path.name} 저장에 실패했습니다. ({error.strerror})")
            return False

    def run(self):
        # 메뉴 번호(int)를 키로, 실행할 메서드를 값으로 둔 dict.
        # if/elif를 6번 나열하지 않고 actions[choice]()로 번호에 맞는 기능을 바로 실행한다.
        # self.play_game처럼 괄호 없이 쓰면 메서드를 "호출"하지 않고 메서드 자체를 값으로 담는다.
        actions = {
            1: self.play_game,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.delete_quiz,
            5: self.show_score,
            6: self.show_history,
        }
        # 사용자가 종료를 고를 때까지 몇 번 반복할지 모르므로 while True.
        # Ctrl+C / EOF는 여기서 잡지 않고 main.py로 전달되어 안내 후 종료된다.
        while True:
            print(MENU)
            choice = read_int("메뉴 번호를 입력하세요: ", 1, EXIT_CHOICE)
            if choice == EXIT_CHOICE:
                print("프로그램을 종료합니다.")
                return
            actions[choice]()

    def play_game(self):
        """모드를 고르고 랜덤으로 출제한 뒤, 점수를 계산하고 기록한다."""
        # 퀴즈가 하나도 없으면 어떤 모드도 할 수 없으므로 모드를 묻지 않고 바로 돌아간다
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        count = self.select_mode()
        if count is None:  # 0(돌아가기)을 고른 경우
            return

        # random.sample: 목록에서 count개를 "중복 없이" 무작위로 뽑는다 (원본 목록은 바뀌지 않음)
        questions = random.sample(self.quizzes, count)
        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")

        correct = 0       # 맞힌 문제 수
        hints_used = 0    # 힌트를 사용한 문제 수
        hint_correct = 0  # 힌트를 쓰고 맞힌 문제 수 (감점 대상)
        # 출제할 문제가 정해져 있으므로 for. enumerate(start=1)로 [문제 1]부터 번호를 붙인다
        for number, quiz in enumerate(questions, start=1):
            print("-" * 40)
            quiz.display(number)
            selected, used_hint = self.ask_answer_or_hint(quiz)
            if used_hint:
                hints_used += 1

            if quiz.check_answer(selected):
                correct += 1
                if used_hint:
                    hint_correct += 1
                print("✅ 정답입니다!")
            else:
                # quiz.answer는 1~4, 리스트 인덱스는 0부터라 1을 뺀다
                print(f"❌ 오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}")

        # 정답 1문제 = 100점, 힌트를 쓰고 맞히면 90점, 오답 0점 → 평균을 100점 만점으로.
        # 미션에 실수 요구가 없어 정수 나눗셈(//)으로 소수점 아래를 버린다. 예: 22.5 → 22
        score = (correct * 100 - hint_correct * 10) // count

        print("=" * 40)
        print(f"🏆 결과: {count}문제 중 {correct}문제 정답! (힌트 {hints_used}회 사용)")
        print(f"점수: {score}점")
        print("=" * 40)

        name = read_initials()
        if self.record_score(count, name, score):
            print("🎉 새로운 최고 점수입니다!")

    def select_mode(self):
        """10/20/30문제 모드를 고르게 한다. 문제 수를 돌려주고, 돌아가기면 None."""
        print("\n[모드 선택]")
        # MODES의 순서대로 1, 2, 3 번호를 붙여 보여준다
        for index, mode in enumerate(MODES, start=1):
            print(f"{index}. {mode}문제")
        print("0. 돌아가기")
        # 퀴즈가 부족한 모드를 고르면 다시 골라야 하므로, 끝나는 시점을 모르는 while
        while True:
            choice = read_int("모드를 선택하세요: ", 0, len(MODES))
            if choice == 0:
                return None
            count = int(MODES[choice - 1])
            # random.sample은 목록보다 많이 뽑을 수 없으므로(ValueError) 미리 막는다
            if count <= len(self.quizzes):
                return count
            print(f"등록된 퀴즈가 {len(self.quizzes)}개라 {count}문제 모드는 할 수 없습니다.")

    def ask_answer_or_hint(self, quiz):
        """정답(1~4)을 받을 때까지 묻는다. 0을 입력하면 힌트를 보여준다.

        (선택한 번호, 힌트 사용 여부)를 돌려준다.
        """
        used_hint = False
        while True:
            # 힌트 요청을 0으로 받아 정답 입력과 같은 read_int 하나로 처리한다
            selected = read_int("정답 입력 (1~4, 힌트: 0): ", 0, 4)
            if selected != 0:
                return selected, used_hint
            if used_hint:
                # 감점은 처음 한 번만. 다시 요청하면 안내만 하고 힌트는 다시 보여준다
                print("이미 힌트를 사용했습니다.")
            used_hint = True
            print(f"💡 힌트: {quiz.hint}")

    def record_score(self, count, name, score):
        """모드별 기록에 이번 결과를 추가하고 저장한다. 최고 점수를 넘었으면 True."""
        record = self.records[str(count)]  # JSON 키가 문자열이라 str로 바꿔 찾는다
        best = record["best_score"]
        # 아직 기록이 없거나(None) 기존 최고 점수보다 높을 때만 갱신 (동점은 기존 기록 유지)
        is_new_best = best is None or score > best["score"]
        if is_new_best:
            record["best_score"] = {"name": name, "score": score}

        record["scores"].append({
            "date": datetime.now().strftime(DATE_FORMAT),
            "name": name,
            "total_questions": count,
            "score": score,
        })
        # 최근 기록 10개만 남긴다. [-10:]은 리스트의 마지막 10개 (10개 이하면 전부)
        record["scores"] = record["scores"][-MAX_RECORDS:]

        # 저장에 실패하면 save_scores()가 실패 안내를 출력한다
        self.save_scores()
        return is_new_best

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호, 힌트를 입력받아 퀴즈를 추가하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        # 선택지 개수만큼 같은 입력을 반복하므로 리스트 컴프리헨션으로 한 번에 모은다
        choices = [read_text(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1~{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = read_text("힌트를 입력하세요: ")

        # 입력 단계에서 이미 검증했으므로 Quiz()의 검사도 통과한다
        self.quizzes.append(Quiz(question, choices, answer, hint))
        # 저장에 성공했을 때만 완료 안내 (실패하면 save_quizzes()가 실패 안내를 출력)
        if self.save_quizzes():
            print(f"✅ 퀴즈가 추가되었습니다! (총 {len(self.quizzes)}개)")
        else:
            print("추가한 퀴즈는 프로그램을 종료하면 사라집니다.")

    def list_quizzes(self):
        """등록된 퀴즈의 번호, 질문, 선택지를 출력한다. 정답은 보여주지 않는다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        # 별도 ID 없이 리스트 순서대로 1부터 번호를 붙인다. 삭제할 때도 이 번호를 사용한다
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
            # 플레이 전에 정답이 노출되지 않도록 선택지만 보여준다 (정답 표시 없음)
            print("    " + " / ".join(quiz.choices))
        print("-" * 40)

    def delete_quiz(self):
        """목록 번호로 퀴즈를 골라 확인 후 삭제하고 저장한다."""
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return
        # 삭제할 번호를 고를 수 있도록 목록을 먼저 보여준다
        self.list_quizzes()
        number = read_int(f"삭제할 퀴즈 번호 (1~{len(self.quizzes)}, 취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return

        # 목록 번호는 1부터, 리스트 인덱스는 0부터라 1을 뺀다
        quiz = self.quizzes[number - 1]
        print(f"\n[{number}] {quiz.question}")
        # 실수로 지우는 것을 막기 위해 한 번 더 확인한다
        if not read_yes_no("이 퀴즈를 삭제할까요? (y/n): "):
            print("삭제를 취소했습니다.")
            return

        # pop(인덱스): 해당 위치의 항목을 리스트에서 꺼내 제거한다
        self.quizzes.pop(number - 1)
        # 저장에 성공했을 때만 완료 안내 (실패하면 save_quizzes()가 실패 안내를 출력)
        if self.save_quizzes():
            print(f"🗑️ 퀴즈가 삭제되었습니다. (남은 퀴즈 {len(self.quizzes)}개)")
        else:
            print("삭제한 내용은 프로그램을 종료하면 되돌아갑니다.")

    def show_score(self):
        """10/20/30문제 모드별 최고 점수와 이니셜을 보여준다."""
        print("\n🏆 모드별 최고 점수")
        print("-" * 40)
        # 모드가 3개로 정해져 있으므로 for로 차례대로 출력한다
        for mode in MODES:
            best = self.records[mode]["best_score"]
            # best_score가 None(null)이면 아직 이 모드를 플레이하지 않은 것
            if best is None:
                print(f"{mode}문제: 기록 없음")
            else:
                print(f"{mode}문제: {best['score']}점 ({best['name']})")
        print("-" * 40)

    def show_history(self):
        """모드별 최근 플레이 기록(최대 10개)을 최신순으로 보여준다."""
        print("\n📜 점수 기록 (모드별 최근 10개)")
        for mode in MODES:
            scores = self.records[mode]["scores"]
            print("-" * 40)
            print(f"[{mode}문제]")
            if not scores:
                print("  기록 없음")
                continue
            # 기록은 오래된 것부터 쌓이므로 reversed()로 뒤집어 최신 기록부터 보여준다
            for entry in reversed(scores):
                print(f"  {entry['date']}  {entry['name']:<3}  "
                      f"{entry['total_questions']}문제  {entry['score']}점")
        print("-" * 40)
