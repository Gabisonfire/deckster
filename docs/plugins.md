# Custom plugins
Custom plugins are simply Python modules. Let's create a simple plugin that sends a random word to our label.

Under your `plugins_dir` specified in your `config.json`, create a folder to hold your plugin:
```bash
mkdir -p ~/deckster/deckster-plugins/gabisonfire
```

Plugins' entry points must be a function called `main` and must receive 3 arguments: `deck`, `key`, and `pressed`.

- `deck`: The current [deck object](https://python-elgato-streamdeck.readthedocs.io/en/stable/modules/devices.html#module-StreamDeck.Devices.StreamDeck) 
- `key`: The `key` that triggered the event. It holds all the information in your config.
- `pressed`: A boolean value. `true` if the button was pressed, `false` if it was released. At the moment, only `pressed` events will trigger a plugin execution.

Now let's create our plugin file:
```bash
touch ~/deckster/deckster-plugins/gabisonfire/random.py
```

```python
# This import is required to update the label/display of a key
from deckster.deckster import update_key_image, update_label_display
from random_word import RandomWords

# Required function definition
def main(deck, key, pressed):
    # Acquire the main logger
    logger = logging.getLogger("deckster")

    # Store the arguments
    args = key.args

    # Check for submitted arguments
    if "min" in args:
        min = args["min"]
    else:
        min = 1

    if "max" in args:
        max = args["max"]
    else:
        max = 10

    # Generate a random word using our arguments
    rw = RandomWords()
    aword = rw.get_random_word(min_length=min, max_length=max)

    # Print the word in the "info" logs
    logger.info(aword)

    # Check if the key configuration is set to send the result to a label or display
    if "send_to_display" in key.args or "send_to_label" in key.args:
            to_label = "send_to_label" in key.args

            # Update the display or label value
            if to_label:
                key.label = aword
            else:
                key.display = aword

            # This updates the label's value on disk
            update_label_display(key, True if "send_to_label" in key.args else False)

            # This recreates an image for the key with the new values.
            update_key_image(deck, key, pressed)
```

Now let's use that plugin in a key configuration:
```json
  {
    "key": 4,
    "page": 1,
    "plugin": "gabisonfire.random",
    "args": {
      "min": 5,
      "max": 10
    },
    "icon_default": "random.png",
    "label": "Random Word",
    "button_type": "push"
  },
```
That's it. When you press your "Random Word" button, the label will change into a random word.
You can also organise plugins in subfolder and add it to the reference. Ex:
```bash
touch ~/deckster/deckster-plugins/gabisonfire/words/random.py
```
```json
    "plugin": "gabisonfire.words.random",
```