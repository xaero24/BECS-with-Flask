FROM python:3.7-slim-buster

COPY . /becs

WORKDIR /becs

RUN pip3 install --upgrade pip

RUN pip3 install -r api/requirements.txt --ignore-installed

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "api/requests.py", "-f" ]