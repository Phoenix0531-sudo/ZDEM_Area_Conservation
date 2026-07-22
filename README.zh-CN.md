# ZDEM Area Conservation

**面向 ZDEM 颜色组的面积守恒 / 三角网格分析**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

对 ZDEM 颗粒包做**面积守恒**检查的批处理工具：读 `.dat` 帧（`zdemio`），对选定 **color#** 建三角网、出图并汇总面积趋势。

`data/`、`data1/`、`figures/` 下的完整实验数据**仅本地**（已 ignore）。CI 使用 `samples/` 中的合成小帧。

## 为什么做这个

盐构造 / 颗粒论文需要证明跟踪区域在变形下面积守恒。自动化三角剖分与统计优于零散旧脚本。

## 功能

- `Area_Conservation.py` — 主分析入口（getopt）  
- `zdemio` / `zdemplot`  
- 论文向 `fig*.py`  
- `samples/` 供测试的小 `.dat`  

## 安装

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation.git
cd ZDEM_Area_Conservation
pip install -r requirements.txt
```

## 使用

```bash
python Area_Conservation.py --help
```

```bash
pytest tests/test_samples_dat.py tests/test_zdemio.py
```

## 数据策略

| 路径 | 是否进 git |
|------|------------|
| `samples/` | 是（合成小样） |
| `data/`、`data1/`、`figures/` | 否，仅本地 |

## 相关 ZDEM 工具

| 仓库 | 作用 |
|------|------|
| [ZDEM_ParticleTracker](https://github.com/Phoenix0531-sudo/ZDEM_ParticleTracker) | 交互式颗粒追踪 + VisPy 真实半径渲染 |
| [ZDEM_Salt_Kinematics](https://github.com/Phoenix0531-sudo/ZDEM_Salt_Kinematics) | 盐体几何/运动学提取与出图 |
| [ZDEM_Area_Conservation](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation) | 面积守恒 / 三角网格分析 |
| [ZDEM_Bond_Fracture](https://github.com/Phoenix0531-sudo/ZDEM_Bond_Fracture) | 粘结损伤序列 + 桌面/CLI |
| [ZDEM_Damage_Thresholds](https://github.com/Phoenix0531-sudo/ZDEM_Damage_Thresholds) | 损伤阈值与应变–能量图 |
| [ZDEM_DFN](https://github.com/Phoenix0531-sudo/ZDEM_DFN) | ZDEM 离散裂隙网络生成 |
| [ZDEM_Model_Editor](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor) | 模型文件可视化编辑 |
| [ZDEM_Archiver](https://github.com/Phoenix0531-sudo/ZDEM_Archiver) | 大体量模拟结果归档清理 |
| [ZDEM3D_WEB](https://github.com/Phoenix0531-sudo/ZDEM3D_WEB) | CAE 云端界面（Django + React + VTK.js） |
## 许可证

MIT。可在署名前提下商用。见 [LICENSE](LICENSE)。
