import os

file_path = f"before/path/name"

new_file_path = f"after/path/name"

# ファイル名を変更
os.rename(file_path, new_file_path)