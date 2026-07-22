# -*- coding: utf-8 -*-
"""
图3: 静态精度验证的基准几何模型
(a) 矩形晶格模型  (b) 六方最密堆积圆形模型
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 3.5), facecolor='white', dpi=300)

# ── (a) 矩形晶格模型 ──
ax1.set_title('(a) 矩形晶格模型', fontsize=12, pad=6)
nx, ny = 30, 15
spacing = 80.0
x = np.arange(nx) * spacing
y = np.arange(ny) * spacing
xx, yy = np.meshgrid(x, y)
points_rect = np.column_stack([xx.ravel(), yy.ravel()])
ax1.plot(points_rect[:, 0], points_rect[:, 1], '.', markersize=2.5, color='#333333')
ax1.set_xlabel('X (m)', fontsize=11)
ax1.set_ylabel('Y (m)', fontsize=11)

# ── (b) 六方最密堆积圆形模型 ──
ax2.set_title('(b) 六方最密堆积圆形模型', fontsize=12, pad=6)
R = 600.0
a = spacing * 0.9  # 粒子间距
rows = int(2 * R / (a * np.sqrt(3) / 2)) + 1
points_hex = []
for row in range(rows):
    yc = -R + row * a * np.sqrt(3) / 2
    offset = (a / 2) if row % 2 == 1 else 0
    cols = int(2 * R / a) + 2
    for col in range(cols):
        xc = -R + col * a + offset
        if xc**2 + yc**2 <= R**2:
            points_hex.append([xc, yc])
points_hex = np.array(points_hex)
ax2.plot(points_hex[:, 0], points_hex[:, 1], '.', markersize=2.5, color='#333333')
ax2.set_xlabel('X (m)', fontsize=11)
ax2.set_yticklabels([])

# 统一格式化
for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', direction='in', labelsize=10, width=0.8, length=4)
    ax.grid(False)
    ax.set_aspect('equal', 'box')

fig.suptitle('图3  基准几何模型（静态精度验证）', fontsize=12, fontweight='bold', y=1.01)
plt.tight_layout(pad=1.0)
plt.subplots_adjust(top=0.88, wspace=0.15)

fig.savefig('Fig3.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('Fig3.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig3 saved.")
plt.close()
