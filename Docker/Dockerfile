FROM python:3.12-alpine

LABEL maintainer="Haomin Kong" \
      author="Haomin Kong" \
      version="3" \
      description="SHMTU Campus Network Auto Auth - Full"

ENV DOCKER_MODE="Haomin Kong" \
    BASE_PATH="/usr/local/shmtu/shmtu-auth/shmtu_auth" \
    LOGS_PATH="/usr/local/shmtu/shmtu-auth/shmtu_auth/logs"

WORKDIR "$BASE_PATH"

# Copy source code
COPY src/shmtu_auth/ "$BASE_PATH/"
COPY requirements.txt $BASE_PATH/requirements.txt

# Setup
RUN sed -i 's/\r$//' $BASE_PATH/*.sh \
    && sed -i 's/\r$//' $BASE_PATH/scripts/*.sh \
    && sed -i 's/\r$//' $BASE_PATH/config/*.sh \
    && rm -f $BASE_PATH/config.toml \
    && rm -f $BASE_PATH/config/config.toml \
    && apk add --no-cache bash tzdata \
    && pip3 --no-cache-dir install -r $BASE_PATH/requirements.txt \
    && pip3 uninstall setuptools -y \
    && pip3 uninstall pip -y \
    && rm -f $BASE_PATH/requirements.txt \
    && rm -rf ~/.cache/pip /tmp/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && mkdir -p $BASE_PATH/logs \
    && chmod +x "$BASE_PATH/start.sh"

ENTRYPOINT ["/usr/local/shmtu/shmtu-auth/shmtu_auth/start.sh"]
