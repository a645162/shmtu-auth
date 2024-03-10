#!/bin/bash

# 遍历当前目录及其子目录，删除所有的__pycache__目录
find . -type d -name "__pycache__" -exec rm -r {} +

rm -f ./shmtu_auth/logs/*

docker build \
  --progress=plain \
  -f Docker/Dockerfile \
  -t a645162/shmtu_auth:latest \
  -t registry.cn-hangzhou.aliyuncs.com/a645162/shmtu_auth:latest \
  .
