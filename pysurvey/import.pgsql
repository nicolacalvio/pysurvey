--
-- PostgreSQL database dump
--

-- Dumped from database version 11.11
-- Dumped by pg_dump version 11.11

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

--
-- Data for Name: domande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.domande ("idSurvey", "idDomanda", question) FROM stdin;
1	1	Come ti chiami?
1	2	Quanti anni hai?
\.


--
-- Data for Name: risposte; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.risposte ("idRisposta", "idDomanda", risposta) FROM stdin;
1	1	Nicola
2	1	Ciccio
3	1	Lucky
4	2	12
5	2	18
6	2	23
\.


--
-- Data for Name: risposte_utenti; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.risposte_utenti ("idRisposta", "idDomanda", "idUtente", "idRispostaUtente") FROM stdin;
\.


--
-- Data for Name: survey; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.survey ("idSurvey", "idUser", titolo) FROM stdin;
1	2	La mia prima survey
2	2	La mia seconda survey
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, email, password, immagine) FROM stdin;
2	Nicola	nicolino1999@gmail.com	sha256$xYdU9RZTqlfNAjUT$d5d9d26b2ed7926ea9c1702df73f26dca1e7cecc7f0c55d451bd361fd560398a	../static/img/profile.png
\.


--
-- Name: domande_idDomanda_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."domande_idDomanda_seq"', 2, true);


--
-- Name: risposte_idRisposta_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."risposte_idRisposta_seq"', 6, true);


--
-- Name: risposte_utenti_idRispostaUtente_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."risposte_utenti_idRispostaUtente_seq"', 1, false);


--
-- Name: survey_idSurvey_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."survey_idSurvey_seq"', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

