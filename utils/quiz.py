import json


with open("utils/questions.json", 'r', encoding='utf-8') as f:
    questions = json.loads(f.read())


class QuizIterator:

    def __iter__(self):
        return self

    def __init__(self) -> None:
        self.limit = len(questions)
        self.counter = 0

    def __next__(self) -> str:
        if self.counter < self.limit:
            self.counter += 1
        else:
            raise StopIteration
        question = questions[str(self.counter)]['text']
        options = questions[str(self.counter)]['options']
        options_str = ', '.join(options)
        return f"{question}\n\nВарианты ответа: {options_str}"


class AnswersIterator:

    def __iter__(self):
        return self

    def __init__(self) -> None:
        self.limit = len(questions)
        self.counter = 0

    def __next__(self) -> str:
        if self.counter < self.limit:
            self.counter += 1
        else:
            raise StopIteration
        return f"{questions[str(self.counter)]['correct_answer']}"
