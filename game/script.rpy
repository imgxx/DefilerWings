﻿# coding=utf-8
init python:
    # Импортируем нужные библиотеки. Возможно это надо засунуть в какой-то отдельный файл инициализации.
    from pythoncode import data
    from pythoncode import core
    from pythoncode import treasures
    from copy import deepcopy
    # Заряжаем пасхалки. Их можно будет встретить в игре лишь однажды
    # Встреченную пасхалку следует добавить в persistent.seen_encounters
    # Проверить была ли встречена пасхалка: if <encounter> (not) in persistent.seen_encounters
    if not hasattr(persistent, 'seen_encounters'):
        persistent.seen_encounters = []
    freeplay = bool()
    save_blocked = False
# Начало игры
    
label start:
    python:
        # Инициализируем game в начале игры, а не при инициализации. Для того чтобы
        game = core.Game(adv_character=ADVCharacter, nvl_character=NVLCharacter)
        narrator = game.narrator    # Ради совместимости с обычным синтаксисом RenPy
    # Прокручиваем заставку.
    call screen sc_intro
    while not game.is_won or not game.is_lost:
        # Если даркона нет выбираем его
        if game.dragon is None or game.dragon.is_dead:
            if not freeplay:
                call lb_choose_dragon
            else:
                call lb_dragon_creator
        $ renpy.block_rollback()
        $ target_label = renpy.call_screen("main_map")
        if renpy.has_label(target_label):
            $ renpy.call(target_label)
        else:
            $ renpy.call("lb_location_missed")
    
    return
