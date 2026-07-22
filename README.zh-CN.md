# ZDEM Area Conservation

**ZDEM 颗粒分布与面积守恒分析 — 三角剖分统计 + 论文风格图。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

ZDEM 颗粒分布与面积守恒分析 — 三角剖分统计 + 论文风格图。

样例优先。CI 不需要多 GB 原始结果。


## Screenshots

<table>
<tr><td width="50%"><img src="docs/screenshots/area-fig1.png" alt="Figure panel"><br><em>Figure panel</em></td><td width="50%"><img src="docs/screenshots/area-stitched.png" alt="Stitched figure"><br><em>Stitched figure</em></td></tr>
</table>

## 功能

- 📐 面向三角剖分的面积守恒指标
- 🧾 ZDEM 结果 `zdemio` / `zdemplot` 辅助
- 🖼️ 论文风格出图脚本（`fig*.py`）
- 🧪 `samples/` 迷你 `.dat`，CI 不依赖超大数据
- ✅ 基于 samples 的严格 CI + 关键 ruff

## 快速开始

### 安装

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation.git
cd ZDEM_Area_Conservation
pip install -r requirements.txt
# or: uv sync
```

### 使用

```bash
python Area_Conservation.py --help
pytest tests/
```

个人大数据集留在本地（`data/`、完整 `figures/`）— 不要强推仓库。

## 项目结构

```
Area_Conservation.py  zdemio.py  zdemplot.py
samples/  figures/  docs/screenshots/
tests/
```

## 相关 ZDEM 工具

| 仓库 | 作用 |
|------|------|
| [ZDEM_ParticleTracker](https://github.com/Phoenix0531-sudo/ZDEM_ParticleTracker) | 交互颗粒追踪 + VisPy 真实半径渲染 |
| [ZDEM_Salt_Kinematics](https://github.com/Phoenix0531-sudo/ZDEM_Salt_Kinematics) | 盐构造几何 / 运动学提取与出图 |
| [ZDEM_Area_Conservation](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation) | 面积守恒 / 三角剖分分析 |
| [ZDEM_Bond_Fracture](https://github.com/Phoenix0531-sudo/ZDEM_Bond_Fracture) | 粘结损伤序列 + 桌面 / CLI |
| [ZDEM_Damage_Thresholds](https://github.com/Phoenix0531-sudo/ZDEM_Damage_Thresholds) | 损伤阈值与应变能图 |
| [ZDEM_DFN](https://github.com/Phoenix0531-sudo/ZDEM_DFN) | ZDEM 离散裂隙网络生成 |
| [ZDEM_Model_Editor](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor) | 模型文件可视化编辑 |
| [ZDEM_Archiver](https://github.com/Phoenix0531-sudo/ZDEM_Archiver) | 大体积模拟结果归档 / 清理 |
| [ZDEM3D_WEB](https://github.com/Phoenix0531-sudo/ZDEM3D_WEB) | CAE 云端界面（Django + React + VTK.js） |

## 说明

把三角剖分与统计自动化，比零散 MATLAB 脚本更适合可复现实验报告。

## 许可证

MIT。在注明出处的前提下可商业使用（以 LICENSE 为准）。详见 [LICENSE](LICENSE)。
