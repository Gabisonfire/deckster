Module common.keys
==================

Functions
---------

    
`fake_key(key_num, icon, page=1)`
:   Generates a fake key
    
    Args:
        key_num (integer): The index of the key
        icon (string): The icon to show
        page (int, optional): The page to assign the key. Defaults to 1.
    
    Returns:
        Key: A Key object

Classes
-------

`Key(json_key)`
:   Class that holds key information
    
    Args:
        json_key (string): Key in json format
    
    Raises:
        Exception: Invalid button type provided
        Exception: No interval provided

    ### Methods

    `schedule_timer(self, deck, plugin_dir)`
    :   Schedules a timer for a toggle type button
        
        Args:
            deck (deck): The deck
            plugin_dir (string): The directory to look for plugiin
        
        Raises:
            FileNotFoundError: Plugin not found

    `to_json(self)`
    :   Key in json format
        
        Returns:
            string: Json output for a key

    `toggle(self)`
    :   Toggles the state of a button
        
        Returns:
            bool: The new state of the key