#!/bin/bash
# SHMTU Auth Headless - Docker 管理脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_usage() {
    echo "用法: $0 <命令>"
    echo ""
    echo "命令:"
    echo "  start     启动服务"
    echo "  stop      停止服务"
    echo "  restart   重启服务"
    echo "  status    查看状态"
    echo "  logs      查看日志"
    echo "  build     构建镜像"
    echo "  help      显示帮助"
}

cmd_start() {
    log_info "启动 shmtu-auth-headless..."
    docker compose -f "$COMPOSE_FILE" up -d
    log_info "服务已启动"
    cmd_status
}

cmd_stop() {
    log_info "停止 shmtu-auth-headless..."
    docker compose -f "$COMPOSE_FILE" down
    log_info "服务已停止"
}

cmd_restart() {
    log_info "重启 shmtu-auth-headless..."
    docker compose -f "$COMPOSE_FILE" restart
    log_info "服务已重启"
}

cmd_status() {
    docker compose -f "$COMPOSE_FILE" ps
}

cmd_logs() {
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100
}

cmd_build() {
    log_info "构建镜像..."
    docker compose -f "$COMPOSE_FILE" build --no-cache
    log_info "构建完成"
}

# 主逻辑
case "${1:-}" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    restart) cmd_restart ;;
    status)  cmd_status ;;
    logs)    cmd_logs ;;
    build)   cmd_build ;;
    help|--help|-h) show_usage ;;
    *)
        log_error "未知命令: ${1:-}"
        show_usage
        exit 1
        ;;
esac
