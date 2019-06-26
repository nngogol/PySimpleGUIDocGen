
# Release Notes:

## 0.1.0 PySimpleGUIWeb 22-Jan-2019

* Initial release
* Text Element
* Input Text Element
* Button Element
* Window class


## 0.2.0 PySimpleGUIWeb 23-Jan-2019

Day 2 of development brings fonts, sizes, and colors...

* For all elements (Text, Input Text, Button):
    * Font family
    * Font size
    * Text Color
    * Background Color
    * Disable
    * Size
* Button Color
* Read timeouts (zero, non-zero, None/pend)
* Window close
* Window background color

## 0.3.0 PySimpleGUIWeb 24-Jan-2019

* Checkbox Element
* Combobox Element
* Listbox Element
* Element padding for all elements

## 0.4.0 PySimpleGUIWeb 26-Jan-2019

Functioning Elements
* Text
* Single line text input
* Multiline Input
* Multiline Output
* Listbox
* Combobox
* Checkbox
* Slider
* Spinner (numbers only...hardcoded to 0 to 100)

New features
* Tooltips for all elements (so cool this works)
* Input Text events
* Text clicked event
* Listbox selected event
* Combobox selected event
* Checkbox Update
* Disable parameter for all elements
* Window.Close shuts down the server
* Enabled exceptions during packing operation
* New test harness exercises all element types

## 0.5.0 PySimpleGUIWeb  1-Feb-2019

* New default font size. Was Helvetica 10, now Helvetica 15
* InputText Element single character events working! (Finally)
* Listbox simple Update (values only)
* Column Element!  New!
* Column element experimental justification setting doesn't work yet
* Element background colors now picked up from container, not top level window
* Autosize Text
* Autosize Button Text


## 0.6.0 PySimpleGUIWeb  3-Feb-2019

* Changed Remi port to 0 so will always get a new free port

## 0.7.0 PySimpleGUIWeb  3-Feb-2019

* Completed `InputText.Update` method so that more demos can be run

## 0.8.0 PySimpleGUIWeb 8-Feb-2019

* Popup support!
* Support for multiple windows

## 0.9.0 PySimpleGUIWeb 14-Feb-2019

* Support for Window.Hide, Window.UnHide (better multi-window support)

## 0.9.1 PySimpleGUIWeb

* Emergency release due to some code to do scrolling of multiline not being right and sometimes crashed programs

## 0.10.0 PySimpleGUIWeb 16-Feb-2019

* Completed Text.Update method. Can now change:
    * Text
    * Font family & size
    * Background color
    * Text Color
    * Visibility
* Completed Button.Update with exception of images
* Completed Spin.Update with except of range. This element still pretty crippled
* Completed Slider.Update - Can update value, visibility, disabled, but not the range
* Image Element!
* Events for Image Element
* Image.Update to change image

## 0.11.0 PySimpleGUIWeb  25-Feb-2019

- Slider - Can update range using .Update method
- NEW Window paramters that allow control over all Remi startup settings
- New Window paramters and default values:
    - web_debug=False
    - web_ip='0.0.0.0'
    - web_port=0
    - web_start_broswer=True
    - web_update_interval=.00001
* Can set the Window backaground image (sorta works sometimes)
    * Struggling to get the "resources" settings understood so can work with files
    * I have a ways to go

## 0.12.0 PySimpleGUIWeb 28-Feb-2019

* Combo.Update now fully functional


## 0.13.0 PySimpleGUIWeb 5-Mar-2019

* Added new parameter to Window - web_multiple_instance
    - Like other Window web parameters, this value is passsed Remi upon start
    - The default value is TRUE (Previously I think default was False by Remi)
    - Was made as a result of comment on repl.it.

## 0.15.0 PySimpleGUIWeb 5-Mar-2019

* Made the multiple_instance parameter FALSE by default (was messing up badly with True)

## 0.16.0 13-Mar-2019

* TABLES!
    * The bare minimum, basic tables are supported
    * Things like alternating colors are not done
    * Enabling Events DOES work so that you can get immediate clicks
    * Value returned is a list of 1ength 1 and contains the value of the cell that was clicked
* Removed use of CloseButton from Popups

## 0.17.0 14-Mar-2019

* More Table features supported
    * Option to display row numbers
    * New parameter `row_header_text`
    * Can turn on / off displaying row numbers
    * `enable_events`
    * `text_color`
    * Font
    * Can get the value of the item clicked using Table.SelectedItem.  Can be coded as window.Element('_table_').SelectedItem


## 0.18.0 15-Mar-2019

* Hotfix for bug that causes Popups / secondary windows to crash
* Table gets `starting_row_num` parameter

## 0.19.0 23-Mar-2019 PySimpleGUIWeb

* do_not_clear defaults to TRUE! for Input and Multiline Input/output
* a few type hints

## 0.20.0 07-Apr-2019 PySimpleGUIWeb

* Output Element WORKS!!  Can re-route stdout to window
* Added Idle function to Remi MyApp for stdout re-route (thanks Davide!!)
* New Shortcuts:
    * I = InputText
    * B = Btn = Butt = Button
* Removed temp size in Multiline setup
* Button - convert button text passed in into a string
* Added support for base64 Images in Image.Update but it's not working! Don't use!
* Changed web_update_interval=.0000001 from 0 (YIKES I HOPE SOMETHING DIDN'T BREAK!)


## 0.21.0 10-Apr-2019 PySimpleGUIWeb

* If `disable_close` parameter set in Window call, then Remi will not disconnect when browser closed.  Great for reconnecting.


## 0.22.0 11-Apr-2019 PySimpleGUIWeb

* NEW Window parameter layout so can skip calling Layout

## 0.23.0 21-Apr-2019 PySimpleGUIWeb

* GRAPH ELEMENT almost done!
    * DrawLine
    * DrawRectangle
    * DrawPoint
    * DrawCicle
    * DrawText
    * Erase
    * Move
    * MoveFigure (by a delta amount)
    * RelocateFigure (draw to a new spot)
    * Update - for background color change
    * Enable events works for single clicks (no drags yet)
* Changed Image element to use SuperImage class
    * Image element works better?
    * Base64 not yet working

## 0.23.1 21-Apr-2019
One-time patch to remove a debug print  

# 0.24.0  PySimpleGUIWeb 23-Apr-2019

* Enabled SuperImage class to accept base64 imagees
* Now use an SvgGroup to hold all of the drawing items
* Circle can now set outline color
* DrawImage still isn't working
* Move isn't working
* Added Relocate for group
* Lazy buttons - Up, Down, Left, Right(()
    * Creates buttons with arrows on them as text
* Base64 support for Image Element


## 0.25.0 PySimpleGUIWeb 25-Apr-19

* DrawImage method WORKS! DrawImage now takes BOTH filenames and base64 variables
* Fix for DrawRectangle (wasn't passing the right parms)

## 0.26.0 PySimpleGUIWeb 1-May-2019

* Combo - converts values into a list of strings
* Image.Update is working with both filename and base64 (but no size controls yet)
* Window - new parameter - return_key_down_events. Normally it's key up events that are returned from Read calls
* Returning keyboard input works!
* Turned off Remi Logging completely (may be a bad idea. can change it back)
* Rearranged code so that same code is used for first window and following windows
* Window disable_close parameter controls wether or not server keeps running after user disconnects

## 0.27.0 PySimpleGUIWeb 8-May-2019

* Changed default icon from string to bytes
* New Text Update to match newer call parameters
* Added image_subsample, image_size parms to be backward compat. Note - not enabled
* SuperImage changes - load both base64 images and files
* Fix for DrawRectangle
* Added data parm to DrawImage
* Added DeleteFigure
* Tab Support
    * Just barely beginning
    * May or may not work
* Window new class variable - AllKeysDict
    * Contains dictionary of all elements and keys
    * Now used by FindElement / Element calls for quick lookup
* Fix for Column elements and rows that didn't line up. Changed tk_row_frame style
* Graph Element
    * enable_events works
    * drag events works
    * click events works


## 0.28.0 PySimpleGUIWeb 15-May-2019

* Menus
    * Yes, the full Menu Bar across the top of the window!
    * PLUS, you get more controls to set the colors and fonts
    * Works with menu keys too
    * Disabled items are not working however
    * Correctly returns menu events
* Listbox
    * Correctly handling Update calls that change the list
    * Correctly returns a LIST of items (even if only 1)
* Button Graphics!
    * Can specify either a filename or image data as the source
    * Update parameters image_data and image_filename work!
* Fix in DrawLine. Wasn't returning the id
* DrawRectangle fixes - transparent fill color is default. Correctly draws coordinates now
* DrawImage seems to work with both data and files
* enable_events parameter for TabGroups
* Frame Element
    * Behaves like a Column element for now since no official Remi Frame
* Fix for popups that get data - New dictionary return values messed up popups. Needed to use keys internally

# Design

## Author
Mike B.


## License
GNU Lesser General Public License (LGPL 3) +

## Acknowledgments
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA1OTc2NTUwMywtMTE2NjcxOTkxNyw0Nz
U4NjU2NzYsLTEwNTcxMDM2NDMsMTIxMzM1MjYzNiwtMTE2MDY4
NDMzOV19
-->