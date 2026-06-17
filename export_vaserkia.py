#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Vaserkia的详细点歌记录CSV文件
"""

import json
import csv

# 读取数据
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取Vaserkia的所有记录
vaserkia_records = [r for r in data['raw_data'] if r['audience'] == 'Vaserkia']

print(f"Vaserkia的总记录数: {len(vaserkia_records)}")

# 生成CSV文件
with open('vaserkia_records.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['序号', '日期', '歌曲名'])
    for i, record in enumerate(vaserkia_records, 1):
        writer.writerow([i, record['date'], record['song']])

print(f"✅ 已生成 vaserkia_records.csv")
print(f"  - 共 {len(vaserkia_records)} 条记录")
print(f"  - 请用Excel打开此文件，对比你的统计")
