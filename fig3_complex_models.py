# -*- coding: utf-8 -*-
"""
图3: 复杂几何模型 — (a)非均匀密度 (b)不连通体 (c)回字形空洞
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans'],
    'font.family': 'sans-serif',
    'font.serif': [],
    'font.size': 12,
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

fig, axes = plt.subplots(1, 3, figsize=(6.3, 2.8), facecolor='white', dpi=300)
np.random.seed(42)

# ── (a) 非均匀密度：中心密集方块 + 外围稀疏点 ──
ax = axes[0]
ax.set_title('(a)', fontsize=14, loc='left', pad=4)
# 密实方块
nx, ny = 16, 16
sp = 120
x0, y0 = 1500, 1200
for i in range(nx):
    for j in range(ny):
        ax.plot(x0+i*sp, y0+j*sp, '.', markersize=8, color='#666666')
# 外围随机稀疏点
n_sparse = 300
xs = np.random.rand(n_sparse) * 4200
ys = np.random.rand(n_sparse) * 3200
# 剔除落在方块内的
mask = ~((xs >= x0) & (xs <= x0+nx*sp) & (ys >= y0) & (ys <= y0+ny*sp))
ax.plot(xs[mask], ys[mask], 'o', markersize=8, color='#999999', fillstyle='none')
ax.set_xlim(0, 4500); ax.set_ylim(0, 3500)
ax.set_ylabel('Y (m)', fontsize=12)

# ── (b) 不连通体：两个分离方块 ──
ax = axes[1]
ax.set_title('(b)', fontsize=14, loc='left', pad=4)
sp2 = 80
for i in range(12):
    for j in range(12):
        ax.plot(600+i*sp2, 600+j*sp2, '.', markersize=8, color='#666666')
        ax.plot(2600+i*sp2, 2600+j*sp2, '.', markersize=8, color='#666666')
ax.set_xlim(0, 4500); ax.set_ylim(0, 3500)

# ── (c) 回字形空洞 ──
ax = axes[2]
ax.set_title('(c)', fontsize=14, loc='left', pad=4)
sp3 = 60
outer, inner = 4000, 2000
ox, oy = 400, 400
for i in range(int(outer/sp3)):
    for j in range(int(outer/sp3)):
        xc = ox + i*sp3
        yc = oy + j*sp3
        cx, cy = outer/2+ox, outer/2+oy
        if not ((cx-inner/2 < xc < cx+inner/2) and (cy-inner/2 < yc < cy+inner/2)):
            ax.plot(xc, yc, '.', markersize=8, color='#666666')
ax.set_xlim(0, 4800); ax.set_ylim(0, 4800)

# 统一样式
for ax in axes:
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.4, color='#cccccc')
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.tick_params(labelsize=11)
for ax in axes[1:]:
    ax.set_yticklabels([])

plt.tight_layout(pad=0.8)
plt.subplots_adjust(wspace=0.3)
fig.text(0.5, 0.015, 'X (m)', ha='center', fontsize=12)

fig.savefig('./figures/Fig3.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig3.png', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig3.svg', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig3 saved.")
plt.close()
