import sys

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QVBoxLayout

sys.path.insert(1, 'C:/Users/l1nt3x/PycharmProjects/compilation-of-python-libs-docs/ui')

from mainui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(self.size())

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.listWidget.addItems(('Python', 'PyQt5', 'Random'))
        self.listWidget.installEventFilter(self)
        layout.addWidget(self.listWidget)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            if source.itemAt(event.pos()) != None:
                menu = QMenu()
                menu.addAction('Open')
                # TODO: сделать открытие в WebView
                menu.addAction('Delete')
                # TODO: сделать new для самого виджета
                # TODO: исправить баги
                if menu.exec_(event.globalPos()):
                    item = source.itemAt(event.pos())
                    print(item.text())
                return True
            return super().eventFilter(source, event)
        return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QListWidget, QVBoxLayout
# from PyQt5.QtCore import QEvent, Qt
#
#
# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Insert Context Menu to ListWidget')
#         self.window_width, self.window_height = 800, 600
#         self.setMinimumSize(self.window_width, self.window_height)
#
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#
#         self.listWidget = QListWidget()
#         self.listWidget.addItems(('Facebook', 'Microsoft', 'Google'))
#         self.listWidget.installEventFilter(self)
#         layout.addWidget(self.listWidget)
#
#     def eventFilter(self, source, event):
#         if event.type() == QEvent.ContextMenu and source is self.listWidget:
#             menu = QMenu()
#             menu.addAction('Action 1')
#             menu.addAction('Action 2')
#             menu.addAction('Action 3')
#
#             if menu.exec_(event.globalPos()):
#                 item = source.itemAt(event.pos())
#                 print(item.text())
#             return True
#         return super().eventFilter(source, event)
#
#
# if __name__ == '__main__':
#     # don't auto scale.
#     QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#
#     app = QApplication(sys.argv)
#     app.setStyleSheet('''
#         QWidget {
#             font-size: 30px;
#         }
#     ''')
#
#     myApp = MyApp()
#     myApp.show()
#
#     try:
#         sys.exit(app.exec_())
#     except SystemExit:
#         print('Closing Window...')
