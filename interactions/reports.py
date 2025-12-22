from typing import List, Dict, Any, Optional
from datetime import datetime

from interactions.base import InteractionBase
from interactions.comment import CommentInteraction
from interactions.like import LikeInteraction
from interactions.subscription import SubscriptionInteraction


class InteractionReport:
    def __init__(self, interactions: List[InteractionBase]):
        self.interactions = interactions
        self.generated_at = datetime.now()

#Genel rapor
    def general_overview(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "total_interactions": len(self.interactions),
            "active": self._count_status("active"),
            "deleted": self._count_status("deleted"),
            "flagged": self._count_status("flagged"),
        }

    def _count_status(self, status: str) -> int:
        return len([i for i in self.interactions if i.status == status])
    
#Comment (yorum) raporu
    def comment_overview(self) -> Dict[str, Any]:
        comments = self._get_comments()

        return {
            "total": len(comments),
            "flagged": len([c for c in comments if c.is_flagged()]),
            "popular": len([c for c in comments if c.is_popular()]),
            "average_length": self._average_comment_length(comments),
            "average_score": self._average_comment_score(comments),
        }

    def _get_comments(self) -> List[CommentInteraction]:
        return [i for i in self.interactions if isinstance(i, CommentInteraction)]

    def _average_comment_length(self, comments: List[CommentInteraction]) -> float:
        if not comments:
            return 0.0
        total = sum(len(c) for c in comments)
        return total / len(comments)

    def _average_comment_score(self, comments: List[CommentInteraction]) -> float:
        if not comments:
            return 0.0
        total = sum(c.calculate_score() for c in comments)
        return total / len(comments)

    def top_comments(self, limit: int = 5) -> List[Dict[str, Any]]:
        comments = sorted(
            self._get_comments(),
            key=lambda c: c.calculate_score(),
            reverse=True
        )
        return [c.to_dict() for c in comments[:limit]]
    
#Like (beğeni) raporu
    def like_overview(self) -> Dict[str, Any]:
        likes = self._get_likes()
        like_count = len([l for l in likes if l.is_like()])
        dislike_count = len([l for l in likes if l.is_dislike()])

        total = like_count + dislike_count
        ratio = (like_count / total * 100) if total > 0 else 0.0

        return {
            "likes": like_count,
            "dislikes": dislike_count,
            "ratio": ratio
        }

    def _get_likes(self) -> List[LikeInteraction]:
        return [i for i in self.interactions if isinstance(i, LikeInteraction)]

    def likes_by_target(self, target_type: str) -> Dict[str, int]:
        result: Dict[str, int] = {}

        for l in self._get_likes():
            if l.target_type == target_type:
                result[l.target_id] = result.get(l.target_id, 0) + 1

        return result
    
#Subscription (abonelik) raporu
     def subscription_overview(self) -> Dict[str, Any]:
        subs = self._get_subscriptions()
        active = [s for s in subs if s.is_subscribed()]

        return {
            "total": len(subs),
            "active": len(active),
            "inactive": len(subs) - len(active),
            "active_ratio": (len(active) / len(subs) * 100) if subs else 0.0
        }

    def _get_subscriptions(self) -> List[SubscriptionInteraction]:
        return [
            i for i in self.interactions
            if isinstance(i, SubscriptionInteraction)
        ]

    def subscribers_by_channel(self) -> Dict[str, int]:
        result: Dict[str, int] = {}

        for s in self._get_subscriptions():
            if s.is_subscribed():
                result[s.channel_id] = result.get(s.channel_id, 0) + 1

        return result

#Filtreli rapor
    def interactions_by_user(self, user_id: str) -> Dict[str, Any]:
        items = [i for i in self.interactions if i.user_id == user_id]

        return {
            "total": len(items),
            "active": len([i for i in items if i.is_active()]),
            "deleted": len([i for i in items if i.is_deleted()]),
            "by_type": self._count_by_type(items)
        }

    def _count_by_type(self, items: List[InteractionBase]) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for i in items:
            name = i.get_class_name()
            result[name] = result.get(name, 0) + 1
        return result

#Export raporu
    def export_full_report(self) -> Dict[str, Any]:
        return {
            "general": self.general_overview(),
            "comments": self.comment_overview(),
            "likes": self.like_overview(),
            "subscriptions": self.subscription_overview(),
            "generated_at": self.generated_at.isoformat()
        }

    def export_raw(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self.interactions]
    
#String
    def __str__(self) -> str:
        return f"InteractionReport(total={len(self.interactions)})"
    