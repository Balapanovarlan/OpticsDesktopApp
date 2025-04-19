from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QComboBox, QLabel, QMainWindow, QPushButton, QTableView,
    QVBoxLayout, QScrollArea, QFormLayout, QWidget
)


class Ui_PreparedQueriesWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(234, 243, 252); font-size: 14pt;")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Основной вертикальный лейаут
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)  # Отступы
        self.verticalLayout.setSpacing(10)  # Расстояние между элементами

        # Заголовок
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: rgb(0, 51, 102); font-size: 18pt; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        # Выпадающий список запросов
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: rgb(255, 255, 255); 
                color: rgb(0, 51, 102); 
                border: 2px solid rgb(180, 220, 240);
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                border-color: rgb(100, 160, 220);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: rgb(180, 220, 240);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(255, 255, 255); 
                color: rgb(0, 51, 102); 
                selection-background-color: rgb(200, 220, 240); 
                selection-color: black; 
                border: 2px solid rgb(180, 220, 240);
            }
        """)
        self.verticalLayout.addWidget(self.comboBox)

        # Область для ввода параметров запроса (изначально скрыта)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("background-color: transparent; border: none;")
        self.scrollArea.setFixedHeight(80)
        self.scrollArea.setVisible(False)  # Скрываем область по умолчанию

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы внутри формы
        self.formLayout.setSpacing(5)  # Расстояние между полями ввода
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # Кнопка для выполнения запроса
        self.executeButton = QPushButton(self.centralwidget)
        self.executeButton.setObjectName("executeButton")
        self.executeButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 220, 240);
                color: rgb(0, 51, 102);
                border: 2px solid rgb(180, 220, 240);
                border-radius: 7px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(180, 200, 230);
            }
            QPushButton:pressed {
                background-color: rgb(150, 180, 210);
            }
        """)
        self.executeButton.setEnabled(False)  # Кнопка недоступна до выбора запроса
        self.verticalLayout.addWidget(self.executeButton)

        # Таблица для отображения результата запроса
        self.resultTable = QTableView(self.centralwidget)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 51, 102);")
        self.resultTable.horizontalHeader().setDefaultSectionSize(170)
        self.verticalLayout.addWidget(self.resultTable)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Выполнение запросов", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Выберите запрос:", None))
        self.comboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", "Выберите запрос", None))
        self.executeButton.setText(QCoreApplication.translate("MainWindow", "Выполнить запрос", None))
