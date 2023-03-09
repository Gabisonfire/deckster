Module common.core
==================

Functions
---------

    
`change_page(increment)`
:   Changes page.
    
    Args:
        increment (integer): For how many pages to move

    
`clear(deck, page=1)`
:   Clears the deck, filling it with empty keys.
    
    Args:
        deck (deck): The deck
        page (int, optional): Page to clear. Defaults to 1.

    
`draw_deck(deck, increment=0, init_draw=False, enable_scheduler=True)`
:   Draws the deck
    
    Args:
        deck (deck): The deck
        increment (int, optional): How many pages to increment. Defaults to 0.
        init_draw (bool, optional): True if it's the first time the deck is drawn. Defaults to False.
        enable_scheduler (bool, optional): Enable the scheduler or not. Defaults to True.

    
`handle_button_action(deck, key, pressed)`
:   Handles the action triggered by the key callback
    
    Args:
        deck (deck): The deck
        key (Key): The triggered key
        pressed (bool): The state of the button
    
    Raises:
        FileNotFoundError: Raised when a plugin is not found
    
    Returns:
        func: The main function of the plugin

    
`handle_button_icon(key, pressed)`
:   Decides which image to display depending on the state and type of the button
    
    Args:
        key (Key): The key activated
        pressed (bool): The status of the button
    
    Returns:
        string: An icon name

    
`key_change_callback(deck, key_num, pressed)`
:   Function called when a button is pressed
    
    Args:
        deck (deck): The deck
        key_num (integer): Index of the key activated
        pressed (bool): True for pressed, false for released

    
`reload(deck)`
:   Reload the deck
    
    Args:
        deck (deck): The deck

    
`render_key_image(deck, icon_filename, key)`
:   Renders the given image on a key
    
    Args:
        deck (deck): The deck
        icon_filename (string): Filename for the icon
        key (Key): The key to render the image on
    
    Raises:
        FileNotFoundError: Icon file path is invalid
    
    Returns:
        StreamDeck Image: An image renderable by the StreamDeck

    
`update_key_image(deck, key, pressed, blank=False)`
:   Update the image on a key
    
    Args:
        deck (deck): The deck
        key (Key): Key to update
        pressed (bool): True if the key was pressed
        blank (bool, optional): Creates a blank image. Defaults to False.

    
`update_key_state(key)`
:   Writes the current toggle state of a key.
    
    Args:
        key (Key): Key to save

    
`update_label_display(key, label=False)`
:   Writes the current text for a label or a display.
    
    Args:
        key (Key): Key to update
        label (bool, optional): Should be set to true if writing a display, false for a label. Defaults to False.

Classes
-------

`deck_vault()`
:   Holds the current Deck object statically.

    ### Class variables

    `deck`
    :