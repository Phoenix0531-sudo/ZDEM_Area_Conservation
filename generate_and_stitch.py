# -*- coding: utf-8 -*-
"""
生成所有时间步的颗粒图并拼接为一张图
从上到下：时间步从小到大，紧贴排列
（带 numpy 兼容修复）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)

# ── numpy 兼容修复 ──
import numpy as np
# 修复 np.matrix.min/max 的 initial 参数问题
_orig_min = np.matrix.min
_orig_max = np.matrix.max
def _patched_min(self, axis=None, out=None, **kwargs):
    kwargs.pop('initial', None)
    return _orig_min(self, axis=axis, out=out)
def _patched_max(self, axis=None, out=None, **kwargs):
    kwargs.pop('initial', None)
    return _orig_max(self, axis=axis, out=out)
np.matrix.min = _patched_min
np.matrix.max = _patched_max

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os, sys, re
sys.path.insert(0, '/app')
import zdemio
import zdemplot

data_dir = '/app/data'
output_dir = '/output'

dat_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.dat')],
                   key=lambda f: int(re.findall(r'\d+', f)[-1]) if re.findall(r'\d+', f) else 0)
print(f"找到 {len(dat_files)} 个 .dat 文件")

ColorList, _ = zdemplot.get_color_map(os.path.join('/app/res', 'ColorRicebal.txt'))

figures = []
step_labels = []
for dat_file in dat_files:
    path = os.path.join(data_dir, dat_file)
    try:
        WALL, BALL, CONTACT, BOND, step, GROUP = zdemio.read_data(path)
    except Exception as e:
        print(f"  跳过 {dat_file}: {e}")
        continue

    BALLIdN1, BALLxyN2, BALLRadN1, BALLColor = zdemio.BallListStrToNumpyArray(BALL)
    WALLIdN1, WALLP1P2xyxyN4 = zdemio.WallListStrToNumpyArray(WALL)
    
    wleft, wright, wbottom, wtop = zdemplot.search_domain(
        WALLP1P2xyxyN4, BALLxyN2, BALLRadN1)
    
    fig = plt.figure(figsize=(6.3, 3.5), facecolor='white', dpi=200)
    ax = plt.gca()
    
    zdemplot.plot_ball(fig, ax, BALLxyN2, BALLRadN1, BALLColor, ColorList)
    zdemplot.plot_wall(fig, ax, WALLP1P2xyxyN4, ColorList, linewidth=1)
    
    ax.set_xlim(max(0, float(wleft)), float(wright))
    ax.set_ylim(float(wbottom), float(wtop))
    ax.set_aspect('equal', 'box')
    ax.axis('off')
    
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    
    temp = f'/tmp/{dat_file}.png'
    fig.savefig(temp, dpi=200, bbox_inches='tight', pad_inches=0, 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    figures.append(temp)
    step_num = int(re.findall(r'\d+', dat_file)[-1])
    step_labels.append(step_num)
    print(f"  {dat_file}: step={step_num}")

print(f"\n生成 {len(figures)} 张图，开始拼接...")

# ── 拼接 ──
from PIL import Image
imgs = [Image.open(f).convert('RGB') for f in figures]
min_w = min(im.width for im in imgs)
total_h = 0
processed = []
for i, (step, img) in enumerate(zip(step_labels, imgs)):
    w, h = img.size
    if i < len(imgs) - 1:
        # 除最后一张外裁掉底部 ~12%（坐标轴区域）
        crop = img.crop((0, 0, w, int(h * 0.88)))
    else:
        crop = img.copy()
    if crop.width != min_w:
        ratio = min_w / crop.width
        crop = crop.resize((min_w, int(crop.height * ratio)), Image.LANCZOS)
    processed.append(crop)
    total_h += crop.height

canvas = Image.new('RGB', (min_w, total_h), 'white')
y = 0
for img in processed:
    canvas.paste(img, (0, y))
    y += img.height

canvas.save(os.path.join(output_dir, 'stitched_figure.pdf'), 'PDF', resolution=300)
canvas.save(os.path.join(output_dir, 'stitched_figure.png'), 'PNG')
print(f"拼接完成: {min_w}x{total_h}")
