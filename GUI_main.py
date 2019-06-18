from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from untitled import *
from GUI_UI_utils import *
import sys
import time
import logging
from make_real_readme import main as do_readme
import os
import platform
import subprocess
from os.path import exists
cd = os.path.dirname(os.path.abspath(__file__))

LOG_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lOOOOOOLOG.log')

def mk_logger():
	global LOG_FILE
	# ===============================
	# 		   logging setup
	# ===============================
	# make logger
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	# mk file
	my_file = logging.FileHandler(LOG_FILE)
	my_file.setLevel(logging.DEBUG)
	my_file.setFormatter(logging.Formatter(
		'%(levelname)s: \t%(message)s'))
	# '%(asctime)s>%(levelname)s: %(message)s'))

	# join
	logger.addHandler(my_file)
	return logger


mylogger = mk_logger()


class MyWin(QtWidgets.QMainWindow):


	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowTitle('Doc maker')
		self.setWindowIcon(QtGui.QIcon('logo.png'))

		self.settings = QSettings('PSGDoc', 'Gicompany', self)
		self.loadS()


		def build_readme_clicked():
			global mylogger
			# self.log_color('STARTING')
			mylogger.debug('STARTING')
			###############################################
			#                                             #
			#                                             #
			#     _ __  _ __ ___ _ __   __ _ _ __ ___     #
			#    | '_ \| '__/ _ \ '_ \ / _` | '__/ _ \    #
			#    | |_) | | |  __/ |_) | (_| | | |  __/    #
			#    | .__/|_|  \___| .__/ \__,_|_|  \___|    #
			#    | |            | |                       #
			#    |_|            |_|                       #
			###############################################
			# getting name
			output_name = self.get_output_name()

			force_over = getv(self.ui.force_override_output)
			# file doesn't exists  OR
			# file exists + override 		-> do the work
			if (not exists(output_name)) or (force_over and exists(output_name)):
				pass
			# file exists + not override 	-> ask
			elif exists(output_name) and (not force_over):
				dialog = QMessageBox()
				dialog.setIcon(QMessageBox.Question)
				dialog.setText(f'Aro you sure want to override {output_name}?')
				dialog.setWindowTitle('Warning')
				dialog.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
				dialog.setDefaultButton(QMessageBox.Yes)
				dialog.setEscapeButton(QMessageBox.No)
				ok = dialog.exec_()
				if ok == QMessageBox.No:
					self.log_color('Ending.\\\\\\')
					return

			####################################
			#                          _       #
			#                         | |      #
			#     _ __ ___   ___  __ _| |_     #
			#    | '_ ` _ \ / _ \/ _` | __|    #
			#    | | | | | |  __/ (_| | |_     #
			#    |_| |_| |_|\___|\__,_|\__|    #
			#                                  #
			#                                  #
			####################################
			try:

				# 1 - grep files
				files = getv2(self, 'c1 c2 c3 c4')
				files_to_include = [index for index, i in enumerate(files) if i[1]]

				# all unchecked
				if not any(files_to_include):
					return

				# 2 - work
				content = do_readme(files_to_include=files_to_include,
									logger=mylogger, output_name=output_name)

				# 3 - output data into GUI
				setv(self.ui.readme_preview, content)

				self.see_logs()

				if getv(self.ui.see_content_after):
					self.see_content()

			except Exception as e:
				self.log_color(f'Error: {str(e)}', 'err')

			self.log_color('Ending')

		def show_readme_clicked():
			readme_file = self.get_output_name()
			if exists(readme_file):
				if platform.system() == "Windows":
					# os.startfile(readme_file)
					subprocess.Popen(["explorer ", readme_file])
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", readme_file])
				else:
					subprocess.Popen(["xdg-open", readme_file])

		self.ui.see_content.clicked.connect(
			lambda: self.see_content())
		self.ui.browse_output.clicked.connect(self.browse_output_clicked)
		self.ui.do_only_readme.clicked.connect(self.do_only_readme_clicked)
		self.ui.do_all.clicked.connect(self.do_all_clicked)
		self.ui.build_readme.clicked.connect(build_readme_clicked)
		self.ui.show_readme.clicked.connect(show_readme_clicked)
		self.ui.clear_logs.clicked.connect(lambda: setv(self.ui.logs, ''))
		# shortcut
		QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
		QShortcut(QKeySequence("Ctrl+B"),
				  self).activated.connect(build_readme_clicked)
	
		# QTimer.singleShot(100, self.see_logs)


	def see_content(self):
		self.ui.tabWidget.setCurrentIndex(1)

	def get_output_name(self):
		output_name = getv(self.ui.output_name)
		
		if not output_name:
			self.log_color("Output file name is empty!", 'err')
			return
		if '/' in output_name or '\\' in output_name:
			output_name = os.path.join(cd, output_name)

		return output_name

	def do_only_readme_clicked(self):
		setv(self.ui.c1, False)
		setv(self.ui.c2, True)
		setv(self.ui.c3, False)
		setv(self.ui.c4, False)

	def do_all_clicked(self):
		setv(self.ui.c1, True)
		setv(self.ui.c2, True)
		setv(self.ui.c3, True)
		setv(self.ui.c4, True)

	def browse_output_clicked(self):
		mypath = QFileDialog.getOpenFileName(
			self, 'Select file', '', 'Any files (*.*)')[0]
		if mypath != '' and exists(mypath):
			setv(self.ui.output_name, mypath)

	# =============================

	def log_color(self, text, color=''):
		mycolor = {
			'err': 'cc0000', 'war': 'f57900',
			'info' 	: '75507b', '': '000000'
		}

		if color not in mycolor.keys():
			self.log('Error, unknows color!')
			return

		if color == '':
			logging.debug(text)
		elif color == 'err':
			logging.error(text)
		elif color == 'info':
			logging.info(text)
		elif color == 'war':
			logging.warning(text)

		self.ui.logs.appendHtml(f'<span style="color:#{mycolor[color]};">{text}</span>')
		global mylogger
		mylogger.debug(text)

	def see_logs(self):
		global LOG_FILE
		
		def color_text(text, color=''):
			mycolor = {
				'ERROR': 'cc0000', 'WARNING': 'f57900',
				'INFO' 	: '75507b', '': '000000',
				'DEBUG' : '000000'
			}

			if color not in mycolor.keys():
				raise Exception('Error, unknows color!')

			return f'<span style="color:#{mycolor[color]};">{text}</span>'
		
		with open(LOG_FILE, 'r', encoding='utf-8') as ff:

			text = ff.read()
			text = text[text.rindex('DEBUG: \tSTARTING'):]
			lines = [i.strip() for i in text.split('\n') if i.strip()]
			result_lines = [color_text(text=i.split(': \t')[1],
												color=i.split(':')[0])
							for i in lines]

			for i in result_lines:
				self.ui.logs.appendHtml(i)
			
			# logcontent = '\n\n'.join(result_lines)
			# self.ui.logs.appendHtml(logcontent)

			# self.ui.logs.appendHtml(text)


	def log(self, text):
		# log textedit -> self.ui.logs

		# QTextEdit verison
		self.ui.logs.append(str(text))

		# # QPlainTextEdit verison
		self.ui.logs.appendPlainText(str(text))

		# scroll to bottom (to see latest text), (after text was inserted)
		self.ui.logs.verticalScrollBar().setValue(
			self.ui.logs.verticalScrollBar().maximum())
		self.ui.logs.moveCursor(QtGui.QTextCursor.End)




	def closeEvent(self, e):
		self.saveS()
		e.accept()
		
	def loadS(self):
		if self.settings.contains('geo'): 						self.setGeometry(self.settings.value('geo'))
		if self.settings.contains('c1'): 						setv(self.ui.c1, self.settings.value('c1', type=bool))
		if self.settings.contains('c2'): 						setv(self.ui.c2, self.settings.value('c2', type=bool))
		if self.settings.contains('c3'): 						setv(self.ui.c3, self.settings.value('c3', type=bool))
		if self.settings.contains('c4'): 						setv(self.ui.c4, self.settings.value('c4', type=bool))
		if self.settings.contains('output_name'): 				setv(self.ui.output_name, self.settings.value('output_name', type=bool))
		if self.settings.contains('force_override_output'): 	setv(self.ui.force_override_output, self.settings.value('force_override_output', type=bool))
		if self.settings.contains('see_content_after'): 		setv(self.ui.see_content_after, self.settings.value('see_content_after'))

	def saveS(self):
		self.settings.setValue('geo',  self.geometry())
		self.settings.setValue('c1',  getv(self.ui.c1))
		self.settings.setValue('c2',  getv(self.ui.c2))
		self.settings.setValue('c3',  getv(self.ui.c3))
		self.settings.setValue('c4',  getv(self.ui.c4))
		self.settings.setValue('output_name',  getv(self.ui.output_name))
		self.settings.setValue('force_override_output',  getv(self.ui.force_override_output))
		self.settings.setValue('see_content_after',  getv(self.ui.see_content_after))



# def color_text(text, color=''):
# 	mycolor = {
# 		'ERROR': 'cc0000', 'WARNING': 'f57900',
# 		'INFO' 	: '75507b', '': '000000'
# 	}

# 	if color not in mycolor.keys():
# 		raise Exception('Error, unknows color!')

# 	return f'<span style="color:#{mycolor[color]};">{text}</span>'

# with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE), 'r', encoding='utf-8') as ff:

# 	text = ff.read()
# 	# text = ff.read().replace('\n', '')
# 	print(1)
# 	print(text)
# 	print(text.rfind('STARTING'))
# 	print(111)
# 	lines = [i.strip() for i in text[text.rindex('STARTING'):] if i.strip()]
# 	print(2)
# 	result_lines = [color_text(text=i.split(': \t')[1],
# 										color=i.split(':')[0])
# 					for i in lines]
# 	logcontent = '\n'.join(result_lines)
# 	print(f'logcontent = {logcontent}')


# import sys; sys.exit(1)

if __name__ == "__main__":
	# normal
	qapp = QtWidgets.QApplication(sys.argv)
	myqapp = MyWin()
	myqapp.show()
	sys.exit(qapp.exec_())
	# quick
	# qapp = QtWidgets.QApplication(sys.argv); myqapp = MyWin(); myqapp.close()
