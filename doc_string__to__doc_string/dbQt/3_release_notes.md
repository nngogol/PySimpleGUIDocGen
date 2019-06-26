# Release Notes:

### 0.12.0   -   20-Nov-2018
Correctly restore stdout when Output Element is deleted
Added Finalize ability
**Better multi-window handling... maybe it's finally fixed!**
Radio button default value
Dial element default value
Show expanded option for trees
Titles for popups

### 0.13.0 -  22-Nov-2018

Focus for Input Text and Multiline Input

- Get focus
- Set focus

Window.FindElementWithFocus works
Multiline input

- Change submits
- Update - disabled, append

Multiline output - Update value, append, disabled, get value
Text clicked submits
File types for open files
Initial folder, file types, for browse buttons
File types standardized on tkinter data format
Find Element With Focus now works for input and multiline input
Yet more multiwindow handling
Relief for Text element
Input text disable
Correct sizing of Comboboxes using visible items parm
Correct default values for input and multiline input
Change submits for multiline
Horizontal and Vertical separators
PopupGetFile and PopupGetFolder - no_window option works

### 0.14.0 - 24-Nov-2018

Slider tick positions set using relief parm
ButtonMenu Element
Multiline.Update font parm
Text.Update color and font now work
Button.Update font support
Window.Element = Window.FindElement
Better font support for all elements - underline, bold
Element padding - complete rework
Text element padding
Button padding
Input Text padding
Input Text password char
Listbox padding
Combobox padding
Multiline padding
Checkbox padding
Radio padding
Progress Bar padding
Output padding
Image padding
Graph padding
Slider - set tick marks using relief parm
Dial - set tick information using resolution and tick interval
Table padding
Tree padding
Separator padding
Force window sizing should mean windows are better sized
Popup - better layout


### 0.15.0 24-Nov-2018

New SystemTray feature!
margin paramter for Text Element.  Takes 4 ints
Corrected button colors when disabled. For now am restoring them to original colors
Border Depth for all elements that support it (inputs, slider, table, tree, etc)
Fix for Element padding done incorrectly!! Sorry about this one


### 0.16.0  24-Nov-2018

Easier forcing to use PyQt5 for testing
Predefined events for Tray Icons
* Double Clicked
* Icon Activated
* Message Clicked
* Timeout key for polling

Tray icon tooltip
Menu keys with programmable separator
Better element padding hierarchy
Menubar now returns values as does the ButtonMenu

### 0.17.0  24-Nov-2018

Window.Hide and UnHide methods

### 0.18.0 26-Nov-2018

Tooltips for all elements
Completion of all SystemTray features
Read with or without timeout
Specify icons from 3 sources
Show message with custom or preset icons
Update
* Menu
* Tooltip
* Icon
PopupScrolled - new location parameter, fixed bug that wasn't closing window when completed

### 0.19.0 28-Nov-2018

Ability to disable menu items by adding ! to the front
Disable menu works for menus, button menus, system tray menus
Combo - Update Method - Value, values, disabled, font
Listbox - Update Method - Values, disabled
Listbox - SetValue Method - sets the selected items
Radio Button - Update Method - value, disabled
Checkbox - Update Method - value, disabled
Spinner - Update Method - value, values, disabled
Spinner - change_submits works
Image - New feature!  click_submits option (acts like a button in a way)
Window - Get screen dimensions
Slider - disable
Dial - disable

### 0.20.0 6-Dec-2018

* Ability to change calculations between characters and pixels
* size_px added to ALL elements that have a size parameter
* General Element.Update(widget, background_color, text_color, font, visible)
* visible parameter added to ALL elements
* enable_events flag
* Input text - enable events, visibility, size_px
* Input text update added capabilities
    * ability to highlight the input string
    * background, text colors and font
* Combo - enable events, visibility, size_px
* Combo - auto complete feature
* Combo - added to Update - background color, text color, font, visible
* Listbox - enable events, visibility, size_px
* Listbox - better scaling from characters to pixels
* Listbox - ability to Update with set to index, text color, font, visibility
* Radio - enable events, visibility, size_px
* Radio - Update additions - background_color, text_color, font, visibility
* Checkbox - enable events, visibility, size_px
* Checkbox - Update additions - background_color, text_color, font, visibility
* Spin - enable events, visibility, size_px
* Spin - Update additions - background_color, text_color, font, visibility
* Multiline input - enable events, visibility, size_px
* Multiline input - Update additions - background_color, text_color, font, visibility
* Multiline input better character to pixel scaling
* Multiline output - enable events, visibility, size_px
* Multiline output - Update additions - background_color, text_color, visibility
* Text - enable events, size in pixels
* Text - Update addition of visibility
* Output - visible, size_px
* Output - added update capability with new value, background_color, text_color, font, visibility
* Button - enable events, visible, size_px
* Button - Color Chooser feature completed
* Button - Color Chooser can target (None, None) which will store the value to be returned with the values from Read()
* Button - fixed bug in SaveAs button code.  Bad filter variable
* Button - Updated added font, visibility
* Button - new SetFocus() method will set the focus onto the button
* ButtonMenu - Update method implemented that includes menu definition changes, text, button color, font, visibility
* ProgressBar - added visibility, size_px
* ProgressBar - added Update method for changing the visibility
* Images - events, size_pix, visibility
* Images - can now get click events for images!
* Images - Update added visibility
* Graph - visibility, size_px
* Graph - Update method for changing visibility
* Frame - visibility, size_px
* Frame - Update method added that controls visibility
* ALL elements inside of a Frame that's invisible will also be invisible
* Tab - visible parameter added, however not yet functional!
* TabGroup - enable events, visibility
* TabGroup - Update for controlling visibility
* Slider - enable events, size_px
* Slider - Update method now includes visibility
* Dial - enable events, size_px, visibility
* Dial - Update method added visibilty control
* Column - visibility added
* Column - Added Update method to control visibility
* ALL elements inside of an invisible Column Element will also be invisible
* MenuBar - added visibility
* MenuBar - Update can now change menu definitions at runtime, and control visibility
* Table - enable events, size_px, visibility
* Table - Update method can control visibility
* Tree - enable events, size_px, visibility
* Tree - Update method can control visibility
* VisibilityChanged() function that must be called when using Qt so that the window will shrink or grow
* window.GetScreenDimensions can now be called prior to window creation
* window.Size property
* enable_events added to all of the shortcut buttons and browse buttons
* Ability to set a button image from a file
* Combo - ability to set a default value
* Combo - Read only setting.  Allows for user editing of value
* Menus - Ability to disable / enable any part of a menu by adding a ! before the entry name
* Tabs - ability to set tab text color, background color, background color of selected tab
* Tabs - ability to set widget area's background color
* Sliders - paging works properly (using page-up page-down or slider slider area to advance slider)
* Tree - Setting number of visible rows implemented
* Added 5 pixels to every window.  Have been having issues with text being cutoff on the right side
* SetOptions - ability to change default error button color for popups

### 0.21.0 - 9-Dec-2018

* Removed use of global variabels - using static class variabels instead
* Listbox.Get() will return current listbox value
* Progressbar now has color support
* Progressbar can be vertical now
* Can change bar or back and background color
* (barcolor, background color - None if use default)
* Table num_rows parameter implemented
* Table.Update - can change number of visible rows
* Window resizable parm - implemented, default changed from False to True
* Window.Move - implemented
* Window.Minimize - implemented
* Window.Disable - implemented
* Window.Enable - implemented
* Window.CurrentLocation - implemented
* Fixed too small scrollbar in Combobox
* Fixed too small scrollbar in Listbox
* Changed "text" window to a complex one for quick regression testing (try running PySimpleGUIQt.py by itself)

### 0.22.0 - 9-Dec-2018

* Spin.Get method - get the current spinner value

### 0.23.0 PySimpleGUIQt

* Fixed crash that was happening with latest pyside2 release!!!!
* Huge update to OneLineProgressMeter
* Debug window got title and do-not-reroute-std-out option
* Popups get a title option
* PopupScrolled getr non-blocking option
* Default logo included in Base64 Format
* Changed Chars to pixels scaling.  Went from (10,25) to (10,35)
* Changed pixel to chars cutoff from 10 to 12
* Change progress bar default size to 200 from 250
* Reworked the _my_windows global variable / class to use Window class variables
* Change in how Elements / Widgets are updated. Need to use {} correctly
* InputText supports drag and drop
* Support for Checkbox.Get()
* Support for strings in spinbox
* Added Update method to Output element
* Changed Button default file_types from *.* to *
* Support for Tab enable_events so they now generate events
* Table.Update can change the number of rows of table
* Window class now manages the list of active popups, user defined icon, QTApplication, num open windows
* Window resizable parameter default changed from False to True
* Window new parameter -  disable_minimize
* Window.GetScreenDimensions added
* Window.Move added
* Window.Minimize added
* Window.Maximize added
* Window.Disable added
* Window.Enable added
* Window.BringToFront added
* Window.CurrentLocation added
* TabGroup now returns which tab is selected in the return values
* Completely new Style generation class and functions (I hope it works!!!!)
* Style reworked for Column, Text, Button, Input, Combobox, Listbox, Input Multiline, Output Multiline, Progress Bar, Spinbox, Output,
* Progress Bar colors are now correct
* Events generated when tabs are changed
* "Better" Table support.   Uses num_rows now and styles the scrollbar
* Tree element can support multiple types of icons including base64
* Fixed tree element scroll bar
* Icon ccan be set using SetOptions
* main for PySimpleGUIQt.py gets a nice test harness that shows lots of Elements


### 0.24.0 PySimpleGUIQt

* do_not_clear defaults to TRUE! for Input and MultilineInput/Output
* Key events for tables (unsure what's actually implemented)
* Tree icons can now be bytes in addition to filename!  (More Base64 support)


### 0.25.0 PySimpleGUIQt 5-Apr-2019

* Uses built-in Default Base64 Logo! (no more .ico file needed)
* New shortcuts for Elements
    * I = InputText
    * B = Butt = Btn = Button
* Convert user supplied button text to string just in case not a string
* Parameter `icon` in `Window` call can be Base64 byte string in addition to filename


### 0.26.0 11-Apr-2019 PySimpleGUIQt

* NEW Window parameter layout so can skip calling Layout


# Design

## Author
Mike B.

## Demo Code Contributors

## License
GNU Lesser General Public License (LGPL 3) +

## Acknowledgments