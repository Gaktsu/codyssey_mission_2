def read_int(prompt, min_value, max_value):
    while True:
        text = input(prompt).strip()

        if not text:
            print("입력값이 없습니다. 다시 입력하세요.")
            continue

        if not (text.isascii() and text.isdigit()) or str(int(text)) != text:
            print("숫자로 된 번호만 입력하세요. (예: 3)")
            continue

        value = int(text)
        if not min_value <= value <= max_value:
            print(f"{min_value}~{max_value} 사이의 번호를 입력하세요.")
            continue

        return value


def read_initials():
    while True:
        text = input("이니셜을 입력하세요 (영문 1~3자): ").strip()
        if text.isascii() and text.isalpha() and 1 <= len(text) <= 3:
            return text.upper()
        print("영문 1~3글자로 입력하세요. (예: KMS)")


def read_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("내용이 비어 있습니다. 다시 입력하세요.")


def read_yes_no(prompt):
    while True:
        text = input(prompt).strip().lower()
        if text == "y":
            return True
        if text == "n":
            return False
        print("y 또는 n으로 입력하세요.")
