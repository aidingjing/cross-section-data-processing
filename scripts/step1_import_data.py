#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.import_service import ImportService
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


def main():
    try:
        config = ConfigUtil.load_config()
        logger = LoggerUtil.setup_logger(
            'Step1Import',
            log_file=config['logging']['file']
        )
        
        logger.info("=" * 80)
        logger.info("步骤1: 数据导入")
        logger.info("=" * 80)
        
        service = ImportService(config)
        
        success_h = service.import_h_section_data()
        if not success_h:
            logger.error("横断面数据导入失败")
            return 1
        
        success_v = service.import_v_section_data()
        if not success_v:
            logger.error("纵断面数据导入失败")
            return 1
        
        logger.info("=" * 80)
        logger.info("步骤1完成：数据导入成功")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
