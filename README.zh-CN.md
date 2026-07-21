# ZDEM 面积守恒分析

**ZDEM 颗粒分布与面积守恒分析工具包**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

ZDEM 颗粒分布与面积守恒分析工具包。

> 作者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo) · 欢迎学习、二次开发与**商业使用**，请保留本仓库署名与许可证声明。

## 技术栈

Python · 科研绘图

## 功能特性

- 颗粒/面积守恒指标
- 基准模型与图件脚本
- 科研绘图输出

## 快速开始

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation.git
cd ZDEM_Area_Conservation
```

```bash
pip install -r requirements.txt
python Area_Conservation.py
```

更完整的英文说明见 [README.md](README.md)。

## 仓库结构（摘要）

```
ZDEM_Area_Conservation/
├─ .github/
├─ copyright/
├─ data/
├─ data1/
├─ docs/
├─ figures/
├─ res/
├─ zdem_area_conservation/
├─ Area_Conservation.py
├─ CHANGELOG.md
├─ Dockerfile
├─ fig1_algorithm_flow.py
├─ fig2_algorithm_flow.py
├─ fig2_benchmark_models.py
├─ fig3_benchmark_models.py
├─ fig3_complex_models.py
├─ fig4_complex_models.py
├─ fig5_benchmark_mesh.py
```

## 测试

```bash
pip install pytest
pytest -q
```

仓库内 `tests/` 至少包含 smoke 测试；有完整测试套件时以 CI 为准。

## CI

GitHub Actions（`push` / `pull_request`）会：

- 安装依赖（requirements / pyproject）
- 运行 `pytest`（**硬失败**）
- 尽力做语法/结构检查

## 许可证

[MIT](LICENSE) — 可自由使用、修改、分发与**商用**，需保留版权与许可声明（提及本仓库 / 作者即可）。

## 关于

维护者：[Phoenix0531-sudo](https://github.com/Phoenix0531-sudo)
