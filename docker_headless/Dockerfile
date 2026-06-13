# 多阶段构建 - 最终镜像更小
FROM python:3.12-alpine AS builder

WORKDIR /build

# 安装依赖到虚拟环境
COPY docker_headless/requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 最终镜像
FROM python:3.12-alpine

LABEL maintainer="Haomin Kong" \
      description="SHMTU Campus Network Auto Auth - Headless" \
      version="2.0"

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 复制虚拟环境和应用
COPY --from=builder /opt/venv /opt/venv
COPY docker_headless/app /app/app

# 安装时区数据
RUN apk add --no-cache tzdata

CMD ["python", "-m", "app.main"]
