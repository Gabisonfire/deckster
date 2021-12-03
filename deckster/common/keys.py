import json
import importlib
import importlib.util
import logging
import os
from common import scheduler


logger = logging.getLogger("deckster")


valid_buttons = [
    "push",
    "toggle",
    "timer_on",
    "timer_toggle"
]

class Key:
    def __init__(self, json_key):
        # Required
        self.key = json_key["key"]
        logger.debug(f"Instantiating key {self.key}: {json_key}")
        self.page = json_key["page"]
        self.icon_default = json_key["icon_default"]
        self.plugin = json_key["plugin"]

        if json_key["button_type"] in valid_buttons:
            self.button_type = json_key["button_type"]
        else:
            raise Exception(f"Invalid button type: '{json_key['button_type']}'")
        
        if self.button_type.startswith("timer"):
            if not "interval" in json_key:
                raise Exception(f"'interval' value is required for button type '{self.button_type}'")
            else:
                self.interval = json_key["interval"]

        # Optional
        if "font_size" in json_key:
            self.font_size = json_key["font_size"]
        else:
            self.font_size = 14

        if "icon_pressed" in json_key:
            self.icon_pressed = json_key["icon_pressed"]
        else:
            self.icon_pressed = self.icon_default

        if "label" in json_key:
            self.label = json_key["label"]

        if "font" in json_key:
            self.font = json_key["font"]
        else:
            self.font = "Roboto-Regular.ttf"

        if "args" in json_key:
            self.args = json_key["args"]

        if "toggle_state" in json_key:
            self.toggle_state = json_key["toggle_state"]
        else:
            self.toggle_state = False

        if "label_color" in json_key:
            self.label_color = json_key["label_color"]
        else:
            self.label_color = "white"
        
        if "label_offset" in json_key:
            self.label_offset = json_key["label_offset"]
        else:
            self.label_offset = 5

        if "label_ext" in json_key:
            self.label_ext = json_key["label_ext"]



    def to_json(self):
        return json.dumps(self.__dict__)
    
    def schedule_timer(self, deck, plugin_dir):
        if not self.button_type.startswith("timer"):
            return
        logger.debug(f"Scheduling timer on key: {self.key}.")
        paused = False
        if self.button_type == "timer_toggle":
            paused = True
        if self.plugin.startswith("builtins."):
            logger.debug(f"Importing builtin plugin 'plugins.{self.plugin}'")
            plugin = importlib.import_module(f"plugins.{self.plugin}", None)
        else:           
           spec = importlib.util.spec_from_file_location(self.plugin.split(".")[-1], os.path.join(plugin_dir, self.plugin.replace(".", "/") + ".py"))
           plugin = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(plugin)
        scheduler.add_job(lambda: plugin.main(deck, self, False), self.interval, id=f"{self.key}{self.page}", paused = paused)
        logger.info(f"Scheduling job({self.key}{self.page}), is paused: {paused}")

    def toggle(self):
        self.toggle_state = not self.toggle_state
        return self.toggle_state