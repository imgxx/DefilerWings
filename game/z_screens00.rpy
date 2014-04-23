init python:
    def SD_Test(st,at):   # функция обработки данных для отображения картинки с надписью
        txx = ''          # текст
        a_hide = 1.0      # параметр прозрачности. 0 = картинки нет
        SD_mapfocus = renpy.focus_coordinates()            # получим координаты изображения (displayable) на который указывает курсор мыши.
        if [SD_mapfocus[0],SD_mapfocus[1]] == [0,177]:     # это координаты городка
            dd = im.Image('./img/bg/market.jpg')           # задаём изображение для иконки городка городка
            txx = 'Рынок'                                  # текст для описания иконки городка
        elif [SD_mapfocus[0],SD_mapfocus[1]] == [817,5]:   # координаты вулкана
            dd = im.Image('./img/bg/cave.jpg')             # задаём изображение для иконки вулкана
            txx = 'Пещера'                                 # текст для описания иконки вулкана
        else:                                              # в любом другом случае
            dd = im.Image('./img/bg/veil.png')             # изображение полупрозрачный чёрный. Заглушка
            a_hide = 0.0                                   # выставляем прозрачность на максимум Изображения нет, текст пуст.
        # Соединяем оба куска (картинку(image) и текст) в одно изображение, задаём его размер;
        # добавляем картинку в заданные координаты, масштабируем картинку и применяем к ней значение прозрачности функцией Transform;
        # добавляем текст в заданные координаты.
        d = LiveComposite((300,100),(0,0),Transform(dd, size =(100,100),alpha = a_hide), (110,80),ui.text(txx)) 
        return (d,0.1)                                     # функция возвращает готовое изображение(displayable) и время перерисовки.

# изображения которые будут использованы при рисовании карты. 
# TODO Опасность конфликта именований.
image SD_testd = DynamicDisplayable(SD_Test)               # Динамическое изображение отображающее иконку и описание зоны. Определяется функцией, заданной выше.
image maptown idle = './img/bg/SD_maptown idle.png'
image maptown hover = './img/bg/SD_maptown hover.png'
image bg market = './img/bg/market.jpg'
image bg cave = './img/bg/cave.jpg'
image mapvolcano idle = './img/bg/SD_mapvolcano idle.png'
image mapvolcano hover = './img/bg/SD_mapvolcano hover.png'

label SD_hellloop:                                         # Цикл GoTo 10 ^_^
    scene                                                  # почистим экран перед испоользованием
    call screen SD_scr_Map                                 # вызовем экран с картой
    return                                                 # хз зачем. Эта строка никогда не активируется, но на всякий случай.
    
screen SD_scr_Map:                                         # Основное окно карты
    tag Main                                               # тэг экрана. Если отображается что-либо с таким же тэгом, данный инстанс его заменит.
    add './img/bg/map.jpg'                                 # Прямой путь до файла. Показывает саму карту.
    # Добавлет динамическое изображение, изменяющееся в зависимости от того, на что указывает курсор.                             
    add 'SD_testd' xpos 362 ypos 648
    # Добавляет две активные графические кнопки в определённых координатах.
    # Обе отображают состояния "неактивно" и "наведённый курсор".
    # При нажатии вызывается функция ассоциированная с действием (action).
    imagebutton xpos -15 ypos 177 idle 'maptown idle' hover 'maptown hover' action Jump('SD_0_site')
    imagebutton xpos 817 ypos 5 idle 'mapvolcano idle' hover 'mapvolcano hover' action Jump('SD_1_site')
    
label SD_0_site:                                            # стандартные ярлыки(label) игрового скрипта. 
    scene bg market                                         # На них ссылаются графические кнопки на экране карты.
    dr 'Съем пару торговцев!'
    return
    
label SD_1_site:
    scene bg cave
    dr 'Распарю старые косточки!'
    return

