"""퀴즈 게임 전체 흐름 관리."""

from src.input_utils import read_int

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


class QuizGame:
    def run(self):
        actions = {
            1: self.play_game,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.delete_quiz,
            5: self.show_score,
            6: self.show_history,
        }
        # Ctrl+C / EOF는 어느 화면에서든 main.py로 전달되어 안내 후 종료
        while True:
            print(MENU)
            choice = read_int("메뉴 번호를 입력하세요: ", 1, EXIT_CHOICE)
            if choice == EXIT_CHOICE:
                print("프로그램을 종료합니다.")
                return
            actions[choice]()

    def play_game(self):
        print("준비 중입니다.")

    def add_quiz(self):
        print("준비 중입니다.")

    def list_quizzes(self):
        print("준비 중입니다.")

    def delete_quiz(self):
        print("준비 중입니다.")

    def show_score(self):
        print("준비 중입니다.")

    def show_history(self):
        print("준비 중입니다.")
