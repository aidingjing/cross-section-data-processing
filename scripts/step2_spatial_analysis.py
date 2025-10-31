#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.spatial_service import SpatialService
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


def main():
    try:
        config = ConfigUtil.load_config()
        logger = LoggerUtil.setup_logger(
            'Step2Spatial',
            log_file=config['logging']['file']
        )
        
        logger.info("=" * 80)
        logger.info("步骤2: 空间关联分析")
        logger.info("=" * 80)
        
        service = SpatialService(config)
        results = service.analyze_all_relationships()
        
        logger.info("=" * 80)
        logger.info("步骤2完成：空间关联分析成功")
        logger.info(f"横断面与纵断面关联: {len(results.get('h_to_v', {}))} 个")
        logger.info(f"横断面与防治对象关联: {len(results.get('h_to_prevention', {}))} 个")
        logger.info(f"纵断面与防治对象关联: {len(results.get('v_to_prevention', {}))} 个")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
