import json
import numpy as np   
from PIL import ImageFont, Image, ImageDraw
from .. import ArtsInfo

MainAttrDatabase = json.load(open('ReliquaryLevelExcelConfigData.json'))
SubAttrDatabase = json.load(open('ReliquaryAffixExcelConfigData.json'))

def gen_name():
    return np.random.choice(sum(ArtsInfo.ArtNames, []), size=1)[0]

def gen_type():
    return np.random.choice(ArtsInfo.TypeNames, size=1)[0]

def gen_main_attr_name():
    return np.random.choice(list(ArtsInfo.MainAttrNames.values()), size=1)[0]

def gen_main_attr_value():
    main_attr_id = np.random.choice(list(ArtsInfo.MainAttrNames.keys()), size=1)[0]
    value = np.random.choice(sum([[j['Value'] for j in i['AddProps'] if j['PropType']==main_attr_id] for i in MainAttrDatabase], []), size=1)[0]
    return ArtsInfo.Formats[main_attr_id].format(value)

def gen_level():
    n = 1
    return ["+" + str(i) for i in np.random.randint(0, 21, size=n)][0]

def gen_single_sub_attr():
    sub_attr_id = np.random.choice(list(ArtsInfo.SubAttrNames.keys()), size=1)[0]
    rare_sub_attr_ranges = [[i['PropValue'] for i in SubAttrDatabase if i['DepotId']==j and i['PropType']==sub_attr_id] for j in [101,201,301,401,501]]
    rare = np.random.choice(5, p=[0.0625, 0.0625, 0.125, 0.25, 0.5])
    n_upgrades = np.random.randint(1,rare+3)
    sub_attr_value = np.random.choice(rare_sub_attr_ranges[rare], size=n_upgrades).sum()
    return ArtsInfo.SubAttrNames[sub_attr_id]+'+'+ArtsInfo.Formats[sub_attr_id].format(sub_attr_value)

def gen_sub_attrs(n=1):
    return [gen_single_sub_attr() for i in range(n)]

def generate_images(texts, font_size_range=(15, 40)):
    result = []
    for text in texts:
        result.append(generate_image(text, font_size_range=font_size_range))
    return np.array(result)

fonts = {i:ImageFont.truetype("genshin.ttf", i) for i in range(10,100)}
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