import base64
import json

import pyglet

import gen
import sceneManager

pyglet.font.add_file("comic.ttf")
is_game_over = False
is_game_win = False
minefield = gen.gen_matrix(10, 0)
is_generated = False
field_object_matrix = gen.gen_matrix(10, 0)
win = pyglet.window.Window(width=600, height=600)
frame = pyglet.gui.Frame(win)
sm = sceneManager.Manager(win, frame)
background = pyglet.image.load("sprites/Menu/menu_background.png")
one = pyglet.image.load("sprites/Game/one.png")
two = pyglet.image.load("sprites/Game/two.png")
three = pyglet.image.load("sprites/Game/three.png")
four = pyglet.image.load("sprites/Game/four.png")
five = pyglet.image.load("sprites/Game/five.png")
six = pyglet.image.load("sprites/Game/six.png")
seven = pyglet.image.load("sprites/Game/seven.png")
eight = pyglet.image.load("sprites/Game/eight.png")
mine = pyglet.image.load("sprites/Game/mine.png")
closed_cell = pyglet.image.load("sprites/Game/closed_cell.png")
flag = pyglet.image.load("sprites/Game/flag.png")
game_over_text = pyglet.text.Label("Ты проиграл!", "Comic Sans Ms", 14, x=300, y=300, anchor_x="center",
                                   anchor_y="center", color=(0, 0, 0, 255))
game_win_text = pyglet.text.Label("Ты выйграл!", "Comic Sans Ms", 14, x=300, y=300, anchor_x="center",
                                  anchor_y="center", color=(0, 0, 0, 255))
mines_left = 15
mines_left_text = pyglet.text.Label("Осталось мин: 15", "Comic Sans Ms", 14, x=300, y=575, anchor_x="center",
                                    anchor_y="center", color=(0, 0, 0, 255))
wins_text = pyglet.text.Label("Выйгрышей:", "Comic Sans Ms", 14, x=50, y=475, anchor_y="center", color=(0, 0, 0, 255))
losing_text = pyglet.text.Label("Проигрышей:", "Comic Sans Ms", 14, x=50, y=375, anchor_y="center",
                                color=(0, 0, 0, 255))


def main():
    global wins_text, losing_text
    main_menu_batch = pyglet.graphics.Batch()
    start_button = pyglet.gui.PushButton(x=250, y=250,
                                         pressed=pyglet.image.load("sprites/Menu/start_button_pressed.png"),
                                         depressed=pyglet.image.load("sprites/Menu/start_button_unpressed.png"),
                                         batch=main_menu_batch)
    stats_button = pyglet.gui.PushButton(x=250, y=190,
                                         pressed=pyglet.image.load("sprites/Menu/stats_button_pressed.png"),
                                         depressed=pyglet.image.load("sprites/Menu/stats_button_unpressed.png"),
                                         batch=main_menu_batch)
    exit_button = pyglet.gui.PushButton(x=250, y=50, pressed=pyglet.image.load("sprites/Menu/exit_button_pressed.png"),
                                        depressed=pyglet.image.load("sprites/Menu/exit_button_unpressed.png"),
                                        batch=main_menu_batch)
    exit_button.set_handler("on_release", win.close)

    def stats_scene():
        global wins_text, losing_text
        with open("save.stats", "r") as f:
            decoded_stats = json.loads(base64.b64decode(f.read().encode("ascii")).decode("ascii"))
        wins_text.text = f"Выйгрышей: {decoded_stats['wins']}"
        losing_text.text = f"Проигрышей: {decoded_stats['losing']}"
        sm.load_scene("StatsMenu")

    stats_button.set_handler("on_release", stats_scene)

    def game_scene():
        sm.load_scene("GameMenu")

    start_button.set_handler("on_release", game_scene)
    sm.add_scene(
        "MainMenu",
        (
            [
                "Image",
                background,
                (0, 0)
            ],
            [
                "PushButton",
                start_button
            ],
            [
                "PushButton",
                stats_button
            ],
            [
                "PushButton",
                exit_button
            ],
        ), main_menu_batch
    )
    stats_menu_batch = pyglet.graphics.Batch()
    wins_text.batch = stats_menu_batch
    losing_text.batch = stats_menu_batch
    back_button = pyglet.gui.PushButton(x=5, y=555, pressed=pyglet.image.load("sprites/Menu/back_button_pressed.png"),
                                        depressed=pyglet.image.load("sprites/Menu/back_button_unpressed.png"),
                                        batch=stats_menu_batch)

    def main_menu_scene():
        sm.load_scene("MainMenu")

    back_button.set_handler("on_release", main_menu_scene)
    sm.add_scene(
        "StatsMenu",
        (
            [
                "Image",
                background,
                (0, 0)
            ],
            [
                "Image",
                pyglet.image.load("sprites/Menu/dark_panel.png"),
                (0, 550)
            ],
            [
                "PushButton",
                back_button
            ],
        ), stats_menu_batch
    )
    game_menu_batch = pyglet.graphics.Batch()
    back_button = pyglet.gui.PushButton(x=5, y=555, pressed=pyglet.image.load("sprites/Menu/back_button_pressed.png"),
                                        depressed=pyglet.image.load("sprites/Menu/back_button_unpressed.png"),
                                        batch=game_menu_batch)

    back_button.set_handler("on_release", main_menu_scene)

    def minesweeper_start():
        global field_object_matrix, is_generated, is_game_over, is_game_win, mines_left
        is_generated = False
        is_game_over = False
        is_game_win = False
        mines_left = 15
        mines_left_text.text = f"Мин осталось: {mines_left}"
        field_object_matrix = gen.gen_matrix(10, False)
        return None

    def minesweeper_update():
        for i in range(10):
            for j in range(10):
                if field_object_matrix[i][j] == 1:
                    match minefield[i][j]:
                        case 1:
                            one.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 2:
                            two.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 3:
                            three.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 4:
                            four.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 5:
                            five.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 6:
                            six.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 7:
                            seven.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 8:
                            eight.blit(50 + i * 50, 525 - (j + 1) * 50)
                        case 9:
                            mine.blit(50 + i * 50, 525 - (j + 1) * 50)
                elif field_object_matrix[i][j] == 0:
                    closed_cell.blit(50 + i * 50, 525 - (j + 1) * 50)
                else:
                    flag.blit(50 + i * 50, 525 - (j + 1) * 50)
        if is_game_over:
            game_over_text.draw()
        if is_game_win:
            game_win_text.draw()
        mines_left_text.draw()

    def minesweeper_mouse_release(*args):
        global minefield, field_object_matrix, is_generated, mines_left
        if is_game_over or is_game_win:
            return
        if 550 > args[0] > 50 and 525 > args[1] > 25:
            i, j = (args[0] - 50) // 50, 9 - (args[1] - 25) // 50
            if not is_generated:
                minefield = gen.gen_field(10, 15, i, j)
                is_generated = True
                args = list(args)
                args[2] = pyglet.window.mouse.LEFT
                args = tuple(args)
            match args[2]:
                case pyglet.window.mouse.LEFT:
                    if field_object_matrix[i][j] == 0:
                        if minefield[i][j] == 9:
                            game_over()
                        field_object_matrix[i][j] = 1
                    count = 0
                    used = gen.gen_matrix(10, False)
                    queue = []
                    used[i][j] = True
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if 10 > i + x >= 0 and 10 > j + y >= 0 and field_object_matrix[i + x][j + y] == 2:
                                count += 1
                    if count == minefield[i][j]:
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if 10 > i + x >= 0 and 10 > j + y >= 0 and field_object_matrix[i + x][j + y] == 0:
                                    field_object_matrix[i + x][j + y] = 1
                                    if minefield[i + x][j + y] == 9:
                                        game_over()
                                    elif minefield[i + x][j + y] == 0:
                                        queue.append((i + x, j + y))
                                        used[i + x][j + y] = True
                    while len(queue) > 0:
                        for x in range(-1, 2):
                            for y in range(-1, 2):
                                if 10 > queue[0][0] + x >= 0 and 10 > queue[0][1] + y >= 0:
                                    if field_object_matrix[queue[0][0] + x][queue[0][1] + y] == 0:
                                        field_object_matrix[queue[0][0] + x][queue[0][1] + y] = 1
                                        if minefield[queue[0][0] + x][queue[0][1] + y] == 0:
                                            if not used[queue[0][0] + x][queue[0][1] + y]:
                                                queue.append((queue[0][0] + x, queue[0][1] + y))
                                                used[queue[0][0] + x][queue[0][1] + y] = True
                        queue.pop(0)
                    count = 0
                    for i in field_object_matrix:
                        for j in i:
                            if j == 1:
                                count += 1
                    if count == 10 * 10 - 15:
                        game_win()
                case pyglet.window.mouse.RIGHT:
                    if field_object_matrix[i][j] != 1:
                        field_object_matrix[i][j] = 2 - field_object_matrix[i][j]
                        if field_object_matrix[i][j]:
                            mines_left -= 1
                        else:
                            mines_left += 1
                        mines_left_text.text = f"Мин осталось: {mines_left}"

    def game_over():
        global is_game_over
        is_game_over = True
        with open("save.stats", "r") as f:
            decoded_stats = json.loads(base64.b64decode(f.read().encode("ascii")).decode("ascii"))
            decoded_stats["losing"] += 1
        with open("save.stats", "w") as f:
            f.write(base64.b64encode(json.dumps(decoded_stats).encode("ascii")).decode("ascii"))

    def game_win():
        global is_game_win
        is_game_win = True
        with open("save.stats", "r") as f:
            decoded_stats = json.loads(base64.b64decode(f.read().encode("ascii")).decode("ascii"))
            decoded_stats["wins"] += 1
        with open("save.stats", "w") as f:
            f.write(base64.b64encode(json.dumps(decoded_stats).encode("ascii")).decode("ascii"))

    sm.add_scene(
        "GameMenu",
        (
            [
                "Image",
                background,
                (0, 0)
            ],
            [
                "Image",
                pyglet.image.load("sprites/Menu/dark_panel.png"),
                (0, 550, 1)
            ],
            [
                "PushButton",
                back_button
            ],
            [
                "Image",
                pyglet.image.load("sprites/Game/game_field.png"),
                (50, 25)
            ],
            [
                "Script",
                minesweeper_start,
                (),
                minesweeper_update,
                (),
                None
            ],
            [
                "Event",
                "on_mouse_release",
                minesweeper_mouse_release
            ]
        ), game_menu_batch
    )
    sm.load_scene("MainMenu")
    pyglet.app.run()


if __name__ == '__main__':
    main()
