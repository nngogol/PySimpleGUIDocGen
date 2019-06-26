

# Release Notes:

### 0.1.0   -   25-Dec-2018

* Support for SystemTray
    * Read, with or without a timeout
    * Catch single click, double click events
    * Source code compatiable with Qt

### 0.2.0   -   26-Dec-2018

* Correctly handling base64 images
* Support for clicking message balloon
* Can Hide and  UnHide the  icon


### 0.3.0   -   27-Dec-2018

* Hooked up buttons!
* Browse file button is only file/folder button that works
* Text, Input and Button elements are the only working elements
* SystemTray can take any kind of image as icon
* Read with Timeout (non-zero) works
* Popups


### 0.4.0 PySimpleGUIWx  30-Dec-2018

* Text Element - colors, font work
* Text Update method works
* Button - Close button implemented
* Button - Implemented basic button, correctly presented Values on Read
* Button - Can now set font
* Changed overall "App" variable usage for better mainloop control
* Windows - Timeouts and non-blocking Reads work
* Windows - Autoclose works
* Windows - Non-blocking calls supported (timeout=0)
* Windows - Grab anywhere works
* Windows - No title-bar works
* Windows - Location and Size working correctly
* Correctly adding element padding to Text, Input, Buttons
* Popups - most Popups work (except for the input type that involve folders)

### 0.5.0 PySimpleGUIWx 6-Jan-2019

* New element - Multiline input
* New element - Multiline output
* Borderless Windows
* Grab anywhere windows
* Alpha channel for windows
* Finishing up the Text and Input Text Elements
* Visibility for all Elements
* Input Get / Set focus
* Output element - unable to get stdout to re-route
* Debug window works


### 0.6.0 9-Jan-2019

* Column Element
* Checkbox Element with events
* Output Element
* Background Image (I think works)
* Debug Print
* One Line Progress Meter
* All Popups works

### 0.7.0 PySimpleGUIWx 21-Jan-2019

* Element.Update support for disabled and tooltip
* Combo Element
* Newest Combo parameters
* Radio Element
* Newest Radio parameters (size_px, visible, enable_events)
* Type hints on Wx widgets
* Spinner Element
* Newest Spinner parameters
* Text Element visibility
* Column Element size_px parameter (unclear if works... likely does not)
* Column visibility
* Column Update method added
* System Tray - support for any kind of image format for icons
* Window.Move
* Window.Minimize
* Window.Maximize
* Window.Disable
* Window.Enable
* Window.Hide
* Window.UnHide
* Window.BringToFront
* Popup non_blocking - returns window and button not just button
* More comprehensive test harness when running PySimpleGUIWx.py

### 0.8.0 20-Feb-2019 PySimpleGUIWx

* Big Try/Except block around Update method for multiline in case window closed
* Text - convert incoming text to string right away
* Text.Update - convert incoming value to string
* Completed Button.Update method.  Can now change text, color, etc.
* Added Try around reading multiline input value - not sure why needed
* OneLineProgressMeter - can update text on every call now

### 0.9.0 06-Mar-2019 PySimpleGUIWx

* Addition of Assert Suppression
    - This was needed for a  multi-threaded version of PySimpleGUIWx
    - Complained when exiting a system tray if did not make this change and ran the tray in a thread
* Tray.Close now correctly Hides the icon
* SetGlobalIcon functional
* Can also now set icon using SetOptions call


### 0.10.0 23-Mar-2019 PySimpleGUIWx

* `do_not_clear` is now TRUE by default on Input and Multiline elements!!


## 0.11.0 11-Apr-2019 PySimpleGUIWx

* NEW Window parameter layout so can skip calling Layout

# Design
# Author
Mike B.

# License
GNU Lesser General Public License (LGPL 3) +

# Acknowledgments
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyMzExNjg0MDAsLTIxNDIwNTI0ODQsOD
g2MzA1Mjk2XX0=
-->