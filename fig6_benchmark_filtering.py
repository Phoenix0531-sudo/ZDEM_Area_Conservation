# -*- coding: utf-8 -*-
"""
图6: 算法在静态精度验证模型上过滤前后的对比
上排: (a)矩形晶格初始剖分 (b)六方圆形初始剖分
下排: (c)矩形晶格过滤后   (d)六方圆形过滤后
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

# ── 生成模型点集 ──
# 矩形晶格
spacing = 80.0
nx, ny = 30, 15
x = np.arange(nx) * spacing
y = np.arange(ny) * spacing
xx, yy = np.meshgrid(x, y)
points_rect = np.column_stack([xx.ravel(), yy.ravel()])

# 六方堆积圆形
R_circ = 600.0
a = spacing * 0.9
rows = int(2 * R_circ / (a * np.sqrt(3) / 2)) + 1
points_hex = []
for row in range(rows):
    yc = -R_circ + row * a * np.sqrt(3) / 2
    offset = a / 2 if row % 2 == 1 else 0
    cols = int(2 * R_circ / a) + 2
    for col in range(cols):
        xc = -R_circ + col * a + offset
        if xc**2 + yc**2 <= R_circ**2:
            points_hex.append([xc, yc])
points_hex = np.array(points_hex)

# ── 三角剖分 + 过滤 ──
def process(points, threshold_factor=3.0):
    avg_r = spacing / 2
    threshold = threshold_factor * avg_r
    tri = Delaunay(points)
    valid = []
    for si in tri.simplices:
        p1, p2, p3 = points[si]
        if (np.linalg.norm(p1-p2) <= threshold and
            np.linalg.norm(p2-p3) <= threshold and
            np.linalg.norm(p3-p1) <= threshold):
            valid.append(si)
    return tri, valid

tri_rect, valid_rect = process(points_rect)
tri_hex, valid_hex = process(points_hex)

# ── 2行 × 2列 ──
fig, axes = plt.subplots(2, 2, figsize=(6.3, 5.8), facecolor='white', dpi=300)
(a1, a2), (a3, a4) = axes

# (a) 矩形-初始
a1.set_title('(a) 矩形晶格 初始剖分', fontsize=12, pad=4)
a1.triplot(points_rect[:,0], points_rect[:,1], tri_rect.simplices, color='#b0b0b0', lw=0.3)
a1.plot(points_rect[:,0], points_rect[:,1], '.', markersize=1.8, color='#333333')

# (b) 六方-初始
a2.set_title('(b) 六方圆形 初始剖分', fontsize=12, pad=4)
a2.triplot(points_hex[:,0], points_hex[:,1], tri_hex.simplices, color='#b0b0b0', lw=0.3)
a2.plot(points_hex[:,0], points_hex[:,1], '.', markersize=1.8, color='#333333')

# (c) 矩形-过滤后
a3.set_title('(c) 矩形晶格 过滤后', fontsize=12, pad=4)
for si in valid_rect:
    t = points_rect[si]
    a3.fill(t[:,0], t[:,1], facecolor='#f0f0f0', edgecolor='#444444', lw=0.4, alpha=0.9)
a3.plot(points_rect[:,0], points_rect[:,1], '.', markersize=1.8, color='#333333')

# (d) 六方-过滤后
a4.set_title('(d) 六方圆形 过滤后', fontsize=12, pad=4)
for si in valid_hex:
    t = points_hex[si]
    a4.fill(t[:,0], t[:,1], facecolor='#f0f0f0', edgecolor='#444444', lw=0.4, alpha=0.9)
a4.plot(points_hex[:,0], points_hex[:,1], '.', markersize=1.8, color='#333333')

for ax in [a1,a2,a3,a4]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(direction='in', labelsize=10, width=0.8, length=4)
    ax.grid(False)
    ax.set_aspect('equal','box')
    ax.set_xlabel('X (m)', fontsize=11)
    ax.set_ylabel('Y (m)', fontsize=11)

fig.suptitle('图6  算法在静态精度验证模型上的过滤前后对比', fontsize=12, fontweight='bold', y=1.015)
plt.tight_layout(pad=0.8)
plt.subplots_adjust(top=0.90, hspace=0.35, wspace=0.2)

fig.savefig('Fig6.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('Fig6.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig6 saved.")
plt.close()
