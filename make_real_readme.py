'''
	structure of project

	make_real_readme.md
		◄-> magic
	_readme.md
		◄-> boilerplate to insert the code


	HEADER_top_part.md
		◄-> header
	FOOTER.md
		◄-> footer
'''


'''
	## Text Element
	## Multiline Text Element
	## Output Element
	## Combo Element
	## Listbox Element
	## Slider Element
	## Radio Button Element
	## Checkbox Element
	## Spin Element
	## Image Element
	## Button Element
	## ButtonMenu Element
	## Vertical Separator Element
	## ProgressBar  Element
	## Column Element
	## Canvas Element
	## Graph Element
	## Table Element
	## Tree Element
	## Pane Element
'''

import json
# from docutils.core import publish_string
from inspect import getmembers, isfunction, isclass, getsource, signature, _empty
from db import PySimpleGUIlib
from datetime import datetime

def readfile(fname):
	with open(fname, 'r', encoding='utf-8') as ff:
		return ff.read()

HEADER_top_part 		= readfile('db/1_HEADER_top_part.md') 			# 1
readme 					= readfile('db/2_readme.md') 					# 2
FOOTER 					= readfile('db/3_FOOTER.md') 					# 3
Release_notes 			= readfile('db/4_Release_notes.md') 			# 4


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
#  ■ ■   magic start here   ■ ■
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

psg_memes = getmembers(PySimpleGUIlib) # memes - is classes, funcions, varialbe
psg_funcs 		= [o for o in psg_memes if isfunction(o[1])]
psg_classes 	= [o for o in psg_memes if isclass(o[1])]

# filter repeated classes
psg_classes_						 = list(set([i[1] for i in psg_classes]))
psg_classes		= list(zip([i.__name__ for i in psg_classes_], psg_classes_))

# with open('common_element_kwargs.json', 'r', encoding='utf-8') as f:
# 	common_element_kwargs = json.load(f)

def get_params_part(code:str) -> dict:
	'''
	from __doc__ to {
		'parameter' :  'desctiption',
		'parameter2' : 'desctiption2',
		'parameter3' : 'desctiption3',
	}
	'''
	only_params = code[code.index(':param'):] # get_only_params_string(code)

	# ■■■■ making dict
	param_lines = only_params.split(':param ')
	param_lines = [i.strip() for i in param_lines if i.strip()] # filter empty lines

	args_kwargs_pairs = {}
	# import pdb; pdb.set_trace();
	for index, i in enumerate(param_lines):
		
		cols = i.split(':')
		param_name, els = cols[0], '\n'.join([j.strip() for j in ':'.join(cols[1:]).split('\n')])
		# param_name, els = cols[0],  ' '.join([j.strip() for j in ':'.join(cols).split('\n')]) # can be this:
		
		param_name, els = param_name.strip(), els.strip()
		args_kwargs_pairs[param_name] = els
	return args_kwargs_pairs

def meme_class(class_name:str, methods:list=[]) -> str:
	# Convert "class_name" to proper MARKDOWN string perpesentation

	# find class object
	target_class = [i for i in psg_classes if i[0] == class_name]
	if not target_class:
		raise Exception(f'ERROR, not found {class_name}')
	if len(target_class) != 1:
		raise Exception(f'ERROR, found multiply items, named "{class_name}"')


	class_object = target_class[0][1]
	CLASS_DOC_STRING = class_object.__doc__
	init__doc_string = class_object.__init__.__doc__
	if CLASS_DOC_STRING == '':
		print(f'Warning, class "doc string" for "{class_name}" is empty')
	if init__doc_string == None:
		raise Exception(f'ERROR, no __init__  "doc string" in "{class_name}"')


	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# strip_4_spaces
	# CLASS_DOC_STRING = '\n'.join([i[4:] for i in CLASS_DOC_STRING.split('\n')])
	CLASS_DOC_STRING = CLASS_DOC_STRING.replace('\n    ', '\n')

	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ▒   ▒ 		   Making INIT_CALL   		 ▒   ▒ #
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	sig, rows = signature(class_object.__init__).parameters, []
	for index, key in enumerate(sig):
		val = sig[key].default
		if 'self' == str(key):
			continue
		if val == _empty: 			rows.append(key)
		elif val == None: 			rows.append(f'{key}=None')
		elif type(val) is int: 		rows.append(f'{key}={val}')
		elif type(val) is str: 		rows.append(f'{key}="{val}"')
		elif type(val) is tuple: 	rows.append(f'{key}={val}')
		elif type(val) is bool: 	rows.append(f'{key}={val}')
		else:
			raise Exception(f'IDK this type -> {key, val}')
	ff = ',\n\t'
	INIT_CALL = f"```python\n{class_name}({ff.join(rows)})\n```"
	
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ▒   ▒- Making params_TABLE ▒   ▒-#
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	md_table =  '\n'.join([ 	f'| {name} | {desc} |'
								for name, desc in
								get_params_part(init__doc_string).items()])
	params_TABLE = f'''Parameters explained:\n\n|Name|Meaning|
	|-|-|
	{md_table}
	|||\n'''.replace('\t', '')


	# ◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙◙
	return f'''{CLASS_DOC_STRING}\n\n{INIT_CALL}\n\n{params_TABLE}'''

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# ■■■■                       | |	■■■■■
# ■■■■   _ __ ___   ___  __ _| |_	■■■■■
# ■■■■  | '_ ` _ \ / _ \/ _` | __|	■■■■■
# ■■■■  | | | | | |  __/ (_| | |_gg	■■■■■
# ■■■■  |_| |_| |_|\___|\__,_|\__|	■■■■■

# ••• preprocess •••
started_mark = '<!-- Start from here -->'
readme = readme[readme.index(started_mark)+len(started_mark):]



# For example: <!-- <+Text+> -->
mark_points = [i.strip()[7:-6].strip() for i in readme.split('\n') if '<!-- <+' in i]
mark_points = [i for i in mark_points if ' ' not in i] # filter tags with space in them, like "<+Text methods+>"
# mark_points = ['Text']

for class_name in mark_points:
	try:
		md_class = meme_class(class_name)
		if not md_class:
			continue
		readme = readme.replace(f'<!-- <+{class_name}+> -->', md_class)
	except Exception as e:
		print(str(e))



# ■■■■■■■■■■■■■■■■■
#  ■ ■ ■ join ■ ■ ■
# ■■■■■■■■■■■■■■■■■

# ▼▼▼ FULL ▼▼▼
Joined_MARKDOWN = '\n\n'.join([HEADER_top_part, readme, FOOTER, Release_notes])
# ▼▼▼ debug mode ▼▼▼
# Joined_MARKDOWN = readme

with open('<<FINAL readme.md', 'w', encoding='utf-8') as ff:
	curr_dt = datetime.today().strftime(' <!-- CREATED: %Y-%m-%d %H.%M -->\n\n') 
	content = curr_dt + Joined_MARKDOWN
	ff.write(content)
