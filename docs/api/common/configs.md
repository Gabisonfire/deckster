Module common.configs
=====================

Functions
---------

    
`empty_set(key_count, page)`
:   Creates empty keys
    
    Args:
        key_count (integer): Number of keys to generate
        page (integer): The page to assign to generated keys
    
    Returns:
        list: A list of empty keys

    
`find_key(key, page, key_list)`
:   Find specific key on a page
    
    Args:
        key (integer): The key number
        page (integer): The page to search the key
        key_list (list): A list of keys
    
    Returns:
        Key: A found key

    
`max_page(key_list)`
:   Find the last page
    
    Args:
        key_list (list): List of keys
    
    Returns:
        integer: Page number

    
`read_config(cfg, custom_config=None)`
:   Read the configuration file
    
    Args:
        cfg (string): the config to read (key)
        custom_config (string, optional): Sepcify an alternate path. Defaults to None.
    
    Returns:
        string: value

    
`read_keys()`
:   Read all keys
    
    Returns:
        list: A list containing all keys

    
`write_config(cfg, value, custom_config=None)`
:   Write value for a config
    
    Args:
        cfg (string): config to update
        value (string): value to write
        custom_config (string, optional): Provide an alternate path. Defaults to None.

    
`write_key_config(key, page, cfg, value)`
:   Write value for a given config for a given key.
    
    Args:
        key (Key): A key
        page (integer): Page number
        cfg (string): config to write
        value (string): value to write