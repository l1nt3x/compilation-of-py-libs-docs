import pickle
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QVBoxLayout

sys.path.insert(1, 'C:/Users/l1nt3x/PycharmProjects/compilation-of-python-libs-docs/ui')

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
        newAct = ''
        check = 'xd'
        if ''.join([item.text() for item in self.listWidget.selectedItems()]) == '':
            newAct = contextMenu.addAction("New")
            check = 'new'
        else:
            openAct = contextMenu.addAction("Open")
            deleteAct = contextMenu.addAction("Delete")
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
                web = QWebEngineView()
                web.Load(QUrl(self.libsData[tmp[0]]))
                # web.setWindowTitle(self.libsData[tmp[0]])
                web.show()
        self.listWidget.clearSelection()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
