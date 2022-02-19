FROM python:3.10-slim@sha256:42d13fdfccf5d97bd23f9c054f22bde0451a3da0a7bb518bcd95fec6be89b50d

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -U pip && pip install -r /code/requirements.txt

COPY . /code

CMD ["/code/docker-entrypoint.sh", "-n"]