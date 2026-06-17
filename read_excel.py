import pandas as pd
import json

# 读取Excel文件的第三个工作表
file_path = r"C:/Users/Tsing/Downloads/岁己数据统计.xlsx"

# 读取所有工作表名称
xl_file = pd.ExcelFile(file_path)
print("工作表名称:", xl_file.sheet_names)

# 读取第三个工作表（索引为2）
df = pd.read_excel(file_path, sheet_name=2)  # 索引2表示第三个工作表

print("\n数据形状:", df.shape)
print("\n列名:")
for i, col in enumerate(df.columns):
    print(f"  列{i}: {col}")

print("\n前10行数据:")
print(df.head(10).to_string())

print("\n数据类型:")
print(df.dtypes)

# 检查空值
print("\n空值统计:")
print(df.isnull().sum())

# 保存为JSON以便后续处理
data = []
for idx, row in df.iterrows():
    record = {}
    for col in df.columns[:5]:  # 只取前5列（A-E列）
        record[str(col)] = str(row[col]) if pd.notna(row[col]) else None
    data.append(record)

# 保存到文件
with open('song_data_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到 song_data_raw.json")
print(f"总记录数: {len(data)}")
