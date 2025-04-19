from PySide6.QtWidgets import QMainWindow
from main_window_ui import Ui_MainWindow
from view_window import ViewWindow
from report_window import ReportWindow
from security_window import SecurityWindow
from help_window import HelpWindow
from prepared_queries import PreparedQueriesWindow

class MainWindow(QMainWindow):
    def __init__(self, db_connection, user_role):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection
        self.user_role = user_role  # Роль, переданная из окна логина

        # Настраиваем интерфейс в зависимости от роли пользователя
        self.setup_role_ui()

        self.ui.viewDataButton.clicked.connect(self.open_view_window)
        self.ui.reportButton.clicked.connect(self.open_reports_window)
        self.ui.securityButton.clicked.connect(self.open_security_window)
        self.ui.helpButton.clicked.connect(self.open_help_window)
        self.ui.exitButton.clicked.connect(self.close)
        self.ui.preparedQueriesButton.clicked.connect(self.open_prepared_queries_window)

    def setup_role_ui(self):
        # Например, если роль клиента, скрываем кнопки отчетов и запросов
        if self.user_role.lower() == "client":
            self.ui.reportButton.hide()
            self.ui.preparedQueriesButton.hide()
            self.ui.securityButton.hide()

        # Для работников можно оставить только ограниченный функционал
        elif self.user_role.lower() == "employee":
            self.ui.reportButton.hide() 
            self.ui.preparedQueriesButton.hide()
            self.ui.securityButton.hide()

        # Если роль приемщика или админа — оставляем все кнопки, либо делаем индивидуальные настройки

    def open_view_window(self):
        self.view_window = ViewWindow(self.db_connection)
        self.view_window.show()

    def open_reports_window(self):
        self.reports_window = ReportWindow(self.db_connection)
        self.reports_window.show()

    def open_security_window(self):
        self.security_window = SecurityWindow(self.db_connection)
        self.security_window.show()

    def open_help_window(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def open_prepared_queries_window(self):
        self.prepared_queries_window = PreparedQueriesWindow(self.db_connection)
        self.prepared_queries_window.show()
