#!/usr/bin/env python3

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config_util import ConfigUtil
from src.utils.logger_util import LoggerUtil


def run_all_steps():
    try:
        config = ConfigUtil.load_config()
        logger = LoggerUtil.setup_logger(
            'Main',
            log_file=config['logging']['file']
        )
        
        logger.info("=" * 80)
        logger.info("开始执行完整流程")
        logger.info("=" * 80)
        
        from scripts.step1_import_data import main as step1
        from scripts.step2_spatial_analysis import main as step2
        from scripts.step3_update_adcd import main as step3
        from scripts.step4_generate_codes import main as step4
        
        steps = [
            ("步骤1: 数据导入", step1),
            ("步骤2: 空间分析", step2),
            ("步骤3: 更新adcd/vecd", step3),
            ("步骤4: 生成编码", step4)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n开始执行 {step_name}")
            result = step_func()
            if result != 0:
                logger.error(f"{step_name} 执行失败")
                return result
            logger.info(f"{step_name} 执行成功\n")
        
        logger.info("=" * 80)
        logger.info("完整流程执行成功！")
        logger.info("=" * 80)
        return 0
        
    except Exception as e:
        print(f"执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


def validate_config():
    try:
        config = ConfigUtil.load_config()
        ConfigUtil.validate_config(config)
        print("配置文件验证通过")
        return 0
    except Exception as e:
        print(f"配置文件验证失败: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='断面数据处理系统')
    parser.add_argument('--all', action='store_true', help='执行完整流程')
    parser.add_argument('--validate-config', action='store_true', help='验证配置文件')
    
    args = parser.parse_args()
    
    if args.validate_config:
        return validate_config()
    elif args.all:
        return run_all_steps()
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
