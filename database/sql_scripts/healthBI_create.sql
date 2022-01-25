-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-01-25 18:01:34.355

-- tables
-- Table: City
CREATE TABLE City (
    City_ID int  NOT NULL,
    CONSTRAINT City_pk PRIMARY KEY (City_ID)
);

-- Table: Country
CREATE TABLE Country (
    Country_ID int  NOT NULL,
    CONSTRAINT Country_pk PRIMARY KEY (Country_ID)
);

-- Table: County
CREATE TABLE County (
    County_ID int  NOT NULL,
    CONSTRAINT County_pk PRIMARY KEY (County_ID)
);

-- Table: DIM_LOCATION
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
    CONSTRAINT StateValidation CHECK (CHECK ((Country_Name is not "NA") OR (State_Name is "NA"))) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT DIM_LOCATION_pk PRIMARY KEY (Location_UID)
);

-- Table: DIM_PROVIDER
CREATE TABLE DIM_PROVIDER (
    Provider_UID bigserial  NOT NULL,
    Provider_Name text  NOT NULL,
    Provider_Address text  NOT NULL,
    ZipCode text  NOT NULL,
    CONSTRAINT DIM_PROVIDER_pk PRIMARY KEY (Provider_UID)
);

-- Table: DIM_TEMPORAL
CREATE TABLE DIM_TEMPORAL (
    Temporal_UID bigint  NOT NULL,
    Year varchar(4)  NOT NULL,
    Month_99 varchar(2)  NOT NULL,
    Month_XXX varchar(3)  NOT NULL,
    Month_Name varchar(9)  NOT NULL,
    Month_XXX_Year varchar(8)  NOT NULL,
    Day_99 varchar(2)  NOT NULL,
    Day_Month_XXX_Year varchar(10)  NOT NULL,
    DayOfWeek_XXX varchar(3)  NOT NULL,
    Quarter_Q9 varchar(2)  NOT NULL,
    Quarter_Q9_Year varchar(7)  NOT NULL DEFAULT "NA",
    Season varchar(6)  NULL,
    CONSTRAINT Temporal_UID PRIMARY KEY (Temporal_UID)
);

-- Table: Division
CREATE TABLE Division (
    Division_ID int  NOT NULL,
    CONSTRAINT Division_pk PRIMARY KEY (Division_ID)
);

-- Table: FACT_INDICATOR
CREATE TABLE FACT_INDICATOR (
    Temporal_UID bigint  NOT NULL,
    Location_UID bigint  NOT NULL,
    Indicator_UID bigint  NOT NULL,
    Indicator_Value real  NOT NULL,
    Import_UID bigint  NOT NULL,
    CONSTRAINT FACT_INDICATOR_PK PRIMARY KEY (Indicator_UID,Location_UID,Temporal_UID)
);

-- Table: IMP_DATAFILE
CREATE TABLE IMP_DATAFILE (
    Import_UID bigserial  NOT NULL,
    DataFile_Name text  NOT NULL,
    Import_Timestamp timestamp  NOT NULL,
    DataSet_UID bigint  NOT NULL,
    CONSTRAINT IMP_DATAFILE_pk PRIMARY KEY (Import_UID)
);

-- Table: IMP_DATASET
CREATE TABLE IMP_DATASET (
    DataSet_UID bigserial  NOT NULL,
    DataSet_Name text  NOT NULL,
    DataSource_UID bigint  NOT NULL,
    CONSTRAINT IMP_DATASET_pk PRIMARY KEY (DataSet_UID)
);

-- Table: IMP_DATASOURCE
CREATE TABLE IMP_DATASOURCE (
    DataSource_UID bigserial  NOT NULL,
    DataSource_Name text  NOT NULL,
    CONSTRAINT IMP_DATASOURCE_pk PRIMARY KEY (DataSource_UID)
);

-- Table: Neighborhood
CREATE TABLE Neighborhood (
    Neighborhood_ID int  NOT NULL,
    CONSTRAINT Neighborhood_pk PRIMARY KEY (Neighborhood_ID)
);

-- Table: Region
CREATE TABLE Region (
    Region_ID int  NOT NULL,
    CONSTRAINT Region_pk PRIMARY KEY (Region_ID)
);

-- Table: State
CREATE TABLE State (
    State_ID int  NOT NULL,
    CONSTRAINT State_pk PRIMARY KEY (State_ID)
);

-- Table: Town
CREATE TABLE Town (
    Town_ID int  NOT NULL,
    CONSTRAINT Town_pk PRIMARY KEY (Town_ID)
);

-- Table: VAR_CATEGORY
CREATE TABLE VAR_CATEGORY (
    Category_UID bigserial  NOT NULL,
    Category_Name text  NOT NULL,
    CONSTRAINT VAR_CATEGORY_pk PRIMARY KEY (Category_UID)
);

-- Table: VAR_INDICATOR
CREATE TABLE VAR_INDICATOR (
    Indicator_UID bigserial  NOT NULL,
    Indicator_Name text  NOT NULL,
    Indicator_Unit text  NULL,
    Topic_UID bigint  NOT NULL,
    CONSTRAINT VAR_INDICATOR_pk PRIMARY KEY (Indicator_UID)
);

-- Table: VAR_TOPIC
CREATE TABLE VAR_TOPIC (
    Topic_UID bigserial  NOT NULL,
    Topic_Name text  NOT NULL,
    Category_UID bigint  NOT NULL,
    CONSTRAINT VAR_TOPIC_pk PRIMARY KEY (Topic_UID)
);

-- foreign keys
-- Reference: FACT_INDICATOR_IMP_DATAFILE (table: FACT_INDICATOR)
ALTER TABLE FACT_INDICATOR ADD CONSTRAINT FACT_INDICATOR_IMP_DATAFILE
    FOREIGN KEY (Import_UID)
    REFERENCES IMP_DATAFILE (Import_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FACT_TABLE_METRIC_DETAILS (table: FACT_INDICATOR)
ALTER TABLE FACT_INDICATOR ADD CONSTRAINT FACT_TABLE_METRIC_DETAILS
    FOREIGN KEY (Indicator_UID)
    REFERENCES VAR_INDICATOR (Indicator_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: FACT_TABLE_TEMPORAL (table: FACT_INDICATOR)
ALTER TABLE FACT_INDICATOR ADD CONSTRAINT FACT_TABLE_TEMPORAL
    FOREIGN KEY (Temporal_UID)
    REFERENCES DIM_TEMPORAL (Temporal_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: IMP_DATAFILE_IMP_DATASET (table: IMP_DATAFILE)
ALTER TABLE IMP_DATAFILE ADD CONSTRAINT IMP_DATAFILE_IMP_DATASET
    FOREIGN KEY (DataSet_UID)
    REFERENCES IMP_DATASET (DataSet_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: IMP_DATASET_IMP_DATASOURCE (table: IMP_DATASET)
ALTER TABLE IMP_DATASET ADD CONSTRAINT IMP_DATASET_IMP_DATASOURCE
    FOREIGN KEY (DataSource_UID)
    REFERENCES IMP_DATASOURCE (DataSource_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: INDICATOR_TOPIC (table: VAR_INDICATOR)
ALTER TABLE VAR_INDICATOR ADD CONSTRAINT INDICATOR_TOPIC
    FOREIGN KEY (Topic_UID)
    REFERENCES VAR_TOPIC (Topic_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: STANDARDIZED_DATA_GEO_LOCATION (table: FACT_INDICATOR)
ALTER TABLE FACT_INDICATOR ADD CONSTRAINT STANDARDIZED_DATA_GEO_LOCATION
    FOREIGN KEY (Location_UID)
    REFERENCES DIM_LOCATION (Location_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: TOPIC_CATERGORY (table: VAR_TOPIC)
ALTER TABLE VAR_TOPIC ADD CONSTRAINT TOPIC_CATERGORY
    FOREIGN KEY (Category_UID)
    REFERENCES VAR_CATEGORY (Category_UID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

