# Builtins - Generators

Unlike plugins, generators are configured in the `config.json` file. They work a lot like plugins, but are executed before the key configuration is read.
All generators require the `enabled` attribute.
Ex:
```json
{
    "generator": "builtins.name",
    "enabled": true,
    [...]
}
```

## steam
Reads installed games and applications, retreive their title and icons and tiles them.

- reference: `builtins.steam`
- requires: (`pip install`)
  - beautifulsoup4
  - vdf
- args:
    - page (int): The page to add the keys to. Required.
    - allow_more_pages (bool): Will keep adding pages starting from `page` as needed. Default: false
    - steam_lib (string): The path to your `libraryfolders.vdf`, usually in `~/.steam/steam/steamapps/`
    - start (int): At what key to start. Remember the key count starts at 0. Default: 0
    - limit (int): Limit of key to use. The generator will use either this or you deck's max keys. Default: 100
    - filters (string/int)[]: Games or apps to filter out, either by title or id. Exact match only at the moment.
    - download_icons (bool): Download or not the icons.
    - overwrite (bool): Will overwrite the file on launch, essentially refreshing the games. Default: false
    - hide_label (bool): Setting to true will show icons only. Default: False
    - font (string): Changes the labels font. Default: Roboto-Regular.ttf
    - add_navigation (bool): Will add page navigation buttons at the provided positions. Default: false
    - previous_key (int): Where to put the `previous` button.
    - previous_icon (string): The icon to use for the `previous` button, relative to `icons_dir`.
    - next_key (int): Where to put the `next` button.
    - next_icon (string): The icon to use for the `next` button, relative to `icons_dir`.
    - sort_titles (bool): Sort titles alphabetically. Default: false
    - padding ([int,int,int,int]): Add padding around the icons. Left, Right, Bottom, Top. Default: [0,0,0,0]
    - label_truncate (int): Will truncate the labels after this amount of characters. Default: No truncating (-1)


Example:
```json
{
    "generator": "builtins.steam",
    "enabled": true,
    "args": {
      "steam_lib": "~/.steam/steam/steamapps/libraryfolders.vdf",
      "start": 0,
      "limit": 15,
      "filters": [
        "Aseprite",
        "Simply Chess"
      ],
      "label_truncate": 100,
      "download_icons": true,
      "overwrite": true,
      "page": 2,
      "hide_label": false,
      "font": "Roboto-Regular.ttf",
      "add_navigation": true,
      "previous_key": 10,
      "previous_icon": "previous.png",
      "next_key": 14,
      "next_icon": "next.png",
      "sort_titles": true,
      "label_truncate": 6,
      "padding": [
        0,
        0,
        0,
        0
      ]
}
```
## Notes:
- Keys generated are stored in the `keys_dir` folder in a file named `steam_generator.json`.
- Icons are saved in the `icons_dir` folder with the game/app's `appid`.
- Bottom padding is automatically set to 20 when a label is visible.
---