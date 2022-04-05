pyinstaller -w -F --clean ^
--add-data "rcc/models_EN/artifact_model_EN_2.6.0.h5;./rcc/models_EN" ^
--add-data "rcc/models_EN/material_model_EN_2.6.0.h5;./rcc/models_EN" ^
--add-data "Tools/ReliquaryLevelExcelConfigData.json;./Tools" ^
--add-data "Tools/ReliquaryAffixExcelConfigData.json;./Tools" ^
--add-data "rcc/genshin.ttf;./rcc" ^
--add-data "rcc/material_names_v26.json;./rcc" ^
--add-data "rcc/char_map_v26.json;./rcc" ^
--hidden-import=h5py ^
--hidden-import=h5py.defs ^
--hidden-import=h5py.utils ^
--hidden-import=h5py.h5ac ^
--hidden-import=h5py._proxy ^
--uac-admin ^
-n Amenoma_EN ^
UImain_EN.py