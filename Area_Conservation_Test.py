# -*- coding: utf-8 -*-
"""
2025/05/30
包羡钧 @ 东华理工大学
功能：
计算颗粒分布的面积守恒性
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
import re
import sys
from matplotlib.patches import Circle  # 添加Circle导入
import matplotlib as mpl
import zdemplot
import getopt # 导入getopt模块用于命令行参数解析
from matplotlib import colors as mcolors # 导入mcolors用于颜色处理
import matplotlib.cm as cm
import zdemio

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 导入zdemplot.py中的函数
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from zdemplot import get_color_map

# 常量定义 (将被命令行参数覆盖)
COLOR_TO_EXTRACT = [7]  # 要提取的颗粒颜色，可以是单个颜色或颜色列表
THRESHOLD_FACTOR = 3.0  # 边长阈值因子
DEFAULT_DATA_DIR = "data" # 默认数据目录

# 绘图开关
PLOT_PARTICLES = True
PLOT_ORIGINAL_TRI = True
PLOT_FILTERED_TRI = True
PLOT_AREA_TREND = 'raw' # 面积趋势图类型: 'raw', 'percentage', 'normalized'

def usage(softwareName):
    """打印脚本使用说明"""
    print(f"用法: python {softwareName} [选项]")
    print("  --dir=<目录>           指定包含 _particles.txt 文件的目录 (默认: data)")
    print("  --colors=<颜色编号,...>  指定要提取的颗粒颜色编号 (逗号分隔, 默认: 7)")
    print("  --threshold=<浮点数>     指定边长阈值因子 (默认: 3.0)")
    print("  --plot-particles=<true|false> 是否绘制颗粒分布图 (默认: true)")
    print("  --plot-original-tri=<true|false> 是否绘制原始三角网格图 (默认: true)")
    print("  --plot-filtered-tri=<true|false> 是否绘制过滤后三角网格图 (默认: true)")
    print("  --plot-area-type=<raw|percentage|normalized> 面积趋势图类型 (默认: raw)")
    print("  -h                     显示此帮助信息")

def read_surface_particles(filename):
    """从_particles.txt文件中读取颗粒信息"""
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
    coords_array = np.array(coords)
    x = coords_array[:, 0].flatten()
    y = coords_array[:, 1].flatten()
    if radii is not None:
        radii_array = np.array(radii).flatten()
        for i in range(len(x)):
            circle = Circle((x[i], y[i]), radii_array[i], fill=True, color='black', alpha=0.6)
            ax.add_patch(circle)
    else:
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
    if coords is not None and radii is not None:
        coords_array = np.array(coords)
        radii_array = np.array(radii).flatten()
        for i in range(len(coords_array)):
            circle = Circle((coords_array[i, 0], coords_array[i, 1]), radii_array[i], fill=True, color='lightgray', alpha=0.3)
            ax.add_patch(circle)
    plt.triplot(tri, color='lime', linestyle='-', alpha=1.0, linewidth=0.8)
    plt.scatter(tri.x, tri.y, c='blue', s=8, alpha=0.5)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.xlabel('X坐标', fontsize=12)
    plt.ylabel('Y坐标', fontsize=12)
    plt.title(title, fontsize=14)
    plt.axis('equal')
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
        
        # 修改为使用3D向量计算面积
        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1], 0])
        v2 = np.array([p3[0] - p1[0], p3[1] - p1[1], 0])
        area = 0.5 * np.linalg.norm(np.cross(v1, v2))
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
    
    # None 检查
    if coords is None or radii is None or colors is None:
        print("没有找到有效的表面颗粒数据 (coords/radii/colors 为 None)")
        return 0.0
    if coords.shape[0] == 0 or radii.shape[0] == 0 or colors.shape[0] == 0:
        print("没有找到有效的表面颗粒数据 (coords/radii/colors 长度为0)")
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
    filtered_coords = np.array([coords[i] for i in color_indices]) if coords is not None else None
    filtered_radii = np.array([radii[i] for i in color_indices]) if radii is not None else None
    filtered_colors = np.array([colors[i] for i in color_indices]) if colors is not None else None
    
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

def export_particles_txt(coords, radii, colors, dat_file):
    """
    根据 dat 文件名，在 data 目录下生成对应的 _particles.txt 文件
    """
    if dat_file is None:
        return
    # 获取 data 目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(dat_file))[0]
    output_file = os.path.join(data_dir, f'{base_name}_particles.txt')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("表面颗粒信息:\n")
            f.write("序号\tX坐标\tY坐标\t半径\t颜色编号\n")
            f.write("-" * 50 + "\n")
            for i in range(coords.shape[0]):
                x = coords[i, 0]
                y = coords[i, 1]
                radius = radii[i, 0]
                color = colors[i, 0]
                f.write(f"{i}\t{x:.2f}\t{y:.2f}\t{radius:.2f}\t{int(color)}\n")
            f.write("-" * 50 + "\n")
            f.write(f"表面颗粒总数: {coords.shape[0]}\n")
        print(f"颗粒信息已保存到 {output_file}")
    except Exception as e:
        print(f"写入文件失败: {str(e)}")

def process_multiple_files(data_dir=DEFAULT_DATA_DIR, color_list=COLOR_TO_EXTRACT, threshold_factor=THRESHOLD_FACTOR):
    """处理data目录下的所有_particles.txt文件"""
    results = []
    
    # 获取data目录的绝对路径
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    
    # 确保目录存在
    if not os.path.exists(data_dir):
        print(f"错误: 目录 '{data_dir}' 不存在")
        return results
    
    # 查找所有_particles.txt文件
    particle_files = [f for f in os.listdir(data_dir) if f.endswith('_particles.txt')]
    
    if not particle_files:
        print(f"在 {data_dir} 中没有找到任何_particles.txt文件")
        return results
    
    # 按文件名排序
    particle_files.sort()
    
    # 处理每个文件
    for file_name in particle_files:
        file_path = os.path.join(data_dir, file_name)
        print(f"\n处理文件: {file_name}")
        
        # 读取表面颗粒数据
        coords, radii, colors = read_surface_particles(file_path)
        
        # None 检查
        if coords is None or radii is None or colors is None:
            print(f"在 {file_name} 中没有找到有效的表面颗粒数据 (coords/radii/colors 为 None)")
            continue
        if coords.shape[0] == 0 or radii.shape[0] == 0 or colors.shape[0] == 0:
            print(f"在 {file_name} 中颗粒数据为空 (coords/radii/colors 长度为0)")
            continue
        
        # 筛选指定颜色的颗粒
        color_indices = []
        for i in range(colors.shape[0]):
            if colors[i, 0] in color_list:
                color_indices.append(i)
        
        if not color_indices:
            print(f"在 {file_name} 中没有找到颜色为{color_list}的颗粒")
            continue
        
        # 提取对应颗粒的坐标、半径和颜色
        filtered_coords = np.array([coords[i] for i in color_indices]) if coords is not None else None
        filtered_radii = np.array([radii[i] for i in color_indices]) if radii is not None else None
        filtered_colors = np.array([colors[i] for i in color_indices]) if colors is not None else None
        print(f"筛选出{len(color_indices)}个颜色为{color_list}的颗粒")
        
        if filtered_coords is None or filtered_radii is None or filtered_colors is None:
            print(f"在 {file_name} 中筛选颗粒时数据有误，跳过该文件")
            continue
        
        # 新增：自动导出 _particles.txt 文件（假设 file_name 源自 dat 文件名）
        # 如果你有 dat 文件路径，可以传入 dat_file，否则用 file_name 替代
        export_particles_txt(filtered_coords, filtered_radii, filtered_colors, dat_file=file_name.replace('_particles.txt', '.dat'))
        
        # 创建三角网格
        tri = create_triangulation(filtered_coords)
        
        if tri is not None:
            # 保存原始三角网格
            original_tri = tri
            
            # 过滤三角形
            filtered_tri = filter_triangles(tri, filtered_coords, filtered_radii, threshold_factor)
            
            if filtered_tri is not None:
                # 计算总面积
                total_area = calculate_triangle_areas(filtered_tri, filtered_coords)
                
                # 保存结果
                results.append({
                    'file_name': file_name,
                    'total_particles': len(color_indices),
                    'area': total_area,
                    'coords': filtered_coords,
                    'radii': filtered_radii,
                    'colors': filtered_colors,
                    'original_tri': original_tri,
                    'tri': filtered_tri
                })
                
                # 将面积精度调整为千位
                rounded_area = round(float(total_area), -3)
                print(f"总面积: {rounded_area:.0f} 平方单位")
    
    return results

def compare_results(results):
    """比较不同文件的结果"""
    if not results:
        print("没有可比较的结果")
        return
    
    print("\n=== 结果比较 ===")
    print("文件名\t\t颗粒数量\t面积(平方单位)")
    print("-" * 50)
    
    # 按文件名中的时间步排序
    sorted_results = sorted(results, key=lambda x: int(''.join(filter(str.isdigit, x['file_name']))))
    
    for result in sorted_results:
        rounded_area = round(float(result['area']), -3)
        print(f"{result['file_name']}\t{result['total_particles']}\t{rounded_area:.0f}")
    
    # 计算相邻图片之间的变化率
    print("\n=== 相邻图片变化分析 ===")
    for i in range(1, len(sorted_results)):
        prev_result = sorted_results[i-1]
        curr_result = sorted_results[i]
        
        # 计算面积变化率
        prev_area = float(prev_result['area'])
        curr_area = float(curr_result['area'])
        area_change = ((curr_area - prev_area) / prev_area) * 100
        
        # 计算颗粒数量变化率
        prev_particles = prev_result['total_particles']
        curr_particles = curr_result['total_particles']
        particle_change = ((curr_particles - prev_particles) / prev_particles) * 100
        
        print(f"\n从 {prev_result['file_name']} 到 {curr_result['file_name']}:")
        print(f"面积变化率: {area_change:+.2f}%")
        print(f"颗粒数量变化率: {particle_change:+.2f}%")
    
    # 计算第一张到最后一张的变化率
    if len(sorted_results) >= 2:
        first_area = float(sorted_results[0]['area'])
        last_area = float(sorted_results[-1]['area'])
        area_change = ((last_area - first_area) / first_area) * 100
        
        print("\n=== 总体变化分析 ===")
        print(f"从 {sorted_results[0]['file_name']} 到 {sorted_results[-1]['file_name']}")
        print(f"面积变化率: {area_change:+.2f}%")
        
        first_particles = sorted_results[0]['total_particles']
        last_particles = sorted_results[-1]['total_particles']
        particle_change = ((last_particles - first_particles) / first_particles) * 100
        print(f"颗粒数量变化率: {particle_change:+.2f}%")

def save_particle_plot(coords, radii, colors, colorlist, filename):
    fig = plt.figure(figsize=(14, 12), facecolor='white')
    ax = plt.gca()
    # 确保输入是 numpy 数组，并处理 None 或空数组情况
    if coords is None or coords.shape[0] == 0:
        print(f"警告: 没有坐标数据无法绘制颗粒图到 {filename}")
        plt.close(fig)
        return
    BALLxyN2 = np.asmatrix(coords)

    if radii is None or radii.shape[0] == 0:
         # 使用默认半径或者根据coords生成同等数量的默认半径
        print(f"警告: 没有半径数据，使用默认半径绘制颗粒图到 {filename}")
        BALLRadN1 = np.asmatrix(np.full((coords.shape[0], 1), 100.0)) # 默认半径 100.0
    else:
        BALLRadN1 = np.asmatrix(radii)

    if colors is None or colors.shape[0] == 0:
        print(f"警告: 没有颜色数据，使用默认颜色 0 绘制颗粒图到 {filename}")
        BALLColorN1 = np.asmatrix(np.full((coords.shape[0], 1), 0)) # 默认颜色 0
    else:
        BALLColorN1 = np.asmatrix(colors)

    # 确保 colorlist 不是 None 或空
    if colorlist is None or len(colorlist) == 0:
        print("错误: 颜色列表为空，无法绘制颗粒图")
        plt.close(fig)
        return

    zdemplot.plot_ball(fig, ax, BALLxyN2, BALLRadN1, BALLColorN1, colorlist)
    zdemplot.zdem_fig_set(
        fig, ax,
        xmaxdefine='false', ymaxdefine='false', xmindefine='false', ymindefine='false',
        xmin=0.0, xmax=70000, ymin=0.0, ymax=25000,
        wbleft=0.0, wbright=70000, wbbottom=0.0, wbtop=25000,
        leftshow='true', rightshow='true', bottomshow='true', topshow='true',
        major_locator=10000.0, minor_locator=1000.0,
        fontsize=12, linewidth=0.5, pagesize=14
    )
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

def save_triangulation_plot(coords, radii, colors, colorlist, tri, filename, filtered=False):
    fig = plt.figure(figsize=(14, 12), facecolor='white')
    ax = plt.gca()
    # 确保输入是 numpy 数组，并处理 None或空数组情况
    if coords is None or coords.shape[0] == 0:
        print(f"警告: 没有坐标数据无法绘制三角网格图到 {filename}")
        plt.close(fig)
        return
    BALLxyN2 = np.asmatrix(coords)

    if radii is None or radii.shape[0] == 0:
         # 使用默认半径或者根据coords生成同等数量的默认半径
        print(f"警告: 没有半径数据，使用默认半径绘制三角网格图到 {filename}")
        BALLRadN1 = np.asmatrix(np.full((coords.shape[0], 1), 100.0)) # 默认半径 100.0
    else:
        BALLRadN1 = np.asmatrix(radii)

    if colors is None or colors.shape[0] == 0:
        print(f"警告: 没有颜色数据，使用默认颜色 0 绘制颗粒图到 {filename}")
        BALLColorN1 = np.asmatrix(np.full((coords.shape[0], 1), 0)) # 默认颜色 0
    else:
        BALLColorN1 = np.asmatrix(colors)

    # 确保 colorlist 不是 None 或空
    if colorlist is None or len(colorlist) == 0:
        print("错误: 颜色列表为空，无法绘制三角网格图")
        plt.close(fig)
        return

    zdemplot.plot_ball(fig, ax, BALLxyN2, BALLRadN1, BALLColorN1, colorlist)
    if tri is not None and tri.triangles.shape[0] > 0: # 检查tri是否有效且有三角形
        color = 'lime'  # 过滤前后都用绿色
        ax.triplot(tri.x, tri.y, tri.triangles, color=color, linestyle='-', alpha=1.0, linewidth=0.2)
    else:
        print(f"警告: 没有有效的三角网格数据，跳过绘制三角网格到 {filename}")

    zdemplot.zdem_fig_set(
        fig, ax,
        xmaxdefine='false', ymaxdefine='false', xmindefine='false', ymindefine='false',
        xmin=0.0, xmax=70000, ymin=0.0, ymax=25000,
        wbleft=0.0, wbright=70000, wbbottom=0.0, wbtop=25000,
        leftshow='true', rightshow='true', bottomshow='true', topshow='true',
        major_locator=10000.0, minor_locator=1000.0,
        fontsize=12, linewidth=0.5, pagesize=14
    )
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_area_trend(results, plot_type='raw'):
    """绘制面积趋势曲线图"""
    if not results:
        print("没有可用于绘制面积趋势图的结果")
        return

    # 按文件名中的数字排序结果
    sorted_results = sorted(results, key=lambda x: int(''.join(filter(str.isdigit, x['file_name']))))

    # 提取文件编号和面积数据
    file_numbers = [int(''.join(filter(str.isdigit, r['file_name']))) for r in sorted_results]
    areas = [r['area'] for r in sorted_results]

    if not file_numbers or not areas:
        print("未能从结果中提取有效的绘图数据")
        return

    y_data = []
    y_label = "面积"
    title = "面积趋势图"

    # 根据plot_type处理y轴数据
    if plot_type == 'percentage':
        if len(areas) > 0 and areas[0] != 0:
            y_data = [((a - areas[0]) / areas[0]) * 100 for a in areas]
            y_label = "面积变化百分比 (%)"
            title = "面积变化百分比趋势图 (相对于第一个文件)"
        else:
            print("警告: 第一个文件的面积为零，无法计算百分比变化")
            return
    elif plot_type == 'normalized':
        if len(areas) > 0 and areas[0] != 0:
            y_data = [a / areas[0] for a in areas]
            y_label = "归一化面积 (相对于第一个文件)"
            title = "归一化面积趋势图 (相对于第一个文件)"
        else:
            print("警告: 第一个文件的面积为零，无法进行归一化")
            return
    else: # 'raw'
        y_data = areas
        y_label = "面积 (平方单位)"
        title = "原始面积趋势图"

    import matplotlib.ticker as mticker
    plt.figure(figsize=(10, 6), facecolor='white')
    plt.plot(file_numbers, y_data, marker='o', linestyle='-')
    plt.xlabel('文件编号', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)

    # 设置y轴刻度为普通数字格式（不使用科学计数法）
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')

    # 自动调整y轴范围以突出变化
    if y_data:
        if plot_type == 'raw':
            base = y_data[0]
            lower = base * 0.95
            upper = base * 1.05
            margin = base * 0.05  # 5%边距
            plt.ylim(lower - margin, upper + margin)
            # 添加±5%参考线，确保线条可见
            plt.axhline(upper, color='red', linestyle='--', linewidth=2, label='+5%', zorder=10)
            plt.axhline(lower, color='blue', linestyle='--', linewidth=2, label='-5%', zorder=10)
            plt.legend(loc='upper right', fontsize=12, frameon=True)
        else:
            ymin = min(y_data)
            ymax = max(y_data)
            y_range = ymax - ymin
            # 添加一个小的边距，例如数据范围的10%
            margin = y_range * 0.1
            if margin == 0: # 防止数据完全一样时边距为0
                 margin = abs(ymin) * 0.1 or 1.0 # 如果ymin也是0，给个默认边距1.0
            plt.ylim(ymin - margin, ymax + margin)

    plt.show()

def dat_to_particles_txt_batch(data_dir, colorlist):
    """
    批量将 data 目录下所有 .dat 文件导出为 _particles.txt
    """
    data_dir_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    if not os.path.exists(data_dir_abs):
        print(f"目录不存在: {data_dir_abs}")
        return
    for file in os.listdir(data_dir_abs):
        if file.endswith('.dat'):
            dat_file = os.path.join(data_dir_abs, file)
            try:
                result = zdemio.read_data(dat_file)
                if result is None:
                    print(f"{dat_file} 解析失败，返回None")
                    continue
                if len(result) == 5:
                    WALL, BALL, CONTACT, BOND, CurrentStep = result
                elif len(result) == 6:
                    WALL, BALL, CONTACT, BOND, CurrentStep, _ = result
                else:
                    print(f"{dat_file} 解析返回值数量异常: {len(result)}")
                    continue
                _, BALLxyN2, BALLRadN1, BALLColorN1 = zdemio.BallListStrToNumpyArray(BALL)
                export_particles_txt(BALLxyN2, BALLRadN1, BALLColorN1, dat_file)
            except Exception as e:
                print(f"处理 {dat_file} 时出错: {e}")

def main():
    # 定义变量并设置默认值
    data_dir = DEFAULT_DATA_DIR
    color_list_to_extract = COLOR_TO_EXTRACT
    threshold_factor = THRESHOLD_FACTOR
    plot_particles_flag = PLOT_PARTICLES
    plot_original_tri_flag = PLOT_ORIGINAL_TRI
    plot_filtered_tri_flag = PLOT_FILTERED_TRI
    plot_area_type = PLOT_AREA_TREND

    try:
        # 解析命令行参数
        opts, args = getopt.getopt(sys.argv[1:], "h",\
        longopts=['dir=','colors=','threshold=','plot-particles=','plot-original-tri=','plot-filtered-tri=', 'plot-area-type='])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(2)

    for op, value in opts:
        if op == "-h":
            usage(sys.argv[0])
            sys.exit()
        elif op == "--dir":
            data_dir = value
        elif op == "--colors":
            try:
                # 将逗号分隔的字符串转换为整数列表
                color_list_to_extract = [int(c.strip()) for c in value.split(',')]
            except ValueError:
                print("错误: --colors 参数需要整数列表，例如: --colors=7,8")
                usage(sys.argv[0])
                sys.exit(2)
        elif op == "--threshold":
            try:
                threshold_factor = float(value)
            except ValueError:
                print("错误: --threshold 参数需要浮点数，例如: --threshold=3.5")
                usage(sys.argv[0])
                sys.exit(2)
        elif op == "--plot-particles":
            plot_particles_flag = value.lower() == 'true'
        elif op == "--plot-original-tri":
            plot_original_tri_flag = value.lower() == 'true'
        elif op == "--plot-filtered-tri":
            plot_filtered_tri_flag = value.lower() == 'true'
        elif op == "--plot-area-type":
            if value.lower() in ['raw', 'percentage', 'normalized']:
                plot_area_type = value.lower()
            else:
                print("错误: --plot-area-type 参数只能是 'raw', 'percentage' 或 'normalized'")
                usage(sys.argv[0])
                sys.exit(2)

    # 处理多个文件前，先批量从 dat 导出 _particles.txt
    dat_to_particles_txt_batch(data_dir, color_list_to_extract)
    # 处理多个文件
    results = process_multiple_files(data_dir=data_dir, color_list=color_list_to_extract, threshold_factor=threshold_factor)

    # 比较结果
    compare_results(results)

    # 绘制面积趋势图
    plot_area_trend(results, plot_type=plot_area_type)

    # 创建保存图片的文件夹
    data_dir_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    particles_dir = os.path.join(data_dir_abs, '0_particles_plot')
    triangulation_dir = os.path.join(data_dir_abs, '1_triangulation_plot')
    filtered_triangulation_dir = os.path.join(data_dir_abs, '2_filtered_triangulation_plot')

    # 使用自定义高级灰+莫兰迪色系
    colorlist = [
        (0.36, 0.54, 0.66),  # 莫兰迪蓝
        (0.80, 0.60, 0.70),  # 莫兰迪粉
        (0.60, 0.80, 0.70),  # 莫兰迪绿
        (0.90, 0.80, 0.60),  # 莫兰迪黄
        (0.70, 0.70, 0.70),  # 高级灰
        (0.50, 0.60, 0.50),  # 莫兰迪灰绿
        (0.80, 0.70, 0.50),  # 莫兰迪棕
        (0.60, 0.60, 0.80),  # 莫兰迪紫
    ]

    for result in results:
        file_name = result.get('file_name')
        coords = result.get('coords')
        radii = result.get('radii')
        colors = result.get('colors')
        original_tri = result.get('original_tri')
        filtered_tri = result.get('tri')

        if file_name is None or coords is None or radii is None or colors is None:
            print(f"警告: 跳过文件 {file_name} 的绘图，因为数据不完整。")
            continue

        base_name = os.path.splitext(file_name)[0]
        print(f"\n正在绘制并保存 {file_name} 的图形...")

        # 颗粒分布图
        if plot_particles_flag:
            os.makedirs(particles_dir, exist_ok=True)
            particle_img = os.path.join(particles_dir, f'{base_name}_particles.jpg')
            save_particle_plot(coords, radii, colors, colorlist, particle_img)

        # 原始三角网格图
        if plot_original_tri_flag:
            os.makedirs(triangulation_dir, exist_ok=True)
            tri_img = os.path.join(triangulation_dir, f'{base_name}_triangulation.jpg')
            save_triangulation_plot(coords, radii, colors, colorlist, original_tri, tri_img, filtered=False)

        # 过滤后三角网格图
        if plot_filtered_tri_flag:
            os.makedirs(filtered_triangulation_dir, exist_ok=True)
            filtered_img = os.path.join(filtered_triangulation_dir, f'{base_name}_filtered_triangulation.jpg')
            save_triangulation_plot(coords, radii, colors, colorlist, filtered_tri, filtered_img, filtered=True)


if __name__ == "__main__":
    main()