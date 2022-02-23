-- Table: VAR_INDICATOR
CREATE TABLE VAR_INDICATOR (
    Indicator_UID bigserial      PRIMARY KEY,
    Indicator_Name varchar(256)  NOT NULL,
    Indicator_Unit varchar(256)  NULL,
    Topic_UID bigint  NOT NULL,
    CONSTRAINT VAR_INDICATOR_NAME_TOPIC_UK UNIQUE (Topic_UID, Indicator_Name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
);