CHOICE_COUNT = 4


class Quiz:
    def __init__(self, question, choices, answer, hint):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("질문이 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 {CHOICE_COUNT}개여야 합니다.")
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("비어 있는 선택지가 있습니다.")
        if type(answer) is not int or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답은 1~{CHOICE_COUNT} 사이의 번호여야 합니다.")
        if not isinstance(hint, str) or not hint.strip():
            raise ValueError("힌트가 비어 있습니다.")

        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number):
        print(f"\n[문제 {number}]")
        print(self.question)
        for i in range(len(self.choices)):
            print(f"  {i + 1}. {self.choices[i]}")

    def check_answer(self, selected):
        return selected == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"], data["hint"])
        except KeyError as error:
            raise ValueError(f"퀴즈 데이터에 {error} 항목이 없습니다.") from None
