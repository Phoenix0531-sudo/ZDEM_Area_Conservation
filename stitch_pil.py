# -*- coding: utf-8 -*-
"""
直接用 Pillow 拼接 JPG 图片
"""
import subprocess, os, sys

# 安装 Pillow
subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow', '-q'], capture_output=True)

from PIL import Image
import re

img_dir = '/images'
output = '/output/stitched_figure.pdf'

# 获取所有 jpg 并排序
files = []
for f in os.listdir(img_dir):
    if f.endswith('.jpg'):
        nums = re.findall(r'\d+', f)
        if nums:
            files.append((int(nums[-1]), os.path.join(img_dir, f)))

if not files:
    print("没有找到 JPG 文件")
    # fallback: 按文件名排序
    files = sorted([(i, os.path.join(img_dir, f)) for i, f in enumerate(os.listdir(img_dir)) if f.endswith('.jpg')])

files.sort(key=lambda x: x[0])
print(f"找到 {len(files)} 张图片")
print(f"时间步: {[f[0] for f in files]}")

# 加载图片，裁剪掉 X 轴数字部分
images = []
for step, path in files:
    img = Image.open(path).convert('RGB')
    w, h = img.size
    # 裁剪掉底部 15% (坐标轴和数字区域)，除最后一张外
    images.append((step, img, w, h))

# 取所有图的最小宽度和统一高度（除去底部坐标轴区域）
# 最后一张保留底部区域，其他去掉
min_w = min(img[2] for img in images)
total_h = 0
processed = []
for i, (step, img, w, h) in enumerate(images):
    if i == len(images) - 1:
        # 最后一张保留全部
        crop = img.crop((0, 0, w, h))
    else:
        # 裁剪掉底部约 12% 坐标轴区域
        crop_h = int(h * 0.88)
        crop = img.crop((0, 0, w, crop_h))
    # 统一宽度
    if crop.width != min_w:
        ratio = min_w / crop.width
        new_h = int(crop.height * ratio)
        crop = crop.resize((min_w, new_h), Image.LANCZOS)
    processed.append((step, crop))
    total_h += crop.height

# 创建拼接大图
canvas = Image.new('RGB', (min_w, total_h), 'white')
y_offset = 0
for step, img in processed:
    canvas.paste(img, (0, y_offset))
    y_offset += img.height

canvas.save(output, 'PDF', resolution=300)
canvas.save('/output/stitched_figure.png', 'PNG')
print(f"拼接完成: {output} ({min_w}x{total_h})")
