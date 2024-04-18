# read the contents of your README file
from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

__version__ = "1.1.0"

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
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "chardet", "PyYaml", "toml",
        "loguru"
    ],
    entry_points={
        "console_scripts": [
            "shmtu-auth = shmtu_auth.__main__:main",
        ],
    },
)
