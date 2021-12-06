# Builtins

## exit
----
Stops all jobs and puts the deck in "standby".

- reference: `builtins.exit`
- args: None

## play
---
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
  "font": "Roboto-Regular.ttf",
  "button_type": "push"
}
```
## shell
---
Executes a shell command

- reference: `builtins.shell`
- args:
  - `command`: An array of command and arguments to execute

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
# page
## next
---
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
    "button_type": "push",
  }
```

## previous
---
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
    "button_type": "push",
  }
```

# web
## get