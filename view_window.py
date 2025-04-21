from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QInputDialog, QDialog, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from view_window_ui import Ui_ViewWindow


class ViewWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.ui = Ui_ViewWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection

        # Настройка кнопок
        self.ui.addButton.clicked.connect(self.add_data)
        self.ui.editButton.clicked.connect(self.edit_data)
        self.ui.deleteButton.clicked.connect(self.delete_data)

        # Загрузка списка таблиц и настройка обработчика изменений
        self.load_table_list()
        self.ui.comboBox.currentIndexChanged.connect(self.load_table_data)

        # Разрешаем редактирование таблицы
        self.ui.tableView.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)

    def load_table_list(self):
        """Загружает список пользовательских таблиц из базы данных."""
        try:
            # Получаем список всех пользовательских таблиц (исключая системные)
            query = """
                SELECT t.name AS table_name
                FROM sys.tables t
                WHERE t.is_ms_shipped = 0
                ORDER BY t.name
            """
            cursor = self.db_connection.execute_query(query)
            tables = [row[0] for row in cursor.fetchall()]

            # Очищаем и заполняем ComboBox
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("Выберите таблицу из списка")
            
            if tables:
                self.ui.comboBox.addItems(tables)
            else:
                QMessageBox.warning(self, "Внимание", "В базе данных не найдено пользовательских таблиц.")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список таблиц: {str(e)}")

    def load_table_data(self):
        """Загружает данные выбранной таблицы."""
        table_name = self.ui.comboBox.currentText()
        if table_name == "Выберите таблицу из списка" or not table_name:
            return

        try:
            # Безопасное формирование запроса с проверкой имени таблицы
            if not self.is_valid_table_name(table_name):
                raise ValueError("Некорректное имя таблицы")

            # Получаем данные и метаинформацию о таблице
            query = f"SELECT * FROM [{table_name}]"
            cursor = self.db_connection.execute_query(query)
            
            # Получаем данные и названия столбцов
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            # Заполняем таблицу
            self.populate_table(results, columns)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def is_valid_table_name(self, name):
        """Проверяет, является ли имя таблицы безопасным."""
        # Простая проверка - имя должно содержать только буквы, цифры и подчеркивания
        return all(c.isalnum() or c == '_' for c in name)

    def populate_table(self, results, columns):
        """Заполняет таблицу данными."""
        model = QStandardItemModel(len(results), len(columns))
        model.setHorizontalHeaderLabels(columns)
        
        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                item = QStandardItem(str(value) if value is not None else "NULL")
                item.setEditable(True)
                model.setItem(row_idx, col_idx, item)
                
        self.ui.tableView.setModel(model)
        self.ui.tableView.horizontalHeader().setDefaultSectionSize(150)

    def add_data(self):
        """Добавляет новую запись в таблицу."""
        table_name = self.ui.comboBox.currentText()
        if not table_name or table_name == "Выберите таблицу из списка":
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для добавления данных.")
            return

        try:
            # Получаем информацию о столбцах таблицы
            columns_query = f"""
                SELECT c.name, t.name AS type_name, c.is_nullable
                FROM sys.columns c
                JOIN sys.types t ON c.user_type_id = t.user_type_id
                WHERE c.object_id = OBJECT_ID('{table_name}')
                ORDER BY c.column_id
            """
            cursor = self.db_connection.execute_query(columns_query)
            columns_info = cursor.fetchall()

            # Создаем диалоговое окно для ввода данных
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Добавить запись в {table_name}")
            dialog.setMinimumWidth(600)
            layout = QVBoxLayout(dialog)

            # Создаем таблицу для ввода данных
            table_widget = QTableWidget(1, len(columns_info))
            table_widget.setHorizontalHeaderLabels([col[0] for col in columns_info])
            layout.addWidget(table_widget)

            # Кнопка добавления
            btn_add = QPushButton("Добавить")
            layout.addWidget(btn_add)

            def save_data():
                try:
                    # Формируем запрос INSERT
                    columns = []
                    values = []
                    
                    for col_idx, (col_name, col_type, is_nullable) in enumerate(columns_info):
                        item = table_widget.item(0, col_idx)
                        value = item.text() if item else ""
                        
                        # Обработка NULL значений
                        if not value and is_nullable:
                            values.append("NULL")
                        elif col_type in ('varchar', 'nvarchar', 'char', 'nchar', 'text'):
                            values.append(f"'{value.replace("'", "''")}'")
                        elif col_type in ('int', 'float', 'decimal', 'bit'):
                            values.append(value if value else "NULL")
                        else:
                            values.append(f"'{value}'")
                            
                        columns.append(f"[{col_name}]")

                    insert_query = f"""
                        INSERT INTO [{table_name}] ({', '.join(columns)})
                        VALUES ({', '.join(values)})
                    """
                    
                    self.db_connection.execute_query(insert_query)
                    QMessageBox.information(self, "Успех", "Данные успешно добавлены!")
                    dialog.close()
                    self.load_table_data()
                    
                except Exception as e:
                    QMessageBox.critical(dialog, "Ошибка", f"Ошибка при добавлении данных: {str(e)}")

            btn_add.clicked.connect(save_data)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подготовить форму добавления: {str(e)}")

    def edit_data(self):
        """Редактирует выбранную запись."""
        selected = self.ui.tableView.selectionModel().selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Внимание", "Выберите ячейку для редактирования.")
            return

        table_name = self.ui.comboBox.currentText()
        if not table_name or table_name == "Выберите таблицу из списка":
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для редактирования.")
            return

        try:
            # Получаем информацию о первичном ключе
            pk_query = f"""
                SELECT c.name
                FROM sys.indexes i
                JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                WHERE i.is_primary_key = 1 AND i.object_id = OBJECT_ID('{table_name}')
            """
            cursor = self.db_connection.execute_query(pk_query)
            pk_columns = [row[0] for row in cursor.fetchall()]

            if not pk_columns:
                QMessageBox.warning(self, "Внимание", "Таблица не имеет первичного ключа. Редактирование невозможно.")
                return

            # Получаем данные модели
            model = self.ui.tableView.model()
            row = selected[0].row()
            col = selected[0].column()
            
            # Получаем новое значение
            new_value = model.data(model.index(row, col))
            column_name = model.headerData(col, Qt.Horizontal)
            
            # Получаем значения первичного ключа
            pk_values = []
            for pk_col in pk_columns:
                pk_col_index = -1
                for i in range(model.columnCount()):
                    if model.headerData(i, Qt.Horizontal) == pk_col:
                        pk_col_index = i
                        break
                
                if pk_col_index == -1:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось найти столбец первичного ключа {pk_col}")
                    return
                
                pk_value = model.data(model.index(row, pk_col_index))
                pk_values.append((pk_col, pk_value))

            # Формируем условие WHERE
            where_parts = []
            for pk_col, pk_value in pk_values:
                if isinstance(pk_value, str):
                    where_parts.append(f"[{pk_col}] = '{pk_value.replace("'", "''")}'")
                else:
                    where_parts.append(f"[{pk_col}] = {pk_value}")

            # Формируем запрос UPDATE
            if isinstance(new_value, str):
                new_value = new_value.replace("'", "''")
                update_value = f"'{new_value}'" if new_value != "NULL" else "NULL"
            else:
                update_value = str(new_value) if new_value is not None else "NULL"

            update_query = f"""
                UPDATE [{table_name}]
                SET [{column_name}] = {update_value}
                WHERE {' AND '.join(where_parts)}
            """

            self.db_connection.execute_query(update_query)
            QMessageBox.information(self, "Успех", "Данные успешно обновлены!")
            self.load_table_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных: {str(e)}")

    def delete_data(self):
        """Удаляет выбранную запись."""
        selected = self.ui.tableView.selectionModel().selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления.")
            return

        table_name = self.ui.comboBox.currentText()
        if not table_name or table_name == "Выберите таблицу из списка":
            QMessageBox.warning(self, "Внимание", "Выберите таблицу для удаления.")
            return

        try:
            # Получаем информацию о первичном ключе
            pk_query = f"""
                SELECT c.name
                FROM sys.indexes i
                JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
                JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
                WHERE i.is_primary_key = 1 AND i.object_id = OBJECT_ID('{table_name}')
            """
            cursor = self.db_connection.execute_query(pk_query)
            pk_columns = [row[0] for row in cursor.fetchall()]

            if not pk_columns:
                QMessageBox.warning(self, "Внимание", "Таблица не имеет первичного ключа. Удаление невозможно.")
                return

            # Получаем данные модели
            model = self.ui.tableView.model()
            row = selected[0].row()
            
            # Получаем значения первичного ключа
            pk_values = []
            for pk_col in pk_columns:
                pk_col_index = -1
                for i in range(model.columnCount()):
                    if model.headerData(i, Qt.Horizontal) == pk_col:
                        pk_col_index = i
                        break
                
                if pk_col_index == -1:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось найти столбец первичного ключа {pk_col}")
                    return
                
                pk_value = model.data(model.index(row, pk_col_index))
                pk_values.append((pk_col, pk_value))

            # Формируем условие WHERE
            where_parts = []
            for pk_col, pk_value in pk_values:
                if isinstance(pk_value, str):
                    where_parts.append(f"[{pk_col}] = '{pk_value.replace("'", "''")}'")
                else:
                    where_parts.append(f"[{pk_col}] = {pk_value}")

            # Запрос подтверждения
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Вы уверены, что хотите удалить выбранную запись?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                delete_query = f"""
                    DELETE FROM [{table_name}]
                    WHERE {' AND '.join(where_parts)}
                """
                
                self.db_connection.execute_query(delete_query)
                QMessageBox.information(self, "Успех", "Запись успешно удалена!")
                self.load_table_data()
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении данных: {str(e)}")