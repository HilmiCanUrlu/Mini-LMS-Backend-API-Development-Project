import urllib.parse
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# SQL Server Bağlantı Ayarları (.env'den okuyoruz)
server = os.getenv('DB_SERVER', r'DESKTOP-1\SQLEXPRESS')
database_name = os.getenv('DB_NAME', 'obs')
driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

# Bağlantı dizesini oluşturma (Windows Authentication - Şifresiz giriş)
conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database_name};Trusted_Connection=yes;"
params = urllib.parse.quote_plus(conn_str)

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Engine (Motor): Veritabanı ile uygulamamız arasındaki ana köprü.
# echo=True ile arka planda çalışan SQL sorgularını terminalde görebileceğiz.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# SessionLocal: Veritabanı ile her iletişim kurduğumuzda kullanacağımız "oturum" aracı.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Her API isteğinde (endpoint) yeni bir veritabanı oturumu açıp, 
# istek bittiğinde güvenlice kapanmasını sağlayan yardımcı bir fonksiyon (Dependency Injection).
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
