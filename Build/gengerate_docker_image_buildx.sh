#!/bin/bash

# 遍历当前目录及其子目录，删除所有的__pycache__目录
find . -type d -name "__pycache__" -exec rm -r {} +

rm -f ./shmtu_auth/logs/*

docker buildx install

docker buildx build \
  --progress=plain --no-cache \
  --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
  -f Docker/Dockerfile \
  -t a645162/shmtu_auth:latest \
  .
