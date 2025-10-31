from typing import Dict, Any, List
import json
from src.dao.database_dao import DatabaseDAO
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil
from src.utils.geo_util import GeoUtil


class CodeService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_dao = DatabaseDAO(ConfigUtil.get_database_config(config))
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def generate_all_codes(self) -> bool:
        self.logger.info("=" * 80)
        self.logger.info("开始生成hecd/vecd编码")
        
        try:
            h_mapping = self._generate_h_codes()
            v_mapping = self._generate_v_codes()
            
            self._update_h_surface_vecd_final(h_mapping, v_mapping)
            
            all_codes = list(h_mapping.values()) + list(v_mapping.values())
            self._update_code_table(all_codes)
            
            self.logger.info("hecd/vecd编码生成完成")
            return True
            
        except Exception as e:
            self.logger.error("生成编码失败", exc_info=True)
            return False
    
    def _generate_h_codes(self) -> Dict[str, str]:
        self.logger.info("生成横断面hecd编码...")
        
        h_surface_table = ConfigUtil.get_table_name(self.config, 'h_surface')
        h_point_table = ConfigUtil.get_table_name(self.config, 'h_point')
        
        results = self.db_dao.execute_query(
            f"SELECT hecd, adcd FROM {h_surface_table} WHERE adcd IS NOT NULL"
        )
        
        hecd_mapping = {}
        update_params = []
        
        for old_hecd, adcd in results:
            clean_adcd = GeoUtil.clean_code(adcd)
            new_hecd = clean_adcd + GeoUtil.generate_random_code(5)
            hecd_mapping[old_hecd] = new_hecd
            update_params.append((new_hecd, old_hecd))
        
        if update_params:
            self.db_dao.batch_update(h_surface_table, ['hecd'], ['hecd'], update_params)
            self.db_dao.batch_update(h_point_table, ['hecd'], ['hecd'], update_params)
        
        self.logger.info(f"生成了 {len(hecd_mapping)} 个hecd编码")
        return hecd_mapping
    
    def _generate_v_codes(self) -> Dict[str, str]:
        self.logger.info("生成纵断面vecd编码...")
        
        v_surface_table = ConfigUtil.get_table_name(self.config, 'v_surface')
        v_point_table = ConfigUtil.get_table_name(self.config, 'v_point')
        
        results = self.db_dao.execute_query(
            f"SELECT vecd, adcd, number FROM {v_surface_table} WHERE adcd IS NOT NULL"
        )
        
        vecd_mapping = {}
        number_to_vecd = {}
        update_params = []
        
        for old_vecd, adcd, number in results:
            clean_adcd = GeoUtil.clean_code(adcd)
            new_vecd = clean_adcd + GeoUtil.generate_random_code(5)
            vecd_mapping[old_vecd] = new_vecd
            if number:
                number_to_vecd[number] = new_vecd
            update_params.append((new_vecd, old_vecd))
        
        if update_params:
            self.db_dao.batch_update(v_surface_table, ['vecd'], ['vecd'], update_params)
            self.db_dao.batch_update(v_point_table, ['vecd'], ['vecd'], update_params)
        
        self.logger.info(f"生成了 {len(vecd_mapping)} 个vecd编码")
        return number_to_vecd
    
    def _update_h_surface_vecd_final(self, h_mapping: Dict, number_to_vecd: Dict):
        self.logger.info("同步更新横断面表vecd字段...")
        
        h_surface_table = ConfigUtil.get_table_name(self.config, 'h_surface')
        
        results = self.db_dao.execute_query(
            f"SELECT hecd, vecd FROM {h_surface_table} WHERE vecd IS NOT NULL"
        )
        
        update_params = []
        for hecd, v_number in results:
            if v_number in number_to_vecd:
                final_vecd = number_to_vecd[v_number]
                update_params.append((final_vecd, hecd))
        
        if update_params:
            self.db_dao.batch_update(h_surface_table, ['vecd'], ['hecd'], update_params)
            self.logger.info(f"更新了 {len(update_params)} 个横断面的vecd关联")
    
    def _update_code_table(self, all_codes: List[str]):
        self.logger.info("更新TZX_ONLY_CODE表...")
        
        code_table = ConfigUtil.get_table_name(self.config, 'code_table')
        
        five_digit_codes = set()
        for code in all_codes:
            if len(code) >= 5:
                five_digit_codes.add(code[-5:])
        
        results = self.db_dao.execute_query(
            f"SELECT CODE FROM {code_table}"
        )
        existing_codes = {row[0] for row in results}
        
        new_codes = five_digit_codes - existing_codes
        
        if new_codes:
            insert_values = [(code,) for code in new_codes]
            self.db_dao.batch_insert(code_table, ['CODE'], insert_values)
            self.logger.info(f"插入了 {len(new_codes)} 个新代码")
        else:
            self.logger.info("没有新代码需要插入")
