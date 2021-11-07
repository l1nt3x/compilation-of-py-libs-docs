from pickle import load  # Saving and loading data

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

import PySyntax
from templatesui import *


class templatesWindow(QWidget, Ui_templates):
    def __init__(self, form_name='Templates (libName)'):
        with open('../compilation-of-python-libs-docs/data.pickle', 'rb') as f:
            self.libsData = dict(sorted(load(f).items()))
        self.libData = self.libsData[form_name]
        self.libTemplates = self.libData['Templates']
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f'Templates ({form_name})')
        self.setWindowIcon(QIcon("../icon.ico"))
        self.listWidget.addItems(self.libTemplates)
        self.listWidget.clicked.connect(self.open_template)
        self.plainTextEdit.setStyleSheet("""QPlainTextEdit
    {
    font-family: 'Consolas';
    font-size: 20px;
    color: #ccc;
    background-color: #2b2b2b;
    }""")

    def open_template(self):
        self.plainTextEdit.clear()
        item = self.listWidget.currentItem().text()
        highlight = PySyntax.PythonHighlighter(self.plainTextEdit.document())
        self.plainTextEdit.insertPlainText(self.libTemplates[item])
