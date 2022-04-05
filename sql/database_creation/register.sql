-- Creation script for register fictional schema
CREATE EXTENSION IF NOT EXISTS postgis;

-- User groups


-- Schemas (use to seperate user group access?)

-- register schema to represent the 'property register' which has all info 
-- on properties.
CREATE SCHEMA IF NOT EXISTS register;

-- Tables
CREATE TABLE IF NOT EXISTS register.properties (
    platform_property_id SERIAL,
    address TEXT UNIQUE,
    PRIMARY KEY (platform_property_id)
);

CREATE TABLE IF NOT EXISTS register.attribute_types (
    attribute_type TEXT UNIQUE,
    description TEXT,
    data_type TEXT CHECK (data_type = 'bool' OR data_type = 'text' OR data_type = 'numeric'),
    PRIMARY KEY (attribute_type)
);

CREATE TABLE IF NOT EXISTS register.attributes (
    platform_attribute_id SERIAL,
    platform_property_id INTEGER NOT NULL,
    attribute_type TEXT NOT NULL,
    bool_value BOOLEAN,
    text_value TEXT,
    numeric_value NUMERIC,
    valid_from DATE NOT NULL,
    valid_to DATE DEFAULT '9999-01-01' CHECK (valid_to > valid_from),
    PRIMARY KEY (platform_attribute_id),
    FOREIGN KEY (platform_property_id) REFERENCES register.properties (platform_property_id),
    FOREIGN KEY (attribute_type) REFERENCES register.attribute_types (attribute_type)
);

CREATE TABLE IF NOT EXISTS register.points (
    platform_point_id SERIAL,
    uprn BIGINT,
    external_id TEXT, -- place holder for other external IDs
    platform_property_id INTEGER,
    geom GEOMETRY,
    PRIMARY KEY (platform_point_id),
    FOREIGN KEY (platform_property_id) REFERENCES register.properties (platform_property_id)
);

CREATE TABLE IF NOT EXISTS register.polygons (
    platform_polygon_id SERIAL,
    inspire_id TEXT,
    nps_id TEXT,
    external_id TEXT, -- place holder for other external IDs
    platform_property_id INTEGER,
    description TEXT,
    geom GEOMETRY,
    PRIMARY KEY (platform_polygon_id),
    FOREIGN KEY (platform_property_id) REFERENCES register.properties (platform_property_id)
);

