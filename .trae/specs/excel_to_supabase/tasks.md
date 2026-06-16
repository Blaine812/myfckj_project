# Excel数据导入Supabase并创建实时看板 - 任务分解与优先级

## [ ] Task 1: 创建数据导入脚本 import_data.py
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 使用pandas读取Excel文件（影刀.xlsx）
  - 处理空值和数据类型转换（日期转ISO字符串）
  - 使用supabase-py连接数据库并批量插入数据
  - 支持清空已有数据或upsert策略
  - 打印成功/失败记录数
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-1.1: 脚本成功读取Excel并输出数据行数
  - `programmatic` TR-1.2: 数据成功插入Supabase，记录数与Excel一致
  - `human-judgment` TR-1.3: 脚本有清晰的输出日志

## [ ] Task 2: 创建实时HTML看板页面 index.html
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 使用Supabase JS SDK实现数据获取和实时订阅
  - 创建响应式布局（统计卡片、图表、数据表格）
  - 集成Chart.js实现图表可视化
  - 支持Realtime订阅和轮询模式自动切换
  - 添加手动刷新按钮和加载动画
- **Acceptance Criteria Addressed**: AC-3, AC-4, AC-5
- **Test Requirements**:
  - `human-judgment` TR-2.1: 页面加载后能显示所有统计卡片
  - `human-judgment` TR-2.2: 图表正确渲染数值数据
  - `human-judgment` TR-2.3: 表格显示完整数据
  - `human-judgment` TR-2.4: 修改数据库后页面自动更新

## [x] Task 3: 创建README.md使用说明文档
- **Priority**: P1
- **Depends On**: Task 1, Task 2
- **Description**: 
  - 说明环境准备步骤（安装依赖）
  - 提供运行数据导入脚本的命令
  - 说明如何启动前端页面
  - 说明如何配置Supabase连接信息
- **Acceptance Criteria Addressed**: 部署说明
- **Test Requirements**:
  - `human-judgment` TR-3.1: 文档清晰易懂，步骤完整
  - `human-judgment` TR-3.2: 命令和配置说明准确