from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QComboBox, QLabel, QMainWindow, QPushButton, QTableView,
    QVBoxLayout, QScrollArea,
    QFormLayout, QWidget
)


class Ui_ReportWindow(object):
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
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)  # Минимальные отступы
        self.verticalLayout.setSpacing(10)  # Расстояние между элементами

        # Заголовок
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: rgb(0, 51, 102); font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        # Выпадающий список отчетов
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: rgb(255, 255, 255); 
                color: rgb(34, 49, 63); 
                border: 2px solid rgb(200, 200, 200);
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox:hover {
                border-color: rgb(135, 206, 250);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: rgb(200, 200, 200);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(255, 255, 255); 
                color: rgb(34, 49, 63); 
                selection-background-color: rgb(135, 206, 250); 
                selection-color: rgb(34, 49, 63); 
                border: 1px solid rgb(200, 200, 200);
            }
        """)
        self.verticalLayout.addWidget(self.comboBox)

        # Область для ввода параметров отчета (изначально скрыта)
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
        self.formLayout.setSpacing(10)  # Расстояние между полями ввода
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        # Кнопка для генерации отчета
        self.generateReportButton = QPushButton(self.centralwidget)
        self.generateReportButton.setObjectName("generateReportButton")
        self.generateReportButton.setStyleSheet("""
            QPushButton {
                background-color: rgb(135, 206, 250); 
                color: rgb(0, 51, 102); 
                font-weight: bold; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(173, 216, 230);
            }
            QPushButton:pressed {
                background-color: rgb(112, 160, 180);
            }
        """)
        self.generateReportButton.setEnabled(False)  # Кнопка недоступна до выбора отчета
        self.verticalLayout.addWidget(self.generateReportButton)

        # Таблица для отображения результата отчета
        self.resultTable = QTableView(self.centralwidget)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setStyleSheet("""
            QTableView {
                background-color: rgb(255, 255, 255); 
                color: rgb(0, 51, 102); 
                border: 1px solid rgb(200, 200, 200);
                gridline-color: rgb(200, 200, 200);
            }
            QHeaderView::section {
                background-color: rgb(234, 243, 252);
                color: rgb(0, 51, 102);
                border: 1px solid rgb(200, 200, 200);
                font-weight: bold;
            }
        """)
        self.resultTable.horizontalHeader().setDefaultSectionSize(170)
        self.verticalLayout.addWidget(self.resultTable)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Отчеты", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Выберите отчет:", None))
        self.comboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", "Выберите отчет", None))
        self.generateReportButton.setText(QCoreApplication.translate("MainWindow", "Сформировать отчет", None))
