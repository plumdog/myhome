#!/bin/bash

GIT_COMMIT=$(git rev-parse HEAD)
git push heroku
heroku config:set GIT_COMMIT="$GIT_COMMIT"
