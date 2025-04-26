import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import re
import sys

# 导入zdemplot.py中的函数
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from zdemplot import get_color_map

# 常量定义
COLOR_TO_EXTRACT = [7]  # 要提取的颗粒颜色，可以是单个颜色或颜色列表
THRESHOLD_FACTOR = 3.0  # 边长阈值因子

def read_surface_particles(filename):
    """从surface_particles.txt文件中读取颗粒信息"""
    particles = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # 跳过前3行（标题和分隔线）
            for line in lines[3:]:
                if line.startswith('-'):  # 遇到分隔线结束读取
                    break
                
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    try:
                        idx = int(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        # 读取半径和颜色信息
                        radius = float(parts[3]) if len(parts) > 3 else 100.0  # 默认半径
                        color = int(parts[4]) if len(parts) > 4 else 0  # 默认颜色
                        
                        particles.append((idx, x, y, radius, color))
                    except (ValueError, IndexError):
                        continue
        
        if not particles:
            print(f"警告: 在 {filename} 中没有找到有效的颗粒数据")
            return None, None, None
        
        # 提取坐标、半径和颜色，使用numpy数组
        coords = np.array([[p[1], p[2]] for p in particles])
        radii = np.array([[p[3]] for p in particles])
        colors = np.array([[p[4]] for p in particles])
        
        print(f"从 {filename} 中读取了 {len(particles)} 个颗粒")
        return coords, radii, colors
    
    except Exception as e:
        print(f"读取 {filename} 时出错: {e}")
        return None, None, None

def plot_particles(coords, radii=None, title="颗粒分布"):
    """绘制颗粒分布"""
    if coords is None or coords.shape[0] == 0:
        print("没有颗粒数据可以绘制")
        return
    
    plt.figure(figsize=(14, 12), facecolor='white')
    ax = plt.gca()
    ax.set_facecolor('white')
    
    # 将matrix转换为array以避免维度问题
    coords_array = np.array(coords)
    
    # 确保使用一维数组
    x = coords_array[:, 0].flatten()
    y = coords_array[:, 1].flatten()
    
    # 使用颗粒实际半径绘制圆形
    if radii is not None:
        radii_array = np.array(radii).flatten()
        for i in range(len(x)):
            circle = plt.Circle((x[i], y[i]), radii_array[i], fill=True, color='black', alpha=0.6)
            ax.add_patch(circle)
    else:
        # 如果没有半径信息，使用默认大小
        plt.scatter(x, y, c='black', s=10, alpha=0.6)
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('X坐标', fontsize=12)
    plt.ylabel('Y坐标', fontsize=12)
    plt.title(title, fontsize=14)
    plt.axis('equal')
    plt.show()

def create_triangulation(coords):
    """创建三角网格划分"""
    if coords is None or coords.shape[0] < 3:
        print("颗粒数量不足，无法创建三角网格")
        return None
    
    # 将matrix转换为array
    coords_array = np.array(coords)
    
    # 检查点是否共线
    if coords_array.shape[0] > 2:
        # 计算所有点的方差
        x_var = np.var(coords_array[:, 0])
        y_var = np.var(coords_array[:, 1])
        
        if x_var < 1e-6 or y_var < 1e-6:
            print("警告: 点几乎在一条直线上，三角剖分可能无法正常工作")
    
    try:
        tri = Triangulation(coords_array[:, 0], coords_array[:, 1])
        
        # 检查三角形数量
        if len(tri.triangles) == 0:
            print("警告: 没有生成任何三角形")
            return None
            
        print(f"成功创建三角网格，共有{len(tri.triangles)}个三角形")
        return tri
    except Exception as e:
        print(f"创建三角网格时出错: {e}")
        return None

def plot_triangulation(tri, coords=None, radii=None, title="三角网格划分"):
    """绘制三角网格划分"""
    if tri is None:
        print("没有三角网格可以绘制")
        return
    
    plt.figure(figsize=(14, 12), facecolor='white')
    ax = plt.gca()
    ax.set_facecolor('white')
    
    # 如果提供了坐标和半径，先绘制颗粒
    if coords is not None and radii is not None:
        coords_array = np.array(coords)
        radii_array = np.array(radii).flatten()
        for i in range(len(coords_array)):
            circle = plt.Circle((coords_array[i, 0], coords_array[i, 1]), radii_array[i], 
                               fill=True, color='lightgray', alpha=0.3)
            ax.add_patch(circle)
    
    # 绘制三角网格
    plt.triplot(tri, color='lime', linestyle='-', alpha=1.0, linewidth=0.8)
    
    # 绘制顶点
    plt.scatter(tri.x, tri.y, c='blue', s=8, alpha=0.5)
    
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('X坐标', fontsize=12)
    plt.ylabel('Y坐标', fontsize=12)
    plt.title(title, fontsize=14)
    
    # 确保坐标轴比例相等
    plt.axis('equal')
    
    # 添加边距
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()
    x_margin = (x_max - x_min) * 0.05
    y_margin = (y_max - y_min) * 0.05
    plt.xlim(x_min - x_margin, x_max + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)
    
    plt.show()

def filter_triangles(tri, coords, radii, threshold_factor=THRESHOLD_FACTOR):
    """过滤边长大于阈值的三角形"""
    if tri is None:
        return None
    
    triangles = tri.triangles
    filtered_triangles = []
    
    # 计算平均半径作为参考
    avg_radius = np.mean(radii) if radii is not None and len(radii) > 0 else 1.0
    threshold = threshold_factor * avg_radius
    
    # 将matrix转换为array
    coords_array = np.array(coords)
    
    for triangle in triangles:
        p1, p2, p3 = coords_array[triangle[0]], coords_array[triangle[1]], coords_array[triangle[2]]
        
        # 计算三边长度
        edge1 = np.linalg.norm(p1 - p2)
        edge2 = np.linalg.norm(p2 - p3)
        edge3 = np.linalg.norm(p3 - p1)
        
        # 如果所有边长都小于阈值，保留该三角形
        if edge1 <= threshold and edge2 <= threshold and edge3 <= threshold:
            filtered_triangles.append(triangle)
    
    # 创建新的三角剖分
    filtered_triangles = np.array(filtered_triangles)
    if len(filtered_triangles) > 0:
        new_tri = Triangulation(tri.x, tri.y, filtered_triangles)
        return new_tri
    else:
        print("警告：过滤后没有剩余三角形")
        return None

def calculate_triangle_areas(tri, coords):
    """计算三角形面积并求和"""
    if tri is None:
        return 0.0
    
    triangles = tri.triangles
    total_area = 0.0
    
    # 将matrix转换为array
    coords_array = np.array(coords)
    
    for triangle in triangles:
        p1, p2, p3 = coords_array[triangle[0]], coords_array[triangle[1]], coords_array[triangle[2]]
        
        # 计算三角形面积（使用叉积）
        area = 0.5 * abs(np.cross(p2 - p1, p3 - p1))
        total_area += area
    
    return total_area

def process_surface_particles(threshold_factor=THRESHOLD_FACTOR):
    """处理surface_particles.txt中的颗粒数据"""
    surface_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "surface_particles.txt")
    
    if not os.path.exists(surface_file):
        print(f"错误: 文件 '{surface_file}' 不存在")
        return 0.0
    
    # 读取表面颗粒数据
    coords, radii, colors = read_surface_particles(surface_file)
    
    if coords is None or coords.shape[0] == 0:
        print("没有找到有效的表面颗粒数据")
        return 0.0
    
    # 确保COLOR_TO_EXTRACT是列表
    color_list = COLOR_TO_EXTRACT if isinstance(COLOR_TO_EXTRACT, list) else [COLOR_TO_EXTRACT]
    
    # 筛选指定颜色的颗粒
    color_indices = []
    for i in range(colors.shape[0]):
        if colors[i, 0] in color_list:
            color_indices.append(i)
    
    if not color_indices:
        print(f"没有找到颜色为{color_list}的颗粒")
        return 0.0
    
    # 提取对应颗粒的坐标和半径
    filtered_coords = np.array([coords[i] for i in color_indices])
    filtered_radii = np.array([radii[i] for i in color_indices])
    
    print(f"筛选出{len(color_indices)}个颜色为{color_list}的颗粒")
    
    # 显示颗粒分布
    plot_particles(filtered_coords, filtered_radii, f"颜色为{color_list}的颗粒分布")
    
    # 创建三角网格
    tri = create_triangulation(filtered_coords)
    
    if tri is not None:
        # 显示三角网格（同时显示颗粒）
        plot_triangulation(tri, filtered_coords, filtered_radii, "原始三角网格划分")
        
        # 过滤三角形
        filtered_tri = filter_triangles(tri, filtered_coords, filtered_radii, threshold_factor)
        
        if filtered_tri is not None:
            # 显示过滤后的三角网格（同时显示颗粒）
            plot_triangulation(filtered_tri, filtered_coords, filtered_radii, 
                              f"过滤后的三角网格划分 (阈值 = {threshold_factor} * 平均半径)")
            
            # 计算总面积
            total_area = calculate_triangle_areas(filtered_tri, filtered_coords)
            # 将面积精度调整为千位
            rounded_area = round(total_area, -3)
            print(f"总面积: {rounded_area:.0f} 平方单位")
            return total_area
    
    return 0.0

def main():
    # 处理表面颗粒数据
    area = process_surface_particles()
    
    # 确保COLOR_TO_EXTRACT是列表
    color_list = COLOR_TO_EXTRACT if isinstance(COLOR_TO_EXTRACT, list) else [COLOR_TO_EXTRACT]
    
    if area > 0:
        # 将面积精度调整为千位
        rounded_area = round(area, -3)
        print(f"\n颜色为{color_list}的颗粒面积计算结果: {rounded_area:.0f} 平方单位")
    else:
        print(f"\n没有找到任何颜色为{color_list}的有效颗粒数据进行面积计算")

if __name__ == "__main__":
    main()