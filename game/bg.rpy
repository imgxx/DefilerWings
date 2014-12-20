# coding=utf-8
init python:
    import os
    import random

    def get_place_bg(type):
        # config.basedir - директория где у нас лежит сама игра.
        # "game" - директория относительно config.basedir где лежат собственно файлы игры и
        # относительно которой высчитываются все пути
        relative_path = "img/bg/" + type  # Относительный путь для движка ренпи
        absolute_path = os.path.join(config.basedir, "game", relative_path)  # Cоставляем абсолютный путь где искать
        filename = random.choice(os.listdir(absolute_path))  # получаем название файла
        return relative_path + "/" + filename  # Возвращаем правильно отформатированно значение

init:
    image bg main = "img/bg/main.jpg"  # заставка главного меню
    image place = ConditionSwitch(
        "place == 'city_gates'", "img/bg/city/outside.png",    # определение фонов для разных мест (потребует доработки)
        "place == 'impassable_coomb'", "img/bg/lair/ravine.png",
        "place == 'impregnable_peak'", "img/bg/lair/cavelarge.png",
        "place == 'solitude_сitadel'", "img/bg/lair/icecave.png",
        "place == 'vulcano_chasm'", "img/bg/lair/volcanocave.png",
        "place == 'underwater_grot'", "img/bg/lair/grotto.png",
        "place == 'underground_burrow'", "img/bg/lair/burrow.png",
        "place == 'dragon_castle'", "img/bg/lair/dragon_castle.png",
        "place == 'castle'", "img/bg/lair/ruins_inside.png",
        "place == 'ogre_den'", "img/bg/lair/cave.png",
        "place == 'broad_cave'", "img/bg/lair/cavelarge.png",
        "place == 'forest_heart'", "img/bg/lair/elfruin.png",
        "place == 'tower_ruin'", "img/bg/lair/tower_lair.png",
        "place == 'monastery_ruin'", "img/bg/lair/crypt_lair.png",
        "place == 'fortress_ruin'", "img/bg/lair/fortress_lair.png",
        "place == 'castle_ruin'", "img/bg/lair/palace_lair.png",
        "place == 'ice_citadel'", "img/bg/lair/icecastle.png",
        "place == 'vulcanic_forge'", "img/bg/lair/volcanoforge.png",
        "place == 'cloud_castle'", "img/bg/lair/cloud_lair.png",
        "place == 'undefwater_mansion'", "img/bg/lair/underwater.png",
        "place == 'underground_palaces'", "img/bg/lair/dwarfruin.png",
        "place == 'forest'", "img/bg/forest/1.png",
        "place == 'mountain'", "img/bg/mountain/1.png",
        "place == 'plain'", "img/bg/plain/3.png",
        "place == 'road'", "img/bg/road/1.png",
        "place == 'sea'", "img/bg/sea/1.png",
        "place == 'sky'", "img/bg/sky/1.png",
        "place == 'gremlins'", "img/bg/special/gremlins.png",
        "place == 'smugglers'", "img/bg/special/smugglers.png",
        "place == 'mordor'", "img/bg/special/mordor.png",
        "place == 'prison'", "img/scene/prison.png",
    )
