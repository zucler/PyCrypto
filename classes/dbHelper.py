import mysql.connector


class DbHelper:
    """ Manage database connection """
    def __init__(self, username, password, db_host, db_port, schema, buffered=True):
        """
        Initialise DbHelper

        Args:
            username (str)
            password (str)
            db_host (str)
            db_port (str)
            schema (str)
            buffered (bool): https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorbuffered.html
        """
        self.connection = None

        self.username = username
        self.password = password
        self.database_host = db_host
        self.database_port = db_port
        self.schema = schema
        self.buffered = buffered

        self.connection = mysql.connector.connect(user=self.username, password=self.password, host=self.database_host,
                                                  port=self.database_port, database=self.schema, buffered=self.buffered)

    def close(self):
        """ Close database connection """
        self.connection.close()

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def get_results_as_dictionary_list(self, query):
        """
        Get results as a list of dictionaries

        Args:
            query (str): MySQL query

        Returns:
            list
        """
        cursor = self.connection.cursor()
        cursor.execute(query)

        results_list = []
        row_data = cursor.fetchone()
        while row_data is not None:
            row = dict(zip(cursor.column_names, row_data))
            results_list.append(row)
            row_data = cursor.fetchone()

        cursor.close()

        return results_list

    def get_first_row_as_dictionary(self, query):
        """
        Get the first row in results set

        Args:
            query (str): MySQL query

        Returns:
            dict
        """
        cursor = self.connection.cursor()
        cursor.execute(query)

        row_data = cursor.fetchone()
        row = dict(zip(cursor.column_names, row_data))

        cursor.close()

        return row
