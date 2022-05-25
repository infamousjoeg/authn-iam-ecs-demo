FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python3", "authn-iam-ecs.py"]