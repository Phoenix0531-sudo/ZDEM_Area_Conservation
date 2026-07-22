# -*- coding: utf-8 -*-
"""
图6: 复杂几何模型三角剖分结果
上排(a-c): 三角剖分/连通性
下排(d-f): 原始点集
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans'],
    'font.family': 'sans-serif',
    'font.serif': [],
    'font.size': 12,
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

fig, axes = plt.subplots(2, 3, figsize=(6.3, 5.0), facecolor='white', dpi=300)
np.random.seed(42)

# ── 生成三种模型点集 ──
# 模型1: 非均匀密度 (密实方块 + 稀疏外围)
nx1, ny1, sp1 = 16, 16, 120
x0, y0 = 1500, 1200
pts_dense = []
for i in range(nx1):
    for j in range(ny1):
        pts_dense.append([x0+i*sp1, y0+j*sp1])
pts_dense = np.array(pts_dense)

n_sparse = 300
xs = np.random.rand(n_sparse)*4200
ys = np.random.rand(n_sparse)*3200
mask = ~((xs>=x0)&(xs<=x0+nx1*sp1)&(ys>=y0)&(ys<=y0+ny1*sp1))
pts_sparse = np.column_stack([xs[mask], ys[mask]])
pts_nud = np.vstack([pts_dense, pts_sparse])  # non-uniform density

# 模型2: 不连通体
pts_disc = []
sp2 = 80
for i in range(12):
    for j in range(12):
        pts_disc.append([600+i*sp2, 600+j*sp2])
        pts_disc.append([2600+i*sp2, 2600+j*sp2])
pts_disc = np.array(pts_disc)

# 模型3: 回字形
pts_ring = []
sp3 = 60
outer, inner = 4000, 2000
ox, oy = 400, 400
for i in range(int(outer/sp3)):
    for j in range(int(outer/sp3)):
        xc = ox + i*sp3; yc = oy + j*sp3
        cx, cy = outer/2+ox, outer/2+oy
        if not ((cx-inner/2<xc<cx+inner/2) and (cy-inner/2<yc<cy+inner/2)):
            pts_ring.append([xc, yc])
pts_ring = np.array(pts_ring)

models = [
    ('非均匀密度', pts_nud),
    ('不连通体', pts_disc),
    ('回字形', pts_ring),
]

# ── 上排: 三角剖分 ──
cols = ['#cc3333', '#cc3333', '#cc3333']
for col, (name, pts) in enumerate(models):
    ax = axes[0, col]
    ax.set_title(f'({chr(97+col)})', fontsize=14, loc='left', pad=4)
    try:
        tri = Delaunay(pts)
        ax.triplot(pts[:,0], pts[:,1], tri.simplices, color='#cc3333', lw=0.5, alpha=0.8)
    except:
        pass
    ax.plot(pts[:,0], pts[:,1], '.', markersize=8, color='#777777')
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.4, color='#cccccc')
    for s in ax.spines.values(): s.set_linewidth(1.0)
    ax.tick_params(labelsize=11)
    if col == 0:
        ax.set_ylabel('Y (m)', fontsize=12)
    else:
        ax.set_yticklabels([])
    ax.set_xlim(0, 5000 if col < 2 else 5000)
    ax.set_ylim(0, 4000 if col < 2 else 5000)

# ── 下排: 原始点集（无三角剖分） ──
for col, (name, pts) in enumerate(models):
    ax = axes[1, col]
    ax.set_title(f'({chr(100+col)})', fontsize=14, loc='left', pad=4)
    ax.plot(pts[:,0], pts[:,1], '.', markersize=8, color='#777777')
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.4, color='#cccccc')
    for s in ax.spines.values(): s.set_linewidth(1.0)
    ax.tick_params(labelsize=11)
    if col == 0:
        ax.set_ylabel('Y (m)', fontsize=12)
    else:
        ax.set_yticklabels([])
    ax.set_xlim(0, 5000 if col < 2 else 5000)
    ax.set_ylim(0, 4000 if col < 2 else 5000)

plt.tight_layout(pad=0.6)
plt.subplots_adjust(hspace=0.35, wspace=0.3)
fig.text(0.5, 0.015, 'X (m)', ha='center', fontsize=12)

fig.savefig('./figures/Fig6.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig6.png', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig6.svg', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig6 saved.")
plt.close()
