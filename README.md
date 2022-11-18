# How to build and run this project

This project is a web application server with a single HTTP endpoint.\
Before proceeding, make sure Python 3.10 or above is installed on your machine.

## Install project dependencies

### Windows
```
$ py -m pip install -r requirements.txt
```

### Linux
```
$ python3 -m pip install -r requirements.txt
```

## Run the application server

From the project root directory, execute the following command:

### Windows
```
$ py -3 ./src/main.py [--port]
```

### Linux
```
$ python3 ./src/main.py [--port]
```

### CLI options
`[--port]` Local port on which the server should listen (default value is 8888).

## Execute a POST request

Provided `curl` is installed on your machine, here is an example command that can be executed:

```curl http://localhost:8888/spaceship/optimize -X POST -H "Content-Type: application/json" -d '[{"name": "Contract1", "start": 0, "duration": 5, "price": 10},{"name": "Contract2", "start": 3, "duration": 7, "price": 14},{"name": "Contract3", "start": 5, "duration": 9, "price": 8},{"name": "Contract4", "start": 5, "duration": 9, "price": 7}]'```