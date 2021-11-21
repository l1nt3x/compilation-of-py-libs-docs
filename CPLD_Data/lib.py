# Importing libraries

from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QWidget
from url_normalize import url_normalize as url_fix

from dbuse import LOAD_DB_TO_DICT, DUMP_FROM_DICT_TO_DB  # Saving and loading data
from libui import *
from templates import templatesWindow


class libWindow(QWidget, Ui_lib):
    def __init__(self, lib_id=1, form_name='libName'):
        super().__init__()
        self.setupUi(self)

        # Reading libraries from data base
        self.libsData = LOAD_DB_TO_DICT('../compilation-of-python-libs-docs/DATA.db')
        self.form_name = form_name[0]
        self.lib_id = lib_id
        self.libData = self.libsData[self.lib_id]

        self.t = None

        # Setting the window preferences
        self.setWindowTitle(self.form_name)

        self.setWindowIcon(QIcon("../compilation-of-python-libs-docs/icon.png"))

        self.setFixedSize(760, 470)

        self.listWidget.addItems(list(self.libData.keys())[1:-1])
        self.listWidget.clicked.connect(self.open_item)
        # print(self.listWidget.items())
        self.listWidget.setCurrentRow(0)
        self.open_item()
        self.listWidget.setCurrentRow(0)
        self.pushButton_2.clicked.connect(self.open_templates)
        self.pushButton.clicked.connect(self.save_item)

    def open_templates(self):
        idd = None
        for lib in list(self.libsData.keys()):
            if str(self.libsData[lib]['Name']) == str(self.form_name):
                idd = lib
                break
        if self.t is None:
            print(2)
            self.t = templatesWindow(lib_id=idd, form_name=self.form_name)
            print(21)
        else:
            self.t = templatesWindow(lib_id=idd, form_name=self.form_name)
        self.t.show()

    def open_item(self):
        editor = self.plainTextEditWURL
        cursor = editor.textCursor()
        fmt = cursor.charFormat()
        cursor.select(QtGui.QTextCursor.Document)
        cursor.setCharFormat(QtGui.QTextCharFormat())
        cursor.clearSelection()
        editor.setTextCursor(cursor)
        editor.clear()
        item = self.listWidget.currentItem().text()
        if item == 'Link':
            fmt.setForeground(QColor('blue'))
            address = self.libData[item]
            fmt.setAnchor(True)
            fmt.setAnchorHref(address)
            fmt.setToolTip(address)
            cursor.insertText(address, fmt)
        else:
            editor.setPlainText(self.libData[item])
        self.listWidget.clearSelection()

    def save_item(self):
        item = self.listWidget.currentItem().text()
        changed = self.plainTextEditWURL.toPlainText()
        if changed == '':
            changed = None
        if item == 'Link' and not changed:
            changed = url_fix(changed)
        self.libData[item] = changed
        self.libsData[self.lib_id] = self.libData

        # Updating data
        DUMP_FROM_DICT_TO_DB(self.libsData)
