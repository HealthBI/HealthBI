-- Table: IMP_DATASET
CREATE TABLE IMP_DATASET (
    DataSet_UID bigserial  NOT NULL,
    DataSet_Name varchar(256)  NOT NULL,
    DataSource_UID bigint  NOT NULL,
    CONSTRAINT IMP_DATASET_pk PRIMARY KEY (DataSet_UID)
);