# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front. Righ now the software is running on a ocal machine and can be a bit buggy. No dockers are imlemented due to shortage of time and various errors.

Additionally, the BECS is initialized with a basic amount of blood packs and is updated based on the usage of thesse packs.

Will work in the future with a Docker container, to be stored in a server, probably a free GCP account.

## How to run:
```
$ ./run_becs.sh
```
After that, the URL for the blood pack submission is:
```
http://127.0.0.1:5000/sendblood.html
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
10. [ ] Dockerize
11. [ ] Make prints more betterer.


Current BECS version: 0.20.4