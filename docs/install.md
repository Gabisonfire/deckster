# Installation

Deckster is installed with pip. Simply run:
```
pip install deckster-sd
```
The install process will create a default `config.json` to your /`home`/`.config`/`deckster` folder.

```json
{
  "icons_dir": "~/deckster/icons",
  "plugins_dir": "~/deckster/deckster-plugins",
  "current_page": 1,
  "keys_dir": "~/deckster/keys.d",
  "loglevel": "info",
  "brightness": 100
}
```

| Configuration | Description | Default | Values |
| :------------ | :---------: | :------ | :----: |
| icons_dir | The directory where the icons are located | ~/deckster/icons | A directory |
| plugins_dir | The directory where your custom plugins are installed | ~/deckster/deckster-plugins | A directory |
| current_page | The page to display. You should not have to manually change this | 1 | integer > 1 |
| keys_dir | The directory where your key configurations are stored | ~/deckster/keys.d | A directory |
| loglevel | The log level to output | info | debug, info, warning, error, critical  |
| brightness | The global brightness of your deck | 100 | integer between 1-100 |
| generators_dir | The directory where your custom generators | ~/deckster/generators | A directory |
| generators | Generator configurations array | [] | An array of configuration. See [generators](generators.md) |

<br/>

# Service
You can have deckster run as a service by using the service file in the repository. Run:
```bash
mkdir -p $HOME/.local/share/systemd/user
cp deckster.service $HOME/.local/share/systemd/user
systemctl --user daemon-reload
systemctl --user enable 
systemctl --user start deckster
```