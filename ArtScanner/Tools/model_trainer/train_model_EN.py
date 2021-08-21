import numpy as np
from PIL import Image
import logging
from tensorflow import get_logger
from tensorflow.keras.models import Model
from tensorflow.keras.layers.experimental.preprocessing import StringLookup
from tensorflow.keras.layers import Input, Reshape, Dense, Dropout, Bidirectional, LSTM
from tensorflow.keras.backend import ctc_decode
from mobilenetv3 import MobileNetV3_Small
from tensorflow.strings import reduce_join
import json
import random as rd
import tensorflow as tf
from PIL import ImageFont, Image, ImageDraw
from tensorflow import keras
from mobilenetv3 import MobileNetV3_Small


Formats = {
    "FIGHT_PROP_CRITICAL":          "{:.1%}",
    "FIGHT_PROP_CRITICAL_HURT":     "{:.1%}",
    "FIGHT_PROP_ATTACK":            "{:,.0f}",
    "FIGHT_PROP_ATTACK_PERCENT":    "{:.1%}",
    "FIGHT_PROP_ELEMENT_MASTERY":   "{:,.0f}",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "{:.1%}",
    "FIGHT_PROP_HP":                "{:,.0f}",
    "FIGHT_PROP_HP_PERCENT":        "{:.1%}",
    "FIGHT_PROP_DEFENSE":           "{:,.0f}",
    "FIGHT_PROP_DEFENSE_PERCENT":   "{:.1%}",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "{:.1%}",
    "FIGHT_PROP_HEAL_ADD":          "{:.1%}",
    "FIGHT_PROP_ROCK_ADD_HURT":     "{:.1%}",
    "FIGHT_PROP_WIND_ADD_HURT":     "{:.1%}",
    "FIGHT_PROP_ICE_ADD_HURT":      "{:.1%}",
    "FIGHT_PROP_WATER_ADD_HURT":    "{:.1%}",
    "FIGHT_PROP_FIRE_ADD_HURT":     "{:.1%}",
    "FIGHT_PROP_ELEC_ADD_HURT":     "{:.1%}",
    "FIGHT_PROP_GRASS_ADD_HURT":    "{:.1%}",
    "FIGHT_PROP_FIRE_SUB_HURT":     "{:.1%}",
}

MainAttrNames = {
    "FIGHT_PROP_CRITICAL":          "暴击率",
    "FIGHT_PROP_CRITICAL_HURT":     "暴击伤害",
    "FIGHT_PROP_ATTACK":            "攻击力",
    "FIGHT_PROP_ATTACK_PERCENT":    "攻击力",
    "FIGHT_PROP_ELEMENT_MASTERY":   "元素精通",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
    "FIGHT_PROP_HP":                "生命值",
    "FIGHT_PROP_HP_PERCENT":        "生命值",
    "FIGHT_PROP_DEFENSE":           "防御力",
    "FIGHT_PROP_DEFENSE_PERCENT":   "防御力",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "物理伤害加成",
    "FIGHT_PROP_HEAL_ADD":          "治疗加成",
    "FIGHT_PROP_ROCK_ADD_HURT":     "岩元素伤害加成",
    "FIGHT_PROP_WIND_ADD_HURT":     "风元素伤害加成",
    "FIGHT_PROP_ICE_ADD_HURT":      "冰元素伤害加成",
    "FIGHT_PROP_WATER_ADD_HURT":    "水元素伤害加成",
    "FIGHT_PROP_FIRE_ADD_HURT":     "火元素伤害加成",
    "FIGHT_PROP_ELEC_ADD_HURT":     "雷元素伤害加成",
    "FIGHT_PROP_GRASS_ADD_HURT":    "草元素伤害加成",
    "FIGHT_PROP_FIRE_SUB_HURT":     "火元素伤害减免",
}
AttrName2Ids = {v: i.replace('_PERCENT', '') for i, v in MainAttrNames.items()}

TypeNames = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]

SubAttrNames = {
    "FIGHT_PROP_CRITICAL":          "暴击率",
    "FIGHT_PROP_CRITICAL_HURT":     "暴击伤害",
    "FIGHT_PROP_ATTACK":            "攻击力",
    "FIGHT_PROP_ATTACK_PERCENT":    "攻击力",
    "FIGHT_PROP_ELEMENT_MASTERY":   "元素精通",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "元素充能效率",
    "FIGHT_PROP_HP":                "生命值",
    "FIGHT_PROP_HP_PERCENT":        "生命值",
    "FIGHT_PROP_DEFENSE":           "防御力",
    "FIGHT_PROP_DEFENSE_PERCENT":   "防御力",
}

RarityToMaxLvs = [4, 4, 12, 16, 20]
RarityToBaseStatNumber = {1: [0], 2: [0, 1], 3: [1, 2], 4: [2, 3], 5: [3, 4]}

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
    ["勋绩之花", "昭武翎羽", "金铜时晷", "盟誓金爵", "将帅兜鏊"],
    ["无垢之花", "贤医之羽", "停摆之刻", "超越之盏", "嗤笑之面"],
    ["明威之镡", "切落之羽", "雷云之笼", "绯花之壶", "华饰之兜"],   # 绝缘之旗印
    ["羁缠之花", "思忆之矢", "朝露之时", "祈望之心", "无常之面"],   # 追忆之注连
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
    "枫原万叶",
    "宵宫",
    "早柚",
]

TypeNamesGenshinArt = ["flower", "feather", "sand", "cup", "head"]
AttrNamesGensinArt = {
    "FIGHT_PROP_CRITICAL":          "critical",
    "FIGHT_PROP_CRITICAL_HURT":     "criticalDamage",
    "FIGHT_PROP_ATTACK":            "attackStatic",
    "FIGHT_PROP_ATTACK_PERCENT":    "attackPercentage",
    "FIGHT_PROP_ELEMENT_MASTERY":   "elementalMastery",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "recharge",
    "FIGHT_PROP_HP":                "lifeStatic",
    "FIGHT_PROP_HP_PERCENT":        "lifePercentage",
    "FIGHT_PROP_DEFENSE":           "defendStatic",
    "FIGHT_PROP_DEFENSE_PERCENT":   "defendPercentage",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "physicalBonus",
    "FIGHT_PROP_HEAL_ADD":          "cureEffect",
    "FIGHT_PROP_ROCK_ADD_HURT":     "rockBonus",
    "FIGHT_PROP_WIND_ADD_HURT":     "windBonus",
    "FIGHT_PROP_ICE_ADD_HURT":      "iceBonus",
    "FIGHT_PROP_WATER_ADD_HURT":    "waterBonus",
    "FIGHT_PROP_FIRE_ADD_HURT":     "fireBonus",
    "FIGHT_PROP_ELEC_ADD_HURT":     "thunderBonus",
    "FIGHT_PROP_GRASS_ADD_HURT":    "grassBonus",
    "FIGHT_PROP_FIRE_SUB_HURT":     "fireDeduct",
}
SetNamesGenshinArt = [
    "archaicPetra",             # 悠古的磐岩
    "blizzardStrayer",          # 冰风迷途的勇士
    "bloodstainedChivalry",     # 染血的骑士道
    "crimsonWitch",             # 炽烈的炎之魔女
    "gladiatorFinale",          # 角斗士的终幕礼
    "heartOfDepth",             # 沉沦之心
    "lavaWalker",               # 渡过烈火的贤人
    "maidenBeloved",            # 被怜爱的少女
    "noblesseOblige",           # 昔日宗室之仪
    "retracingBolide",          # 逆飞的流星
    "thunderSmoother",          # 平息雷鸣的尊者
    "thunderingFury",           # 如雷的盛怒
    "viridescentVenerer",       # 翠绿之影
    "wandererTroupe",           # 流浪大地的乐团
    "berserker",                # 战狂
    "braveHeart",               # 勇士之心
    "defenderWill",             # 守护之心
    "exile",                    # 流放者
    "gambler",                  # 赌徒
    "instructor",               # 教官
    "martialArtist",            # 武人
    "prayersForDestiny",        # 祭水之人
    "prayersForIllumination",   # 祭火之人
    "prayersForWisdom",         # 祭雷之人
    "prayersToSpringtime",      # 祭冰之人
    "resolutionOfSojourner",    # 行者之心
    "scholar",                  # 学士
    "tinyMiracle",              # 奇迹
    "adventurer",               # 冒险家
    "luckyDog",                 # 幸运儿
    "travelingDoctor",          # 游医
    "tenacityOfTheMillelith",   # 千岩牢固
    "paleFlame",                # 苍白之火
    "shimenawaReminiscence",    # 追忆之注连
    "emblemOfSeveredFate",      # 绝缘之旗印

]

TypeNamesMingyuLab = ['flower', 'plume', 'eon', 'goblet', 'circlet']
AttrNamesMingyuLab = {
    "FIGHT_PROP_CRITICAL":          "critRate",
    "FIGHT_PROP_CRITICAL_HURT":     "critDamage",
    "FIGHT_PROP_ATTACK":            "flatATK",
    "FIGHT_PROP_ATTACK_PERCENT":    "percentATK",
    "FIGHT_PROP_ELEMENT_MASTERY":   "elementalMastery",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "energyRecharge",
    "FIGHT_PROP_HP":                "flatHP",
    "FIGHT_PROP_HP_PERCENT":        "percentHP",
    "FIGHT_PROP_DEFENSE":           "flatDEF",
    "FIGHT_PROP_DEFENSE_PERCENT":   "percentDEF",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "physicalDamage",
    "FIGHT_PROP_HEAL_ADD":          "healing",
    "FIGHT_PROP_ROCK_ADD_HURT":     "geoDamage",
    "FIGHT_PROP_WIND_ADD_HURT":     "anemoDamage",
    "FIGHT_PROP_ICE_ADD_HURT":      "cryoDamage",
    "FIGHT_PROP_WATER_ADD_HURT":    "hydroDamage",
    "FIGHT_PROP_FIRE_ADD_HURT":     "pyroDamage",
    "FIGHT_PROP_ELEC_ADD_HURT":     "electroDamage",
    "FIGHT_PROP_GRASS_ADD_HURT":    "dendroDamage",
    "FIGHT_PROP_FIRE_SUB_HURT":     "pyroDEF",
}

SetNamesMingyuLab = [
    "archaic_petra",                # 悠古的磐岩
    "blizzard_walker",              # 冰风迷途的勇士
    "bloodstained_chivalry",        # 染血的骑士道
    "crimson_witch_of_flames",      # 炽烈的炎之魔女
    "gladiators_finale",            # 角斗士的终幕礼
    "heart_of_depth",               # 沉沦之心
    "lavawalker",                   # 渡过烈火的贤人
    "maiden_beloved",               # 被怜爱的少女
    "noblesse_oblige",              # 昔日宗室之仪
    "retracing_bolide",             # 逆飞的流星
    "thundersoother",               # 平息雷鸣的尊者
    "thundering_fury",              # 如雷的盛怒
    "viridescent_venerer",          # 翠绿之影
    "wanderers_troupe",             # 流浪大地的乐团
    "berserker",                    # 战狂
    "brave_heart",                  # 勇士之心
    "defenders_will",               # 守护之心
    "the_exile",                    # 流放者
    "gambler",                      # 赌徒
    "instructor",                   # 教官
    "martial_artist",               # 武人
    "prayers_of_destiny",           # 祭水之人
    "prayers_of_illumination",      # 祭火之人
    "prayers_of_wisdom",            # 祭雷之人
    "prayers_of_springtime",        # 祭冰之人
    "resolution_of_sojourner",      # 行者之心
    "scholar",                      # 学士
    "tiny_miracle",                 # 奇迹
    "adventurer",                   # 冒险家
    "lucky_dog",                    # 幸运儿
    "traveling_doctor",             # 游医
    "tenacity_of_the_millelith",    # 千岩牢固
    "pale_flame",                   # 苍白之火
    "reminiscence_of_shime",        # 追忆之注连
    "seal_of_insulation",           # 绝缘之旗印
]

MainAttrValue = {
    5: {
        "FIGHT_PROP_CRITICAL": [0.047, 0.060, 0.073, 0.086, 0.099, 0.113, 0.126, 0.139, 0.152, 0.166, 0.179, 0.192, 0.205,
                                0.218, 0.232, 0.245, 0.258, 0.271, 0.284, 0.298, 0.311, ],
        "FIGHT_PROP_CRITICAL_HURT": [0.093, 0.120, 0.146, 0.173, 0.199, 0.225, 0.252, 0.278, 0.305, 0.331, 0.357, 0.384,
                                     0.410, 0.437, 0.463, 0.490, 0.516, 0.542, 0.569, 0.595, 0.622, ],
        "FIGHT_PROP_ATTACK": [47, 60, 73, 86, 100, 113, 126, 139, 152, 166, 179, 192, 205, 219, 232, 245, 258, 272, 285,
                              298, 311, ],
        "FIGHT_PROP_ATTACK_PERCENT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                      0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_ELEMENT_MASTERY": [28, 36, 44, 52, 60, 68, 76, 84, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171,
                                       179, 187, ],
        "FIGHT_PROP_CHARGE_EFFICIENCY": [0.078, 0.100, 0.122, 0.144, 0.166, 0.188, 0.210, 0.232, 0.254, 0.276, 0.298, 0.320,
                                         0.342, 0.364, 0.386, 0.408, 0.430, 0.452, 0.474, 0.496, 0.518, ],
        "FIGHT_PROP_HP": [717, 920, 1123, 1326, 1530, 1733, 1936, 2139, 2342, 2545, 2749, 2952, 3155, 3358, 3561, 3764,
                          3967, 4171, 4374, 4577, 4780, ],
        "FIGHT_PROP_HP_PERCENT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308,
                                  0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_DEFENSE_PERCENT": [0.087, 0.112, 0.137, 0.162, 0.186, 0.211, 0.236, 0.261, 0.286, 0.310, 0.335, 0.360,
                                       0.385, 0.409, 0.434, 0.459, 0.484, 0.508, 0.533, 0.558, 0.583, ],
        "FIGHT_PROP_PHYSICAL_ADD_HURT": [0.087, 0.112, 0.137, 0.162, 0.186, 0.211, 0.236, 0.261, 0.286, 0.310, 0.335, 0.360,
                                         0.385, 0.409, 0.434, 0.459, 0.484, 0.508, 0.533, 0.558, 0.583, ],
        "FIGHT_PROP_HEAL_ADD": [0.054, 0.069, 0.084, 0.100, 0.115, 0.130, 0.145, 0.161, 0.176, 0.191, 0.206, 0.221, 0.237,
                                0.252, 0.267, 0.282, 0.298, 0.313, 0.328, 0.343, 0.359, ],
        "FIGHT_PROP_ROCK_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                     0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_WIND_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                     0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_ICE_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                    0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_WATER_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                      0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_FIRE_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                     0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_ELEC_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                     0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
        "FIGHT_PROP_GRASS_ADD_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288,
                                      0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466, ],
    },
    4: {
        "FIGHT_PROP_CRITICAL": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137,
                                0.149, 0.161, 0.173, 0.185, 0.197, 0.208, 0.220, 0.232, ],
        "FIGHT_PROP_CRITICAL_HURT": [0.084, 0.108, 0.131, 0.155, 0.179, 0.203, 0.227, 0.250, 0.274,
                                     0.298, 0.322, 0.345, 0.369, 0.393, 0.417, 0.441, 0.464, ],
        "FIGHT_PROP_ATTACK": [42, 54, 66, 78, 90, 102, 113, 125, 137, 149, 161, 173, 185, 197, 209, 221, 232, ],
        "FIGHT_PROP_ATTACK_PERCENT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223, 0.241,
                                      0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_ELEMENT_MASTERY": [25, 32, 39, 47, 54, 61, 68, 75, 82, 89, 97, 104, 111, 118, 125, 132, 139, ],
        "FIGHT_PROP_CHARGE_EFFICIENCY": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228,
                                         0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, ],
        "FIGHT_PROP_HP": [645, 828, 1011, 1194, 1377, 1559, 1742, 1925, 2108, 2291, 2474, 2657, 2839, 3022,
                          3205, 3388, 3571, ],
        "FIGHT_PROP_HP_PERCENT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223, 0.241,
                                  0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_DEFENSE_PERCENT": [0.079, 0.101, 0.123, 0.146, 0.168, 0.190, 0.212, 0.235, 0.257, 0.279, 0.302,
                                       0.324, 0.346, 0.368, 0.391, 0.413, 0.435, ],
        "FIGHT_PROP_PHYSICAL_ADD_HURT": [0.079, 0.101, 0.123, 0.146, 0.168, 0.190, 0.212, 0.235, 0.257,
                                         0.279, 0.302, 0.324, 0.346, 0.368, 0.391, 0.413, 0.435, ],
        "FIGHT_PROP_HEAL_ADD": [0.048, 0.062, 0.076, 0.090, 0.103, 0.117, 0.131, 0.144, 0.158, 0.172, 0.186,
                                0.199, 0.213, 0.227, 0.240, 0.254, 0.268, ],
        "FIGHT_PROP_ROCK_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                     0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_WIND_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                     0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_ICE_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                    0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_WATER_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                      0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_FIRE_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                     0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_ELEC_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                     0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
        "FIGHT_PROP_GRASS_ADD_HURT": [0.063, 0.081, 0.099, 0.116, 0.134, 0.152, 0.170, 0.188, 0.206, 0.223,
                                      0.241, 0.259, 0.277, 0.295, 0.313, 0.330, 0.348, ],
    },
    3: {
        "FIGHT_PROP_CRITICAL": [0.035, 0.045, 0.055, 0.065, 0.075, 0.084, 0.094, 0.104,
                                0.114, 0.124, 0.134, 0.144, 0.154, ],
        "FIGHT_PROP_CRITICAL_HURT": [0.070, 0.090, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209,
                                     0.228, 0.248, 0.268, 0.288, 0.308, ],
        "FIGHT_PROP_ATTACK": [28, 36, 44, 52, 60, 68, 76, 84, 91, 99, 107, 115, 123, ],
        "FIGHT_PROP_ATTACK_PERCENT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171, 0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_ELEMENT_MASTERY": [21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 80, 86, 92, ],
        "FIGHT_PROP_CHARGE_EFFICIENCY": [0.058, 0.075, 0.091, 0.108, 0.124, 0.141, 0.157, 0.174,
                                         0.190, 0.207, 0.223, 0.240, 0.256, ],
        "FIGHT_PROP_HP": [430, 552, 674, 796, 918, 1040, 1162, 1283, 1405, 1527, 1649, 1771, 1893, ],
        "FIGHT_PROP_HP_PERCENT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171, 0.186,
                                  0.201, 0.216, 0.231, ],
        "FIGHT_PROP_DEFENSE_PERCENT": [0.066, 0.084, 0.103, 0.121, 0.140, 0.158, 0.177, 0.196, 0.214, 0.233,
                                       0.251, 0.270, 0.288, ],
        "FIGHT_PROP_PHYSICAL_ADD_HURT": [0.066, 0.084, 0.103, 0.121, 0.140, 0.158, 0.177, 0.196,
                                         0.214, 0.233, 0.251, 0.270, 0.288, ],
        "FIGHT_PROP_HEAL_ADD": [0.040, 0.052, 0.063, 0.075, 0.086, 0.098, 0.109, 0.120, 0.132,
                                0.143, 0.155, 0.166, 0.178, ],
        "FIGHT_PROP_ROCK_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                     0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_WIND_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                     0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_ICE_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                    0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_WATER_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                      0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_FIRE_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                     0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_ELEC_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                     0.186, 0.201, 0.216, 0.231, ],
        "FIGHT_PROP_GRASS_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171,
                                      0.186, 0.201, 0.216, 0.231, ],
    },
    2: {
        "FIGHT_PROP_CRITICAL": [0.028, 0.036, 0.044, 0.052, 0.060, 0.068, 0.076, 0.083, 0.091, ],
        "FIGHT_PROP_CRITICAL_HURT": [0.056, 0.072, 0.088, 0.104, 0.119, 0.135, 0.151, 0.167, 0.183, ],
        "FIGHT_PROP_ATTACK": [17, 22, 26, 31, 36, 41, 45, 50, 55, ],
        "FIGHT_PROP_ATTACK_PERCENT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_ELEMENT_MASTERY": [17, 22, 26, 31, 36, 41, 45, 50, 55, ],
        "FIGHT_PROP_CHARGE_EFFICIENCY": [0.047, 0.060, 0.073, 0.086, 0.099, 0.113, 0.126, 0.139, 0.152, ],
        "FIGHT_PROP_HP": [258, 331, 404, 478, 551, 624, 697, 770, 843, ],
        "FIGHT_PROP_HP_PERCENT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_DEFENSE_PERCENT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171, ],
        "FIGHT_PROP_PHYSICAL_ADD_HURT": [0.052, 0.067, 0.082, 0.097, 0.112, 0.127, 0.142, 0.156, 0.171, ],
        "FIGHT_PROP_HEAL_ADD": [0.032, 0.041, 0.051, 0.060, 0.069, 0.078, 0.087, 0.096, 0.105, ],
        "FIGHT_PROP_ROCK_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_WIND_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_ICE_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_WATER_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_FIRE_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_ELEC_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
        "FIGHT_PROP_GRASS_ADD_HURT": [0.042, 0.054, 0.066, 0.078, 0.090, 0.101, 0.113, 0.125, 0.137, ],
    }
}

MainAttrNames_EN = {
    "FIGHT_PROP_CRITICAL":          "CRIT Rate",
    "FIGHT_PROP_CRITICAL_HURT":     "CRIT DMG",
    "FIGHT_PROP_ATTACK":            "ATK",
    "FIGHT_PROP_ATTACK_PERCENT":    "ATK",
    "FIGHT_PROP_ELEMENT_MASTERY":   "Elemental Mastery",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "Energy Recharge",
    "FIGHT_PROP_HP":                "HP",
    "FIGHT_PROP_HP_PERCENT":        "HP",
    "FIGHT_PROP_DEFENSE":           "DEF",
    "FIGHT_PROP_DEFENSE_PERCENT":   "DEF",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "Physical DMG Bonus",
    "FIGHT_PROP_HEAL_ADD":          "Healing Bonus",
    "FIGHT_PROP_ROCK_ADD_HURT":     "Geo DMG Bonus",
    "FIGHT_PROP_WIND_ADD_HURT":     "Anemo DMG Bonus",
    "FIGHT_PROP_ICE_ADD_HURT":      "Cryo DMG Bonus",
    "FIGHT_PROP_WATER_ADD_HURT":    "Hydro DMG Bonus",
    "FIGHT_PROP_FIRE_ADD_HURT":     "Pyro DMG Bonus",
    "FIGHT_PROP_ELEC_ADD_HURT":     "Electro DMG Bonus",
    "FIGHT_PROP_GRASS_ADD_HURT":    "Dendro DMG Bonus",
}

TypeNames_EN = ["Flower of Life",
                "Plume of Death",
                "Sands of Eon",
                "Goblet of Eonothem",
                "Circlet of Logos"]

AttrName2Ids_EN = {v: i.replace('_PERCENT', '') for i, v in MainAttrNames_EN.items()}

SubAttrNames_EN = {
    "FIGHT_PROP_CRITICAL":          "CRIT Rate",
    "FIGHT_PROP_CRITICAL_HURT":     "CRIT DMG",
    "FIGHT_PROP_ATTACK":            "ATK",
    "FIGHT_PROP_ATTACK_PERCENT":    "ATK",
    "FIGHT_PROP_ELEMENT_MASTERY":   "Elemental Mastery",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "Energy Recharge",
    "FIGHT_PROP_HP":                "HP",
    "FIGHT_PROP_HP_PERCENT":        "HP",
    "FIGHT_PROP_DEFENSE":           "DEF",
    "FIGHT_PROP_DEFENSE_PERCENT":   "DEF",
}

ArtNames_EN = [
    ['Flower of Creviced Cliff', 'Feather of Jagged Peaks', 'Sundial of Enduring Jade',
     'Goblet of Chiseled Crag', 'Mask of Solitude Basalt'],
    ['Snowswept Memory', "Icebreaker's Resolve", "Frozen Homeland's Demise",
     'Frost-Weaved Dignity', "Broken Rime's Echo"],
    ['Bloodstained Flower of Iron', 'Bloodstained Black Plume', 'Bloodstained Final Hour',
     "Bloodstained Chevalier's Goblet", 'Bloodstained Iron Mask'],
    ["Witch's Flower of Blaze", "Witch's Ever-Burning Plume",
     "Witch's End Time", "Witch's Heart Flames", "Witch's Scorching Hat"],
    ["Gladiator's Nostalgia", "Gladiator's Destiny", "Gladiator's Longing",
     "Gladiator's Intoxication", "Gladiator's Triumphus"],
    ['Gilded Corsage', 'Gust of Nostalgia', 'Copper Compass',
     'Goblet of Thundering Deep', 'Wine-Stained Tricorne'],
    ["Lavawalker's Resolution", "Lavawalker's Salvation", "Lavawalker's Torment",
     "Lavawalker's Epiphany", "Lavawalker's Wisdom"],
    ["Maiden's Distant Love", "Maiden's Heart-stricken Infatuation", "Maiden's Passing Youth",
     "Maiden's Fleeting Leisure", "Maiden's Fading Beauty"],
    ['Royal Flora', 'Royal Plume', 'Royal Pocket Watch',
     'Royal Silver Urn', 'Royal Masque'],
    ["Summer Night's Bloom", "Summer Night's Finale", "Summer Night's Moment",
     "Summer Night's Waterballoon", "Summer Night's Mask"],
    ["Thundersoother's Heart", "Thundersoother's Plume", 'Hour of Soothing Thunder',
     "Thundersoother's Goblet", "Thundersoother's Diadem"],
    ["Thunderbird's Mercy", 'Survivor of Catastrophe', 'Hourglass of Thunder',
     'Omen of Thunderstorm', "Thunder Summoner's Crown"],
    ['In Remembrance of Viridescent Fields', 'Viridescent Arrow Feather',
     "Viridescent Venerer's Determination", "Viridescent Venerer's Vessel",
     "Viridescent Venerer's Diadem"],
    ["Troupe's Dawnlight", "Bard's Arrow Feather", "Concert's Final Hour",
     "Wanderer's String-Kettle", "Conductor's Top Hat"],
    ["Berserker's Rose", "Berserker's Indigo Feather", "Berserker's Timepiece",
     "Berserker's Bone Goblet", "Berserker's Battle Mask"],
    ['Medal of the Brave', 'Prospect of the Brave', 'Fortitude of the Brave',
     'Outset of the Brave', 'Crown of the Brave'],
    ["Guardian's Flower", "Guardian's Sigil", "Guardian's Clock",
     "Guardian's Vessel", "Guardian's Band"],
    ["Exile's Flower", "Exile's Feather", "Exile's Pocket Watch",
     "Exile's Goblet", "Exile's Circlet"],
    ["Gambler's Brooch", "Gambler's Feather Accessory", "Gambler's Pocket Watch",
     "Gambler's Dice Cup", "Gambler's Earrings"],
    ["Instructor's Brooch", "Instructor's Feather Accessory", "Instructor's Pocket Watch",
     "Instructor's Tea Cup", "Instructor's Cap"],
    ["Martial Artist's Red Flower", "Martial Artist's Feather Accessory",
     "Martial Artist's Water Hourglass", "Martial Artist's Wine Cup",
     "Martial Artist's Bandana"],
    ['Tiara of Torrents'], ['Tiara of Flame'],
    ['Tiara of Thunder'], ['Tiara of Frost'],
    ['Heart of Comradeship', 'Feather of Homecoming', 'Sundial of the Sojourner',
     'Goblet of the Sojourner', 'Crown of Parting'],
    ["Scholar's Bookmark", "Scholar's Quill Pen", "Scholar's Clock",
     "Scholar's Ink Cup", "Scholar's Lens"],
    ["Tiny Miracle's Flower", "Tiny Miracle's Feather", "Tiny Miracle's Hourglass",
     "Tiny Miracle's Goblet", "Tiny Miracle's Earrings"],
    ["Adventurer's Flower", "Adventurer's Tail Feather", "Adventurer's Pocket Watch",
     "Adventurer's Golden Goblet", "Adventurer's Bandana"],
    ["Lucky Dog's Clover", "Lucky Dog's Eagle Feather", "Lucky Dog's Hourglass",
     "Lucky Dog's Goblet", "Lucky Dog's Silver Circlet"],
    ["Traveling Doctor's Silver Lotus", "Traveling Doctor's Owl Feather",
     "Traveling Doctor's Pocket Watch", "Traveling Doctor's Medicine Pot",
     "Traveling Doctor's Handkerchief"],
    ['Flower of Accolades', 'Ceremonial War-Plume', 'Orichalceous Time-Dial',
     "Noble's Pledging Vessel", "General's Ancient Helm"],
    ['Stainless Bloom', "Wise Doctor's Pinion", 'Moment of Cessation',
     'Surpassing Cup', 'Mocking Mask'],
    ['Magnificent Tsuba', 'Sundered Feather', 'Storm Cage',
     'Scarlet Vessel', 'Ornate Kabuto'],
    ['Entangling Bloom', 'Shaft of Remembrance', "Morning Dew's Moment",
     'Hopeful Heart', 'Capricious Visage']
]


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


import json

import numpy as np
from PIL import ImageFont, Image, ImageDraw

MainAttrDatabase = json.load(open('../ReliquaryLevelExcelConfigData.json'))
SubAttrDatabase = json.load(open('../ReliquaryAffixExcelConfigData.json'))


def gen_name():
    return np.random.choice(sum(ArtNames_EN, []), size=1)[0]


def gen_type():
    return np.random.choice(TypeNames_EN, size=1)[0]


def gen_main_attr_name():
    return np.random.choice(list(MainAttrNames_EN.values()), size=1)[0]


def gen_main_attr_value():
    main_attr_id = np.random.choice(list(MainAttrNames_EN.keys()), size=1)[0]
    value = np.random.choice(
        sum([[j['Value'] for j in i['AddProps'] if j['PropType'] == main_attr_id] for i in MainAttrDatabase], []),
        size=1)[0]
    return Formats[main_attr_id].format(value)


def gen_level():
    n = 1
    return ["+" + str(i) for i in np.random.randint(0, 21, size=n)][0]


def gen_single_sub_attr():
    sub_attr_id = np.random.choice(list(SubAttrNames_EN.keys()), size=1)[0]
    rare_sub_attr_ranges = [
        [i['PropValue'] for i in SubAttrDatabase if i['DepotId'] == j and i['PropType'] == sub_attr_id] for j in
        [101, 201, 301, 401, 501]]
    rare = np.random.choice(5, p=[0.0625, 0.0625, 0.125, 0.25, 0.5])
    n_upgrades = np.random.randint(1, rare + 3)
    sub_attr_value = np.random.choice(rare_sub_attr_ranges[rare], size=n_upgrades).sum()
    return SubAttrNames_EN[sub_attr_id] + '+' + Formats[sub_attr_id].format(sub_attr_value)


def gen_sub_attrs(n=1):
    return [gen_single_sub_attr() for i in range(n)]


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
        font_size_range=(30, 50)
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


def train_generator():
    q = 0
    while True:
        q += 1
        sub_attrs_num = rd.randrange(1, 5)
        info_train = [gen_name(), gen_type(), gen_main_attr_name(), gen_main_attr_value(),
                      gen_level(), *gen_sub_attrs(sub_attrs_num)]
        imgs = generate_images(info_train)
        info = {"name": imgs[0],
                "type": imgs[1],
                "main_attr_name": imgs[2],
                "main_attr_value": imgs[3],
                "level": imgs[4],
                }
        expect_info = {"name": info_train[0],
                       "type": info_train[1],
                       "main_attr_name": info_train[2],
                       "main_attr_value": info_train[3],
                       "level": info_train[4]}
        for i in range(sub_attrs_num):
            info[f'subattr_{i + 1}'] = imgs[i + 5]
            expect_info[f'subattr_{i + 1}'] = info_train[i + 5]
        x = np.concatenate([preprocess(info[key]).T[None, :, :, None] for key in sorted(info.keys())], axis=0)

        f = [list(expect_info[key]) for key in sorted(expect_info.keys())]
        w = []
        for lst in f:
            w.append([i.encode('utf-8') for i in lst] + [b''] * (max_length - len(lst)))
        y = char_to_num(w)
        yield x, y
    return


characters = sorted(
    [
        *set(
            "".join(
                sum(ArtNames_EN, [])
                + TypeNames_EN
                + list(MainAttrNames_EN.values())
                + list(SubAttrNames_EN.values())
                + list(".,+%0123456789")
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
model = Model(inputs=[input_img], outputs=output, name="ocr_model_en")

opt = keras.optimizers.Adam()
model.compile(loss=ctc_loss, optimizer=opt, metrics=[CTCAccuracy('ctc_accu')])
model.run_eagerly = True
model.summary()


filepath = "./train/weights-improvement-EN-{epoch:02d}-{ctc_accu:.2f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='ctc_accu', verbose=1, save_best_only=True,
                                                mode='max')
reduce = keras.callbacks.ReduceLROnPlateau(monitor='ctc_accu', factor=0.5, min_lr=1e-7, verbose=1, patience=3)
callbacks_list = [reduce, checkpoint]

# -- train model --
history = model.fit(x=train_generator(), steps_per_epoch=512, epochs=168, callbacks=callbacks_list)
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
