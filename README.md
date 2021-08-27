# 「天目」 -- Amenoma

[简体中文](./README.md) | [English](./README_en.md)

> 「天目流的诀窍就是滴水穿石的耐心和全力以赴的意志」

原名 GenshinArtScanner.

扫描背包中的圣遗物，并导出至 json 格式。之后可导入圣遗物分析工具( [莫娜占卜铺](https://www.mona-uranai.com) 、 [MingyuLab](https://genshin.mingyulab.com) 、 [Genshin Optimizer](https://frzyc.github.io/genshin-optimizer ) 进行计算与规划等。

- 已支持 原神2.0 的圣遗物!
- 重构了扫描流程，大幅提高使用体验


## 下载

有多个版本可供下载：

- Amenoma.exe
  带界面的单文件版本，启动时间略长。(推荐)

- Amenoma.zip
  带界面的多文件版本，解压后使用，启动时间较短。缺点是解压后占用空间较大。

- AmenomaCLI.exe
  使用命令行的单文件版本。

> 使用中文界面时，请确保下载不带有后缀 *_EN* 的版本。不同语言的版本不能通用。

## 用法

1. 双击 Amenoma.exe 打开程序，等待一会儿代码的解压
2. 将原神调整分辨率为 1600 * 900，打开背包 - 圣遗物
3. 捕获窗口并等待
4. 调整扫描选项
5. 开始扫描
6. 扫描结果存储在运行文件夹 *artifacts.genshinart.json*(莫娜占卜铺) / *artifacts.mingyulab.json*(MingyuLab) / *artifacts.genshin-optimizer.json*(Genshin Optimizer)

> [其他问题](#Q&A)


## 开发环境搭建

> 普通用户请跳过这一节

```cmd
conda env create -f ./ArtScanner/Tools/model_trainer/dev_env.yml
```

## 版权说明

### 开源协议

[GNU GENERAL PUBLIC LICENSE Version 3](https://www.gnu.org/licenses/gpl-3.0.html)

### 声明

您下载或使用本软件，视为您知悉并同意以下内容：

- 本软件为离线软件，无需网络环境，不会上传任何信息。
- 本软件需要操控鼠标对自动对背包中的圣遗物进行点击，并对窗口进行截图。
- 本项目仅为个人爱好，与 miHoYo 公司无任何关系
- 本软件为开源软件，不对您因使用本软件而造成的任何损失负责。


## 鸣谢

- [ProblemFactory/GenshinArtScanner](https://github.com/ProblemFactory/GenshinArtScanner)
的项目
- [honeyhunterworld](https://genshin.honeyhunterworld.com/) 的数据支持
- 各位测试与使用者的支持


## Q&A

已知问题：

1. 在宽屏的显示器上（21:9），行列数计算错误。

> 如果遇到问题或任何建议，请提交 issues 或邮件至 [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## 捐赠

我是一名在校大学生，该项目花费了我大量的时间。
非常感谢您的支持！

<img src="https://daydreaming.top/wp-content/uploads/2021/08/QQ图片20210822004740.jpg" width="135" height="210" alt="Alipay"/>

<img src="https://daydreaming.top/wp-content/uploads/2021/08/QQ图片20210822004735.png" width="153" height="210" alt="Wechat"/>

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)
