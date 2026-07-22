# -*- coding: utf-8 -*-
"""
图7: 算法在复杂几何模型上过滤前后的对比
上排:(a)非均匀密度初始 (b)不连通体初始 (c)回字形初始
下排:(d)非均匀密度过滤后 (e)不连通体过滤后 (f)回字形过滤后
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei'],
    'font.family': 'sans-serif', 'font.serif': [],
    'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
})

# ── 模型点集 ──
np.random.seed(1)
n = 500
# (a) 非均匀密度
r = np.random.rand(n) * 700
theta = np.random.rand(n) * 2 * np.pi
keep = np.random.rand(n) < np.exp(-r / 300)
pm1 = np.column_stack([r[keep]*np.cos(theta[keep]), r[keep]*np.sin(theta[keep])])

# (b) 不连通体
n2 = 300
pm2_l = np.column_stack([np.random.randn(n2)*80-300, np.random.randn(n2)*80])
pm2_r = np.column_stack([np.random.randn(n2)*80+300, np.random.randn(n2)*80])
pm2 = np.vstack([pm2_l, pm2_r])

# (c) 回字形
ow, iw = 600, 300
n3 = 800
xo = (np.random.rand(n3)-0.5)*ow; yo = (np.random.rand(n3)-0.5)*ow
mask = ~((np.abs(xo)<iw/2) & (np.abs(yo)<iw/2))
pm3 = np.column_stack([xo[mask], yo[mask]])

models = [
    ('非均匀密度', pm1),
    ('不连通体', pm2),
    ('回字形空洞', pm3),
]

# ── 剖分+过滤 ──
def process(pts, factor=3.0):
    avg_r = 40.0  # 近似颗粒间距
    th = factor * avg_r
    tri = Delaunay(pts)
    valid = []
    for si in tri.simplices:
        p1,p2,p3 = pts[si]
        if (np.linalg.norm(p1-p2)<=th and np.linalg.norm(p2-p3)<=th and np.linalg.norm(p3-p1)<=th):
            valid.append(si)
    return tri, valid

results = [process(m[1]) for m in models]

# ── 2行 × 3列 ──
fig, axes = plt.subplots(2, 3, figsize=(6.3, 4.6), facecolor='white', dpi=300)
labels_top = ['(a)', '(b)', '(c)']
labels_bot = ['(d)', '(e)', '(f)']

for col, (name, pts) in enumerate(models):
    tri, valid = results[col]

    # 上排: 初始剖分
    ax_top = axes[0, col]
    ax_top.set_title(f'{labels_top[col]} {name} 初始剖分', fontsize=11, pad=4)
    ax_top.triplot(pts[:,0], pts[:,1], tri.simplices, color='#b0b0b0', lw=0.3)
    ax_top.plot(pts[:,0], pts[:,1], '.', markersize=1.8, color='#333333')

    # 下排: 过滤后
    ax_bot = axes[1, col]
    ax_bot.set_title(f'{labels_bot[col]} {name} 过滤后', fontsize=11, pad=4)
    for si in valid:
        t = pts[si]
        ax_bot.fill(t[:,0], t[:,1], facecolor='#f0f0f0', edgecolor='#444444', lw=0.4, alpha=0.9)
    ax_bot.plot(pts[:,0], pts[:,1], '.', markersize=1.8, color='#333333')

for ax in axes.flat:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(direction='in', labelsize=9, width=0.8, length=3)
    ax.grid(False)
    ax.set_aspect('equal','box')
    ax.set_xlabel('X (m)', fontsize=10)
    ax.set_ylabel('Y (m)', fontsize=10)

# 隐藏非左侧面板的重复Y轴标签
axes[0, 1].set_yticklabels([])  # (b)
axes[0, 2].set_yticklabels([])  # (c)
axes[1, 1].set_yticklabels([])  # (e)
axes[1, 2].set_yticklabels([])  # (f)

fig.suptitle('图7  算法在复杂几何模型上的过滤前后对比', fontsize=12, fontweight='bold', y=1.015)
plt.tight_layout(pad=0.6)
plt.subplots_adjust(top=0.89, hspace=0.4, wspace=0.25)

fig.savefig('Fig7.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('Fig7.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig7 saved.")
plt.close()
