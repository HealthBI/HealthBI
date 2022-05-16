# HealthBI

Requirements/Dependecies:
- Python version: TBD
- Install pandas version:
- Install postgres version: 13.4
- Install psycopg2 version:

Note: to test, create database in postgres manually before running HealthBI since there is no script to create database yet.
Setup Postgres:
1. create a database called "healthbi"
2. run sql scripts needed to create database tables

HealthBI.py is the main script.
<br>
Usage: `python HealthBI.py csv_file json_file`

Running Django app:
1. go to the ./HealthBI/Website directory
2. run `python manage.py runserver`
