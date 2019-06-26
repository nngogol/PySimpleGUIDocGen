
![pysimplegui_logo](https://user-images.githubusercontent.com/13696193/43165867-fe02e3b2-8f62-11e8-9fd0-cc7c86b11772.png)

![Downloads](http://pepy.tech/badge/pysimpleguiwx)

![Awesome Meter](https://img.shields.io/badge/Awesome_meter-1000-yellow.svg)

![Python Version](https://img.shields.io/badge/Python-3.x-yellow.svg)

![Python Version](https://img.shields.io/badge/PySimpleGUIWx_For_Python_3.x_Version-0..0-orange.svg?longCache=true&style=for-the-badge)



# PySimpleGUIWx

The WxPython port of PySimpleGUI

## Primary PySimpleGUI Documentation

To get instructions on how use PySimpleGUI's APIs, please reference the [main documentation](http://www.PySimpleGUI.org).
This Readme is for information ***specific to*** the WxPython port of PySimpleGUI.


## Why Use PySimpleGUIWx Over The Other Ports?

PySimpleGUIWx brings the number of PySimpleGUI ports to 3.

Why use PySimpleGUIWx over PySimpleGUIQt PySimpleGUI (tkinter version)?

There are a couple of easy reasons to use PySimpleGUIWx over PySimpleGUIQt.

One is __footprint__. Using `PyInstaller EXE`, we get this:

|PySimpleGUI Version | Size of EXE|
|---|---|
|PySimpleGUIWx | 9 MB |
|PySimpleGUIQt | 240 MB |

Another is __cool widgets__.

WxPython has some nice advanced widgets that will be offered though PySimpleGUIWx, hopefully sooner than later.

The System Tray feature works well with a feature set identical to PySimpleGUIQt.  If you are looking for a System Tray feature, PySimpleGUIWx is recommended over PySimpleGUIQt; the primary reason being size of the WxPython framework versus the size of Qt. They both give you very similar features. They look and behave in an ***identical*** fashion when using PySimpleGUI. That's the beauty of the PSG SDK, the function calls are the same for all implementations of PySimpleGUI.  The source code is highly portable between the GUI frameworks.

This simple list is another way of looking at the question....

1. It's simple and easy to program GUIs
2. You can move between the GUI frameworks tkinter, Qt and WxPython by changing a single line of code, the import statement.
3. Get the same custom layout and access to the same widgets but in a simple, easy to use and understand interface.
4. It's fun to program GUIs again


## Engineering Pre-Release   Version 0.7.0

[Announcements of Latest Developments](https://github.com/MikeTheWatchGuy/PySimpleGUI/issues/142)

Having trouble? Visit the [GitHub site ](http://www.PySimpleGUI.com) and log an Issue.

