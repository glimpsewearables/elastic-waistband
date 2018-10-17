#Glimpse Wearables
#Version 1.0
FROM python:3.5

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
    python-dev
    
RUN pyvenv /venv

ADD nginx.conf /etc/nginx/

# Server
EXPOSE 80
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:80"]