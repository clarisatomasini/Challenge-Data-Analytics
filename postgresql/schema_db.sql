CREATE ROLE update_etl_data WITH
	LOGIN
	NOSUPERUSER
	CREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';
	
-- Database: datos_argentina

-- DROP DATABASE IF EXISTS datos_argentina;

CREATE DATABASE datos_argentina
    WITH 
    OWNER = update_etl_data
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Argentina.1252'
    LC_CTYPE = 'Spanish_Argentina.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Table: public.data

-- DROP TABLE IF EXISTS public.data;

CREATE TABLE IF NOT EXISTS public.data
(
    index bigint,
    cod_localidad bigint,
    id_provincia bigint,
    id_departamento bigint,
    categoria text COLLATE pg_catalog."default",
    provincia text COLLATE pg_catalog."default",
    localidad text COLLATE pg_catalog."default",
    nombre text COLLATE pg_catalog."default",
    domicilio text COLLATE pg_catalog."default",
    codigo_postal text COLLATE pg_catalog."default",
    numero_telefono text COLLATE pg_catalog."default",
    mail text COLLATE pg_catalog."default",
    web text COLLATE pg_catalog."default",
    fecha_carga timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.data
    OWNER to update_etl_data;
-- Index: ix_data_index

-- DROP INDEX IF EXISTS public.ix_data_index;

CREATE INDEX IF NOT EXISTS ix_data_index
    ON public.data USING btree
    (index ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.registros

-- DROP TABLE IF EXISTS public.registros;

CREATE TABLE IF NOT EXISTS public.registros
(
    index bigint,
    provincia text COLLATE pg_catalog."default",
    categoria text COLLATE pg_catalog."default",
    fuente text COLLATE pg_catalog."default",
    cantidad bigint,
    fecha_carga timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.registros
    OWNER to update_etl_data;
-- Index: ix_registros_index

-- DROP INDEX IF EXISTS public.ix_registros_index;

CREATE INDEX IF NOT EXISTS ix_registros_index
    ON public.registros USING btree
    (index ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.info_cines

-- DROP TABLE IF EXISTS public.info_cines;

CREATE TABLE IF NOT EXISTS public.info_cines
(
    index bigint,
    provincia text COLLATE pg_catalog."default",
    pantallas double precision,
    butacas double precision,
    fecha_carga timestamp without time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.info_cines
    OWNER to update_etl_data;
-- Index: ix_info_cines_index

-- DROP INDEX IF EXISTS public.ix_info_cines_index;

CREATE INDEX IF NOT EXISTS ix_info_cines_index
    ON public.info_cines USING btree
    (index ASC NULLS LAST)
    TABLESPACE pg_default;