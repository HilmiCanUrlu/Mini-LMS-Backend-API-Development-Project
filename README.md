# Mini LMS Backend API v2 🎓

Bu proje, bir Öğrenci Yönetim Sistemi (LMS) için geliştirilmiş modern, performanslı ve ölçeklenebilir bir backend API çözümüdür. FastAPI ve SQLAlchemy kullanılarak geliştirilen bu sürüm (v2), gelişmiş modüler mimari ve tam Docker desteği ile gelmektedir.

## 📄 Proje Dökümantasyonu

*   [Veri Modeli Şeması (Database Schema)](SCHEMA.md)
*   [İş Kuralları Dökümantasyonu (Business Rules)](BUSINESS_RULES.md)
*   [Performans Değerlendirme Raporu](PERFORMANCE_REPORT.md)

## 🚀 Öne Çıkan Özellikler

*   **Tam Docker Desteği**: Tek komutla (`docker-compose up`) veritabanı ve API kurulumu.
*   **Gelişmiş Kimlik Doğrulama**: JWT (JSON Web Token) tabanlı güvenli giriş sistemi.
*   **Öğrenci Yönetimi**: Detaylı öğrenci kayıt, sorgulama ve transkript işlemleri.
*   **Ders ve Not Sistemi**: Not girişi (Vize/Final), otomatik ortalama hesaplama ve başarı durumu takibi.
*   **Analiz ve Raporlama**: SQL View'lar üzerinden ders bazlı başarı analizi ve istatistikler.
*   **Otomatik Veritabanı Kurulumu**: Docker başlatıldığında tablolar, view'lar ve örnek veriler otomatik oluşturulur.
*   **Türkçe Hata Mesajları**: Kullanıcı dostu ve açıklayıcı hata geri bildirimleri.

## 🔐 Örnek Giriş Bilgileri

Sistemi test etmek için aşağıdaki varsayılan hesapları kullanabilirsiniz:

| Rol | Kullanıcı Adı (Username) | Şifre (Password) |
| :--- | :--- | :--- |
| **Öğretmen / Admin** | `admin/ogretmen` | `123` |
| **Öğrenci** | `1/herhangi bir öğrenci no` | `123` |

## 🛠️ Teknoloji Yığını

*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
*   **Veritabanı**: Microsoft SQL Server
*   **Konteynerleştirme**: Docker & Docker Compose
*   **Güvenlik**: Passlib (Bcrypt), Python-Jose (JWT)

---

## 📸 Ekran Görüntüleri

Buraya uygulamanıza ait ekran görüntülerini ekleyebilirsiniz:

> [!TIP]
> **Swagger UI (API Dökümantasyonu)**
> ![Swagger UI](buraya_goruntu_yolu.png)
> *Otomatik oluşturulan interaktif API dökümantasyonu.*

> [!TIP]
> **Veritabanı Şeması**
> ![Veritabanı](buraya_goruntu_yolu_2.png)
> *SQL Server üzerindeki tablo yapısı.*

---

## 🛠️ Kurulum Rehberi

### **Yöntem 1: Docker ile Kurulum (Önerilen - Sıfır Kurulum)**

Bu yöntemle bilgisayarınıza hiçbir kütüphane veya veritabanı kurmanıza gerek kalmaz. Sadece Docker Desktop'ın yüklü olması yeterlidir.

1.  Projeyi indirin ve terminalden proje dizinine gidin.
2.  Şu komutu çalıştırın:
    ```bash
    docker-compose up --build
    ```
3.  Sistem hazır olduğunda API dökümantasyonuna şu adresten ulaşabilirsiniz:
    `http://localhost:8000/docs`

---

### **Yöntem 2: Manuel Kurulum (Geliştiriciler İçin)**

1.  **Python Ortamı**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Veritabanı**:
    *   Microsoft SQL Server'da `obs` adında bir veritabanı oluşturun.
    *   `db-init/setup.sql` içindeki kodları SQL Server üzerinde çalıştırın.

3.  **.env Ayarları**:
    Root dizinindeki `.env` dosyasını kendi veritabanı bilgilerinizle düzenleyin.

4.  **Uygulamayı Çalıştırın**:
    ```bash
    uvicorn main:app --reload
    ```

---

## 🔗 Endpoint Grupları

| Grup | Açıklama |
| :--- | :--- |
| `/auth` | Kullanıcı girişi ve Token işlemleri. |
| `/ogrenci` | Öğrenci listeleme, ekleme ve transkript sorgulama. |
| `/not` | Not girişi ve güncelleme (Sadece öğretmen yetkisiyle). |
| `/ders` | Tüm derslerin listelenmesi ve başarı analizleri. |

---

## 🧪 Örnek API Parametreleri

API üzerinden işlem yaparken kullanabileceğiniz örnek JSON gövdeleri:

### **1. Yeni Öğrenci Kaydı (`POST /ogrenci`)**
```json
{
  "ogrenci_id": 210201005,
  "ad": "Ece",
  "soyad": "Kaya",
  "bolum_id": 1,
  "sifre": 123456
}
```

### **2. Not Girişi (`POST /not`)**
*Not: Bu işlem için Öğretmen token'ı gereklidir.*
```json
{
  "ogrenci_id": 210201001,
  "ders_id": 101,
  "vize": 75,
  "final": 85
}
```

### **3. Giriş Yapma (`POST /auth/login`)**
*Form Data (x-www-form-urlencoded) olarak gönderilmelidir:*
- `username`: 210201001 (Öğrenci) veya admin (Öğretmen)
- `password`: 123456

---

---

## 👨‍💻 Geliştirme Notları

*   **v2 Değişiklikleri**: Kod yapısı `api`, `core`, `models`, `schemas` ve `services` olarak katmanlı mimariye ayrıldı.
*   **Güvenlik**: Şifreler hash'lenerek saklanmakta ve tüm hassas işlemler yetki kontrolüne tabidir.

---

Bu proje, bir backend sisteminin tüm katmanlarını (API, DB, Docker, Auth) öğrenmek ve uygulamak amacıyla v2 olarak geliştirilmiştir.
