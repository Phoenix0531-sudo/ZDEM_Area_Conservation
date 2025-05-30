# ZDEM 面积守恒测试

开发者：包羡钧

本程序用于测试 ZDEM 模拟中颗粒分布的面积守恒性，主要功能包括：
1. 读取 ZDEM 模拟结果中的颗粒数据
2. 计算指定颜色颗粒的分布面积
3. 分析不同时间步之间的面积变化
4. 可视化颗粒分布和三角网格划分

### 环境要求
```
pip install numpy
pip install matplotlib
```

### 运行程序
```
将dat文件放入data文件夹中
./main.py --dir=DataDir
python Area_Conservation_Test.py
```

### 参数说明

- `COLOR_TO_EXTRACT`: 要提取的颗粒颜色，默认为 [7]
- `THRESHOLD_FACTOR`: 三角网格边长阈值因子，默认为 3.0

### 输出说明

程序会输出以下信息：
1. 每个时间步的颗粒数量和面积
2. 相邻时间步之间的面积变化率
3. 从初始到最终状态的总体变化率
4. 颗粒分布和三角网格的可视化图形

## 文件说明

- `Area_Conservation_Test.py`: 主程序文件
  * 实现面积守恒性测试的核心功能
  * 包含颗粒数据读取、三角网格生成、面积计算等功能
  * 提供可视化接口和结果分析功能

- `zdemplot.py`: 绘图相关函数
- `data/`: 存放 ZDEM 模拟结果数据的目录
  * 存放原始 dat 文件
  * 存放生成的 particles.txt 文件
  * 存放输出的 jpg 图片文件
