
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




if __name__ == "__main__":
	data = CF_insight()
	from pprint import pprint
	pprint(data)
