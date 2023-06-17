FROM python:3.11
RUN pip install uwsgi
RUN apt-get update --fix-missing
RUN apt-get -y install  python-dev-is-python3

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /uwsgi
COPY docker/bin/* /usr/local/bin/
COPY docker/uwsgi.ini /uwsgi.ini

# Copy the rest of the application's code
COPY . /app

# Run the app
#CMD cd /app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
CMD cd / && uwsgi --ini uwsgi.ini
