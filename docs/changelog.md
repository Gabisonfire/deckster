# 0.6 * Breaking changes *
- Moved a lot of code to deckster.common.core for easier debug and organization.
  - Plugins requiring methods like `update_key_image` or `update_label_display` need to update their imports from `deckster.deckster` to `deckster.common.core`.
- Updated pillow to 9.2.0 due to vulnerabilities.
- Added the [Homeassistant plugin](https://deckster-sd.readthedocs.io/en/latest/plugins/)
- Added the [lock plugin](https://deckster-sd.readthedocs.io/en/latest/plugins/)
- Added [key templates](https://deckster-sd.readthedocs.io/en/latest/config/)
- Added ability for plugins to manage the state of a toggle type button. See [Homeassistant plugin](https://deckster-sd.readthedocs.io/en/latest/plugins/) for examples.
- Added [modules](https://deckster-sd.readthedocs.io/en/latest/modules/) functionality
- Added `run_once` functionality for plugins.

# 0.5
- Fix for bad json formatting  (https://github.com/Gabisonfire/deckster/issues/4)
- Updated pillow for security purposes
- Fix custom plugins not loading on `timer_on`

# 0.4
- Updated pillow for security purposes
- Added jq filters for GET requests

# 0.3
- Updated service file for proper user install.
- Proper SIGTERM handling
- Steam generator: Automatically add pages as needed.

# 0.2
- Added generators
  - Added Steam as builtin generator
- Various code optimization
- Added `padding` option
- Added `label_truncate` option to use mostly with generators
- Retry if no deck is found initially

# 0.1
- Initial release