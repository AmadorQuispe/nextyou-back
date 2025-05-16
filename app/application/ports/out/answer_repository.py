
from typing import Protocol


class AnswerRepository(Protocol):
    def find_all_by_user_id(self, user_id):
        pass