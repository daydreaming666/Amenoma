# 「天目」 -- Amenoma

[简体中文](./README.md) | [English](./README_en.md)

> The essence of Amenoma Art is to have the patience to move mountains and unrelenting willpower.

The Original name was GAS -- GenshinArtScanner

Scan the Artifact in the backpack and export them to json format. Later, they can be imported to Artifact analysis tools( [mona-uranai](https://www.mona-uranai.com), [MingyuLab](https://genshin.mingyulab.com), [Genshin Optimizer](https://frzyc.github.io/genshin-optimizer )) for calculation and planning, etc. 

- genshin 2.0 Artifact supported!
- Refactored the scanning process to greatly improve the user experience!

## Download

Multiple versions available for download: 

- Amenoma_EN.exe
  Single-file version with GUI, which takes longer to start.
- Amenoma_EN.zip 
  Multi-file version with GUI, can be used after decompression, and the startup time is shorter.The disadvantage is that it takes up more space after decompression.

> For EngLish users:
> 
> Please make sure to download the version with the suffix *_EN*. Versions in different languages **cannot** be used universally. 


## Usage

1. Double-click ArtScanner.exe to open the program, and wait a while for the program to decompress. 
2. Adjust the resolution of the *Genshin Impact* to 1600 * 900, open Bag - Artifacts.
3. Capture the window and wait.
4. Adjust scanning options.
5. Start scanning 
6. Scan results are stored in current running folder *artifacts.genshinart.json*(mona-uranai) / *artifacts.mingyulab.json*(MingyuLab) / *artifacts.genshin-optimizer.json*(Genshin Optimizer).

> [Other Questions](#Q&A)


## Development Environment Setup 

> Skip this section if you're not developer.

```cmd
conda env create -f ./ArtScanner/Tools/model_trainer/dev_env.yml
```

## Copyright

### Open-Source LICENSE

[APACHE LICENSE, VERSION 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

### Announcement

When you download or use this software, you are deemed to know and agree to the following: 

- This software is offline software, no network environment is required, and no information will be uploaded. 
- This software needs to manipulate the mouse to automatically click on the holy relic in the backpack and take a screenshot of the window. 
- This project is only a personal hobby and has nothing to do with miHoYo.
- This software is open source software and is not responsible for any losses caused by your use of this software. 

> The above content is subject to the Chinese version 

## Thanks

- [ProblemFactory/GenshinArtScanner](https://github.com/ProblemFactory/GenshinArtScanner) the Project
- [honeyhunterworld](https://genshin.honeyhunterworld.com/) Data support.
- Supports from users and testers.

## Q&A

Known issues:

1. On a widescreen display (21:9), rows and columns are calculated incorrectly. 

> If you encounter problems or any suggestions, please submit issues or email to [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## Donate

I am a college student, and this project took me a lot of time.
Thank you very much for your support! 

<img src="https://daydreaming.top/wp-content/uploads/2021/08/QQ图片20210822004740.jpg" width="135" height="210" alt="Alipay"/>

<img src="https://daydreaming.top/wp-content/uploads/2021/08/QQ图片20210822004735.png" width="153" height="210" alt="Wechat"/>

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)