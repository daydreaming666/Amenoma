# 「天目」 -- Amenoma

[简体中文](README.md) | [English](README_en.md)

> The essence of Amenoma Art is to have the patience to move mountains and unrelenting willpower.

Scan the Artifact and Materials in the Inventory and export them to json format. Then, they can be imported to Artifact analysis tools and Material Planning tools for calculation and planning, etc. 

### Artifact

*Supported Formats*
* Mona-Uranai
* Genmo Calculator
* GOOD (Genshin Open Object Description)
-------------------------------
*Analysis Tools*
* [Mona-uranai](https://www.mona-uranai.com)
* [Genmo Calculator](https://genshin.mingyulab.com)
* [Genshin Optimizer](https://frzyc.github.io/genshin-optimizer)

### Materials

*Supported Formats*
* GOOD (Genshin Open Object Description)
---------------------------------
*Planning Tools*
* [Seelie](https://seelie.me)
* [Genshin Center](https://genshin-center.com/)

> Join My Discord Server for reporting bugs & suggestions or just chatting with us. `-->` [Amenoma Smithy](https://discord.gg/5e3WyFNG9A)

If you are using it for the first time, make sure to read this file. If anything confuses, contact me.

Give me star if you think it's easy to use. Thanks!

## Download

- [Github Release](https://github.com/daydreaming666/Amenoma/releases)
- [Google Drive](https://drive.google.com/drive/folders/1FYrsXy_nznVcV_aN4731FTDWQcAacivy?usp=sharing)

Multiple versions available for download: 

- Amenoma_EN.exe
  Single-file version with GUI, which takes longer to start.
- Amenoma_EN.zip 
  Multi-file version with GUI, can be used after decompression, and the startup time is shorter.The disadvantage is that it takes up more space after decompression.

> For EngLish users:
> 
> Please make sure to download the version with the suffix *_EN*. Versions in different languages **cannot** be used universally. 


## Usage


### Scan Artifacts
1. Double-click ArtScanner.exe to open the program, and wait a while for the program to decompress. 
2. Adjust the resolution of the *Genshin Impact* to 1600 * 900 (Or others that meets 16:9).
3. Open Inventory - Artifacts.
4. Capture the window. (If it is not been captured)
5. Adjust scanning options.
6. Start scanning (Mouse middle-click to interrupt).
7. Scan results are stored in current running folder.
   - `artifacts.genshinart.json`  Mona-uranai 
   - `artifacts.genmocalc.json`   Genmo Calculator
   - `artifacts.GOOD.json`        Genshin Optimizer

### Scan Materials
Similar to above.
And the exported json file is `materials.GOOD.json`

> [Other Questions](#qa)


## Release Notes

2.5.0
- Add support for Genshin Impact 2.5.0
- The feature of scanning materials is temporarily disabled due to the re-training of the model.

2.3.2
- Significantly increase the scanning speed of materials 

2.3.1
- Rollback the refactoring of click and page turning, so that the speed can return to the previous one.
- (if the code can run, don't touch it)

Version 2.3.0 released 

- New Features:
- Scanning materials supported. You can scan materials and import the to *Seelie / Genshin Center* in one click.
- updated Genshin 2.3.0 Artifacts.
- Added autocorrection for the type of Artifact
- Added the detection of location and locked status of the Artifact

- Bug Fixes:
- floating point errors as GOOD values

## Development Environment Setup 

> Skip this section if you're not developer.

```cmd
conda env create -f ./ArtScanner/Tools/model_trainer/dev_env.yml
```
> More development docs [AmenomaDevDocs](AmenomaDevDocs/.)

## Copyright

### Open-Source LICENSE

[GNU GENERAL PUBLIC LICENSE Version 3](https://www.gnu.org/licenses/gpl-3.0.html)

### Announcement

When you download or use this software, you are deemed to know and agree to the following: 

- This software is offline software, no network environment is required, and no information will be uploaded. 
- This software needs to manipulate the mouse to automatically click on the Artifacts in the Inventory and take a screenshot of the window. Therefore, it needs Administrator permission.
- This software only read information from screen, and never hook processes or modify memory.
- This software is open source software and is not responsible for any losses caused by your use of this software. 
- This project is only a personal hobby and has nothing to do with miHoYo.

> The above content is subject to the Chinese version 

## Thanks

- [ProblemFactory/GenshinArtScanner](https://github.com/ProblemFactory/GenshinArtScanner) This project uses the model of GenshinArtScanner.
- [honeyhunterworld](https://genshin.honeyhunterworld.com/) Data support.
- Supports from users and testers.

## Q&A

known issues:

1. In some cases, mouse controlling not work at all, including moving and clicking. Check if you're in pad mode, which will cause the error.
2. The aligner doesn't work well in some cases. It scrolls down the list even at the beginning of scanning. If this happens, check that if you are using any color filters, e.g. Nvidia ... , close them and try scanning again.
3. Some amount of the Materials are not correct, because of the error coordinates while turning the page.


> If you encounter problems or any suggestions, please submit issues or email to [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## Donate

I am a college student, and this project took me a lot of time.
Thank you very much for your support! 

Alipay: 15269372273

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)


> PS. 
> The project is maintained by a Chinese Dev whose English is not so good. Contact me if you need any help.**
