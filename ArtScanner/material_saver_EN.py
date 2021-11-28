import json

import ZODB
import persistent
import transaction

import MaterialInfo
import utils


class Material(persistent.Persistent):
    def __init__(self, info, detail_img, image):
        """
        :param info:  dict with keys
            'name'  : str,
            'amount': str,
        :param detail_img:
        :param image: the captured image or None
        """
        self.name = info['name']
        self.amount = info['amount']

        if image is not None:
            self.image = image


class MaterialDatabase:
    def __init__(self):
        self.db = ZODB.DB(None)
        self.conn = self.db.open()
        self.root = self.conn.root()
        self.root['size'] = 0

    def __del__(self):
        self.db.close()

    def add(self, info, detail_img, img, raise_error=False):
        try:
            self.root[str(self.root['size'])] = Material(info, detail_img, img)
            self.root['size'] += 1
            transaction.commit()
            return True
        except Exception as e:
            utils.logger.exception(e)
            if raise_error:
                raise
            return False

    def exportGOODJSON(self, path):
        result = {
            "format": "GOOD",
            "version": 0xef,
            "source": "Amenoma",
            "materials": {}
        }
        for index in range(int(self.root['size'])):
            material = self.root[str(index)]
            result['materials'][MaterialInfo.MaterialsNameEN[material.name]] = material.amount
        f = open(path, "wb")
        s = json.dumps(result, ensure_ascii=False)
        f.write(s.encode('utf-8'))
        f.close()
