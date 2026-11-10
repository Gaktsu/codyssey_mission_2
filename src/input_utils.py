"""공통 입력 처리."""


def read_int(prompt, min_value, max_value):
    """min_value~max_value 범위의 정수를 올바르게 입력할 때까지 반복해서 묻는다.

    앞뒤 공백은 제거하며, "02", "+2", "1_0"처럼 번호 그대로가 아닌 입력은 거부한다.
    KeyboardInterrupt / EOFError는 호출한 쪽에서 처리하도록 그대로 전달한다.
    """
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
