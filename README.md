# Excel数据导入Supabase并创建实时看板

本项目用于将Excel文件中的数据导入Supabase数据库，并创建一个实时数据看板网页进行可视化展示。

## 项目结构

```
├── import_data.py    # 数据导入脚本
├── index.html        # 实时看板页面
└── README.md         # 使用说明
```

## 环境准备

### 1. 安装Python依赖

```bash
pip install pandas openpyxl supabase
```

### 2. 配置Supabase连接信息

#### 在 `import_data.py` 中配置：

```python
# Supabase配置
SUPABASE_URL = "https://gvdlqqtdtdqdahzfvjra.supabase.co"
SUPABASE_KEY = "your_anon_key_here"  # 替换为你的anon key
```

#### 在 `index.html` 中配置：

```javascript
const SUPABASE_URL = "https://gvdlqqtdtdqdahzfvjra.supabase.co";
const SUPABASE_KEY = "your_anon_key_here";  // 替换为你的anon key
const TABLE_NAME = "影刀";  // Excel文件名（不含扩展名）
```

## 运行数据导入脚本

```bash
python import_data.py
```

脚本会：
1. 读取 `C:\Users\Lenovo\Desktop\影刀.xlsx` 文件
2. 处理空值和数据类型转换
3. 清空Supabase表中已有数据
4. 批量插入所有行
5. 打印成功/失败记录数

## 启动前端页面

### 方法一：直接打开HTML文件

直接用浏览器打开 `index.html` 文件即可。

### 方法二：使用本地服务器（推荐）

```bash
npx serve .
```

然后在浏览器中访问显示的地址（通常是 `http://localhost:3000`）。

## 功能特性

### 数据导入脚本 (`import_data.py`)
- 支持读取Excel文件（.xlsx格式）
- 自动处理日期类型转换（转为ISO字符串）
- 自动处理空值
- 支持分批批量插入（每批100条）
- 清空已有数据后重新导入

### 实时看板页面 (`index.html`)
- **统计卡片**：显示帖子总数、累计浏览量、平均浏览量、活跃作者数等
- **图表可视化**：
  - 问题分类分布（环形图）
  - 各分类平均浏览量对比（柱状图）
  - 按小时发帖量与平均浏览量（组合图）
  - 情感倾向分布（柱状图）
- **详细数据表格**：显示前20条数据
- **实时更新**：
  - 优先使用Supabase Realtime订阅
  - 失败时自动切换到轮询模式（每5秒刷新）
- **手动刷新按钮**：可手动刷新数据
- **响应式布局**：适配PC和移动端

## 验收标准

1. ✅ 运行导入脚本后，Supabase表中出现与Excel完全一致的数据
2. ✅ 打开HTML页面，能立即看到数据库中的全部数据
3. ✅ 通过Supabase仪表盘修改数据后，页面自动更新（Realtime模式<1秒，轮询模式<5秒）
4. ✅ 图表和统计卡片根据当前数据动态变化
5. ✅ 界面美观，与常见数据看板风格一致

## 注意事项

1. 确保Supabase数据库已创建，并且已启用Realtime功能（在Supabase控制台的Realtime设置中开启）
2. 如果Excel数据量很大（>10万行），建议修改 `import_data.py` 中的 `batch_size` 参数
3. 如果遇到连接问题，请检查网络连接和Supabase配置信息是否正确

## 技术栈

- **后端脚本**: Python + pandas + openpyxl + supabase-py
- **前端页面**: HTML + CSS + JavaScript
- **图表库**: Chart.js (CDN)
- **数据库**: Supabase (PostgreSQL)

## 联系方式

如有问题，请联系项目维护者。