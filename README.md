<div align="center">

# ZDEM 颗粒分布与面积守恒分析

**Area Conservation Analysis for Z-Discrete Element Method (ZDEM) Simulations**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](setup.py)
[![Dependencies](https://img.shields.io/badge/dependencies-numpy%20%7C%20scipy%20%7C%20matplotlib-orange)](requirements.txt)

</div>

---

## 项目简介 | Overview

在 ZDEM 离散元数值模拟中，监测颗粒体系在加载过程中的面积守恒性是判断模拟物理合理性的重要指标。然而，ZDEM 原始输出为按时间步分片的 `.dat` 格式，无法直接获取颗粒覆盖面积随加载进程的变化趋势。本项目自动完成从 `.dat` 到三角网格面积分析的完整链路：批量解析 ZDEM 结果文件，通过 Delaunay 三角剖分和边长阈值过滤计算有效覆盖面积，输出面积随时间步的变化趋势图，并直观标识安全波动区间。

> In ZDEM (Z-Discrete Element Method) simulations, monitoring the area conservation of granular assemblies during loading is critical for verifying physical validity. However, raw ZDEM outputs are fragmented `.dat` files that do not directly reveal how the particle-covered area evolves over time. This project bridges the gap: it batch-processes ZDEM result files, computes the effective coverage area via Delaunay triangulation with edge-length threshold filtering, and produces trend charts with safety-band annotations.

---

## 技术特性 | Technical Highlights

| 特性 | Feature | 说明 |
|------|---------|------|
| **批量 dat 解析** | Batch .dat Parsing | 自动扫描目录下所有 ZDEM `.dat` 文件，提取颗粒坐标、半径、颜色信息 |
| **Delaunay 三角剖分** | Delaunay Triangulation | 基于 scipy.spatial 实现，支持重复点检测与异常容错 |
| **边长阈值过滤** | Edge-length Filtering | 以颗粒平均半径的倍数截断过长三角形边，消除异常跨接 |
| **面积趋势可视化** | Area Trend Visualization | 支持原始值 / 归一化 / 百分比三种模式，含安全波动区间的标注 |
| **论文规范输出** | Publication-quality Figures | 默认输出 PDF + SVG 矢量格式，符合学术期刊插图规范 |
| **命令行可配置** | CLI Configurable | 数据目录、颗粒颜色筛选、阈值因子、图表类型等全部通过参数控制 |

---

## 目录 | Table of Contents

- [数据准备](#数据准备--data-preparation)
- [算法原理](#算法原理--algorithm)
- [模块文档](#模块文档--module-reference)
- [快速开始](#快速开始--quick-start)
- [输出说明](#输出说明--output)
- [安装依赖](#安装依赖--installation)
- [项目结构](#项目结构--project-structure)
- [引用](#引用--citation)
- [许可证](#许可证--license)

---

## 数据准备 | Data Preparation

使用本工具前，请确保你的 ZDEM 模拟结果目录包含 `.dat` 格式的输出文件。建议将所有 `.dat` 文件放置在同一目录（默认 `data/`）下。程序会自动将 `.dat` 转换为 `_particles.txt` 格式的中间文件，包含每个颗粒的坐标、半径和颜色编号。

> Before using this tool, make sure your ZDEM simulation outputs are `.dat` files placed in a single directory (default: `data/`). The program automatically converts `.dat` files into `_particles.txt` intermediate files containing each particle's coordinates, radius, and color index.

---

## 算法原理 | Algorithm

面积守恒性分析的核心流程如下：

1. **颗粒筛选** — 按颜色编号（或全部）筛选待分析颗粒
2. **Delaunay 三角剖分** — 以颗粒坐标为节点生成三角网格
3. **边长过滤** — 计算颗粒平均半径 `R_avg`，设定边长阈值 `T = factor x R_avg`，剔除三边均超标的三角形
4. **面积计算** — 对剩余三角形求和，得到该时间步颗粒体系的有效覆盖面积
5. **趋势分析** — 以首步面积为基准，计算各步面积变化率（百分比），绘制趋势曲线并标记安全波动区间

> The core pipeline: (1) filter particles by color, (2) construct Delaunay triangulation, (3) remove triangles whose all three edges exceed the threshold (factor x mean radius), (4) sum the remaining triangle areas, and (5) compute relative changes against the initial timestep with safety-band visualization.

---

## 模块文档 | Module Reference

### Area_Conservation.py 主程序参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--dir` | str | `data` | 指定 .dat 文件所在目录 |
| `--colors` | str | `all` | 颗粒颜色编号（逗号分隔，或 `all` / `*` 表示全部） |
| `--threshold` | float | `3.0` | 三角网格边长阈值因子（相对于平均半径的倍数） |
| `--threshold-percent` | float | `5.0` | 面积趋势图阈值百分比 |
| `--hint-band-percent` | float | 同阈值 | 安全波动区间宽度百分比 |
| `--plot-original-tri` | bool | `true` | 是否绘制原始三角网格图 |
| `--plot-filtered-tri` | bool | `true` | 是否绘制过滤后三角网格图 |
| `--plot-area-type` | str | `raw` | 面积趋势图类型：`raw` / `percentage` / `normalized` |
| `--paper-style` | bool | `false` | 启用论文风格（加粗坐标轴、统一字号） |
| `--xmax` / `--ymax` | float | `70000` / `25000` | 绘图区域最大值 |

### 辅助模块

| 模块 | 功能 |
|------|------|
| `zdemio.py` | ZDEM `.dat` 文件读取与格式转换（含墙体、接触、粘结数据解析） |
| `zdemplot.py` | 颗粒、墙体、网格的绘制函数及坐标轴样式设置 |

---

## 快速开始 | Quick Start

```bash
# 1. 将 ZDEM .dat 文件放入 data/ 目录
# 2. 运行主分析脚本
python Area_Conservation.py

# 3. 指定颜色和阈值
python Area_Conservation.py --colors=7,8 --threshold=3.5

# 4. 论文风格输出
python Area_Conservation.py --paper-style=true --plot-area-type=percentage --threshold-percent=5.0
```

> 1. Place ZDEM `.dat` files into the `data/` directory.
> 2. Run the main analysis script.
> 3. Optionally specify color indices and threshold.
> 4. Enable paper style for publication-ready figures.

---

## 输出说明 | Output

### 控制台输出

程序执行时输出以下信息：

- 数据目录及筛选条件
- 每个文件的颗粒数量与有效覆盖面积
- 相邻时间步的面积 / 颗粒数量变化率（百分比）
- 首尾步的总体变化率

```
--- 开始处理ZDEM颗粒分布与面积守恒分析 ---
数据目录: data
提取颜色: 全部颜色
阈值因子: 3.0

=== 结果比较 ===
文件名             颗粒数量    面积(平方单位)
--------------------------------------------------
all_0000101000_particles.txt  1234    567890
all_0000102000_particles.txt  1230    567000

=== 相邻文件变化分析 ===
面积变化率: -0.16%
颗粒数量变化率: -0.32%

=== 总体变化分析 ===
面积变化率: -0.16%
颗粒数量变化率: -0.32%
```

### 图表输出

| 文件 | 格式 | 说明 |
|------|------|------|
| `data/1_triangulation_plot/*.pdf` | PDF + SVG | 原始 Delaunay 三角网格图 |
| `data/2_filtered_triangulation_plot/*.pdf` | PDF + SVG | 边长阈值过滤后的三角网格图 |
| `data/area_trend.pdf` | PDF + SVG | 面积变化趋势曲线（含安全波动区间） |

---

## 安装依赖 | Installation

```bash
pip install -r requirements.txt
```

| 依赖 | 最低版本 | 用途 |
|------|----------|------|
| numpy | >= 1.21.0 | 数值计算与矩阵运算 |
| scipy | >= 1.7.0 | Delaunay 三角剖分 |
| matplotlib | >= 3.4.0 | 数据可视化与图片输出 |

---

## 项目结构 | Project Structure

```
.
├── Area_Conservation.py     # 主分析脚本
├── main.py                  # ZDEM 原始数据批量绘图程序
├── zdemio.py                # ZDEM 数据读取与格式转换
├── zdemplot.py              # 颗粒与网格绘图函数
├── zdem_area_conservation/  # Python 包接口
│   └── __init__.py
├── data/                    # 数据目录（用户自建）
│   ├── *.dat                # ZDEM 原始结果文件
│   ├── *_particles.txt      # 自动生成的颗粒信息文件
│   ├── 1_triangulation_plot/ # 三角网格图输出
│   └── 2_filtered_triangulation_plot/ # 过滤网格图输出
├── res/
│   └── ColorRicebal.txt     # 颜色表文件
├── requirements.txt         # Python 依赖
├── setup.py                 # 安装脚本
├── LICENSE                  # MIT 许可证
└── README.md
```

---

## Docker 使用 | Docker Usage

本项目为 CLI/科学计算工具，Docker 提供便捷的构建验证环境。

```bash
docker build -t zdem-area-conservation .
docker run --rm zdem-area-conservation
```

---

## 引用 | Citation

If you use this tool in your research, please cite it as:

```bibtex
@software{zdem_area_conservation2026,
  title     = {{ZDEM Area Conservation}: Granular Coverage Analysis for Z-Discrete Element Method Simulations},
  year      = {2026},
  url       = {https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation},
  version   = {1.0.0},
  license   = {MIT}
}
```

---

## 许可证 | License

This project is open-sourced under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Made for the ZDEM research community**

</div>
