import json
import os
from typing import Dict, Any, Optional


class ConfigUtil:
    _config_cache: Optional[Dict[str, Any]] = None
    _field_mapping_cache: Optional[Dict[str, Any]] = None
    
    @staticmethod
    def load_config(config_path: str = 'config/config.json') -> Dict[str, Any]:
        if ConfigUtil._config_cache is not None:
            return ConfigUtil._config_cache
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            ConfigUtil._config_cache = json.load(f)
        
        return ConfigUtil._config_cache
    
    @staticmethod
    def load_field_mapping(mapping_path: str = 'config/field_mapping.json') -> Dict[str, Any]:
        if ConfigUtil._field_mapping_cache is not None:
            return ConfigUtil._field_mapping_cache
        
        if not os.path.exists(mapping_path):
            raise FileNotFoundError(f"字段映射文件不存在: {mapping_path}")
        
        with open(mapping_path, 'r', encoding='utf-8') as f:
            ConfigUtil._field_mapping_cache = json.load(f)
        
        return ConfigUtil._field_mapping_cache
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        required_keys = ['database', 'shapefiles', 'tables', 'batch', 'output']
        
        for key in required_keys:
            if key not in config:
                raise ValueError(f"配置文件缺少必需的键: {key}")
        
        db_config = config['database']
        required_db_keys = ['host', 'port', 'user', 'password', 'database']
        for key in required_db_keys:
            if key not in db_config:
                raise ValueError(f"数据库配置缺少必需的键: {key}")
        
        return True
    
    @staticmethod
    def get_database_config(config: Dict[str, Any]) -> Dict[str, Any]:
        return config['database']
    
    @staticmethod
    def get_shapefile_path(config: Dict[str, Any], key: str) -> str:
        return config['shapefiles'].get(key, '')
    
    @staticmethod
    def get_table_name(config: Dict[str, Any], key: str) -> str:
        return config['tables'].get(key, '')
    
    @staticmethod
    def get_batch_config(config: Dict[str, Any]) -> Dict[str, int]:
        return config['batch']
    
    @staticmethod
    def clear_cache():
        ConfigUtil._config_cache = None
        ConfigUtil._field_mapping_cache = None
