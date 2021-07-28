from make_real_readme import main
import json,os,time

def writejson(a_path:str, a_dict:dict) -> None:
	with open(a_path, 'w', encoding='utf-8') as output_file: json.dump(a_dict, output_file, ensure_ascii=False, indent=2)
def readjson(a_path:str) -> dict:
	with open(a_path, 'r', encoding='utf-8') as f: return json.load(f)

rfile = readfile = lambda fpath: open(fpath, 'r', encoding='utf-8').read();
wfile = writefile = lambda fpath, x: open(fpath, 'w', encoding='utf-8').write(x)


def timeit(f):
	def wrapper(*args, **kwargs):
		start = time.time()
		res = f(*args, **kwargs)
		end = time.time()
		# print('\nНачало в    : ', start)
		# print('\n ({}) Начало в    : '.format(f.__name__, start))
		# print('Окончено в  : ', end)
		# print('Длительность: ', end - start)
		# print('')
		return res
	return wrapper




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
	def error(self, m, metadata={}):   self.error_list.append([self.tick(), m, metadata])
	def warning(self, m, metadata={}): self.warning_list.append([self.tick(), m, metadata])
	def info(self, m, metadata={}):    self.info_list.append([self.tick(), m, metadata])
	def debug(self, m, metadata={}):   self.debug_list.append([self.tick(), m, metadata])

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
	@timeit
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
	@timeit
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
	@timeit
	def load_to_listbox(self):
		'''
		read .json
		'''
		return sorted(readjson(self.json_name),
					  key=lambda x: x['message_time'])


insert_md_section_for__class_methods = False
remove_repeated_sections_classmethods = False



@timeit
def compile_call_ref(output_filename='LoG_call_ref', replace_pipe_bar_in_TYPE_TEXT_char='', _underscore_MD_files_FOLDER='', **kw):
	''' Compile a "5_call_reference.md" file'''

	global insert_md_section_for__class_methods, remove_repeated_sections_classmethods
	log_obj = BESTLOG(os.path.join(cd, output_filename))
	
	main(logger=log_obj,
		 main_md_file=os.path.join(_underscore_MD_files_FOLDER, '5_call_reference.md'), _underscore_MD_files_FOLDER = _underscore_MD_files_FOLDER,
		 insert_md_section_for__class_methods=insert_md_section_for__class_methods,
		 remove_repeated_sections_classmethods=remove_repeated_sections_classmethods,
		 files_to_include=[],
		 output_name=kw['CALL_REFERENCE_OFILENAME'],
		 delete_html_comments=True,
		 replace_pipe_bar_in_TYPE_TEXT_char=replace_pipe_bar_in_TYPE_TEXT_char)
	log_obj.save()
	return log_obj.load(**kw), log_obj.load_to_listbox()


@timeit
def compile_readme(output_filename='LoG', replace_pipe_bar_in_TYPE_TEXT_char='', _underscore_MD_files_FOLDER='', **kw):
	''' Compile a "2_readme.md" file'''
	global insert_md_section_for__class_methods, remove_repeated_sections_classmethods
	log_obj = BESTLOG(os.path.join(cd, output_filename))
	main(logger=log_obj,
		 main_md_file=os.path.join(_underscore_MD_files_FOLDER, '2_readme.md'), _underscore_MD_files_FOLDER = _underscore_MD_files_FOLDER,
		 insert_md_section_for__class_methods=insert_md_section_for__class_methods,
		 remove_repeated_sections_classmethods=remove_repeated_sections_classmethods,
		 files_to_include=[0, 1, 2, 3],
		 output_name=kw['README_OFILENAME'],
		 delete_html_comments=True,
		 replace_pipe_bar_in_TYPE_TEXT_char=replace_pipe_bar_in_TYPE_TEXT_char)
	log_obj.save()
	return log_obj.load(**kw), log_obj.load_to_listbox()

def compile_all_stuff(**kw):
	'''
		Compile a "2_ and 5_" .md filess
		return output from them
	'''
	return compile_readme(**kw), compile_call_ref(**kw)



if __name__ == '__main__':

	#
	#
	# cli
	#
	#
	import argparse
	parser = argparse.ArgumentParser(description='psg INTERFACE')
	parser.add_argument("-ojson", metavar="ojson", type=str, help="where to output data")
	cli_args = parser.parse_args()
	ojson = cli_args.ojson
	# ==============

	cd = os.path.dirname(os.path.abspath(__file__))
	values = eval(eval(rfile(os.path.join(cd, 'input_psg_values.json'))))
	data = compile_all_stuff(
		use_psg_color=values['use_psg_color'],
		show_time=values['show_time'],
		replace_pipe_bar_in_TYPE_TEXT_char=values['replace_pipe_bar_in_TYPE_TEXT_char'],

		CALL_REFERENCE_OFILENAME = values['CALL_REFERENCE_OFILENAME'],
		README_OFILENAME = values['README_OFILENAME'],
		_underscore_MD_files_FOLDER = values['_underscore_MD_files_FOLDER'],
		)
	writejson(cli_args.ojson, data)



	# log_obj = BESTLOG(os.path.join(cd, output_filename))
	# main(...)
	# log_obj.save()
	# result = log_obj.load(**kw), log_obj.load_to_listbox()



