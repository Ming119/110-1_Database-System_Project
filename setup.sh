#!/bin/bash

function setup_db() {

}

function install() {
  apt-get update && apt-get upgrade -y
  apt-get install mariadb-server -y
  apt-get install python3-pip -y

  pip3 install -r requirements.txt

  setup_db
}

function active() {
  . ./venv/bin/activate
  export FLASK_APP=app
  export PYTHONPATH=./app
}

function run_dev() {
  export FLASK_ENV=develoopment

  flask run || python3 -m flask run
}

function run_deploy() {
  flask run --host=0.0.0.0 || python3 -m flask run --host=0.0.0.0
}

$1
