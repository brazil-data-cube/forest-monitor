#!/bin/bash

##### DEPLOY

echo
echo "BUILD STARTED"
echo

echo
echo "NEW TAG - API FOREST MONITOR:"
read API_FM_TAG

IMAGE_API_FM="registry.dpi.inpe.br/brazildatacube/forest-monitor"

IMAGE_API_FM_FULL="${IMAGE_API_FM}:${API_FM_TAG}"

docker build -t ${IMAGE_API_FM_FULL} -f docker/Dockerfile .

docker push ${IMAGE_API_FM_FULL}