# İş Kuralları Dökümantasyonu (Business Rules) 📋

Bu döküman, Mini LMS Backend API v2 projesinde uygulanan mantıksal kuralları ve sistemi yöneten temel prensipleri içerir.

## 1. Kimlik Doğrulama ve Yetkilendirme (Auth & Role Management)

*   **Çift Yönlü Giriş**:
    *   **Öğrenciler**: Giriş yaparken kullanıcı adı olarak `ogrenci_id` (numara) kullanmalıdır.
    *   **Öğretmenler/Yöneticiler**: Giriş yaparken sözel kullanıcı adlarını kullanırlar.
*   **Rol Bazlı Erişim Kontrolü (RBAC)**:
    *   **Öğrenci Rolü**: Sadece kendi bilgilerini, derslerini ve transkriptini görüntüleyebilir. Not girişi yapamaz.
    *   **Öğretmen Rolü**: Öğrenci ekleyebilir, ders analizlerini görebilir ve öğrencilere not girişi/güncellemesi yapabilir.
*   **Oturum Yönetimi**: Tüm API istekleri geçerli bir JWT Bearer Token gerektirir (Public endpointler hariç). Token süresi varsayılan olarak 60 dakikadır.

## 2. Akademik ve Notlandırma Kuralları

*   **Not Hesaplama Mantığı**:
    *   Yıl sonu ortalaması şu formülle hesaplanır: `(Vize * %40) + (Final * %60)`.
*   **Geçme/Kalma Şartı**:
    *   Hesaplanan ortalama **50.0** ve üzeri ise öğrenci dersten "Geçti", altında ise "Kaldı" kabul edilir.
*   **Not Giriş Kısıtlaması**:
    *   Bir öğrenciye not girişi yapılabilmesi için, o öğrencinin ilgili derse **mutlaka kayıtlı (DersKayitlari tablosunda kaydı bulunması)** olması gerekir. Kaydı olmayan öğrenciye not girişi yapılamaz (API 400 Hatası döner).

## 3. Veri Girişi ve Bütünlük Kuralları

*   **Öğrenci Kaydı**:
    *   Yeni öğrenci kaydedilirken `kayit_tarihi` sistem tarafından otomatik olarak o günün tarihi olarak atanır.
    *   Her öğrencinin benzersiz bir `ogrenci_id`'si olmalıdır.
*   **Bölüm İlişkisi**:
    *   Öğrenci ve dersler mutlaka mevcut bir bölüme (`bolum_id`) bağlı olmalıdır. Silinen bir bölüme bağlı kayıtlar için veritabanı kısıtlamaları (Foreign Key) geçerlidir.

## 4. Analiz ve Raporlama Kuralları

*   **Ders Analizi**:
    *   Ders başarı oranı; o dersi alan tüm öğrenciler içinden dersten geçenlerin (`ortalama >= 50`) toplam öğrenci sayısına bölünmesiyle hesaplanır.
*   **Transkript**:
    *   Öğrencinin transkriptinde sadece kayıtlı olduğu dersler ve varsa bu derslere ait not/durum bilgisi listelenir. Henüz notu girilmemiş dersler de transkriptte "Notu Yok" veya boş olarak listelenmeye devam eder.

## 5. Hata ve Geri Bildirim Standartları

*   Tüm iş kuralı ihlallerinde API, kullanıcıya Türkçe mesaj içeren uygun HTTP durum kodlarını döner:
    *   **401**: Geçersiz kimlik bilgileri veya eksik token.
    *   **403**: Yetkisiz işlem denemesi (Örn: Öğrencinin not girmeye çalışması).
    *   **404**: Aranan kaydın (Öğrenci, Ders, Not) bulunamaması.
    *   **400**: Mantıksal hatalar (Örn: Derse kayıtlı olmayan öğrenciye not vermek).

---
*Bu kurallar sistemin tutarlılığını ve akademik doğruluğunu garanti altına almak için tasarlanmıştır.*
