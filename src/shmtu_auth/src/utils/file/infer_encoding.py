# -*- coding: utf-8 -*-

import chardet


def infer_encoding(file_path: str) -> str:
    # Check Encoding
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result_encoding = chardet.detect(raw_data)
        encoding = result_encoding["encoding"]

        if encoding is None:
            encoding = "utf-8"

    return encoding


def read_file_with_auto_encoding(file_path: str) -> str:
    # Check Encoding
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result_encoding = chardet.detect(raw_data)
        encoding = result_encoding["encoding"]

        if encoding is None:
            encoding = "utf-8"

        file_content = raw_data.decode(encoding).strip()

    return file_content
