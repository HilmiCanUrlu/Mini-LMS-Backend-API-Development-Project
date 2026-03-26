-- SQL Server Veritabanını SIFIRDAN Oluşturma Dosyası
-- Buradaki kod parçaları Docker ayağa kalktığında sadece BİR KEZ çalıştırılır ve tabloları doldurur.

CREATE DATABASE obs;
GO

USE obs;
GO

-- 1. ADIM: TABLOLARI YARATIN
-- Lütfen SQL Server Management Studio (SSMS) kullanıp, kendi "obs" veritabanınıza sağ tıklayarak:
-- Tasks (Görevler) -> Generate Scripts (Komut Dizisi Oluştur) -> Tablolar, View'lar, Verilerin hepsi 
-- seçeneğini seçip, o dosyanın içindeki tüm metni kopyalayarak AŞAĞIYA YAPIŞTIRIN!

-- ÖRNEK:
-- CREATE TABLE Bolumler ( bolum_id int PRIMARY KEY, bolum_adi nvarchar(50) ... )
-- CREATE VIEW vw_TranskriptSenaryosu2 AS SELECT ...
-- INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES ('admin', '123')
