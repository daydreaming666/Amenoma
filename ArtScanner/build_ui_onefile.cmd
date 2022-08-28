pyinstaller -w -F ^
--add-data "rcc/models_CHS/artifact_model_3.0.0.h5;./rcc/models_CHS" ^
--add-data "rcc/models_CHS/material_model_3.0.0.h5;./rcc/models_CHS" ^
--add-data "Tools/ReliquaryLevelExcelConfigData.json;./Tools" ^
--add-data "Tools/ReliquaryAffixExcelConfigData.json;./Tools" ^
--add-data "rcc/genshin.ttf;./rcc" ^
--add-data "rcc/material_names_v30.json;./rcc" ^
--add-data "rcc/char_map_v30.json;./rcc" ^
--hidden-import=h5py ^
--hidden-import=h5py.defs ^
--hidden-import=h5py.utils ^
--hidden-import=h5py.h5ac ^
--hidden-import=h5py._proxy ^
--uac-admin ^
-n Amenoma ^
UImain.py