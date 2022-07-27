# 「天目」 -- Amenoma
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdaydreaming666%2FAmenoma.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdaydreaming666%2FAmenoma?ref=badge_shield)


[简体中文](README.md) | [English](README_en.md)

> 「天目流的诀窍就是滴水穿石的耐心和全力以赴的意志」

扫描背包中的圣遗物和材料，并导出至 json 格式。之后可导入至圣遗物分析工具与材料规划工具进行分析与规划。

### 圣遗物

**支持的格式**
* 莫娜占卜铺
* 原魔计算器
* GOOD (Genshin Open Object Description)
-------------------------
**分析工具**
* [莫娜占卜铺](https://www.mona-uranai.com)
* [原魔计算器](https://genshin.mingyulab.com)
* [Genshin Optimizer](https://frzyc.github.io/genshin-optimizer)

### 材料

**支持的格式**
* GOOD (Genshin Open Object Description)
---------------------------------
**规划工具**
* [Seelie 仙灵](https://seelie.me)
* [Genshin Center](https://genshin-center.com/)

> 加入
> 
> Discord Server [Amenoma Smithy](https://discord.gg/5e3WyFNG9A)
>
> QQ 群： 910549414
> 
> 反馈 BUG, 提出建议 和 ~~聊天吹水~~

如果你是第一次使用，请确保完整读完此页。

觉得好用，请给我 Star。 十分感谢！

## 下载

- [Github Release](https://github.com/daydreaming666/Amenoma/releases)
- [Google Drive](https://drive.google.com/drive/folders/1FYrsXy_nznVcV_aN4731FTDWQcAacivy?usp=sharing)
- [百度网盘 提取码:i2hd](https://pan.baidu.com/s/1CDHgZAbFWEPoqt4183GT9A)

- Amenoma.exe 

  中文版

- Amenoma_EN.exe
  
  英文版

> 使用中文界面时，请**不要**下载 *Amenoma_EN.exe* 的版本。不同语言的版本不能通用。

## 用法

### 扫描圣遗物
1. 双击 Amenoma.exe 打开程序，等待一会儿代码的解压
2. 将原神调整分辨率为 1600 * 900
3. 打开背包 - 圣遗物
4. 捕获窗口(如果没有被捕获)
5. 调整扫描选项
6. 开始扫描(使用鼠标中键打断扫描并停止)
7. 扫描结果存储在运行文件夹
   - `artifacts.genshinart.json` 莫娜占卜铺
   - `artifacts.genmocalc.json`  原魔计算器 
   - `artifacts.GOOD.json`       Genshin Optimizer

### 扫描材料
与上述步骤类似，但注意导出文件名为`materials.GOOD.json`.

> [其他问题](#qa)


## Release Notes

2.7.0
- 更新适配原神2.7

2.6.0
- 更新适配原神2.6
- 增加格式转换功能


## 开发环境搭建

> 普通用户请跳过这一节

```cmd
conda env create -f ./ArtScanner/Tools/model_trainer/dev_env.yml
```

> 更多开发文档[AmenomaDevDocs](AmenomaDevDocs/.)

## 版权说明

### 开源协议

[GNU GENERAL PUBLIC LICENSE Version 3](https://www.gnu.org/licenses/gpl-3.0.html)

### 声明

您下载或使用本软件，视为您知悉并同意以下内容：

- 本软件为离线软件，无需网络环境，不会上传任何信息。
- 本软件需要操控鼠标对自动对背包中的圣遗物进行点击，并对窗口进行截图，因此需要管理员权限。
- 本软件仅对屏幕信息进行识别，不会 hook 进程与修改内存。
- 本软件为开源软件，不对您因使用本软件而造成的任何损失负责。
- 本项目仅为个人爱好，与 miHoYo 公司无任何关系。


## 鸣谢

- [ProblemFactory/GenshinArtScanner](https://github.com/ProblemFactory/GenshinArtScanner)
的项目，本项目使用了GenshinArtScanner的模型
- [theBowja/genshin-db](https://github.com/theBowja/genshin-db) 数据支持
- 各位测试与使用者的支持


## Q&A

- Q: 当使用超宽屏时，背包的行列数不对。
- A: 更改分辨率后重启游戏即可。

---------------

- Q: 使用手柄进行游戏时无法扫描。
- A: 扫描前请将操作模式切换为「鼠标 & 键盘」。

---------------

- Q: 扫描物品时数目并非完全正确。
- A: 因为是扫描屏幕识别而非读取内存，有少部分错误和识别失败是正常现象。

---------------

- Q: 未支持最新版本的圣遗物/材料。
- A: 更新程序即可。因为是自训练模型，我从获取到新版本数据到更新程序需要一定时间（大概要数天到一周）。


> 如果遇到问题或任何建议，请提交 issues 或邮件至 [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## 捐赠

我是一名在校大学生，该项目花费了我大量的时间。
非常感谢您的支持！

支付宝： 15269372273

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdaydreaming666%2FAmenoma.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdaydreaming666%2FAmenoma?ref=badge_large)