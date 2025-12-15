from abc import ABC, abstractmethod
from datetime import datetime
class InteractionBase(ABC):

    def __init__(self, interaction_id: str, user_id: str):
        self.interaction_id = interaction_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.status = "active"   

    def is_active(self) -> bool:
        return self.status == "active"

    def is_deleted(self) -> bool:
        return self.status == "deleted"

    def mark_as_deleted(self) -> None:
        self.status = "deleted"

    def restore(self) -> None:
        self.status = "active"

    def get_age_in_seconds(self) -> float:
        delta = datetime.now() - self.created_at
        return delta.total_seconds()