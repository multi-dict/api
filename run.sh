#!/bin/bash

NAME=api

docker rm -f "$NAME" > /dev/null 2>&1

docker build -t "multidict/$NAME" .
docker run -it --rm \
           -p 8000:8000 \
           -e PORT=8000 \
           -e ROLE='busymoms' \
           -v "$(pwd)/src":/src \
           --name "$NAME" \
           "multidict/$NAME"
