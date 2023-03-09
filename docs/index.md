## **Deckster**
A service to manage your Streamdeck easily on Linux

---
### **Features**
- Push or Toggle buttons
- Supports pages
- Timer actions
- Support JSON and YAML key configs
- Builtin functions:
  - GET Request
    - Send result to label or image
  - POST Request
  - Play audio file
  - Execute a shell command
  - Lock streamdeck
  - Homeassistant API
- Customizable labels
- Use icons and/or text
- Builtin key generators for:
  - Steam

### **Quickstart**
- `pip install deckster-sd`
- Confirm the directories configuration in `~/config.json`
- Edit your keys in the defined `keys_dir`
- Run `deckster`

### **Documentation**
- [Installation](install.md)
- [Configuration](config.md)
- [Builtin Plugins](plugins.md)
- [Custom Plugins](custom_plugins.md)
- [Modules](modules.md)
- [Builtin Generators](generators.md)
- [Custom Generators](custom_generators.md)
- [API Reference](api/common/index.md)
- [Changelog](changelog.md)

Built with [Dean Camera](https://github.com/abcminiuser/)'s awesome [Streamdeck](https://pypi.org/project/streamdeck/) library.

