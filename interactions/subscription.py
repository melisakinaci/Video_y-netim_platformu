from typing import Dict, Any
from datetime import datetime

from interactions.base import InteractionBase

# Subscription (abonelik) etkileşimlerini yöneten sınıf
class SubscriptionInteraction(InteractionBase):
    total_subscriptions = 0
    total_unsubscriptions = 0

    def __init__(
            self,
            interaction_id: str,
            user_id: str,
            channel_id: str,
            action_type: str = "subscribe",
            notification_level: str = "all"
    ):
        super().__init__(interaction_id, user_id)
        self.channel_id = channel_id
        self.action_type = action_type
        self.notification_level = notification_level
        self.created_at = datetime.now()
        self.tier = "free"

        #Global sayaçlar
        if action_type == "subscribe":
            SubscriptionInteraction.total_subscriptions += 1
        else:
            SubscriptionInteraction.total_unsubscriptions += 1

     #Abonelik işlemini başlatma
    def process(self) -> bool:
        if not self.validate():
            self.set_status("flagged")
            return False
        
        if self.action_type == "subscribe":
            self._handle_subscription()
        else:
            self._unhandle_subscription()

        return True
    
    #Girdi doğrulama
    def validate(self) -> bool:
        if self.action_type not in ["subscribe", "unsubscribe"]:
            return False
        
        if self.notification_level not in ["all", "personalized", "none"]:
            return False
        
        if not self.user_id or not self.channel_id:
            return False
       
        return True
    
    #Abone olma işlemi
    def _handle_subscription(self) -> None:
        self.status = "active"

    #Abonelik iptal işlemi
    def _unhandle_subscription(self) -> None:
        self.status = "inactive"

    #Kullanıcı aktif olarak abone mi?
    def is_subscribed(self) -> bool:
        return self.action_type == "subscrive" and self.is_active()
    
    #Bildirim seviyesini güncelleme
    def set_notification_level(self, level: str) -> bool:
        allowed = ["all", "personalized", "none"]
        if level not in allowed:
            raise ValueError("Incalid notification level")
        self.notification_level = level

    #Abonelik paketini yükseltme
    def upgrade_tier(self, tier: str) -> bool:
        allowed = ["free", "basic", "premium"]
        if tier in allowed:
            self.tier = tier

    #Paketi varsayılana çekme
    def downgrade_tier(self) -> None:
        self.tier = "free"

    #Dictionary formatına çevirme
    def to_dict(self) -> Dict[str, Any]:
        return{
            "interaction_id": self.interaction_id,
            "user_id" : self.user_id,
            "channel_id": self.channel_id,
            "action_type": self.action_type,
            "notification_level": self.notification_level,
            "tier" : self.tier,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    #Toplam abonelik sayısı
    @classmethod
    def get_total_subscriptions(cls) -> int:
        return cls.total_subscriptions
    
    #Toplam abonelik iptal sayısı
    @classmethod
    def get_total_unsubscriptions(cls) -> int:
        return cls.total_unsubscriptions
    
    #Net abonelik değişimi
    @classmethod
    def get_net_subscriptions(cls) -> int:
        return cls.total_subscriptions - cls.total_unsubscriptions
    
    #Elde tutma oranı
    @staticmethod
    def calculate_retention(subscriptions: int, unsubscriptions: int) -> float:
        if subscriptions == 0:
            return 0.0
        return ((subscriptions - unsubscriptions) / subscriptions) * 100.0
    
    #Kayıp oranı
    @staticmethod
    def caltulate_churn(subscriptions: int, unsubscriptions: int) -> float:
        if subscriptions == 0:
            return 0.0
        return ( unsubscriptions / subscriptions) * 100.0
    
    def __str__(self) -> str:
        return(
            f"SubscriptionInteraction("
            f"id = {self.interaction_id},"
            f"action = {self.action_type},"
            f"channel = {self.channel_id} )"
        )
    