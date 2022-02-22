-- Table: IMP_DATAFILE
CREATE TABLE IMP_DATAFILE (
    Import_UID bigserial  NOT NULL,
    DataFile_Name varchar(256)  NOT NULL,
    Import_Timestamp timestamp  NOT NULL,
    DataSet_UID bigint  NOT NULL,
    CONSTRAINT IMP_DATAFILE_pk PRIMARY KEY (Import_UID)
);