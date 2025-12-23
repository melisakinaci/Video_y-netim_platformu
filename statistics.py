from typing import List, Dict, Any
from datetime import datetime, timedelta

from interactions.base import InteractionBase
from interactions.comment import CommentInteraction
from interactions.like import LikeInteraction
from interactions.subscription import SubscriptionInteraction

class InteractionStatistics:
    def __init__(self, interactions: List[InteractionBase]):
        self.interactions = interactions
        self.generated_at = datetime.now()

#Genel sayılar
    def total_count(self) -> int:
        return len(self.interactions)
    
    def count_by_type(self) -> Dict[str, int]:
        result: Dict[str, int] = {}
        for i in self.interactions:
            name = i.get_class_name()
            result[name] = result.get(name, 0) + 1
        return result
    
    def count_by_status(self) -> Dict[str, int]:
        result = {"active": 0, "deleted": 0, "flagged": 0}
        for i in self.interactions:
            result[i.status] += 1
        return result
    
#Comment işlemleri
    def get_comments(self) -> List[CommentInteraction]:
        return [i for i in self.interactions if isinstance(i, CommentInteraction)]
    
    def total_comments(self) -> int:
        return len(self.get_comments())

    def flagged_comments(self) -> List[CommentInteraction]:
        return len([c for c in self.get_comments() if c.is_flagged()])
    
    def popular_comments(self) -> List[CommentInteraction]:
        return len([c for c in self.get_comments() if c.is_popular()])
    
    def average_comment_length(self) -> float:
        comments = self.get_comments()
        if not comments:
            return 0.0
        total = sum(len(c.content) for c in comments)
        return total / len(comments)
    
    def average_comment_score(self) -> float:
        comments = self.get_comments()
        if not comments:
            return 0.0
        total = sum(c.calculate_score() for c in comments)
        return total / len(comments)
    
#Like işlemleri
    def get_likes(self) -> List[LikeInteraction]:
        return [i for i in self.interactions if isinstance(i, LikeInteraction)]
    
    def total_likes(self) -> int:
        return len([l for l in self.get_likes() if l.is_like()])
    
    def total_dislikes(self) -> int:
        return len([l for l in self.get_likes() if l.is_dislike()])
    
    def like_ratio(self) -> float:
        likes = self.total_likes()
        dislikes = self.total_dislikes()
        total = likes + dislikes
        if total == 0:
            return 0.0
        return (likes / total) * 100
    
    def controversial_items(self) -> int:
        count = 0
        for l in self.get_likes():
            if LikeInteraction.is_controversial(1, 1):
                count += 1
        return count
    
#Subscription (abonelik) işlemleri
    def get_subscriptions(self) -> List[SubscriptionInteraction]:
        return [
            i for i in self.interactions
            if isinstance(i, SubscriptionInteraction)
        ]
    def active_subscriptions(self) -> int:
        return len([s for s in self.get_subscriptions() if s.is_subscribed()])
    
    def total_subscriptions(self) -> int:
        return len(self.get_subscriptions())

    def subscription_ratio(self) -> float:
        total = self.total_subscriptions()
        if total == 0:
            return 0.0
        return (self.active_subscriptions() / total) * 100
    
#Zaman bazlı analiz
    def interactions_last_days(self, days: int) -> int:
        since = datetime.now() - timedelta(days=days) 
        return len([i for i in self.interactions if i.created_at >= since])

    def daily_average(self, days: int) -> float:
        if days <= 0:
            return 0.0
        return self.interactions_last_days(days) / days

#Rapor
    def generate_summary(self) -> Dict[str, Any]:
        return{
            "generated_at": self.generated_at,
            "total_interactions": self.total_count(),
            "by_type": self.count_by_type(),
            "by_status": self.count_by_status(),
            "comments": {
                "total": self.total_comments(),
                "flagged": self.flagged_comments(),
                "popular": self.popular_comments(),
                "average_length": self.average_comment_length(),
                "average_score":self.average_comment_score()
            },
            "likes": {
                "likes": self.total_likes(),
                "dislikes": self.total_dislikes(),
                "like_ratio": self.like_ratio()
            },
            "subscriptions": {
                "total": self.total_subscriptions(),
                "active": self.active_subscriptions(),
                "ratio": self.subscription_ratio()
            }
        }   
    
    def __str__(self) -> str:
        return f"InteractionStatistics(total={self.total_count()})"
    
        
    