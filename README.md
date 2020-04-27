# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front. The BECS is initialized with a basic amount of blood packs and is updated based on the usage of thesse packs. Tested on Ubuntu 20.04 machine so no known support for other systems or machines. A prerequisite is having a docker installation on the machine, if you don’t know or don’t have it you can run:

```
$ sudo apt install docker.io
```

Most of the work is done by using flask's redirecting functions, and some features were implemented according to these limitations. Further development might include migrating to an NGINX server and using flask solely as an API.

The data is stored in a local object derived from a python file. The file is initialized with some data - in a real scenario the data is non-existent. Right now the object has only the counts of each blood pack and methods for basic extraction parameters. Future work will include expansion of the data to include individual blood packs with submission dates and expiration will be taken in account. Additionaly, the data will be migrated to a remote SQL or noSQL server.

The web app works with a Docker container, also a ready-to-go version is stored in a free GCP account and any future development will be updated there.

## How to run:
```
$ docker build -t becs:latest .
$ docker run -p 5000:5000 becs:latest
```
After that, the URL for the website (and the inventory) is:
```
http://0.0.0.0:5000/
```

For the external, already running website you can visit:
```
http://34.89.179.147:5000/
```

## TODO:
- [ ] Add user log in, sign up and log out options.
- [ ] Add safe (encrypted) data transfer.
- [ ] Implement NGINX server instead of flask redirects.
- [ ] Move to external database.
- [X] Create better layout of components in pages.
- [ ] Add time stamps to blood packs.
- [ ] Add better checks and correct responses for various cases.
- [ ] Maybe switch to PHP components?
- [X] Add table page with all blood types and pack counts.
- [ ] Add action logging and suitable page.
- [X] Dockerize
- [ ] Make prints more betterer.


Current BECS version: 0.20.4.5