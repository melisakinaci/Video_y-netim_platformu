from interactions.comment import CommentInteraction
from interactions.like import LikeInteraction
from interactions.subscription import SubscriptionInteraction
from manager import InteractionManager

print("Test başladı")

manager = InteractionManager()

comment = CommentInteraction(
    interaction_id="c1",
    user_id="u1",
    video_id="v1",
    comment_text="Bu bir test yorumudur"
)

like = LikeInteraction(
    interaction_id="l1",
    user_id="u2",
    target_id="v1",
    target_type="video",
    like_type="like"
)

subscription = SubscriptionInteraction(
    interaction_id="s1",
    user_id="u3",
    channel_id="ch1"
)

manager.add_interaction(comment)
manager.add_interaction(like)
manager.add_interaction(subscription)

print("Toplam interaction:", manager.get_total_count())
print("Aktif interaction sayısı:", len(manager.get_active()))

print("Test bitti")

