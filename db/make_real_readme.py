from inspect import getmembers, isfunction, isclass, getsource, signature, _empty
from datetime import datetime
import PySimpleGUIlib
import click, logging, json, re, os

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

	# ▓▓▓▓ making dict
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

def get_sig_table_parts(function_obj, function_name, doc_string):
	"""
	Convert "function + __doc__" tp "method call + params table" in MARKDOWN
	"""

	doc_string = doc_string.strip()

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▒   ▒ 		   Making INIT_CALL   		 ▒   ▒ #
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# where the magic begins
	sig, rows = signature(function_obj).parameters, []
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
	sig_content = ',\n\t'.join(rows)
	sign = f"\n```python\n{function_name}({sig_content})\n```"
	# where the magic stops, for real.


	# --------------
	# SPECIAL CASES
	# --------------
	params_names = list(dict(sig).keys())
	if 'self' in params_names and params_names[0] == params_names[-1] and not doc_string:
		"""
		def Get(self):
			''' '''
		
		->
		Get() - method
		"""
		return f'\n\n{function_name}() - method\n\n', ''
	if 'self' in params_names and params_names[0] == params_names[-1] and doc_string and ':param' not in doc_string:
		"""
		def Get(self):
			''' bla bla'''
		
		->
		Get() - bla bla 
		"""
		return f'\n\n{function_name}() - {doc_string}\n\n' , ''

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▒   ▒- 		Making params_TABLE			 ▒   ▒-#
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	md_table =  '\n'.join([ 	f'|{name}|{desc}|'
								for name, desc in
								get_params_part(doc_string).items()])
	params_TABLE = f'''\nParameters explained:\n
						|Name|Meaning|
						|---|---|
						{md_table}
						\n'''.replace('\t', '')
	
	if not md_table.strip():
		params_TABLE = ''


	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▒   ▒- 		return value parsing 		 ▒   ▒-#
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	return_guy      = [i.strip() for i in doc_string.split('\n') if ':return:' in i]
	if not return_guy:
		return_guy = ''
	else:
		return_guy = return_guy[0].strip()[8:]
		return_guy = f'\n\nreturn value: {return_guy}\n'

	return sign, params_TABLE + return_guy

####################################################################################################################
#     ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______     #
#    |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    #
#     ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______     #
#    |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    #
#                                                                                                                  #
####################################################################################################################
# injection_points
"""
injection_point structure cal look like this:

FUNCTION

	{
		"tag" : "<!-- <+func.hello+> -->",
		"function_object" : "<function hello at 0x7fdcfd888ea0>",
		"parent_class" : None,
		"part1" : "func",
		"part2" : "hello",
		"number" : ""
	}
	{
		"tag" : "<!-- <+func.1hello+> -->",
		"function_object" : "<function hello at 0x7fdcfd888ea0>",
		"parent_class" : None,
		"part1" : "func",
		"part2" : "hello",
		"number" : "1"
	}

CLASS

	{
		"tag" : "<!-- <+Mike_Like.__init__+> -->",
		"function_object" : <function Mike_Like.__init__ at 0x7fdcfd888ea0>,
		"parent_class" : <class '__main__.Mike_Like'>,
		"part1" : "Mike_Like",
		"part2" : "__init__",
		"number" : ""
	}
	{
		"tag" : "<!-- <+Mike_Like.2__init__+> -->",
		"function_object" : <function Mike_Like.__init__ at 0x7fdcfd888ea0>,
		"parent_class" : <class '__main__.Mike_Like'>,
		"part1" : "Mike_Like",
		"part2" : "__init__",
		"number" : "2"
	}

"""
####################################################################################################################
#     ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______     #
#    |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    #
#     ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______     #
#    |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    #
#                                                                                                                  #
####################################################################################################################

def pad_n(text): return f'\n{text}\n'

def render(injection):
	if injection['part1'] == 'func': # function
		sig, table = get_sig_table_parts(function_obj=injection['function_object'],
							function_name=injection['part2'],
							doc_string=injection['function_object'].__doc__)
	else: # class method
		function_name = injection['parent_class'].__name__ if injection['part2'] == '__init__' else injection['part2']
		sig, table = get_sig_table_parts(function_obj=injection['function_object'],
							function_name=function_name,
							doc_string=injection['function_object'].__doc__)

	if injection['number'] == '':  return pad_n(sig) + pad_n(table)
	if injection['number'] == '1': return pad_n(sig)
	if injection['number'] == '2': return pad_n(table)

def readfile(fname):
	with open(fname, 'r', encoding='utf-8') as ff:
		return ff.read()

def main(do_full_readme=False, files_to_include:list=[], logger=None, output_name=None, delete_html_comments=True):
	"""
	Goal is:
	1) load 1_ 2_ 3_ 4_
	2) get memes - classes and functions in PSG
	3) find all tags in 2_
	4) structure tags and REAL objects
	5) replaces classes, functions.
	6) join 1 big readme file
	"""

	# if logger == None: raise Exception('give me a logger')

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 1 loading files
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	HEADER_top_part 		= readfile('1_HEADER_top_part.md') 	# 1
	readme 					= readfile('2_readme.md') 			# 2
	FOOTER 					= readfile('3_FOOTER.md') 			# 3
	Release_notes 			= readfile('4_Release_notes.md') 	# 4
	
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 2 GET classes, funcions, varialbe a.k.a. memes
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	psg_members = getmembers(PySimpleGUIlib)

	psg_funcs 		= [o for o in psg_members if isfunction(o[1])]
	psg_classes 	= [o for o in psg_members if isclass(o[1])]
	psg_classes_	 = list(set([i[1] for i in psg_classes])) # filtering
	psg_classes		= list(zip([i.__name__ for i in psg_classes_], psg_classes_))

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓                       | |	▓▓▓▓▓
	# ▓▓▓▓   _ __ ___   ___  __ _| |_	▓▓▓▓▓
	# ▓▓▓▓  | '_ ` _ \ / _ \/ _` | __|	▓▓▓▓▓
	# ▓▓▓▓  | | | | | |  __/ (_| | |_  	▓▓▓▓▓
	# ▓▓▓▓  |_| |_| |_|\___|\__,_|\__|	▓▓▓▓▓

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 3 find all tags in 2_readme
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# strip top of the file head
	started_mark = '<!-- Start from here -->'; readme = readme[readme.index(started_mark)+len(started_mark):]

	# find with regex
	regex_pattern = re.compile(r'<!-- <\+[a-zA-Z_]+\.([a-zA-Z_]+)\+> -->'); mark_points = [i for i in readme.split('\n') if regex_pattern.match(i)]

	# if there are REPEATED tags -> show them.
	if len(list(set(mark_points))) != len(mark_points):
		[mark_points.remove(x) for x in set(mark_points)];
		if logger: logger.error("You have repeated tags! \n {0}".format(','.join(mark_points)))
		return ''

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 4 structure tags and REAL objects
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓

	injection_points = []
	classes_method_tags = [ j for j in mark_points if 'func.' not in j]
	func_tags = [ j for j in mark_points if 'func.' in j]
	
	# ░▒▓◘◘◘▓ functions ▓◘◘◘▓▒░
	for tag in func_tags:

		try:
			__, function_name = tag.split('.')
			function_name = function_name.split('+')[0]
			part2 = function_name

			# ░▒▓ filter number ▓▒░
			number = ''
			if part2[0] in ['1', '2']:
				number, part2 = part2[0], part2[1:]

			# ░▒▓ find function ▓▒░
			founded_function = [func for func_name, func in psg_funcs if func_name == function_name]
			if not founded_function:
				if logger: logger.error(f'function "{function_name}" not found in PySimpleGUI')
				continue
			if len(founded_function) > 1 :
				if logger: logger.error(f'more than 1 function named "{function_name}" found in PySimpleGUI')
				continue

			# ░▒▓ collect ▓▒░
			injection_points.append({
				"tag" : tag,
				"function_object" : founded_function[0],
				"parent_class" : None,
				"part1" : 'func',
				"part2" : part2,
				"number" : number,
			})
		except Exception as e:
			if logger: logger.error(f'               {str(e)}')
			continue

	# ░▒▓◘◘◘▓ classes ▓◘◘◘▓▒░
	for tag in classes_method_tags:
		try:
			class_name, method_name = tag.split('.')
			class_name, method_name = class_name.split('+')[-1], method_name.split('+')[0]
			part1, part2 = class_name, method_name
			
			# ░▒▓ filter number ▓▒░
			number = ''
			if part2[0] in ['1', '2']:
				number, method_name = part2[0], part2[1:]

			
			# ░▒▓ find class ▓▒░
			founded_class = [a_class_obj for a_class_name, a_class_obj in psg_classes if a_class_name == class_name]
			if not founded_class:
				if logger: logger.error(f'class "{tag}" not found in PySimpleGUI')
				continue
			if len(founded_class) > 1 :
				if logger: logger.error(f'more than 1 class named "{tag}" found in PySimpleGUI')
				continue

			# ░▒▓ find method ▓▒░
			try:
				if method_name != 'doc':
					founded_method = getattr(founded_class[0], method_name)
				else:
					founded_method = None
			except AttributeError as e:
				if logger: logger.error(f'METHOD not found!: {str(e)}')
				continue
			except Exception as e:
				if logger: logger.error(str(e))
				continue

			# ░▒▓ collect ▓▒░
			injection_points.append({
				"tag" : tag,
				"function_object" : founded_method,
				"parent_class" : founded_class[0],
				"part1" : part1,
				"part2" : part2,
				"number" : number,
			})
		except Exception as e:
			if logger: logger.error(f'```````````````````````{str(e)}')
			continue

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 5 injecting
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓

	for injection in injection_points:

		if injection['part2'] == 'doc': # our special snowflake "doc"
			readme = readme.replace(injection['tag'], injection['parent_class'].__doc__)
		else:
			readme = readme.replace(injection['tag'], render(injection))

	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓
	# ▓▓▓▓▓▓▓▓▓▓▓▓ 6 join
	# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓

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

			# ░▒▓ html removing ▓▒░
			if delete_html_comments:
				if logger: logger.info('Deleting html comments')
				
				# remove html comments
				stackedit_data = content[content.index('<!--stackedit_data:'):]
				filtered_readme_file = re.sub(r'<!--([\s\S]*?)-->', '\n', content, flags=re.MULTILINE)
				filtered_readme_file += stackedit_data
				filtered_readme_file = filtered_readme_file.replace('\n\n\n', '\n\n')
				filtered_readme_file = filtered_readme_file.replace('\n\n\n', '\n\n')
				filtered_readme_file = filtered_readme_file.replace('\n\n\n', '\n\n')
				filtered_readme_file = filtered_readme_file.replace('\n\n\n', '\n\n')
				content = filtered_readme_file.replace('\n\n\n', '\n\n')

			ff.write(content)

		return content


@click.command()
@click.option('-nol', '--no_log',  					is_flag=True, help='Disable log')
@click.option('-rml', '--delete_log', 				is_flag=True, help='Delete log file after generating')
@click.option('-rmh', '--delete_html_comments', 	is_flag=True, help='Delete html comment in the generated .md file')
@click.option('-o', '--output_name', 				default='FINALreadme.md',	type=click.Path(), help='Name for generated .md file')
@click.option('-lo', '--log_file', 					default='LOGS.log',			type=click.Path(), help='Name for log file')
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
	logger.info('STARTING')

	main(logger=logger,
		files_to_include=[0,1,2,3],
		output_name=output_name,
		delete_html_comments=delete_html_comments)

	logger.info('FINISHED')


	# --------------------
	# ----- POST process-- 
	# --------------------

	if delete_log:
		# delete log file
		log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
		if os.path.exists(log_file):
			try:
				os.remove(log_file)
			except Exception as e:
				print(str(e))

if __name__ == '__main__':
	cli()
