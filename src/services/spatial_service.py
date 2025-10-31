from typing import Dict, Any
import json
import os
from src.dao.shapefile_dao import ShapefileDAO
from src.dao.spatial_dao import SpatialDAO
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


class SpatialService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.spatial_dao = SpatialDAO()
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def analyze_all_relationships(self) -> Dict[str, Dict]:
        self.logger.info("=" * 80)
        self.logger.info("开始空间关联分析")
        
        results = {}
        
        results['h_to_v'] = self.analyze_h_to_v_relationship()
        results['h_to_prevention'] = self.analyze_h_to_prevention_relationship()
        results['v_to_prevention'] = self.analyze_v_to_prevention_relationship()
        
        self._save_mappings(results)
        
        self.logger.info("所有空间关联分析完成")
        return results
    
    def analyze_h_to_v_relationship(self) -> Dict[str, List[str]]:
        self.logger.info("分析横断面与纵断面相交关系...")
        
        h_line_path = ConfigUtil.get_shapefile_path(self.config, 'h_line')
        v_line_path = ConfigUtil.get_shapefile_path(self.config, 'v_line')
        
        h_dao = ShapefileDAO(h_line_path)
        v_dao = ShapefileDAO(v_line_path)
        
        h_records = h_dao.read_lines()
        v_records = v_dao.read_lines()
        
        result = self.spatial_dao.batch_line_to_line_analysis(
            h_records, v_records, 'NUMBER', 'NUMBER'
        )
        
        return result
    
    def analyze_h_to_prevention_relationship(self) -> Dict[str, List[str]]:
        self.logger.info("分析横断面与防治对象相交关系...")
        
        h_line_path = ConfigUtil.get_shapefile_path(self.config, 'h_line')
        prevention_path = ConfigUtil.get_shapefile_path(self.config, 'prevention_area')
        
        h_dao = ShapefileDAO(h_line_path)
        p_dao = ShapefileDAO(prevention_path)
        
        h_records = h_dao.read_lines()
        p_records = p_dao.read_polygons()
        
        result = self.spatial_dao.batch_line_to_polygon_analysis(
            h_records, p_records, 'NUMBER', '代码'
        )
        
        return result
    
    def analyze_v_to_prevention_relationship(self) -> Dict[str, List[str]]:
        self.logger.info("分析纵断面与防治对象相交关系...")
        
        v_line_path = ConfigUtil.get_shapefile_path(self.config, 'v_line')
        prevention_path = ConfigUtil.get_shapefile_path(self.config, 'prevention_area')
        
        v_dao = ShapefileDAO(v_line_path)
        p_dao = ShapefileDAO(prevention_path)
        
        v_records = v_dao.read_lines()
        p_records = p_dao.read_polygons()
        
        result = self.spatial_dao.batch_line_to_polygon_analysis(
            v_records, p_records, 'NUMBER', '代码'
        )
        
        return result
    
    def _save_mappings(self, results: Dict):
        mapping_dir = self.config['output']['mapping_dir']
        os.makedirs(mapping_dir, exist_ok=True)
        
        for key, value in results.items():
            filepath = os.path.join(mapping_dir, f"{key}_mapping.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, indent=2)
            self.logger.info(f"保存映射文件: {filepath}")
