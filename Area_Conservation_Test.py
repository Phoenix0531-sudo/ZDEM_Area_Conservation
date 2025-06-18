# -*- coding: utf-8 -*-
"""
2025/05/30
包羡钧 @ 东华理工大学

功能：
计算颗粒分布的面积守恒性，批量处理ZDEM模拟的.dat文件，
生成并分析指定颜色颗粒的三角网格，输出优化前后三角网格图及面积统计。
支持命令行参数配置数据目录、颗粒颜色、网格阈值等。
"""

import os
import sys
import getopt
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from matplotlib.patches import Circle
import matplotlib.ticker as mticker
import warnings
from typing import List, Tuple, Dict, Union # 导入兼容旧Python版本的类型提示

# 导入zdemio和zdemplot模块
# 确保zdemio.py和zdemplot.py在与此脚本相同的目录下
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import zdemio
import zdemplot

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 常量定义 (将被命令行参数覆盖)
COLOR_TO_EXTRACT = [7]         # 要提取的颗粒颜色编号
THRESHOLD_FACTOR = 3.0        # 三角网格边长阈值因子
DEFAULT_DATA_DIR = "data"       # 默认数据目录
PLOT_ORIGINAL_TRI = True       # 是否绘制原始三角网格
PLOT_FILTERED_TRI = True       # 是否绘制过滤后三角网格
PLOT_AREA_TREND = 'raw'         # 面积趋势图类型: 'raw', 'percentage', 'normalized'

# 自定义颜色列表，用于绘图，覆盖get_color_map的默认读取
# 确保与zdemplot.py中的颜色索引对应
CUSTOM_COLOR_LIST = [
    (0.36, 0.54, 0.66),  # 莫兰迪蓝
    (0.80, 0.60, 0.70),  # 莫兰迪粉
    (0.60, 0.80, 0.70),  # 莫兰迪绿
    (0.90, 0.80, 0.60),  # 莫兰迪黄
    (0.70, 0.70, 0.70),  # 高级灰
    (0.50, 0.60, 0.50),  # 莫兰迪灰绿
    (0.80, 0.70, 0.50),  # 莫兰迪棕
    (0.60, 0.60, 0.80),  # 莫兰迪紫
    (1.0, 0.0, 0.0),     # 红色 (例如，对应颜色编号8，如果需要更多颜色)
    (0.0, 1.0, 0.0),     # 绿色
    (0.0, 0.0, 1.0),     # 蓝色
    (1.0, 1.0, 0.0),     # 黄色
    (1.0, 0.0, 1.0),     # 品红
    (0.0, 1.0, 1.0),     # 青色
    (0.5, 0.5, 0.5),     # 中灰
    (0.2, 0.2, 0.2),     # 深灰
    (0.9, 0.9, 0.9),     # 浅灰
]

# ===================== 辅助函数 =====================

def usage(software_name):
    """打印脚本使用说明"""
    print(f"用法: python {software_name} [选项]")
    print("  --dir=<目录>           指定包含 .dat 文件的目录 (默认: data)")
    print("  --colors=<颜色编号,...>  指定要提取的颗粒颜色编号 (逗号分隔, 默认: 7)")
    print("  --threshold=<浮点数>     指定边长阈值因子 (默认: 3.0)")
    # print("  --plot-particles=<true|false> 是否绘制颗粒分布图 (默认: true)")  # 已移除
    print("  --plot-original-tri=<true|false> 是否绘制原始三角网格图 (默认: true)")
    print("  --plot-filtered-tri=<true|false> 是否绘制过滤后三角网格图 (默认: true)")
    print("  --plot-area-type=<raw|percentage|normalized> 面积趋势图类型 (默认: raw)")
    print("  -h                     显示此帮助信息")

def read_surface_particles(filename):
    """从_particles.txt文件中读取颗粒信息"""
    particles_data = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # 跳过前3行（标题和分隔线）
            if len(lines) < 4: # 确保文件至少有标题、分隔线和一行数据
                warnings.warn(f"文件 '{filename}' 内容不足，无法解析颗粒数据。", UserWarning)
                return None, None, None

            for line in lines[3:]:
                if line.strip().startswith('-'):  # 遇到分隔线结束读取
                    break
                
                parts = line.strip().split('\t')
                if len(parts) >= 5: # 确保至少有 序号 X Y 半径 颜色编号
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        radius = float(parts[3])
                        color = int(float(parts[4])) # 确保颜色是整数
                        
                        particles_data.append((x, y, radius, color))
                    except ValueError:
                        warnings.warn(f"跳过文件 '{filename}' 中格式错误的行: {line.strip()}", UserWarning)
                        continue
        
        if not particles_data:
            warnings.warn(f"在 '{filename}' 中没有找到有效的颗粒数据。", UserWarning)
            return None, None, None
        
        # 提取坐标、半径和颜色
        coords = np.array([[p[0], p[1]] for p in particles_data], dtype=np.float32)
        radii = np.array([[p[2]] for p in particles_data], dtype=np.float32)
        
        # 关键修正：将颜色数组重塑为 (N, 1) 以兼容 zdemplot.plot_ball 内部的 c[0,0] 索引
        colors = np.array([[p[3]] for p in particles_data], dtype=np.int32)  # (N,1)

        print(f"从 '{filename}' 中读取了 {len(particles_data)} 个颗粒。")
        return coords, radii, colors
    
    except FileNotFoundError:
        print(f"错误: 文件 '{filename}' 未找到。")
        return None, None, None
    except Exception as e:
        print(f"读取文件 '{filename}' 时发生未知错误: {e}")
        return None, None, None

def create_triangulation(coords):
    """创建三角网格划分"""
    if coords is None or coords.shape[0] < 3:
        print("颗粒数量不足，无法创建三角网格 (至少需要3个颗粒)。")
        return None
    
    # 检查点是否共线或重复
    if coords.shape[0] > 2:
        unique_coords = np.unique(coords, axis=0)
        if unique_coords.shape[0] < 3:
            warnings.warn("警告: 颗粒点存在大量重复或几乎共线，三角剖分可能不准确或失败。", UserWarning)
            return None
    
    try:
        tri = Triangulation(coords[:, 0], coords[:, 1])
        
        # 检查三角形数量
        if len(tri.triangles) == 0:
            warnings.warn("警告: 没有生成任何三角形。", UserWarning)
            return None
            
        print(f"成功创建三角网格，共有 {len(tri.triangles)} 个三角形。")
        return tri
    except Exception as e:
        print(f"创建三角网格时出错: {e}")
        return None

def filter_triangles(tri, coords, radii, threshold_factor):
    """
    过滤边长大于阈值的三角形。
    阈值 = threshold_factor * 平均颗粒半径。
    """
    if tri is None or coords is None or radii is None or len(radii) == 0:
        warnings.warn("无效的输入数据，无法过滤三角形。", UserWarning)
        return None
    
    triangles = tri.triangles
    
    avg_radius = np.mean(radii)
    threshold = threshold_factor * avg_radius
    
    # 获取三角形的顶点坐标
    triangle_coords = coords[triangles] # 形状: (num_triangles, 3, 2)
    
    # 向量化计算所有三角形的边长
    p1 = triangle_coords[:, 0, :]
    p2 = triangle_coords[:, 1, :]
    p3 = triangle_coords[:, 2, :]

    edge1 = np.linalg.norm(p1 - p2, axis=1)
    edge2 = np.linalg.norm(p2 - p3, axis=1)
    edge3 = np.linalg.norm(p3 - p1, axis=1)
    
    # 判断哪些三角形的所有边长都小于阈值
    mask = (edge1 <= threshold) & (edge2 <= threshold) & (edge3 <= threshold)
    
    filtered_triangles = triangles[mask]
    
    if len(filtered_triangles) > 0:
        new_tri = Triangulation(tri.x, tri.y, filtered_triangles)
        print(f"过滤后剩余 {len(filtered_triangles)} 个三角形 (阈值 = {threshold:.2f})。")
        return new_tri
    else:
        warnings.warn(f"警告: 过滤后没有剩余三角形 (阈值 = {threshold:.2f})。", UserWarning)
        return None

def calculate_triangle_areas(tri, coords):
    """计算三角形面积并求和"""
    if tri is None or coords is None or tri.triangles.shape[0] == 0:
        return 0.0
    
    triangles = tri.triangles
    
    # 向量化计算面积
    p1 = coords[triangles[:, 0]]
    p2 = coords[triangles[:, 1]]
    p3 = coords[triangles[:, 2]]

    # 使用叉积的模长计算面积 (适用于2D，扩展到3D再取Z分量)
    # 向量 (p2-p1) 和 (p3-p1)
    vec1 = p2 - p1
    vec2 = p3 - p1
    
    # 2D叉积的Z分量 = x1*y2 - x2*y1
    cross_product_z = vec1[:, 0] * vec2[:, 1] - vec1[:, 1] * vec2[:, 0]
    
    areas = 0.5 * np.abs(cross_product_z)
    total_area = np.sum(areas)
    
    return float(total_area) # 确保返回的是float

def export_particles_txt(coords, radii, colors, original_dat_file_path):
    """
    根据原始 dat 文件名，在 data 目录下生成对应的 _particles.txt 文件
    """
    if coords is None or radii is None or colors is None or coords.shape[0] == 0:
        warnings.warn(f"没有有效的颗粒数据可供导出到文本文件。", UserWarning)
        return
    if not original_dat_file_path:
        warnings.warn(f"未提供原始 .dat 文件路径，无法确定输出文件名。", UserWarning)
        return

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    
    # 从完整路径中提取文件名并去除扩展名
    base_name = os.path.splitext(os.path.basename(original_dat_file_path))[0]
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
                color = int(colors[i, 0])  # 只用[i,0]
                f.write(f"{i}\t{x:.2f}\t{y:.2f}\t{radius:.2f}\t{color}\n")
            
            f.write("-" * 50 + "\n")
            f.write(f"表面颗粒总数: {coords.shape[0]}\n")
        print(f"颗粒信息已保存到 '{output_file}'。")
    except Exception as e:
        print(f"写入文件 '{output_file}' 失败: {e}")

def dat_to_particles_txt_batch(data_dir):
    """
    批量将指定 data 目录下的所有 .dat 文件导出为 _particles.txt
    """
    data_dir_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    if not os.path.exists(data_dir_abs):
        warnings.warn(f"目录不存在: '{data_dir_abs}'。跳过 .dat 文件转换。", UserWarning)
        return

    dat_files = [f for f in os.listdir(data_dir_abs) if f.endswith('.dat')]
    if not dat_files:
        print(f"在 '{data_dir_abs}' 中没有找到任何 .dat 文件。")
        return

    for file_name in sorted(dat_files): # 排序以确保顺序
        dat_file_path = os.path.join(data_dir_abs, file_name)
        print(f"正在处理 .dat 文件: '{file_name}' 进行颗粒数据提取...")
        try:
            result = zdemio.read_data(dat_file_path)
            if result is None:
                warnings.warn(f"'{file_name}' 解析失败，zdemio.read_data 返回 None。", UserWarning)
                continue
            
            # 根据返回结果的长度，安全解包
            if len(result) == 5:
                _WALL, BALL, _CONTACT, _BOND, _CurrentStep = result
            elif len(result) == 6:
                _WALL, BALL, _CONTACT, _BOND, _CurrentStep, _ = result
            else:
                warnings.warn(f"'{file_name}' 解析返回值数量异常: {len(result)}。跳过。", UserWarning)
                continue
            
            # 使用 zdemio.BallListStrToNumpyArray 转换颗粒数据
            _, BALLxyN2_raw, BALLRadN1_raw, BALLColorN1_raw = zdemio.BallListStrToNumpyArray(BALL)

            # 调整颜色数组形状以兼容 zdemplot 的 c[0,0] 索引
            # 原始的 BALLColorN1_raw 可能是 (N, 1) 或 (N,)
            # 我们需要它在 zdemplot.plot_ball 循环时，c 是 (1,1) 形状，从而 c[0,0] 有效
            BALLColorN1_reshaped = BALLColorN1_raw.reshape(-1, 1)  # (N,1)

            export_particles_txt(BALLxyN2_raw, BALLRadN1_raw, BALLColorN1_reshaped, dat_file_path)
        except Exception as e:
            print(f"处理 '{file_name}' 时出错: {e}")

def process_multiple_files(data_dir, color_list, threshold_factor):
    """处理data目录下的所有_particles.txt文件，进行分析和绘图"""
    results = []
    
    data_dir_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    if not os.path.exists(data_dir_abs):
        print(f"错误: 目录 '{data_dir_abs}' 不存在。")
        return results
    
    particle_files = [f for f in os.listdir(data_dir_abs) if f.endswith('_particles.txt')]
    if not particle_files:
        warnings.warn(f"在 '{data_dir_abs}' 中没有找到任何 _particles.txt 文件。", UserWarning)
        return results
    
    # 按文件名中的数字排序，假设文件名格式为 "xxx_N.dat_particles.txt"
    particle_files.sort(key=lambda f: int(re.findall(r'\d+', f)[-1]) if re.findall(r'\d+', f) else 0)
    
    for file_name in particle_files:
        file_path = os.path.join(data_dir_abs, file_name)
        print(f"\n--- 正在处理文件: '{file_name}' ---")
        
        coords, radii, colors = read_surface_particles(file_path)
        
        if coords is None or radii is None or colors is None:
            warnings.warn(f"文件 '{file_name}' 缺少有效的颗粒数据，跳过该文件。", UserWarning)
            continue
        
        # 筛选指定颜色的颗粒
        # colors 数组现在是 (N, 1)，所以访问颜色值需要 colors[i, 0]
        color_indices = [i for i in range(colors.shape[0]) if colors[i, 0] in color_list]
        
        if not color_indices:
            print(f"在 '{file_name}' 中没有找到颜色为 {color_list} 的颗粒，跳过该文件。")
            continue
        
        filtered_coords = coords[color_indices]
        filtered_radii = radii[color_indices]
        filtered_colors = colors[color_indices]
        print(f"从 '{file_name}' 中筛选出 {len(color_indices)} 个颜色为 {color_list} 的颗粒。")
        
        if filtered_coords.shape[0] < 3: # 至少3个点才能三角化
            warnings.warn(f"筛选后的颗粒数量不足3个 ({filtered_coords.shape[0]}个)，无法进行三角剖分，跳过文件 '{file_name}'。", UserWarning)
            continue

        original_tri = create_triangulation(filtered_coords)
        
        if original_tri is not None:
            filtered_tri = filter_triangles(original_tri, filtered_coords, filtered_radii, threshold_factor)
            
            if filtered_tri is not None:
                total_area = calculate_triangle_areas(filtered_tri, filtered_coords)
                
                results.append({
                    'file_name': file_name,
                    'total_particles': filtered_coords.shape[0],
                    'area': total_area,
                    'coords': filtered_coords,
                    'radii': filtered_radii,
                    'colors': filtered_colors,
                    'original_tri': original_tri,
                    'tri': filtered_tri # 过滤后的三角网格
                })
                print(f"文件 '{file_name}' 总面积: {total_area:.2f} 平方单位。")
    
    return results

def compare_results(results):
    """比较不同文件的颗粒数量和面积结果"""
    if not results:
        print("没有可比较的结果。")
        return
    
    print("\n=== 结果比较 ===")
    print("文件名\t\t颗粒数量\t面积(平方单位)")
    print("-" * 50)
    
    # 再次排序以防万一，确保输出顺序正确
    sorted_results = sorted(results, key=lambda x: int(re.findall(r'\d+', x['file_name'])[-1]) if re.findall(r'\d+', x['file_name']) else 0)
    
    for result in sorted_results:
        # 将面积精度调整为千位显示，但实际数值保持浮点数
        rounded_area_display = round(result['area'], -3) if result['area'] >= 1000 else result['area']
        print(f"{result['file_name']}\t{result['total_particles']}\t{rounded_area_display:.0f}") # 显示为整数

    print("\n=== 相邻文件变化分析 ===")
    for i in range(1, len(sorted_results)):
        prev_result = sorted_results[i-1]
        curr_result = sorted_results[i]
        
        prev_area = prev_result['area']
        curr_area = curr_result['area']
        area_change = ((curr_area - prev_area) / prev_area) * 100 if prev_area != 0 else float('inf')
        
        prev_particles = prev_result['total_particles']
        curr_particles = curr_result['total_particles']
        particle_change = ((curr_particles - prev_particles) / prev_particles) * 100 if prev_particles != 0 else float('inf')
        
        print(f"\n从 '{prev_result['file_name']}' 到 '{curr_result['file_name']}':")
        print(f"面积变化率: {area_change:+.2f}%")
        print(f"颗粒数量变化率: {particle_change:+.2f}%")
    
    if len(sorted_results) >= 2:
        first_area = sorted_results[0]['area']
        last_area = sorted_results[-1]['area']
        area_change_overall = ((last_area - first_area) / first_area) * 100 if first_area != 0 else float('inf')
        
        first_particles = sorted_results[0]['total_particles']
        last_particles = sorted_results[-1]['total_particles']
        particle_change_overall = ((last_particles - first_particles) / first_particles) * 100 if first_particles != 0 else float('inf')

        print("\n=== 总体变化分析 ===")
        print(f"从 '{sorted_results[0]['file_name']}' 到 '{sorted_results[-1]['file_name']}'")
        print(f"面积变化率: {area_change_overall:+.2f}%")
        print(f"颗粒数量变化率: {particle_change_overall:+.2f}%")

def save_particle_plot(coords, radii, colors, color_list, filename):
    """保存颗粒分布图"""
    # 此函数已根据用户要求不再调用，但保留其定义以防未来需要
    warnings.warn("警告: save_particle_plot 函数已根据用户要求不再调用，此图不会生成。", UserWarning)
    if coords is None or coords.shape[0] == 0:
        warnings.warn(f"没有坐标数据，无法绘制颗粒图到 '{filename}'。", UserWarning)
        return

    fig, ax = plt.subplots(figsize=(14, 12), facecolor='white')
    ax.set_facecolor('white')

    # 这里我们直接传递 read_surface_particles 返回的已经重塑为 (N, 1) 的 colors 数组
    zdemplot.plot_ball(fig, ax, coords, radii, colors, color_list)
    
    # 绘图区域设置，确保与 main.py 输出一致，强制定义边界
    zdemplot.zdem_fig_set(
        fig, ax,
        xmaxdefine='true', ymaxdefine='true', xmindefine='true', ymindefine='true', # 强制使用xmin/xmax/ymin/ymax
        xmin=0.0, xmax=70000.0, ymin=0.0, ymax=25000.0,
        wbleft=0.0, wbright=70000.0, wbbottom=0.0, wbtop=25000.0,
        leftshow='true', rightshow='true', bottomshow='true', topshow='true',
        major_locator=10000.0, minor_locator=1000.0,
        fontsize=12, linewidth=0.5, pagesize=14
    )
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"颗粒分布图已保存到 '{filename}'。")

def save_triangulation_plot(coords, radii, colors, color_list, tri, filename, filtered=False):
    """保存三角网格图（叠加颗粒）"""
    if coords is None or coords.shape[0] == 0:
        warnings.warn(f"没有坐标数据，无法绘制三角网格图到 '{filename}'。", UserWarning)
        return

    fig, ax = plt.subplots(figsize=(14, 12), facecolor='white')
    ax.set_facecolor('white')

    # 绘制颗粒
    zdemplot.plot_ball(fig, ax, coords, radii, colors, color_list)
    
    # 绘制三角网格
    if tri is not None and tri.triangles.shape[0] > 0:
        color = 'lime' if not filtered else 'red' # 过滤前绿色，过滤后红色
        ax.triplot(tri.x, tri.y, tri.triangles, color=color, linestyle='-', alpha=1.0, linewidth=0.2)
    else:
        warnings.warn(f"没有有效的三角网格数据，跳过绘制网格线到 '{filename}'。", UserWarning)

    # 绘图区域设置，确保与 main.py 输出一致，强制定义边界
    zdemplot.zdem_fig_set(
        fig, ax,
        xmaxdefine='true', ymaxdefine='true', xmindefine='true', ymindefine='true', # 强制使用xmin/xmax/ymin/ymax
        xmin=0.0, xmax=70000.0, ymin=0.0, ymax=25000.0,
        wbleft=0.0, wbright=70000.0, wbbottom=0.0, wbtop=25000.0,
        leftshow='true', rightshow='true', bottomshow='true', topshow='true',
        major_locator=10000.0, minor_locator=1000.0,
        fontsize=12, linewidth=0.5, pagesize=14
    )
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"{'过滤后' if filtered else '原始'}三角网格图已保存到 '{filename}'。")


def plot_area_trend(results, plot_type='raw'):
    """绘制面积趋势曲线图，并自动保存到 data 目录下"""
    if not results:
        print("没有可用于绘制面积趋势图的结果。")
        return

    # 按文件名中的数字排序结果
    sorted_results = sorted(results, key=lambda x: int(re.findall(r'\d+', x['file_name'])[-1]) if re.findall(r'\d+', x['file_name']) else 0)

    file_numbers = [int(re.findall(r'\d+', r['file_name'])[-1]) for r in sorted_results if re.findall(r'\d+', r['file_name'])]
    areas = [r['area'] for r in sorted_results if re.findall(r'\d+', r['file_name'])]

    if not file_numbers or not areas:
        warnings.warn("未能从结果中提取有效的绘图数据，无法绘制面积趋势图。", UserWarning)
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
            warnings.warn("警告: 第一个文件的面积为零，无法计算百分比变化。", UserWarning)
            return
    elif plot_type == 'normalized':
        if len(areas) > 0 and areas[0] != 0:
            y_data = [a / areas[0] for a in areas]
            y_label = "归一化面积 (相对于第一个文件)"
            title = "归一化面积趋势图 (相对于第一个文件)"
        else:
            warnings.warn("警告: 第一个文件的面积为零，无法进行归一化。", UserWarning)
            return
    else: # 'raw'
        y_data = areas
        y_label = "面积 (平方单位)"
        title = "原始面积趋势图"

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.plot(file_numbers, y_data, marker='o', linestyle='-', color='blue', linewidth=2)
    ax.set_xlabel('文件编号', fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)

    # 设置y轴刻度为普通数字格式（不使用科学计数法）
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')

    # 自动调整y轴范围以突出变化
    if y_data:
        # 添加一个小的边距，例如数据范围的10%
        ymin_val, ymax_val = np.min(y_data), np.max(y_data)
        y_range = ymax_val - ymin_val
        margin = y_range * 0.1
        if margin == 0: # 防止数据完全一样时边距为0
            margin = abs(ymin_val) * 0.1 or 1.0 # 如果ymin也是0，给个默认边距1.0
        ax.set_ylim(ymin_val - margin, ymax_val + margin)

        if plot_type == 'raw' and len(y_data) > 0 and y_data[0] != 0:
            # 添加±5%参考线，以第一个点的面积为基准
            base_area = y_data[0]
            upper_bound = base_area * 1.05
            lower_bound = base_area * 0.95
            
            # 仅在合理范围内绘制参考线，避免线跑到图外很远
            if lower_bound < ymax_val + margin and upper_bound > ymin_val - margin:
                ax.axhline(upper_bound, color='red', linestyle=':', linewidth=1.5, label='+5% 波动', zorder=10)
                ax.axhline(lower_bound, color='green', linestyle=':', linewidth=1.5, label='-5% 波动', zorder=10)
                ax.legend(loc='upper right', fontsize=10, frameon=True)
            elif lower_bound > ymax_val + margin: # 如果下限远高于图上限
                ax.axhline(upper_bound, color='red', linestyle=':', linewidth=1.5, label='+5% 波动', zorder=10)
            elif upper_bound < ymin_val - margin: # 如果上限远低于图下限
                ax.axhline(lower_bound, color='green', linestyle=':', linewidth=1.5, label='-5% 波动', zorder=10)

    # 自动保存到 data 目录下
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    save_path = os.path.join(data_dir, 'area_trend.jpg')
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"面积趋势图已保存到: {save_path}")

# ===================== 主流程 =====================

def main():
    # 定义变量并设置默认值
    data_dir = DEFAULT_DATA_DIR
    color_list_to_extract = COLOR_TO_EXTRACT
    threshold_factor = THRESHOLD_FACTOR
    plot_original_tri_flag = PLOT_ORIGINAL_TRI
    plot_filtered_tri_flag = PLOT_FILTERED_TRI
    plot_area_type = PLOT_AREA_TREND

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h",\
        longopts=['dir=','colors=','threshold=','plot-original-tri=','plot-filtered-tri=', 'plot-area-type='])
    except getopt.GetoptError as err:
        print(f"命令行参数错误: {err}")
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
                color_list_to_extract = [int(c.strip()) for c in value.split(',')]
            except ValueError:
                print("错误: --colors 参数需要整数列表，例如: --colors=7,8。")
                usage(sys.argv[0])
                sys.exit(2)
        elif op == "--threshold":
            try:
                threshold_factor = float(value)
            except ValueError:
                print("错误: --threshold 参数需要浮点数，例如: --threshold=3.5。")
                usage(sys.argv[0])
                sys.exit(2)
        elif op == "--plot-original-tri":
            plot_original_tri_flag = value.lower() == 'true'
        elif op == "--plot-filtered-tri":
            plot_filtered_tri_flag = value.lower() == 'true'
        elif op == "--plot-area-type":
            if value.lower() in ['raw', 'percentage', 'normalized']:
                plot_area_type = value.lower()
            else:
                print("错误: --plot-area-type 参数只能是 'raw', 'percentage' 或 'normalized'。")
                usage(sys.argv[0])
                sys.exit(2)

    print("--- 开始处理ZDEM颗粒分布与面积守恒分析 ---")
    print(f"数据目录: {data_dir}")
    print(f"提取颜色: {color_list_to_extract}")
    print(f"阈值因子: {threshold_factor}")

    # 1. 批量将 .dat 文件导出为 _particles.txt 文件
    dat_to_particles_txt_batch(data_dir)
    
    # 2. 处理 _particles.txt 文件，进行颗粒筛选、三角剖分和面积计算
    results = process_multiple_files(data_dir=data_dir, color_list=color_list_to_extract, threshold_factor=threshold_factor)
    
    # 3. 比较和分析结果
    compare_results(results)
    
    # 4. 绘制面积趋势图
    plot_area_trend(results, plot_type=plot_area_type)

    # 5. 保存各种图片
    data_dir_abs = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
    # 颗粒分布图目录不再需要，但为了兼容性，可以保留定义，只是不再调用save_particle_plot
    # particles_dir = os.path.join(data_dir_abs, '0_particles_plot') 
    triangulation_dir = os.path.join(data_dir_abs, '1_triangulation_plot')
    filtered_triangulation_dir = os.path.join(data_dir_abs, '2_filtered_triangulation_plot')

    # 使用自定义的颜色列表 (CUSTOM_COLOR_LIST) 传递给绘图函数
    drawing_color_list = CUSTOM_COLOR_LIST
    
    if not results:
        warnings.warn("没有可用于绘图的结果，跳过图片保存。", UserWarning)
        return

    for result in results:
        file_name = result.get('file_name')
        coords = result.get('coords')
        radii = result.get('radii')
        colors = result.get('colors')
        original_tri = result.get('original_tri')
        filtered_tri = result.get('tri')

        # 关键修正：保证 colors 是 (N,1,1)，这样 for c in colors 时 c[0,0] 有效
        if colors is not None:
            colors = np.array(colors)
            if len(colors.shape) == 1:
                colors = colors.reshape(-1, 1, 1)
            elif len(colors.shape) == 2:
                colors = colors.reshape(-1, 1, 1)
            elif len(colors.shape) > 3:
                colors = colors.reshape(-1, 1, 1)
        print(f"DEBUG: {file_name} colors.shape = {None if colors is None else colors.shape}")

        if file_name is None or coords is None or radii is None or colors is None:
            warnings.warn(f"跳过文件 '{file_name}' 的绘图，因为数据不完整。", UserWarning)
            continue
        
        base_name = os.path.splitext(file_name)[0]
        print(f"\n正在绘制并保存 '{file_name}' 的图形...")
        
        # 原始三角网格图
        if plot_original_tri_flag:
            os.makedirs(triangulation_dir, exist_ok=True)
            tri_img = os.path.join(triangulation_dir, f'{base_name}_triangulation.jpg')
            save_triangulation_plot(coords, radii, colors, drawing_color_list, original_tri, tri_img, filtered=False)
        
        # 过滤后三角网格图
        if plot_filtered_tri_flag:
            os.makedirs(filtered_triangulation_dir, exist_ok=True)
            filtered_img = os.path.join(filtered_triangulation_dir, f'{base_name}_filtered_triangulation.jpg')
            save_triangulation_plot(coords, radii, colors, drawing_color_list, filtered_tri, filtered_img, filtered=True)

    print("--- ZDEM颗粒分布与面积守恒分析完成 ---")

if __name__ == "__main__":
    main()
