"""프로그램 진입점: 프로젝트 루트에서 `python -m src.main`으로 실행."""

from src.quiz_game import QuizGame


def main():
    try:
        QuizGame().run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
