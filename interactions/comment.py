from typing import Dict, Any, List, Optional
from interactions.base import InteractionBase

class CommentInteraction(InteractionBase):
    def __init__(
            self,
            interaction_id: str,
            user_id: str,
            video_id: str,
            comment_text: str,
            parent_comment_id: Optional[str] = None
    ):
        super().__init__(interaction_id, user_id)
        self.video_id = video_id
        self.comment_text = comment_text
        self.parent_comment_id = parent_comment_id

        self.like_count = 0
        self.dislike_count = 0
        self.reply_count = 0

        self.is_edited = False
        self.is_pinned = False

        self.flags: List[str] = []

    def process(self) -> bool:
        if not self.validate():
            return False
        if self.detect_basic_spam():
            self.flags.append("spam")
            self.set_status("flagged")
            return False
        return True
    
    def validate(self) -> bool:
        if not self.comment_text:
            return False
        if len(self.comment_text.strip()) == 0:
            return False
        if len(self.comment_text) > 500:
            return False
        if not self.user_id or not self.video_id:
            return False
        return True
    
    def edit_comment(self, new_text: str) -> None:
        if not new_text or len(new_text.strip()) == 0:
            raise ValueError("Yorum metni boş olamaz.")
        self.comment_text = new_text
        self.is_edited = True

    def pin(self) -> None:
        self.is_pinned = True

    def unpin(self) -> None:
        self.is_pinned = False

    def add_like(self) -> None:
        self.like_count += 1

    def remove_like(self) -> None:
        if self.like_count > 0:
            self.like_count -= 1

    def add_dislike(self) -> None:
        self.dislike_count += 1

    def remove_dislike(self) -> None:
        if self.dislike_count > 0:
            self.dislike_count -= 1

    def toggle_like(self) -> None:
        if self.like_count > 0:
            self.like_count -= 1
            self.dislike_count += 1
        else:
            self.like_count += 1

    def is_reply(self) -> bool:
        return self.parent_comment_id is not None
    
    def add_reply(self) -> None:
        self.reply_count += 1

    def get_word_count(self) -> int:
        return len(self.comment_text.split())
    
    def get_character_count(self) -> int:
        return len(self.comment_text)
    
    def is_long_comment(self) -> bool:
        return self.get_word_count() > 100
    
    def prewiew(self, lenght: int = 50) -> str:
        if len(self.comment_text) <= lenght:
            return self.comment_text
        return self.comment_text[:lenght] + "..."
    
    def has_reactions(self) -> bool:
        return self.get_reaction_count() > 0
    
    def get_reaction_count(self) -> int:
        return self.like_count + self.dislike_count
    
    def get_like_ratio(self) -> float:
        total = self.get_reaction_count()
        if total == 0:
            return 0.0
        return (self.like_count / total) * 100
    
    def calculate_score(self) -> float:
        score = (
            self.like_count * 1.0 +
            self.reply_count * 2.0 -
            self.dislike_count * 0.5
        )
        return max(0.0, score)
    
    def is_popular(self) -> bool:
        return self.like_count >= 10 or self.reply_count >= 5
    
    def detect_basic_spam(self) -> bool:
        text = self.comment_text.lower()

        if text.count("http") > 2:
            return True
        
        if self.get_character_count() > 100 and self.get_word_count() < 5:
            return True
        
        repeated = 0
        last_char = " "
        
        for c in text:
            if c == last_char:
                repeated += 1
                if repeated > 6:
                    return True
            else:
                repeated = 0
                last_char = c

        return False
    
    def find_mentions(self) -> List[str]:
        return [w[1:] for w in self.comment_text.split() if w.startswith("@")]
    
    def find_hashtags(self) -> List[str]:
        return [w[1:] for w in self.comment_text.split() if w.startswith("#")]
    
    def add_flag(self, reason: str) -> None:
        if reason not in self.flags:
            self.flags.append(reason)

    def clear_flags(self) -> None:
        self.flags.clear()

    def is_flagged(self) -> bool:
        return len(self.flags) > 0 or self.status == "flagged"
    
    def to_dict(self) -> Dict[str, Any]:
        return{
            "interaction_id": self.interaction_id,
            "user_id": self.user_id,
            "video_id": self.video_id,
            "parent_comment_id": self.parent_comment_id,
            "comment_text": self.comment_text,
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "reply_count": self.reply_count,
            "is_edited": self.is_edited,
            "is_pinned": self.is_pinned,
            "flags": self.flags,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    def __len__(self) -> int:
        return len(self.comment_text)
    
    def __str__(self) -> str:
        return f"Comment({self.interaction_id}, score = {self.calculate_score()})"