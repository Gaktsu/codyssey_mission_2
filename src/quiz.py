"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""

CHOICE_COUNT = 4


# 문제 하나의 데이터(질문, 선택지, 정답, 힌트)와 그 데이터를 다루는 동작(출력, 정답 확인)을 묶는다.
# 힌트를 썼는지 같은 "이번 게임"의 상태는 문제 자체의 정보가 아니므로 여기에 두지 않는다.
class Quiz:
    def __init__(self, question, choices, answer, hint):
        # 객체를 만드는 순간 값을 검사해, 잘못된 퀴즈 객체가 아예 만들어지지 않게 한다.
        # 기본 퀴즈 생성, 퀴즈 추가, 파일 불러오기가 모두 이 검사를 거치므로 규칙이 한 곳에만 있다.
        # 파일을 불러올 때 이 ValueError가 나면 그 파일을 손상된 것으로 판단할 수 있다.
        if not isinstance(question, str) or not question.strip():
            raise ValueError("질문이 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 {CHOICE_COUNT}개여야 합니다.")
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("비어 있는 선택지가 있습니다.")
        # bool은 int의 하위 타입이라 isinstance(True, int)가 참이 된다.
        # JSON의 true가 정답 1로 통과하지 않도록 type()으로 정확히 int인지 확인한다.
        if type(answer) is not int or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답은 1~{CHOICE_COUNT} 사이의 번호여야 합니다.")
        if not isinstance(hint, str) or not hint.strip():
            raise ValueError("힌트가 비어 있습니다.")

        # 검사를 통과한 값을 이 객체의 속성으로 저장해 다른 메서드에서 self.question 등으로 쓴다.
        self.question = question
        self.choices = choices        # 순서대로 1~4번에 대응하므로 list
        self.answer = answer          # 사용자가 입력하는 번호와 바로 비교하도록 1~4의 int
        self.hint = hint

    def display(self, number):
        """문제 번호, 질문, 선택지 1~4를 출력한다."""
        print(f"\n[문제 {number}]")
        print(self.question)
        # 선택지 4개를 차례로 출력하므로 for. enumerate(start=1)로 사용자에게 보여줄 1~4 번호를 붙인다.
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def check_answer(self, selected):
        """선택한 번호가 정답이면 True, 아니면 False."""
        # 출력은 하지 않고 판단만 해서 돌려준다. 정답/오답 안내와 점수 계산은 호출한 쪽에서 한다.
        return selected == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict로 변환한다."""
        # json 모듈은 Quiz 객체를 직접 저장할 수 없어(TypeError) dict로 바꿔서 넘긴다.
        # dict의 키 이름이 그대로 JSON 키가 되어 파일을 열어 봐도 각 값의 의미를 알 수 있다.
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    # 파일에서 읽은 dict로 "새 객체를 만드는" 메서드라 아직 객체가 없는 상태에서 호출해야 한다.
    # 그래서 self 대신 클래스 자체(cls)를 받는 classmethod로 만들고 Quiz.from_dict(data)로 호출한다.
    @classmethod
    def from_dict(cls, data):
        """JSON에서 읽은 dict로 Quiz를 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"], data["hint"])
        # 키가 빠진 경우(KeyError)도 ValueError로 바꿔, 불러오는 쪽에서 "손상"을 한 종류로만 처리하게 한다.
        except KeyError as error:
            raise ValueError(f"퀴즈 데이터에 {error} 항목이 없습니다.") from None
