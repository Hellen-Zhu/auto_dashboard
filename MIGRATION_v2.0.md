# Migration Guide: v1.0 → v2.0 单表设计重构

## 📋 概述

**日期**: 2025-10-14
**变更类型**: 重大架构更新 - Breaking Change
**影响范围**: 后端API、前端UI、数据模型

---

## 🔄 架构变更

### 旧架构 (v1.0 - 2表设计)
```
api_auto_cases (测试用例模板)
  ├─ id
  ├─ name, service, module, component, tags
  ├─ parameters (JSONB) - 仅包含 steps
  └─ author, created_at

case_data_sets (参数化数据集)
  ├─ id, case_id (FK)
  ├─ data_set_name
  ├─ variables (JSONB) - 测试数据
  ├─ validations_override (JSONB) - 验证规则
  ├─ environments (Array)
  ├─ jira_id
  └─ is_active
```

### 新架构 (v2.0 - 单表设计)
```
api_auto_cases (统一测试用例表)
  ├─ id
  ├─ name, service, module, component, tags
  ├─ environments (Array) ✨ 新增
  ├─ jira_id (String) ✨ 新增
  ├─ is_active (Boolean) ✨ 新增
  ├─ test_config (JSONB) 📦 结构变更
  │   ├─ steps (Array) - 测试步骤
  │   ├─ variables (Dict) - 测试变量
  │   └─ validations (Dict) - 验证规则
  └─ author, created_at
```

---

## ✨ 核心变更

### 1. 数据模型变更

#### test_config 结构
**旧 (parameters)**:
```json
{
  "steps": [
    {
      "order": 1,
      "method": "GET",
      "path": "/api/endpoint",
      ...
    }
  ]
}
```

**新 (test_config)**:
```json
{
  "steps": [
    {
      "order": 1,
      "method": "GET",
      "path": "/api/endpoint",
      ...
    }
  ],
  "variables": {
    "key": "value"
  },
  "validations": {
    "1": {
      "expectedStatusCode": 200,
      "notNull": ["$.result"]
    }
  }
}
```

#### 新增字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `environments` | Array | 适用环境列表，空=全部环境 | `["uat", "prod"]` |
| `jira_id` | String | 关联的Jira票据ID | `"PROJ-123"` |
| `is_active` | Boolean | 是否激活该测试用例 | `true` |

---

## 🔧 后端变更

### Models (models.py)

**已删除**:
- `CaseDataSet` 类

**更新**:
```python
class ApiAutoCase(Base):
    # 新增字段
    environments = Column(ARRAY(Text), index=True)
    jira_id = Column(String(50), unique=True)
    is_active = Column(Boolean, default=True, index=True)

    # 字段名变更
    test_config = Column(JSONB, nullable=False)  # 原 parameters

    # 已移除
    # data_sets = relationship(...)  # 无 FK 关系
```

### Schemas (schemas.py)

**新增字段**:
```python
class CaseBase(BaseModel):
    environments: Optional[List[str]] = None
    jira_id: Optional[str] = None
    test_config: Dict[str, Any]  # 原 parameters
    is_active: bool = True
```

**废弃**:
- `DataSetBase`, `DataSetCreate`, `DataSetUpdate`, `DataSetResponse`

### CRUD (crud.py)

**新增功能**:
```python
def get_cases(..., env: Optional[str] = None, is_active: Optional[bool] = True):
    # 支持环境过滤
    if env:
        query = query.filter(
            or_(
                ApiAutoCase.environments == None,
                ApiAutoCase.environments.any(env)
            )
        )
    # 支持激活状态过滤
    if is_active is not None:
        query = query.filter(ApiAutoCase.is_active == is_active)
```

**已删除**:
- `get_datasets_by_case()`
- `get_dataset_by_id()`
- `create_dataset()`
- `update_dataset()`
- `delete_dataset()`

### API Endpoints (api/cases.py)

**更新**:
```python
# 新增查询参数
@router.get("/cases")
def list_cases(..., env: Optional[str] = None, is_active: Optional[bool] = True):
    pass

# 验证 test_config 结构
@router.post("/cases")
def create_case(case: CaseCreate, ...):
    if 'steps' not in case.test_config:
        raise ValueError("test_config must contain 'steps' array")
```

**废弃**:
- `/api/cases/{case_id}/datasets` - 获取数据集列表
- `/api/datasets` - 创建数据集
- `/api/datasets/{id}` - 更新/删除数据集

---

## 🎨 前端变更

### index.html

#### 新增表单字段
```html
<!-- Environments -->
<input type="text" id="caseEnvironments" placeholder="例如: uat, prod">

<!-- Jira ID -->
<input type="text" id="caseJiraId" placeholder="例如: PROJ-123">

<!-- 激活状态 -->
<select id="caseIsActive">
    <option value="true">激活</option>
    <option value="false">未激活</option>
</select>
```

#### 字段名更新
```javascript
// 旧
document.getElementById('caseParameters').value

// 新
document.getElementById('caseTestConfig').value
```

#### 默认模板变更
```javascript
// 新增 variables 和 validations
const defaultTestConfig = {
    steps: [...],
    variables: { example_var: 'example_value' },
    validations: { '1': { expectedStatusCode: 200 } }
};
```

#### 移除功能
- **"数据集" 按钮** - 已移除，因为单表设计不再需要单独的数据集管理

---

## 🚀 迁移步骤

### 对于新系统部署

✅ **无需迁移** - 直接使用 v2.0 代码即可

### 对于已有部署

1. **备份数据库**
   ```bash
   pg_dump -h localhost -p 5435 -U postgres apitest > backup_v1.sql
   ```

2. **更新代码**
   ```bash
   cd /Users/hellen/PycharmProjects/crypto-test-admin
   git pull  # 或手动更新文件
   ```

3. **重启后端**
   ```bash
   cd backend
   source venv/bin/activate
   # Backend会自动重载
   ```

4. **清除浏览器缓存**
   - 强制刷新前端: Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)

---

## ⚠️ 兼容性说明

### 向后不兼容

#### 数据模型
- ❌ `case_data_sets` 表不再使用
- ❌ `parameters` 字段已重命名为 `test_config`
- ❌ `test_config` 必须包含 `steps`, `variables`, `validations`

#### API响应
```json
// v1.0 响应
{
  "id": 1,
  "name": "Test Case",
  "parameters": { "steps": [...] }
}

// v2.0 响应
{
  "id": 1,
  "name": "Test Case",
  "test_config": {
    "steps": [...],
    "variables": {...},
    "validations": {...}
  },
  "environments": ["uat"],
  "jira_id": null,
  "is_active": true
}
```

### 向前兼容

✅ 已有数据库中的 `api_auto_cases` 表可以继续工作
✅ `test_environments` 表无变更
⚠️ 需要确保现有数据的 `test_config` 包含所需字段

---

## 📊 数据验证

### 检查数据完整性

```sql
-- 检查 test_config 结构
SELECT
    id,
    name,
    test_config ? 'steps' AS has_steps,
    test_config ? 'variables' AS has_variables,
    test_config ? 'validations' AS has_validations
FROM api_auto_cases
WHERE is_active = true
LIMIT 10;
```

### 查看新增字段

```sql
-- 查看环境和Jira ID分布
SELECT
    environments,
    jira_id,
    is_active,
    COUNT(*) AS count
FROM api_auto_cases
GROUP BY environments, jira_id, is_active;
```

---

## 🧪 测试

### API测试

```bash
# 1. 获取用例列表 (新增环境过滤)
curl 'http://localhost:8000/api/cases?env=uat&is_active=true&limit=5'

# 2. 创建用例 (新结构)
curl -X POST 'http://localhost:8000/api/cases' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Test Case",
    "service": "exchange_svc",
    "environments": ["uat"],
    "jira_id": "PROJ-123",
    "is_active": true,
    "test_config": {
      "steps": [{...}],
      "variables": {},
      "validations": {}
    }
  }'
```

### UI测试

1. **访问**: http://localhost:3000
2. **创建用例**: 验证新字段显示正确
3. **编辑用例**: 验证 test_config 加载正确
4. **删除用例**: 验证不再提示"删除关联数据集"

---

## 📚 相关文档

- **README.md** - 已更新完整文档
- **API文档**: http://localhost:8000/docs
- **测试框架**: `/Users/hellen/PycharmProjects/crypto_api_test`

---

## 🎯 下一步

### 已完成
- ✅ 后端模型重构
- ✅ API端点更新
- ✅ 前端UI适配
- ✅ 文档更新

### 未来规划
- [ ] 数据迁移工具 (2表→单表)
- [ ] 批量编辑环境
- [ ] Jira集成
- [ ] 高级过滤器

---

## 📞 支持

如有问题，请联系: Hellen Zhu

**项目地址**: `/Users/hellen/PycharmProjects/crypto-test-admin`
