-- SQL Server Veritabanını SIFIRDAN Oluşturma Dosyası
CREATE DATABASE obs;
GO

USE obs;
GO

-- 1. Bölümler Tablosu
CREATE TABLE Bolumler (
    bolum_id INT PRIMARY KEY,
    bolum_adi NVARCHAR(50),
    fakulte_adi NVARCHAR(50)
);

-- 2. Kullanıcılar (Öğretmenler) Tablosu
CREATE TABLE Kullanicilar (
    ogretmen_id INT PRIMARY KEY IDENTITY(1,1),
    kullanici_adi NVARCHAR(50) NOT NULL,
    sifre NVARCHAR(50) NOT NULL
);

-- 3. Öğrenciler Tablosu
CREATE TABLE Ogrenciler (
    ogrenci_id INT PRIMARY KEY,
    ad NVARCHAR(50),
    soyad NVARCHAR(50),
    bolum_id INT,
    kayit_tarihi DATE,
    sifre INT,
    CONSTRAINT FK_Ogrenciler_Bolumler FOREIGN KEY (bolum_id) REFERENCES Bolumler(bolum_id)
);

-- 4. Dersler Tablosu
CREATE TABLE Dersler (
    ders_id INT PRIMARY KEY,
    ders_adi NVARCHAR(50),
    bolum_id INT,
    ogretmen_id INT,
    CONSTRAINT FK_Dersler_Bolumler FOREIGN KEY (bolum_id) REFERENCES Bolumler(bolum_id),
    CONSTRAINT FK_Dersler_Kullanicilar FOREIGN KEY (ogretmen_id) REFERENCES Kullanicilar(ogretmen_id)
);

-- 5. Ders Kayıtları Tablosu
CREATE TABLE DersKayitlari (
    kayit_id INT PRIMARY KEY IDENTITY(1,1),
    ogrenci_id INT,
    ders_id INT,
    kayit_tarihi DATE,
    CONSTRAINT FK_DersKayitlari_Ogrenciler FOREIGN KEY (ogrenci_id) REFERENCES Ogrenciler(ogrenci_id),
    CONSTRAINT FK_DersKayitlari_Dersler FOREIGN KEY (ders_id) REFERENCES Dersler(ders_id)
);

-- 6. Notlar Tablosu
CREATE TABLE Notlar (
    not_id INT PRIMARY KEY IDENTITY(20,1),
    ogrenci_id INT,
    ders_id INT,
    vize INT,
    final INT,
    CONSTRAINT FK_Notlar_Ogrenciler FOREIGN KEY (ogrenci_id) REFERENCES Ogrenciler(ogrenci_id),
    CONSTRAINT FK_Notlar_Dersler FOREIGN KEY (ders_id) REFERENCES Dersler(ders_id)
);

-- ÖRNEK VERİLER
INSERT INTO Bolumler (bolum_id, bolum_adi, fakulte_adi) VALUES (1, 'Bilgisayar Mühendisliği', 'Mühendislik Fakültesi');
INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES ('admin', '123456'); -- ID 1 olur
INSERT INTO Ogrenciler (ogrenci_id, ad, soyad, bolum_id, kayit_tarihi, sifre) VALUES (210201001, 'Ahmet', 'Yılmaz', 1, '2023-09-01', 123456);
INSERT INTO Dersler (ders_id, ders_adi, bolum_id, ogretmen_id) VALUES (101, 'Veritabanı Yönetim Sistemleri', 1, 1);
INSERT INTO DersKayitlari (ogrenci_id, ders_id, kayit_tarihi) VALUES (210201001, 101, '2023-10-01');

GO

-- Transkript View'ı
CREATE VIEW vw_TranskriptSenaryosu2 AS
SELECT 
    o.ogrenci_id AS Ogrenci_Numarası,
    o.ad AS Ad,
    o.soyad AS Soyad,
    b.bolum_adi AS Bolum,
    d.ders_adi AS Ders,
    n.vize AS Vize,
    n.final AS Final,
    CAST((n.vize * 0.4 + n.final * 0.6) AS NUMERIC(13,1)) AS Ortalama,
    CASE WHEN (n.vize * 0.4 + n.final * 0.6) >= 50 THEN 'Geçti' ELSE 'Kaldı' END AS Durum
FROM Ogrenciler o
JOIN Bolumler b ON o.bolum_id = b.bolum_id
JOIN DersKayitlari dk ON o.ogrenci_id = dk.ogrenci_id
JOIN Dersler d ON dk.ders_id = d.ders_id
LEFT JOIN Notlar n ON o.ogrenci_id = n.ogrenci_id AND d.ders_id = n.ders_id;
GO

-- Ders Analiz View'ı
CREATE VIEW vw_Ders_Analiz AS
SELECT 
    d.ders_adi AS Ders,
    COUNT(dk.ogrenci_id) AS Ogrenci_Sayisi,
    AVG(CAST((n.vize * 0.4 + n.final * 0.6) AS NUMERIC(38,6))) AS Ortalama_Not,
    CAST(SUM(CASE WHEN (n.vize * 0.4 + n.final * 0.6) >= 50 THEN 1 ELSE 0 END) AS NUMERIC) / NULLIF(COUNT(dk.ogrenci_id), 0) AS Basari_Orani
FROM Dersler d
JOIN DersKayitlari dk ON d.ders_id = dk.ders_id
LEFT JOIN Notlar n ON dk.ogrenci_id = n.ogrenci_id AND dk.ders_id = n.ders_id
GROUP BY d.ders_adi;
GO

-- PERFORMANS İNDEKSLERİ (1000+ Kayıt için Önerilen)
CREATE INDEX IX_Notlar_OgrenciDers ON Notlar (ogrenci_id, ders_id);
CREATE INDEX IX_DersKayitlari_OgrenciDers ON DersKayitlari (ogrenci_id, ders_id);
CREATE INDEX IX_Ogrenciler_BolumID ON Ogrenciler (bolum_id);
GO
