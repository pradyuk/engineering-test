CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

DROP TABLE IF EXISTS properties;
CREATE TABLE IF NOT EXISTS properties(
     id varchar(100) NOT NULL,
     geocode_geo geography NULL,
     parcel_geo geography NULL,
     building_geo geography NULL,
     image_bounds float8[] NULL,
     image_url text NULL,
     CONSTRAINT properties_pk PRIMARY KEY (id)
);
DROP TABLE IF EXISTS pointstable;
CREATE TABLE IF NOT EXISTS pointstable(
    idl geography NULL,
    longi float8 NOT NULL,
    lat float8 NOT NULL,
    CONSTRAINT pointstable_pk PRIMARY KEY (idl)
);
