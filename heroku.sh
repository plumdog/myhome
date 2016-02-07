#!/bin/bash

function error {
    echo "Error: $1"
    exit 1
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR"

message="$(git log -1 --pretty=%B)"
message="$(echo -e $message)"

rm -rf _html
python main.py || error "Unable to build html pages"

cd _html || error "Unable to move int html directyr"

touch composer.json
touch index.php

mv index.html home.html

echo '<?php include_once("home.html"); ?>' > index.php
echo '{}' > composer.json

git init
git add .

git commit -m "$message" # todo - lift the commit message from the real git repo
heroku git:remote -a desolate-springs-9039
git push heroku master -f
