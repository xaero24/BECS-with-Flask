# BECS-with-Flask
A simple BECS (Blood Establishment Computer Software) with a Flask backend and HTML front.

Works with a Docker container, to be stored in a server, probably a free GCP account.

## How to run:
```
$ Docker build -t becs:latest .
$ Docker run becs
```
After that, the URL for the blood pack submission is:
```
http://0.0.0.0:5000/sendblood.html
```

## Notes:
Some placehoder functions are kept in the server for future development. Now they are of no use but later will have part in the blood packs distribution.

## TODO:
1. [ ] Add user log in, sign up and log out options.
2. [ ] Add safe (encrypted) data transfer.
3. [ ] Implement NGINX server instead of flask redirections.
4. [ ] Create better layout of components in pages.
5. [ ] Add time stamps.
6. [ ] Add better checks and correct responses for various cases.
7. [ ] Maybe switch to PHP components?
8. [ ] Add table page with all blood types and pack counts.
9. [ ] Add action logging and suitable page.
