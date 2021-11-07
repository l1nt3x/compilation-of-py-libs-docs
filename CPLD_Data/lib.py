# Importing libraries

from pickle import load, dump  # Saving and loading data

from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QWidget
from url_normalize import url_normalize as url_fix

from libui import *
from templates import templatesWindow


class libWindow(QWidget, Ui_lib):
    def __init__(self, form_name='libName'):
        self.form_name = form_name
        self.t = None
        self.lib = form_name
        with open('../compilation-of-python-libs-docs/data.pickle', 'rb') as f:
            self.libsData = dict(sorted(load(f).items()))
        self.libData = self.libsData[self.lib]
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(form_name)
        self.listWidget.addItems(list(self.libData.keys())[:-1])
        self.listWidget.clicked.connect(self.open_item)
        self.pushButton_2.clicked.connect(self.open_templates)
        self.pushButton.clicked.connect(self.save_item)
        self.setWindowIcon(QIcon("../icon.ico"))
        self.setFixedSize(760, 470)

    def open_templates(self):
        if self.t is None:
            self.t = templatesWindow(form_name=self.form_name)
        else:
            self.t = templatesWindow(form_name=self.form_name)
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
        self.libsData[self.lib] = self.libData
        with open('../compilation-of-python-libs-docs/data.pickle', 'wb') as f:
            dump(dict(sorted(self.libsData.items())), f)
