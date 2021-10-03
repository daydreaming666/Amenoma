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

MaterialsNameCHS = [
    "长生仙",
    "冒险阅历",
    "冒险家的经验",
    "特工祭刀",
    "燃愿玛瑙块",
    "燃愿玛瑙断片",
    "燃愿玛瑙",
    "燃愿玛瑙碎屑",
    "蓝染花鳉",
    "赤魔王",
    "赤穗酒枡",
    "杏仁",
    "天云草实",
    "紫晶块",
    "苹果",
    "孔雀木",
    "灰烬之心",
    "培根",
    "竹节",
    "竹笋",
    "玄岩之塔",
    "树莓",
    "斗棘鱼",
    "桦木",
    "鸟蛋",
    "漆黑陨铁的一角",
    "苦炮鲀",
    "黑铜号角",
    "黑晶号角",
    "血玉之枝",
    "蓝色染料",
    "凛风奔狼的断牙",
    "凛风奔狼的裂齿",
    "凛风奔狼的始龀",
    "凛风奔狼的怀乡",
    "璀璨原钻块",
    "璀璨原钻断片",
    "璀璨原钻",
    "璀璨原钻碎屑",
    "流纹褐蝶鱼",
    "黄油",
    "蝴蝶翅膀",
    "卷心菜",
    "嘟嘟莲",
    "胡萝卜",
    "塞西莉亚花",
    "狮牙斗士的铁链",
    "混沌枢纽",
    "混沌回路",
    "混沌炉心",
    "混沌装置",
    "混沌机关",
    "混沌真眼",
    "奶酪",
    "「冷鲜肉」",
    "漆黑陨铁的一块",
    "净水之心",
    "好感经验",
    "远海夷地的瑚枝",
    "石珀",
    "螃蟹",
    "蟹黄",
    "奶油",
    "智识之冕",
    "水晶块",
    "晶核",
    "水晶宴",
    "晶凝之华",
    "晶化骨髓",
    "水晶棱镜",
    "萃华木",
    "破损的面具",
    "蒲公英籽",
    "夤夜刻像",
    "擒霞客",
    "地脉的旧枝",
    "地脉的枯叶",
    "幽邃刻像",
    "高塔孤王的残垣",
    "血斛",
    "排异之露",
    "黯淡棱镜",
    "孤云寒林的神体",
    "导能绘卷",
    "龙王之冕",
    "狮牙斗士的理想",
    "鱼干",
    "东风之爪",
    "东风之翎",
    "东风的吐息",
    "电气水晶",
    "海皇香脂",
    "原素花蜜",
    "常燃火种",
    "布匹",
    "名刀镡",
    "腐殖龙髓",
    "狮牙斗士的枷锁",
    "牢固的箭簇",
    "杉木",
    "鱼肉",
    "烈焰花花蕊",
    "面粉",
    "禁咒绘卷",
    "石化的骨片",
    "禽肉",
    "脆弱的骨片",
    "高塔孤王的断片",
    "「童真的断篇」",
    "垂香木",
    "青蛙",
    "鎏金之鳞",
    "琉璃百合",
    "琉璃花鳉",
    "晦暗刻像",
    "远海夷地的金枝",
    "金赤假龙",
    "攫金鸦印",
    "漆黑陨铁的一粒",
    "「诗文」的指引",
    "「勤劳」的指引",
    "「风雅」的指引",
    "「自由」的指引",
    "「黄金」的指引",
    "「天光」的指引",
    "「繁荣」的指引",
    "「抗争」的指引",
    "「浮世」的指引",
    "火腿",
    "沉重号角",
    "狱火之蝶",
    "大英雄的经验",
    "极寒之核",
    "马尾",
    "猎兵祭刀",
    "飓风之种",
    "督察长祭刀",
    "铁块",
    "远海夷地的琼枝",
    "果酱",
    "远海夷地的玉枝",
    "绝云椒椒",
    "未熟之玉",
    "影打刀镡",
    "灯纸纤维",
    "堇瓜",
    "地脉的新芽",
    "尉官的徽记",
    "雷光棱镜",
    "蜥蜴尾巴",
    "鳅鳅宝玉",
    "莲蓬",
    "发光髓",
    "孤云寒林的光砂",
    "肺棘鱼",
    "孤云寒林的辉岩",
    "魔晶块",
    "枫木",
    "魔偶机心",
    "今昔剧画之鬼人",
    "今昔剧画之一角",
    "今昔剧画之虎啮",
    "今昔剧画之恶尉",
    "松茸",
    "花鳉",
    "牛奶",
    "薄荷",
    "冰雾花花朵",
    "雾虚草囊",
    "雾虚花粉",
    "雾虚灯芯",
    "雾海云间的金丹",
    "雾海云间的铅丹",
    "雾海云间的汞丹",
    "雾海云间的转还",
    "熔毁之刻",
    "摩拉",
    "蘑菇",
    "生长碧翡块",
    "生长碧翡断片",
    "生长碧翡",
    "生长碧翡碎屑",
    "鸣草",
    "鸣神御灵的亲爱",
    "鸣神御灵的欢喜",
    "鸣神御灵的勇武",
    "鸣神御灵的明惠",
    "夜泊石",
    "北陆弓原胚",
    "北陆法器原胚",
    "北陆双手剑原胚",
    "北陆长柄武器原胚",
    "北陆单手剑原胚",
    "破旧的刀镡",
    "不祥的面具",
    "鬼兜虫",
    "洋葱",
    "御伽木",
    "胡椒",
    "恒常机关之心",
    "慕风蘑菇",
    "「诗文」的哲学",
    "「勤劳」的哲学",
    "「风雅」的哲学",
    "「自由」的哲学",
    "「黄金」的哲学",
    "「天光」的哲学",
    "「繁荣」的哲学",
    "「抗争」的哲学",
    "「浮世」的哲学",
    "漆黑陨铁的一片",
    "松果",
    "松木",
    "浮生石片",
    "偏光棱镜",
    "土豆",
    "原石",
    "坚牢黄玉块",
    "坚牢黄玉断片",
    "坚牢黄玉",
    "坚牢黄玉碎屑",
    "炮鲀",
    "流纹京紫蝶鱼",
    "清心",
    "白萝卜",
    "雷鸣仙",
    "兽肉",
    "新兵的徽记",
    "红色染料",
    "孤云寒林的圣骸",
    "稻米",
    "北风之环",
    "锖假龙",
    "绯樱绣球",
    "盐",
    "却砂木",
    "珊瑚真珠",
    "香肠",
    "高塔孤王的碎梦",
    "海灵芝",
    "海草",
    "封魔绘卷",
    "士官的徽记",
    "狮牙斗士的镣铐",
    "武炼之魂·孤影",
    "魔王之刃·残片",
    "锐利的箭簇",
    "微光花蜜",
    "哀叙冰玉块",
    "哀叙冰玉断片",
    "哀叙冰玉",
    "哀叙冰玉碎屑",
    "虾仁",
    "霓裳花",
    "天原银莲",
    "藏银鸦印",
    "史莱姆原浆",
    "史莱姆凝液",
    "史莱姆清",
    "小灯草",
    "熏鱼",
    "熏禽肉",
    "阴燃之珠",
    "金鱼草",
    "雪中君",
    "浮游幽核",
    "浮游干核",
    "浮游晶化核",
    "北风的魂匣",
    "污秽的面具",
    "星螺",
    "星银矿石",
    "雷霆数珠",
    "奇异的「牙齿」",
    "结实的骨片",
    "糖",
    "日落果",
    "甜甜花",
    "甜甜花鳉",
    "北风之尾",
    "「诗文」的教导",
    "「勤劳」的教导",
    "「风雅」的教导",
    "「自由」的教导",
    "「黄金」的教导",
    "「天光」的教导",
    "「繁荣」的教导",
    "「抗争」的教导",
    "「浮世」的教导",
    "流纹茶蝶鱼",
    "「看得见的风」",
    "高塔孤王的破瓦",
    "豆腐",
    "番茄",
    "寻宝鸦印",
    "吞天之鲸·只角",
    "鳗肉",
    "最胜紫晶块",
    "最胜紫晶断片",
    "最胜紫晶",
    "最胜紫晶碎屑",
    "落落莓",
    "涤净青金块",
    "涤净青金断片",
    "涤净青金",
    "涤净青金碎屑",
    "自在松石块",
    "自在松石断片",
    "自在松石",
    "自在松石碎屑",
    "鸩棘鱼",
    "琉璃袋",
    "汲取了生命力的龙牙",
    "流浪者的经验",
    "历战的箭簇",
    "小麦",
    "白铁块",
    "骗骗花蜜",
    "灯芯绒材",
    "风车菊",
    "钩钩果",
    "黄色染料",
    "梦见木",
]


def gen_num():
    return str(np.random.randint(0, 9999))


def gen_material_name():
    return np.random.choice(MaterialsNameCHS, size=1)[0]


def generate_material():
    info_train1 = [gen_material_name(), gen_num()]
    info_train2 = [gen_material_name(), gen_num()]
    info_train3 = [gen_material_name(), gen_num()]
    info_train4 = [gen_material_name(), gen_num()]
    info_train5 = [gen_material_name(), gen_num()]
    info_train6 = [gen_material_name(), gen_num()]
    info_train7 = [gen_material_name(), gen_num()]
    info_train8 = [gen_material_name(), gen_num()]
    imgs1 = generate_images(info_train1)
    imgs2 = generate_images(info_train2)
    imgs3 = generate_images(info_train3)
    imgs4 = generate_images(info_train4)
    imgs5 = generate_images(info_train5)
    imgs6 = generate_images(info_train6)
    imgs7 = generate_images(info_train7)
    imgs8 = generate_images(info_train8)
    info = {"name1": imgs1[0], "amount1": imgs1[1],
            "name2": imgs2[0], "amount2": imgs2[1],
            "name3": imgs3[0], "amount3": imgs3[1],
            "name4": imgs4[0], "amount4": imgs4[1],
            "name5": imgs5[0], "amount5": imgs5[1],
            "name6": imgs6[0], "amount6": imgs6[1],
            "name7": imgs7[0], "amount7": imgs7[1],
            "name8": imgs8[0], "amount8": imgs8[1]
            }
    expect_info = {"name1": info_train1[0], "amount1": info_train1[1],
                   "name2": info_train2[0], "amount2": info_train2[1],
                   "name3": info_train3[0], "amount3": info_train3[1],
                   "name4": info_train4[0], "amount4": info_train4[1],
                   "name5": info_train5[0], "amount5": info_train5[1],
                   "name6": info_train6[0], "amount6": info_train6[1],
                   "name7": info_train7[0], "amount7": info_train7[1],
                   "name8": info_train8[0], "amount8": info_train8[1]
                   }
    return info, expect_info


def train_generator():
    q = 0
    while True:
        q += 1
        # gen = np.random.choice([generate_artifact, generate_material], size=1)[0]
        info, expect_info = generate_material()
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
            **{'star': detect_star(art_img), 'locked': detect_lock(art_img)}}


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


filepath = "./train/materials-weights-improvement-{epoch:02d}-{ctc_accu:.2f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='ctc_accu', verbose=1, save_best_only=True,
                                                mode='max')
reduce = keras.callbacks.ReduceLROnPlateau(monitor='ctc_accu', factor=0.5, min_lr=1e-7, verbose=1, patience=5)

callbacks_list = [reduce, checkpoint]

opt = keras.optimizers.Adam()
model.compile(loss=ctc_loss, optimizer=opt, metrics=[CTCAccuracy('ctc_accu')])
model.run_eagerly = True
model.summary()

model.fit(x=train_generator(), steps_per_epoch=8192, epochs=1)
model.fit(x=train_generator(), steps_per_epoch=4096, epochs=2)
model.fit(x=train_generator(), steps_per_epoch=2048, epochs=4)
model.fit(x=train_generator(), steps_per_epoch=1024, epochs=16)


history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=512, callbacks=callbacks_list)
