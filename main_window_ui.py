from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 500)
        MainWindow.setStyleSheet("background-color: rgb(234, 243, 252); font-size: 14pt;")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QRect(100, 50, 400, 400))
        self.layoutWidget.setObjectName("layoutWidget")

        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: rgb(0, 51, 102); font-size: 18pt;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        # Кнопка "Просмотр данных"
        self.viewDataButton = QPushButton(self.layoutWidget)
        self.viewDataButton.setObjectName("viewDataButton")
        self.viewDataButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.viewDataButton)

        # Кнопка "Отчеты"
        self.reportButton = QPushButton(self.layoutWidget)
        self.reportButton.setObjectName("reportButton")
        self.reportButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.reportButton)

        # Кнопка "Запросы"
        self.preparedQueriesButton = QPushButton(self.layoutWidget)
        self.preparedQueriesButton.setObjectName("preparedQueriesButton")
        self.preparedQueriesButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.preparedQueriesButton)

        #Кнопка Безопасность
        self.securityButton = QPushButton(self.layoutWidget)
        self.securityButton.setObjectName('securityButton')
        self.securityButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.securityButton)

        # Кнопка "Справка"
        self.helpButton = QPushButton(self.layoutWidget)
        self.helpButton.setObjectName("helpButton")
        self.helpButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.helpButton)

        # Кнопка "Выход"
        self.exitButton = QPushButton(self.layoutWidget)
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setStyleSheet(
            "QPushButton {\n"
            "background-color: rgb(0, 123, 255);\n"
            "color: white;\n"
            "font-size: 14pt;\n"
            "border-radius: 10px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(30, 144, 255);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "background-color: rgb(25, 25, 112);\n"
            "}\n"
        )
        self.verticalLayout.addWidget(self.exitButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Главное меню", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Выберите действие:", None))
        self.viewDataButton.setText(QCoreApplication.translate("MainWindow", "Просмотр данных", None))
        self.reportButton.setText(QCoreApplication.translate("MainWindow", "Отчеты", None))
        self.preparedQueriesButton.setText(QCoreApplication.translate("MainWindow", "Запросы", None))
        self.securityButton.setText(QCoreApplication.translate('MainWindow', 'Безопасность', None))
        self.helpButton.setText(QCoreApplication.translate("MainWindow", "Справка", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", "Выход", None))
