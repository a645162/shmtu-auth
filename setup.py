# read the contents of your README file
from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("version.txt", "r", encoding="utf-8") as f:
    __version__ = f.read().strip()

if __version__.strip() == "":
    print("version.txt is empty")
    exit(1)

setup(
    name="shmtu-auth",
    version=__version__,
    description="上海海事大学校园网自动认证工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a645162/shmtu-auth",
    author="Haomin Kong",
    author_email="a645162@gmail.com",
    license="GPLv3",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=[
        "requests",
        "chardet", "PyYaml", "toml",
        "loguru"
    ],
    entry_points={
        "console_scripts": [
            "shmtu-auth = shmtu_auth.main_start:main",
        ],
    },
)
