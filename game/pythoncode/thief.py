# -*- coding: cp866 -*-

import random
__config__ = {
    'gemstone_type': {'�������': 16, '�㡨���': 8, '⮯����': 4, '�����⮬': 2},
    'gemstone_size': {' � ������訬 %s': 1, ' � %s': 4, ' � ����訬 %s': 15, ' � ����訬 %s � ��ࠬ����� ��᪮�쪨� ��������': 50},
    'jewellery_type': {'�����': 1, '�㫮�': 3, '���५�': 5, '⨠�': 6, '��஭�': 15, '᪨����': 25},
    'jewellery_metal': {'����⮩': 12, '��ॡ���': 1},
    'weapon_type': {
        '�ॢ��� �������': {'�㫠��': 4, '��ࣥ����': 7},
        '������� �㪮����': {'������': 1, '������ ���': 9},
        '������� �ॢ���': {'����': 3, '�����': 8},
        '�ॢ���': {'����': 2}},
    'weapon_decorate': {
        '�ॢ���': {'१��': 1, '����஢����': 2},
        '�������': {'����஢�����': 1, '��஭����': 2, '�ࠢ�����': 3, '���ॡ७���': 4, '������筭��': 5},
        '�������': {'����஢����': 2, '��஭���': 3, '�ࠢ����': 4, '���ॡ७��': 5, '������筭�': 6},
        '�㪮����': {'����⮩': 12, '�ॡ�ﭮ�': 1}}}


def d(*args):
    if len(args) == 0:
        true = 1
        false = 2
    if len(args) == 1:
        true = 1
        false = args[0] - 1
    if len(args) == 2:
        true = args[0]
        false = args[1] - args[0]
    return random.choice([True for index in range(true)] + [False for index in range(false)])


def rusconvert(word1, word2):
    config = {'�': {'��': '��', '�': '��'}, '�': {'��': '�', '�': '�'}, '�': {'��': '��', '�': '�'},
        '�': {'��': '��', '�': '��'}, '�': {'��': '��', '�': '��'}, '�': {'��': '��', '�': '�'}}
    for key, value in config.items():
        if word1[-len(key):] == key:
            for key2, value2 in value.items():
                if word2[-len(key2):] == key2:
                    return word2[:-len(key2)] + value2


def get_some_weapon():
    possible_weapon = []
    for weapon_type, weapon_names in __config__['weapon_type'].items():
        weapon_decorates = weapon_type.split()
        for weapon_name, weapon_cost in weapon_names.items():
            possible_weapon.append((weapon_cost, weapon_name))
            for weapon_decorate_type_name, weapon_decorate_type_cost in __config__['weapon_decorate'][weapon_decorates[0]].items():
                decorate_name = '� %s %s' % (weapon_decorate_type_name, weapon_decorates[0])
                possible_weapon.append((weapon_cost + weapon_decorate_type_cost, '%s %s' % (weapon_name, decorate_name)))
                if len(weapon_decorates) > 1:
                    for second_weapon_decorate_type_name, second_weapon_decorate_type_cost in __config__['weapon_decorate'][weapon_decorates[1]].items():
                        second_decorate_name = '%s %s' % (second_weapon_decorate_type_name, weapon_decorates[1])
                        possible_weapon.append((weapon_cost + weapon_decorate_type_cost + second_weapon_decorate_type_cost, '%s %s � %s' % (weapon_name, decorate_name, second_decorate_name)))
            if len(weapon_decorates) > 1:
                for second_weapon_decorate_type_name, second_weapon_decorate_type_cost in __config__['weapon_decorate'][weapon_decorates[1]].items():
                    second_decorate_name = '� %s %s' % (second_weapon_decorate_type_name, weapon_decorates[1])
                    possible_weapon.append((weapon_cost + second_weapon_decorate_type_cost, '%s %s' % (weapon_name, second_decorate_name)))
    return possible_weapon


def get_some_jewellery():
    possible_jewellery = []
    for jewellery_metal_name, jewellery_metal_cost in __config__['jewellery_metal'].items():
        for jewellery_type_name, jewellery_type_cost in __config__['jewellery_type'].items():
            cost = jewellery_metal_cost * jewellery_type_cost
            jewellery = '%s %s' % (rusconvert(jewellery_type_name, jewellery_metal_name), jewellery_type_name)
            possible_jewellery.append((cost, jewellery))
            for gemstone_size_name, gemstone_size_cost in __config__['gemstone_size'].items():
                for gemstone_type_name, gemstone_type_cost in __config__['gemstone_type'].items():
                    cost_with_gemstone = cost + gemstone_size_cost * gemstone_type_cost
                    jewellery_with_gemstone = jewellery + (gemstone_size_name % gemstone_type_name)
                    possible_jewellery.append((cost_with_gemstone, jewellery_with_gemstone))
    return possible_jewellery


def get_treasure(quantity):
    if quantity >= 3:
        coin = True
        if (quantity - 1) % 2 == 0:
            weapon_quantity = jewellery_quantity = (quantity - 1) / 2
        else:
            quantity_list = [(quantity - 1) / 2, (quantity) / 2]
            random.shuffle(quantity_list)
            weapon_quantity, jewellery_quantity = quantity_list
    elif quantity == 2:
        weapon_quantity = jewellery_quantity = 1
        coin = False
    elif quantity == 1:
        quantity_list = [0, 1]
        random.shuffle(quantity_list)
        weapon_quantity, jewellery_quantity = quantity_list
        coin = False
    else:
        coin = False
        weapon_quantity = jewellery_quantity = 0
    possible_jewellery = get_some_jewellery()
    possible_weapon = get_some_weapon()
    output = []
    summa = 0
    while jewellery_quantity > 0:
        cost, name = random.choice(possible_jewellery)
        output.append((cost, name))
        summa += cost
        jewellery_quantity -= 1
    while weapon_quantity > 0:
        cost, name = random.choice(possible_weapon)
        output.append((cost, name))
        summa += cost
        weapon_quantity -= 1
    if coin:
        output.append((summa / 2, '��ॡ�'))
        summa += summa / 2
    output.reverse()
    return output


class Dragon(object):
    config = {
        'possible_lair_defense': (('��堭��᪨� ����誨', 1), ('�����᪨� ����誨', 1), ('������� ⢠�', 1), ('��࠭�', 2), ('���⭠� ��࠭�', 3)),
        'possible_lair_location': (
            ('��५���� ��ࠣ', 0, []),
            ('������㯭�� ���設�', 0, ['��쯨����']),
            ('��⠤��� �������⢠', 0, ['��쯨����', '���� �� 宫���']),
            ('�㫪����᪠� ��ᥫ���', 0, ['��쯨����', '���� �� ����']),
            ('�������� ���', 0, ['�������']),
            ('��������� ���', 1, []),
            ('�ࠪ���� �����', 1, []),
            ('��૮�� ����', 1, []),
            ('����ୠ� ����', 1, []),
            ('�㨭� ��譨', 0, []),
            ('�㨭� ���������', 1, []),
            ('�㨭� �������� �९���', 2, []),
            ('�㨭� ��஫��᪮�� �����', 3, []),
            ('���ﭠ� �⠤���', 1, ['��쯨����', '���� �� 宫���']),
            ('�㫪����᪠� �㧭��', 1, ['���� �� ����']),
            ('����� � �������', 2, ['�����']),
            ('�������� �஬�', 1, ['�������']),
            ('������� ��⮣�', 2, ['��쯨����']))}

    def __init__(self):
        self.sleep = True
        self.ill_fame_level = 0
        self.ill_fame_point = 0
        self.treasure_room = []
        self.treasure_room_silver = 0
        self.achievement = {'��ࠦ ᮪஢��': True}
        self.lair_location = ('��५���� ��ࠣ', 0, [])
        self.lair_defense = []
        self.my_enemy = {}
        self.thief_loot = []

    def make_thief(self):
        thief_level = sum([1 for index in range(3 + self.ill_fame_level) if d()])
        if thief_level > 0:
            self.my_enemy['thief'] = Thief(self, thief_level)
            return True
        else:
            return False

    def del_thief(self, data):
        if data['result'] == 'success':
            self.achievement['��ࠦ ᮪஢��'] = False
        elif data['result'] in ['death', 'catch']:
            self.ill_fame_point += data['level'] + len(data['items'])
            self.thief_loot.extend(data['items'])
        if 'comment' in data:
            print('debug: ' + data['comment'])
        if 'sex' in data:
            if data['sex'] == 'female':
                print('�ࠪ��: ����祭� ����⢥����')
            else:
                print('�ࠪ��: �ꥤ�� ���')
        del self.my_enemy['thief']

    def give_item(self, item):
        if 'thief' in self.my_enemy:
            self.thief_loot.remove(item)
            self.my_enemy['thief'].take_item(item)

    def switch_sleep(self):
        self.sleep = False if self.sleep else True
        print('�ࠪ��: sleep = ' + str(self.sleep))

    def check_lair_restriction(self):
        return self.lair_location[2]

    def check_lair_inaccessibility(self):
        return self.lair_location[1]

    def get_lair_defense(self):
        return self.lair_defense

    def check_sleep(self):
        return self.sleep

    def add_treasure(self, treasure_list):
        for treasure in treasure_list:
            if treasure[1] == '��ॡ�':
                self.treasure_room_silver += treasure[0]
            else:
                self.treasure_room.append(treasure)

    def remove_treasure(self, treasure_list):
        for treasure in treasure_list:
            if treasure[1] == '��ॡ�':
                self.treasure_room_silver -= treasure[0]
            else:
                self.treasure_room.remove(treasure)

    def list_treasure(self):
        return self.treasure_room + [(self.treasure_room_silver, '��ॡ�')]


class Thief(object):
    config = {
        'possible_level_name': {5: '�����-���', 4: '����⥫� �஡���', 3: '�����騪', 2: '����譨�', 1: '��த��'},
        'male_name': ['��⠭', '���', '����', '��', '���', '�����', '���', '�����', '�⠭', '����', '����', '�����', '������'],
        'female_name': ['����', '����', '����', '����', '���', '����', '���', '����', '����', '���', '�㭠', '����'],
        'male_nickname': ['����⮩', '�㤮�', '����', '�릨�', '�����', '�஬��', '��ᮩ', '����', '�����'],
        'female_nickname': ['���窠', '����', '��誠', '��஫���', '������', '����짪��', '�����', '��ॡ�ﭠ�'],
        'unisex_nickname': ['�㪮���', '�������', '��௨�', '����', '����', '��������', '���', '���', '��稫�'],
        'possible_ability': {
            '��쯨����': ['��쯨����'],
            '�����騪': ['�������'],
            '������': [],
            '��堭��': [],
            '���⮪ �����': [],
            '��ࠢ�⥫�': [],
            '���ᨭ': [],
            '��筠� ⥭�': [],
            '������': []},
        'possible_items': {
            '���� ��ࠡ�����': [[], '���宩 ����'],
            '�奬� ⠩��� ��室��': [[], None],
            '����� ���讪': [[], None],
            '�������� ��讪': [[], '����� ��讪'],
            '��⨤��': [['����'], None],
            '���஢���� ������': [[], '�ப���� ������'],
            '�����-���������': [[], '����� ���栭��'],
            '����稥 ᠭ�����': [['�����', '��쯨����'], '�騯���� ᠭ�����'],
            '�嫠����騩 ��㫥�': [['���� �� ����'], '��஧���� ��㫥�'],
            '���ॢ��騩 ��㫥�': [['���� �� 宫���'], '������ ��㫥�']}}

    def __init__(self, target, level):
        self.target = target
        self.level = level
        self.ability = list(set([random.choice(list(self.config['possible_ability'].keys())) for index in range(self.level) if d(2)]))
        self.level_name = self.config['possible_level_name'][level] if level in self.config['possible_level_name'] else '��� %s' % str(level)
        self.sex = random.choice(['male', 'female'])
        self.name = self.make_name()
        self.items = []
        print('debug: ����� %s �� ����� %s' % (self.level_name, self.name)) # debug

    def about(self):
        print('��� = ' + self.name)
        print('��� = ' + self.sex)
        print('�஢��� = ' + self.level_name)
        print('ᯮᮡ����:' + '\n'.join(self.ability))
        print('�।����:' + '\n'.join(self.items))

    def make_name(self):
        if random.choice([False, True]):
            if self.sex == 'male':
                name = random.choice(self.config['male_nickname']) + ' ' + random.choice(self.config['male_name'])
            else:
                name = random.choice(self.config['female_nickname']) + ' ' + random.choice(self.config['female_name'])
        else:
            if self.sex == 'male':
                name = random.choice(self.config['male_name']) + ' ' + random.choice(self.config['unisex_nickname'])
            else:
                name = random.choice(self.config['female_name']) + ' ' + random.choice(self.config['unisex_nickname'])
        return name

    def find_effects(self):
        effects = []
        for ability in self.ability:
            if ability in self.config['possible_ability']:
                effects.extend(self.config['possible_ability'][ability])
        for key, value in self.config['possible_items'].items():
            for item in self.items:
                if item == key or item == value[1]:
                    effects.extend(value[0])
        return set(effects)

    def breaking_items(self):
        output = []
        for item in self.items:
            if item in self.config['possible_items']:
                if self.config['possible_items'][item][1] is not None:
                    output.append(self.config['possible_items'][item][1])
            else:
                output.append(item)
        return output

    def take_item(self, bad_item):
        self.items = [bad_item] + [index for index in self.items if self.config['possible_items'][index][1] != bad_item]

    def act(self):
        if self.target.check_sleep():
            if d(self.level + len(self.items), 6):
                must_have_item_effect = self.go_to_lair()
                if len(must_have_item_effect) == 0:
                    self.sneak()
                else:
                    self.preparation(must_have_item_effect)
            else:
                self.preparation()
        else:
            print('debug: %s �릨����.' % self.name) # debug

    def preparation(self, must_have_item_effect=None):
        if must_have_item_effect is None:
            possible_items = list(set(self.config['possible_items'].keys()) - set(self.items))
        else:
            possible_items = list(set([key for key, value in self.config['possible_items'].items() if must_have_item_effect[0] in value[0]]) - set(self.items))
        if len(possible_items) == 0:
            must_have_item_effect = self.go_to_lair()
            if len(must_have_item_effect) == 0:
                self.sneak()
            else:
                self.target.del_thief({'result': 'pass', 'comment': 'debug: %s ᤠ���� �� �� ������������ �������� �� ������' % self.name})
        else:
            if d(2):
                self.items.append(random.choice(possible_items))

    def go_to_lair(self):
        return list(set(self.target.check_lair_restriction()) - self.find_effects())

    def sneak(self):
        death = False
        for key, value in self.config['possible_items'].items():
            for item in self.items:
                if item == value[1] and item is not None:
                    if len(set(value[0]) | set(self.target.check_lair_restriction())) != 0:
                        death = True
        if death:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': [], 'comment': '��ண� 㡨��'})
            return
        if '���� ��ࠡ�����' in self.items:
            luck = self.level + 1
        elif '���宩 ����' in self.items:
            luck = self.level - 1
        else:
            luck = self.level
        if '�奬� ⠩��� ��室��' not in self.items:
            luck -= sum([1 for index in range(self.target.check_lair_inaccessibility()) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': '������㯭���� 㡨��'})
            return
        lair_defense = dict(self.target.get_lair_defense())
        if '��堭��' not in self.ability:
            if '��堭��᪨� ����誨' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['��堭��᪨� ����誨']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': '��堭��᪨� ����誨 㡨��'})
            return
        if '���⮪ �����' not in self.ability:
            if '�����᪨� ����誨' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['�����᪨� ����誨']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': '�����᪨� ����誨 㡨��'})
            return
        if '��ࠢ�⥫�' not in self.ability and '��⨤��' not in self.items and '������� ⢠�' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['������� ⢠�']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': '������� ⢠� 㡨��'})
            return
        if '�ப���� ������' in self.items and '��࠭�' in lair_defense:
            luck -= lair_defense['��࠭�']
        else:
            if '���ᨭ' not in self.ability and '���஢���� ������' not in self.items and '��࠭�' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['��࠭�']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': '��࠭� �������'})
            return
        if '����� ���栭��' in self.items and '���⭠� ��࠭�' in lair_defense:
            luck -= lair_defense['���⭠� ��࠭�']
        else:
            if '��筠� ⥭�' not in self.ability and '�����-���������' not in self.items and '���⭠� ��࠭�' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['���⭠� ��࠭�']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': '���⭠� ��࠭� �������'})
            return
        if luck > 0:
            self.theft(luck)

    def theft(self, luck):
        if '������' in self.ability:
            luck += 1
        if '�������� ��讪' in self.items:
            luck += 1
        spoil = []
        fail = False
        while luck > 0 and not fail:
            list_treasure = list(reversed(sorted(self.target.list_treasure())))
            treasure = (100, '��ॡ�')
            if len(list_treasure) > 1:
                if list_treasure[0][1] == '��ॡ�' and (list_treasure[1][0] or list_treasure[1][0] > list_treasure[0][0]) > 100:
                    treasure = list_treasure[1]
                elif list_treasure[0][1] != '��ॡ�' and list_treasure[0][0] > 100:
                    treasure = list_treasure[0]
            elif len(list_treasure) == 1:
                if list_treasure[0][1] != '��ॡ�' or (list_treasure[0][1] == '��ॡ�' and list_treasure[0][0] < 100):
                    treasure = list_treasure[0]
            else:
                break
            if '������' not in self.ability and '����� ���讪' not in self.items:
                if d(5 - self.level, 10):
                    fail = True
            if not fail:
                self.target.remove_treasure([treasure])
                spoil.append(treasure)
            luck -= 1
        if fail:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': '�ࠪ�� ������'})
        else:
            if '����� ��讪' in self.items:
                self.target.add_treasure(spoil)
            self.target.del_thief({'result': 'success', 'comment': '�ࠦ� �ᯥ譠'})


def main():
    dragon = Dragon()
    menu = '''menu:
0 ��室
1 � �ࠪ���
2 ������� ᮪஢��
3 ������/�������
4 ᬥ���� ������
5 ��������/���� �����
6 �஢��� ᫠��
7 � ���
8 ���� ���� �।���
9 㡨�� ���'''
    print(menu)
    dragon.add_treasure(get_treasure(123)) # debug
    while True:
        menu_item = raw_input('###������ �����: ')
        if str(menu_item) == '':
            if 'thief' in dragon.my_enemy:
                work = dragon.my_enemy['thief'].act()
            else:
                if dragon.sleep:
                    if dragon.make_thief():
                        work = dragon.my_enemy['thief'].act()
        elif menu_item == '0':
            break
        elif menu_item == '1':
            print('����⮥ ���� = ' + str(sum([index[0] for index in dragon.list_treasure()])))
            print('sleep = ' + str(dragon.sleep))
            print('�஢��� ᫠�� = ' + str(dragon.ill_fame_level))
            print('�窨 ᫠�� = ' + str(dragon.ill_fame_point))
            print('������ = ' + dragon.lair_location[0])
            print('��ࠦ ᮪஢�� = ' + str(dragon.achievement['��ࠦ ᮪஢��']))
            print('���� ������:\n' + '\n'.join([name for name, value in dragon.lair_defense]))
            print('��஢᪨� �।����:\n' + '\n'.join(dragon.thief_loot))
        elif menu_item == '2':
            try:
                dragon.add_treasure(get_treasure(int(raw_input('###������ ������⢮ ᮪஢��: '))))
            except ValueError:
                print('###������ �᫮!')
        elif menu_item == '3':
            dragon.switch_sleep()
        elif menu_item == '4':
            print('������ = ' + dragon.lair_location[0])
            for num, lair in enumerate(dragon.config['possible_lair_location']):
                print(str(num) + lair[0])
            try:
                dragon.lair_location = dragon.config['possible_lair_location'][int(input('###������ ����� ������: '))]
            except ValueError:
                print('###������ �᫮!')
        elif menu_item == '5':
            dragon.lair_defense
            for num, defense in enumerate(dragon.config['possible_lair_defense']):
                print(str(num) + defense[0] + ' = ' + str(defense in dragon.lair_defense))
            try:
                number = int(raw_input('###������ ����� �����: '))
                if dragon.config['possible_lair_defense'][number] in dragon.lair_defense:
                    dragon.lair_defense.remove(dragon.config['possible_lair_defense'][number])
                else:
                    dragon.lair_defense.append(dragon.config['possible_lair_defense'][number])
            except ValueError:
                print('###������ �᫮!')
        elif menu_item == '6':
            try:
                dragon.ill_fame_level = int(raw_input('###������ �஢��� ᫠��: '))
            except ValueError:
                print('###������ �᫮!')
        elif menu_item == '7':
            if 'thief' in dragon.my_enemy:
                dragon.my_enemy['thief'].about()
        elif menu_item == '8':
            if 'thief' in dragon.my_enemy:
                for num, lair in enumerate(dragon.thief_loot):
                    print(str(num) + lair)
                try:
                    number = int(raw_input('###������ ����� �।���: '))
                    dragon.give_item(dragon.thief_loot[number])
                except ValueError:
                    print('###������ �᫮!')
        elif menu_item == '9':
            if 'thief' in dragon.my_enemy:
                del dragon.my_enemy['thief']
        else:
            print(menu)


if __name__ == '__main__':
    main()
