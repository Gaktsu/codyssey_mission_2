"""공통 입력 처리."""


# 메뉴(1~7), 정답(1~4), 모드 선택, 삭제 번호가 모두 "범위 안의 정수를 받을 때까지 묻기"라는
# 같은 작업이라 함수 하나로 만들고 매개변수(안내 문구, 최솟값, 최댓값)만 바꿔 재사용한다.
# 검증 규칙을 바꿀 때도 이 함수만 고치면 된다.
def read_int(prompt, min_value, max_value):
    """min_value~max_value 범위의 정수를 올바르게 입력할 때까지 반복해서 묻는다.

    앞뒤 공백은 제거하며, "02", "+2", "1_0"처럼 번호 그대로가 아닌 입력은 거부한다.
    KeyboardInterrupt / EOFError는 호출한 쪽에서 처리하도록 그대로 전달한다.
    """
    # 사용자가 언제 올바른 값을 입력할지 모르므로 for가 아닌 while True로 반복하고,
    # 올바른 값이 들어오면 return으로 빠져나간다.
    while True:
        # input()은 항상 str을 돌려준다. " 2 "도 2로 처리하도록 앞뒤 공백을 제거한다.
        text = input(prompt).strip()

        # 빈 문자열("")은 거짓이므로 not text가 참 → 그냥 Enter를 친 경우
        if not text:
            print("입력값이 없습니다. 다시 입력하세요.")
            continue

        # int()에 "abc"를 넣으면 ValueError가 나므로, 숫자로만 이루어졌는지 먼저 확인한다.
        # isdigit()만 쓰면 아랍 숫자 같은 비ASCII 숫자도 통과하므로 isascii()를 함께 검사한다.
        # str(int("02"))는 "2"가 되어 원래 입력과 달라지므로 "02", "+2"처럼
        # 번호 그대로가 아닌 입력을 거부할 수 있다.
        if not (text.isascii() and text.isdigit()) or str(int(text)) != text:
            print("숫자로 된 번호만 입력하세요. (예: 3)")
            continue

        value = int(text)
        if not min_value <= value <= max_value:
            print(f"{min_value}~{max_value} 사이의 번호를 입력하세요.")
            continue

        # 오류 안내는 화면에만 보여주면 되므로 print, 입력값은 호출한 쪽에서 써야 하므로 return
        return value


def read_initials():
    """영문 1~3글자 이니셜을 올바르게 입력할 때까지 묻고, 대문자로 바꿔 돌려준다."""
    while True:
        text = input("이니셜을 입력하세요 (영문 1~3자): ").strip()
        # isalpha()만 쓰면 한글도 통과하므로 isascii()로 영문만 허용한다
        if text.isascii() and text.isalpha() and 1 <= len(text) <= 3:
            # kms, KMS, Kms를 같은 사람으로 보도록 대문자로 통일한다
            return text.upper()
        print("영문 1~3글자로 입력하세요. (예: KMS)")
