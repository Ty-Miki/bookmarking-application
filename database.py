import sqlite3

class DatabaseManager:
    """A class for managing a SQLite database.
    Args:
        database_filename (str): The filename of the SQLite database.
    """
    
    def __init__(self, database_filename):
        """Initializes the DatabaseManager object.
        Args:
            database_filename (str): The filename of the SQLite database.
        """
        self.connection = sqlite3.connect(database=database_filename)
        
    def __del__(self):
        """Closes the connection to the database.
        This method is automatically called when the object is 
        garbage collected or when the program terminates."""
        self.connection.close()
    
    def _execute(self, statement, values=None):
        """Executes an SQL statement with optional parameter values.
        Args:
            statement (str): The SQL statement to execute.
            values (tuple, optional): The parameter values to substitute in the statement. Defaults to None.
        Returns:
            cursor: The cursor object.
        """
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor
    
    def create_table(self, table_name, columns):
        """Creates a table in the database.
        Args:
            table_name (str): The name of the table.
            columns (dict): A dictionary mapping column names to data types.
        """
        columns_with_types = ', '.join(f"{column_name} {data_type}" for column_name, data_type in columns.items())
        self._execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});")
    
    def add(self, table_name, data):
        """Inserts a row of data into the table.
        Args:
            table_name (str): The name of the table.
            data (dict): A dictionary mapping column names to values.
        """
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())
        self._execute(f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})", column_values,)
        
    def delete(self, table_name, criteria):
        """Deletes rows from the table based on the given criteria.
        Args:
            table_name (str): The name of the table.
            criteria (dict): A dictionary mapping column names to values for the delete criteria.
        """
        placeholder = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholder)
        self._execute(f"DELETE FROM {table_name} WHERE {delete_criteria};", tuple(criteria.values()))
        
    def select(self, table_name, criteria=None, order_by=None):
        """Retrieves rows from the table based on the given criteria and order.

        Args:
            table_name (str): The name of the table.
            criteria (dict, optional): A dictionary mapping column names to values for the select criteria. Defaults to None.
            order_by (str, optional): The column name to order the results by. Defaults to None.

        Returns:
            cursor: The cursor object.
        """
        criteria = criteria or {}
        query = f'SELECT * FROM {table_name}'
        
        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'
        
        if order_by:
            query += f' ORDER BY {order_by}'
        
        return self._execute(query, tuple(criteria.values()),)
    
    def update(self, table_name, criteria, data):
        """Updates rows in the table based on the given criteria with the provided data.
        Args:
            table_name (str): The name of the table.
            criteria (dict): A dictionary mapping column names to values for the update criteria.
            data (dict): A dictionary mapping column names to new values.
        """
        update_placeholders = [f'{column} = ?' for column in criteria.keys()]
        update_criteria = ' AND '.join(update_placeholders)
        data_placeholders = ', '.join(f'{key} = ?' for key in data.keys())
        values = tuple(data.values()) + tuple(criteria.values())
        self._execute(f'UPDATE {table_name} SET {data_placeholders} WHERE {update_criteria};',values,)
        
        
        