# 断面数据处理系统

## 项目简介

处理河流横断面和纵断面的地理空间数据，包括数据导入、空间分析和编码生成。

## 功能特性

- ✅ 横断面和纵断面数据导入
- ✅ 空间关联分析（断面与防治对象）
- ✅ 自动生成唯一编码（hecd/vecd）
- ✅ 批量数据处理和更新
- ✅ 完整的日志记录

## 技术栈

- Python 3.8+
- MySQL 5.7+
- pymysql
- GDAL/OGR (计划中)
- pandas

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

复制配置示例文件并修改：

```bash
cp config/config.example.json config/config.json
```

编辑 `config/config.json`，填入您的数据库连接信息和Shapefile路径。

### 3. 准备数据

将Shapefile文件放到 `data/shapefiles/` 目录：
- 横断面点.shp
- 横断面线.shp
- 纵断面点.shp
- 纵断面线.shp
- 防治对象分布面_合并.shp

### 4. 运行

```bash
# 步骤1: 数据导入
python scripts/step1_import_data.py

# 步骤2: 空间分析
python scripts/step2_spatial_analysis.py

# 步骤3: 更新adcd字段
python scripts/step3_update_adcd.py

# 步骤4: 生成编码
python scripts/step4_generate_codes.py
```

## 项目结构

```
cross-section-data-processing/
├── config/                 # 配置文件
├── src/                    # 源代码
│   ├── models/            # 数据模型
│   ├── dao/               # 数据访问层
│   ├── services/          # 业务逻辑层
│   └── utils/             # 工具类
├── scripts/               # 执行脚本
├── tests/                 # 测试
├── data/                  # 数据目录
└── docs/                  # 文档
```

## 开发状态

🚧 项目正在开发中...

- [x] 项目结构设计
- [x] 工具类模块
- [ ] DAO层实现
- [ ] 服务层实现
- [ ] 执行脚本
- [ ] 测试

## 许可证

MIT License

## 作者

开发中...
