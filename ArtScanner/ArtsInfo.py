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
    # "FIGHT_PROP_GRASS_ADD_HURT":    "草元素伤害加成",
    # "FIGHT_PROP_FIRE_SUB_HURT":     "火元素伤害减免",
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
    # todo fix typo
    # ["勋绩之花", "昭武翎羽", "金铜时晷", "盟誓金爵", "将帅兜鍪"],
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
    "thunderSmoother",          # 平息鸣雷的尊者
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
    "emblemOfSeveredFate",      # 绝缘之旗印
    "shimenawaReminiscence",    # 追忆之注连

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
    "seal_of_insulation",           # 绝缘之旗印
    "reminiscence_of_shime",        # 追忆之注连
]

TypeNamesGOOD = ['flower', 'plume', 'sands', 'goblet', 'circlet']

AttrNamesGOOD = {
    "FIGHT_PROP_CRITICAL":          "critRate_",
    "FIGHT_PROP_CRITICAL_HURT":     "critDMG_",
    "FIGHT_PROP_ATTACK":            "atk",
    "FIGHT_PROP_ATTACK_PERCENT":    "atk_",
    "FIGHT_PROP_ELEMENT_MASTERY":   "eleMas",
    "FIGHT_PROP_CHARGE_EFFICIENCY": "enerRech_",
    "FIGHT_PROP_HP":                "hp",
    "FIGHT_PROP_HP_PERCENT":        "hp_",
    "FIGHT_PROP_DEFENSE":           "def",
    "FIGHT_PROP_DEFENSE_PERCENT":   "def_",
    "FIGHT_PROP_PHYSICAL_ADD_HURT": "physical_dmg_",
    "FIGHT_PROP_HEAL_ADD":          "heal_",
    "FIGHT_PROP_ROCK_ADD_HURT":     "geo_dmg_",
    "FIGHT_PROP_WIND_ADD_HURT":     "anemo_dmg_",
    "FIGHT_PROP_ICE_ADD_HURT":      "cryo_dmg_",
    "FIGHT_PROP_WATER_ADD_HURT":    "hydro_dmg_",
    "FIGHT_PROP_FIRE_ADD_HURT":     "pyro_dmg_",
    "FIGHT_PROP_ELEC_ADD_HURT":     "electro_dmg_",
    "FIGHT_PROP_GRASS_ADD_HURT":    "dendro_dmg_"
}

SetNamesGOOD = [
    'ArchaicPetra', 'BlizzardStrayer', 'BloodstainedChivalry',
    'CrimsonWitchOfFlames', 'GladiatorsFinale', 'HeartOfDepth',
    'Lavawalker', 'MaidenBeloved', 'NoblesseOblige',
    'RetracingBolide', 'Thundersoother', 'ThunderingFury',
    'ViridescentVenerer', 'WanderersTroupe', 'Berserker',
    'BraveHeart', 'DefendersWill', 'TheExile', 'Gambler',
    'Instructor', 'MartialArtist', 'PrayersForDestiny',
    'PrayersForIllumination', 'PrayersForWisdom', 'PrayersToSpringtime',
    'ResolutionOfSojourner', 'Scholar', 'TinyMiracle',
    'Adventurer', 'LuckyDog', 'TravelingDoctor',
    'TenacityOfTheMillelith', 'PaleFlame',
    'EmblemOfSeveredFate', 'ShimenawasReminiscence'
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

SetNames = [
    "悠古的磐岩",
    "冰风迷途的勇士",
    "染血的骑士道",
    "炽烈的炎之魔女",
    "角斗士的终幕礼",
    "沉沦之心",
    "渡过烈火的贤人",
    "被怜爱的少女",
    "昔日宗室之仪",
    "逆飞的流星",
    "平息雷鸣的尊者",
    "如雷的盛怒",
    "翠绿之影",
    "流浪大地的乐团",
    "战狂",
    "勇士之心",
    "守护之心",
    "流放者",
    "赌徒",
    "教官",
    "武人",
    "祭水之人",
    "祭火之人",
    "祭雷之人",
    "祭冰之人",
    "行者之心",
    "学士",
    "奇迹",
    "冒险家",
    "幸运儿",
    "游医",
    "千岩牢固",
    "苍白之火",
    "绝缘之旗印",
    "追忆之注连",
]

Setnames_EN = ['Archaic Petra',
               'Blizzard Strayer',
               'Bloodstained Chivalry',
               'Crimson Witch of Flames',
               "Gladiator's Finale", 'Heart of Depth',
               'Lavawalker', 'Maiden Beloved',
               'Noblesse Oblige', 'Retracing Bolide',
               'Thundersoother',
               'Thundering Fury', 'Viridescent Venerer',
               "Wanderer's Troupe", 'Berserker',
               'Brave Heart', "Defender's Will", 'The Exile',
               'Gambler', 'Instructor', 'Martial Artist',
               'Prayers for Destiny', 'Prayers for Illumination',
               'Prayers for Wisdom', 'Prayers to Springtime',
               'Resolution of Sojourner', 'Scholar', 'Tiny Miracle',
               'Adventurer', 'Lucky Dog', 'Traveling Doctor',
               'Tenacity of the Millelith', 'Pale Flame',
               'Emblem of Severed Fate',
               "Shimenawa's Reminiscence"]

