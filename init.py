import os
import glob
import json

# 获取当前路径
current_directory = os.getcwd()
excluded_directory = "tools"

# 使用 glob 模块获取所有 .h 文件的路径
h_files = glob.glob(os.path.join(current_directory, '**/*.h'), recursive=True)

# 提取包含 .h 文件的文件夹路径，并排除指定的文件夹
excluded_folder = os.path.join(current_directory, excluded_directory)
h_folders = set(os.path.dirname(h_file) for h_file in h_files if not h_file.startswith(excluded_folder))

# 将路径转换为相对路径并去除当前目录部分
relative_folders = [f'"{folder.split(current_directory)[1].lstrip(os.sep)}"' for folder in h_folders]

# 在除了最后一个目录的所有目录的末尾添加逗号
formatted_folders = [folder + "," for folder in relative_folders[:-1]] + [relative_folders[-1]]

# 读取或创建 .vscode/c_cpp_properties.json 文件
vscode_config_path = os.path.join(current_directory, ".vscode", "c_cpp_properties.json")
if os.path.exists(vscode_config_path):
    with open(vscode_config_path, "r") as f:
        config = json.load(f)
else:
    config = {
        "configurations": [
            {
                "name": "Linux",
                "includePath": [],
                "defines": [],
                "compilerPath": "",
                "cStandard": "c99",
                "cppStandard": "c++17",
                "intelliSenseMode": "linux-gcc-arm4"
            }
        ],
        "version": 4
    }

# 将路径添加到 includePath 中
include_path = config["configurations"][0]["includePath"]
for folder in relative_folders:
    # 去掉双引号，保留相对路径
    clean_folder = folder.strip('"')
    # 添加到 includePath 中（避免重复添加）
    if clean_folder not in include_path:
        include_path.append(clean_folder)

# 将更新后的配置写回文件
if not os.path.exists(os.path.dirname(vscode_config_path)):
    os.makedirs(os.path.dirname(vscode_config_path))

with open(vscode_config_path, "w") as f:
    json.dump(config, f, indent=4)
