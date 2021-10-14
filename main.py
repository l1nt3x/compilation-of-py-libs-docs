import pickle
import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QVBoxLayout, QInputDialog, QDialog, \
    QPushButton, QLabel

from mainui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open('data.pickle', 'rb') as f:
            self.libsData = pickle.load(f)

        self.setFixedSize(self.size())

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.listWidget.addItems(list(self.libsData.keys()))
        self.listWidget.installEventFilter(self)
        layout.addWidget(self.listWidget)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        deleteAct = ''
        openAct = ''
        editAct = ''
        check = 'xd'
        changeLinkAct = ''

        if ''.join([item.text() for item in self.listWidget.selectedItems()]) == '':
            newAct = contextMenu.addAction("New")
            check = 'new'
        else:
            openAct = contextMenu.addAction("Open")
            deleteAct = contextMenu.addAction("Delete")
            editAct = contextMenu.addAction('Edit')
            changeLinkAct = contextMenu.addAction('Change lib link')
            check = 'opedel'
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if check == 'opedel':
            tmp = [item.text() for item in self.listWidget.selectedItems()]
            if action == deleteAct:
                self.listWidget.clear()
                del self.libsData[tmp[0]]
                self.listWidget.addItems(list(self.libsData.keys()))
                with open('data.pickle', 'wb') as f:
                    pickle.dump(self.libsData, f)
            elif action == openAct:
                if self.libsData[tmp[0]] == 'No link':
                    dlg = QDialog()
                    dlg.setFixedSize(160, 70)
                    b1 = QPushButton("OK", dlg)
                    b1.move(40, 40)
                    b1.clicked.connect(dlg.close)
                    l1 = QLabel('Please change link for this lib', dlg)
                    l1.move(10, 10)
                    dlg.setWindowTitle("No link")
                    dlg.setWindowModality(Qt.ApplicationModal)
                    dlg.exec_()
                else:
                    webbrowser.open(self.libsData[tmp[0]])

            elif action == changeLinkAct:
                edit_link, ok_pressed = QInputDialog.getText(self, "Change link",
                                                             "Input lib link:")
                if ok_pressed:
                    self.libsData[tmp[0]] = edit_link
                    with open('data.pickle', 'wb') as f:
                        pickle.dump(self.libsData, f)
            elif action == editAct:
                edit_entry, ok_pressed = QInputDialog.getText(self, "Edit entry",
                                                              "Input new lib name:")
                if ok_pressed:
                    del self.libsData[tmp[0]]
                    self.libsData[edit_entry] = 'No link'
                    self.listWidget.clear()
                    self.listWidget.addItems(list(self.libsData.keys()))
                    with open('data.pickle', 'wb') as f:
                        pickle.dump(self.libsData, f)
        elif check == 'new':
            new_entry, ok_pressed = QInputDialog.getText(self, "New entry", "Input lib name:")
            if ok_pressed:
                self.libsData[new_entry] = 'No link'
                self.listWidget.clear()
                self.listWidget.addItems(list(self.libsData.keys()))
                with open('data.pickle', 'wb') as f:
                    pickle.dump(self.libsData, f)
        self.listWidget.clearSelection()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
