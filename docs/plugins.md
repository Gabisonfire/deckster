# Builtins - Plugins
---
## exit
Stops all jobs and puts the deck in "standby".

- reference: `builtins.exit`
- args: None
---
## play
Plays a sound file.

- reference: `builtins.play`
- args: 
  - `sound`: Full path to a sound file.

Example:
```json
{
  "key": 1,
  "page": 1,
  "plugin": "builtins.play",
  "args": {
      "sound": "/path/to/file.mp3"
  },
  "icon_default": "sound.png",
  "label": "Play",
  "button_type": "push"
}
```
---
## shell
Executes a shell command

- reference: `builtins.shell`
- args:
  - `command` (array of string): An array of command and arguments to execute

Example:
```json
  {
    "key": 4,
    "page": 1,
    "plugin": "builtins.shell",
    "args": {
      "command": [
        "ls",
        "-l"
      ]
    },
    "icon_default": "shell.png",
    "label": "shell",
    "button_type": "push"
  },
```
---
## page.next
Switches to the next page on the deck.

- reference: `builtins.page.next`
- args: None

Example:
```json
  {
    "key": 14,
    "page": 1,
    "plugin": "builtins.page.next",
    "icon_default": "next.png",
    "label": "next",
    "button_type": "push"
  }
```
---
## page.previous
Switches to the previous page on the deck.

- reference: `builtins.page.previous`
- args: None

Example:
```json
  {
    "key": 10,
    "page": 1,
    "plugin": "builtins.page.previous",
    "icon_default": "previous.png",
    "label": "previous",
    "button_type": "push"
  }
```
---
## web.get
Makes a GET request

- reference: `builtins.web.get`
- args:
  - `url`(string): The url
  - `status_codes`(array of int): Expected status codes to process the request
  - `json_parse` (string): A [jq expression](https://stedolan.github.io/jq/manual/#Basicfilters) to parse the returned json
  - `json_data`(json): optional, JSON body of the request
  - `headers` (json): optional, Headers to apply to the request
  - `send_to_label` (bool): optional, sends the result to the key's label.
  - `send_to_display` (bool): optional, sends the result to the key's display.

Example:
```json
  {
    "key": 3,
    "page": 1,
    "plugin": "builtins.web.get",
    "args": {
      "url": "http://worldtimeapi.org/api/timezone/America/Toronto",
      "status_codes": [
        200,
        201
      ],
      "json_parse": "day_of_week",
      "send_to_display": true
    },
    "icon_default": "@display",
    "icon_pressed": "@display",
    "label": "Day",
    "font_size": 14,
    "display_size": 24,
    "display_offset": 10,
    "button_type": "timer_on",
    "interval": 10
  },
```
---
## web.post
Makes a post request.

- reference: `builtins.web.post`
- args:
  - `url`(string): The url
  - `json_data`(json): JSON body of the request
  - `headers` (json): Headers to apply to the request
  - `status_codes`(array of int): Expected status codes to process the request

```json
  {
    "key": 0,
    "page": 1,
    "plugin": "builtins.web.post",
    "args": {
      "url": "https://home-assistant.com/api/services/light/toggle",
      "headers": {
        "Content-type": "application/json",
        "Authorization": "Bearer ABCDEFG12345"
      },
      "json_data": {
        "entity_id": "light.light_strip"
      },
      "status_codes": [
        200,
        201
      ]
    },
    "icon_default": "light.png",
    "label": "Light on",
    "label_color": "green",
    "button_type": "push_toggle"
  },
```
---
## homeassistant
Interacts with the Homeassistant API

- reference: `builtins.homeassistant`
- args:
  - `ha_base_url`(string): The base url to your homeassistant instance
  - `domain`(string): switch, scene, light, etc
  - `action`(string): toggle, turn_on, turn_off, etc.
  - `entity_id`(string): The entity id
  - `token`(string): Your HA api token
  - `track_state`(bool): Activates states tracking. Queries HA for a state. (Useful for entities accessible outside Deckster.)
  - `state_activated`(string): The HA state when the device is considered "on".
  - `state_deactivated`(string): The HA state when the device is considered "off".
  - `state_check_interval`(int): The interval in seconds for deckster to query the entitie's state.

```json
  {
    "key": 0,
    "page": 1,
    "plugin": "builtins.homeassistant",
    "args": {
      "ha_base_url": "https://home-assistant.com/api/services/light/toggle",
      "domain": "switch",
      "action": "toggle",
      "entity_id": "my_ha_light",
      "token": "asdkMTNkM2IwOTQ123MmE0NTI4321YmVkNTRjYzM1YzViasdYTJkZasd",
      "track_state": true,
      "state_activated": "on",
      "state_deactivated": "off",
      "state_check_interval": 5
    },
    "icon_default": "light.png",
    "label": "Light",
    "label_color": "green",
    "button_type": "push_toggle"
  },
```

## lock
Locks the deck until a passcode is entered.
When pressed, the selected icon will be moved to the designated `key_on_lock` and all buttons will be deactivated until the keys provided by `combination` are pressed in the given order. Dont forget that the first key on the deck is key "0".

Please note that the combination is easily readable, this is not meant to protect sensitive information/actions.

- reference: `builtins.lock`
- args:
  - `combination`(int array): The keys to press and order to unlock the deck
  - `key_on_lock`(int): On which key to display the icon when locked.

```json
  {
    "page": 1,
    "key": 0,
    "plugin": "builtins.lock",
    "args": {
      "combination": [
        0,
        4,
        10,
        14
      ],
      "key_on_lock": 7
    },
    "icon_default": "lock.png",
    "label": "@hide",
    "button_type": "push"
  },
```