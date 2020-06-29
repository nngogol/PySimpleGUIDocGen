import PySimpleGUIDocGen.db.PySimpleGUIlib as tk_lib
from inspect import *; import re, os, importlib

def get_code(obj):
	# get source code from module object or path-like str, that contains sorce for module
	if 'module' in str(type(obj)): file_path, module_name = obj.__file__, obj.__name__
	elif 'str' in str(type(obj)): file_path, module_name = obj, os.path.splitext(os.path.basename(obj))[0]
	else: return ''

	spec = importlib.util.spec_from_file_location(module_name, file_path)
	module = importlib.util.module_from_spec(spec) # spec.loader.exec_module(module)
	return ''.join(getsourcelines(module)[0])

#####################################################################
#                         _           _     _                       #
#                        | |         | |   | |                      #
#    __   __     ___  ___| | ___  ___| |_  | |__   ___ _ __ ___     #
#    \ \ / /    / __|/ _ \ |/ _ \/ __| __| | '_ \ / _ \ '__/ _ \    #
#     \ V /     \__ \  __/ |  __/ (__| |_  | | | |  __/ | |  __/    #
#      \_/      |___/\___|_|\___|\___|\__| |_| |_|\___|_|  \___|    #
#                                                                   #
#                                                                   #
#####################################################################
# 1) Change string to 'qt' or 'wx' or 'web' to get different docs
# 2) ofile = version_type + 'alabama.txt' word
WHAT_DO_I_WANT = 'qt'                   # 1
ofile = WHAT_DO_I_WANT + 'alabama.txt'  # 2

if WHAT_DO_I_WANT == 'qt': 		import dbQt.PySimpleGUIQtlib as target_lib
if WHAT_DO_I_WANT == 'wx': 		import dbWx.PySimpleGUIWxlib as target_lib
if WHAT_DO_I_WANT == 'web': 	import dbWeb.PySimpleGUIWeblib as target_lib

tk_members, tg_members = getmembers(tk_lib), getmembers(target_lib)
# ---------------------
tk_funcs       = [o for o in tk_members if isfunction(o[1])]
tk_classes     = [o for o in tk_members if isclass(o[1])]
tk_classes_    = list(set([i[1] for i in tk_classes])) # filtering
tk_classes     = list(zip([i.__name__ for i in tk_classes_], tk_classes_))
# ---------------------
tg_funcs       = [o for o in tg_members if isfunction(o[1])]
tg_classes     = [o for o in tg_members if isclass(o[1])]
tg_classes_    = list(set([i[1] for i in tg_classes])) # filtering
tg_classes     = list(zip([i.__name__ for i in tg_classes_], tg_classes_))

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
#==#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

# classes
tk_objs     = {name:obj for name, obj in tk_classes} # in tk_funcs} # funcs
target_objs = {name:obj for name, obj in tg_classes} # in tg_funcs} # funcs

# 						   "to" - qt wx web 		"was" - tk
overlay_func_objs = {name:{'to': target_objs[name], 'was':psg_obj} for name, psg_obj in tk_objs.items() if name in target_objs}
overlay_clas_objs = {name:{'to': target_objs[name], 'was':psg_obj} for name, psg_obj in tk_objs.items() if name in target_objs}

tcode = get_code(target_lib) # qt wx web

for class_name, val in overlay_clas_objs.items():
	print(f'doing {class_name}', end=' ')
	
	tclas_doc, tinit_doc = val['to'].__doc__, val['to'].__init__.__doc__
	if tclas_doc == None: tclas_doc = ''
	if tinit_doc == None: tinit_doc = ''

	regex_pattern_find 	= re.compile(r'(class ' + class_name+ r'\(Element\):)\s*\n*([\d\D]*?)\n*?\s*?(def __init__[\d\D]*?:)\s*?\n*?([\d\D]*?)\n*?\s*?self')
	tcode = re.sub(regex_pattern_find, r"\1 \n    '''" + tclas_doc + r"\n    '''\n\t\3\n    '''"+ tinit_doc + r"\n    '''\n    self", tcode)
	print('ok')

with open(ofile, 'w', encoding='utf-8') as ff: ff.write(tcode)