from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import QComboBox, QLabel, QMainWindow, QPushButton, QTableView, QVBoxLayout, QHBoxLayout, QWidget


class Ui_ViewWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(234, 243, 252); font-size: 14pt;")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: rgb(0, 51, 102);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.9); 
                color: rgb(0, 51, 102); 
                border: 2px solid rgb(200, 220, 240);
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                border-color: rgb(100, 150, 200);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: rgb(200, 220, 240);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: white; 
                color: rgb(0, 51, 102); 
                selection-background-color: rgb(200, 220, 240); 
                selection-color: black; 
                border: 2px solid rgb(200, 220, 240);
            }
        """)
        self.verticalLayout.addWidget(self.comboBox)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.tableView.setStyleSheet("background-color: rgba(255,255,255,0.9); color: rgb(0, 51, 102);")
        self.tableView.horizontalHeader().setDefaultSectionSize(170)
        self.verticalLayout.addWidget(self.tableView)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.addButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(173, 216, 230);
                color: rgb(0, 51, 102);
                font-size: 14pt;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(186, 226, 240);
            }
            QPushButton:pressed {
                background-color: rgb(155, 201, 225);
            }
        """)
        self.buttonLayout.addWidget(self.addButton)

        self.editButton = QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.editButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(173, 216, 230);
                color: rgb(0, 51, 102);
                font-size: 14pt;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(186, 226, 240);
            }
            QPushButton:pressed {
                background-color: rgb(155, 201, 225);
            }
        """)
        self.buttonLayout.addWidget(self.editButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(173, 216, 230);
                color: rgb(0, 51, 102);
                font-size: 14pt;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(186, 226, 240);
            }
            QPushButton:pressed {
                background-color: rgb(155, 201, 225);
            }
        """)
        self.buttonLayout.addWidget(self.deleteButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Просмотр данных", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Выберите таблицу для просмотра:", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", "Добавить", None))
        self.editButton.setText(QCoreApplication.translate("MainWindow", "Редактировать", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", "Удалить", None))
