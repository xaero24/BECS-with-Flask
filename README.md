# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front. The BECS is initialized with a basic amount of blood packs and is updated based on the usage of thesse packs.

Works with a Docker container, stored in a free GCP account.

## How to run:
```
$ docker build -t becs:latest .
$ docker run becs:latest
```
After that, the URL for the website (and the inventory) is:
```
http://127.0.0.1:5000/
```

For the external, already running website you can visit:
```
http://34.89.179.147:5000/
```

## TODO:
1. [ ] Add user log in, sign up and log out options.
2. [ ] Add safe (encrypted) data transfer.
3. [ ] Implement NGINX server instead of flask redirects.
4. [X] Create better layout of components in pages.
5. [ ] Add time stamps to blood packs.
6. [ ] Add better checks and correct responses for various cases.
7. [ ] Maybe switch to PHP components?
8. [X] Add table page with all blood types and pack counts.
9. [ ] Add action logging and suitable page.
10. [X] Dockerize
11. [ ] Make prints more betterer.


Current BECS version: 0.20.4.5