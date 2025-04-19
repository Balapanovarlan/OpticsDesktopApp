from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, QTextEdit


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        if not HelpWindow.objectName():
            HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(600, 400)
        HelpWindow.setStyleSheet("background-color: rgb(234, 243, 252); font-size: 14pt;")

        self.centralwidget = QWidget(HelpWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QRect(20, 20, 560, 360))
        self.layoutWidget.setObjectName("layoutWidget")

        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: rgb(0, 51, 102); font-size: 18pt; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        # Текст справки
        self.helpText = QTextEdit(self.layoutWidget)
        self.helpText.setObjectName("helpText")
        self.helpText.setReadOnly(True)
        self.helpText.setStyleSheet(
            "background-color: rgb(255, 255, 255); "
            "color: rgb(0, 51, 102); "
            "border: 2px solid rgb(200, 220, 240); "
            "border-radius: 10px;"
        )
        self.verticalLayout.addWidget(self.helpText)

        HelpWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HelpWindow)
        QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        HelpWindow.setWindowTitle(QCoreApplication.translate("HelpWindow", "Справка", None))
        self.label.setText(QCoreApplication.translate("HelpWindow", "Справочная информация", None))
