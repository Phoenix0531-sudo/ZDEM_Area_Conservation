import numpy as np
import matplotlib
import matplotlib.font_manager
# 强制刷新 matplotlib 字体缓存，确保系统已安装字体被正确识别
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# ── 全局字体：sans-serif 优先匹配系统中文字体；stix math 处理英文/数字 ──
plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'DejaVu Sans'],
    'font.family': 'sans-serif',
    'font.serif': [],            # 清空衬线字体列表，防止回退到 Times New Roman 导致中文乱码
    'mathtext.fontset': 'stix',
})

# 模拟颗粒分布
NUM_POINTS = 300
BOX1 = (0, 10, 0, 3)
BOX2 = (2, 8, 3, 5)

# 边长阈值因子
THRESHOLD_FACTOR = 3.0

# --- 学术色彩方案 (Professional Color Scheme) ---
PARTICLE_COLOR = 'k'                   # 颗粒颜色 (黑色)
INITIAL_TRI_COLOR = '#a9a9a9'          # 初始网格线颜色 (深灰色)
VALID_TRI_FILL_COLOR = '#cae1ff'        # 有效三角形填充色 (柔和的淡蓝色)
VALID_TRI_EDGE_COLOR = '#191970'        # 有效三角形边框色 (午夜蓝)
AXIS_BORDER_COLOR = 'black'            # 坐标轴边框颜色

# --- 2. 生成模拟数据 (Generate Simulation Data) ---
# (此部分代码与之前相同，保持不变)
points1 = np.random.rand(int(NUM_POINTS * 0.7), 2)
points1[:, 0] = points1[:, 0] * (BOX1[1] - BOX1[0]) + BOX1[0]
points1[:, 1] = points1[:, 1] * (BOX1[3] - BOX1[2]) + BOX1[2]
points2 = np.random.rand(int(NUM_POINTS * 0.3), 2)
points2[:, 0] = points2[:, 0] * (BOX2[1] - BOX2[0]) + BOX2[0]
points2[:, 1] = points2[:, 1] * (BOX2[3] - BOX2[2]) + BOX2[2]
points = np.vstack([points1, points2])
avg_radius = 0.5
threshold = THRESHOLD_FACTOR * avg_radius

# --- 3. 执行三角剖分与优化 (Perform Triangulation and Filtering) ---
# (此部分代码与之前相同，保持不变)
initial_tri = Delaunay(points)
valid_triangles_indices = []
for simplex_indices in initial_tri.simplices:
    simplex_coords = points[simplex_indices]
    p1, p2, p3 = simplex_coords
    edge1_len = np.linalg.norm(p1 - p2)
    edge2_len = np.linalg.norm(p2 - p3)
    edge3_len = np.linalg.norm(p3 - p1)
    if (edge1_len <= threshold) and (edge2_len <= threshold) and (edge3_len <= threshold):
        valid_triangles_indices.append(simplex_indices)

# --- 4. 绘制学术级图表 (Create Publication-Quality Plot) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 3.2), facecolor='white')

# --- 子图 (a): 初始 Delaunay 三角剖分 ---
ax1.set_title('(a) 初始Delaunay三角剖分', fontsize=12, pad=12)
ax1.triplot(points[:, 0], points[:, 1], initial_tri.simplices, color=INITIAL_TRI_COLOR, lw=0.75)
ax1.plot(points[:, 0], points[:, 1], '.', markersize=2.5, color=PARTICLE_COLOR)

# --- 子图 (b): 优化后的三角网格 ---
ax2.set_title('(b) 边长阈值过滤后', fontsize=12, pad=12)
for tri_indices in valid_triangles_indices:
    triangle = points[tri_indices]
    ax2.fill(triangle[:, 0], triangle[:, 1],
             facecolor=VALID_TRI_FILL_COLOR, edgecolor=VALID_TRI_EDGE_COLOR,
             linewidth=0.8)
ax2.plot(points[:, 0], points[:, 1], '.', markersize=2.5, color=PARTICLE_COLOR)

# --- 为两个子图统一应用学术化样式 ---
for ax in [ax1, ax2]:
    ax.set_aspect('equal', 'box')
    ax.grid(False)
    ax.margins(0)

    # 坐标轴样式：L型（隐藏上/右脊线）、刻度朝内
    ax.tick_params(axis='both', which='major', direction='in', labelsize=10, width=1.2, length=5)
    ax.tick_params(axis='both', which='minor', direction='in', width=1.0, length=3)
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_yticks([0, 2, 4, 6])
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
        spine.set_color(AXIS_BORDER_COLOR)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

ax1.set_ylabel('Y (m)', fontsize=11)
ax1.set_xlabel('X (m)', fontsize=12)
ax2.tick_params(axis='y', labelleft=False)
ax2.set_ylabel('')


plt.subplots_adjust(wspace=0.3)

plt.savefig('./figures/Fig1.pdf', dpi=300, bbox_inches='tight')
plt.savefig('./figures/Fig1.png', dpi=300, bbox_inches='tight')
plt.savefig('./figures/Fig1.svg', dpi=300, bbox_inches='tight')
plt.show()
