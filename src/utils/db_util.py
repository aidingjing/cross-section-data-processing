import pymysql
from typing import Dict, Any, List, Tuple, Optional
from contextlib import contextmanager


class DBUtil:
    @staticmethod
    @contextmanager
    def get_connection(db_config: Dict[str, Any]):
        connection = None
        try:
            connection = pymysql.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                charset=db_config.get('charset', 'utf8mb4'),
                autocommit=False
            )
            yield connection
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def set_utf8mb4(cursor):
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")
    
    @staticmethod
    def set_timeout(cursor, timeout: int = 300):
        cursor.execute(f"SET SESSION innodb_lock_wait_timeout = {timeout}")
    
    @staticmethod
    def build_insert_sql(table_name: str, columns: List[str]) -> str:
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    @staticmethod
    def build_update_sql(table_name: str, set_columns: List[str], where_columns: List[str]) -> str:
        set_clause = ', '.join([f"{col} = %s" for col in set_columns])
        where_clause = ' AND '.join([f"{col} = %s" for col in where_columns])
        return f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    
    @staticmethod
    def format_value_for_sql(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return value.strip() if value.strip() else None
        return value
