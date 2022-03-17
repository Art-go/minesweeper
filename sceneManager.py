import pyglet


class Manager:
    def __init__(self, win: pyglet.window.Window, frame: pyglet.gui.Frame):
        self.scenes = {}
        self.win = win
        self.active_scene = None
        self.frame = frame

        @win.event
        def on_draw():
            self.on_draw_func(self.win)

        @win.event
        def on_mouse_release(x, y, button, modifers):
            self.on_mouse_release(x, y, button, modifers)
            frame.on_mouse_release(x, y, button, modifers)

        self.on_draw_func = None
        self.on_mouse_release = self.pass_func

    @staticmethod
    def pass_func(*args):
        pass

    def add_scene(self, name: str, objects: tuple, batch: pyglet.graphics.Batch):
        self.scenes[name] = Scene(objects, batch)

    def load_scene(self, name: str):
        if self.active_scene is not None:
            for i in self.scenes[self.active_scene].temp_objects:
                if i[0] in ["PushButton", "ToggleButton", "Slider", "TextEntry"]:
                    self.frame.remove_widget(i[1])
                elif i[0] == "Event":
                    match i[1]:
                        case "on_mouse_release":
                            self.on_mouse_release = self.pass_func
        self.active_scene = name
        self.scenes[name].temp_obects = list(self.scenes[name].objects)
        for i in self.scenes[name].objects:
            if i[0] in ["PushButton", "ToggleButton", "Slider", "TextEntry"]:
                self.frame.add_widget(i[1])
            elif i[0] == "Script":
                _ = []
                for j in i[2]:
                    match j:
                        case "win":
                            _.append(self.win)
                        case "objects":
                            _.append(self.scenes[name].temp_obects)
                i[5] = (i[1](*_))
            elif i[0] == "Event":
                match i[1]:
                    case "on_mouse_release":
                        self.on_mouse_release = i[2]
        self.on_draw_func = self.scenes[name].func


class Scene:
    def __init__(self, objects: tuple, batch: pyglet.graphics.Batch):
        self.objects = objects
        self.batch = batch
        self.temp_objects = list(objects)

    def func(self, win: pyglet.window.Window):
        win.clear()
        for i in self.temp_objects:
            match i[0]:
                case "Image":
                    i[1].blit(*i[2])
                case "Script":
                    temp = []
                    for j in i[4]:
                        match j:
                            case "win":
                                temp.append(win)
                            case "objects":
                                temp.append(self.temp_obects)
                            case "return_from_start":
                                temp.append(i[5])
                    i[3](*temp)
                case _:
                    pass
        self.batch.draw()
