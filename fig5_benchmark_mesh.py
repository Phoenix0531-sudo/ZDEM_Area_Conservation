# -*- coding: utf-8 -*-
"""
图5: 基准几何模型三角剖分结果 — (a)(c)矩形晶格 (b)(d)六方圆形+局部放大
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np
from matplotlib.collections import PatchCollection
from scipy.spatial import Delaunay

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans'],
    'font.family': 'sans-serif',
    'font.serif': [],
    'font.size': 12,
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

fig, axes = plt.subplots(2, 2, figsize=(6.3, 6.0), facecolor='white', dpi=300)

# ── 矩形晶格点集 ──
spacing = 170
nx, ny = int(4800/spacing)+1, int(3600/spacing)+1
x = np.arange(nx)*spacing; y = np.arange(ny)*spacing
xx,yy = np.meshgrid(x,y)
pts_rect = np.column_stack([xx.ravel(), yy.ravel()])

# ── 六方圆形点集 ──
R = 2500; a = spacing*0.87
rows = int(2*R/(a*np.sqrt(3)/2))+1
pts_hex = []
for row in range(rows):
    yc = -R + row*a*np.sqrt(3)/2; offset = a/2 if row%2==1 else 0
    cols = int(2*R/a)+2
    for col in range(cols):
        xc = -R + col*a + offset
        if xc**2+yc**2 <= R**2: pts_hex.append([xc+R, yc+R])
pts_hex = np.array(pts_hex)

# ── Delaunay 三角剖分 ──
tri_rect = Delaunay(pts_rect)
tri_hex = Delaunay(pts_hex)
edge_color = '#cc3333'  # 红色网格线

def plot_mesh(ax, pts, tri, use_circles=False):
    ax.triplot(pts[:,0], pts[:,1], tri.simplices, color=edge_color, lw=0.5, alpha=0.8)
    if use_circles:
        r = a * 0.5
        patches = [plt.Circle((x, y), r) for x, y in pts]
        pc = PatchCollection(patches, facecolor='#999999', edgecolor='#444444', linewidth=0.2)
        ax.add_collection(pc)
    else:
        ax.plot(pts[:,0], pts[:,1], '.', markersize=8, color='#777777')
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.4, color='#cccccc')
    for s in ax.spines.values(): s.set_linewidth(1.0)
    ax.tick_params(labelsize=11)

# (a) 矩形晶格
ax = axes[0,0]; ax.set_title('(a)', fontsize=14, loc='left', pad=4)
plot_mesh(ax, pts_rect, tri_rect)
ax.set_xlim(0,5000); ax.set_ylim(0,4200)
ax.set_ylabel('Y (m)', fontsize=12)

# (b) 六方圆形 + 局部放大
ax = axes[0,1]; ax.set_title('(b)', fontsize=14, loc='left', pad=4)
plot_mesh(ax, pts_hex, tri_hex, use_circles=True)
ax.set_xlim(0,5000); ax.set_ylim(0,5000)
ax.set_yticklabels([])

# 放大视图
axins = inset_axes(ax, width='30%', height='30%', loc='upper right',
                   bbox_to_anchor=(0.05,0.05,0.9,0.9), bbox_transform=ax.transAxes)
r0 = a*0.5*0.87
cx0, cy0 = 2500, 2800
for row in range(3):
    for col in range(3):
        xi = cx0 + (col-1)*a + (a/2 if row%2==1 else 0)
        yi = cy0 + (row-1)*a*np.sqrt(3)/2
        cr = plt.Circle((xi,yi), r0, facecolor='#999999', edgecolor='#444444', lw=0.6)
        axins.add_patch(cr)
axins.set_xlim(cx0-a, cx0+a); axins.set_ylim(cy0-a*np.sqrt(3)/2, cy0+a*np.sqrt(3)/2)
axins.set_aspect('equal')
axins.tick_params(labelleft=False,labelbottom=False,left=False,bottom=False)
mark_inset(ax, axins, loc1=1, loc2=3, fc='none', ec='black', lw=0.8)

# (c) 矩形晶格（过滤后—均匀点阵过滤无变化，视觉一致）
ax = axes[1,0]; ax.set_title('(c)', fontsize=14, loc='left', pad=4)
plot_mesh(ax, pts_rect, tri_rect)
ax.set_xlim(0,5000); ax.set_ylim(0,4200)
ax.set_ylabel('Y (m)', fontsize=12)

# (d) 六方圆形（过滤后）
ax = axes[1,1]; ax.set_title('(d)', fontsize=14, loc='left', pad=4)
plot_mesh(ax, pts_hex, tri_hex, use_circles=True)
ax.set_xlim(0,5000); ax.set_ylim(0,5000)
ax.set_yticklabels([])

axins2 = inset_axes(ax, width='30%', height='30%', loc='upper right',
                    bbox_to_anchor=(0.05,0.05,0.9,0.9), bbox_transform=ax.transAxes)
for row in range(3):
    for col in range(3):
        xi = cx0 + (col-1)*a + (a/2 if row%2==1 else 0)
        yi = cy0 + (row-1)*a*np.sqrt(3)/2
        cr = plt.Circle((xi,yi), r0, facecolor='#999999', edgecolor='#444444', lw=0.6)
        axins2.add_patch(cr)
axins2.set_xlim(cx0-a, cx0+a); axins2.set_ylim(cy0-a*np.sqrt(3)/2, cy0+a*np.sqrt(3)/2)
axins2.set_aspect('equal')
axins2.tick_params(labelleft=False,labelbottom=False,left=False,bottom=False)
mark_inset(ax, axins2, loc1=1, loc2=3, fc='none', ec='black', lw=0.8)

plt.tight_layout(pad=0.8)
plt.subplots_adjust(hspace=0.35, wspace=0.3)
fig.text(0.5, 0.015, 'X (m)', ha='center', fontsize=12)

fig.savefig('./figures/Fig5.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig5.png', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('./figures/Fig5.svg', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig5 saved.")
plt.close()
