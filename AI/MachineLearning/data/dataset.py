import os

import kagglehub

# Download latest version
path = kagglehub.dataset_download("ruizema123/advertising-channel-analysis")

print("Path to dataset files:", path)

# 当前目录
workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

os.system(f"mv {path} {workdir}")


