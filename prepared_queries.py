from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QLabel, QFormLayout, QDateEdit
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from PySide6.QtCore import QDate
from prepared_queries_ui import Ui_PreparedQueriesWindow
from datetime import datetime

class PreparedQueriesWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.ui = Ui_PreparedQueriesWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection

        # Список запросов в виде хранимых процедур и их параметры
        self.queries = {
            "Список оправ, которые были реализованы «I-го» числа": {
                "proc": "GetSoldFramesByDate",
                "params": [("Дата (OrderDate)", "date")]
            },
            "Перечень заказов, где ФИО заказчика «. . . .»": {
                "proc": "GetOrdersByCustomer",
                "params": [("ФИО заказчика (CustomerName)", "text")]
            },
            "Количество заказов, выполненных каждым из работников": {
                "proc": "GetOrdersCountByEmployee",
                "params": []
            },
            "Вычислить плановую дату выполнения каждого из заказов": {
                "proc": "GetPlannedCompletionDates",
                "params": []
            },
            "Сумма прихода по каждому из дней I-го месяца текущего года": {
                "proc": "GetDailyRevenueByMonth",
                "params": [("Номер месяца (MonthNumber)", "number")]
            },
        }

        # Добавление запросов в выпадающий список
        self.ui.comboBox.addItems(["Выберите запрос"] + list(self.queries.keys()))
        self.ui.comboBox.setCurrentIndex(0)

        # Событие при изменении запроса
        self.ui.comboBox.currentIndexChanged.connect(self.update_inputs)

        # Подключение кнопки выполнения
        self.ui.executeButton.clicked.connect(self.execute_query)

        # Скрыть область ввода параметров по умолчанию
        self.ui.scrollArea.setVisible(False)
        self.ui.executeButton.setEnabled(False)

    def update_inputs(self):
        """
        Обновляет поля ввода параметров в зависимости от выбранного запроса.
        """
        query_name = self.ui.comboBox.currentText()
        self.clear_inputs()

        if query_name != "Выберите запрос" and query_name in self.queries:
            self.ui.scrollArea.setVisible(True)
            self.ui.executeButton.setEnabled(True)
            for param_name, param_type in self.queries[query_name]["params"]:
                label = QLabel(param_name, self)
                label.setStyleSheet("color: rgb(0, 51, 102);")

                if param_type == "date":
                    input_field = QDateEdit(self)
                    input_field.setCalendarPopup(True)
                    input_field.setDisplayFormat("yyyy-MM-dd")
                    input_field.setDate(QDate.currentDate())
                elif param_type == "number":
                    input_field = QLineEdit(self)
                    input_field.setPlaceholderText("Введите число")
                    input_field.setValidator(QIntValidator())
                else:
                    input_field = QLineEdit(self)

                input_field.setStyleSheet("color: rgb(0, 51, 102); background-color: rgb(255,255,255)")
                input_field.setObjectName(param_name)
                self.ui.formLayout.addRow(label, input_field)
        else:
            self.ui.scrollArea.setVisible(False)
            self.ui.executeButton.setEnabled(False)

    def clear_inputs(self):
        """
        Очищает текущие поля ввода.
        """
        while self.ui.formLayout.rowCount():
            self.ui.formLayout.removeRow(0)

    def execute_query(self):
        """
        Выполняет вызов хранимой процедуры на основе введенных параметров.
        """
        query_name = self.ui.comboBox.currentText()
        if not query_name or query_name not in self.queries:
            QMessageBox.warning(self, "Предупреждение", "Выберите запрос из списка.")
            return

        # Получение параметров
        params = []
        for i in range(self.ui.formLayout.rowCount()):
            input_field = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            if isinstance(input_field, QDateEdit):
                params.append(input_field.date().toString("yyyy-MM-dd"))
            else:
                params.append(input_field.text().strip())

        if self.queries[query_name]["params"] and not all(params):
            QMessageBox.warning(self, "Предупреждение", "Заполните все параметры.")
            return

        # Формирование вызова хранимой процедуры
        proc_name = self.queries[query_name]["proc"]
        # Формируем строку вызова: если есть параметры, добавляем символы ? через запятую
        if params:
            placeholders = ", ".join(["?"] * len(params))
            exec_command = f"EXEC {proc_name} {placeholders}"
        else:
            exec_command = f"EXEC {proc_name}"

        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute(exec_command, tuple(params))
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            # Отображение результатов
            self.populate_table(results, columns)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось выполнить запрос: {e}")

    def populate_table(self, results, columns):
        """
        Отображает результаты запроса в таблице.
        """
        if not results:
            QMessageBox.information(self, "Результат", "Нет данных для отображения.")
            return

        # Создание модели для отображения данных
        model = QStandardItemModel(len(results), len(columns))
        model.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(results):
            for col_idx, value in enumerate(row_data):
                item = QStandardItem(str(value))
                model.setItem(row_idx, col_idx, item)

        self.ui.resultTable.setModel(model)
