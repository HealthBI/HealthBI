-- Table: IMP_DATASOURCE
CREATE TABLE IMP_DATASOURCE (
    DataSource_UID bigserial  NOT NULL,
    DataSource_Name varchar(256)  NOT NULL,
    DataSource_Source varchar(1024)  NOT NULL,
    CONSTRAINT IMP_DATASOURCE_pk PRIMARY KEY (DataSource_UID)
);
