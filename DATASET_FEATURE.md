# 数据集管理功能使用指南

## 🎉 新功能上线！

现在你可以通过Web界面管理测试用例的**参数化数据集**了！

---

## 📚 什么是数据集？

数据集（Dataset）是参数化测试的核心概念：
- **一个测试用例** = 测试逻辑（测试步骤）
- **多个数据集** = 不同的测试数据

**例如**：
- 测试用例：获取K线数据API
- 数据集1：正常参数（BTC_USD, 1h, 100条）
- 数据集2：边界值测试（BTC_USD, 1m, 1000条）
- 数据集3：异常参数（INVALID, 1h, -1条）

同一个测试用例使用不同的数据集，可以生成多个测试场景！

---

## 🚀 如何使用

### 1. 进入数据集管理页面

**方法一**：从测试用例列表
1. 访问 http://localhost:3000
2. 在用例列表中找到目标用例
3. 点击该用例的 **"数据集"** 按钮

**方法二**：直接访问
```
http://localhost:3000/datasets.html?caseId={用例ID}
```

### 2. 查看现有数据集

进入数据集管理页面后，你会看到：
- 数据集列表（表格形式）
- 每个数据集的信息：
  - ID
  - 数据集名称
  - Jira ID（如有）
  - 适用环境（dev/uat/prod）
  - 变量数量
  - 状态（启用/禁用）

### 3. 创建新数据集

点击 **"+ 添加数据集"** 按钮，填写表单：

#### 必填字段

**数据集名称**：
```
例如：正常参数、边界值测试、异常场景
```

**测试数据变量（JSON格式）**：
```json
{
  "symbol": "BTC_USD",
  "timeframe": "1h",
  "count": 100
}
```

这些变量会替换测试用例中的占位符：
- 测试步骤中的 `{{@symbol}}` → 会被替换为 `"BTC_USD"`
- 测试步骤中的 `{{@timeframe}}` → 会被替换为 `"1h"`
- 测试步骤中的 `{{@count}}` → 会被替换为 `100`

#### 可选字段

**Jira ID**：
```
例如：PROJ-123
关联的Jira任务ID，方便追踪
```

**适用环境**：
```
选择此数据集适用的环境：
□ dev
☑ uat
□ prod

不选择 = 在所有环境下都运行
```

**状态**：
```
☑ 启用此数据集  （勾选=启用，不勾选=禁用）
```

**验证规则覆盖**（高级）：
```json
{
  "step_1": {
    "validations": [
      {"type": "status_code", "expected": 400}
    ]
  }
}
```
用于覆盖测试用例中定义的验证规则。

### 4. 编辑数据集

1. 在数据集列表中找到目标数据集
2. 点击 **"编辑"** 按钮
3. 修改任何字段
4. 点击 **"保存"**

### 5. 查看变量内容

点击 **"查看变量"** 按钮，会弹出对话框显示该数据集的所有变量（只读模式）。

### 6. 删除数据集

1. 在数据集列表中找到目标数据集
2. 点击 **"删除"** 按钮
3. 确认删除

**注意**：删除数据集不会影响测试用例本身。

---

## 💡 使用场景示例

### 场景1：正向测试 + 边界测试

**测试用例**：获取K线数据
```json
{
  "steps": [
    {
      "method": "GET",
      "path": "/exchange/v1/public/get-candlestick",
      "request": {
        "params": {
          "instrument_name": "{{@symbol}}",
          "timeframe": "{{@timeframe}}",
          "count": "{{@count}}"
        }
      }
    }
  ]
}
```

**数据集1：正常参数**
```json
{
  "symbol": "BTC_USD",
  "timeframe": "1h",
  "count": 100
}
```

**数据集2：边界值 - 最小数量**
```json
{
  "symbol": "BTC_USD",
  "timeframe": "1m",
  "count": 1
}
```

**数据集3：边界值 - 最大数量**
```json
{
  "symbol": "BTC_USD",
  "timeframe": "1h",
  "count": 1000
}
```

### 场景2：异常测试

**数据集1：无效的交易对**
```json
{
  "symbol": "INVALID_PAIR",
  "timeframe": "1h",
  "count": 100
}
```
配合验证规则覆盖：
```json
{
  "step_1": {
    "validations": [
      {"type": "status_code", "expected": 400},
      {"type": "body", "path": "$.code", "expected": 40004}
    ]
  }
}
```

**数据集2：无效的时间框架**
```json
{
  "symbol": "BTC_USD",
  "timeframe": "invalid",
  "count": 100
}
```

### 场景3：环境专属测试

**数据集1：UAT环境专用**
```json
{
  "symbol": "TEST_PAIR",
  "timeframe": "1h",
  "count": 10
}
```
设置适用环境：只勾选 `uat`

**数据集2：生产环境专用**
```json
{
  "symbol": "BTC_USD",
  "timeframe": "1h",
  "count": 100
}
```
设置适用环境：只勾选 `prod`

---

## 🎯 最佳实践

### 1. 命名规范

**推荐的数据集命名格式**：
```
[类型][编号]: [简短描述]

例如：
- PT01: Normal Parameters (正向测试01)
- PT02: Boundary - Min Count (正向测试02 - 边界最小值)
- NT01: Invalid Instrument (异常测试01)
- NT02: Missing Required Param (异常测试02)
- ET01: Edge Case - Zero Count (边界测试01)
```

### 2. 变量设计

**清晰的变量名**：
```json
// ✅ 推荐
{
  "symbol": "BTC_USD",
  "timeframe": "1h",
  "expected_count": 100
}

// ❌ 不推荐
{
  "s": "BTC_USD",
  "tf": "1h",
  "c": 100
}
```

### 3. 环境分离

- **UAT环境**：可以使用测试数据、破坏性操作
- **生产环境**：只使用真实数据、只读操作

使用环境选择器确保测试在正确的环境运行。

### 4. Jira关联

为每个数据集关联Jira ID，方便：
- 追踪需求变更
- 定位bug来源
- 生成测试报告

---

## 🔗 与测试框架集成

### 执行特定数据集

```bash
cd /Users/hellen/PycharmProjects/crypto_api_test

# 执行某个用例的所有数据集
python run.py --env uat --id 11

# 执行特定数据集
python run.py --env uat --jira PROJ-123
```

### 数据集如何工作？

1. **测试框架读取数据集**：
   ```python
   # 从数据库查询
   SELECT * FROM case_data_sets WHERE case_id = 11 AND is_active = true
   ```

2. **替换占位符**：
   ```python
   # 原始步骤
   path: "/api?symbol={{@symbol}}&tf={{@timeframe}}"

   # 数据集
   {"symbol": "BTC_USD", "timeframe": "1h"}

   # 替换后
   path: "/api?symbol=BTC_USD&tf=1h"
   ```

3. **应用验证规则**：
   - 使用用例中定义的验证
   - 如果数据集有 `validations_override`，则覆盖

---

## 📊 数据集统计

### 查看用例的数据集数量

在测试用例列表页面，每个用例都会显示关联的数据集数量（未来版本）。

### 数据集执行情况

数据集的执行结果会写入数据库：
```sql
SELECT * FROM auto_case_audit WHERE data_set_id = 116;
```

---

## ⚡ 快捷操作

### 快速复制数据集

1. 编辑一个现有数据集
2. 修改名称和变量
3. 保存（会创建新数据集）

### 批量禁用/启用

通过 `is_active` 字段，可以快速禁用某些数据集，而不删除它们。

---

## 🐛 故障排查

### 数据集页面无法加载

**问题**：点击"数据集"按钮后，页面显示"未指定测试用例ID"

**解决**：
1. 确保URL包含 `?caseId=数字`
2. 检查浏览器控制台是否有JavaScript错误

### 变量未生效

**问题**：创建了数据集，但测试中占位符未被替换

**检查**：
1. 变量名是否与用例中的占位符一致（区分大小写）
2. 数据集是否启用（`is_active = true`）
3. 数据集的适用环境是否包含当前测试环境

### JSON格式错误

**问题**：保存时提示"JSON格式错误"

**解决**：
1. 使用在线JSON验证器检查格式
2. 确保所有字符串用双引号 `"`，不是单引号 `'`
3. 确保最后一个字段后没有多余的逗号

---

## 📝 API参考

### 获取数据集列表
```bash
GET /api/cases/{case_id}/datasets
```

### 创建数据集
```bash
POST /api/datasets
Content-Type: application/json

{
  "case_id": 11,
  "data_set_name": "正常参数",
  "variables": {"symbol": "BTC_USD"},
  "environments": ["uat"],
  "is_active": true
}
```

### 更新数据集
```bash
PUT /api/datasets/{dataset_id}
Content-Type: application/json

{
  "data_set_name": "更新后的名称",
  "variables": {"symbol": "ETH_USD"}
}
```

### 删除数据集
```bash
DELETE /api/datasets/{dataset_id}
```

---

## 🎓 下一步学习

1. 尝试为现有用例创建3个不同的数据集
2. 使用环境选择器，让不同数据集在不同环境运行
3. 使用验证规则覆盖，测试异常场景
4. 通过原测试框架执行，查看多数据集的执行效果

---

## ✨ 总结

通过数据集管理功能，你现在可以：
- ✅ 无需修改代码，快速添加测试场景
- ✅ 通过Web界面管理所有测试数据
- ✅ 实现数据驱动测试
- ✅ 轻松维护大量测试用例

**访问地址**：http://localhost:3000

祝测试愉快！🎉
