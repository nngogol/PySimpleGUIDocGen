import subprocess,re,datetime,time,os,platform,json,PySimpleGUI as sg; from subprocess import Popen; from make_real_readme import main
cd = os.path.dirname(os.path.abspath(__file__))

def readfile(filename):
	with open(filename, 'r', encoding='utf-8') as ff: return ff.read()
def writefile(fpath, content):
	with open(fpath, 'w', encoding='utf-8') as ff: ff.write(content)
def writejson(a_path:str, a_dict:dict) -> None:
	with open(a_path, 'w', encoding='utf-8') as output_file: json.dump(a_dict, output_file, ensure_ascii=False, indent=2)
def readjson(a_path:str) -> dict:
	with open(a_path, 'r', encoding='utf-8') as f: return json.load(f)


def openfile(a_path):
	# File exists?
	if not os.path.exists(a_path): return sg.Popup(f"Error! This file doesn't exists: {a_path}")

	# check: OS
	if 'Windows' in platform.system():
		os.startfile(a_path)

	elif 'Linux' in platform.system():
		Popen(f'exo-open "{a_path}"', shell=True)

def opendir(a_path):
	# Folder exists?
	if not os.path.exists(a_path): return sg.Popup(f"Error! This directory doesn't exists: {a_path}")

	try:
		# check: OS
		if 'Windows' in platform.system():
			os.startfile(a_path)
		elif 'Linux' in platform.system():
			Popen(f'exo-open --launch FileManager --working-directory "{a_path}"', shell=True)
	except Exception as e:
		sg.Popen(f"Error, can't open a file: '{e}'")


########################################################################
#                              __ _            _                       #
#                             / _(_)          | |                      #
#    __   __   ___ ___  _ __ | |_ _  __ _     | |__   ___ _ __ ___     #
#    \ \ / /  / __/ _ \| '_ \|  _| |/ _` |    | '_ \ / _ \ '__/ _ \    #
#     \ V /  | (_| (_) | | | | | | | (_| |    | | | |  __/ | |  __/    #
#      \_/    \___\___/|_| |_|_| |_|\__, |    |_| |_|\___|_|  \___|    #
#                                    __/ |                             #
#                                   |___/                              #
########################################################################
def load_configs(): return readjson(os.path.join(cd, 'app_configs.json'))
def save_configs(a_config:dict): writejson(os.path.join(cd, 'app_configs.json'), a_config)



APP_CONFIGS = load_configs()
README_OFILENAME = APP_CONFIGS['README_FILENAME']
CALL_REFERENCE_OFILENAME = APP_CONFIGS['CALL_REFERENCE_FILENAME']


##-#-#-# ##-#-#-#
# Post-process logic
##-#-#-# ##-#-#-#
insert_md_section_for__class_methods = False
remove_repeated_sections_classmethods = False

class BESTLOG(object):
	def __init__(self, filename):
		# my_file = logging.FileHandler(filename, mode='w')
		# my_file.setLevel(logging.DEBUG)
		# my_file.setFormatter(logging.Formatter('%(asctime)s>%(levelname)s: %(message)s'))
		# logger = logging.getLogger(__name__)
		# logger.setLevel(logging.DEBUG)
		# logger.addHandler(my_file)
		self.filename = filename
		self.json_name = filename + '.json'
		self.error_list = []
		self.warning_list = []
		self.info_list = []
		self.debug_list = []
		self.tick_amount=1
		self.names = self.messages_names = 'error warning info debug'.split(' ')

	def tick(self):
		self.tick_amount+=1
		return self.tick_amount

	#######################################################################
	#      __             _                             _ _               #
	#     / _|           | |                           (_) |              #
	#    | |_ ___  _ __  | |_ _ __ __ _ _ __  ___ _ __  _| | ___ _ __     #
	#    |  _/ _ \| '__| | __| '__/ _` | '_ \/ __| '_ \| | |/ _ \ '__|    #
	#    | || (_) | |    | |_| | | (_| | | | \__ \ |_) | | |  __/ |       #
	#    |_| \___/|_|     \__|_|  \__,_|_| |_|___/ .__/|_|_|\___|_|       #
	#                                            | |                      #
	#                                            |_|                      #
	#######################################################################
	def error(self, m, metadata={}):
		self.error_list.append([self.tick(), m, metadata])
	def warning(self, m, metadata={}):
		self.warning_list.append([self.tick(), m, metadata])
	def info(self, m, metadata={}):
		self.info_list.append([self.tick(), m, metadata])
	def debug(self, m, metadata={}):
		self.debug_list.append([self.tick(), m, metadata])

	##########################################
	#      __                                #
	#     / _|                               #
	#    | |_ ___  _ __   _ __ ___   ___     #
	#    |  _/ _ \| '__| | '_ ` _ \ / _ \    #
	#    | || (_) | |    | | | | | |  __/    #
	#    |_| \___/|_|    |_| |_| |_|\___|    #
	#                                        #
	#                                        #
	##########################################
	def tolist(self):    return zip([self.error_list, self.warning_list, self.info_list, self.debug_list], self.names)
	def todict(self):    return {'error' : self.error_list, 'warning' : self.warning_list, 'info' : self.info_list, 'debug' : self.debug_list}
	
	def save(self):
		'''
		{
			'message_type' : message_type,
			'message_text' : m_text,
			'message_time' : m_time,
			'message_metadata' : m_metadata
		}
		'''
		all_messages_list = []
		for messages, message_type in self.tolist():
			results_ = [{'message_type' : message_type,
						'message_text' : m_text,
						'message_time' : m_time,
						'message_metadata' : m_metadata}
						for m_time, m_text, m_metadata in messages]
			all_messages_list.extend(results_)

		# sort messages on time
		all_messages_list = sorted(all_messages_list,
							key=lambda x: x['message_time'])
		
		# convert time
		# for i in all_messages_list: i['message_time'] = i['message_time'].strftime('%Y-%m-%d %H:%M:%S.%f')

		writejson(self.json_name, all_messages_list)
	def load(self, **kw):
		'''
			return dict with messages
			
			kw = {
				use_psg_color : bool
				show_time : bool
			}
		'''

		# plan:
		# read json, convert time

		# read
		all_messages_list = readjson(self.json_name)
		# convert time
		# for i in all_messages_list: i['message_time'] = datetime.datetime.strptime(i['message_time'], '%Y-%m-%d %H:%M:%S.%f')

		def format_message(message):
			if kw['show_time']:
				return str(message['message_time']) + ':' + message['message_text'] 
			else:
				return message['message_text']


		#=========#
		# 4 lists #
		#=========#
		error_list =   [i for i in all_messages_list if i['message_type'] == 'error']
		warning_list = [i for i in all_messages_list if i['message_type'] == 'warning']
		info_list =    [i for i in all_messages_list if i['message_type'] == 'info']
		debug_list =   [i for i in all_messages_list if i['message_type'] == 'debug']


		#=================#
		# and 1 more list #
		#=================#
		# colors = {'warning' : 'magenta', 'info' : 'black'}
		colors = {'warning' : 'blue', 'info' : 'black'}
		warning_info_ = []
		for message in sorted(warning_list + info_list, key=lambda x: x['message_time']):
			if kw['use_psg_color']:
				warning_info_.append([   format_message(message),
										colors.get(message['message_type'])   ])
			else:
				warning_info_.append(format_message(message))

		error_list = [format_message(i) for i in error_list]
		warning_list = [format_message(i) for i in warning_list]
		info_list = [format_message(i) for i in info_list]
		debug_list = [format_message(i) for i in debug_list]

		return error_list, warning_list, info_list, debug_list, warning_info_
	def load_to_listbox(self):
		'''
		read .json
		'''
		return sorted(readjson(self.json_name),
					  key=lambda x: x['message_time'])

def compile_call_ref(output_filename='output/LoG_call_ref', **kw):
	''' Compile a "5_call_reference.md" file'''

	log_obj = BESTLOG(os.path.join(cd, output_filename))
	
	main(logger=log_obj,
		 main_md_file='markdown input files/5_call_reference.md',
		 insert_md_section_for__class_methods=insert_md_section_for__class_methods,
		 remove_repeated_sections_classmethods=remove_repeated_sections_classmethods,
		 files_to_include=[],
		 output_name=CALL_REFERENCE_OFILENAME,
		 delete_html_comments=True)
	log_obj.save()
	return log_obj.load(**kw), log_obj.load_to_listbox()

def compile_readme(output_filename='output/LoG', **kw):
	''' Compile a "2_readme.md" file'''
	log_obj = BESTLOG(os.path.join(cd, output_filename))
	main(logger=log_obj,
		 insert_md_section_for__class_methods=insert_md_section_for__class_methods,
		 remove_repeated_sections_classmethods=remove_repeated_sections_classmethods,
		 files_to_include=[0, 1, 2, 3],
		 output_name=README_OFILENAME,
		 delete_html_comments=True)
	log_obj.save()
	return log_obj.load(**kw), log_obj.load_to_listbox()

def compile_all_stuff(**kw):
	'''
		Compile a "2_ and 5_" .md filess
		return output from them
	'''
	return compile_readme(**kw), compile_call_ref(**kw)


########################################
#     _____                            #
#    |  __ \                           #
#    | |__) |__  _ __  _   _ _ __      #
#    |  ___/ _ \| '_ \| | | | '_ \     #
#    | |  | (_) | |_) | |_| | |_) |    #
#    |_|   \___/| .__/ \__,_| .__/     #
#               | |         | |        #
#               |_|         |_|        #
########################################

def md2psg(target_text):
	# target = 'This is **bold** and *italic* words'
	#              V
	# sg.T('This is '), sg.T('bold', font=...bold), ...'

	# imports
	from collections import namedtuple
	spec = namedtuple('spec', 'char text'.split(' '))

	# START
	# =====
	parts = re.compile(r'([\*]{1,2})([\s\S]*?)([\*]{1,2})', flags=re.M|re.DOTALL).split(target_text)
	chuncks, skip_this = [], 0
	for index, part in enumerate(parts):
		if skip_this != 0:
			skip_this -= 1; continue

		if part not in ['*', '**']: chuncks.append(part)
		else:
			skip_this = 2
			chuncks.append(spec(part, parts[index+1]))

	font_norm = ('Mono 13 ')     # (*sg.DEFAULT_FONT, 'italic')
	font_bold = ('Mono 13 italic')     # (*sg.DEFAULT_FONT, 'italic')
	font_ita  = ('Mono 13 bold')       # (*sg.DEFAULT_FONT, 'bold')
	
	list_of_Ts = []
	for chunck in chuncks:
		if type(chunck) is str:     list_of_Ts.append(sg.T(chunck, font=font_norm, size=(len(chunck), 1), pad=(0,0)))
		elif type(chunck) is spec:
			if chunck.char == '*':  list_of_Ts.append(sg.T(chunck.text, font=font_ita, pad=(0,0), size=(len(chunck.text), 1)))
			if chunck.char == '**': list_of_Ts.append(sg.T(chunck.text, font=font_bold,  pad=(0,0), size=(len(chunck.text), 1)))
	return list_of_Ts


def mini_GUI():
	my_font = ("Helvetica", 12)
	my_font2 = ("Helvetica", 12, "bold")
	my_font3 = ("Helvetica", 15, "bold")
	my_font4 = ("Mono", 18, "bold")

	def make_tab(word):

		def tabs(*layouts):
			return sg.TabGroup( 
				[[ sg.Tab(title, lay, key=f'-tab-{word_}-{index}-')
					for index, (title, word_, lay) in enumerate(layouts)
				]]
			)

		return [[
			sg.Column(layout=[
				[sg.T('debug', font=my_font, text_color='blue')],
				[sg.ML(size=(50-15, 15), key=f'-{word}-debug-')],
				[sg.T('error', font=my_font, text_color='red')],
				[sg.ML(size=(50-15, 15), key=f'-{word}-error-')],
			], pad=(0, 0)),
			sg.T('    '),
			sg.Column(layout=[
				[sg.T('warning', font=my_font2)],
				[sg.ML(size=(70-12, 15), key=f'-{word}-warning-')],
				[sg.T('info', font=my_font2)],
				[sg.ML(size=(70-12, 15), key=f'-{word}-info-')],
			], pad=(0, 0)),

			tabs(
				('Text', word, [
					[sg.T('warning info', font=my_font3)]
					,[sg.ML(size=(110, 30), key=f'-{word}-warning_info-')]
				]),
				('Listbox', word, [
					[sg.T('warning info listbox', font=my_font3)]
					,[sg.Listbox([], size=(100, 25), key=f'-{word}-listbox-', enable_events=True)]
				])
			)

		]]
	layout = [
		[ sg.TabGroup( 	[[  sg.Tab('README', make_tab('README')),
							sg.Tab('CALL_REF', make_tab('CALL_REF')),
							sg.Tab('General settings', [
									[sg.T('text editor:'), sg.Combo(['pycharm', 'subl'], default_value='subl', key='_text_editor_combo_')]
								])
						]] )
		]
	]

	psg_module_path = str(sg).split("' from '")[1][:-2]
	window = sg.Window('We are live! Again! --- ' + 'Completed making            {}, {}'.format(os.path.basename(README_OFILENAME), os.path.basename(CALL_REFERENCE_OFILENAME)), [
		[sg.T(size=(30,1), key='-compile-time-')],
		[sg.T(f'The PySimpleGUI module being processed is "{psg_module_path}"')],
		[
			sg.B('Run again (F1)', key='-run-')
			,sg.Col([
					[sg.CB('show time in logs (F2)', False, key='show_time')],
					[sg.CB('Logs with Color (F3)', True, key='use_psg_color')],
					[sg.CB('will filter special names', True, key='checkbox_filter_special_names')]
			])
			,sg.Col([
					[sg.B('open call ref', key='-open_call_ref-')],
					[sg.B('open readme.txt', key='-open_readme.txt-')],
					[sg.B('open "db folder"', key='-open_db_folder-')],
			])
			,sg.T(' '*10)
			,sg.Col([
					# [sg.T('output name for call_ref markdown file', key=(15,1)), sg.I(key='')],
					
					[*md2psg('markdown outputFileName *FOR* **readme  **: ')
						,sg.I(README_OFILENAME, key='md1', size=(25, 1))
						,sg.B('open in explorer', key='open in explorer_readme')]
					
					,[*md2psg('markdown outputFileName *FOR* **call ref**: ')
						,sg.I(CALL_REFERENCE_OFILENAME, key='md2', size=(25, 1))
						,sg.B('open in explorer', key='open in explorer_calref')]
				])
		]
		,*layout
	], resizable=True, finalize=True, location=(0,0), return_keyboard_events = True)
	
	def update_time_in_GUI():
		window['-compile-time-'](datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))

	def update_compilation_in_psg(values):

		# get results
		result_readme__for_txt_n_listbox, result_call_ref__for_txt_n_listbox = compile_all_stuff(
												use_psg_color=values['use_psg_color'],
												show_time=values['show_time'])

		result_readme_txt,   result_readme_listbox_items   = result_readme__for_txt_n_listbox
		result_call_ref_txt, result_call_ref_listbox_items = result_call_ref__for_txt_n_listbox
		
		# =========== listbox's
		# -{word}-listbox-
		class ParsingError(object):
			def __init__(self, log_obj):
				self.log_obj = log_obj
				self.text = log_obj['message_text']

			def __str__(self): return self.__repr__()
			def __repr__(self):
				'''qwe'''
				# {
				#  'message_type': 'info',
				#  'message_text': 'STARTING',
				#  'message_time': 2,
				#  'message_metadata': {}
				# }

				text = self.log_obj['message_text']
				metadata = self.log_obj['message_metadata']
				lineno = ''
				if 'lineno' in metadata.keys(): lineno = "(line:" + str(metadata['lineno']) + ') '

				return f'{lineno} {text}'

		window['-README-listbox-']([ParsingError(i) for i in result_readme_listbox_items])
		window['-CALL_REF-listbox-']([ParsingError(i) for i in result_call_ref_listbox_items])

		# =========== multitext's

		def set_it(prefix = 'CALL_REF', messages_obj = result_call_ref_txt):
			t_error, t_warning, t_info, t_debug = ['\n'.join(i) for i in messages_obj[:4]]
			window[f'-{prefix}-error-'](t_error)
			window[f'-{prefix}-warning-'](t_warning)
			window[f'-{prefix}-info-'](t_info)
			window[f'-{prefix}-debug-'](t_debug)

			# /// colors warning_info
			window[f'-{prefix}-warning_info-'].update('')
			t_warning_info_obj = messages_obj[-1]
			if values['use_psg_color']:
				
				def is_valid_regex_LogMessage(msg):
					regex_str = rf"fix .:return:. in .SetFocus|SetTooltip|Update|__init__|bind|expand|set_cursor|set_size."
					return not bool(re.search(regex_str, msg, flags=re.M|re.DOTALL))

				for text, color in t_warning_info_obj:
					# print(values)
					if values['checkbox_filter_special_names'] and not is_valid_regex_LogMessage(text): continue
					window[f'-{prefix}-warning_info-'].print(text, text_color=color)
			else:
				window[f'-{prefix}-warning_info-'](t_warning_info_obj)
		
		# two calls
		set_it('README', result_readme_txt)
		set_it('CALL_REF', result_call_ref_txt)

		# ~~~~~~~~~~~~
		# GUI updating
		# ~~~~~~~~~~~~
		update_time_in_GUI()

	values = window.read(timeout=10)[1]
	update_compilation_in_psg(values)
	# update_compilation_in_psg({'use_psg_color':not False, 'show_time':False})
	
	while True:
		event, values = window()

		if event in ('Exit', None):
			APP_CONFIGS['README_FILENAME'], APP_CONFIGS['CALL_REFERENCE_FILENAME'] = window['md1'].get(), window['md2'].get()
			save_configs(APP_CONFIGS)
			break
		
		print('PSG event>', event)

		if event == '-README-listbox-':
			res = values['-README-listbox-'][0]
			qwe = res.log_obj['message_metadata']
			print(f'qwe = {qwe}')

		if event == '-CALL_REF-listbox-':
			res = values['-CALL_REF-listbox-'][0]
			metadata = res.log_obj['message_metadata']
			if 'lineno' in metadata.keys():
				lineno = metadata['lineno']
				texteditor = values['_text_editor_combo_']

				if 'pycharm' == texteditor:
					subprocess.Popen(f'{texteditor} --line {lineno} PySimpleGUI.py', shell=True)
				elif 'subl' == texteditor:
					subprocess.Popen(f'{texteditor} PySimpleGUI.py:{lineno}', shell=True)


		# if event == '-CALL_REF-listbox-':
		# 	res = values['-CALL_REF-listbox-'][0]
		# 	print(f'res = {res}')


		# buttons
		if event == '-run-':              update_compilation_in_psg(values)
		if event == '-open_readme.txt-':  openfile(README_OFILENAME)
		if event == '-open_call_ref-':    openfile(CALL_REFERENCE_OFILENAME)
		if event == '-open_db_folder-':   opendir(cd)
		if event == '-open_github_gallery-':   opendir(cd)
		if event == 'open in explorer_readme':
			CD = os.path.dirname(os.path.abspath(__file__))
			opendir(os.path.dirname(os.path.join(CD, values['md1'])))
		if event == 'open in explorer_calref':
			CD = os.path.dirname(os.path.abspath(__file__))
			opendir(os.path.dirname(os.path.join(CD, values['md2'])))
		# hotkeys
		if 'F1' in event: update_compilation_in_psg(values)
		if 'F2' in event: window['show_time'](not values['show_time'])
		if 'F3' in event: window['use_psg_color'](not values['use_psg_color'])

	window.close()


if __name__ == '__main__':
	mini_GUI()
	# sg.PopupScrolled('Completed making {}'.format(README_OFILENAME), ''.join(lines), size=(80,50))