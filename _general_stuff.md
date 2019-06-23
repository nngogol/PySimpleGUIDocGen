
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓



```
Listbox(values
        default_values=None
        select_mode=None
        change_submits=False
        bind_return_key=False
        size=(None, None)
        disabled = False,
        auto_size_text=None
        font=None
        background_color=None
        text_color=None
        key=None
        pad=None
        right_click_menu=None
        tooltip=None,
        visible=True):
```


- values - Choices to be displayed. List of strings
- select_mode - Defines how to list is to operate.
        - Choices include constants or strings:
                - Constants version:
                        - LISTBOX_SELECT_MODE_BROWSE
                        - LISTBOX_SELECT_MODE_EXTENDED
                        - LISTBOX_SELECT_MODE_MULTIPLE
                        - LISTBOX_SELECT_MODE_SINGLE - the default
                - Strings version:
                        - 'browse'
                        - 'extended'
                        - 'multiple'
                        - 'single'
- change_submits - if True, the window read will return with a button value of ''
- bind_return_key - if the focus is on the listbox and the user presses return key, or if the user double clicks an item, then the read will return
- size - (width, height) of element in characters
- disapled - Bool. If True element is disabled
- auto_size_text - Bool. True if size should fit the text length
- background_color - color to use for the input field background
- font - font to use for items in list
- text_color - color to use for the typed text
- key - Dictionary key to use for return values and to find element
- pad - amount of padding to use when packing
- tooltip - tooltip text



▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓




```python
Multiline(default_text='',
        enter_submits=False,
        disabled=False,
        autoscroll=False,
        size=(None, None),
        auto_size_text=None,
        background_color=None,
        text_color=None,
        change_submits=False,
        enable_events=False,
        do_not_clear=False,
        key=None,
        focus=False,
        font=None,
        pad=None,
        tooltip=None
        right_click_menu=None,
        visible=True)
```
|name|meaning|
|-|-|
| default_text | Text to display in the text box      |
| change_submits | Bool. If True, pressing Enter key submits window |
| anable_events | Bool. same as change_submits|
| autoscroll | Bool.  Causes "cursor" to always be at the end of the text   |
| size | Element's size  |
| right_click_menu | menu definition to displat if right clicked    |
| auto_size_text | Bool. Change width to match size of text      |
||| 


▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓



```python
Tree(   data=None,
        headings=None,
        visible_column_map=None,
        col_widths=None,
        col0_width=10,
        def_col_width=10,
        auto_size_columns=True,
        max_col_width=20,
        select_mode=None,
        show_expanded=False,
        change_submits=False,
        enable_events=False,
        font=None,
        justification='right',
        text_color=None,
        background_color=None,
        num_rows=None,
        row_height=None,
        pad=None,
        key=None,
        tooltip=None,
        right_click_menu=None,
        visible=True)
```
```
class Tree(data=None - data in TreeData format
         headings=None - list of strings representing your headings
         visible_column_map=None - list of bools indicating which columns to display
         col_widths=None - list of column widths
         col0_width=10 - width of the first column which has the text data
         def_col_width=10 - default column width
         auto_size_columns=True - if true will autosize columns (currenly only sizes to col heading width)
         max_col_width=20 - max width for columns in characters
         select_mode=None - not yet used
         show_expanded - Bool - if True the tree will be fully expanded when shown
         font=None - the display font
         justification='right' - justification for data display
         text_color=None- color of text to display
         background_color=None - background color
         num_rows=None - number of rows to display
         row_height=None - height of rows in pixels
         pad=None - element padding
         key=None - key for element
         tooltip=None - tooltip
```


 


▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

```python
Table(  values,
        headings=None,
        visible_column_map=None,
        col_widths=None,
        def_col_width=10,
        auto_size_columns=True,
        max_col_width=20,
        select_mode=None,
        display_row_numbers=False,
        num_rows=None,
        row_height=None,
        font=None,
        justification='right',
        text_color=None,
        background_color=None,
        alternating_row_color=None,
        row_colors=None,
        vertical_scroll_only=True,
        size=(None,None),
        change_submits=False,
        enable_events=False,
        bind_return_key=False,
        pad=None,
        key=None,
        tooltip=None,
        right_click_menu=None,
        visible=True):

```

values - Your table's array
headings - list of strings representing your headings, if you have any
visible_column_map - list of bools. If True, column in that position is shown.  Defaults to all columns
col_widths - list of column widths
def_col_width - default column width. defaults to 10
auto_size_columns - bool. If True column widths are determined by table contents
max_col_width - maximum width of a column. defaults to 25
select_mode - table rows can be selected, but doesn't currently do anything
display_row_numbers - bool. If True shows numbers next to rows
num_rows = the number of rows to display at a time (same as size[0])
row_height = number of pixels high a row should be. Normally left as default value
font - font for table entries
justification - left, right, center
text_color - color of text
alternating row color - if set will change background color for alternating rows
row_colors - list of tuples representing (row_number, color) e.g. row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
vertical_scroll_only - if True will not show a horizontal scrollbar.   NOTE - will have to disable to get horizontal scrollbars
background_color - cell background color
size - (None, number of rows) - don't use, use num_rows instead
enable_events - will return a 'row selected' event when row is selected
change_submits - the old way of indicating enable_events
bind_return_key - returns event if a double click or a return key is pressed while row is highlighted
pad - element padding for packing
key - key used to lookup element
tooltip - tooltip text


```python
def Update(self, values=None):
```
`values` is a table containing your rows just like you passed in when creating the Table Element.

