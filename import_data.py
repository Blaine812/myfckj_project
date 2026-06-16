import pandas as pd
import json
from supabase import create_client, Client
from datetime import datetime

# Supabase配置 - 用户需要根据实际情况修改
SUPABASE_URL = "https://gvdlqqtdtdqdahzfvjra.supabase.co"
SUPABASE_KEY = "YOUR_SERVICE_ROLE_KEY_HERE"  # 请替换为你的Supabase service role key

# Excel文件路径
EXCEL_FILE_PATH = r"C:\Users\Lenovo\Desktop\影刀.xlsx"

def read_excel_data(file_path):
    """读取Excel文件并返回数据列表和列信息"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"成功读取Excel文件，共 {len(df)} 行数据")
        
        # 过滤掉Unnamed列
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        print(f"过滤后列名: {df.columns.tolist()}")
        
        # 获取列的数据类型信息
        column_info = []
        for col in df.columns:
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                sample_value = non_null_values.iloc[0]
                if isinstance(sample_value, (int, float)):
                    col_type = 'numeric'
                elif isinstance(sample_value, pd.Timestamp):
                    col_type = 'timestamp'
                else:
                    col_type = 'text'
            else:
                col_type = 'text'
            column_info.append({'name': col, 'type': col_type})
        
        # 处理数据类型转换
        data = []
        for _, row in df.iterrows():
            row_dict = {}
            for col in df.columns:
                value = row[col]
                
                if isinstance(value, pd.Timestamp):
                    row_dict[col] = value.isoformat()
                elif pd.isna(value) or value == '':
                    row_dict[col] = None
                elif isinstance(value, (int, float)):
                    row_dict[col] = value
                else:
                    row_dict[col] = str(value)
            data.append(row_dict)
        
        print(f"数据处理完成，转换为 {len(data)} 条记录")
        return data, column_info, df.columns.tolist()
    
    except Exception as e:
        print(f"读取Excel文件失败: {str(e)}")
        return None, None, None

def connect_supabase(url, key):
    """连接Supabase"""
    try:
        supabase: Client = create_client(url, key)
        print("成功连接Supabase")
        return supabase
    except Exception as e:
        print(f"连接Supabase失败: {str(e)}")
        return None

def get_table_name_from_excel(file_path):
    """从Excel文件名获取表名（去除扩展名）"""
    import os
    file_name = os.path.basename(file_path)
    table_name = os.path.splitext(file_name)[0]
    return table_name

def generate_create_table_sql(table_name, column_info):
    """生成创建表的SQL语句"""
    columns_sql = []
    columns_sql.append("id SERIAL PRIMARY KEY")
    
    for col in column_info:
        col_name = col['name']
        col_type = col['type']
        
        escaped_name = f'"{col_name}"'
        
        if col_type == 'numeric':
            pg_type = 'numeric'
        elif col_type == 'timestamp':
            pg_type = 'timestamp with time zone'
        else:
            pg_type = 'text'
        
        columns_sql.append(f'{escaped_name} {pg_type}')
    
    create_sql = f'''CREATE TABLE "{table_name}" (
    {",\n    ".join(columns_sql)}
);'''
    
    return create_sql

def reset_sequence(supabase, table_name):
    """重置表的自增序列，让ID从1开始"""
    try:
        # 使用RPC执行SQL来重置序列
        result = supabase.rpc('execute_sql', {
            'sql': f"ALTER SEQUENCE \"{table_name}_id_seq\" RESTART WITH 1"
        }).execute()
        print(f"序列 {table_name}_id_seq 已重置")
        return True
    except Exception as e:
        print(f"使用RPC重置序列失败: {str(e)}")
        # 尝试使用DELETE后自动重置的替代方法
        return False

def insert_data_to_supabase(supabase, table_name, data, excel_columns):
    """批量插入数据到Supabase"""
    if not data:
        print("没有数据需要插入")
        return 0
    
    try:
        print(f"正在清空表 {table_name} 中的数据...")
        try:
            supabase.table(table_name).delete().neq('id', 0).execute()
            print("表数据已清空")
        except Exception as e:
            print(f"清空表失败: {str(e)}")
        
        print(f"正在重置ID序列...")
        reset_sequence(supabase, table_name)
        
        print(f"正在插入 {len(data)} 条数据...")
        print(f"要插入的列: {excel_columns}")
        
        batch_size = 100
        success_count = 0
        fail_count = 0
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            try:
                response = supabase.table(table_name).insert(batch).execute()
                if response.data:
                    success_count += len(response.data)
                else:
                    fail_count += len(batch)
                print(f"已插入 {i+len(batch)}/{len(data)} 条数据")
            except Exception as e:
                print(f"批量插入失败: {str(e)}")
                fail_count += len(batch)
        
        print(f"\n数据插入完成!")
        print(f"成功: {success_count} 条")
        print(f"失败: {fail_count} 条")
        
        return success_count
    
    except Exception as e:
        print(f"插入数据失败: {str(e)}")
        return 0

def main():
    print("=" * 60)
    print("Excel数据导入Supabase工具")
    print("=" * 60)
    
    if not SUPABASE_KEY or SUPABASE_KEY == "YOUR_ANON_KEY":
        print("错误: 请先配置SUPABASE_KEY")
        return
    
    data, column_info, excel_columns = read_excel_data(EXCEL_FILE_PATH)
    if not data or not column_info:
        return
    
    table_name = get_table_name_from_excel(EXCEL_FILE_PATH)
    print(f"\n表名: {table_name}")
    
    supabase = connect_supabase(SUPABASE_URL, SUPABASE_KEY)
    if not supabase:
        return
    
    print("\n开始插入数据...")
    success_count = insert_data_to_supabase(supabase, table_name, data, excel_columns)
    
    print("\n" + "=" * 60)
    if success_count > 0:
        print(f"成功导入 {success_count} 条数据到表 {table_name}")
    else:
        print("数据导入失败")
    print("=" * 60)

if __name__ == "__main__":
    main()