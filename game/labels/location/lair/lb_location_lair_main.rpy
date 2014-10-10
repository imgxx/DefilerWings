label lb_location_lair_main:
    $ place = 'lair'
    show place as bg
    
    menu:
        'Осмотреть дракона':
            #чтобы вывести сообщение от имени дракона можно использовать "game.dragon"
            game.dragon "[game.dragon.description]"
        'Сотворить заклинание'  if game.dragon.energy() > 0:
            python:
                spells_menu = []
                for spell in data.spell_list.keys():
                    if spell not in game.dragon.spells:
                        spells_menu.append((data.spell_list_rus[spell], spell))
                spells_menu.append(('Вернуться в логово', 'back'))
                spell_name = renpy.display_menu(spells_menu)
                
            if spell_name == 'back':
                jump lb_location_lair_main
            else:
                python: 
                    game.dragon.spells.append(spell_name)
                    game.dragon.drain_energy()
                    game.dragon.gain_rage()

        'Чахнуть над златом' if game.lair.treasury.wealth > 0:
            #TODO: заменить на адекватный вариант
            $ description = u"%s собрал кучу сокровищ общей стоимостью %s" % (game.dragon.name, treasures.number_conjugation_rus(game.lair.treasury.wealth, u"фартинг"))
            nvl clear
            "[description]"
            menu:
                'Драгоценные камни':
                    nvl clear
                    "[game.lair.treasury.gems_list]"
                'Поделочные материалы':
                    nvl clear
                    "[game.lair.treasury.materials_list]"
                'Монеты':
                    nvl clear
                    $ description = u"В сокровищнице:\n"
                    $ description += u"%s\n" % treasures.number_conjugation_rus(game.lair.treasury.farting, u"фартинг")
                    $ description += u"%s\n" % treasures.number_conjugation_rus(game.lair.treasury.taller, u"талер")
                    $ description += u"%s" %treasures.number_conjugation_rus(game.lair.treasury.dublon, u"дублон")
                    "[description]"
                'Безделушки':
                    menu:
                        'Самая дорогая в сокровищнице':
                            nvl clear
                            "[game.lair.treasury.most_expensive_jewelry]"
                        'Случайная':
                            nvl clear
                            "[game.lair.treasury.random_jewelry]"
                        'Вернуться в логово':
                            jump lb_location_lair_main   
                'Вернуться в логово':
                    jump lb_location_lair_main                              

        'Проведать пленниц' if game.girls_list.prisoners_count:
            call screen girls_menu
        'Лечь спать':
            nvl clear
            python:
                # Делаем хитрую штуку.
                # Используем переменную game_loaded чтобы определить была ли игра загружена.
                # Но ставим ее перед самым сохранинием, используя renpy.retain_after_load() для того
                # чтобы она попала в сохранение.
                if 'game_loaded' in locals() and game_loaded:
                    del game_loaded
                    game.narrator("game loaded")
                    renpy.restart_interaction()
                else:
                    game_loaded = True
                    renpy.retain_after_load()
                    game.save()
                    game.sleep()
                    game.narrator("game saved")
                    del game_loaded
        'Покинуть логово':
            $ pass
            
    return