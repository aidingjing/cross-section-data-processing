#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.code_service import CodeService
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


def main():
    try:
        config = ConfigUtil.load_config()
        logger = LoggerUtil.setup_logger(
            'Step4Code',
            log_file=config['logging']['file']
        )
        
        logger.info("=" * 80)
        logger.info("步骤4: 生成hecd/vecd编码")
        logger.info("=" * 80)
        
        service = CodeService(config)
        success = service.generate_all_codes()
        
        if not success:
            logger.error("生成编码失败")
            return 1
        
        logger.info("=" * 80)
        logger.info("步骤4完成：hecd/vecd编码生成成功")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
