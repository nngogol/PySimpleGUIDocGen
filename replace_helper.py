general_data = [
	{
		"0": ":  (Default value",
		"1": ":                     (Default value"
	},{
		"0": "click_submits:  (Default value = ",
		"1": "click_submits: if clicked will trigger `Call()` (Default value = "
	},{
		"0": ":param key: ",
		"1": ":param key: (common_key) Used with window.FindElement and with return values "
	},{
		"0": ":param enable_events: ",
		"1": ":param enable_events: (common_key) Turns on the element specific events.(Default value = False) "
	},{
		"0": ":param visible:  (Default value = True)",
		"1": ":param visible: set visibility state of the element (Default value = True)"
	},{
		"0": ":param auto_size_text: ",
		"1": ":param auto_size_text: True if size should fit the text length "
	},{
		"0": ":param background_color: ",
		"1": ":param background_color: color of background "
	},{
		"0": ":param change_submits: ",
		"1": ":param change_submits: If True, pressing Enter key submits window "
	},{
		"0": ":param size: ",
		"1": ":param size: (common_key) (w,h) w=characters-wide, h=rows-high "
	},{
		"0": ":param pad: ",
		"1": ":param pad: (common_key) Amount of padding to put around element "
	},{
		"0": ":param font: ",
		"1": ":param font: (common_key) specifies the font family, size, etc (Default value = None) "
	},{
		"0": ":param tooltip:  (Default value = None)",
		"1": ":param tooltip: text, that will appear the you hover on (Default value = None)"
	},{
		"0": ":param text_color:  (Default value = None)",
		"1": ":param text_color: element's text color (Default value = None)"
	},{
		"0": ":param readonly:  ",
		"1": ":param readonly:  make element readonly "
	},{
		"0": ":param disabled:  (Default value = False)",
		"1": ":param disabled: set disable state for element (Default value = False)"
	},{
		"0": ":param disabled:  (Default value = False)",
		"1": ":param disabled: set disable state for element (Default value = False)"
	},{
		"0": ":param password_char: ",
		"1": ":param password_char: Passwork character if this is a password field"
	},{
		"0": ":param icon:  (Default value = DEFAULT_WINDOW_ICON)",
		"1": ":param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)"
	},{
		"0": ":param grab_anywhere:  (Default value = False)",
		"1": ":param grab_anywhere: If True can grab anywhere to move the window (Default value = False)"
	},{
		"0": ":param location:  (Default value = (None, None))",
		"1": ":param location: Location on screen to display (Default value = (None, None))"
	},{
		"0": ":param line_width:  (Default value = None)",
		"1": ":param line_width: Width of lines in characters (Default value = None)"
	},{
		"0": ":param text_color:  (Default value = None)",
		"1": ":param text_color: color of the text (Default value = None)"
	},{
		"0": ":param focus:  (Default value = False)",
		"1": ":param focus: if focus should be set to this (Default value = None)"
	},{
		"0": ":param justification:  (Default value = None)",
		"1": ":param justification: justification for data display (Default value = None)"
	},{
		"0": ":param do_not_clear:  (Default value = True)",
		"1": ":param do_not_clear: see docx (Default value = True)"
	},{
		"0": ":param right_click_menu:  (Default value = None)",
		"1": ':param right_click_menu: see "Right Click Menus" (Default value = None)'
	}
]
# ■■■■■■
# update

updates = [
	{
		"0": ":param disabled:  (Default value = None)",
		"1": ":param disabled: disable or enable state of the element (Default value = None)"
	},{
		"0": ":param visible:  (Default value = None)",
		"1": ":param visible:  change visibility of element (Default value = None)"
	}
]


def update_readme(content):
	for row in general_data:
		from_, to_ = row["0"], row["1"]
		content = content.replace(from_, to_)
	for row in updates:
		from_, to_ = row["0"], row["1"]
		content = content.replace(from_, to_)
	return content