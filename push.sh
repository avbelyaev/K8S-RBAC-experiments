#!/bin/bash

IMAGE_TAG=docker.pkg.github.com/avbelyaev/k8s-rbac-experiments/flask-sample
# FIXME update version
IMAGE_VERSION=3

echo "Building image"
docker build --tag ${IMAGE_TAG}:${IMAGE_VERSION} .

echo "Pushing image"
docker push ${IMAGE_TAG}:${IMAGE_VERSION}

echo "Image has been pushed"
