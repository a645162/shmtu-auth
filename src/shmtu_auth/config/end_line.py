# -*- coding: utf-8 -*-


def convert_to_crlf(file_path):
    # 读取文件
    with open(file_path, "r", newline="") as file:
        lines = file.readlines()

    # 检查每一行的行尾
    lf_detected = any(line.endswith("\n") for line in lines)

    # 如果至少有一行的行尾为LF，则修改为CRLF
    if lf_detected:
        with open(file_path, "w", newline="") as file:
            for line in lines:
                file.write(line.rstrip("\r\n") + "\r\n")


def convert_to_lf(file_path):
    # 读取文件
    with open(file_path, "r", newline="") as file:
        lines = file.readlines()

    # 检查每一行的行尾
    crlf_detected = any(line.endswith("\r\n") for line in lines)

    # 如果至少有一行的行尾为CRLF，则修改为LF
    if crlf_detected:
        with open(file_path, "w", newline="") as file:
            for line in lines:
                file.write(line.rstrip("\r\n") + "\n")
