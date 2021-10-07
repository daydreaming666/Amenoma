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

MaterialsNameEN = [
    "Abiding Angelfish",
    "Adventure EXP",
    "Adventurer's Experience",
    "Agent's Sacrificial Knife",
    "Agnidus Agate Chunk",
    "Agnidus Agate Fragment",
    "Agnidus Agate Gemstone",
    "Agnidus Agate Sliver",
    "Aizen Medaka",
    "Akai Maou",
    "Ako's Sake Vessel",
    "Almond",
    "Amakumo Fruit",
    "Amethyst Lump",
    "Apple",
    "Aralia Wood",
    "Ashen Heart",
    "Bacon",
    "Bamboo Segment",
    "Bamboo Shoot",
    "Basalt Pillar",
    "Berry",
    "Betta",
    "Birch Wood",
    "Bird Egg",
    "Bit of Aerosiderite",
    "Bitter Pufferfish",
    "Black Bronze Horn",
    "Black Crystal Horn",
    "Bloodjade Branch",
    "Blue Dye",
    "Boreal Wolf's Broken Fang",
    "Boreal Wolf's Cracked Tooth",
    "Boreal Wolf's Milk Tooth",
    "Boreal Wolf's Nostalgia",
    "Brilliant Diamond Chunk",
    "Brilliant Diamond Fragment",
    "Brilliant Diamond Gemstone",
    "Brilliant Diamond Sliver",
    "Brown Shirakodai",
    "Butter",
    "Butterfly Wings",
    "Cabbage",
    "Calla Lily",
    "Carrot",
    "Cecilia",
    "Chains of the Dandelion Gladiator",
    "Chaos Axis",
    "Chaos Circuit",
    "Chaos Core",
    "Chaos Device",
    "Chaos Gear",
    "Chaos Oculus",
    "Cheese",
    "Chilled Meat",
    "Chunk of Aerosiderite",
    "Cleansing Heart",
    "Companionship EXP",
    "Coral Branch of a Distant Sea",
    "Cor Lapis",
    "Crab",
    "Crab Roe",
    "Cream",
    "Crown of Insight",
    "Crystal Chunk",
    "Crystal Core",
    "Crystalfish",
    "Crystalline Bloom",
    "Crystal Marrow",
    "Crystal Prism",
    "Cuihua Wood",
    "Damaged Mask",
    "Dandelion Seed",
    "Dark Statuette",
    "Dawncatcher",
    "Dead Ley Line Branch",
    "Dead Ley Line Leaves",
    "Deathly Statuette",
    "Debris of Decarabian's City",
    "Dendrobium",
    "Dew of Repudiation",
    "Dismal Prism",
    "Divine Body from Guyun",
    "Divining Scroll",
    "Dragon Lord's Crown",
    "Dream of the Dandelion Gladiator",
    "Dried Fish",
    "Dvalin's Claw",
    "Dvalin's Plume",
    "Dvalin's Sigh",
    "Electro Crystal",
    "Emperor's Balsam",
    "Energy Nectar",
    "Everflame Seed",
    "Fabric",
    "Famed Handguard",
    "Festering Dragon Marrow",
    "Fetters of the Dandelion Gladiator",
    "Firm Arrowhead",
    "Fir Wood",
    "Fish",
    "Flaming Flower Stamen",
    "Flour",
    "Forbidden Curse Scroll",
    "Fossilized Bone Shard",
    "Fowl",
    "Fragile Bone Shard",
    "Fragment of Decarabian's Epic",
    "\"Fragments of Innocence\"",
    "Fragrant Cedar Wood",
    "Frog",
    "Gilded Scale",
    "Glaze Lily",
    "Glaze Medaka",
    "Gloomy Statuette",
    "Golden Branch of a Distant Sea",
    "Golden Koi",
    "Golden Raven Insignia",
    "Grain of Aerosiderite",
    "Guide to Ballad",
    "Guide to Diligence",
    "Guide to Elegance",
    "Guide to Freedom",
    "Guide to Gold",
    "Guide to Light",
    "Guide to Prosperity",
    "Guide to Resistance",
    "Guide to Transience",
    "Ham",
    "Heavy Horn",
    "Hellfire Butterfly",
    "Hero's Wit",
    "Hoarfrost Core",
    "Horsetail",
    "Hunter's Sacrificial Knife",
    "Hurricane Seed",
    "Inspector's Sacrificial Knife",
    "Iron Chunk",
    "Jade Branch of a Distant Sea",
    "Jam",
    "Jeweled Branch of a Distant Sea",
    "Jueyun Chili",
    "Juvenile Jade",
    "Kageuchi Handguard",
    "Lantern Fiber",
    "Lavender Melon",
    "Ley Line Sprout",
    "Lieutenant's Insignia",
    "Lightning Prism",
    "Lizard Tail",
    "Loach Pearl",
    "Lotus Head",
    "Luminescent Spine",
    "Luminous Sands from Guyun",
    "Lunged Stickleback",
    "Lustrous Stone from Guyun",
    "Magical Crystal Chunk",
    "Maple Wood",
    "Marionette Core",
    "Mask of the Kijin",
    "Mask of the One-Horned",
    "Mask of the Tiger's Bite",
    "Mask of the Wicked Lieutenant",
    "Matsutake",
    "Medaka",
    "Milk",
    "Mint",
    "Mist Flower Corolla",
    "Mist Grass",
    "Mist Grass Pollen",
    "Mist Grass Wick",
    "Mist Veiled Gold Elixir",
    "Mist Veiled Lead Elixir",
    "Mist Veiled Mercury Elixir",
    "Mist Veiled Primo Elixir",
    "Molten Moment",
    "Mora",
    "Mushroom",
    "Nagadus Emerald Chunk",
    "Nagadus Emerald Fragment",
    "Nagadus Emerald Gemstone",
    "Nagadus Emerald Sliver",
    "Naku Weed",
    "Narukami's Affection",
    "Narukami's Joy",
    "Narukami's Valor",
    "Narukami's Wisdom",
    "Noctilucous Jade",
    "Northlander Bow Billet",
    "Northlander Catalyst Billet",
    "Northlander Claymore Billet",
    "Northlander Polearm Billet",
    "Northlander Sword Billet",
    "Old Handguard",
    "Ominous Mask",
    "Onikabuto",
    "Onion",
    "Otogi Wood",
    "Pepper",
    "Perpetual Heart",
    "Philanemo Mushroom",
    "Philosophies of Ballad",
    "Philosophies of Diligence",
    "Philosophies of Elegance",
    "Philosophies of Freedom",
    "Philosophies of Gold",
    "Philosophies of Light",
    "Philosophies of Prosperity",
    "Philosophies of Resistance",
    "Philosophies of Transience",
    "Piece of Aerosiderite",
    "Pinecone",
    "Pine Wood",
    "Plaustrite Shard",
    "Polarizing Prism",
    "Potato",
    "Primogem",
    "Prithiva Topaz Chunk",
    "Prithiva Topaz Fragment",
    "Prithiva Topaz Gemstone",
    "Prithiva Topaz Sliver",
    "Pufferfish",
    "Purple Shirakodai",
    "Qingxin",
    "Radish",
    "Raimei Angelfish",
    "Raw Meat",
    "Recruit's Insignia",
    "Red Dye",
    "Relic from Guyun",
    "Rice",
    "Ring of Boreas",
    "Rusty Koi",
    "Sakura Bloom",
    "Salt",
    "Sandbearer Wood",
    "Sango Pearl",
    "Sausage",
    "Scattered Piece of Decarabian's Dream",
    "Sea Ganoderma",
    "Seagrass",
    "Sealed Scroll",
    "Sergeant's Insignia",
    "Shackles of the Dandelion Gladiator",
    "Shadow of the Warrior",
    "Shard of a Foul Legacy",
    "Sharp Arrowhead",
    "Shimmering Nectar",
    "Shivada Jade Chunk",
    "Shivada Jade Fragment",
    "Shivada Jade Gemstone",
    "Shivada Jade Sliver",
    "Shrimp Meat",
    "Silk Flower",
    "Silver Lotus",
    "Silver Raven Insignia",
    "Slime Concentrate",
    "Slime Condensate",
    "Slime Secretions",
    "Small Lamp Grass",
    "Smoked Fish",
    "Smoked Fowl",
    "Smoldering Pearl",
    "Snapdragon",
    "Snowstrider",
    "Spectral Heart",
    "Spectral Husk",
    "Spectral Nucleus",
    "Spirit Locket of Boreas",
    "Stained Mask",
    "Starconch",
    "Starsilver",
    "Storm Beads",
    "Strange Tooth",
    "Sturdy Bone Shard",
    "Sugar",
    "Sunsettia",
    "Sweet Flower",
    "Sweet-Flower Medaka",
    "Tail of Boreas",
    "Teachings of Ballad",
    "Teachings of Diligence",
    "Teachings of Elegance",
    "Teachings of Freedom",
    "Teachings of Gold",
    "Teachings of Light",
    "Teachings of Prosperity",
    "Teachings of Resistance",
    "Teachings of Transience",
    "Tea-Colored Shirakodai",
    "\"The Visible Winds\"",
    "Tile of Decarabian's Tower",
    "Tofu",
    "Tomato",
    "Treasure Hoarder Insignia",
    "Tusk of Monoceros Caeli",
    "Unagi Meat",
    "Vajrada Amethyst Chunk",
    "Vajrada Amethyst Fragment",
    "Vajrada Amethyst Gemstone",
    "Vajrada Amethyst Sliver",
    "Valberry",
    "Varunada Lazurite Chunk",
    "Varunada Lazurite Fragment",
    "Varunada Lazurite Gemstone",
    "Varunada Lazurite Sliver",
    "Vayuda Turquoise Chunk",
    "Vayuda Turquoise Fragment",
    "Vayuda Turquoise Gemstone",
    "Vayuda Turquoise Sliver",
    "Venomspine Fish",
    "Violetgrass",
    "Vitalized Dragontooth",
    "Wanderer's Advice",
    "Weathered Arrowhead",
    "Wheat",
    "White Iron Chunk",
    "Whopperflower Nectar",
    "Wick Material",
    "Windwheel Aster",
    "Wolfhook",
    "Yellow Dye",
    "Yumemiru Wood",
]


def gen_num():
    return str(np.random.randint(0, 9999))


def gen_material_name():
    return np.random.choice(MaterialsNameEN, size=1)[0]


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


scale_ratio = 1
characters = sorted(
    [
        *set(
            "".join(
                list(MaterialsNameEN)
                + list("0123456789")
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
