import json
import random as rd

import numpy as np
import tensorflow as tf
from PIL import ImageFont, Image, ImageDraw
from tensorflow import keras
from tensorflow.keras.backend import ctc_decode
from tensorflow.keras.layers import Input, Reshape, Dense, Dropout, Bidirectional, LSTM
from tensorflow.keras.layers.experimental.preprocessing import StringLookup
from tensorflow.keras.models import Model
from tensorflow.strings import reduce_join

from mobilenetv3 import MobileNetV3_Small

import ArtScanner.ArtsInfo as Info

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
    equipped_coords = [105, 1060, 500, 1100]
    lock_coords = [570, 405, 620, 455]


import json

import numpy as np
from PIL import ImageFont, Image, ImageDraw

MainAttrDatabase = json.load(open('../ArtScanner/Tools/ReliquaryLevelExcelConfigData.json'))
SubAttrDatabase = json.load(open('../ArtScanner/Tools/ReliquaryAffixExcelConfigData.json'))

Users_EN = list(Info.UsersEN.keys())

def gen_artifact_name():
    return np.random.choice(sum(Info.ArtNames_EN, []), size=1)[0]


def gen_type():
    return np.random.choice(Info.TypeNames_EN, size=1)[0]


def gen_main_attr_name():
    return np.random.choice(list(Info.MainAttrNames_EN.values()), size=1)[0]


def gen_main_attr_value():
    main_attr_id = np.random.choice(list(Info.MainAttrNames_EN.keys()), size=1)[0]
    value = np.random.choice(
        sum([[j['Value'] for j in i['AddProps'] if j['PropType'] == main_attr_id] for i in MainAttrDatabase], []),
        size=1)[0]
    return Info.Formats[main_attr_id].format(value)


def gen_level():
    n = 1
    return ["+" + str(i) for i in np.random.randint(0, 21, size=n)][0]


def gen_equipped():
    return 'Equipped: ' + np.random.choice(Users_EN, size=1)[0]


def gen_single_sub_attr():
    sub_attr_id = np.random.choice(list(Info.SubAttrNames_EN.keys()), size=1)[0]
    rare_sub_attr_ranges = [
        [i['PropValue'] for i in SubAttrDatabase if i['DepotId'] == j and i['PropType'] == sub_attr_id] for j in
        [101, 201, 301, 401, 501]]
    rare = np.random.choice(5, p=[0.0625, 0.0625, 0.125, 0.25, 0.5])
    n_upgrades = np.random.randint(1, rare + 3)
    sub_attr_value = np.random.choice(rare_sub_attr_ranges[rare], size=n_upgrades).sum()
    return Info.SubAttrNames_EN[sub_attr_id] + '+' + Info.Formats[sub_attr_id].format(sub_attr_value)


def gen_sub_attrs(n=1):
    return [gen_single_sub_attr() for _ in range(n)]


def generate_artifact():
    sub_attrs_num = rd.randrange(1, 5)
    info_train = [gen_artifact_name(), gen_type(), gen_main_attr_name(), gen_main_attr_value(),
                  gen_level(), gen_equipped(), *gen_sub_attrs(sub_attrs_num)]
    imgs = generate_images(info_train)
    info = {"name": imgs[0],
            "type": imgs[1],
            "main_attr_name": imgs[2],
            "main_attr_value": imgs[3],
            "level": imgs[4],
            "equipped": imgs[5]
            }
    expect_info = {"name": info_train[0],
                   "type": info_train[1],
                   "main_attr_name": info_train[2],
                   "main_attr_value": info_train[3],
                   "level": info_train[4],
                   "equipped": info_train[5]
                   }
    for i in range(sub_attrs_num):
        info[f'subattr_{i + 1}'] = imgs[i + 6]
        expect_info[f'subattr_{i + 1}'] = info_train[i + 6]
    return info, expect_info


def train_generator():
    q = 0
    while True:
        q += 1
        # gen = np.random.choice([generate_artifact, generate_material], size=1)[0]
        info, expect_info = generate_artifact()
        x = np.concatenate([preprocess(info[key]).T[None, :, :, None]
                            for key in sorted(info.keys())], axis=0)
        f = [list(expect_info[key]) for key in sorted(expect_info.keys())]
        w = []
        for lst in f:
            w.append([i.encode('utf-8') for i in lst] + [b''] * (max_length - len(lst)))
        y = char_to_num(w)
        yield x, y
    return


def generate_image_EN(text, font_size_range=(20, 45)):
    pos = np.random.randint(0, 10), np.random.randint(0, 10)
    backcolor = (
        np.random.randint(150, 255),
        np.random.randint(150, 255),
        np.random.randint(150, 255),
    )
    forecolor = (
        np.random.randint(0, 75),
        np.random.randint(0, 75),
        np.random.randint(0, 75),
    )
    img = Image.new("RGB", (770, 60), backcolor)
    draw = ImageDraw.Draw(img)
    if len(text) >= 35:
        font_size_range = (30, 50)
        txt1 = text[:-len(text.split(" ")[-1])]
        txt2 = text[-len(text.split(" ")[-1]):]
        font_size = int(np.random.randint(*font_size_range) / 2)
        font = fonts[font_size]
        pos2 = pos[0], pos[1] + int(font_size * 1.2)
        draw.text(pos, txt1, forecolor, font=font)
        draw.text(pos2, txt2, forecolor, font=font)
    else:
        draw.text(pos, text, forecolor, font=fonts[np.random.randint(*font_size_range)])
    draw = ImageDraw.Draw(img)
    return img


def generate_images(texts, font_size_range=(15, 40)):
    result = []
    for text in texts:
        result.append(generate_image_EN(text, font_size_range=font_size_range))
    #     return np.array(result)
    return result


fonts = {i: ImageFont.truetype("../ArtScanner/rcc/genshin.ttf", i) for i in range(10, 100)}


# 灰度
def to_gray(text_img):
    text_img = np.array(text_img)
    if len(text_img.shape) > 2:
        text_img = (text_img[..., :3] @ [[[0.299], [0.587], [0.114]]])[:, :, 0]
    return np.array(text_img, np.float32)


def normalize(img, auto_inverse=True):
    img -= img.min()
    img /= img.max()
    if auto_inverse and img[-1, -1] > 0.5:
        img = 1 - img
    return img


def resize_to_height(img):
    global height
    height_ = height
    return (
            np.array(
                Image.fromarray(np.uint8(img * 255)).resize(
                    (int(img.shape[1] * height_ / img.shape[0]), height_),
                    Image.BILINEAR, )
            ) / 255)


def pad_to_width(img):
    global width
    width_ = width

    if img.shape[1] >= width_:
        return img[:, :width_]

    return np.pad(
        img, [[0, 0], [0, width_ - img.shape[1]]], mode="constant", constant_values=0
    )


# 裁剪
def crop(img, tol=0.7):
    # img is 2D image data
    # tol  is tolerance
    mask = img > tol
    m, n = img.shape
    mask0, mask1 = mask.any(0), mask.any(1)
    col_start, col_end = mask0.argmax(), n - mask0[::-1].argmax()
    row_start, row_end = mask1.argmax(), m - mask1[::-1].argmax()
    #     print(row_end-row_start, col_end-col_start)
    return img[row_start:row_end, col_start:col_end]


# 二值化 -- 删除背景
def binarization(img, thresh=0.5):
    return np.where((img < thresh), 0, img)


def resplice(img):
    line_height = 27
    if (img[30] == 0.).all():
        res1 = img[:line_height, :]
        res2 = img[-line_height:, :]
        space = np.zeros((res1.shape[0], 10))
        res = np.concatenate((res1, space, res2), axis=1)
        return crop(res, tol=0)
    else:
        return img


def zoom(img):
    height_ = 60
    return (
            np.array(
                Image.fromarray(np.uint8(img * 255)).resize(
                    (int(img.shape[1] * height_ / img.shape[0]), height_),
                    Image.BILINEAR, )
            ) / 255)


def preprocess(text_img):
    result = to_gray(text_img)
    result = normalize(result, True)
    result = binarization(result)
    result = crop(result, tol=0)

    result = zoom(result)
    result = resplice(result)

    result = resize_to_height(result)
    result = pad_to_width(result)
    return result


def decode(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :max_length]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = num_to_char(res)
        res = reduce_join(res)
        res = res.numpy().decode("utf-8")
        output_text.append(res)
    return output_text


@tf.autograph.experimental.do_not_convert
def ctc_loss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.math.count_nonzero(y_true, axis=-1, keepdims=True)

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    return keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)


# A utility function to decode the output of the network
def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
              :, :max_length
              ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = num_to_char(res)
        res = tf.strings.reduce_join(res)
        res = res.numpy().decode("utf-8")
        output_text.append(res)
    return output_text


class CTCAccuracy(tf.keras.metrics.Metric):
    def __init__(self, name='ctc_accuracy', **kwargs):
        super(CTCAccuracy, self).__init__(name=name, **kwargs)
        self.correct_count = 0
        self.all_count = 0

    def update_state(self, y_true, y_pred, sample_weight=None):
        pred_text = decode_batch_predictions(y_pred)
        self.all_count += len(pred_text)
        true_text = []
        for res in y_true:
            res = num_to_char(res)
            res = tf.strings.reduce_join(res)
            res = res.numpy().decode("utf-8")
            true_text.append(res)
        self.correct_count += sum([i == j for i, j in zip(pred_text, true_text)])

    def result(self):
        return self.correct_count / self.all_count

    def reset_states(self):
        self.correct_count = 0
        self.all_count = 0


# def train_generator():
#     q = 0
#     while True:
#         q += 1
#         sub_attrs_num = rd.randrange(1, 5)
#         info_train = [gen_name(), gen_type(), gen_main_attr_name(), gen_main_attr_value(),
#                       gen_level(), *gen_sub_attrs(sub_attrs_num)]
#         imgs = generate_images(info_train)
#         info = {"name": imgs[0],
#                 "type": imgs[1],
#                 "main_attr_name": imgs[2],
#                 "main_attr_value": imgs[3],
#                 "level": imgs[4],
#                 }
#         expect_info = {"name": info_train[0],
#                        "type": info_train[1],
#                        "main_attr_name": info_train[2],
#                        "main_attr_value": info_train[3],
#                        "level": info_train[4]}
#         for i in range(sub_attrs_num):
#             info[f'subattr_{i + 1}'] = imgs[i + 5]
#             expect_info[f'subattr_{i + 1}'] = info_train[i + 5]
#         x = np.concatenate([preprocess(info[key]).T[None, :, :, None] for key in sorted(info.keys())], axis=0)
#
#         f = [list(expect_info[key]) for key in sorted(expect_info.keys())]
#         w = []
#         for lst in f:
#             w.append([i.encode('utf-8') for i in lst] + [b''] * (max_length - len(lst)))
#         y = char_to_num(w)
#         yield x, y
#     return


characters = sorted(
    [
        *set(
            "".join(
                sum(Info.ArtNames_EN, [])
                + Info.TypeNames_EN
                + list(Info.MainAttrNames_EN.values())
                + list(Info.SubAttrNames_EN.values())
                + list(".,+%0123456789")
                + list(Users_EN)
                + list('Equipped: ')
            )
        )
    ]
)

char_to_num = StringLookup(
    vocabulary=list(characters), num_oov_indices=0, mask_token="")
num_to_char = StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", mask_token="", invert=True)

width = 384
height = 16
max_length = 40
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
x = Dense(96, activation="relu", name="dense1")(x)
x = Dropout(0.2)(x)

# RNNs
x = Bidirectional(LSTM(192, return_sequences=True, dropout=0.25))(x)
x = Bidirectional(LSTM(96, return_sequences=True, dropout=0.25))(x)

# Output layer
output = Dense(len(characters) + 2, activation="softmax", name="dense2")(x)

# Define the model
model = Model(inputs=[input_img], outputs=output, name="ocr_model_en")

opt = keras.optimizers.Adam()
model.compile(loss=ctc_loss, optimizer=opt, metrics=[CTCAccuracy('ctc_accu')])
model.run_eagerly = True
model.summary()

filepath = "./train/artifact-weights-improvement-EN-{epoch:02d}-{ctc_accu:.3f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='ctc_accu', verbose=1, save_best_only=True,
                                                mode='max')
reduce = keras.callbacks.ReduceLROnPlateau(monitor='ctc_accu', factor=0.5, min_lr=1e-7, verbose=1, patience=5)
callbacks_list = [reduce, checkpoint]

# -- train model --
# history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=168, callbacks=callbacks_list)
# history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=168, callbacks=callbacks_list)


# -- test functions --

scale_ratio = 0.625


def extract_art_info_EN(art_img):
    name = art_img.crop([i * scale_ratio for i in Config_EN.name_coords])
    type = art_img.crop([i * scale_ratio for i in Config_EN.type_coords])
    main_attr_name = art_img.crop([i * scale_ratio for i in Config_EN.main_attr_name_coords])
    main_attr_value = art_img.crop([i * scale_ratio for i in Config_EN.main_attr_value_coords])
    level = art_img.crop([i * scale_ratio for i in Config_EN.level_coords])
    subattr_1 = art_img.crop([i * scale_ratio for i in Config_EN.subattr_1_coords])  # [73, 83, 102]
    subattr_2 = art_img.crop([i * scale_ratio for i in Config_EN.subattr_2_coords])
    subattr_3 = art_img.crop([i * scale_ratio for i in Config_EN.subattr_3_coords])
    subattr_4 = art_img.crop([i * scale_ratio for i in Config_EN.subattr_4_coords])
    equipped = art_img.crop([i * scale_ratio for i in Config_EN.equipped_coords])
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
    return {key: value for key, value in locals().items() if key not in ['art_img']}


model.fit(x=train_generator(), steps_per_epoch=8192, epochs=1)
model.fit(x=train_generator(), steps_per_epoch=4096, epochs=2)
model.fit(x=train_generator(), steps_per_epoch=2048, epochs=4)
model.fit(x=train_generator(), steps_per_epoch=1024, epochs=8)

history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=512, callbacks=callbacks_list)

