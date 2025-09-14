import os

import kagglehub

# Download latest version
path = kagglehub.dataset_download("mgocen/20-newsgroups")
print("Path to dataset files:", path)

# 当前目录
workdir = os.path.dirname(os.path.abspath(__file__)) + "/"

os.system(f"mv {path} {workdir}")


