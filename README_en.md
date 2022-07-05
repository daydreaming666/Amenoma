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

- Amenoma_EN.exe
  
  English version.

- Amenoma.exe
  
  Chinese version.

> For English users:
> 
> **DO NOT** download the *Amenoma.exe* file, which is build for the Chinese version.
> Download the *Amenoma_EN.exe* file instead.

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

2.7.0
- Update for Genshin 2.7

2.6.0
- Update for Genshin 2.6
- A new feature of format conversion.

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
- [theBowja/genshin-db](https://github.com/theBowja/genshin-db) Data support.
- Supports from users and testers.

## Q&A

- Q: Wrong Columns/Lines while using a ultra-wide screen.
- A: Restart the game after changing resolution.

---------------

- Q: Could not scan while using a controller.
- A: Switch the control mode to 「Mouse & Keyboard」 before using.

---------------

- Q: The numbers of items/materials are not completely accurate and some fail to be scanned.
- A: This is normal because it scans the screen for recognition instead of reading memory。

---------------

- Q: Not supported the artifact/materials from the latest version.
- A: Just update the program. Because it's a manually-trained model, it takes me a few days to update the program.

> If you encounter problems or any suggestions, please submit issues or email to [daydreaming@foxmail.com](mailto://daydreaming@foxmail.com)


## Donate

I am a college student, and this project took me a lot of time.
Thank you very much for your support! 

Alipay: 15269372273

[PayPal@daydreaming666](https://www.paypal.me/daydreaming666)


> PS. 
> The project is maintained by a Chinese Dev whose English is not so good. Contact me if you need any help.**
