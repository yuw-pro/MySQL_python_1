import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector

class MySQLHelper:
    def __init__(self, host=None, user=None,
                  password=None, database=None):
        self.host = host or 'localhost'
        self.user = user or 'root'
        self.password = password or os.getenv('MySQL_password')
        self.database = database or 'students_sql'
        self.connection = None
    def connect(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
            )
        return self.connection
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def query_studnets(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE students_id = %s", (student_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    def query_hot_search(self, rank_no):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM hot_search WHERE rank_no = %s", (rank_no,))
        result = cursor.fetchall()
        cursor.close()
        return result
    def query_all(self, table):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        cursor.close()
        return result
    def query(self, columns, table, condition=None, params=None):
        query = f"SELECT {columns} FROM {table}"
        if condition is not None:
            query += f" WHERE {condition}"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        finally:
            cursor.close()
        return results
    
    def query_one(self, student_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE students_id = %s", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update_student(self, student_id, name, age):
        query = "UPDATE students SET name = %s, age = %s WHERE students_id = %s"
        params = (name, age, student_id)
        self.execute_query(query, params)
    def update_hot_search(self, rank_no, title, hot_value, url, fetched_time):
        query = "UPDATE hot_search SET title = %s, hot_value = %s, url = %s, fetched_time = %s WHERE rank_no = %s"
        params = (title, hot_value, url, fetched_time, rank_no)
        self.execute_query(query, params)
    def update(self, table, columns, condition, values = None):
        query = f"UPDATE {table} SET {columns} WHERE {condition}"
        self.execute_query(query, values)

    def insert_student(self, name, age):
        query = "INSERT INTO students (name, age) VALUES (%s, %s)"
        params = (name, age)
        self.execute_query(query, params)  
    def insert_hot_search(self, rank_no, title, hot_value, url, fetched_time):
        query = "INSERT INTO hot_search (rank_no, title, hot_value, url, fetched_time) VALUES (%s, %s, %s, %s, %s)"
        params = (rank_no, title, hot_value, url, fetched_time)
        self.execute_query(query, params)
    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.execute_query(query)

    def delete_hot_search(self, rank_no):
        query = "DELETE FROM hot_search WHERE rank_no = %s"
        params = (rank_no,)
        self.execute_query(query, params)
    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE students_id = %s"
        params = (student_id,)
        self.execute_query(query, params)
    def delete(self, table, condition, params=None):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query, params)
    
    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
    