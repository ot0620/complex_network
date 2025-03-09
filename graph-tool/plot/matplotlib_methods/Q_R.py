colors = ["red", "orange", "yellow", "green", "blue", "cyan", "purple", (0.03, 0.18, 0.42), (0.4, 0, 0.4)]

plt.figure(figsize=(8, 6))
for i, (q, r) in enumerate(zip(Q_all_list, R_all_list)):
    color = colors[i % len(colors)]
    label = f"{name_list[i]}"
    plt.plot(q, r, 'o-', color=color, label=label)

plt.xlabel("Q", fontsize=20)
plt.ylabel(r"$R^{IB}$", fontsize=20)
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.75))

# x軸の範囲と目盛りを設定
plt.xlim(0, 1)
plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=20)

# y軸の範囲を設定
max_y_value = max(max(m) for m in R_all_list)  # L_net_listの最大値を取得
plt.ylim(0, max_y_value + 0.1 * max_y_value)  # 最大値に少し余裕を持たせる
# y軸の目盛りのフォントサイズを設定
plt.yticks(fontsize=20)

plt.grid(False)
plt.tight_layout()
plt.show()