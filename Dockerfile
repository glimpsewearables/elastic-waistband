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
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
ADD . /code/

RUN apt-get install -y nginx && \
    mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    mkdir -p /run/nginx

RUN python manage.py collectstatic --no-input

ADD nginx.conf /etc/nginx/
RUN nginx -t

# Server
EXPOSE 80
STOPSIGNAL SIGINT
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "glimpseAPI.wsgi:application"]