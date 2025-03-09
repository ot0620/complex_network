import os

# ディレクトリの作成
directory = (f"ここに保存先とファイル名を入力。指定した文字を入力する場合は｛｝で括って表す。")
#例：(f"~/research_codes/my_code/create/module_network_data_N={n}/SF/w={w}")
os.makedirs(os.path.expanduser(directory), exist_ok=True)