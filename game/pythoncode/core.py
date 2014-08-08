#!/usr/bin/env python
# coding=utf-8
import random
import math
import data
from data import get_modifier
from copy import deepcopy
import renpy.exports as renpy
import renpy as renpy_internal
import renpy.store as store
names = {}
names['peasant'] = [u'Манька', u'Зойка', u'Жанна']

def tuples_sum(tuple_list):
    return sum([first for first, _ in tuple_list]), sum([second for _, second in tuple_list])


class Game(store.object):
    def __init__(self, base_character):
        """
        :param base_character: Базовый класс для персонажа. Скорее всего NVLCharacter.
        """
        self.base_character = base_character
        self.thief = None
        self.lair = None  # текущее логово
        self.reputation_points = 0  # Дурная слава дракона
        self.mobilization = 0  # мобилизация королевства
        self._year = 0  # текущий год
        self.currentCharacter = None # Последний говоривший персонаж. Используется для поиска аватарки.
        
                
        self.lair = Lair()
        self.dragon = Dragon(gameRef=self, base_character=base_character)
        self.knight = Knight(gameRef=self, base_character=base_character)
        self.narrator = Sayer(gameRef=self, base_character=base_character)
        self.girl = Girl(gameRef=self, base_character=base_character)
        self.thief = Thief(reputation=self.reputation(), gameRef=self, base_character=base_character)

    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, value):
        if value >= self._year:
            self._year = value
        else:
            raise Exception ("Время не может течь назад")
        
    def save(self):
        '''
        Логика сохранения игры.
        '''
        renpy.rename_save("1-1", "1-2") #Переименовываем старый сейв
        renpy.take_screenshot() # Делаем скриншот для отображения в сейве
        renpy.save("1-1")               # Сохраняем игру
        return True
    
    def battle(self, fighter1, fighter2):
        """
        Логика сражения.
        :param fighter1: Fighter
        :param fighter2: Fighter
        :return: Текст описывающий сражение.
        """
        hit1 = sum(fighter1.attack()[key][1] for key in fighter1.attack())
        for attacks in range(1,sum(fighter1.attack()[key][0] for key in fighter1.attack()) +1):
            dice = random.randint(1,3)
            if dice ==1:
                hit1 +=1       
        hit2 = sum(fighter2.attack()[key][1] for key in fighter2.attack())
        for attacks in range(1, sum(fighter2.attack()[key][0] for key in fighter2.attack()) +1):
            dice = random.randint(1,3)
            if dice == 1:
                hit2 += 1
        prot1 = sum(fighter1.protection()[key][1] for key in fighter1.protection())
        for protects in range(1, sum(fighter1.protection()[key][1]for key in fighter1.protection())+1):
            dice = random.randint(1,3)
            if dice == 1:
                prot1 +=1
        prot2 = sum(fighter2.protection()[key][1] for key in fighter2.protection())
        for protects in range(1, sum(fighter2.protection()[key][1] for key in fighter2.protection())+1):
            dice = random.randint(1,3)
            if dice ==1:
                prot2 +=1        
        """
        Возможные результаты боя
        """
        if hit1 > prot2:#Дракон попал
            if hit2 <= prot1:
                return (True, u"%s Побеждает %s не получив ран"%(fighter1.name, fighter2.name))
            elif hit2 > prot1:
                return (True, u"%s Побеждает %s получив рану"%(fighter1.name, fighter2.name))
                #также увеличиваем показатель ранений дракона   
        elif hit1 <= prot2:#дракон не попал
            if hit2 <= prot1:
                return (False, u"%s не побеждает, ран нет"%(fighter1.name))
                #тут предлагаем игроку бежать или продолжить бой
            elif hit2 > prot1:
                return (False, u"%s не побеждает, ранен"%(fighter1.name))
                #тут предлагаем игроку бежать или продолжить бой
                #также увеличиваем показатель ранений дракона

    def next_year(self):
        '''
        Логика смены года.
        Проверки на появление/левелап/рейд рыцаря/вора.
        Изменение дурной славы.
        Что-то ещё?
        '''
        self.year += 1
        # Если вора нет, то пробуем создать его
        if self.thief is None:
            self.thief = Thief(reputation=self.reputation(), gameRef=self, base_character = self.base_character)
        else: # Иначе пробуем его пустить на дело
            if random.choice(range(6)) in range(1+len(self.thief.items)):
                #self.thief.do_stuff() # Идем на дело
                pass
            else:
                if random.choice(range(2)) == 0:    # C 50% шансом получаем шмотку
                    self.thief.receive_item()

    def sleep(self):
        """
        Рассчитывается количество лет которое дракон проспит.
        Попытки бегства женщин.
        Сброс характеристик дракона.
        """
        time_to_sleep = self.dragon.injuries + 1
        # Сбрасываем характеристики дракона
        self.dragon.rest()
        # Спим
        for i in xrange(time_to_sleep):
            self.year += 1
            self.next_year()
            if self.knight:
                if 1 == random.randint(1, 3):
                    self.knight.upgrade()
            else:
                self._create_knight()
            if self.thief:
                if 1 == random.randint(1, 3):
                    self.thief.upgrade()
            else:
                self._create_knight()

    def _create_knight(self):
        """
        Проверка на появление рыцаря.
        """
        raise NotImplementedError

    def _create_thief(self):
        """
        Проверка на появление вора.
        """
        raise NotImplementedError

    def reputation(self):
        """
        Видимые игроку очки дурной славы.
        Рассчитываются по хитрой формуле.
        """
        #т.к. логарифма нуля не существует, а меньше 1 логарифм будет отрицательным
        if self.reputation_points < 1:
            return 0
        return math.floor(math.log(self.reputation_points))
        
    @staticmethod
    def weighted_random(data):
        """
        :param data: list of tuples (option, weight), где option - возвращаемый вариант, а
                     weight - вес варианта. Чем больше, тем вероятнее что он выпадет.
        :return: option, или None, если сделать выбор не удалось.
        Пример использования:
        coin_flip = weighted_random([("орёл", 1), ("решка",1)])
        """
        if len(data)>0:
            import bisect
            #Складываем вес всех доступных энкаунтеров
            accumulated = []
            total = 0
            for option, weight in data:
                assert weight >= 0
                accumulated.append(weight + total)
                total += weight
            #Проверяем, что суммарный вес не равен нулю.
            if total == 0:
                return None
            r = random.random() * accumulated[-1]
            return data[bisect.bisect(accumulated, r)][0]
        return None


class Treasury(object):
    def __init__(self):
        self.copper_coins = 0
        self.silver_coins = 0
        self.gold_coins = 0
        # списки строк
        self.materials = []
        self.jewelry = []
        self.equipment = []

    def money(self):
        """
        :return: Суммарная стоимость всего, что есть в сокровищнице(Золотое ложе).
        """
        raise NotImplementedError


class Lair(object):
    def __init__(self, type = "impassable_coomb"):
        self.type = data.Container(type, data.lair_types[type])
        self.upgrades = data.Container('lair_upgrades')
        self.inaccessibility = 0
        # Сокровищиница
        self.treasury = Treasury()
        # Список модификаций(ловушки, стражи и.т.п.)
        self.modifiers = []
        # Список женщин в логове
        self.women = []
        
    def reachable(self, abilities):
        '''
        Функция для проверки доступности логова
        :param abilities: - список способностей у того, кто пытается достичь, например, для вора: [ 'alpinism', 'swimming' ]
        :return: Возращает True ,если до логова можно добраться и False если нет
        '''
        for r in self.requirements():
            if r not in abilities:
                return False
        return True
    
    def requirements(self):
        '''
        :return: Возвращает список способностей которые нужны чтобы достичь логова.
        '''
        if self.upgrades.requires:
            return self.type.require + self.upgrades.require
        return self.type.require

class Sayer(store.object):
    '''
    Базовый класс для всего что умеет говорить
    '''
    def __init__(self,gameRef, base_character, *args, **kwargs):
        """
        :param gameRef: Game object
        :param base_character: base_character базовый класс персонажа от которого будет вестись вещание
        """
        self.avatar = None      # По умолчанию аватарки нет
        self._gameRef = gameRef # Проставляем ссылку на игру
        self._base_character = base_character # На всякий случай если захотим пересоздать (но зачем?)
        self._real_character = base_character() # Создаем объект от которого будет вестись вещание
    
    @property   #Задаем имя через свойство, чтобы при изменении его передавать в персонажа.
    def name(self):
        return self._real_character.name
    
    @name.setter
    def name(self, value):
        self._real_character.name = value
        
    def __call__(self, *args, **kwargs):
        """
        Этот метод используется при попытке сказать что-то персонажем.
        Переопределяем, чтобы сообщить игре, что сейчас говорит этот персонаж.
        """
        self._gameRef.currentCharacter = self # Прописываем кто говорит в настоящий момент
        self._real_character(*args, **kwargs) # На самом деле говорим
        
    def third(self, *args, **kwargs):
        '''
        Говорим от третьего лица. Принимаются предложения на более удачное название.
        Например прямая речь:
        $ game.person ("Что-нибудь")
        game.person "Где-нибудь"
        Рассказ о том что делает этот персонаж:
        $ game.person.third("Делая что-нибудь")
        game.person.third "Делая где-нибудь"
        '''
        self._gameRef.currentCharacter = self # Делаем вид, что сказали сами
        self._gameRef.narrator._real_character(*args, **kwargs) # Говорим о лица нарратора. Грязный хак.
        

class Girl(Sayer):
    """
    Базовый класс для всего, с чем можно заниматься сексом.
    """
            
    def __init__(self, *args, **kwargs):
        super(Girl, self).__init__(*args, **kwargs) # Инициализируем родителя
        self.virgin = True # девственность = пригодность для оплодотворения драконом
        self.pregnant = 0 # 0 - не беременна, 1 - беременна базовым отродьем, 2 - беременна продвинутым отродьем
        self.quality = 0 # Репродуктивное качество женщины. Если коварство дракона превышает её репродуктивное качество, то отродье будет продвинутым. Иначе базовым
        self.status = 'free' # 'free' - находится вне логова и жива, 'hostage' - заточена в логове и жива, 'dead' - умерла  
        self.name = random.choice(names['peasant'])
        self.treashure = []
            
class Fighter(Sayer):
    """
    Базовый класс для всего, что способно драться.
    Декоратор нужен чтобы реализовывать эффекты вроде иммунитета или ядовитого дыхания.
    То есть такие, которые воздействуют на модификаторы противника.
    """

    def __init__(self, *args, **kwargs):
        """
        :param gameRef: Game object
        """
        super(Fighter, self).__init__(*args, **kwargs)
        self._modifiers = []
        self.avatar = None # По умолчанию аватарки нет, нужно выбрать в потомках.

    def protection(self):
        """
        :rtype : dict
        :return: Значение защиты данного бойца в виде котртежа (защита, верная защита).
        """
        result = dict()
        for type in data.protection_types:
            result[type] = tuples_sum(
                [get_modifier(mod).protection[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).protection[0] == type]
            )
        return result

    def attack(self):
        """
        :rtype : dict
        :return: Словарик, ключами которого являются типы атаки(лед, огонь, яд...),
        а значениями кортежи вида (атака, верная атака)
        """
        result = dict()
        for type in data.attack_types:
            result[type] = tuples_sum(
                [get_modifier(mod).attack[1]
                 for mod in self.modifiers()
                 if get_modifier(mod).attack[0] == type]
            )
        return result

class Dragon(Fighter):
    """
    Класс дракона.
    """

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        # TODO: нужно дать игроку возможность называть своего дракона при первом выборе выборе и давать следующим драконом это имя как фамильное после рандомного личного
        self.name = u"Старый Охотник"
        self._tiredness = 0  # увеличивается при каждом действии
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.hunger = 3  # range 0..3, ресурс восстанавливается до 3 после каждого отдыха
        self.health = 2 # range 0..2, ресурс восстанавливается до 2 после каждого отдыха
        self.reputation_points = 1 # при наборе определённого количества растёт уровень дурной славы

        self.anatomy = ['size', 'paws', 'size', 'wings', 'size', 'paws']
        self.heads = ['green']  # головы дракона
        self.spells = []  # заклинания наложенные на дракона(обнуляются после сна)
        self.avatar = "img/avadragon/green/1.jpg"

    def _debug_print(self):
        # self(u'Дракон по имени {0}'.format(self.name))
        # self(u'Список всех модификаторов {0}'.format(', '.join(self.modifiers())))
        # self(u'Вид дракона {0}'.format(self.kind()))
        # self(u'Размер {0}'.format(data.size_texts[self.size()]))
        # self(u'Анатомия дракона {0}'.format(', '.join(self.anatomy)))
        # self(u'Наложенная на дракона магия {0}'.format(' '.join(self.spells)))
        # self(u'Цвета голов дракона {0}'.format(', '.join(self.heads)))
        # self(u'Энергия {0} из {1}'.format(self.energy(), self.max_energy()))
        # self(u'Могущество {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.attack().items()])))
        # self(u'Несокрушимость {0}'.format(', '.join(['{0} {1}'.format(k, v) for k, v in self.protection().items()])))
        # self(u'Коварство {0}'.format(self.magic()))
        # self(u'Чудовищиность {0}'.format(self.fear()))
        children = self.children()
        for child in children:
            self(u'Ребенок {0}'.format(', '.join(child.anatomy[-3:] + child.heads)))


    def modifiers(self):
        """
        :return: Список модификаторов дракона
        """
        return self.anatomy + \
               [mod for head_color in self.heads for mod in data.dragon_heads[head_color]] + \
               [mod for spell in self.spells for mod in data.spell_list[spell]]

    def max_energy(self):
        """
        :return: Максимальная энергия(целое число)
        """
        return sum([get_modifier(mod).max_energy for mod in self.modifiers()])

    def energy(self):
        """
        :return: Оставшаяся энергия(целое число)
        """
        return self.max_energy() - self._tiredness
        
    def drain_energy(self, drain=1):
        """
        :param drain: количество отнимаемой у дракона энергии.
        :return: True если успешно, иначе False.
        """
        if self.energy() - drain >= 0:
            self._tiredness = self._tiredness + drain
            return True
        return False
            
    def gain_rage(self, gain=1):
        """
        Увеличивает раздражение дракона на :gain:
        """
        if self.bloodiness < 5:
            self.bloodiness += 1
            return True
        return False
                
    def magic(self):
        """
        :return: Магическая сила(целое число)
        """
        return sum([get_modifier(mod).magic for mod in self.modifiers()])
            
    def reputation(self):
        """
        Видимые игроку очки дурной славы.
        Рассчитываются по хитрой формуле.
        """
        return math.floor(math.log(self.reputation_points))
        
    def fear(self):
        """
        :return: Значение чудовищносити(целое число)
        """
        return sum([get_modifier(mod).fear for mod in self.modifiers()])

    def rest(self):
        self._tiredness = 0  # range 0..max_energy
        self.bloodiness = 0  # range 0..5
        self.lust = 3  # range 0..3
        self.hunger = 3  # range 0..3
        self.spells = []  # заклинания сбрасываются

    def color(self):
        """
        :return: Текстовое представление базового цвета дракона
        """
        if self.heads[0] == 'red':
            return u'красный'
        elif self.heads[0] == 'black':
            return u'черный'
        elif self.heads[0] == 'blue':
            return u'синий'
        elif self.heads[0] == 'gold':
            return u'золотой'
        elif self.heads[0] == 'silver':
            return u'серебряный'
        elif self.heads[0] == 'copper':
            return u'бронзовый'
        elif self.heads[0] == 'iron':
            return u'стальной'
        elif self.heads[0] == 'shadow':
            return u'фантомный'
        elif self.heads[0] == 'white':
            return u'белый'
        else:
            return u'зеленый'

    def kind(self):
        """
        :return: Текстовое представление 'вида' дракона
        """
        wings = self.wings()
        paws = self.paws()
        heads = len(self.heads)
        if wings == 0 and paws == 0:
            return u"ползучий гад"
        if wings > 0 and paws == 0:
            return u'летучий гад'
        if wings == 0 and paws >= 0:
            return u'линдвурм'
        if wings > 0 and paws == 1:
            return u'вирвен'
        if wings == 0 and heads > 1:
            if heads == 2:
                return u'двуглавый гидра'
            if heads == 3:
                return u'трехглавый гидра'
            if heads == 4:
                return u'четырёхглавый гидра'
            if heads == 5:
                return u'пятиглавый гидра'
            if heads == 6:
                return u'шестиглавый гидра'
            if heads == 7:
                return u'семиглавый гидрус'
        if wings == 1 and paws == 2 and heads == 1:
            return u'дракон'
        if wings > 0 and paws >= 1 and heads > 1:
            if heads == 2:
                return u'двуглавый дракон'
            if heads == 3:
                return u'трехглавый дракон'
            if heads == 4:
                return u'четырёхглавый дракон'
            if heads == 5:
                return u'пятиглавый дракон'
            if heads == 6:
                return u'шестиглавый дракон'
            if heads == 7:
                return u'семиглавый дракон'

    def size(self):
        """
        :return: Размер дракона(число от 1 до 6)
        """
        return self.modifiers().count('size')

    def wings(self):
        """
        :return: Количество пар крыльев
        """
        return self.modifiers().count('wings')

    def paws(self):
        """
        :return: Количество пар лап
        """
        return self.modifiers().count('paws')

    def children(self):
        """
        Сгенерировать список потомков.
        Вызывается при отставке дракона.
        :return: list of Dragons
        """
        # Обнуляем заклинания, они уже не понадобятся
        self.spells = []
        # Формируем список возможных улучшений
        dragon_leveling = ['head']
        if self.size() < 6:
            dragon_leveling += ['size']
        if self.paws() < 3:
            dragon_leveling += ['paws']
        if self.wings() < 3:
            dragon_leveling += ['wings']
        if 'tough_scale' not in self.modifiers():
            dragon_leveling += ['tough_scale']
        if 'clutches' not in self.modifiers():
            dragon_leveling += ['clutches']
        if 'fangs' not in self.modifiers() and self.paws() > 0:
            dragon_leveling += ['fangs']
        if 'horns' not in self.modifiers():
            dragon_leveling += ['horns']
        if 'ugly' not in self.modifiers():
            dragon_leveling += ['ugly']
        if 'poisoned_sting' not in self.modifiers():
            dragon_leveling += ['poisoned_sting']
        if self.modifiers().count('cunning') < 3:
            dragon_leveling += ['cunning']
        if self.heads.count('green') > 0:
            dragon_leveling += ['color']
        # Выбираем три случайных способности
        number_of_abilities = 3
        new_abilities = random.sample(dragon_leveling, number_of_abilities)
        children = [deepcopy(self) for i in range(0, number_of_abilities)]
        for i in range(0, number_of_abilities):
            if new_abilities[i] == 'color':
                # список возможных цветов
                colors = ['red', 'white', 'blue', 'black', 'iron', 'copper', 'silver', 'gold', 'shadow']
                children[i].heads[self.heads.index('green')] = random.choice(colors)
            elif new_abilities[i] == 'head':
                children[i].heads += ['green']
            else:
                children[i].anatomy += [new_abilities[i]]
        return children


class Enemy(Fighter):
    """
    Класс одноразового противника для энкаунтера.
    """

    def __init__(self, kind = 'generic',  *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Enemy, self).__init__(*args, **kwargs)
        self.name = data.mob[kind]['name']
        self.power = data.mob[kind]['power']
        self.defence = data.mob[kind]['defence']
        self.fight_intro = data.mob[kind]['intro']
        self.abilities = []
        self.equipment = []

    def modifiers(self):
        return []

    def attack(self):
        return self.power

    def protection(self):
        return self.defence

class Knight(Fighter):
    """
    Класс рыцаря.
    Набросок для тестирования боя.
    Спутников, особенности и снаряжение предпологается засовывать в переменную _modifiers
    """

    def __init__(self, *args, **kwargs):
        """
        Здесь должна быть генерация нового рыцаря.
        """
        super(Knight, self).__init__(*args, **kwargs)
        self.name = u"Сер Ланселот Озёрный"
        self.power = 1
        self.abilities = []
        self.equipment = [u"щит", u"меч", u"броня", u"копьё", u"скакун", u"спутник"]

    def modifiers(self):
        return self._modifiers + self.abilities + self.equipment

    def attack(self):
        a = super(Knight, self).attack()
        if "liberator" in self.modifiers():
            # TODO: подумать как получаем ссылку на логово
            # Увеличиваем атаку в соответствии со списком женщин в логове
            raise NotImplementedError
        a['base'][0] + self.power
        return a

    def protection(self):
        p = super(Knight, self).protection()
        if "liberator" in self.modifiers():
            # Увеличиваем защиту в соответствии со списком женщин в логове
            raise NotImplementedError
        p['base'][0] + self.power
        return p

    def title(self):
        """
        :return: Текстовое представление 'звания' рыцаря.
        """
        if self.power == 1:
            return u"Бедный рыцарь"
        elif self.power == 2:
            return u"Странствующий рыцарь"
        elif self.power == 3:
            return u"Межевой рыцарь"
        elif self.power == 4:
            return u"Благородный рыцарь"
        elif self.power == 5:
            return u"Паладин рыцарь"
        elif self.power == 6:
            return u"Прекрасный принц"
        else:
            assert False, u"Недопустимое значение поля power"

    def upgrade(self):
        """
        Метод вызвается если рыцать не пошел драться с драконом.
        Добавляет новое снаряжение.
        """
        raise NotImplementedError

class Thief(Sayer):
    """
    Класс вора.
    """
    
    def __new__(cls, reputation, **kwargs):
        obj = super(Thief, cls).__new__(cls, **kwargs)
        skill = 0
        for i in range(3+reputation):
            if random.choice(range(3)) == 0:
                skill += 1
        # Если не повезло и уровень вора по прежнему на нуле - он не появляется
        if skill == 0:
            return None
        else:
            obj._skill = skill
            return obj
    
    def __init__(self, *args, **kwargs):
        super(Thief, self).__init__(*args, **kwargs)
        self.name = "%s %s" % (random.choice(data.thief_first_names), random.choice(data.thief_last_names))
        self.abilities = data.Container("thief_abilities")
        self.items = data.Container("thief_items")
        # Определяем способности вора
        ability_list = [ a for a in data.thief_abilities ] # Составляем список из возможных способностей
        ability_list = ability_list + [ None for i in range(len(ability_list)) ] # Добавляем невалидных вариантов
        for level in range(self._skill):
            ab = random.choice(ability_list)
            if ab is not None and ab not in self.abilities:
                self.abilities.add(ab, data.thief_abilities[ab])

    @property # Read-Only
    def skill(self):
        return self._skill + self.items.sum("skill")

    def title(self):
        """
        :return: Текстовое представление 'звания' вора.
        """
        try:
            return data.thief_titles[self.skill - 1]
        except:
            raise Exception("Cannot determine title for skill level %s" % self.skill)

    def receive_item(self):
        #TODO: учесь что список может быть пустым
        item_list = [ i for i in data.thief_items if i not in self.items ]
        item = random.choice(item_list)
        self.items.add(item, data.thief_items[item])
        self(u"Я получил предмет %s" % data.thief_items[item].name)
        return True

    def new_item(self):
        """
        Метод вызвается если вор не пошел грабить дракона.
        Здесь идёт выбор новой вещи(подготовка к грабежу).
        """
        raise NotImplementedError
    
    def description(self):
        '''
        Описание вора, возвращает строку с описанием.
        TODO: добавить описания вещей
        '''
        d = []
        d.append(u"Мастерство: %d" % self.skill)
        if self.abilities:
            d.append(u"Способности: ")
            for ability in self.abilities:
                d.append(u"    %s: %s" % (self.abilities[ability].name, self.abilities[ability].description))
        else:
            d.append(u"Способности отсутствуют")
        if self.items:
            d.append(u"Вещи:")
            for item in self.items:
                d.append(u"    %s: %s" % (self.items[item].name, self.items[item].description))
        else:
            d.append(u"Вещи отсутствуют")
        return u"\n".join(d)
    
    def steal(self, lair):
        '''
        Вор пытается урасть что-нибудь.
        :param lair: Логово из которого происходит кража
        '''
        # Для начала пытаемся понять можем ли мы попасть в логово:
        if lair.reachable([ a for ab in self.abilities for a in self.abilities[ab].provide ]):
            # TODO: логика сломанных предметов
            luck = self.skill
            # Проверка неприступности
            for i in range(lair.inaccessability):
                if random.choice(range(3)) == 0:
                    luck -= 1
            if luck < 0:
                self.die ("inaccessability")
            # Проверка ловушек и стражей
            for upgrade in lair.upgrades:
                for i in range(data.lair_upgrades[upgrade].protection):
                    if random.choice(range(3)) == 0:
                        luck -= 1
                    if luck < 0:
                        self.die(upgrade)
            if luck == 0:
                pass # Отступаем
            else:
                # Грабим логово
                # TODO: Добавить проклятые вещи
                attempts = 1
                if "greedy" in self.abilities:
                    attempts += 1
                if "bottomless_sac" in self.items:
                    attempts *= 2
                for i in range(attemtps):
                    if random.choice(range(10)) in range(5 - self.skill):
                        #Берем шмотку
                        self("Взял бы шмотку, но пока ничего не релизовали")
                    else:
                        #Мы разбудили дракона
                        self.die("wake_up")
        else: #До логова добраться не получилось, получаем предмет c 50%м шансом
            if random.choice(range(2)) == 0:
                self.thief.receive_item()
    
    def check_luck(self, luck):
        pass
    
    def die(self, reason=None):
        '''
        Вор умирает
        '''
        if reason is None:
            self("Я погиб при невыясненных обстоятельствах.")
        else:
            target_label = "lb_thief_die_"+reason
            if renpy.has_label(target_label):
                renpy.call(target_label)
            else:
                renpy.call("lb_missed", label = target_label)
        self = None
        
