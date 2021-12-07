# 「天目」 -- Amenoma

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

有多个版本可供下载：

- Amenoma.exe
  带界面的单文件版本，启动时间略长。(推荐)

- Amenoma.zip
  带界面的多文件版本，解压后使用，启动时间较短。缺点是解压后占用空间较大。

- AmenomaCLI.exe
  使用命令行的单文件版本。(该版本仅维护圣遗物名称识别模型)

> 使用中文界面时，请确保下载不带有后缀 *_EN* 的版本。不同语言的版本不能通用。

## 用法

### 扫描圣遗物
1. 双击 Amenoma.exe 打开程序，等待一会儿代码的解压
2. 将原神调整分辨率为 1600 * 900
3. 打开背包 - 圣遗物
4. 捕获窗口(如果没有被捕获)
5. 调整扫描选项
6. 开始扫描
7. 扫描结果存储在运行文件夹
   - `artifacts.genshinart.json` 莫娜占卜铺
   - `artifacts.genmocalc.json`  原魔计算器 
   - `artifacts.GOOD.json`       Genshin Optimizer

### 扫描材料
与上述步骤类似，但注意导出文件名为`materials.GOOD.json`.

> [其他问题](#qa)


## Release Notes

2.3.1
- 回滚了对点击与翻页的重构，使得速度可以回到之前。
- （假如代码能跑，就不要动它）

2.3.0版本已发布。

- 新功能：
- 支持扫描材料，现在可以扫描材料并一键导入 *Seelie 仙灵 / Genshin Center* 来进行物品规划。
- 已更新原神 2.3 版本的圣遗物。
- 增加了对于类型名称的自动纠错
- 增加了对于装备位置和是否上锁的检测

- bug 修复：
- GOOD 格式的浮点误差


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
- [honeyhunterworld](https://genshin.honeyhunterworld.com/) 的数据支持
- 各位测试与使用者的支持


## Q&A

已知的问题：

1. 有时，对鼠标的控制完全不生效，包括滚轮和点击。假如你遇到了这个情况，请联系我，我需要更多的信息来找出原因。
2. 有时，对齐操作进行的不正常。在扫描一开始时就会把列表向下滚动。检查下是否启用了色彩滤镜（如 NVIDIA） ，关闭重新扫描即可。
3. 因翻页时坐标有一定的误差，部分物品的数量会识别失败。

> 如果遇到问题或任何建议，请提交 issues 或邮件至 [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## 捐赠

我是一名在校大学生，该项目花费了我大量的时间。
非常感谢您的支持！

支付宝： 15269372273

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)
