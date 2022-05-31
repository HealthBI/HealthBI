# HealthBI

# Description
HealthBI is a data analytics tool that allows a health researcher to load data into a database, query the data, and find correlations amongst the data with respect to temporal and location parameters.

# Installation
Requirements/Dependecies:
- Python version: TBD
- Install pandas version: 1.4.2
- Install postgres version: 13.4
- Install psycopg2 version: 2.9.3

Note: to test, create database in postgres manually before running HealthBI since there is no script to create database yet.
Setup Postgres:
1. create a database called "healthbi"
2. run sql scripts needed to create database tables (NOTE: add test first row into each table)

Sample Workflow (may need to change depending on your environment):
1. pip install postrgres
2. psql -U postgres (launches postgres as user 'postgres')
3. CREATE DATABASE healthbi; (SQL command which creates database 'healthbi')
4. \c healthbi; (connects to database 'healthbi')
5. \i healthbi.sql (to load tables)

Running Django app:
1. go to the ./HealthBI/Website directory
2. run `python manage.py runserver

# Usage
There are four main endpoints for our API. Upload, View, Correlate, and Select.

**Upload** allows a user to upload a .csv file into the database
Usage: `python ./api/HealthBI.py upload csv_file json_file`
 
*Use case* (from root directory):
python ./api/HealthBI.py upload ./sampleData/Demographics.csv ./database/dictionary/demographic_mapping.json

**View** allows the user to view all datasets currently loaded into the database
Usage: `python. ./api/HealthBI.py view`

**Correlate** allows the user to find the correlation value of two indicators with respect to a temporal and a location parameter
Usage: `python ./api/HealthBI.py correlate temporal location indicator indicator indicator`

*Use case* (from root directory):
python ./api/HealthBI.py

**Select** allows the user to find 
Usage: 'python ./api/HealthBI.py select

# Contributors
Corinna Hoang
Trang Hoang
Chris Lynch
Charles Porter
Devang Rungta
Angie Marg





