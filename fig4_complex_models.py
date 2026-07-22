# -*- coding: utf-8 -*-
"""
图4: 用于鲁棒性测试的复杂几何模型
(a) 非均匀密度模型  (b) 不连通体模型  (c) 带回字形空洞模型
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei'],
    'font.family': 'sans-serif',
    'font.serif': [],
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

fig, axes = plt.subplots(1, 3, figsize=(6.3, 3.0), facecolor='white', dpi=300)
(ax1, ax2, ax3) = axes

np.random.seed(1)

# ── (a) 非均匀密度模型：中心密、边缘疏 ──
ax1.set_title('(a) 非均匀密度模型', fontsize=12, pad=6)
n = 500
r = np.random.rand(n) * 700
theta = np.random.rand(n) * 2 * np.pi
# 密度从中心向外递减
keep = np.random.rand(n) < np.exp(-r / 300)
xa = r[keep] * np.cos(theta[keep])
ya = r[keep] * np.sin(theta[keep])
ax1.plot(xa, ya, '.', markersize=2.5, color='#333333')
ax1.set_xlabel('X (m)', fontsize=11)

# ── (b) 不连通体模型：两个分离的团簇 ──
ax2.set_title('(b) 不连通体模型', fontsize=12, pad=6)
n2 = 300
# 左团
xl = np.random.randn(n2) * 80 - 300
yl = np.random.randn(n2) * 80
# 右团
xr = np.random.randn(n2) * 80 + 300
yr = np.random.randn(n2) * 80
ax2.plot(xl, yl, '.', markersize=2.5, color='#333333')
ax2.plot(xr, yr, '.', markersize=2.5, color='#333333')
ax2.set_xlabel('X (m)', fontsize=11)

# ── (c) 回字形空洞模型：方框状，内部掏空 ──
ax3.set_title('(c) 回字形空洞模型', fontsize=12, pad=6)
outer_w, inner_w = 600, 300
n3 = 800
# 外框
xo = (np.random.rand(n3) - 0.5) * outer_w
yo = (np.random.rand(n3) - 0.5) * outer_w
# 剔除内部方块
mask = ~((np.abs(xo) < inner_w/2) & (np.abs(yo) < inner_w/2))
ax3.plot(xo[mask], yo[mask], '.', markersize=2.5, color='#333333')
ax3.set_xlabel('X (m)', fontsize=11)

# 统一格式化
for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', direction='in', labelsize=10, width=0.8, length=4)
    ax.grid(False)
    ax.set_aspect('equal', 'box')
    ax.set_ylabel('Y (m)', fontsize=11)

ax2.set_yticklabels([])
ax3.set_yticklabels([])

fig.suptitle('图4  复杂几何模型（鲁棒性测试）', fontsize=12, fontweight='bold', y=1.01)
plt.tight_layout(pad=1.0)
plt.subplots_adjust(top=0.85, wspace=0.2)

fig.savefig('Fig4.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('Fig4.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig4 saved.")
plt.close()
