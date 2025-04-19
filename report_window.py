from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit, QLabel, QFormLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from report_window_ui import Ui_ReportWindow

class ReportWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.ui = Ui_ReportWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection

        # Список отчетов и их параметры (используем имена хранимых процедур)
        self.reports = {
            "Приходная ведомость «I-го» приемщика на «j-ю» дату": {
                "proc": "usp_GetReceiptStatement",
                "params": [("Код приемщика (ReceiverCode)", "number"),
                           ("Дата платежа (PaymentDate)", "date")]
            },
            "Бланк заказа": {
                "proc": "usp_GetOrderForm",
                "params": [("Номер заказа (OrderID)", "number")]
            },
            "Заказы, выполненные работником в текущую дату": {
                "proc": "usp_GetOrdersByEmployeeToday",
                "params": [("Код сотрудника (EmployeeID)", "number")]
            }
        }

        # Добавление отчетов в выпадающий список
        self.ui.comboBox.addItems(["Выберите отчет"] + list(self.reports.keys()))
        self.ui.comboBox.setCurrentIndex(0)

        # Событие при изменении отчета
        self.ui.comboBox.currentIndexChanged.connect(self.update_inputs)

        # Подключение кнопки
        self.ui.generateReportButton.clicked.connect(self.generate_report)

        # Скрыть область ввода параметров по умолчанию
        self.ui.scrollArea.setVisible(False)
        self.ui.generateReportButton.setEnabled(False)

    def update_inputs(self):
        """
        Обновляет поля ввода параметров в зависимости от выбранного отчета.
        """
        report_name = self.ui.comboBox.currentText()
        self.clear_inputs()

        if report_name != "Выберите отчет" and report_name in self.reports:
            self.ui.scrollArea.setVisible(True)
            self.ui.generateReportButton.setEnabled(True)
            for param_name, param_type in self.reports[report_name]["params"]:
                label = QLabel(param_name, self)
                label.setStyleSheet("color: rgb(0, 51, 102);")
                if param_type == "date":
                    from PySide6.QtWidgets import QDateEdit
                    from PySide6.QtCore import QDate
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
            self.ui.generateReportButton.setEnabled(False)

    def clear_inputs(self):
        """
        Очищает текущие поля ввода.
        """
        while self.ui.formLayout.rowCount():
            self.ui.formLayout.removeRow(0)

    def generate_report(self):
        """
        Генерирует отчет на основе введенных параметров, вызывая хранимую процедуру.
        """
        report_name = self.ui.comboBox.currentText()
        if not report_name or report_name not in self.reports:
            QMessageBox.warning(self, "Предупреждение", "Выберите отчет из списка.")
            return

        # Получить параметры
        params = []
        for i in range(self.ui.formLayout.rowCount()):
            input_field = self.ui.formLayout.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            # Для дат преобразуем в нужный формат
            if hasattr(input_field, "date"):
                params.append(input_field.date().toString("yyyy-MM-dd"))
            else:
                params.append(input_field.text().strip())

        if self.reports[report_name]["params"] and not all(params):
            QMessageBox.warning(self, "Предупреждение", "Заполните все параметры.")
            return

        # Формирование вызова хранимой процедуры
        proc_name = self.reports[report_name]["proc"]
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
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчет: {e}")

    def populate_table(self, results, columns):
        """
        Отображает результаты отчета в таблице.
        """
        if not results:
            QMessageBox.information(self, "Результат", "Нет данных для отображения.")
            return

        model = QStandardItemModel(len(results), len(columns))
        model.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(results):
            for col_idx, value in enumerate(row_data):
                item = QStandardItem(str(value))
                model.setItem(row_idx, col_idx, item)

        self.ui.resultTable.setModel(model)
