import os
from manager import InteractionManager
from statistics import InteractionStatistics
from reports import InteractionReport
from interactions.comment import CommentInteraction
from interactions.like import LikeInteraction
from interactions.subscription import SubscriptionInteraction

def run_extended_test():
    print(" === VİDEO YÖNETİM PLATFORMU SİSTEM TESTİ BAŞLADI === \n")

    # 1. SİSTEMİ BAŞLAT
    manager = InteractionManager()

    # 2. TEST VERİLERİ OLUŞTURMA
    print(" Test verileri sisteme yükleniyor...")

    #Yorumlar
    c1 = CommentInteraction("c1", "ahmet123", "video_101", "Bu harika bir eğitici video olmuş, teşekkürler!")
    c1.process()
    for _ in range(15): c1.add_like() # Popüler yorum simülasyonu
    
    c2 = CommentInteraction("c2", "mehmet_can", "video_101", "Ses kalitesi biraz düşük kalmış.")
    c2.process()
    c2.set_status("flagged") # Sorunlu yorum simülasyonu

    c3 = CommentInteraction("c3", "zeynep_tech", "video_102", "Daha fazla içerik bekliyoruz!")
    c3.process()

    #Beğeni
    l1 = LikeInteraction("l1", "user_x", "video_101", "video", "like")
    l2 = LikeInteraction("l2", "user_y", "video_101", "video", "like")
    l3 = LikeInteraction("l3", "user_z", "video_101", "video", "dislike")
    l4 = LikeInteraction("l4", "ahmet123", "c2", "comment", "dislike") # Yoruma dislike

    #Abonelik 
    s1 = SubscriptionInteraction("s1", "ahmet123", "yazilim_kanali")
    s1.process()
    
    s2 = SubscriptionInteraction("s2", "zeynep_tech", "yazilim_kanali")
    s2.process()

    #3. VERİLERİ MANAGER'A EKLE
    test_data = [c1, c2, c3, l1, l2, l3, l4, s1, s2]
    for data in test_data:
        manager.add_interaction(data)

    print(f" {len(test_data)} adet etkileşim başarıyla kaydedildi.\n")

    #4. İSTATİSTİK MODÜLÜNÜ ÇALIŞTIR
    print(" --- İSTATİSTİKSEL ANALİZ ---")
    stats = InteractionStatistics(manager.interactions)
    summary = stats.generate_summary()

    print(f"Toplam Etkileşim: {summary['total_interactions']}")
    print(f"Yorum Sayısı: {summary['comments']['total']}")
    print(f"Ortalama Yorum Uzunluğu: {summary['comments']['average_length']} karakter")
    print(f"Beğeni Oranı: %{summary['likes']['like_ratio']:.2f}")
    
    #5. RAPORLAMA MODÜLÜNÜ ÇALIŞTIR
    print("\n --- DETAYLI RAPOR ÇIKTISI ---")
    report = InteractionReport(manager.interactions)
    
    #Kelime analizi
    keyword = "harika"
    count = report.keyword_frequency(keyword)
    print(f" '{keyword}' kelimesi yorumlarda {count} kez geçiyor.")

    # Video bazlı beğeni dağılımı
    video_stats = report.likes_by_video()
    print(f" Video 101 Beğeni Sayısı: {video_stats.get('video_101', 0)}")

    #En uzun yorumu bulma
    longest = report.longest_comments(1)
    if longest:
        print(f" En uzun yorum: '{longest[0]['comment_text'][:30]}...' ({len(longest[0]['comment_text'])} harf)")

    #6. MANAGER FİLTRELEME TESTİ
    print("\n --- FİLTRELEME TESTLERİ ---")
    tech_subs = manager.get_channel_subscribers("yazilim_kanali")
    print(f" 'yazilim_kanali' Aktif Abone Sayısı: {len(tech_subs)}")
    
    flagged = manager.get_flagged_comments()
    print(f" İncelenmesi Gereken (Flagged) Yorumlar: {len(flagged)}")

    print("\n === TÜM TESTLER BAŞARIYLA TAMAMLANDI === ")

if __name__ == "__main__":
    #Önce eski pycache kalıntılarını temizleyelim (Hata almamak için)
    if os.path.exists("__pycache__"):
        import shutil
        shutil.rmtree("__pycache__", ignore_errors=True)
    
    run_extended_test()