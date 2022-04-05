import os

import model_trainer.converters.model_converter_artifact as mca
import model_trainer.converters.model_converter_artifact_EN as mcaEN
import model_trainer.converters.model_converter_material as mcm
import model_trainer.converters.model_converter_material_EN as mcmEN
import model_trainer.model_info as mi


if __name__ == '__main__':
    os.makedirs(mi.OUTPUT_DIR, exist_ok=True)
    mca.convert()
    # mcaEN.convert()
    # mcm.convert()
    # mcmEN.convert()
