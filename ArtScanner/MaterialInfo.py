import json
import os

current_path = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(current_path, 'rcc/material_names_v25.json'), encoding='utf-8'))

MaterialsNameCHS = data['CHS']
MaterialsNameEN = data['EN']

if __name__ == '__main__':
    print(f"{MaterialsNameCHS=}")
    print(f"{MaterialsNameEN=}")
