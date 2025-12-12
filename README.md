# InvestTrack

一个用于记录个人投资的轻量仓库，使用 MySQL 作为后台数据库，后端示例使用 Python + Flask + SQLAlchemy。

数据模型（简要）
- Institution: 机构（name 等）
- Product: 机构下的产品或一次投资记录，字段包括：
  - invested_amount: 投资值（投入金额）
  - term_months: 投资期限（以月计）
  - current_value: 现值
  - expected_profit: 预期收益
  - actual_profit: 实际收益
  - annualized_return: 年化收益（可由系统根据 invested_amount、current_value 与期限计算）

快速开始
1. 克隆仓库（或将本示例文件放入新仓库）
2. 启动 MySQL（推荐使用 Docker Compose）:
   - 编辑 `.env.example` 为 `.env` 并根据需要修改
   - 运行: `docker-compose up -d`
3. 创建 Python 虚拟环境并安装依赖:
   - python3 -m venv .venv
   - source .venv/bin/activate
   - pip install -r backend/requirements.txt
4. 初始化数据库（如果希望直接执行 SQL 初始化脚本）:
   - 使用 MySQL 客户端连接到容器中的数据库，运行 `sql/schema.sql`
   - 或直接运行后端，后端会在首次启动时自动创建表（SQLAlchemy create_all）
5. 运行后端:
   - cd backend
   - export FLASK_APP=app.py
   - export FLASK_ENV=development
   - flask run --host=0.0.0.0 --port=5000

示例 API（后端示例）
- GET /institutions
- POST /institutions  { "name": "机构A" }
- GET /institutions/<id>/products
- POST /institutions/<id>/products
  payload 示例:
  {
    "name": "产品A",
    "invested_amount": 10000.00,
    "term_months": 12,
    "current_value": 11000.00,
    "expected_profit": 1000.00,
    "actual_profit": 1000.00,
    "annualized_return": null,
    "purchase_date": "2025-01-01"
  }
后端会在 annualized_return 为空时自动计算：annualized_return = (current_value / invested_amount) ** (12 / term_months) - 1
