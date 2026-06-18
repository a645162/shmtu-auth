# 构建与打包

## PyInstaller 打包

### Windows Console 版本

```powershell
# 使用 PyInstaller
pyinstaller --onefile --console src/shmtu_auth/main_start.py

# 或使用项目脚本
.\Build\windows_generate_exe_console.ps1
```

### Windows GUI 版本

```powershell
# 使用 Nuitka（推荐）
.\Build\windows_generate_exe_gui_nuitka.ps1

# 或使用 PyInstaller
.\Build\windows_generate_exe_gui.ps1
```

### macOS

```bash
# 生成 .app 包
./Build/macos_generate_gui_app_bundle.sh

# 生成 .dmg 安装包
./Build/macos_generate_gui_dmg.sh
```

## Docker 构建

### Headless 版本

```bash
cd docker_headless
docker build -f Dockerfile -t shmtu-auth-headless:local ..
```

### 完整版本

```bash
cd Docker
docker build -f Dockerfile -t shmtu-auth:local ..
```

## PyPI 发布

```bash
# 构建分发包
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

## 版本管理

版本号定义在 `src/shmtu_auth/version.py` 中，通过 `pyproject.toml` 的动态版本机制引用：

```toml
[tool.setuptools.dynamic]
version = {attr = "shmtu_auth.__version__"}
```

## CI/CD

项目配置了多个 GitHub Actions 工作流：

| 工作流 | 触发 | 功能 |
|--------|------|------|
| `docker-image-main-latest.yaml` | push main | 构建 Docker 镜像 |
| `docker-image-tag.yaml` | tag push | 构建指定版本镜像 |
| `python-publish-pypi.yaml` | release | 发布到 PyPI |
| `pyinstaller-windows-*.yaml` | 手动/推送 | Windows 打包 |
| `auto-tag.yaml` | 手动 | 自动打标签 |
