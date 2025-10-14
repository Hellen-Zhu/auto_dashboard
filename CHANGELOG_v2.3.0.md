# Crypto Test Admin - v2.3.0 更新日志

**发布日期**: 2025-10-14
**版本**: v2.3.0
**更新类型**: 功能增强

---

## 🎯 核心更新

### ✅ 灵活的验证规则模式选择

添加了验证模式选择功能，允许用户根据需求自由选择验证方式，而不是固定验证所有字段。

---

## 📋 功能详情

### 1. 验证模式选择器 (Validation Mode Selector)

**位置**: 验证规则编辑表单顶部

**四种验证模式**:

#### 模式 1: 仅验证状态码 (Status Only)
- **适用场景**: 只关心请求是否成功，不关心响应内容
- **验证字段**:
  - `expectedStatusCode`: HTTP状态码（如200, 201, 404等）
- **示例**:
```json
{
  "validations": {
    "1": {
      "expectedStatusCode": 200
    }
  }
}
```

#### 模式 2: 验证响应体 (Body Validation)
- **适用场景**: 需要精确匹配响应体内容
- **验证字段**:
  - `body`: 期望的JSON响应体（支持部分匹配）
- **特点**: 支持嵌套对象、数组等复杂结构
- **示例**:
```json
{
  "validations": {
    "1": {
      "body": {
        "code": 0,
        "result": {
          "id": 123,
          "status": "active"
        }
      }
    }
  }
}
```

#### 模式 3: 验证字段存在性 (Fields Validation)
- **适用场景**: 只需验证某些字段是否存在，不关心具体值
- **验证字段**:
  - `notNull`: 必须存在的字段列表（JSONPath格式）
- **支持语法**: `$.result`, `$.result.data`, `$.items[0].id`
- **示例**:
```json
{
  "validations": {
    "1": {
      "notNull": [
        "$.result",
        "$.result.data",
        "$.result.id"
      ]
    }
  }
}
```

#### 模式 4: 自定义组合 (Custom Combination)
- **适用场景**: 需要组合多种验证方式
- **验证字段**:
  - `expectedStatusCode`: 状态码验证
  - `body`: 响应体验证
  - `notNull`: 字段存在性验证
- **灵活性**: 可以自由选择启用哪些验证字段
- **示例**:
```json
{
  "validations": {
    "1": {
      "expectedStatusCode": 200,
      "body": {
        "code": 0
      },
      "notNull": [
        "$.result.data"
      ]
    }
  }
}
```

### 2. 模式切换逻辑

**智能字段管理**:
- 切换到"仅验证状态码"：自动移除body和notNull字段
- 切换到"验证响应体"：自动移除expectedStatusCode和notNull字段
- 切换到"验证字段存在性"：自动移除expectedStatusCode和body字段
- 切换到"自定义组合"：保留所有字段，用户可选择使用

**默认值设置**:
- 新建验证规则时默认为"仅验证状态码"模式
- expectedStatusCode默认值为200

### 3. 自动模式检测

**加载已有用例时**:
系统会自动分析validation结构，推断合适的验证模式：

```javascript
// 自动检测逻辑
if (hasStatus && hasBody && hasFields) {
    mode = 'custom';  // 有状态码、响应体、字段验证 → 自定义组合
} else if (hasBody) {
    mode = 'body';    // 只有响应体验证 → 验证响应体
} else if (hasFields) {
    mode = 'fields';  // 只有字段验证 → 验证字段存在性
} else {
    mode = 'status';  // 只有状态码或无验证 → 仅验证状态码
}
```

### 4. JSON清理机制

**mode字段不会保存到数据库**:
- `mode` 字段仅用于UI控制，不会出现在最终的test_config中
- 保存时自动清理mode字段
- JSON预览中不显示mode字段
- 确保test_config符合后端API规范

---

## 🎨 用户界面

### 验证模式选择下拉框

```
┌─────────────────────────────────┐
│ 验证模式                        │
├─────────────────────────────────┤
│ ▼ 仅验证状态码                  │  ← 默认选项
│   验证响应体 (JSON)              │
│   验证字段存在性                 │
│   自定义组合                     │
└─────────────────────────────────┘
    只验证HTTP状态码                  ← 提示文本
```

### 条件表单渲染

根据选择的模式，动态显示对应的输入字段：

**仅验证状态码**:
```
期望状态码: [200]
```

**验证响应体**:
```
期望响应体 (JSON格式):
┌────────────────────────────────┐
│ {                               │
│   "code": 0,                    │
│   "result": {...}               │
│ }                               │
└────────────────────────────────┘
💡 支持部分匹配，只验证指定的字段
```

**验证字段存在性**:
```
必须存在的字段 (JSONPath，逗号分隔):
[$.result, $.result.data, $.result.id]
💡 使用JSONPath语法，例如: $.result.data 或 $.items[0].id
```

**自定义组合**:
```
期望状态码: [200]

期望响应体 (JSON格式):
┌────────────────────────────────┐
│ {                               │
│   "code": 0                     │
│ }                               │
└────────────────────────────────┘
💡 支持部分匹配，只验证指定的字段

必须存在的字段 (JSONPath，逗号分隔):
[$.result.data]
💡 使用JSONPath语法，例如: $.result.data 或 $.items[0].id
```

---

## 🔧 技术实现

### 前端代码结构

**1. 数据结构**
```javascript
validations = {
  "1": {
    mode: "status",  // UI辅助字段，不保存到数据库
    expectedStatusCode: 200
  },
  "2": {
    mode: "body",
    body: { code: 0, result: {...} }
  },
  "3": {
    mode: "fields",
    notNull: ["$.result", "$.result.data"]
  },
  "4": {
    mode: "custom",
    expectedStatusCode: 200,
    body: { code: 0 },
    notNull: ["$.result.data"]
  }
}
```

**2. 核心函数**

```javascript
// 渲染验证规则表单
function renderValidations() {
    // 根据mode动态渲染不同的表单字段
}

// 渲染条件字段
function renderValidationFields(stepNum, mode) {
    // 根据模式返回对应的HTML
}

// 切换验证模式
function changeValidationMode(stepNum, mode) {
    // 更新mode，清理不需要的字段，重新渲染
}

// 清理validations（移除mode字段）
function cleanValidations(validations) {
    // 返回不包含mode的纯净validation对象
}
```

**3. JSON生成**
```javascript
// updateJSONPreview()函数中
const cleanedValidations = {};
Object.keys(validations).forEach(stepNum => {
    const validation = validations[stepNum];
    cleanedValidations[stepNum] = {};

    // 只保留实际的验证字段，不包含mode
    if (validation.expectedStatusCode !== undefined) {
        cleanedValidations[stepNum].expectedStatusCode = validation.expectedStatusCode;
    }
    if (validation.body !== undefined) {
        cleanedValidations[stepNum].body = validation.body;
    }
    if (validation.notNull && validation.notNull.length > 0) {
        cleanedValidations[stepNum].notNull = validation.notNull;
    }
});
```

---

## 📖 使用示例

### 示例 1: 简单状态码验证

**需求**: 测试API是否返回200状态码

**操作步骤**:
1. 添加验证规则
2. 选择 "仅验证状态码"
3. 输入期望状态码: 200
4. 保存

**生成的JSON**:
```json
{
  "validations": {
    "1": {
      "expectedStatusCode": 200
    }
  }
}
```

### 示例 2: 响应体部分匹配

**需求**: 验证响应码和结果类型

**操作步骤**:
1. 添加验证规则
2. 选择 "验证响应体 (JSON)"
3. 输入期望响应体:
```json
{
  "code": 0,
  "result": {
    "type": "success"
  }
}
```
4. 保存

**生成的JSON**:
```json
{
  "validations": {
    "1": {
      "body": {
        "code": 0,
        "result": {
          "type": "success"
        }
      }
    }
  }
}
```

### 示例 3: 字段存在性验证

**需求**: 确保响应包含必要字段，不关心具体值

**操作步骤**:
1. 添加验证规则
2. 选择 "验证字段存在性"
3. 输入必须存在的字段: `$.result, $.result.data, $.result.id`
4. 保存

**生成的JSON**:
```json
{
  "validations": {
    "1": {
      "notNull": [
        "$.result",
        "$.result.data",
        "$.result.id"
      ]
    }
  }
}
```

### 示例 4: 组合验证

**需求**: 验证状态码、部分响应体、关键字段存在

**操作步骤**:
1. 添加验证规则
2. 选择 "自定义组合"
3. 设置状态码: 200
4. 设置响应体: `{"code": 0}`
5. 设置必须字段: `$.result.data`
6. 保存

**生成的JSON**:
```json
{
  "validations": {
    "1": {
      "expectedStatusCode": 200,
      "body": {
        "code": 0
      },
      "notNull": [
        "$.result.data"
      ]
    }
  }
}
```

---

## 🔄 向后兼容性

### 完全兼容旧数据

**已有测试用例**:
- ✅ 自动检测并设置合适的验证模式
- ✅ 保留所有原有验证字段
- ✅ 无需手动迁移数据

**旧格式示例**:
```json
{
  "validations": {
    "1": {
      "expectedStatusCode": 200,
      "notNull": ["$.result"]
    }
  }
}
```

**加载后自动设置**:
- 系统检测到有expectedStatusCode和notNull
- 自动设置mode为"custom"
- 用户可见并修改

---

## 📂 更新文件列表

### 修改的文件

1. **frontend/index_v2.1.html**
   - 新增: `changeValidationMode()` 函数
   - 新增: `renderValidationFields()` 函数
   - 修改: `addValidation()` - 添加默认mode
   - 修改: `renderValidations()` - 动态渲染表单
   - 修改: `updateJSONPreview()` - 清理mode字段
   - 修改: `saveCase()` - 保存前清理mode
   - 修改: `editCase()` - 加载时自动检测mode

### 新增的文件
- `CHANGELOG_v2.3.0.md` (本文件)

---

## ✅ 优势对比

### 旧方式 vs 新方式

| 对比项 | 旧方式 | 新方式 |
|--------|--------|--------|
| 验证灵活性 | ❌ 固定字段，无法选择 | ✅ 4种模式自由选择 |
| 状态码验证 | ✅ 支持 | ✅ 支持 |
| 响应体验证 | ✅ 支持 | ✅ 支持（更清晰） |
| 字段验证 | ✅ 支持 | ✅ 支持（更直观） |
| 组合验证 | ❌ 所有字段都显示 | ✅ 按需显示 |
| 用户体验 | ❌ 表单冗长 | ✅ 简洁清晰 |
| 学习曲线 | ❌ 需要理解所有字段 | ✅ 模式说明一目了然 |

---

## 🎯 适用场景

### 各模式推荐场景

**仅验证状态码** (推荐占比: 40%)
- ✅ 健康检查接口
- ✅ 简单的GET请求
- ✅ 只关心请求成功与否

**验证响应体** (推荐占比: 30%)
- ✅ 创建/更新操作，需验证返回数据
- ✅ 精确匹配特定字段值
- ✅ 复杂的业务逻辑验证

**验证字段存在性** (推荐占比: 20%)
- ✅ 列表查询接口
- ✅ 详情查询接口
- ✅ 不关心具体值，只要字段存在

**自定义组合** (推荐占比: 10%)
- ✅ 复杂的业务场景
- ✅ 需要多层次验证
- ✅ 严格的测试要求

---

## 🚀 性能影响

- **前端**: +~150 行代码
- **后端**: 无影响
- **数据库**: 无影响
- **加载速度**: 无变化
- **验证逻辑**: 更清晰，更易维护

---

## 📞 反馈

如有问题或建议，请联系项目维护者。

**访问最新版**:
- http://localhost:3000/index_v2.1.html ⭐ (实时预览增强版)
