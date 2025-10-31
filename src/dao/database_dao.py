import pymysql
from typing import Dict, Any, List, Tuple, Optional
from src.utils.db_util import DBUtil
from src.utils.logger_util import LoggerUtil


class DatabaseDAO:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def truncate_table(self, table_name: str) -> bool:
        try:
            with DBUtil.get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                DBUtil.set_utf8mb4(cursor)
                
                cursor.execute(f"TRUNCATE TABLE {table_name}")
                conn.commit()
                
                self.logger.info(f"成功清空表: {table_name}")
                cursor.close()
                return True
                
        except Exception as e:
            self.logger.error(f"清空表失败: {table_name}", exc_info=True)
            return False
    
    def batch_insert(
        self, 
        table_name: str, 
        columns: List[str], 
        values: List[Tuple],
        batch_size: int = 1000
    ) -> int:
        if not values:
            return 0
        
        try:
            with DBUtil.get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                DBUtil.set_utf8mb4(cursor)
                DBUtil.set_timeout(cursor)
                
                insert_sql = DBUtil.build_insert_sql(table_name, columns)
                total_inserted = 0
                
                for i in range(0, len(values), batch_size):
                    batch = values[i:i + batch_size]
                    cursor.executemany(insert_sql, batch)
                    total_inserted += cursor.rowcount
                    
                    if (i + batch_size) % 5000 == 0:
                        conn.commit()
                        self.logger.info(f"已插入 {total_inserted} 条记录到 {table_name}")
                
                conn.commit()
                cursor.close()
                
                self.logger.info(f"成功插入 {total_inserted} 条记录到 {table_name}")
                return total_inserted
                
        except Exception as e:
            self.logger.error(f"批量插入失败: {table_name}", exc_info=True)
            raise
    
    def batch_update(
        self,
        table_name: str,
        set_columns: List[str],
        where_columns: List[str],
        params: List[Tuple],
        batch_size: int = 1000
    ) -> int:
        if not params:
            return 0
        
        try:
            with DBUtil.get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                DBUtil.set_utf8mb4(cursor)
                DBUtil.set_timeout(cursor)
                
                update_sql = DBUtil.build_update_sql(table_name, set_columns, where_columns)
                total_updated = 0
                
                for i in range(0, len(params), batch_size):
                    batch = params[i:i + batch_size]
                    cursor.executemany(update_sql, batch)
                    total_updated += cursor.rowcount
                    
                    if (i + batch_size) % 5000 == 0:
                        conn.commit()
                        self.logger.info(f"已更新 {total_updated} 条记录在 {table_name}")
                
                conn.commit()
                cursor.close()
                
                self.logger.info(f"成功更新 {total_updated} 条记录在 {table_name}")
                return total_updated
                
        except Exception as e:
            self.logger.error(f"批量更新失败: {table_name}", exc_info=True)
            raise
    
    def execute_query(self, sql: str, params: Tuple = None) -> List[Tuple]:
        try:
            with DBUtil.get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                DBUtil.set_utf8mb4(cursor)
                
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                
                results = cursor.fetchall()
                cursor.close()
                
                return results
                
        except Exception as e:
            self.logger.error(f"查询失败: {sql}", exc_info=True)
            raise
    
    def execute_update(self, sql: str, params: Tuple = None) -> int:
        try:
            with DBUtil.get_connection(self.db_config) as conn:
                cursor = conn.cursor()
                DBUtil.set_utf8mb4(cursor)
                
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                
                affected_rows = cursor.rowcount
                conn.commit()
                cursor.close()
                
                return affected_rows
                
        except Exception as e:
            self.logger.error(f"更新失败: {sql}", exc_info=True)
            raise
