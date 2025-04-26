import numpy as np
import matplotlib.pyplot as plt
import os  # 添加os模块用于打开文件

def read_surface_points(filename):
    points = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[3:]:  # 跳过前3行
            if line.startswith('-'): break
            data = line.strip().split('\t')
            if len(data) >= 3:
                idx, x, y = int(data[0]), float(data[1]), float(data[2])
                points.append((x, y))
    return np.array(points)

def plot_surface_points(points, output_name):
    plt.figure(figsize=(12, 8), facecolor='white')
    ax = plt.gca()
    ax.set_facecolor('white')
    
    plt.scatter(points[:,0], points[:,1], 
               c='red',
               s=15,
               alpha=0.8,
               marker='o')
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('X坐标', fontsize=12)
    plt.ylabel('Y坐标', fontsize=12)
    plt.title('表面颗粒分布', fontsize=14)
    plt.axis('equal')
    
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    plt.close()

# 读取并绘制表面点
surface_points = read_surface_points('surface_particles.txt')
plot_surface_points(surface_points, 'surface_points.png')

print("图片已保存为 surface_points.png")

# 自动打开生成的图片
try:
    os.startfile('surface_points.png')
    print("已自动打开图片")
except Exception as e:
    print(f"无法自动打开图片: {e}")