#!/bin/bash

install() {
  apt-get update && apt-get upgrade -y
  apt-get install mariadb-server -y
  apt-get install python3-pip -y

  pip3 install -r requirements.txt
}

run-dev() {
  export FLASK_APP=app
  export FLASK_ENV=develoopment
  export PYTHONPATH=./app

  flask run || python3 -m flask run
}

run-deploy() {
  export FLASK_APP=app
  export PYTHONPATH=./app

  flask run --host=0.0.0.0 || python3 -m flask run --host=0.0.0.0
}
