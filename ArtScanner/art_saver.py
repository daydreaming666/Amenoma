import ArtsInfo
from utils import decodeValue
import ZODB, ZODB.FileStorage
import persistent, transaction
from enum import IntEnum as Enum
import json

class ArtifactType(Enum):
    FLOWER = 0
    PLUME = 1
    SANDS = 2
    GOBLET = 3
    CIRCLET = 4
    @classmethod
    def fromString(cls, s):
        try:
            return getattr(cls, s.upper())
        except:
            return cls(ArtsInfo.TypeNamesGenshinArt.index(s))

class ArtifactStatType(Enum):
    FIGHT_PROP_CRITICAL = 0
    FIGHT_PROP_CRITICAL_HURT = 1
    FIGHT_PROP_ATTACK = 2
    FIGHT_PROP_ATTACK_PERCENT = 3
    FIGHT_PROP_ELEMENT_MASTERY = 4
    FIGHT_PROP_CHARGE_EFFICIENCY = 5
    FIGHT_PROP_HP = 6
    FIGHT_PROP_HP_PERCENT = 7
    FIGHT_PROP_DEFENSE = 8
    FIGHT_PROP_DEFENSE_PERCENT = 9
    FIGHT_PROP_PHYSICAL_ADD_HURT = 10
    FIGHT_PROP_HEAL_ADD = 11
    FIGHT_PROP_ROCK_ADD_HURT = 12
    FIGHT_PROP_WIND_ADD_HURT = 13
    FIGHT_PROP_ICE_ADD_HURT = 14
    FIGHT_PROP_WATER_ADD_HURT = 15
    FIGHT_PROP_FIRE_ADD_HURT = 16
    FIGHT_PROP_ELEC_ADD_HURT = 17
    FIGHT_PROP_GRASS_ADD_HURT = 18
    FIGHT_PROP_FIRE_SUB_HURT = 19

class ArtifactStat:
    def __init__(self, name, value):
        name = ArtsInfo.AttrName2Ids[name]
        value = decodeValue(value)
        if type(value) == float and (name+'_PERCENT') in ArtsInfo.AttrNamesGensinArt:
            name += '_PERCENT'
        self.type = getattr(ArtifactStatType, name)
        self.value = value

class Artifact(persistent.Persistent):
    def __init__(self, info, image):
        '''
            info: dict with keys:
                'name': str, name of artifact
                'type': str, type of artifact 
                'level': str/int, upgraded level of artifact, example: '+0', '0', 1
                'star': int, rarity, 1-5
                'main_attr_name': str, name of main stat
                'main_attr_value': str/int/float, main stat value, example: '38.5%', '4,760', 144
                'subattr_{i}': str, substat description, i could be 1-4, example: '暴击率+3.5%', '攻击力+130'
            image: PIL.Image, screenshot of the artifact, will be shrinked to 300x512 to save space
        '''
        typeid = ArtsInfo.TypeNames.index(info['type'])
        setid = [i for i,v in enumerate(ArtsInfo.ArtNames) if info['name'] in v][0]
        self.name = info['name'] 
        self.type = ArtifactType(typeid)
        self.setname = ArtsInfo.SetNamesGenshinArt[setid]
        self.level = decodeValue(info['level'])
        self.rarity = info['star']
        self.stat = ArtifactStat(info['main_attr_name'], info['main_attr_value'])
        self.substats = [ArtifactStat(*info[tag].split('+')) for tag in sorted(info.keys()) if "subattr_" in tag]
        self.image = image.resize((300, 512))

class ArtDatabase:
    def __init__(self, path='artifacts.dat'):
        self.storage = ZODB.FileStorage.FileStorage(path)
        self.db = ZODB.DB(self.storage)
        self.conn = self.db.open()
        self.root = self.conn.root()
        if 'size' not in self.root:
            self.root['size'] = 0

    def add(self, info, art_img):
        try:
            self.root[str(self.root['size'])] = Artifact(info, art_img)
            self.root['size'] += 1
            transaction.commit()
            return True
        except Exception as e:
            return False

    def exportGenshinArtJSON(self, path):
        result = {"version":"1", "flower":[], "feather":[], "sand":[], "cup":[], "head":[]}
        for art_id in range(self.root['size']):
            art = self.root[str(art_id)]
            result[ArtsInfo.TypeNamesGenshinArt[art.type]].append(
                {
                    "setName": art.setname,
                    "position": ArtsInfo.TypeNamesGenshinArt[art.type],
                    "detailName": art.name,
                    "mainTag": {
                        'name': ArtsInfo.AttrNamesGensinArt[art.stat.type.name], 
                        'value': art.stat.value
                        },
                    "normalTags": [
                        {
                            'name': ArtsInfo.AttrNamesGensinArt[stat.type.name], 
                            'value': stat.value
                        }
                        for stat in art.substats
                    ],
                    "omit": False,
                    "id":art_id,
                    'level': art.level,
                    'star': art.rarity
                }
            )
        f = open(path, "wb")
        s = json.dumps(result, ensure_ascii=False)
        f.write(s.encode('utf-8'))
        f.close()
