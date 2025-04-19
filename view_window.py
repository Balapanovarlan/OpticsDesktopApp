from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QInputDialog, QDialog, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from view_window_ui import Ui_ViewWindow


class ViewWindow(QMainWindow):
    ALLOWED_TABLES = [
        "Orders", "Employees", "Receivers", "Order_Lens", "Lens",
        "Frames", "Order_Frames", "Order_Cash", "Order_Services", "Services", "TestMask"
    ]

    def __init__(self, db_connection):
        super().__init__()
        self.ui = Ui_ViewWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection

        self.ui.addButton.clicked.connect(self.add_data)
        self.ui.editButton.clicked.connect(self.edit_data)
        self.ui.deleteButton.clicked.connect(self.delete_data)

        # Загрузить список таблиц из БД
        self.load_table_list()
        self.ui.comboBox.currentIndexChanged.connect(self.load_table_data)

        # Установить возможность редактирования в таблице
        self.ui.tableView.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)

    def load_table_list(self):
        """
        Загружает список таблиц из базы данных и добавляет их в ComboBox.
        """
        try:
            query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            cursor = self.db_connection.execute_query(query)
            all_tables = [row[0] for row in cursor.fetchall()]

            # Фильтрация таблиц
            filtered_tables = [table for table in all_tables if table in self.ALLOWED_TABLES]

            # Очистить ComboBox перед добавлением
            self.ui.comboBox.clear()

            # Добавить текст "Выберите таблицу из списка" как первый элемент
            self.ui.comboBox.addItem("Выберите таблицу из списка")
            self.ui.comboBox.setCurrentIndex(0)  # Устанавливаем этот текст как выбранный

            if filtered_tables:
                self.ui.comboBox.addItems(filtered_tables)
            else:
                QMessageBox.warning(self, "Внимание", "Не найдено подходящих таблиц в базе данных.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список таблиц.")


    def load_table_data(self):
        """
        Загружает данные выбранной таблицы и отображает их в QTableView.
        """
        table_name = self.ui.comboBox.currentText()
        if table_name == "Выберите таблицу из списка" or not table_name:
            QMessageBox.information(self, "Информация", "Пожалуйста, выберите таблицу из списка.")
            return

        try:
            query = f"SELECT * FROM {table_name}"
            cursor = self.db_connection.execute_query(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.populate_table(results, columns)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные из таблицы.")

    def populate_table(self, results, columns):
        """
        Заполняет QTableView данными.
        """
        model = QStandardItemModel(len(results), len(columns))
        model.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                model.setItem(row_idx, col_idx, QStandardItem(str(value)))
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setDefaultSectionSize(150)

    def add_data(self):
        """
        Открывает диалоговое окно для добавления новых данных.
        """
        table_name = self.ui.comboBox.currentText()
        if not table_name:
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для добавления данных.")
            return

        # Получить заголовки столбцов
        columns_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
        cursor = self.db_connection.execute_query(columns_query)
        columns = [row[0] for row in cursor.fetchall()]

        # Создание модального окна для ввода данных
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить запись")
        dialog.resize(800, 200)
        dialog_layout = QVBoxLayout(dialog)

        table_widget = QTableWidget(1, len(columns))
        table_widget.setHorizontalHeaderLabels(columns)
        table_widget.horizontalHeader().setDefaultSectionSize(150)
        dialog_layout.addWidget(table_widget)

        add_button = QPushButton("Добавить")
        dialog_layout.addWidget(add_button)

        def save_data():
            values = [
                f"'{table_widget.item(0, col).text()}'" if table_widget.item(0, col) else "NULL"
                for col in range(len(columns))
            ]
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(values)})"
            try:
                self.db_connection.execute_query(insert_query)
                QMessageBox.information(self, "Успех", "Данные успешно добавлены!")
                dialog.accept()
                self.load_table_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить данные.")

        add_button.clicked.connect(save_data)
        dialog.exec()

    def edit_data(self):
        """
        Сохраняет изменения, внесенные в таблицу.
        """
        selected_indexes = self.ui.tableView.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Внимание", "Выберите ячейку для редактирования.")
            return

        # Определяем строку, колонку и таблицу
        row = selected_indexes[0].row()
        column = selected_indexes[0].column()
        table_name = self.ui.comboBox.currentText()

        if not table_name:
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для редактирования данных.")
            return

        # Получаем новое значение из таблицы
        new_value = self.ui.tableView.model().data(self.ui.tableView.model().index(row, column))
        column_name = self.ui.tableView.model().headerData(column, Qt.Horizontal)
        primary_key_value = self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0))
        primary_key_column = self.ui.tableView.model().headerData(0, Qt.Horizontal)

        # Обработка имен колонок с пробелами
        column_name = f"[{column_name}]"
        primary_key_column = f"[{primary_key_column}]"

        # Обработка значений
        if new_value is None or new_value.strip() == "":
            new_value = "NULL"
        else:
            new_value = f"'{new_value}'"

        if isinstance(primary_key_value, str):
            primary_key_value = f"'{primary_key_value}'"

        # Формирование SQL-запроса
        query = f"UPDATE {table_name} SET {column_name}={new_value} WHERE {primary_key_column}={primary_key_value}"

        # Выполнение SQL-запроса
        try:
            self.db_connection.execute_query(query)
            QMessageBox.information(self, "Успех", "Данные успешно обновлены!")
            self.load_table_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные.")


    def delete_data(self):
        """
        Удаляет выбранную строку.
        """
        selected_indexes = self.ui.tableView.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Внимание", "Выберите строку для удаления.")
            return

        row = selected_indexes[0].row()
        table_name = self.ui.comboBox.currentText()
        if not table_name:
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для удаления данных.")
            return

        # Получение значения первичного ключа
        primary_key_value = self.ui.tableView.model().data(self.ui.tableView.model().index(row, 0))
        primary_key_column = self.ui.tableView.model().headerData(0, Qt.Horizontal)

        # Проверка и обработка имени колонки и значения
        primary_key_column = f"[{primary_key_column}]"  # Обрамляем имя колонки квадратными скобками
        if isinstance(primary_key_value, str):
            primary_key_value = f"'{primary_key_value}'"  # Добавляем кавычки для строковых значений

        query = f"DELETE FROM {table_name} WHERE {primary_key_column}={primary_key_value}"
        try:
            self.db_connection.execute_query(query)
            QMessageBox.information(self, "Успех", "Данные успешно удалены!")
            self.load_table_data()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось удалить данные. Возможно, есть ограничения целостности."
            )

