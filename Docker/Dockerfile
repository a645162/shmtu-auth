#FROM python:3.8-alpine
FROM python:3.12-alpine
#FROM python:3.12-slim

MAINTAINER Haomin Kong

LABEL AUTHOR="Haomin Kong" VERSION=3

ENV BASE_PATH="/usr/local/shmtu/shmtu-auth"

WORKDIR "$BASE_PATH"

ENV LOGS_PATH="$BASE_PATH/logs"

# Copy Directory
COPY shmtu_auth/ "$BASE_PATH/"

# Copy Files
COPY requirements.txt $BASE_PATH/requirements.txt

RUN    sed -i 's/\r$//' $BASE_PATH/*.sh \
    && sed -i 's/\r$//' $BASE_PATH/scripts/*.sh \
    && sed -i 's/\r$//' $BASE_PATH/config/*.sh \
    && apk add --no-cache bash \
    && pip3 --no-cache-dir install -r $BASE_PATH/requirements.txt \
    && rm -f $BASE_PATH/requirements.txt \
    && rm -rf ~/.cache/pip \
    && rm -rf /tmp/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Haomin Kong >> /docker_author \
    && echo "Asia/Shanghai" > /etc/timezone \
    && mkdir $BASE_PATH/logs \
    && chmod +x "$BASE_PATH/start.sh"

ENTRYPOINT ["/usr/local/shmtu/shmtu-auth/start.sh"]

# For Debug
#ENTRYPOINT ["top"]
