FROM python:3.11

WORKDIR /app

COPY . /app

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y libpq-dev python3-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]