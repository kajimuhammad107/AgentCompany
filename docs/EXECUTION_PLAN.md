# AgentCompany 执行计划

_基于 Star-Office-UI 改造，实现多部门多角色 Agent 公司可视化_

---

## 一、现有代码分析

### 可复用部分
1. **Phaser 3 渲染引擎**（frontend/game.js, layout.js）
   - 2D 像素渲染、动画系统、资源加载
   - 状态切换逻辑（idle/writing/error 等）
   - 直接扩展为多角色渲染

2. **Flask 后端**（backend/app.py）
   - 状态管理 API（/state, /agents-state）
   - 扩展数据模型支持多部门/多角色

3. **像素风美术资产**（assets/）
   - spritesheet 动画系统
   - 为新角色创建类似动画

### 需要改造部分
1. **数据模型**：从单角色���展到 Department + Role + RoleStatus
2. **前端布局**：从单角色办公室扩展到分区显示（部门区块）
3. **配置系统**：新增配置驱动的组织结构定义

---

## 二、任务拆解（可并行执行）

### 阶段 1：数据层改造（2-3 小时）

#### Task 1.1：后端数据模型扩展
**负责人**：Backend Dev Agent  
**目标**：扩展 Flask API 支持多部门多角色  
**输入**：
- 现有 backend/app.py
- PRD 中的数据模型定义

**输出**：
- 新增 API：
  - `GET /api/departments` — 返回部门列表
  - `GET /api/roles` — 返回角色列表（可按部门筛选）
  - `GET /api/roles/:id/status` — 返回角色状态
  - `POST /api/roles/:id/status` — 更新角色状态
- 数据结构：
  ```json
  {
    "departments": [
      {"id": "tech", "name": "Tech", "color": "#4A90E2"}
    ],
    "roles": [
      {"id": "spark", "name": "Spark", "title": "CEO", "departmentId": null, "avatar": "spark.png"}
    ],
    "roleStatus": {
      "spark": {
        "statusCode": "working",
        "currentTask": "Review Q1 roadmap",
        "lastUpdatedAt": "2026-03-04T09:00:00Z",
        "riskLevel": "low",
        "blockers": []
      }
    }
  }
  ```

**验收标准**：
- API 返回正确的 JSON 数据
- 支持 Mock 数据（4 个角色 + 3 个部门）
- 单元测试覆盖率 >80%

**工期**：2 小时

---

#### Task 1.2：配置文件定义
**负责人**：Config Dev Agent  
**目标**：创建配置驱动的组织结构定义  
**输入**：PRD 中的组织结构要求

**输出**：
- `config/organization.json`：
  ```json
  {
    "departments": [
      {"id": "tech", "name": "Tech", "color": "#4A90E2"},
      {"id": "investment", "name": "Investment", "color": "#50C878"},
      {"id": "content", "name": "Content", "color": "#FFB347"}
    ],
    "roles": [
      {"id": "spark", "name": "Spark", "title": "CEO", "departmentId": null, "avatar": "spark.png"},
      {"id": "forge", "name": "Forge", "title": "Tech Lead", "departmentId": "tech", "avatar": "forge.png"},
      {"id": "finley", "name": "Finley", "title": "Investment Analyst", "departmentId": "investment", "avatar": "finley.png"},
      {"id": "quill", "name": "Quill", "title": "Content Writer", "departmentId": "content", "avatar": "quill.png"}
    ]
  }
  ```

- `config/status-registry.json`（状态语义映射）：
  ```json
  {
    "idle": {"label": "空闲", "color": "#888", "icon": "💤", "animation": "idle"},
    "working": {"label": "工作中", "color": "#4A90E2", "icon": "💻", "animation": "typing"},
    "speaking": {"label": "沟通中", "color": "#50C878", "icon": "💬", "animation": "talking"},
    "tool_calling": {"label": "调用工具", "color": "#FFB347", "icon": "🔧", "animation": "tool"},
    "error": {"label": "异常", "color": "#E74C3C", "icon": "⚠️", "animation": "error"}
  }
  ```

**验收标准**：
- 配置文件格式正确（JSON Schema 验证）
- 后端能正确加载配置

**工期**：1 小时

---

### 阶段 2：前端布局改造（4-5 小时）

#### Task 2.1：多角色布局系统
**负责人**：Frontend Dev Agent  
**目标**：改造 layout.js，支持多角色分区显示  
**输入**：
- 现有 frontend/layout.js
- config/organization.json

**输出**：
- 新增 `LAYOUT.departments` 配置：
  ```javascript
  departments: {
    tech: { x: 200, y: 150, width: 300, height: 200 },
    investment: { x: 550, y: 150, width: 300, height: 200 },
    content: { x: 900, y: 150, width: 300, height: 200 }
  }
  ```

- 新增 `LAYOUT.roles` 配置：
  ```javascript
  roles: {
    spark: { x: 640, y: 50, scale: 1.2 },  // CEO 居中顶部
    forge: { x: 250, y: 200, scale: 1.0 },
    finley: { x: 600, y: 200, scale: 1.0 },
    quill: { x: 950, y: 200, scale: 1.0 }
  }
  ```

**验收标准**：
- 4 个角色正确显示在各自区域
- 部门区块有视觉分隔（背景色/边框）
- 响应式布局（支持 1280x720 和 1920x1080）

**工期**：3 小时

---

#### Task 2.2：角色卡片组件
**负责人**：Frontend Dev Agent  
**目标**：创建可复用的角色卡片组件  
**输入**：
- config/organization.json
- config/status-registry.json

**输出**：
- `frontend/components/RoleCard.js`：
  - 显示角色头像、名字、职位
  - 显示当前状态（图标 + 颜色）
  - 显示当前任务（文本）
  - 点击展开详情面板

**验收标准**：
- 卡片样式符合像素风格
- 状态变化有动画反馈
- 点击事件正确触发

**工期**：2 小时

---

#### Task 2.3：详情面板改造
**负责人**：Frontend Dev Agent  
**目标**：改造详情面板支持多角色切换  
**输入**：现有详情面板逻辑

**输出**：
- 点击不同角色，详情面板更新内容
- 显示：
  - 角色基本信息（名字、职位、部门）
  - 当前状态（statusCode + 语义标签）
  - 当前任务（currentTask）
  - 最近更新时间（lastUpdatedAt）
  - 风险等级（riskLevel）
  - 阻塞项（blockers）

**验收标准**：
- 切换角色时详情面板平滑更新
- 数据正确显示

**工期**：2 小时

---

### 阶段 3：交互功能（3-4 小时）

#### Task 3.1：筛选功能
**负责人**：Frontend Dev Agent  
**目标**：实现按部门/状态筛选角色  
**输入**：config/organization.json, config/status-registry.json

**输出**：
- 筛选面板（左上角）：
  - 部门筛选：All / Tech / Investment / Content
  - 状态筛选：All / idle / working / speaking / tool_calling / error
- 筛选逻辑：
  - 选中筛选条件后，只显示符合条件的角色
  - 未选中的角色淡出（opacity: 0.3）

**验收标准**：
- 筛选逻辑正确
- 动画流畅

**工期**：2 小时

---

#### Task 3.2：刷新机制
**负责人**：Frontend Dev Agent  
**目标**：实现手动刷新 + 自动刷新  
**输入**：现有刷新逻辑

**输出**：
- 手动刷新按钮（右上角）
- 自动刷新（可配置间隔，默认 30 秒）
- 刷新时显示加载动画

**验收标准**：
- 手动刷新立即生效
- 自动刷新按间隔执行
- 加载动画正确显示

**工期**：1 小时

---

#### Task 3.3：状态动画
**负责人**：Animation Dev Agent  
**目标**：为不同状态添加像素动画  
**输入**：config/status-registry.json

**输出**：
- idle：角色静止，轻微呼吸动画
- working：角色打字动画（手指移动）
- speaking：角色说话动画（嘴巴开合）
- tool_calling：角色使用工具动画（手持工具）
- error：角色困惑动画（头上问号）

**验收标准**：
- 动画流畅（60fps）
- 状态切换时动画平滑过渡

**工期**：3 小时

---

### 阶段 4：测试与文档（2-3 小时）

#### Task 4.1：单元测试
**负责人**：Testing Agent  
**目标**：补全单元测试  
**输入**：所有新增代码

**输出**：
- 后端测试：
  - API 端点测试（departments, roles, status）
  - 数据模型测试
  - 配置加载测试
- 前端测试：
  - 组件渲染测试（RoleCard, DetailPanel）
  - 筛选逻辑测试
  - 刷新机制测试

**验收标准**：
- 测试覆盖率 >80%
- 所有测试通过

**工期**：2 小时

---

#### Task 4.2：文档更新
**负责人**：Doc Agent  
**目标**：更新项目文档  
**输入**：所有新增功能

**输出**：
- `README.md`：
  - 项目介绍
  - 快速启动
  - 配置说明
- `docs/API.md`：
  - API 端点文档
  - 数据结构说明
- `docs/CONFIG.md`：
  - 配置文件说明
  - 如何新增部门/角色

**验收标准**：
- 文档清晰易懂
- 示例代码可运行

**工期**：1 小时

---

## 三、并行执行策略

### 第一轮并行（阶段 1）
- Task 1.1（后端数据模型）+ Task 1.2（配置文件）同时进行
- 预计 2-3 小时完成

### 第二轮并行（阶段 2）
- Task 2.1（布局系统）+ Task 2.2（角色卡片）+ Task 2.3（详情面板）同时进行
- 预计 4-5 小时完成

### 第三轮并行（阶段 3）
- Task 3.1（筛选）+ Task 3.2（刷新）+ Task 3.3（动画）同时进行
- 预计 3-4 小时完成

### 第四轮并行（阶段 4）
- Task 4.1（测试）+ Task 4.2（文档）同时进行
- 预计 2-3 小时完成

---

## 四、总工期估算

- **最短路径**（理想并行）：11-15 小时
- **保守估计**（考虑集成调试）：15-20 小时

---

## 五、风险与依赖

### 风险
1. **美术资产不足**：如果没有 4 个角色的 spritesheet，需要额外时间制作
2. **Phaser 版本兼容**：Star-Office-UI 用的是 Phaser 3.80.1，需确保新功能兼容
3. **状态同步延迟**：如果后端数据源是真实 Agent 状态，需考虑轮询频率和性能

### 依赖
1. Task 2.x 依赖 Task 1.x 完成（前端需要后端 API）
2. Task 3.3 依赖 Task 2.2 完成（动画需要角色卡片组件）
3. Task 4.1 依赖所有开发任务完成

---

## 六、验收标准（整体）

### 功能验收
- ✅ 打开页面后，能直观看到 4 个角色 + 3 个部门
- ✅ 可区分角色状态（idle/working/speaking/tool_calling/error）
- ✅ 点击角色查看详情
- ✅ 按部门/状态筛选角色
- ✅ 手动刷新 + 自动刷新（30 秒）
- ✅ 支持通过配置新增 1 个虚拟部门和角色（无需改核心渲染组件）

### 技术验收
- ✅ 代码结构清晰（frontend/backend/config 分离）
- ✅ 测试覆盖率 >80%
- ✅ 文档完整（README + API + CONFIG）
- ✅ 构建成功（npm run build 无错误）

---

## 七、下一步行动

1. **立即启动阶段 1**：调用 Agent Teams 并行执行 Task 1.1 + Task 1.2
2. **等待回调**：任务完成后检查结果，验证 API 和配置文件
3. **启动阶段 2**：基于阶段 1 的产出，启动前端改造
4. **迭代验证**：每个阶段完成后，Forge 自己验证功能，有问题立即修复
5. **最终交付**：所有阶段完成后，通知 jelly 体验

---

_执行计划生成时间：2026-03-04_  
_预计完成时间：2026-03-04（如果今晚开始，明早完成）_
