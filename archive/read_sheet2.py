import pandas as pd
import json

# 读取Excel文件的第二个工作表
file_path = r"C:/Users/Tsing/Downloads/岁己数据统计.xlsx"

# 读取第二个工作表（索引为1）
df = pd.read_excel(file_path, sheet_name=1)

print("工作表名: 岁己今天唱什么")
print("\n数据形状:", df.shape)
print("\n前20行数据:")
print(df.head(20).to_string())

print("\n\n列名:")
for i, col in enumerate(df.columns):
    print(f"  列{i} ({chr(65+i)}列): {col}")

# 检查哪列有日期、歌曲、观众信息
print("\n\n检查各列数据类型和内容示例:")
for i, col in enumerate(df.columns[:10]):
    print(f"\n列{i} ({chr(65+i)}): {col}")
    non_null = df[col].dropna()
    if len(non_null) > 0:
        print(f"  前5个值: {non_null.head(5).tolist()}")
        if len(non_null) > 5:
            print(f"  ...")
