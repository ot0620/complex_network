import matplotlib.pyplot as plt
import os

# 保存先のディレクトリを指定
save_dir = os.path.expanduser('~/path/name/directory')
os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

# EPS形式で図を保存（フルパスを指定）
save_path = os.path.join(save_dir, f"image_name.eps")
plt.savefig(save_path, format='eps', bbox_inches='tight')
