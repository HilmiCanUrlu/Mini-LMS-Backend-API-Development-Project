from typing import Any, Optional
import datetime
import decimal

from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, NCHAR, Numeric, PrimaryKeyConstraint, String, Table, Unicode, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import NullType

class Base(DeclarativeBase):
    pass


t_AuditLog = Table(
    'AuditLog', Base.metadata,
    Column('log_id', Integer),
    Column('tablo_adi', NCHAR(10, 'Turkish_CI_AS')),
    Column('islem_tipi', NCHAR(10, 'Turkish_CI_AS')),
    Column('eski_deger', Unicode(255, 'Turkish_CI_AS')),
    Column('yeni_deger', Unicode(255, 'Turkish_CI_AS')),
    Column('kullanici', NCHAR(10, 'Turkish_CI_AS')),
    Column('tarih', Date)
)


t_BolumBaskani = Table(
    'BolumBaskani', Base.metadata,
    Column('bolum_id', Integer, nullable=False),
    Column('bolum_adi', String(50, 'Turkish_CI_AS')),
    Column('ogrenci_id', Integer, nullable=False),
    Column('ogrenci_ad_soyad', String(101, 'Turkish_CI_AS')),
    Column('ders_id', Integer, nullable=False),
    Column('ders_adi', String(50, 'Turkish_CI_AS')),
    Column('vize', Integer),
    Column('final', Integer),
    Column('ortalama', Numeric(13, 1))
)


class Bolumler(Base):
    __tablename__ = 'Bolumler'
    __table_args__ = (
        PrimaryKeyConstraint('bolum_id', name='PK_Bolumler'),
    )

    bolum_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bolum_adi: Mapped[Optional[str]] = mapped_column(String(50, 'Turkish_CI_AS'))
    fakulte_adi: Mapped[Optional[str]] = mapped_column(String(50, 'Turkish_CI_AS'))

    Dersler: Mapped[list['Dersler']] = relationship('Dersler', back_populates='bolum')
    Ogrenciler: Mapped[list['Ogrenciler']] = relationship('Ogrenciler', back_populates='bolum')


class Kullanicilar(Base):
    __tablename__ = 'Kullanicilar'
    __table_args__ = (
        PrimaryKeyConstraint('ogretmen_id', name='PK_Kullanicilar'),
    )

    ogretmen_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kullanici_adi: Mapped[str] = mapped_column(Unicode(50, 'Turkish_CI_AS'), nullable=False)
    sifre: Mapped[str] = mapped_column(Unicode(50, 'Turkish_CI_AS'), nullable=False)

    Dersler: Mapped[list['Dersler']] = relationship('Dersler', back_populates='ogretmen')


t_OgrenciSorgu = Table(
    'OgrenciSorgu', Base.metadata,
    Column('ogrenci_id', Integer, nullable=False),
    Column('ogrenci_ad_soyad', String(101, 'Turkish_CI_AS')),
    Column('ders_adi', String(50, 'Turkish_CI_AS')),
    Column('vize', Integer),
    Column('final', Integer),
    Column('ortalama', Numeric(13, 1))
)


t_OgretmenDersListesi = Table(
    'OgretmenDersListesi', Base.metadata,
    Column('ogretmen_id', Integer),
    Column('ders_adi', String(50, 'Turkish_CI_AS')),
    Column('ogrenci_id', Integer, nullable=False),
    Column('ogrenci_ad_soyad', String(101, 'Turkish_CI_AS')),
    Column('vize', Integer),
    Column('final', Integer),
    Column('ortalama', Numeric(13, 1))
)


class Quizler(Base):
    __tablename__ = 'Quizler'
    __table_args__ = (
        PrimaryKeyConstraint('quiz_id', name='PK_Quizler'),
    )

    quiz_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ders_id: Mapped[Optional[int]] = mapped_column(Integer)
    tarih: Mapped[Optional[datetime.date]] = mapped_column(Date)
    agirlik_orani: Mapped[Optional[int]] = mapped_column(Integer)


class Roller(Base):
    __tablename__ = 'Roller'
    __table_args__ = (
        PrimaryKeyConstraint('rol_id', name='PK_Roller'),
    )

    rol_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rol_adi: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Turkish_CI_AS'))


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B6128DA90B8'),
        Index('UK_principal_name', 'principal_id', 'name', mssql_clustered=False, unique=True)
    )

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    principal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    diagram_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer)
    definition: Mapped[Optional[bytes]] = mapped_column(LargeBinary)


t_vw_Bolum_Basarı_Raporu = Table(
    'vw_Bolum_Basarı_Raporu', Base.metadata,
    Column('Fakulte', String(50, 'Turkish_CI_AS')),
    Column('Bolum', String(50, 'Turkish_CI_AS')),
    Column('Toplam_Ogrenci', Integer),
    Column('Ders_Alan_Ogrenci', Integer),
    Column('Bolum_Ortalaması', Numeric(38, 6)),
    Column('En_Basarılı_Ogrenci', Unicode(131, 'Turkish_CI_AS'))
)


t_vw_Ders_Analiz = Table(
    'vw_Ders_Analiz', Base.metadata,
    Column('Ders', String(50, 'Turkish_CI_AS')),
    Column('Ogrenci_Sayisi', Integer),
    Column('Ortalama_Not', Numeric(38, 6)),
    Column('Basari_Orani', Numeric(26, 12))
)


t_vw_OgrenciNotOrtalamalari = Table(
    'vw_OgrenciNotOrtalamalari', Base.metadata,
    Column('ogrenci_id', Integer, nullable=False),
    Column('ad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('soyad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('bolum_id', Integer, nullable=False),
    Column('Ortalama', Numeric(38, 6))
)


t_vw_TranskriptSenaryosu2 = Table(
    'vw_TranskriptSenaryosu2', Base.metadata,
    Column('Ogrenci_Numarası', Integer, nullable=False),
    Column('Ad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('Soyad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('Bolum', String(50, 'Turkish_CI_AS')),
    Column('Ders', String(50, 'Turkish_CI_AS')),
    Column('Vize', Integer),
    Column('Final', Integer),
    Column('Ortalama', Numeric(13, 1)),
    Column('Durum', String(21, 'Turkish_CI_AS'), nullable=False)
)


t_vw_notlarvedurumbilgisi = Table(
    'vw_notlarvedurumbilgisi', Base.metadata,
    Column('ogrenci_id', Integer, nullable=False),
    Column('vize', Integer),
    Column('final', Integer),
    Column('Ortalama', Numeric(13, 1)),
    Column('Durum', String(14, 'Turkish_CI_AS'), nullable=False)
)


t_vw_ogrencibilgileri = Table(
    'vw_ogrencibilgileri', Base.metadata,
    Column('ogrenci_id', Integer, nullable=False),
    Column('ad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('soyad', String(50, 'Turkish_CI_AS'), nullable=False),
    Column('bolum_adi', String(50, 'Turkish_CI_AS'))
)


t_vw_ogrencilerinaldigidersler = Table(
    'vw_ogrencilerinaldigidersler', Base.metadata,
    Column('ogrenci_id', Integer, nullable=False),
    Column('ders_adi', String(50, 'Turkish_CI_AS'))
)


class Dersler(Base):
    __tablename__ = 'Dersler'
    __table_args__ = (
        ForeignKeyConstraint(['bolum_id'], ['Bolumler.bolum_id'], name='FK_Dersler_Bolumler'),
        ForeignKeyConstraint(['ogretmen_id'], ['Kullanicilar.ogretmen_id'], name='FK_Dersler_Kullanicilar'),
        PrimaryKeyConstraint('ders_id', name='PK_Dersler')
    )

    ders_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ders_adi: Mapped[Optional[str]] = mapped_column(String(50, 'Turkish_CI_AS'))
    bolum_id: Mapped[Optional[int]] = mapped_column(Integer)
    ogretmen_id: Mapped[Optional[int]] = mapped_column(Integer)

    bolum: Mapped[Optional['Bolumler']] = relationship('Bolumler', back_populates='Dersler')
    ogretmen: Mapped[Optional['Kullanicilar']] = relationship('Kullanicilar', back_populates='Dersler')
    DersKayitlari: Mapped[list['DersKayitlari']] = relationship('DersKayitlari', back_populates='ders')
    Notlar: Mapped[list['Notlar']] = relationship('Notlar', back_populates='ders')
    Odevler: Mapped[list['Odevler']] = relationship('Odevler', back_populates='ders')


t_KullaniciRolleri = Table(
    'KullaniciRolleri', Base.metadata,
    Column('rol_id', Integer),
    Column('ogretmen_id', Integer),
    ForeignKeyConstraint(['rol_id'], ['Roller.rol_id'], name='FK_KullaniciRolleri_Roller'),
    ForeignKeyConstraint(['rol_id'], ['Kullanicilar.ogretmen_id'], name='FK_KullaniciRolleri_Kullanicilar')
)


class Ogrenciler(Base):
    __tablename__ = 'Ogrenciler'
    __table_args__ = (
        ForeignKeyConstraint(['bolum_id'], ['Bolumler.bolum_id'], name='FK_Ogrenciler_Bolumler'),
        PrimaryKeyConstraint('ogrenci_id', name='PK_Ogrenciler')
    )

    ogrenci_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    ad: Mapped[Optional[str]] = mapped_column(String(50, 'Turkish_CI_AS'))
    soyad: Mapped[Optional[str]] = mapped_column(String(50, 'Turkish_CI_AS'))
    bolum_id: Mapped[Optional[int]] = mapped_column(Integer)
    kayit_tarihi: Mapped[Optional[datetime.date]] = mapped_column(Date)
    sifre: Mapped[Optional[int]] = mapped_column(Integer)

    bolum: Mapped[Optional['Bolumler']] = relationship('Bolumler', back_populates='Ogrenciler')
    DersKayitlari: Mapped[list['DersKayitlari']] = relationship('DersKayitlari', back_populates='ogrenci')
    Notlar: Mapped[list['Notlar']] = relationship('Notlar', back_populates='ogrenci')
    NotlarHistory: Mapped[list['NotlarHistory']] = relationship('NotlarHistory', back_populates='ogrenci')


class DersKayitlari(Base):
    __tablename__ = 'DersKayitlari'
    __table_args__ = (
        ForeignKeyConstraint(['ders_id'], ['Dersler.ders_id'], name='FK_DersKayitlari_Dersler'),
        ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_DersKayitlari_Ogrenciler'),
        PrimaryKeyConstraint('kayit_id', name='PK_DersKayitlari'),
        Index('idx_DersKayitlari_ogrenci_ders', 'ogrenci_id', 'ders_id', mssql_clustered=False)
    )

    kayit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ogrenci_id: Mapped[Optional[int]] = mapped_column(Integer)
    ders_id: Mapped[Optional[int]] = mapped_column(Integer)
    kayit_tarihi: Mapped[Optional[datetime.date]] = mapped_column(Date)

    ders: Mapped[Optional['Dersler']] = relationship('Dersler', back_populates='DersKayitlari')
    ogrenci: Mapped[Optional['Ogrenciler']] = relationship('Ogrenciler', back_populates='DersKayitlari')


t_Devamsizlik = Table(
    'Devamsizlik', Base.metadata,
    Column('ogrenci_id', Integer),
    Column('ders_id', Integer),
    Column('toplam_ders', Integer),
    Column('katilim_sayisi', Integer),
    Column('durum', Unicode(20, 'Turkish_CI_AS')),
    ForeignKeyConstraint(['ders_id'], ['Dersler.ders_id'], name='FK_Devamsizlik_Dersler'),
    ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_Devamsizlik_Ogrenciler'),
    Index('idx_Devamsizlik', 'ogrenci_id', 'ders_id', mssql_clustered=False)
)


class Notlar(Base):
    __tablename__ = 'Notlar'
    __table_args__ = (
        ForeignKeyConstraint(['ders_id'], ['Dersler.ders_id'], name='FK_Notlar_Dersler'),
        ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_Notlar_Ogrenciler1'),
        PrimaryKeyConstraint('not_id', name='PK_Notlar'),
        Index('IX_Notlar_OgrenciID', 'ogrenci_id', mssql_clustered=False),
        Index('idx_Notlar_ogrenci_ders', 'ogrenci_id', 'ders_id', mssql_clustered=False)
    )

    not_id: Mapped[int] = mapped_column(Integer, Identity(start=20, increment=1), primary_key=True)
    ogrenci_id: Mapped[Optional[int]] = mapped_column(Integer)
    ders_id: Mapped[Optional[int]] = mapped_column(Integer)
    vize: Mapped[Optional[int]] = mapped_column(Integer)
    final: Mapped[Optional[int]] = mapped_column(Integer)

    ders: Mapped[Optional['Dersler']] = relationship('Dersler', back_populates='Notlar')
    ogrenci: Mapped[Optional['Ogrenciler']] = relationship('Ogrenciler', back_populates='Notlar')
    NotlarHistory: Mapped[list['NotlarHistory']] = relationship('NotlarHistory', back_populates='not_')


class Odevler(Base):
    __tablename__ = 'Odevler'
    __table_args__ = (
        ForeignKeyConstraint(['ders_id'], ['Dersler.ders_id'], name='FK_Odevler_Dersler'),
        PrimaryKeyConstraint('odev_id', name='PK_Odevler')
    )

    odev_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ders_id: Mapped[Optional[int]] = mapped_column(Integer)
    baslik: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'Turkish_CI_AS'))
    son_tarih: Mapped[Optional[datetime.date]] = mapped_column(Date)
    agirlik_orani: Mapped[Optional[int]] = mapped_column(Integer)

    ders: Mapped[Optional['Dersler']] = relationship('Dersler', back_populates='Odevler')


t_QuizNotlari = Table(
    'QuizNotlari', Base.metadata,
    Column('ogrenci_id', Integer),
    Column('quiz_id', Integer),
    Column('notu', Integer),
    ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_QuizNotlari_Ogrenciler'),
    ForeignKeyConstraint(['quiz_id'], ['Quizler.quiz_id'], name='FK_QuizNotlari_Quizler'),
    Index('uq_QuizNotlari', 'ogrenci_id', 'quiz_id', mssql_clustered=False, unique=True)
)


class NotlarHistory(Base):
    __tablename__ = 'NotlarHistory'
    __table_args__ = (
        ForeignKeyConstraint(['not_id'], ['Notlar.not_id'], name='FK_NotlarHistory_Notlar'),
        ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_NotlarHistory_Ogrenciler'),
        PrimaryKeyConstraint('history_id', name='PK__NotlarHi__096AA2E9CF56871A')
    )

    history_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    not_id: Mapped[Optional[int]] = mapped_column(Integer)
    ogrenci_id: Mapped[Optional[int]] = mapped_column(Integer)
    ders_id: Mapped[Optional[int]] = mapped_column(Integer)
    eski_vize: Mapped[Optional[int]] = mapped_column(Integer)
    eski_final: Mapped[Optional[int]] = mapped_column(Integer)
    eski_ortalama: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(5, 2))
    degistiren_kullanici: Mapped[Optional[str]] = mapped_column(Unicode(100, 'Turkish_CI_AS'))
    degistirme_tarihi: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))

    not_: Mapped[Optional['Notlar']] = relationship('Notlar', back_populates='NotlarHistory')
    ogrenci: Mapped[Optional['Ogrenciler']] = relationship('Ogrenciler', back_populates='NotlarHistory')


t_OdevNotlari = Table(
    'OdevNotlari', Base.metadata,
    Column('ogrenci_id', Integer),
    Column('odev_id', Integer, nullable=False),
    Column('notu', Integer),
    ForeignKeyConstraint(['ogrenci_id'], ['Odevler.odev_id'], name='FK_OdevNotlari_Odevler'),
    ForeignKeyConstraint(['ogrenci_id'], ['Ogrenciler.ogrenci_id'], name='FK_OdevNotlari_Ogrenciler'),
    Index('uq_OdevNotlari', 'ogrenci_id', 'odev_id', mssql_clustered=False, unique=True)
)
