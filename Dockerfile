FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG 'False'
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /src;
ADD /src /src
WORKDIR /src
VOLUME /static
EXPOSE 8000
ENTRYPOINT bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn glimpseAPI.wsgi -b 0.0.0.0:8000"