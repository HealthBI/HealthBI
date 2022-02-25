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
