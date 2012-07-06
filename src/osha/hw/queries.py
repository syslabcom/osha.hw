# SQL queries

pg_create_ocps = """
CREATE TABLE hw_ocps
(
  id character varying(255) NOT NULL,
  title character varying(255),
  description text,
  manager character varying(255),
  street character varying(255),
  addressextra character varying(255),
  city character varying(255),
  zipcode character varying(255),
  country character varying(255),
  email character varying(255),
  phone character varying(255),
  fax character varying(255),
  url character varying(255),
  campaignurl character varying(255),
  organisationtype character varying(255),
  businesssector character varying(255),
  missionstatement text,
  campaign_pledge text,
  ceoname character varying(255),
  keyname character varying(255),
  keyposition character varying(255),
  keyemail character varying(255),
  keytel character varying(255),
  representativename character varying(255),
  representativeemail character varying(255),
  representativetel character varying(255),
  subject character varying(255),
  location character varying(255),
  language character varying(255),
  effectivedate date,
  expirationdate date,
  creation_date date,
  modification_date date,
  CONSTRAINT hw_ocps_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
"""

pg_create_fops = """
CREATE TABLE hw_fops
(
  id character varying(255) NOT NULL,
  title character varying(255),
  description text,
  manager character varying(255),
  street character varying(255),
  addressextra character varying(255),
  city character varying(255),
  zipcode character varying(255),
  country character varying(255),
  email character varying(255),
  phone character varying(255),
  fax character varying(255),
  url character varying(255),
  campaignurl character varying(255),
  organisationtype character varying(255),
  businesssector character varying(255),
  missionstatement text,
  ceoname character varying(255),
  keyname character varying(255),
  keyposition character varying(255),
  keyemail character varying(255),
  keytel character varying(255),
  representativename character varying(255),
  representativeemail character varying(255),
  representativetel character varying(255),
  subject character varying(255),
  location character varying(255),
  language character varying(255),
  effectivedate date,
  expirationdate date,
  creation_date date,
  modification_date date,
  CONSTRAINT hw_fops_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
"""

pg_create_ocp_events = """
CREATE TABLE ocp_events
(
  partner_id character varying(255) NOT NULL,
  id character varying(255) NOT NULL,
  url character varying(255),
  CONSTRAINT ocp_events_pkey PRIMARY KEY (partner_id , id )
)
WITH (
  OIDS=FALSE
);
"""

pg_create_ocp_news = """
CREATE TABLE ocp_news
(
  partner_id character varying(255) NOT NULL,
  id character varying(255) NOT NULL,
  url character varying(255),
  CONSTRAINT ocp_news_pkey PRIMARY KEY (partner_id , id )
)
WITH (
  OIDS=FALSE
);
"""

pg_create_fop_events = """
CREATE TABLE fop_events
(
  partner_id character varying(255) NOT NULL,
  id character varying(255) NOT NULL,
  url character varying(255),
  CONSTRAINT fop_events_pkey PRIMARY KEY (partner_id , id )
)
WITH (
  OIDS=FALSE
);
"""

pg_create_fop_news = """
CREATE TABLE fop_news
(
  partner_id character varying(255) NOT NULL,
  id character varying(255) NOT NULL,
  url character varying(255),
  CONSTRAINT fop_news_pkey PRIMARY KEY (partner_id , id )
)
WITH (
  OIDS=FALSE
);
"""

create_statements = (
    pg_create_ocps,
    pg_create_fops,
    pg_create_ocp_events,
    pg_create_fop_events,
    pg_create_ocp_news,
    pg_create_fop_news,
)

drop_statements = """
    DROP TABLE IF EXISTS hw_ocps;
    DROP TABLE IF EXISTS hw_fops;
    DROP TABLE IF EXISTS ocp_events;
    DROP TABLE IF EXISTS fop_events;
    DROP TABLE IF EXISTS ocp_news;
    DROP TABLE IF EXISTS fop_news;
"""

is_ocp_available = """
SELECT count(*) from hw_ocps
WHERE id = '%(id)s'"""

insert_ocp = """
INSERT INTO hw_ocps
("id", "title", "description", "manager", "street",
"addressextra", "city", "zipcode", "country", "email", "phone", "fax", "url",
"campaignurl", "organisationtype", "businesssector", "missionstatement",
"campaign_pledge","ceoname", "keyname", "keyposition", "keyemail", "keytel",
"representativename", "representativeemail", "representativetel", "subject",
"location", "language", "effectivedate", "expirationdate", 
"creation_date", "modification_date")
VALUES
('%(id)s', '%(title)s', '%(description)s', '%(manager)s', '%(street)s',
'%(addressextra)s', '%(city)s', '%(zipcode)s', '%(country)s', '%(email)s', '%(phone)s', '%(fax)s', '%(url)s',
'%(campaignurl)s', '%(organisationtype)s', '%(businesssector)s', '%(missionstatement)s',
'%(campaign_pledge)s','%(ceoname)s', '%(keyname)s', '%(keyposition)s', '%(keyemail)s', '%(keytel)s',
'%(representativename)s', '%(representativeemail)s', '%(representativetel)s', '%(subject)s',
'%(location)s', '%(language)s', '%(effectivedate)s', '%(expirationdate)s', 
'%(creation_date)s', '%(modification_date)s')
"""

update_ocp = """
UPDATE hw_ocps SET
("title", "description", "manager", "street",
"addressextra", "city", "zipcode", "country", "email", "phone", "fax", "url",
"campaignurl", "organisationtype", "businesssector", "missionstatement",
"campaign_pledge","ceoname", "keyname", "keyposition", "keyemail", "keytel",
"representativename", "representativeemail", "representativetel", "subject",
"location", "language", "effectivedate", "expirationdate", 
"creation_date", "modification_date") =
('%(title)s', '%(description)s', '%(manager)s', '%(street)s',
'%(addressextra)s', '%(city)s', '%(zipcode)s', '%(country)s', '%(email)s', '%(phone)s', '%(fax)s', '%(url)s',
'%(campaignurl)s', '%(organisationtype)s', '%(businesssector)s', '%(missionstatement)s',
'%(campaign_pledge)s','%(ceoname)s', '%(keyname)s', '%(keyposition)s', '%(keyemail)s', '%(keytel)s',
'%(representativename)s', '%(representativeemail)s', '%(representativetel)s', '%(subject)s',
'%(location)s', '%(language)s', '%(effectivedate)s', '%(expirationdate)s', 
'%(creation_date)s', '%(modification_date)s')
WHERE ID = '%(id)s'
"""

is_fop_available = """
SELECT count(*) FROM hw_fops
WHERE id = '%(id)s'"""

insert_fop = """
INSERT INTO hw_fops
("id", "title", "description", "manager", "street",
"addressextra", "city", "zipcode", "country", "email", "phone", "fax", "url",
"campaignurl", "organisationtype", "businesssector", "missionstatement",
"ceoname", "keyname", "keyposition", "keyemail", "keytel",
"representativename", "representativeemail", "representativetel", "subject",
"location", "language", "effectivedate", "expirationdate", 
"creation_date", "modification_date")
VALUES
('%(id)s', '%(title)s', '%(description)s', '%(manager)s', '%(street)s',
'%(addressextra)s', '%(city)s', '%(zipcode)s', '%(country)s', '%(email)s', '%(phone)s', '%(fax)s', '%(url)s',
'%(campaignurl)s', '%(organisationtype)s', '%(businesssector)s', '%(missionstatement)s',
'%(ceoname)s', '%(keyname)s', '%(keyposition)s', '%(keyemail)s', '%(keytel)s',
'%(representativename)s', '%(representativeemail)s', '%(representativetel)s', '%(subject)s',
'%(location)s', '%(language)s', '%(effectivedate)s', '%(expirationdate)s', 
'%(creation_date)s', '%(modification_date)s')
"""

update_fop = """
UPDATE hw_fops SET
("title", "description", "manager", "street",
"addressextra", "city", "zipcode", "country", "email", "phone", "fax", "url",
"campaignurl", "organisationtype", "businesssector", "missionstatement",
"ceoname", "keyname", "keyposition", "keyemail", "keytel",
"representativename", "representativeemail", "representativetel", "subject",
"location", "language", "effectivedate", "expirationdate", 
"creation_date", "modification_date") =
('%(title)s', '%(description)s', '%(manager)s', '%(street)s',
'%(addressextra)s', '%(city)s', '%(zipcode)s', '%(country)s', '%(email)s', '%(phone)s', '%(fax)s', '%(url)s',
'%(campaignurl)s', '%(organisationtype)s', '%(businesssector)s', '%(missionstatement)s',
'%(ceoname)s', '%(keyname)s', '%(keyposition)s', '%(keyemail)s', '%(keytel)s',
'%(representativename)s', '%(representativeemail)s', '%(representativetel)s', '%(subject)s',
'%(location)s', '%(language)s', '%(effectivedate)s', '%(expirationdate)s', 
'%(creation_date)s', '%(modification_date)s')
WHERE ID = '%(id)s'
"""

get_ocps = """
SELECT * FROM hw_ocps
ORDER BY title"""

get_fops = """
SELECT * FROM hw_fops
ORDER BY title"""

get_ocp_by_id = """
SELECT * FROM hw_ocps
WHERE id='%(id)s'"""

get_fop_by_id = """
SELECT * FROM hw_fops
WHERE id='%(id)s'"""

is_ocp_event_available = """
SELECT count(*) FROM ocp_events
WHERE partner_id='%(partner_id)s' AND id='%(id)s'
"""

is_fop_event_available = """
SELECT count(*) FROM fop_events
WHERE partner_id='%(partner_id)s' AND id='%(id)s'
"""

get_ocp_events = """
SELECT * FROM ocp_events
WHERE partner_id='%(partner_id)s'"""

get_fop_events = """
SELECT * FROM fop_events
WHERE partner_id='%(partner_id)s'"""

get_ocp_news = """
SELECT * FROM ocp_news
WHERE partner_id='%(partner_id)s'"""

get_fop_news = """
SELECT * FROM fop_news
WHERE partner_id='%(partner_id)s'"""


insert_ocp_event = """
INSERT INTO ocp_events
("partner_id", "id", "url")
VALUES
('%(partner_id)s', '%(id)s', '%(url)s')
"""

update_ocp_event = """
UPDATE ocp_events SET
url = '%(url)s'
WHERE
partner_id='%(partner_id)s' AND id='%(id)s'
"""

insert_fop_event = """
INSERT INTO fop_events
("partner_id", "id", "url")
VALUES
('%(partner_id)s', '%(id)s', '%(url)s')
"""

update_fop_event = """
UPDATE fop_events SET
url = '%(url)s'
WHERE
partner_id='%(partner_id)s' AND id='%(id)s'
"""

is_ocp_news_available = """
SELECT count(*) FROM ocp_news
WHERE partner_id='%(partner_id)s' AND id='%(id)s'
"""

is_fop_news_available = """
SELECT count(*) FROM fop_news
WHERE partner_id='%(partner_id)s' AND id='%(id)s'
"""

insert_ocp_news = """
INSERT INTO ocp_news
("partner_id", "id", "url")
VALUES
('%(partner_id)s', '%(id)s', '%(url)s')
"""

update_ocp_news = """
UPDATE ocp_news SET
url = '%(url)s'
WHERE
partner_id='%(partner_id)s' AND id='%(id)s'
"""

insert_fop_news = """
INSERT INTO fop_news
("partner_id", "id", "url")
VALUES
('%(partner_id)s', '%(id)s', '%(url)s')
"""

update_fop_news = """
UPDATE fop_news SET
url = '%(url)s'
WHERE
partner_id='%(partner_id)s' AND id='%(id)s'
"""


# queries for the campaign charter

create_hw2012_charter = """
CREATE TABLE registration2012 (
    "ID" serial,
    "Firstname" character varying(255),
    "Lastname" character varying(255),
    "Address" character varying(255),
    "Postalcode" character varying(255),
    "City" character varying(255),
    "Country" character varying(255),
    "Email" character varying(255),
    "Telephone" character varying(255),
    "Organisation" character varying(255),
    "Function" character varying(255),
    "Language" character varying(255),
    "Commitment_other" character varying(255),
    "Date" date,
    "Commitment" bit varying,
    "Sector" character varying(255)
);
ALTER TABLE ONLY registration2012
    ADD CONSTRAINT registration_pkey_2012 PRIMARY KEY ("ID");
"""
insert_hw2012_charter = """
INSERT INTO registration2012
("Firstname", "Lastname", "Address", "Postalcode", "City", "Country", "Email", 
"Telephone", "Organisation", "Function", "Language", "Commitment_other", 
"Date", "Commitment", "Sector")
Values
('%(Firstname)s', '%(Lastname)s', '%(Address)s', '%(Postalcode)s', 
'%(City)s', '%(Country)s', '%(Email)s', '%(Telephone)s', 
'%(Organisation)s', '%(Function)s', '%(Language)s', '%(Commitment_other)s', 
'%(Date)s', '%(Commitment)s', '%(Sector)s')
"""