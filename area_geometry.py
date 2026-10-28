# -*- coding: utf-8 -*-
"""Delaunay triangulation and retained-triangle area calculation."""
import warnings

import numpy as np
from matplotlib.tri import Triangulation
from scipy.spatial import Delaunay


def create_triangulation(coords):
    """创建三角网格划分"""
    if coords is None or coords.shape[0] < 3:
        print("颗粒数量不足，无法创建三角网格 (至少需要3个颗粒)。")
        return None
    if coords.shape[0] > 2:
        unique_coords = np.unique(coords, axis=0)
        if unique_coords.shape[0] < 3:
            warnings.warn("警告: 颗粒点存在大量重复或几乎共线，三角剖分可能不准确或失败。", UserWarning)
            return None
    try:
        delaunay = Delaunay(coords)
        tri = Triangulation(coords[:, 0], coords[:, 1], triangles=delaunay.simplices)
        if len(tri.triangles) == 0:
            warnings.warn("警告: 没有生成任何三角形。", UserWarning)
            return None
        return tri
    except Exception as e:
        print(f"创建三角网格时出错: {e}")
        return None

def filter_triangles(tri, coords, radii, threshold_factor):
    """过滤边长大于阈值的三角形。"""
    if tri is None or coords is None or radii is None or len(radii) == 0:
        warnings.warn("无效的输入数据，无法过滤三角形。", UserWarning)
        return None
    triangles = tri.triangles
    avg_radius = np.mean(radii)
    threshold = threshold_factor * avg_radius
    triangle_coords = coords[triangles]
    p1 = triangle_coords[:, 0, :]
    p2 = triangle_coords[:, 1, :]
    p3 = triangle_coords[:, 2, :]
    edge1 = np.linalg.norm(p1 - p2, axis=1)
    edge2 = np.linalg.norm(p2 - p3, axis=1)
    edge3 = np.linalg.norm(p3 - p1, axis=1)
    mask = (edge1 <= threshold) & (edge2 <= threshold) & (edge3 <= threshold)
    filtered_triangles = triangles[mask]
    if len(filtered_triangles) > 0:
        new_tri = Triangulation(tri.x, tri.y, filtered_triangles)
        return new_tri
    else:
        warnings.warn(f"警告: 过滤后没有剩余三角形 (阈值 = {threshold:.2f})。", UserWarning)
        return None

def calculate_triangle_areas(tri, coords):
    """计算三角形面积并求和"""
    if tri is None or coords is None or tri.triangles.shape[0] == 0:
        return 0.0
    triangles = tri.triangles
    p1 = coords[triangles[:, 0]]
    p2 = coords[triangles[:, 1]]
    p3 = coords[triangles[:, 2]]
    vec1 = p2 - p1
    vec2 = p3 - p1
    cross_product_z = vec1[:, 0] * vec2[:, 1] - vec1[:, 1] * vec2[:, 0]
    areas = 0.5 * np.abs(cross_product_z)
    total_area = np.sum(areas)
    return float(total_area)
