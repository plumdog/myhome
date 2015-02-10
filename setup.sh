#!/bin/bash

virtualenv --python=python3.4 .
./bin/pip install -r requirements.txt
chmod a+w myhome/db.sqlite3
chmod a+w myhome/
