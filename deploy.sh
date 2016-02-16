#!/bin/bash

function error {
    echo "Error: $1"
    exit 1
}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR"

rm -rf _html
python main.py || error "Unable to build html pages"

cp CNAME _html/

cd _html || error "Unable to move int html directyr"

git init
git add .

git commit -m "Deploy"
git remote add origin git@github.com:plumdog/plumdog.github.io.git
git push -u origin master -f
