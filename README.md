# Mini LMS Backend API

Bu proje, Microsoft SQL Server tabanlı bir **Öğrenci, Ders ve Not Otomasyon Sistemi (Mini LMS)** veritabanının üzerine geliştirilmiş çok katmanlı, asenkron ve yüksek performanslı bir REST API hizmetidir. Model-Katman (Layered Architecture) prensiplerine uygun olarak kodlanmıştır.

## 🚀 Özellikler (Features)
1. **Güçlü Veri Yönetimi**: Hazır veritabanındaki Karmaşık Görünümler (Views) ve İlişkisel Tablolar (Foreign Keys) otomatik olarak ORM şemalarına (`SQLAlchemy`) dönüştürülmüştür.
2. **Rol Tabanlı Kimlik Doğrulama (JWT)**: `Ogrenciler` ve `Kullanicilar` (Öğretmenler) rolleri birbirinden ayrılarak `/login` sokağında denetlenir. Tüm Not Girişi işlemleri (`POST, PUT`) öğretmen yetkisiyle sınırlandırılmıştır.
3. **Katı İş Kuralları (Business Logic)**: Uygulamanın Service (`app/services/`) katmanına aşağıdaki kurallar enjekte edilmiştir:
   - Derse kayıtlı olmayan öğrenciye "Not Girişi" yapılamaz.
   - Devamsızlıktan kalmış öğrenciye ("Kaldı") not girilemez.
   - Puanlar (Vize, Final) 0-100 aralığında olmalıdır.
4. **CORS Desteği**: İleride geliştirilecek tüm Frontend arayüzleri (React, Vue.js vb.) için izin erişimleri mevcuttur.

---

## 🏗️ Proje Mimarisi (Klasör Yapısı)
Proje kaynak kodları dışa kapalı olarak `/app` dizini altında mikro katmanlara ayrılmıştır:
- `api/`       -> Rotasyonlar (Uç noktalar/Endpointler)
- `core/`     -> Veritabanı bağlayıcıları ve JWT Security (Güvenlik) algoritmaları
- `models/`   -> SQL Server Modelleri (Object Relational Mapping)
- `schemas/`  -> Veri süzgeci olan Pydantic Validasyonları (Girdi/Çıktı kuralları)
- `services/` -> Core İş ve Karar mantıklarının (Business Rules) yazıldığı bölüm
- `main.py`   -> Ana sunucu dosyası

---

## 🛠️ Yerel (Local) Kurulum Adımları
### Gereksinimler:
* Python 3.10+
* Windows ODBC Driver 17 for SQL Server 
* Microsoft SQL Server (Çalışır ve "obs" adlı veritabanı yansıtılmış durumda)

### Kurulum (Windows):
```powershell
# 1. Projeyi İndirin / Dizine Girin
cd Mini-LMS-Backend-API

# 2. Sanal Ortamı Oluşturun ve Aktif Edin
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Bağımlılıkları İndirin
pip install -r requirements.txt

# 4. .env Dosyasını Yapılandırın (Kendi veritabanı ayarlarınızı girin)
# DB_URL=mssql+pyodbc:///?odbc_connect=...

# 5. Sunucuyu (Uvicorn) Canlı Olarak Ayağa Kaldırın
uvicorn app.main:app --reload
```

Sunucu başladıktan sonra, arayüze ve dokümantasyona **http://127.0.0.1:8000/docs** adresinden ulaşabilirsiniz.

---

## 🐳 Docker ile Kurulum (Tam Otonom - Sıfır Veritabanı Gereksinimi)
Projeyi inceleyecek kişi veya hocanız, bilgisayarına hiçbir şekilde **SQL Server Veritabanı veya Veri indirmek zorunda kalmaz!** Docker Compose devreye girer girmez şunları yapar:
1. İçerisinde boş ve temiz Microsoft SQL Server yüklü, şifreli bir sunucu (Konteyner) makinesi ayağa kaldırır.
2. `db-init` servisi devreye girerek, `./db-init/setup.sql` dosyasının içine bıraktığınız View ve Tablo yapılarınızı (Script) okur ve bu yeni sunucuyu "obs" veritabanı ile doldurup hazır hale getirir.
3. Son olarak `web` (FastAPI) ayağa kalkar ve veritabanıyla konuşmaya başlar.

Sadece şu komutu terminale yazmanız yeterlidir:
```bash
docker-compose up --build
```
* Sunucuya Tarayıcıdan Erişim: `http://localhost:8000/docs`

> [!IMPORTANT]
> Projeyi teslim/transfer etmeden ÖNCE; kendi SQL Server bilgisayarınızdaki "obs" veritabanına sağ tıklayıp -> Görevler (Tasks) -> Dizi Oluştur (Generate Scripts) diyerek uygulamanızın tablo, view ve test verilerini script haline getirip **`db-init/setup.sql`** dosyasının içerisine yapıştırınız. Docker okumayı bu dosyadan yapacaktır.
