import json
import importlib
import importlib.util
import logging
import os
from deckster.common import scheduler


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
        if not json_key["plugin"] == "empty":
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
        if "label_truncate" in json_key:
            self.label_truncate = json_key["label_truncate"]
        else:
            self.label_truncate = -1

        if "padding" in json_key:
            self.padding = json_key["padding"]
        else:
            self.padding = [0,0,0,0]
        
        if "font_size" in json_key:
            self.font_size = json_key["font_size"]
        else:
            self.font_size = 14

        if "font" in json_key:
            self.font = json_key["font"]
        else:
            self.font = "Roboto-Regular.ttf"

        if "icon_pressed" in json_key:
            self.icon_pressed = json_key["icon_pressed"]
        else:
            self.icon_pressed = self.icon_default

        if "label" in json_key:
            self.label = json_key["label"]

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

        if "display" in json_key:
            self.display = json_key["display"]
        else:
            self.display = "NULL"
        
        if "display_offset" in json_key:
            self.display_offset = json_key["display_offset"]
        else:
            self.display_offset = 15

        if "display_color" in json_key:
            self.display_color = json_key["display_color"]
        else:
            self.display_color = "white"

        if "display_size" in json_key:
            self.display_size = json_key["display_size"]
        else:
            self.display_size = 14

        if "display_font" in json_key:
            self.display_font = json_key["display_font"]
        else:
            self.display_font = "Roboto-Regular.ttf"

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
            plugin = importlib.import_module(f"deckster.plugins.{self.plugin}", None)
        else:           
           spec = importlib.util.spec_from_file_location(self.plugin.split(".")[-1], os.path.join(plugin_dir, self.plugin.replace(".", "/") + ".py"))
           plugin = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(plugin)
        scheduler.add_job(lambda: plugin.main(deck, self, False), self.interval, id=f"{self.key}{self.page}", paused = paused)
        logger.info(f"Scheduling job({self.key}{self.page}), is paused: {paused}")

    def toggle(self):
        self.toggle_state = not self.toggle_state
        return self.toggle_state