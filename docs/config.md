## Key Configuration

Keys are configured by referencing their numbers starting from 0, left to right. Keys are loaded from the `keys_dir` directory ([see install](install.md)) and can be in either JSON or YAML format. Examples can be found in the repository under `keys.d`.


| Configuration | Description | Required | Values | Default |
| :------------ | :---------: | :------: | :----: | :-----:
| key | The key the config applies to | x | int from 0 to your max key ||
| page | The page this key needs to be displayed on | x | int >= 1 ||
| template | The template file name without extension. See [Special Configurations](#special-configurations) | | string ||
| icon_default | The icon file to display when in "default" or "released" state. | x | Your icon filename relative to the `icons_dir` in your config. ||
| icon_pressed | The icon file to display when in "pressed" | | Your icon filename relative to the `icons_dir` in your config. | `icon_default` |
| plugin | The plugin to apply to this key. | x | See [builtins](builtins.md) or a [custom plugin](plugins.md) ||
| args | The arguments to be sent to the plugin, if applicable. | | See individual plugins | |
| button_type | The type of button this key is. | x | `push`, `toggle`, `timer_on`, `timer_toggle` ||
| interval | The interval in seconds for a `timer` type button. | If button_type is set to `timer_*` | int ||
| font_size | The size of the font for key labels | | int | 14 |
| font | The font to use for labels | | An installed font | Roboto-Regular.ttf |
| label | The text displayed in the label | | string | |
| label_color | The color of the text displayed by the label | | Common HTML color names. | white |
| label_offset | The offset of the label relative to the bottom. | | int | 5 |
| label_truncate | The maximum of characters a label will display. | | int | None (-1) |
| display | Text to display. Requires icons to be set to `@display`. See [Special Configurations](#special-configurations) | | string | |
| display_offset | The offset of the text relative to the top. | | int | 15 |
| display_color | The color of the text displayed by the `display` | | Common HTML color names. | white |
| display_size | The size of the font for key displays | | int | 14 |
| display_font |  The font to use for displays | | An installed font | Roboto-Regular.ttf |
| padding | The padding applied to the icon. Left, right, bottom, top | | [int,int,int,int] | [0,0,0,0] |
| toggle_state | The state stored for `toggle` type buttons. | | true, false | Written by Deckster |
| modules | A list of modules to load. | | ["module_name"] | Refer to [modules](https://deckster-sd.readthedocs.io/en/latest/modules/) |

---

## Special Configurations
- `icon_default`, `icon_pressed`
  - `@hide`: Will hide the icon entirely
  - `@display`: Will display text instead of an icon
- `button_type`
  - `push`: Push to activate
  - `toggle`: Push to activate, push again to deactivate
  - `timer_on`: Will start the timer when the deck starts
  - `timer_toggle`: Will start the timer when pressed, stop when pressed again.
- `label`
  - `@hide`: Will hide the label.
- `toggle_state`: This is used by Deckster to keep the state of `toggle` type buttons. It is kept inside the configuration to allow users to manually change it if needed.
- `padding`: When a label is shown, the bottom padding is automatically set to 20.
- `template`: A file name within the `keys_dir` with a `.tmpl` extension, containing a json object with attributes to apply to all keys referring to the template. This can considerably reduce the keys definitions. Each key will have the template's content merged.

Example:

style1.tmpl
```
  {
    "plugin": "builtins.web.post",
    "args": {
      "url": "http://someurl.example.com",
      "headers": {
        "Content-type": "application/json",
        "Authorization": "78sdfhd8safh7sdhfsdhf8shd78fasdfshdfh7"
      },
      "status_codes": [
        200
      ]
    },
    "label_offset": 25,
    "label_color": "green",
    "font": "NotoSansMono-Black.ttf",
    "font_size": 30,
    "button_type": "push",
    "interval": 5,
  },
```

keys.json
```
  {
    "page": 1,
    "key": 1,
    "template": "style1",
    "args": {
      "json_data": {
        "foo": "bar"
    },
    "icon_default": "light1.png",
    "icon_pressed": "light2.png",
  },
  {
    "page": 1,
    "key": 2,
    "template": "style1",
    "args": {
      "json_data": {
        "foo": "barbarbar"
    },
    "icon_default": "light3.png",
    "icon_pressed": "light4.png",
  },
```

**Please note that `page` and `key` cannot be in a template file as they are required for key identification.**