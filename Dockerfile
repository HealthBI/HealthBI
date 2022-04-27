FROM python:3

WORKDIR /docker

COPY . /docker

RUN pip install django

CMD ["python3", "/docker/Website/manage.py", "runserver", "0.0.0.0:80"]
