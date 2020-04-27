FROM python:3.7-slim-buster

COPY . /api

WORKDIR /api

RUN pip3 install --upgrade pip

RUN pip3 install -r api/requirements.txt --ignore-installed

ENTRYPOINT [ "python3" ]

CMD [ "api/requests.py" ]