# -*- coding: utf-8 -*-
"""
图2: 基准几何模型 — (a)矩形晶格 (b)六方最密堆积圆形+局部放大
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans'],
    'font.family': 'sans-serif', 'font.serif': [],
    'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 3.5), facecolor='white', dpi=300)
PARTICLE_COLOR = '#777777'
PARTICLE_EDGE = '#888888'

# ── (a) 矩形晶格 ──
ax1.set_title('(a)', fontsize=14, loc='left', pad=6)
sp = 300
nx, ny = int(4800/sp)+1, int(3600/sp)+1
x = np.arange(nx)*sp; y = np.arange(ny)*sp
xx,yy = np.meshgrid(x,y)
ax1.plot(xx.ravel(), yy.ravel(), '.', markersize=18, color=PARTICLE_COLOR)
ax1.set_xlim(0,5000); ax1.set_ylim(0,4200)
ax1.set_ylabel('Y (m)', fontsize=12)
ax1.set_xlabel('X (m)', fontsize=12)
ax1.tick_params(axis='y', labelleft=True)

# ── (b) 六方最密堆积圆形（实际碰触圆球） ──
ax2.set_title('(b)', fontsize=14, loc='left', pad=6)
R = 2500; r = 100  # 球半径
# 生成六方网格点
a = r*2  # 同排圆心距
b = r*np.sqrt(3)  # 排间距
cx, cy = R, R  # 圆心
pts = []
for row in range(-int(R/b)-1, int(R/b)+2):
    yy_off = cy + row*b
    if abs(yy_off-cy) > R: continue
    for col in range(-int(R/a)-1, int(R/a)+2):
        xx_off = cx + col*a + (a/2 if row%2==1 else 0)
        if (xx_off-cx)**2 + (yy_off-cy)**2 <= R**2:
            circle = plt.Circle((xx_off, yy_off), r, facecolor='#aaaaaa',
                                edgecolor=PARTICLE_EDGE, linewidth=0.2)
            ax2.add_patch(circle)
ax2.set_xlim(0,5000); ax2.set_ylim(0,5000)
ax2.set_aspect('equal')
ax2.tick_params(axis='y', labelleft=False)

# 放大视图
axins = inset_axes(ax2, width='30%', height='30%', loc='upper right',
                   bbox_to_anchor=(0.05,0.05,0.9,0.9), bbox_transform=ax2.transAxes)
for row in range(3):
    for col in range(3):
        xi = (col-1)*a + (a/2 if row%2==1 else 0)
        yi = (row-1)*b
        cr = plt.Circle((xi, yi), r*1.2, facecolor='#999999', edgecolor='#444444', lw=0.6)
        axins.add_patch(cr)
axins.set_xlim(-a, a); axins.set_ylim(-b, b)
axins.set_aspect('equal')
axins.tick_params(labelleft=False,labelbottom=False,left=False,bottom=False)
cx0, cy0 = cx, cy
ax2.add_patch(plt.Rectangle((cx0-a, cy0-b), 2*a, 2*b, fill=False, ec='black', lw=1.0, ls='-'))

# 网格
for ax in [ax1, ax2]:
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.4, color='#cccccc')
    for s in ax.spines.values(): s.set_linewidth(1.0)
    ax.tick_params(labelsize=11)

plt.tight_layout(pad=1.0)
plt.subplots_adjust(wspace=0.3)

fig.savefig('./figures/Fig2.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig2.png', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig2.svg', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig2 saved.")
plt.close()
