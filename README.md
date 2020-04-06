# BECS-with-Flask
A simple BECS software with a Flask backend and HTML front.

Works with a Docker container, to be stored in a server, probably a free GCP account.

## How to run:
```
$ Docker build -t becs:latest .
$ Docker run becs
```

## Notes:
Some placehoder functions are kept in the server for future development. Now they are of no use but later will have part in the blood packs distribution.

## TODO:
01. [] Add user log in, sign up and log out options.
02. [] Add safe (encrypted) data transfer.
03. [] Implement NGINX server instead of flask redirections.
04. [] Create better layout of components in pages.
05. [] Add time stamps.
06. [] Add better checks and correct responses for various cases.
07. [] Maybe switch to PHP components?
08. [] Add table page with all blood types and pack counts.
09. [] Add action logging and suitable page.