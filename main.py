# Importing libraries
from pickle import load, dump  # Saving and loading data
from sys import argv, exit  # App execution
from webbrowser import open as open_URL  # Opening libs' urls

# App developing
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QVBoxLayout, QInputDialog, QDialog, \
    QPushButton, QLabel, QShortcut
from url_normalize import url_normalize as url_fix  # URL normalizing

from mainui import Ui_MainWindow  # App's UI


# MainWindow class
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Setting a window icon
        self.setWindowIcon(QIcon("icon.ico"))

        # Reading libraries from data base
        with open('data.pickle', 'rb') as f:
            self.libsData = dict(sorted(load(f).items()))

        self.libraries_List.itemDoubleClicked.connect(self.open_lib)
        enter_key = QShortcut(QKeySequence(Qt.Key_Return), self)
        enter_key.activated.connect(self.open_lib)

        # Setting fixed size
        self.setFixedSize(self.size())

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Transfering data from data base into libraries_List
        self.libraries_List.addItems(list(self.libsData.keys()))
        self.libraries_List.installEventFilter(self)
        layout.addWidget(self.libraries_List)

        # Setting search function to search search_Edit
        self.search_Edit.textChanged.connect(self.search_update)
        self.search_Edit.setPlaceholderText('Search')

    def open_lib(self):
        # Getting an item name that was right clicked
        selected_item = [item.text() for item in self.libraries_List.selectedItems()]
        if not selected_item:
            return 11

        # If selected lib hasn't URL
        if self.libsData[selected_item[0]] == 'No URL':
            # Declaring dialog
            dlg = QDialog()
            dlg.setFixedSize(160, 70)
            b1 = QPushButton("OK", dlg)
            b1.move(40, 40)
            b1.clicked.connect(dlg.close)
            l1 = QLabel('Please change URL for this lib', dlg)
            l1.move(10, 10)
            dlg.setWindowTitle("No URL")
            dlg.setWindowModality(Qt.ApplicationModal)
            dlg.exec_()
        else:
            open_URL(self.libsData[selected_item[0]])  # Opening URL

    # Creating context menu
    def contextMenuEvent(self, event):
        # Declaring context menu (right click menu)
        contextMenu = QMenu(self)

        # Declaring acts
        deleteAct = ''
        openAct = ''
        editAct = ''
        changeURLAct = ''
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
            changeURLAct = contextMenu.addAction('Change lib URL')  # Edit entry's URL

            check = 'opedel'  # self.libraries_List item was right clicked

        # Getting chosen action
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        # If self.libraries_List item was right clicked
        if check == 'opedel':
            # If delete action was chosen
            if action == deleteAct:
                self.libraries_List.clear()  # Clearing self.libraries_List widget
                del self.libsData[selected_item[0]]  # Deleting an entry from data
                # Showing data in self.libraries_List
                self.libraries_List.addItems(list(self.libsData.keys()))
                # Updating data
                with open('data.pickle', 'wb') as f:
                    dump(dict(sorted(self.libsData.items())), f)
            # If open action was chosen
            elif action == openAct:
                # If an item hasn't an URL
                if self.libsData[selected_item[0]] == 'No URL':
                    # Declaring dialog
                    dlg = QDialog()
                    dlg.setFixedSize(160, 70)
                    b1 = QPushButton("OK", dlg)
                    b1.move(40, 40)
                    b1.clicked.connect(dlg.close)
                    l1 = QLabel('Please change URL for this lib', dlg)
                    l1.move(10, 10)
                    dlg.setWindowTitle("No URL")
                    dlg.setWindowModality(Qt.ApplicationModal)
                    dlg.exec_()
                else:
                    open_URL(self.libsData[selected_item[0]])  # Opening URL
            # If open action was chosen
            elif action == changeURLAct:
                # Change URL dialog
                edit_URL, ok_pressed = QInputDialog.getText(self, "Change URL", "Input lib URL:")
                if ok_pressed:
                    if edit_URL != '':
                        self.libsData[selected_item[0]] = url_fix(edit_URL)  # Assigning new URL
                    else:
                        self.libsData[selected_item[0]] = 'No URL'  # Assigning new URL
                    # Updating data
                    with open('data.pickle', 'wb') as f:
                        dump(dict(sorted(self.libsData.items())), f)
            # If edit action was chosen
            elif action == editAct:
                # Edit entry dialog
                edit_entry, ok_pressed = QInputDialog.getText(self, "Edit entry",
                                                              "Input new lib name:")
                if ok_pressed:
                    del self.libsData[selected_item[0]]  # Deleting an old entry
                    self.libsData[edit_entry] = 'No URL'  # Creating a new entry
                    self.libraries_List.clear()  # Clearing self.libraries_List widget
                    # Showing data in self.libraries_List
                    self.libraries_List.addItems(list(self.libsData.keys()))
                    # Updating data
                    with open('data.pickle', 'wb') as f:
                        dump(dict(sorted(self.libsData.items())), f)
        # If self.libraries_List item was right clicked
        elif check == 'new':
            # If new action was chosen
            if action == newAct:
                # New entry dialog
                new_entry, ok_pressed = QInputDialog.getText(self, "New entry", "Input lib name:")
                if ok_pressed:
                    # Entry's URL dialog
                    URL, ok_pressed = QInputDialog.getText(self, "Change URL", "Input lib URL:")
                    if ok_pressed:
                        if URL != '':
                            self.libsData[new_entry] = url_fix(URL)  # Assigning new URL
                        else:
                            self.libsData[new_entry] = 'No URL'  # Assigning new URL

                    else:
                        self.libsData[new_entry] = 'No URL'
                    self.libraries_List.clear()
                    self.libraries_List.addItems(list(self.libsData.keys()))
                    # Updating data
                    with open('data.pickle', 'wb') as f:
                        dump(dict(sorted(self.libsData.items())), f)
        # Clearing listWidget selection
        self.libraries_List.clearSelection()

    # Search function
    def search_update(self):
        text = self.search_Edit.text()
        tmp = self.libsData.copy()
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
