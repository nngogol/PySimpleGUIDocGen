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

# from docutils.core import publish_string
from inspect import getmembers, isfunction, isclass, getsource, signature, _empty
from db import PySimpleGUIlib
from datetime import datetime; import json
import re

def get_params_part(code:str) -> dict:
	"""
	Find ":param " part in given "doc string"

	from __doc__ to {
		'parameter' :  'desctiption',
		'parameter2' : 'desctiption2',
		'parameter3' : 'desctiption3',
	}
	"""
	only_params = code[code.index(':param'):] # get_only_params_string(code)

	# ■■■■ making dict
	param_lines = only_params.split(':param ')
	param_lines = [i.strip() for i in param_lines if i.strip()] # filter empty lines

	args_kwargs_pairs = {}
	for index, i in enumerate(param_lines):
		
		cols = i.split(':')
		param_name, els = cols[0], '\n'.join([j.strip() for j in ':'.join(cols[1:]).split('\n')])
		# param_name, els = cols[0],  ' '.join([j.strip() for j in ':'.join(cols).split('\n')]) # can be this:
		
		param_name, els = param_name.strip(), els.strip()
		args_kwargs_pairs[param_name] = els
	return args_kwargs_pairs

def method_to_md(class_obj, method_name):
	"""
	Convert class method DOC string to MARKDOWN: method call + params table
	"""

	method 				= getattr(class_obj, method_name)
	method_doc_string 	= method.__doc__.strip()

	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ▒   ▒ 		   Making INIT_CALL   		 ▒   ▒ #
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# where the magic begins
	sig, rows = signature(method).parameters, []
	for index, key in enumerate(sig):
		val = sig[key].default
		if 'self' == str(key): 		continue
		if val == _empty: 			rows.append(key)
		elif val == None: 			rows.append(f'{key}=None')
		elif type(val) is int: 		rows.append(f'{key}={val}')
		elif type(val) is str: 		rows.append(f'{key}="{val}"')
		elif type(val) is tuple: 	rows.append(f'{key}={val}')
		elif type(val) is bool: 	rows.append(f'{key}={val}')
		else:
			raise Exception(f'IDK this type -> {key, val}')

	# where the magic stops
	ff = ',\n\t'

	# replace __init__ to "REAL class name"
	if method_name == '__init__': method_name = class_obj.__name__
	METHOD_SIGNATURE = f"```python\n{method_name}({ff.join(rows)})\n```"
	# where the magic stops, for real.



	# --------------
	# RETURN SPECIAL
	# --------------
	params_names = list(dict(sig).keys())
	if 'self' in params_names and params_names[0] == params_names[-1] and not method_doc_string:
		"""
		def Get(self):
			''' '''
		
		->
		Get() <br>
		"""
		return f'\n<br>\n{method_name}()<br>\n\n'
	if 'self' in params_names and params_names[0] == params_names[-1] and method_doc_string and ':param' not in method_doc_string:
		"""
		def Get(self):
			''' bla bla'''
		
		->
		Get() - bla bla <br>
		"""
		return f'\n<br>\n{method_name}() - {method_doc_string}<br>\n\n'

	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ▒   ▒- 		Making params_TABLE			 ▒   ▒-#
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	md_table =  '\n'.join([ 	f'|{name}|{desc}|'
								for name, desc in
								get_params_part(method_doc_string).items()])
	params_TABLE = f'''\n Parameters explained:\n
						|Name|Meaning|
						|-|-|
						{md_table}
						|||
						'''.replace('\t', '')
	
	if not md_table.strip():
		params_TABLE = ''

	return f'''\n{METHOD_SIGNATURE}\n\n{params_TABLE}\n\n'''


def make_md_parts(psg_classes, class_name:str, logger=None, READMEFILE='') -> list:
	"""
	Convert "class_name" to list of "from and to" parts to replace in 2_readme.md
	"""

	# find class object
	target_class = [i for i in psg_classes if i[0] == class_name]
	if not target_class:
		raise Exception(f'ERROR, not found {class_name}')
	if len(target_class) != 1:
		raise Exception(f'ERROR, found multiply items, named "{class_name}"')

	# take class object
	class_object = target_class[0][1]
	class_object_doc = class_object.__doc__.replace('\n    ', '\n').strip()

	# regex all target tags, like <+X+>
	methods_regex = re.compile(r'<\+' + class_name + r'\.(\w+)\+>')
	methods = [i.group(1) for i in re.finditer(methods_regex, READMEFILE)]
	special_methods = ['doc']

	def format_my_tag(my_class_name, method_name):
		# <!-- <+Text.doc+> -->
		return f'<!-- <+{my_class_name}.{method_name}+> -->'
		# <+Text.doc+>
		# return f'<+{class_name}.{method_name}+>'

	# methods_dict = { f'<+{class_name}.{method_name}+>': method_to_md(class_object, method_name) for method_name in methods if method_name not in special_methods}
	methods_dict = {}
	for method_name in methods:
		if method_name not in special_methods:
			# if 'Listbox' == class_name:
				
			key = format_my_tag(class_name, method_name)
			val = method_to_md(class_object, method_name)
			methods_dict[key] = val

	# append class doc string
	methods_dict[f'<!-- <+{class_name}.doc+> -->'] = class_object_doc
	if class_object_doc == '':
		logger.warning(f'Warning, "{class_name}.__doc__" == ""')

	return methods_dict

def make_md_parts_func(psg_funcs, func_name:str, logger=None, READMEFILE='') -> list:
	"""
	Convert "func_name" to "md content" to replace in 2_readme.md
	"""

	# find class object
	target_class = [i for i in psg_funcs if i[0] == func_name]
	if not target_class:
		raise Exception(f'ERROR, not found {func_name}')
	if len(target_class) != 1:
		raise Exception(f'ERROR, found multiply items, named "{class_name}"')

	# take class object
	class_object = target_class[0][1]
	class_object_doc = class_object.__doc__.replace('\n    ', '\n').strip()

	# regex all target tags, like <+X+>
	methods_regex = re.compile(r'<\+' + class_name + r'\.(\w+)\+>')
	methods = [i.group(1) for i in re.finditer(methods_regex, READMEFILE)]
	special_methods = ['doc']

	def format_my_tag(my_class_name, method_name):
		# <!-- <+Text.doc+> -->
		return f'<!-- <+{my_class_name}.{method_name}+> -->'
		# <+Text.doc+>
		# return f'<+{class_name}.{method_name}+>'

	# methods_dict = { f'<+{class_name}.{method_name}+>': method_to_md(class_object, method_name) for method_name in methods if method_name not in special_methods}
	methods_dict = {}
	for method_name in methods:
		if method_name not in special_methods:
			# if 'Listbox' == class_name:
				
			key = format_my_tag(class_name, method_name)
			val = method_to_md(class_object, method_name)
			methods_dict[key] = val

	# append class doc string
	methods_dict[f'<!-- <+{class_name}.doc+> -->'] = class_object_doc
	if class_object_doc == '':
		logger.warning(f'Warning, "{class_name}.__doc__" == ""')

	return methods_dict

def main(do_full_readme=False, files_to_include:list=[], logger=None, output_name=None):
	if logger == None:
		raise Exception('give me a logger')

	def readfile(fname):
		with open(fname, 'r', encoding='utf-8') as ff:
			return ff.read()

	HEADER_top_part 		= readfile('db/1_HEADER_top_part.md') 			# 1
	readme 					= readfile('db/2_readme.md') 					# 2
	FOOTER 					= readfile('db/3_FOOTER.md') 					# 3
	Release_notes 			= readfile('db/4_Release_notes.md') 			# 4

	common_element_kwargs = 'tooltip size colors pad font key visible'.split(' ')
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	#  ■ ■   magic start here   ■ ■
	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# memes - is classes, funcions, varialbe
	psg_classes_funcs_variables = getmembers(PySimpleGUIlib)
	psg_funcs 		= [o for o in psg_classes_funcs_variables if isfunction(o[1])]
	psg_classes 	= [o for o in psg_classes_funcs_variables if isclass(o[1])]
	# filter repeated classes
	psg_classes_	 = list(set([i[1] for i in psg_classes]))
	psg_classes		= list(zip([i.__name__ for i in psg_classes_], psg_classes_))


	# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
	# ■■■■                       | |	■■■■■
	# ■■■■   _ __ ___   ___  __ _| |_	■■■■■
	# ■■■■  | '_ ` _ \ / _ \/ _` | __|	■■■■■
	# ■■■■  | | | | | |  __/ (_| | |_  	■■■■■
	# ■■■■  |_| |_| |_|\___|\__,_|\__|	■■■■■
	# mark_points = [i.strip()[7:-6].strip() for i in readme.split('\n') if '<!-- <+' in i]
	# mark_points = [i for i in mark_points if ' ' not in i]  # filter these -> "<+X Y+>"
	# mark_points = ['Text'] # dummy test


	# ••• preprocess •••
	started_mark = '<!-- Start from here -->'
	readme = readme[readme.index(started_mark)+len(started_mark):]

	regex_pattern = re.compile(r'<!-- <\+[a-zA-Z_]+\.([a-zA-Z_]+)\+> -->')
	mark_points = [i for i in readme.split('\n') if regex_pattern.match(i)]

	if len(list(set(mark_points))) != len(mark_points):
		[mark_points.remove(x) for x in set(mark_points)]
		repeated = ','.join(mark_points)
		logger.error("You have repeated tags! \n {0}".format(repeated))
		return ''

	# functions
	# mark_points_funcs = [i for i in mark_points if 'func'in i]
	# done_funcs = []
	# for func_name_tag in mark_points_funcs:
	# 	try:
	# 		func_name = func_name_tag.split('.')[1].split('+')[1]
	# 		if func_name in done_funcs:
	# 			continue
	# 		done_funcs.append(func_name)

	# 		md_parts = make_md_parts_func(psg_funcs, func_name=func_name, READMEFILE=readme, logger=logger)
	# 		for from_, to_ in md_parts.items():
	# 			if from_ == 'doc':
	# 				continue

	# 			if from_ in readme:
	# 				readme = readme.replace(from_, to_)
	# 			else:
	# 				logger.warning(f"CAN'T replace '{from_}'")
	# 	except Exception as e:
	# 		logger.error(str(e))

	# classes
	mark_points_classes = [i for i in mark_points if 'func' not in i]
	done_classes = []
	for class_name_tag in mark_points_classes:
		try:
			class_name = class_name_tag.split('.')[0].split('+')[1]
			if class_name in done_classes:
				continue
			done_classes.append(class_name)
			md_parts = make_md_parts(psg_classes, class_name=class_name, READMEFILE=readme, logger=logger)
			for from_, to_ in md_parts.items():
				if from_ == 'doc':
					continue

				if from_ in readme:
					readme = readme.replace(from_, to_)
				else:
					logger.warning(f"CAN'T replace '{from_}'")

				# readme = readme.replace(f'<!-- {from_} -->', to_)
			# readme = readme.replace(f'<!-- <+{class_name}+> -->', md_class)
		except Exception as e:
			logger.error(str(e))

	# ■■■■■■■■■■■■■■■■■
	#  ■ ■ ■ join ■ ■ ■
	# ■■■■■■■■■■■■■■■■■
	files = []
	if 0 in files_to_include: files.append(HEADER_top_part)
	if 1 in files_to_include: files.append(readme)
	if 2 in files_to_include: files.append(FOOTER)
	if 3 in files_to_include: files.append(Release_notes)
	Joined_MARKDOWN = '\n\n'.join(files) if do_full_readme or files else readme

	if output_name:
		with open(output_name, 'w', encoding='utf-8') as ff:
			curr_dt = datetime.today().strftime('<!-- CREATED: %Y-%m-%d %H.%M.%S -->\n') 
			content = curr_dt + Joined_MARKDOWN
			ff.write(content)

	return content


if __name__ == '__main__':
	import logging

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	my_file = logging.FileHandler('example.log'); my_file.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(levelname)s: \t%(message)s')
	# formatter = logging.Formatter('%(asctime)s>%(levelname)s: %(message)s')
	my_file.setFormatter(formatter)
	logger.addHandler(my_file)
	
	logger.debug('STARTING \n\n')
	main(logger=logger, files_to_include=[0,1,2,3,4], output_name="TEST.readme.md")