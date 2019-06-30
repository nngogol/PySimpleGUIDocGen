#!/usr/bin/python3
import sys, types, datetime, time, pickle, calendar, textwrap, operator, inspect
from random import randint

if sys.version_info[0] >= 3:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter.colorchooser import askcolor
    from tkinter import ttk
    import tkinter.scrolledtext as tkst
    import tkinter.font
else:
    import Tkinter as tk
    import tkFileDialog
    import ttk
    import tkColorChooser
    import tkFont
    import ScrolledText


class Element():
    """The base class for all Elements.
    Holds the basic description of an Element like size and colors


    """
    def __init__(self, type, size=(None, None), auto_size_text=None, font=None, background_color=None, text_color=None, key=None, pad=None, tooltip=None, visible=True):
        """

        :param type: ??????????????????????????
        :param size: ▲ (w,h) w=characters-wide, h=rows-high 
        :param auto_size_text: True if size should fit the text length 
        :param font: ▲ specifies the font family, size, etc 
        :param background_color: color of background 
        :param text_color: element's text color 
        :param key: ▲ Used with window.FindElement and with return values 
        :param pad: ▲ Amount of padding to put around element 
        :param tooltip: text, that will appear the you hover on 
        :param visible: set visibility state of the element (Default = True)

        """
        pass

    def _FindReturnKeyBoundButton(self, form):
        """

        :param form: 

        """
        return None

    def SetTooltip(self, tooltip_text):
        """

        :param tooltip_text: 

        """
        self.TooltipObject = ToolTip(self.Widget, text=tooltip_text, timeout=DEFAULT_TOOLTIP_TIME)


class InputText(Element):
    """Shows a single line of input."""

    def __init__(self, default_text='', size=(None, None), visible=True):
        """

        :param default_text: Text initially shown in the input box (Default value = '')
        :param size: ▲ (w,h) w=characters-wide, h=rows-high 
        :param visible: set visibility state of the element (Default = True)
        """
        
        self.TKEntry = self.Widget = None          # type: tk.Entry
        super().__init__(ELEM_TYPE_INPUT_TEXT)

    # =========================
    def method11(self, alice=None, bob=None):
        """"""
        pass
    def method12(self):
        """"""
        pass
    # =========================
    def method21(self, alice=None, bob=None):
        """hello world"""
        pass
    def method22(self):
        """hello world"""
        pass
    # =========================
    def method31(self, alice=None, bob=None):
        """hello world

        :param alice:   test1
        :param bob:     test2
        """
        pass
    def method32(self, alice=None, bob=None):
        """hello world

        :param alice:   test1
        :param bob:     test2
        :return:  ABC!!!222
        """
        pass
    
    def method33(self, alice=None, bob=None):
        """hello world

        :return:  ABC!!!222
        """
        pass
    def method34(self, alice=None, bob=None):
        """
        :return:  ABC!!!222
        """
        pass
    def method35(self):
        """

        :return:  ABC!!!222
        """
        pass
    
    def method36(self):
        """hello world

        :return:  ABC!!!222
        """
        pass
    # =========================
