from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(406, 567)  # Размер окна
        Dialog.setFixedSize(406, 567)  # Фиксируем размер окна
        Dialog.setStyleSheet(
            "background-color: rgb(234, 243, 252);\n"
            "font: 14pt \"Sans Serif Collection\";"
        )

        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(50, 20, 301, 521))

        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.label.setEnabled(True)
        font = QFont()
        font.setFamilies(["Sans Serif Collection"])
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet(
            "background-color: rgba(255,255,255,0);\n"
            "color: rgb(0, 51, 102);\n"  # Тёмно-синий текст
            "border: none;\n"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"  # Белый фон
            "color: rgb(0, 51, 102);\n"  # Тёмно-синий текст
            "border: 1px solid rgb(173, 216, 230);\n"  # Голубая граница
            "border-radius: 10px;\n"
            "padding: 5px;"
        )
        self.verticalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(
            "background-color: rgba(255,255,255,0);\n"
            "color: rgb(0, 51, 102);\n"  # Тёмно-синий текст
            "border: none;\n"
        )
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "color: rgb(0, 51, 102);\n"
            "border: 1px solid rgb(173, 216, 230);\n"
            "border-radius: 10px;\n"
            "padding: 5px;"
        )
        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet(
            "background-color: rgba(255,255,255,0);\n"
            "color: rgb(0, 51, 102);\n"
            "border: none;\n"
        )
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(self.layoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "color: rgb(0, 51, 102);\n"
            "border: 1px solid rgb(173, 216, 230);\n"
            "border-radius: 10px;\n"
            "padding: 5px;"
        )
        self.verticalLayout.addWidget(self.lineEdit_3)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setStyleSheet(
            "background-color: rgba(255,255,255,0);\n"
            "color: rgb(0, 51, 102);\n"
            "border: none;\n"
        )
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(self.layoutWidget)
        self.lineEdit_4.setEchoMode(QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "color: rgb(0, 51, 102);\n"
            "border: 1px solid rgb(173, 216, 230);\n"
            "border-radius: 10px;\n"
            "padding: 5px;"
        )
        self.verticalLayout.addWidget(self.lineEdit_4)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(
            "QPushButton{\n"
            "background-color: rgb(0, 123, 255);\n"  # Синий фон
            "border: none;\n"
            "color: white;\n"  # Белый текст
            "border-radius: 7px;\n"
            "padding: 10px;\n"
            "}\n"
            "QPushButton:hover{\n"
            "background-color: rgb(30, 144, 255);\n"  # Ярко-синий на наведение
            "}\n"
            "QPushButton:pressed{\n"
            "background-color: rgb(25, 25, 112);\n"  # Тёмно-синий на нажатие
            "}\n"
        )
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Login", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Имя сервера", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Имя базы данных", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "Имя пользователя", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "Пароль", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", "Подключиться", None))
