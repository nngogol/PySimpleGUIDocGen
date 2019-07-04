
'''
PSG
->

"classes" : [
	{
		"classname": "inputtext",
		"methods": [
			{
				"name" : "...",
				"obj" : <func>
			},{
				"name" : "...",
				"obj" : <func>
			},{
				"name" : "...",
				"obj" : <func>
			},
		]
	},{
		"classname": "button",
		"methods": [
			{
				"name" : "...",
				"obj" : <func>
			},{
				"name" : "...",
				"obj" : <func>
			},{
				"name" : "...",
				"obj" : <func>
			},
		]
	},
]
"func" : [
	{
		"name" : "Popup",
		"obj" : <func>,
		"desc" : <func>,
		"params" : <func>,
		"return" : <func>,
	},
	{...},
	{...},
	{...}
]

'''

from inspect import getmembers, isfunction, isclass, signature
import PySimpleGUI, re

def get_params_part(code: str, name_=None, versbose=False) -> dict:
	"""
	Find ":param " part in given "doc string".

	from __doc__ to {
		'parameter' :  'desctiption',
	}
	"""

	# if doc_string is empty
	if code == None:
		return {}
	elif '' == code.strip():
		return {}
	elif ':param' not in code:
		return {}
	elif ':return:' in code.strip(): # strip ':return:'
		regg_ = re.compile(r':return[\d\D]*?:param', flags=re.MULTILINE)
		new_code = code[:code.index(':return:')]
		
		
		if len(list(regg_.finditer(code))) > 0:
			if versbose: print(f'warning-> ":return" MUST BY AT THE END. FIX IT NOW in {name_}!!!\nBut i will try to parse it...')
			code = re.sub(regg_, r':param', code)

	try:
		only_params = code[code.index(':param'):]  # get_only_params_string(code)
	except Exception as e:
		if versbose: print(f'SORRY, fail at parsing that stuff in {name_}')
		return {}

	# making dict
	param_lines = only_params.split(':param ')
	param_lines = [i.strip()
				   for i in param_lines if i.strip()]  # filter empty lines

	args_kwargs_pairs = {}
	for index, i in enumerate(param_lines):

		cols = i.split(':')
		param_name, els = cols[0], '\n'.join(
			[j.strip() for j in ':'.join(cols[1:]).split('\n')])
		# param_name, els = cols[0],  ' '.join([j.strip() for j in ':'.join(cols).split('\n')]) # can be this:

		param_name, els = param_name.strip(), els.strip()
		args_kwargs_pairs[param_name] = els

	return args_kwargs_pairs


def get_return_part(code: str) -> str:
	""" Find ":return:" part in given "doc string"."""
	if code == None:
		return ''
	if ':return:' not in code:
		return ''
	return code[code.index(':return:')+len(':return:'):].strip()


def get_doc_desc(doc_string):

	if doc_string == None:  return ''
	if ':param' in doc_string:  doc_string = doc_string[:doc_string.index(':param')]
	if ':return:' in doc_string: doc_string = doc_string[:doc_string.index(':return:')]

	desc = doc_string.strip().replace('    ', '')

	return f'\n{desc}' if desc else ''

def get_methods_from_class(_class):
	return [v for k,v in _class.__dict__.items() if isfunction(v)]

# CF means "class + function"
def CF_insight(versbose=False) -> dict:

	psg_members     = getmembers(PySimpleGUI)
	psg_funcs       = [o for o in psg_members if isfunction(o[1])]
	psg_classes     = [o for o in psg_members if isclass(o[1])]
	psg_classes_    = list(set([i[1] for i in psg_classes]))  # filtering
	psg_classes     = list(zip([i.__name__ for i in psg_classes_], psg_classes_))

	def _func(): pass

	def func_item(func):
		if type(func) is type(_func):
			name, a_func = func.__name__, func
		else:
			name, a_func = func
		return { "name": name,
			  "obj" : a_func,
			  "__doc__" : a_func.__doc__,
			  "doc_desc" : get_doc_desc(a_func.__doc__),
			  "return_part" : get_return_part(a_func.__doc__),
			  "params_part" : get_params_part(a_func.__doc__, a_func, versbose=versbose)
			} 

	def class_item(someclass):

		name, a_class = someclass
		return { "name": name, "obj" : a_class,
				  "methods" : [ func_item(a_method) for a_method in get_methods_from_class(a_class)],
				  "__doc___class" : a_class.__doc__,
				  "__doc___init" : a_class.__init__.__doc__,
				  "__doc___init_params" : get_params_part(a_class.__init__.__doc__, a_class, versbose=versbose),
		}

	functions_stuff = [ func_item(i) for i in psg_funcs]
	classes_stuff = [ class_item(i) for i in psg_classes]
	
	if versbose: print('done/')
	return functions_stuff, classes_stuff


data = CF_insight()

from pprint import pprint
pprint(data)













































































import sys; sys.exit(1)




def special_cases(function_name, sig, doc_string):

	doca, params_names = doc_string.strip(), list(dict(sig).keys())
	if 'self' in params_names and len(params_names) == 1 and not doca:
		"""
		def Get(self):
			''' '''

		->
		```python
		Get()
		```
		"""
		return True, f'\n\n```python\n{function_name}()\n```\n\n'

	# -return -param
	elif 'self' in params_names and len(params_names) == 1 and doca and ':param' not in doca and ':return:' not in doca:
		"""
		def Get(self):
			''' 
			blah blah blah
			'''

		->

		```python
		Get() # blah blah blah
		```

		"""
		return True, f'\n\n```python\n{function_name}() # {doca}\n```\n\n'

	# +return -param
	elif 'self' in params_names and len(params_names) == 1 and doca and ':param' not in doca and ':return:' in doca:
		"""
		def Get(self):
			''' 
			blah blah blah
			:return: blah-blah
			'''

		->

		```python
		Get() -> blah-blah # blah blah blah
		```

		"""
		return_part = get_return_part(doca)
		desc_ = get_doc_desc(doca)
		return True, f'\n\n{desc_}\n\n```\n{function_name}() -> {return_part}\n```\n\n'

	# +return -param
	elif 'self' in params_names and len(params_names) == 1 and doca and ':param' not in doca and ':return:' in doca:
		"""
		def SetFocus(self, elem):
			''' 
			blah blah blah
			
			:param elem: qwerty
			'''
		"""
		return False, ''


	return False, ''


def get_sig_table_parts(function_obj, function_name, doc_string, logger=None):
	"""
	Convert "function + __doc__" tp "method call + params table" in MARKDOWN
	"""

	doc_string = doc_string.strip()

	# qpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqp
	# 0   0            Making INIT_CALL          0   0 #
	# qpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqp

	try:
		sig, rows = signature(function_obj).parameters, []
	except Exception as e:
		if logger: logger.error(f'PROBLEM WITH {function_obj} {function_name}')
		return '', ''
	for index, key in enumerate(sig):
		val = sig[key].default
		if 'self' == str(key):
			continue
		if val == _empty:        rows.append(key)
		elif val == None:        rows.append(f'{key}=None')
		elif type(val) is int:   rows.append(f'{key}={val}')
		elif type(val) is str:   rows.append(f'{key}="{val}"')
		elif type(val) is tuple: rows.append(f'{key}={val}')
		elif type(val) is bool:  rows.append(f'{key}={val}')
		else:
			raise Exception(f'IDK this type -> {key, val}')

	sig_content = f',\n{TAB_char}'.join(rows)
	sign = "\n\n{0}\n\n```\n{1}({2})\n```".format(get_doc_desc(doc_string), function_name, sig_content)

	if function_name == 'method34': import pdb; pdb.set_trace();
	# --------------
	# SPECIAL CASES
	# --------------
	result = special_cases(function_name, sig, doc_string)
	if result[0]:
		return result[1], ''
	# qpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqp
	# 0   0          Making params_TABLE         0   0 #
	# qpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqpqp

	# 1
	return_guy = get_return_part(doc_string)
	if not return_guy:
		return_guy = ''
		md_return = ''
	else:
		return_guy = return_guy.strip()
		md_return = TABLE_RETURN_TEMPLATE.format(return_guy=return_guy)
		# return_guy = f'\n\nreturn value: {return_guy}\n'
		# return_guy_val_str = return_guy

	# 2
	md_table = '\n'.join([TABLE_ROW_TEMPLATE.format(name=name, desc=desc)
						   for name, desc in
						   get_params_part(doc_string).items()])

	# 3
	params_TABLE = TABLE_TEMPLATE.format(md_table=md_table, md_return=md_return).replace(TAB_char, '').replace('    ', '').replace('\t', '')

	# 1 and N
	# if len(get_params_part(doc_string).items()) == 1:
	#     params_TABLE = TABLE_TEMPLATE.replace('Parameters Descriptions:', 'Parameter Description:').format(md_table=md_table, md_return=md_return).replace(TAB_char, '').replace('    ', '').replace('\t', '')
	# else:
	#     params_TABLE = TABLE_TEMPLATE.format(md_table=md_table, md_return=md_return).replace(TAB_char, '').replace('    ', '').replace('\t', '')

	if not md_table.strip():
		params_TABLE = ''
		
		if return_guy:
			sign = sign[:-4] + f' -> {return_guy}\n```\n'

	return sign, params_TABLE


def pad_n(text): return f'\n{text}\n'


def render(injection, logger=None):
	if injection['part1'] == 'func':  # function
		sig, table = get_sig_table_parts(function_obj=injection['function_object'],
										 function_name=injection['part2'],
										 doc_string=injection['function_object'].__doc__, logger=logger)
	else:  # class method
		function_name = injection['parent_class'].__name__ if injection['part2'] == '__init__' else injection['part2']
		sig, table = get_sig_table_parts(function_obj=injection['function_object'],
										 function_name=function_name,
										 doc_string=injection['function_object'].__doc__, logger=logger)

	if injection['number'] == '':
		return pad_n(sig) + pad_n(table)
	elif injection['number'] == '1':
		return pad_n(sig)
	elif injection['number'] == '2':
		return pad_n(table)
	else:
		if logger: logger.error(f'Error in processing {injection}')


def readfile(fname):
	with open(fname, 'r', encoding='utf-8') as ff:
		return ff.read()


def main(do_full_readme=False, files_to_include: list = [], logger=None, output_name=None, delete_html_comments=True, delete_x3_newlines=True, allow_multiple_tags=True):
	"""
	Goal is:
	1) load 1_ 2_ 3_ 4_
	2) get memes - classes and functions in PSG
	3) find all tags in 2_
	4) structure tags and REAL objects
	5) replaces classes, functions.
	6) join 1 big readme file
	"""
	if logger: logger.info(f'STARTING')

	# 888888888888888888888888888888888888888888
	# ===========  1 loading files =========== #
	# 888888888888888888888888888888888888888888
	HEADER_top_part = readfile('1_HEADER_top_part.md')  # 1
	readme          = readfile('2_readme.md')           # 2
	FOOTER          = readfile('3_FOOTER.md')           # 3
	Release_notes   = readfile('4_Release_notes.md')    # 4


	# 8888888888888888888888888888888888888888888888888888888888888888888888888
	# ===========  2 GET classes, funcions, varialbe a.k.a. memes =========== #
	# 8888888888888888888888888888888888888888888888888888888888888888888888888
	psg_members = getmembers(PySimpleGUIlib)

	psg_funcs = [o for o in psg_members if isfunction(o[1])]
	psg_classes = [o for o in psg_members if isclass(o[1])]
	psg_classes_ = list(set([i[1] for i in psg_classes]))  # filtering
	psg_classes = list(zip([i.__name__ for i in psg_classes_], psg_classes_))

	# IlilIlilIlilIlilIlilIlilIlilIlilIlilIlIlIl
	# ilIli-                       | |    -ilIli
	# ilIli-   _ __ ___   ___  __ _| |_   -ilIli
	# ilIli-  | '_ ` _ \ / _ \/ _` | __|  -ilIli
	# ilIli-  | | | | | |  __/ (_| | |_   -ilIli
	# ilIli-  |_| |_| |_|\___|\__,_|\__|  -ilIli

	# 8888888888888888888888888888888888888888888888888888888
	# ===========  3 find all tags in 2_readme  =========== #
	# 8888888888888888888888888888888888888888888888888888888

	# strip top of the file head
	started_mark = '<!-- Start from here -->'
	if started_mark in readme:
		readme = readme[readme.index(started_mark)+len(started_mark):]

	# find with regex
	regex_pattern = re.compile(r'<!-- <\+[a-zA-Z_]+[\d\w_]*\.([a-zA-Z_]+[\d\w_]*)\+> -->')
	mark_points = [i for i in readme.split('\n') if regex_pattern.match(i)]

	# if there are REPEATED tags -> show them.
	# if not allow_multiple_tags and len(list(set(mark_points))) != len(mark_points):
	#     [mark_points.remove(x) for x in set(mark_points)]
	#     if logger:
	#         logger.error("You have repeated tags! \n {0}".format(
	#             ','.join(mark_points)))
	#     return ''

	# 8888888888888888888888888888888888888888888888888888888888888
	# ===========  4 structure tags and REAL objects  =========== #
	# 8888888888888888888888888888888888888888888888888888888888888

	injection_points = []
	classes_method_tags = [j for j in mark_points if 'func.' not in j]
	func_tags = [j for j in mark_points if 'func.' in j]

	# 0===0 functions 0===0
	for tag in func_tags:

		try:
			__, function_name = tag.split('.')
			function_name = function_name.split('+')[0]
			part2 = function_name

			# {{{{{{{{{ filter number }}}}}}}}}
			number = ''
			if part2[0] in ['1', '2']:
				number, part2 = part2[0], part2[1:]

			# {{{{{{{{{ find function }}}}}}}}}
			founded_function = [func for func_name,
								func in psg_funcs if func_name == function_name]
			if not founded_function:
				if logger: logger.error(f'function "{function_name}" not found in PySimpleGUI')
				continue
			if len(founded_function) > 1:
				if logger: logger.error(f'more than 1 function named "{function_name}" found in PySimpleGUI')
				continue

			# {{{{{{{{{ collect }}}}}}}}}
			injection_points.append({
				"tag": tag,
				"function_object": founded_function[0],
				"parent_class": None,
				"part1": 'func',
				"part2": part2,
				"number": number,
			})
		except Exception as e:
			if logger:
				logger.error(f'               {str(e)}')
			continue

	# 0===0 classes 0===0
	for tag in classes_method_tags:
		try:
			class_name, method_name = tag.split('.')
			class_name, method_name = class_name.split('+')[-1], method_name.split('+')[0]
			part1, part2 = class_name, method_name

			# {{{{{{{{{ filter number }}}}}}}}}
			number = ''
			if part2[0] in ['1', '2']:
				number, method_name = part2[0], part2[1:]

			# {{{{{{{{{ find class }}}}}}}}}
			founded_class = [a_class_obj for a_class_name,
							 a_class_obj in psg_classes if a_class_name == class_name]
			if not founded_class:
				if logger: logger.error(f'class "{tag}" not found in PySimpleGUI')
				continue
			if len(founded_class) > 1:
				if logger: logger.error(f'more than 1 class named "{tag}" found in PySimpleGUI')
				continue

			# {{{{{{{{{ find method }}}}}}}}}
			try:
				if method_name != 'doc':
					founded_method = getattr(founded_class[0], method_name)
					# GLG.append([founded_method, founded_class[0], method_name])
					# string_type = str(type(founded_method))
					# if 'property' in string_type or 'bound' in string_type:
					#     print(string_type)
					#     # import pdb; pdb.set_trace();
					#     if logger:
					#         logger.error(f'Property "{founded_method}" is not parsed.')
					#     continue
				else:
					founded_method = None
			except AttributeError as e:
				if logger: logger.error(f'METHOD not found!: {str(e)}')
				continue
			except Exception as e:
				if logger: logger.error(str(e))
				continue

			# {{{{{{{{{ collect }}}}}}}}}
			injection_points.append({
				"tag": tag,
				"function_object": founded_method,
				"parent_class": founded_class[0],
				"part1": part1,
				"part2": part2,
				"number": number,
			})
		except Exception as e:
			if logger:
				logger.error(f'```````````````````````{str(e)}')
			continue

	# 888888888888888888888888888888888888888
	# ===========  5 injecting  =========== #
	# 888888888888888888888888888888888888888

	success_tags = []
	bad_tags = []
	for injection in injection_points:
		if injection['part2'] == 'doc':  # our special snowflake "doc"
			readme = readme.replace(injection['tag'], injection['parent_class'].__doc__)
		else:
			tag = injection['tag']
			content = render(injection, logger=logger)
			if content:
				success_tags.append(f'{tag} - COMPLETE')
			else:
				bad_tags.append(f'{tag} - FAIL')
			readme = readme.replace(injection['tag'], content)
	if logger:
		success_tags_str    = '\n'.join(success_tags).strip()
		bad_tags_str        = '\n'.join(bad_tags).strip()
		good_message        = f'DONE {len(success_tags)} TAGS:\n' + '\n'.join(success_tags) if success_tags_str else 'All tags are wrong//'
		bad_message         = f'FAIL WITH {len(bad_tags)} TAGS:\n' + '\n'.join(bad_tags) if bad_tags_str else 'No bad tags, YES!'
		logger.info(good_message)
		logger.info(bad_message)
	# 8888888888888888888888888888888888
	# ===========  6 join  =========== #
	# 8888888888888888888888888888888888

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

			# {{{{{{{{{ html removing }}}}}}}}}
			if delete_html_comments:
				if logger: logger.info('Deleting html comments')

				# remove html comments
				filt_readme = re.sub(
					r'<!--([\s\S]*?)-->', '\n', content, flags=re.MULTILINE)

				for i in range(5):
					filt_readme = filt_readme.replace('\n\n\n', '\n\n')

				# add staked_edit
				if '<!--stackedit_data:' in content:
					stackedit_data = content[content.index(
						'<!--stackedit_data:'):]
					filt_readme += stackedit_data

				content = filt_readme

			# {{{{{{{{{ filter multiple multilines EVERYWHERE }}}}}}}}}
			if delete_x3_newlines:

				# removing spaces
				content = re.sub(r'^[ ]+$', '', content, flags=re.MULTILINE)
				# removing \n
				content = re.sub(r'\n{3,}', '\n\n',
								 content, flags=re.MULTILINE)

			# FINISH
			content = content.strip()
			ff.write(content)

		if logger: logger.info(f'ending. writing to a file///////////////')
		return content

	if logger: logger.error(f'Error in main')


@click.command()
@click.option('-nol', '--no_log',                   is_flag=True, help='Disable log')
@click.option('-rml', '--delete_log',               is_flag=True, help='Delete log file after generating')
@click.option('-rmh', '--delete_html_comments',     is_flag=True, help='Delete html comment in the generated .md file')
@click.option('-o', '--output_name',                default='FINALreadme.md',   type=click.Path(), help='Name for generated .md file')
@click.option('-lo', '--log_file',                  default='LOGS.log',         type=click.Path(), help='Name for log file')
def cli(no_log, delete_log, delete_html_comments, output_name, log_file):
	# --------------------
	# ----- logging setup-
	# --------------------

	logger = logging.getLogger(__name__)
	if no_log:
		logger.setLevel(logging.CRITICAL)
		# delete_log = True
	else:
		logger.setLevel(logging.DEBUG)

	my_file = logging.FileHandler(log_file, mode='w')
	my_file.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s>%(levelname)s: %(message)s')

	my_file.setFormatter(formatter)
	logger.addHandler(my_file)

	main(logger=logger,
		 files_to_include=[0, 1, 2, 3],
		 output_name=output_name,
		 delete_html_comments=delete_html_comments)

	# --------------------
	# ----- POST process--
	# --------------------

	if delete_log:
		# delete log file
		log_file = os.path.join(os.path.dirname(
			os.path.abspath(__file__)), log_file)
		if os.path.exists(log_file):
			try:
				os.remove(log_file)
			except Exception as e:
				logger.error(str(e))

if __name__ == '__main__':
	# my_mode = 'cli-mode'
	# my_mode = 'debug-mode'
	my_mode = 'debug-mode2'

	if my_mode == 'cli-mode':
		cli()
	elif my_mode == 'debug-mode':
		main(files_to_include=[0, 1, 2, 3],
			 output_name='johnson_n_johnson.txt',
			 delete_html_comments=True)
	elif my_mode == 'debug-mode2':
		import logging; logger = logging.getLogger(__name__); logger.setLevel(logging.DEBUG)
		my_file = logging.FileHandler('usage.log.txt', mode='w'); my_file.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s>%(levelname)s: %(message)s')
		my_file.setFormatter(formatter); logger.addHandler(my_file);
		main(logger=logger, files_to_include=[1],
			 output_name='johnson_n_johnson.txt',
			 delete_html_comments=True)



































































import sys; sys.exit(1)
import os
# REAL compile
from subprocess import run
from textwrap import wrap
import re

target_file = 'readme.md'
def readfile(fname):
	with open(fname, 'r', encoding='utf-8') as ff:
		return ff.read()
def writefile(target_file, content):
	with open(target_file, 'w', encoding='utf-8') as ff:
		ff.write(content)


def wrap_long_tables_columns(content):
	contlines     = content.split('\n')
	regex_pattern = re.compile(r'^\s*\|[\d\D]*?\|[\d\D]*?\|\n*', flags=re.MULTILINE)
	new_cont = []

	def process(table_line):
		"""
		from:
		|bla bla| qwe ewr ert tryu ytiu y|

		to:
		|bla bla| qwe ewr |
		|       | ert tryu
		|       | ytiu y |
		"""
		columns = table_line.strip('|').split('|')
		second_column = wrap(columns[1], width=65)

		if len(second_column) == 0:
			raise Exception('WTF')
		elif len(second_column) == 1:
			return table_line
		elif len(second_column) > 1:
			first_line = f"| {columns[0]} | {second_column[0]} |\n"
			other_lines = [ '| {0} | {1} |'.format((' '*len(columns[0])), i) for i in second_column[1:]]
			return first_line + '\n'.join(other_lines)

	lines_ro_replace = []
	for index, line in enumerate(contlines):
		if not line.strip():
			new_cont.append(line)
		elif regex_pattern.match(line):
			print(index, line)
			new_cont.append(process(line))
		else:
			new_cont.append(line)
	return '\n'.join(new_cont)

readme = readfile(target_file)
res = wrap_long_tables_columns(readme)
# 1 way
#    1) rename readme.md to OLD_readme.md
#    2) write new content to readme.md
# os.rename(target_file, f'OLD_{target_file}')
# writefile(f'build/{target_file}', wrap_long_tables_columns(readme))

# 2 way
try:
	os.mkdir('build')
except Exception as e:
	print(str(e))

try:
	writefile(f'build/{target_file}', wrap_long_tables_columns(readme))
except Exception as e:
	print(str(e))

run(f"echo 1", shell=True)
run(f"pandoc build/{target_file} -o build/{target_file.replace('md', 'pdf')} --from markdown --template=RED_PILL_latex_template.tex --listings", shell=True)







































































































import sys; sys.exit(1)

import PySimpleGUI


from inspect import *
res = signature(PySimpleGUI.Window.DecrementOpenCount)
print(res)

import sys; sys.exit(1)

import inspect
import PySimpleGUI

psg_members = inspect.getmembers(PySimpleGUI)

psg_funcs    = [o for o in psg_members if inspect.isfunction(o[1])]
psg_classes  = [o for o in psg_members if inspect.isclass(o[1])]
psg_classes_ = list(set([i[1] for i in psg_classes])) # filtering
psg_classes  = list(zip([i.__name__ for i in psg_classes_], psg_classes_))

for i in psg_classes:
	if 'Tk' in i[0] or 'TK' in i[0] or 'Element' == i[0]: # or 'Window' == i[0]:
		continue
	print('')
	print(i[0])
	print('\n'.join(['\t' +  j[0] for j in inspect.getmembers(i[1]) if '_' not in j[0]  ]))

import sys; sys.exit(1)

code = '''

hello1
hello2
hello3

:param sad: qwe6
:param sad2: qwe5
:param sad3: qwe4
:return: hello


'''

code = code[:code.index(':return:')]
print(f'code = {code}')


import sys; sys.exit(1)

# print(__path__)
print(__file__)

import sys; sys.exit(1)

# import re
# d = '''
# mn widths, etc.

 

# Unlike Tables there is no standard format for trees.  Thus the data structure passed to the Tree Elem
# '''

# output = re.sub(r'^[ ]+$', '', d, flags=re.MULTILINE)
# print(output)





# import sys; sys.exit(1)

d="""

trhg
trhtr
htrh
:return: HELLO
"""

# only_return = d[d.index(':return:')+len(':return:'):]
only_return = d[:d.index(':return:')]
print(only_return)



import sys; sys.exit(1)
import inspect
import PySimpleGUI

psg_members = inspect.getmembers(PySimpleGUI)

psg_funcs    = [o for o in psg_members if inspect.isfunction(o[1])]
psg_classes  = [o for o in psg_members if inspect.isclass(o[1])]
psg_classes_ = list(set([i[1] for i in psg_classes])) # filtering
psg_classes  = list(zip([i.__name__ for i in psg_classes_], psg_classes_))

for i in psg_classes:
	if 'Tk' in i[0] or 'TK' in i[0] or 'Element' == i[0]: # or 'Window' == i[0]:
		continue
	print('')
	print(i[0])
	print('\n'.join(['\t' +  j[0] for j in inspect.getmembers(i[1]) if '_' not in j[0]  ]))

import sys; sys.exit(1)

from datetime import datetime
import PySimpleGUI
import click, logging, json, re, os


psg_members = getmembers(PySimpleGUI)
print(f'psg_members = {psg_members}')

psg_funcs       = [o for o in psg_members if isfunction(o[1])]
psg_classes     = [o for o in psg_members if isclass(o[1])]
psg_classes_     = list(set([i[1] for i in psg_classes])) # filtering
psg_classes     = list(zip([i.__name__ for i in psg_classes_], psg_classes_))


for i in psg_classes[2:6]:

	print(i)
	print(help(i))
	continue

	methods = [i for i in getmembers(i)]
	# methods = [i for i in getmembers(i) if 'method' in str(i[1])]
	print(f'{i[0]}')
	print(f'\t{methods}')

import sys; sys.exit(1)


























import sys; sys.exit(1)

a = 'hello heloo heloo'
import re

output = re.sub(r'hel', '1', a, flags=re.MULTILINE, count=2)
print(f'output = {output}')



import sys; sys.exit(1)
from inspect import *; import re, os
import importlib
import click

# res = importlib.util.spec_from_file_location('PySimpleGUI',"/home/gogol/Desktop/кладовка/_DONE/pysimpleguiDOCUMENTATION2019/PySimpleGUIDocGen/db/PySimpleGUIlib.py")
res = importlib.util.spec_from_file_location("/home/gogol/Desktop/кладовка/_DONE/pysimpleguiDOCUMENTATION2019/PySimpleGUIDocGen/db/PySimpleGUIlib.py")
print(f'res = {res}')
import sys; sys.exit(1)
obj = click
file_path, module_name = obj.__file__, obj.__name__

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)
res = ''.join(getsourcelines(module)[0])
print(f'res = {res}')

import sys; sys.exit(1)

import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/home/gogol/Desktop/кладовка/_DONE/pysimpleguiDOCUMENTATION2019/PySimpleGUIDocGen/db/PySimpleGUIlib.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.MyClass()

import importlib.util
import sys

# For illustrative purposes.
import tokenize
file_path = tokenize.__file__
module_name = tokenize.__name__

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


import sys; sys.exit(1)
from inspect import *
from inspect import getmembers, isfunction, isclass, getsource, signature, _empty
import psg, psgqt, psgwx, psgwb
import re, os

#           tk
# ---------------------
psg_members = getmembers(psg)
psg_code    = getmembers(psgqt)
# ---------------------
psg_funcs       = [o for o in psg_members if isfunction(o[1])]
psg_classes     = [o for o in psg_members if isclass(o[1])]
psg_classes_    = list(set([i[1] for i in psg_classes])) # filtering
psg_classes     = list(zip([i.__name__ for i in psg_classes_], psg_classes_))


#           qt
# ---------------------
psgqt_members = getmembers(psgqt)
psgqt_code    = getmembers(psgqt)
# ---------------------
psgqt_funcs     = [o for o in psgqt_members if isfunction(o[1])]
psgqt_classes   = [o for o in psgqt_members if isclass(o[1])]
psgqt_classes_  = list(set([i[1] for i in psgqt_classes])) # filtering
psgqt_classes   = list(zip([i.__name__ for i in psgqt_classes_], psgqt_classes_))


#           wx
# ---------------------
psgwx_members = getmembers(psgwx)
psgwx_code    = getmembers(psgwx)
# ---------------------
psgwx_funcs     = [o for o in psgwx_members if isfunction(o[1])]
psgwx_classes   = [o for o in psgwx_members if isclass(o[1])]
psgwx_classes_  = list(set([i[1] for i in psgwx_classes])) # filtering
psgwx_classes   = list(zip([i.__name__ for i in psgwx_classes_], psgwx_classes_))


#           wb
# ---------------------
psgwb_members = getmembers(psgwb)
psgwb_code    = getmembers(psgwb)
# ---------------------
psgwb_funcs     = [o for o in psgwb_members if isfunction(o[1])]
psgwb_classes   = [o for o in psgwb_members if isclass(o[1])]
psgwb_classes_  = list(set([i[1] for i in psgwb_classes])) # filtering
psgwb_classes   = list(zip([i.__name__ for i in psgwb_classes_], psgwb_classes_))



# ------------------------------------------
# ------------------------------------------
psg_objs   = {name:obj for name, obj in psg_funcs}
psgqt_objs = {name:obj for name, obj in psgqt_funcs}
psgwx_objs = {name:obj for name, obj in psgwx_funcs}
psgwb_objs = {name:obj for name, obj in psgwb_funcs}

overlay_objs = {name:{'qt': psgqt_objs[name], 'tk':psg_obj} for name, psg_obj in psg_objs.items() if name in psgqt_objs}

from pprint import pprint
pprint(overlay_objs)

for key, val in overlay_objs.items():
	print('----------------------------')

	print('-QT VERISON-')
	print(val['qt'].__doc__)
	print('-TK VERISON-')
	print(val['tk'].__doc__)
# [print(dict(i)) for i in psgqt_funcs]

import sys; sys.exit(1)















































































import sys; sys.exit(1)

#             One instance
import logging
logging.basicConfig( filename='example.log',
					 datefmt='%m.%d.%Y %I:%M:%S',
					 format='%(asctime)s>%(levelname)s: %(message)s',
					 level=logging.DEBUG)

# logging.debug('debug')
# logging.error('error')
# logging.info('info')


logger = logging.getLogger('my_app')
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.NOTSET)
logger.setLevel(logging.CRITICAL)
# logger.setLevel(logging.NOTSET)

my_file = logging.FileHandler('example.log'); my_file.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s>%(levelname)s: %(message)s')

my_file.setFormatter(formatter)
logger.addHandler(my_file)


# logger.debug('debug')
# logger.error('error')
logger.info('info')

























































import sys; sys.exit(1)
dd = '''


GNU Lesser General Public License (LGPL 3) +

## Acknowledgments

#### SORRY!! Will add these back.  Lost due to file length limitation
<!-- asdasdas -->


'''


import sys; sys.exit(1)

doc_string = '''

	:param title:  (Default value = None)
	:param button_color:  (Default value = None)
	:param background_color: color of background (Default value = None)
	:param text_color: color of the text (Default value = None)
	:param auto_close:  (Default value = False)
	:param auto_close_duration:  (Default value = None)
	:return: some stuff
'''

from_return = doc_string[doc_string.index(':return:'):]
if ':param' in from_return:

	from_return = from_return[:from_return.index(':param')]

import sys; sys.exit(1)


da = '''

### Examples

**Possible use cases for 1st tag:**

<!-- <+Button.
dasf kldsjmfklo mdsfm dsf 
		dsf dsf
	ds
	ds

	doc+> -->
<!-- <+Button.2__init__+> -->

**Possible use cases for 1st tag:**


'''



import re

output = re.sub(r'<!--([\s\S]*?)-->', '\n', da, flags=re.MULTILINE)
print(f'output = {output}')




import sys; sys.exit(1)
class Person(object):
	""" """
	def __init__(self, name, age=20, color='white', dicksize=None, width=180):
		"""

		:param name: 
		:param age: age of person (Default value = 20)
		:param color:  (Default value = 'white')
		:param dicksize:  (Default value = None)
		:param width:  (Default value = 180)

		"""
		self.name = name
		self.age = age
		self.color = color
		self.width = width


class Mike_Like(Person):
	""" """
	def __init__(self, name, age=55, color='IDK', dicksize=999, width=480):
		"""

		:param name: 
		:param age: age of person (Default value = 55)
		:param color:  (Default value = 'IDK')
		:param dicksize:  (Default value = 999)
		:param width:  (Default value = 480)

		"""
		self.name = name
		self.age = age
		self.color = color
		self.width = width

def hello():
	pass
m1 = Mike_Like.__init__
m1 = hello
print(getattr(Mike_Like, '__init__'))
# print(f'm1 = {m1.__name__}')











import sys; sys.exit(1)
import numpy as np
print(f'res = {res}')


import sys; sys.exit(1)
d = 'ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x "/media/gogol/w/yyy/долгие видео/курс фруктов/out.mp4"'
import subprocess
p = subprocess.Popen(d, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(p.communicate()[0].decode().strip())

import sys; sys.exit(1)
from base64 import b64decode as dd
from base64 import b64encode as de

ppp = de(b'''Q2xlYW5yb29tIFNvZnR3YXJlIEVuZ2luZWVyaW5nINGG0LU=''')
print(f'ppp = {ppp}')


import sys; sys.exit(1)
dd=[["Cleanroom Software Engineering це", "Сукупність адміністративних та технологічних процесів, що дозволяють колективам розробників планувати, вимірювати, специфікувати, проектувати, кодувати, тестувати і сертифікувати програмні продукти."]
,["DFD - це:", "діаграми потоків даних"]
,["JDBC (Java DataBase Connectivity) - це", "Iнтерфейс прикладного програмування (API) для виконання SQL-запитів до баз даних із програм, написаних мовою Java"]
,["Lok-метрики оцінки коду...", "Вимірюють кількість рядків коду"]
,["ODBC (Open Database Connetcivity - відкритий інтерфейс до баз даних) - це", "Уніфікований доступ до даних з персональних комп'ютерів працюючих під керуванням операційної системи Windows"]
,["ODBC - це", "Програмний шар, що уніфікує інтерфейс додатків з базами даних."]
,["SQL-оператор, що активізується під час виконання певних операцій над об'єктами бази даних, - це:", "Тригер"]
,["TickIT:", "«Використання ISO 9001:2000 для побудови систем менеджменту якості програмних продуктів, сертифікації та безперервного поліпшення»"]
,["Абстракція – це:", "Iнша відповідь"]
,["Агрегатні функції у фразі WHERE:", "Не можна використовувати"]
,["Адміністратор може обмежувати можливості користувачів у виконанні тих чи інших.", "системних дій"]
,["Альфа-тестування це:", "Внутрішнє пробне використання"]
,["Атрибут android:onClick призначений для:", "вказівки потрібного методу при виборі пункту меню"]
,["Багатозадачність на основі режиму розділу часу називаеться", "Витісняючою"]
,["Банк даних (БнД) — це", "Система спеціальним чином організованих даних — баз даних, програмних, технічних, мовних, організаційно-методичних засобів, призначених для забезпечення централізованого нагромадження і колективного багатоцільового використання даних"]
,["Безпосередньо дані визначеного типу для опису атрибутів носять назву:", "Поля"]
,["Бета-тестування це:", "Пробне використання із залученням відібраних зовнішніх користувачів"]
,["Блоки операторів, які виконуються при отриманні або установці властивості, носять назву", "Код доступу"]
,["В CSS дозволяє враховувати різні умови або події при визначенні властивостей HTM-тегу:", "інша відповідь"]
,["В діаграмі варіантів використання UML використовується асоціація між:", "Актором та варіантом використання"]
,["В межах якого пакета робіт виконується підготовка тестових даних ?", "тестування системи"]
,["В найбільшій степені підкреслюють роль ОС критерії ефективності обчислювальної системи", "Зручність роботи користувачів"]
,["В один і той же час переглядати дані можуть декілька користувачів, але змінювати дані може тільки один користувач – визначається наступним типом управління доступом користувачів:", "Оптимістичним"]
,["В ОС, кожен процес яких має тільки один потік, виникають проблеми організації паралельних обчислень в рамках", "Процесу"]
,["В процедурі оголошеній змінній задати значення можна командою:", "SELECT"]
,["В РНР не можна викликати функцію до її визначення:", "визначену всередині умовних операторів або інших функцій"]
,["В Україні сертифікацію проводить", "УкрСЕПО"]
,["В яких випадках конструктор не викликається?", "Інша відповідь"]
,["В яких цілях потрібно використовувати горизонтальний прототип1. Для прояснення неясних або багато альтернативних вимог", "Для макетування компонентів систем"]
,["В якому артефакті перераховані відповідальності класу і класи, які знаходяться в кооперації з класом, який розглядається?", "Карти представлення"]
,["В якому вигляді оформлюється кожне відгалуження основного сценарію?", "У вигляді розширення"]
,["В якому випадку карточка історії користувача підлягає процедурі розділу?", "Якщо оцінка більше трьох пунктів"]
,["В якому випадку операторна функція для перевантаження унарних операцій не має параметрів?", "Iнша відповідь"]
,["В якому розділі знаходяться моделі, побудовані в процесі аналізу вимог", "Модель аналізу"]
,["В якому розділі шаблону документа “Vision” RUP описуються акроніми і скорочення", "Введення"]
,["В якому розділі шаблону документа “Vision” RUP описуються акроніми і скорочення", "Вихідні положення"]
,["В якому розділі шаблону повного опису варіанта використання по Коберну послідовно описуються всі альтернативні сценарії", "Інша відповідь"]
,["В якому розділі шаблону повного опису варіантів використання по Коберну вказується ім’я ролі основного актора або його опис", "Основна діюча особа"]
,["В якому стані може перебувати Активність?", "зупинена"]
,["В якості клієнта для резервного копіювання в BackupPC можуть використовуватись:", "Інша відповідь"]
,["В якій моделі кожен прийом може підлягати декомпозиції", "DFD"]
,["В якій частині шаблону SRS описуються компоненти, які можуть впливати на життєздатність розроблюваної системи?", "Передбачення і залежності4. Інша відповідь"]
,["В якій із запропонованих методологій виділяється робочий потік ділового моделювання?", "RUP"]
,["Важливою причиною застосування програмних переривань замість звичайних інструкцій виклику підпрограм, являється можливість зміни користувацького режиму процесора на _____, одночасно з викликом процедури", "Привілейований"]
,["Веб-сторінка розгортається на весь екран по ширині незалежно від встановленої роздільної здатності монітора при використанні:", "еластичного дизайну"]
,["Вербальні комунікації здійснюються за допомогою", "усного мовлення"]
,["Верифікаціяі програмного забезпечення це", "Процес забезпечення правильної реалізації програмного забезпечення, яке відповідає специфікаціям, виконується протягом усього життєвого циклу."]
,["Вертикальна структура в організованій групі, створеній для досягнення певної мети, не вибудовується на рівні", "рівень офіційних емоційних відносин"]
,["Виберіть маску мережі класу А", "255.0.0.0"]
,["Виберіть маску мережі класу С", "Інша відповідь"]
,["Виберіть об’єкти, які можна включати у роль бази даних SQL Server 2000.", "Інша відповідь"]
,["Виберіть правильну послідовність стадій розвитку конфлікту", "суперечлива ситуація, перешкоджання зі сторони одного з учасників досягнення цілей іншими учасниками, інцидент, конфлікт"]
,["Виберіть специфікації з моноканальною топологією", "10- BaSe-2"]
,["Вибірка (R WHERE f) відношення R по формулі f являє собою", "Відношення з таким же заголовком і тілом, що складається з таких кортежів відношення R, що задовольняють істинності логічного вираження, заданого формулою f"]
,["Видаляє привілеї вже існуючих облікових записів оператор:", "Інша відповідь"]
,["Види ручного рецензування коду:", "Парне програмування, buddy-рев’ю, групове рев’ю, формальне рев’ю"]
,["Види числової інформації, що накопичується регістром нагромадження, називаються", "ресурси"]
,["Видимість в UML не є властивістю", "примітки"]
,["Визначити для якої стадії формування групи характерна така ситуація. Члени групи починають конструктивно пристосовуватися до відмінностей у поглядах і співпрацюють один з одним. Виникає почуття товариства, групова згуртованість. Співробітники ідентифікують себе з групою.", "становлення норм поведінки"]
,["Визначити процеси, які відносяться до керованого рівня зрілості", "Моніторинг та контроль проекту"]
,["Визначити форму ступінчатого представлення", "П’ять рівнів зрілості з 22 областями технологічних процесів"]
,["Визначте базові типи топологій", "Моноканальна"]
,["Визначте найбільшу довжину витої пари 5-ї категорії в метрах1. 100", "180"]
,["Визначте найбільшу довжину тонкого коаксиального кабелю в метрах", "500"]
,["Визначте найбільшу швидкість передачі інформації по витій парі в Мбіт/с (стандарт 100base-T4).", "100"]
,["Визначте найбільшу швидкість передачі інформації по коаксиальному кабелю в Мбіт/с (стандарт 10 - base 2)", "10"]
,["Визначте призначення алгоритму Колберга.", "Інша відповідь."]
,["Виклик методу або делегата здійснюється за допомогою операції", "x ()"]
,["Виклик функції в SQL може виконуватися:", "Там, де допускається ставити вираз"]
,["Виокремлення інформаційних об’єктів предметної області (таблиць), які підлягають зберіганню в БД, а також визначення характеристик об’єктів і зв’язків між ними відбувається на етапі:", "Інфологічного моделювання"]
,["Вираз DELETE FROM ПРЕДМЕТ означає:", "Видалення усіх рядків таблиці"]
,["Вираз SELECT Назва AS Назва_Організації... означає:", "Перевизначення імені стовпця"]
,["Вкажіть базовий API для Java ME", "CLDC"]
,["Вкажіть види обфускації.", "Лексична обфускація."]
,["Вкажіть види стандартних ролей SQL Server.", "На рівні сервера."]
,["Вкажіть види стеганографії.", "Цифровий підпис."]
,["Вкажіть властивості статичних функцій-членів класу?", "Статична змінна-член є загальною для всіх екземплярів класу"]
,["Вкажіть властивості статичних функцій-членів класу?", "Статична функція-член класу безпосередньо може посилатися тільки на статичні змінні і статичні функції, що належать її класу"]
,["Вкажіть діапазон IP- адрес класу А", "1- 126"]
,["Вкажіть діапазон IP- адрес класу В", "128- 191"]
,["Вкажіть зміст засобів безпеки Access 2003 в меню Сервіс.", "Створення користувачів."]
,["Вкажіть конструкцію, яка підтримує обробку подій користувацького інтерфейсу за допомогою команд у середовищі розробки Android Studio?", "Displayable"]
,["Вкажіть конфігураційний файл клієнта служби перетворення імен?", "/etc/hosts"]
,["Вкажіть коректний запис", "Движение.Количество: = ТекСтрокаМатериалы.Количество"]
,["Вкажіть кількість рівнів в моделі OSI", "Інша відповідь"]
,["Вкажіть назви декомпіляторів", "Boomerang"]
,["Вкажіть найбільшу кількість комп’ютерів, які можна під’єднати до мережі класу А", "16 777 214"]
,["Вкажіть найбільшу кількість комп’ютерів, які можна під’єднати до мережі класу С", "224"]
,["Вкажіть найбільшу швидкість в зіркоподібній топології в Мбіт/с (Стандарт 10 - base - Т)", "10"]
,["Вкажіть найбільшу швидкість в кільцевій топології в Мбіт/с (Token Ring).", "Інша відповідь"]
,["Вкажіть найбільшу швидкість в моноканальній топології в Мбіт/с (Стандарт 10 – base - 5).", "10"]
,["Вкажіть об’єкти, які можна включати у роль бази даних", "Користувачів SQL Server;"]
,["Вкажіть особливості роботи комутаторів", "Пропускна здатність пропорційна кількості портів"]
,["Вкажіть особливість визначення конструктора класу", "Конструктор не може повертати значення"]
,["Вкажіть правильне твердження", "Деструктор може бути віртуальним"]
,["Вкажіть правильні твердження", "Деструктор викликається під час знищення об’єкта"]
,["Вкажіть правильні твердження", "Деструктор може бути тільки один в класі"]
,["Вкажіть призначення вбудованої ролі SQL Server Sysadmin", "Може виконувати будь-які дії в SQL Server"]
,["Вкажіть призначення засобу адміністратор робочих груп в системі безпеки Access 2003.", "Інша відповідь"]
,["Вкажіть призначення формату ACCDB бази даних Access 2007.", "Інша відповідь"]
,["Вкажіть призначення формату ACCDE бази даних Access 2007.", "Формат відомий як скомпільований двійковий файл. Скомпільваний двійковий файл Office Access 2007 — це файл додатку базы даних, при збережені йкого весь код VBA був скомпільований."]
,["Вкажіть протоколи прикладного рівня", "FTP"]
,["Вкажіть протоколи транспортного рівня", "TCP"]
,["Вкажіть різновиди витої пари", "Неекранована"]
,["Вкажіть різновиди коаксіального кабелю", "Тонкий"]
,["Вкажіть різновиди оптоволоконного кабелю", "Багатомодовий"]
,["Вкажіть службу, що керує життєвим циклом додатків", "Activity Manager"]
,["Вкажіть способи захисту програмного забезпечення.", "Обфускація."]
,["Вкажіть функції ведення журналів доступу SQL Server.", "Реєструвати всі спроби отримання доступу до системи баз даних"]
,["Вкажіть функції транспортного рівня моделі OSI", "Забезпечує зв'язок між кінцевими пунктами і надійність"]
,["Вказати основні підзадачі декомпіляції.", "Виявлення параметрів і значень, що повертаються."]
,["Вказати послідовність створення підписаного пакету 2007.", "Microsoft Office — Опублікувати - Запакувати і підписати."]
,["Вкладеність тригерів є допустимою?", "Так"]
,["Властивості класу визначаються", "Специфікаторами"]
,["Властивості унікальності та ненадмірності характерні для:", "Первинних ключів"]
,["Властивість «Подвал» має", "елемент керування «Табличное поле»"]
,["Внесення змін та розвиток БД відносяться до наступного етапу життєвого циклу БД:", "Супроводження"]
,["Встановлення SUID-біта дає можливість", "Виконувати файл з правами власника"]
,["Від чого залежить ступінь деталізації операцій проекту?", "від кількості контрольних подій"]
,["Відзначити порт, який використовується за умовчанням для роботи MySQL:", "Інша відповідь"]
,["Відмова програмного забезпечення (failure) це", "Перехід програмного забезпечення з працюючого стану в неробочий або коли одержуються результати, які не відповідають заданим допустимим значенням."]
,["Відношення асоціації неможливе між", "інший варіант"]
,["Відношення залежності неможливо між", "примітками"]
,["Відношення узагальнення неможливо між", "станами"]
,["Вільний резерв часу виконання роботи – це", "Запас часу, яким можна розраховувати при виконанні даної роботи, припускаючи, що робота почнеться в свій ранній термін і наступні за нею роботи настануть в ранні терміни"]
,["Вірним є твердження: Для 1С:Підприємство 8.0 існує...", "одна платформа і множина конфігурацій"]
,["Віртуальні таблиці зберігають:", "Тільки текст запиту SELECT"]
,["Віртуальні таблиці можна використовувати для", "визначення типу даних"]
,["Головна особливість, що відрізняє смартфон від звичайного мобільного телефону?", "навність операційної системи"]
,["Головні цілі перегляду (за IEEE 1028):", "Пошук аномалій, покращення продукту, обговорення альтернативних шляхів реалізації, оцінка відповідності стандартам і специфікаціям"]
,["Група в системі видаляється за допомогою команди", "groupdel"]
,["Дайте визначення TCP — вікна", "Максимальна кількість сегментів відправлених без підтвердження повідомлення про отримання."]
,["Дайте визначення електронних ключів при захисті ПЗ", "Являє собою невеликий пристрій, який під’єднується до одного з портів комп'ютера."]
,["Дайте визначення обфускації.", "Заплутування програмного коду."]
,["Дані поля n_z таблиці bd1 потрібно скопіювати в таблицю bd2:", "insert into bd2 n_z select n_z from bd1"]
,["Дати визначення декомпілюванню.", "Створення програми високого рівня, що еквівалентна програмі на мові асемблера."]
,["Дахом «Дому якості» є:", "Кореляційна матриця технічних характеристик"]
,["Дефект (fault) в програмному забезпечення це", "Наслідок використання елементів програми, який може призвести до деякої події (невірна інтерпретація цього елементу комп’ютером)"]
,["Джерела помилок:", "Інша відповідь"]
,["Директива private –", "Iнша відповідь"]
,["Директива protected –", "Iнша відповідь"]
,["Для виключення нераціональних переривань програм в 'незручні' для них моменти часу розробник програми для ОС з не витісняючою багатозадачністю сам може визначати моменти", "Передачі управління ОС"]
,["Для доступу до методів об'єкта в РНР використовується оператор:", "інша відповідь"]
,["Для доступу до функцій і змінних в РНР всередині визначення класу використовують:", "псевдозмінну $this"]
,["Для користувача основним є режим роботи", "1С:Підприємство"]
,["Для одержання властивості об'єкта в РНР використовують наступний запис:", "$ім'я_об'єкта->назва_властивості"]
,["Для опису оцінки значень показників якості використовуються наступні методи:", "Вимірювальний, реєстраційний , розрахунковий, експертний"]
,["Для перебору колекції значень можна використати конструкцію", "Для каждого...из...цикл"]
,["Для переведення XML-даних в дерево об'єктів використовується функція РНР:", "domxml_open_file()"]
,["Для прискорення роботи багатошарового ядра іноді може відбуватися безпосереднє звернення зверху до функцій нижніх шарів, минаючи ______ шари.", "Проміжні"]
,["Для підключення додаткових ppa-репозиторіїв використовується команда", "apt-add-repository ppa:speed-dreams/ppa"]
,["Для підключення зовнішніх файлів в РНР використовується оператор:", "open_file"]
,["Для підрахунку кількості усіх значень використовується вираз:", "Інша відповідь"]
,["Для скасування виконання транзакції команду ROLLBACK потрібно виконати:", "До команди COMMIT"]
,["Для створення друкованої форми документа використовують:", "інша відповідь"]
,["Для чого визначається оцінка реалізуємості проекту?", "чи буде проект успішним чи він приречений на невдачу"]
,["Для чого виконується аналіз відхилень при управлінні розкладом проекту?", "для порівняння директивних дат початку та виконання з фактичними/прогнозними"]
,["Для чого потрібен файл маніфесту AndroidManifest.xml:", "надає основну інформацію про програму системи"]
,["Для чого служить smbd?", "Дозволяє працювати як клієнтові по протоколу SMB на системах Linux"]
,["Для чого служить smbd?", "Дозволяє працювати як клієнтові по протоколу SMB на системах Linux"]
,["Для чого служить testprns?", "Інша відповідь"]
,["Для швидкого макетування аспектів та компонентів системи створюються", "Досліджувані прототипи"]
,["До елементів структури групи не належить", "групова згуртованість"]
,["До клієнт-серверної архітектури можна віднести наступний зразок проектування:", "Facade"]
,["До культурних бар’єрів на шляху ефективних комунікацій відносяться таки перешкоди", "різне розуміння одних і тих самих жестів та різне сприйняття дистанції між співрозмовниками представниками різних країн"]
,["До операторів циклу в РНР відносяться:", "while, do...while, foreach, for"]
,["До організаційних бар’єрів на шляху ефективних комунікацій відносяться такі перешкоди:", "наявність великої кількості рівнів в структурі управління та відсутність регламенту діяльності працівників та підрозділів"]
,["До основних складових поняття веб-дизайну відносять:", "зміст, оформлення, технології, подання, мета"]
,["До скалярних типів даних в РНР відносяться:", "Boolean, integer, float, string"]
,["До типу даних «РЯДКИ СИМВОЛІВ» мови SQL відносяться:", "CHARACTER"]
,["До часових бар’єрів на шляху ефективних комунікацій відносяться такі перешкоди:", "відсутність у керівника часу для того, щоб вислухати кожного співробітника та дефіцит часу спілкування"]
,["До яких прийомів відноситься затвердження вимог", "Прийоми отримання вторинних вимог"]
,["До яких прийомів можна віднести визначення потрібної функціональності системи?", "До прийомів отримання вторинних вимог"]
,["До якої області знань проектного управління відноситься процес тестування програмного продукту?", "управління якістю"]
,["До якої фази можна віднести бета-версію продукта?", "Фаза конструювання"]
,["Добутком відношення Rl ступеня к1 і відношення R2 ступеня к2 (Rl TIMES R2), що не мають однакових імен атрибутів, є", "Відношення R ступеня (к1+к2), заголовок якого представляє поєднання заголовків відношень R1 і R2, а тіло - має кортежі, такі, що перші к1 елементів кортежів належать множині Rl, а останні к2 елементів - множині R2;"]
,["Додаток, що знаходиться в процесі розробки, називається", "Проектом"]
,["Документ можна проводити по декільком регістрам?", "так"]
,["Дослідницьке тестування визначається як...", "одночасне навчання, проектування тесту і його виконання"]
,["Доступ до захищених даних-членів класу здійснюється ...", "За допомогою відкритих (public) функцій-членів класу"]
,["Дружню функцію слід оголосити із специфікатором доступу ...", "Будь-яким з перелічених"]
,["Дія в UML може бути одного з наступних типів (вкажіть зайве)", "інший варіант"]
,["Діяльності і техніки гарантії якості включають", "Інспекцію, верифікацію, валідацію програмного забезпечення"]
,["З механізмом віртуальних методів пов’язуються поняття", "Поліморфізму"]
,["З нижче наведеного виберіть вірне твердження", "певні групи створюються переважно для розв’язку певних проблем"]
,["З позиції розробника структуру сайту умовно можна поділити на два рівні:", "логічний та фізичний"]
,["З якою метою використовуються вимоги програмістом", "Розробка програмного коду"]
,["За допомогою чого можна розширити функціональні вимоги кількісними метриками?", "За допомогою аспектів застосовності"]
,["За допомогою якого процесу можна змоделювати АИС", "Аналіз моделі"]
,["За допомогою якої програми можна визначити, коли користувач останній раз працював у системі?", "Lastlog"]
,["За кількістю часу, що витрачається, робота може бути", "Дійсною і фіктивною"]
,["Заборона на вхід певного користувача в систему з певного хоста можна заборонити або дозволити в", "access.conf"]
,["Запис alter table bd1 change n_z n_z char(9) not null; означає", "Заміну значень поля n_z таблиці bd1 на ненульові значення"]
,["Запис alter table bd1 drop nomer; означає:", "Видалення поля nomer таблиці bd1"]
,["Запис ALTER TABLE products ENGINE = INNODB означає", "Зміну типу таблиці"]
,["Запис select * from bd1; виведе як результат", "Назви та значення усіх полів"]
,["Збереження контексту поточного потоку, що підлягає заміні; завантаження контексту нового потоку, обраного в результаті планування; запуск нового потоку на виконання. Такий порядок:", "Диспетчеризації"]
,["Збільшення числа шарів ядра веде до деякого уповільнення його роботи за рахунок міжшарової взаємодії, а зменшення - _____ розширюваності і логічності системи.", "Погіршення"]
,["Зв’язок «один-до-багатьох» передбачає, що одному представнику сутності А відповідає наступна кількість представників сутності В:", "Нуль, один або декілька"]
,["Здатність проведення має об’єкт", "Інша відповідь"]
,["Зміна стану регістра нагромадження може відбуватися при", "проведенні документа"]
,["Змінити структуру таблиці після її створення можна за допомогою оператора:", "ALTER TABLE"]
,["Змінювати значення у наявних рядках таблиці надає можливість оператор:", "Інша відповідь"]
,["Зіставлення таблиці з її псевдонімом здійснюється у фразі:", "Інша відповідь"]
,["Кардинальність відношення – це:", "Кількість рядків"]
,["Квантифікатор * в регулярних виразах РНР означає:", "інша відповідь"]
,["Керований код, який створюється компілятором при компіляції початкового коду в .NET Framework, носить назву", "IL-код"]
,["Клас – це ...", "Опис об’єктів, що мають подібні властивості"]
,["Клас – це ...", "Тип даних, який описує структури даних та множину операцій над ними"]
,["Клас – це:", "Iнша відповідь"]
,["Клас, який успадковується, називається", "Базовим"]
,["Класифікація типів відмов", "Інша відповідь"]
,["Ключове слово Экспорт вказує на те, що процедура", "може бути доступна з інших програмних модулів"]
,["Ключові аспекти планування тестової діяльності включають:", "Координацію персоналу, управління устаткуванням та іншими засобами необхідними для організації тестування, планування обробки небажаних результатів"]
,["Кожне реляційне відношення має один і лише один:", "Інша відповідь"]
,["Коли повинні виконуватися конструктори базового і похідного класів, використовується ключове слово", "base"]
,["Коли складається план ітерацій?", "Інша відповідь"]
,["Коли частинами оперативної пам'яті і віртуального адресного простору є сегменти довільного розміру, то мова йде про розподіл", "Сегментний"]
,["Команда apt-get clean", "Очищає кеш пакетів"]
,["Команда apt-get update", "Оновлює список доступних пакетів"]
,["Команда ssh-copy-id служить для", "Копіювання ключа авторизації на віддалену машину"]
,["Команда «ЗАВЕРШИТИ ТРАНЗАКЦІЮ»", "Інша відповідь"]
,["Команда «СКАСУВАТИ ТРАНЗАКЦІЮ»", "Інша відповідь"]
,["Комунікаційний канал — це", "засіб цілеспрямованого передавання інформації"]
,["Комунікація як процес передбачає наявність", "інша відповідь"]
,["Комунікація як термін латинського походження означає:", "інша відповідь"]
,["Комірка табличного документа може містити", "текст, параметр, шаблон"]
,["Конструктор екземпляру класу викликається", "Автоматично"]
,["Конструкція, яка інкапсулює семантичну інформацію про дію у середовищі розробки Android Studio?", "Клас Command"]
,["Конструкції, що використовуються у виразах для означення певних дій над даними - це:", "Оператори"]
,["Коректне записане звернення до елементу", "Перечисления.ВидыНоменклатуры.Материал"]
,["Користувач в системі видаляється з допомогою команди:", "deluser"]
,["Користувач може вносити зміни у", "конфігурацію бази даних"]
,["Кратність в UML є властивістю (вкажіть зайве)", "операції"]
,["Ліве крило «дому якості»", "Стовпець пріоритетів користувацьких характеристик"]
,["Масив який при необхідності може збільшувати свій розмір, є", "Динамічним"]
,["Мета динамічного тестування за принципом чорного ящика...", "Виявлення одним тестом максимального числа помилок з використанням невеликої підмножини можливих вхідних даних"]
,["Метод білого ящика дозволяє...", "Дослідити внутрішню структуру програми"]
,["Метод класу – це:", "Iнша відповідь"]
,["Метод перевірки на несуперечливість передбачає:", "Інша відповідь"]
,["Метод перевірки правильності програм...", "Інша відповідь"]
,["Метод сірого ящика...", "Заснований на влаштування вхідної області функції на під-області виявлення помилок"]
,["Методи тестування поділяються на:", "інша відповідь"]
,["Метрика програмного забезпечення (software metric) це", "Міра, яка дозволяє отримати числове значення деякої властивості програмного забезпечення або його специфікації"]
,["Метрика Холстед це", "Метрика обчислювана на підставі аналізу числа рядків і синтаксичних елементів початкового коду програми"]
,["Метрика циклічної складності за Мак-Кейбом це", "Показник оцінки складності потоку управління програмою і обчислюється на основі графа керуючої логіки програми"]
,["Метрика Чепіна це", "Оцінка інформаційної міцності окремо взятого програмного модуля за допомогою аналізу характеру використання змінних зі списку вводу-виводу"]
,["Модель вважається суперечливою, якщо безліч вихідних переходів простого стану", "містить переходи з однаковими подіями і спільними сторожовими умовами"]
,["Модель вважається суперечливою, якщо для даної події безліч вихідних переходів по цій події з виконаними сторожовими умовами", "містить більше одного елемента"]
,["Модель даних використовується", "Для генерації схеми бази даних"]
,["Модель оцінки рівня зрілості процесів розробки разом з його похідними це", "CMM"]
,["Модель якості Боема визначає:", "Якість програмного забезпечення за заданим набором ознак і показників"]
,["Модель якості Друмі будується за...", "5 етапів"]
,["Модель якості МакКола має таку кількість перспектив для виявлення якості програмного продукту:", "3"]
,["Моделі класів часто називають", "об'єктними моделями"]
,["Модуль – це", "«сховище» для тексту програми вбудованою мовою"]
,["Модульність – це:", "Iнша відповідь"]
,["Можливість настроювання системи на особливості конкретного підприємства та класу розв'язуваних завдань називається", "конфігурованість"]
,["Можуть бути регістрами залишків і регістрами оборотів", "Інша відповідь"]
,["На діаграмі взаємодії UML застосовують такі типи сутностей", "інший варіант"]
,["На діаграмі використання UML застосовують такі основні типи сутностей", "Варіанти використання"]
,["На діаграмі класів UML застосовують такий тип сутностей, як:", "Інтерфейси"]
,["На діаграмі компонентів UML застосовують такий тип сутностей, як:", "Класи"]
,["На діаграмі кооперації (комунікації) UML застосовують наступні основні типи сутностей", "інший варіант"]
,["На діаграмі послідовності UML застосовують такі типи сутностей", "інший варіант"]
,["На діаграмі розміщення (розгортання) UML не застосовують такий тип сутностей, як:", "Варіанти використання"]
,["На діаграмі станів UML застосовують такі типи сутностей", "Стани"]
,["На зміст дисципліни формування черги впливають:", "Інша відповідь"]
,["На малюнку C є", "класом асоціації A-B"]
,["На малюнку наступні відносини є допустимими на канонічної діаграмі використання", "Асоціація A-C"]
,["На малюнку наступні відносини є неприпустимими на канонічній діаграмі варіантів використання", "Асоціація С-D"]
,["На малюнку наступні повідомлення є неприпустимими на канонічної діаграмі послідовності", "М3"]
,["На малюнку об'єкт А", "існує до початку взаємодії"]
,["На малюнку об'єкт В", "виникає в процесі взаємодії"]
,["На малюнку об'єкт С", "інший варіант"]
,["На малюнку", "A використовує інтерфейс B"]
,["На малюнку", "A є узагальненням В"]
,["На фазі ініціації проекту хорошою вважається оцінка трудовитрат з точністю", "Інша відповідь"]
,["На шляху ефективних комунікацій зустрічаються такі бар’єри:", "фізичні, часові, культурні3) часові та культурні"]
,["На якому етапі проекту виконується аналіз бізнес-процесів?", "планування проекту"]
,["На якому етапі проекту виконується створення технічних специфікацій?", "проектування"]
,["На якому етапі проекту виконується формулювання вимог в термінах конкретних дій за допомогою яких команда планує та реалізує проект?", "визначення вимог проекту"]
,["На якому етапі проекту потрібно розробляти заходи з забезпечення якості проекту?", "на початку проекту"]
,["На якому рівні проходить інтегроване управління проектом", "На початковому"]
,["На якій фазі можливе отримання відгуків і оцінок замовника?", "На фазі вироблення концепції"]
,["На якій фазі можливе отримання відгуків і оцінок замовника?", "На фазі впровадження"]
,["На якій фазі проекту починаються роботи по формуванню бачення продукту і границь проекту?", "На ранній фазі проекту"]
,["Набір таблиць даних, які описують, що визначено в модулі, носить назву", "Метадані"]
,["Назвіть найбільш відомий спосіб створення прототипів", "RAD"]
,["Назвіть найбільш відомий спосіб створення прототипів", "RAD"]
,["Назвіть основний вид відношень, який використовується в діаграмі варіантів використання", "Асоціація"]
,["Назвіть сучасний метод вилучення вимог", "JAD"]
,["Наслідування – це:", "Iнша відповідь"]
,["Об'єкт конфігурації Довідник може мати", "довільну кількість форм"]
,["Об'єкт, що генерує інформацію про 'невизначеній програмній події', носить назву", "Виняток"]
,["Об'єкти конфігурації, які дозволяють створювати в базі даних структури, призначені для нагромадження інформації в зручному для наступного аналізу вигляді, – це", "Регістри"]
,["Об'єктна модель документа (Document Object Model – DOM) – це:", "стандарт, який регламентує спосіб подання вмісту документа (зокрема веб-сторінки) у вигляді набору об'єктів"]
,["Об`єднанням двох сумісних відношень R1 і R2 однакової розмірності (Rl UNION R2) є відношення R, яке:", "Містить всі елементи вихідних відношень (за виключенням повторень)"]
,["Обмеження в аналізі вимог– це...", "Формулювання умов, які модифікують вимоги або набори вимог, звужуючи вибір"]
,["Обов'язковими розділами класу в UML є", "розділ імені"]
,["Обробник події створюється", "окремий для кожної події"]
,["Об’єднання C(R1, R2) відношень R1 і R2 за умовою, заданою формулою f, являє собою", "Відношення R, яке можна одержати шляхом декартового добутку відношень R1 і R2 з наступним застосуванням до результату операції вибірки по формулі f. Правила запису формули f такі ж, як і для операції селекції"]
,["Об’єкти конфігурації 1С:Підприємство відрізняються", "набором властивостей"]
,["Об’єкти тестування це", "Компоненти, групи компонентів, підсистеми, система"]
,["Окремим оператором виконується виклик:", "Процедури"]
,["Оператор визначення представлення у мові SQL:", "column name"]
,["Оператор перевірки приналежності елемента множині:", "Інша відповідь"]
,["Операція В=А для об’єктів класів може застосовуватися, якщо...", "Об’єкт А є похідним від об’єкта В"]
,["Операція доступу до змісту об'єкта частинами — це", "Інша відповідь"]
,["Операція знищення об'єкта — це:", "Iнша відповідь"]
,["Операція створення і (або) ініціалізації об'єкта — це:", "Iнша відповідь"]
,["Операція, яка змінює стан об'єкта шляхом запису чи доступу — це:", "Інша відповідь"]
,["Операція, яка надає доступ для визначення стану об'єкта без його змін — це:", "Інша відповідь"]
,["Опис параметрів мережевих інтерфейсів Ubuntu знаходиться в каталозі:", "/etc/network"]
,["ОС-комплекс взаємопов’язаних програм, що діють як інтерфейс між додатками та користувачами з однієї сторони, а з іншої сторони - ...", "Апаратурою комп’ютера"]
,["Основними елементами процесу комунікації є", "інша відповідь"]
,["Основні складові TQM", "Інша відповідь"]
,["Оцінка надійності програмного забезпечення характеризується такими статистичними показниками:", "Ймовірність і час безвідмовної роботи, можливість відмови і частота відмов"]
,["Палітра властивостей – це", "спеціальне службове вікно, що дозволяє редагувати всі існуючі властивості об'єкта конфігурації"]
,["Параметр, що характеризує міру взаємодії модуля з іншими модулями - це:", "зчеплення"]
,["Параметром оператора throw є", "об'єкт"]
,["Парсинг веб-документа означає:", "його трансляцію в певну організовану структуру, що підходить для подальшої обробки"]
,["Перевантаження методів є проявом", "Поліморфізму"]
,["Перевизначення віртуального методу здійснюється службовим словом", "override"]
,["Перевіряє, чи належить елемент множині, предикат:", "Інша відповідь"]
,["Передумови функціонального тестування:", "коректне оформлення вимог і обмежень до якості програмного забезпечення"]
,["Передумови функціонального тестування:", "Інша відповідь"]
,["Перетином двох сумісних відношень R1 і R2 однакової розмірності (R1 INTERSECT R2) є відношення R, яке:", "Містить кортежі, які одночасно належать обом вихідним відношенням"]
,["Планування якості включає:", "Інша відповідь"]
,["Повний об'єм робіт по проектуванню, виключаючи архітектуру і реалізацію – це...", "детальне проектування"]
,["Подія таймера", "виникає після закінчення заданого інтервалу часу"]
,["Полями класу називають –", "Iнша відповідь"]
,["Поліморфізм дозволяє...", "Реагувати об’єктам різних типів по- різному на те саме повідомлення"]
,["Поняття поліморфізму означає", "Iнша відповідь"]
,["Поняття потенційного ключа є:", "Семантичним поняттям"]
,["Поняття інкапсуляції", "Iнша відповідь"]
,["Потреба потоку відразу в декількох ресурсах є необхідною умовою", "Інша відповідь"]
,["Потрібно вивести назви ораганізацій:", "SELECT ОРАГАНІЗАЦІЯ.Назва FROM ОРАГАНІЗАЦІЯ"]
,["Потрібно надійно ізолювати в декількох модулях, що не розподіляти по всій системі апаратнозалежний", "Інша відповідь"]
,["Поясніть значення терміну мода", "Інша відповідь"]
,["Поєднання схем організації, предметизації і навігації, реалізованих в інформаційній системі, – це:", "інформаційна архітектура"]
,["Праве крило «дому якості»", "Таблиця рейтингів споживчих характеристик"]
,["Предикат EXISTS, коли підзапит, до якого він застосовується, містить хоча б один рядок, повертає:", "Значення TRUE"]
,["При аналізі вимог в рамках проекту розглядається...", "Степінь деталізації вимог"]
,["При верифікації АІС визначається, що", "АІС відповідає сформульованим вимогам"]
,["При виконанні транзакції відбувається наступне:", "Виконуються усі дії, або жодної"]
,["При використанні ftp сервера vsftpd необхідно дозволити вхід в систему анонімним користувачам. Який з перерахованих нижче параметрів слід використовувати?", "Інша відповідь"]
,["При використанні ftp сервера vsftpd необхідно дозволити вхід в систему звичайним користувачам. Який з перерахованих нижче параметрів слід використовувати?", "anonymous_enable"]
,["При встановленні прав специфікатор ON *.* означає:", "Всі бази даних, всі таблиці"]
,["При зміні процесу відбувається перемикання", "Інша відповідь"]
,["При компіляції IL-коду в машинний код CLR виконує", "Верифікацію"]
,["При налаштуваннях за замовчуванням Squid приймає з’єднання на порту:", "3128"]
,["При наявності шару машинно-залежних компонентів ядра відбувається підміна реальної апаратури комп'ютера якоюсь уніфікованою віртуальною машиною, яка для всіх варіантів апаратної платформи є _____", "Однаковою"]
,["При організації віртуального хостингу WEB серверів який контейнер використовують для опису кожного WEB сервера в конфігураційному файлі сервера Apache?", "VirtualHost"]
,["При передачі параметрів у збережену процедуру дозволяється:", "Задавати декілька параметрів різних типів"]
,["При перейменуванні об’єкта бази даних привілей, прив’язаний до нього:", "Не буде виконуватись"]
,["При появі в системі більш пріоритетного готового до виконання потоку при обслуговуванні з відносними пріоритетами виконання поточного потоку _____", "не переривається"]
,["При створенні моделі класів доцільно розробляти і використовувати вже існуюче програмне забезпечення, яке утворює базис для сімейства схожих додатків. Таке сімейство, називається...", "каркасом"]
,["При створенні потоку ОС генерує спеціальну інформаційну структуру", "Дескриптор потоку"]
,["Призначення засобу Дозволи в системі безпеки Access 2003.", "Забезпечує доступ до об’єктів бази даних."]
,["Призначення конструктора як функції-члена класу полягає в тому, що ...", "Конструктор копіює об’єкти одного класу"]
,["Призначення конструктора як функції-члена класу полягає в тому, що ...", "Конструктор створює об’єкт класу"]
,["Призначення конструктора як функції-члена класу полягає в тому, що ...", "Конструктор ініціалізує дані-члени класу"]
,["Призначення оцінок управління полягає...", "Інша відповідь"]
,["Призначення програми Filigrana.exe", "Реалізація алгоритму стеганографії."]
,["Принцип PDCA (цикл Демінга-Шухарта):", "Інша відповідь"]
,["Приховування деталей реалізації називається", "Інкапсуляцією"]
,["Причинами створення груп є емоційна близькість, почуття, що поділяють люди, так стверджує", "теорія формування груп"]
,["Причинами створення груп є загальні установки та цінності, так стверджує", "теорія рівноваги"]
,["Причинами створення груп є отримання вигоди від співробітництва, так стверджує", "теорія обміну"]
,["Причинами створення груп є просторова та географічна близькість, так стверджує", "теорія близькості"]
,["Проблема оракула характеризується:", "Критерієм чи пройдено тест чи ні"]
,["Проведення документа може бути", "інша відповідь"]
,["Програмна оболонка, яка дозволяє керувати сайтом в режимі он-лайн, – це:", "система управління контентом"]
,["Продовжіть «CALS ...", "Описує сукупність принципів та технологій інформаційної підтримки життєвого циклу продукції на всіх його стадіях"]
,["Проекція відношення А на атрибути X, Y,..., Z (А [X, Y,..., Z]), де множина {X, Y,..., Z} є підмножиною повного списку атрибутів заголовка відношення А, являє собою", "Відношення з заголовком X, Y,..., Z і тілом, що містить кортежі відношення А, за винятком повторюваних кортежів"]
,["Простий (несегментированний) спонтанний перехід обов'язково має", "інший варіант"]
,["Простий (сегментований) перехід по події може мати", "інший варіант"]
,["Простий стан не може мати", "Двох або більше вихідних спонтанних переходів без сторожевої умови"]
,["Процес DMAIC це", "Визначення, вимірювання, аналіз, вдосконалення, управління"]
,["Процес аналізу і проектування, який розділяє застосування на апаратні і програмні компоненти – це:", "системна розробка"]
,["Процес представлення даних у вигляді простих двовимірних таблиць, який дозволяє усунути дублювання цих даних і забезпечує несуперечність збережених у базі даних, - це:", "Нормалізація таблиць"]
,["Процес тестування включає в себе", "концепції, стратегії, техніки, вимірювання тестування"]
,["Процес управління якістю включає", "Забезпечення якості, верифікацію та валідацію, рецензування, аудит"]
,["Процеси вирішення завдань управління якістю (за Юран)", "Планування якості, контроль якості, поліпшення якості"]
,["Під узгодженістю вимог розуміється:", "Несуперечливість вимог"]
,["Підберіть означення «порада для управління змінами»", "Порада для змін конфігурації"]
,["Підзапит - це", "Запит, що може входити в предикаті умови вибірки оператора SQL"]
,["Підходи в обробці розподілених даних", "Технологія тиражування"]
,["Підхід на основі кращих практик ґрунтується ...", "На відмові від моделі «як треба»"]
,["Після етапу формування вимог до системи виконується етап ...", "Розробка концепції системи"]
,["Реалізація системних викликів: використовуючи асемблер, програміст встановлює значення регістрів і / або областей пам'яті, а потім виконує спеціальну інструкцію виклику сервісу або програмного переривання для звернення до деякої", "Функції ОС"]
,["Результатом виконання запиту є:", "Відношення"]
,["Результатом ділення відношень R1 з атрибутами А і В на відношення R2 з атрибутом У (R1 DIVIDEBY R2), де А і В прості чи складені атрибути, причому атрибут У — загальний атрибут, визначений на тому самому домені (множині доменів складеного атрибута), є", "Відношення R із заголовком А і тілом, що складається з кортежів м таких, що у відношенні R1 є кортежі (м, s), причому множина значень s включає множину значень атрибута У відношення R2"]
,["Ресурси обробників переривань належать", "Інша відповідь"]
,["Роботи з тестування організовані в єдиний процес на основі врахування таких елементів:", "людей, інструментів, регламентів, кількісних оцінок"]
,["Розділення бази даних Access 2007 на файл даних та логіки.", "Робота з базами даних — База даних Access."]
,["Розробка логічної і фізичної структури сайту, компонування сторінки, верстальної структури, елементів навігації – це задачі наступного етапу розробки сайту:", "передпроектна підготовка"]
,["Розрізняють наступні типи конфліктів", "інша відповідь"]
,["Рядки таблиці у мові інфологічного моделювання ”Таблиці-зв`язки” - це", "Перелік атрибутів сутності"]
,["Рівень цілісності програмного забезпечення визначається...", "На підставі можливих наслідків збою програмного забезпечення та можливість виникнення такого збою"]
,["Рівні тестування тестів", "Над окремим модулем, групою модулів або системою, в цілому"]
,["Рівні цілісності пропонуються стандартом", "IEEE 1012-98"]
,["Різницею двох сумісних відношень R1 і R2 однакової розмірності (Rl MINUS R2) є відношення R, яке:", "Інша відповідь"]
,["С # -програми виконують операції введення-виведення за допомогою", "Потоків"]
,["Серія стандартів якості...", "ISO 9000"]
,["Сила взаємозв'язків між елементами модуля - це:", "зв'язність"]
,["Скільки виділяється оцінок «зрілості»", "5"]
,["Скільки етапів розвитку нараховують бази даних", "4"]
,["Скільки рекомендується використовувати атрибутів при першому впровадженні засобів керування змінами", "Не більше п’яти"]
,["Службовий файл веб-сайту, в якому описано правила індексації сайту для пошукових машин:", "robots.txt"]
,["Стандарт ДСТУ в якому визначено якості програмного забезпечення", "ДСТУ 2844-1994"]
,["Стандарт ДСТУ в якому визначено якості програмного забезпечення", "ДСТУ 2844-1994"]
,["Стандартними розділами класу в UML не є", "розділ властивостей"]
,["Створення в рамках однієї ОС декількох прикладних програмних середовищ дозволяє мати єдину версію програми і переносити її між різними", "ОС"]
,["Створення структурованої інформаційної моделі предметної області є метою:", "Інфологічного рівня проектування"]
,["Степінь відношення – це:", "Кількість стовбців"]
,["Стратегії інтеграційного тестування:", "«зверху-вниз», «знизу-вгору»"]
,["Сукупність команд, що часто використовуються як єдине ціле, - це:", "Збережені процедури"]
,["Сутність може мати:", "Декілька атрибутів"]
,["Сутність ПО, яку необхідно відображувати в БД з точки зору прикладної програми чи користувача БД – це:", "Інформаційний об’єкт"]
,["Сутність стеганографії.", "Прихована передача інформації."]
,["Таблиця, що не містить повторюваних полів і складових значень полів, як мінімум знаходиться в:", "Інша відповідь"]
,["Тестові сценарії розробляються:", "для перевірки функціональних вимог, для оцінки не функціональних вимог"]
,["Тестування належить до:", "Динамічних технік забезпечення якості програмних систем"]
,["Тестування, орієнтоване на дефекти:", "передбачення помилок, тестування мутацій"]
,["Технологія розподіленої бази даних", "Включає фрагменти даних, розташовані на різних вузлах мережі"]
,["Технологія розробки веб-інтерфейсів, що дає можливість браузеру взаємодіяти з веб- сервером без видимого для користувача перезавантаження сторінки, – це:", "AJAX"]
,["Технологія тиражування даних - це", "В кожному вузлі мережі дублюються дані всіх комп'ютерів"]
,["Техніки SQM можуть бути розподілені по категоріях на", "Інша відповідь"]
,["Техніки тестування орієнтовані на код", "тести, що базуються на блок-схемі, тести на основі потоків даних,"]
,["Техніки тестування, що базуються на аналізі подальшого використання", "операційний профіль, тестування на основі надійності інженерного процесу"]
,["Техніки тестування, що базуються на природі застосування", "об’єктно-орієнтоване тестування, компонентно-орієнтоване тестування"]
,["Техніки тестування, що базуються на специфікації", "еквівалентне розділення, аналіз граничних значень, таблиці прийняття рішень"]
,["Техніки управління якістю розділені на", "Статичні, динамічні"]
,["Типізація – це:", "Iнша відповідь"]
,["Традиційно негативний досвід випуску та тестування тільки великих релізів називають", "“big bang”"]
,["Тупикові ситуації не можуть вирішитися без впливу ззовні, тому в складі ОС повинні бути засоби їх", "Запобігання"]
,["У UML використовуються наступні типи подій (вкажіть зайве)", "подія створення"]
,["У базі знань використовуються знання:", "Алгоритмічні (процедурні) знання"]
,["У конструкторі базового класу для ініціалізації полів використовується параметр", "this"]
,["У науці зміст поняття “комунікація” тлумачать як", "інша відповідь"]
,["У об’єкті конфігурації Довідник дозволяється ієрархія:", "інша відповідь"]
,["У розгорнутому вигляді QFD включає стільки фаз", "4"]
,["У розподілених системах з декількома процесорами (кожен з яких має свою оперативну пам'ять) синхронізація може бути реалізована тільки за допомогою передачі", "Повідомлення"]
,["У С # виключення представляються", "Класами"]
,["У середовищі ОС з не витісняючою багатозадачністю, де програма використовує дані монопольно, знімається проблема", "Захисту даних"]
,["У стандарті IEEE 1028-97 представлено таку кількість типів перевірок і аудитів", "5"]
,["У чому відмінності значень специфікаторів для властивостей і методів?", "Відмінностей немає"]
,["У якому файлі визначається рівень виконання за замовчуванням під час завантаження системи", "/etc/inittab"]
,["Універсальна модель якості має такі характеристики:", "Функціональність, надійність, зручність застосування, ефективність, супроводжуваність, портативність"]
,["Управління обробкою виключень в C # грунтується на використанні оператора", "try"]
,["Утиліта для виконання адміністративних функцій:", "mysql"]
,["Формальні методи доведення програм поділяються на", "Інша відповідь"]
,["Формами взаємодії людини і групи є", "кооперація, злиття, конфлікт"]
,["Фрагмент ...FROM СКЛАД f... означає:", "Задання псевдоніму таблиці"]
,["Фрази HAVING та GROUP BY використовуються так:", "Фраза HAVING може використовуватися лише за наявності фрази GROUP BY"]
,["Фундаментальна модель CSS містить елементи:", "селектор, властивість, значення"]
,["Функція в РНР визначається наступним чином:", "function Ім'я_функції (параметри) \\{...\\}"]
,["Функція концепції ”тонкого клієнта”", "Інша відповідь"]
,["Функція РНР file() призначена для:", "зчитування даних"]
,["Функція-конструктор в РНР повинна мати ім'я:", "інша відповідь"]
,["Характеристика продукту формується К.Вігерсом як набір логічно зв’язаних...", "Функціональних вимог"]
,["Характерною особливістю HTML5 є:", "семантична розмітка"]
,["Хеш-таблиця, призначена для зберігання пар ключ / значення, носить назву", "Словник"]
,["Час дії пароля користувача (якщо цей параметр потрібний) слід вказувати", "у файлі /etc/shadow"]
,["Через що реалізується варіант використання:", "Через функцію системи"]
,["Чи дозволяється використовувати структури управління потоками даних у збережених процедурах і функціях?", "Так"]
,["Чим є подія з ймовірністю настання 100%?", "достовірною подією"]
,["Швидкість передачі при мережевій технологій 4G становить:", "від 100 Мбіт/с до 1Гбіт/с"]
,["Шифрування бази даних Access 2007.", "Відкриття в монопольному режимі - Робота з базами даних — Зашифрувати паролем - Введення та підтвердження пароля."]
,["Що визначають технологічні межі проекту?", "всі системи та існуючі інтерфейси, які пов’язані з реалізацією ІТ-проекту"]
,["Що визначають функціональні межі проекту?", "бізнес-направлення та бізнес-процеси, що охоплюються проектом автоматизації"]
,["Що з перерахованого є модулем Samba?", "smbd"]
,["Що може бути проміжним рішенням між електронним та паперовим варіантами прототипів UI класу?", "Презентації"]
,["Що може бути результатом робочого потоку «аналізу вимог»", "Набір артефактів"]
,["Що можна віднести до незапланованих змін вимог?", "Запропонування нової функціональності і суттєвої модифікації після затвердження базової версії вимог до проекту"]
,["Що означає операція * =?", "Множення з присвоєнням"]
,["Що робить процес комунікації двостороннім", "зворотній зв'язок"]
,["Що розуміти під «позолотою» продукту?", "Інша відповідь"]
,["Що таке Activity?", "вікно"]
,["Що таке WorkBreakdownStructure ?", "План робіт по створенню і розробці програмного продукту з деталізацією"]
,["Що таке WorkBreakdownStructure?", "Затвердження вимог до кінцевої АІС"]
,["Що таке емулятор?", "віртуальна машина, на якій запускається додаток"]
,["Що таке життєвий цикл проекту?", "послідовність фаз проекту через які він має пройти для гарантованого досягнення цілей проекту"]
,["Що таке ймовірність настання ризику в проекті?", "ймовірність того, що ризик настане"]
,["Що таке кількісний аналіз ризиків?", "оцінка ймовірності виникнення ризиків та розміри збитків/вигоди"]
,["Що таке мідлет?", "архів JAR"]
,["Що таке набір функціональних і не функціональних вимог, які розробники погоджуються реалізовувати у відповідній версії?", "Інша відповідь"]
,["Що таке повноваження?", "визначений набір функцій та повноважень в проекті, створений з метою розподілу обов’язків між членами команди проекту"]
,["Що таке повнота окремої вимоги", "Інша відповідь"]
,["Що таке повнота системи вимог?", "Властивість, яка означає, що сукупність артефактів, які описують вимоги, повність описує все те, що потрібно від системи, яка розробляється"]
,["Що таке проектна роль?", "визначений набір функцій та повноважень в проекті, створений з метою розподілу обов’язків між членами команди проекту"]
,["Що таке ризик проекту?", "кумулятивний ефект ймовірностей настання невизначених подій, здатних здійснити негативний або позитивний вплив на цілі проекту"]
,["Що являє собою колекція в C #?", "Групу об'єктів"]
,["Що із нижче перераховано включено в область процесів?", "Трасування"]
,["Що із перерахованого відповідає за забезпечення логіки обробки даних в інформаційній системі?", "Програмні засоби"]
,["Щоб показати, що клас є абстрактним, в UML застосовується", "курсив імені класу"]
,["Як називаються папки, в яких містяться графічні ресурси, призначені для різних розмірів екрану?", "drawable"]
,["Як називаються інструменти розробки додатків для мобільних платформ?", "SDK"]
,["Як називається архітектура розміщення елементів інтерфейсу користувача для конкретного вікна, що представляє Activity?", "інша відповідь."]
,["Як називається віртуальна машина, яка забезпечує середовище виконання Android додатків та компонентів ОС", "DVM"]
,["Як називається перелік основних подій, які повинні бути включені в розклад для моніторингу ходу виконання та управління проектом?", "список контрольних подій"]
,["Як називається проектна роль посадової особи, що відповідає за предметну область?", "інша відповідь"]
,["Як називається проектна роль посадової особи, що відповідає за стратегічне управління ходом реалізації проекту?", "інша відповідь"]
,["Як називається служба, що призначена для доступу до рядкових, графічних та інших типів ресурсів?", "інша відповідь."]
,["Як називається утиліта для розробки користувацького інтерфейсу у середовищі розробки Android Studio?", "інша відповідь"]
,["Як розраховується величина ризику?", "шляхом множення ймовірності виникнення ризику на відповідні наслідки"]
,["Яка активність називається головною?", "Інша відповідь"]
,["Яка діаграма показує статичну структуру проблемної області", "Інша відповідь"]
,["Яка з перерахованих дій має бути виконана раніше інших при розробці розкладу проекта?", "визначення переліку операцій, які повинні бути включені в розклад"]
,["Яка з перерахованих організаційних структур є ієрархічною", "Функціональна"]
,["Яка кількість стандартних ролей передбачена в SQL Server 2000.", "Інша відповідь."]
,["Яка методологія ґрунтується на постійному тісному контакті між Замовником та Виконавцем?", "XP"]
,["Яка операція застосовується для отримання типу?", "typedef"]
,["Яка операція здійснює перевірку приналежності типом?", "is"]
,["Яка програма за замовчуванням викликається ядром Linux для завантаження модулів?", "Insmod"]
,["Яка із запропонованих стратегій є ключовою? Яка із запропонованих стратегій є ключовою?", "Інтерв’ю з експертами"]
,["Яке з наведених нижче тверджень є вірним", "комунікація відбулася, якщо отримувач отримав, зрозумів і прийняв повідомлення"]
,["Яке представлення грає центральну роль при розробці архітектури системи RUP", "Представлення варіантів використання"]
,["Яке твердження не є вірним?", "якісний аналіз ризиків є повільним та дорогим способом встановлення пріоритетів ризиків"]
,["Яке твердження є вірним?", "при формуванні стратегії комунікацій враховується ступінь відповідальності/участі в проекті"]
,["Яке твердження є вірним?", "процес забезпечення якості включає методи безперервного покращення якості майбутніх проектів"]
,["Яке інтерв’ю передбачає детальне планування бесіди?", "Структуроване"]
,["Який аспект оцінювання реалізованості проекту дозволяє визначити, чи є запропоновані часові межі проекту реальними та досяжними?", "оцінка реалізованості проектного розкладу"]
,["Який атрибут вказує ім’я класу?", "android:name"]
,["Який елемент є кореневим елементом маніфесту?", "< manifest>"]
,["Який з, перерахованих нижче, видів комунікацій називають «виноградною лозою»", "неформальні комунікації"]
,["Який клас дозволяє розмістити декілька Активностей або Представлень в рамках одного екрану, використовуючи вкладки для перемикання між елементами?", "інша відповідь"]
,["Який клас інкапсулює обробку ресурсів, необхідних для підтримки елемента MapView всередині Активності у середовищі розробки Android Studio?", "інша відповідь"]
,["Який кластер працює з вимогами тестування", "Кластер тестування в фазі планування"]
,["Який кластер працює з вимогами тестування", "Кластер тестування в фазі розробки"]
,["Який метод викликається збирачем сміття безпосередньо перед видаленням об'єкта з пам'яті?", "Деструктор"]
,["Який метод можна використовувати для оцінювання трудомісткості та термінів розробки програмного забезпечення при наявності власного досвіду чи досвіду експертів, отриманого в схожих проектах ?", "метод PERT"]
,["Який метод повинна містити кожна консольна програма на мові С#?", "Main ()"]
,["Який перехід обумовлений настанням сторожових умов", "Альтернативний"]
,["Який прототип відсутній в класифікації Вігерса?", "Інша відповідь"]
,["Який процес являється механізмом сумування і фільтрації змін?", "Процес контролю змін"]
,["Який стандарт не поділяє поняття верифікації та валідації?", "Інша відповідь"]
,["Який тип бази даних підтримує доступ на основі стандарту SQL?", "Реляційного типу"]
,["Який тип даних усуває необхідність в заголовних та бібліотечних файлах при компіляції?", "Метадані"]
,["Який тип стратегії реагування на появу негативних ризиків виключає загрозу ризику шляхом передачі негативних загроз ризику з відповідальністю реагування на ризик третій стороні?", "передача ризику"]
,["Який файл оголошує ім'я Java-пакета додатку, який є унікальним ідентифікатором?", "AndroidManifest.xml"]
,["Який часовий резерв має послідовність операцій, що лежить на критичному шляху?", "нульовий"]
,["Який із аналізів вивчає взаємодію автоматизованої інформаційної системи і її середовища?", "Аналіз вимог"]
,["Яким типом даних є структура?", "Розмірним"]
,["Яким чином К. Вігерс увів поняття коректності вимог", "Через точність опису функціональності"]
,["Якою мовою є C #?", "Об'єктно-орієнтованою"]
,["Яку ймовірність виникнення повинна мати подія, щоб вона вважалася ризиком?", "ймовірність більше 0 і менше 100 %"]
,["Яку офіційну мову не включає в себе.NET Framework?", "Python"]
,["Яку програму слід виконати для того, щоб видалити програму з черги виконання демона atd?", "atrm"]
,["Яку роль виконує бізнес менеджер зі сторони виконавця?", "представляє виконавця в його договірних відносинах з замовником"]
,["Яку роль виконує менеджер проекту зі сторони виконавця?", "управління термінами, вартістю та якістю проекту"]
,["Якщо A, B, C, D - класи, то наступні системи композицій є допустимими:", "В"]
,["Якщо A, B, C, D - класи, то наступні системи композицій є неприпустимими", "Г"]
,["Якщо в програмі використовується покажчик на об'єкт класу, то конструктор класу буде викликано...", "Під час виділення динамічної пам'яті для об'єкта"]
,["Якщо виконується оновлення рядків таблиці, то в тригері допускається звернення до старих і нових значень рядків, що оновлюються?", "Так"]
,["Якщо деструктор визначений як зовнішній, то використовується специфікатор", "extern"]
,["Якщо деяка активність може бути перервана подією і може тривати необмежено довго, то така активність", "називається в UML діяльністю"]
,["Якщо деяка активність не може бути перервана подією і може тривати необмежено довго, то така активність", "не визначається і не використовується в UML"]
,["Якщо квант часу виконання процесу стане більшим, сумарні накладні витрати на диспетчеризацію процесів будуть", "Інша відповідь"]
,["Якщо керівники підрозділів забезпечують регулярний зворотній зв'язок з співробітниками та прислуховуються до їх думки, то це може привести до того, що", "співробітники  будуть  задоволені  роботою  і  підвищать  продуктивність  праці  та  якість виконання завдань "]
,["Якщо кожен елемент списку містить посилання на наступний елемент, такий список є", "інша відповідь"]
,["Якщо кратність полюса асоціації задана символами 0..1, то це означає, що", "не більше одного примірника класифікатора на даному полюсі асоціації бере участь у зв'язках, породжуваних асоціацією"]
,["Якщо кратність полюса асоціації задана символом *, то це означає, що", "невизначену кількість примірників класифікатора на даному полюсі асоціації бере участь у зв'язках, породжуваних асоціацією"]
,["Якщо метод не повертає ніякого значення, необхідно вказати тип", "void"]
,["Якщо програміст не вказав жодного конструктора, полям вказівкового типу присвоюється значення", "null"]
,["Якщо у полюса асоціації вказано кваліфікатор з кратністю 0..1, то це означає що", "кратність полюса дорівнює 0 або 1"]
,["Які блокування накладаються на дані, що обробляються в рамках транзакцій, визначає:", "Рівень ізоляції транзакції"]
,["Які відмінність інспекцій від оцінок (управлінської і технічної):", "Інша відповідь"]
,["Які документи проекту формуються на фазі ініціації проекту", "Концепція"]
,["Які діаграми використовуються для визначення границь системи", "Горизонтальні діаграми"]
,["Які з перерахованих бізнес-вигод проекту є найбільш визначеними?", "фінансові"]
,["Які з перерахованих бізнес-вигод проекту є найменш визначеними?", "якісні"]
,["Які з перерахованих дій повинні бути виконанні пізніше інших при розробці розкладу?", "визначення критичного шляху"]
,["Які з перерахованих навиків виконавців проекту відносять до адміністративних навиків?", "прийняття стратегічних рішень"]
,["Які з перерахованих навиків виконавців проекту відносять до технічних навиків?", "вміння управляти проектом та його технологією"]
,["Які з перерахованих функцій виконує архітектор системи?", "інша відповідь"]
,["Які особливості не властиві проектній організаційні структурі?", "Інша відповідь"]
,["Які особливості не властиві функціональній організаційній структурі?", "Інша відповідь"]
,["Які папки знаходяться у папці app?", "manifest, java, res"]
,["Які прототипи використовуються для демонстрації технічної здійсненності?", "Дослідницькі еволюційні"]
,["Які прототипи використовуються для прояснення і уточнення прикладів використання і функціональних вимог", "Поведінкові одноразові прототипи"]
,["Які ризики проекту неможливо визначити і неможливо спланувати дії з реагування на них?", "невідомі ризики"]
,["Які ролі в проекті не належать до виробничої групи:", "Інша відповідь"]
,["Які ролі в проекті не належать до групи аналізу:", "Інша відповідь"]
,["Які ролі в проекті не належать до групи забезпечення, яка, як правило не входить в команду проекту:", "Інша відповідь"]
,["Які твердження щодо статичних даних-членів класу правильні?", "Статична змінна–член класу оголошують в інтерфейсі класу зі специфікатором static"]
,["Які твердження щодо статичних даних-членів класу правильні?", "Статичні змінні-члени класу існують незалежно від будь-якого об’єкта класу"]
,["Якій структурі відповідає ступеневе представлення CMMS-SE/SW::Якій структурі відповідає ступеневе представлення CMMS-SE/SW", "SE-CMM"]
,["Якість ПЗ характеризується трьома головними аспектами", "Якість програмного продукту, якість процесів життєвого циклу, якість супроводу"]
,["Ім'я стереотипу в UML виділяється", "Лапками «»"]
,["Імені в UML не мають", "інший варіант"]
,["Інспекція програмного забезпечення...", "Аналіз та перевірка різних уявлень системи, програмного забезпечення і виконується на всіх етапах життєвого циклу розробки програмного забезпечення"]
,["Інсталяційні тести проводяться:", "для перевірки процедури інсталяції системи в цільовому оточені"]
,["Інтенсивність відмов це", "Частота появи відмов у програмному забезпеченні при її тестуванні або експлуатації"]
,["Інтерактивна розкадровка це:", "Одноразовий горизонтальний прототип"]
,["Інфраструктура процесу тестування включає", "Виділення об’єктів тестування, проведення класифікації,підготовка тестів, виконання , пошук помилок, служба проведення і керування процесом тестування, аналіз результатів тестування"]
,["Існують такі рівні тестування:", "модульне тестування, системне тестування, інтеграційне тестування"]
,["Об'єктно-орієнтоване програмування — це", "Iнша відповідь"]
]

for q,a in dd:
	print(f',["{q[:60]}","{a[:16]}"]')



import sys; sys.exit(1)
# res = len(list(set([i[:16] for i in dd]))
# print(f'res = {res}')
# print('\n'.join([i[:16] for i in dd]))













import sys; sys.exit(1)
for i in trs: # for i in soup.select('table#someid tr'):
	tds = i.findAll('td')

	name    = tds[0].font.a.text
	age     = tds[1].a.text
	salary  = i.select('a#salary').text
	person = Person(name, age, salary)
	print(person)

#############################################################
# Example 2 - tag+id
for a in soup.findAll('a#neededID'):
	print(a.text)


#############################################################
# Example 3 - tag+attributes
# TARGET -> <img class="big" row_type="black"> 
for img in soup.findAll('img', attrs={'class':'big', 'row_type':'black'}):
	print(img)

# Example 4 - take all a in div
result = []





































































import sys; sys.exit(1)
# improt pyqt5 or pyside2
import sys; qt_version_ = ''
try:
	import PyQt5; qt_version_ = 'q5' if not qt_version_ else qt_version_
except Exception as e: pass
try:
	import PySide2; qt_version_ = 's2' if not qt_version_ else qt_version_
except Exception as e: pass
if not qt_version_: sys.exit(1)



























import sys; sys.exit(1)
import PySimpleGUI as sg
from pprint import pprint

pprint([sg.T for i in range(3)])

























import sys; sys.exit(1)

layout = [
	[sg.T('Text'), sg.I('Name'), sg.B('Button1') ],
	[sg.T('Text'), sg.I('Age '), sg.B('Button2') ],
	[sg.T('Text'), sg.I('City'), sg.B('Button3') ],
]

window = sg.Window('Simple App, Really simple.', layout)

while True:
	event, values = window.Read()
	if event is None or event == 'Exit': break

	print(event, values)

	if event == 'Button1':
		pass
	if event == 'Button2':
		pass
	if event == 'Button3':
		pass


window.Close()
import sys; sys.exit(1)

def hello(name, age, dicksize) -> int:
	return 1234

print(hello('Mike', 55, 212412))




import sys; sys.exit(1)

#           One instance



import logging
logging.basicConfig( filename='example.log',
					 datefmt='%m.%d.%Y %I:%M:%S',
					 format='%(levelname)s \t: %(message)s',
					 level=logging.DEBUG)

logging.debug('1')
logging.error('2')
logging.info('3')


































































# import sys; sys.exit(1)
# import re
# READMEFILE = r'''


# The code is a crude representation of the GUI, laid out in text.
# ## Shortcut Functions / Multiple Function Names

# Many of the main method calls and Element names have shortcuts.  This enables you to code much quicker once you are used to using the SDK.  The Text Element, for example, has 3 different names `Text`, `Txt` or`T`.  InputText can also be written `Input` or `In` .  `FindElement` was recently renamed to `Element` because it's a commonly used function.


# <!-- %!% -->
# ## Text Element | `T == Txt == Text`
# Basic Element. It displays text. That's it.

# <!-- <+Text.doc+> -->


# ```python
# layout = [
#   [sg.Text('This is what a Text Element looks like')],
#   [sg.T('Second label')],
#  ]
# ```
# ![simple text](https://user-images.githubusercontent.com/13696193/44959877-e9d97b00-aec3-11e8-9d24-b4405ee4a148.jpg)

# <!-- <+Text.__init__+> -->

# ### Text Methods

# <!-- <+Text.Update+> -->

# ---
# <!-- <+Text.Update+> -->

# '''.split('\n')

# regex_pattern = re.compile(r'<!-- <\+[a-zA-Z_]+\.([a-zA-Z_]+)\+> -->')
# [i for i in READMEFILE if regex_pattern.match(i)]
#   if :
#       print(i)
# import sys; sys.exit(1)
# regex_pattern = re.compile(r'<\+\w+\.(\w+)\+>')
# # 2 Найди группы                      -> [part1, part2, part3]
# for index, i in enumerate(re.finditer(regex_pattern, READMEFILE)):
#   print(f'{index} - > {i.group(1)}')
	

# import sys; sys.exit(1)
# class Person(object):
#   """ """
#   def __init__(self, name, age=20, color='white', dicksize=None, width=180):
#       """

#       :param name: 
#       :param age: age of person (Default value = 20)
#       :param color:  (Default value = 'white')
#       :param dicksize:  (Default value = None)
#       :param width:  (Default value = 180)

#       """
#       self.name = name
#       self.age = age
#       self.color = color
#       self.width = width


# class Mike_Like(Person):
#   """ """
#   def __init__(self, name, age=55, color='IDK', dicksize=999, width=480):
#       """

#       :param name: 
#       :param age: age of person (Default value = 55)
#       :param color:  (Default value = 'IDK')
#       :param dicksize:  (Default value = 999)
#       :param width:  (Default value = 480)

#       """
#       self.name = name
#       self.age = age
#       self.color = color
#       self.width = width


# m1 = Mike_Like('john')
# m2 = Mike_Like('john')


















import sys; sys.exit(1)
for i in trs: # for i in soup.select('table#someid tr'):
	tds = i.findAll('td')

	name    = tds[0].font.a.text
	age     = tds[1].a.text
	salary  = i.select('a#salary').text
	person = Person(name, age, salary)
	print(person)

#############################################################
# Example 2 - tag+id
for a in soup.findAll('a#neededID'):
	print(a.text)


#############################################################
# Example 3 - tag+attributes
# TARGET -> <img class="big" row_type="black"> 
for img in soup.findAll('img', attrs={'class':'big', 'row_type':'black'}):
	print(img)

# Example 4 - take all a in div
result = []





































































import sys; sys.exit(1)
# improt pyqt5 or pyside2
import sys; qt_version_ = ''
try:
	import PyQt5; qt_version_ = 'q5' if not qt_version_ else qt_version_
except Exception as e: pass
try:
	import PySide2; qt_version_ = 's2' if not qt_version_ else qt_version_
except Exception as e: pass
if not qt_version_: sys.exit(1)



























import sys; sys.exit(1)
import PySimpleGUI as sg
from pprint import pprint

pprint([sg.T for i in range(3)])

























import sys; sys.exit(1)

layout = [
	[sg.T('Text'), sg.I('Name'), sg.B('Button1') ],
	[sg.T('Text'), sg.I('Age '), sg.B('Button2') ],
	[sg.T('Text'), sg.I('City'), sg.B('Button3') ],
]

window = sg.Window('Simple App, Really simple.', layout)

while True:
	event, values = window.Read()
	if event is None or event == 'Exit': break

	print(event, values)

	if event == 'Button1':
		pass
	if event == 'Button2':
		pass
	if event == 'Button3':
		pass


window.Close()
import sys; sys.exit(1)

def hello(name, age, dicksize) -> int:
	return 1234

print(hello('Mike', 55, 212412))




import sys; sys.exit(1)

#           One instance



import logging
logging.basicConfig( filename='example.log',
					 datefmt='%m.%d.%Y %I:%M:%S',
					 format='%(levelname)s \t: %(message)s',
					 level=logging.DEBUG)

logging.debug('1')
logging.error('2')
logging.info('3')


































































import sys; sys.exit(1)
import re
READMEFILE = r'''


The code is a crude representation of the GUI, laid out in text.
## Shortcut Functions / Multiple Function Names

Many of the main method calls and Element names have shortcuts.  This enables you to code much quicker once you are used to using the SDK.  The Text Element, for example, has 3 different names `Text`, `Txt` or`T`.  InputText can also be written `Input` or `In` .  `FindElement` was recently renamed to `Element` because it's a commonly used function.


<!-- %!% -->
## Text Element | `T == Txt == Text`
Basic Element. It displays text. That's it.

<!-- <+Text.doc+> -->


```python
layout = [
  [sg.Text('This is what a Text Element looks like')],
  [sg.T('Second label')],
 ]
```
![simple text](https://user-images.githubusercontent.com/13696193/44959877-e9d97b00-aec3-11e8-9d24-b4405ee4a148.jpg)

<!-- <+Text.__init__+> -->

### Text Methods

<!-- <+Text.Update+> -->

---
<!-- <+Text.Update+> -->

'''.split('\n')

regex_pattern = re.compile(r'<!-- <\+[a-zA-Z_]+\.([a-zA-Z_]+)\+> -->')
[i for i in READMEFILE if regex_pattern.match(i)]
import sys; sys.exit(1)
regex_pattern = re.compile(r'<\+\w+\.(\w+)\+>')
# 2 Найди группы                        -> [part1, part2, part3]
for index, i in enumerate(re.finditer(regex_pattern, READMEFILE)):
	print(f'{index} - > {i.group(1)}')
	

import sys; sys.exit(1)
class Person(object):
	""" """
	def __init__(self, name, age=20, color='white', dicksize=None, width=180):
		"""

		:param name: 
		:param age: age of person (Default value = 20)
		:param color:  (Default value = 'white')
		:param dicksize:  (Default value = None)
		:param width:  (Default value = 180)

		"""
		self.name = name
		self.age = age
		self.color = color
		self.width = width


class Mike_Like(Person):
	""" """
	def __init__(self, name, age=55, color='IDK', dicksize=999, width=480):
		"""

		:param name: 
		:param age: age of person (Default value = 55)
		:param color:  (Default value = 'IDK')
		:param dicksize:  (Default value = 999)
		:param width:  (Default value = 480)

		"""
		self.name = name
		self.age = age
		self.color = color
		self.width = width


m1 = Mike_Like('john')
m2 = Mike_Like('john')





