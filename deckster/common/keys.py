import json
import common.scheduler
import importlib
import importlib.util
import os

valid_buttons = [
    "push",
    "toggle",
    "timer_on",
    "timer_toggle"
]

class Key:
    def __init__(self, json_key):
        # Mandatory
        self.key = json_key["key"]
        self.page = json_key["page"]
        self.icon_default = json_key["icon_default"]
        if json_key["button_type"] in valid_buttons:
            self.button_type = json_key["button_type"]
        else:
            raise Exception(f"Invalid button type: '{json_key['button_type']}'")
        self.plugin = json_key["plugin"]
        
        # Optional
        if "icon_pressed" in json_key:
            self.icon_pressed = json_key["icon_pressed"]
        else:
            self.icon_pressed = self.icon_default
        if "label" in json_key:
            self.label = json_key["label"]
        if "font" in json_key:
            self.font = json_key["font"]
        if "args" in json_key:
            self.args = json_key["args"]
        if "toggle_state" in json_key:
            self.toggle_state = json_key["toggle_state"]
        else:
            self.toggle_state = False
        if self.button_type.startswith("timer"):
            if not "interval" in json_key:
                raise Exception(f"'interval' value is required for button type '{self.button_type}'")
            else:
                self.interval = json_key["interval"]

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def schedule_timer(self, deck):        
        if not self.button_type.startswith("timer"):
            return
        paused = False
        if self.button_type == "timer_toggle":
            paused = True
        if self.plugin.startswith("builtins."):
            plugin = importlib.import_module("plugins." + self.plugin, None)
        else:           
           spec = importlib.util.spec_from_file_location(self.plugin.split(".")[-1], os.path.join(common.configs.read_config("plugins_dir"), self.plugin.replace(".", "/") + ".py"))
           plugin = importlib.util.module_from_spec(spec)
           spec.loader.exec_module(plugin)
        state = {
            "deck": deck, 
            "key": self.to_json(),
            "pressed": True
        }
        common.scheduler.add_job(lambda: plugin.main(state), self.interval, id=f"{self.key}{self.page}", paused = paused)
        print(f"Scheduling job({self.key}{self.page}), is paused: {paused}")

    def write_state(self):
        print(f"Writing state for {self.key}:{self.toggle_state}")
        common.configs.write_key_config(self.key , self.page, "toggle_state", self.toggle_state)

    def toggle(self):
        self.toggle_state = not self.toggle_state
        self.write_state()
        return self.toggle_state

