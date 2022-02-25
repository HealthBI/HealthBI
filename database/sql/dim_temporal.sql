-- Table: DIM_TEMPORAL
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
INSERT INTO dim_temporal VALUES (2000, '2000', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA') 
ON CONFLICT (dim_temporal) DO NOTHING;