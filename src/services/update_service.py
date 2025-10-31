from typing import Dict, Any, List
import json
import os
from src.dao.database_dao import DatabaseDAO
from src.dao.shapefile_dao import ShapefileDAO
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


class UpdateService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_dao = DatabaseDAO(ConfigUtil.get_database_config(config))
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def update_adcd_and_vecd(self, mappings: Dict[str, Dict]) -> bool:
        self.logger.info("=" * 80)
        self.logger.info("开始更新adcd和vecd字段")
        
        try:
            h_to_v = mappings.get('h_to_v', {})
            h_to_prevention = mappings.get('h_to_prevention', {})
            v_to_prevention = mappings.get('v_to_prevention', {})
            
            self._update_h_surface_adcd(h_to_prevention)
            self._update_v_surface_adcd(v_to_prevention)
            self._update_h_surface_vecd_temp(h_to_v)
            
            self.logger.info("adcd和vecd字段更新完成")
            return True
            
        except Exception as e:
            self.logger.error("更新adcd和vecd失败", exc_info=True)
            return False
    
    def _update_h_surface_adcd(self, h_to_prevention: Dict):
        self.logger.info("更新横断面表adcd字段...")
        
        h_surface_table = ConfigUtil.get_table_name(self.config, 'h_surface')
        
        params = []
        for number, adcd_list in h_to_prevention.items():
            if adcd_list:
                adcd = adcd_list[0]
                params.append((adcd, number))
        
        if params:
            self.db_dao.batch_update(
                h_surface_table,
                ['adcd'],
                ['number'],
                params
            )
    
    def _update_v_surface_adcd(self, v_to_prevention: Dict):
        self.logger.info("更新纵断面表adcd字段...")
        
        v_surface_table = ConfigUtil.get_table_name(self.config, 'v_surface')
        
        params = []
        for number, adcd_list in v_to_prevention.items():
            if adcd_list:
                adcd = adcd_list[0]
                params.append((adcd, number))
        
        if params:
            self.db_dao.batch_update(
                v_surface_table,
                ['adcd'],
                ['number'],
                params
            )
    
    def _update_h_surface_vecd_temp(self, h_to_v: Dict):
        self.logger.info("更新横断面表vecd临时关联...")
        
        h_surface_table = ConfigUtil.get_table_name(self.config, 'h_surface')
        
        params = []
        for h_number, v_numbers in h_to_v.items():
            if v_numbers:
                v_number = v_numbers[0]
                params.append((v_number, h_number))
        
        if params:
            self.db_dao.batch_update(
                h_surface_table,
                ['vecd'],
                ['number'],
                params
            )
