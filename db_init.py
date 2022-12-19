import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """
    create table if not exists kullanici
    (
        kullanıcı_id  char(5)  not null,
        primary key(kullanıcı_id)
    );
    """,
    """
    create table if not exists admin
    (
        admin_ad  varchar(18),
        admin_sifre  varchar(18),
        kullanıcı_id  char(5)  not null,
        primary key(kullanıcı_id)
    );
    """,
    """
    create table if not exists uye
    (
        uye_ad  varchar(18),
        uye_sifre  varchar(18),
        kullanıcı_id  char(5)  not null,
        primary key(kullanıcı_id) 
    );
    """,
    """
    create table if not exists ziyaretci
    (
        kullanıcı_id  char(5)  not null,
        primary key(kullanıcı_id)
    );

    """,
    """
    create table if not exists siparis
    (
        siparis_id  char(10)  not null ,
        kullanıcı_id  char(5)  not null,
        siparis_tarihi  date,
        primary key(siparis_id)
    );

    alter table siparis
        drop constraint if exists olusturulur;
    alter table siparis
        add constraint olusturulur foreign key (kullanıcı_id) references kullanici(kullanıcı_id) on delete set null;
    """,
    """
    create table if not exists ilac
    (
        ilac_id  char(10)  not null ,
        siparis_id  char(10) ,
        firma_id  char(5)  not null,
        ilac_cesidi  varchar(18) ,
        ilac_adi  varchar(18) ,
        son_kullanma_tarihi  date,
        primary key (ilac_id)
    );

    alter table ilac
        drop constraint if exists uretılır;
    alter table ilac
        add constraint uretılır foreign key (ilac_id) references ilac(ilac_id) on delete set null;

    alter table ilac
        drop constraint if exists siparis_edilir;
    alter table ilac
        add constraint siparis_edilir foreign key (siparis_id) references siparis(siparis_id) on delete set null;
    """,
    """
    create table if not exists firma
    (
        firma_id  char(5)  not null ,
        firma_ad  varchar(18) ,
        firma_adres  varchar(60) ,
        firma_tel_no  char(9) ,
        firma_e_posta  varchar(18) ,
        ilac_id  char(10)  not null,
        primary key (firma_id)
    );
    """,
    """   
    create table if not exists eczane
    (
        eczane_id  char(5) not null ,
        eczane_ad  varchar(18) ,
        eczane_adres  varchar(60) ,
        eczane_tel_no  char(9) ,
        eczane_e_posta  varchar(18),
        primary key (eczane_id)
    );
    """,
    """
    create table if not exists anlasma_saglar
    (
        eczane_id  char(5) not null ,
        firma_id  char(5)  not null ,
        primary key (eczane_id, firma_id),
        foreign key (eczane_id) references eczane(eczane_id),
        foreign key (firma_id) references firma(firma_id)
    );
    """,
    """
    create table if not exists eczane_siparis
    (
        eczane_id  char(5) not null ,
        siparis_id  char(10)  not null ,
        primary key (eczane_id, siparis_id),
        foreign key (eczane_id) references eczane(eczane_id)
    );

    alter table eczane_siparis
	    drop constraint if exists eczane_siparis_fk1;
    alter table eczane_siparis
	    add constraint  eczane_siparis_fk1 foreign key (siparis_id) references siparis(siparis_id) on delete cascade;
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py")  # , file=sys.stderr)
        sys.exit(1)
    initialize(url)
