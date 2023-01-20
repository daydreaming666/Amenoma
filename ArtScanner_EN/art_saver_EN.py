import json
import os
import sys
from enum import IntEnum as Enum

import ZODB
import persistent
import transaction

import ArtsInfo
import utils
from utils import logger

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


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
    def __init__(self, name, value, rarity=0, level=0, isMain=False):
        name = ArtsInfo.AttrName2Ids_EN[name]
        value = utils.decodeValue(value)
        if type(value) == float and (name + '_PERCENT') in ArtsInfo.MainAttrNames_EN:
            name += '_PERCENT'
        self.type = getattr(ArtifactStatType, name)
        # self.value = value
        if isMain:
            try:
                self.value = ArtsInfo.MainAttrValue[rarity][name][level]
            except KeyError:
                self.value = value
        else:
            self.value = value

    def __eq__(self, other):
        if type(other) == int or type(other) == float:
            self_value_str = ArtsInfo.Formats[self.type.name].format(
                self.value + 1e-5)
            other_str = ArtsInfo.Formats[self.type.name].format(other + 1e-5)
            return other_str == self_value_str
        return str(self) == str(other)

    def compare_value(self, other):
        self_value_str = ArtsInfo.Formats[self.type.name].format(
            self.value + 1e-5)
        other_str = ArtsInfo.Formats[self.type.name].format(other + 1e-5)
        if self_value_str == other_str:
            return 0
        if utils.decodeValue(self_value_str) < utils.decodeValue(other_str):
            return -1
        return 1

    def __str__(self):
        return ArtsInfo.MainAttrNames_EN[self.type.name] + "+" + ArtsInfo.Formats[self.type.name].format(
            self.value + 1e-5)


class Artifact(persistent.Persistent):
    rare_substat_ranges = {getattr(ArtifactStatType, k): {j // 100: [i['PropValue'] for i in json.load(open(
        f'{bundle_dir}/Tools/ReliquaryAffixExcelConfigData.json')) if i['DepotId'] == j and i['PropType'] == k] for j in
                                                          [101, 201, 301, 401, 501]} for k in
                           ArtsInfo.SubAttrNames_EN.keys()}
    level_stat_range = {getattr(ArtifactStatType, k): {
        l: {r: sum([[j['Value'] for j in i['AddProps'] if j['PropType'] == k] for i in json.load(
            open(f'{bundle_dir}/Tools/ReliquaryLevelExcelConfigData.json')) if
                    i.get('Level', -1) == l + 1 and i.get('Rank', -1) == r], []) for r in range(1, 6)} for l in
        range(21)} for k in ArtsInfo.MainAttrNames_EN.keys()}

    def __init__(self, info, image):
        """
            info: dict with keys:
                'name': str, name of artifact
                'type': str, type of artifact
                'level': str/int, upgraded level of artifact, example: '+0', '0', 1
                'star': int, rarity, 1-5
                'main_attr_name': str, name of main stat
                'main_attr_value': str/int/float, main stat value, example: '38.5%', '4,760', 144
                'subattr_{i}': str, substat description, i could be 1-4, example: '暴击率+3.5%', '攻击力+130'
            image: PIL.Image, screenshot of the artifact, will be shrinked to 300x512 to save space
        """

        self.name = info['name']

        typeid = ArtsInfo.TypeNames_EN.index(info['type'])
        self.setid = info['setid']
        self.type = ArtifactType(typeid)
        self.level = utils.decodeValue(info['level'])
        self.rarity = info['star']
        self.locked = info['locked']
        self.equipped = (info['equipped']
                         if (info['equipped'] == "" or info['equipped'] == 'Traveler')
                         else ArtsInfo.UsersEN[info['equipped']])
        self.stat = ArtifactStat(
            info['main_attr_name'],
            info['main_attr_value'],
            rarity=self.rarity, level=self.level, isMain=True)
        self.substats = [ArtifactStat(*info[tag].split('+'))
                         for tag in sorted(info.keys()) if "subattr_" in tag]
        if image is not None:
            self.image = image.resize((300, 512))
        assert self.is_valid(), "Artifact attributes are not valid"

    def is_valid(self):
        if self.level > ArtsInfo.RarityToMaxLvs[self.rarity - 1]:
            logger.error(f"Save Artifact failed: bad level")
            return False
        if self.stat not in self.__class__.level_stat_range[self.stat.type][self.level][self.rarity]:
            logger.error(f"Save Artifact failed: bad main stat value")
            return False
        if not self.calculate_substat_upgrades():
            logger.error(f"Save Artifact failed: bad sub stat value")
            return False
        return True

    def calculate_substat_upgrades(self):
        def all_possible_combinations(l, n_comb):
            if n_comb == 0:
                return [0]
            t = all_possible_combinations(l, n_comb - 1)
            result = []
            for i in l:
                for j in t:
                    result.append(i + j)
            return result

        def all_possible_combinations_nested(l, target_values=None):
            if len(l) == 0:
                return [tuple()]
            t = all_possible_combinations_nested(l[1:], None)
            result = []
            for i in l[0]:
                for j in t:
                    if target_values is None or sum(j) + i in target_values:
                        result.append((i,) + j)
            return result

        n_upgrades = self.level // 4
        substat_upgrade_possibilities = []
        for i in self.substats:
            substat_range = sorted(
                self.__class__.rare_substat_ranges[i.type][self.rarity])
            substat_upgrade_possibilities.append([])
            for j in range(1, n_upgrades + 2):
                if i.compare_value(substat_range[-1] * j) > 0:
                    continue
                if i.compare_value(substat_range[0] * j) < 0:
                    break
                if i in [k for k in all_possible_combinations(substat_range, j)]:
                    substat_upgrade_possibilities[-1].append(j)
            if len(substat_upgrade_possibilities[-1]) == 0:
                return []
        return all_possible_combinations_nested(substat_upgrade_possibilities, target_values=set(
            [i + n_upgrades for i in ArtsInfo.RarityToBaseStatNumber[self.rarity]]))


class ArtDatabase:
    def __init__(self):
        self.db = ZODB.DB(None)
        self.conn = self.db.open()
        self.root = self.conn.root()
        self.root['size'] = 0

    def __del__(self):
        self.db.close()

    def add(self, info, art_img, raise_error=False):
        try:
            self.root[str(self.root['size'])] = Artifact(info, art_img)
            self.root['size'] += 1
            transaction.commit()
            return True
        except Exception as e:
            utils.logger.exception(e)
            if raise_error:
                raise
            return False

    def exportGOODJSON(self, settings: dict):
        path = settings['path']
        result = {
            "format": "GOOD",
            "version": 1,  # artifact only
            "source": "Amenoma",
            "artifacts": [],
        }
        for art_id in range(self.root['size']):
            art: Artifact = self.root[str(art_id)]
            res = {
                    "setKey": ArtsInfo.SetNamesGOOD[art.setid],
                    "slotKey": ArtsInfo.TypeNamesGOOD[art.type],
                    "level": art.level,
                    "rarity": art.rarity if 3 <= art.rarity <= 5 else 0,
                    "mainStatKey": ArtsInfo.AttrNamesGOOD[art.stat.type.name],
                    "location": art.equipped,
                    "lock": art.locked,
                    "substats": [
                        {
                            "key": ArtsInfo.AttrNamesGOOD[substat.type.name],
                            "value": round(substat.value * 100, 1)
                            if ArtsInfo.AttrNamesGOOD[substat.type.name].endswith("_")
                            else substat.value,
                        }
                        for substat in art.substats
                    ]
                }
            if not settings['exportLocation']:
                del res['location']
            result['artifacts'].append(res)

        if path and path != "":
            self.exportFile(path, result)
        else:
            return result

    def exportGenshinArtJSON(self, settings: dict):
        path = settings['path']
        result = {"version": "1", "flower": [],
                  "feather": [], "sand": [], "cup": [], "head": []}
        for art_id in range(self.root['size']):
            art = self.root[str(art_id)]
            result[ArtsInfo.TypeNamesGenshinArt[art.type]].append(
                {
                    "setName": ArtsInfo.SetNamesGenshinArt[art.setid],
                    "position": ArtsInfo.TypeNamesGenshinArt[art.type],
                    "detailName": art.name,
                    "mainTag": {
                        'name': ArtsInfo.AttrNamesGenshinArt[art.stat.type.name],
                        'value': art.stat.value
                    },
                    "normalTags": [
                        {
                            'name': ArtsInfo.AttrNamesGenshinArt[stat.type.name],
                            'value': stat.value
                        }
                        for stat in art.substats
                    ],
                    "omit": False,
                    "id": art_id,
                    'level': art.level,
                    'star': art.rarity
                })

        if path and path != "":
            self.exportFile(path, result)
        else:
            return result

    def exportGenmoCalcJSON(self, settings: dict):
        path = settings['path']
        result = []
        for art_id in range(self.root['size']):
            art = self.root[str(art_id)]
            if len(art.substats) < 4 or art.rarity != 5:
                continue
            info = {
                "asKey": ArtsInfo.SetNamesMingyuLab[art.setid],
                "rarity": art.rarity,
                "slot": ArtsInfo.TypeNamesMingyuLab[art.type],
                "level": art.level,
                "mainStat": ArtsInfo.AttrNamesMingyuLab[art.stat.type.name],
                "mark": "none"
            }
            for i, stat in enumerate(art.substats):
                info[f"subStat{i + 1}Type"] = ArtsInfo.AttrNamesMingyuLab[stat.type.name]
                info[f"subStat{i + 1}Value"] = \
                    ArtsInfo.Formats[stat.type.name].format(stat.value).replace('%', '').replace(',', '')
            result.append(info)

        if path and path != "":
            self.exportFile(path, result)
        else:
            return result

    @staticmethod
    def exportFile(path, result):
        f = open(path, "wb")
        s = json.dumps(result, ensure_ascii=False)
        f.write(s.encode('utf-8'))
        f.close()
