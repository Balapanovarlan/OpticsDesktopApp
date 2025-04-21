from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QAbstractItemView, QTableWidgetItem, QListWidget, QListWidgetItem, QDialogButtonBox,QDialog, QVBoxLayout
from security_window_ui import Ui_SecurityWindow
from PySide6.QtCore import Qt
import os

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
        self.ui.btnAudit.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(6)) 
    
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

        self.ui.btnAuditPath.clicked.connect(self.select_audit_path)
        self.ui.btnCreateAudit.clicked.connect(self.create_or_update_audit)
        self.ui.btnCreateSpec.clicked.connect(self.create_or_update_spec)
        self.ui.btnToggleAudit.clicked.connect(self.toggle_audit_state)
        self.ui.btnRefreshLog.clicked.connect(self.refresh_audit_log)

        # Загрузка данных
        self.load_users_and_roles()
        self.load_current_recovery_model()
        self.load_available_logins()
        self.load_existing_users()
        self.load_objects()
        self.load_mask_tables()
        self.load_audit_initial()


    def load_objects(self):
        """Загружает список всех таблиц для выдачи прав через процедуру usp_GetAllTables."""
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("EXEC usp_GetAllTables")
            tables = [row[0] for row in cursor.fetchall()]
            # Очищаем и заполняем комбобокс объектов
            self.ui.cbObject.clear()
            self.ui.cbObject.addItems(tables)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список таблиц:\n{e}")


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
                EXEC usp_GetAllRoles
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
            
    def load_audit_initial(self):
        try:
            cur = self.db_connection.get_cursor()

            # Загрузка списка баз данных для создания спецификации
            cur.execute("SELECT name FROM sys.databases WHERE database_id > 4;")
            self.ui.cbSpecDb.clear()
            self.ui.cbSpecDb.addItems([r[0] for r in cur.fetchall()])

            # Автоподстановка имени аудита, если поле пустое
            if not self.ui.leAuditName.text().strip():
                cur.execute("SELECT TOP (1) name FROM sys.server_audits;")
                row = cur.fetchone()
                if row:
                    self.ui.leAuditName.setText(row[0])

            # Получение текущего состояния и пути аудита из DMV
            name = self.ui.leAuditName.text().strip()
            if name:
                cur.execute("""
                    SELECT status_desc, audit_file_path
                    FROM sys.dm_server_audit_status
                    WHERE name = ?
                """, (name,))
                row = cur.fetchone()
                if row:
                    state, fullpath = row
                    # Отображаем статус
                    self.ui.lblAuditState.setText(state)
                    # Меняем текст кнопки в зависимости от состояния
                    self.ui.btnToggleAudit.setText(
                        "Выключить" if state.upper() == "STARTED" else "Включить"
                    )
                    # Если путь ещё не задан в UI — вычленяем каталог из полного пути
                    if not self.ui.leAuditPath.text().strip() and fullpath:
                        folder = os.path.dirname(fullpath)
                        if not folder.endswith(os.sep):
                            folder += os.sep
                        self.ui.leAuditPath.setText(folder)

        except Exception as e:
            print("init audit page:", e)

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
            cursor.execute(f"CREATE LOGIN {login} WITH PASSWORD = '{password}' ")
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
            cursor.execute(
                "EXEC [Optics].dbo.usp_CreateDatabaseUser ?, ?",
                (login, username)
            )
            result = cursor.fetchone()
            # **Обязательно «проглатываем» все оставшиеся наборы**
            while cursor.nextset():
                pass

            if result.ErrorCode == 0:
                self.db_connection.connection.commit()
                QMessageBox.information(self, "Успех", result.Message)
                self.ui.leDbUserName.clear()

                # Перезагружаем списки — эти методы создают СВОИ cursors
                self.load_existing_users()
                self.load_users_and_roles()
            else:
                QMessageBox.warning(self, "Ошибка", result.Message)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать пользователя:\n{e}")
        finally:
            # Закрываем cursor, чтобы гарантировать, что он не будет удерживать ресурс
            try:
                cursor.close()
            except:
                pass

    def create_role(self):
        """Создание новой роли через хранимую процедуру с очисткой курсора и закрытием."""
        role_name = self.ui.leRoleName.text().strip()
        if not role_name:
            QMessageBox.warning(self, "Ошибка", "Введите имя роли")
            return

        cursor = None
        try:
            cursor = self.db_connection.get_cursor()
            # Вызываем процедуру через трёхчастное имя
            cursor.execute("EXEC [Optics].dbo.usp_CreateRole ?", (role_name,))
            result = cursor.fetchone()
            # Проглатываем все оставшиеся result‑set’ы
            while cursor.nextset():
                pass

            if result.ErrorCode == 0:
                self.db_connection.connection.commit()
                QMessageBox.information(self, "Успех", result.Message)
                self.ui.leRoleName.clear()
                # Перезагружаем список ролей и пользователей
                self.load_users_and_roles()
            else:
                QMessageBox.warning(self, "Ошибка", result.Message)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать роль:\n{e}")
        finally:
            # Закрываем cursor, чтобы освободить соединение
            if cursor:
                try:
                    cursor.close()
                except:
                    pass


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
        if not selected_user:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления")
            return

        confirm = QMessageBox.question(self, "Подтверждение",
                                    f"Удалить '{selected_user}'?", 
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return

        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute(
                "EXEC [Optics].dbo.usp_DeleteDatabaseUser @UserName = ?", 
                (selected_user,)
            )
            result = cursor.fetchone()
            while cursor.nextset():
                pass

            if result.ErrorCode == 0:
                self.db_connection.connection.commit()
                QMessageBox.information(self, "Успешно", result.Message)
                self.load_existing_users()
                self.load_users_and_roles()
            else:
                QMessageBox.warning(self, "Ошибка", result.Message)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя:\n{e}")
        finally:
            try:
                cursor.close()
            except:
                pass


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
        backup_path = self.ui.leRestoreFile.text().strip()
        mode = self.ui.cbRestoreMode.currentText()
        replace_flag = 1 if self.ui.cbReplace.isChecked() else 0
        standby_file = self.ui.leStandbyFile.text().strip() if mode == "STANDBY" else None

        db_name = getattr(self.db_connection, "database", None)
        if not db_name:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить текущую базу данных.")
            return

        if not backup_path:
            QMessageBox.warning(self, "Ошибка", "Укажите файл бэкапа.")
            return
        if mode == "STANDBY" and not standby_file:
            QMessageBox.warning(self, "Ошибка", "Для STANDBY укажите standby-файл.")
            return

        cursor = self.db_connection.get_cursor()
        
        # Сохраняем текущий режим autocommit
        original_autocommit = self.db_connection.connection.autocommit
        try:
            # Включаем autocommit для RESTORE
            self.db_connection.connection.autocommit = True

            # Выполняем восстановление
            cursor.execute("USE master;")
            cursor.execute(
                "EXEC master.dbo.usp_RestoreDatabase ?, ?, ?, ?, ?",
                (db_name, backup_path, mode, replace_flag, standby_file)
            )

            QMessageBox.information(self, "Успех", f"База «{db_name}» восстановлена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка восстановления: {str(e)}")
        finally:
            # Восстанавливаем исходный режим autocommit
            self.db_connection.connection.autocommit = original_autocommit
            try:
                cursor.execute(f"USE [{db_name}];")
            except Exception as e:
                print(f"Не удалось переключиться на базу: {str(e)}")


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

    def select_audit_path(self):
        path = QFileDialog.getExistingDirectory(
            self, "Выберите каталог для файлов аудита", ""
        )
        if path:
            # нормализуем слэши и добавляем завершающий
            path = os.path.normpath(path)
            if not path.endswith(os.sep):
                path += os.sep
            self.ui.leAuditPath.setText(path)

    def create_or_update_audit(self):
        """Создать или обновить аудит через master.dbo.sp_CreateAudit,
        затем вернуть контекст в исходную базу."""
        name      = self.ui.leAuditName.text().strip()
        folder    = self.ui.leAuditPath.text().strip()
        max_size  = self.ui.spinMaxSize.value()
        max_files = self.ui.spinMaxFiles.value()

        # Текущая база, в которой надо вернуть контекст
        db_name = getattr(self.db_connection, "database", None)
        if not (name and folder and db_name):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля и убедитесь, что выбрана база.")
            return

        # Нормализация пути для SQL Server
        folder = folder.replace('/', '\\')
        if not folder.endswith('\\'):
            folder += '\\'

        cursor = self.db_connection.get_cursor()
        try:
            # Переключаемся на master и вызываем процедуру
            cursor.execute("USE master;")
            cursor.execute(
                "EXEC master.dbo.sp_CreateAudit "
                "@AuditName = ?, @AuditPath = ?, @MaxSizeMB = ?, @MaxFiles = ?, @DatabaseName = ?",
                (name, folder, max_size, max_files, db_name)
            )
            self.db_connection.connection.commit()
            QMessageBox.information(self, "Успех", "Аудит создан или обновлён.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            # Возвращаемся в исходную базу
            try:
                cursor.execute(f"USE [{db_name}];")
            except:
                pass


    def create_or_update_spec(self):
        """Создаёт или обновляет спецификацию аудита, с переключением контекста в master или нужную БД и возвратом в исходную."""
        audit_name = self.ui.leAuditName.text().strip()
        if not audit_name:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте Audit (SERVER AUDIT).")
            return

        actions = [
            self.ui.listActions.item(i).text()
            for i in range(self.ui.listActions.count())
            if self.ui.listActions.item(i).checkState() == Qt.Checked
        ]
        if not actions:
            QMessageBox.warning(self, "Ошибка", "Отметьте хотя бы одно действие.")
            return

        cur = self.db_connection.get_cursor()
        # запомним исходную базу для возврата
        orig_db = getattr(self.db_connection, "database", None)

        try:
            if self.ui.rbServer.isChecked():
                spec = f"{audit_name}_ServerSpec"
                # работаем в master
                cur.execute("USE master;")

                cur.execute("""
                    IF EXISTS (SELECT 1 FROM sys.server_audit_specifications WHERE name = ?)
                    BEGIN
                        ALTER SERVER AUDIT SPECIFICATION [{}] WITH (STATE = OFF);
                        DROP SERVER AUDIT SPECIFICATION [{}];
                    END
                """.format(spec, spec), (spec,))

                cur.execute(f"CREATE SERVER AUDIT SPECIFICATION [{spec}] FOR SERVER AUDIT [{audit_name}];")
                for action in actions:
                    cur.execute(f"ALTER SERVER AUDIT SPECIFICATION [{spec}] ADD ({action});")
                cur.execute(f"ALTER SERVER AUDIT SPECIFICATION [{spec}] WITH (STATE = ON);")

            else:
                # Database‑level
                target_db = self.ui.cbSpecDb.currentText()
                spec = f"{audit_name}_{target_db}_DbSpec"
                # переключаемся в целевую БД
                cur.execute(f"USE [{target_db}];")

                cur.execute("""
                    IF EXISTS (SELECT 1 FROM sys.database_audit_specifications WHERE name = ?)
                    BEGIN
                        ALTER DATABASE AUDIT SPECIFICATION [{}] WITH (STATE = OFF);
                        DROP DATABASE AUDIT SPECIFICATION [{}];
                    END
                """.format(spec, spec), (spec,))

                cur.execute(f"CREATE DATABASE AUDIT SPECIFICATION [{spec}] FOR SERVER AUDIT [{audit_name}];")
                for action in actions:
                    cur.execute(f"ALTER DATABASE AUDIT SPECIFICATION [{spec}] ADD ({action});")
                cur.execute(f"ALTER DATABASE AUDIT SPECIFICATION [{spec}] WITH (STATE = ON);")

            self.db_connection.connection.commit()
            QMessageBox.information(self, "Успех", "Спецификация создана / обновлена.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

        finally:
            # всегда возвращаемся в исходную базу
            if orig_db:
                try:
                    cur.execute(f"USE [{orig_db}];")
                except:
                    pass


    def toggle_audit_state(self):
        """Переключает состояние Server Audit и возвращает контекст в исходную базу."""
        name = self.ui.leAuditName.text().strip()
        if not name:
            return

        cur = self.db_connection.get_cursor()
        orig_db = getattr(self.db_connection, "database", None)

        try:
            # Переключаемся в мастер
            cur.execute("USE master;")

            # Получаем информацию об аудите
            cur.execute("""
                SELECT 
                    s.is_state_enabled,
                    d.status_desc
                FROM sys.server_audits AS s
            LEFT JOIN sys.dm_server_audit_status AS d
                    ON s.name = d.name
                WHERE s.name = ?
            """, (name,))
            row = cur.fetchone()
            if not row:
                QMessageBox.warning(self, "Ошибка", f"Аудит «{name}» не найден.")
                return

            is_enabled, status_desc = row
            current = (
                status_desc.upper()
                if status_desc
                else ("STARTED" if is_enabled == 1 else "OFF")
            )

            # Решаем, включить или выключить
            new_state = "OFF" if current == "STARTED" else "ON"
            cur.execute(f"ALTER SERVER AUDIT [{name}] WITH (STATE = {new_state});")
            self.db_connection.connection.commit()

            # Обновляем UI
            display = "STARTED" if new_state == "ON" else "OFF"
            self.ui.lblAuditState.setText(display)
            self.ui.btnToggleAudit.setText("Выключить" if display == "STARTED" else "Включить")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

        finally:
            # Всегда возвращаемся в исходную базу
            if orig_db:
                try:
                    cur.execute(f"USE [{orig_db}];")
                except:
                    pass


    def refresh_audit_log(self):
        """Обновляет таблицу с последними записями аудита, переключаясь в master и возвращая контекст."""
        folder = self.ui.leAuditPath.text().strip()
        if not folder:
            QMessageBox.warning(self, "Ошибка", "Не указан каталог файлов аудита.")
            return

        # нормализация пути для SQL Server
        folder = folder.replace('/', '\\')
        if not folder.endswith('\\'):
            folder += '\\'
        pattern = folder + "*.sqlaudit"

        cur = self.db_connection.get_cursor()
        orig_db = getattr(self.db_connection, "database", None)
        try:
            # Переключаемся в master для чтения файлов аудита
            cur.execute("USE master;")
            cur.execute("""
                SELECT TOP 200
                    event_time,
                    action_id,
                    succeeded,
                    server_principal_name,
                    database_name,
                    schema_name,
                    object_name,
                    statement
                FROM sys.fn_get_audit_file(?, DEFAULT, DEFAULT)
                ORDER BY event_time DESC;
            """, (pattern,))

            rows    = cur.fetchall()
            headers = [d[0] for d in cur.description]
            tbl     = self.ui.tblAuditLog
            tbl.setRowCount(len(rows))
            tbl.setColumnCount(len(headers))
            tbl.setHorizontalHeaderLabels(headers)

            for r, row in enumerate(rows):
                for c, val in enumerate(row):
                    tbl.setItem(r, c, QTableWidgetItem(str(val) if val is not None else ""))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            # Возвращаемся в исходную базу
            if orig_db:
                try:
                    cur.execute(f"USE [{orig_db}];")
                except:
                    pass

