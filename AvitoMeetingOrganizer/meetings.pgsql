--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: meeting; Type: TABLE; Schema: public; Owner: Nikita
--

CREATE TABLE public.meeting (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL
);


ALTER TABLE public.meeting OWNER TO "Nikita";

--
-- Name: meeting_id_seq; Type: SEQUENCE; Schema: public; Owner: Nikita
--

CREATE SEQUENCE public.meeting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meeting_id_seq OWNER TO "Nikita";

--
-- Name: meeting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Nikita
--

ALTER SEQUENCE public.meeting_id_seq OWNED BY public.meeting.id;


--
-- Name: participant; Type: TABLE; Schema: public; Owner: Nikita
--

CREATE TABLE public.participant (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    surname character varying(30) NOT NULL,
    email character varying(30) NOT NULL,
    meetingid integer NOT NULL
);


ALTER TABLE public.participant OWNER TO "Nikita";

--
-- Name: participant_id_seq; Type: SEQUENCE; Schema: public; Owner: Nikita
--

CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_id_seq OWNER TO "Nikita";

--
-- Name: participant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: Nikita
--

ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;


--
-- Name: meeting id; Type: DEFAULT; Schema: public; Owner: Nikita
--

ALTER TABLE ONLY public.meeting ALTER COLUMN id SET DEFAULT nextval('public.meeting_id_seq'::regclass);


--
-- Name: participant id; Type: DEFAULT; Schema: public; Owner: Nikita
--

ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);


--
-- Data for Name: meeting; Type: TABLE DATA; Schema: public; Owner: Nikita
--

COPY public.meeting (id, name, date, "time") FROM stdin;
3	aaa	1999-02-10	10:00:00
4	bbb	1900-01-01	00:00:00
5	ccc	1950-06-15	12:00:00
\.


--
-- Data for Name: participant; Type: TABLE DATA; Schema: public; Owner: Nikita
--

COPY public.participant (id, name, surname, email, meetingid) FROM stdin;
3	Dima	Dimovich	d@d.ru	4
4	Fedor	Fedorovich	f@f.ru	3
5	Boris	Borisovich	b@b.ru	3
6	Viktor	Viktorovich	v@v.ru	4
9	Michail	Michailovich	m@m.ru	3
19	Ivan	Ivanovich	i@i.ru	3
\.


--
-- Name: meeting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Nikita
--

SELECT pg_catalog.setval('public.meeting_id_seq', 36, true);


--
-- Name: participant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: Nikita
--

SELECT pg_catalog.setval('public.participant_id_seq', 96, true);


--
-- Name: meeting meeting_pkey; Type: CONSTRAINT; Schema: public; Owner: Nikita
--

ALTER TABLE ONLY public.meeting
    ADD CONSTRAINT meeting_pkey PRIMARY KEY (id);


--
-- Name: participant participant_pkey; Type: CONSTRAINT; Schema: public; Owner: Nikita
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (id);


--
-- Name: participant participant_meetingid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: Nikita
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_meetingid_fkey FOREIGN KEY (meetingid) REFERENCES public.meeting(id);


--
-- PostgreSQL database dump complete
--

