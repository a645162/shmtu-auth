import argparse
import os

from .config.config_toml import read_config_toml


def parse_run_args():
    parser = argparse.ArgumentParser(
        description='ShangHai Maritime University Campus Network Auto Auth Tool',
    )

    parser.add_argument(
        '-t', '--toml',
        help='Toml config path',
    )

    args = parser.parse_args()

    if hasattr(args, 'toml') and args.toml:
        print('Try to Parse TOML...')

        toml_path = args.toml

        if not os.path.exists(toml_path):
            print('Toml config not found!')
            return

        if read_config_toml(toml_path):
            print('Parse TOML Config Success!')
        else:
            print('Parse TOML Config Failed!')

