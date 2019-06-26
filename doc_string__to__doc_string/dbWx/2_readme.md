
this text will not be in the final readme.
this text will not be in the final readme.
this text will not be in the final readme.
this text will not be in the final readme.



<!-- Start from here -->

## What Works

Remember, these are Engineering Releases.  Not all features are complete, but generally speaking those that are marked as completed and working are working quite well.  It's not an "Engineering Quality".  The completed features are at about a Beta level.

### Ready to use

#### Elements

* Text
* Input Text
* Buttons including file/folder browse
* Input multiline
* Output multiline
* Output
* Columns
* Progress Meters
* Checkbox
* Radio Button
* Combobox
* Spinner


#### Features
* System Tray
* Debug Print
* Invisible/Visible Elements
* All Popups
* Check box
* Keyboard key events
* Mouse wheel events
* Multiple windows
* Read with timeout
* Background images
* One Line Progress Meter (tm)
* Auto-closing windows
* No titlebar windows
* Grab anywhere windows
* Alpha channel
* Window size
* Window disappear/reappear
* Get screen size
* Get window location
* Change window size
* Window move
* Window minimize
* Window maximize
* Window Disable
* Window Enable
* Window Hide
* Window UnHide
* Window Bring to front
* Look and Feel settings
* Default Icon
* Base64 Icons




It won't take long to poke at these and hit errors.  For example, the code to do Button Updates is not complete.  Most of the time you won't be doing this.

Due to the small size of the development team, features may feel a little "thin" for a while.  The idea is to implement with enough depth that 80% of the uses are covered.  It's a multi-pass, iterative approach.

If you, the reader, are having problems or have hit a spot where something is not yet implemented, then open an Issue.  They are often completed in a day.  This process of users pushing the boundaries is what drives the priorities for development.  It's "real world" kinds of problems that have made PySimpleGUI what it is today.



## SystemTray

This was the first fully functioning feature of PySimpleGUIWx.  Previously only the Qt port supported the System Tray.  Why use Wx?  The footprint is much much smaller.  An EXE file created using PyInstaller is 9 MB for PySimpleGUIWx, when using Qt it's 240 MB.

Now it's possible to "tack on" the System Tray to your PySimpleGUI application.

If you're unable to upgrade to Qt but want the System Tray feature, then adding PySimpleGUIWx to your project may be the way to go.

You can mix your System Tray's event loop with your normal Window event loop by adding a timeout to both your Window.Read call and your SystemTray.Read call.

### Source code compatibility

PySimpleGUIWx's System Tray feature has been tested against the same PySimpleGUIQt feature.  As long as you don't use features that are not yet supported you'll find your source code will run on either PySimpleGUIQt or PySimpleGUIWx by changing the import statement.


## System Tray Design Pattern

Here is a design pattern you can use to get a jump-start.

This program will create a system tray icon and perform a blocking Read.

```python
import PySimpleGUIWx as sg

tray = sg.SystemTray(menu= ['menu',['Open', ['&Save::KEY', '---', 'Issues', '!Disabled'], 'E&xit']],
					 filename=r'C:\Python\PycharmProjects\GooeyGUI\default_icon.ico')
tray.ShowMessage('My Message', 'The tray icon is up and runnning!')
while True:
	event = tray.Read()
	print(event)
	if event == 'Exit':
		break
```


## Menu Definitions

See the original, full documentation for PySimpleGUI to get an understanding of how menus are defined.


## SystemTray Methods

### Read - Read the context menu or check for events

```python
def Read(timeout=None)
'''
	Reads the context menu
	:param timeout: Optional.  Any value other than None indicates a non-blocking read
	:return:   String representing meny item chosen. None if nothing read.
'''
```
The `timeout` parameter specifies how long to wait for an event to take place.  If nothing happens within the timeout period, then a "timeout event" is returned.  These types of reads make it possible to run asynchronously.  To run non-blocked, specify `timeout=0`on the Read call (not yet supported).

Read returns the menu text, complete with key, for the menu item chosen.  If you specified `Open::key` as the menu entry, and the user clicked on `Open`, then you will receive the string `Open::key` upon completion of the Read.

#### Read special return values

In addition to Menu Items, the Read call can return several special values.    They include:

EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED - Tray icon was double clicked
EVENT_SYSTEM_TRAY_ICON_ACTIVATED - Tray icon was single clicked
EVENT_SYSTEM_TRAY_MESSAGE_CLICKED - a message balloon was clicked
TIMEOUT_KEY is returned if no events are available if the timeout value is set in the Read call


### ShowMessage

Just like Qt, you can create a pop-up message.  Unlike Qt, you cannot set your own custom icon in the message, at least you can't at the moment.

The preset `messageicon` values are:

- SYSTEM_TRAY_MESSAGE_ICON_INFORMATION
- SYSTEM_TRAY_MESSAGE_ICON_WARNING
- SYSTEM_TRAY_MESSAGE_ICON_CRITICAL
- SYSTEM_TRAY_MESSAGE_ICON_NOICON

```python
ShowMessage(title, message, filename=None, data=None, data_base64=None, messageicon=None, time=10000):
'''
	Shows a balloon above icon in system tray
	:param title:  Title shown in balloon
	:param message: Message to be displayed
	:param filename: Optional icon filename
	:param data: Optional in-ram icon
	:param data_base64: Optional base64 icon
	:param time: How long to display message in milliseconds  :return:
'''
```

### Update

You can update any of these items within a SystemTray object
* Menu definition
* Icon (not working yet)
* Tooltip

 Change them all or just 1.

```python
Update(menu=None, tooltip=None,filename=None, data=None, data_base64=None,)
'''
	Updates the menu, tooltip or icon
	:param menu: menu defintion
	:param tooltip: string representing tooltip
	:param filename:  icon filename
	:param data:  icon raw image
	:param data_base64: icon base 64 image
	:return:
'''
```
## Menus with Keys

You can add a key to your menu items.  To do so, you add :: and the key value to the end of your menu definition.

`menu_def = ['File', ['Hide::key', '&Open::key', '&Save',['1', '2', ['a','b']], '&Properties', 'E&xit']]`

The menu definition adds a key "key" to the menu entries Hide and Open.

If you want to change the separator characters from :: top something else,change the variable `MENU_KEY_SEPARATOR`

When a menu item has a key and it is chosen, then entire string is returned.  If Hide were selected, then Hide::key would be returned from the Read.  Note that the shortcut character & is NOT returned from Reads.


## Popups

Starting with release 0.4.0, most of the Popup functions work.  This means you can do things like show information in a window when there's a choice made in a System Tray menu.  Or if your program finds some event it wishes to inform the user about.  For example, when new Issues are posted on a GitHub project.