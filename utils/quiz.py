import json
from abc import ABC, abstractmethod


with open("utils/questions.json", 'r', encoding='utf-8') as f:
    questions = json.loads(f.read())


class QuizIterator(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    def __init__(self) -> None:
        self.limit = len(questions)
        self.counter = 0

    @abstractmethod
    def __next__(self):
        if self.counter < self.limit:
            self.counter += 1
        else:
            raise StopIteration


class QuestionIterator(QuizIterator):

    def __iter__(self):
        return self

    def __next__(self) -> str:
        super().__next__()
        return f"{questions[str(self.counter)]['text']}"


class OptionsIterator(QuizIterator):

    def __iter__(self):
        return self

    def __next__(self) -> list:
        super().__next__()
        return questions[str(self.counter)]['options']


class AnswersIterator(QuizIterator):

    def __iter__(self):
        return self

    def __next__(self) -> str:
        super().__next__()
        return f"{questions[str(self.counter)]['correct_answer']}"
