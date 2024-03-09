FROM python:3.8-alpine
MAINTAINER Haomin Kong

LABEL AUTHOR="Haomin Kong" VERSION=3

WORKDIR /ysuauth

ENV BASE_PATH="/usr/local/shmtu/shmtu-auth"

ENV LOGS_PATH="$BASE_PATH/logs" \
    SETTINGS_PATH="$BASE_PATH/settings"

# Copy Directory
COPY shmtu_auth/* "$BASE_PATH/"

# Copy Files
COPY requirements.txt $BASE_PATH/requirements.txt

RUN echo "[global] \
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple \
    trusted-host = pypi.tuna.tsinghua.edu.cn \
    timeout = 120 \
    " > /etc/pip.conf \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache build-base libffi-dev tzdata bash curl \
    && pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U \
    && pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 --no-cache-dir install -r $BASE_PATH/requirements.txt \
    && rm -f $BASE_PATH/requirements.txt \
    && rm -rf ~/.cache/pip \
    && rm -rf /tmp/* \
    && apk del libffi-dev build-base \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Haomin Kong >> docker_status \
    && echo "Asia/Shanghai" > /etc/timezone \
    && chmod +x "$BASE_PATH/start.sh"

ENTRYPOINT ["$BASE_PATH/start.sh"]
