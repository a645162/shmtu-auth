# -*- coding: utf-8 -*-

import argparse
import os

from shmtu_auth.src.config.config_toml import read_config_toml


def parse_run_args():
    parser = argparse.ArgumentParser(
        description="ShangHai Maritime University Campus Network Auto Auth Tool",
    )

    parser.add_argument(
        "-t",
        "--toml",
        help="Toml config path",
    )

    args = parser.parse_args()
    # Parse Start

    toml_path = "./config.toml"
    if not os.path.exists(toml_path):
        toml_path = "./config/config.toml"

    if hasattr(args, "toml") and args.toml:
        print("User TOML path was set.")
        toml_path = args.toml.strip()

    if os.path.exists(toml_path):
        if read_config_toml(toml_path):
            print("Parse TOML Config Success!")
        else:
            print("Parse TOML Config Failed!")
    else:
        print("Toml config not found!")

    # Parse End
