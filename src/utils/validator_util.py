import os
from typing import List, Dict, Any
import pymysql


class ValidatorUtil:
    @staticmethod
    def validate_shapefile_exists(path: str) -> bool:
        if not path:
            return False
        
        base_path = path.replace('.shp', '')
        required_files = ['.shp', '.dbf', '.shx']
        
        for ext in required_files:
            if not os.path.exists(base_path + ext):
                return False
        
        return True
    
    @staticmethod
    def validate_database_connection(config: Dict[str, Any]) -> bool:
        try:
            connection = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset=config.get('charset', 'utf8mb4')
            )
            connection.close()
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_field_mapping(shapefile_fields: List[str], mapping: Dict[str, Any]) -> bool:
        for db_field, shp_field in mapping.items():
            if shp_field is None:
                continue
            
            if isinstance(shp_field, dict):
                continue
            
            if shp_field not in shapefile_fields:
                return False
        
        return True
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        return True
    
    @staticmethod
    def validate_geometry(geometry) -> bool:
        if geometry is None:
            return False
        
        try:
            return geometry.IsValid()
        except Exception:
            return False
    
    @staticmethod
    def validate_directory_exists(path: str, create_if_missing: bool = True) -> bool:
        if os.path.exists(path):
            return os.path.isdir(path)
        
        if create_if_missing:
            try:
                os.makedirs(path, exist_ok=True)
                return True
            except Exception:
                return False
        
        return False
