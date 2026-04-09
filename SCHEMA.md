# Veri Modeli Şeması (Data Schema) 📊

Aşağıda Mini LMS sisteminin veritabanı yapısı ve tablolar arası ilişkiler Mermaid diagramı ile gösterilmiştir.

```mermaid
erDiagram
    Bolumler ||--o{ Ogrenciler : "sahip"
    Bolumler ||--o{ Dersler : "içerir"
    Kullanicilar ||--o{ Dersler : "verir"
    Ogrenciler ||--o{ DersKayitlari : "kaydolur"
    Dersler ||--o{ DersKayitlari : "kayıt alır"
    Ogrenciler ||--o{ Notlar : "notu var"
    Dersler ||--o{ Notlar : "notu var"
    Ogrenciler ||--o{ Devamsizlik : "durumu var"
    Dersler ||--o{ Devamsizlik : "durumu var"

    Bolumler {
        int bolum_id PK
        string bolum_adi
        string fakulte_adi
    }

    Kullanicilar {
        int ogretmen_id PK
        string kullanici_adi
        string sifre
    }

    Ogrenciler {
        int ogrenci_id PK
        string ad
        string soyad
        int bolum_id FK
        date kayit_tarihi
        int sifre
    }

    Dersler {
        int ders_id PK
        string ders_adi
        int bolum_id FK
        int ogretmen_id FK
    }

    DersKayitlari {
        int kayit_id PK
        int ogrenci_id FK
        int ders_id FK
        date kayit_tarihi
    }

    Notlar {
        int not_id PK
        int ogrenci_id FK
        int ders_id FK
        int vize
        int final
    }

    Devamsizlik {
        int ogrenci_id FK
        int ders_id FK
        int toplam_ders
        int katilim_sayisi
        string durum
    }
```

## Tablo Açıklamaları

*   **Bolumler**: Fakülte ve bölümlerin tanımlandığı temel tablo.
*   **Kullanicilar**: Sistemdeki öğretmenlerin ve yöneticilerin giriş bilgilerini tutar.
*   **Ogrenciler**: Öğrenci bilgilerini ve bölüm eşleşmelerini tutar.
*   **Dersler**: Bölüm bazlı açılan dersler ve bu dersleri veren öğretmenleri eşleştirir.
*   **DersKayitlari**: Öğrencilerin hangi dersleri aldığını takip eder (n-n ilişki çözümü).
*   **Notlar**: Öğrencilerin ders bazlı vize ve final sonuçlarını saklar.
*   **Devamsizlik**: Derse katılım oranlarını takip ederek otomatik kalma hesaplamasında kullanılır.

---
*Bu şema SQLAlchemy modelleri (`models.py`) ile tam uyumludur.*
