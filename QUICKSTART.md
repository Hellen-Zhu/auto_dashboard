# 快速开始指南

## 🎯 MVP已完成！

恭喜！Crypto Test Admin MVP版本已经成功部署并运行。

---

## ✅ 当前状态

### 已启动的服务

1. **后端API** ✅
   - 地址: http://localhost:8000
   - 状态: 运行中
   - API文档: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

2. **前端UI** ✅
   - 地址: http://localhost:3000
   - 状态: 运行中
   - 可直接在浏览器中访问

### 数据库连接

```
Host: localhost:5435
Database: apitest
User: postgres
已成功连接并可以读取测试用例数据 ✅
```

---

## 🚀 如何使用

### 1. 访问Web界面

在浏览器中打开: **http://localhost:3000**

你应该能看到:
- 顶部导航栏 "Crypto Test Admin"
- 筛选器 (Service, Module)
- 测试用例列表
- "创建用例" 按钮

### 2. 查看现有测试用例

界面会自动加载所有测试用例。你应该能看到:
- ID
- 用例名称
- Service标签
- Module
- Tags标签
- 步骤数
- 创建时间
- 操作按钮 (编辑、删除)

### 3. 创建新测试用例

1. 点击右上角的 **"+ 创建用例"** 按钮
2. 填写表单:
   - **用例名称**: 例如 "测试获取用户信息"
   - **Service**: exchange_svc (必填)
   - **Module**: user (可选)
   - **Component**: profile (可选)
   - **Tags**: P0, smoke (逗号分隔)
   - **描述**: 测试用例的详细说明

3. 编辑测试步骤JSON:
```json
{
  "steps": [
    {
      "order": 1,
      "protocol": "http",
      "description": "获取用户信息",
      "method": "GET",
      "path": "/api/user/profile",
      "request": {
        "headers": {
          "Content-Type": "application/json"
        },
        "params": {
          "user_id": "{{@user_id}}"
        },
        "body": {}
      },
      "validations": [
        {"type": "status_code", "expected": 200}
      ],
      "outputs": {
        "username": "$.data.username"
      }
    }
  ]
}
```

4. 点击 **"保存"** 按钮

### 4. 编辑测试用例

1. 在用例列表中找到要编辑的用例
2. 点击 **"编辑"** 按钮
3. 修改任何字段
4. 点击 **"保存"**

### 5. 删除测试用例

1. 在用例列表中找到要删除的用例
2. 点击 **"删除"** 按钮
3. 确认删除操作

**注意**: 删除用例会同时删除所有关联的数据集（级联删除）。

### 6. 筛选测试用例

使用顶部的下拉菜单:
- **Service筛选**: 选择特定的Service
- **Module筛选**: 选择特定的Module
- 点击 **"刷新"** 按钮重新加载

---

## 🔧 验证系统功能

### 测试后端API

```bash
# 1. Health Check
curl http://localhost:8000/health

# 应该返回:
# {"status":"healthy","service":"crypto-test-admin-api"}

# 2. 获取测试用例列表
curl http://localhost:8000/api/cases?limit=5

# 应该返回JSON格式的用例列表

# 3. 获取Services列表
curl http://localhost:8000/api/services

# 应该返回所有唯一的service名称
```

### 测试前端页面

1. 打开浏览器开发者工具 (F12)
2. 访问 http://localhost:3000
3. 查看Console标签页，应该没有错误
4. 查看Network标签页，应该能看到对 `/api/cases` 的成功请求

---

## 🎨 与原测试框架集成

### 在UI中创建的用例可立即被测试框架执行

```bash
cd /Users/hellen/PycharmProjects/crypto_api_test

# 查看所有用例
python run.py --env uat

# 运行特定用例 (使用UI中创建的用例ID)
python run.py --env uat --id {case_id}

# 按service筛选
python run.py --env uat --service exchange_svc
```

数据是实时同步的！

---

## 🛠️ 管理服务

### 启动服务

```bash
cd /Users/hellen/PycharmProjects/crypto-test-admin

# 使用启动脚本
./start.sh
```

### 停止服务

```bash
# 使用停止脚本
./stop.sh

# 或者手动停止
lsof -ti:8000 | xargs kill  # 停止后端
lsof -ti:3000 | xargs kill  # 停止前端
```

### 重启服务

```bash
./stop.sh && ./start.sh
```

### 查看日志

```bash
# 后端日志
tail -f /tmp/crypto-admin-backend.log

# 前端日志
tail -f /tmp/crypto-admin-frontend.log
```

---

## 📊 项目结构

```
crypto-test-admin/
├── backend/                    # ✅ FastAPI后端
│   ├── main.py                # API入口
│   ├── database.py            # 数据库连接
│   ├── models.py              # ORM模型
│   ├── schemas.py             # 数据验证
│   ├── crud.py                # CRUD操作
│   ├── api/                   # API路由
│   ├── venv/                  # Python虚拟环境
│   ├── .env                   # 配置文件
│   └── requirements.txt
│
├── frontend/                   # ✅ Web UI
│   └── index.html             # 单页面应用
│
├── start.sh                    # 启动脚本
├── stop.sh                     # 停止脚本
├── README.md                   # 项目文档
└── QUICKSTART.md              # 本文件
```

---

## 🐛 常见问题

### Q: 前端无法加载数据

**A**: 检查以下几点:
1. 后端是否正常运行: `curl http://localhost:8000/health`
2. 浏览器开发者工具中是否有CORS错误
3. 确保使用HTTP服务器运行前端，而不是直接打开HTML文件

### Q: 后端连接数据库失败

**A**: 检查:
1. PostgreSQL是否运行: `lsof -i :5435`
2. `backend/.env` 配置是否正确
3. 数据库连接: `psql -h localhost -p 5435 -U postgres -d apitest`

### Q: 如何查看详细的API文档？

**A**: 访问 http://localhost:8000/docs (Swagger UI)

### Q: 创建的用例无法在原测试框架中看到

**A**: 这不可能发生，因为两个系统共享同一个数据库。
检查:
1. 用例是否创建成功（查看UI列表）
2. 测试框架的查询条件是否正确
3. 数据库中是否有数据: `psql -h localhost -p 5435 -U postgres -d apitest -c "SELECT id, name FROM api_auto_cases ORDER BY id DESC LIMIT 5;"`

---

## 🎯 下一步

### 立即可以做的:

1. ✅ 在Web UI中浏览现有测试用例
2. ✅ 创建新的测试用例
3. ✅ 编辑和删除测试用例
4. ✅ 使用筛选器查找特定用例
5. ✅ 通过原测试框架执行新创建的用例

### 未来增强 (Phase 2):

- [ ] 数据集管理页面
- [ ] 环境配置管理
- [ ] 可视化步骤构建器
- [ ] React版本前端 (更丰富的UI)
- [ ] 用户认证和权限管理

---

## 📞 需要帮助？

如有问题，请:
1. 查看 README.md 了解更多详情
2. 查看 backend/README.md 了解API详情
3. 查看后端日志: `/tmp/crypto-admin-backend.log`
4. 访问API文档: http://localhost:8000/docs

---

## 🎉 恭喜！

你已经成功部署并运行了Crypto Test Admin MVP！

现在可以:
- ✅ 通过Web界面管理测试用例
- ✅ 无需直接操作数据库
- ✅ 与原测试框架无缝集成
- ✅ 提高团队协作效率

**开始使用吧！** → http://localhost:3000
