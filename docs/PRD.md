# Agent Company 2D 像素可视化系统（V1）PRD

## 1. 目标
构建一个 2D 像素风的 Agent 公司可视化系统，优先实现“可读、可管、可扩展”：
- 一眼看懂组织结构（总览 → 部门 → 角色）
- 快速判断角色状态（在线/任务/风险）
- 基础管理操作（筛选、定位、详情、刷新）

## 2. 范围
### 2.1 V1 必做
1. 2D 像素办公室主界面
   - 公司总览区
   - 部门区块（Tech / Investment / Content）
   - 角色卡片（Spark / Forge / Finley / Quill）
2. 状态可视化
   - 在线状态
   - 当前任务
   - 最近更新时间
   - 风险/阻塞标记
   - 轻量像素动画反馈
3. 基础交互
   - 点击角色查看详情
   - 按部门 / 状态筛选
   - 手动刷新 + 自动刷新（可配置）
4. 配置驱动扩展
   - 新增部门/角色只改配置，不改核心渲染组件
5. 工程可落地
   - 清晰目录、状态管理、Mock 数据

### 2.2 V1 非目标
- 3D 场景
- 游戏玩法系统
- 重特效动画

## 3. 关键交互
- 进入页面：默认展示总览 + 部门 + 角色卡片
- 点击角色：右侧详情面板更新
- 筛选：按部门或状态快速聚焦
- 刷新：手动立即刷新；自动按间隔刷新

## 4. 数据与状态模型（配置驱动）
- Department: id, name, color
- Role: id, name, title, departmentId, avatar
- RoleStatus: roleId, statusCode, currentTask, lastUpdatedAt, riskLevel, blockers
- StatusRegistry（全局状态语义表）
  - 不在组件内写死枚举
  - 统一映射展示文案、颜色、图标、动画

## 5. 验收标准
1. 打开页面后，能直观看到 Agent 公司组织结构
2. 可区分 4 个角色状态，且可查看详情
3. 支持通过配置新增 1 个虚拟部门和角色（无需改核心渲染组件）
4. 代码结构清晰，可持续扩展

## 6. Research Inputs（必读资料影响）
### 6.1 OpenClaw Office（管理能力）
参考资料：`/Users/jelly/Documents/Knowledge-Base/10-AI/工具/可视化/OpenClaw-Office.md`

设计影响：
1. **信息层级固定为总览→部门→角色详情**，避免“纯展示”缺少管理入口。
2. 引入稳定状态语义（idle/working/speaking/tool_calling/error）并映射到 V1 展示字典。
3. UI 必须可筛选、可定位、可快速查看细节，不做单纯大屏动画。

### 6.2 Star Office UI（2D 像素表达）
参考资料：`/Users/jelly/Documents/Knowledge-Base/10-AI/工具/可视化/Star-Office-UI.md`

设计影响：
1. 采用 **2D 像素风 + 空间分区表达状态**（例如阻塞/风险角色强调区）。
2. 优先走“轻后端 + 配置化”路线，先做可演示版本再接真实源。
3. 保持移动端和普通屏幕可读，动画只做状态反馈。

### 6.3 Claude Code Hooks Observability（可观测性）
参考资料：`/Users/jelly/Documents/Knowledge-Base/10-AI/工具/可视化/Claude-Code-Hooks-Observability.md`

设计影响：
1. V1 先用 polling，但数据层预留事件流适配器（WebSocket/Event Adapter）。
2. 强制引入**状态标准化映射层**，后续多数据源统一落到标准状态模型。
3. 将“最近事件/时间轴”列入 M2/M3，解释“当前状态为何如此”。
