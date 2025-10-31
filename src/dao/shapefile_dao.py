import shapefile
from typing import List, Dict, Any, Tuple
from src.utils.logger_util import LoggerUtil


class ShapefileDAO:
    def __init__(self, shapefile_path: str):
        self.shapefile_path = shapefile_path
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def read_points(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"读取Shapefile: {self.shapefile_path}")
            
            sf = shapefile.Reader(self.shapefile_path, encoding='utf-8')
            fields = [field[0] for field in sf.fields[1:]]
            
            records = []
            for i, record in enumerate(sf.iterShapeRecords()):
                attributes = record.record
                geometry = record.shape
                
                if geometry.shapeType == shapefile.POINT:
                    x, y = geometry.points[0]
                else:
                    x, y = None, None
                
                row_data = dict(zip(fields, attributes))
                row_data['lgtd'] = x
                row_data['lttd'] = y
                records.append(row_data)
                
                if (i + 1) % 5000 == 0:
                    self.logger.info(f"已读取 {i + 1} 条记录...")
            
            self.logger.info(f"成功读取 {len(records)} 条点记录")
            return records
            
        except Exception as e:
            self.logger.error(f"读取Shapefile失败: {self.shapefile_path}", exc_info=True)
            raise
    
    def read_lines(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"读取Shapefile: {self.shapefile_path}")
            
            sf = shapefile.Reader(self.shapefile_path, encoding='utf-8')
            fields = [field[0] for field in sf.fields[1:]]
            
            records = []
            for i, record in enumerate(sf.iterShapeRecords()):
                attributes = record.record
                geometry = record.shape
                
                row_data = dict(zip(fields, attributes))
                row_data['geometry'] = geometry
                records.append(row_data)
            
            self.logger.info(f"成功读取 {len(records)} 条线记录")
            return records
            
        except Exception as e:
            self.logger.error(f"读取Shapefile失败: {self.shapefile_path}", exc_info=True)
            raise
    
    def read_polygons(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"读取Shapefile: {self.shapefile_path}")
            
            sf = shapefile.Reader(self.shapefile_path, encoding='utf-8')
            fields = [field[0] for field in sf.fields[1:]]
            
            records = []
            for i, record in enumerate(sf.iterShapeRecords()):
                attributes = record.record
                geometry = record.shape
                
                row_data = dict(zip(fields, attributes))
                row_data['geometry'] = geometry
                records.append(row_data)
            
            self.logger.info(f"成功读取 {len(records)} 条面记录")
            return records
            
        except Exception as e:
            self.logger.error(f"读取Shapefile失败: {self.shapefile_path}", exc_info=True)
            raise
    
    def get_field_names(self) -> List[str]:
        try:
            sf = shapefile.Reader(self.shapefile_path, encoding='utf-8')
            return [field[0] for field in sf.fields[1:]]
        except Exception as e:
            self.logger.error(f"获取字段名失败: {self.shapefile_path}", exc_info=True)
            raise
    
    def get_feature_count(self) -> int:
        try:
            sf = shapefile.Reader(self.shapefile_path, encoding='utf-8')
            return len(sf)
        except Exception as e:
            self.logger.error(f"获取要素数量失败: {self.shapefile_path}", exc_info=True)
            raise
