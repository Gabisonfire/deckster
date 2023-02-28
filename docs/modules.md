# Modules
Modules are optional and that extend Deckster's features. They can be enabled from the config file. [See config](https://deckster-sd.readthedocs.io/en/latest/config/)

## api

- args:
  - `api_port`(int): The port the API should listen on. (default: 5000)

Routes:
 - `/deck/reload`: Reloads the deck and reinitiate keys from the key files.

 Examples:
 ```
curl localhost:5000/deck/reload                                                                                                    ()
"Deck reloaded"
```