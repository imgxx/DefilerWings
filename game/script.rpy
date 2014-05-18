﻿init python:
    from pythoncode.core import Game
    from pythoncode.core import Dragon
    game = Game()
    drag = Dragon()

init:
    $ narrator = NVLCharacter(None, kind=nvl)
    define dragon =  Character("Дракон", color="#c8ffc8", kind=nvl, image="dragon")
    image side dragon = "dragon ava"
    image bg main = "img/bg/main.jpg"  # заставка главного меню
    image place = ConditionSwitch(              
        "place == 'farscape'", "img/bg/far_scape.jpg",    # определение фонов для определенных мест  
        "place == 'cave'", "img/bg/cave.jpg",
        "place == 'castle'", "img/bg/castle.jpg",
        "place == 'market'", "img/bg/market.jpg",
        "place == 'road'", "img/bg/road.jpg",
    )

# Начало игры
    
label start:
    $ avatars = Avatars() # Инициализируем модуль с аватарками
    
    show screen status_bar
    call screen main_map
    
    if result == "castle":           # то что происходит после клика
        scene bg main
        $ bg ("Куда теперь?")
        menu:
            'Рынок':
                $ place = 'market'
            'Замок':
                $ place = 'castle'
            'Карта':
                jump start
    if result == "road":
        menu:
            'Дорога':
                $ place = 'road'
            'Карта':
                jump start
    if result == "cave":
        menu:
            'Пещера':
                $ place = 'cave'
            'Карта':
                jump start
    if result == "view":
        menu:
            'Красивый вид':
                $ place = 'farscape'
            'Карта':
                jump start
        
    
    show place
    $ avatars.DisplayLeft("princess ava ") # Показываем принцессу слева
    $ avatars.DisplayRight("dragon ava") # Показываем дракона справа
    pr 'Hello world!'
    dr 'Grrrrr'
    jump start

    
    return
 
label fight:
    $ renpy.say(None, game.battle(game.knight, game.dragon))
    jump start

label lair:
    "Вы входите в логово"
    dragon "Аррггххх"
    $ renpy.say(dragon, 'Моё имя ' + drag.name + ', я ' + drag.kind())
    "dddfa"
    
