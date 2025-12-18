from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

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

    def set_status(self, status: str) -> None:
        allowed = ["active", "deleted", "flagged"]
        if status not in allowed:
            raise ValueError("Geçersiz durum değeri")
        self.status = status


    def get_age_in_seconds(self) -> float:
        delta = datetime.now() - self.created_at
        return delta.total_seconds()
    
    def  get_age_in_minutes(self) -> float:
        return self.get_age_in_seconds() / 60

    def get_age_in_hours(self) -> float:
        return self.get_age_in_minutes() / 60
    
    def get_created_date(self) -> str:
        return self.created_at.strftime("%Y-%m-%d")
    
    @abstractmethod
    def process(self) -> bool:
        pass
    @abstractmethod
    def validate(self) -> bool:
        pass


    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    def is_owner(self, user_id: str) -> bool:
        return self.user_id == user_id
    
    def has_permission(self, user_id: str) -> bool:
        return self.is_owner(user_id) and self.is_active()

    

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
   
    def __str__(self) -> str:
        return f"{self.get_class_name()}({self.interaction_id})"
    
    def __repr__(self) -> str:
        return (
            f"{self.get_class_name()}("
            f"id{self.interaction_id},"
            f"user={self.user_id},"
            f"status={self.status})"
        )




    