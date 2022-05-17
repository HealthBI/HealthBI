drop table dim_location;
drop table dim_temporal;
drop table var_category;
drop table var_topic;
drop table var_indicator;

CREATE TABLE DIM_LOCATION (
    Location_UID bigserial  NOT NULL,
    Country_Name text  NOT NULL,
    Region_Name text  NOT NULL,
    Division_Name text  NOT NULL,
    State_Name text  NOT NULL,
    County_Name text  NOT NULL,
    City_Name text  NOT NULL,
    Town_Name text  NOT NULL,
    Neighborhood_Name text  NOT NULL,
    -- CONSTRAINT StateValidation CHECK (CHECK ((Country_Name is not "NA") OR (State_Name is "NA"))) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT DIM_LOCATION_pk PRIMARY KEY (Location_UID)
);

INSERT INTO dim_location (country_name, region_name, division_name, state_name, county_name, city_name, town_name, neighborhood_name) VALUES('US', 'Alabama', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');

CREATE TABLE DIM_TEMPORAL (
    Temporal_UID bigint  NOT NULL,
    Year varchar(128)  NOT NULL,
    Month_99 varchar(128)  NOT NULL,
    Month_XXX varchar(128)  NOT NULL,
    Month_Name varchar(128)  NOT NULL,
    Month_XXX_Year varchar(128)  NOT NULL,
    Day_99 varchar(128)  NOT NULL,
    Day_Month_XXX_Year varchar(128)  NOT NULL,
    DayOfWeek_XXX varchar(128)  NULL,
    Quarter_Q9 varchar(128)  NULL,
    Quarter_Q9_Year varchar(128)  NULL,
    Season varchar(128)  NULL,
    CONSTRAINT Temporal_UID PRIMARY KEY (Temporal_UID)
);
INSERT INTO dim_temporal VALUES (-1, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA');
INSERT INTO dim_temporal VALUES (12340000, '2001', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'); 
ON CONFLICT (dim_temporal) DO NOTHING;

CREATE TABLE VAR_CATEGORY (
    Category_UID bigserial  PRIMARY KEY,
    Category_Name varchar(256)  NOT NULL,
    CONSTRAINT VAR_CATEGORY_NAME_UK UNIQUE (Category_Name) NOT DEFERRABLE  INITIALLY IMMEDIATE
);

CREATE TABLE VAR_TOPIC (
    Topic_UID bigserial  PRIMARY KEY,
    Topic_Name varchar(256)  NOT NULL,
    Category_UID bigint  NOT NULL,
    CONSTRAINT VAR_TOPIC_NAME_CATEGORY_UK UNIQUE (Category_UID, Topic_Name) NOT DEFERRABLE  INITIALLY IMMEDIATE
);

CREATE TABLE VAR_INDICATOR (
    Indicator_UID bigserial      PRIMARY KEY,
    Indicator_Name varchar(256)  NOT NULL,
    Indicator_Unit varchar(256)  NULL,
    Topic_UID bigint  NOT NULL,
    CONSTRAINT VAR_INDICATOR_NAME_TOPIC_UK UNIQUE (Topic_UID, Indicator_Name) NOT DEFERRABLE  INITIALLY IMMEDIATE
);

select * from dim_location;
select * from dim_temporal;
select * from var_category;
select * from var_topic;
select * from var_indicator;