#!/usr/bin/env python3

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.update_service import UpdateService
from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


def main():
    try:
        config = ConfigUtil.load_config()
        logger = LoggerUtil.setup_logger(
            'Step3Update',
            log_file=config['logging']['file']
        )
        
        logger.info("=" * 80)
        logger.info("步骤3: 更新adcd和vecd字段")
        logger.info("=" * 80)
        
        mapping_dir = config['output']['mapping_dir']
        
        with open(os.path.join(mapping_dir, 'h_to_v_mapping.json'), 'r', encoding='utf-8') as f:
            h_to_v = json.load(f)
        
        with open(os.path.join(mapping_dir, 'h_to_prevention_mapping.json'), 'r', encoding='utf-8') as f:
            h_to_prevention = json.load(f)
        
        with open(os.path.join(mapping_dir, 'v_to_prevention_mapping.json'), 'r', encoding='utf-8') as f:
            v_to_prevention = json.load(f)
        
        mappings = {
            'h_to_v': h_to_v,
            'h_to_prevention': h_to_prevention,
            'v_to_prevention': v_to_prevention
        }
        
        service = UpdateService(config)
        success = service.update_adcd_and_vecd(mappings)
        
        if not success:
            logger.error("更新adcd和vecd字段失败")
            return 1
        
        logger.info("=" * 80)
        logger.info("步骤3完成：adcd和vecd字段更新成功")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
