import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# .ENV Dosyasından ayarlamalar okunur
load_dotenv()

# JWT'nin kırılamaz olmasını sağlayan şifre (Bu projede basit bir örnek kullandım)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hilmi_mini_lms_cok_gizli_anahtar_999")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token 1 Saat Geçerli Olacak

# Bcrypt hash kütüphanesi hazır (Ama bizim DB'deki şifreler "int" veya düz metin olduğu için esneklik sağlandı)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Frontend'de kilit (Authenticate) ikonu çıkaracak Swagger bağlantısı
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def verify_password(plain_password, stored_password):
    """
    Kullanıcının girdiği şifre (plain_password) ile veritabanındaki (stored_password) karşılaştırılır.
    Veritabanımızda henüz hash'li şifre saklamıyorsak, verileri güvenle Text olarak eşleştiriyoruz.
    """
    return str(plain_password) == str(stored_password)

def create_access_token(data: dict):
    """
    Kullanıcı başarılı giriş yaptığında eline verilecek dijital VIP Kartı (JWT Token) üretimi
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Eğer bir "Kilitli/Korunan" endpoint varsa (Örn: Sadece öğretmenler not girebilir)
    diğer API dosyaları bu kütüphaneyi çağırarak gelen kişinin rolünü (student veya teacher) kontrol edebilir.
    """
    try:
        # Tokeni decode ederek içinden bizim koyduğumuz "sub" (Kullanıcı İD'si) bilgisine ulaş.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Yetkilendirme Başarısız: Token İçeriği Hatalı.")
        return payload  # Token içindeki bütün sözlüğü döner. (Örn: role='ogretmen')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Oturum süreniz (1 Saat) doldu. Lütfen tekrar Login olun.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Geçersiz (Kırık) Token Gönderimi.")
