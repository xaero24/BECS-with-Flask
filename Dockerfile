FROM python:3.7-slim-buster

WORKDIR /api/

ADD . /api/

COPY . /api/

RUN pip3 install --upgrade pip

RUN pip3 install -r api/requirements.txt --ignore-installed

EXPOSE 8080

CMD [ "flask", "run", "-h", "0.0.0.0", "-p", "8080" ]
