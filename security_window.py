from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QAbstractItemView, QTableWidgetItem, QListWidget, QListWidgetItem, QDialogButtonBox,QDialog, QVBoxLayout
from security_window_ui import Ui_SecurityWindow
from PySide6.QtCore import Qt

class SecurityWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.ui = Ui_SecurityWindow()
        self.ui.setupUi(self)
        self.db_connection = db_connection

        db = getattr(self.db_connection, "database", None) or "-"

        self.ui.gbCreateUser.setTitle(f"Создание пользователя БД: {db}")
        self.ui.gbManageUsers.setTitle(f"Управление пользователями БД: {db}")


        # Подключаем переключение страниц
        self.ui.btnUserManagement.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btnRoleManagement.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.btnPermissions.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btnBackup.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.btnRestore.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.btnMask.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(5))
        
        # Подключаем новые обработчики
        self.ui.btnCreateLogin.clicked.connect(self.create_login)
        self.ui.btnCreateUser.clicked.connect(self.create_user)
        self.ui.btnDeleteUser.clicked.connect(self.delete_user) 
        self.ui.btnCreateRole.clicked.connect(self.create_role)
        self.ui.btnAssignRole.clicked.connect(self.assign_role)
        self.ui.btnRevokeRole.clicked.connect(self.revoke_role) 
        self.ui.btnSetPermissions.clicked.connect(self.set_permissions)
        self.ui.btnViewPermissions.clicked.connect(self.view_permissions)
        self.ui.btnChoosePath.clicked.connect(self.select_backup_path)
        self.ui.btnCreateBackup.clicked.connect(self.create_backup)
        self.ui.btnSetRecovery.clicked.connect(self.set_recovery_model)
        self.ui.btnChooseRestoreFile.clicked.connect(self.select_restore_file)
        self.ui.btnChooseStandbyFile.clicked.connect(self.select_standby_file)
        self.ui.btnRestoreDb.clicked.connect(self.restore_database)

        self.ui.btnSelectColumns.clicked.connect(self.select_columns)
        self.ui.btnDoMask.clicked.connect(self.apply_mask)
        self.ui.btnDoUnmask.clicked.connect(self.remove_mask)


        # Загрузка данных
        self.load_users_and_roles()
        self.load_current_recovery_model()
        self.load_available_logins()
        self.load_existing_users()
        self.load_mask_tables()

    def load_users_and_roles(self):
        try:
            cursor = self.db_connection.get_cursor()
            
            # Загрузка пользователей
            cursor.execute("EXEC usp_GetAllUsers")
            users = [row[0] for row in cursor.fetchall()]
            
            # Обновляем комбобоксы с пользователями
            for combo in [self.ui.cbUser, self.ui.cbExistingUsers, self.ui.cbRevokeUser]:
                combo.clear()
                combo.addItems(users)
            
            # Загрузка ролей
            cursor.execute("""
                SELECT name 
                FROM sys.database_principals 
                WHERE type = 'R' 
                AND name NOT LIKE 'db_%'  -- исключаем стандартные роли
                ORDER BY name
            """)
            roles = [row[0] for row in cursor.fetchall()]
            
            # Обновляем комбобоксы с ролями
            for combo in [self.ui.cbRole, self.ui.cbPermRole, self.ui.cbRevokeRole]:
                combo.clear()
                combo.addItems(roles)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")


    def load_mask_tables(self):
        """Заполняем список таблиц для маскировки."""
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("""
                SELECT name
                  FROM sys.tables
                 WHERE type = 'U'
                 ORDER BY name
            """)
            tables = [row[0] for row in cursor.fetchall()]
            self.ui.cbMaskTable.clear()
            self.ui.cbMaskTable.addItems(tables)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список таблиц:\n{e}")


    def load_available_logins(self):
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_GetNonSystemLogins")
            logins = [row[0] for row in cursor.fetchall()]
            
            self.ui.cbAvailableLogins.clear()
            self.ui.cbAvailableLogins.addItems(logins)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить логины: {str(e)}")

    def load_existing_users(self):
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("""
                SELECT name 
                FROM sys.database_principals 
                WHERE type IN ('S', 'U') 
                AND name NOT IN ('dbo', 'guest', 'sys', 'INFORMATION_SCHEMA')
                ORDER BY name
            """)
            users = [row[0] for row in cursor.fetchall()]            
            self.ui.cbExistingUsers.clear()
            self.ui.cbExistingUsers.addItems(users)            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить пользователей: {str(e)}")
            

    def create_login(self):
        """Создание нового логина"""
        login = self.ui.leLoginName.text().strip()
        password = self.ui.leLoginPassword.text().strip()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля для создания логина")
            return
            
        try:
            cursor = self.db_connection.get_cursor()
            # Используем параметризованный запрос для безопасности
            cursor.execute("CREATE LOGIN ? WITH PASSWORD = ?", 
                        (login, password))
            self.db_connection.connection.commit()
            
            QMessageBox.information(self, "Успех", "Логин успешно создан")
            self.load_available_logins()  # Обновляем список логинов
            
            # Очищаем поля
            self.ui.leLoginName.clear()
            self.ui.leLoginPassword.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать логин: {str(e)}")

    def create_user(self):
        login = self.ui.cbAvailableLogins.currentText()
        username = self.ui.leDbUserName.text().strip()
        
        if not login or not username:
            QMessageBox.warning(self, "Ошибка", "Выберите логин и укажите имя пользователя")
            return
            
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_CreateDatabaseUser ?, ?", (login, username))
            result = cursor.fetchone()
            
            if result.ErrorCode == 0:
                self.db_connection.connection.commit()
                QMessageBox.information(self, "Успех", result.Message)
                self.ui.leDbUserName.clear()
                self.load_existing_users()  # Обновляем список пользователей
            else:
                QMessageBox.warning(self, "Ошибка", result.Message)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать пользователя: {str(e)}")


    def create_role(self):
        """Создание новой роли через хранимую процедуру"""
        role_name = self.ui.leRoleName.text().strip()
        
        if not role_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя роли")
            return
        
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_CreateRole ?", (role_name,))
            result = cursor.fetchone()
            
            if result.ErrorCode == 0:
                self.db_connection.connection.commit()
                QMessageBox.information(self, "Успех", result.Message)
                self.load_users_and_roles()
                self.ui.leRoleName.clear()
            else:
                QMessageBox.warning(self, "Ошибка", result.Message)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать роль: {str(e)}")

    def assign_role(self):
        user = self.ui.cbUser.currentText()
        role = self.ui.cbRole.currentText()
        if not user or not role:
            QMessageBox.warning(self, "Предупреждение", "Выберите пользователя и роль.")
            return
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_AssignRoleToUser ?, ?", (user, role))
            self.db_connection.connection.commit()
            QMessageBox.information(self, "Успех", f"Роль {role} успешно назначена пользователю {user}!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось назначить роль: {e}")

    def set_permissions(self):
        role = self.ui.cbPermRole.currentText()
        obj = self.ui.cbObject.currentText()
        action = self.ui.cbAction.currentText()
        select_flag = 1 if self.ui.cbSelect.isChecked() else 0
        insert_flag = 1 if self.ui.cbInsert.isChecked() else 0
        update_flag = 1 if self.ui.cbUpdate.isChecked() else 0
        delete_flag = 1 if self.ui.cbDelete.isChecked() else 0
        execute_flag = 1 if self.ui.cbExecute.isChecked() else 0

        if not role or not obj or not action:
            QMessageBox.warning(self, "Предупреждение", "Выберите роль, объект и действие.")
            return

        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_SetTablePermissions ?, ?, ?, ?, ?, ?, ?, ?",
                           (role, obj, action, select_flag, insert_flag, update_flag, delete_flag, execute_flag))
            self.db_connection.connection.commit()
            QMessageBox.information(self, "Успех", "Права успешно применены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось установить права: {e}")

    def view_permissions(self):
        role = self.ui.cbPermRole.currentText()
        if not role:
            QMessageBox.warning(self, "Ошибка", "Выберите роль для просмотра её прав.")
            return

        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC dbo.usp_GetRolePermissions ?", (role,))
            rows = cursor.fetchall()

            if not rows:
                self.ui.tePermissionsOutput.setPlainText(f"У роли '{role}' нет явных разрешений.")
                return

            # Формируем текст вывода
            lines = []
            for state, name, cls, schema, obj in rows:
                target = obj or "(вся БД)"
                if schema:
                    target = f"{schema}.{target}"
                lines.append(f"{state:6} {name:10} on {cls:<10} {target}")
            
            self.ui.tePermissionsOutput.setPlainText("\n".join(lines))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить права роли:\n{e}")

    
    def delete_user(self):
        selected_user = self.ui.cbExistingUsers.currentText()
        # Проверяем, что пользователь выбран
        if not selected_user:
            QMessageBox.warning(
                self,
                "Ошибка выбора",
                "Пожалуйста, выберите пользователя для удаления",
                QMessageBox.StandardButton.Ok
            )
            return
        # Запрашиваем подтверждение
        confirm = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить пользователя '{selected_user}'?\n"
            "Это действие нельзя отменить!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if confirm != QMessageBox.StandardButton.Yes:
            return
        
        try:
            # Выполняем удаление через хранимую процедуру
            with self.db_connection.get_cursor() as cursor:
                cursor.execute("EXEC usp_DeleteDatabaseUser @UserName = ?", selected_user)
                result = cursor.fetchone()
                
                # Обрабатываем результат
                if result.ErrorCode == 0:
                    self.db_connection.connection.commit()
                    QMessageBox.information(
                        self,
                        "Успешное удаление",
                        f"Пользователь '{selected_user}' успешно удален",
                        QMessageBox.StandardButton.Ok
                    )
                    
                    # Обновляем списки
                    self.load_existing_users()
                    self.load_users_and_roles()
                else:
                    QMessageBox.warning(
                        self,
                        "Ошибка удаления",
                        result.Message,
                        QMessageBox.StandardButton.Ok
                    )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Критическая ошибка",
                f"Не удалось удалить пользователя:\n{str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def revoke_role(self):
        user = self.ui.cbRevokeUser.currentText()
        role = self.ui.cbRevokeRole.currentText()
        
        if not user or not role:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя и роль")
            return
            
        try:
            confirm = QMessageBox.question(
                self, 
                "Подтверждение", 
                f"Отозвать роль {role} у пользователя {user}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                cursor = self.db_connection.get_cursor()
                cursor.execute("EXEC usp_RevokeRoleFromUser ?, ?", (user, role))
                result = cursor.fetchone()
                
                if result.ErrorCode == 0:
                    self.db_connection.connection.commit()
                    QMessageBox.information(self, "Успех", result.Message)
                else:
                    QMessageBox.warning(self, "Ошибка", result.Message)
                    
        except Exception :
            QMessageBox.critical(self, "Ошибка", f"Ошибка отзыва роли")

    def select_backup_path(self):
        """Выбор папки для сохранения бэкапа"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для сохранения",
            "",
            QFileDialog.ShowDirsOnly
        )
        if path:
            self.ui.leBackupPath.setText(path)

    def create_backup(self):
        """Создание резервной копии"""
        path = self.ui.leBackupPath.text()
        backup_type = self.ui.cbBackupType.currentText()
        
        if not path:
            QMessageBox.warning(self, "Ошибка", "Укажите папку для сохранения")
            return
            
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_BackupDatabase ?, ?", 
                         (path, backup_type))
            QMessageBox.information(self, "Успех", "Резервная копия создана успешно")
        except Exception as e :
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания бэкапа:\n {str(e)}")

    def load_current_recovery_model(self):
        """Загрузка текущей модели восстановления"""
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("""
                SELECT recovery_model_desc 
                FROM sys.databases 
                WHERE name = 'Optics'
            """)
            result = cursor.fetchone()
            if result:
                current_model = result[0]
                index = self.ui.cbRecoveryModel.findText(current_model)
                if index >= 0:
                    self.ui.cbRecoveryModel.setCurrentIndex(index)
        except Exception :
            print(f"Ошибка загрузки модели восстановления")

    def set_recovery_model(self):
        """Установка новой модели восстановления"""
        model = self.ui.cbRecoveryModel.currentText()
        
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_SetRecoveryModel ?", (model,))
            self.db_connection.connection.commit()
            QMessageBox.information(self, "Успех", 
                                  f"Модель восстановления изменена на {model}")
        except Exception as e :
            QMessageBox.critical(self, "Ошибка", 
                               f"Не удалось изменить модель {str(e)}")
            
    def select_restore_file(self):
        """Выбрать файл .bak для восстановления"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл бэкапа",
            "",
            "Backup Files (*.bak);;All Files (*)"
        )
        if path:
            self.ui.leRestoreFile.setText(path)

    def select_standby_file(self):
        """Выбрать файл standby для режима STANDBY"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Выберите файл для Standby (undo)",
            "",
            "Standby Files (*.tst *.undo);;All Files (*)"
        )
        if path:
            self.ui.leStandbyFile.setText(path)

    def restore_database(self):
        """Выполнить восстановление через usp_RestoreDatabase из контекста master."""
        # 1) Сбор параметров из UI
        backup_path  = self.ui.leRestoreFile.text().strip()
        mode         = self.ui.cbRestoreMode.currentText()
        replace_flag = 1 if self.ui.cbReplace.isChecked() else 0
        standby_file = self.ui.leStandbyFile.text().strip() if mode == "STANDBY" else None
        db_name      = 'Optics'  # можно брать из self.db_connection.database

        # 2) Простая валидация
        if not backup_path:
            QMessageBox.warning(self, "Ошибка", "Укажите файл бэкапа для восстановления")
            return
        if mode == "STANDBY" and not standby_file:
            QMessageBox.warning(self, "Ошибка", "Для режима STANDBY укажите файл Standby")
            return

        try:
            cursor = self.db_connection.get_cursor()

            # 3a) Сначала переключаемся на master
            cursor.execute("USE master;")

            # 3b) А теперь вызываем нашу процедуру
            cursor.execute(
                "EXEC master.dbo.usp_RestoreDatabase "
                "?, ?, ?, ?, ?",
                (db_name, backup_path, mode, replace_flag, standby_file)
            )

            # 4) Фиксируем изменения
            self.db_connection.connection.commit()

        except Exception as e:
            # Показываем полное сообщение об ошибке
            QMessageBox.critical(self, "Ошибка восстановления", str(e))
            return

        # 5) Успех
        QMessageBox.information(self, "Успех", f"База «{db_name}» успешно восстановлена")



    def select_columns(self):
        """Открывает диалог для выбора столбцов выбранной таблицы."""
        table = self.ui.cbMaskTable.currentText()
        if not table:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите таблицу.")
            return

        # Достаём список столбцов из БД
        try:
            cursor = self.db_connection.get_cursor()
            # параметризованный запрос не поддерживает OBJECT_ID(?), поэтому через f‑строку
            cursor.execute(f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{table}')")
            cols = [r[0] for r in cursor.fetchall()]
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить столбцы:\n{e}")
            return

        # Диалог с чекбоксами
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Столбцы таблицы {table}")
        lay = QVBoxLayout(dlg)
        listw = QListWidget()
        listw.setSelectionMode(QAbstractItemView.NoSelection)
        for c in cols:
            item = QListWidgetItem(c)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            listw.addItem(item)
        lay.addWidget(listw)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        lay.addWidget(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)

        if dlg.exec() != QDialog.Accepted:
            return

        # Сохраняем выбор
        self.mask_columns = [
            listw.item(i).text()
            for i in range(listw.count())
            if listw.item(i).checkState() == Qt.Checked
        ]
        if not self.mask_columns:
            QMessageBox.warning(self, "Внимание", "Нужно выбрать хотя бы один столбец.")
            return

        # Обновляем текст кнопки
        self.ui.btnSelectColumns.setText("Столбцы: " + ", ".join(self.mask_columns))


    def apply_mask(self):
        table = self.ui.cbMaskTable.currentText()
        if not table:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите таблицу.")
            return

        cols = getattr(self, "mask_columns", [])
        if not cols:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите столбцы.")
            return

        mask_type = self.ui.cbMaskType.currentText().upper()
        prefix = self.ui.spinStart.value()
        suffix = self.ui.spinEnd.value()

        if mask_type == "PARTIAL" and suffix < prefix:
            QMessageBox.warning(self, "Ошибка", "Диапазон PARTIAL указан неверно.")
            return

        try:
            cursor = self.db_connection.get_cursor()
            for col in cols:
                # Проверка существования таблицы
                cursor.execute("SELECT 1 FROM sys.tables WHERE name = ?", (table,))
                if not cursor.fetchone():
                    raise Exception(f"Таблица '{table}' не существует.")

                # Проверка существования столбца
                cursor.execute(
                    "SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID(?) AND name = ?",
                    (table, col)
                )
                if not cursor.fetchone():
                    raise Exception(f"Столбец '{col}' не существует в таблице '{table}'.")

                # Проверка текущей маскировки
                cursor.execute("""
                    SELECT 1 
                    FROM sys.masked_columns 
                    WHERE object_id = OBJECT_ID(?) AND name = ?
                    """, (table, col))
                if cursor.fetchone():
                    cursor.execute(f"ALTER TABLE [{table}] ALTER COLUMN [{col}] DROP MASKED")

                # Применение новой маскировки
                if mask_type != "NONE":
                    if mask_type == "PARTIAL":
                        mask_function = f'partial({prefix}, "XXXXXXXXXXXX", {suffix})'
                    else:
                        mask_function = f"{mask_type}()"
                    
                    sql = f"""
                        ALTER TABLE [{table}]
                        ALTER COLUMN [{col}] ADD MASKED WITH (FUNCTION = '{mask_function}')
                        """
                    cursor.execute(sql)
            
            self.db_connection.connection.commit()

            # Обновление отображения таблицы
            cursor.execute(f"""
                exec as user = 'client_optics';
                SELECT * FROM {table};
                REVERT;
            """)
            rows = cursor.fetchall()
            
            headers = [d[0] for d in cursor.description]

            tbl = self.ui.tableMaskResult
            tbl.setRowCount(0)
            tbl.setColumnCount(len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.setRowCount(len(rows))

            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    tbl.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ""))

            QMessageBox.information(self, "Успех", "Маскирование применено.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при маскировании: {str(e)}")

    def remove_mask(self):
        """Удаление динамической маскировки."""
        table = self.ui.cbMaskTable.currentText()
        cols = getattr(self, 'mask_columns', [])
        if not table or not cols:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите таблицу и столбцы.")
            return

        try:
            cursor = self.db_connection.get_cursor()
            for col in cols:
                # Проверка существования маскировки
                cursor.execute("""
                    SELECT 1 
                    FROM sys.masked_columns 
                    WHERE object_id = OBJECT_ID(?) AND name = ?
                    """, (table, col))
                if cursor.fetchone():
                    cursor.execute(f"ALTER TABLE [{table}] ALTER COLUMN [{col}] DROP MASKED")
            
            self.db_connection.connection.commit()

            # Обновление отображения
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            headers = [d[0] for d in cursor.description]

            tbl = self.ui.tableMaskResult
            tbl.setRowCount(0)
            tbl.setColumnCount(len(headers))
            tbl.setHorizontalHeaderLabels(headers)
            tbl.setRowCount(len(rows))

            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    tbl.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ""))

            QMessageBox.information(self, "Успех", "Маскировка снята.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении маскировки: {str(e)}")

