# Resmi Python Tabanı
FROM python:3.10-slim

# Container içi Sistem Güncellemesi ve SQL Server ODBC Yüklemesi İçin Gerekli Paketlerin Kurulumu
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Microsoft SQL Server (ODBC Driver 17) Repository Key Eklemesi
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

# ODBC Driver 17 Paket Yükleme (EULA Lisans Kuralları Otomatik Kabul Edilecek)
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && rm -rf /var/lib/apt/lists/*

# Uygulama Dizini
WORKDIR /app

# Sistem Kütüphanelerini Kopyala ve Yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama Dosyalarını Docker İçine Taşı
COPY . .

# Konteyner Dışına Port İzni
EXPOSE 8000

# Uvicorn Sunucusunu Başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
