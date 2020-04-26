--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--

DROP DATABASE template_postgis;
DROP DATABASE tofro;




--
-- Drop roles
--

DROP ROLE admin;


--
-- Roles
--

CREATE ROLE admin;
ALTER ROLE admin WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md580a19f669b02edfbc208a5386ab5036b';






--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO admin;

\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: admin
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: admin
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO admin;

\connect postgres

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: template_postgis; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE template_postgis WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE template_postgis OWNER TO admin;

\connect template_postgis

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: template_postgis; Type: DATABASE PROPERTIES; Schema: -; Owner: admin
--

ALTER DATABASE template_postgis IS_TEMPLATE = true;
ALTER DATABASE template_postgis SET search_path TO '$user', 'public', 'tiger';


\connect template_postgis

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO admin;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO admin;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO admin;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.2 (Debian 11.2-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tofro; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE tofro WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE tofro OWNER TO admin;

\connect tofro

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tofro; Type: DATABASE PROPERTIES; Schema: -; Owner: admin
--

ALTER DATABASE tofro SET search_path TO '$user', 'public', 'tiger';


\connect tofro

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO admin;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO admin;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO admin;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: admin
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO admin;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: core_event; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_event (
    id integer NOT NULL,
    datetime timestamp with time zone,
    event_type_id integer,
    user_id integer
);


ALTER TABLE public.core_event OWNER TO admin;

--
-- Name: core_event_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_event_id_seq OWNER TO admin;

--
-- Name: core_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_event_id_seq OWNED BY public.core_event.id;


--
-- Name: core_eventtype; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_eventtype (
    id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.core_eventtype OWNER TO admin;

--
-- Name: core_eventtype_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_eventtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_eventtype_id_seq OWNER TO admin;

--
-- Name: core_eventtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_eventtype_id_seq OWNED BY public.core_eventtype.id;


--
-- Name: core_helper; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_helper (
    user_ptr_id integer NOT NULL,
    user_type character varying(20),
    dbs_number character varying(12),
    access_to_car boolean,
    driving_license boolean,
    ts_and_cs_confirmed boolean,
    health_checklist_received boolean,
    key_worker boolean,
    id_received boolean,
    reference_details character varying(250),
    available_mon_morning boolean,
    available_mon_afternoon boolean,
    available_mon_evening boolean,
    available_tues_morning boolean,
    available_tues_afternoon boolean,
    available_tues_evening boolean,
    available_wed_morning boolean,
    available_wed_afternoon boolean,
    available_wed_evening boolean,
    available_thur_morning boolean,
    available_thur_afternoon boolean,
    available_thur_evening boolean,
    available_fri_morning boolean,
    available_fri_afternoon boolean,
    available_fri_evening boolean,
    available_sat_morning boolean,
    available_sat_afternoon boolean,
    available_sat_evening boolean,
    available_sun_morning boolean,
    available_sun_afternoon boolean,
    available_sun_evening boolean
);


ALTER TABLE public.core_helper OWNER TO admin;

--
-- Name: core_helperward; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_helperward (
    id integer NOT NULL,
    ward_id integer,
    helper_id integer
);


ALTER TABLE public.core_helperward OWNER TO admin;

--
-- Name: core_helperward_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_helperward_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_helperward_id_seq OWNER TO admin;

--
-- Name: core_helperward_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_helperward_id_seq OWNED BY public.core_helperward.id;


--
-- Name: core_helppreference; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_helppreference (
    id integer NOT NULL,
    help_type_id integer,
    helper_id integer
);


ALTER TABLE public.core_helppreference OWNER TO admin;

--
-- Name: core_helppreference_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_helppreference_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_helppreference_id_seq OWNER TO admin;

--
-- Name: core_helppreference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_helppreference_id_seq OWNED BY public.core_helppreference.id;


--
-- Name: core_helptype; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_helptype (
    id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.core_helptype OWNER TO admin;

--
-- Name: core_helptype_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_helptype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_helptype_id_seq OWNER TO admin;

--
-- Name: core_helptype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_helptype_id_seq OWNED BY public.core_helptype.id;


--
-- Name: core_job; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_job (
    id integer NOT NULL,
    added_by character varying(100),
    designated_coordinator character varying(100),
    call_datetime timestamp with time zone,
    call_duration interval,
    requested_datetime timestamp with time zone,
    "timeTaken" interval,
    notes character varying(500),
    public_description character varying(500),
    job_priority_id integer,
    job_status_id integer,
    helper_id integer,
    requester_id integer
);


ALTER TABLE public.core_job OWNER TO admin;

--
-- Name: core_job_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_job_id_seq OWNER TO admin;

--
-- Name: core_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_job_id_seq OWNED BY public.core_job.id;


--
-- Name: core_jobpriority; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_jobpriority (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.core_jobpriority OWNER TO admin;

--
-- Name: core_jobpriority_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_jobpriority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_jobpriority_id_seq OWNER TO admin;

--
-- Name: core_jobpriority_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_jobpriority_id_seq OWNED BY public.core_jobpriority.id;


--
-- Name: core_jobstatus; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_jobstatus (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.core_jobstatus OWNER TO admin;

--
-- Name: core_jobstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_jobstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_jobstatus_id_seq OWNER TO admin;

--
-- Name: core_jobstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_jobstatus_id_seq OWNED BY public.core_jobstatus.id;


--
-- Name: core_relationship; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_relationship (
    id integer NOT NULL,
    created_datetime timestamp with time zone,
    user_1_id integer,
    user_2_id integer
);


ALTER TABLE public.core_relationship OWNER TO admin;

--
-- Name: core_relationship_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_relationship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_relationship_id_seq OWNER TO admin;

--
-- Name: core_relationship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_relationship_id_seq OWNED BY public.core_relationship.id;


--
-- Name: core_requester; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_requester (
    user_ptr_id integer NOT NULL,
    user_type character varying(20),
    address_line_1 character varying(100),
    address_line_2 character varying(100),
    address_line_3 character varying(100),
    postcode character varying(100),
    internet_access boolean,
    smart_device boolean,
    confident_online_shopping boolean,
    confident_online_comms boolean,
    shielded boolean,
    ward_id integer
);


ALTER TABLE public.core_requester OWNER TO admin;

--
-- Name: core_user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_user (
    id integer NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    phone_number_primary character varying(15),
    phone_number_secondary character varying(15),
    email_primary character varying(15),
    email_secondary character varying(15),
    notes character varying(500)
);


ALTER TABLE public.core_user OWNER TO admin;

--
-- Name: core_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_user_id_seq OWNER TO admin;

--
-- Name: core_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_user_id_seq OWNED BY public.core_user.id;


--
-- Name: core_ward; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.core_ward (
    id integer NOT NULL,
    name character varying(50)
);


ALTER TABLE public.core_ward OWNER TO admin;

--
-- Name: core_ward_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.core_ward_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_ward_id_seq OWNER TO admin;

--
-- Name: core_ward_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.core_ward_id_seq OWNED BY public.core_ward.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: core_event id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_event ALTER COLUMN id SET DEFAULT nextval('public.core_event_id_seq'::regclass);


--
-- Name: core_eventtype id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_eventtype ALTER COLUMN id SET DEFAULT nextval('public.core_eventtype_id_seq'::regclass);


--
-- Name: core_helperward id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helperward ALTER COLUMN id SET DEFAULT nextval('public.core_helperward_id_seq'::regclass);


--
-- Name: core_helppreference id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helppreference ALTER COLUMN id SET DEFAULT nextval('public.core_helppreference_id_seq'::regclass);


--
-- Name: core_helptype id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helptype ALTER COLUMN id SET DEFAULT nextval('public.core_helptype_id_seq'::regclass);


--
-- Name: core_job id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job ALTER COLUMN id SET DEFAULT nextval('public.core_job_id_seq'::regclass);


--
-- Name: core_jobpriority id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_jobpriority ALTER COLUMN id SET DEFAULT nextval('public.core_jobpriority_id_seq'::regclass);


--
-- Name: core_jobstatus id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_jobstatus ALTER COLUMN id SET DEFAULT nextval('public.core_jobstatus_id_seq'::regclass);


--
-- Name: core_relationship id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_relationship ALTER COLUMN id SET DEFAULT nextval('public.core_relationship_id_seq'::regclass);


--
-- Name: core_user id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_user ALTER COLUMN id SET DEFAULT nextval('public.core_user_id_seq'::regclass);


--
-- Name: core_ward id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_ward ALTER COLUMN id SET DEFAULT nextval('public.core_ward_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add event type	1	add_eventtype
2	Can change event type	1	change_eventtype
3	Can delete event type	1	delete_eventtype
4	Can view event type	1	view_eventtype
5	Can add help type	2	add_helptype
6	Can change help type	2	change_helptype
7	Can delete help type	2	delete_helptype
8	Can view help type	2	view_helptype
9	Can add job priority	3	add_jobpriority
10	Can change job priority	3	change_jobpriority
11	Can delete job priority	3	delete_jobpriority
12	Can view job priority	3	view_jobpriority
13	Can add job status	4	add_jobstatus
14	Can change job status	4	change_jobstatus
15	Can delete job status	4	delete_jobstatus
16	Can view job status	4	view_jobstatus
17	Can add user	5	add_user
18	Can change user	5	change_user
19	Can delete user	5	delete_user
20	Can view user	5	view_user
21	Can add ward	6	add_ward
22	Can change ward	6	change_ward
23	Can delete ward	6	delete_ward
24	Can view ward	6	view_ward
25	Can add helper	7	add_helper
26	Can change helper	7	change_helper
27	Can delete helper	7	delete_helper
28	Can view helper	7	view_helper
29	Can add relationship	8	add_relationship
30	Can change relationship	8	change_relationship
31	Can delete relationship	8	delete_relationship
32	Can view relationship	8	view_relationship
33	Can add event	9	add_event
34	Can change event	9	change_event
35	Can delete event	9	delete_event
36	Can view event	9	view_event
37	Can add requester	10	add_requester
38	Can change requester	10	change_requester
39	Can delete requester	10	delete_requester
40	Can view requester	10	view_requester
41	Can add job	11	add_job
42	Can change job	11	change_job
43	Can delete job	11	delete_job
44	Can view job	11	view_job
45	Can add help preference	12	add_helppreference
46	Can change help preference	12	change_helppreference
47	Can delete help preference	12	delete_helppreference
48	Can view help preference	12	view_helppreference
49	Can add helper ward	13	add_helperward
50	Can change helper ward	13	change_helperward
51	Can delete helper ward	13	delete_helperward
52	Can view helper ward	13	view_helperward
53	Can add log entry	14	add_logentry
54	Can change log entry	14	change_logentry
55	Can delete log entry	14	delete_logentry
56	Can view log entry	14	view_logentry
57	Can add permission	15	add_permission
58	Can change permission	15	change_permission
59	Can delete permission	15	delete_permission
60	Can view permission	15	view_permission
61	Can add group	16	add_group
62	Can change group	16	change_group
63	Can delete group	16	delete_group
64	Can view group	16	view_group
65	Can add user	17	add_user
66	Can change user	17	change_user
67	Can delete user	17	delete_user
68	Can view user	17	view_user
69	Can add content type	18	add_contenttype
70	Can change content type	18	change_contenttype
71	Can delete content type	18	delete_contenttype
72	Can view content type	18	view_contenttype
73	Can add session	19	add_session
74	Can change session	19	change_session
75	Can delete session	19	delete_session
76	Can view session	19	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$180000$AtErFJmEr1w5$0ldTdxbYGZq99UzDWGim0B5za33moCyb4JfwoHB8OIY=	2020-04-26 08:39:55.397432+00	t	admin				t	t	2020-04-25 21:34:07.559013+00
5	pbkdf2_sha256$180000$q3XYaEVpoLlR$+YqezteCVZNYntT1RObrTu55TtzcCFhI5kUPQYjLdvY=	\N	f	evander.xacobe	Evander	Xacobe	e.xacobe@hotmail.com	t	t	2020-04-26 08:55:16+00
3	pbkdf2_sha256$180000$lQX0rncLRX9Q$f1ys6sYqsKO/0EuzgDYnj8p8vzceOUYyzj0QeDVovk4=	\N	f	edythe.penelope	Edythe	Penelope	edythe.penelope@kwa.co.uk	t	t	2020-04-26 08:53:59+00
4	pbkdf2_sha256$180000$k7YBzHQn0NkI$lyd1LdWqDwfM7uzW9lalSVf4CPRZSfZFhb9gdF562VE=	\N	f	lassana.jude	Lassana	Jude	lassana@kwmc.org	t	t	2020-04-26 08:54:40+00
2	pbkdf2_sha256$180000$vU1Sc7YviaDv$AYXlZMCwWUdS24ge7XtiR0G8P+C/iMJIjmPw3EvbdcU=	\N	f	lilly.luana	Lilly	Luana	lilly.l@fcc.co.uk	t	t	2020-04-26 08:53:10+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
1	5	1
2	5	2
3	5	3
4	5	4
5	5	5
6	5	6
7	5	7
8	5	8
9	5	9
10	5	10
11	5	11
12	5	12
13	5	13
14	5	14
15	5	15
16	5	16
17	5	17
18	5	18
19	5	19
20	5	20
21	5	21
22	5	22
23	5	23
24	5	24
25	5	25
26	5	26
27	5	27
28	5	28
29	5	29
30	5	30
31	5	31
32	5	32
33	5	33
34	5	34
35	5	35
36	5	36
37	5	37
38	5	38
39	5	39
40	5	40
41	5	41
42	5	42
43	5	43
44	5	44
45	5	45
46	5	46
47	5	47
48	5	48
49	5	49
50	5	50
51	5	51
52	5	52
53	5	53
54	5	54
55	5	55
56	5	56
57	5	57
58	5	58
59	5	59
60	5	60
61	5	61
62	5	62
63	5	63
64	5	64
65	5	65
66	5	66
67	5	67
68	5	68
69	5	69
70	5	70
71	5	71
72	5	72
73	5	73
74	5	74
75	5	75
76	5	76
77	3	1
78	3	2
79	3	3
80	3	4
81	3	5
82	3	6
83	3	7
84	3	8
85	3	9
86	3	10
87	3	11
88	3	12
89	3	13
90	3	14
91	3	15
92	3	16
93	3	17
94	3	18
95	3	19
96	3	20
97	3	21
98	3	22
99	3	23
100	3	24
101	3	25
102	3	26
103	3	27
104	3	28
105	3	29
106	3	30
107	3	31
108	3	32
109	3	33
110	3	34
111	3	35
112	3	36
113	3	37
114	3	38
115	3	39
116	3	40
117	3	41
118	3	42
119	3	43
120	3	44
121	3	45
122	3	46
123	3	47
124	3	48
125	3	49
126	3	50
127	3	51
128	3	52
129	3	53
130	3	54
131	3	55
132	3	56
133	3	57
134	3	58
135	3	59
136	3	60
137	3	61
138	3	62
139	3	63
140	3	64
141	3	65
142	3	66
143	3	67
144	3	68
145	3	69
146	3	70
147	3	71
148	3	72
149	3	73
150	3	74
151	3	75
152	3	76
153	4	1
154	4	2
155	4	3
156	4	4
157	4	5
158	4	6
159	4	7
160	4	8
161	4	9
162	4	10
163	4	11
164	4	12
165	4	13
166	4	14
167	4	15
168	4	16
169	4	17
170	4	18
171	4	19
172	4	20
173	4	21
174	4	22
175	4	23
176	4	24
177	4	25
178	4	26
179	4	27
180	4	28
181	4	29
182	4	30
183	4	31
184	4	32
185	4	33
186	4	34
187	4	35
188	4	36
189	4	37
190	4	38
191	4	39
192	4	40
193	4	41
194	4	42
195	4	43
196	4	44
197	4	45
198	4	46
199	4	47
200	4	48
201	4	49
202	4	50
203	4	51
204	4	52
205	4	53
206	4	54
207	4	55
208	4	56
209	4	57
210	4	58
211	4	59
212	4	60
213	4	61
214	4	62
215	4	63
216	4	64
217	4	65
218	4	66
219	4	67
220	4	68
221	4	69
222	4	70
223	4	71
224	4	72
225	4	73
226	4	74
227	4	75
228	4	76
229	2	1
230	2	2
231	2	3
232	2	4
233	2	5
234	2	6
235	2	7
236	2	8
237	2	9
238	2	10
239	2	11
240	2	12
241	2	13
242	2	14
243	2	15
244	2	16
245	2	17
246	2	18
247	2	19
248	2	20
249	2	21
250	2	22
251	2	23
252	2	24
253	2	25
254	2	26
255	2	27
256	2	28
257	2	29
258	2	30
259	2	31
260	2	32
261	2	33
262	2	34
263	2	35
264	2	36
265	2	37
266	2	38
267	2	39
268	2	40
269	2	41
270	2	42
271	2	43
272	2	44
273	2	45
274	2	46
275	2	47
276	2	48
277	2	49
278	2	50
279	2	51
280	2	52
281	2	53
282	2	54
283	2	55
284	2	56
285	2	57
286	2	58
287	2	59
288	2	60
289	2	61
290	2	62
291	2	63
292	2	64
293	2	65
294	2	66
295	2	67
296	2	68
297	2	69
298	2	70
299	2	71
300	2	72
301	2	73
302	2	74
303	2	75
304	2	76
\.


--
-- Data for Name: core_event; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_event (id, datetime, event_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: core_eventtype; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_eventtype (id, name) FROM stdin;
\.


--
-- Data for Name: core_helper; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_helper (user_ptr_id, user_type, dbs_number, access_to_car, driving_license, ts_and_cs_confirmed, health_checklist_received, key_worker, id_received, reference_details, available_mon_morning, available_mon_afternoon, available_mon_evening, available_tues_morning, available_tues_afternoon, available_tues_evening, available_wed_morning, available_wed_afternoon, available_wed_evening, available_thur_morning, available_thur_afternoon, available_thur_evening, available_fri_morning, available_fri_afternoon, available_fri_evening, available_sat_morning, available_sat_afternoon, available_sat_evening, available_sun_morning, available_sun_afternoon, available_sun_evening) FROM stdin;
5	helper	10294850	t	t	t	t	t	t	?	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t
6	helper	93840595	f	f	t	t	t	t	?	t	t	t	t	t	t	t	t	t	t	t	t	t	t	t	f	f	f	f	f	f
7	helper	03958593	t	t	t	t	t	t	?	f	f	f	f	f	f	f	f	f	f	f	f	f	f	f	t	t	t	t	t	t
8	helper	02382348	t	t	f	t	t	t	?	f	f	t	f	f	t	f	f	t	f	f	t	f	f	t	t	t	f	t	t	f
\.


--
-- Data for Name: core_helperward; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_helperward (id, ward_id, helper_id) FROM stdin;
\.


--
-- Data for Name: core_helppreference; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_helppreference (id, help_type_id, helper_id) FROM stdin;
\.


--
-- Data for Name: core_helptype; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_helptype (id, name) FROM stdin;
1	shopping
2	food_parcel
3	prescription
4	call
5	dog_walk
6	chores
\.


--
-- Data for Name: core_job; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_job (id, added_by, designated_coordinator, call_datetime, call_duration, requested_datetime, "timeTaken", notes, public_description, job_priority_id, job_status_id, helper_id, requester_id) FROM stdin;
1	edythe.penelope	edythe.penelope	2020-04-02 12:30:00+00	00:00:15	2020-05-02 09:00:00+00	00:00:30	n/a	n/a	1	1	5	1
2	Lassana Jude	Edythe Penelope	2020-04-20 09:56:41+00	00:00:05	2020-04-20 17:00:00+00	00:00:30	All went fine	Phil needs food delivered	3	4	7	4
\.


--
-- Data for Name: core_jobpriority; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_jobpriority (id, name) FROM stdin;
1	low
2	medium
3	high
\.


--
-- Data for Name: core_jobstatus; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_jobstatus (id, name) FROM stdin;
1	pending_help
2	helper_interest
3	helper_assigned
4	completed
5	couldnt_complete
\.


--
-- Data for Name: core_relationship; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_relationship (id, created_datetime, user_1_id, user_2_id) FROM stdin;
\.


--
-- Data for Name: core_requester; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_requester (user_ptr_id, user_type, address_line_1, address_line_2, address_line_3, postcode, internet_access, smart_device, confident_online_shopping, confident_online_comms, shielded, ward_id) FROM stdin;
1	requester	123 Fake Street	Hengrove	Bristol	BS1 2AB	f	f	f	f	t	6
2	requester	40 Bake Road	Knowle	Bristol	BS1 6LI	t	f	t	t	f	1
3	requester	80 Main Way	Bedminster	Bristol	BS2 8XL	f	f	f	f	t	4
4	requester	101 Diagon Alley	Totterdown	Bristol	BS3 6OU	f	t	f	f	t	5
\.


--
-- Data for Name: core_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_user (id, first_name, last_name, phone_number_primary, phone_number_secondary, email_primary, email_secondary, notes) FROM stdin;
1	František	Loke	0117499901	0117499902	františek@g.com	f.loke@g.com	n/a
2	Melisa	Callisto	0117933321	0117933322	melisa@h.com	callisto@h.com	n/a
3	Kassandra	Mario	01179144099	01179144098	kassandra@i.com	mario@i.com	n/a
4	Aemilia	Penjani	01179983049	01179983048	aemilia@b.com	penjani@b.com	n/a
5	Rama	Maria	07891573948	07891573949	rama@g.com	maria@g.com	n/a
6	Oved	Kolman	07987132453	07987132454	oved@h.com	kolman@h.com	n/a
7	Darina	Sultan	07867888777	07867888779	darina.sultan	darina.sultan	n/a
8	Blair	Haamid	07778947362	07778947363	blair.haamid	blair.haamid	n/a
\.


--
-- Data for Name: core_ward; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.core_ward (id, name) FROM stdin;
1	knowle
2	knowle_west
3	hartcliffe
4	bedminster
5	totterdown
6	hengrove
7	brislington
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2020-04-26 08:53:10.274399+00	2	lilly.luana	1	[{"added": {}}]	17	1
2	2020-04-26 08:53:59.880153+00	3	edythe.penelope	1	[{"added": {}}]	17	1
3	2020-04-26 08:54:41.005594+00	4	lassana.jude	1	[{"added": {}}]	17	1
4	2020-04-26 08:55:16.473316+00	5	evander.xacobe	1	[{"added": {}}]	17	1
5	2020-04-26 08:56:36.652589+00	5	evander.xacobe	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Staff status", "User permissions"]}}]	17	1
6	2020-04-26 08:57:54.458994+00	3	edythe.penelope	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Staff status", "User permissions"]}}]	17	1
7	2020-04-26 08:58:23.047139+00	4	lassana.jude	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Staff status", "User permissions"]}}]	17	1
8	2020-04-26 08:59:09.368151+00	2	lilly.luana	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Staff status", "User permissions"]}}]	17	1
9	2020-04-26 09:29:32.659123+00	1	Requester 1: František Loke	1	[{"added": {}}]	10	1
10	2020-04-26 09:31:30.874276+00	2	Requester 2: Melisa Callisto	1	[{"added": {}}]	10	1
11	2020-04-26 09:32:56.898774+00	3	Requester 3: Kassandra Mario	1	[{"added": {}}]	10	1
12	2020-04-26 09:34:16.939428+00	4	Requester 4: Aemilia Penjani	1	[{"added": {}}]	10	1
13	2020-04-26 09:40:41.991631+00	5	Helper 5: Rama Maria	1	[{"added": {}}]	7	1
14	2020-04-26 09:42:40.012222+00	6	Helper 6: Oved Kolman	1	[{"added": {}}]	7	1
15	2020-04-26 09:44:33.468176+00	7	Helper 7: Darina Sultan	1	[{"added": {}}]	7	1
16	2020-04-26 09:46:49.172815+00	8	Helper 8: Blair Haamid	1	[{"added": {}}]	7	1
17	2020-04-26 09:51:50.705909+00	1	Job: 1	1	[{"added": {}}]	11	1
18	2020-04-26 09:57:38.626965+00	2	Job: 2	1	[{"added": {}}]	11	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	core	eventtype
2	core	helptype
3	core	jobpriority
4	core	jobstatus
5	core	user
6	core	ward
7	core	helper
8	core	relationship
9	core	event
10	core	requester
11	core	job
12	core	helppreference
13	core	helperward
14	admin	logentry
15	auth	permission
16	auth	group
17	auth	user
18	contenttypes	contenttype
19	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-04-25 21:34:05.967131+00
2	auth	0001_initial	2020-04-25 21:34:06.015384+00
3	admin	0001_initial	2020-04-25 21:34:06.08071+00
4	admin	0002_logentry_remove_auto_add	2020-04-25 21:34:06.101325+00
5	admin	0003_logentry_add_action_flag_choices	2020-04-25 21:34:06.11652+00
6	contenttypes	0002_remove_content_type_name	2020-04-25 21:34:06.139437+00
7	auth	0002_alter_permission_name_max_length	2020-04-25 21:34:06.148292+00
8	auth	0003_alter_user_email_max_length	2020-04-25 21:34:06.160833+00
9	auth	0004_alter_user_username_opts	2020-04-25 21:34:06.174431+00
10	auth	0005_alter_user_last_login_null	2020-04-25 21:34:06.187926+00
11	auth	0006_require_contenttypes_0002	2020-04-25 21:34:06.192304+00
12	auth	0007_alter_validators_add_error_messages	2020-04-25 21:34:06.203759+00
13	auth	0008_alter_user_username_max_length	2020-04-25 21:34:06.221182+00
14	auth	0009_alter_user_last_name_max_length	2020-04-25 21:34:06.233487+00
15	auth	0010_alter_group_name_max_length	2020-04-25 21:34:06.246028+00
16	auth	0011_update_proxy_permissions	2020-04-25 21:34:06.257791+00
17	core	0001_initial	2020-04-25 21:34:06.384954+00
18	core	0002_test_data_load	2020-04-25 21:34:06.602274+00
19	sessions	0001_initial	2020-04-25 21:34:06.617859+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
22a4i0qycp7b78z0n0dxgf15c9ndg1ui	MDA2YmQxNGNjMDk2NDliZWQ2MzkzZWRmNGEwNmRiNmJiZTgyNmIwNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNTdlMjI1MzI0MzMxMWZkNTAxNmFlNGQwYWQ3OGVmMDJiNzg4MjNiIn0=	2020-05-10 08:39:55.400684+00
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 76, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 5, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 304, true);


--
-- Name: core_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_event_id_seq', 1, false);


--
-- Name: core_eventtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_eventtype_id_seq', 1, false);


--
-- Name: core_helperward_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_helperward_id_seq', 1, false);


--
-- Name: core_helppreference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_helppreference_id_seq', 1, false);


--
-- Name: core_helptype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_helptype_id_seq', 6, true);


--
-- Name: core_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_job_id_seq', 2, true);


--
-- Name: core_jobpriority_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_jobpriority_id_seq', 3, true);


--
-- Name: core_jobstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_jobstatus_id_seq', 5, true);


--
-- Name: core_relationship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_relationship_id_seq', 1, false);


--
-- Name: core_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_user_id_seq', 8, true);


--
-- Name: core_ward_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.core_ward_id_seq', 7, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 18, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 19, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: core_event core_event_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_pkey PRIMARY KEY (id);


--
-- Name: core_eventtype core_eventtype_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_eventtype
    ADD CONSTRAINT core_eventtype_pkey PRIMARY KEY (id);


--
-- Name: core_helper core_helper_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helper
    ADD CONSTRAINT core_helper_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: core_helperward core_helperward_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helperward
    ADD CONSTRAINT core_helperward_pkey PRIMARY KEY (id);


--
-- Name: core_helppreference core_helppreference_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helppreference
    ADD CONSTRAINT core_helppreference_pkey PRIMARY KEY (id);


--
-- Name: core_helptype core_helptype_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helptype
    ADD CONSTRAINT core_helptype_pkey PRIMARY KEY (id);


--
-- Name: core_job core_job_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job
    ADD CONSTRAINT core_job_pkey PRIMARY KEY (id);


--
-- Name: core_jobpriority core_jobpriority_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_jobpriority
    ADD CONSTRAINT core_jobpriority_pkey PRIMARY KEY (id);


--
-- Name: core_jobstatus core_jobstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_jobstatus
    ADD CONSTRAINT core_jobstatus_pkey PRIMARY KEY (id);


--
-- Name: core_relationship core_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_relationship
    ADD CONSTRAINT core_relationship_pkey PRIMARY KEY (id);


--
-- Name: core_requester core_requester_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_requester
    ADD CONSTRAINT core_requester_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: core_user core_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_pkey PRIMARY KEY (id);


--
-- Name: core_ward core_ward_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_ward
    ADD CONSTRAINT core_ward_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: core_event_event_type_id_737d84c2; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_event_event_type_id_737d84c2 ON public.core_event USING btree (event_type_id);


--
-- Name: core_event_user_id_b4d85d27; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_event_user_id_b4d85d27 ON public.core_event USING btree (user_id);


--
-- Name: core_helperward_helper_id_7a87497d; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_helperward_helper_id_7a87497d ON public.core_helperward USING btree (helper_id);


--
-- Name: core_helperward_ward_id_250079ed; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_helperward_ward_id_250079ed ON public.core_helperward USING btree (ward_id);


--
-- Name: core_helppreference_help_type_id_287fa89a; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_helppreference_help_type_id_287fa89a ON public.core_helppreference USING btree (help_type_id);


--
-- Name: core_helppreference_helper_id_3f12edb6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_helppreference_helper_id_3f12edb6 ON public.core_helppreference USING btree (helper_id);


--
-- Name: core_job_helper_id_6b54b909; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_job_helper_id_6b54b909 ON public.core_job USING btree (helper_id);


--
-- Name: core_job_job_priority_id_8876ebfc; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_job_job_priority_id_8876ebfc ON public.core_job USING btree (job_priority_id);


--
-- Name: core_job_job_status_id_1f54ad80; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_job_job_status_id_1f54ad80 ON public.core_job USING btree (job_status_id);


--
-- Name: core_job_requester_id_14b14619; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_job_requester_id_14b14619 ON public.core_job USING btree (requester_id);


--
-- Name: core_relationship_user_1_id_6b80be06; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_relationship_user_1_id_6b80be06 ON public.core_relationship USING btree (user_1_id);


--
-- Name: core_relationship_user_2_id_d1795d8f; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_relationship_user_2_id_d1795d8f ON public.core_relationship USING btree (user_2_id);


--
-- Name: core_requester_ward_id_bafa7298; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX core_requester_ward_id_bafa7298 ON public.core_requester USING btree (ward_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_event core_event_event_type_id_737d84c2_fk_core_eventtype_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_event_type_id_737d84c2_fk_core_eventtype_id FOREIGN KEY (event_type_id) REFERENCES public.core_eventtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_event core_event_user_id_b4d85d27_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_user_id_b4d85d27_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_helper core_helper_user_ptr_id_43457ecd_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helper
    ADD CONSTRAINT core_helper_user_ptr_id_43457ecd_fk_core_user_id FOREIGN KEY (user_ptr_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_helperward core_helperward_helper_id_7a87497d_fk_core_helper_user_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helperward
    ADD CONSTRAINT core_helperward_helper_id_7a87497d_fk_core_helper_user_ptr_id FOREIGN KEY (helper_id) REFERENCES public.core_helper(user_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_helperward core_helperward_ward_id_250079ed_fk_core_ward_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helperward
    ADD CONSTRAINT core_helperward_ward_id_250079ed_fk_core_ward_id FOREIGN KEY (ward_id) REFERENCES public.core_ward(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_helppreference core_helppreference_help_type_id_287fa89a_fk_core_helptype_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helppreference
    ADD CONSTRAINT core_helppreference_help_type_id_287fa89a_fk_core_helptype_id FOREIGN KEY (help_type_id) REFERENCES public.core_helptype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_helppreference core_helppreference_helper_id_3f12edb6_fk_core_help; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_helppreference
    ADD CONSTRAINT core_helppreference_helper_id_3f12edb6_fk_core_help FOREIGN KEY (helper_id) REFERENCES public.core_helper(user_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_job core_job_helper_id_6b54b909_fk_core_helper_user_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job
    ADD CONSTRAINT core_job_helper_id_6b54b909_fk_core_helper_user_ptr_id FOREIGN KEY (helper_id) REFERENCES public.core_helper(user_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_job core_job_job_priority_id_8876ebfc_fk_core_jobpriority_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job
    ADD CONSTRAINT core_job_job_priority_id_8876ebfc_fk_core_jobpriority_id FOREIGN KEY (job_priority_id) REFERENCES public.core_jobpriority(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_job core_job_job_status_id_1f54ad80_fk_core_jobstatus_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job
    ADD CONSTRAINT core_job_job_status_id_1f54ad80_fk_core_jobstatus_id FOREIGN KEY (job_status_id) REFERENCES public.core_jobstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_job core_job_requester_id_14b14619_fk_core_requester_user_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_job
    ADD CONSTRAINT core_job_requester_id_14b14619_fk_core_requester_user_ptr_id FOREIGN KEY (requester_id) REFERENCES public.core_requester(user_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_relationship core_relationship_user_1_id_6b80be06_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_relationship
    ADD CONSTRAINT core_relationship_user_1_id_6b80be06_fk_core_user_id FOREIGN KEY (user_1_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_relationship core_relationship_user_2_id_d1795d8f_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_relationship
    ADD CONSTRAINT core_relationship_user_2_id_d1795d8f_fk_core_user_id FOREIGN KEY (user_2_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_requester core_requester_user_ptr_id_a68e25c1_fk_core_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_requester
    ADD CONSTRAINT core_requester_user_ptr_id_a68e25c1_fk_core_user_id FOREIGN KEY (user_ptr_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_requester core_requester_ward_id_bafa7298_fk_core_ward_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.core_requester
    ADD CONSTRAINT core_requester_ward_id_bafa7298_fk_core_ward_id FOREIGN KEY (ward_id) REFERENCES public.core_ward(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

