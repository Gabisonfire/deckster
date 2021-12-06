# Deckster
### A service to manage your Streamdeck easily on Linux
---

## Quickstart
```
pip install deckster-sd
```
The install process will create a default `config.json` to your /`home`/`.config`/`deckster` folder. The just run `deckster`.

# Service
You can have deckster run as a service by using the service file template in the repository. Replace "myusername" with your linux user and then run:
```bash
sudo cp deckster.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start deckster
```