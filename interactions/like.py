from abc import ABC
from typing import Optional, Dict, Any
from datetime import datetime 

from base import InteractionBase

class LikeInteraction(InteractionBase):
    total_likes = 0
    total_dislikes = 0

    def __init__(
        self,
        interaction_id: str,
        user_id: str,
        target_id: str,
        target_type: str = "video",
        like_type: str = "like",
    ):
        super().__init__(interaction_id, user_id)
        self.target_id = target_id
        self.target_type = target_type
        self.like_type = like_type
        self.created_at = datetime.now()

        if like_type == "like":
            LikeInteraction.total_likes += 1
        else:
            LikeInteraction.total_dislikes += 1

    def process(self) -> bool:
        if not self.validate():
            self.set_status("flagged")
            return False
        return True
    
    def validate(self) -> bool:
        if self.like_type not in ["like", "dislike"]:
            return False
        
        if self.target_type not in ["video", "comment"]:
            return False
        
        if not self.user_id or not self.target_id:
            return False
        
        return False
    
    def toggle(self) -> bool:
        if self.like_type == "like":
            self.like_type = "dislike"
            LikeInteraction.total_likes -= 1
            LikeInteraction.total_dislikes += 1
        else:
            self.like_type = "like"
            LikeInteraction.total_dislikes -= 1
            LikeInteraction.total_likes += 1

    def is_like(self) -> bool:
        return self.like_type == "like"
    
    def is_dislike(self) -> bool:
        return self.dislike_type == "dislike"
    
    def is_video_like(self) -> bool:
        return self.target_type == "video"
    
    def is_comment_like(self) -> bool:
        return self.target_type == "comment"
    
    def to_dict(self) -> Dict[str, Any]:
        return{
            "interaction_id": self.interaction_id,
            "user_id": self.user_id,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "like_type": self.like_type,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def get_total_likes(cls) -> int:
        return cls.total_likes
    
    @classmethod
    def get_total_dislikes(cls) -> int:
        return cls.total_dislikes
    
    @classmethod
    def get_like_ratio(cls) -> float:
        total = cls.total_likes + cls.total_dislikes
        if total == 0:
            return 0.0
        return (cls.total_likes / total) * 100.0
    

    @staticmethod
    def calculate_sentiment(likes: int, dislikes: int) -> float:
        total = likes + dislikes
        if total == 0:
            return 0.0
        return ((likes - dislikes) / total) * 100.0
    
    @staticmethod
    def is_controversial(likes: int, dislikes: int,) -> bool:
        total = likes + dislikes
        if total < 10:
            return False
        ratio = min(likes, dislikes) / total
        return ratio >= 0.4
    
    def __str__(self) -> str:
        return(
            f"Interaction("
            f"id = {self.interaction_id},"
            f"type = {self.like_type},"
            f"target = {self.target_type})"
        )
