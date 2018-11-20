FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install -r requirements.txt

COPY . /src

EXPOSE 8080

CMD ["python", "run.py"]