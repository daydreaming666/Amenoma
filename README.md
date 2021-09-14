# 「天目」 -- Amenoma

[简体中文](README.md) | [English](README_en.md)

> 「天目流的诀窍就是滴水穿石的耐心和全力以赴的意志」

扫描背包中的圣遗物，并导出至 json 格式。之后可导入圣遗物分析工具( [莫娜占卜铺](https://www.mona-uranai.com) 、 [原魔计算器](https://genshin.mingyulab.com) 、 [Genshin Optimizer](https://frzyc.github.io/genshin-optimizer ) 进行计算与规划等。

2.1.1版本已发布。

新功能：

- 根据导出器自动调节调出选项
- 适配 GOOD (Genshin Open Object Description)
- 好用的 logger
- 副词条名自动纠错
- 更多的扫描和导出选项
  - 使用增强的捕获窗口（云游戏适配）
  - 一次性导出所有格式（方便使用多种工具对比）
  - 可选择导出所有图片（不止导出失败的图片）
  - 根据套装过滤圣遗物
- 微小的 UI 调整

bug 修复：

- 修复了一个可能识别出错误星星数量的 bug
- 已扫描数量统计错误

**重要警告：目前，请不要使用 GOOD 格式导入 Genshin Optimizer！这会导致您的数据库被清空（角色和武器）。请使用莫娜格式导入。**

> 加入
> 
> Discord Server [Amenoma Smithy](https://discord.gg/S3B9NB7Bk2)
>
> QQ 群： 910549414
> 
> 反馈 BUG, 提出建议 和 ~~聊天吹水~~

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

> [其他问题](#qa)


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

这里还没写呢 QwQ

> 如果遇到问题或任何建议，请提交 issues 或邮件至 [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## 捐赠

我是一名在校大学生，该项目花费了我大量的时间。
非常感谢您的支持！

支付宝： 15269372273

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)
