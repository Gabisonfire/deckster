import json

class Key:
    def __init__(self, name, key, page, icon_default, icon_pressed, font, label, plugin, args, button_type):
        self.name = name
        self.key = key
        self.page = page
        self.icon_default = icon_default
        self.icon_pressed = icon_pressed
        self.font = font
        self.label = label
        self.plugin = plugin
        self.args = args
        self.button_type = button_type
        self.toggle_state = False

    def to_json(self):
        return json.dumps(self.__dict__)
