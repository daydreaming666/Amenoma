import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from PIL import Image
import ArtsInfo
import logging
from tensorflow import get_logger
from tensorflow.keras.models import Model
from tensorflow.keras.layers.experimental.preprocessing import StringLookup
from tensorflow.keras.layers import Input, Reshape, Dense, Dropout, Bidirectional, LSTM
from tensorflow.keras.backend import ctc_decode
from mobilenetv3 import MobileNetV3_Small
from tensorflow.strings import reduce_join

get_logger().setLevel(logging.ERROR)


# class OCR:
#     def __init__(self, model_path='mn_model.h5', scale_ratio=1):
#         pass

class Config_EN:
    name_coords = [33, 4, 619, 72]
    type_coords = [32, 89, 350, 134]
    main_attr_name_coords = [35, 200, 350, 240]
    main_attr_value_coords = [35, 240, 350, 300]
    star_coords = [30, 310, 350, 360]
    level_coords = [43, 414, 112, 444]
    subattr_1_coords = [67, 480, 560, 520]
    subattr_2_coords = [67, 532, 560, 572]
    subattr_3_coords = [67, 584, 560, 624]
    subattr_4_coords = [67, 636, 560, 676]


class OCR:
    def __init__(self, model_weight='mn_model_weight.h5', scale_ratio=1):
        self.scale_ratio = scale_ratio
        self.characters = sorted(
            [
                *set(
                    "".join(
                        sum(ArtsInfo.ArtNames_EN, [])
                        + ArtsInfo.TypeNames_EN
                        + list(ArtsInfo.MainAttrNames_EN.values())
                        + list(ArtsInfo.SubAttrNames_EN.values())
                        + list(".,+%0123456789")
                    )
                )
            ]
        )
        # Mapping characters to integers
        self.char_to_num = StringLookup(
            vocabulary=list(self.characters), num_oov_indices=0, mask_token=""
        )

        # Mapping integers back to original characters
        self.num_to_char = StringLookup(
            vocabulary=self.char_to_num.get_vocabulary(), oov_token="", mask_token="", invert=True
        )



        self.width = 384
        self.height = 16
        self.max_length = 40
        self.build_model(input_shape=(self.width, self.height))
        self.model.load_weights(model_weight)

    def setScaleRatio(self, scaleRatio):
        self.scale_ratio = scaleRatio

    def detect_info(self, art_img):
        info = self.extract_art_info_EN(art_img)
        x = np.concatenate([self.preprocess(info[key]).T[None, :, :, None] for key in sorted(info.keys())], axis=0)
        y = self.model.predict(x)
        y = self.decode(y)
        return {**{key: v for key, v in zip(sorted(info.keys()), y)}, **{'star': self.detect_star(art_img)}}

    def extract_art_info_EN(self, art_img):
        name = art_img.crop([i * self.scale_ratio for i in Config_EN.name_coords])
        type = art_img.crop([i * self.scale_ratio for i in Config_EN.type_coords])
        main_attr_name = art_img.crop([i * self.scale_ratio for i in Config_EN.main_attr_name_coords])
        main_attr_value = art_img.crop([i * self.scale_ratio for i in Config_EN.main_attr_value_coords])
        level = art_img.crop([i * self.scale_ratio for i in Config_EN.level_coords])
        subattr_1 = art_img.crop([i * self.scale_ratio for i in Config_EN.subattr_1_coords])
        subattr_2 = art_img.crop([i * self.scale_ratio for i in Config_EN.subattr_2_coords])
        subattr_3 = art_img.crop([i * self.scale_ratio for i in Config_EN.subattr_3_coords])
        subattr_4 = art_img.crop([i * self.scale_ratio for i in Config_EN.subattr_4_coords])
        if np.all(np.abs(np.array(subattr_1, np.float) - [[[73, 83, 102]]]).max(axis=-1) > 25):
            del subattr_1
            del subattr_2
            del subattr_3
            del subattr_4
        elif np.all(np.abs(np.array(subattr_2, np.float) - [[[73, 83, 102]]]).max(axis=-1) > 25):
            del subattr_2
            del subattr_3
            del subattr_4
        elif np.all(np.abs(np.array(subattr_3, np.float) - [[[73, 83, 102]]]).max(axis=-1) > 25):
            del subattr_3
            del subattr_4
        elif np.all(np.abs(np.array(subattr_4, np.float) - [[[73, 83, 102]]]).max(axis=-1) > 25):
            del subattr_4
        return {key: value for key, value in locals().items() if key not in ['art_img', 'self']}

    def detect_star(self, art_img):
        star = art_img.crop([i * self.scale_ratio for i in Config_EN.star_coords])
        cropped_star = self.crop(self.normalize(self.to_gray(star)))
        coef = cropped_star.shape[1] / cropped_star.shape[0]
        coef = coef / 1.30882352 + 0.21568627
        return int(round(coef))

    def to_gray(self, text_img):
        text_img = np.array(text_img)
        if len(text_img.shape) > 2:
            text_img = (text_img[..., :3] @ [[[0.299], [0.587], [0.114]]])[:, :, 0]
        return np.array(text_img, np.float32)

    def normalize(self, img, auto_inverse=True):
        img -= img.min()
        img /= img.max()
        if auto_inverse and img[-1, -1] > 0.5:
            img = 1 - img
        return img

    def binarization(self, img, thresh=0.5):
        return np.where((img < thresh), 0, img)

    def resplice(self, img):
        line_height = 27
        if (img[30] == 0.).all():
            res1 = img[:line_height, :]
            res2 = img[-line_height:, :]
            space = np.zeros((res1.shape[0], 10))
            res = np.concatenate((res1, space, res2), axis=1)
            return self.crop(res, tol=0)
        else:
            return img

    def zoom(self, img):
        height_ = 60
        return (
                np.array(
                    Image.fromarray(np.uint8(img * 255)).resize(
                        (int(img.shape[1] * height_ / img.shape[0]), height_),
                        Image.BILINEAR, )
                ) / 255)


    def crop(self, img, tol=0.7):
        # img is 2D image data
        # tol  is tolerance
        mask = img > tol
        m, n = img.shape
        mask0, mask1 = mask.any(0), mask.any(1)
        col_start, col_end = mask0.argmax(), n - mask0[::-1].argmax()
        row_start, row_end = mask1.argmax(), m - mask1[::-1].argmax()
        #     print(row_end-row_start, col_end-col_start)
        return img[row_start:row_end, col_start:col_end]

    def resize_to_height(self, img):
        height = self.height
        return (
                np.array(
                    Image.fromarray(np.uint8(img * 255)).resize(
                        (int(img.shape[1] * height / img.shape[0]), height),
                        Image.BILINEAR,
                    )
                )
                / 255
        )

    def pad_to_width(self, img):
        width = self.width
        if img.shape[1] >= width:
            return img[:, :width]
        return np.pad(
            img, [[0, 0], [0, width - img.shape[1]]], mode="constant", constant_values=0
        )

    def preprocess(self, text_img):
        result = self.to_gray(text_img)
        result = self.normalize(result, True)
        result = self.binarization(result)
        result = self.crop(result, tol=0)

        result = self.zoom(result)
        result = self.resplice(result)

        result = self.resize_to_height(result)
        result = self.pad_to_width(result)
        return result

    def decode(self, pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        # Use greedy search. For complex tasks, you can use beam search
        results = ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :self.max_length]
        # Iterate over the results and get back the text
        output_text = []

        for res in results:
            res = self.num_to_char(res)
            res = reduce_join(res)
            res = res.numpy().decode("utf-8")
            output_text.append(res)
        return output_text

    def build_model(self, input_shape):
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
        output = Dense(len(self.characters) + 2, activation="softmax", name="dense2")(x)

        # Define the model
        self.model = Model(inputs=[input_img], outputs=output, name="ocr_model_v1")

