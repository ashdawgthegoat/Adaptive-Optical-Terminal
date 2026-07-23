# The settings app built as a standalone application should have the following things.
    
    1. A three panel layout with a floating panel. the left panel hosting the sections such as Appearence, Wifi, Bluetooth, Sound, About us (for now, as many more will be added in the future updates.)
    2. The right panel should host the properties of each section selected in the left panel. The Properties panel is used only for navigation. Property values are modified exclusively through the Overlay.
    3. Once a certain property is selected, a floating panel (overlay) will appear containing the elements that can be changed in the particular property.
    4. After changing the elements of a property in the floating panel. The preview of the changed element will be displayed in the middle panel. 

# Navigation:

    * Primarly keyboard navigation with mouse integration later.
    * Enter key for selection.
    * Esc key for returning back.

# Implemetation:

    1. Preview will update live based on the property changed.
    2. No changes will be committed unless the user explicitly applies them.

# Purpose:

    The Settings application allows the user to configure
    WandererUI and preview changes before applying them.

# Sections (Displayed on the left panel):

    Appearence
    Wi-Fi
    Bluetooth
    Audio
    Modules
    About

# Properties:

    For every section, list its corresponding properties on the right panel.

    ex: Appearence - Theme, Wallpaper, Font, Accent

# Preview Behaiviour:

    it displays preview of a change one at a time,

    ex: Theme - Miniature Desktop Updates.
        Wallpaper - Wallpaper renderer updates.
        Font - Typography specimen updates.
        Accent - Recolors the minature desktop.
        About Us - Information about the Wanderer Project and the UI info in general.
        Rest will have their placeholders.

# Overlay behaviour:

    *It's lifecycle in settings application can be defined as:

    Enter on property
    ↓

    Overlay opens

    ↓

    User selects value

    ↓

    Preview updates

    ↓

    Esc closes overlay

    ↓

    Apply commits changes

    ↓

    Cancel restores previous values

# Navigation state machine:

    * the focus is initially on the left panel. and as the user navigates through the options, their corresponding properties will appear on the right panel.
    * once the user selects an option, the focus immediately shifts to the right panel.
    * then once the user selects the property in the right panel. the overlay appears an the focus is shifted to the overlay.
    * After changes are done in the overlay and confirms the preview, the user can hit the ESC key to close overlay and the focus shifts back to right panel and hitting ESC key once again returns focus to the left panel.
    * If the user commits the changes before hitting the ESC key from the left panel which will return them back to the desktop and close the application then the changes are applied. Else the user will be notified (using overlay obviously) and then the user can commit or reject the changes from the notification.

    Apply
    - Commits staged changes.
    - Does not close the application.

    Exit
    - If nothing is staged, closes immediately.
    - If staged changes exist, asks whether to Apply or Discard.

# Definition of Done:

    The standalone Settings application is complete when:

    ✓ Keyboard navigation works.

    ✓ Overlay works.

    ✓ Theme preview works.

    ✓ Wallpaper preview works.

    ✓ Font preview works.

    ✓ Changes are staged.

    ✓ Apply commits changes.

    ✓ Cancel discards staged changes.

    ✓ No WandererUI services are required.

# Application Lifecycle:

    Launch

    ↓

    Focus starts on the left panel.

    ↓

    User navigates Settings.

    ↓

    If no staged changes exist:

    Esc from the left panel exits Settings.

    ↓

    If staged changes exist:

    Esc from the left panel opens a confirmation overlay.

    ↓

    Apply

    ↓

    Changes are committed.

    ↓

    Settings exits.

    ↓

    Discard

    ↓

    Changes are reverted.

    ↓

    Settings exits.

# Important Note:

    The Preview panel never modifies application state.

    It is a visualization of the currently staged changes only.