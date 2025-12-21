from typing import List, Dict, Any, Type
from interactions.base import  InteractionBase
from interactions.comment import CommentInteraction
from interactions.like import LikeInteraction
from interactions.subscription import SubscriptionInteraction

#Tüm interaction nesnelerini yöneten sınıf
class InteractionManager:
    def __init__(self):
        self.interaction: List[InteractionBase] = []

#Yeni interaction ekleme
    def add_interaction(self, interaction: InteractionBase) -> None:
        self.interaction.append(interaction)

#Interaction sileme
    def remove_interaction(self, interaction_id: str) -> bool:
        for i in self.interactions:
            if i.interaction_id == interaction_id:
                i.mark_as_deleted()
                return True
        return False
    
#ID ile interaction bulunması
    def get_by_id(self, interaction_id: str) -> InteractionBase | None:
        for i in self.interactions:
            if i.interaction_id == interaction_id:
                return i
        return None
    
#Kullanıcıya göre filtreleme
    def get_by_user(self, user_id: str) -> List[InteractionBase]:
        return [i for i in self.interactions if i.user_id == user_id]
    
#Türe göre filtreleme
    def get_by_type(self, interaction_type: Type[InteractionBase]) -> List[InteractionBase]:
        return [i for i in self.interactions if isinstance(i, interaction_type)]
    
#Sadece aktif olanlarrı alma
    def get_active(self) -> List[InteractionBase]:
        return [i for i in self.interactions if i.is_active()]
    
#Tüm interaction sayısı
    def get_total_count(self) -> int:
        return len(self.interactions)
    
#Türe göre sayı
    def count_by_type(self) -> Dict[str,int]:
        result: Dict[str, int] = {}
        for i in self.interactions:
            name = i.get_class_name()
            result[name] = result.get(name, 0) + 1
        return result
    
#Kullanıcı bazlı özet raporu
    def get_user_summary(self, user_id: str) -> Dict[str, Any]:
        user_items = self.get_by_user(user_id)
        summary = {
            "total": len(user_items),
            "active": len([i for i in user_items if i.is_active()]),
            "deleted": len([i for i in user_items if i.is_deleted()])
        }
        return summary
    
#Interactionları dictionary listesine çevirme
    def to_dict_list(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self.interactions]
    
#Yorumları döndürme
    def get_comments(self)-> List[CommentInteraction]:
        return self.get_by_type(CommentInteraction)
    
#Beğenileri döndürme
    def get_likes(self) -> List[LikeInteraction]:
        return self.get_by_type(LikeInteraction)
    
#Abonelikleri döndürme
    def get_subscriptions(self) -> List[SubscriptionInteraction]:
        return self.get_by_type(SubscriptionInteraction)
    
#Temizleme
    def clear_all(self) -> None:
        self.interactions.clear()

#String gösterim
    def __str__(self) -> str:
        return f"InteractionManager(total_interactions = {self.get_total_count()})"
    

#Gün7 genişletme

#Yorum (comment) işlemi
    def get_comments_by_video(self, video_id: str) -> List[CommentInteraction]:
        return [
            c for c in self.get_comments()
            if c.video_id == video_id
        ]
    
    def get_flagged_comments(self) -> List[CommentInteraction]:
        return [
            c for c in self.get_comments()
            if c.is_flagged()
        ]
    
    def get_popular_comments(self) -> List[CommentInteraction]:
        return [
            c for c in self.get_comments()
            if c.is_popular()
        ]
    
#Like (beğenme) işlemi
    def count_likes(self) -> int:
        return len([ l for l in self.get_likes() if l.is_like()])
    
    def count_dislikes(self) -> int:
        return len([ l for l in self.get_likes() if l.is_dislike()])
    
    def get_video_likes(self, video_id: str) -> List[LikeInteraction]:
        return [
            l for l in self.get_likes()
            if l.target_type == "video" and l.target_id == video_id
        ]
    
    def get_comment_likes(self, comment_id: str) -> List[LikeInteraction]:
        return [
            l for l in self.get_likes()
            if l.target_type == "comment" and l.target_id == comment_id
        ]
    
#Subscription (abonelik) işkemi
    def get_active_subscriptions(self) -> List[SubscriptionInteraction]:
        return [
            s for s in self.get_subscriptions()
            if s.is_subscribed()
        ]
    
    def get_channel_subscribers(self, channel_id: str) -> List[SubscriptionInteraction]:
        return [
            s for s in self.get_subscriptions()
            if s.channel_id == channel_id and s.is_subscribed()
        ]

#Durum bazlı sayım
    def count_by_status(self) -> Dict[str, int]:
        result = {"active": 0, "deleted": 0, "flagged": 0}
        for i in self.interactions:
            result[i.status] += 1
        return result
    
#Arama
    def search_comments(self, keyword: str) -> List[CommentInteraction]:
        keyword = keyword.lower()
        return [
            c for c in self.get_comments()
            if keyword in c.comment_text.lower()
        ]
    
#Export etme
    def export_active(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self.get_active()]
    
        