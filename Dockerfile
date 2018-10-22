FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /src;
ADD /src /src
WORKDIR /src
ENTRYPOINT bash -c "python manage.py makemigrations && python manage.py migrate && gunicorn glimpseAPI.wsgi -b 0.0.0.0:8000"