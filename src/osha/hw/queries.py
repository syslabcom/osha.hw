# SQL queries

pg_create_ocps = """
CREATE TABLE campaign_ocps
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
  CONSTRAINT campaign_ocps_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE campaign_ocps OWNER TO postgres;
"""

pg_create_fops = """
CREATE TABLE campaign_fops
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
  CONSTRAINT campaign_fops_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE campaign_fops OWNER TO postgres;
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
ALTER TABLE ocp_events OWNER TO postgres;
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
ALTER TABLE ocp_news OWNER TO postgres;
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
ALTER TABLE fop_events OWNER TO postgres;
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
ALTER TABLE fop_news OWNER TO postgres;
"""

create_statements = (
    pg_create_ocps,
    pg_create_fops,
    pg_create_ocp_events,
    pg_create_fop_events,
    pg_create_ocp_news,
    pg_create_fop_news,
)

is_ocp_available = """
SELECT count(*) from campaign_ocps
WHERE id = '%(id)s'"""

insert_ocp = """
INSERT INTO campaign_ocps
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
UPDATE campaign_ocps SET
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
SELECT count(*) from campaign_fops
WHERE id = '%(id)s'"""

insert_fop = """
INSERT INTO campaign_fops
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
UPDATE campaign_fops SET
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
