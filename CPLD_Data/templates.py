from copy import deepcopy

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

import PySyntax
from dbuse import LOAD_DB_TO_DICT  # Saving and loading data
from templatesui import *


class templatesWindow(QWidget, Ui_templates):
    def __init__(self, lib_id=1, form_name='Templates (libName)'):
        super().__init__()
        self.setupUi(self)
        # Reading libraries from data base
        self.libsData = LOAD_DB_TO_DICT('../compilation-of-python-libs-docs/DATA.db')
        self.lib_id = lib_id
        self.libData = self.libsData[self.lib_id]
        self.libTemplates = self.libData['Templates']
        self.form_name = form_name
        # Setting a window preferences
        self.setWindowTitle(f'Templates ({self.form_name})')
        self.setWindowIcon(QIcon("../compilation-of-python-libs-docs/icon.png"))
        self.setFixedSize(self.size())
        self.listWidget.addItems(self.libTemplates.keys())
        self.listWidget.clicked.connect(self.open_template)
        self.plainTextEdit.setStyleSheet("""QPlainTextEdit
    {
    font-family: 'Consolas';
    font-size: 20px;
    color: #ccc;
    background-color: #2b2b2b;
    }""")
        # self.pushButton.clicked.connect(self.save_template) # TODO: fix it *1
        self.pushButton.setDisabled(True)  # TODO: fix it *1
        # Setting search function to search search_Edit
        self.lineEdit.textChanged.connect(self.search_update)
        self.lineEdit.setPlaceholderText('Search')

    def open_template(self):
        self.plainTextEdit.clear()
        item = self.listWidget.currentItem().text()
        highlight = PySyntax.PythonHighlighter(self.plainTextEdit.document())
        self.plainTextEdit.insertPlainText(self.libTemplates[item])

    # TODO: fix it *1
    # def save_template(self):
    #     self.libsData[self.lib_id]['Templates'][self.listWidget.currentItem().text()] = self.plainTextEdit.toPlainText().replace("'", '"')
    #     self.open_template()
    #     # Updating data
    #     DUMP_FROM_DICT_TO_DB(self.libsData)

    # TODO: fix it *2
    # Creating context menu
    # def contextMenuEvent(self, event):
    #     # Declaring context menu (right click menu)
    #     contextMenu = QMenu(self)
    #
    #     # Declaring acts
    #     deleteAct = ''
    #     newAct = ''
    #
    #     # Getting an item name that was right clicked
    #     selected_item = ''.join([item.text() for item in self.listWidget.selectedItems()])
    #
    #     # If it was clicked on self.libraries_List
    #     if ''.join(selected_item) == '':
    #         newAct = contextMenu.addAction("New")  # New entry
    #
    #         check = 'new'  # self.libraries_List was right clicked
    #     # If it was clicked on self.libraries_List item
    #     else:
    #         deleteAct = contextMenu.addAction("Delete")  # Delete entry
    #
    #         check = 'del'  # self.libraries_List item was right clicked
    #
    #     # Getting chosen action
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    #
    #     # If self.libraries_List item was right clicked
    #     if check == 'del':
    #         # If delete action was chosen
    #         if action == deleteAct:
    #             self.listWidget.clear()  # Clearing self.libraries_List widget
    #             del self.libsData[self.lib_id]['Templates'][selected_item]  # Deleting a template from data
    #             # Showing data in self.libraries_List
    #             self.listWidget.addItems(list(self.libTemplates.keys()))
    #             # Updating data
    #             DUMP_FROM_DICT_TO_DB(self.libsData)
    #             self.plainTextEdit.clear()
    #     # If self.libraries_List item was right clicked
    #     elif check == 'new':
    #         # If new action was chosen
    #         if action == newAct:
    #             # New entry dialog
    #             new_entry, ok_pressed = QInputDialog.getText(self, "New template",
    #                                                          "Input template name:")
    #             if ok_pressed:
    #                 self.libsData[self.lib_id]['Templates'][str(new_entry)] = 'No content'
    #                 self.listWidget.clear()
    #                 self.listWidget.addItems(list(self.libTemplates.keys()))
    #                 # Updating data
    #                 DUMP_FROM_DICT_TO_DB(self.libsData)
    #     # Clearing listWidget selection
    #     self.listWidget.clearSelection()

    # Search function
    def search_update(self):
        text = self.lineEdit.text()
        tmp = deepcopy(self.libTemplates)
        tmp2 = []
        # Showing only suitable items in listWidget
        for item in tmp:
            if text.lower() in item.lower():
                tmp2.append(item)
        self.listWidget.clear()
        self.listWidget.addItems(tmp2)
