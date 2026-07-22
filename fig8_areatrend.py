# -*- coding: utf-8 -*-
"""
图8: 面积趋势曲线 — 回退到用户原始风格
蓝线+圆标记、虚线网格、图例框、四边坐标轴
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
import numpy as np
import os, re
from scipy.spatial import Delaunay

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei'],
    'font.family': 'sans-serif',
    'font.serif': [],
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

# ── 读 particles.txt 数据 ──
data_dir = '/app/data'
def read_particles(fname):
    pts = []
    with open(fname, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines[3:]:
        if line.strip().startswith('-'): break
        parts = line.strip().split('\t')
        if len(parts) >= 5:
            try: pts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            except: pass
    if not pts: return None, None
    coords = np.array([[p[0],p[1]] for p in pts], dtype=np.float32)
    radii = np.array([[p[2]] for p in pts], dtype=np.float32)
    return coords, radii

def compute_area(coords, radii, factor=3.0):
    if coords is None or coords.shape[0] < 3: return 0.0
    tri = Delaunay(coords)
    avg_r = float(np.mean(radii))
    th = factor * avg_r
    total = 0.0
    for si in tri.simplices:
        p1,p2,p3 = coords[si]
        if (np.linalg.norm(p1-p2)<=th and np.linalg.norm(p2-p3)<=th and np.linalg.norm(p3-p1)<=th):
            total += 0.5 * abs((p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0]))
    return total

files = sorted([f for f in os.listdir(data_dir) if f.endswith('_particles.txt')],
               key=lambda f: int(re.findall(r'\d+', f)[-1]) if re.findall(r'\d+', f) else 0)
steps, areas = [], []
for fname in files:
    path = os.path.join(data_dir, fname)
    coords, radii = read_particles(path)
    if coords is None: continue
    area = compute_area(coords, radii)
    num = int(re.findall(r'\d+', fname)[-1])
    steps.append(num); areas.append(area)
    print(f'{fname}: {area:.0f}')

if len(steps) < 2:
    print("数据不足"); exit()

# ── 基准线 ──
base = areas[0]
threshold = 0.05  # 5%
upper = base * (1 + threshold)
lower = base * (1 - threshold)

# ── 绘图（用户原始风格） ──
fig, ax = plt.subplots(figsize=(6.3, 4.0), facecolor='white', dpi=300)
ax.plot(steps, areas, marker='o', markersize=5, linestyle='-',
        color='#1f77b4', linewidth=1.5, label='面积趋势', alpha=0.9)
ax.axhline(base, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
ax.axhline(upper, color='red', linestyle='--', linewidth=1.0,
           label=f'+5% 容忍阈值 ({upper:.0f})', alpha=0.7)
ax.axhline(lower, color='green', linestyle='--', linewidth=1.0,
           label=f'-5% 容忍阈值 ({lower:.0f})', alpha=0.7)

ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
ax.legend(loc='upper right', fontsize=10, frameon=True, fancybox=False, edgecolor='black')
ax.set_xlabel('文件编号', fontsize=13)
ax.set_ylabel('面积 (m²)', fontsize=13)
ax.tick_params(axis='both', labelsize=11)

fig.suptitle('面积趋势', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout(pad=1.0)
plt.subplots_adjust(top=0.92)

fig.savefig('/app/data/Fig8_趋势.pdf', dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig('/app/data/Fig8_趋势.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Fig8 saved.")
plt.close()
