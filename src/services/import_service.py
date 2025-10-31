from typing import Dict, Any, List
from src.dao.database_dao import DatabaseDAO
from src.dao.shapefile_dao import ShapefileDAO
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil
from src.constants import DM_IDENTITY_MAPPING


class ImportService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_dao = DatabaseDAO(ConfigUtil.get_database_config(config))
        self.field_mapping = ConfigUtil.load_field_mapping()
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def import_h_section_data(self) -> bool:
        self.logger.info("=" * 80)
        self.logger.info("开始导入横断面数据")
        
        try:
            h_point_path = ConfigUtil.get_shapefile_path(self.config, 'h_point')
            h_line_path = ConfigUtil.get_shapefile_path(self.config, 'h_line')
            
            point_dao = ShapefileDAO(h_point_path)
            line_dao = ShapefileDAO(h_line_path)
            
            point_records = point_dao.read_points()
            line_records = line_dao.read_lines()
            
            name_to_number = {rec['NAME']: rec['NUMBER'] for rec in line_records if 'NAME' in rec and 'NUMBER' in rec}
            
            self.logger.info(f"读取到 {len(point_records)} 条横断面点记录")
            self.logger.info(f"读取到 {len(line_records)} 条横断面线记录")
            
            h_point_table = ConfigUtil.get_table_name(self.config, 'h_point')
            h_surface_table = ConfigUtil.get_table_name(self.config, 'h_surface')
            
            self.db_dao.truncate_table(h_point_table)
            self.db_dao.truncate_table(h_surface_table)
            
            point_values = self._prepare_h_point_data(point_records)
            self.db_dao.batch_insert(
                h_point_table,
                ['hecd', 'pcode', 'cdistance', 'ele', 'lgtd', 'lttd', 'coeff', 'moditime', 'orderNo'],
                point_values
            )
            
            surface_values = self._prepare_h_surface_data(point_records, name_to_number)
            self.db_dao.batch_insert(
                h_surface_table,
                ['hecd', 'channel', 'address', 'number', 'dmidentit', 'coeff', 'adcd', 'vecd', 'moditime'],
                surface_values
            )
            
            self.logger.info("横断面数据导入完成")
            return True
            
        except Exception as e:
            self.logger.error("横断面数据导入失败", exc_info=True)
            return False
    
    def import_v_section_data(self) -> bool:
        self.logger.info("=" * 80)
        self.logger.info("开始导入纵断面数据")
        
        try:
            v_point_path = ConfigUtil.get_shapefile_path(self.config, 'v_point')
            v_line_path = ConfigUtil.get_shapefile_path(self.config, 'v_line')
            
            point_dao = ShapefileDAO(v_point_path)
            line_dao = ShapefileDAO(v_line_path)
            
            point_records = point_dao.read_points()
            line_records = line_dao.read_lines()
            
            name_to_number = {rec['NAME']: rec['NUMBER'] for rec in line_records if 'NAME' in rec and 'NUMBER' in rec}
            
            self.logger.info(f"读取到 {len(point_records)} 条纵断面点记录")
            self.logger.info(f"读取到 {len(line_records)} 条纵断面线记录")
            
            v_point_table = ConfigUtil.get_table_name(self.config, 'v_point')
            v_surface_table = ConfigUtil.get_table_name(self.config, 'v_surface')
            
            self.db_dao.truncate_table(v_point_table)
            self.db_dao.truncate_table(v_surface_table)
            
            point_values = self._prepare_v_point_data(point_records)
            self.db_dao.batch_insert(
                v_point_table,
                ['vecd', 'pname', 'cdistance', 'channel', 'bele', 'ele', 'lgtd', 'lttd', 'cltype', 'moditime', 'orderNo'],
                point_values
            )
            
            surface_values = self._prepare_v_surface_data(point_records, name_to_number)
            self.db_dao.batch_insert(
                v_surface_table,
                ['vecd', 'channel', 'address', 'number', 'adcd', 'cele', 'clgtd', 'clttd', 'eletype', 'method', 'moditime'],
                surface_values
            )
            
            self.logger.info("纵断面数据导入完成")
            return True
            
        except Exception as e:
            self.logger.error("纵断面数据导入失败", exc_info=True)
            return False
    
    def _prepare_h_point_data(self, records: List[Dict]) -> List[tuple]:
        values = []
        for rec in records:
            values.append((
                rec.get('hecd'),
                rec.get('pcode'),
                rec.get('cdistance'),
                rec.get('ele'),
                rec.get('lgtd'),
                rec.get('lttd'),
                rec.get('coeff'),
                None,
                rec.get('orderNo')
            ))
        return values
    
    def _prepare_h_surface_data(self, records: List[Dict], name_to_number: Dict) -> List[tuple]:
        grouped = {}
        for rec in records:
            hecd = rec.get('hecd')
            if hecd not in grouped:
                grouped[hecd] = rec
        
        values = []
        for hecd, rec in grouped.items():
            name = rec.get('名称')
            number = name_to_number.get(name) if name else None
            category = rec.get('类别')
            dmidentit = DM_IDENTITY_MAPPING.get(category) if category else None
            
            values.append((
                hecd,
                rec.get('河流名'),
                name,
                number,
                dmidentit,
                rec.get('coeff'),
                None,
                None,
                None
            ))
        
        return values
    
    def _prepare_v_point_data(self, records: List[Dict]) -> List[tuple]:
        values = []
        for rec in records:
            values.append((
                rec.get('vecd'),
                rec.get('pname'),
                rec.get('cdistance'),
                rec.get('河流名'),
                rec.get('bele'),
                rec.get('bele'),
                rec.get('lgtd'),
                rec.get('lttd'),
                None,
                None,
                rec.get('orderNo')
            ))
        return values
    
    def _prepare_v_surface_data(self, records: List[Dict], name_to_number: Dict) -> List[tuple]:
        grouped = {}
        for rec in records:
            vecd = rec.get('vecd')
            if vecd not in grouped:
                grouped[vecd] = rec
        
        values = []
        for vecd, rec in grouped.items():
            name = rec.get('名称')
            number = name_to_number.get(name) if name else None
            
            values.append((
                vecd,
                rec.get('河流名'),
                name,
                number,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ))
        
        return values
