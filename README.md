# Deckster
### A service to manage your Stream Deck easily on Linux
---

## Documentation

[Online Documentation](https://deckster-sd.readthedocs.io/en/latest/)

## Quickstart
```
pip install deckster-sd
```
The install process will create a default `config.json` to your /`~/`/`.config`/`deckster` folder. Then just run `deckster`.

Install dependencies and add permissions:
```bash
# Install system packages needed for the default LibUSB HIDAPI backend
sudo apt install -y libudev-dev libusb-1.0-0-dev libhidapi-libusb0

# Install system packages needed for the Python Pillow package installation
sudo apt install -y libjpeg-dev zlib1g-dev libopenjp2-7 libtiff5

# Add udev rule to allow all users non-root access to Elgato StreamDeck devices:
sudo tee /etc/udev/rules.d/10-streamdeck.rules << EOF
    SUBSYSTEMS=="usb", ATTRS{idVendor}=="0fd9", GROUP="users", TAG+="uaccess"
    EOF

# Reload udev rules to ensure the new permissions take effect
    sudo udevadm control --reload-rules
```

# Service
You can have deckster run as a service by using the service file template in the repository.
```bash
mkdir -p $HOME/.local/share/systemd/user
cp deckster.service $HOME/.local/share/systemd/user
systemctl --user daemon-reload
systemctl --user enable 
systemctl --user start deckster
```