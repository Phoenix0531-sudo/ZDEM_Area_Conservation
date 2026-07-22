# -*- coding: utf-8 -*-
"""
拼接11张ZDEM颗粒图：从上到下时间步从小到大排列，
除最后一张外隐藏X轴数字，紧贴无间距。
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import os, re, sys

# 图片目录
img_dir = sys.argv[1] if len(sys.argv) > 1 else '/images'
output = '/output/stitched_figure.pdf'

# 获取所有jpg并解析时间步数字
files = []
for f in os.listdir(img_dir):
    if f.endswith('.jpg'):
        # 尝试从文件名解析数字
        nums = re.findall(r'\d+', f)
        if nums:
            step = int(nums[-1])
            files.append((step, os.path.join(img_dir, f)))

if not files:
    print("未找到JPG文件")
    sys.exit(1)

files.sort(key=lambda x: x[0])
print(f"找到 {len(files)} 张图片，时间步: {[f[0] for f in files]}")

# 读取所有图片
images = [mpimg.imread(f[1]) for f in files]
n = len(images)

# 获取图片尺寸（所有图应一致）
h_img, w_img = images[0].shape[:2]
aspect = w_img / h_img

# 图宽6.3in，高根据图片比例算
fig_width = 6.3
single_height = fig_width / aspect  # 每张图高度
total_height = single_height * n * 0.85  # 紧贴，不要留白

fig = plt.figure(figsize=(fig_width, total_height), facecolor='white')

# 用 GridSpec 紧密排列
gs = gridspec.GridSpec(n, 1, hspace=0, wspace=0,
                        left=0, right=1, bottom=0, top=1)

for i in range(n):
    ax = fig.add_subplot(gs[i])
    ax.imshow(images[i], aspect='auto')
    ax.set_xlim(0, w_img)
    ax.set_ylim(h_img, 0)  # 翻转Y轴
    
    # 隐藏坐标轴上下左右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # 刻度设置
    ax.tick_params(which='both', length=0, labelsize=0, pad=0)
    
    # 隐藏所有刻度标签
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    
    # 显示Y轴刻度标签（时间步编号）
    # 在每个图左侧显示时间步
    step = files[i][0]
    ax.text(-w_img * 0.02, h_img / 2, f'{step}', fontsize=9,
            ha='right', va='center', transform=ax.transData,
            fontfamily='sans-serif')

fig.savefig(output, dpi=300, bbox_inches='tight', pad_inches=0,
            facecolor='white', edgecolor='none')
print(f"拼接图已保存到 {output}")
