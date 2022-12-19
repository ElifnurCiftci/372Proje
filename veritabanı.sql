CREATE TABLE KULLANICI
(
	kullanıcı_id  CHAR(5)  NOT NULL
);

ALTER TABLE KULLANICI
	ADD CONSTRAINT  XPKKULLANICI PRIMARY KEY (kullanıcı_id);

CREATE TABLE ADMIN
(
	admin_ad  VARCHAR(18),
	admin_sifre  VARCHAR(18),
	kullanıcı_id  CHAR(5)  NOT NULL 
);

ALTER TABLE ADMIN
	ADD CONSTRAINT  XPKADMIN PRIMARY KEY (kullanıcı_id);

CREATE TABLE UYE
(
	uye_ad  VARCHAR(18),
	uye_sifre  VARCHAR(18),
	kullanıcı_id  CHAR(5)  NOT NULL 
);

ALTER TABLE UYE
	ADD CONSTRAINT  XPKUYE PRIMARY KEY (kullanıcı_id);

CREATE TABLE ZIYARETCI
(
	kullanıcı_id  CHAR(5)  NOT NULL 
);

ALTER TABLE ZIYARETCI
	ADD CONSTRAINT  XPKZIYARETCI PRIMARY KEY (kullanıcı_id);

CREATE TABLE SIPARIS
(
	siparis_id  CHAR(10)  NOT NULL ,
	kullanıcı_id  CHAR(5)  NOT NULL,
	siparis_tarihi  DATE  
);

ALTER TABLE SIPARIS
	ADD CONSTRAINT  XPKSIPARIS PRIMARY KEY (siparis_id);

ALTER TABLE SIPARIS
	ADD CONSTRAINT  olusturulur FOREIGN KEY (kullanıcı_id) REFERENCES KULLANICI(kullanıcı_id) ON DELETE SET NULL;

CREATE TABLE ILAC
(
	ilac_id  CHAR(10)  NOT NULL ,
	siparis_id  CHAR(10) ,
	firma_id  CHAR(5)  NOT NULL,
	ilac_cesidi  VARCHAR(18) ,
	ilac_adi  VARCHAR(18) ,
	son_kullanma_tarihi  DATE
);

ALTER TABLE ILAC
	ADD CONSTRAINT  XPKILAC PRIMARY KEY (ilac_id);

ALTER TABLE ILAC
	ADD CONSTRAINT  uretılır FOREIGN KEY (ilac_id) REFERENCES ILAC(ilac_id) ON DELETE SET NULL;

ALTER TABLE ILAC
	ADD CONSTRAINT  siparis_edilir FOREIGN KEY (siparis_id) REFERENCES SIPARIS(siparis_id) ON DELETE SET  ON UPDATE CASCADE;

CREATE TABLE FIRMA
(
	firma_id  CHAR(5)  NOT NULL ,
	firma_ad  VARCHAR(18) ,
	firma_adres  VARCHAR(60) ,
	firma_tel_no  CHAR(9) ,
	firma_e_posta  VARCHAR(18) ,
	ilac_id  CHAR(10)  NOT NULL 
);

ALTER TABLE FIRMA
	ADD CONSTRAINT  XPKFIRMA PRIMARY KEY (firma_id);
	
CREATE TABLE ECZANE
(
	eczane_id  CHAR(5) NOT NULL ,
	eczane_ad  VARCHAR(18) ,
	eczane_adres  VARCHAR(60) ,
	eczane_tel_no  CHAR(9) ,
	eczane_e_posta  VARCHAR(18)
);

ALTER TABLE ECZANE
	ADD CONSTRAINT  XPKECZANE PRIMARY KEY (eczane_id);
	
CREATE TABLE ANLASMA_SAGLAR
(
    eczane_id  CHAR(5) NOT NULL ,
	firma_id  CHAR(5)  NOT NULL ,
    PRIMARY KEY (eczane_id, firma_id),
    FOREIGN KEY (eczane_id) REFERENCES ECZANE(eczane_id),
    FOREIGN KEY (firma_id) REFERENCES FIRMA(firma_id)
);

CREATE TABLE ECZANE_SIPARIS
(
    eczane_id  CHAR(5) NOT NULL ,
	siparis_id  CHAR(10)  NOT NULL ,
    PRIMARY KEY (eczane_id, siparis_id),
    FOREIGN KEY (eczane_id) REFERENCES ECZANE(eczane_id)
);

ALTER TABLE ECZANE_SIPARIS
	DROP CONSTRAINT IF EXISTS eczane_siparis_fk1
ALTER TABLE ECZANE_SIPARIS
	ADD CONSTRAINT  eczane_siparis_fk1 FOREIGN KEY (siparis_id) REFERENCES SIPARIS(siparis_id) ON DELETE CASCADE;


ALTER TABLE ADMIN
	ADD CONSTRAINT  Is_a_KULLANICI FOREIGN KEY (kullanıcı_id) REFERENCES KULLANICI(kullanıcı_id) ON DELETE CASCADE;

ALTER TABLE UYE
	DROP CONSTRAINT IF EXISTS Is_a_KULLANICI
ALTER TABLE UYE
	ADD CONSTRAINT  Is_a_KULLANICI FOREIGN KEY (kullanıcı_id) REFERENCES KULLANICI(kullanıcı_id) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE ZIYARETCI
	ADD CONSTRAINT  Is_a_KULLANICI FOREIGN KEY (kullanıcı_id) REFERENCES KULLANICI(kullanıcı_id) ON DELETE CASCADE;