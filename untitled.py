# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/gogol/Desktop/кладовка/pysimpleguiDOCUMENTATION2019/v3/PySimpleGUIDocGen/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 698)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.build_readme = QtWidgets.QPushButton(self.tab)
        self.build_readme.setObjectName("build_readme")
        self.gridLayout_3.addWidget(self.build_readme, 4, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.clear_logs = QtWidgets.QPushButton(self.tab)
        self.clear_logs.setObjectName("clear_logs")
        self.gridLayout_4.addWidget(self.clear_logs, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.show_readme = QtWidgets.QPushButton(self.tab)
        self.show_readme.setObjectName("show_readme")
        self.gridLayout_3.addWidget(self.show_readme, 6, 0, 1, 1)
        self.logs = QtWidgets.QPlainTextEdit(self.tab)
        self.logs.setObjectName("logs")
        self.gridLayout_3.addWidget(self.logs, 3, 0, 1, 1)
        self.see_content = QtWidgets.QPushButton(self.tab)
        self.see_content.setObjectName("see_content")
        self.gridLayout_3.addWidget(self.see_content, 5, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(11)
        self.gridLayout.setObjectName("gridLayout")
        self.c4 = QtWidgets.QCheckBox(self.frame)
        self.c4.setChecked(True)
        self.c4.setObjectName("c4")
        self.gridLayout.addWidget(self.c4, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.c3 = QtWidgets.QCheckBox(self.frame)
        self.c3.setChecked(True)
        self.c3.setObjectName("c3")
        self.gridLayout.addWidget(self.c3, 3, 0, 1, 1)
        self.c1 = QtWidgets.QCheckBox(self.frame)
        self.c1.setChecked(True)
        self.c1.setObjectName("c1")
        self.gridLayout.addWidget(self.c1, 1, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.frame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.do_only_readme = QtWidgets.QPushButton(self.splitter)
        self.do_only_readme.setObjectName("do_only_readme")
        self.do_all = QtWidgets.QPushButton(self.splitter)
        self.do_all.setObjectName("do_all")
        self.gridLayout.addWidget(self.splitter, 5, 0, 1, 1)
        self.c2 = QtWidgets.QCheckBox(self.frame)
        self.c2.setChecked(True)
        self.c2.setObjectName("c2")
        self.gridLayout.addWidget(self.c2, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.readme_preview = QtWidgets.QPlainTextEdit(self.tab_2)
        self.readme_preview.setFrameShape(QtWidgets.QFrame.Box)
        self.readme_preview.setReadOnly(True)
        self.readme_preview.setTabStopWidth(2)
        self.readme_preview.setBackgroundVisible(False)
        self.readme_preview.setObjectName("readme_preview")
        self.gridLayout_9.addWidget(self.readme_preview, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.formLayout = QtWidgets.QFormLayout(self.tab_3)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 0, 0, 1, 1)
        self.force_override_output = QtWidgets.QCheckBox(self.tab_3)
        self.force_override_output.setChecked(True)
        self.force_override_output.setObjectName("force_override_output")
        self.gridLayout_7.addWidget(self.force_override_output, 0, 1, 1, 1)
        self.output_name = QtWidgets.QLineEdit(self.tab_3)
        self.output_name.setObjectName("output_name")
        self.gridLayout_7.addWidget(self.output_name, 0, 2, 1, 1)
        self.browse_output = QtWidgets.QToolButton(self.tab_3)
        self.browse_output.setObjectName("browse_output")
        self.gridLayout_7.addWidget(self.browse_output, 0, 3, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.gridLayout_7)
        self.see_content_after = QtWidgets.QCheckBox(self.tab_3)
        self.see_content_after.setChecked(False)
        self.see_content_after.setObjectName("see_content_after")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.see_content_after)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.build_readme.setText(_translate("MainWindow", " ( ͡° ͜ʖ ͡°) BUILD"))
        self.label_4.setText(_translate("MainWindow", "   Logs:"))
        self.clear_logs.setText(_translate("MainWindow", "clear logs"))
        self.show_readme.setText(_translate("MainWindow", "open readme.md in explorer"))
        self.see_content.setText(_translate("MainWindow", "See content"))
        self.c4.setText(_translate("MainWindow", "4_Release_notes"))
        self.label_2.setText(_translate("MainWindow", "Select needed parts:"))
        self.c3.setText(_translate("MainWindow", "3_FOOTER"))
        self.c1.setText(_translate("MainWindow", "1_HEADER_top_part"))
        self.do_only_readme.setText(_translate("MainWindow", "▲ do ▲\n"
"2_readme "))
        self.do_all.setText(_translate("MainWindow", "■ all ■"))
        self.c2.setText(_translate("MainWindow", "2_readme"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Builder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "README.md preview"))
        self.label_5.setText(_translate("MainWindow", "Output name"))
        self.force_override_output.setText(_translate("MainWindow", "force overridee"))
        self.output_name.setText(_translate("MainWindow", "_readme.md"))
        self.browse_output.setText(_translate("MainWindow", "..."))
        self.see_content_after.setText(_translate("MainWindow", "see content after BUILD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Settings"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())