from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()


class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    NUMBERS = "numbers"
    SHORT_ANSWER = "short_answer"
    THIS_OR_THAT = "this_or_that"

    def to_slide_component(self):
        # TODO: implement this
        if self == QuestionType.MULTIPLE_CHOICE:
            return "multiple_choice"
        elif self == QuestionType.NUMBERS:
            return "numbers"
        elif self == QuestionType.SHORT_ANSWER:
            return "short_answer"
        elif self == QuestionType.THIS_OR_THAT:
            return "this_or_that"

    def to_str(self):
        return self.value
