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

MainAttrDatabase = json.load(open('../ReliquaryLevelExcelConfigData.json'))
SubAttrDatabase = json.load(open('../ReliquaryAffixExcelConfigData.json'))

Formats = {
    "FIGHT_PROP_CRITICAL": "{:.1%}",
    "FIGHT_PROP_CRITICAL_HURT": "{:.1%}",
    "FIGHT_PROP_ATTACK": "{:,.0f}",
    "FIGHT_PROP_ATTACK_PERCENT": "{:.1%}",
    "FIGHT_PROP_ELEMENT_MASTERY": "{:,.0f}",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "{:.1%}",
    "FIGHT_PROP_HP": "{:,.0f}",
    "FIGHT_PROP_HP_PERCENT": "{:.1%}",
    "FIGHT_PROP_DEFENSE": "{:,.0f}",
    "FIGHT_PROP_DEFENSE_PERCENT": "{:.1%}",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_HEAL_ADD": "{:.1%}",
    "FIGHT_PROP_ROCK_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_WIND_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_ICE_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_WATER_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_FIRE_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_ELEC_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_GRASS_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_FIRE_SUB_HURT": "{:.1%}",
}

MainAttrNames = {
    "FIGHT_PROP_CRITICAL": "暴击率",
    "FIGHT_PROP_CRITICAL_HURT": "暴击伤害",
    "FIGHT_PROP_ATTACK": "攻击力",
    "FIGHT_PROP_ATTACK_PERCENT": "攻击力",
    "FIGHT_PROP_ELEMENT_MASTERY": "元素精通",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
    "FIGHT_PROP_HP": "生命值",
    "FIGHT_PROP_HP_PERCENT": "生命值",
    "FIGHT_PROP_DEFENSE": "防御力",
    "FIGHT_PROP_DEFENSE_PERCENT": "防御力",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "物理伤害加成",
    "FIGHT_PROP_HEAL_ADD": "治疗加成",
    "FIGHT_PROP_ROCK_ADD_HURT": "岩元素伤害加成",
    "FIGHT_PROP_WIND_ADD_HURT": "风元素伤害加成",
    "FIGHT_PROP_ICE_ADD_HURT": "冰元素伤害加成",
    "FIGHT_PROP_WATER_ADD_HURT": "水元素伤害加成",
    "FIGHT_PROP_FIRE_ADD_HURT": "火元素伤害加成",
    "FIGHT_PROP_ELEC_ADD_HURT": "雷元素伤害加成",
}
AttrName2Ids = {v: i.replace('_PERCENT', '') for i, v in MainAttrNames.items()}

TypeNames = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]

SubAttrNames = {
    "FIGHT_PROP_CRITICAL": "暴击率",
    "FIGHT_PROP_CRITICAL_HURT": "暴击伤害",
    "FIGHT_PROP_ATTACK": "攻击力",
    "FIGHT_PROP_ATTACK_PERCENT": "攻击力",
    "FIGHT_PROP_ELEMENT_MASTERY": "元素精通",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
    "FIGHT_PROP_HP": "生命值",
    "FIGHT_PROP_HP_PERCENT": "生命值",
    "FIGHT_PROP_DEFENSE": "防御力",
    "FIGHT_PROP_DEFENSE_PERCENT": "防御力",
}

ArtNames = [
    ["磐陀裂生之花", "嵯峨群峰之翼", "星罗圭璧之晷", "巉岩琢塑之樽", "不动玄石之相"],
    ["历经风雪的思念", "摧冰而行的执望", "冰雪故园的终期", "遍结寒霜的傲骨", "破冰踏雪的回音"],
    ["染血的铁之心", "染血的黑之羽", "骑士染血之时", "染血骑士之杯", "染血的铁假面"],
    ["魔女的炎之花", "魔女常燃之羽", "魔女破灭之时", "魔女的心之火", "焦灼的魔女帽"],
    ["角斗士的留恋", "角斗士的归宿", "角斗士的希冀", "角斗士的酣醉", "角斗士的凯旋"],
    ["饰金胸花", "追忆之风", "坚铜罗盘", "沉波之盏", "酒渍船帽"],
    ["渡火者的决绝", "渡火者的解脱", "渡火者的煎熬", "渡火者的醒悟", "渡火者的智慧"],
    ["远方的少女之心", "少女飘摇的思念", "少女苦短的良辰", "少女片刻的闲暇", "少女易逝的芳颜"],
    ["宗室之花", "宗室之翎", "宗室时计", "宗室银瓮", "宗室面具"],
    ["夏祭之花", "夏祭终末", "夏祭之刻", "夏祭水玉", "夏祭之面"],
    ["平雷之心", "平雷之羽", "平雷之刻", "平雷之器", "平雷之冠"],
    ["雷鸟的怜悯", "雷灾的孑遗", "雷霆的时计", "降雷的凶兆", "唤雷的头冠"],
    ["野花记忆的绿野", "猎人青翠的箭羽", "翠绿猎人的笃定", "翠绿猎人的容器", "翠绿的猎人之冠"],
    ["乐团的晨光", "琴师的箭羽", "终幕的时计", "吟游者之壶", "指挥的礼帽"],
    ["战狂的蔷薇", "战狂的翎羽", "战狂的时计", "战狂的骨杯", "战狂的鬼面"],
    ["勇士的勋章", "勇士的期许", "勇士的坚毅", "勇士的壮行", "勇士的冠冕"],
    ["守护之花", "守护徽印", "守护座钟", "守护之皿", "守护束带"],
    ["流放者之花", "流放者之羽", "流放者怀表", "流放者之杯", "流放者头冠"],
    ["赌徒的胸花", "赌徒的羽饰", "赌徒的怀表", "赌徒的骰盅", "赌徒的耳环"],
    ["教官的胸花", "教官的羽饰", "教官的怀表", "教官的茶杯", "教官的帽子"],
    ["武人的红花", "武人的羽饰", "武人的水漏", "武人的酒杯", "武人的头巾"],
    ["祭水礼冠"],
    ["祭火礼冠"],
    ["祭雷礼冠"],
    ["祭冰礼冠"],
    ["故人之心", "归乡之羽", "逐光之石", "异国之盏", "感别之冠"],
    ["学士的书签", "学士的羽笔", "学士的时钟", "学士的墨杯", "学士的镜片"],
    ["奇迹之花", "奇迹之羽", "奇迹之沙", "奇迹之杯", "奇迹耳坠"],
    ["冒险家之花", "冒险家尾羽", "冒险家怀表", "冒险家金杯", "冒险家头带"],
    ["幸运儿绿花", "幸运儿鹰羽", "幸运儿沙漏", "幸运儿之杯", "幸运儿银冠"],
    ["游医的银莲", "游医的枭羽", "游医的怀钟", "游医的药壶", "游医的方巾"],
    ["勋绩之花", "昭武翎羽", "金铜时晷", "盟誓金爵", "将帅兜鍪"],
    ["无垢之花", "贤医之羽", "停摆之刻", "超越之盏", "嗤笑之面"],
    ["明威之镡", "切落之羽", "雷云之笼", "绯花之壶", "华饰之兜"],  # 绝缘之旗印
    ["羁缠之花", "思忆之矢", "朝露之时", "祈望之心", "无常之面"],  # 追忆之注连
    ["祝圣精华", "祝圣油膏"],                                  # 强化材料
]

Users = [
    "空",
    "荧",
    "安柏",
    "凯亚",
    "丽莎",
    "琴",
    "可莉",
    "诺艾尔",
    "芭芭拉",
    "温迪",
    "雷泽",
    "迪卢克",
    "班尼特",
    "菲谢尔",
    "北斗",
    "凝光",
    "香菱",
    "行秋",
    "重云",
    "砂糖",
    "莫娜",
    "刻晴",
    "七七",
    "达达利亚",
    "迪奥娜",
    "钟离",
    "辛焱",
    "阿贝多",
    "甘雨",
    "魈",
    "胡桃",
    "罗莎莉亚",
    "烟绯",
    "优菈",
    "埃洛伊",
    "珊瑚宫心海",
    "雷电将军",
    "九条裟罗",
    "早柚",
    "宵宫",
    "神里绫华",
    "枫原万叶",
    "托马"
]


def gen_num():
    return str(np.random.randint(0, 9999))


def gen_artifact_name():
    return np.random.choice(sum(ArtNames, []), size=1)[0]


def gen_type():
    return np.random.choice(TypeNames, size=1)[0]


def gen_main_attr_name():
    return np.random.choice(list(MainAttrNames.values()), size=1)[0]


def gen_main_attr_value():
    main_attr_id = np.random.choice(list(MainAttrNames.keys()), size=1)[0]
    value = np.random.choice(
        sum([[j['Value'] for j in i['AddProps'] if j['PropType'] == main_attr_id] for i in MainAttrDatabase], []),
        size=1)[0]
    return Formats[main_attr_id].format(value)


def gen_level():
    n = 1
    return ["+" + str(i) for i in np.random.randint(0, 21, size=n)][0]


def gen_equipped():
    return np.random.choice(Users, size=1)[0] + "已装备"


def gen_single_sub_attr():
    sub_attr_id = np.random.choice(list(SubAttrNames.keys()), size=1)[0]
    rare_sub_attr_ranges = [
        [i['PropValue'] for i in SubAttrDatabase if i['DepotId'] == j and i['PropType'] == sub_attr_id] for j in
        [101, 201, 301, 401, 501]]
    rare = np.random.choice(5, p=[0.0625, 0.0625, 0.125, 0.25, 0.5])
    n_upgrades = np.random.randint(1, rare + 3)
    sub_attr_value = np.random.choice(rare_sub_attr_ranges[rare], size=n_upgrades).sum()
    return SubAttrNames[sub_attr_id] + '+' + Formats[sub_attr_id].format(sub_attr_value)


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


def generate_image(text, font_size_range=(15, 40)):
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
    img = Image.new("RGB", (550, 55), backcolor)
    draw = ImageDraw.Draw(img)
    draw.text(pos, text, forecolor, font=fonts[np.random.randint(*font_size_range)])
    draw = ImageDraw.Draw(img)
    return img


def generate_images(texts, font_size_range=(15, 40)):
    result = []
    for text in texts:
        result.append(generate_image(text, font_size_range=font_size_range))
    #     return np.array(result)
    return result


fonts = {i: ImageFont.truetype("../genshin.ttf", i) for i in range(10, 100)}


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


def resize_to_height(img):
    global height
    height_ = height
    return (
            np.array(
                Image.fromarray(np.uint8(img * 255)).resize(
                    (int(img.shape[1] * height_ / img.shape[0]), height_),
                    Image.BILINEAR, )
            ) / 255)


def binarization(img, thresh=0.5):
    return np.where((img < thresh), 0, img)


def pad_to_width(img):
    global width
    width_ = width
    if img.shape[1] >= width_:
        return img[:, :width_]
    return np.pad(
        img, [[0, 0], [0, width_ - img.shape[1]]], mode="constant", constant_values=0
    )


def preprocess(text_img):
    result = to_gray(text_img)
    result = normalize(result, True)
    result = binarization(result)
    result = crop(result)
    result = normalize(result, False)
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


scale_ratio = 1
characters = sorted(
    [
        *set(
            "".join(
                sum(ArtNames, [])
                + TypeNames
                + list(MainAttrNames.values())
                + list(SubAttrNames.values())
                + list(".,+%0123456789")
                + list(Users)
                + list("已装备")
                # + list(MaterialsNameCHS)
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

opt = keras.optimizers.Adam()
model.compile(loss=ctc_loss, optimizer=opt, metrics=[CTCAccuracy('ctc_accu')])
model.run_eagerly = True
model.summary()


# test functions
class Config:
    name_coords = [33, 8, 619, 69]
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


def extract_art_info(art_img):
    name = art_img.crop([i * scale_ratio for i in Config.name_coords])
    type = art_img.crop([i * scale_ratio for i in Config.type_coords])
    main_attr_name = art_img.crop([i * scale_ratio for i in Config.main_attr_name_coords])
    main_attr_value = art_img.crop([i * scale_ratio for i in Config.main_attr_value_coords])
    level = art_img.crop([i * scale_ratio for i in Config.level_coords])
    subattr_1 = art_img.crop([i * scale_ratio for i in Config.subattr_1_coords])  # [73, 83, 102]
    subattr_2 = art_img.crop([i * scale_ratio for i in Config.subattr_2_coords])
    subattr_3 = art_img.crop([i * scale_ratio for i in Config.subattr_3_coords])
    subattr_4 = art_img.crop([i * scale_ratio for i in Config.subattr_4_coords])
    equipped = art_img.crop([i * scale_ratio for i in Config.equipped_coords])
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


def detect_info(art_img):
    info = extract_art_info(art_img)
    x = np.concatenate([preprocess(info[key]).T[None, :, :, None] for key in sorted(info.keys())], axis=0)
    y = model.predict(x)
    y = decode(y)
    return {**{key: v for key, v in zip(sorted(info.keys()), y)},
            **{'star': detect_star(art_img),
               'locked': detect_lock(art_img)}}


def detect_star(art_img):
    star = art_img.crop([i * scale_ratio for i in Config.star_coords])
    cropped_star = crop(normalize(to_gray(star)))
    coef = cropped_star.shape[1] / cropped_star.shape[0]
    coef = coef / 1.30882352 + 0.21568627
    return int(round(coef))


def detect_lock(img) -> bool:
    lock = img.crop([i * scale_ratio for i in Config.lock_coords])
    result = to_gray(lock)
    result = normalize(result, auto_inverse=False)
    result = np.where((result < 0.5), 0, 1)
    return np.add.reduce(np.add.reduce(result)) < 500


filepath = "./train/artifact-weights-improvement-{epoch:02d}-{ctc_accu:.2f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='ctc_accu', verbose=1, save_best_only=True,
                                                mode='max')
reduce = keras.callbacks.ReduceLROnPlateau(monitor='ctc_accu', factor=0.75, min_lr=1e-7, verbose=1, patience=3)

callbacks_list = [reduce, checkpoint]

# model.fit(x=train_generator(), steps_per_epoch=8192, epochs=1)
# model.fit(x=train_generator(), steps_per_epoch=4096, epochs=2)
# model.fit(x=train_generator(), steps_per_epoch=2048, epochs=4)
# model.fit(x=train_generator(), steps_per_epoch=1024, epochs=16)
#
# history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=128, callbacks=callbacks_list)
