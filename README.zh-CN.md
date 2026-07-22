# ZDEM Area Conservation

**ZDEM 颗粒子集面积守恒分析 — Delaunay/三角网、color# 过滤、论文图脚本、样例优先 CI。**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

批量处理 ZDEM `.dat`：按 **颜色组** 选颗粒，建三角网，统计变形过程中的 **面积**。替代零散 MATLAB 脚本。

## 预览

![ZDEM Area Conservation](docs/screenshots/preview.png)

## 主入口

`Area_Conservation.py`（getopt）：`zdemio`/`zdemplot` 读写绘图，`Triangulation`/`Delaunay` 建网，按 color# 过滤，导出网格图与面积趋势；`Agg` 无界面出图；自动探测中文字体。

`fig1_*.py` … `fig8_areatrend.py` 为论文/报告向图件脚本。

## 数据策略

- **`samples/`**：CI 迷你帧  
- **`data/`、`data1/`、完整 figures**：仅本地，勿强推  

## 安装运行

```bash
pip install -r requirements.txt
python Area_Conservation.py --help
pytest tests/
```

## 许可证

MIT。详见 [LICENSE](LICENSE)。
