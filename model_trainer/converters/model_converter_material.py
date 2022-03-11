import os.path

from tensorflow.keras.layers import Input, Reshape, Dense, Dropout, Bidirectional, LSTM
from tensorflow.keras.layers.experimental.preprocessing import StringLookup
from tensorflow.keras.models import Model

from ArtScanner.MaterialInfo import MaterialsNameCHS as MN
from model_trainer.mobilenetv3 import MobileNetV3_Small

import model_trainer.model_info as model_info

MaterialsNameCHS = list(MN.keys())

characters = sorted(
    [
        *set(
            "".join(
                list(MaterialsNameCHS)
                + list("0123456789")
            )
        )
    ]
)
char_to_num = StringLookup(
    vocabulary=list(characters), num_oov_indices=0, mask_token="")
num_to_char = StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", mask_token="", invert=True)

width = 240
height = 16
max_length = 15

input_shape = (width, height)

input_img = Input(
    shape=(input_shape[0], input_shape[1], 1), name="image", dtype="float32"
)
mobilenet = MobileNetV3_Small(
    (input_shape[0], input_shape[1], 1), 0, alpha=1.0, include_top=False
).build()
x = mobilenet(input_img)
new_shape = ((input_shape[0] // 8), (input_shape[1] // 8) * 576)
x = Reshape(target_shape=new_shape, name="reshape")(x)
x = Dense(64, activation="relu", name="dense1")(x)
x = Dropout(0.2)(x)

# RNNs
x = Bidirectional(LSTM(128, return_sequences=True, dropout=0.25))(x)
x = Bidirectional(LSTM(64, return_sequences=True, dropout=0.25))(x)

# Output layer
output = Dense(len(characters) + 2, activation="softmax", name="dense2")(x)

# Define the model
model = Model(inputs=[input_img], outputs=output, name="ocr_model_v1")
model.load_weights(os.path.join("..", model_info.MODEL_DIR, model_info.MATERIALS_MODEL_NAME))


def convert():
    model.summary()
    model.save(os.path.join(model_info.OUTPUT_DIR,
                            f"material_model_{model_info.MODEL_TARGET_VERSION}.h5"))
