#!/bin/bash

PROJECT="forestmonitor"

REPOSITORY="forest-monitor-backend"

VERSION=$(grep version setup.py | head -1 | sed 's/.*"\(.*\)".*/\1/')

docker build -t $PROJECT/$REPOSITORY:v$VERSION -f Dockerfile .

docker push $PROJECT/$REPOSITORY:v$VERSION
