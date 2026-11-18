from src.quiz_game import QuizGame


def main():
    try:
        QuizGame().run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
