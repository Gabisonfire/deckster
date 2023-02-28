# Modules
Modules are optional and that extend Deckster's features. They can be enabled from the config file. [See config](https://deckster-sd.readthedocs.io/en/latest/config/)

## api

- args:
  - `api_port`(int): The port the API should listen on. (default: 5000)
  - `api_token`(string): Token for authenticated endpoints. See `routes` below. You can disable authentication completely by setting this to "disabled"

Routes:
- `/deck/reload`: Authenticated. Reloads the deck and reinitiate keys from the key files.
- `/deck/lock`: Authenticated. Reloads the deck and reinitiate keys from the key files.
  - `mode`:
    - `blank`: Blanks the deck completely. Can only be unlocked via the `unlock` api.
    - `keyed`: Can be unlocked with a key combination.
      - `combination`(int array): An array of integer that represent the keys and order to input.
      - `icon_key`(int): The key that will display the icon
      - `icon`(string): The name (and extension) of the icon relative to the plugin directory specific in the config file.
- `/deck/unlock`: Authenticated. Reloads the deck and reinitiate keys from the key files.

Examples:
 ```
curl localhost:5000/deck/reload
{"message":"Deck reloaded","operation":"success"}
```
```
curl -XPOST -H "Content-Type: application/json" -d '{"mode":"keyed", "combination": [1,2,3,4], "icon_key":7, "icon": "lock.png"}' localhost:5000/deck/lock
{"message":"Deck locked","operation":"success"}
```
```
curl -XPOST -H "Content-Type: application/json" -d '{"mode":"blank"}' localhost:5000/deck/unlock
{"message":"Deck unlocked","operation":"success"}
```