# Development environment set-up

This project can only be run on the Windows operating system.

We recommend using Anaconda with Python version 3.8.

Conda Download Address：https://www.anaconda.com/

1. Open CMD or Powershell 

(you need to obtain administrator privileges to execute scripts that control the mouse and keyboard).

cd to the project path (assuming it is Amenoma) and execute the following command：

```
Amenoma> conda env create -f ./ArtScanner/build_env_ui.yml
```

2.The environment is suitable for running programs 

and the default command to activate the environment is as follows：

```
conda activate ArtScannerBuildUI
```

3.Run, compile the UIMain.py file using Python

Chinese version:

```
python UIMain.py
```

English version:

```
python UIMain_EN.py
```