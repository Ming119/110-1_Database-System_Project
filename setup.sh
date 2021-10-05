apt-get update && apt-get upgrade -y
apt-get install mariadb-server -y
apt-get install python3-pip -y

pip3 install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=develoopment

flask init-db || python3 -m flask init-db
flask run || python3 -m flask run
