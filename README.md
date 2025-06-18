# ZDEM 颗粒分布与面积守恒分析

开发者：包羡钧

本项目用于分析 ZDEM 模拟中颗粒分布的面积守恒性，支持批量处理、统计分析和可视化。适用于颗粒体系的时序演化、面积变化率分析等科学研究场景。

---

## 主要功能

1. **dat文件批量处理**  
   - 自动将`data`目录下所有`.dat`文件转换为与`surface_particles.txt`格式一致的`_particles.txt`颗粒信息文件。
   - 支持自定义颗粒颜色筛选，便于后续分析。

2. **颗粒分布与面积守恒分析**  
   - 批量读取`_particles.txt`文件，筛选指定颜色颗粒，自动进行三角剖分与面积计算。
   - 输出每个文件的颗粒数量、面积、相邻文件的面积/数量变化率，以及首尾文件的总体变化率。

3. **可视化与图片自动保存**  
   - 每个时间步自动生成三类图片：颗粒分布图、原始三角网格图、过滤后三角网格图。
   - 图片风格与主程序一致，自动保存到`data/0_particles_plot`、`data/1_triangulation_plot`、`data/2_filtered_triangulation_plot`目录。

4. **参数灵活配置**  
   - 支持命令行参数自定义数据目录、颗粒颜色、三角网格边长阈值、图片类型等。
   - 兼容多种数据格式和色表，支持自定义色表文件。

5. **健壮性与易用性**  
   - 完善的异常处理，自动跳过无效数据，输出详细警告和错误提示。
   - 代码结构清晰，注释详细，便于维护和扩展。

---

## 环境要求

```bash
pip install numpy
pip install matplotlib
```

---

## 目录结构

- `Area_Conservation_Test.py`: 主程序文件
  * 实现面积守恒性测试的核心功能
  * 包含颗粒数据读取、三角网格生成、面积计算等功能
  * 提供可视化接口和结果分析功能

- `zdemplot.py`: 绘图相关函数
- `data/`: 存放 ZDEM 模拟结果数据的目录
  * 存放原始 dat 文件
  * 存放生成的 particles.txt 文件
  * 存放输出的 jpg 图片文件
.
├── Area_Conservation_Test.py # 主分析与可视化脚本
├── main.py # ZDEM原始数据批量绘图主程序
├── zdemplot.py # 颗粒与网格绘图函数
├── zdemio.py # ZDEM数据读取与格式转换
├── data/
│ ├── .dat # ZDEM原始数据文件
│ ├── _particles.txt # 自动生成的颗粒信息文件
│ ├── 0_particles_plot/ # 颗粒分布图片
│ ├── 1_triangulation_plot/ # 原始三角网格图片
│ └── 2_filtered_triangulation_plot/ # 过滤后三角网格图片
└── README.md
```

---

## 快速开始

1. **准备数据**  
   将所有`.dat`文件放入`data`文件夹。

2. **批量生成颗粒信息文件**  
   运行主分析脚本，会自动批量生成`_particles.txt`文件：
   ```bash
   python Area_Conservation_Test.py
   ```

3. **参数说明（可选）**  
   支持如下命令行参数：
   ```
   --dir=<目录>           指定数据目录（默认：data）
   --colors=<编号,...>    指定颗粒颜色编号（如7,8）
   --threshold=<浮点数>   三角网格边长阈值因子（默认3.0）
   --plot-particles=<true|false> 是否绘制颗粒分布图
   --plot-original-tri=<true|false> 是否绘制原始三角网格图
   --plot-filtered-tri=<true|false> 是否绘制过滤后三角网格图
   --plot-area-type=<raw|percentage|normalized> 面积趋势图类型
   -h                     显示帮助
   ```

4. **输出内容**  
   - 每个时间步的颗粒数量、面积
   - 相邻时间步的面积/数量变化率
   - 首尾文件的总体变化率
   - 三类图片自动保存到对应目录

---

## 主要文件说明

- `Area_Conservation_Test.py`  
  * 主分析与可视化脚本，支持批量处理、面积统计、趋势分析和图片自动保存。
- `main.py`  
  * ZDEM原始数据批量绘图主程序，支持多线程并行处理。
- `zdemplot.py`  
  * 颗粒、墙体、网格等绘图函数，支持自定义色表和风格。
- `zdemio.py`  
  * ZDEM数据读取、格式转换、色表管理等底层工具函数。

---

## 常见问题与报错说明

- 色表文件缺失：请确保`res/ColorRicebal.txt`存在或指定自定义色表。
- 类型不匹配、None下标访问：已在主程序中做了健壮性处理，遇到警告可检查数据完整性。
- 图片风格不统一：所有图片均调用`zdemplot.plot_ball`，风格与主程序一致。
- 其他问题请查阅代码注释或联系开发者。

---

## 更新日志

- 支持dat文件自动批量转换为颗粒信息txt
- 批量面积分析与趋势可视化
- 图片自动保存与风格统一
- 代码结构优化与详细注释

---

如需扩展功能或有其他需求，欢迎在本项目基础上继续开发！