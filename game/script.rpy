﻿# определяем персонажей
define dr = Character("Дракон")
define pr = Character("Принцесса")
define bg = Character(None)

init:
    image map = "img/bg/map.jpg"  # определение карт
    image map2 = "img/bg/map2.jpg"
image bg main = "img/bg/main.jpg"  # заставка главного меню
image place = ConditionSwitch(              
    "place == 'farscape'", "img/bg/far_scape.jpg",    # определение фонов для определенных мест  
    "place == 'cave'", "img/bg/cave.jpg",
    "place == 'castle'", "img/bg/castle.jpg",
    "place == 'market'", "img/bg/market.jpg",
    "place == 'road'", "img/bg/road.jpg",
    )

# Начало игры

label splashscreen:
    python:
        if not persistent.disclaimer_accepted:                  # Проверяем был ли принят дисклеймер. Если нет, то:
            disclaimer_status = renpy.call_screen("disclaimer") # Показываем экран с дисклеймером.
            if disclaimer_status:                               # И если дисклеймер приняли, то 
                persistent.disclaimer_accepted = True           # Сохраняем этот факт на будущее
    
    scene black
    with Pause(1)

    show text "Old Huntsman present..." with dissolve   # интро
    with Pause(1)
    
    show text "Defiler Wings" with dissolve
    with Pause(2)

    hide text with dissolve
    with Pause(1)

    return
    
label start:
    $ avatars = Avatars() # Инициализируем модуль с аватарками
    scene bg main
    menu:
        "Демо карты":
            jump SD_hellloop
        "Пропустить":
            jump SD_skip
label SD_skip:
    $ result = renpy.imagemap("img/bg/map.jpg", "img/bg/map2.jpg", [  # координаты кликабельных мест мапы
        (230, 230, 325, 315, "castle"),
        (520, 215, 585, 260, "road"),
        (690, 315, 750, 375, "cave"),
        (585, 375, 690, 435, "view"),
        ])
    
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
