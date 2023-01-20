# 开发环境搭建

该项目仅可在Windows操作系统上运行.

推荐使用自带Python 3.8版本的Anaconda.

Conda下载地址：https://www.anaconda.com/

1.打开CMD或Powershell（需要获取管理员权限执行键鼠控制脚本），

进入项目地址（假设是Amenoma），执行如下命令：

```
Amenoma> conda env create -f ./ArtScanner/build_env_ui.yml
```

2.该环境适用于运行程序，激活环境默认命令如下：

```
conda activate ArtScannerBuildUI
```

3.运行，使用Python编译UIMain.py文件

```
python UIMain.py
```

英文版：

```
python UIMain_EN.py
```