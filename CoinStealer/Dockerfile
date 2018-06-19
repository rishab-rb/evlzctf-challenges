
FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-venv python3-dev gunicorn

# Setup django application
RUN mkdir -p /deploy/app
COPY app /deploy/app
RUN pip3 install -r /deploy/app/requirements.txt
WORKDIR /deploy/app

EXPOSE 1338

# Start gunicorn
CMD ["gunicorn","-w", "4", "-b", "0.0.0.0:1338", "application:app"]
