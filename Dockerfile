#Glimpse Wearables
#Version 1.0
FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim \ 
    python-pip \ 
    python-dev \
    virtualenv

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

RUN apt-get install -y nginx && \
    mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    mkdir -p /run/nginx

ADD nginx.conf /etc/nginx/

RUN virtualenv /venv
RUN /bin/bash -c "source /venv/bin/activate && pip install pyserial && deactivate"

# Server
EXPOSE 80
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:80"]