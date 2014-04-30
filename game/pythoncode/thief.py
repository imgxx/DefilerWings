#encoding:utf-8
#!/usr/bin/python3

import random
__config__ = {
    'gemstone_type': {'алмазом': 16, 'рубином': 8, 'топазом': 4, 'аметистом': 2},
    'gemstone_size': {' с небольшим %s': 1, ' с %s': 4, ' с большим %s': 15, ' с большим %s в обрамлении нескольких небольших': 50},
    'jewellery_type': {'кольцо': 1, 'кулон': 3, 'ожерелье': 5, 'тиара': 6, 'корона': 15, 'скипетр': 25},
    'jewellery_metal': {'Золотой': 12, 'Серебряный': 1},
    'weapon_type': {
        'древком головой': {'Булава': 4, 'Моргенштерн': 7},
        'лезвием рукоятью': {'Кинжал': 1, 'Длинный меч': 9},
        'лезвием древком': {'Копье': 3, 'Топор': 8},
        'древком': {'Посох': 2}},
    'weapon_decorate': {
        'древком': {'резным': 1, 'полированным': 2},
        'головой': {'полированной': 1, 'вороненой': 2, 'травленой': 3, 'посеребренной': 4, 'позолочнной': 5},
        'лезвием': {'полированным': 2, 'вороненым': 3, 'травленым': 4, 'посеребренным': 5, 'позолочнным': 6},
        'рукоятью': {'золотой': 12, 'серебряной': 1}}}


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
    config = {'о': {'ой': 'ое', 'ый': 'ое'}, 'и': {'ой': 'ые', 'ый': 'ые'}, 'н': {'ой': 'ой', 'ый': 'ый'},
        'е': {'ой': 'ое', 'ый': 'ое'}, 'а': {'ой': 'ая', 'ый': 'ая'}, 'р': {'ой': 'ой', 'ый': 'ый'}}
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
                decorate_name = 'с %s %s' % (weapon_decorate_type_name, weapon_decorates[0])
                possible_weapon.append((weapon_cost + weapon_decorate_type_cost, '%s %s' % (weapon_name, decorate_name)))
                if len(weapon_decorates) > 1:
                    for second_weapon_decorate_type_name, second_weapon_decorate_type_cost in __config__['weapon_decorate'][weapon_decorates[1]].items():
                        second_decorate_name = '%s %s' % (second_weapon_decorate_type_name, weapon_decorates[1])
                        possible_weapon.append((weapon_cost + weapon_decorate_type_cost + second_weapon_decorate_type_cost, '%s %s и %s' % (weapon_name, decorate_name, second_decorate_name)))
            if len(weapon_decorates) > 1:
                for second_weapon_decorate_type_name, second_weapon_decorate_type_cost in __config__['weapon_decorate'][weapon_decorates[1]].items():
                    second_decorate_name = 'с %s %s' % (second_weapon_decorate_type_name, weapon_decorates[1])
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
        output.append((summa / 2, 'Серебро'))
        summa += summa / 2
    output.reverse()
    return output


class Dragon(object):
    config = {
        'possible_lair_defense': (('Механические ловушки', 1), ('Магические ловушки', 1), ('Ядовитые твари', 1), ('Охрана', 2), ('Элитная охрана', 3)),
        'possible_lair_location': (
            ('Буреломный овраг', 0, []),
            ('Неприступная вершина', 0, ['альпинизм']),
            ('Цитадель одиночества', 0, ['альпинизм', 'защита от холода']),
            ('Вулканическая расселина', 0, ['альпинизм', 'защита от огня']),
            ('Подводный грот', 0, ['плаванье']),
            ('Подземная нора', 1, []),
            ('Драконий замок', 1, []),
            ('Берлога людоеда', 1, []),
            ('Просторная пещера', 1, []),
            ('Руины башни', 0, []),
            ('Руины монастыря', 1, []),
            ('Руины каменной крепости', 2, []),
            ('Руины королевского замка', 3, []),
            ('Ледяная цитадель', 1, ['альпинизм', 'защита от холода']),
            ('Вулканическая кузница', 1, ['защита от огня']),
            ('Замок в облаках', 2, ['полёт']),
            ('Подводные хоромы', 1, ['плаванье']),
            ('Подгорные чертоги', 2, ['альпинизм']))}

    def __init__(self):
        self.sleep = True
        self.ill_fame_level = 0
        self.ill_fame_point = 0
        self.treasure_room = []
        self.treasure_room_silver = 0
        self.achievement = {'Страж сокровищ': True}
        self.lair_location = ('Буреломный овраг', 0, [])
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
            self.achievement['Страж сокровищ'] = False
        elif data['result'] in ['death', 'catch']:
            self.ill_fame_point += data['level'] + len(data['items'])
            self.thief_loot.extend(data['items'])
        if 'comment' in data:
            print(data['comment'])
        if 'sex' in data:
            if data['sex'] == 'female':
                print('Дракон: получена девственница')
            else:
                print('Дракон: съеден вор')
        del self.my_enemy['thief']

    def give_item(self, item):
        if 'thief' in self.my_enemy:
            self.thief_loot.remove(item)
            self.my_enemy['thief'].take_item(item)

    def switch_sleep(self):
        self.sleep = False if self.sleep else True
        print('Дракон: sleep =', str(self.sleep))

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
            if treasure[1] == 'Серебро':
                self.treasure_room_silver += treasure[0]
            else:
                self.treasure_room.append(treasure)

    def remove_treasure(self, treasure_list):
        for treasure in treasure_list:
            if treasure[1] == 'Серебро':
                self.treasure_room_silver -= treasure[0]
            else:
                self.treasure_room.remove(treasure)

    def list_treasure(self):
        return self.treasure_room + [(self.treasure_room_silver, 'Серебро')]


class Thief(object):
    config = {
        'possible_level_name': {5: 'мастер-вор', 4: 'расхититель гробниц', 3: 'взломщик', 2: 'домушник', 1: 'мародёр'},
        'male_name': ['Натан', 'Лео', 'Энзо', 'Луи', 'Жюль', 'Тимео', 'Уго', 'Артюр', 'Этан', 'Матис', 'Адам', 'Нолан', 'Клеман'],
        'female_name': ['Эмма', 'Лола', 'Клоэ', 'Инес', 'Леа', 'Мано', 'Зоэ', 'Лилу', 'Лина', 'Эва', 'Луна', 'Алис'],
        'male_nickname': ['Золотой', 'Худой', 'Лысый', 'Рыжий', 'Сиплый', 'Хромой', 'Касой', 'Сизый', 'Палёный'],
        'female_nickname': ['Штучка', 'Тихая', 'Кошка', 'Королева', 'Ловкая', 'Скользкая', 'Хитрая', 'Серебряная'],
        'unisex_nickname': ['Луковица', 'Медведь', 'Кирпич', 'Левша', 'Тень', 'Снежинка', 'Гадюка', 'Искра', 'Точило'],
        'possible_ability': {
            'Альпинист': ['альпинизм'],
            'Ныряльщик': ['плаванье'],
            'Жадина': [],
            'Механик': [],
            'Знаток магии': [],
            'Отравитель': [],
            'Ассасин': [],
            'Ночная тень': [],
            'Ловкач': []},
        'possible_items': {
            'План ограбления': [[], 'Плохой план'],
            'Схема тайных проходов': [[], None],
            'Сонный порошок': [[], None],
            'Бездонный мешок': [[], 'Дырявый мешок'],
            'Антидот': [['Твари'], None],
            'Зачарованный кинжал': [[], 'Проклятый кинжал'],
            'Кольцо-невидимка': [[], 'Кольцо мерцания'],
            'Летучие сандалии': [['полёт', 'альпинизм'], 'Ощипанные сандалии'],
            'Охлаждающий амулет': [['защита от огня'], 'Морозильный амулет'],
            'Согревающий амулет': [['защита от холода'], 'Шашлычный амулет']}}

    def __init__(self, target, level):
        self.target = target
        self.level = level
        self.ability = list(set([random.choice(list(self.config['possible_ability'].keys())) for index in range(self.level) if d(2)]))
        self.level_name = self.config['possible_level_name'][level] if level in self.config['possible_level_name'] else 'вор %s' % str(level)
        self.sex = random.choice(['male', 'female'])
        self.name = self.make_name()
        self.items = []
        print('debug: Появился %s по имени %s' % (self.level_name, self.name))  # debug

    def about(self):
        print('имя =', self.name)
        print('уровень =', self.level_name)
        print('способности:' + ', '.join(self.ability))
        print('пол =', self.sex)
        print('предметы:' + '\n'.join(self.items))

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
            print('debug: %s выжидает.' % self.name)  # debug

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
                self.target.del_thief({'result': 'pass', 'comment': 'debug: %s сдается из за невозможности добраться до логова' % self.name})
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
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': [], 'comment': 'дорога убила'})
            return
        if 'План ограбления' in self.items:
            luck = self.level + 1
        elif 'Плохой план' in self.items:
            luck = self.level - 1
        else:
            luck = self.level
        if 'Схема тайных проходов' not in self.items:
            luck -= sum([1 for index in range(self.target.check_lair_inaccessibility()) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': 'неприступность убила'})
            return
        lair_defense = dict(self.target.get_lair_defense())
        if 'Механик' not in self.ability:
            if 'Механические ловушки' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['Механические ловушки']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': 'Механические ловушки убили'})
            return
        if 'Знаток магии' not in self.ability:
            if 'Магические ловушки' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['Магические ловушки']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': 'Магические ловушки убили'})
            return
        if 'Отравитель' not in self.ability and 'Антидот' not in self.items and 'Ядовитые твари' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['Ядовитые твари']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'death', 'level': self.level, 'items': self.breaking_items(), 'comment': 'Ядовитые твари убили'})
            return
        if 'Проклятый кинжал' in self.items and 'Охрана' in lair_defense:
            luck -= lair_defense['Охрана']
        else:
            if 'Ассасин' not in self.ability and 'Зачарованный кинжал' not in self.items and 'Охрана' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['Охрана']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': 'Охрана поймала'})
            return
        if 'Кольцо мерцания' in self.items and 'Элитная охрана' in lair_defense:
            luck -= lair_defense['Элитная охрана']
        else:
            if 'Ночная тень' not in self.ability and 'Кольцо-невидимка' not in self.items and 'Элитная охрана' in lair_defense:
                luck -= sum([1 for index in range(lair_defense['Элитная охрана']) if d()])
        if luck < 0:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': 'Элитная охрана поймала'})
            return
        if luck > 0:
            self.theft(luck)

    def theft(self, luck):
        if 'Жадина' in self.ability:
            luck += 1
        if 'Бездонный мешок' in self.items:
            luck += 1
        spoil = []
        fail = False
        while luck > 0 and not fail:
            list_treasure = list(reversed(sorted(self.target.list_treasure())))
            treasure = (100, 'Серебро')
            if len(list_treasure) > 1:
                if list_treasure[0][1] == 'Серебро' and (list_treasure[1][0] or list_treasure[1][0] > list_treasure[0][0]) > 100:
                    treasure = list_treasure[1]
                elif list_treasure[0][1] != 'Серебро' and list_treasure[0][0] > 100:
                    treasure = list_treasure[0]
            elif len(list_treasure) == 1:
                if list_treasure[0][1] != 'Серебро' or (list_treasure[0][1] == 'Серебро' and list_treasure[0][0] < 100):
                    treasure = list_treasure[0]
            else:
                break
            if 'Ловкач' not in self.ability and 'Сонный порошок' not in self.items:
                if d(5 - self.level, 10):
                    fail = True
            if not fail:
                self.target.remove_treasure([treasure])
                spoil.append(treasure)
            luck -= 1
        if fail:
            self.target.del_thief({'result': 'catch', 'level': self.level, 'items': self.breaking_items(), 'sex': self.sex, 'comment': 'дракон поймал'})
        else:
            if 'Дырявый мешок' in self.items:
                self.target.add_treasure(spoil)
            self.target.del_thief({'result': 'success'})


def main():
    dragon = Dragon()
    menu = '''menu:
    0 выход
    1 о драконе
    2 получить сокровища
    3 заснуть/проснутся
    4 сменить логово
    5 добавить/убрать зашиту
    6 уровень славы
    7 о воре
    8 дать вору предмет
    9 убить вора'''
    print(menu)
    dragon.add_treasure(get_treasure(123))  # debug
    while True:
        menu_item = input('###Введите номер: ')
        if menu_item == '':
            if 'thief' in dragon.my_enemy:
                work = dragon.my_enemy['thief'].act()
            else:
                if dragon.sleep:
                    if dragon.make_thief():
                        work = dragon.my_enemy['thief'].act()
        elif menu_item == '0':
            break
        elif menu_item == '1':
            print('золотое ложе =', sum([index[0] for index in dragon.list_treasure()]))
            print('sleep =', str(dragon.sleep))
            print('уровень славы =', str(dragon.ill_fame_level))
            print('очки славы =', str(dragon.ill_fame_point))
            print('логово =', dragon.lair_location[0])
            print('страж сокровищ =', str(dragon.achievement['Страж сокровищ']))
            print('защита логова:\n' + '\n'.join([name for name, value in dragon.lair_defense]))
            print('воровские предметы:\n' + '\n'.join(dragon.thief_loot))
        elif menu_item == '2':
            try:
                dragon.add_treasure(get_treasure(int(input('###Введите количество сокровищ: '))))
            except ValueError:
                print('###Вводите число!')
        elif menu_item == '3':
            dragon.switch_sleep()
        elif menu_item == '4':
            print('логово =', dragon.lair_location[0])
            for num, lair in enumerate(dragon.config['possible_lair_location']):
                print(num, lair[0])
            try:
                dragon.lair_location = dragon.config['possible_lair_location'][int(input('###Введите номер логова: '))]
            except ValueError:
                print('###Вводите число!')
        elif menu_item == '5':
            dragon.lair_defense
            for num, defense in enumerate(dragon.config['possible_lair_defense']):
                print(num, defense[0], '=', str(defense in dragon.lair_defense))
            try:
                number = int(input('###Введите номер зашиты: '))
                if dragon.config['possible_lair_defense'][number] in dragon.lair_defense:
                    dragon.lair_defense.remove(dragon.config['possible_lair_defense'][number])
                else:
                    dragon.lair_defense.append(dragon.config['possible_lair_defense'][number])
            except ValueError:
                print('###Вводите число!')
        elif menu_item == '6':
            try:
                dragon.ill_fame_level = int(input('###Введите уровень славы: '))
            except ValueError:
                print('###Вводите число!')
        elif menu_item == '7':
            if 'thief' in dragon.my_enemy:
                dragon.my_enemy['thief'].about()
        elif menu_item == '8':
            if 'thief' in dragon.my_enemy:
                for num, lair in enumerate(dragon.thief_loot):
                    print(num, lair)
                try:
                    number = int(input('###Введите номер предмета: '))
                    dragon.give_item(dragon.thief_loot[number])
                except ValueError:
                    print('###Вводите число!')
        elif menu_item == '9':
            if 'thief' in dragon.my_enemy:
                del dragon.my_enemy['thief']
        else:
            print(menu)


if __name__ == '__main__':
    main()
