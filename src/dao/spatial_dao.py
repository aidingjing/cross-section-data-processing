from typing import Dict, List, Tuple
from src.utils.logger_util import LoggerUtil
import shapefile


class SpatialDAO:
    def __init__(self):
        self.logger = LoggerUtil.get_logger(self.__class__.__name__)
    
    def check_line_intersects_line(self, line1, line2) -> bool:
        try:
            bbox1 = line1.bbox
            bbox2 = line2.bbox
            
            if bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2]:
                return False
            if bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3]:
                return False
            
            points1 = line1.points
            points2 = line2.points
            
            for i in range(len(points1) - 1):
                for j in range(len(points2) - 1):
                    if self._segments_intersect(
                        points1[i], points1[i+1],
                        points2[j], points2[j+1]
                    ):
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error("线段相交判断失败", exc_info=True)
            return False
    
    def check_line_intersects_polygon(self, line, polygon) -> bool:
        try:
            bbox_line = line.bbox
            bbox_poly = polygon.bbox
            
            if bbox_line[2] < bbox_poly[0] or bbox_line[0] > bbox_poly[2]:
                return False
            if bbox_line[3] < bbox_poly[1] or bbox_line[1] > bbox_poly[3]:
                return False
            
            line_points = line.points
            poly_points = polygon.points
            
            for point in line_points:
                if self._point_in_polygon(point, poly_points):
                    return True
            
            for i in range(len(line_points) - 1):
                for j in range(len(poly_points) - 1):
                    if self._segments_intersect(
                        line_points[i], line_points[i+1],
                        poly_points[j], poly_points[j+1]
                    ):
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error("线面相交判断失败", exc_info=True)
            return False
    
    def _segments_intersect(self, p1: Tuple, p2: Tuple, p3: Tuple, p4: Tuple) -> bool:
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        
        return ccw(p1,p3,p4) != ccw(p2,p3,p4) and ccw(p1,p2,p3) != ccw(p1,p2,p4)
    
    def _point_in_polygon(self, point: Tuple, polygon_points: List[Tuple]) -> bool:
        x, y = point
        n = len(polygon_points)
        inside = False
        
        p1x, p1y = polygon_points[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon_points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def batch_line_to_line_analysis(
        self, 
        layer1_records: List[Dict], 
        layer2_records: List[Dict],
        key1: str = 'NUMBER',
        key2: str = 'NUMBER'
    ) -> Dict[str, List[str]]:
        self.logger.info(f"开始线线相交分析: {len(layer1_records)} x {len(layer2_records)}")
        
        result = {}
        total = len(layer1_records)
        
        for idx, rec1 in enumerate(layer1_records):
            geom1 = rec1['geometry']
            key1_val = rec1.get(key1)
            
            if not key1_val:
                continue
            
            intersecting = []
            for rec2 in layer2_records:
                geom2 = rec2['geometry']
                key2_val = rec2.get(key2)
                
                if not key2_val:
                    continue
                
                if self.check_line_intersects_line(geom1, geom2):
                    intersecting.append(key2_val)
            
            if intersecting:
                result[key1_val] = intersecting
            
            if (idx + 1) % 50 == 0:
                self.logger.info(f"已处理 {idx + 1}/{total}")
        
        self.logger.info(f"线线相交分析完成，找到 {len(result)} 个相交关系")
        return result
    
    def batch_line_to_polygon_analysis(
        self,
        line_records: List[Dict],
        polygon_records: List[Dict],
        line_key: str = 'NUMBER',
        polygon_key: str = '代码'
    ) -> Dict[str, List[str]]:
        self.logger.info(f"开始线面相交分析: {len(line_records)} x {len(polygon_records)}")
        
        result = {}
        total = len(line_records)
        
        for idx, line_rec in enumerate(line_records):
            line_geom = line_rec['geometry']
            line_key_val = line_rec.get(line_key)
            
            if not line_key_val:
                continue
            
            intersecting = []
            for poly_rec in polygon_records:
                poly_geom = poly_rec['geometry']
                poly_key_val = poly_rec.get(polygon_key)
                
                if not poly_key_val:
                    continue
                
                if self.check_line_intersects_polygon(line_geom, poly_geom):
                    intersecting.append(poly_key_val)
            
            if intersecting:
                result[line_key_val] = intersecting
            
            if (idx + 1) % 50 == 0:
                self.logger.info(f"已处理 {idx + 1}/{total}")
        
        self.logger.info(f"线面相交分析完成，找到 {len(result)} 个相交关系")
        return result
