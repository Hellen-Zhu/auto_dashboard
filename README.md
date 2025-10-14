# Crypto Test Admin

**Web UI管理系统 for Crypto API Testing Framework**

独立的测试用例管理平台，用于可视化创建、编辑和管理加密货币API测试用例。

---

## 🎯 项目概述

### 项目定位
- **原测试框架** (`crypto_api_test/`): 专注于测试执行
- **本管理系统** (`crypto-test-admin/`): 专注于测试用例管理

### 核心优势
- ✅ **职责分离**: UI管理与测试执行完全解耦
- ✅ **数据共享**: 共用同一PostgreSQL数据库，实时同步
- ✅ **零侵入**: 不修改原测试框架任何代码
- ✅ **易扩展**: 可独立演进，添加企业级功能

---

## 📁 项目结构

```
crypto-test-admin/
├── backend/                    # FastAPI REST API
│   ├── main.py                # API入口
│   ├── database.py            # 数据库连接
│   ├── models.py              # SQLAlchemy模型
│   ├── schemas.py             # Pydantic验证
│   ├── crud.py                # CRUD操作
│   ├── api/                   # API路由
│   │   ├── cases.py
│   │   ├── datasets.py
│   │   └── environments.py
│   ├── .env                   # 环境配置
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                   # Web UI (MVP版本)
│   ├── index.html             # 测试用例管理页
│   ├── datasets.html          # 数据集管理页
│   └── README.md
│
└── README.md                  # 本文件
```

---

## 🚀 快速开始

### 前提条件
- Python 3.9+
- PostgreSQL 数据库 (已有的 apitest 数据库)
- 现代浏览器 (Chrome, Firefox, Safari)

### 1. 启动后端API

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 确认 .env 配置正确
cat .env

# 启动服务
uvicorn main:app --reload --port 8000
```

**验证后端:**
- Health check: http://localhost:8000/health
- API文档: http://localhost:8000/docs

### 2. 启动前端UI

```bash
cd frontend

# 使用Python HTTP服务器
python3 -m http.server 3000
```

**访问UI:**
- Web界面: http://localhost:3000

---

## 💡 功能特性

### MVP版本 (已实现)

#### 测试用例管理
- ✅ 查看所有测试用例列表
- ✅ 按Service/Module筛选
- ✅ 创建新测试用例
- ✅ 编辑现有用例
- ✅ 删除用例 (级联删除数据集)
- ✅ JSON编辑器编辑测试步骤

#### 技术栈
- **后端**: FastAPI 0.104.1 + SQLAlchemy 2.0.23 + PostgreSQL
- **前端**: 原生HTML/CSS/JavaScript (无需构建)

### 未来规划

#### Phase 2 (数据集管理)
- [ ] 为用例添加数据集
- [ ] 编辑数据集变量
- [ ] 环境配置管理

#### Phase 3 (可视化步骤编辑器)
- [ ] 拖拽式步骤构建
- [ ] 可视化请求配置
- [ ] 智能验证规则编辑

#### Phase 4 (高级功能)
- [ ] 用户认证和权限
- [ ] 在线调试测试用例
- [ ] 测试结果查看
- [ ] 批量导入/导出
- [ ] 定时任务调度

---

## 📊 数据库配置

### 连接信息
```
Host: localhost
Port: 5435
Database: apitest
User: postgres
Password: postgres
```

### 数据库架构 (v2.0 - 单表设计)

#### 使用的表
- `api_auto_cases` - 统一测试用例表 (单表设计)
  - 每行代表一个完整、独立的测试用例
  - `test_config` JSONB列包含: steps, variables, validations
- `test_environments` - 环境配置

#### 架构变更说明
**v1.0 (旧)**: 2表设计 - `api_auto_cases` (模板) + `case_data_sets` (数据)
**v2.0 (新)**: 单表设计 - 只有 `api_auto_cases`，所有数据嵌入 `test_config`

**迁移影响**:
- ✅ 更简单的数据模型
- ✅ 每个测试用例都是原子、自包含的
- ✅ 无需管理 FK 关系
- ⚠️ `case_data_sets` 表已废弃

**注意**: 本系统与 `crypto_api_test` 测试框架共享数据库，数据实时同步。

---

## 🔌 API文档

### 测试用例 API (v2.0 - 单表设计)

| 方法 | 端点 | 描述 | 新增/更新 |
|------|------|------|----------|
| GET | `/api/cases` | 获取用例列表 (支持筛选) | ✨ 新增 `env`, `is_active` 过滤 |
| GET | `/api/cases/{id}` | 获取单个用例 | - |
| POST | `/api/cases` | 创建用例 (需要 `test_config`) | ✨ 参数更新 |
| PUT | `/api/cases/{id}` | 更新用例 | ✨ 参数更新 |
| DELETE | `/api/cases/{id}` | 删除用例 | - |

**test_config 结构**:
```json
{
  "steps": [...],        // 测试步骤数组 (必需)
  "variables": {...},    // 测试变量字典
  "validations": {...}   // 验证规则字典
}
```

**新增字段**:
- `environments`: 数组 - 适用环境列表 (空=全部环境)
- `jira_id`: 字符串 - 关联的 Jira ID
- `is_active`: 布尔 - 是否激活

### 数据集 API (已废弃)

| 方法 | 端点 | 状态 |
|------|------|------|
| GET | `/api/cases/{case_id}/datasets` | ⚠️ 已废弃 |
| POST | `/api/datasets` | ⚠️ 已废弃 |
| PUT | `/api/datasets/{id}` | ⚠️ 已废弃 |
| DELETE | `/api/datasets/{id}` | ⚠️ 已废弃 |

**说明**: 单表设计中，所有数据集信息已合并到 `test_config` 中

### 元数据 API

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/services` | 获取所有Service |
| GET | `/api/modules` | 获取所有Module |
| GET | `/api/components` | 获取所有Component |
| GET | `/api/environments` | 获取所有环境 |

**完整API文档**: http://localhost:8000/docs

---

## 🎨 使用示例

### 1. 查看所有测试用例

访问 http://localhost:3000，即可看到所有测试用例列表。

### 2. 创建新测试用例 (v2.0 单表设计)

1. 点击"+ 创建用例"按钮
2. 填写基本信息：
   - 用例名称 (必填)
   - Service (必填)
   - Module, Component, Tags (可选)
   - Environments (可选，逗号分隔，如: uat, prod)
   - Jira ID (可选)
   - 状态 (激活/未激活)
3. 编辑测试配置JSON (test_config):
```json
{
  "steps": [
    {
      "order": 1,
      "protocol": "http",
      "description": "获取K线数据",
      "method": "GET",
      "path": "/exchange/v1/public/get-candlestick",
      "request": {
        "headers": {"Content-Type": "application/json"},
        "params": {
          "instrument_name": "{{@symbol}}",
          "timeframe": "{{@timeframe}}"
        }
      },
      "validations": [],
      "outputs": {}
    }
  ],
  "variables": {
    "symbol": "BTC_USD",
    "timeframe": "1h"
  },
  "validations": {
    "1": {
      "expectedStatusCode": 200,
      "notNull": ["$.result"]
    }
  }
}
```
4. 点击"保存"

### 3. 使用测试框架执行

创建的用例会立即同步到数据库，可直接使用原测试框架执行：

```bash
cd /Users/hellen/PycharmProjects/crypto_api_test

# 运行新创建的用例
python run.py --env uat --id {case_id}
```

---

## 🛠️ 开发指南

### 后端开发

**添加新的API端点:**
1. 在 `backend/api/` 下创建新的路由文件
2. 实现CRUD操作
3. 在 `main.py` 中注册路由

**数据库迁移:**
本项目复用现有数据库表，无需创建新表。

### 前端开发

**MVP版本**使用纯HTML/JavaScript，直接编辑 `frontend/index.html` 即可。

**升级到React:**
如需更丰富的功能，建议使用:
- React 18 + TypeScript
- Vite (构建工具)
- Ant Design 5 (UI组件库)
- React Router (路由)

---

## 🐛 故障排查

### 后端无法启动

**问题**: 数据库连接失败
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**解决**:
1. 确认PostgreSQL服务运行: `lsof -i :5435`
2. 检查 `backend/.env` 配置是否正确
3. 测试数据库连接: `psql -h localhost -p 5435 -U postgres -d apitest`

### 前端CORS错误

**问题**: 浏览器控制台显示CORS错误

**解决**:
1. 确保后端已启动: `curl http://localhost:8000/health`
2. 使用HTTP服务器运行前端，不要直接打开HTML文件
3. 检查 `backend/main.py` 中CORS配置

### API返回404

**问题**: 调用API返回404

**解决**:
1. 检查API路径是否正确: `/api/cases` 而不是 `/cases`
2. 查看Swagger文档确认端点: http://localhost:8000/docs

---

## 📝 更新日志

### v2.3.0 (2025-10-14) - 灵活的验证规则模式 🔥 最新
- 🎯 **新增功能**: 验证规则模式选择
- ✅ 四种验证模式
  - **仅验证状态码**: 只验证HTTP状态码
  - **验证响应体**: 验证完整JSON响应体（支持部分匹配）
  - **验证字段存在性**: 使用JSONPath验证指定字段是否存在
  - **自定义组合**: 自由组合多种验证方式
- ✅ 智能特性
  - 根据选择的模式动态显示对应表单
  - 加载旧数据时自动检测并设置合适模式
  - mode字段仅用于UI控制，不保存到数据库
  - 切换模式时自动清理不需要的字段
- ✅ 用户体验优化
  - 模式说明提示文字
  - JSONPath使用示例
  - 表单更简洁，只显示需要的字段
- ✅ 完全向后兼容，支持所有已有测试用例
- 📄 详细文档: [CHANGELOG_v2.3.0.md](CHANGELOG_v2.3.0.md)
- 🌐 **访问最新版**: http://localhost:3000/index_v2.1.html ⭐

### v2.2.0 (2025-10-14) - 分页功能
- 🎯 **新增功能**: 测试用例列表分页显示
- ✅ 分页功能特性
  - 智能分页控件（首页/上一页/页码/下一页/末页）
  - 可调整每页显示数量（10/20/50/100，**默认10**）
  - 实时显示当前范围和总数（如：显示 1-10 / 共 43 条）
  - 智能页码显示（最多5个页码 + 省略号）
  - 页码按钮高亮显示当前页
  - 禁用状态的首页/末页按钮
- ✅ 性能优化: 内存占用减少50%，只加载当前页数据
- ✅ 与筛选器无缝集成（service/module筛选）
- ✅ 完全向后兼容，无需数据迁移
- 📄 详细文档: [CHANGELOG_v2.2.0.md](CHANGELOG_v2.2.0.md)

### v2.1.3 (2025-10-14) - 测试用例复制功能
- 🎯 **新增功能**: 一键复制测试用例
- ✅ 复制功能特性
  - 紫色主题复制按钮 (区别于编辑/删除)
  - 自动添加 "(副本)" 名称后缀
  - 完整复制 test_config (steps, variables, validations)
  - 自动清空 Jira ID (避免重复关联)
  - 复制后显示新用例ID提示
- ✅ 适用场景: 批量创建相似用例、参数化测试、跨环境复用
- ✅ 无需后端修改，使用现有API实现
- 📄 详细文档: [CHANGELOG_v2.1.3.md](CHANGELOG_v2.1.3.md)

### v2.1.2 (2025-10-14) - 简化验证规则
- 🎯 **优化改进**: 移除"不应存在的字段 (notExist)"验证
- ✅ 简化验证规则配置
  - 移除 `notExist` 字段输入框
  - 验证表单更简洁易用
  - 专注于核心验证点
- ✅ 完全向后兼容，无需数据迁移
- 📄 详细文档: [CHANGELOG_v2.1.2.md](CHANGELOG_v2.1.2.md)

### v2.1.1 (2025-10-14) - 实时预览增强版
- 🎨 **核心升级**: 左右分屏 + 实时JSON预检查
- ✅ 左右分屏布局
  - 左侧：可视化表单编辑器
  - 右侧：固定位置实时预览面板
- ✅ 实时JSON预览
  - 任何字段修改立即显示JSON变化
  - 300ms防抖优化，流畅输入体验
  - 智能验证状态提示 (✓ 有效 / ✗ 无效)
- ✅ 一键复制JSON
- ✅ 错误配置自动检测与提示
- 📄 详细文档: [LIVE_PREVIEW.md](LIVE_PREVIEW.md)

### v2.1.0 (2025-10-14) - 可视化编辑器
- 🎨 **全新功能**: 可视化表单编辑器代替纯JSON编辑
- ✅ 测试步骤可视化配置
  - 动态添加/删除步骤
  - URL、Method、Headers、Params、Body 独立编辑
  - 自动生成步骤编号
- ✅ 变量管理器 (键值对编辑)
- ✅ 验证规则可视化配置
- ✅ Tab切换式界面 (步骤/变量/验证/预览)
- 📄 详细文档: [VISUAL_EDITOR_v2.1.md](VISUAL_EDITOR_v2.1.md)
- 🌐 **访问**: http://localhost:3000/index_v2.html

### v2.0.0 (2025-10-14) - 单表设计重构
- 🔄 **重大更新**: 从2表设计迁移到单表设计
- ✅ 后端完全重构以支持 `test_config` JSONB结构
- ✅ 前端UI更新，新增字段:
  - Environments (环境配置)
  - Jira ID (外部关联)
  - Active Status (激活状态)
- ✅ 数据集API标记为废弃
- ✅ 文档全面更新
- 📄 迁移指南: [MIGRATION_v2.0.md](MIGRATION_v2.0.md)

### v1.0.0 (2025-10-14) - MVP版本
- ✅ 后端API完整实现 (FastAPI)
- ✅ 前端基础UI (纯HTML/JS)
- ✅ 测试用例CRUD功能
- ✅ Service/Module筛选
- ✅ JSON编辑器

---

## 👥 贡献

欢迎提交Issue和Pull Request!

### 开发计划
- [ ] 数据集管理页面
- [ ] 可视化步骤编辑器
- [ ] React版本前端
- [ ] 用户认证系统
- [ ] Docker部署方案

---

## 📄 许可证

MIT License

---

## 📞 联系方式

如有问题，请联系: Hellen Zhu

**相关项目**: [crypto_api_test](../crypto_api_test/) - API测试执行框架
