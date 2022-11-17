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