# Importing libraries
from sys import argv, exit  # App execution

# App developing
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QVBoxLayout, QInputDialog, QShortcut

from dbuse import LOAD_DB_TO_DICT, DUMP_FROM_DICT_TO_DB
# Another windows
from lib import libWindow
from mainui import Ui_MainWindow  # App's UI


# MainWindow class
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.w = None  # No external window yet.
        super().__init__()
        self.setupUi(self)

        # Setting a window icon
        self.setWindowIcon(QIcon("../compilation-of-python-libs-docs/icon.png"))

        # Reading libraries from data base
        self.libsData = LOAD_DB_TO_DICT('../compilation-of-python-libs-docs/DATA.db')

        self.libraries_List.itemDoubleClicked.connect(self.open_lib)
        enter_key = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_key.activated.connect(self.open_lib)

        # Setting fixed size
        self.setFixedSize(self.size())

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Transfering data from data base into libraries_List
        libs_names = []
        for x in self.libsData.keys():
            libs_names.append(str(self.libsData[x]['Name']))

        self.libraries_List.addItems(libs_names)
        self.libraries_List.installEventFilter(self)
        layout.addWidget(self.libraries_List)

        # Setting search function to search search_Edit
        self.search_Edit.textChanged.connect(self.search_update)
        self.search_Edit.setPlaceholderText('Search')

    def open_lib(self):
        # Getting an item name that was clicked
        selected_item = [item.text() for item in self.libraries_List.selectedItems()]
        idd = None
        for lib in list(self.libsData.keys()):
            if str(self.libsData[lib]['Name']) == str(selected_item[0]):
                idd = lib
                break
        if not selected_item:
            return 11
        if self.w is None:
            self.w = libWindow(lib_id=idd, form_name=selected_item)
        else:
            self.w = libWindow(lib_id=idd, form_name=selected_item)
        self.w.show()
        self.libraries_List.clearSelection()

    # Creating context menu
    def contextMenuEvent(self, event):
        # Declaring context menu (right click menu)
        contextMenu = QMenu(self)

        # Declaring acts
        deleteAct = ''
        openAct = ''
        editAct = ''
        newAct = ''

        # Getting an item name that was right clicked
        selected_item = [item.text() for item in self.libraries_List.selectedItems()]

        # If it was clicked on self.libraries_List
        if ''.join(selected_item) == '':
            newAct = contextMenu.addAction("New")  # New entry

            check = 'new'  # self.libraries_List was right clicked
        # If it was clicked on self.libraries_List item
        else:
            openAct = contextMenu.addAction("Open")  # Open entry
            deleteAct = contextMenu.addAction("Delete")  # Delete entry
            editAct = contextMenu.addAction('Edit')  # Edit entry's name

            check = 'opedel'  # self.libraries_List item was right clicked

        # Getting chosen action
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        # If self.libraries_List item was right clicked
        if check == 'opedel':
            # If delete action was chosen
            if action == deleteAct:
                self.libraries_List.clear()  # Clearing self.libraries_List widget
                idd = None
                for lib in list(self.libsData.keys()):
                    if str(self.libsData[lib]['Name']) == str(selected_item[0]):
                        idd = lib
                        break
                del self.libsData[idd]  # Deleting an entry from data
                # Showing data in self.libraries_List
                libs_names = []
                for x in self.libsData.keys():
                    libs_names.append(str(self.libsData[x]['Name']))

                self.libraries_List.addItems(libs_names)
                # Updating data
                DUMP_FROM_DICT_TO_DB(self.libsData)

            # If open action was chosen
            elif action == openAct:
                self.open_lib()
            # If edit action was chosen
            elif action == editAct:
                # Edit entry dialog
                edit_entry, ok_pressed = QInputDialog.getText(self, "Edit entry",
                                                              "Input new lib name:")
                if ok_pressed:
                    idd = None
                    for lib in list(self.libsData.keys()):
                        if str(self.libsData[lib]['Name']) == str(selected_item[0]):
                            idd = lib
                            break
                    self.libsData[idd]['Name'] = edit_entry
                    self.libraries_List.clear()  # Clearing self.libraries_List widget
                    # Showing data in self.libraries_List
                    libs_names = []
                    for x in self.libsData.keys():
                        libs_names.append(str(self.libsData[x]['Name']))

                    self.libraries_List.addItems(libs_names)
                    # Updating data
                    DUMP_FROM_DICT_TO_DB(self.libsData)
        # If self.libraries_List item was right clicked
        elif check == 'new':
            # If new action was chosen
            if action == newAct:
                # New entry dialog
                new_entry, ok_pressed = QInputDialog.getText(self, "New entry", "Input lib name:")
                if ok_pressed:
                    self.libsData[len(self.libsData) + 1] = {
                        'Name': new_entry,
                        'Description': 'NO DESCRIPTION',
                        'Link': 'NO_LINK',
                        'Templates': {
                            'PathToLib': f'str({new_entry})[16 + len("{new_entry}"):-1])'
                        }
                    }
                    self.libraries_List.clear()
                    # Showing data in self.libraries_List
                    libs_names = []
                    for x in self.libsData.keys():
                        libs_names.append(str(self.libsData[x]['Name']))
                    self.libraries_List.addItems(libs_names)
                    # Updating data
                    DUMP_FROM_DICT_TO_DB(self.libsData)
        # Clearing listWidget selection
        self.libraries_List.clearSelection()

    # Search function
    def search_update(self):
        text = self.search_Edit.text()
        tmp = []
        for x in self.libsData.keys():
            tmp.append(str(self.libsData[x]['Name']))
        tmp2 = []
        # Showing only suitable items in listWidget
        for item in tmp:
            if text.lower() in item.lower():
                tmp2.append(item)
        self.libraries_List.clear()
        self.libraries_List.addItems(tmp2)


# Executing app
if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainWindow()
    ex.show()
    exit(app.exec_())
