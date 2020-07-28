# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front. The BECS may be initialized with a basic amount of blood packs and is updated based on the usage of these packs. Tested on Ubuntu 20.04 machine so no known support for other systems or machines. A prerequisite is having a docker installation on the machine, if you don’t know or don’t have it you can run:

```
$ sudo apt install docker.io
```

Most of the work is done by using flask's redirecting functions, and some features were implemented according to these limitations. Further development might include migrating to an NGINX server and using flask solely as an API.

The data is stored locally, and the blood bank is a (custom) BECS class. The database may be initialized with some data - in a real scenario the data is non-existent. The option is controlled via a custom run with a -f flag, i.e. addition of the parameter to the Dockerfile is needed. To do this, change the following line in the Dockerfile:
```
CMD [ "api/requests.py" ]
```
to:
```
CMD [ "api/requests.py", "-f" ]
```

The web app works with a Docker container, also a ready-to-go version is stored in a free GCP account and any future development will be updated there.

NOTE: Right now the remote server is down until further notice.

## UPDATES:
28/07/2020:
- Divided blood packs to cooled and frozen, with counts of each in a separate file. Local JSON database is used.
- Added option to pull prioritized packs. Normal will pull frozen packs, emergency will pull cooled packs.
- Added timed job to check for old packs in the coolers and move them to the freezers.
- Newly added packs are now added into the coolers.
- MCI events will pull packs in an emergency priority.
- Updated the blood bank class to use the files and to handle prioritized pull/push.
- Implemented MD5 encryption for passwords (any other encryption is possible in the future, now it's a PoC).
- Added an option to populate the database with mock data on the first run or to place zeros and no packs.
- Changed the logging format to a more convenient one.
- Existing log files are now listed in the log export page.
- General code cleanup and other various minor updates.


## How to run:
Since this web app is located on a remote server, you may have to manually change the IP addresses to localhost:5000, located in the action attribute of the form tags in the following files (if the addresses are not already changed to localhost):

api/templates/front/getblood.html
api/templates/front/index.html
api/templates/front/logexport.html
api/templates/front/masswithdrawal.html
api/templates/front/sendblood.html
api/templates/front/signup.html
api/templates/front/user.html (in all the forms)

Then, in the project root open the terminal and run:

```
$ docker build -t becs:latest .
$ docker run -p 5000:5000 becs:latest
```
After that, the URL for the website login page is:
```
http://0.0.0.0:5000/
```

For the external, already running website you can visit:
```
http://34.89.179.147:5000/
```
The remote server address may change in the future, as noted above.

## TODO:
- [X] Add user log in, sign up and log out options.
- [X] Add safe (encrypted) data transfer.
- [ ] Move to external database.
- [X] Create better layout of components in pages.
- [X] Add time stamps to blood packs.
- [X] Add better checks and correct responses for various cases.
- [X] Add table page with all blood types and pack counts.
- [X] Add action logging and suitable page.
- [X] Dockerize
- [X] Make prints more betterer.
- [ ] Add log file downloads for a time span instead of a single date.


Current BECS version: 1.20.7.28