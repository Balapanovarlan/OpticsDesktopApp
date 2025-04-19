import pyodbc

class DatabaseConnection:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                f'Trusted_Connection=no;'
                f'Encrypt=no;',
                autocommit=True
            )
        except pyodbc.Error :
            raise Exception(f"Ошибка подключения к базе данных")

    def get_cursor(self):
        if not self.connection:
            raise Exception("Нет активного подключения к базе данных.")
        return self.connection.cursor()

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Нет активного подключения к базе данных.")
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                self.connection.commit()
            return cursor
        except Exception as ex:
            raise Exception(f"Ошибка выполнения запроса:")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
