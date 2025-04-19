from PySide6.QtWidgets import QDialog, QMessageBox
from login_ui import Ui_Dialog
from main_window import MainWindow
from db_connection import DatabaseConnection

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Установка предустановленных данных
        self.ui.lineEdit.setText("localhost")  # Имя сервера
        self.ui.lineEdit_2.setText("Optics")    # Имя базы данных
        self.ui.lineEdit_3.setText("admin_optics") # Логин
        self.ui.lineEdit_4.setText("Admin@123")   # Пароль

        # Подключение кнопки
        self.ui.pushButton.clicked.connect(self.connect_to_db)

    def connect_to_db(self):
        server = self.ui.lineEdit.text()
        database = self.ui.lineEdit_2.text()
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()

        try:
            # Подключение к БД
            self.db = DatabaseConnection(server, database, username, password)
            self.db.connect()
            QMessageBox.information(self, "Успех", "Подключение успешно установлено!")

            # Получаем роль пользователя через метод get_user_role
            user_role = self.get_user_role(username)

            # Закрываем окно логина и открываем главное меню с передачей роли
            self.close()
            self.main_window = MainWindow(self.db, user_role)
            self.main_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться: {e}")

    def get_user_role(self, username):
        """
        Определяет роль пользователя на основе логина.
        В данном примере роль задается статически. 
        При необходимости можно заменить этот метод запросом к таблице пользователей.
        """
        username = username.lower()
        if username == "admin_optics":
            return "admin"
        elif username == "reception_optics":
            return "receiver"
        elif username == "employee_optics":
            return "employee"
        elif username == "client_optics":
            return "client"
        else:
            # По умолчанию, если логин не найден, считаем пользователя клиентом
            return "client"
