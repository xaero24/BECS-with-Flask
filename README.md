# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front. The BECS is initialized with a basic amount of blood packs and is updated based on the usage of thesse packs. Tested on Ubuntu 20.04 machine so no known support for other systems or machines. A prerequisite is having a docker installation on the machine, if you don’t know or don’t have it you can run:

```
$ sudo apt install docker.io
```

Most of the work is done by using flask's redirecting functions, and some features were implemented according to these limitations. Further development might include migrating to an NGINX server and using flask solely as an API.

The data is stored in a local object derived from a python file. The file is initialized with some data - in a real scenario the data is non-existent. Right now the object has only the counts of each blood pack and methods for basic extraction parameters. Future work will include expansion of the data to include individual blood packs with submission dates and expiration will be taken in account. Additionaly, the data will be migrated to a remote SQL or noSQL server.

The web app works with a Docker container, also a ready-to-go version is stored in a free GCP account and any future development will be updated there.

## UPDATES:
30/06/2020:
- Added support for multiple user privileges - admin, user, student
- Added logging functionality
- Added log file download - for now by a single date, spanned downloads will come later
- Added checks for user actions, ESPECIALLY in API endpoints
- Added admin functions - up/downgrade users, delete users, etc
- Responsiveness added to web pages and mobile display should be better
- Added integration of W3.CSS (thus the responsiveness)
- Solved a few linking and routing issues
- Added checks for log-in times and last actions, and checks for valid time since last action - more than 24 hours since last action is considered logged out


## How to run:
Since this web app is located on a remote server, you will have to manually change the IP addresses to 127.0.0.1:5000, located in the action attribute of the form tags in the following files:

api/templates/front/getblood.html
api/templates/front/sendblood.html
api/templates/front/masswithdrawal.html

Then, in the project root open the terminal and run:

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
- [X] Add user log in, sign up and log out options.
- [ ] Add safe (encrypted) data transfer.
- [ ] Implement NGINX server instead of flask redirects.
- [ ] Move to external database.
- [X] Create better layout of components in pages.
- [ ] Add time stamps to blood packs.
- [X] Add better checks and correct responses for various cases.
- [ ] Maybe switch to PHP components?
- [X] Add table page with all blood types and pack counts.
- [X] Add action logging and suitable page.
- [X] Dockerize
- [X] Make prints more betterer.
- [ ] Add log file downloads for a time span instead of a single date


Current BECS version: 0.20.6.30