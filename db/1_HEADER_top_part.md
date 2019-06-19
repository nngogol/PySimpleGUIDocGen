<!--
HOW DO I INSERT IMAGES ???
	easy.

	■■■ 1 pic at CENTER ■■■

	<div align="center" style="padding: 5px;">
		<img src="...">
	</div>

	■■■ N pic, inline, Space around ■■■

	<p style="display: flex;justify-content: space-around;">
		<img src="...">
	</p>

	■■■ N pic, inline, padding ■■■

	<p style="display: flex;justify-content: space-around;">
		<img style="padding:10px;" src="..." >
		<img style="padding:10px;" src="..." >
		<img style="padding:10px;" src="..." >
	</p>


 -->

![pysimplegui_logo](https://user-images.githubusercontent.com/13696193/43165867-fe02e3b2-8f62-11e8-9fd0-cc7c86b11772.png)

[![Downloads](http://pepy.tech/badge/pysimplegui)](http://pepy.tech/project/pysimplegui) tkinter

[![Downloads ](https://pepy.tech/badge/pysimplegui27)](https://pepy.tech/project/pysimplegui27) tkinter 2.7

[![Downloads](https://pepy.tech/badge/pysimpleguiqt)](https://pepy.tech/project/pysimpleguiqt) Qt

[![Downloads](https://pepy.tech/badge/pysimpleguiwx)](https://pepy.tech/project/pysimpleguiWx) WxPython

[![Downloads](https://pepy.tech/badge/pysimpleguiweb)](https://pepy.tech/project/pysimpleguiWeb) Web (Remi)


![Documentation Status](https://readthedocs.org/projects/pysimplegui/badge/?version=latest)
![Awesome Meter](https://img.shields.io/badge/Awesome_meter-100-yellow.svg)
![Python Version](https://img.shields.io/badge/Python-2.7_3.x-yellow.svg)



# PySimpleGUI

* Create windows that look and operate _identically_ to those created directly with tkinter, Qt, WxPython, and Remi.
* Requires 1/2 to 1/5th the amount of code as underlying frameworks.
* For exampl, develop a working Qt application in 1/2 to 1/5th the number lines of code.
* The savings can be even greater depending on your application.
* One afternoon is all that is required to learn the PySimpleGUI concepts and APIs.

## Supports both Python 2.7 & 3 when using tkinter

## Supports both PySide2 and PyQt5 (limited support)

## Effortlessly move across tkinter, Qt, WxPython, and the Web (Remi) by changing only the import statement

## The *only* way to write both desktop and web based GUIs at the same time


![Python Version](https://img.shields.io/badge/PySimpleGUI_For_Python_3.x_Version-4.0.0-red.svg?longCache=true&style=for-the-badge)

![Python Version](https://img.shields.io/badge/PySimpleGUI_For_Python_2.7_Version-2.0.0-blue.svg?longCache=true&style=for-the-badge)

![Python Version](https://img.shields.io/badge/PySimpleGUIQt_Version-0.31.0-orange.svg?longCache=true&style=for-the-badge)

![Python Version](https://img.shields.io/badge/PySimpleGUIWx_version-0.11.0-orange.svg?longCache=true&style=for-the-badge)

![Python Version](https://img.shields.io/badge/PySimpleGUIWeb_Version-0.28.1-orange.svg?longCache=true&style=for-the-badge)

[Announcements of Latest Developments](https://github.com/MikeTheWatchGuy/PySimpleGUI/issues/142)

[ReadTheDocs](http://pysimplegui.readthedocs.io/)

[COOKBOOK!](https://pysimplegui.readthedocs.io/cookbook/)

[Brief Tutorial](https://pysimplegui.readthedocs.io/tutorial/)

[Latest Demos and Master Branch on GitHub](https://github.com/MikeTheWatchGuy/PySimpleGUI)

[Docs in PDF Format](https://github.com/MikeTheWatchGuy/PySimpleGUI/tree/master/docs)

[Repl.it Home for PySimpleGUI](https://repl.it/@PySimpleGUI)

Super-simple GUI to use... Powerfully customizable

Home of the 1-line custom GUI & 1-line progress meter

The native GUI framework for perfectionists with deadlines

Actively developed and supported (It's 2019 and still going strong)

#### Note regarding Python versions
As of 9/25/2018 **both Python 3 and Python 2.7 are supported**!   The Python 3 version is named `PySimpleGUI`. The Python 2.7 version is `PySimpleGUI27`.  They are installed separately and the imports are different. See instructions in Installation section for more info.

# Qt Version


Check out the new PySimpleGUI port to the Qt GUI Framework.  You can learn more on the [PySimpleGUIQt GitHub site](https://github.com/MikeTheWatchGuy/PySimpleGUI/tree/master/PySimpleGUIQt).  **There is a separate Readme file for the Qt version** that you'll find there.

Give it a shot if you're looking for something a bit more "modern".  PySimpleGUIQt is currently in Alpha.  All of the widgets are operational but some may not yet be full-featured.  If one is missing and your project needs it, log an Issue and you'll likely get priority support.

Here is a summary of the Qt Elements

![scrolling graphics](https://user-images.githubusercontent.com/13696193/48665874-8bfd0e00-ea84-11e8-880d-8e164d9fea34.gif)

Are there enough things on there to cover your GUI solution?


## Source code compatibility
Your source code is completely portable from one platform to another by simply changing the import statement.

# WxPython Version

[PySimpleGUIWx GitHub site](https://github.com/PySimpleGUI/PySimpleGUI/tree/master/PySimpleGUIWx).  **There is a separate Readme file for the WxPython version**.

Started in late December 2018 PySimpleGUIWx started with the SystemTray Icon feature.    This enabled the package to have one fully functioning feature that can be used along with tkinter to provide a complete program.    The System Tray feature is complete and working very well.

The Windowing code is coming together with Reads now operational which means Popups work.  The elements are getting completed on a regular basis.  3 more were just checked in. At least 1 new element is getting completed a week.

# Web Version (Remi)

[PySimpleGUIWeb GitHub site](https://github.com/PySimpleGUI/PySimpleGUI/tree/master/PySimpleGUIWeb).  **There is a separate Readme file for the Web version**.

New for 2019, PySimpleGUIWeb.  This is an exciting development!  PySimpleGUI in your Web Browser!

The underlying framework supplying the web capability is the Python package Remi.  https://github.com/dddomodossola/remi  Remi provides the widgets as well as a web server for you to connect to.  It's an exiting new platform to be running on and has temporarily bumped the WxPython port from the highest priority.  PySimpleGUIWeb is the current high priority project.

Read on and you'll understand even more why this is an important project...

# repl.it Version

***Want to really get your mind blown?***  Check out this [PySimpleGUI program](https://repl.it/@PySimpleGUI/PySimpleGUIWeb-Demos) running in your web browser.

Thanks to the magic of repl.it and Remi it's possible to run PySimpleGUI code in a browser window without having Python running on your computer.

The programs you write using repl.it will automatically download and install the latest PySimpleGUIWeb from PyPI onto a virtual Python environment.  All that is required is to type `import PySimpleGUIWeb` you'll have a Python environment up and running with the latest PyPI release of PySimpleGUIWeb.

This is an exciting new development that's opening up all kinds of possibilities for new ways to program and learn PySimpleGUI.   Stayed tuned, much more to be posted about this in the near future.

Educators in particular should be interested.  Students can not only post their homework easily for their teacher to access, but teachers can also run the students programs online.  No downloading needed.  Run it and check the results.

Depending on how you're viewing this document, you may or may not see an embedded browser window below that is running PySimpleGUI code.

<!-- <iframe height="1000px" width="100%" src="https://repl.it/@PySimpleGUI/PySimpleGUIWeb-Demos?lite=true" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" sandbox="allow-forms allow-pointer-lock allow-popups allow-same-origin allow-scripts allow-modals"></iframe> -->

# Support

PySimpleGUI is an active project.  Bugs are fixed, features are added, often.  Should you run into trouble, open an issue on the GitHub site and you'll receive help by someone in the community.

# Platforms

It's surprising that Python GUI code is completely cross platform from Windows to Mac to Linux.  No source code changes.  This is true for both  PySimpleGUI and PySimpleGUIQt.

However, **Macs** suck.  They suck on tkinter in particular.  The "Look and feel" calls are disabled for Macs.  Colored buttons in particular are broken.  Not in the PySimpleGUI code, of course.    It's mostly because Macs suck.  Consider using Qt instead of tkinter on the Mac.  Or, if using tkinter, bring your own button images.

---

Looking for a GUI package?     Are you

* looking to take your Python code from the world of command lines and into the convenience of a GUI?  *
* sitting on a Raspberry **Pi** with a touchscreen that's going to waste because you don't have the time to learn a GUI SDK?
* into Machine Learning and are sick of the command line?
* wanting to distribute your Python code to Windows users as a single .EXE file that launches straight into a GUI, much like a WinForms app?
* would like to run a program in the system tray?
* a teacher wanting to teach your students how to program using a GUI?
* a student that wants to put a GUI onto their project?
* looking for an active project?

Look no further, **you've found your GUI package**.

```python
import PySimpleGUI as sg

sg.Popup('Hello From PySimpleGUI!', 'This is the shortest GUI program ever!')
```


![hello world](https://user-images.githubusercontent.com/13696193/44960047-1f7f6380-aec6-11e8-9d5e-12ef935bcade.jpg)


Or how about a ***custom GUI*** in 1 line of code?

```python
import PySimpleGUI as sg

event, (filename,) = sg.Window('Get filename example'). Layout([[sg.Text('Filename')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()] ]).Read()
```

![get filename](https://user-images.githubusercontent.com/13696193/44960039-f1018880-aec5-11e8-8a43-3d7f8ff93b67.jpg)


Build beautiful customized windows that fit your specific problem.  Let PySimpleGUI solve your GUI problem while you solve your real problems.   Look through the Cookbook, find a matching recipe, copy, paste, run within minutes.  This is the process PySimpleGUI was designed to facilitate.

Your windows don't have to look like "boring" old windows.  Add a few custom graphics to your windows to polish things up.

![batterup2](https://user-images.githubusercontent.com/13696193/50378902-6aa2bb00-060a-11e9-8f2f-d746694fa4ee.gif)


![uno_final](https://user-images.githubusercontent.com/13696193/49945232-67952580-feba-11e8-90c8-7dc31c5f7c67.gif)

PySimpleGUI wraps tkinter or Qt so that you get all the same widgets as you would tkinter/Qt, but you interact with them in a more friendly way.  It does the layout and boilerplate code for you and presents you with a simple, efficient interface.

![everything dark theme](https://user-images.githubusercontent.com/13696193/44959854-b1d23800-aec3-11e8-90b6-5af915a86d15.jpg)

Perhaps you're looking for a way to interact with your **Raspberry Pi** in a more friendly way.  The same for shown as on Pi (roughly the same)

![raspberry pi everything demo](https://user-images.githubusercontent.com/13696193/44279694-5b58ce80-a220-11e8-9ab6-d6021f5a944f.jpg)

In addition to a primary GUI, you can add a Progress Meter to your code with ONE LINE of code.  Slide this line into any of your `for` loops and get a nice meter:


```python
OneLineProgressMeter('My meter title', current_value, max value, 'key')
```

![easyprogressmeter](https://user-images.githubusercontent.com/13696193/44960065-83099100-aec6-11e8-8aa8-96e4b100a0e4.jpg)

It's simple to show animated GIFs.

![loading animation](https://user-images.githubusercontent.com/13696193/51280871-d2041e80-19ae-11e9-8757-802eb95352ed.gif)

How about embedding a game inside of a GUI?  This game of Pong is written in tkinter and then dropped into the PySimpleGUI window creating a game that has an accompanying GUI.

![pong](https://user-images.githubusercontent.com/13696193/45860012-2d8d0b00-bd33-11e8-9efd-3eaf4c30f324.gif)

Combining PySimpleGUI with PyInstaller creates something truly remarkable and special, a Python program that looks like a Windows WinForms application.  This application with working menu was created in 20 lines of Python code.  It is a single .EXE file that launches straight into the screen you see.  And more good news, the only icon you see on the taskbar is the window itself... there is no pesky shell window.

![menu demo](https://user-images.githubusercontent.com/13696193/45923097-8fbc4c00-beaa-11e8-87d2-01a5331811c8.gif)


## Background
I was frustrated by having to deal with the dos prompt when I had a powerful Windows machine right in front of me.  Why is it SO difficult to do even the simplest of input/output to a window in Python??

There are a number of 'easy to use' Python GUIs, but they were too limited for my requirements.  PySimpleGUI aims for the same simplicity found in packages like `EasyGUI`and `WxSimpleGUI` , both really handy but limited, and adds the ability to define your own layouts.   This ability to make your own windows using a large palette of widgets is but one difference  between the existing "simple" packages and `PySimpleGUI`.

With a simple GUI, it becomes practical to "associate" .py files with the python interpreter on Windows.  Double click a py file and up pops a GUI window, a more pleasant experience than opening a dos Window and typing a command line.

The `PySimpleGUI` package is focused on the ***developer***.
> Create a custom GUI with as little and as simple code as possible.

This was the primary focus used to create PySimpleGUI.

> "Do it in a Python-like way"

was the second.

## Features

While simple to use, PySimpleGUI has significant depth to be explored by more advanced programmers.  The feature set goes way beyond the requirements of a beginner programmer, and into the  required features needed for complex GUIs.

Features of PySimpleGUI include:
- Support for Python versions 2.7 and 3
- Text
- Single Line Input
- Buttons including these types:
	- File Browse
	- Files Browse
	- Folder Browse
	- SaveAs
	- Non-closing return
	- Close window
	- Realtime
	- Calendar chooser
	- Color chooser
	- Button Menu
- Checkboxes
- Radio Buttons
- Listbox
- Option Menu
- Menubar
- Button Menu
- Slider
- Dial
- Graph
- Frame with title
- Icons
- Multi-line Text Input
- Scroll-able Output
- Images
- Tables
- Trees
- Progress Bar            Async/Non-Blocking Windows
- Tabbed windows
- Paned windows
- Persistent Windows
- Redirect Python Output/Errors to scrolling window
- 'Higher level' APIs (e.g. MessageBox, YesNobox, ...)
- Single-Line-Of-Code Proress Bar & Debug Print
- Complete control of colors, look and feel
- Selection of pre-defined palettes
- Button images
- Horizontal and Verticle Separators
- Return values as dictionary
- Set focus
- Bind return key to buttons
- Group widgets into a column and place into window anywhere
- Scrollable columns
- Keyboard low-level key capture
- Mouse scroll-wheel support
- Get Listbox values as they are selected
- Get slider, spinner, combo as they are changed
- Update elements in a live window
- Bulk window-fill operation
- Save / Load window to/from disk
- Borderless (no titlebar) windows
- Always on top windows
- Menus with ALT-hotkey
- Right click pop-up menu
- Tooltips
- Clickable links
- Transparent windows
- Movable windows
- Animated GIFs
- No async programming required (no callbacks to worry about)

An example of many widgets used on a single window.  A little further down you'll find the 21 lines of code required to create this complex window.  Try it if you don't believe it.  Install PySimpleGUI then :

Start Python, copy and paste the code below into the >>> prompt and hit enter. This will pop up...

![everything example](https://user-images.githubusercontent.com/13696193/43097412-0a4652aa-8e8a-11e8-8e09-939484e3c568.jpg)

```python
import PySimpleGUI as sg

layout = [[sg.Text('All graphic widgets in one window!', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
	[sg.Text('Here is some text.... and a place to enter text')],
	[sg.InputText()],
	[sg.Checkbox('My first checkbox!'), sg.Checkbox('My second checkbox!', default=True)],
	[sg.Radio('My first Radio!     ', "RADIO1", default=True), sg.Radio('My second Radio!', "RADIO1")],
	[sg.Multiline(default_text='This is the default Text shoulsd you decide not to type anything',)],
[sg.InputCombo(['Combobox 1', 'Combobox 2'], size=(20, 3)),
	sg.Slider(range=(1, 100), orientation='h', size=(35, 20), default_value=85)],
[sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(30, 6)),
	sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=25),
	sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=75),
	sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=10)],
[sg.Text('_'  * 100, size=(70, 1))],
[sg.Text('Choose Source and Destination Folders', size=(35, 1))],
[sg.Text('Source Folder', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Source'),
	sg.FolderBrowse()],
[sg.Text('Destination Folder', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Dest'),
	sg.FolderBrowse()],
[sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]

event, values  = sg.Window('Everything bagel', layout, auto_size_text=True, default_element_size=(40, 1)).Read()
```



---
### Design Goals

> Copy, Paste, Run.

`PySimpleGUI's` goal with the API is to be easy on the programmer, and to function in a Python-like way. Since GUIs are visual, it was desirable for the code to visually match what's on the screen.  By providing a significant amount of documentation and an easy to use Cookbook, it's possible to see your first GUI within 5 minutes of beginning the installation.

> Be Pythonic

Be Pythonic... Attempted to use language constructs in a natural way and to exploit some of Python's interesting features.  Python's lists and optional parameters make PySimpleGUI work smoothly.

- windows are represented as Python lists.
- A window is a list of rows
- A row is a list of elements
- Return values are a list of button presses and input values.
- Return values can also be represented as a dictionary
- The SDK calls collapse down into a single line of Python code that presents a custom GUI and returns values
-  Linear programming instead of callbacks

#### Lofty Goals

>  Change Python

The hope is not that ***this*** package will become part of the Python Standard Library.

The hope is that Python will become ***the*** go-to language for creating GUI programs that run on Windows, Mac, and Linux *for all levels of developer*.

The hope is that beginners that are interested in graphic design will have an easy way to express themselves, right from the start of their Python experience.

There is a noticeable gap in the Python GUI solution.  Fill that gap and who knows what will happen.

Maybe there's no "there there".  ***Or*** maybe a simple GUI API will enable Python to dominate yet another computing discipline like it has so many others.   This is my attempt to find out.


# Getting Started with PySimpleGUI

## Installing PySimpleGUI

### Installing  Python 3

`pip install --upgrade PySimpleGUI`

On some systems you need to run pip3.

`pip3 install --upgrade PySimpleGUI`

On a Raspberry Pi, this is should work:

`sudo pip3 install --upgrade pysimplegui`

Some users have found that upgrading required using an extra flag on the pip `--no-cache-dir`.

`pip install --upgrade --no-cache-dir`

On some versions of Linux you will need to first install pip.  Need the Chicken before you can get the Egg (get it... Egg?)

`sudo apt install python3-pip`

If for some reason you are unable to install using `pip`, don't worry, you can still import PySimpleGUI by downloading the file PySimleGUI.py and placing it in your folder along with the application that is importing it.

`tkinter` is a requirement for PySimpleGUI (the only requirement).  Some OS variants, such as Ubuntu, do not some with `tkinter` already installed.  If you get an error similar to:

`ImportError: No module named tkinter`

then you need to install `tkinter`.

For python 2.7

`sudo apt-get install python-tk`

For python 3
`sudo apt-get install python3-tk`

More information about installing tkinter can be found here: https://www.techinfected.net/2015/09/how-to-install-and-use-tkinter-in-ubuntu-debian-linux-mint.html


### Installing for Python 2.7

`pip install --upgrade PySimpleGUI27`
or
`pip2 install --upgrade PySimpleGUI27`

You may need to also install "future" for version 2.7

`pip install future`
or
`pip2 install future`

Python 2.7 support is relatively new and the bugs are still being worked out.  I'm unsure what may need to be done to install tkinter for Python 2.7.  Will update this readme when more info is available

Like above, you may have to install either pip or tkinter.  To do this on Python 2.7:

`sudo apt install python-pip`

`sudo apt install python-tkinter`

### Testing your installation

Once you have installed, or copied the .py file to your app folder, you can test the installation using python.  At the command prompt start up Python.

#### Instructions for Python 2.7:
```python
>>> import PySimpleGUI27
>>> PySimpleGUI27.main()
```

#### Instructions for Python 3:

```python3
>>> import PySimpleGUI
>>> PySimpleGUI.main()
```

You will see a sample window in the center of your screen.  If it's not installed correctly you are likely to get an error message during one of those commands

Here is the window you should see:

![sample window](https://user-images.githubusercontent.com/13696193/46097669-79efa500-c190-11e8-885c-e5d4d5d09ea6.jpg)



### Prerequisites
Python 2.7 or Python 3
tkinter

PySimpleGUI Runs on all Python3 platforms that have tkinter running on them.  It has been tested on Windows, Mac, Linux, Raspberry Pi.  Even runs on `pypy3`.

### EXE file creation

If you wish to create an EXE from your PySimpleGUI application, you will need to install `PyInstaller`.  There are instructions on how to create an EXE at the bottom of this ReadMe


## Using  - Python 3

To use in your code, simply import....
`import PySimpleGUI as sg`

Then use either "high level" API calls or build your own windows.

`sg.Popup('This is my first Popup')`

![first popup](https://user-images.githubusercontent.com/13696193/44957300-c7813680-ae9e-11e8-9a8c-c70198db7907.jpg)


Yes, it's just that easy to have a window appear on the screen using Python.  With PySimpleGUI, making a custom window appear isn't much more difficult.  The goal is to get you running on your GUI within ***minutes***, not hours nor days.

## Using  - Python 2.7

Those using Python 2.7 will import a different module name
`import PySimpleGUI27 as sg`

## Code Samples Assume Python 3

While all of the code examples you will see in this Readme and the  Cookbook assume Python 3 and thus have an `import PySimpleGUI` at the top, you can run ***all*** of this code on Python 2.7 by changing the import statement to `import PySimpleGUI27`

---
# APIs

PySimpleGUI can be broken down into 2 types of API's:
* High Level single call functions    (The `Popup` calls)
* Custom window functions


### Python Language Features

There are a number of Python language features that PySimpleGUI utilizes heavily for API access that should be understood...
* Variable number of arguments to a function call
* Optional parameters to a function call
* Dictionaries

#### Variable Number of Arguments

The "High Level" API calls that *output* values take a variable number of arguments so that they match a "print" statement as much as possible.  The idea is to make it simple for the programmer to output as many items as desired and in any format.  The user need not convert the variables to be output into the strings.  The PySimpleGUI functions do that for the user.

sg.Popup('Variable number of parameters example', var1, var2, "etc")

Each new item begins on a new line in the Popup

![snap0179](https://user-images.githubusercontent.com/13696193/43658129-f6ca49c6-9725-11e8-9317-1f77443eb04a.jpg)


#### Optional Parameters to a Function Call

This feature of the Python language is utilized ***heavily*** as a method of customizing windows and window Elements.  Rather than requiring the programmer to specify every possible option for a widget, instead only the options the caller wants to override are specified.

Here is the function definition for the Popup function. The details aren't important.  What is important is seeing that there is a long list of potential tweaks that a caller can make.  However, they don't *have* to be specified on each and every call.

```python
def Popup(*args,
		   button_color=None,
		   button_type=MSG_BOX_OK,
		   auto_close=False,
		   auto_close_duration=None,
		   icon=DEFAULT_WINDOW_ICON,
		   line_width=MESSAGE_BOX_LINE_WIDTH,
		   font=None):
```

If the caller wanted to change the button color to be black on yellow, the call would look something like this:
`sg.Popup('This box has a custom button color', button_color=('black', 'yellow'))`

![snap0180](https://user-images.githubusercontent.com/13696193/43658171-13a72bfe-9726-11e8-8c7a-0a46e46fb202.jpg)

#### Dictionaries

Dictionaries are used by more advanced PySimpleGUI users.  You'll know that dictionaries are being used if you see a `key` parameter on any Element.  Dictionaries are used in 2 ways:
1. To identify values when a window is read
2. To identify Elements so that they can be "updated"

---

