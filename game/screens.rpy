﻿# coding=utf-8
# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    use sc_dialog(who, game.currentCharacter.avatar, what)
    use status_bar
    # Use the quick menu.
    use quick_menu


##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window:
        style "menu_window"
        xalign 0.3
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, action, chosen in items:
                if action:
                    button:
                        action action
                        style "menu_choice_button"
                        text caption style "menu_choice"
                else:
                    text caption style "menu_caption"

    use status_bar

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)

    python:
        style.menu_choice_button.background = Frame("img/bg/button-idle.png", 5, 5)
        style.menu_choice_button.hover_background = Frame("img/bg/button-hovered.png", 5, 5)
        style.menu_choice_button.ypadding = 4


##############################################################################
# DF_Choice
#
# Custom screen that's used to display in-game menus.
#
# На вход экрану подается список из опций выбора, со следущем синтаксисом.
# (caption, value, visible=True, condition=True)
# где:
#   caption - текст опции
#   value - возвращаемое значение при выборе этой опции
#   visible - условие при котором опция видна, по-умолчанию True
#   condition - условие при котором опция доступна для выбора, по-умолчанию True
# Пример листа:
#  [("Пункт 1", 1, True, False), - Видимый, но недоступный для выбора пункт
#   ("Пункт 2", 2, persistent.punkt2_visible) - пункт показываестя только если ранее переменная persistent.punkt2_visible была выставлена в True
#   ("Пункт 3", 3, persistent.punkt3_visible, energy > 10)] - тоже самое что пункт2 + можно выбрать только при значении energy > 10
screen dw_choice(items):
    window:
        style "menu_window"
        xalign 0.3
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, value, visible, condition in items:
                if visible and condition:
                    button:
                        action Return(value)
                        style "menu_choice_button"
                        text caption style "menu_choice"
                if visible and not condition:
                    button:
                        action NullAction()
                        style "menu_choice_button"
                        text caption style "menu_choice_inactive"
    use status_bar

init python:
    # Наследуем дефолтный стиль для текста
    style.menu_choice_inactive = Style("menu_choice")
    # И делаем текст серым, чтобы показать его недоступность
    style.menu_choice_inactive.color = "#C0C0C0"

##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"
        xpos 200
        xsize 760
        align(0.0, 0.0)

        viewport:
            mousewheel True
            scrollbars "vertical"
            yinitial 1.0

            has vbox:
                style "nvl_vbox"

            # Display dialogue.
            for who, what, who_id, what_id, window_id in dialogue:
                window:
                    id window_id
                    has hbox:
                        spacing 10
                    if who is not None:
                        text who id who_id
                    text what id what_id

            # Display a menu, if given.
            if items:
                vbox:
                    id "menu"
                    for caption, action, chosen in items:
                        if action:
                            button:
                                style "nvl_menu_choice_button"
                                action action
                                text caption style "nvl_menu_choice"
                        else:
                            text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use status_bar
    use quick_menu
    use sc_avatar

##############################################################################
# Main Menu
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # This ensures that any other menu screen is replaced.
    tag menu

    # The background of the main menu.
    window:
        style "mm_root"

    # The main menu buttons.
    frame:
        style_group "mm"
        xalign .966
        yalign .89
        xmaximum 200

        # has vbox
        if not renpy.can_load("1-1"):
            textbutton _("Начать сюжет") action Start():
                xalign .966
                yalign .465
        else:
            textbutton _("Продолжить сюжет") action FileLoad("1", confirm=False, page="1"):
                xalign .966
                yalign .465
        if not renpy.can_load("1-3"):
            textbutton _("Свободная игра") action SetVariable("freeplay", True), Start():
                xalign .966
                yalign .580
        else:
            textbutton _("Продолжить свободную")action FileLoad("3", confirm=False, page="1"):
                xalign .966
                yalign .580
        textbutton _("Настройки") action ShowMenu("preferences"):
            xalign .966
            yalign .695
        textbutton _("Помощь") action Help():
            xalign .966
            yalign .81
        textbutton _("Выход") action Quit(confirm=False):
            xalign .966
            yalign .925

    # text "{font=fonts/Lombardina.ttf}Крылья":
        # xalign 0.94
        # yalign 0.11
        # text_align 1
        # size 90
        # bold False
        # color "#607080"
    # text "{font=fonts/Lombardina.ttf}Осквернителя":
        # xalign 0.95
        # yalign 0.22
        # text_align 1
        # size 60
        # bold False
        # color "#607080"
    text "{font=fonts/PFMonumentaPro-Regular.ttf}Версия: %s" % config.version:
        xalign 0.96
        yalign 0.29
        text_align 0.5
        size 14
        bold False
        color "#241511"

init -2 python:
    style.mm_button.size_group = "mm"

init python:
    style.mm_button.background = Frame("img/menu/button/idle.png", 10, 10)
    style.mm_button.hover_background = Frame("img/menu/button/hover.png", 10, 10)
    style.mm_button.selected_background = Frame("img/menu/button/selected.png", 10, 10)
    style.mm_button.selected_hover_background = Frame("img/menu/button/selected.png", 10, 10)
    style.mm_frame.background = Frame("img/menu/frame.png", 125, 25)

    style.mm_button_text.size = 22
    style.mm_button_text.font = "fonts/PFMonumentaPro-Regular.ttf"

    style.mm_button.yminimum = 70
    style.mm_button.xminimum = 280

##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # The background of the game menu.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Обратно") action Return()
        textbutton _("Настройки") action ShowMenu("preferences")
        # textbutton _("Сохранить игру") action ShowMenu("save")
        # textbutton _("Загрузить игру") action ShowMenu("load")
        textbutton _("Главное меню") action MainMenu()
        textbutton _("Помощь") action Help()
        textbutton _("Выход") action Quit()

init -2:

    # Make all game menu navigation buttons the same size.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        $ columns = 2
        $ rows = 2

        # Display a grid of file slots.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Display ten file slots, numbered 1 - 10.
            for i in range(1, columns * rows + 1):

                # Each file slot is a button.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Add the screenshot.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

screen load:

    # This ensures that any other menu screen is replaced.
    tag menu

    use navigation
    use file_picker

init -2:
    style file_picker_frame is menu_frame
    style file_picker_nav_button is small_button
    style file_picker_nav_button_text is small_button_text
    style file_picker_button is large_button
    style file_picker_text is large_button_text


##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # Include the navigation.
    use navigation

    # Put the navigation columns in a three-wide grid.
    grid 3 1:
        style_group "prefs"
        xfill True

        # The left column.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Экран")
                textbutton _("В окне") action Preference("display", "window")
                textbutton _("Полныйэкран") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Переход")
                textbutton _("Все") action Preference("transitions", "all")
                textbutton _("Ничего") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Скорость текста")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Джостик...") action Preference("joystick")
            
            frame:
                style_group "pref"
                has vbox

                textbutton _("Сброс сюжетной игры") action Game_Reset()

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Пропуск")
                textbutton _("Увиденные сцены") action Preference("skip", "seen")
                textbutton _("Все сцены") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Начать пропуск") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("После выбора")
                textbutton _("Закончить пропуск") action Preference("after choices", "stop")
                textbutton _("Продолжить пропуск") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Громкость музыки")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Громкость звука")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Тест звука"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Громкость голоса")
                    bar value Preference("voice volume")

                    textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Тест"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2:
    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0

    # style pref_root:
    #    background img/menu/gmenu.png
    
    python:
        class Game_Reset(object):
            def __call__(self):
                renpy.unlink_save("1-1")

##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100
            if message == layout.QUIT and not main_menu and not save_blocked:
                if not freeplay:
                    textbutton _("Да") action FileSave("1", confirm=False, page="1"), yes_action
                else:
                    textbutton _("Да") action FileSave("3", confirm=False, page="1"), yes_action
            elif message == layout.MAIN_MENU and not save_blocked:
                if not freeplay:
                    textbutton _("Да") action FileSave("1", confirm=False, page="1"), yes_action
                else:
                    textbutton _("Да") action FileSave("3", confirm=False, page="1"), yes_action
            else:
                textbutton _("Да") action yes_action
            textbutton _("Нет") action no_action

    # Right-click and escape answer "no".
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu:

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Назад") action Rollback()
        # textbutton _("Сохранить") action ShowMenu('save')
        # textbutton _("Б.сохранение") action QuickSave()
        textbutton _("Б.загрузка") action QuickLoad()
        textbutton _("пропуск") action Skip()
        textbutton _("Б.пропуск") action Skip(fast=True, confirm=True)
        textbutton _("Авто") action Preference("auto-forward", "toggle")
        textbutton _("Настройки") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"

##############################################################################
# Menu for girls in prison
init python:
        girls_rows = 3
        girls_cols = 4
        girls_cells = girls_rows * girls_cols
        girl_page = 0
        girl_position_priority = (
            6, 7, 8, 9,
            5, 0, 1, 10,
            4, 3, 2, 11
        )
screen girls_menu:

    # This ensures that any other menu screen is replaced.
    tag menu

    frame background "img/scene/prison.png":
        if girl_page * girls_cells > game.girls_list.prisoners_count:
            $ girl_page = 0
        $ next_girl_page = girl_page + 1
        $ prev_girl_page = girl_page - 1
        $ position_i = -1

        for row_i in xrange(girls_rows):
            grid girls_cols 1:
                spacing 50
                ypos row_i * 230
                xsize 200
                for col_i in xrange(girls_cols):
                    $ position_i += 1
                    $ girl_i = girl_page * girls_cells + girl_position_priority[position_i]
                    if girl_i < game.girls_list.prisoners_count:
                        imagebutton idle Image(im.Grayscale(game.girls_list.prisoners[girl_i].avatar)) hover game.girls_list.prisoners[girl_i].avatar action[Function(game.girls_list.set_active, girl_i), Jump('lb_nature_sex')]
                    else:
                        null

        hbox:
            ypos 680
            xpos 60
            spacing 50
            if girl_page > 0:
                textbutton _("Предыдущая страница") action[SetVariable('girl_page', prev_girl_page), Show("girls_menu")]
            else:
                textbutton _("Предыдущая страница") action None
            textbutton _("Вернуться") action Return()
            if next_girl_page * girls_cells < game.girls_list.prisoners_count:
                textbutton _("Следующая страница") action[SetVariable('girl_page', next_girl_page), Show("girls_menu")]
            else:
                textbutton _("Следующая страница") action None