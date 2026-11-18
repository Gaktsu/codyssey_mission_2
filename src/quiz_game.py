import json
import random
from datetime import datetime
from pathlib import Path

from src.default_quizzes import create_default_quizzes
from src.input_utils import read_initials, read_int, read_text, read_yes_no
from src.quiz import CHOICE_COUNT, Quiz

DATA_DIR = Path("data")
STATE_FILE = DATA_DIR / "state.json"
SCORES_FILE = DATA_DIR / "scores.json"

MODES = ("10", "20", "30")
MAX_RECORDS = 10
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

EXIT_CHOICE = 7


def create_empty_records():
    return {mode: {"best_score": None, "scores": []} for mode in MODES}


def check_name(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("이름(이니셜)이 비어 있습니다.")


def check_score(value):
    if type(value) is not int or not 0 <= value <= 100:
        raise ValueError("점수는 0~100 사이의 정수여야 합니다.")


def validate_scores(data):
    if not isinstance(data, dict) or not isinstance(data.get("mode"), dict):
        raise ValueError("mode 항목이 없습니다.")
    for mode in MODES:
        record = data["mode"].get(mode)
        if not isinstance(record, dict) or not isinstance(record.get("scores"), list):
            raise ValueError(f"{mode}문제 모드 기록 형식이 올바르지 않습니다.")

        best = record.get("best_score")
        if best is not None:
            if not isinstance(best, dict):
                raise ValueError(f"{mode}문제 모드 최고 점수 형식이 올바르지 않습니다.")
            check_name(best.get("name"))
            check_score(best.get("score"))

        for entry in record["scores"]:
            if not isinstance(entry, dict):
                raise ValueError(f"{mode}문제 모드 기록 형식이 올바르지 않습니다.")
            try:
                datetime.strptime(entry.get("date"), DATE_FORMAT)
            except (TypeError, ValueError):
                raise ValueError("기록의 날짜 형식이 올바르지 않습니다.") from None
            check_name(entry.get("name"))
            total = entry.get("total_questions")
            if type(total) is not int or total < 0:
                raise ValueError("푼 문제 수는 0 이상의 정수여야 합니다.")
            check_score(entry.get("score"))


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.records = {}
        self.load_quizzes()
        self.load_scores()
        print(f"\n📂 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

    # ---------- 메뉴 ----------

    def show_menu(self):
        print(MENU)

    # 메뉴를 출력, 선택을 하는 함수
    def run(self):
        while True:
            self.show_menu()
            choice = read_int("메뉴 번호를 입력하세요: ", 1, EXIT_CHOICE)
            if choice == 1:
                self.play_game()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_score()
            elif choice == 6:
                self.show_history()
            else:
                print("프로그램을 종료합니다.")
                return

    # ---------- 1. 퀴즈 풀기 ----------

    def play_game(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        count = self.select_mode()
        if count is None:
            return

        questions = random.sample(self.quizzes, count)
        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")

        correct, hints_used, hint_correct = self.ask_questions(questions)
        score = self.calculate_score(count, correct, hint_correct)
        self.show_result(count, correct, hints_used, score)

        name = read_initials()
        if self.record_score(count, name, score):
            print("🎉 새로운 최고 점수입니다!")

    def select_mode(self):
        print("\n[모드 선택]")
        for i in range(len(MODES)):
            print(f"{i + 1}. {MODES[i]}문제")
        print("0. 돌아가기")
        while True:
            choice = read_int("모드를 선택하세요: ", 0, len(MODES))
            if choice == 0:
                return None
            count = int(MODES[choice - 1])
            if count <= len(self.quizzes):
                return count
            print(f"등록된 퀴즈가 {len(self.quizzes)}개라 {count}문제 모드는 할 수 없습니다.")

    def ask_questions(self, questions):
        correct = 0
        hints_used = 0
        hint_correct = 0
        for i in range(len(questions)):
            quiz = questions[i]
            print("-" * 40)
            quiz.display(i + 1)
            selected, used_hint = self.ask_answer_or_hint(quiz)
            if used_hint:
                hints_used += 1

            if quiz.check_answer(selected):
                correct += 1
                if used_hint:
                    hint_correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}")
        return correct, hints_used, hint_correct

    def ask_answer_or_hint(self, quiz):
        used_hint = False
        while True:
            selected = read_int("정답 입력 (1~4, 힌트: 0): ", 0, 4)
            if selected != 0:
                return selected, used_hint
            if used_hint:
                print("이미 힌트를 사용했습니다.")
            used_hint = True
            print(f"💡 힌트: {quiz.hint}")

    def calculate_score(self, count, correct, hint_correct):
        return (correct * 100 - hint_correct * 10) // count

    def show_result(self, count, correct, hints_used, score):
        print("=" * 40)
        print(f"🏆 결과: {count}문제 중 {correct}문제 정답! (힌트 {hints_used}회 사용)")
        print(f"점수: {score}점")
        print("=" * 40)

    def record_score(self, count, name, score):
        record = self.records[str(count)]
        best = record["best_score"]
        is_new_best = best is None or score > best["score"]
        if is_new_best:
            record["best_score"] = {"name": name, "score": score}

        record["scores"].append({
            "date": datetime.now().strftime(DATE_FORMAT),
            "name": name,
            "total_questions": count,
            "score": score,
        })
        record["scores"] = record["scores"][-MAX_RECORDS:]

        self.save_scores()
        return is_new_best

    # ---------- 2. 퀴즈 추가 ----------

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1~{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = read_text("힌트를 입력하세요: ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_quizzes():
            print(f"✅ 퀴즈가 추가되었습니다! (총 {len(self.quizzes)}개)")
        else:
            print("추가한 퀴즈는 프로그램을 종료하면 사라집니다.")

    # ---------- 3. 퀴즈 목록 ----------

    def list_quizzes(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i in range(len(self.quizzes)):
            quiz = self.quizzes[i]
            print(f"[{i + 1}] {quiz.question}")
            print("    " + " / ".join(quiz.choices))
        print("-" * 40)

    # ---------- 4. 퀴즈 삭제 ----------

    def delete_quiz(self):
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_int(f"삭제할 퀴즈 번호 (1~{len(self.quizzes)}, 취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return

        quiz = self.quizzes[number - 1]
        print(f"\n[{number}] {quiz.question}")
        if not read_yes_no("이 퀴즈를 삭제할까요? (y/n): "):
            print("삭제를 취소했습니다.")
            return

        self.quizzes.pop(number - 1)
        if self.save_quizzes():
            print(f"🗑️ 퀴즈가 삭제되었습니다. (남은 퀴즈 {len(self.quizzes)}개)")
        else:
            print("삭제한 내용은 프로그램을 종료하면 되돌아갑니다.")

    # ---------- 5. 최고 점수 ----------

    def show_score(self):
        print("\n🏆 모드별 최고 점수")
        print("-" * 40)
        for mode in MODES:
            best = self.records[mode]["best_score"]
            if best is None:
                print(f"{mode}문제: 기록 없음")
            else:
                print(f"{mode}문제: {best['score']}점 ({best['name']})")
        print("-" * 40)

    # ---------- 6. 점수 기록 ----------

    def show_history(self):
        print("\n📜 점수 기록 (모드별 최근 10개)")
        for mode in MODES:
            scores = self.records[mode]["scores"]
            print("-" * 40)
            print(f"[{mode}문제]")
            if not scores:
                print("  기록 없음")
                continue
            for entry in reversed(scores):
                print(f"  {entry['date']}  {entry['name']:<3}  "
                      f"{entry['total_questions']}문제  {entry['score']}점")
        print("-" * 40)

    # ---------- 데이터 불러오기 / 저장 ----------

    def load_quizzes(self):
        try:
            with open(STATE_FILE, encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("quizzes 목록이 없습니다.")
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            return
        except FileNotFoundError:
            print("⚠️ 퀴즈 파일이 없어 기본 퀴즈로 시작합니다.")
        except ValueError as error:
            print(f"⚠️ 퀴즈 파일이 손상되어 기본 퀴즈로 시작합니다. ({error})")
        except OSError as error:
            print(f"⚠️ 퀴즈 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. ({error.strerror})")
        self.quizzes = create_default_quizzes()

    def load_scores(self):
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
            print(f"⚠️ 점수 파일을 읽을 수 없어 빈 기록으로 시작합니다. ({error.strerror})")
            self.records = create_empty_records()
            return
        self.records = create_empty_records()
        self.save_scores()

    def save_quizzes(self):
        data = {"quizzes": [quiz.to_dict() for quiz in self.quizzes]}
        return self.write_json(STATE_FILE, data)

    def save_scores(self):
        return self.write_json(SCORES_FILE, {"mode": self.records})

    def write_json(self, path, data):
        try:
            DATA_DIR.mkdir(exist_ok=True)
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except OSError as error:
            print(f"⚠️ {path.name} 저장에 실패했습니다. ({error.strerror})")
            return False
