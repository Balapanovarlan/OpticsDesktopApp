from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                               QFormLayout, QLineEdit, QPushButton, QComboBox, 
                               QCheckBox, QFrame, QStackedWidget, QPlainTextEdit,
                                 QLabel, QTableWidget, QSpinBox, QScrollArea,
                                 QRadioButton, QListWidget, QListWidgetItem)

class Ui_SecurityWindow(object):
    def setupUi(self, SecurityWindow):
        if not SecurityWindow.objectName():
            SecurityWindow.setObjectName("SecurityWindow")
        SecurityWindow.resize(900, 700)
        
        # Основные стили
        base_style = """
            QWidget {
                font-family: 'Segoe UI';
                font-size: 11pt;
            }
            
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 16px;
                padding: 12px 8px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px;
            }
            
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #106ebe;
            }
            
            QPushButton:pressed {
                background-color: #005a9e;
            }
            
            QLineEdit, QComboBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 6px 8px;
                background: white;
                min-height: 28px;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078d4;
            }
            
            QCheckBox {
                spacing: 6px;
            }
        """
        
        sidebar_style = """
            QFrame#sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e0e0e0;
            }
            
            QPushButton {
                background-color: transparent;
                color: #323130;
                text-align: left;
                padding: 8px 12px;
                border-radius: 4px;
            }
            
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            
        """
        
        SecurityWindow.setStyleSheet(base_style)

        # Центральный виджет и основной макет
        self.centralwidget = QWidget(SecurityWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # Сайдбар
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet(sidebar_style)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(8, 12, 8, 12)
        self.sidebarLayout.setSpacing(4)
        
        # Кнопки сайдбара
        self.btnUserManagement = QPushButton("Пользователи", self.sidebar)
        self.btnUserManagement.setCheckable(True)
        self.btnUserManagement.setChecked(True)
        
        self.btnRoleManagement = QPushButton("Роли", self.sidebar)
        self.btnRoleManagement.setCheckable(True)
        
        self.btnPermissions = QPushButton("Права", self.sidebar)
        self.btnPermissions.setCheckable(True)

        self.btnBackup = QPushButton("Резервное копирование", self.sidebar)

        self.btnRestore = QPushButton("Восстановление", self.sidebar)
        self.btnRestore.setCheckable(True)

        self.btnMask = QPushButton("Маскировка данных", self.sidebar)
        self.btnMask.setCheckable(True)

        self.btnAudit = QPushButton("Аудит", self.sidebar)   
        self.btnAudit.setCheckable(True)
        
        # Добавляем кнопки
        self.sidebarLayout.addWidget(self.btnUserManagement)
        self.sidebarLayout.addWidget(self.btnRoleManagement)
        self.sidebarLayout.addWidget(self.btnPermissions)
        self.sidebarLayout.addWidget(self.btnBackup)
        self.sidebarLayout.addWidget(self.btnRestore)
        self.sidebarLayout.addWidget(self.btnMask)
        self.sidebarLayout.addWidget(self.btnAudit)
        self.sidebarLayout.addStretch()
        
        # Контейнер страниц
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setContentsMargins(16, 16, 16, 16)
        
        # Страницы
        self.pageUserManagement = QWidget()
        self.setupUserManagementPage()
        self.stackedWidget.addWidget(self.pageUserManagement)
        
        self.pageRoleManagement = QWidget()
        self.setupRoleManagementPage()
        self.stackedWidget.addWidget(self.pageRoleManagement)
        
        self.pagePermissions = QWidget()
        self.setupPermissionsPage()
        self.stackedWidget.addWidget(self.pagePermissions)

        self.pageBackup = QWidget()
        self.setupBackupPage()
        self.stackedWidget.addWidget(self.pageBackup)

        self.pageRestore = QWidget()
        self.setupRestorePage()
        self.stackedWidget.addWidget(self.pageRestore)

        self.pageMask = QWidget()
        self.setupMaskPage()
        self.stackedWidget.addWidget(self.pageMask)

        self.pageAudit = QWidget()                
        self.setupAuditPage()                     
        self.stackedWidget.addWidget(self.pageAudit)

        # Компоновка
        self.mainLayout.addWidget(self.sidebar)
        self.mainLayout.addWidget(self.stackedWidget)

        SecurityWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SecurityWindow)
        QMetaObject.connectSlotsByName(SecurityWindow)

    def setupUserManagementPage(self):
        layout = QVBoxLayout(self.pageUserManagement)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Группа создания логина
        self.gbCreateLogin = QGroupBox()
        self.gbCreateLogin.setTitle("Создание логина сервера")
        form_login = QFormLayout(self.gbCreateLogin)
        form_login.setContentsMargins(8, 12, 8, 12)
        form_login.setSpacing(8)
        
        self.leLoginName = QLineEdit()
        self.leLoginPassword = QLineEdit()
        self.leLoginPassword.setEchoMode(QLineEdit.Password)
        self.btnCreateLogin = QPushButton("Создать логин")
        self.btnCreateLogin.setStyleSheet("background-color: #4CAF50; color: white;")
        
        form_login.addRow("Имя логина:", self.leLoginName)
        form_login.addRow("Пароль:", self.leLoginPassword)
        form_login.addRow(self.btnCreateLogin)
        
        # Группа создания пользователя БД
        self.gbCreateUser = QGroupBox()
        self.gbCreateUser.setTitle("Создание пользователя БД")
        form_user = QFormLayout(self.gbCreateUser)
        form_user.setContentsMargins(8, 12, 8, 12)
        form_user.setSpacing(8)
        
        self.cbAvailableLogins = QComboBox()
        self.leDbUserName = QLineEdit()
        self.btnCreateUser = QPushButton("Создать пользователя")
        self.btnCreateUser.setStyleSheet("background-color: #2196F3; color: white;")
        
        form_user.addRow("Выберите логин:", self.cbAvailableLogins)
        form_user.addRow("Имя пользователя в БД:", self.leDbUserName)
        form_user.addRow(self.btnCreateUser)
        
        # Группа управления пользователями
        self.gbManageUsers = QGroupBox()
        self.gbManageUsers.setTitle("Управление пользователями БД")
        form_manage = QFormLayout(self.gbManageUsers)
        form_manage.setContentsMargins(8, 12, 8, 12)
        form_manage.setSpacing(8)
        
        self.cbExistingUsers = QComboBox()
        self.btnDeleteUser = QPushButton("Удалить пользователя")
        self.btnDeleteUser.setStyleSheet("background-color: #d13438; color: white;")
        
        form_manage.addRow("Выберите пользователя:", self.cbExistingUsers)
        form_manage.addRow(self.btnDeleteUser)
        
        # Добавляем все группы на страницу
        layout.addWidget(self.gbCreateLogin)
        layout.addWidget(self.gbCreateUser)
        layout.addWidget(self.gbManageUsers)
        layout.addStretch()

    def setupRoleManagementPage(self):
        layout = QVBoxLayout(self.pageRoleManagement)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Новая группа создания ролей
        self.gbCreateRole = QGroupBox()
        self.gbCreateRole.setTitle("Создание новой роли")
        form_create = QFormLayout(self.gbCreateRole)
        form_create.setContentsMargins(8, 12, 8, 12)
        form_create.setSpacing(8)
        
        self.leRoleName = QLineEdit()
        self.leRoleName.setPlaceholderText("Введите имя новой роли")
        self.btnCreateRole = QPushButton("Создать роль")
        self.btnCreateRole.setStyleSheet("background-color: #107C10; color: white;")
        
        form_create.addRow("Имя роли:", self.leRoleName)
        form_create.addRow(self.btnCreateRole)
        
        # Существующая группа назначения ролей
        self.gbAssignRole = QGroupBox()
        self.gbAssignRole.setTitle("Назначение роли пользователю")
        form_assign = QFormLayout(self.gbAssignRole)
        form_assign.setContentsMargins(8, 12, 8, 12)
        form_assign.setSpacing(8)
        
        self.cbUser = QComboBox()
        self.cbRole = QComboBox()
        self.btnAssignRole = QPushButton("Назначить роль")
        
        form_assign.addRow("Пользователь:", self.cbUser)
        form_assign.addRow("Роль:", self.cbRole)
        form_assign.addRow(self.btnAssignRole)
        
        # Новая группа для удаления ролей
        self.gbRevokeRole = QGroupBox()
        self.gbRevokeRole.setTitle("Отзыв роли у пользователя")
        form_revoke = QFormLayout(self.gbRevokeRole)
        form_revoke.setContentsMargins(8, 12, 8, 12)
        form_revoke.setSpacing(8)
        
        self.cbRevokeUser = QComboBox()
        self.cbRevokeRole = QComboBox()
        self.btnRevokeRole = QPushButton("Отозвать роль")
        self.btnRevokeRole.setStyleSheet("background-color: #d13438;")
        
        form_revoke.addRow("Пользователь:", self.cbRevokeUser)
        form_revoke.addRow("Роль для отзыва:", self.cbRevokeRole)
        form_revoke.addRow(self.btnRevokeRole)
        
        # Добавляем все группы в layout
        layout.addWidget(self.gbCreateRole)
        layout.addWidget(self.gbAssignRole)
        layout.addWidget(self.gbRevokeRole)
        layout.addStretch()
    

    def setupPermissionsPage(self):
        layout = QVBoxLayout(self.pagePermissions)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)
        
        # Группа выдачи прав
        self.gbSetPermissions = QGroupBox()
        self.gbSetPermissions.setTitle("Выдача прав на объект")
        form = QFormLayout(self.gbSetPermissions)
        form.setContentsMargins(8, 12, 8, 12)
        form.setSpacing(8)
        
        self.cbPermRole = QComboBox()
        self.cbObject = QComboBox()
        self.cbAction = QComboBox()
        self.cbAction.addItems(["GRANT", "DENY", "REVOKE"])
        self.cbSelect = QCheckBox("SELECT")
        self.cbInsert = QCheckBox("INSERT")
        self.cbUpdate = QCheckBox("UPDATE")
        self.cbDelete = QCheckBox("DELETE")
        self.cbExecute = QCheckBox("EXECUTE")
        self.btnSetPermissions = QPushButton("Применить права")
        
        form.addRow("Роль:", self.cbPermRole)
        form.addRow("Объект:", self.cbObject)
        form.addRow("Действие:", self.cbAction)
        form.addRow("Права:", self.cbSelect)
        form.addRow("", self.cbInsert)
        form.addRow("", self.cbUpdate)
        form.addRow("", self.cbDelete)
        form.addRow("", self.cbExecute)
        form.addRow(self.btnSetPermissions)
        
        layout.addWidget(self.gbSetPermissions)

           # --- Блок просмотра прав роли ---
        self.gbViewPermissions = QGroupBox("Просмотр прав роли")
        view_layout = QVBoxLayout(self.gbViewPermissions)
        view_layout.setContentsMargins(8, 12, 8, 12)
        view_layout.setSpacing(6)

        # Переключатель роли (используем уже заполнённый cbPermRole)
        self.btnViewPermissions = QPushButton("Показать права")
        # Текстовое поле для вывода
        self.tePermissionsOutput = QPlainTextEdit()
        self.tePermissionsOutput.setReadOnly(True)
        self.tePermissionsOutput.setFixedHeight(140)

        view_layout.addWidget(self.btnViewPermissions)
        view_layout.addWidget(self.tePermissionsOutput)

        layout.addWidget(self.gbViewPermissions)

        layout.addStretch()


    def setupBackupPage(self):
        layout = QVBoxLayout(self.pageBackup)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Группа настроек бэкапа
        self.gbBackup = QGroupBox("Резервное копирование")
        backup_layout = QFormLayout(self.gbBackup)
        
        # Выбор типа бэкапа
        self.cbBackupType = QComboBox()
        self.cbBackupType.addItems(["FULL", "DIFFERENTIAL", "LOG"])
        
        # Поле для пути
        self.leBackupPath = QLineEdit()
        self.leBackupPath.setPlaceholderText("Выберите папку для сохранения")
        self.btnChoosePath = QPushButton("Обзор...")
        
        # Кнопка создания бэкапа
        self.btnCreateBackup = QPushButton("Создать резервную копию")
        self.btnCreateBackup.setStyleSheet("background-color: #4CAF50; color: white;")
        
        backup_layout.addRow("Тип бэкапа:", self.cbBackupType)
        backup_layout.addRow("Папка назначения:", self.leBackupPath)
        backup_layout.addRow("", self.btnChoosePath)
        backup_layout.addRow(self.btnCreateBackup)
        
        # Группа управления моделью восстановления
        self.gbRecovery = QGroupBox("Управление моделью восстановления")
        recovery_layout = QFormLayout(self.gbRecovery)
        
        self.cbRecoveryModel = QComboBox()
        self.cbRecoveryModel.addItems(["FULL", "SIMPLE", "BULK_LOGGED"])
        self.btnSetRecovery = QPushButton("Применить модель")
        self.btnSetRecovery.setStyleSheet("background-color: #2196F3; color: white;")
        
        recovery_layout.addRow("Модель восстановления:", self.cbRecoveryModel)
        recovery_layout.addRow(self.btnSetRecovery)
        
        # Добавляем группы на страницу
        layout.addWidget(self.gbBackup)
        layout.addWidget(self.gbRecovery)
        layout.addStretch()

    def setupRestorePage(self):
        layout = QVBoxLayout(self.pageRestore)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        # --- Группа параметров восстановления ---
        gbRestore = QGroupBox("Восстановление базы данных")
        form = QFormLayout(gbRestore)
        form.setContentsMargins(8, 12, 8, 12)
        form.setSpacing(8)

        # 1) Выбор файла бэкапа
        self.leRestoreFile = QLineEdit()
        self.leRestoreFile.setPlaceholderText("Выберите файл .bak")
        self.btnChooseRestoreFile = QPushButton("Обзор…")
        h1 = QHBoxLayout()
        h1.addWidget(self.leRestoreFile)
        h1.addWidget(self.btnChooseRestoreFile)
        form.addRow("Файл бэкапа:", h1)

        # 2) Режим восстановления
        self.cbRestoreMode = QComboBox()
        self.cbRestoreMode.addItems(["RECOVERY", "NORECOVERY", "STANDBY"])
        form.addRow("Режим восстановления:", self.cbRestoreMode)

        # 3) Путь для standby (только если выбрали STANDBY)
        self.leStandbyFile = QLineEdit()
        self.leStandbyFile.setPlaceholderText("Файл для Standby")
        self.leStandbyFile.setEnabled(False)
        self.btnChooseStandbyFile = QPushButton("Обзор…")
        self.btnChooseStandbyFile.setEnabled(False)
        h2 = QHBoxLayout()
        h2.addWidget(self.leStandbyFile)
        h2.addWidget(self.btnChooseStandbyFile)
        form.addRow("Standby-файл:", h2)

        # 4) WITH REPLACE
        self.cbReplace = QCheckBox("WITH REPLACE")
        form.addRow("", self.cbReplace)

        # 5) Кнопка «Восстановить»
        self.btnRestoreDb = QPushButton("Восстановить")
        self.btnRestoreDb.setStyleSheet("background-color: #4CAF50; color: white;")
        form.addRow(self.btnRestoreDb)

        layout.addWidget(gbRestore)
        layout.addStretch()
        
        # --- логика включения поля standby-файла ---
        # (не забудьте импорты QHBoxLayout, QLineEdit, QPushButton, QComboBox, QCheckBox)
        self.cbRestoreMode.currentTextChanged.connect(
            lambda mode: (
                self.leStandbyFile.setEnabled(mode == "STANDBY"),
                self.btnChooseStandbyFile.setEnabled(mode == "STANDBY")
            )
        )

    def setupMaskPage(self):
        # Общий контейнер
        layout = QVBoxLayout(self.pageMask)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)
        
        # Группа 1: выбор таблицы и столбцов
        gbSelect = QGroupBox("Выбор таблицы и столбцов")
        form1 = QFormLayout(gbSelect)
        form1.setContentsMargins(8, 12, 8, 12)
        form1.setSpacing(8)
        
        self.cbMaskTable      = QComboBox()
        self.btnSelectColumns = QPushButton("Выбрать столбцы…")
        
        form1.addRow("Таблица:", self.cbMaskTable)
        form1.addRow("Столбцы:", self.btnSelectColumns)
        layout.addWidget(gbSelect)
        
        # Группа 2: параметры маскирования
        gbOptions = QGroupBox("Параметры маскирования")
        form2 = QFormLayout(gbOptions)
        form2.setContentsMargins(8, 12, 8, 12)
        form2.setSpacing(8)
        
        self.cbMaskType = QComboBox()
        self.cbMaskType.addItems(["Email", "Default", "Partial", "Random"])

        self.spinStart = QSpinBox()
        self.spinEnd   = QSpinBox()
        for sp in (self.spinStart, self.spinEnd):
            sp.setRange(0, 1_000_000)
            sp.setEnabled(False)
        
        # Включать/отключать спины при выборе Partial
        self.cbMaskType.currentTextChanged.connect(
            lambda t: [sp.setEnabled(t in ("Partial","Random")) for sp in (self.spinStart, self.spinEnd)]
        )
        
        form2.addRow("Тип маскировки:", self.cbMaskType)
        # inline‑диапазон
        hRange = QHBoxLayout()
        hRange.addWidget(QLabel("С:"))
        hRange.addWidget(self.spinStart)
        hRange.addWidget(QLabel("По:"))
        hRange.addWidget(self.spinEnd)
        form2.addRow("Диапазон:", hRange)
        
        hBtns = QHBoxLayout()
        self.btnDoMask   = QPushButton("Маскировать")
        self.btnDoUnmask = QPushButton("Снять маскировку")
        hBtns.addWidget(self.btnDoMask)
        hBtns.addWidget(self.btnDoUnmask)
        form2.addRow(hBtns)
            
        layout.addWidget(gbOptions)
        
        # Группа 3: результат
        gbResult = QGroupBox("Результат маскирования")
        vboxRes = QVBoxLayout(gbResult)
        vboxRes.setContentsMargins(8, 12, 8, 12)
        
        self.tableMaskResult = QTableWidget()
        self.tableMaskResult.setColumnCount(0)
        self.tableMaskResult.setRowCount(0)
        vboxRes.addWidget(self.tableMaskResult)
        
        layout.addWidget(gbResult)
        
        layout.addStretch()

    def setupAuditPage(self):
        # 1) Обёртка: scroll area
        outer = QVBoxLayout(self.pageAudit)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea(self.pageAudit)
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        # --- Группа 1. Настройки приёмника ----------------
        gbReceiver = QGroupBox("Настройки аудита (SERVER AUDIT)")
        fRec = QFormLayout(gbReceiver)
        fRec.setLabelAlignment(Qt.AlignRight)
        fRec.setFormAlignment(Qt.AlignLeft)

        self.leAuditName  = QLineEdit();  self.leAuditName.setPlaceholderText("OpticsAudit")
        self.leAuditPath  = QLineEdit()
        self.btnAuditPath = QPushButton("Обзор…")
        hPath = QHBoxLayout(); hPath.addWidget(self.leAuditPath); hPath.addWidget(self.btnAuditPath)

        self.spinMaxSize  = QSpinBox();  self.spinMaxSize.setRange(2, 10240); self.spinMaxSize.setSuffix(" МБ")
        self.spinMaxFiles = QSpinBox();  self.spinMaxFiles.setRange(1, 512)

        self.btnCreateAudit = QPushButton("Создать / изменить аудит")

        fRec.addRow("Имя аудита:",     self.leAuditName)
        fRec.addRow("Каталог файлов:", hPath)
        fRec.addRow("Макс. размер:",   self.spinMaxSize)
        fRec.addRow("Макс. файлов:",   self.spinMaxFiles)
        fRec.addRow(self.btnCreateAudit)

        layout.addWidget(gbReceiver)

        # --- Группа 2. Спецификация ----------------------
        gbSpec = QGroupBox("Спецификация аудита")
        fSpec = QFormLayout(gbSpec)
        fSpec.setLabelAlignment(Qt.AlignRight)
        fSpec.setFormAlignment(Qt.AlignLeft)

        # уровень
        hLvl = QHBoxLayout()
        self.rbServer = QRadioButton("Server‑level"); self.rbServer.setChecked(True)
        self.rbDb     = QRadioButton("Database‑level")
        hLvl.addWidget(self.rbServer); hLvl.addWidget(self.rbDb)
        fSpec.addRow("Уровень:", hLvl)

        # база
        self.cbSpecDb = QComboBox(); self.cbSpecDb.setEnabled(False)
        fSpec.addRow("База данных:", self.cbSpecDb)

        # действия (ограничиваем высоту)
        self.listActions = QListWidget()
        self.listActions.setMaximumHeight(100)
        for ag in [
            "DATABASE_OBJECT_CHANGE_GROUP",
            "DATABASE_PRINCIPAL_CHANGE_GROUP",
            "SCHEMA_OBJECT_ACCESS_GROUP",
            "SUCCESSFUL_LOGIN_GROUP",
            "FAILED_LOGIN_GROUP"
        ]:
            itm = QListWidgetItem(ag)
            itm.setFlags(itm.flags() | Qt.ItemIsUserCheckable)
            itm.setCheckState(Qt.Unchecked)
            self.listActions.addItem(itm)
        fSpec.addRow("Действия:", self.listActions)

        self.btnCreateSpec = QPushButton("Создать / изменить спецификацию")
        fSpec.addRow(self.btnCreateSpec)
        layout.addWidget(gbSpec)

        # переключатель активности
        gbState = QGroupBox("Состояние аудита")
        hState = QHBoxLayout(gbState)
        self.lblAuditState  = QLabel("OFF"); self.lblAuditState.setAlignment(Qt.AlignCenter)
        self.lblAuditState.setStyleSheet("font-weight:600;")
        self.btnToggleAudit = QPushButton("Включить")
        hState.addWidget(self.lblAuditState); hState.addStretch(); hState.addWidget(self.btnToggleAudit)
        layout.addWidget(gbState)

        # --- Группа 4. Просмотр журнала -----------------
        gbLog = QGroupBox("Просмотр журнала")
        vLog  = QVBoxLayout(gbLog)
        self.btnRefreshLog = QPushButton("Обновить")
        self.tblAuditLog   = QTableWidget()
        self.tblAuditLog.setMinimumHeight(200)
        vLog.addWidget(self.btnRefreshLog)
        vLog.addWidget(self.tblAuditLog)
        layout.addWidget(gbLog)

        layout.addStretch()

        # --- логика включения базы при Database‑level ----
        self.rbDb.toggled.connect(lambda on: self.cbSpecDb.setEnabled(on))

    def retranslateUi(self, SecurityWindow):
        _translate = QCoreApplication.translate
        SecurityWindow.setWindowTitle(_translate("SecurityWindow", "Окно безопасности"))