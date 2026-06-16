# Excel数据导入Supabase并创建实时看板 - 产品需求文档

## Overview
- **Summary**: 本项目将读取本地Excel文件（影刀.xlsx）中的数据，导入到Supabase数据库，并创建一个实时数据看板网页进行可视化展示。
- **Purpose**: 实现Excel数据的云端存储和实时可视化，支持数据的动态更新和图表展示。
- **Target Users**: 需要进行数据管理和可视化的业务用户。

## Goals
- 成功读取Excel文件并导入Supabase数据库
- 创建美观的实时数据看板网页
- 支持数据的实时更新（Realtime或轮询模式）
- 实现图表可视化和统计卡片展示

## Non-Goals (Out of Scope)
- 复杂的用户认证系统
- 数据导出功能
- 复杂的权限管理

## Background & Context
- Excel文件位于：C:\Users\Lenovo\Desktop\影刀.xlsx
- Supabase已创建，提供了连接URL
- 需要参考附件图片设计网页布局

## Functional Requirements
- **FR-1**: 读取Excel文件，处理空值和数据类型转换
- **FR-2**: 连接Supabase数据库，批量插入数据
- **FR-3**: 创建实时HTML看板，展示表格数据
- **FR-4**: 实现统计卡片和图表可视化
- **FR-5**: 支持Realtime订阅或轮询模式更新数据

## Non-Functional Requirements
- **NFR-1**: 响应式布局，适配PC和移动端
- **NFR-2**: 数据更新延迟不超过5秒（轮询模式）或1秒（Realtime模式）
- **NFR-3**: 界面美观，与常见数据看板风格一致

## Constraints
- **Technical**: Python环境需安装pandas、openpyxl、supabase库
- **Dependencies**: Supabase JS SDK (CDN)、Chart.js

## Assumptions
- 用户已创建Supabase数据库并启用Realtime功能
- 用户提供的Supabase连接信息正确
- Excel文件格式规范，第一行为列名

## Acceptance Criteria

### AC-1: Excel数据读取成功
- **Given**: Excel文件存在于指定路径
- **When**: 运行import_data.py脚本
- **Then**: 成功读取数据，处理空值和数据类型转换，输出JSON格式数据
- **Verification**: `programmatic`

### AC-2: 数据成功导入Supabase
- **Given**: Supabase连接正常
- **When**: 运行import_data.py脚本
- **Then**: 数据批量插入成功，打印成功/失败记录数
- **Verification**: `programmatic`

### AC-3: HTML看板展示数据
- **Given**: 数据库已有数据
- **When**: 打开index.html页面
- **Then**: 页面显示完整的表格数据和统计卡片
- **Verification**: `human-judgment`

### AC-4: 实时更新功能
- **Given**: 数据库数据发生变化
- **When**: 通过Supabase仪表盘修改数据
- **Then**: 页面在1秒内（Realtime）或5秒内（轮询）自动更新
- **Verification**: `human-judgment`

### AC-5: 图表可视化
- **Given**: 页面已加载
- **When**: 查看图表区域
- **Then**: 图表正确显示数值字段的可视化效果
- **Verification**: `human-judgment`

## Open Questions
- [ ] 用户需要提供Supabase的anon key
- [ ] 需要确认Excel文件的具体结构和数据类型