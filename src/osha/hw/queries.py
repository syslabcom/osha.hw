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
  campaignpledge text,
  ceoname character varying(255),
  keyname character varying(255),
  keyposition character varying(255),
  keyemail character varying(255),
  keytel character varying(255),
  representativename character varying(255),
  representativeemail character varying(255),
  representativetel character varying(255),
  subject character varying(255),
  relateditems character varying(255),
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
  relateditems character varying(255),
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
