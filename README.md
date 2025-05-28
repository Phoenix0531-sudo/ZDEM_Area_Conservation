## zdem2jpg后处理脚本

开发者：李长圣 徐雯峤

### 追加许可信息到 `zdem.lic`

```
pip3 install pyDes
```

1. 将 `zdem.lic` 复制到本文件夹
2. 打开 `issue.py` 设置注册信息
3. 运行 `issue.py`  追加发布许可证到 `zdem.lic`

### 运行 软件

```
./main.py -h
```

### 功能：

读取VBOX计算结果，生成jpg图片。 plot ball to jpg

```
./main.py --dir=DataDir
```

- 输入参数：

    ```
    [1] DataDir  VBOX计算结果所在目录
    ```

- 输出：

    ```
    [1] jpg格式文件
    ```


### 实例：

```
./main.py --dir=./example #将读取 ./example/*.dat 生成 ./example/*.jpg
./main.py --dir=./example --xmax=40000 --ymax=10000 --xmove=0.0 --ymove=0.0 --xmin=0.0 --ymin=0.0 --major_locator=1000.0 --minor_locator=100.0 --fontsize=12 --dpi=300 --linewidth=1
./main.py --dir=./data --xmax=40000 --ymax=10000 --xmove=-1000.0 --ymove=-1000.0 --xmin=0.0 --ymin=0.0 --major_locator=10000.0 --minor_locator=1000.0 --fontsize=12
```

### 使用 pyinstaller 打包程序为exe

1. 采用虚拟环境方法  `conda activate zdem`

    - 配置虚拟环境并且生成可执行文件
        ```
            bash Anaconda3-2020.11-Linux-x86_64.sh
            conda -V
            conda list
            conda env list
            conda update conda
            conda create -n zdem python=3.8 # 3.8.13
            conda activate zdem
            pip3 install matplotlib # 3.5.2 
            pip3 install pyDes  # 2.0.1
            pip3 install pyinstaller # 5.0.1
            home/lichangsheng/desktop/git/zdempost/main.py -h
            pyi-makespec -F main.py #生成配置文件 `main.spec` ，已经生成可以跳过
            pyinstaller main.spec  #生成的可执行文件见dist文件夹
        ```

    - `mian.spec` 中内容如下：
        ```
        # -*- mode: python ; coding: utf-8 -*-
        
        block_cipher = None


        a = Analysis(
            ['main.py'],
            pathex=[],
            binaries=[],
            datas=[('res', 'res'),
                ('/home/lichangsheng/Desktop/bin/anaconda3/envs/zdem/lib/python3.8/site-packages/matplotlib/mpl-data/matplotlibrc', 'matplotlib/mpl-data')],
            hiddenimports=[],
            hookspath=[],
            hooksconfig={},
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False,
        )
        pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

        exe = EXE(
            pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            [],
            name='main',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            upx_exclude=[],
            runtime_tmpdir=None,
            console=True,
            disable_windowed_traceback=False,
            argv_emulation=False,
            target_arch=None,
            codesign_identity=None,
            entitlements_file=None,
        )
        ```

    - 删除虚拟环境
        ```    
        conda install -n zdem [package]
        conda remove --name zdem  $package_name 
        conda deactivate
        conda remove -n your_env_name --all
        ```

2. 安装纯净系统法
    - 安装 `Centos 7.0`
    - 安装 `Python-3.8.3.tgz`
        ```
        tar -zxvf  Python-3.8.3.tgz
        cd Python-3.8.3
        ./configure  --enable-share
        make && make install
        ```
    - 安装 `matplotlib` `pyDes` `pyinstaller`
        ```
        pip3 install matplotlib
        pip3 install pyDes
        pip3 install pyinstaller
        pyinstaller --version
        ```
    - 打包生成一个可执行文件
        1. `pyi-makespec -F main.py` 生成main.spec文件：
        2. 修改 `mian.spec` 文件内容，如下

            ```
            # -*- mode: python -*-

            block_cipher = None

            a = Analysis(['main.py','zdemio.py','zdemplot.py'],
                    pathex=['C:\\Users\\xxx\\PycharmProjects\\Test'],
                    binaries=[],
                    datas=[('res', 'res'),
            ('/opt/python38/lib/python3.8/site-packages/matplotlib/mpl-data/matplotlibrc', 'matplotlib/mpl-data')], //重点
                    hiddenimports=[],
                    hookspath=[],
                    runtime_hooks=[],
                    excludes=[],
                    win_no_prefer_redirects=False,
                    win_private_assemblies=False,
                    cipher=block_cipher,
                    noarchive=False)
            pyz = PYZ(a.pure, a.zipped_data,
                    cipher=block_cipher)
            exe = EXE(pyz,
                a.scripts,
                a.binaries,
                a.zipfiles,
                a.datas,
                [],
                name='main',
                debug=False,
                bootloader_ignore_signals=False,
                strip=False,
                upx=True,
                runtime_tmpdir=None,
                console=True )
            ```
        3. `pyinstaller -F main.spec` 生成的可执行文件见dist文件夹

        4. 构建错误： `OSError: [Errno 28] No space left on device` 
            删除build文件夹重新构建
            ```
            rm -r build
            pyinstaller -F main.spec
            ```
        5. 其它方法，生成多个文件。
            ```
            pyi-makespec main.py
            pyinstaller main.spec
            ```
### 生成 `pyc` 运行程序

1. 生成 `.pyc`

    ```
    python -m main.py
    python -m vboxio.py
    python -m vboxplot.py
    ```
    
2. 见 `__pycache__` 目录

3. 重命名为 
    ```
    main.pyc -> zdem2jpg
    vboxio.pyc 
    vboxplot.pyc
    ```
4. 复制 `res` 目录到 `__pycache__` 目录

5. 运行
    ```
    python ./__pycache__/zdem2jpg -h
    ```

### 更新日志

- 2.2 (2022/05/15 )
    * 采用虚拟环境方法 `conda activate zdem` 生成可执行文件 `zdem2jpg`  
- 2.2 (2022/05/11 )
    1. 开启license
    2. 修复wall数量为零时，zdemplot.search_domain() search_domain_wall()无法计算墙体边界，导致无法绘制图形
- 2.2 beta (2022/03/28 )
    1. == 广播查找索引，将创建 n个颗粒m个bond的超级大矩阵，导致内存溢出 ，plot_contactbond()中Id1Id2ToIndex1Index2()

- 2.2 beta (2022/03/26 ) clear code rubbish, numpy array -> matrix
- 2.2 beta (2022-03-25)
    * 需要在bios中关闭CPU超线程才能正确并行计算，具体原因未知。
- 2.2 beta (2022-03-23)
    * 修复plotbond中，--xmax=40000 --ymax=10000，不起作用问题。
    * 修改数据为numpy array
    * 改为EllipseCollection 和 LineCollection绘制大量圆和线段，速度提高~9倍
    * 增加 --ballplot 默认为ture
- 2.1 (2021-06-17) 
    * 修复单核并行错误，max_workers=len(os.sched_getaffinity(pid))获取可用核心数
    * 强制 `xmin` `xmax` `ymin` `ymax` 生效






 python main.py --dir=./data --surfaceshow=true --dpi=300 --pagesize=14