-- Table: DIM_PROVIDER
CREATE TABLE DIM_PROVIDER (
    Provider_UID bigserial  NOT NULL,
    Provider_Name text  NOT NULL,
    Provider_Address text  NOT NULL,
    ZipCode text  NOT NULL,
    CONSTRAINT DIM_PROVIDER_pk PRIMARY KEY (Provider_UID)
);