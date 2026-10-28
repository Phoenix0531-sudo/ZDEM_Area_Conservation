# ZDEM Area Conservation

用于二维 ZDEM 模拟颗粒子集面积估算的 Python 工具：对指定颜色颗粒进行 Delaunay 三角剖分，过滤长边三角形，并比较不同模拟帧的面积。

[English](README.md) · [许可证](LICENSE)

![示例图](docs/screenshots/preview.png)

## 方法

程序从每个 ZDEM `.dat` 文件中提取颗粒坐标、半径和颜色编号，按颜色筛选颗粒（默认全部颜色），再进行 Delaunay 三角剖分。仅保留三条边长度均不超过 `k × 颗粒平均半径` 的三角形，并将保留三角形的面积求和；默认阈值因子 `k = 3.0`。

对于选中颗粒的中心 $p_i$ 和半径 $r_i$，记平均半径为 $\bar r$，满足每条边长均不超过 $k\bar r$ 的 Delaunay 三角形集合为 $T_k$，则估算面积为 $A_k = \sum_{t\in T_k} \operatorname{area}(t)$。该值是保留三角形的面积之和，**不是颗粒圆盘面积之和**；改变阈值或筛选颜色可能改变结果。

程序按文件名中的数字排序比较各帧面积。趋势图横轴为归一化的文件编号；百分比模式以首个有效帧面积为基准，显示相对变化。该方法是数值模拟的后处理，**不能单独作为物理实测或面积守恒已经成立的证明**；坐标单位、输入来源和参数适用性需根据具体数据确认。

## 环境与安装

需要 Python 3.10 或更高版本。运行依赖为 NumPy、SciPy 和 Matplotlib；`requirements.txt` 还包含测试用的 pytest。

```bash
python -m pip install -r requirements.txt
python Area_Conservation.py -h
```

## 数据与运行

- `samples/` 是两帧用于测试的**人工构造迷你样例**，不是实验数据，详见 [samples/README.md](samples/README.md)。
- `data/` 不纳入 Git，可保存本地模拟数据和输出；运行前请另行保留原始数据。

将兼容的 `.dat` 文件放入项目根目录的 `data/`，例如：

```bash
python Area_Conservation.py --dir=data --colors=all --threshold=3.0 --plot-area-type=percentage
```

`--colors=7,8` 可筛选颜色编号，`--xmax`、`--ymax` 可调整网格图坐标范围，`--plot-area-type=raw|percentage|normalized` 可选择面积趋势显示方式。其他选项见 `python Area_Conservation.py -h`。默认绘图范围和单位标注应根据实际数据核实后再用于发表。

**输出与注意事项：**颗粒文本文件（`*_particles.txt`）及 `area_trend.pdf`、`.svg` 写入项目根目录的 `data/`；原始和过滤后三角网的 PDF、SVG 写入所选输入目录。同名文件可能被覆盖。当前实现即使指定其他 `--dir`，仍会将颗粒中间文件和趋势图写入根目录 `data/`，但从所选输入目录读取颗粒文本。因此，在该路径问题修复前，完整流程应使用默认 `data/`；直接对 `samples/` 或其他目录运行不能作为可靠的端到端示例。程序在终端输出颗粒数量及面积比较，默认不导出面积汇总表。

## 测试与复现

```bash
python -m pytest -q tests
```

现有测试覆盖样例解析、辅助函数和基础导入，不代表已验证特定模拟的科学准确性。为便于复现，应记录源数据、模拟工况、坐标单位、筛选颜色、阈值因子、绘图设置、Python 与依赖版本，以及仓库版本（`git rev-parse HEAD`）。程序目前不会自动导出这些设置或面积汇总表。完整本地模拟数据未包含在仓库中，因此仅凭合成样例不能复现基于这些数据获得的结果。

## 目录结构

| 路径 | 用途 |
| --- | --- |
| `Area_Conservation.py` | 面积分析与绘图入口 |
| `zdemio.py`、`zdemplot.py` | ZDEM 数据解析和绘图辅助模块 |
| `samples/`、`tests/` | 合成样例和自动化测试 |
| `data/` | 本地模拟数据与输出，不纳入 Git |

## 引用与许可

本仓库目前没有确定的论文或引用元数据。用于研究时，请在相关论文可用后引用论文，并记录所使用的仓库版本。代码采用 [MIT 许可证](LICENSE)。
