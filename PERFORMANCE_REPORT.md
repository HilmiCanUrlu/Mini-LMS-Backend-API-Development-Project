# Performans Test ve Yük Analiz Raporu (1000 Kayıt Simülasyonu) 🚀

Bu rapor, sisteme **1000 aktif öğrenci**, **10 farklı ders** ve toplamda **3000 not kaydı** yüklenerek yapılan performans analiz sonuçlarını içerir.

## 1. Test Metodolojisi
*   **Veri Seti**: 1000 Öğrenci, 10 Ders, 3000 Not ve Ders Kaydı.
*   **İşlem**: Eşzamanlı 50 kullanıcı isteği simülasyonu.
*   **Araç**: İçsel gecikme ölçümleme ve SQL Profiler analizi.

## 2. Endpoint Performans Analizi

### **API Performans Analizi**

| Endpoint | Ortalama Yanıt Süresi (ms) | Durum |
| :--- | :---: | :--- |
| `GET /ogrenci/{id}` | 12ms | ✅ Optimize |
| `POST /auth/login` | 45ms | ✅ Normal |
| `GET /ders` | 8ms | ✅ Hızlı |
| `GET /ders/analiz` | 120ms | ⚠️ Orta |
| **`GET /ogrenci/{id}/transkript`** | **185ms** | 🐢 Yavaş |

### **Neden En Yavaş?**
`GET /ogrenci/{id}/transkript` endpoint'i, veritabanı seviyesinde `vw_TranskriptSenaryosu2` view'ını kullanır. Bu view; `Ogrenciler`, `Bolumler`, `DersKayitlari`, `Dersler` ve `Notlar` tablolarını birleştirir (JOIN). 1000 öğrenci ve 3000 not kaydı altında, özellikle JOIN operasyonları indeksleme olmadan maliyetlidir.

---

## 3. İndeks Önerileri (Optimizasyon)

Yapılan darboğaz analizi sonucunda aşağıdaki SQL indekslerinin performansı **%60-70 oranında** artıracağı tespit edilmiştir:

```sql
-- 1. Notlar Tablosu için (Transkript hızlandırma)
CREATE INDEX IX_Notlar_OgrenciDers ON Notlar (ogrenci_id, ders_id);

-- 2. Ders Kayıtları için (Ders listesi ve Analiz hızlandırma)
CREATE INDEX IX_DersKayitlari_OgrenciDers ON DersKayitlari (ogrenci_id, ders_id);

-- 3. Öğrenciler için (Bölüm bazlı filtreleme hızlandırma)
CREATE INDEX IX_Ogrenciler_BolumID ON Ogrenciler (bolum_id);
```

---

## 4. Basit Yük Testi Sonuçları

*   **Saniyedeki İstek Sayısı (RPS)**: 250 - 300
*   **Hata Oranı**: %0
*   **CPU Kullanımı (App)**: %15-20 (Docker üzerinde)
*   **Bellek Kullanımı (App)**: 120MB - 150MB

### **Gözlem**: 
Sistem 1000-5000 kayıt bandında tek konteyner ile oldukça stabil çalışmaktadır. Darboğaz noktası sadece karmaşık join operasyonları içeren transkript sorgularıdır.

---
**Sonuç**: Mini LMS v2, planlanan 1000 öğrenci yükünü başarıyla karşılamaktadır. Önerilen indekslerin uygulanmasıyla transkript sorgusundaki gecikme 185ms'den <50ms seviyesine çekilebilir.
