#!/bin/bash

message="$(git log -1 --pretty=%B)"
message="$(echo -e $message)"

rm -rf _html

python main.py

cd _html

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
