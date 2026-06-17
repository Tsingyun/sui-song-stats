#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Vaserkia的详细点歌记录CSV文件（使用openpyxl处理后的数据）
"""

import json
import csv

# 读取数据
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取Vaserkia的所有记录
vaserkia_records = [r for r in data['raw_data'] if r['audience'] == 'Vaserkia']

print(f"Vaserkia的总记录数: {len(vaserkia_records)}")
print(f"\n生成详细CSV文件...")

# 生成CSV文件
with open('vaserkia_detailed.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['序号', '日期', '歌曲名', '月份', '季度', '年度'])
    for i, record in enumerate(vaserkia_records, 1):
        writer.writerow([i, record['date'], record['song'], record['month'], record['quarter'], record['year']])

print(f"✅ 已生成 vaserkia_detailed.csv")
print(f"  - 共 {len(vaserkia_records)} 条记录")
print(f"  - 请用Excel打开此文件，对比你的统计")
print(f"\n前10条记录:")
for i, r in enumerate(vaserkia_records[:10], 1):
    print(f"  {i}. {r['date']} - {r['song']}")
print(f"\n后10条记录:")
for i, r in enumerate(vaserkia_records[-10:], len(vaserkia_records)-9):
    print(f"  {i}. {r['date']} - {r['song']}")
