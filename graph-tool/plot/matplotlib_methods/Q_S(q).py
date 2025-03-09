colors = ["red", "orange", "yellow", "green", "blue", "cyan", "purple", (0.03, 0.18, 0.42), (0.4, 0, 0.4)]
rem_nd_frac = np.linspace(0, 1, num=n)
plt.figure(figsize=(7.5, 6))
for j in range(len(w_list)):
    data = MB_avg_list[j]
    label = f"w={w_list[j]}"
    line = plt.plot(1 - rem_nd_frac, data, label=label, color=colors[j])

plt.xlabel("q", fontsize=20)
plt.ylabel(r"$S^{1st}(q)/N$", fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.ylim(0, 1)
plt.xlim(0, 1)
plt.legend(loc="upper right", fontsize=17)
plt.tight_layout()

# 保存先のディレクトリを指定
save_dir = os.path.expanduser('~/path/name')
os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成
# EPS形式で図を保存（フルパスを指定）
save_path = os.path.join(save_dir, f"file_name")
plt.savefig(save_path, format='eps', bbox_inches='tight')

plt.show()