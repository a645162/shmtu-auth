import os

# 设置base_dir为当前py文件所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 计算输入和输出文件的绝对路径
input_qrc_path = os.path.join(base_dir, "resources.qrc")
output_py_path = os.path.join(base_dir, "../../src/shmtu_auth/src/gui/resource/resources.py")

# Convert relative paths to absolute paths
input_qrc_path = os.path.abspath(input_qrc_path)
output_py_path = os.path.abspath(output_py_path)

print(f"Input QRC Path: {input_qrc_path}")
print(f"Output PY Path: {output_py_path}")

# 确保输出目录存在
output_dir = os.path.dirname(output_py_path)
os.makedirs(output_dir, exist_ok=True)

ret = os.system(f'pyside6-rcc "{input_qrc_path}" -o "{output_py_path}"')

if ret != 0:
    print("Failed!")
    exit(1)

print("Done!")
